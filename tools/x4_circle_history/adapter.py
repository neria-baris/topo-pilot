"""Restricted, read-only E4 adapter (API.md adapter.py).

Loads ONLY through the injected `ArtifactStore.load(cls, id, consumer="analysis")`. That call
checks the access policy, completeness and canonical checksum, then runs `validate()`. Scored
panels (outside {1, 2}) are refused BEFORE any load unless a scoring release is supplied. Token
column 32 (w33) is never returned. No module-level I/O.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from errors import AccessDenied, JoinError
from scores import history_digests

ALLOWED_PANELS = frozenset({1, 2})


@dataclass(frozen=True)
class E4Manifest:
    per_model: dict
    hook: str = "resid_post_3"
    end: int = 32
    panel_size: int = 512
    n_panels: int = 8


def _contracts():
    from topo_pilot.contracts import ActivationSet, HistoryIndex, ObservationSet, tokens_hash

    return ActivationSet, HistoryIndex, ObservationSet, tokens_hash


class RestrictedE4Adapter:
    """Panels 1-2 only by default; lineage verified before any array is returned."""

    def __init__(self, store, manifest: E4Manifest, *, scoring_release=None) -> None:
        self._store = store
        self._manifest = manifest
        self._scoring_release = scoring_release

    def _ids(self, model):
        try:
            return self._manifest.per_model[model]
        except KeyError as exc:
            raise JoinError(f"model {model!r} not in manifest") from exc

    def _load(self, model):
        ActivationSet, HistoryIndex, ObservationSet, tokens_hash = _contracts()
        ids = self._ids(model)
        obs = self._store.load(ObservationSet, ids["ObservationSet"], consumer="analysis")
        hist = self._store.load(HistoryIndex, ids["HistoryIndex"], consumer="analysis")
        acts = self._store.load(ActivationSet, ids["ActivationSet"], consumer="analysis")
        return obs, hist, acts, tokens_hash

    def _verify(self, model, obs, hist, acts, tokens_hash) -> dict:
        m, ids = self._manifest, self._ids(model)
        a_parents = set(self._store.meta(ids["ActivationSet"]).parent_ids)
        h_parents = set(self._store.meta(ids["HistoryIndex"]).parent_ids)
        checks = {
            "activation_parents": {ids["ObservationSet"], ids["HistoryIndex"], ids["checkpoint"]}
            <= a_parents,
            "history_parent": ids["ObservationSet"] in h_parents,
            "source_model": acts.source == "model",
            "checkpoint_id": acts.checkpoint_id == ids["checkpoint"],
            "hook_present": m.hook in tuple(acts.hooks),
            "dataset_id": hist.dataset_id == ids["ObservationSet"],
            "split_test": obs.split == "test",
            "end_all": bool(np.all(np.asarray(hist.end) == m.end)),
            "panel_layout": (int(hist.panel_size), int(hist.n_panels))
            == (m.panel_size, m.n_panels),
            "history_order": np.array_equal(
                np.asarray(acts.history_id).astype(str), np.asarray(hist.history_id).astype(str)
            ),
        }
        row_of = {int(s): r for r, s in enumerate(np.asarray(obs.sequence_id))}
        try:
            rows = np.array([row_of[int(s)] for s in np.asarray(hist.sequence_id)], dtype=np.int64)
        except KeyError as exc:
            raise JoinError(
                f"model {model}: history sequence_id {exc} absent from observations"
            ) from exc
        recomputed = [tokens_hash(obs.tokens[r, : m.end]) for r in rows]
        checks["tokens_hash"] = recomputed == [str(h) for h in np.asarray(hist.tokens_hash)]
        failed = [k for k, ok in checks.items() if not ok]
        if failed:
            raise JoinError(f"model {model}: lineage checks failed {failed}")
        return {"checks": checks, "rows": rows, "hook_index": tuple(acts.hooks).index(m.hook)}

    def lineage(self, model) -> dict:
        obs, hist, acts, th = self._load(model)
        return self._verify(model, obs, hist, acts, th)["checks"]

    def panels(self, model, panels=(1, 2)) -> dict:
        requested = {int(p) for p in panels}
        if not requested <= ALLOWED_PANELS and self._scoring_release is None:
            raise AccessDenied(
                f"panels {sorted(requested - ALLOWED_PANELS)} need a scoring release"
            )
        obs, hist, acts, th = self._load(model)
        info = self._verify(model, obs, hist, acts, th)
        panel = np.asarray(hist.panel)
        out = {}
        for p in sorted(requested):
            sel = np.flatnonzero(panel == p)
            order = sel[np.argsort(np.asarray(hist.history_id)[sel].astype(str), kind="stable")]
            out[p] = {
                "history_id": np.asarray(hist.history_id)[order].astype(str),
                "sequence_id": np.asarray(hist.sequence_id)[order].astype(np.int64),
                "named32": np.asarray(obs.tokens)[info["rows"][order], : self._manifest.end].copy(),
                "activation": np.asarray(acts.A)[order, info["hook_index"], :].astype(np.float64),
            }
        return out

    def join_keys(self, model, symbol_perm) -> dict:
        """Identity-only join material for ALL panels: sequence_id, panel and canonical digest.

        No token, activation or score arrays leave this method. It is used only for the
        cross-model pairing check, which the contract permits on scored panels.
        """
        from scores import canonical_from_named

        obs, hist, acts, th = self._load(model)
        info = self._verify(model, obs, hist, acts, th)
        named = np.asarray(obs.tokens)[info["rows"], : self._manifest.end]
        canonical = canonical_from_named(named, symbol_perm)
        return {
            "sequence_id": np.asarray(hist.sequence_id).astype(np.int64),
            "panel": np.asarray(hist.panel).astype(np.int64),
            "digest": history_digests(canonical),
        }

    def identity_report(self) -> dict:
        """All lineage/join checks for every model and panel; counts/booleans/digests only."""
        report = {}
        for model in self._manifest.per_model:
            obs, hist, acts, th = self._load(model)
            info = self._verify(model, obs, hist, acts, th)
            panel = np.asarray(hist.panel)
            report[str(model)] = {
                "checks": {k: bool(v) for k, v in info["checks"].items()},
                "rows": int(len(info["rows"])),
                "panel_counts": {int(p): int(np.sum(panel == p)) for p in np.unique(panel)},
                "history_digest_of_digests": _digest_of(np.asarray(hist.tokens_hash).astype(str)),
            }
        return report


def _digest_of(values) -> str:
    import hashlib

    return hashlib.sha256("\n".join(map(str, values)).encode("utf-8")).hexdigest()


def cross_model_join(per_model: dict) -> dict:
    """Pair rows across models by sequence_id with identical canonical digests; no fallback."""
    if not per_model:
        raise JoinError("no models to join")
    keyed = {}
    for model, d in per_model.items():
        seq = np.asarray(d["sequence_id"], dtype=np.int64)
        panel = np.asarray(d["panel"], dtype=np.int64)
        digests = list(d["digest"]) if "digest" in d else history_digests(d["canonical32"])
        if (
            len(set(seq.tolist())) != len(seq)
            or panel.shape != seq.shape
            or len(digests) != len(seq)
        ):
            raise JoinError(f"model {model}: duplicate or misaligned sequence ids")
        keyed[model] = {int(s): (int(p), dg) for s, p, dg in zip(seq, panel, digests)}
    reference = next(iter(keyed.values()))
    for model, mapping in keyed.items():
        if mapping != reference:
            raise JoinError(f"model {model}: sequence/panel/canonical-history mismatch")
    common = np.array(sorted(reference), dtype=np.int64)
    order = {
        model: np.argsort(np.asarray(d["sequence_id"], dtype=np.int64), kind="stable")
        for model, d in per_model.items()
    }
    return {"order": order, "sequence_id": common}

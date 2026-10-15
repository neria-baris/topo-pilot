"""C1' exposure registry v1: per-source readers for the frozen c1_data.build_registry (job 0027;
protocol §2.4 sources a-c, §16 row 2). Kept outside tools/c1prime so the job-0026 frozen
file set is unchanged. Identity-only: token arrays and identity columns (sequence
id, history id) are read; no scored diagnostic, activation or endpoint is decoded.

Usage (venv, through a store-local binding of the frozen c1_meter_bind):
  python c1_registry_sources.py <out_dir>   -> registry_v1.json + REGISTRY_MANIFEST_v1.json
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "c1prime"))
import c1_config  # noqa: E402,F401  (frozen; sets the K4/0014 sys.path)
import c1_data  # noqa: E402  (frozen build_registry)

ROOT = Path(r"X:\Downloads\projects\topo-pilot")
ART = ROOT / "topo-pilot" / "artifacts"
EMPTY = np.zeros((0, 32), dtype=np.uint8)


def sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical32(named, perm) -> np.ndarray:
    """canonical = argsort(perm)[named] (K4 CONTRACT symbols), first 32 tokens."""
    named, perm = np.asarray(named, dtype=np.int64), np.asarray(perm, dtype=np.int64)
    if sorted(perm.tolist()) != list(range(len(perm))) or named.size and named.max() >= len(perm):
        raise ValueError("symbol_perm is not a permutation covering the tokens")
    return np.argsort(perm, kind="stable")[named[:, :32]].astype(np.uint8)


def _store():
    from topo_pilot.contracts import ArtifactStore
    from topo_pilot.contracts.backends import LocalFSBackend

    return ArtifactStore(LocalFSBackend(ART))


def observation_set_sources(store=None, root=ART) -> tuple:
    """Source (a): every ObservationSet, canonicalised with its own EmissionSpec perm."""
    from topo_pilot.contracts import EmissionSpec, ObservationSet

    store = store or _store()
    sources, seqs = [], {}
    for d in sorted(p for p in (Path(root) / "ObservationSet").iterdir() if p.is_dir()):
        meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
        em = [p for p in meta["parent_ids"] if (Path(root) / "EmissionSpec" / p).is_dir()]

        def reader(path, oid=d.name, em=tuple(em)):
            obs = store.load(ObservationSet, oid, consumer="analysis")
            spec = store.load(EmissionSpec, em[0], consumer="analysis")
            seqs[oid] = np.asarray(obs.sequence_id, dtype=np.int64)
            return canonical32(obs.tokens, spec.symbol_perm)

        sources.append({"name": f"a:ObservationSet/{d.name}", "path": d / "payload.npz",
                        "reader": reader,
                        "meta": {"source": "a", "split": meta["config"].get("split"),
                                 "config": meta["config"], "emission_spec": em,
                                 "meta_sha256": sha(d / "meta.json"),
                                 "canonicalisation": "argsort(EmissionSpec.symbol_perm)[named]"
                                 "[:, :32]"}})
    return sources, seqs


def _npz_tokens(key, cols=32):
    def reader(path):
        with np.load(path, allow_pickle=False) as z:
            return np.asarray(z[key])[:, :cols].astype(np.uint8)
    return reader


def _empty(reason):
    def reader(path):
        return EMPTY
    return reader, reason


def store_sources(root=ROOT) -> list:
    """Source (b): the stores named in §2.4(b), each recorded explicitly (empty ones included)."""
    out = []

    def add(name, path, reader, meta):
        out.append({"name": name, "path": Path(path), "reader": reader, "meta": meta})

    for kind in ("reference", "repetition1", "repetition2", "repetition3"):
        add(f"b:X4-B2/{kind}", root / "x4b2-research-store/exports" / f"pool_{kind}_tokens.npz",
            _npz_tokens("canonical_tokens"), {"source": "b", "store": "x4b2-research-store",
                                              "tokens": "canonical_tokens[:, :32]"})
    for split in ("calibration", "validation"):
        add(f"b:X4/x4-history-feas/{split}", root / "x4-history-feas-store" / f"{split}.npz",
            _npz_tokens("tokens"), {"source": "b", "store": "x4-history-feas-store",
                                    "tokens": "canonical (sampled with canonical E)"})
    k4 = root / "x4-circle-history-feas-store-0015"
    for m in (1729, 2718, 3141):
        for part in ("calibration", "validation"):
            add(f"b:K4-0015/oracle_{m}/{part}", k4 / f"oracle_{m}.npz",
                _npz_tokens(f"{part}_canonical32"), {"source": "b", "store": k4.name,
                                                     "jobs": "0015/0016/0018"})
    add("b:K4-0015/REFERENCE_CACHE K=32", k4 / "REFERENCE_CACHE.json", reference_cache_reader,
        {"source": "b", "store": k4.name, "note": "K < 32 entries are suffixes, not 32-symbol "
         "histories; only K = 32 entries are histories"})
    empties = {
        "b:X4/x4b-research-store": (root / "x4b-research-store/exports/pool_test.npz",
                                    "no stored tokens: canonical_ids reference E4 test/dev "
                                    "ObservationSets of source (a) (coverage-checked)"),
        "b:job-0014/x4-oracle-profile-store-0014":
            (root / "x4-oracle-profile-store-0014/profile/rows_calibration.npz",
             "no stored tokens: ids reference x4-history-feas histories (coverage-checked)"),
        "b:X4-F/x4f-gates-research-store": (root / "x4f-gates-research-store/exports/"
                                            "x4f_gates_1729.npz", "no stored tokens or donor "
                                            "prefixes: history_id references E4 HistoryIndex "
                                            "(coverage-checked)"),
        "b:d1-seam-oracle-store": (root / "d1-seam-oracle-store/run_0020/report.json",
                                   "no stored 32-symbol histories: D-1 histories were exactly "
                                   "enumerated over a 5-symbol alphabet (different process)"),
        "b:chart-diag-store-0023": (root / "chart-diag-store-0023/DIAG.json",
                                    "no stored tokens: history ids of E4 panels 1-2 "
                                    "(coverage-checked)"),
        "b:x2a-stage0-oracle-store": (root / "x2a-stage0-oracle-store/report.json",
                                      "no stored histories: model arrays, PH diagrams and "
                                      "summaries only (T^2 disjoint-union process)"),
    }
    for name, (path, reason) in empties.items():
        reader, why = _empty(reason)
        add(name, path, reader, {"source": "b", "contributes": "none", "reason": why})
    return out


def reference_cache_reader(path) -> np.ndarray:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = [e["history"] for e in data["entries"] if int(e.get("K", 0)) == 32]
    toks = [[int(h[i:i + 16], 16) for i in range(0, len(h), 16)] for h in rows]
    return np.asarray(toks, dtype=np.int64).astype(np.uint8) if toks else EMPTY


def _token_lists(obj, found):
    if isinstance(obj, list):
        if len(obj) in (32, 33) and all(isinstance(v, int) and 0 <= v < 256 for v in obj):
            found.append(obj[:32])
        else:
            for v in obj:
                _token_lists(v, found)
    elif isinstance(obj, dict):
        for v in obj.values():
            _token_lists(v, found)


def handoff_sources(root=ROOT / "agent-handoff") -> list:
    """Source (c): every JSON under agent-handoff (excluding .git and CLI logs) scanned for
    32- or 33-element integer lists in 0..255 (candidate recorded histories)."""
    out = []
    for p in sorted(Path(root).rglob("*.json")):
        if ".git" in p.parts:
            continue

        def reader(path):
            found = []
            try:
                _token_lists(json.loads(Path(path).read_text(encoding="utf-8-sig")), found)
            except ValueError:
                return EMPTY
            return np.asarray(found, dtype=np.uint8) if found else EMPTY

        out.append({"name": f"c:{p.relative_to(root).as_posix()}", "path": p, "reader": reader,
                    "meta": {"source": "c", "scan": "integer lists of length 32/33 in 0..255"}})
    return out


def history_index_ids(store=None, root=ART) -> dict:
    """history_id -> sequence_id over every HistoryIndex (identity columns only)."""
    from topo_pilot.contracts import HistoryIndex

    store = store or _store()
    ids = {}
    for d in sorted(p for p in (Path(root) / "HistoryIndex").iterdir() if p.is_dir()):
        h = store.load(HistoryIndex, d.name, consumer="analysis")
        ids.update(zip(np.asarray(h.history_id).astype(str).tolist(),
                       np.asarray(h.sequence_id, dtype=np.int64).tolist()))
    return ids


def coverage(seqs_a: dict, hist_ids: dict, root=ROOT) -> dict:
    """Id-only stores reference only histories of source (a) (or of a scanned store)."""
    seq_a = set(np.concatenate(list(seqs_a.values())).tolist()) if seqs_a else set()
    rep = {}
    x4b = []
    for f in sorted((root / "x4b-research-store/exports").glob("pool_*.npz")):
        with np.load(f, allow_pickle=False) as z:
            x4b += [int(c.split("|")[1]) for c in z["canonical_ids"].tolist()]
    rep["x4b_seq_in_a"] = {"n": len(x4b), "missing": len(set(x4b) - seq_a)}
    x4f = []
    for f in sorted((root / "x4f-gates-research-store/exports").glob("x4f_gates_*.npz")):
        with np.load(f, allow_pickle=False) as z:
            x4f += z["history_id"].astype(str).tolist()
    rep["x4f_ids_in_history_index"] = {"n": len(x4f), "missing": len(set(x4f) - set(hist_ids))}
    rep["x4f_seq_in_a"] = {"missing": len({hist_ids[h] for h in x4f if h in hist_ids} - seq_a)}
    diag = json.loads((root / "chart-diag-store-0023/DIAG.json").read_text(encoding="utf-8"))
    dids = [o["history_id"] for c in diag["cases"].values() for o in c["outside_giant"]]
    rep["chart_diag_ids_in_history_index"] = {"n": len(dids),
                                              "missing": len(set(dids) - set(hist_ids))}
    hf = set()
    for split in ("calibration", "validation"):
        with np.load(root / "x4-history-feas-store" / f"{split}.npz", allow_pickle=False) as z:
            hf |= set(z["ids"].astype(str).tolist())
    j14 = set()
    for f in sorted((root / "x4-oracle-profile-store-0014/profile").glob("rows_*.npz")):
        with np.load(f, allow_pickle=False) as z:
            j14 |= set(z["ids"].astype(str).tolist())
    rep["job0014_ids_in_x4hf"] = {"n": len(j14), "missing": len(j14 - hf)}
    rep["complete"] = all(v.get("missing", 0) == 0 for v in rep.values() if isinstance(v, dict))
    return rep


def build(out_dir) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    store = _store()
    a_sources, seqs = observation_set_sources(store)
    sources = a_sources + store_sources() + handoff_sources()
    reg = c1_data.build_registry(sources)
    hist = history_index_ids(store)
    cov = coverage(seqs, hist)
    extra_seq = set()
    for s in ("reference", "repetition1", "repetition2", "repetition3"):
        with np.load(ROOT / "x4b2-research-store/exports" / f"pool_{s}_tokens.npz") as z:
            extra_seq |= set(z["sequence_id"].astype(np.int64).tolist())
    seq_all = sorted(set(np.concatenate(list(seqs.values())).tolist()) | extra_seq)
    by_source = {}
    for e in reg["entries"]:
        by_source.setdefault(e["meta"]["source"], 0)
        by_source[e["meta"]["source"]] += e["contributes"]
    registry = {"schema": "c1prime-registry-v1", "protocol_sha256": c1_config.CONTRACT[
        "protocol_sha256"], "version": 1, "sources": "a-c (§2.4)", "status": reg["status"],
        "n_digests": reg["n_digests"], "union_sha256": reg["union_sha256"],
        "digests": reg["digests"], "sequence_ids": seq_all, "coverage": cov}
    with (out / "registry_v1.json").open("x", encoding="utf-8") as f:
        f.write(json.dumps(registry))
    manifest = {"entries": reg["entries"], "missing": reg["missing"], "coverage": cov,
                "contributions_by_source": by_source, "n_digests": reg["n_digests"],
                "union_sha256": reg["union_sha256"], "n_sequence_ids": len(seq_all),
                "registry_v1_sha256": sha(out / "registry_v1.json")}
    with (out / "REGISTRY_MANIFEST_v1.json").open("x", encoding="utf-8") as f:
        f.write(json.dumps(manifest, indent=1, default=str))
    return manifest


if __name__ == "__main__":
    m = build(Path(sys.argv[1]))
    print(json.dumps({k: m[k] for k in ("n_digests", "n_sequence_ids", "contributions_by_source",
                                        "registry_v1_sha256")}, default=str))
    print(json.dumps(m["coverage"]))
    print("missing", json.dumps(m["missing"])[:2000])

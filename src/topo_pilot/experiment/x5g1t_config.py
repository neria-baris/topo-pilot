"""X5 G1 study configuration (x5g1-train-v4 §10; API v4 §3): an exact-key ``StudyConfig``, the
frozen ``PRODUCTION`` values and a READ-ONLY validator that every stage runs before any sampler,
model or output. A distinct ``synthetic-fixture`` mode serves tiny tests and can never pass as
production. Unknown, missing, mistyped or tampered values fail closed with ``ConfigInvalid``.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import os
import re
from pathlib import Path

from topo_pilot.analysis import X5_GRID
from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    LocalFSBackend,
    TransitionSpec,
    WorldSpec,
)

from .x4b import ReadThroughBackend
from .x5g1_safety import verify_sources_full
from .x5g1t_checks import canonical
from .x5g1t_lineage import ARMS, CODES, NAMESPACE, stream
from .x5g1t_train import study_train_config

MODES = ("production", "synthetic-fixture")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class ConfigInvalid(RuntimeError):
    """The study configuration is malformed, tampered or unsafe; nothing was computed."""


_NUM = (int, float)
_TYPES = {"mode": str, "protocol": str, "protocol_doc": str, "protocol_doc_sha256": str,
          "read_roots": list, "study_root": str, "ledger_path": str, "mailbox": str,
          "sources": dict, "source_producers": dict, "stored_checkpoint": (list, type(None)),
          "masters": list, "sizes": dict, "model_config": dict, "steps": int, "grid": list,
          "gc": dict, "threads": int, "bootstrap_draws": int, "cap_s": _NUM,
          "cumulative_cap_s": _NUM, "check_stored_ids": bool, "env": dict}


@dataclasses.dataclass(frozen=True)
class StudyConfig:
    mode: str
    protocol: str
    protocol_doc: str
    protocol_doc_sha256: str
    read_roots: list
    study_root: str
    ledger_path: str
    mailbox: str
    sources: dict
    source_producers: dict
    stored_checkpoint: list | None
    masters: list
    sizes: dict
    model_config: dict
    steps: int
    grid: list
    gc: dict
    threads: int
    bootstrap_draws: int
    cap_s: float
    cumulative_cap_s: float
    check_stored_ids: bool
    env: dict

    @classmethod
    def from_dict(cls, d) -> StudyConfig:
        if not isinstance(d, dict):
            raise ConfigInvalid(f"config must be a JSON object, got {type(d).__name__}")
        keys = set(_TYPES)
        if set(d) != keys:
            raise ConfigInvalid(f"config keys: missing {sorted(keys - set(d))}, "
                                f"unknown {sorted(set(d) - keys)}")
        for k, t in _TYPES.items():
            v = d[k]
            if not isinstance(v, t) or (isinstance(v, bool) and t is not bool):
                raise ConfigInvalid(f"config {k!r} has type {type(v).__name__}")
        if d["mode"] not in MODES:
            raise ConfigInvalid(f"config mode {d['mode']!r} not in {MODES}")
        for k in ("cap_s", "cumulative_cap_s"):
            if not math.isfinite(d[k]):
                raise ConfigInvalid(f"config {k!r} is not finite")
        _check_shapes(d)
        return cls(**d)

    @property
    def root(self) -> Path:
        return Path(self.study_root)

    def expected_sources(self) -> dict:
        """``{id: (cls, sha)}`` for the world, both transition kernels and the emission."""
        s = self.sources
        exp = {s["world"][0]: (WorldSpec, s["world"][1])}
        exp.update({aid: (TransitionSpec, sha) for aid, sha in s["T"].values()})
        exp[s["E"][0]] = (EmissionSpec, s["E"][1])
        return exp


def _pair(v, what: str) -> None:
    if not (isinstance(v, list) and len(v) == 2 and isinstance(v[0], str) and v[0]
            and isinstance(v[1], str) and _HEX64.match(v[1])):
        raise ConfigInvalid(f"{what} must be [id, 64-hex sha], got {v!r}")


def _check_shapes(d: dict) -> None:
    s = d["sources"]
    if set(s) != {"world", "T", "E"} or not isinstance(s["T"], dict) or set(s["T"]) != set(ARMS):
        raise ConfigInvalid(f"sources must be {{world, T: {{{', '.join(ARMS)}}}, E}}")
    _pair(s["world"], "sources.world")
    _pair(s["E"], "sources.E")
    for arm in ARMS:
        _pair(s["T"][arm], f"sources.T.{arm}")
    ids = {s["world"][0], s["E"][0], *(s["T"][a][0] for a in ARMS)}
    if set(d["source_producers"]) != ids or not all(
            isinstance(v, str) for v in d["source_producers"].values()):
        raise ConfigInvalid("source_producers must map exactly the world/T/E ids to strings")
    if d["stored_checkpoint"] is not None:
        _pair(d["stored_checkpoint"], "stored_checkpoint")
    if not _HEX64.match(d["protocol_doc_sha256"]):
        raise ConfigInvalid("protocol_doc_sha256 must be 64 lower-case hex")
    if set(d["sizes"]) != {"train", "dev", "test"} or not all(
            isinstance(v, int) and not isinstance(v, bool) for v in d["sizes"].values()):
        raise ConfigInvalid("sizes must be {train, dev, test} ints")
    if set(d["gc"]) != set(ARMS) or not all(
            isinstance(v, _NUM) and not isinstance(v, bool) for v in d["gc"].values()):
        raise ConfigInvalid("gc must be {a0, a020} numbers")
    if not all(isinstance(r, str) for r in d["read_roots"]) or not d["read_roots"]:
        raise ConfigInvalid("read_roots must be a non-empty list of strings")
    if not all(isinstance(t, int) and not isinstance(t, bool) for t in d["grid"]):
        raise ConfigInvalid("grid must be a list of ints")
    if not all(isinstance(k, str) and isinstance(v, str) for k, v in d["env"].items()):
        raise ConfigInvalid("env must map strings to strings")


def load_config(path: Path) -> StudyConfig:
    try:
        d = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise ConfigInvalid(f"config {path}: {type(exc).__name__}: {exc}") from exc
    return StudyConfig.from_dict(d)


@dataclasses.dataclass(frozen=True)
class ProductionSpec:
    protocol: str
    protocol_doc: str
    protocol_doc_sha256: str
    read_roots: tuple[str, ...]
    study_root: str
    ledger_path: str
    mailbox: str
    sources: dict
    source_producers: dict
    stored_checkpoint: tuple[str, str]
    stored_model_config: dict
    stored_train_config: dict
    masters: tuple
    sizes: dict
    steps: int
    grid: tuple[int, ...]
    gc: dict
    threads: int
    bootstrap_draws: int
    cap_s: float
    cumulative_cap_s: float
    check_stored_ids: bool
    env: dict
    lineage: dict


def current_lineage() -> dict:
    return {"namespace": NAMESPACE, "codes": dict(CODES), "stream_tail": stream("train")[2:]}


_TOP = r"X:\Downloads\projects\topo-pilot"
PRODUCTION = ProductionSpec(
    protocol="x5g1-train-v4",
    protocol_doc="docs/proposals/X5_G1_TRAINING_PROTOCOL_V4.md",
    protocol_doc_sha256="24270a7372cfc366152f09593ca9a735bbf8b261b262d789e14a9d1d3a0f1838",
    read_roots=(rf"{_TOP}\topo-pilot\artifacts", rf"{_TOP}\x5g1-research-store\store",
                rf"{_TOP}\x4b2-research-store\store"),
    study_root=rf"{_TOP}\x5g1t-research-store",
    ledger_path=rf"{_TOP}\x5g1-research-store\cpu_ledger.json",
    mailbox=rf"{_TOP}\agent-handoff",
    sources={
        "world": ["21feee1d8ee5422e",
                  "b6f0746e46d20d202c1a74220f96357a0a80375d57046ffea69b03f3f354f77f"],
        "T": {"a0": ["e4dafc7b9785c172",
                     "f94340a64769df1c89935c1767a58d2f764b0f31a49e675bd43d8484eeba68dd"],
              "a020": ["08a22a03727d2295",
                       "663d0011c7f9b541a436359c885a9f367dda280b20b594e484ff1492b8686b7b"]},
        "E": ["3633ac27dab50cf4",
              "f5b6197c22e3613f12a29feb9dec2ccd357749928032f4dc844364d6884bb1fb"]},
    source_producers={"21feee1d8ee5422e": "84152ab27e91+dirty",
                      "e4dafc7b9785c172": "84152ab27e91+dirty",
                      "08a22a03727d2295": "64482629c39b",
                      "3633ac27dab50cf4": "84152ab27e91+dirty"},
    stored_checkpoint=("c3358e3cb9c352fb",
                       "bcd024efc2ff30f76940d459dba95a693f536fb7cc3b2441c4ee5145dcf8596b"),
    stored_model_config={"activation": "gelu", "d_mlp": 512, "d_model": 128, "dropout": 0.0,
                         "n_ctx": 33, "n_heads": 4, "n_layers": 4, "tie_embeddings": False,
                         "vocab_in": 37, "vocab_out": 36},
    stored_train_config={  # the stored E3 dict
        "batch_size": 128, "checkpoint_steps": [0, 50, 100, 200, 400, 700, 1000, 1500, 2000,
                                                3000, 4000, 5000], "device": "auto",
        "grad_clip": 1.0, "lr": 0.001, "schedule": "cosine", "steps": 5000, "warmup": 200,
        "weight_decay": 0.1},
    masters=(310001, 310002, 310003), sizes={"train": 131072, "dev": 4096, "test": 4096},
    steps=5000, grid=tuple(int(t) for t in X5_GRID),
    gc={"a0": 0.27133797235249024, "a020": 0.2939268960103646},
    threads=1, bootstrap_draws=2000, cap_s=21600.0, cumulative_cap_s=21600.0,
    check_stored_ids=True,
    env={"OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "OMP_NUM_THREADS": "1"},
    lineage={"namespace": "x5g1-train-v1", "codes": {"train": 9, "dev": 10, "test": 11},
             "stream_tail": ("cylinder", "overlap", "1.25")},
)


def _norm(p) -> str:
    return os.path.normcase(str(Path(p).resolve()))


def _within(path, root) -> bool:
    """``path`` equals ``root`` or lies inside it (resolved, case-normalised)."""
    a, b = _norm(path), _norm(root)
    return a == b or a.startswith(b.rstrip("\\/") + os.sep)


def _fail(what: str) -> ConfigInvalid:
    return ConfigInvalid(f"config check failed: {what}")

def read_chain(roots):
    """Read-through backend chain over ``roots`` (the first is the innermost); writes nothing."""
    backends = [LocalFSBackend(Path(r)) for r in roots]
    ro = backends[0]
    for b in backends[1:]:
        ro = ReadThroughBackend(b, ro)
    return ro


def read_store(roots) -> ArtifactStore:
    return ArtifactStore(read_chain(roots))


def _protocol_doc(cfg: StudyConfig, repo: Path) -> str:
    doc = Path(repo) / cfg.protocol_doc
    try:
        sha = hashlib.sha256(doc.read_bytes()).hexdigest()
    except OSError as exc:
        raise _fail(f"protocol document {doc}: {exc}") from exc
    if sha != cfg.protocol_doc_sha256:
        raise _fail(f"protocol document sha {sha} != config {cfg.protocol_doc_sha256}")
    return sha


def _write_roots(cfg: StudyConfig, repo: Path, spec: ProductionSpec) -> None:
    main_repo = Path(spec.read_roots[0]).parent
    for r in (*cfg.read_roots, repo, main_repo):
        if _within(cfg.study_root, r):
            raise _fail(f"study root {cfg.study_root} is inside protected/read root {r}")
    if _within(cfg.ledger_path, cfg.study_root):
        raise _fail("ledger lies inside the study root")


def _verify_sources(cfg: StudyConfig, store: ArtifactStore) -> dict:
    hashes = {}
    for aid, (cls, sha) in cfg.expected_sources().items():
        try:
            meta = store.meta(aid)
        except Exception as exc:  # noqa: BLE001 - any failure is a refusal
            raise _fail(f"source {aid}: {type(exc).__name__}: {exc}") from exc
        if meta.artifact_type != cls.__name__:
            raise _fail(f"source {aid} is {meta.artifact_type}, expected {cls.__name__}")
        if meta.producer_version != cfg.source_producers[aid]:
            raise _fail(f"source {aid} producer {meta.producer_version} != config")
        hashes[aid] = sha
    bad = verify_sources_full(store, cfg.expected_sources())
    if bad:
        raise _fail("source integrity: " + "; ".join(bad))
    return hashes


def _verify_stored_checkpoint(cfg: StudyConfig, store: ArtifactStore,
                              spec: ProductionSpec) -> None:
    """Metadata only (never weights): model config and E3 train config as stored."""
    cid, sha = cfg.stored_checkpoint
    try:
        meta = store.meta(cid)
    except Exception as exc:  # noqa: BLE001
        raise _fail(f"stored checkpoint {cid}: {type(exc).__name__}: {exc}") from exc
    if meta.artifact_type != "Checkpoint" or meta.payload_sha256 != sha:
        raise _fail(f"stored checkpoint {cid}: type/payload mismatch")
    stored_model = meta.config.get("model_config")
    stored_train = meta.config.get("train_config")
    if canonical(stored_model) != canonical(spec.stored_model_config) \
            or canonical(stored_train) != canonical(spec.stored_train_config):
        raise _fail("stored checkpoint configs differ from the frozen specification")
    if canonical(cfg.model_config) != canonical(stored_model):
        raise _fail("model_config differs from the stored checkpoint")
    allowed = {**stored_train, "checkpoint_steps": list(cfg.grid), "device": "cpu"}
    if canonical(dataclasses.asdict(study_train_config(cfg.steps, cfg.grid))) != canonical(allowed):
        raise _fail("study train config differs from the stored one beyond grid/device")


def _production(cfg: StudyConfig, repo: Path, spec: ProductionSpec) -> dict:
    checks = {"protocol": (cfg.protocol, spec.protocol),
              "protocol_doc": (cfg.protocol_doc, spec.protocol_doc),
              "protocol_doc_sha256": (cfg.protocol_doc_sha256, spec.protocol_doc_sha256),
              "sources": (cfg.sources, spec.sources),
              "source_producers": (cfg.source_producers, spec.source_producers),
              "stored_checkpoint": (cfg.stored_checkpoint, list(spec.stored_checkpoint)),
              "masters": (cfg.masters, list(spec.masters)), "sizes": (cfg.sizes, spec.sizes),
              "steps": (cfg.steps, spec.steps), "grid": (cfg.grid, list(spec.grid)),
              "gc": (cfg.gc, spec.gc), "threads": (cfg.threads, spec.threads),
              "bootstrap_draws": (cfg.bootstrap_draws, spec.bootstrap_draws),
              "cap_s": (float(cfg.cap_s), float(spec.cap_s)),
              "cumulative_cap_s": (float(cfg.cumulative_cap_s), float(spec.cumulative_cap_s)),
              "check_stored_ids": (cfg.check_stored_ids, spec.check_stored_ids),
              "env": (cfg.env, spec.env), "lineage": (current_lineage(), spec.lineage)}
    for k, (got, want) in checks.items():
        if canonical(got) != canonical(want):
            raise _fail(f"{k} {got!r} != production {want!r}")
    paths = {"study_root": (cfg.study_root, spec.study_root),
             "ledger_path": (cfg.ledger_path, spec.ledger_path),
             "mailbox": (cfg.mailbox, spec.mailbox)}
    for k, (got, want) in paths.items():
        if _norm(got) != _norm(want):
            raise _fail(f"{k} {got} != production {want}")
    if [_norm(r) for r in cfg.read_roots] != [_norm(r) for r in spec.read_roots]:
        raise _fail("read_roots differ from production")
    if _protocol_doc(cfg, repo) != spec.protocol_doc_sha256:
        raise _fail("repository protocol document differs from production")
    for k, v in cfg.env.items():
        if os.environ.get(k) != v:
            raise _fail(f"environment {k}={os.environ.get(k)!r}, required {v!r} before Python")
    _write_roots(cfg, repo, spec)
    store = read_store(cfg.read_roots)
    hashes = _verify_sources(cfg, store)
    _verify_stored_checkpoint(cfg, store, spec)
    return hashes


def _synthetic(cfg: StudyConfig, repo: Path, spec: ProductionSpec) -> dict:
    if "SYNTHETIC" not in cfg.protocol:
        raise _fail("synthetic-fixture protocol must contain 'SYNTHETIC'")
    prod_roots = (*spec.read_roots, spec.study_root, spec.mailbox, Path(spec.ledger_path).parent)
    for p in (*cfg.read_roots, cfg.study_root, cfg.ledger_path, cfg.mailbox):
        for r in prod_roots:
            if _within(p, r):
                raise _fail(f"synthetic path {p} is inside production root {r}")
    prod_ids = {spec.sources["world"][0], spec.sources["E"][0],
                *(v[0] for v in spec.sources["T"].values()), spec.stored_checkpoint[0]}
    if prod_ids & set(cfg.expected_sources()):
        raise _fail("synthetic config uses a production source id")
    g = cfg.grid
    if len(g) < 3 or g[0] != 0 or g[-1] != cfg.steps or any(b <= a for a, b in zip(g, g[1:])):
        raise _fail(f"grid {g} must be strictly increasing from 0 to steps with >= 3 points")
    if not all(v > 0 for v in cfg.sizes.values()):
        raise _fail("sizes must be positive")
    if not all(math.isfinite(v) and v > 0 for v in cfg.gc.values()):
        raise _fail("G_C values must be positive and finite")
    if not cfg.masters or not all(isinstance(m, int) and not isinstance(m, bool)
                                  for m in cfg.masters):
        raise _fail("masters must be a non-empty list of ints")
    if cfg.threads < 1:
        raise _fail("threads must be >= 1")
    if cfg.stored_checkpoint is not None:
        raise _fail("synthetic-fixture configs carry no stored checkpoint")
    _protocol_doc(cfg, repo)
    _write_roots(cfg, repo, spec)
    return _verify_sources(cfg, read_store(cfg.read_roots))


def validate_config(cfg: StudyConfig, repo: Path, spec: ProductionSpec = PRODUCTION) -> dict:
    """Read-only report (resolved roots, mode, checked hashes); ``ConfigInvalid`` otherwise."""
    if not isinstance(cfg, StudyConfig):
        raise ConfigInvalid(f"expected a StudyConfig, got {type(cfg).__name__}")
    if cfg.mode == "production":
        hashes = _production(cfg, Path(repo), spec)
    elif cfg.mode == "synthetic-fixture":
        hashes = _synthetic(cfg, Path(repo), spec)
    else:
        raise ConfigInvalid(f"unknown mode {cfg.mode!r}")
    return {"mode": cfg.mode, "protocol": cfg.protocol,
            "protocol_doc_sha256": cfg.protocol_doc_sha256,
            "roots": {"read_roots": [_norm(r) for r in cfg.read_roots],
                      "study_root": _norm(cfg.study_root),
                      "ledger_path": _norm(cfg.ledger_path), "mailbox": _norm(cfg.mailbox)},
            "source_sha256": hashes, "stored_checkpoint": cfg.stored_checkpoint,
            "env": dict(cfg.env)}

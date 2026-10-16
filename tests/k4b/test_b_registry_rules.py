"""Author B, round 2: coordinator ruling R23 (API §15), the registry classification amendments to
`k4b_registry.inventory`/`classify`/`build`, on synthetic trees under tmp_path. Rule 1:
ObservationSet stores with own payloads are SCANNED via source (f) (raw tokens[:, :32] when no
EmissionSpec perm resolves); a stray history file outside the ObservationSet root → INCOMPLETE.
Rule 2: "synthetic test fixtures" only under a basetemp segment with ≤ 1,024 header rows. Rule 3:
main inventoried deep (tests/, .venv). Rule 4: unreadable files are fixtures only inside a
basetemp segment. Rule 5: dedicated-reader directories are not deep-scanned; no sealed D-2a array
is opened. Basetemp segments are judged on the path relative to the inventoried root (tmp_path
itself lies under pytest's basetemp). `classify` gets an empty `scanned_readers` mapping (as in
round 1); every npz is built here with numpy; header reads suffice for every expectation."""

from __future__ import annotations

import builtins
import hashlib
import io
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry", "tools/x4_circle_history",
             "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import numpy as np  # noqa: E402
import pytest  # noqa: E402

import c1_data  # noqa: E402
import c1_registry_sources  # noqa: E402
import k4b_config  # noqa: E402
import k4b_registry  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

FIXTURES = "synthetic test fixtures"
DEDICATED = ("agent-handoff", "c1prime-store", "d2a-store")
POOLS = list(k4b_config.CONTRACT["registry"]["d2a"]["pools"])
SEALED = ("test", "testN")


def entry(mapping, root, name):
    for key in (name, str(root / name), root / name, (root / name).as_posix()):
        if key in mapping:
            return mapping[key]
    raise KeyError(name)


def names(paths) -> set:
    return {Path(p).name for p in paths}


def is_under(path, base) -> bool:
    try:
        Path(path).resolve().relative_to(Path(base).resolve())
    except ValueError:
        return False
    return True


def put(path: Path, **arrays) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, **arrays)
    return path


def hist(path: Path, rows: int, cols: int = 33, key: str = "tokens") -> Path:
    return put(path, **{key: np.zeros((rows, cols), dtype=np.uint8)})


def junk(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"not an npz archive\n" * 4)


def truncated(path: Path) -> None:
    hist(path, 6)
    data = path.read_bytes()
    path.write_bytes(data[: len(data) // 2])


def note(d: Path) -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / "README.txt").write_text("notes only\n", encoding="utf-8")


def classify_root(root):
    inv = k4b_registry.inventory(root)
    return inv, k4b_registry.classify(inv, {})


def klass(root, name) -> dict:
    return entry(classify_root(root)[1], root, name)


def deep(root: Path, top: str, segs) -> Path:
    return root.joinpath(top, *segs)


# ------------------------------------------------------- rule 2: synthetic test fixtures

SEGMENTS = [
    ("tmp-0048", ("pytest-of-pc2", "pytest-7", "test_a0")),
    ("tmp-0048", ("bt3", "test_a0")),
    ("tmp-0048", ("pt-17", "test_b0", "sub")),
    ("coord-scratch", ("pt-abc", "test_c0")),
    ("coord-scratch", ("bt", "x")),
    ("work-dir", ("deep", "pytest-of-someone", "pytest-1", "t0")),
    ("pytest-of-pc2", ("pytest-3", "test_d0")),
]


@pytest.mark.parametrize("top,segs", SEGMENTS)
def test_fixtures_in_a_basetemp_segment_are_not_scanned(tmp_path, top, segs):
    root = tmp_path / "root"
    base = deep(root, top, segs)
    hist(base / "fix.npz", 5)
    hist(base / "more" / "canon.npz", 1024, 32, key="canon32")  # 1,024 rows: still a fixture
    put(base / "ids.npz", x=np.ones((3, 32), dtype=np.int64))
    note(root / top)
    c = klass(root, top)
    assert c["class"] == "NOT_SCANNED"
    assert FIXTURES in c["reason"]


@pytest.mark.parametrize("key,rows,cols,dtype", [("tokens", 1025, 33, np.uint8),
                                                 ("x", 1025, 32, np.int64),
                                                 ("canon32", 4096, 32, np.uint8)])
def test_fixture_with_more_than_1024_rows_is_incomplete(tmp_path, key, rows, cols, dtype):
    root = tmp_path / "root"
    base = deep(root, "tmp-0048", ("pytest-of-pc2", "pytest-1", "test_e0"))
    hist(base / "small.npz", 3)
    put(base / "big.npz", **{key: np.zeros((rows, cols), dtype=dtype)})
    assert klass(root, "tmp-0048")["class"] == "INCOMPLETE"


def test_one_large_array_in_a_small_file_is_incomplete(tmp_path):
    root = tmp_path / "root"
    base = deep(root, "coord-scratch", ("bt9", "t0"))
    put(base / "mixed.npz", tokens=np.zeros((10, 33), dtype=np.uint8),
        named32=np.zeros((1025, 32), dtype=np.uint8))
    assert klass(root, "coord-scratch")["class"] == "INCOMPLETE"


OUTSIDE = [
    ("tmp-0048", ("data",)),
    ("tmp-0048", ("sub", "bt3")),        # bt* not directly under the tmp-* directory
    ("tmp-0048", ("sub", "pt-1")),
    ("work-dir", ("bt3",)),              # bt* under neither tmp-* nor coord-scratch
    ("coord-scratch", ("cache",)),
    ("topo-pilot-wt", ("tests", "fixtures")),  # tests/ is rule 3 (main) only, not a segment
]


@pytest.mark.parametrize("top,segs", OUTSIDE)
def test_history_outside_a_basetemp_segment_is_incomplete(tmp_path, top, segs):
    root = tmp_path / "root"
    hist(deep(root, top, segs) / "h.npz", 5)
    c = klass(root, top)
    assert c["class"] == "INCOMPLETE"
    assert c["reason"]


def test_one_file_outside_the_segment_spoils_the_directory(tmp_path):
    root = tmp_path / "root"
    hist(deep(root, "tmp-0048", ("bt1", "t0")) / "ok.npz", 5)
    hist(deep(root, "tmp-0048", ("export",)) / "h.npz", 5)
    assert klass(root, "tmp-0048")["class"] == "INCOMPLETE"


# ------------------------------------------------------------ rule 4: unreadable files

@pytest.mark.parametrize("make", [junk, truncated])
def test_unreadable_file_inside_a_segment_counts_as_fixture(tmp_path, make):
    root = tmp_path / "root"
    base = deep(root, "tmp-0048", ("pytest-of-pc2", "pytest-2", "test_f0"))
    hist(base / "ok.npz", 4)
    make(base / "broken.npz")
    c = klass(root, "tmp-0048")
    assert c["class"] == "NOT_SCANNED" and FIXTURES in c["reason"]


@pytest.mark.parametrize("make", [junk, truncated])
@pytest.mark.parametrize("segs", [("export",), ("sub", "bt2")])
def test_unreadable_file_outside_a_segment_is_incomplete(tmp_path, make, segs):
    root = tmp_path / "root"
    hist(deep(root, "tmp-0048", ("bt1", "t0")) / "ok.npz", 4)
    make(deep(root, "tmp-0048", segs) / "broken.npz")
    assert klass(root, "tmp-0048")["class"] == "INCOMPLETE"


# ------------------------------------------------------------- rule 3: main, deep

def main_tree(root: Path) -> Path:
    main = root / "topo-pilot"
    note(main)
    hist(main / "tests" / "fixtures" / "tiny.npz", 8)
    put(main / "tests" / "oracle" / "data" / "ids.npz", x=np.ones((16, 32), dtype=np.int64))
    hist(main / ".venv" / "Lib" / "site-packages" / "pkg" / "data" / "sample.npz", 1024, 32,
         key="canon32")
    hist(main / "tmp" / "pytest-of-pc2" / "pytest-1" / "t0" / "fix.npz", 5)
    return main


def test_main_inventory_is_deep_including_tests_and_venv(tmp_path):
    root = tmp_path / "root"
    main = main_tree(root)
    hist(main.joinpath("a", "b", "c", "d", "e", "f") / "deep.npz", 3)
    files = names(entry(k4b_registry.inventory(root), root, "topo-pilot")["history_files"])
    assert {"tiny.npz", "ids.npz", "sample.npz", "fix.npz", "deep.npz"} <= files


def test_main_with_only_tests_venv_and_basetemp_fixtures_is_not_incomplete(tmp_path):
    root = tmp_path / "root"
    main_tree(root)
    assert klass(root, "topo-pilot")["class"] != "INCOMPLETE"


@pytest.mark.parametrize("rel,rows", [
    (("scripts", "out", "h.npz"), 5),               # outside tests/, .venv and basetemp
    (("results", "x4", "hist.npz"), 5),
    (("a", "b", "c", "d", "e", "f", "deep.npz"), 3),
    (("tests", "big.npz"), 1025),                   # under tests/ but more than 1,024 rows
    ((".venv", "Lib", "big.npz"), 2000),
])
def test_main_file_failing_rule_2a_prime_makes_main_incomplete(tmp_path, rel, rows):
    root = tmp_path / "root"
    hist(main_tree(root).joinpath(*rel), rows)
    assert klass(root, "topo-pilot")["class"] == "INCOMPLETE"


# ------------------------------------------------- rule 1: ObservationSet stores (source f)

def os_store(store: Path) -> np.ndarray:
    from topo_pilot.contracts import ArtifactStore, LocalFSBackend
    from topo_pilot.contracts.testing import tiny_observations

    obs = tiny_observations(R=8, seed=3)
    ArtifactStore(LocalFSBackend(store)).save(
        obs, config={"split": "test", "fixture": "k4b-r23"}, parents=[], seed_map={},
        consumer="dataset")
    return np.asarray(obs.tokens)


@pytest.mark.parametrize("top,sub", [("x5g1-research-store", ("store",)),
                                     ("x5g1t-fixture-run", ("study", "store")),
                                     ("x9-new-research-store", ("store",))])
def test_observation_set_store_is_scanned_via_source_f(tmp_path, top, sub):
    root = tmp_path / "root"
    store = root.joinpath(top, *sub)
    tokens = os_store(store)
    note(root / top)
    inv, classes = classify_root(root)
    roots = entry(inv, root, top)["observation_set_roots"]
    assert any(is_under(r, store) for r in roots)
    assert entry(classes, root, top)["class"] == "SCANNED"
    srcs = [s for s in k4b_registry.source_f(root, inv, classes) if is_under(s["path"], root / top)]
    assert srcs
    reg = c1_data.build_registry(srcs)
    assert reg["status"] == "PASS"
    # no EmissionSpec parent resolves: the raw tokens[:, :32] are the contribution
    assert set(reg["digests"]) == c1_data.registry_digests(tokens[:, :32].astype(np.uint8))


@pytest.mark.parametrize("stray", [("exports", "hist.npz"), ("study", "cache", "canon.npz")])
def test_stray_history_outside_the_os_root_is_incomplete(tmp_path, stray):
    root = tmp_path / "root"
    os_store(root / "x5g1-research-store" / "store")
    hist(root.joinpath("x5g1-research-store", *stray), 5)
    assert klass(root, "x5g1-research-store")["class"] == "INCOMPLETE"


def test_history_file_inside_the_os_root_counts_as_covered(tmp_path):
    root = tmp_path / "root"
    store = root / "x5g1t-research-store" / "store"
    os_store(store)
    art = next(p for p in (store / "ObservationSet").iterdir() if p.is_dir())
    hist(art / "copy_tokens.npz", 8)
    assert klass(root, "x5g1t-research-store")["class"] == "SCANNED"


# ------------------------------------------- rule 5: dedicated readers, sealed D-2a pools

def dig(i) -> str:
    return hashlib.sha256(bytes([i % 256]) * 32 + str(i).encode()).hexdigest()


def c1prime_store(root: Path) -> Path:
    store = root / "c1prime-store"
    (store / "registry").mkdir(parents=True)
    (store / "registry" / "registry_v1.json").write_text(
        json.dumps({"schema": "c1prime-registry-v1", "digests": [dig(i) for i in range(4)]}),
        encoding="utf-8")
    put(store / "stages" / "S3" / "HIST_cal_b0.npz",
        **{k: np.array([dig(50 + 10 * j + i) for i in range(3)])
           for j, k in enumerate(("digest_H", "digest_Hp", "digest_Hm"))})
    return store


def d2a_store(root: Path) -> Path:
    store = root / "d2a-store"
    store.mkdir(parents=True)
    rng = np.random.default_rng(21)
    (store / "pools.json").write_text(json.dumps({p: {"n": 10 + i} for i, p in enumerate(POOLS)}),
                                      encoding="utf-8")
    for i, p in enumerate(POOLS):
        lo, hi = (0, 5) if p in SEALED else (5, 36)
        tok = rng.integers(lo, hi, (10 + i, 33)).astype(np.uint8)
        for path in (store / "pools" / f"{p}.npz", store / f"{p}.npz", store / p / "tokens.npz"):
            put(path, tokens=tok)
    return store


def mailbox(root: Path) -> Path:
    box = root / "agent-handoff" / "jobs" / "0001"
    box.mkdir(parents=True)
    (box / "status.json").write_text(json.dumps({"row": list(range(32))}), encoding="utf-8")
    return root / "agent-handoff"


def sealed(path, d2a: Path) -> bool:
    try:
        rel = Path(path).resolve().relative_to(d2a.resolve())
    except ValueError:
        return False
    return any(Path(part).stem in SEALED for part in rel.parts)


def guard(monkeypatch, d2a: Path, seen: list) -> None:
    """Record every opened path; refuse (raise) on any sealed D-2a pool array."""
    real_open, real_load = builtins.open, np.load

    def note_path(file):
        if isinstance(file, (str, bytes, os.PathLike)):
            p = Path(os.fsdecode(os.fspath(file)))
            seen.append(p)
            if sealed(p, d2a):
                raise AssertionError(f"sealed D-2a array opened: {p}")

    def spy_open(file, *args, **kwargs):
        note_path(file)
        return real_open(file, *args, **kwargs)

    def spy_load(file, *args, **kwargs):
        note_path(file)
        return real_load(file, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", spy_open)
    monkeypatch.setattr(io, "open", spy_open)
    monkeypatch.setattr(np, "load", spy_load)


def test_dedicated_dirs_are_not_deep_scanned_by_the_inventory(tmp_path, monkeypatch):
    root = tmp_path / "root"
    d2a = d2a_store(root)
    c1prime_store(root)
    mailbox(root)
    hist(deep(root, "tmp-0048", ("bt1", "t0")) / "f.npz", 3)
    seen: list = []
    guard(monkeypatch, d2a, seen)
    inv = k4b_registry.inventory(root, exclude=DEDICATED)
    monkeypatch.undo()
    assert not [p for p in seen if any(is_under(p, root / d) for d in DEDICATED)]
    for d in DEDICATED:
        try:
            e = entry(inv, root, d)
        except KeyError:
            continue
        assert not e["history_files"] and not e["observation_set_roots"]
    assert "f.npz" in names(entry(inv, root, "tmp-0048")["history_files"])


def test_build_never_opens_a_sealed_pool_array(tmp_path, monkeypatch):
    root = tmp_path / "root"
    art = root / "topo-pilot" / "artifacts"
    for sub in ("ObservationSet", "EmissionSpec", "HistoryIndex"):
        (art / sub).mkdir(parents=True)
    mailbox(root)
    store = c1prime_store(root)
    monkeypatch.setitem(k4b_config.CONTRACT["registry"], "c1prime_registry_v1_sha256",
                        hashlib.sha256((store / "registry" / "registry_v1.json").read_bytes())
                        .hexdigest())
    d2a = d2a_store(root)
    hist(deep(root, "tmp-0048", ("pytest-of-pc2", "pytest-1", "t0")) / "fix.npz", 4)
    monkeypatch.setattr(c1_registry_sources, "ROOT", root)
    monkeypatch.setattr(c1_registry_sources, "ART", art)
    monkeypatch.setattr(k4b_config, "ROOT", root)
    for name, value in (("ROOT", root), ("ART", art)):
        if hasattr(k4b_registry, name):
            monkeypatch.setattr(k4b_registry, name, value)
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    seen: list = []
    guard(monkeypatch, d2a, seen)
    try:
        k4b_registry.build("K-REG1", out_dir, root=root)
    except C1GateFailure:
        pass  # the absent source-(b) stores make this registry INCOMPLETE; only access matters
    assert not [p for p in seen if sealed(p, d2a)]

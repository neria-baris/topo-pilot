"""X6S1 registry: digests, on-disk sorted digest runs, the bounded-memory K-REG2 identity reader,
the REG1 sources, the extended inventory, REG1/REG2, separation and the diagnostics
(X6S1-FROZEN-v1 §6.4-§6.6, RC10; API.md §10, §13 items 5 and 24). Import performs no I/O beyond
the reused C1'/K4b CONTRACT.json reads (API.md §13 item 24)."""
# fmt: off

from __future__ import annotations

import hashlib
import io
import itertools
import json
import time
import zipfile
from fractions import Fraction
from pathlib import Path

import x6s1_data as sd  # first: its import applies the API.md §1 sys.path convention

REPO = sd.REPO
import c1_registry_sources as crs  # noqa: E402
import k4b_registry as kr  # noqa: E402
import k4b_registry_k as kk  # noqa: E402
import numpy as np  # noqa: E402
import x6_exact as xe  # noqa: E402
import x6_model as xm  # noqa: E402

from topo_pilot.contracts import canonical_json  # noqa: E402
from topo_pilot.contracts.errors import StageFailure  # noqa: E402
from topo_pilot.dataset.checks import check_disjoint  # noqa: E402

LINEAGE, INCOMPLETE = "FAIL_TECHNICAL/LINEAGE", "INCONCLUSIVE/REGISTRY_INCOMPLETE"
MAILBOX, K4B_STORE, REG_RUN = sd.MAILBOX, sd.K4B_STORE, sd.REG_RUN
V32 = np.dtype((np.void, 32))
CHUNK_BYTES = 64 * 2**20  # K-REG2 stream chunk cap (API.md §13 item 24)
POOL_KINDS = ("train", "dev", "val", "gate", "smoke", "prefix", "test")
FOREIGN_REASON = {"agent-handoff": "REG1 source (b): handoff JSON (§6.4 (b))",
                  "k4b-store": "REG1 source (c): foreign alarm, reader k and K-REG2 (§6.4 (c))"}
NOT_X6 = "not an X6 directory: other processes' histories are not X6 exposures (§6.6 item 1)"
EMPTY = np.zeros((0, 32), dtype=np.uint8)

class RegistryError(RuntimeError):
    def __init__(self, status: str, detail: str = ""):
        super().__init__(f"{status}: {detail}" if detail else status)
        self.status = status
def _req(ok, status: str, detail: str) -> None:
    if not ok:
        raise RegistryError(status, detail)
def _file_sha(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()
def utc_iso() -> str: return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# ---- digests and keys (§6.4) ----
def row_digests(tokens) -> np.ndarray:
    """uint8 [n, 32]: sha256 of each row's w_1..w_32 bytes (uint8)."""
    t = np.asarray(tokens)
    if t.ndim != 2 or t.shape[1] < 32 or t.dtype.kind not in "iu":
        raise ValueError(f"tokens must be integer [n, >= 32], got {t.dtype} {t.shape}")
    if t.dtype != np.uint8:
        if t.size and (t.min() < 0 or t.max() > 255):
            raise ValueError("token value outside 0..255")
        t = t.astype(np.uint8)
    b, sha = np.ascontiguousarray(t[:, :32]).tobytes(), hashlib.sha256
    return np.frombuffer(b"".join(sha(b[i:i + 32]).digest() for i in range(0, len(b), 32)),
                         dtype=np.uint8).reshape(-1, 32)
def _u8(digests) -> np.ndarray: return np.ascontiguousarray(digests).view(np.uint8).reshape(-1, 32)
def _void(digests) -> np.ndarray: return _u8(digests).view(V32).reshape(-1)
def digest_keys(digests) -> np.ndarray:
    """uint64 [n]: the first 8 digest bytes read big-endian (key order = digest byte order)."""
    return np.ascontiguousarray(_u8(digests)[:, :8]).view(">u8").reshape(-1).astype(np.uint64)
def hex_to_digests(hex_array) -> np.ndarray:
    a = np.asarray(hex_array, dtype=str).reshape(-1)
    if a.size and not bool(np.all(np.char.str_len(a) == 64)):
        raise ValueError("a digest hex string is not 64 characters")
    return np.frombuffer(bytes.fromhex("".join(a.tolist())), dtype=np.uint8).reshape(-1, 32)
def _member(q, ref) -> np.ndarray:
    """bool [len(q)]: full 32-byte membership of void digests q in the sorted void array ref."""
    if not len(ref) or not len(q):
        return np.zeros(len(q), dtype=bool)
    return np.asarray(ref[np.minimum(np.searchsorted(ref, q), len(ref) - 1)] == q, dtype=bool)
def _hits(q, ref) -> int: return int(_member(q, ref).sum())
def _bound(key) -> np.ndarray:  # the smallest digest with this key, as a void [1]
    return np.frombuffer(int(key).to_bytes(8, "big") + bytes(24), dtype=V32)

# ---- sorted digest runs on disk (§6.4, §13.4; API.md §13 items 5, 24) ----
class DigestSet:
    """Sorted runs of 32-byte digests on disk plus the merged sorted uint64 keys (duplicates kept;
    `n` counts them). `base` is the set whose runs this one includes (REG2 -> REG1)."""

    def __init__(self, paths, keys=None, run=REG_RUN, base=None, shas=None):
        self.paths, self.run, self.base = [Path(p) for p in paths], int(run), base
        self.shas = dict(shas or {})
        if keys is None:
            parts = [digest_keys(self._run(i)) for i in range(len(self.paths))]
            keys = np.sort(np.concatenate(parts)) if parts else np.zeros(0, dtype=np.uint64)
        self.keys, self.n = keys, int(len(keys))

    def _run(self, i) -> np.ndarray:
        return _void(np.load(self.paths[i], mmap_mode="r", allow_pickle=False))

    @classmethod
    def build(cls, chunks, run_dir, run=REG_RUN, base=None) -> DigestSet:
        """Sorts runs of <= run identities (filled across chunks) into a new run_dir."""
        run_dir, run = Path(run_dir), int(run)
        run_dir.mkdir(parents=True)  # a new directory per set (exclusive)
        paths, keys, shas, buf, nbuf = [], [], {}, [], 0
        def flush():
            v, bio = np.sort(np.concatenate(buf)), io.BytesIO()
            np.save(bio, _u8(v), allow_pickle=False)
            paths.append(run_dir / f"run_{len(paths):05d}.npy")
            with open(paths[-1], "xb") as fh:
                fh.write(bio.getvalue())
            shas[str(paths[-1])] = hashlib.sha256(bio.getvalue()).hexdigest()
            keys.append(digest_keys(v))
            buf.clear()
        for chunk in chunks:
            v = _void(np.asarray(chunk, dtype=np.uint8))
            while len(v):
                buf.append(v[:run - nbuf])
                v, nbuf = v[len(buf[-1]):], nbuf + len(buf[-1])
                if nbuf == run:
                    flush()
                    nbuf = 0
        if buf:
            flush()
        if base is not None:
            paths, shas = base.paths + paths, {**base.shas, **shas}
            keys.append(base.keys)
        merged = np.sort(np.concatenate(keys)) if keys else np.zeros(0, dtype=np.uint64)
        return cls(paths, merged, run, base, shas)

    def contains(self, digests) -> np.ndarray:
        """Key candidate search, then full-digest confirmation against the runs."""
        q = _u8(digests)
        k = digest_keys(q)
        cand = np.flatnonzero(np.searchsorted(self.keys, k, "right")
                              > np.searchsorted(self.keys, k, "left"))
        out = np.zeros(len(q), dtype=bool)
        if len(cand):
            qv, found = _void(q[cand]), np.zeros(len(cand), dtype=bool)
            for i in range(len(self.paths)):
                found |= _member(qv, self._run(i))
            out[cand] = found
        return out

    def blocks(self):
        """The sorted unique digests (void) in key blocks of about `run` identities."""
        runs = [self._run(i) for i in range(len(self.paths))]
        lo = [0] * len(runs)
        for b in [_bound(k) for k in np.unique(self.keys[::max(self.run, 1)])[1:]] + [None]:
            parts = []
            for j, r in enumerate(runs):
                hi = len(r) if b is None else int(np.searchsorted(r, b)[0])
                parts.append(np.asarray(r[lo[j]:hi]))
                lo[j] = hi
            if parts:
                yield np.unique(np.concatenate(parts))

    def sha256(self) -> str:
        """sha256 of the sorted unique full digests (32 bytes each), concatenated."""
        h = hashlib.sha256()
        for block in self.blocks():
            h.update(block.tobytes())
        return h.hexdigest()

# ---- bounded-memory K-REG2 identity reader (§6.4 (c), RC10) ----
def _npy_header(f) -> tuple:
    version = np.lib.format.read_magic(f)
    _req(version in ((1, 0), (2, 0)), LINEAGE, f"unsupported .npy format {version}")
    read = (np.lib.format.read_array_header_1_0 if version == (1, 0)
            else np.lib.format.read_array_header_2_0)
    return read(f)  # (shape, fortran_order, dtype)
def _stream(out_dir, version, key, want, run):
    path = Path(out_dir) / f"{version}_digests.npz"
    with zipfile.ZipFile(path) as z:
        _req(f"{key}.npy" in z.namelist(), LINEAGE, f"{path.name} has no member {key}")
        with z.open(f"{key}.npy") as f:
            shape, fortran, dtype = _npy_header(f)
            _req(dtype == np.dtype(want) and len(shape) == 1 and not fortran, LINEAGE,
                 f"{key}: stored {dtype} {shape} (want {want}, 1-D)")
            step, left = max(1, min(int(run), CHUNK_BYTES // dtype.itemsize)), shape[0]
            while left:
                k = min(step, left)
                buf = f.read(k * dtype.itemsize)
                _req(len(buf) == k * dtype.itemsize, LINEAGE, f"{key}: truncated member")
                left -= k
                yield np.frombuffer(buf, dtype=dtype)
def iter_kreg2(out_dir, version="K-REG2", run=REG_RUN):
    """The stored `digests` (<U64) in stored order, chunks of <= run entries; no full load."""
    return _stream(out_dir, version, "digests", "<U64", run)
def iter_kreg2_seq_ids(out_dir, version="K-REG2", run=REG_RUN):
    return _stream(out_dir, version, "seq_ids", "<i8", run)
def _ascending(c, last) -> bool:
    return bool(np.all(c[1:] > c[:-1])) and (last is None or c[0] > last)
def read_kreg2(out_dir, version="K-REG2", run=REG_RUN) -> dict:
    """Streams and validates K-REG2 against its manifest (dtype, shape, strict order, count,
    canonical union hashes); any mismatch is RegistryError(LINEAGE)."""
    out_dir = Path(out_dir)
    try:
        man = json.loads((out_dir / f"{version}.json").read_text(encoding="utf-8"))
    except ValueError as exc:
        raise RegistryError(LINEAGE, f"{version}.json unreadable: {exc!r}") from exc
    fsha = _file_sha(out_dir / f"{version}_digests.npz")
    _req(fsha == str(man.get("digest_file_sha256", "")).lower(), LINEAGE,
         f"{version}_digests.npz does not re-hash to its manifest")
    h, keys, n, last = hashlib.sha256(), [], 0, None
    for c in iter_kreg2(out_dir, version, run):
        _req(_ascending(c, last), LINEAGE, "digests are not strictly ascending")
        h.update((("\n" if n else "") + "\n".join(c.tolist())).encode("utf-8"))
        try:
            keys.append(digest_keys(hex_to_digests(c)))
        except ValueError as exc:
            raise RegistryError(LINEAGE, f"digest format: {exc}") from exc
        n, last = n + len(c), c[-1]
    _req(n == man.get("n_digests"), LINEAGE, f"{n} digests, manifest {man.get('n_digests')}")
    _req(h.hexdigest() == man.get("digests_sha256"), LINEAGE, "digest union hash mismatch")
    hs, ns, last = hashlib.sha256(), 0, None
    for c in iter_kreg2_seq_ids(out_dir, version, run):
        _req(_ascending(c, last), LINEAGE, "sequence ids are not strictly ascending")
        hs.update(c.tobytes())
        ns, last = ns + len(c), c[-1]
    _req(hs.hexdigest() == man.get("seq_id_union_sha256"), LINEAGE, "seq-id union hash mismatch")
    return {"n_digests": n, "n_seq_ids": ns, "dtype": "<U64", "shape": [n], "seq_dtype": "int64",
            "digests_sha256": h.hexdigest(), "seq_id_union_sha256": hs.hexdigest(),
            "digest_file_sha256": fsha, "manifest": man,
            "keys": np.concatenate(keys) if keys else np.zeros(0, dtype=np.uint64)}

# ---- REG1 sources (§6.4 (a)-(c)) ----
CASES = tuple((f, p, 0) for f in ("W1", "W2") for p in ("P0", "P1", "P3")) + tuple(
    (f, "P6", y0) for f in ("W1", "W2") for y0 in range(3)) + (("W3", "P0", 0), ("W3p", "P0", 0))
def _pad32(hists) -> np.ndarray:
    out = np.zeros((len(hists), 32), dtype=np.uint8)
    for i, h in enumerate(hists):
        out[i, :min(len(h), 32)] = h[:32]
    return out
def constructed_histories() -> dict:
    """Stage-0 constructed histories (W1, W2 with P0/P1/P3/P6, W3, W3', the Decimal reference
    set's constructed part), zero-padded to 32 symbols (API.md §13 item 24)."""
    fam: dict = {}
    for f, pre, y0 in CASES:
        fam.setdefault(f, []).extend(xe.witness_tokens(f, m, y, pre, y0)
                                     for m in xe.members(f) for y in range(3))
    v = xm.vertex
    ref = [(w,) for w in range(18)] + [(a, b) for a in range(18) for b in range(18)
                                       if v(b) in xm.NEIGHBOURS[v(a)]]
    ref += [(5,) * 32, tuple(15 + k % 3 for k in range(32)), xe.witness_tokens("W2", "AB", 1, "P6"),
            xe.witness_tokens("W1", "U", 0) + (17,)]
    fam["reference"] = ref
    return {k: _pad32(h) for k, h in fam.items()}
def stage0_rows() -> dict:
    """REG1 (a): regenerated stage-0 MC tokens per arm (NA counts checked) and the stage-0
    constructed histories."""
    mc = sd.regenerate_stage0()
    counts = sd.stage0_counts(mc["NA"])
    return {"status": sd.stage0_count_check(counts), "counts": counts, "mc": mc,
            "constructed": constructed_histories()}
def _x6_valid(rows) -> list:
    out = []
    for r in np.asarray(rows, dtype=np.uint8).reshape(-1, 32).tolist():
        try:
            xm.parse(r)
        except ValueError:
            continue
        out.append(r)
    return out
def handoff_rows(mailbox=MAILBOX) -> dict:
    """REG1 (b): X6-valid 32/33-element lists (first 32 symbols) of every handoff JSON."""
    mailbox = Path(mailbox)
    v = kr.validate_handoff_json(mailbox)
    if not mailbox.is_dir() or not v["ok"]:
        return {"status": INCOMPLETE, "rows": EMPTY,
                "failures": v["failures"] or [{"path": str(mailbox), "error": "absent"}]}
    rows = [r for it in crs.handoff_sources(mailbox) for r in _x6_valid(it["reader"](it["path"]))]
    return {"status": "PASS", "rows": np.asarray(rows, dtype=np.uint8).reshape(-1, 32),
            "failures": []}
def foreign_sources(k4b_store=K4B_STORE, bound=sd.KREG2_FILES) -> dict:
    """REG1 (c): reader k classification of k4b-store plus the streamed, validated K-REG2."""
    store = Path(k4b_store)
    kdir, names = store / "registry", ("K-REG2.json", "K-REG2_digests.npz")
    if not all((kdir / f).is_file() for f in names):
        return {"status": INCOMPLETE, "reason": f"{kdir}: K-REG2 files absent"}
    k, kreg = kk.source_k(store), read_kreg2(kdir, "K-REG2")
    if bound is not None:
        _req(_file_sha(kdir / names[0]) == bound[names[0]].lower()
             and kreg["digest_file_sha256"] == bound[names[1]].lower()
             and kreg["n_digests"] == sd.KREG2_N_DIGESTS, LINEAGE,
             "K-REG2 differs from its frozen binding (§15 D5)")
    return {"status": k["status"], "kreg_dir": str(kdir), "source_k": k, "summary": kk.summary(k),
            "kreg2": {key: val for key, val in kreg.items() if key != "keys"},
            "reason": "foreign alarm (§6.4 (c), §6.6 item 3)"}

# ---- extended inventory (§6.4 (d)) ----
def _headers(path) -> list:
    """[(key, dtype, shape)] from .npy headers only (a .npy file, or each .npz member)."""
    path = Path(path)
    if path.suffix == ".npy":
        with open(path, "rb") as f:
            shape, _, dtype = _npy_header(f)
        return [("", dtype, shape)]
    out = []
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            with z.open(name) as f:
                shape, _, dtype = _npy_header(f)
            out.append((name[:-4] if name.endswith(".npy") else name, dtype, shape))
    return out
def _history_bearing(path) -> bool:
    return any(k in kk.HISTORY_KEYS or k.startswith("digest")
               or (dt.kind in "iu" and len(sh) >= 2 and sh[-1] in (32, 33))
               for k, dt, sh in _headers(path))
def _scan(root, reg) -> dict:
    """One X6 root: every history-bearing .npz/.npy, ObservationSet object and history-bearing
    JSON must be a hash-identical registered copy; anything else is unclassified."""
    root = Path(root)
    if not root.is_dir():
        return {"absent": True, "unclassified": [], "copies": []}
    bad, copies = [], []
    def check(path, files, why):
        shas = {_file_sha(f) for f in files}
        if files and shas <= set(reg):
            copies.append({"path": str(path), "names": sorted(reg[s] for s in shas)})
        else:
            bad.append({"path": str(path), "reason": why})
    files = sorted(p for p in root.rglob("*") if p.is_file())
    objs = sorted({f.parent for f in files
                   if f.name == "meta.json" and f.parent.parent.name == "ObservationSet"})
    for o in objs:
        check(o, [f for f in files if o in f.parents and f.suffix in (".npz", ".npy")],
              "ObservationSet object not registered")
    for f in files:
        if f.suffix not in (".npz", ".npy") or any(o in f.parents for o in objs):
            continue
        try:
            hist = _history_bearing(f)
        except Exception as exc:  # any unreadable array file is unclassified
            bad.append({"path": str(f), "reason": f"unreadable {exc!r}"})
            continue
        if hist:
            check(f, [f], "history-bearing array not registered")
    for fail in kr.validate_handoff_json(root)["failures"]:
        bad.append({"path": fail["path"], "reason": f"unparsable JSON {fail['error']}"})
    for it in crs.handoff_sources(root):
        if _x6_valid(it["reader"](it["path"])):
            check(Path(it["path"]), [Path(it["path"])], "history-bearing JSON not registered")
    return {"absent": False, "unclassified": bad, "copies": copies}
def inventory_x6(project_root, scratch_roots, registered) -> dict:
    """k4b_registry.inventory(project_root) as one component, then the extended scan of the X6
    directories under the root and of every named X6 scratch root (API.md §13 item 24)."""
    reg = {str(k).lower(): v for k, v in registered.items()}
    inv = kr.inventory(project_root)
    roots, foreign = [], []
    for name, rec in inv.items():
        if "x6" in name.lower():
            roots.append(Path(rec["path"]))
            continue
        n = sum(len(rec[k]) for k in ("history_files", "observation_set_roots", "unreadable"))
        foreign.append({"path": rec["path"], "reason": FOREIGN_REASON.get(name, NOT_X6)
                        + f"; {n} history-bearing item(s)"})
    scans = {str(r): _scan(r, reg) for r in roots + [Path(s) for s in scratch_roots]}
    bad = [u["path"] for s in scans.values() for u in s["unclassified"]]
    return {"status": INCOMPLETE if bad else "PASS", "unclassified": bad, "foreign": foreign,
            "components": {"k4b_inventory": inv, "x6": scans}}

# ---- REG1 / REG2 (§6.4) ----
def collision_mass(n) -> Fraction: return n * Fraction(1, 16) * Fraction(1, 5**31)
def _chunks(tokens, step=REG_RUN):
    tokens = getattr(tokens, "tokens", tokens)
    for i in range(0, len(tokens), step):
        yield row_digests(tokens[i:i + step])
def _feed(srcs, stats):
    for name, kind, chunks in srcs:
        h, n = hashlib.sha256(), 0
        for c in chunks:
            c = np.ascontiguousarray(c, dtype=np.uint8).reshape(-1, 32)
            h.update(c.tobytes())
            n += len(c)
            yield c
        stats.append({"name": name, "kind": kind, "n": n, "sha256": h.hexdigest()})
def _write_reg(store, version, srcs, base=None, prior=()) -> dict:
    reg, stats = Path(store) / "registry", list(prior)
    ds = DigestSet.build(_feed(srcs, stats), reg / "runs" / version, base=base)
    man = {"version": version, "status": "PASS", "n": ds.n, "sources": stats,
           "digest_sha256": ds.sha256(), "collision_mass": str(collision_mass(ds.n)),
           "built_utc": utc_iso(), "base": None if base is None else "X6-REG1",
           "runs": [{"file": p.relative_to(reg).as_posix(), "sha256": ds.shas[str(p)]}
                    for p in ds.paths]}
    with open(reg / f"{version}.json", "xb") as fh:
        fh.write(canonical_json(man).encode("utf-8"))
    return man
def open_reg(store, version, manifest=None) -> DigestSet:
    """Reopens X6-REG1/X6-REG2 from its manifest; every run file is re-hashed."""
    reg = Path(store) / "registry"
    man = json.loads((reg / f"{version}.json").read_text(encoding="utf-8"))
    _req(man.get("status") == "PASS" and (manifest is None or json.loads(canonical_json(
        manifest)) == man), LINEAGE, f"{version} manifest differs or is not PASS")
    for r in man["runs"]:
        _req(_file_sha(reg / r["file"]) == r["sha256"], LINEAGE, f"{r['file']} re-hash mismatch")
    return DigestSet([reg / r["file"] for r in man["runs"]],
                     base=open_reg(store, man["base"]) if man.get("base") else None,
                     shas={str(reg / r["file"]): r["sha256"] for r in man["runs"]})
def build_reg1(store, sources) -> dict:
    """X6-REG1 from {"stage0", "inventory", "handoff", "foreign"} (before any stage-1 draw)."""
    need = ("stage0", "inventory", "handoff", "foreign")
    st = {k: sources[k]["status"] if k in sources else INCOMPLETE for k in need}
    _req(LINEAGE not in st.values(), LINEAGE, f"REG1 source statuses {st}")
    _req(set(st.values()) == {"PASS"}, INCOMPLETE, f"REG1 source statuses {st}")
    s0, fo = sources["stage0"], sources["foreign"]
    srcs = [(f"stage0_mc_{a}", "stage0_mc", _chunks(t)) for a, t in s0["mc"].items()]
    srcs += [(f"stage0_{k}", "stage0_constructed", _chunks(t))
             for k, t in s0["constructed"].items()]
    srcs.append(("handoff", "handoff_json", _chunks(sources["handoff"]["rows"])))
    srcs.append(("K-REG2", "foreign_kreg2", (hex_to_digests(c) for c in iter_kreg2(
        fo["kreg_dir"]))))
    srcs += [(it["name"], "foreign_k", itertools.chain(_chunks(it["reader"](it["path"])), [
        hex_to_digests(sorted(it["digests"]))])) for it in fo["source_k"]["sources"]]
    return _write_reg(store, "X6-REG1", srcs)
def build_reg2(store, reg1, pools) -> dict:
    """X6-REG2 = REG1 runs + every non-test stage-1 pool (after the draw, before the test draw)."""
    names = [s["name"] for s in sd.NONTEST_POOLS]
    extra = sorted(set(pools) - set(names))
    if extra:
        raise ValueError(f"REG2 takes the non-test pools only; refused {extra}")
    _req(not set(names) - set(pools), INCOMPLETE, f"REG2 lacks {sorted(set(names) - set(pools))}")
    srcs = [(n, "pool", _chunks(pools[n])) for n in names]
    return _write_reg(store, "X6-REG2", srcs, open_reg(store, "X6-REG1", reg1), reg1["sources"])

# ---- separation (§6.5) and diagnostics ----
def _kind(name) -> str:
    kind = str(name).split("_")[0]
    if kind not in POOL_KINDS:
        raise ValueError(f"unregistered pool name {name}")
    return kind
def separation(reg2, pools, reg1=None) -> dict:
    """§6.5 on every row: test ∩ REG2 = ∅ per arm; tests pairwise disjoint; val ∩ (REG1 ∪ train ∪
    dev ∪ gate ∪ smoke ∪ prefix) = ∅; gate, prefix, smoke disjoint from train and dev; sequence
    ids disjoint (check_disjoint); within-pool duplicates counted and kept."""
    reg1 = getattr(reg2, "base", None) if reg1 is None else reg1
    kind = {n: _kind(n) for n in pools}
    sv = {n: np.sort(_void(row_digests(p.tokens))) for n, p in pools.items()}
    def of(*kinds): return [n for n in pools if kind[n] in kinds]
    tests, vals, small = of("test"), of("val"), of("gate", "smoke", "prefix")
    td = np.sort(np.concatenate([sv[n] for n in of("train", "dev")] or [np.zeros(0, V32)]))
    checks = {
        "test_reg2": {n: int(reg2.contains(sv[n]).sum()) for n in tests},
        "test_pairs": {f"{a}|{b}": _hits(sv[a], sv[b]) for i, a in enumerate(tests)
                       for b in tests[i + 1:]},
        "val_nontest": {n: _hits(sv[n], td) + sum(_hits(sv[n], sv[m]) for m in small)
                        for n in vals},
        "gsp_train_dev": {n: _hits(sv[n], td) for n in small},
        "val_reg1": "NOT_RUN" if reg1 is None else {n: int(reg1.contains(sv[n]).sum())
                                                    for n in vals}}
    try:
        check_disjoint(**{n: np.asarray(p.sequence_id) for n, p in pools.items()})
        checks["seq_ids"] = "PASS"
    except StageFailure as exc:
        checks["seq_ids"] = f"FAIL: {exc}"
    hits = [v for c in checks.values() if isinstance(c, dict) for v in c.values()]
    status = (LINEAGE if any(hits) or checks["seq_ids"] != "PASS"
              else INCOMPLETE if vals and reg1 is None else "PASS")
    return {"status": status, "checks": checks,
            "duplicates": {n: int((v[1:] == v[:-1]).sum()) for n, v in sv.items()}}
def id_reuse(pools, other_sets) -> dict:
    """Sequence-id reuse between stage-1 pools and ObservationSets of other stores (diagnostic)."""
    def ids(o): return np.asarray(getattr(o, "sequence_id", o), dtype=np.int64)
    reuse = {p: {o: int(np.intersect1d(ids(pools[p]), ids(other_sets[o])).size)
                 for o in other_sets} for p in pools}
    return {"status": "DIAGNOSTIC", "reuse": reuse,
            "total": sum(v for r in reuse.values() for v in r.values())}
def cross_process(reg) -> dict:
    """Digest coincidences by source pair (diagnostic): distinct digests of a found in b; reg maps
    a source name to uint8 [n, 32] digests or a DigestSet (two DigestSets: None)."""
    names, out = list(reg), {}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            x, y = (reg[b], reg[a]) if isinstance(reg[a], DigestSet) else (reg[a], reg[b])
            if isinstance(x, DigestSet):
                out[f"{a}|{b}"] = None
                continue
            xv = np.unique(_void(x))
            out[f"{a}|{b}"] = (int(y.contains(xv).sum()) if isinstance(y, DigestSet)
                               else _hits(xv, np.sort(_void(y))))
    return {"status": "DIAGNOSTIC", "coincidences": out}

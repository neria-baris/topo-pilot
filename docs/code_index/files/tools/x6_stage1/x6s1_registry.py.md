# `tools/x6_stage1/x6s1_registry.py`

- Source: [tools/x6_stage1/x6s1_registry.py](../../../../../tools/x6_stage1/x6s1_registry.py)
- Kind: python
- Lines: 486

## Module docstring

> X6S1 registry: digests, on-disk sorted digest runs, the bounded-memory K-REG2 identity reader,
> the REG1 sources, the extended inventory, REG1/REG2, separation and the diagnostics
> (X6S1-FROZEN-v1 §6.4-§6.6, RC10; API.md §10, §13 items 5 and 24). Import performs no I/O beyond
> the reused C1'/K4b CONTRACT.json reads (API.md §13 item 24).

## Imports

### Internal (repo files)

- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](x6s1_data.py.md) (line 18, via same directory)
- `import c1_registry_sources` -> [tools/c1prime_registry/c1_registry_sources.py](../c1prime_registry/c1_registry_sources.py.md) (line 21, via unique basename)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../k4b/k4b_registry.py.md) (line 22, via unique basename)
- `import k4b_registry_k` -> [tools/k4b/k4b_registry_k.py](../k4b/k4b_registry_k.py.md) (line 23, via unique basename)
- `import x6_exact` -> [tools/x6_stage0/x6_exact.py](../x6_stage0/x6_exact.py.md) (line 25, via unique basename)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 26, via unique basename)
- `from topo_pilot.contracts import canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 28, via package root)
- `from topo_pilot.contracts.errors import StageFailure` -> [src/topo_pilot/contracts/errors.py](../../src/topo_pilot/contracts/errors.py.md) (line 29, via package root)
- `from topo_pilot.dataset.checks import check_disjoint` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 30, via package root)

### External (third-party)

- `numpy` (lines 24)

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 15)
- `hashlib` (lines 9)
- `io` (lines 10)
- `itertools` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 16)
- `time` (lines 13)
- `zipfile` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_readout/test_b_registry.py](../../tests/c2_readout/test_b_registry.py.md) (line 27, import)
- [tests/x6_stage1/test_b_seed_pool_reg.py](../../tests/x6_stage1/test_b_seed_pool_reg.py.md) (line 23, import)
- [tools/c2_nd/nd_registry.py](../c2_nd/nd_registry.py.md) (line 44, import)
- [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 102, import)
- [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 329, import)
- [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 354, import)
- [tools/hwsc/hwsc_dry2.py](../hwsc/hwsc_dry2.py.md) (line 182, import)
- [tools/hwsc/hwsc_scratch.py](../hwsc/hwsc_scratch.py.md) (line 15, import)
- [tools/x6_stage1/x6s1_stage_pre.py](x6s1_stage_pre.py.md) (line 33, import)

## Top-level constants

- `CASES`
- `CHUNK_BYTES`
- `EMPTY`
- `FOREIGN_REASON`
- `NOT_X6`
- `POOL_KINDS`
- `REPO`
- `V32`

## Classes and functions

- **class `RegistryError(RuntimeError)`** [L42-45]
- **method `RegistryError.__init__`** [L43-45]: `def __init__(self, status: str, detail: str = '')`
- **function `_req`** [L46-48]: `def _req(ok, status: str, detail: str) -> None`
- **function `_file_sha`** [L49-54]: `def _file_sha(path) -> str`
- **function `utc_iso`** [L55-55]: `def utc_iso() -> str`
- **function `row_digests`** [L58-69]: `def row_digests(tokens) -> np.ndarray` - uint8 [n, 32]: sha256 of each row's w_1..w_32 bytes (uint8).
- **function `_u8`** [L70-70]: `def _u8(digests) -> np.ndarray`
- **function `_void`** [L71-71]: `def _void(digests) -> np.ndarray`
- **function `digest_keys`** [L72-74]: `def digest_keys(digests) -> np.ndarray` - uint64 [n]: the first 8 digest bytes read big-endian (key order = digest byte order).
- **function `hex_to_digests`** [L75-79]: `def hex_to_digests(hex_array) -> np.ndarray`
- **function `_member`** [L80-84]: `def _member(q, ref) -> np.ndarray` - bool [len(q)]: full 32-byte membership of void digests q in the sorted void array ref.
- **function `_hits`** [L85-85]: `def _hits(q, ref) -> int`
- **function `_bound`** [L86-87]: `def _bound(key) -> np.ndarray`
- **class `DigestSet`** [L90-168] - Sorted runs of 32-byte digests on disk plus the merged sorted uint64 keys (duplicates kept;
- **method `DigestSet.__init__`** [L94-100]: `def __init__(self, paths, keys=None, run=REG_RUN, base=None, shas=None)`
- **method `DigestSet._run`** [L102-103]: `def _run(self, i) -> np.ndarray`
- **method `DigestSet.build`** [L106-134]: `def build(cls, chunks, run_dir, run=REG_RUN, base=None) -> DigestSet` decorators: @classmethod - Sorts runs of <= run identities (filled across chunks) into a new run_dir.
- **method `DigestSet.contains`** [L136-148]: `def contains(self, digests) -> np.ndarray` - Key candidate search, then full-digest confirmation against the runs.
- **method `DigestSet.blocks`** [L150-161]: `def blocks(self)` - The sorted unique digests (void) in key blocks of about `run` identities.
- **method `DigestSet.sha256`** [L163-168]: `def sha256(self) -> str` - sha256 of the sorted unique full digests (32 bytes each), concatenated.
- **function `_npy_header`** [L171-176]: `def _npy_header(f) -> tuple`
- **function `_stream`** [L177-191]: `def _stream(out_dir, version, key, want, run)`
- **function `iter_kreg2`** [L192-194]: `def iter_kreg2(out_dir, version='K-REG2', run=REG_RUN)` - The stored `digests` (<U64) in stored order, chunks of <= run entries; no full load.
- **function `iter_kreg2_seq_ids`** [L195-196]: `def iter_kreg2_seq_ids(out_dir, version='K-REG2', run=REG_RUN)`
- **function `_ascending`** [L197-198]: `def _ascending(c, last) -> bool`
- **function `read_kreg2`** [L199-230]: `def read_kreg2(out_dir, version='K-REG2', run=REG_RUN) -> dict` - Streams and validates K-REG2 against its manifest (dtype, shape, strict order, count,
- **function `_pad32`** [L235-239]: `def _pad32(hists) -> np.ndarray`
- **function `constructed_histories`** [L240-253]: `def constructed_histories() -> dict` - Stage-0 constructed histories (W1, W2 with P0/P1/P3/P6, W3, W3', the Decimal reference
- **function `stage0_rows`** [L254-260]: `def stage0_rows() -> dict` - REG1 (a): regenerated stage-0 MC tokens per arm (NA counts checked) and the stage-0
- **function `_x6_valid`** [L261-269]: `def _x6_valid(rows) -> list`
- **function `handoff_rows`** [L270-279]: `def handoff_rows(mailbox=MAILBOX) -> dict` - REG1 (b): X6-valid 32/33-element lists (first 32 symbols) of every handoff JSON.
- **function `foreign_sources`** [L280-294]: `def foreign_sources(k4b_store=K4B_STORE, bound=sd.KREG2_FILES) -> dict` - REG1 (c): reader k classification of k4b-store plus the streamed, validated K-REG2.
- **function `_headers`** [L297-310]: `def _headers(path) -> list` - [(key, dtype, shape)] from .npy headers only (a .npy file, or each .npz member).
- **function `_history_bearing`** [L311-314]: `def _history_bearing(path) -> bool`
- **function `_scan`** [L315-349]: `def _scan(root, reg) -> dict` - One X6 root: every history-bearing .npz/.npy, ObservationSet object and history-bearing
- **function `inventory_x6`** [L350-366]: `def inventory_x6(project_root, scratch_roots, registered) -> dict` - k4b_registry.inventory(project_root) as one component, then the extended scan of the X6
- **function `collision_mass`** [L369-369]: `def collision_mass(n) -> Fraction`
- **function `_chunks`** [L370-373]: `def _chunks(tokens, step=REG_RUN)`
- **function `_feed`** [L374-382]: `def _feed(srcs, stats)`
- **function `_write_reg`** [L383-393]: `def _write_reg(store, version, srcs, base=None, prior=()) -> dict`
- **function `open_reg`** [L394-404]: `def open_reg(store, version, manifest=None) -> DigestSet` - Reopens X6-REG1/X6-REG2 from its manifest; every run file is re-hashed.
- **function `build_reg1`** [L405-420]: `def build_reg1(store, sources) -> dict` - X6-REG1 from {"stage0", "inventory", "handoff", "foreign"} (before any stage-1 draw).
- **function `build_reg2`** [L421-429]: `def build_reg2(store, reg1, pools) -> dict` - X6-REG2 = REG1 runs + every non-test stage-1 pool (after the draw, before the test draw).
- **function `_kind`** [L432-436]: `def _kind(name) -> str`
- **function `separation`** [L437-465]: `def separation(reg2, pools, reg1=None) -> dict` - §6.5 on every row: test ∩ REG2 = ∅ per arm; tests pairwise disjoint; val ∩ (REG1 ∪ train ∪
- **function `id_reuse`** [L466-472]: `def id_reuse(pools, other_sets) -> dict` - Sequence-id reuse between stage-1 pools and ObservationSets of other stores (diagnostic).
- **function `cross_process`** [L473-486]: `def cross_process(reg) -> dict` - Digest coincidences by source pair (diagnostic): distinct digests of a found in b; reg maps


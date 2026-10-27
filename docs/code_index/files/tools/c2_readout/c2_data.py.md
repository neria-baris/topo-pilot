# `tools/c2_readout/c2_data.py`

- Source: [tools/c2_readout/c2_data.py](../../../../../tools/c2_readout/c2_data.py)
- Kind: python
- Lines: 337

## Module docstring

> C2 data: sampling (scope c2-v1), sequence ids, panels, the y-translation donor H^Y (the sign
> rule k_Y and the off-grid rule), the rho^(m) index map, history tables with the H^Y digest where
> defined, the coverage tally, namespace admission and store admission (API.md §4, §19.3;
> C2-FROZEN-v2 §2.2, §2.11, §5.2-§5.5, §11).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](c2_config.py.md) (line 19, via same directory)
- `import c1_data` -> [tools/c1prime/c1_data.py](../c1prime/c1_data.py.md) (line 22, via unique basename)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../c1prime/c1_oracle.py.md) (line 23, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 25, via unique basename)
- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 27, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 28, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 29, via package root)

### External (third-party)

- `numpy` (lines 24)

### Standard library

- `__future__` (lines 11)
- `fnmatch` (lines 13)
- `hashlib` (lines 14)
- `json` (lines 15)
- `os` (lines 16)
- `pathlib` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_b_registry.py](../../tests/c2_nd/test_b_registry.py.md) (line 24, import)
- [tests/c2_nd/test_impl_dry_hs.py](../../tests/c2_nd/test_impl_dry_hs.py.md) (line 28, import)
- [tests/c2_readout/test_a_oracle.py](../../tests/c2_readout/test_a_oracle.py.md) (line 35, import)
- [tests/c2_readout/test_b_fwl_l1.py](../../tests/c2_readout/test_b_fwl_l1.py.md) (line 323, import)
- [tests/c2_readout/test_b_lineage.py](../../tests/c2_readout/test_b_lineage.py.md) (line 24, import)
- [tests/c2_readout/test_b_patch.py](../../tests/c2_readout/test_b_patch.py.md) (line 320, import)
- [tests/c2_readout/test_b_policy.py](../../tests/c2_readout/test_b_policy.py.md) (line 25, import)
- [tests/c2_readout/test_b_registry.py](../../tests/c2_readout/test_b_registry.py.md) (line 23, import)
- [tools/c2_nd/nd_data.py](../c2_nd/nd_data.py.md) (line 18, import)
- [tools/c2_nd/nd_driver.py](../c2_nd/nd_driver.py.md) (line 22, import)
- [tools/c2_nd/nd_dry.py](../c2_nd/nd_dry.py.md) (line 23, import)
- [tools/c2_nd/nd_registry.py](../c2_nd/nd_registry.py.md) (line 25, import)
- [tools/c2_nd/nd_split.py](../c2_nd/nd_split.py.md) (line 17, import)
- [tools/c2_nd/nd_stage_base.py](../c2_nd/nd_stage_base.py.md) (line 22, import)
- [tools/c2_nd/nd_stage_pre.py](../c2_nd/nd_stage_pre.py.md) (line 19, import)
- [tools/c2_readout/c2_driver.py](c2_driver.py.md) (line 22, import)
- [tools/c2_readout/c2_oracle.py](c2_oracle.py.md) (line 21, import)
- [tools/c2_readout/c2_registry.py](c2_registry.py.md) (line 23, import)
- [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 22, import)
- [tools/c2_readout/c2_stage_post.py](c2_stage_post.py.md) (line 15, import)
- [tools/c2_readout/c2_stage_pre.py](c2_stage_pre.py.md) (line 21, import)

## Top-level constants

- `CHUNK`
- `LINEAGE`
- `METER_FILES`
- `MODEL_REASONS`
- `NAMED`
- `NEEDLE`
- `OWN_GATES`
- `PAYLOAD_DIRS`
- `REASONS`
- `SKIP_DIRS`
- `SPLITS`
- `STORE_SUFFIXES`

## Classes and functions

- **function `history_generator`** [L37-40]: `def history_generator(split, block) -> np.random.Generator`
- **function `sequence_ids`** [L43-45]: `def sequence_ids(split, block) -> np.ndarray`
- **function `sample_block`** [L48-55]: `def sample_block(T, E_canon, pi, split, block) -> tuple` - One HMMSampler.sample(4096, rng) call; w33 and the latent states dropped at once.
- **function `sample_split`** [L58-66]: `def sample_split(T, E_canon, pi, split, blocks) -> tuple` - Blocks 0..blocks-1 in block order: canonical uint8 [n, 32], sequence ids, panels.
- **function `lowest`** [L69-70]: `def lowest(seq_ids, n) -> np.ndarray`
- **function `k_y`** [L74-77]: `def k_y(b31, coords) -> np.ndarray` - k_Y(H) = +1 iff ybar(b31(H)) < 11/2, else -1 (toward the interior; fy_alt.py).
- **function `y_donor`** [L80-90]: `def y_donor(canon32, k) -> tuple` - H^Y = (6a + (b + k) on w1..w31, w32) and Y_def; an off-grid row is OFF in full (never
- **function `donors4`** [L93-95]: `def donors4(canon32, k) -> tuple` - (H, H+, H-, H^Y) in ROLES order (c1_oracle.donors for the first three).
- **function `role_arrays`** [L98-104]: `def role_arrays(canon32, k) -> dict` - {role: (tokens, rows)}: every row for H, H+, H-; the Y_def rows only for H^Y.
- **function `rho_m_index`** [L107-111]: `def rho_m_index(coords, m) -> np.ndarray` - idx[i] = the state with coordinates ((x_i + m) mod 12, y_i), one grid cell per unit.
- **function `history_table`** [L115-130]: `def history_table(canon32, seq_ids, panel, k) -> dict` - Canonical tokens, ids, panels, k_Y, Y_def and the four digest columns ("" where H^Y is
- **function `table_roles`** [L133-134]: `def table_roles(table) -> dict`
- **function `table_digests`** [L137-141]: `def table_digests(table) -> set`
- **function `coverage_tally`** [L168-170]: `def coverage_tally(flags) -> dict` - Rows per reason key, in the given order; a row counts under every reason it carries.
- **function `file_sha`** [L189-194]: `def file_sha(path) -> str`
- **function `contains_scope`** [L197-205]: `def contains_scope(path, needle=NEEDLE) -> bool` - True iff the file bytes contain `needle` (1 MiB chunks, len(needle) - 1 bytes overlap).
- **function `_rel`** [L208-215]: `def _rel(path, base)` - The posix path of `path` relative to `base`, or None if it lies outside.
- **function `_walk`** [L218-222]: `def _walk(top, skip=())`
- **function `_scanned`** [L225-233]: `def _scanned(rel_parts) -> bool`
- **function `_norm`** [L236-237]: `def _norm(mapping) -> dict`
- **function `_pinned`** [L240-242]: `def _pinned(rel, sha, pins) -> bool` - A byte copy of a pinned file at the same repository-relative path (e.g. main's merge).
- **function `namespace_scan`** [L245-270]: `def namespace_scan(root=None, pinned=None, lineage=None) -> dict` - G0 (vi): every file of the §4.4 file set whose bytes contain "c2-v1" must be pinned
- **function `_meter_file`** [L273-278]: `def _meter_file(rel) -> bool`
- **function `store_admission`** [L281-293]: `def store_admission(store, lineage, first_sampling) -> dict` - G0 (vii): every store file is meter bookkeeping or recognised with its exact sha256; at
- **function `_own_suffix_ok`** [L299-308]: `def _own_suffix_ok(name, rows, stage) -> bool` - R-0107-2: STAGES.jsonl gets exactly one STARTED line of this stage; GATES.jsonl only
- **function `own_records`** [L311-337]: `def own_records(store, stage, lineage) -> dict` - G0 (vii), R-0107-2 (D-0107-1): {name: sha256} for GATES.jsonl and STAGES.jsonl, each an


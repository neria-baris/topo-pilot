# `tools/x6_stage0/x6_run.py`

- Source: [tools/x6_stage0/x6_run.py](../../../../../tools/x6_stage0/x6_run.py)
- Kind: python
- Lines: 380

## Module docstring

> X6 stage 0: Monte Carlo, G5-G7, PoE, labels and outcome (D), S0, store lineage, per-gate
> records, preflight, run, report and CLI (X6-FROZEN-v1 sections 6-10; API.md 6). Every Decimal
> operation runs in an explicit 80-, 120- or 200-digit context (x6_dp.CTX, x6_dp.C200).

## Imports

### Internal (repo files)

- `import x6_model` -> [tools/x6_stage0/x6_model.py](x6_model.py.md) (line 18, via same directory)
- `import x6_dp` -> [tools/x6_stage0/x6_dp.py](x6_dp.py.md) (line 19, via same directory)
- `import x6_exact` -> [tools/x6_stage0/x6_exact.py](x6_exact.py.md) (line 20, via same directory)
- `from independent_reference import decimal_suffix_posterior, enumerate_posterior` -> [tests/oracle_profile/independent_reference.py](../../tests/oracle_profile/independent_reference.py.md) (line 21, via unique basename)
- `from oracle_profile import suffix_posterior` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 22, via unique basename)
- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 23, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 24, via package root)
- `from topo_pilot.oracle import BayesFilter, FutureOperator` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 25, via package root)
- `from x6_model import ANCHOR_NB, BATCH, LADDER, MC_ARMS, MC_FLOOR, MC_K, MC_ROWS, MC_STREAM, N_CHECK, THETA_ROW, TOL_DEC, TOL_LOGEV, TOL_NUM, WINDOWS` -> [tools/x6_stage0/x6_model.py](x6_model.py.md) (line 26, via same directory)
- `from x6_store import G7_DP_ITEMS, G7_ITEMS, ORDER, OUTCOMES, S8_NOT_RUN, _typed, decide, label_cert, labels, scratch_ok, write_preflight, ALLOWLIST, ATTEMPT_RE, GATES, KERNEL_DIFF_EXPECTED, MAILBOX, METER_FILES, PF_SUITES, PROTECTED_PATHS, VOLATILE_KEYS, _load, _norm, allowlist_ok, archive_attempt, canonical_json, compare_attempt, jsonable, kernel_diff_ok, lineage_precheck, read_manifest, reports_equal, s0_check, s0_lineage, sha256_file, strip_volatile, write_gate, write_manifest, write_marker` -> [tools/x6_stage0/x6_store.py](x6_store.py.md) (line 28, via same directory)

### External (third-party)

- `numpy` (lines 16)

### Standard library

- `__future__` (lines 5)
- `argparse` (lines 7)
- `fractions` (lines 12)
- `functools` (lines 13)
- `hashlib` (lines 8)
- `math` (lines 9)
- `pathlib` (lines 14)
- `sys` (lines 10)
- `time` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/x6_stage0/test_x6_stage0_dp.py](../../tests/x6_stage0/test_x6_stage0_dp.py.md) (line 28, import)
- [tests/x6_stage1/test_b_seed_pool_reg.py](../../tests/x6_stage1/test_b_seed_pool_reg.py.md) (line 27, import)
- [tools/x6_stage1/x6s1_data.py](../x6_stage1/x6s1_data.py.md) (line 265, import)
- [tools/x6_stage1/x6s1_stage_pre.py](../x6_stage1/x6s1_stage_pre.py.md) (line 28, import)

## Top-level constants

- `SIG`
- `_CF`

## Classes and functions

- **function `sample`** [L40-43]: `def sample(arm: str, n: int, tree)`
- **function `indicator_se`** [L44-44]: `def indicator_se(p, n: int) -> float`
- **function `mc_check`** [L45-45]: `def mc_check(estimate, exact, se)`
- **function `_mc`** [L46-48]: `def _mc(est, exact, se) -> dict`
- **function `indicator_check`** [L49-49]: `def indicator_check(hits: int, n: int, p) -> dict`
- **function `sample_se`** [L50-50]: `def sample_se(x) -> float`
- **function `_mean`** [L51-51]: `def _mean(x, exact) -> dict`
- **function `_flt`** [L52-52]: `def _flt(value, tol) -> dict`
- **function `_bf`** [L53-53]: `def _bf(m: dict)`
- **function `_fo`** [L54-54]: `def _fo(m: dict)`
- **function `_batches`** [L55-55]: `def _batches(toks)`
- **function `_clean`** [L56-56]: `def _clean(*a) -> bool`
- **function `_maxabs`** [L57-57]: `def _maxabs(a, b) -> float`
- **function `_kl_rows`** [L58-61]: `def _kl_rows(p, q)`
- **function `_cf_float`** [L64-69]: `def _cf_float(arm: str, h) -> tuple`
- **function `_filter_check`** [L70-84]: `def _filter_check(arm: str, toks, hook=None) -> dict` - Unchanged BayesFilter b_t, q_t (t <= 32, and q_0) against the closed form (Theorem 1).
- **function `_decimal_reference`** [L87-118]: `def _decimal_reference(na) -> dict` - Section 9.5 reference set: Decimal (80 digits; edge cases also 120) against Fractions.
- **function `gate_G5`** [L120-136]: `def gate_G5(rows) -> dict`
- **function `_cue_part`** [L140-142]: `def _cue_part(m: int, w) -> np.ndarray` decorators: @lru_cache(maxsize=None)
- **function `_row_certified`** [L144-146]: `def _row_certified(n: int, w, z: int) -> bool` decorators: @lru_cache(maxsize=None) - The row's exact class (n, y, v_32, kappa, z) is certified row-KL >= THETA_ROW.
- **function `_row_info`** [L147-152]: `def _row_info(toks, labels) -> list`
- **function `gate_G6`** [L154-202]: `def gate_G6(rows, g4) -> dict`
- **function `_zero`** [L205-205]: `def _zero(enc) -> bool`
- **function `_pos`** [L206-206]: `def _pos(enc) -> bool`
- **function `_q_diffs`** [L207-213]: `def _q_diffs(toks, base: str, others) -> dict`
- **function `_controls_float`** [L214-226]: `def _controls_float(rows) -> dict` - NOCUE (NA vs TRIV under E_nc, uniform fibre, base walk) and TOKPERM maximum errors.
- **function `gate_G7`** [L228-272]: `def gate_G7(rows, g3, g4, s8: bool = False) -> dict`
- **function `poe`** [L274-286]: `def poe(rows) -> dict`
- **function `_call`** [L289-293]: `def _call(fn, *args) -> dict`
- **function `run`** [L295-362]: `def run(store, dispatch) -> dict`
- **function `main`** [L364-377]: `def main(argv=None) -> int`


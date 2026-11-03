# `tools/hwsu/hwsu_oracle.py`

- Source: [tools/hwsu/hwsu_oracle.py](../../../../../tools/hwsu/hwsu_oracle.py)
- Kind: python
- Lines: 194

## Module docstring

> HWSU oracle quantities, KO cases, Decimal rows, Lemma P arrays, problem O (API.md §3; protocol
> §2.2, §2.3, §2.6, §4.2, §5.2). All arithmetic is in canonical symbol order (D-1).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](hwsu_config.py.md) (line 6, via same directory)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../c1prime/c1_oracle.py.md) (line 9, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../c2_readout/c2_attrib.py.md) (line 10, via unique basename)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../c2_readout/c2_code.py.md) (line 11, via unique basename)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../c2_readout/c2_decide.py.md) (line 12, via unique basename)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](../c2_readout/c2_oracle.py.md) (line 13, via unique basename)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](../c2_readout/c2_stats.py.md) (line 14, via unique basename)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 15, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 16, via unique basename)
- `from topo_pilot.oracle import BayesFilter` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 17, via package root)

### External (third-party)

- `numpy` (lines 7)

### Standard library

- `__future__` (lines 4)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_a_of_gates.py](../../tests/hwsu/test_a_of_gates.py.md) (line 16, import)
- [tests/hwsu/test_a_of_lemmas.py](../../tests/hwsu/test_a_of_lemmas.py.md) (line 17, import)
- [tests/hwsu/test_a_of_oracle.py](../../tests/hwsu/test_a_of_oracle.py.md) (line 15, import)
- [tests/hwsu/test_a_u2_estimand.py](../../tests/hwsu/test_a_u2_estimand.py.md) (line 18, import)
- [tests/hwsu/test_a_u2_known.py](../../tests/hwsu/test_a_u2_known.py.md) (line 17, import)
- [tests/hwsu/test_b_of_obligation.py](../../tests/hwsu/test_b_of_obligation.py.md) (line 326, import)
- [tools/hwsu/hwsu_dry.py](hwsu_dry.py.md) (line 11, import)
- [tools/hwsu/hwsu_dry_b.py](hwsu_dry_b.py.md) (line 9, import)
- [tools/hwsu/hwsu_of.py](hwsu_of.py.md) (line 11, import)
- [tools/hwsu/u2/hwsu_dry2b.py](u2/hwsu_dry2b.py.md) (line 15, import)
- [tools/hwsu/u2/hwsu_e2.py](u2/hwsu_e2.py.md) (line 12, import)
- [tools/hwsu/u2/hwsu_gates.py](u2/hwsu_gates.py.md) (line 15, import)
- [tools/hwsu/u2/hwsu_known.py](u2/hwsu_known.py.md) (line 14, import)

## Top-level constants

- `CASES`
- `ORACLE`
- `_CAT`
- `_EXPECT`

## Classes and functions

- **function `helmert`** [L23-29]: `def helmert(n=36)`
- **function `arm_oracle`** [L32-36]: `def arm_oracle(T, E, pi, canon32, coords) -> dict`
- **function `suffix_oracle`** [L39-56]: `def suffix_oracle(T, E, pi, canons, coords, suffix_len=4) -> list`
- **function `m4_check`** [L59-63]: `def m4_check(T, E, pi, canon32, coords, m4) -> dict`
- **function `pair_core`** [L66-68]: `def pair_core(o1, o2) -> dict`
- **function `ko_logits`** [L72-79]: `def ko_logits(o, s, case)`
- **function `readout_A`** [L82-83]: `def readout_A(d, z1, z2, N)`
- **function `ko_identities`** [L86-96]: `def ko_identities(G, A) -> dict`
- **function `ko_categories`** [L105-129]: `def ko_categories(G, A, seed, alpha=None, draws=None) -> dict`
- **function `decimal_rows`** [L133-153]: `def decimal_rows(T, E, pi, a1, a2, o1, o2, s1, pc, k=None) -> dict`
- **function `lemma_p_arrays`** [L157-165]: `def lemma_p_arrays(o1, o2, s1, pc) -> dict`
- **function `label_share`** [L168-172]: `def label_share(qbar1, qbar2)`
- **function `problem_o`** [L175-183]: `def problem_o(o_fit, w32_fit, K=None, euclidean=False) -> dict`
- **function `share_arrays`** [L186-190]: `def share_arrays(pr, pc, o1, o2) -> dict`
- **function `share_guard_beta`** [L193-194]: `def share_guard_beta(pr, pc, dy) -> float`


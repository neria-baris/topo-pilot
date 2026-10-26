# `tests/c2_nd/test_a_family.py`

- Source: [tests/c2_nd/test_a_family.py](../../../../../tests/c2_nd/test_a_family.py)
- Kind: python
- Lines: 396

## Module docstring

> Author A (job 0121): T-FAMILY-ND (the exhaustive grid of §8.4) and T-EDGE (MD-9).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](../../tools/c2_nd/nd_config.py.md) (line 22, via sys.path edit)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../../tools/c2_readout/c2_decide.py.md) (line 25, via unique basename)
- `import nd_decide` -> [tools/c2_nd/nd_decide.py](../../tools/c2_nd/nd_decide.py.md) (line 26, via sys.path edit)

### External (third-party)

- none

### Standard library

- `__future__` (lines 10)
- `fractions` (lines 15)
- `functools` (lines 12)
- `itertools` (lines 13)
- `pathlib` (lines 16)
- `sys` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `str(REPO / 'tools' / 'c2_nd')` -> `tools/c2_nd`

## Imported by

- none

## Top-level constants

- `D_BASES`
- `EDGES`
- `G`
- `KAPPAS`
- `NEC_KEYS`
- `NM_BASES`
- `NM_CATS`
- `NR_BASES`
- `NR_CATS`
- `PATS`
- `REPO`
- `R_CASE`

## Classes and functions

- **function `_b`** [L36-41]: `def _b(cfg)`
- **function `_s`** [L44-45]: `def _s(v)`
- **function `_fs`** [L48-49]: `def _fs(x)`
- **function `_signs`** [L52-53]: `def _signs(b)`
- **function `_cat`** [L56-63]: `def _cat(sg, z1, z5, w, v, names)` - §2.3 table (N-R, N-M): returns the one declared category, else INC(/NUMERICAL).
- **function `_prereq`** [L66-74]: `def _prereq(b, y_active, flags)` - RESP (L(V3x) > g) and SPEC (U(Y1) < -g when Y1 is active) come first (§4.3).
- **function `nr_expect`** [L77-87]: `def nr_expect(b, y_active)`
- **function `_got`** [L90-94]: `def _got(r, flags)`
- **function `d_expect`** [L101-118]: `def d_expect(b, y_active)`
- **function `nm_expect`** [L124-137]: `def nm_expect(b)`
- **function `nm_got`** [L140-145]: `def nm_got(r)`
- **function `nr_events`** [L149-165]: `def nr_events(k, M='')`
- **function `d_events`** [L168-178]: `def d_events(p, s_false)`
- **function `nm_events`** [L181-186]: `def nm_events(t, k)`
- **function `_forced`** [L189-191]: `def _forced(signs, mu)`
- **function `_cover`** [L194-202]: `def _cover(cache, truth, mu, listed)`
- **function `_grid`** [L205-217]: `def _grid(stats, fixed, model, expect, got, cats, flags)` - Every sign pattern of `stats`: the rule equals the protocol table (so the categories
- **test `test_family_nr_grid`** [L221-236]: `def test_family_nr_grid()`
- **test `test_family_d_grid`** [L239-253]: `def test_family_d_grid()`
- **test `test_family_nm_grid`** [L256-270]: `def test_family_nm_grid()`
- **test `test_family_prerequisites_resp_and_spec`** [L273-288]: `def test_family_prerequisites_resp_and_spec()`
- **function `_kc`** [L298-302]: `def _kc(case, y_active=False, **kw)`
- **test `test_family_kc_cases_and_gates`** [L305-326]: `def test_family_kc_cases_and_gates()`
- **test `test_family_kc_contradiction_blocks_not_used_and_kcr_does_not`** [L329-339]: `def test_family_kc_contradiction_blocks_not_used_and_kcr_does_not()`
- **test `test_edge_every_threshold_array`** [L358-373]: `def test_edge_every_threshold_array()`
- **test `test_edge_named_cases`** [L376-396]: `def test_edge_named_cases()`


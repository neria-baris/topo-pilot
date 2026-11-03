# `tools/hwsu/u2/hwsu_dry2b.py`

- Source: [tools/hwsu/u2/hwsu_dry2b.py](../../../../../../tools/hwsu/u2/hwsu_dry2b.py)
- Kind: python
- Lines: 259

## Module docstring

> HWSU model-phase dry run DRU, cases that need no training (API_U2.md section 6; split from
> hwsu_dry2 by size): KS-P, KS-RULES and DRU3-DRU9. Synthetic worlds and roots only, scope
> hwsu-dry-v1, nothing under the project root. DRU1, DRU2 and DRU-REG stay in hwsu_dry2, the only
> file that may reference hwsb_train.train, hwsc_data.make_train_dev_c and
> hwsc_registry_build.build (R-0223-3).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../hwsu_config.py.md) (line 9, via unique basename)
- `import hwsu_bind_u2` -> [tools/hwsu/u2/hwsu_bind_u2.py](hwsu_bind_u2.py.md) (line 10, via same directory)
- `import hwsu_decide` -> [tools/hwsu/u2/hwsu_decide.py](hwsu_decide.py.md) (line 11, via same directory)
- `import hwsu_dry` -> [tools/hwsu/hwsu_dry.py](../hwsu_dry.py.md) (line 12, via unique basename)
- `import hwsu_known` -> [tools/hwsu/u2/hwsu_known.py](hwsu_known.py.md) (line 13, via same directory)
- `import hwsu_model` -> [tools/hwsu/u2/hwsu_model.py](hwsu_model.py.md) (line 14, via same directory)
- `import hwsu_oracle` -> [tools/hwsu/hwsu_oracle.py](../hwsu_oracle.py.md) (line 15, via unique basename)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](../hwsu_records.py.md) (line 16, via unique basename)
- `import u2` -> [tools/hwsu/u2/__init__.py](__init__.py.md) (line 17, via unique basename)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../../c1prime/c1_oracle.py.md) (line 23, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../x4_circle_history/stage_records.py.md) (line 25, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../c1prime/c1_records.py.md) (line 26, via unique basename)

### External (third-party)

- `numpy` (lines 24)

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 20)
- `itertools` (lines 18)
- `json` (lines 19)
- `pathlib` (lines 21)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsu/u2/hwsu_dry2.py](hwsu_dry2.py.md) (line 13, import)

## Top-level constants

- none

## Classes and functions

- **function `_res`** [L29-30]: `def _res(ok, **details) -> dict`
- **function `_chain_laws`** [L34-55]: `def _chain_laws(P=4)`
- **function `ks_p`** [L58-100]: `def ks_p(base) -> dict` - Lemma P2 pair moment = conditional covariance (exact Fractions) and Lemma J (floats).
- **function `_bj`** [L103-105]: `def _bj(l1, u1, l3, u3, la, g=0.01) -> dict`
- **function `ks_rules`** [L108-136]: `def ks_rules(base) -> dict`
- **function `_ko_world`** [L140-145]: `def _ko_world(n=256)`
- **function `dru3`** [L148-163]: `def dru3(base, ctx=None) -> dict`
- **function `dru4`** [L166-175]: `def dru4(base, ctx=None) -> dict`
- **function `dru5`** [L178-189]: `def dru5(base, ctx=None) -> dict`
- **function `dru6`** [L192-209]: `def dru6(base, ctx=None) -> dict`
- **function `dru7`** [L212-226]: `def dru7(base, ctx=None) -> dict`
- **function `dru8`** [L229-242]: `def dru8(base, ctx=None) -> dict`
- **function `dru9`** [L245-259]: `def dru9(base, ctx=None) -> dict`


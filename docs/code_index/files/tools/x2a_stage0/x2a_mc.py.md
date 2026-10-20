# `tools/x2a_stage0/x2a_mc.py`

- Source: [tools/x2a_stage0/x2a_mc.py](../../../../../tools/x2a_stage0/x2a_mc.py)
- Kind: python
- Lines: 368

## Module docstring

> X2a stage 0, part 2 (X2A-FROZEN-v1; API.md): seeded sampling, batched filter statistics,
> windows, blocks, additive score, credits, SE / intervals / Hoeffding, decision labels, G3, G4, D,
> G5 and the descriptive Monte Carlo (N-local, P-ref, long horizon).

## Imports

### Internal (repo files)

- `import x2a_model` -> [tools/x2a_stage0/x2a_model.py](x2a_model.py.md) (line 15, via same directory)
- `from independent_reference import decimal_suffix_posterior` -> [tests/oracle_profile/independent_reference.py](../../tests/oracle_profile/independent_reference.py.md) (line 16, via unique basename)
- `from oracle_profile import suffix_posterior` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 17, via unique basename)
- `from topo_pilot.contracts import SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 20, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 21, via package root)
- `from topo_pilot.oracle import BayesFilter, LastSymbolPosterior, context_gain` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 22, via package root)

### External (third-party)

- `numpy` (lines 11)
- `scipy` (lines 18)

### Standard library

- `__future__` (lines 5)
- `math` (lines 7)
- `pathlib` (lines 9)
- `sys` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 13: `[p for p in (str(Path(__file__).resolve().parent),) if p not in sys.path]` -> `tools/x2a_stage0`

## Imported by

- [tests/x2a_stage0/test_x2a_stage0.py](../../tests/x2a_stage0/test_x2a_stage0.py.md) (line 36, import)
- [tests/x2a_stage0/test_x2a_stage0_ph.py](../../tests/x2a_stage0/test_x2a_stage0_ph.py.md) (line 29, import)
- [tools/x2a_stage0/x2a_ph.py](x2a_ph.py.md) (line 16, import)

## Top-level constants

- `CURVE_T`
- `MC_SIZES`

## Classes and functions

- **function `entropy_b`** [L30-32]: `def entropy_b(p)`
- **function `_hb`** [L34-35]: `def _hb(mA, mB)`
- **function `mass_pi`** [L37-38]: `def mass_pi(b, n_A=NA)`
- **function `mass_logit`** [L40-42]: `def mass_logit(b, n_A=NA)`
- **function `expit_pi`** [L44-45]: `def expit_pi(s)`
- **function `decision`** [L47-49]: `def decision(pi_d, tau=TAU)`
- **function `credit`** [L51-53]: `def credit(pi_full, pi_d, tau=TAU)`
- **function `additive_score`** [L55-58]: `def additive_score(Tt, Et, pit, tokens, n_A=NA, block=8, n_blocks=4)`
- **function `strat_mean_se`** [L60-63]: `def strat_mean_se(x_A, x_B)`
- **function `interval`** [L65-66]: `def interval(mean, se, z=Z99)`
- **function `hoeffding`** [L68-69]: `def hoeffding(R, n, delta)`
- **function `_lu`** [L71-72]: `def _lu(m, se, hw)`
- **function `p3_label`** [L74-76]: `def p3_label(d3, se, hw=None)`
- **function `p4_label`** [L78-81]: `def p4_label(i8, se8, i32, se32, hw8=None, hw32=None)`
- **function `a3_label`** [L83-84]: `def a3_label(d_add, se, hw=None)`
- **function `scientific_outcome`** [L86-89]: `def scientific_outcome(p3, p4, a3)`
- **function `hoeffding_label`** [L91-95]: `def hoeffding_label(S, delta=0.01)`
- **function `sample`** [L98-100]: `def sample(T, E, n, rng, n_obs=33)`
- **function `_kl`** [L102-103]: `def _kl(p, r)`
- **function `_batch`** [L105-136]: `def _batch(m, tok, label, keep)`
- **function `row_stats`** [L138-143]: `def row_stats(model, tokens, batch=2048, label=None, keep=0)`
- **function `_ms`** [L145-151]: `def _ms(A, B, key, R=None, n=None, f=None)`
- **function `summarise`** [L153-186]: `def summarise(A, B)`
- **function `_max`** [L189-190]: `def _max(acc, key, val)`
- **function `gate_G3`** [L192-237]: `def gate_G3(m, tok_A, tok_B, exact=None, n_rows=2 ** 13, chunk=1024)`
- **function `gate_G4`** [L239-261]: `def gate_G4(exact, S)`
- **function `gate_D`** [L263-277]: `def gate_D(S)`
- **function `control_tokens`** [L279-285]: `def control_tokens(models, tree)`
- **function `_pi_dev`** [L287-295]: `def _pi_dev(m, toks, batch=2048, full=False)`
- **function `gate_G5`** [L297-318]: `def gate_G5(models, exact, ctl, main_tok, n_swap=2 ** 13)`
- **function `descriptive_mc`** [L320-336]: `def descriptive_mc(models, ctl, exact, keep_pref=4096)`
- **function `long_horizon`** [L338-368]: `def long_horizon(m, tree, n=2 ** 15, ts=(32, 48, 64, 96, 128), batch=4096)`


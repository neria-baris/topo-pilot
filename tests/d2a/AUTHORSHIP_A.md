# tests/d2a (author A): independence record, job 0028 (D-2a)

**Author:** independent test author A (a Claude Code subagent), 2026-10-15. I am not the
implementer. I wrote these tests before any implementation existed, from the frozen protocol and
the API contract only.

## Files written

| File | Lines | Test functions | Ids |
|---|---|---|---|
| `tests/learner/test_multihorizon.py` | 399 | 18 | T-TRUNK, T-HEAD, T-CAUS, T-TARGET, T-LOSS, T-GRAD, T-RNG, T-LOAD, T-DECAY; horizon ∉ {2, 3}; requested hooks only |
| `tests/d2a/test_a_world.py` | 238 | 14 | T-SEED (streams, ids, `master_collisions`, `bin_positions`); pool table; `process`, `world_kernels`; `decision_rows`; `pad`; test-pool guard (S9) |
| `tests/d2a/test_a_templates.py` | 155 | 9 | T-TPL; `registered_templates`; `template_hashes`; `g0_tpl` |
| `tests/d2a/test_a_targets.py` | 290 | 12 | T-FIX; `g0_fix`; T-SUPP; G0-NUM identities on a small batch; the C⊕C oracle null; T-PRIOR |
| `tests/d2a/test_a_pad.py` | 74 | 1 (7 cases) | T-PAD |
| `tests/d2a/AUTHORSHIP_A.md` | this file | | |

## What I read

- `agent-handoff/planning/responses/D2A-FROZEN-v1.md`. I read lines 1–977 in full: §0–§11.4 and the start of §11.5. I used grep to find the test ids in the rest of the file.
- `topo-pilot-d2a/tools/d2a/API.md`, in full.
- Read-only production code in `topo-pilot-d2a`:
  - `src/topo_pilot/learner/{__init__,config,model,trainer,stage}.py`;
  - `contracts/errors.py`, plus the `SeedTree` part of `ids.py`, `Checkpoint`, `ObservationSet`, `ArtifactMeta` and the meta-writing part of `store.py`;
  - `contracts/testing.py` (`tiny_observations` only) and `contracts/layout.py` (`model_inputs` and `targets`);
  - `dataset/public.py`, plus the `HMMSampler` part of `sampler.py`;
  - `oracle/_filter.py` (the `BayesFilter` part), `oracle/_common.py::as_model` and part of `oracle/_futures.py`;
  - `tools/d1_seam/d1_seam.py`, in full;
  - `tools/x4_oracle_profile/oracle_profile.py`: `suffix_posterior`, `_model_arrays` and `_checked_k`.
- Existing tests, for style only:
  - `tests/learner/conftest.py`, `test_training.py` and `test_checkpoint.py`;
  - `tests/learner/test_trainer_golden.py`, the already-committed commit-A golden test;
  - the header of `tests/d1_seam/test_d1_seam.py`;
  - `tests/d1_seam/AUTHORSHIP.md`;
  - `pyproject.toml` (markers and ruff settings).

## What I did not read

- No `tools/d2a/*.py`. When I listed `tools/d2a/`, it held only `API.md`.
- No `src/topo_pilot/learner/multihorizon.py`. It did not exist.
- Nothing under `C:/Users/pc2/AppData/Local/Temp/claude/`.
- No file by author B (`tests/d2a/test_b_*.py`). One deviation is recorded below.
- No git history. I ran no git command and made no commit.

## What I executed

All runs used the venv Python with `PYTHONPATH=topo-pilot-d2a/src` and with TEMP/TMP set to `tmp-0028/`. The scratch scripts are in `tmp-0028/`.

**Read-only checks of existing code (`a_check.py` … `a_check4.py`, under 5 CPU-seconds in total).**
- `d1_seam.exact_history` at my two hand templates (t = 16 and t = 28). Both gave π = 1/4 and 3/4, b_C = b_M with y-law (2/3, 1/3, 0) on column 3, Q1 = (1/5, 1/5, 3/5, 0, 0), pair TV of J2 = 1/150, distant-marginal TV = 1/150 and identical final 8-symbol windows.
- My re-implementation of the API enumeration order: counts 48 and 9,216, and the hand templates sit at indices 16 and 6,218.
- My independent S2/S3 path enumeration. It gave (3, 4, 8, 9) and the 24 entries of API S3.
- My Fraction J3, checked against `exact_history` J. Its first-two-symbol marginal is exact.
- The exact μT^k priors against the float matrix power.
- `BayesFilter` from those priors on a 400-episode test batch.

**Tooling only.**
- Small Python text-replacement scripts edited my own files.
- `ruff check` ran on my files by name, with `--fix` for import order only. I did not run `ruff format`.

**Never run.** The tests themselves; they cannot run until the modules exist.

**Deviation.** I ran `ruff check` once over the `tests/d2a/` directory. Its summary listed `test_b_resource.py:9` and `test_b_targets.py:9` with code I001. I saw no content of those files and did not open them; every later lint run named my files only.

Ruff places `topo_pilot.learner.multihorizon` among the third-party imports while the module is missing. I put it back in the first-party block by hand, so the files are lint-clean under `known-first-party = ['topo_pilot']`, which is the grouping that will apply once the module exists.

## Independence of the references

The tests call the module functions under test. Every expected value comes from one of these sources:
- `d1_seam.exact_history` and `exact_model` (Fractions);
- hand values;
- independent code in the test files: a Fraction J3, a column-3 read-string enumeration, Fraction μT^k priors, a re-implementation of the template order, the bin rule and the joint index;
- `SeedTree` streams named in the API;
- the production `BayesFilter` run from explicit priors.

No reference imports `d2a_targets` or `d2a_world` target code.

## Ambiguities and the reading chosen

1. **`master_collisions` return value.** The test assumes it returns the paths of the offending `meta.json` files, and compares them as resolved `Path`s. A hit is read as a `seed_map` value equal to DATA or MODEL, or the master's digits appearing in the `config` text. The planted hits use exact values.
2. **`template_hashes`.** The test assumes a hex sha256 string per pair, compared case-insensitively.
3. **POOLS seed slot.** The API marks the seed of unseeded pools "—". The test does not check that slot; it checks only `(proc, n, split)`, and the seed where one is given.
4. **Sequence ids.** No API function exposes ids without `save_pools`, which I may not call. The test checks the order of `SEQ_CODE` (1..21) and that the ranges `SEQ_CODE·2^32 + arange(n)` are disjoint.
5. **Stream scope types.** The seed `s` and the bin id `b` are passed as ints, literally as written in the API.
6. **Tolerances the protocol does not state:**
   - T-PAD and T-TARGET use 1e-6, the T-CAUS tolerance.
   - T-LOSS hand values use 1e-12 in float64.
   - The G0-FIX TV values use 1e-12, the J2 entry tolerance.
   - T-PRIOR equalities of posterior vectors and predictives use 1e-11, the protocol's window cross-check tolerance. The prior itself uses 1e-12.
   - The C⊕C null tests world-conditional TVs of Q1, J2 and J3 at 1e-12.
7. **Input length of `oracle_at`.** Named histories are passed as `[1, t]` arrays, not padded. Padding H_EDGE (which ends in σ2) with σ0 gives an impossible continuation, and API §2.2 says only `tokens[:, :t]` are used.
8. **The `D2A_STAGE` guard.** The test requires `D2A_STAGE == "3"` exactly, so "33" raises LEAKAGE. The admitted case is checked only as "not LEAKAGE" on an empty tmp store.
9. **Unknown hook.** `MultiHorizonLM.forward` with an unknown hook is expected to raise UNKNOWN_HOOK, because the §4.5 code delegates to the parent forward.
10. **Additions beyond the listed ids.** All follow the protocol or the API text literally:
    - T-GRAD also checks that pos_emb gradients at rows > p are ≤ 1e-6 and that `unembed` receives no gradient.
    - T-HEAD checks bitwise equality with `0.02·randn` drawn from `Generator().manual_seed(aux_seed)`, with k = 2 drawn before k = 3.
    - `check_causal_joint` must leave the global RNG untouched and must catch a planted future-leaking head.
    - The Trainer must actually use `loss_fn`: the joint heads move after 2 steps.
    - Step-0 dev CE must be bitwise equal across H1, H2 and H3.
    - `g0_fix()` and `g0_tpl()` must return PASS with every check true.
    - Exact G0-TPL values are checked on a subsample of the registered templates.
    - The G0-NUM identities are checked on a 400-episode batch from a test-only SeedTree master (4242).
11. **T-LOAD "malformed state".** Read as garbage bytes, a payload without a `"model"` key, or a config whose shapes do not match. An H1 checkpoint loaded with `load_multi_horizon(·, 2)` must raise INVALID_CONFIG.
12. **File name.** Protocol §11.4 names `tests/d2a/AUTHORSHIP.md`. Following the task instruction, this file is `AUTHORSHIP_A.md`.

## Correction round (job 0029, R7)

The job 0029 review (R7) ruled that D2A-FROZEN-v1 §2.4 registers 19 pools: train-s1..s4, dev-s1..s4, trainN-s1/s2, devN-s1/s2, stage0, stage0N, cal, val, test, valN and testN. The "21" in API.md §2.1 is a slip. I had copied that 21 into three assertions in `test_a_world.py`, although ORDER and EXPECTED list 19 pools. Those three assertions are now 19: `len(ORDER)` in `test_pool_table_follows_api`, and the distinct-seed and distinct-first-draw counts in `test_T_SEED_streams_pairwise_distinct`. Nothing else changed. This round I took the ruling as quoted in the task and opened no files other than these two. I compiled the file with `py_compile` and did not run pytest.

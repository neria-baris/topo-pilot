# Authorship record: independent test author A (job 0121)

Author: clean-context Claude subagent (author A: algebra, statistics, decoy maths), 2026-10-26.
Branch `c2nd-impl`, worktree `topo-pilot-c2nd`, started at 28e54b4.

## Files
| File | Items (TEST_PLAN §2) |
|---|---|
| `test_a_identity.py` | T-N1, T-LNSCALE, T-LEAK, T-DOSE |
| `test_a_known.py` | T-NEC-KNOWN (with erratum E-C2ND-1), T-RULE6, T-PROJ-ND, T-COPY |
| `test_a_decoy_maths.py` | T-MOVE, T-GAIN, T-ILLUSION |
| `test_a_family.py` | T-FAMILY-ND, T-EDGE |
| `test_a_inference.py` | T-RULES-ND, T-BOOT-ND, T-LADDER-ND |

## What I read
- `agent-handoff/jobs/0121/task.md`; `agent-handoff/jobs/0116/review.md` (rulings R-0116-1..5,
  erratum E-C2ND-1).
- `tools/c2_nd/TEST_PLAN.md` and `tools/c2_nd/API.md` (in full); `tools/c2_nd/PROTOCOL_C2ND_v1.md`
  §1-§10.1 and §11.3-§12; `tools/c2_nd/CONTRACT.json` (its key list and the blocks `families`
  to `tolerances`).
- Reused production code, read-only: `tools/c2_readout/c2_decide.py`, `c2_attrib.py`,
  `c2_code.py`, `c2_config.py`, `c2_stats.py` (P1 part), `c2_driver.py` (the `LogitPolicy`
  class only); `tools/c1prime/c1_endpoint.py` (head), `c1_means.py`, `c1_records.py`
  (`C1GateFailure`), `c1_fit.py` (`fwl_design`); `tools/x4_circle_history/precision.py`;
  `src/topo_pilot/analysis/x4f_scores.py` (`ledoit_wolf`).
- Directory listings of file names only: `tests/` and `tests/c2_readout/` (to check the pytest
  layout), `tools/c1prime/`; the pytest options in `pyproject.toml`.

## What I did not read
- No file `tools/c2_nd/*.py` was read, listed or searched (the only listing of `tools/c2_nd`
  named `*.md` and `*.json`).
- No test file or record of author B (`test_b_*.py`, `AUTHORSHIP_B.md`), and no file content of
  `tests/c2_readout/`.
- No store (`c2-readout-store`, `c2nd-store`, any other), no `00_READ_ME_FIRST*`, no
  `docs/research_summary/`.

## What I executed
- No test, no project import, no formatter. The only Python run was
  `X:/Downloads/topo-scratch/0121a/check.py` with `python -I`: it reads my own five files as
  text, runs `ast.parse` and `compile` in memory, and counts lines, long lines and CR bytes.
- Shell: `git` (log, status, add and commit of my files by name), `ls`, `wc`, `grep`, `sed`.

## API-AMBIGUITY and defects recorded in the tests
1. `nd_attrib.sigma(a3, eps)` (API §7.3): the formula `sqrt(np.var(a3, axis=1) + eps)` "on
   resid_post_3[:, 32]"; the test passes the 2-d position-32 rows.
2. `nd_decoy.adapter_identities(..., heads)` (API §6.5): the form of `heads` and the inputs of
   `pred_DNULLR`/`pred_DID` are not fixed; the tests pass `{kind: M'}` readout matrices
   (`n_out x p`) and check only the keys that need no rows.
3. `nd_decoy.dx(arrays, policy)` (API §6.5): the per-decoy array keys are not fixed; the tests
   pass the `c2_attrib.pair` keys (construction projector) for `DNULL` only.
4. `nd_attrib.d_stream(..., refit)` (API §7.3): only `refit["problem"]` is fixed; the tests add
   `P_S`, `P_G`, `Sigma`.
5. `nd_decide.statement_licence(kind, values)` (API §8.4): kinds not named; the flag names
   `rule6a`, `rule6b`, `rule6c`, `nested` are used.
6. `nd_decide.kc_case` (API §8.3) with the keys of `case_arrays` (API §7.3): no `Zc090`/`Zc100`
   reach a case, so `nr_model` there must not need them (the nested entry is not a KC statement).
7. `nd_decide.nr_variant_category(b, v, primary)`: `primary` is passed as the `nr_model` result
   dict (as `c2_decide.variant_category`); `d_model` is assumed to return the `r_model` keys
   (`resp`, `spec`, `coarse`, `endpoint_formed`, ...) plus `rule6b`.
8. API §8.4 says no licence template says "necessary" outside NECESSARY/NECESSARY_M, but the
   protocol's N-M KM3 sentence (§7.1) says "need not be shown necessary here"; only the
   "sufficient and necessary" rule is tested.
9. PLAN-DEFECT (T-ILLUSION (ii); protocol §5.1, §10.1 criterion 3): a decoy built with the
   Euclidean projector `B (B'B)^-1 B'` in place of the oblique `P_S` still has
   `C M' B = 0` and `M' P_S = 0` exactly (because `(I - P_E) B = 0`), so M0-D (vii) and DX
   must pass on it; the test asserts that algebra. The J-built decoy fails both, as specified.
10. E-C2ND-1 applied: the protocol's "half and half" known case is replaced by psi = 0.3, 0.7
    and 0.5.

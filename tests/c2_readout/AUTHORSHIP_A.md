# AUTHORSHIP_A: independent test author A, job 0101 (C2-FROZEN-v1 §13.3)

Author: a clean-context Claude subagent launched by coordinator session dcecc9ff, 2026-10-21.
Worktree `X:/Downloads/projects/topo-pilot/topo-pilot-c2`, branch `c2-0100` (base 018c608).
Assignment: Author A, algebra, statistics and oracle (TEST_PLAN.md §2).

## Files and §13.3 items

| File | §13.3 items |
|---|---|
| `test_a_readout.py` | T-READOUT; T-ORDER (RC-1, NEW-7); T-GLS part 1 (Lemmas G1-G3, Euclidean variant, whitened-design fixtures, "B in the nuisance span") |
| `test_a_gls.py` | T-GLS part 2 (v2 G1 scale-invariance fixture D-0104-2; GLS-REF, NEW-1 fixtures 1-6, Lemmas GR and INV, dctx/dsolve/dinverse) |
| `test_a_partition.py` | T-PARTITION; T-RANDOM; T-ENERGY (RC-4); T-HEADKERNEL; T-BOOT part (C2-M descriptive stream NEW-5, indicator form) |
| `test_a_scope.py` | T-SCOPE (RC-2, NEW-4; R and S*); T-LEAK (RC-7); T-PROJ |
| `test_a_oracle.py` | T-ORACLE (v2: the H^Y donor, D-0104-1); T-ROT (RC-14); T-LADDER (RC-15; moved here in v2) |
| `test_a_inference.py` | T-FAMILY (Lemma FW, FW-M); T-RULES (RC-8, RC-13, NEW-6); T-BOOT part (shared index stream, Fraction ranks) |

TEST_PLAN.md §2 places T-GLS (all), T-LADDER and the whole of T-BOOT in other files; they were
split by module under test (§4: "an author may split an item over two of their own files")
to respect the 400-line limit. Every Author A item is covered; no item moved to author B.

## What I read

- `agent-handoff/jobs/0101/task.md`.
- `tools/c2_readout/PROTOCOL_C2_v1.md`: header, §0-§11, §13 (13.1-13.5), Appendix A.
  Not read: §12 (cost), §14-§17, §18-§20 (dispositions).
- `tools/c2_readout/API.md` (all), `tools/c2_readout/CONTRACT.json` (all),
  `tools/c2_readout/TEST_PLAN.md` (all).
- Reused production code (§13.1 and `hashes.reused_extra`), read-only, in the c2 worktree:
  `tools/c1prime/c1_oracle.py` (lines 1-200), `c1_fit.py` (15-100, 147-205), `c1_means.py`,
  `c1_endpoint.py` (15-55), `c1_gates.py` (70-115), `c1_model.py` (`load_model64`);
  `tools/x4_circle_history/precision.py` (1-100); `tools/c1prime_registry/c1_registry_sources.py`
  (`canonical32`); `src/topo_pilot/oracle/_filter.py` (`BayesFilter`), `_common.py`
  (`as_model`, `check_tokens`); `tools/x4_oracle_profile/oracle_profile.py` (`circle_features`);
  `src/topo_pilot/learner/config.py` (`ModelConfig`), `learner/model.py` (`TransformerLM`);
  `src/topo_pilot/analysis/x4f_scores.py` (`ledoit_wolf`).
- For the test-import convention only: the file list of `tests/c1prime/` and the first 30 lines
  of two author-A test files there; the `[tool.pytest.ini_options]` block of `pyproject.toml`.

## What I did not read

- No file `tools/c2_readout/*.py` was read, listed or searched (none existed; the only listing of
  `tools/c2_readout` used the globs `*.md` and `*.json`).
- `topo-pilot/00_READ_ME_FIRST_*`, `docs/research_summary/`, any store payload (`*.npz`, `*.pt`),
  any scientific history or checkpoint, author B's tests.

## What I executed

Nothing of the tests or of any module under test. Only, with
`.venv/Scripts/python.exe -s`, scripts in the session scratchpad that read my own six files and
(i) `ast.parse` + `compile` them in memory, (ii) check line counts, line lengths, LF endings and
the bytecode global names, (iii) move test functions between my own files (byte-level, LF kept).
Plus read-only `git status`/`git log`, `sed`, `grep`, `wc` on the files listed above. No
formatter was run. All fixtures are synthetic.

## API-AMBIGUITY and API-ASSUMPTION notes (also in the test files)

1. **T-ORACLE grid** (`test_a_oracle.py`): protocol §13.3 asks for a 4 x 4 cylinder, but the
   index maps fixed by protocol §2.2/§2.11 and API.md §4.2 are the 12-grid maps (x, 11 - y) and
   ((x + m) mod 12, y), and `c1_oracle.m32` needs x in 0..11. The fixture is a 12 x 2 cylinder
   (x periodic, rows y = 5, 6), the smallest on which those maps act.
2. **GLS-REF fixture 5** (`test_a_gls.py`): API.md §9.1 does not say whether `u_D` in
   `theta`/`enclosure` reads the active decimal context; the protocol's reduced-precision
   fixture needs it, so the test wraps the residual and `cs.enclosure` in
   `decimal.localcontext(cs.dctx(12))`.
3. **GLS-REF fixture 1 layout**: the protocol's 3-d fixture is evaluated literally by the
   test's own Fraction/Decimal implementation; for the module it is embedded in R^8 with 5
   nuisance columns and K = 1 (the API.md §8.2/§9.1 column layout). The perturbed first solve
   (and, fixture 2, the perturbed second solve) is injected by replacing `cs.dsolve`, the calls
   being identified by their shapes.
4. **`co2.oracle_role`**: API.md §6.2 returns `m32` but the signature has no `coords`; the test
   calls the documented signature and does not assert `m32`.
5. **`cdc.r_model` / `cdc.m_model` input** (API-ASSUMPTION): `b` = {statistic name of §11.1
   without the model suffix: stream_bounds entry plus its guard `"g"`}, the report.json
   `per_model.bounds` layout of API.md §15.2; outputs read as booleans (`resp`, `spec`,
   `negative`, `coarse.gt010/lt050`).
6. **M rule 6** (`test_a_inference.py`): when Ztau is undeclared and one of its bounds is inside
   the guard, API.md §11.2 does not say INC or INC/NUMERICAL; both are accepted there.
7. **`cdc.variant_category`, `cdc.qualifiers`** (API-ASSUMPTION): `primary`/`per_model` are
   `r_model` outputs, `variants` = {model: {variant: category}}, `p1` = the `cs.p1` result
   (`precision_limited`).
8. **`cdc.endpoint_status`** (API-ASSUMPTION): `gate_history` = GATES.jsonl records (API.md
   §15.1) as dicts; a T-PRE-MODEL exclusion is expected as `NOT_RUN/T-PRE` (protocol §7 row 24,
   API.md §17 row 24).
9. **`ca.post_desc`**: API.md §10 does not fix its input layout; the test passes
   {name: {"num", "den", "E", "gate"}} and accepts any output entry holding the ratio and the
   label "unlicensed (gate T-PRE); computed after the outcome".
10. **`ca.desc_intervals`**: the result key per (num, den) pair is not fixed; the test accepts
    `(num, den)`, `"num/den"` or `num`, and an `"UNDEFINED"` value.
11. **`cdc.licence` values**: the bracket-to-key mapping is not fixed; the test passes one
    superset dict of the API.md §11.2 keys with scalar values.
12. **`cs.p1` kernels**: the test replaces `precision.sd_b4_draws/centered_draws/
    precision_summary` (and same-named attributes of `c2_stats`, if any) to record seeds, cfg and
    gated arrays; arrays are identified by a marker value in their first entry.
13. **`cs.n_test`**: the input holds only alive families (no `None` entries).

## Correction round (0102 review)

Defect reported by the implementer through the coordinator: in `test_a_gls.py`, `_pa` built
the T-LADDER parametrize table with `dict(base[name], **row)`, whose int model keys raise
`TypeError: keywords must be strings` at collection. Fixed by the author to
`{**base[name], **row}` (same meaning). No other change. Checked again only by in-memory
`ast.parse` + `compile` and the line-length/line-count/LF checks; nothing executed, no
formatter, no `tools/c2_readout/*.py` read.

## v2 update (C2-FROZEN-v2, job 0105)

Coordinator instruction: bring the tests to C2-FROZEN-v2 (`agent-handoff/planning/responses/
C2-FROZEN-v2.md`, sha256 51f78976...4583; D-0104-1, D-0104-2).

- **Read:** C2-FROZEN-v2 21 (the change log), 2.2, 2.3, 2.5 (Lemma G1 and the new G1 check),
  5.4, 5.5, 7 row 6 and 13.3 (T-GLS, T-ORACLE); `API.md` erratum 19.3 (commit 9c81b54, the
  H^Y donor API, the whitened G1 identity) and 19.1; `topo-scratch/0104/fy_alt.py` (sha256
  0e1113ed...63aa, the construction v2 2.2 names); the job 0105 task. Not read:
  `tools/c2_readout/*.py` (never listed or searched), `PROTOCOL_C2_v2.md` (the mailbox file
  was read instead), stores, author B's tests.
- **T-ORACLE (`test_a_oracle.py`):** the H^R tests (sigma, reflect_donor, rho_R_index,
  symmetry_report_R, the closed form of b32(H^R)) are removed. New: the k_Y sign rule with
  ybar = 5.5 giving -1; the shift b -> b + k on w1..w31 with a and w32 kept; the off-grid rule
  (row 5 under +1, row 0 under -1; w32 never shifted; OFF = 255 rows; no clamp, no wrap;
  role_arrays forms H^Y only on Y_def rows); REASONS and the OFF_GRID_Y tally; oracle_split
  with the H^Y oracle by the exact forward against an exact Fraction filter (NaN off grid; the
  o_H cache path); E_y and f_y with OFF_GRID_Y rows ineligible; reason_flags (S_Y, LIK_Y not
  evaluated off grid); the descriptive x leakage lambda_x. The rotation-oracle and T-ROT tests
  are unchanged apart from the new oracle_split signature.
- **T-GLS:** `test_a_readout.py` G1 test in the v2 form (dimensionless identities absolute
  1e-10, P_S Gamma and P_G B relative to max|Gamma|, max|B|, whitened self-adjointness
  ||P~ - P~'||_max <= 1e-10 with P~ = R^-T P R'). `test_a_gls.py` adds the scale-invariance
  fixture: Sigma by c in {1e-8, 1, 1e8} and [Gamma, B] by sqrt(c); the check passes and P is
  unchanged at every c, v1's absolute ||W P - P'W||_max exceeds 1e-10 at c = 1e-8, a planted
  oblique (non-self-adjoint) projector that satisfies every other identity fails at every c,
  and the Euclidean variant reduces to ||P - P'||_max.
- **T-LEAK (`test_a_scope.py`):** the y-placebo arrays renamed to the H^Y nomenclature; no
  behaviour change (the fixture is donor-agnostic). T-PARTITION never used the reflection.
- **File balance:** T-LADDER moved unchanged from `test_a_gls.py` to `test_a_oracle.py`
  (400-line limit).
- **Executed:** nothing; in-memory `ast.parse` + `compile`, the line/LF checks and the
  bytecode-name check only. No formatter.
- **API-AMBIGUITY:** none new; the tests follow erratum 19.3 as written (`k_y`, `y_donor`,
  `OFF`, `donors4(canon32, k_y)`, `role_arrays`, `oracle_split(..., k_y, o_H=None)`,
  `eligibility`, `reason_flags`, `x_leakage` returning {b31, b32}).

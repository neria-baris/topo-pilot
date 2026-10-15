# tools/d1_seam: written contract (job 0019; derived from D1-FROZEN-v1)

**Authority:** `agent-handoff/planning/responses/D1-FROZEN-v1.md` (sha256 68EBD82F9FD8E3C82114ADEF713F3AA9F7283BEBFF7AE38C5FFB266E62E10B21) and its coordinator addendum (sha256 1EE0291D7AEB071BAE961E963950A75743EF8259DD889C7134E1C886983D2669). Section numbers below refer to the protocol (§n).

**Precedence:** the protocol is authoritative. This contract only names the functions the module exposes, so that the independent test file can be written before the module exists. It changes no scientific choice: no parameter, value, tolerance, gate or stop rule. Where this contract and the protocol differ, the protocol wins.

## Files

| File | Role |
|---|---|
| `tools/d1_seam/d1_seam.py` | The module. One file, at most 400 lines (§6.2, S6). |
| `tests/d1_seam/test_d1_seam.py` | The independent test file (§6.2). |
| `tests/d1_seam/AUTHORSHIP.md` | The test author's independence record. |

**Store:** `X:/Downloads/projects/topo-pilot/d1-seam-oracle-store/`. It holds `report.json`, `model.npz`, a CPU ledger and logs. Every run uses one thread.

## Conventions (§0, §2, §6.1 field 4)

- Tokens: σ0 = 0, σ2 = 1, σ3 = 2, A = 3, B = 4. Module constants: `S0, S2, S3, A, B = 0, 1, 2, 3, 4`.
- State index within a world: i(x, y) = 3x + y, with x ∈ 0..3 and y ∈ 0..2. Mixture index: 12z + 3x + y, with z = 0 for C and z = 1 for M.
- Row vectors throughout. Event order: emit, then transition (`emit_then_transition`).
- All exact quantities are `fractions.Fraction`. A probability vector is a `list[Fraction]`. A two-step joint is a 5×5 `list[list[Fraction]]`, indexed `[first symbol][second symbol]`.
- Named histories are tuples of token ids, exposed as constants:
  - `H_STAR = (A, S2, S3)`;
  - `H_A = (A, S2, S3, S0, A, S2, S3, S0, A, S2, S3)`;
  - `H_B = (A, S2, S3, S0, B, S2, S3, S0, A, S2, S3)`;
  - `H_EDGE = (A, S2, S3, S0, A, S2)`;
  - `H_MAX = (A, S2, S3, S0, A, B, S0, S3)`.
- `K_DEPTH = 8`.

## Model construction

```python
VARIANTS = ("frozen", "N1", "N2", "N3", "L1", "L2")
```

`exact_world_T(world) -> list[list[Fraction]]`
- `world` is "C" or "M". Returns the 12×12 kernel built from the coordinate formulas of §2.1–§2.2, with a = 1/5 per edge neighbour and 1 − deg/5 on the diagonal.
- C seam edges: (3, y)–(0, y). M seam edges: (3, y)–(0, 2 − y).

`exact_E(variant="frozen") -> list[list[Fraction]]`
- Returns the 12×5 literal array of §2.4.
- "N2" replaces the column-1 rows by (0, 0, 0, 1/2, 1/2) in both blocks.
- "L2" replaces the column-2 rows by the column-1 rows (§5.2 G6).

`exact_model(variant="frozen") -> dict` with these keys, all Fraction:
- `"T"`: the 24×24 mixture blockdiag(T_C, T_M). For "N1" it is blockdiag(T_C, T_C).
- `"E"`: the 24×5 mixture vstack(E_C, E_M).
  - E_C = E_M = exact_E(variant) for every variant except "L1".
  - For "L1", the M block's column-1 rows are reflected: E_M′(1, y) = E(1, 2 − y).
- `"mu"`: length 24, with 1/2 at indices 3 and 15 (state (1, 0)) and 0 elsewhere.
  - For "N3" it is 1/2 at indices 4 and 16 (state (1, 1)).

`float_model() -> dict` (frozen variant only) with float64 numpy arrays:
- `"T_C"`, `"T_M"` (12×12): `TransitionBuilder().build(world, TransitionConfig(p_stay=0.2)).T` for each world's WorldSpec.
- `"E"` (12×5): the float of the literal array.
- `"T"` (24×24) and `"E_mix"` (24×5): `np.vstack((E, E))`, built once.
- `"mu"` (24), `"mu_C"` (12, 1 at index 3) and `"mu_M"` (12, 1 at index 3).

`build_worlds() -> dict {"C": WorldSpec, "M": WorldSpec}`
- C: `build_world(WorldConfig(family="cylinder", dims=(4, 3), metric="flat"))`.
- M: the local, unregistered `_D1MobiusBuilder`, validated in the order of §2.6.
- Any exception propagates to the caller, which turns it into INVALID (S2).
- Never mutates `WORLD_REGISTRY`. Never calls `process._geometry.point_distances` or `is_x_periodic`.

## Exact filtering and futures

`exact_history(history, variant="frozen") -> dict` gives exact values for one history. It raises `ValueError` if P(h) = 0. Keys:

| Key | Meaning |
|---|---|
| `"P_C"`, `"P_M"`, `"P"` | world-conditional probabilities and the mixture probability ½(P_C + P_M) |
| `"pi"` | P(Z = M ∣ h) |
| `"b_C"`, `"b_M"` | 12-vectors, world-conditional filtered beliefs |
| `"b_mix"` | 24-vector, ((1 − π)·b_C, π·b_M) |
| `"Q1_C"`, `"Q1_M"`, `"Q1"` | next-symbol laws, world-conditional and mixture |
| `"J_C"`, `"J_M"`, `"J"` | 5×5 two-step joints |
| `"Q2dist_C"`, `"Q2dist_M"`, `"Q2dist"` | distant-symbol marginals: J summed over the first symbol |
| `"par"` | seam parity of the history (§0) |
| `"informed"` | bool: some A/B observation was made at odd parity (§3.3) |

Only these definitions are used: Q1 = b T E; J[i][j] = b T diag(E[:, i]) T E[:, j]; for the mixture, Q = (1 − π)·Q_C + π·Q_M.

`tv(p, q) -> Fraction` is ½ Σ ∣p − q∣ over a vector or a 5×5 array.

## Gates (§5.2), each returning `{"status": "PASS" | "FAIL", "values": {...}}`

| Function | Gate |
|---|---|
| `gate_G0(worlds)` | G0 structure |
| `gate_G0S(worlds)` | G0S surface links |
| `gate_G0O(worlds)` | G0O orientability certificate |
| `gate_G1()` | G1 kernel identities |
| `gate_G2(variant="frozen", K=8)` | G2 enumeration, G2.1–G2.11 |
| `gate_G3()` | G3 named witnesses, including F3 and the 80-digit logarithms |
| `gate_G4(enum)` | G4 float cross-check |
| `gate_G5()` | G5 Decimal reference, 650 histories |
| `gate_G6()` | G6 controls N1, N2, N3, L1, L2 and P1 |

`gate_G2` returns these values, as Fractions or ints:
- `"N_t"`: the list for t = 1..8;
- `"HI_t"`: the σ3-ending counts;
- `"HI_mass_t"`: P(h ∈ 𝓗_I) per t;
- `"D_t"`: the start-law artefact P_C(W_t = A) − P_M(W_t = A), t = 1..8;
- `"max_branch_count"`: decision-phase nodes with ∣δ_M∣ > ∣δ_C∣;
- `"violations"`: a dict from check name to a count of exact-identity failures;
- `"named"`: exact_history output for H_STAR, H_MAX and the prefixes required by G2.8.

The expected values are those of §3.2, §3.8, §4 and §3.6. `gate_G2` with a control variant runs the same enumeration on that variant; G6 uses this.

## Run and verdict (§5.1, §5.3, §7.2)

`run(out_dir, preflight) -> dict`
- `preflight` is a dict `{check_name: bool}`. It records the mandatory §6.1–§6.2 checks, which are executed before `run` (see "Preflight" below).
- If any value is False, or the dict is empty, the verdict is **INVALID** and every gate is NOT_RUN.
- Otherwise the gates run in the order G0, G0S, G0O, G1, G2, G3, G4, G5, G6. The run stops at the first FAIL; the remaining gates are recorded as NOT_RUN and the verdict is FAIL.
- An exception while a gate is being evaluated gives INVALID; the remaining gates are NOT_RUN.
- If every gate passes, the verdict is PASS.
- Writes `out_dir/report.json`: the verdict; every gate's status and values (Fractions as strings, plus 30-digit Decimal renderings where useful); CPU time; the protocol and request hashes; the HEAD commit.
- Writes `out_dir/model.npz`: T_C, T_M, E and μ.
- Returns the report dict.
- The 20-CPU-minute ceiling and the 2 GB memory limit (S1) are enforced by the meter that runs `run`. A meter kill is INVALID.

**Preflight** (mandatory, run before `run` under the same meter):
- the unchanged `tests/world`, `tests/process`, `tests/oracle` and `tests/oracle_profile`;
- `tests/d1_seam`, which includes registry hygiene, the geometry guards, the Decimal trap and the control outcomes;
- `tools/check_file_sizes.py`, which enforces the 400-line limit.

## What the independent tests must cover (§6.2)

- The closed-form values of §3.5, §3.6 (h_max) and §4, from an independent Fraction path-sum reference in the test file. That reference must not import the module's exact kernels.
- The N_t counts.
- **Registry hygiene:** WORLD_REGISTRY is identical before and after importing the module and running `build_worlds`.
- **Geometry guards:** monkeypatch `topo_pilot.process._geometry.point_distances` and `is_x_periodic` to raise, then `build_worlds`, `float_model` and `exact_history` must still work.
- **The Decimal trap (§6.2).** Use history (A, A), the production `TransitionBuilder` float64 kernels, the exact dyadic emission array and the fixed start.
  - With Decimal string inputs representing the rational model, `independent_reference.decimal_suffix_posterior` must agree with the exact posterior within 1e-45.
  - With the production float kernels passed directly, at least one mixture-posterior entry must differ from the rational posterior by more than 1e-19.
- Each G6 control's expected outcome.
- The module file has at most 400 lines.

## Delta for job 0020 (addendum 2, sha256 2258ED96…3F6F; implementation choices only)

**Module split.** There are two files, each at most 400 lines.
- `d1_seam.py` holds: constants, `exact_world_T`, `exact_E`, `exact_model`, `_D1MobiusBuilder`, `build_worlds`, `float_model`, `exact_history`, `tv`, the enumerator, and `gate_G0`, `gate_G0S`, `gate_G0O`, `gate_G1`, `gate_G2` (including G2.11) and `gate_G3`.
- `d1_seam_checks.py` holds `gate_G4`, `gate_G5`, `gate_G6`, `s0_check` and `run`. It does `import d1_seam`.
- The last line of `d1_seam.py` re-exports `gate_G4`, `gate_G5`, `gate_G6` and `run` from `d1_seam_checks`, so `import d1_seam` exposes every API name. That module-end import avoids a circular import.

**Gate signatures.**
- `gate_G0(worlds, E_mix=None)`: `E_mix` defaults to `float_model()["E_mix"]`. The L1 harness passes the L1 mixture emission to evaluate the G0.6 block-equality criterion.
- `gate_G1(variant="frozen")` and `gate_G2(variant="frozen", K=8)`: G6 uses the variant forms.
- `gate_G4(enum)`: `enum` is the dict returned by `gate_G2()`. Its private `"_data"` key holds the exact per-node values (history, b_C, b_M, π, P, and the futures at 𝓗_I nodes); it is never written to the report.
- `gate_G5()` and `gate_G6()` take no arguments.

**`values` keys** (every gate also has `values["checks"]`, a dict from check name to bool; PASS means all are True):

| Gate | Keys |
|---|---|
| G0 | `edges_C`, `edges_M` |
| G0S | per world, a list of 12 vertex-link shapes such as ("arc", 3) or ("cycle", 4) |
| G0O | per world, `boundary_components`, `consistent` (the orientation cocycle), `rank_gf3` and `nullity_gf2` |
| G1 | `checks` only |
| G2 | `N_t`, `HI_t`, `HI_mass_t`, `D_t`, `violations`, `max_branch_count`, `joint_pos_marginal_zero`, `named_reached`, `named_values_ok`, `named` (h_star and h_max as (P, π)) |
| G3 | `KL`, `KL_rev`, `MI` (80-digit Decimals, rendered to 32 characters) |
| G4 | `max_errors` and `tolerances` (per §5.2 G4 quantity), `pair_tv`, `edge_tv1` |
| G5 | `histories` (650) and `max_abs_error` |
| G6 | per control, its exact quantities |

G2 `violations` names: `lemmaB`, `thmCb`, `thmCa`, `mixture`, `thmA`, `D2`, `F1`, `F2`, `pi_not_half`, `tv1_nonzero` and `tv2_nonzero_HI`. Only the first eight gate the frozen run; the last three are the counters the N1 and N2 controls read.

**Control harnesses (G6).**
- N1: TV₂ is also evaluated at **every** enumerated node, not only 𝓗_I.
- L1: both detections are evaluated: (i) `gate_G0(worlds, E_mix=L1)` must report E_blocks False; (ii) the G2.4 (Theorem C(a)) check on L1 at K = 1 must count violations, and π(A) = 1/4.
- L2: `gate_G1("L2")` must report its Theorem A row checks False, and the (3, 0) and (3, 2) rows must differ.

**`run(out_dir, preflight)` report.**
- `report["verdict"]` is PASS, FAIL or INVALID. `report["first_failed"]` names the gate.
- `report["gates"][name]["status"]` is PASS, FAIL, INVALID or NOT_RUN, with that gate's values.
- Also recorded: `report["preflight"]`, `report["S0"]` (`hashes_ok` over the protocol, both addenda and the request; `kernel_diff_empty` over `src/`, `tools/x4_oracle_profile/` and `tests/oracle_profile/` against 4f219d6; `head`), `model_sha256` and `cpu_s`.
- **Order:** a failed or missing preflight gives INVALID. Otherwise an S0 mismatch gives INVALID. Otherwise G0…G6 run, stopping at the first FAIL. An exception while evaluating a gate is INVALID, as are builder exceptions under S2.
- `report.json` is always written; `model.npz` (T_C, T_M, E, μ) is written once the worlds are built.
- CLI: `python d1_seam_checks.py --out <dir> --preflight <preflight.json>`.

**Metering and preflight** (not part of the module).
- **Meter:** every run uses the unchanged job-0014 meter, bound by a store-local script `d1-seam-oracle-store/d1_meter_bind.py` that rebinds module names only, with the same pattern as job 0016's meter_bind:
  - the store's own ledger and lock;
  - CPU measure-only, per the owner override;
  - the methodological 20 CPU-minute ceiling (S1) passed as `--max-cpu 1200` for the gate run;
  - Job Object memory limited to 2 GiB (S1);
  - one thread, set by the meter's environment variables.
- **Preflight:** the record `d1-seam-oracle-store/preflight.json` is built from metered runs of:
  - pytest on `tests/world`, `tests/process`, `tests/oracle` and `tests/oracle_profile` (regressions);
  - pytest on `tests/d1_seam`, which covers registry hygiene, the geometry guards, the Decimal trap, the controls and the 400-line check;
  - `tools/check_file_sizes.py`.

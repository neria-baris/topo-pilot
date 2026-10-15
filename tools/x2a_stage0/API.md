# tools/x2a_stage0: written contract (job 0025; derived from X2A-FROZEN-v1)

**Authority:** `agent-handoff/planning/responses/X2A-FROZEN-v1.md` (sha256 C80808CB7F22D9A171385FCB1AB7D03973E80DAFE638DFA758B6A84CA8341939). Section numbers (§n), gate ids (G0–G5, PF, S0) and lemma names below refer to the protocol.

**Precedence:** the protocol is authoritative. This contract only names the functions, inputs, outputs and report keys of the module, so that the independent tests can be written before the module exists. It changes no scientific choice: no parameter, value, tolerance, gate, stop rule or reading rule. Where this contract and the protocol differ, the protocol wins.

## Files (§8.1)

| File | Role | Budget |
|---|---|---|
| `tools/x2a_stage0/x2a_model.py` | constants; local torus builder and validation; field `e`, E_A and the variants; mixture assembly; exact k ≤ 4 enumeration and the corrected JS; closed forms; stencil filter; gates G0, G1, G2 | ≤ 400 lines |
| `tools/x2a_stage0/x2a_mc.py` | seeded sampling; batched filter pass and per-row statistics; windows, blocks and the additive score; credits; SE, intervals, Hoeffding; decision labels; G3, G4, D, G5; N-local, P-ref, long horizon | ≤ 400 lines |
| `tools/x2a_stage0/x2a_ph.py` | band rule (K1), C-world (K2), H0 threshold (K3); clouds; β̂ readings; PH controls; surrogates; outcome logic; `s0_check`; `run` and report writing | ≤ 400 lines |
| `tests/x2a_stage0/test_x2a_stage0.py` (+ optional `test_x2a_stage0_ph.py`) | independent tests (§8.4) | ≤ 400 lines each |
| `tests/x2a_stage0/AUTHORSHIP.md` | the test author's independence record | — |

Import convention: each module file adds `tools/x2a_stage0`, `tools/x4_oracle_profile` and `tests/oracle_profile` to `sys.path` itself (the D-1 pattern), so tests import them by bare name: `import x2a_model as xm`, `import x2a_mc as xc`, `import x2a_ph as xp`. Importing a module performs no I/O and no computation beyond constants.

**Store:** `X:/Downloads/projects/topo-pilot/x2a-stage0-oracle-store/`: `report.json`, `model.npz`, `ph_diagrams.npz`, `preflight.json`, CPU ledger and logs. One thread.

## Conventions (§0, §8.2 field 4)

- Row vectors; event order emit, then transition. float64 throughout; no epsilon, no clipping to manufacture finite logs.
- Within-component state `z = (x, y)`, index `12x + y`. Mixture index `144·[c = B] + 12x + y`: rows 0..143 are component A (first block), 144..287 component B (second block).
- Symbol `j = (a, b)`, token id `6a + b`, centre `(0.5 + 2a, 0.5 + 2b)`.
- π (the component posterior) always means the **second-block (B) mass** of a 288-entry mixture belief.
- Decision codes: `1` = B, `0` = A, `-1` = tie.
- Information in nats.

## x2a_model.py

### Constants

`N_SIDE = 12`, `N = 144`, `N_MIX = 288`, `V = 36`, `SIGMA = 1.25`, `P_STAY = 0.2`, `ALPHA = 0.2`, `T_STAR = 32`, `K_S = 8`, `WINDOWS = (1, 2, 4, 8)`, `BLOCK = 8`, `N_BLOCKS = 4`, `TAU = 1e-12`, `Z99 = 2.576`, `MASTER_X2A0 = 20261015`, `FAMILY = "_x2a_torus_local"`, `BASE_COMMIT = "c364f95e5573940cdc24b569b0fb7c6a16c97ab8"`, `REQUEST_SHA256 = "4132C43812F50171F118C61FB69B8111B068B7BF598C03E30CE00F9C7DC94595"`, `PROTOCOL_SHA256 = "C80808CB7F22D9A171385FCB1AB7D03973E80DAFE638DFA758B6A84CA8341939"`.

`VARIANTS = ("main", "N-iso", "N-same", "N-id", "N-swap", "P-ref", "N-local")`.

### Index helpers

- `state(x, y) -> int`: `12·(x mod 12) + (y mod 12)`.
- `token(a, b) -> int`: `6a + b`.
- `delta12(u, v)`: `min(|u − v| mod 12, 12 − (|u − v| mod 12))`, elementwise on arrays.

### World and kernel (§2.1, §2.2)

- `class _X2aTorusBuilder(QuotientLatticeBuilder)`: exactly the §2.1 ClassVars. Never registered.
- `build_world() -> WorldSpec`: §2.1 steps 1–4 in order. Any exception propagates (the runner turns it into INVALID, S2). Never mutates `WORLD_REGISTRY`. Never calls `process._geometry.point_distances` or `is_x_periodic`.
- `kernel(spec) -> ndarray [144, 144]`: `TransitionBuilder().build(spec, TransitionConfig(p_stay=0.2)).T`.

### Emission arrays (§2.3, §2.4, §2.6)

- `field_e() -> ndarray [12, 6]`: the 1-D field `e[x, a]` (§2.3).
- `emission_A(e=None) -> ndarray [144, 36]`: `E_A[12x + y, 6a + b] = e[x, a]·e[y, b]`.
- `dehn_perm() -> int64 [144]`: `dehn_perm()[12x + y] = 12·((x + y) mod 12) + y`, so `E_B = E_A[dehn_perm()]`.
- `iso_perm() -> int64 [144]`: `iso_perm()[12x + y] = 12·((x + 1) mod 12) + y` (N-iso).
- `emission_local(E_A) -> ndarray [144, 36]`: `¾·E_A[z] + ⅛·E_A[z + 2e_x] + ⅛·E_A[z − 2e_x]` (N-local; x mod 12).
- `emission_pref(spec, E_A) -> (E_P, sx, sy, state_perm)`: via the unchanged `draw_axis_permutation(spec)` and `axis_state_perm(sx, sy, (12, 12))`; `E_P = E_A[state_perm]`.

### Mixtures and variants (§2.5, §2.6)

- `mixture(T, E1, E2) -> (Tt, Et, pit)`: `Tt = blockdiag(T, T)` [288, 288], `Et = np.vstack((E1, E2))` [288, 36] built once, `pit = full(288, 1/288)`.
- `variant_model(variant, spec=None) -> dict` with keys `"spec"`, `"T"`, `"E1"`, `"E2"`, `"Tt"`, `"Et"`, `"pit"`, and for `"P-ref"` also `"sx"`, `"sy"`, `"state_perm"`. If `spec` is None, `build_world()` is called. Blocks per §2.6:

| variant | E1 | E2 |
|---|---|---|
| `"main"` | E_A | E_B = E_A[dehn_perm()] |
| `"N-iso"` | E_A | E_A[iso_perm()] |
| `"N-same"` | E_A | E_A (a copy) |
| `"N-id"` | 1/36 everywhere | 1/36 everywhere |
| `"N-swap"` | E_B | E_A |
| `"P-ref"` | E_A | E_P |
| `"N-local"` | E_A | emission_local(E_A) |

  Unknown names raise `ValueError`.

### Exact enumeration (§4.1)

- `window_law(T, E, k) -> ndarray [V**k]`: P(w_1..w_k) for one component, uniform start `1/n` over the `n = T.shape[0]` states, emit then transition. Flat C order: index `Σ_s w_s·V^(k−s)` (w_1 most significant). Generic in `n`, `V` and `k ≥ 1`.
- `js_phi(r) -> ndarray`: `φ(r) = ½[(1 + r)ln(1 + r) + (1 − r)ln(1 − r)]`, the series `r²/2 + r⁴/12 + r⁶/30 + r⁸/56` for `|r| < 1e-3`, and `φ(±1) = ln 2` exactly.
- `js_information(PA, PB) -> float`: `I = Σ_h M(h)·φ(r(h))`, `M = ½(PA + PB)`, `r = (PA − PB)/(PA + PB)`; entries with `M = 0` contribute 0; accumulated with `math.fsum` over chunks. (Disjoint point masses give ln 2.)
- `bayes_accuracy(PA, PB) -> float`: `Σ_h max(PA, PB)/2`.
- `exact_curve(T, E1, E2, kmax=4) -> dict`: `{"I": [I_1..I_kmax], "acc": [acc_1..acc_kmax]}` from `window_law` of each component.
- `G_overlap(e, d) -> float`: `Σ_x e[x, 0]·e[(x + d) mod 12, 0]`.
- `delta_rep_closed(e) -> float`: `(ALPHA/2)·G(1)·(G(0) − G(1))` (T2).
- `pair_law(T, E) -> ndarray [V, V]`: `(1/n)·Eᵀ T E` (§4.1 item 1).

### Stencil reference filter (§5.4 G3.1)

`stencil_filter(E1, E2, tokens) -> dict` with `"b"` [R, P, 288] (mixture beliefs b_1..b_P), `"pi"` [R, P] and `"log_evidence"` [R] (mixture). It never forms T: the transition is `0.2·(a + roll(a, ±1, axis 0) + roll(a, ±1, axis 1))` on 12×12 arrays per component, and the two components are combined by their log-evidences.

### Gates

`gate_G0(spec, T) -> dict`, `gate_G1(models) -> dict`, `gate_G2(models) -> dict`, where `models` maps variant name to `variant_model(...)`. Each returns `{"status": "PASS" | "FAIL", ...}` with the observed values of every §5.2–§5.3 check. G2 also stores the exact curves of every variant under `"exact"`.

## x2a_mc.py

### Elementary statistics (§4.2, Lemma C, Lemma A, §6.3)

- `entropy_b(p) -> ndarray`: `H_b(p) = −p ln p − (1 − p) ln(1 − p)` with `0·ln 0 := 0`.
- `mass_pi(b, n_A=144) -> ndarray`: π = `b[..., n_A:].sum(-1)`.
- `mass_logit(b, n_A=144) -> ndarray`: `log(b[..., n_A:].sum(-1)) − log(b[..., :n_A].sum(-1))`, from the separately accumulated masses (RC 8).
- `expit_pi(s) -> ndarray`: numerically stable expit.
- `decision(pi_d, tau=TAU) -> int8 ndarray`: `-1` if `|pi_d − ½| ≤ tau`, else `1` if `pi_d > ½`, else `0`.
- `credit(pi_full, pi_d, tau=TAU) -> ndarray`: Lemma C credit of the decision made from `pi_d`, against the exact posterior `pi_full`: `pi_full` if B, `1 − pi_full` if A, `½` if tie.
- `additive_score(Tt, Et, pit, tokens, n_A=144, block=8, n_blocks=4) -> ndarray [R]`: `s_add = Σ_β mass_logit(BayesFilter(Tt, Et, pit).run(tokens[:, block·(β−1):block·β]).b[:, block − 1], n_A)` over β = 1..n_blocks (Lemma A). Generic in the model size: `n_A` is the number of first-block states.
- `strat_mean_se(x_A, x_B) -> (mean, se)`: `mean = ½(mean(x_A) + mean(x_B))`, `se = sqrt(¼(s_A²/n_A + s_B²/n_B))`, with sample variances (ddof = 1).
- `interval(mean, se, z=Z99) -> (L, U)`: `mean ∓ z·se`.
- `hoeffding(R, n, delta) -> float`: `R·sqrt(ln(2/delta)/(2n))`.

### Decision labels (§5.6, §5.9)

- `p3_label(d3, se) -> str`: `"PASS"` if `L99(D3) − TAU ≥ 0.10`; `"FAIL"` if `U99(D3) < 0.10`; else `"THRESHOLD_INCONCLUSIVE"`.
- `p4_label(i8, se8, i32, se32) -> str`: `"PASS"` if `U99(I8) ≤ ½·L99(I32)`; `"FAIL"` if `L99(I8) > ½·U99(I32)`; else `"THRESHOLD_INCONCLUSIVE"`.
- `a3_label(d_add, se) -> str`: `"NONADDITIVE"` iff `L99(D_add) ≥ 0.03`, else `"ADDITIVE"`.
- `scientific_outcome(p3, p4, a3) -> str`: `"GO_P1_NONADDITIVE"` if P3 = P4 = PASS and A3 = NONADDITIVE; `"GO_P1_ADDITIVE"` if P3 = P4 = PASS and A3 = ADDITIVE; otherwise `"STOP_P1"`.
- `hoeffding_label(...)`: the bound-robustness counterpart at δ = 0.01 (§5.6); a difference is reported as `BOUND_SENSITIVE` and never changes a label.

### Pipeline (§6.1, §4.2)

- `sample(T, E, n, rng, n_obs=33) -> tokens`: one `HMMSampler(T, E, full(n_states, 1/n_states), SequenceLayout(n_obs=n_obs)).sample(n, rng)` call.
- `row_stats(model, tokens, batch=2048) -> dict`: per-row arrays for every §4.2 statistic: the full-history filter on `tokens[:, :32]`, windows k ∈ {1, 2, 4, 8} at t*, blocks 1–3 (block 4 is the k = 8 window), `s_add`, increments, V_t and the concentration inputs.
- `summarise(stats_A, stats_B) -> dict`: estimates with SE (and Hoeffding where §6.3 applies) for every §4.2 quantity.
- `gate_G3(model, tok_A, tok_B, exact=None) -> dict`, `gate_G4(exact, summary) -> dict`, `gate_D(summary) -> dict`, `gate_G5(...) -> dict`: `{"status": ..., values}` per §5.4–§5.8. `gate_D` returns values and the labels P3, P4 and A3, never a PASS/FAIL status.
- Descriptive: N-local and P-ref Monte Carlo, the long-horizon curve (§6.5), concentration, LLR slope, context gains, P5.

## x2a_ph.py

### Readings on diagrams (§7.2–§7.5)

Diagram rows are `DiagramResult.rows`: `[n, 4]` with columns `(dim, birth, death, censored)`; H0's essential bar has `death = inf`.

- `betti_at(rows, dim, r) -> int`: `#{dim-bars with birth ≤ r < death}` (infinite bars alive).
- `band_select(diagrams, lo=0.0, hi=0.99, min_width=0.08) -> dict`: `diagrams` is a list of rows arrays, one per ρ. For each, `S_ρ = {r ∈ [lo, hi] : β₀(r) = 1 and β₁(r) = 2}`, evaluated on the half-open segments between consecutive endpoints (each segment read at its midpoint). `S = ∩_ρ S_ρ`; its longest connected interval `[l, u)`, with ties broken by the smaller `l`. Returns `{"status": "OK" | "CALIBRATION_INCONCLUSIVE", "interval": (l, u) | None, "band": (l + (u − l)/4, u − (u − l)/4) | None, "S": [[l, u], ...]}`. `"OK"` requires `u − l ≥ min_width`.
- `beta1_band(rows, band) -> int`: `#{H1 bars with birth ≤ band[0] and death > band[1]}`.
- `k2_check(rows) -> dict`: `{"n_bars": #{H1 bars with persistence ≥ 1.0}, "ok": n_bars == 2}` (C-world).
- `clusters_at(D, h, dedup_map, min_size=26) -> dict`: single linkage at height `h` (MST edges longer than `h` cut; scipy `minimum_spanning_tree` and `connected_components`). Cluster sizes count **original** points through `dedup_map`. Only clusters with ≥ `min_size` original points are retained. Returns `{"count": #retained, "labels": int64 [M_original] (cluster 0..count−1, −1 if not retained), "retained_fraction": float}`.
- `split_check(labels, truth, purity=0.95) -> dict`: `{"split": bool, "purity": float}`. `split` holds iff there are exactly two retained clusters, each with a majority-label fraction ≥ `purity` over its retained points, and the two majority labels differ. `purity` is the smaller of the two fractions (0.0 if not two clusters).
- `h0_star(xhalf_rows, x1_rows) -> dict`: lists of per-panel rows. `m` = max over panels of (the largest finite H0 death of X^½, the second-largest finite H0 death of X¹). Returns `{"m": m, "ok": 1 − m > 0.05, "h0": (m + 1)/2}`.

### Outcome logic (§5.9, §7.5, §7.6)

- `q1_outcome(n_a, n_b, n_pref, invalid=False) -> str`: counts of panels (out of 8) with β̂₁(B_PH) = 2. `"INVALID"` if `invalid`. `"PASS"` if `n_a ≥ 7`, `n_b ≥ 7` and `n_pref < 7`. `"NON_SPECIFIC"` if `n_a ≥ 7`, `n_b ≥ 7` and `n_pref ≥ 7`. Otherwise `"FAIL"`.
- `q2_outcome(n_full_split, n_win_connected, n_win_split, invalid=False) -> str`: panel counts out of 8, with FULL_SPLIT = `n_full_split ≥ 7`, WIN_CONNECTED = `n_win_connected ≥ 7` and WIN_SPLIT = `n_win_split ≥ 7`. `"INVALID"` takes precedence; then `"NOT_SEPARATED"` if not FULL_SPLIT; `"SEPARATED_FULL_ONLY"` if WIN_CONNECTED; `"SEPARATED_BOTH"` if WIN_SPLIT; else `"WINDOW_UNRESOLVED"`.
- `validity(statuses) -> (verdict, first_failed)`: `statuses` maps `"PF", "S0", "G0", "G1", "G2", "G3", "G4", "G5"` to `"PASS" | "FAIL" | "INVALID" | "NOT_RUN"`. The first non-PASS gate in that order decides:
  - PF or S0 not PASS → `"INVALID"`;
  - a gate `"INVALID"` → `"INVALID"`;
  - a gate `"FAIL"` → `"FAIL"`;
  - a gate `"NOT_RUN"` with no earlier failure → `"INVALID"`.

  All PASS → `("PASS", None)`.
- `released(verdict, first_failed, labels) -> dict`: the D and PH labels if the verdict is `"PASS"`; every label `"WITHHELD"` if `first_failed == "G5"`; every label `"NOT_RUN"` otherwise. Values are kept either way.

### Run (§5.0, §5.1, §8.3)

- `s0_check() -> dict`: `{"protocol_sha256_ok", "request_sha256_ok", "kernel_diff_empty", "head", "hashes"}` (protocol and request files under `agent-handoff/planning/`; `git diff BASE_COMMIT HEAD -- src tools/x4_oracle_profile tests/oracle_profile` empty).
- `run(out_dir, preflight) -> dict`: requires every value of `preflight` true (PF), then S0, then G0 → G1 → G2 → G3 → G4 → D (sealed) → PH → G5, stopping per §5.0 and §5.10. Writes `report.json`, `model.npz` (T, e, E_A, E_B, E_N, E_P and their sha256 in the report) and `ph_diagrams.npz`.
- CLI: `python x2a_ph.py --out <dir> --preflight <preflight.json>`.

### report.json keys

`protocol`, `protocol_sha256`, `verdict` (PASS/FAIL/INVALID), `first_failed`, `gates` (PF, S0, G0–G5, each with `status` and values), `exact` (I_k and acc_k for k ≤ 4 per variant; hand values beside computed), `curves` (Î_t, Î′_t, âcc_t for t = 1..32 with SE and Hoeffding; increments; V_t; concentration; LLR slope), `windows` (k ∈ {1, 2, 4, 8}), `D` (D3, I_8^win, I_32, D_add with SE and intervals; acc_add, I_add^LB, ρ_add; the paired P4 form; block boundaries `[8, 16, 24]`; labels or WITHHELD), `outcome`, `P5`, `PH` (K1, K2, K3, C-emis, Q1, Q2, controls, noise floor, retained fractions), `descriptive` (N-local with its reading rule, P-ref, long horizon with its reliability flag, context gains, bound robustness), `seeds` (the main tree's `SeedTree.issued`; the P-ref helper stream with sx, sy and state_perm), `model_sha256`, `cpu_s`.

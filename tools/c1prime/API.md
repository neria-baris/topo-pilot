# tools/c1prime: written contract (job 0026; derived from C1′-v1)

**Authority.** `tools/c1prime/PROTOCOL_C1PRIME_v1.md`, sha256 0B1F107EC7BB241E97D812EE995AD91DFB1416D719B70942DC3A567B766CF33A. It is materialised from C1-FROZEN-v1 (D1DF1AEF…5DBA) and C1PRIME-DELTA-FROZEN-v1 (4556EB91…9A58) by `materialise_protocol.py`. Section numbers (§n), gate rows (§16 row n), and lemma and theorem names refer to it.

**Precedence.** The protocol is authoritative. This contract, `CONTRACT.json`, `TEST_PLAN.md` and `CERTIFICATE.md` only name the functions, inputs, outputs, statuses and records, so that the independent tests can be written before the code exists. They change no scientific choice: no estimand, parameter, tolerance, seed, gate, stop rule or reading rule. Where they differ from the protocol, the protocol wins. The test author records the conflict.

**Scope of job 0026.** Code and synthetic tests only.
- No real payload is decoded, apart from the integrity hashing already permitted.
- No history is sampled, no model forward runs on real histories, and no stage executes.

The data stages need coordinator releases R1–R3 (§17) in later jobs.

## 0. Package, paths and conventions

**Package.** `tools/c1prime/`. The protocol's §18 field 4 calls it `tools/c1_state_forcing/`. The dispatching task names `tools/c1prime/`, which is a path, not a scientific choice. Every file is at most 400 lines (S6 pattern). Tests live in `tests/c1prime/`.

**Store.** `X:/Downloads/projects/topo-pilot/c1prime-store/` (task path; §17 names `c1-state-forcing-store`). It holds GATES.jsonl, STAGES.jsonl, immutable NPZ/JSON records (`write_new`/`save_npz`, exclusive create), the CPU ledger (schema `x4-oracle-profile-ledger-v1`), RUN.lock and logs.

**Import convention.** Every module file inserts, at import and in this order, `tools/c1prime`, `tools/x4_circle_history` and `tools/x4_oracle_profile` into sys.path, as K4 does. Importing `error_bound` additionally inserts `tests/oracle_profile`, as frozen. Tests import modules by bare name (`import c1_chart`). Importing a module performs no I/O beyond reading `CONTRACT.json` (in `c1_config`), no sampling and no model work.

**Reused unchanged** (never edited; frozen hashes checked where the protocol says so):
- K4: `chart`, `cochain`, `errors`, `scores`, `adapter.cross_model_join`, `stage_records`, `precision`, `error_bound` (public names only), `op_guard`, `env_identity`.
- Job 0014: `oracle_profile`, `meter`, `controls`, `winjob`; `independent_reference.decimal_suffix_posterior`.
- `src/topo_pilot` (§18 field 1).

**Conventions.**
- Arrays are float64 unless stated.
- Canonical symbol j = 6a + b. Named = perm[canonical]; canonical = argsort(perm)[named]. E_canon = E_named[:, perm].
- States are indexed in WorldSpec order; coordinates come from `spec.coords`.
- "inverted_cdf" means `np.quantile(..., method="inverted_cdf")`.
- Every "exact" comparison uses `fractions.Fraction` of the float64 values.

**Statuses** (strings, exactly):
- `"PASS"`;
- `"FAIL_TECHNICAL"` and `"FAIL_TECHNICAL/<KIND>"` with KIND ∈ {IDENTITY, LINEAGE, ORACLE, NUMERICAL, MODEL};
- `"INCONCLUSIVE/<REASON>"` with REASON ∈ {CHART_UNAVAILABLE, ELIGIBILITY, HEADROOM, NUMERICAL, PATCH_MODEL_DEGENERATE, SUPPORT_DEGENERATE, RBF_DEGENERATE, FAMILY_UNMATCHED, NUISANCE_CONFOUNDED, SUPPORT, DECODER_INADEQUATE, CHART_NOT_REGISTERING, MANIPULATION_FAILED, MODEL_HEADROOM, UNDERPOWERED, TEST_GATE, REGISTRY_INCOMPLETE, RESOURCE};
- endpoint outcomes `"PASS"`, `"FAIL"`, `"MIXED"`, and per model `"PASS_j"`, `"FAIL_j"`, `"INC_j"`.

The record field `status` holds the prefix before "/" (FAIL_TECHNICAL, INCONCLUSIVE, PASS). The field `reason` holds the suffix and the message.

## 1. c1_config.py

| Name | Contract |
|---|---|
| `HERE`, `REPO`, `CONTRACT_PATH` | Paths of the package, the worktree, and `CONTRACT.json` |
| `load_contract(path=CONTRACT_PATH) -> dict` | JSON loaded, then JSON `null` decoded to `float("inf")` for `chart.lift_cpu_cap_s` and `resources.cpu_cap_s` |
| `chart_cfg(contract=None) -> dict` | The cfg dict passed to `chart`/`cochain`: every kernel key of `contract["chart"]` (`field`, `lift_bounds`, `lift_node_limit`, `lift_rounding_tol`, `local_passes`, `local_vertices`, `extension_k`, `support_min_resultant`, `fidelity_min_agreement`, `phase_bins`, `phase_bin_min_rows`, `overall_resultant_max`), plus `lift_cpu_cap_s = inf` and `native_operation_wall_s = 600` |
| `MODELS = (1729, 2718, 3141)`; `SITE = "resid_post_3"`; `INDEX = 32`; `BOS = 36` | Constants |
| `STATUS` helpers: `status_of(full) -> (status, reason)` | Splits `"INCONCLUSIVE/SUPPORT"` into `("INCONCLUSIVE", "SUPPORT")`; `"PASS"` gives `("PASS", None)` |

## 2. c1_records.py: stage records, gate boundary, exception mapping (§16 conventions, §18 field 2)

- `PREREQUISITE = {"oracle": None, "calibration": "oracle", "validation": "calibration", "fresh": "validation"}`. `bind_stage_records()` assigns it to `stage_records.PREREQUISITE` and returns the module.
- `REQUIRED_PASS = {"oracle": [...], "calibration": [...], "validation": [...]}`: the gate names that must have PASS records before the next stage (from §16 rows 0–5, 6–11 and 12–19):
  - oracle: G0, H1, H2, H3, H4, N0, H5;
  - calibration: M0, C0-cal, F1, M1, M2-cal, M3-cal;
  - validation: C0-val, M4, M2-val, M3-val, V1, V2, V3, P1.
- `check_pass_set(out, stage) -> None`: raises `stage_records.StageRefused` (via `stage_records.refuse`) unless every name in `REQUIRED_PASS[PREREQUISITE[stage]]` has a PASS record and no gate has a non-PASS record. Called by `begin_stage` before `stage_records.begin`.
- `begin_stage(out, stage, models) -> None`: `bind_stage_records()`, then `check_pass_set` (if the stage has a prerequisite), then `stage_records.begin(out, stage, models)`.
- `classify_exception(exc) -> (status, reason)`, the mapping of §16 conventions (v4, review fix 5):

| Exception | Status |
|---|---|
| `errors.Invalid`, `errors.JoinError` | `FAIL_TECHNICAL` |
| `errors.Unresolved` | `INCONCLUSIVE` |
| `oracle_profile.ProfileError`, a `ValueError` raised by `independent_reference` (reference input) | `FAIL_TECHNICAL/ORACLE` |
| `decimal.DecimalException` (any subclass), `CertificateFlag` (below) | `FAIL_TECHNICAL/NUMERICAL` |
| `StageFailure` with code `PH_RESOURCE_LIMIT` | `INCONCLUSIVE/RESOURCE` |
| `StageFailure` with code `GATE_FAILED` and attribute `c1_status` | that status (a declared unmet criterion) |
| any other `StageFailure` | `FAIL_TECHNICAL`, with reason `"<code>: <message>"` (original code and message preserved) |
| `C1GateFailure` (below) | its `.status` |
| anything else | `FAIL_TECHNICAL` |

- `class C1GateFailure(Exception)`: `.status` (full status string) and `.reason`. It is raised by C1 kernels for a declared unmet criterion.
- `class CertificateFlag(Exception)`: a watched Decimal flag in a certificate computation (P3).
- `adapt_chart_exception(exc) -> (status, reason) | None`, the chart boundary of §14 / c1prime-v1-rulings 1, 2, 6. Before the generic mapping:
  1. `errors.Invalid` with message exactly `"not a cocycle mod p"`, raised in `cochain.integer_lift` (the innermost frame of `exc.__traceback__` whose code is `cochain.integer_lift`) → `("INCONCLUSIVE", "CHART_UNAVAILABLE: float32/float64 filtration boundary")`.
  2. `errors.Invalid` raised in `cochain.smooth_phase`. The diagnostics are read from that frame's locals `f` and `residual` in `exc.__traceback__`, without rerunning anything:
     - any non-finite entry of `f` or a non-finite `residual` → `("FAIL_TECHNICAL", ...)`;
     - every `f` finite and `residual` finite and > 1e-8 → `("INCONCLUSIVE", "CHART_UNAVAILABLE: <original message>")`;
     - the frame or locals unavailable → `("FAIL_TECHNICAL", "smoothing diagnostics unavailable")`.
  3. Anything else → `None` (the generic mapping applies).
- `smoothing_diagnostics(exc) -> dict | None`: `{"f_finite": bool, "residual": float}` from the frame locals, or None when unavailable.
- `run_c1_gate(out, gate, fn, chart=False) -> object`. Runs `fn()`.
  - On an exception: if `chart`, `adapt_chart_exception` first; then `classify_exception`. Writes one gate record `record_gate(out, gate, status, reason=..., exception=type name, operation=originating function name)` and raises `C1Stop(gate, status, reason)` from the original exception.
  - On a returned dict with key `"status"`: records it (`"PASS"` or the full status, split into status/reason). If not PASS, raises `C1Stop`.
  - `stage_records.run_gate` is never relied on for classification.
- `class C1Stop(Exception)`: `.gate`, `.status` (full) and `.reason`. The first non-PASS stops the cohort.
- `GATE_ORDER`: a tuple of `(row, stage, gate)` in §16 order:

  | Row | Stage | Gate |
  |---|---|---|
  | 0 | pre-data | G0 |
  | 1 | S3 | H1 |
  | 2 | S3 | H2 |
  | 3 | S3 | H3 |
  | 4 | S3 | H4 |
  | 4a | S3 | N0 |
  | 5 | S3 | H5 |
  | 6 | S4 | M0 |
  | 7 | S4 | C0-cal |
  | 8 | S4 | F1 |
  | 9 | S4 | M1 |
  | 10 | S4 | M2-cal |
  | 11 | S4 | M3-cal |
  | 12 | S5 | C0-val |
  | 13 | S5 | M4 |
  | 14 | S5 | M2-val |
  | 15 | S5 | M3-val |
  | 16 | S5 | V1 |
  | 17 | S5 | V2 |
  | 18 | S5 | V3 |
  | 19 | S5 | P1 |
  | — | S6 | ACCEPT |
  | 20 | S7 | T-PRE |
  | 21 | S7 | NUM |
  | 22 | S7 | ENDPOINT |

  `STAGE_GATES` maps the stages oracle, calibration, validation and fresh to their gate names.
- `class LogitPolicy` enforces the computation-order rule (§2.2) for the driver and the tests:
  - `begin(gate)` sets the current gate (it must be the next gate of GATE_ORDER after the last passed one; else FAIL_TECHNICAL);
  - `passed(gate)` marks it PASS;
  - `require(kind)` raises `C1GateFailure("FAIL_TECHNICAL", ...)` unless the kind is allowed at the current gate:

  | Kind | Allowed at | Extra condition |
  |---|---|---|
  | `"identity_check"` (identity patch, zero patch, tail-path identity) | M0, P1, T-PRE | — |
  | `"donor"` (full-donor logits retained for A_full / Z_full) | V3, P1, T-PRE, NUM, ENDPOINT | — |
  | `"endpoint"` (primary/control logits retained for A, Y, Z) | P1, NUM, ENDPOINT | NUM and ENDPOINT also require that T-PRE has passed |

  No kind is allowed at any calibration gate other than M0 (identity_check).

## 3. c1_chart.py: the C1′ chart (§14)

- `landmark_ids(seq_ids) -> ndarray[str]`: 20-digit zero-padded decimal strings, in the given (ascending) order.
- `class ConstructionLedger(path)`: a JSON-backed count of chart constructions in the store (`CHART_CONSTRUCTIONS.json`).
  - `.claim(model, role)` with role ∈ {"production", "direct"}: raises `C1GateFailure("FAIL_TECHNICAL", ...)` if (model, role) was already claimed (no retry or substitution) or if 6 constructions exist.
  - The claim is written with `write_new`-style durability before construction starts.
- `components(edges, n) -> (labels int64[n], sizes int64[n_comp])`: `scipy.sparse.csgraph.connected_components(directed=False)` of ({0..n−1}, edges).
- `giant(labels, sizes) -> (cstar int64[m], m)`: the largest component; ties go to the component containing the smallest index; cstar is ascending.
- `giant_pass(m, n=512) -> bool`: `100*m >= 95*n` in integers. For n = 512 this is m ≥ 487.
- `restrict(edges, cocycle, cstar, n) -> (edges_C, a_C)`: the edges with both ends in C*, re-indexed through the ascending C* order. They stay lexicographic, with the matching cocycle entries.
- `fit_chart_lcc(X, ids, cfg, guard=None, timed=None, persist=None) -> chart.Chart`, the steps of §14 exactly.
  1. `chart._check_landmarks`; `cdist(X, X)` on all n.
  2. `ripser.ripser(D, maxdim=1, coeff=cfg["field"], distance_matrix=True, do_cocycles=True)`; `select_h1_bar`; r = (b + d)/2.
  3. `edge_list(D, r)`; `cocycle_to_edges(cocycles[1][k], E, field)`.
  4. Components; C*; ℓ_max = the largest finite H0 death of `dgms[0]`.
  5. **Pre-raise record.** `persist("giant", {...})` with b, d, r, k, ℓ_max, the component count, the sorted sizes (descending), the excluded landmark_ids, m, n and `giant_pass`. If GIANT fails, raise `C1GateFailure("INCONCLUSIVE/CHART_UNAVAILABLE", "GIANT_BELOW_0.95")`.
  6. `restrict`.
  7. `triangle_system`, then `integer_lift` (followed by `persist("lift", {"kind": ...})`), then `primitive_class(α, E_C, triangles, m, field)` (followed by `persist("primitive", {"g": g})`), then `smooth_phase` (followed by `persist("smoothing", {"residual": r})`).
  8. `chart._neighbor_scale(D[np.ix_(cstar, cstar)])`.
  9. Returns `Chart(ids[cstar], X[cstar], phi, sigma, support, d8, E_C, a_C, alpha, correction, beta, q, g, info)`. `info` holds the frozen fit_chart fields (birth, death, radius, bar_index, n_edges, n_triangles, lift, smoothing_residual), plus n, m, `l_max`, `n_components`, `component_sizes`, `excluded_ids`, `lift_kind` and `cstar` (the indices).

  `persist` is a callable `persist(name, dict)`. The driver binds it to `write_new` under the store, with names `CHART_<model>_<role>_<name>.json`. With `persist=None` nothing is written. Exceptions from the frozen kernels propagate unchanged, so the chart boundary of `run_c1_gate(..., chart=True)` classifies them. When the graph is connected (m = n), the returned Chart equals `chart.fit_chart(X, ids, cfg)` bitwise in every array and scalar field; only `info` gains keys.
- `fit_production_gauge(ch, m32_cstar) -> chart.Gauge`: `chart.fit_gauge(ch, m32_cstar)` unchanged. Raises as frozen: Invalid for a non-finite alignment; Unresolved("zero gauge alignment").
- `IDENTITY_CARRIER = chart.Gauge(sign=1, shift=0.0, alignment=0.0)`.
- `serialise(ch, gauge, role) -> dict`: `chart.chart_to_arrays(ch, gauge)` plus `info_json` with role ("production" or "validation_only") and `gauge_fitted` (True only for production).
- `c0_val(prod, gauge, val_X, direct, cfg) -> dict`: the four C0-val criteria of §14 on the 512 val-panel rows (in ascending landmark_id order), computed with the frozen kernels:
  - `ext = chart.extend(prod, gauge, val_X, cfg)`;
  - `n_supported = int(ext.supported.sum())`, with support pass iff `100*n_supported >= 99*512`;
  - `fidelity = chart.agreement(ext.phase[direct.info["cstar"]], direct.phi)`, pass iff ≥ `cfg["fidelity_min_agreement"]`;
  - `bins = chart.phase_bin_counts(ext.phase, 12)`, pass iff every bin ≥ 8;
  - `resultant = chart.overall_resultant(ext.phase)`, pass iff ≤ 0.30.

  It returns those values, `"criteria"` (four booleans) and `"status"`: "PASS" if all four hold, else `"INCONCLUSIVE/CHART_UNAVAILABLE"`. `chart.chart_gates` is never called.
- `extend_phase(prod, gauge, Q, cfg, timed=None) -> chart.Extension`: `chart.extend` unchanged. It is the only source of φ.

## 4. c1_oracle.py: donors, symmetry, oracle quantities, eligibility (§3, §4)

**Donors and symmetry**
- `tau(canonical, k) -> ndarray`: the symbol map τ_k(6a + b) = 6((a + k) mod 6) + b, elementwise.
- `donors(canon32) -> (H, Hp, Hm)`: H = canon32. H^±: columns 0..30 mapped by τ_±1, column 31 (w32) unchanged.
- `rho_index(coords, k) -> int64[N]`: the state permutation ρ_k(x, y) = ((x + 2k) mod 12, y), as an index array s ↦ ρ_k(s), from the WorldSpec coordinates.
- `symmetry_report(T, E, pi, coords) -> dict`:
  - `max_dev` (the 1e-14 checks: T[ρz, ρz′] vs T[z, z′], E[ρz, τ_k j] vs E[z, j], π uniform, for k = ±1);
  - `exact_invariance` (bool: T and π equal bitwise under ρ_k);
  - `r_E` (Fraction: max_{k,z,v} |E[ρ_k z, τ_k v]/E[z, v] − 1| exactly);
  - `eps_sym` (Fraction r_E/(1 − r_E), or None if r_E ≥ 1).
- `closed_form_b32(b31, T, E, w32, rho) -> ndarray`: the §3.2 closed form for the donor H^k.
  - `b31` [R, N] is H's own posterior after 31 symbols, and `rho = rho_index(coords, k)`.
  - The transported posterior is `t = zeros_like(b31); t[:, rho] = b31`, that is, t(ρ_k s) = b31(s).
  - The result is `u = (t @ T) * E[:, w32].T` (row r uses symbol `w32[r]`), divided by its row sum.
- `closed_form_tolerance(eps_sym, delta=2e-12) -> (t, t + t**2) | None`: t = 2δ/(1−δ) + 62·eps_sym, as Fractions. None if eps_sym is None or t > 3/2 (the enclosure branch).
- `rel_agree(xhat, xref, tol) -> bool`: |xhat_i/xref_i − 1| ≤ tol for every i, in exact rationals.
- `interval_rule(xhat, xtilde, beta, a=2e-12) -> str`: the §3.4 three-way rule against I_v = [x̃/(1+β), x̃/(1−β)], in exact rationals.
  - `"PASS"` if D_high ≤ a;
  - `"FAIL_TECHNICAL/ORACLE"` if D_low > a;
  - else `"INCONCLUSIVE/NUMERICAL"`.

  A non-finite x̂ gives `"FAIL_TECHNICAL/ORACLE"`.

**Oracle (§3.3; canonical, once per row)**
- `run_oracle(T, E, pi, tokens32) -> dict`: `BayesFilter(T, E, pi).run(tokens32)`, giving b31 = `b[:, 30]`, b32 = `b[:, 31]`, q = `q[:, 32]`, s = `ce[:, 31]`, log_evidence and `b_all` (the full b).
- `G_hat(qp, qm) -> (G, d, lam, lp, lm)`, C3:
  - lp = `np.log(qp)`, lm = `np.log(qm)`;
  - d = qp − qm, λ = lp − lm (elementwise float64);
  - G = 0.5·osum_v fl(d_v·λ_v) in canonical v order, an ordered left-to-right accumulation per row.
- `G_named(d, lam, perm) -> ndarray`: the same kernel on the arrays permuted into named order (`x_named[perm[j]] = x_canon[j]`).
- `named_from_canonical(x, perm)`, `canonical_from_named_cols(x, perm)`: column permutations.

**Covariates**
- `y_marginal(b, coords) -> [R, 12]`: Σ over states with y = c.
- `m32(b, coords) -> [R, 2]`: b @ `oracle_profile.circle_features(coords)`.
- `nuisance(b, coords) -> [R, 3]`: (ȳ, Var y, ‖m32‖), with y the integer state coordinate.

**Eligibility (§4)**
- `s_max(s_cal) -> float`: inverted_cdf 0.999 quantile over all calibration rows.
- `eligible(sp, sm, smax, le_H, le_Hp, le_Hm) -> bool[R]`: sp ≤ smax, sm ≤ smax, and all three log-evidences finite.
- `eligible_fraction(mask) -> float`.
- `kappa_nu(nu_p, nu_m, nu_nat_cal, elig_cal) -> float`: the mean over eligible calibration rows of ‖ν⁺ − ν⁻‖² divided by tr of the population covariance (ddof = 0) of ν over all calibration rows.
- `leakage_active(kappa) -> bool`: κ ≥ 0.01.

**Decimal reference (§3.4; route-F step 2 helper)**
- `decimal_posterior60(T, E, pi, suffix) -> list[Decimal]`. The provenance replica of `error_bound._reference_posterior`: `trapping_context(60)`, `decimal_suffix_posterior(..., digits=60)`, and a watched-flag check that raises `CertificateFlag`.
- `decimal_predictive(b, T, E, digits=60) -> list[Decimal]`: Σ_z b(z) Σ_z′ T(z, z′) E(z′, v), in the trapping context.
- `decimal_reference(T, E, pi, h32) -> dict`: the §3.4 reference for one 32-token canonical history, inside `trapping_context(80)`.
  - `b31` and `b32` come from `decimal_posterior60` on the first 31 and on all 32 tokens.
  - `q31 = decimal_predictive(b31)` and `q32 = decimal_predictive(b32)`.
  - `ln_q32` is the Decimal `ln` of `q32`, and `s = −ln q31[w32]` is the surprisal.

  All values are lists of Decimal.
- `h3_compare(x_hat, x_dec, p1_ok, beta) -> str`:
  - if `p1_ok`, `"PASS"` iff componentwise |x̂/x̃ − 1| ≤ 2·10⁻¹² in exact rationals, else `"FAIL_TECHNICAL/ORACLE"`;
  - otherwise `interval_rule(x_hat, x_dec, beta, 2e-12)`.

## 5. c1_cert.py: certificate core (§15.3.2–15.3.7; see CERTIFICATE.md)

- **Constants** (exact `Fraction`s):
  - `U = Fraction(1, 2**53)`, `U1 = U/(1 − U)`;
  - `gamma(n) = n·U/(1 − n·U)`;
  - `ZETA = Fraction(1, 2**800)`;
  - `rho_bar_ref(L, N, d) = (2(L−1)(d+2) + 2 + 2N + d)·U1`;
  - `C1HAT`, `DELTA1`, `C3HAT`, `DELTA3` (fl(0.1), |fl(0.1) − 1/10|, and likewise for 0.3).
- `up(c) -> float`: `math.nextafter(float(c), inf)` when `Fraction(float(c)) < c`, else `float(c)`. It always satisfies up(c) ≥ c.
- `OUT(x) -> Fraction`: (1 + 2⁻³⁰)·Fraction(x) + ZETA.
- `osum(cols) -> ndarray[R]`: ordered accumulation over a list of per-row arrays: acc = cols[0], then acc = acc + cols[k] for k = 1, …, in order.
- `reference_oracle(T, E, pi, tokens32) -> dict`, C0:
  - it never calls BLAS or a numpy reduction;
  - it returns `b` [R, 32, N], `q_ref` [R, V], `nu_min` [R] (min over t, z of b̂_t(z)) and `finite` [R];
  - support sets `S_col(z)` and `S_row(z)` are read from T > 0, ascending.
- `p0(T, E_list, pi) -> dict`: the P0 checks in exact rationals. It returns `ok`, `eps_E`, `pi_min`, `tau_plus`, `d`, `nu0`, `omega_TE`, `identical` (bitwise E identity across the list), `N` and `V`. When not ok, the status is `"FAIL_TECHNICAL/IDENTITY"`.
- `p1(nu_min, finite, nu0) -> bool[R]`.
- `discrepancy(q_hat, q_ref) -> list[Fraction]`: r_h = max_v |q̂ − q^ref|/q^ref per row, exactly.
- `rho_main(r_h, rho_bar) -> Fraction`: ρ̄_ref + r_h/(1 − r_h). P4 requires r_h ≤ 1/2.
- `route_f(T, E, pi, tokens32, q_hat) -> dict`: steps 1–4 of §15.3.7. It returns `r`, `x`, `rho_F` and `ok` (x ≤ 1/2), using `error_bound.posterior_envelope(32, N)` and `gamma_digits(2N+2, 60)`.
- `measured_log_error(q_hat, l_hat) -> list[Fraction]`: ē_ℓ per row (M-ln, 40-digit `ln`; e = |ℓ̂ − 𝓛| + 10⁻³⁸·|𝓛|; max over the row's values; `up`). It raises `CertificateFlag` on a watched flag.
- `p2_leaves(**arrays) -> bool`: the P2 limits.
  - logits |z| ≤ 2¹⁹;
  - q̂ > 0 finite; ℓ̂ finite;
  - Â, Ĝ, Ŷ, Ẑ, Ẑ_full finite with magnitude ≤ 2²¹;
  - ē_ℓ ≤ 2²¹;
  - every bound-evaluation data leaf ≤ 2²³.
- `a1_selftest() -> dict`: the A1 self-test vectors of CERTIFICATE.md §A1, with `"ok"` and every case recorded.

## 6. c1_means.py: tree mean, bootstrap streams, ranks (§15.3.2 C7, §3.5, §11, §12.3)

- `tree_mean(X) -> ndarray`: the mean over the last axis by the balanced tree. Adjacent pairs are added level by level, an unmatched last entry is carried, and the final value is divided once by n.
- `bootstrap_means(arrays, seed, draws=5000) -> dict[name, ndarray[draws]]`:
  - one `np.random.Generator(np.random.PCG64(seed))`;
  - per draw, exactly one `idx = rng.integers(0, n, size=n)`;
  - for every array (dict name → 1-D array of length n), `tree_mean(array[idx])`.

  The draws are shared across every array and model, never batched across draws.
- `c1_bootstrap_means(x, rng, draws) -> ndarray`: the H5 wrapper, with the same index stream as `oracle_profile.bootstrap_profile`.
- `rank_for(p, draws=5000) -> int`: ⌈draws·p⌉ in exact rationals: 250 (0.05), 84 (0.05/3), 4917 (1 − 0.05/3).
- `quantile_with_rank(values, p) -> (v, k)`: `np.quantile(values, p, method="inverted_cdf")` and its rank. A `rank_check` failure raises `C1GateFailure("FAIL_TECHNICAL/NUMERICAL", ...)`.
- `rank_check(values, v, k) -> bool`: #{values < v} < k ≤ #{values ≤ v}.

## 7. c1_bounds.py: row bounds, constants and guards (§15.3.8–15.3.11)

All bound functions take per-symbol data as Python lists of length V (36). Each entry is a numpy array over rows, or a scalar. Constants come in a `consts` mapping produced by `bound_constants()`, whose values are up(c) floats. The functions use only binary `+` and `*` on these objects, never numpy reductions, so a counting object can be substituted (CERTIFICATE.md §L5).
- `bound_constants() -> dict`: half, u1, gamma_V, gamma31_32, inv_1mu, c1_term (u′ĉ₁ + δ₁), c3_term (u′ĉ₃ + δ₃), tenth, three_tenths, thirty_second, zeta and two. Each is `up` of the exact rational.
- `b_G(d, lam, qp, qm, rho_p, rho_m, e_l, consts)`: Theorem 2. The terms are ρ̄^± = ρ + ρ·ρ, ε^d_v and ε^λ_v.
- `b_A(d, Delta, qp, qm, rho_p, rho_m, max_abs_Delta, omega_TE, consts)`: Theorem 3.
- `b_Y(Y, bA_T, bA_C_list, A_C_list, consts)`, `b_Z(Z, bY, G, bG, consts)` and `b_Zf(Zf, bA_full, G, bG, consts)`: Theorem 4.
- `B_constant(max_b, max_abs, n) -> Fraction`: OUT(max_b) + γ_{d_n+1}·Fraction(max_abs) + ZETA, with d_n = ⌈log₂ n⌉.
- `guard_endpoint(L, U, B) -> dict`: per model F = max(B, 10⁻⁹). It returns `"INCONCLUSIVE/NUMERICAL"` if |L| ≤ F or |U| ≤ F (exact rationals), else `"PASS"`.
- `guard_H5(lower, B_H) -> str`: Γ = Fraction(lower) − 1/100, g = max(B_H, 10⁻⁹). `"PASS"` if Γ > g; `"INCONCLUSIVE/HEADROOM"` if Γ ≤ −g; else `"INCONCLUSIVE/NUMERICAL"`.
- `guard_V3(L_list, B_list) -> str`: `"PASS"` if Γ_j > g_j for all j; `"INCONCLUSIVE/MODEL_HEADROOM"` if Γ_j ≤ −g_j for some j; else `"INCONCLUSIVE/NUMERICAL"`.
- `class Sym`: a counting value for L5. `Sym.leaf()` makes a leaf; `+` and `*` on Sym (or Sym with a number) build nodes. `.nodes`, `.monomials` and `.degree` are computed after replication.

## 8. c1_model.py: float64 model evaluation (§5.1, §5.4, §15.1)

- `load_model64(checkpoint) -> (model64, sha_f32)`:
  - `learner.stage.load_model`;
  - the float32 state-dict sha256;
  - `.to(torch.float64)`;
  - a check that every parameter cast back to float32 equals the original bitwise (else `C1GateFailure("FAIL_TECHNICAL/MODEL")`);
  - `torch.set_num_threads(1)`.
- `state_sha(model) -> str`: the sha256 of the float32 state dict, iterated in key order.
- `model_inputs(named32) -> torch.LongTensor[R, 33]`: [BOS, w1..w32].
- `activations(model64, inputs, batch=1024) -> [R, 128]`: `model64(inputs, return_hooks=(SITE,)).hooks[SITE][:, 32, :]` under `torch.no_grad()`. Logits are discarded unread.
- `patched_logits(model64, inputs, a, batch=1024) -> [R, 36]`: `forward_with_patch(model64, inputs, SITE, 32, a).logits[:, 32]`.
- `natural_logits(model64, inputs, batch=1024) -> [R, 36]`: `model64(inputs).logits[:, 32]`.
- `tail_logits(model64, a) -> [R, 36]`: `model64.unembed(model64.ln_final(a))`.
- `identity_patch_ok(model64, inputs, a) -> bool`: bitwise equality of patched and natural logits.
- `tail_identity(model64, inputs, a_forced) -> float`: the max abs difference of `log_softmax` between the tail path and `forward_with_patch` (gate: ≤ 1e-12).

## 9. c1_fit.py: FWL, whitening, frames, decoders (§5.2–5.5, §6, §7)

- `standardise_nuisance(z_cal) -> (mean, scale)`: the calibration mean and population SD, with scale 1 for constant columns.
- `fwl_design(w32, zt, f) -> [R, 41]`: 36 indicator columns (canonical w), 3 nuisance columns and 2 phase columns (cos, sin).
- `fit_fwl(a, w32, zt, phi) -> dict`: OLS by `numpy.linalg.lstsq`. It returns `alpha` [36, 128], `Gamma` [3, 128], `B` [128, 2], `rank`, `cond` and `sv_B`.
- `f1_check(fit) -> str`: `"PASS"` iff rank 41, cond ≤ 1e8, σ_max(B) > 0, and then σ_min/σ_max ≥ 1e-6; else `"INCONCLUSIVE/PATCH_MODEL_DEGENERATE"`. It also reports the within-class partial R² diagnostics.
- `forced(a, B, phi_s, phi_d) -> ndarray`: a + (f(φ_d) − f(φ_s)) @ Bᵀ.
- `residual(a, w32, zt, fit) -> ndarray`: r = a − α̂_w − Γ̂ z̃.
- `whitening(r_cal) -> dict`: `x4f_scores.ledoit_wolf(r_cal)` → (r̄, Σ_W); W = Σ_W^{−1/2} (symmetric, by `eigh`); W_inv. It returns `"INCONCLUSIVE/SUPPORT_DEGENERATE"` as its status if λ_min ≤ 1e-12·λ_max.
- `qr_pos(M) -> ndarray`: Q·diag(sign(diag R)) from `numpy.linalg.qr`.
- `primary_coords(W, B, Delta) -> (Qt, c)`: Q̃ = qr_pos(W B); c = (W Δ) @ Q̃ (row-wise Q̃ᵀ W Δ).
- `haar_frames(model_seed, count=32) -> list[ndarray[128, 2]]`: for r = 0..31, `qr_pos(SeedTree(0).generator("c1-sf-v1", "frame", model_seed, r).standard_normal((128, 2)))`.
- `control_delta(W_inv, Q_r, c) -> ndarray`: Δ_r = (Q_r c) mapped by W⁻¹, row-wise.
- `m1_report(W, Delta_pm, Qt, frames, c_pm) -> dict`:
  - the three identities with the §6 comparison definitions (norm per row, uncentred and pooled-centred spectra, orthonormality);
  - `"status"` "PASS" or "FAIL_TECHNICAL".
- `fit_decoder(a_cal, Y_cal, panel_cal, model_seed, target) -> Decoder`, the §7 pipeline steps 1–5:
  - standardizer;
  - `rbf_bandwidth` with the rbf_bandwidth stream;
  - `rbf_map` with the rbf stream;
  - `rbf_features`;
  - `nested_ridge`;
  - the `RidgeProbe` refit.

  `Decoder` has `.predict(a)` and `.equivalence` (the max abs difference against nested_ridge's `pred_val`; M1 needs ≤ 1e-10). ℓ = None raises `C1GateFailure("INCONCLUSIVE/RBF_DEGENERATE")`.
- `w_hat(dec_w, a) -> int[R]`: argmax, with ties to the lowest index.

## 10. c1_gates.py: damage, leakage, support, registration, adequacy (§7–§10)

- `D_w(w_nat, w_pm_list) -> float`: (1/2n) Σ_{i,±} 1[ŵ(a^±) ≠ ŵ(a)].
- `D_y(y_nat, y_pm_list, tr_cov) -> float`.
- `leakage(y_p, y_m, nu_p, nu_m) -> float`.
- `m2(Dw_T, Dy_T, Dw_C_list, Dy_C_list, L_T=None, active=False) -> dict`: the §8.2 table, plus leakage when active. Status `"PASS"`, `"INCONCLUSIVE/FAMILY_UNMATCHED"` or `"INCONCLUSIVE/NUISANCE_CONFOUNDED"`. Family and matching are checked before leakage.
- `mahalanobis(a, w, zt, fit, white) -> ndarray`: ‖W(a − α̂_w − Γ̂ z̃ − r̄)‖ row-wise.
- `q99(DM_cal) -> float`: inverted_cdf 0.99.
- `frac_beyond(DM, q) -> float`.
- `m3(F_S, F_D, F_T, F_C_list, Sup) -> dict`: the four requirements of §9. `Sup` holds S, D, T and the C mean. Status `"PASS"` or `"INCONCLUSIVE/SUPPORT"`.
- `wrap(x) -> ndarray`: maps to (−π, π].
- `v1(phi_p, phi_m, m32_p, m32_m) -> dict`: med* by inverted_cdf; the rows with |δ*| ≥ med*; the fraction with sign(δ) = sign(δ*), where sign(0) disagrees. Pass iff ≥ 0.75, else `"INCONCLUSIVE/CHART_NOT_REGISTERING"`.
- `v2(phi_s, phi_pm, phi_T_pm) -> dict`: κ, and the agreement over arms with |d| ≥ the inverted_cdf median. Pass iff 0.5 ≤ κ ≤ 1.5 and agreement ≥ 0.80, else `"INCONCLUSIVE/MANIPULATION_FAILED"`.
- `m4(w_pred, w_true, y_pred, y_true, y_mean_cal) -> dict`: accuracy ≥ 0.95 and `r2_pooled` ≥ 0.50 (None fails), else `"INCONCLUSIVE/DECODER_INADEQUATE"`.

## 11. c1_endpoint.py: crossed contrast, inference, decision (§11–§13)

- `A_hat(d, z_plus, z_minus) -> ndarray[R]`, C4: Δ = z⁺ − z⁻ (gathered in canonical order by the caller); A = 0.5·osum_v fl(d_v·Δ_v).
- `Y_hat(A_T, A_C_list) -> ndarray`, C5: m_C = fl(osum_r A_{C_r}·2⁻⁵); Y = fl(A_T − m_C).
- `Z_hat(Y, G) -> ndarray`, C6: fl(Y − fl(0.1·G)).
- `Zfull_hat(A_full, G) -> ndarray`: fl(A_full − fl(0.3·G)).
- `A_logsoftmax(qp, qm, lp_plus, lp_minus)`: the log-softmax definition, secondary use only.
- `endpoint_bounds(Z_by_model, seed=520503, draws=5000) -> dict`: shared index draws (c1_means); L_j and U_j at ranks 84 and 4917, with rank checks.
- `per_model_status(L, U) -> str`: PASS_j iff L > 0; FAIL_j iff U < 0; else INC_j (equality is INC_j).
- `overall(statuses) -> str`: PASS iff all PASS_j; FAIL iff all FAIL_j; else MIXED.
- `v3(Zfull_by_model, B_V3, seed) -> dict`: lower bounds at rank 84, then `guard_V3`.
- `h5(G, B_H, seed) -> dict`: `c1_bootstrap_means` at rank 250, `percentile_interval`, then `guard_H5`.
- `ladder(Z_val, G_val, models) -> dict`: `precision.sd_b4_draws` (seed 520501), then for N in (4096, 8192, 16384) `centered_draws` (seed 520502) and `precision_summary` with cfg {alpha 0.05/3, power 0.80, delta 0.0, alternative (0.20 − 0.10)·Ḡ_val, projected_N N}. It returns the per-N summaries and N_test (the smallest PASS), or `"INCONCLUSIVE/UNDERPOWERED"`.
- `k_blocks(N_test, f_val) -> int`: ⌈N_test/((f_val − 0.02)·4096)⌉ in exact rationals of the float values.
- `fresh_fraction_ok(f_test, f_val) -> bool`: |f_test − f_val| ≤ 0.02 and f_test ≥ f_val − 0.02.
- `ratio_reduction(meanY, meanG, c) -> bool`: E[Y − cG] > 0, defined for meanG > 0.

## 12. c1_data.py: histories, registry, separation (§2.2–§2.4)

- `history_generator(split, block)`: `SeedTree(0).generator("data", "c1-sf-v1", split, block, "cylinder", "overlap", "1.25")`.
- `sequence_ids(split, block) -> int64[4096]`: `make_sequence_ids(process_code("cylinder", "overlap", "1.25", f"c1-sf-v1/{split}/b{block}"), "test", 4096)`.
- `sample_block(T, E_canon, pi, split, block) -> (canon32 uint8[4096, 32], seq_ids)`: one `HMMSampler.sample(4096, rng)` call; w33 and the states dropped at once.
- `panels(seq_ids, block) -> int[R]`: 4·block + ⌊rank/1024⌋.
- `lowest(seq_ids, n) -> int64[n]`: the row indices of the n lowest sequence_ids, ascending.
- `history_table(canon32, seq_ids, panel) -> dict`: the arrays plus per-row digests of H, H⁺ and H⁻ (`scores.history_digests`).
- `registry_digests(canon32) -> set[str]`.
- `separation(U_cal, U_val, R1) -> dict`: the empty-intersection checks over every role combination. Status `"PASS"` or `"FAIL_TECHNICAL/LINEAGE"`.
- `build_registry(sources) -> dict`: a manifest with each scanned input's content hash, its canonicalisation metadata and its contribution count, and the union digest set. A source that is not readable gives `"INCONCLUSIVE/REGISTRY_INCOMPLETE"`.
- `first_token_ok(first, pE, split) -> bool`: `check_first_token` does not raise.

## 13. c1_release.py: C1 release (§17, §18 field 2)

- `SCHEMA = "c1prime-release-v1"`; `STAGES = {"oracle", "calibration", "validation", "fresh"}`; issuer `"claude-coordinator"` only, bound like K4 release.py's Claude branch (assumption record, live runtime mode).
- `verify(path, mailbox=MAILBOX, out=None, head=None, contract_path=CONTRACT_PATH) -> dict`. `head=None` reads the worktree HEAD from the git files, as K4's `release._head` does; tests may pass a string. `out=None` uses the contract's output_root. The checks:
  - the live RUN_NEXT request and task digest;
  - the release lives in the job directory;
  - the source HEAD;
  - the CONTRACT sha and FREEZE sha;
  - `released_stages` ⊆ STAGES;
  - the stage-specific fields:
    - R1 needs `authority` {owner_decisions {path, sha256}, diag_json {path, sha256}, job_0023_accept {path, sha256}} and `registry_v1` {path, sha256};
    - R3 needs `N_test`, `k` and `registry_v2`.

  It raises `ReleaseError` otherwise.

## 14. c1_meter_bind.py, c1_env.py, c1_freeze.py (bindings)

- **c1_meter_bind.** It rebinds the unchanged meter/controls/winjob:
  - `controls.JOB_ID` and `TASK_SHA256`;
  - `meter.OUT/LEDGER/EMERGENCY/LOCK/ACTIVE/LOG_DIR` (in the store);
  - `meter.CAP_S = meter.STOP_NEW_S = inf`;
  - `meter.OUTPUT_CAP = 16 GiB`;
  - `winjob.MEMORY_CAP = 12 GiB`;
  - `meter.WORKER_SESSION` = the authorized executing worker (protocol §18): the verified release's `worker_session`, which must be named in the job's task.md (`c1_release.authorized_worker`). Without the field, it is the contract's worker session (job 0035, ruling R10: worker rotations no longer require a re-freeze).

  It forces `--max-cpu inf --max-wall inf`. It installs `limit_reason` with the disk safe-STOP and the op-marker deadline, using `disk_reason` and `make_limiter`, which are extracted from K4 meter_bind with provenance. It never imports K4 `meter_bind`.

  The functions:
  - `bind(job_id, task_sha256, out, worker_session) -> None`;
  - `disk_reason(usage=shutil.disk_usage) -> str | None`: C: < 2 GB or X: < 30 GB free;
  - `make_limiter(op_marker=None, disk=disk_reason, legacy=None, clock=time.time) -> callable`: the `meter.limit_reason` signature, checked every 8th poll for disk;
  - `rewrite_argv(argv) -> list`, which forces `--max-cpu inf` and `--max-wall inf`;
  - `main()`.
- **c1_env.** `SCIENTIFIC_IMPORTS` adds torch and the c1prime modules. `record()` rebinds `env_identity.SCIENTIFIC_IMPORTS`, then calls `import_scientific()`, then `env_identity.record()`.
- **c1_freeze.** It provides `snapshot(name)`, `compare(a, b)`, `freeze()` and `verify()`.
  - FREEZE.json holds the commit, the contract/protocol/API/TEST_PLAN/CERTIFICATE hashes, the sha256 of every frozen code and test file, the reused-unchanged files with their K4/0014 freeze hashes, and the environment record.
  - A protected-record snapshot is taken before and after; it is the listing hash of the stores and the main artifact store.
  - The fresh-venv pin check compares `requirements.lock` against the installed distributions of the venv interpreter.

## 15. c1_driver.py and c1_driver_late.py: the stage driver (§16 order)

`run_stage(stage, release_path) -> dict` runs exactly one stage under `begin_stage`, with gates in §16 order through `run_c1_gate`. The first non-PASS raises `C1Stop`, writes the stop record and ends the stage. Each stage:
- **oracle (S3):** G0, H1, H2, H3, H4, N0, H5.
- **calibration (S4):** M0, C0-cal (`chart=True`), F1, M1, M2-cal, M3-cal.
- **validation (S5):** C0-val, M4, M2-val, M3-val, V1, V2, V3, P1. The sealed file `SEALED_VALIDATION.json` is written with `write_new` and never read by the driver.
- **fresh (S7):** T-PRE, NUM, ENDPOINT.

The computation-order rule (§2.2) is enforced:
- On calibration, the only logits read are the M0 identity/zero-patch checks.
- Donor logits are first retained at V3, and primary/control logits at P1.
- No fresh primary/control A, Y or Z is computed before T-PRE passes.

The driver is implemented in job 0026 but never run on data in this job.

## 16. Records written (immutable)

- **Gates and stages.** GATES.jsonl and STAGES.jsonl (`stage_records`).
- **Chart records.** `CHART_<model>_<role>_{giant,lift,primitive,smoothing}.json`, `CHART_<model>_<role>.npz` (serialised) and `CHART_CONSTRUCTIONS.json`.
- **History and oracle records.** History tables `HIST_<split>_b<block>.npz`; `ORACLE_<split>.npz`; `CERT_<split>.npz` plus `CERT_<split>.json` (exact rational strings, §15.3.15).
- **Fitted objects.** `FIT_<model>.npz` (FWL, W, frames, decoders' frozen arrays).
- **Gate reports.** `GATE_REPORT_validation.json` and `SEALED_VALIDATION.json`.
- **Final records.** `ENDPOINT.json`; `FREEZE.json` and snapshots.

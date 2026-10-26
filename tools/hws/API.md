# tools/hws: written contract (job 0118; derived from HWS-DESIGN-v1)

**Authority.** `tools/hws/PROTOCOL_HWS_v1.md`, a byte-for-byte copy of `agent-handoff/planning/responses/HWS-DESIGN-v1.md` (sha256 `d96906097ab8b6ec464a2dbd4b477353b2950aa58e5b5995b7b6086ce68963a9`; it becomes HWS-FROZEN-v1 at the final execution freeze). J1 AUTH: owner addendum 29. Section marks (§n), DR numbers, KC numbers, RC and MD numbers refer to the protocol.

**Precedence.** The protocol wins on any conflict; a difference is a contract defect to report, never to resolve in code. `CONTRACT.json` holds the machine-readable values (exact values are strings for `fractions.Fraction`). This file fixes names, signatures, shapes, dtypes, streams, record schemas, report keys, store layout and the meter binding, so that the independent tests (`TEST_PLAN.md`) can be written before any module exists. It changes no scientific choice. Where the protocol leaves a detail open, the simplest consistent option is fixed in §14 "Choices" (cited as "choice n").

**Nothing here authorises a run.** No sampling, oracle run or test run follows from this contract (§0.1, RC-4).

## 0. Conventions

- **Seven modules** under `tools/hws/` (§12.1), each at most 400 lines (`tools/check_file_sizes.py`): `hws_worlds`, `hws_oracle`, `hws_exact`, `hws_stats`, `hws_select`, `hws_driver`, `hws_meter_bind`. No other `.py` file in `tools/hws/`; no edit to any existing file; no `src` edit; no `CENTER_REGISTRY` entry; no private (leading-underscore) name of a reused module is imported (choice 1).
- **Import convention.** Every module imports `hws_worlds` first. `hws_worlds` computes `HERE = Path(__file__).resolve().parent`, `REPO = HERE.parents[1]` and prepends, if absent, in this order: `tools/hws`, `tools/k4b`, `tools/c1prime`, `tools/x4_circle_history`, `tools/x4_oracle_profile` (all under `REPO`). Reused tool modules are imported by bare name (`oracle_profile`, `k4b_scores`, `scores`, `error_bound`, `process_law`, `stage_records`, `c1_means`, `k4b_meter_bind`, `meter`, `winjob`, `controls`, `op_guard`). Dependency order (no cycles): `hws_worlds` ← `hws_stats` ← `hws_oracle` ← `hws_exact` ← `hws_select` ← `hws_driver`; `hws_meter_bind` imports only `hws_worlds` and the meter modules. Import performs no I/O beyond reading CONTRACT.json files (HWS, and K4b/C1′ through the reused modules) and no computation beyond small constants.
- **Run** with `X:/Downloads/projects/topo-pilot/topo-pilot/.venv/Scripts/python.exe -s` and `PYTHONPATH=<worktree>/src`, single thread (meter `THREAD_VARS` = 1).
- **Numbers.** Levels, thresholds and alphas are `Fraction`s (CONTRACT strings). Configs receive `float(level)`. Statistical comparisons are float64 on the reported bounds, equality passes (§5.2). Exact filters (E2, E4) compare `Fraction(float(x))` with the exact threshold (choice 6).
- **Statuses** are full strings: `PASS`, `INELIGIBLE/E<k>`, `EXCLUDED/C<k>`, `CANDIDATE/CONFIDENT|POSSIBLE|MARGINAL`, `FAIL_TECHNICAL/<REASON>`, `INCONCLUSIVE/RESOURCE_OR_AUTHORITY`, `NOT_RUN`. A technical stop is raised as `HwsStop(status, reason)` (defined in `hws_worlds`, subclass of `RuntimeError`, attributes `status`, `reason`). Exception mapping: choice 43.
- **Writes** only inside the store passed as `out` (never a module default inside a function), by exclusive create (`stage_records.write_new`, `stage_records.save_npz`). Append-only exceptions: `GATES.jsonl` (`stage_records.record_gate`), `STAGES.jsonl` (`hws_driver.append_stage_event`), `logs/`. `cpu_ledger.json` is written only by the meter.
- **No payload access.** No function opens or hashes any `payload.npz`, `state.pt`, `.pt`, any `.npz` other than HWS's own `hist/**/*.npz`, or anything under `sealed/`. `inputs.load_artifact`, `inputs.load_process`, `k4b_data.load_process` and `inputs.verify_input_hashes` are never called (§3 KC1).
- **World keys** are strings `W{W}-q{q}-s{float(σ)!r}-p{float(p)!r}` (e.g. `W12-q1-s1.25-p0.2`); known-zero worlds `U-W12`, `N-W12` (§6.6). Key order is Python `str` order (choice 3).

## 1. `hws_worlds.py` (≈240 lines): constants, grid, keys, tiers, builders, alias map, symmetry, E1–E3

### 1.1 Constants and paths

| Name | Value / signature | Contract |
|---|---|---|
| `HERE`, `REPO`, `CONTRACT_PATH`, `PROTOCOL_PATH` | `Path`s | `HERE/"CONTRACT.json"`, `HERE/"PROTOCOL_HWS_v1.md"` |
| `ROOT` | `Path("X:/Downloads/projects/topo-pilot")` | project root (G0 search root) |
| `STORE`, `DRY_STORE` | `ROOT/"hws-store"`, `Path("X:/Downloads/topo-scratch/hws-dry")` | driver defaults only |
| `load_contract(path=CONTRACT_PATH) -> dict` | | `json.loads` of the UTF-8 file |
| `CONTRACT` | `load_contract()` at import | |
| `HwsStop(status, reason)` | exception | see §0 |
| `H`, `L`, `N_AXIAL` | `12`, `32`, `6` | |
| `P_LEVELS`, `SIGMA_LEVELS` | `tuple[Fraction]` | CONTRACT `levels.p` (1/5 … 15/16), `levels.sigma` (5/4 … 3) |
| `Q_LEVELS`, `W_LEVELS` | `(1, 2, 3)`, `(8, 12, 16)` | |
| `X1_P`, `X1_SIGMA` | `(Fraction(31, 32),)`, `(Fraction(7, 2), Fraction(4))` | |
| `S2_P_MID`, `S2_SIGMA_MID` | `dict[(Fraction lo, Fraction hi)] -> Fraction` | CONTRACT `levels.s2_p_edges`, `s2_sigma_edges` (RC-6 frozen p values 3/8, 2/3, 5/6, 11/12, 23/24) |
| `P_INDEX`, `SIGMA_INDEX` | `dict[Fraction] -> Fraction` | CONTRACT `levels.index` (half steps for midpoints) |
| `W0` | `World(12, 1, Fraction(5, 4), Fraction(1, 5))` | key `W12-q1-s1.25-p0.2` |

### 1.2 World keys, grid, tiers, distance

| Name | Contract |
|---|---|
| `World` | `@dataclass(frozen=True, order=False)` with fields `W: int`, `q: int`, `sigma: Fraction`, `p: Fraction`; property `key -> str` (format of §0); `sigma_f`, `p_f` → floats |
| `world_key(W, q, sigma, p) -> str` | the key string; `repr(float(sigma))`, `repr(float(p))` |
| `grid() -> list[World]` | the 225 worlds of §4.4, order W ascending, then q, σ, p ascending (choice 4) |
| `x1_worlds(add_p: bool, add_sigma: bool, cells) -> list[World]` | `cells`: iterable of eligible `(W, q)` cells. Every world in those cells with p ∈ `P_LEVELS + (X1_P if add_p)` and σ ∈ `SIGMA_LEVELS + (X1_SIGMA if add_sigma)` that is not in `grid()`. Same order as `grid()`. Counts with all six eligible cells: 30, 60, 102 (CONTRACT `grid.x1_counts_max`) |
| `tier(w) -> int` | 0 if W = 12 and q = 1; 1 if W = 12 and q = 2; 2 if W ∈ {8, 16}. W = 12, q = 3 → `ValueError` (never eligible) |
| `changed_factors(w) -> int` | number of factors ≠ w0: (p ≠ 1/5) + (σ ≠ 5/4) + (q ≠ 1) + (W ≠ 12), 0–4 (§5.5 step 3) |
| `distance(w) -> Fraction` | `P_INDEX[p] + SIGMA_INDEX[σ] + (q − 1) + (0 if W == 12 else 1)` (§5.5 step 4; midpoints count half steps) |
| `cells_of(worlds) -> list[(W, q)]` | distinct cells, ascending |

### 1.3 Centres, alias map, features, builders

| Name | Contract |
|---|---|
| `centres(W, n_axial=6) -> float64 [n_axial·W/2, 2]` | row `j = n_axial·i + b` holds `(0.5 + 2i, 0.5 + 2b)`, i < W/2, b < n_axial (MD-5). At W = 12 equals `GridCenters().centers(world, 36, rng)` bitwise |
| `anchored_labels(W, q) -> int64 [W/2]` | g(i) of §4.3: m = ⌈(W/2 − 1)/q⌉; g(0) = 0; g(i) = 1 + ((i − 1) mod m). CONTRACT `alias.maps` lists g, groups, n_A, V′ for W ∈ {6, 8, 12, 16} |
| `unanchored_labels(W, q) -> int64 [W/2]` | g(i) = i mod (W/(2q)); `ValueError` unless (W/2) mod q == 0. Dry-run negative control only (DR3) |
| `n_labels(labels) -> int`; `v_prime(labels, n_axial=6) -> int` | n_A = max + 1; V′ = n_axial·n_A |
| `symbol_sizes(labels, n_axial=6) -> int64 [V′]` | \|v\| = number of centres merged into v = 6g + b (E2) |
| `merge_columns(E_centres, labels, n_axial=6) -> float64 [N, V′]` | E′[:, n_axial·g + b] = Σ_{i: g(i)=g} E_centres[:, n_axial·i + b], summed in ascending i (never averaged or renormalised). At q = 1 with W = 12 the result equals `E_centres` bitwise |
| `features(coords, W) -> float64 [N, 2]` | `np.column_stack((np.cos(a), np.sin(a)))`, `a = 2.0*np.pi*x/W`, x = coords[:, 0]; bitwise equal to `oracle_profile.circle_features(coords)` at W = 12 (DR5) |
| `build_world(W, Hh=12) -> WorldSpec` | `world.registry.build_world(WorldConfig("cylinder", (W, Hh), "flat"))` |
| `build_transition(world, p) -> TransitionSpec` | `TransitionBuilder().build(world, TransitionConfig(p_stay=float(p)))` |
| `centre_emission(world, W, sigma, n_axial=6) -> float64 [N, n_axial·W/2]` | W = 12 and n_axial = 6: `OverlapGaussian().build(world, EmissionConfig("overlap", 36, float(sigma), "grid"), SeedTree(1729))` then `oracle_profile.canonical_emission(spec.E, spec.symbol_perm)`. Otherwise: `d = point_distances(world, centres(W, n_axial), "flat")`, `logits = -(d**2) / (2.0 * float(sigma)**2)`, `E = np.exp(logits - logsumexp(logits, axis=1, keepdims=True))` (`scipy.special.logsumexp`; the expression of `emission._overlap_core`, not imported). A centre outside the chart raises `StageFailure` (E1) |
| `build_process(w, alias="anchored", Hh=12, n_axial=6) -> dict` | Steps §4.6 1–5. Returns `{"key", "world_key": World, "W", "q", "sigma", "p", "tier", "world": WorldSpec, "T": float64 [N, N], "pi": float64 [N], "E_centres": float64 [N, n_axial·W/2], "E": float64 [N, V′] (canonical, aliased), "labels": int64 [W/2], "sizes": int64 [V′], "V": V′, "N": N, "n_axial", "coords": float64 [N, 2], "features": float64 [N, 2], "e1": dict}`. `alias` ∈ {`"anchored"`, `"unanchored"`}. Builder `StageFailure` or `oracle_profile.ProfileError` → returned with `e1 = {"status": "INELIGIBLE/E1", "reason": str}` and the array fields absent (choice 5); otherwise `e1 = {"status": "PASS", "validate": validate_process(...) maxima}` |
| `build_known_zero(kind) -> dict` | `kind` ∈ {"U", "N"} at w0 geometry (W = 12, p = 1/5): `Unique` with `EmissionConfig("unique", 144, None, "grid")`, or `Identical` with `EmissionConfig("identical", 36, None, "grid")`, each with `SeedTree(1729)`, then `canonical_emission`. Same dict as `build_process` with key `U-W12`/`N-W12`, `n_axial` 12 (U) or 6 (N) (choice 8), tier 0 |
| `build_tiny(sigma=Fraction(1), p=Fraction(1, 2), alias="anchored", q=1) -> dict` | DR1 tiny world: `build_world(6, 2)`, `centres(6, n_axial=1)` = (0.5 + 2i, 0.5), i < 3, mirrored softmax, labels `anchored_labels(6, q)` (or unanchored), n_axial 1. Same dict shape |

### 1.4 Symmetry and exact filters E1–E3

| Name | Contract |
|---|---|
| `translate_states(W, Hh, s) -> int64 [N]` | z = x·Hh + y ↦ ((x + s) mod W)·Hh + y |
| `reflect_states(W, Hh, c) -> int64 [N]` | z ↦ ((c − x) mod W)·Hh + y |
| `symmetry_check(E, W, Hh=12, tol=1e-9) -> dict` | For every s ∈ 1..W−1 and c ∈ 0..W−1: `dev = max |E[perm] − E|`. Returns `{"translations": [s with dev ≤ tol], "reflections": [c with dev ≤ tol], "min_dev_translation": float, "min_dev_reflection": float, "symmetric": bool}` (E3, §4.3). T commutes with both maps, so E′ decides |
| `e2_check(p_v, sizes, V_centres) -> dict` | `{"status": "PASS" | "INELIGIBLE/E2", "worst": {"v", "p_v", "threshold"}}`; pass iff every `Fraction(float(p_v[v])) ≥ Fraction(sizes[v], 2·V_centres)` (OPEN-4 ruling; V_centres = n_axial·W/2) |
| `exact_filters(proc, p_v) -> dict` | E1 (from `proc["e1"]`), E2 (`e2_check`), E3 (`symmetry_check(proc["E"], W, Hh)`; any translation or reflection → `INELIGIBLE/E3`). First failing in order E1, E2, E3 sets `status`; all three records kept |

## 2. `hws_stats.py` (≈150 lines): means, SEs, bounds, z constants, bootstrap, E5, nulls

| Name | Contract |
|---|---|
| `z_of(alpha: Fraction) -> float` | `statistics.NormalDist().inv_cdf(float(1 - alpha))` |
| `Z1`, `ZW`, `Z3`, `ZNULL`, `Z975` | `z_of` of CONTRACT `z.Z1.alpha` (1/100), `ZW` (1/24640 = 0.05/(4·308)), `Z3` (1/320), `ZNULL` (1/432600 = 0.01/(2·2163)), `central95` (1/40). Report-only decimals in CONTRACT (2.3263…, 3.9409…, 2.7344…, 4.5812…, 1.9600…) |
| `RANK_F` | `c1_means.rank_for(Fraction(1, 320), 5000)` = 16, checked at import (mismatch → `HwsStop("FAIL_TECHNICAL/NUMERICAL", …)`) |
| `summary(x) -> dict` | x float64 [n], finite. `{"n", "mean": float(c1_means.tree_mean(x)), "sd": float(np.std(x, ddof=1)), "se": sd/√n}` (choice 10) |
| `screen_bounds(x) -> dict` | `summary(x)` plus `"L1" = mean − Z1·se`, `"U1" = mean + Z1·se`, `"Lw" = mean − ZW·se`, `"Uw" = mean + ZW·se` (§5.3 items 1–2) |
| `s3_bounds(x, boot) -> dict` | `screen_bounds(x)` plus `"L3_normal" = mean − Z3·se`, `"L3_boot"` = `c1_means.quantile_with_rank(boot, Fraction(1, 320))[0]` (rank 16 of 5,000), `"L3" = min(L3_normal, L3_boot)`, `"central95_boot"` = values at ranks 125 and 4,875 (`quantile_with_rank` at 1/40 and 39/40) |
| `normal95(s) -> (lo, hi)` | `mean ∓ Z975·se` (hand-off intervals for non-bootstrapped quantities; choice 21) |
| `bootstrap(arrays: dict[str, float64 [n]], seed: int) -> dict[str, float64 [5000]]` | `c1_means.bootstrap_means(arrays, seed, 5000)` unchanged (one index vector per draw shared by every array) |
| `null_z(x) -> dict` | `s = summary(x)`; `z = |mean|/se`; `se == 0` → `z = 0.0` if `mean == 0` else `inf` (choice 10). Returns `{"mean", "se", "z", "exceeds": z > ZNULL}` |
| `e5(m32) -> dict` | m32 float64 [n, 2]. `norm = ‖m32‖`; `phase = k4b_scores.oracle_phase(m32)`; `bins = np.minimum(np.floor(phase·12/(2π)).astype(int), 11)`, counts over 12 bins; `u = scores.unit_vectors(phase)`; `resultant = ‖mean(u)‖`. `pass` iff `100·#(norm ≥ 0.2) ≥ 95·n` and `64·min(counts) ≥ n` and `resultant ≤ 0.30` (§2.5; choice 11). Returns `{"frac_norm_ge_0.2", "bin_counts": [12 ints], "min_bin", "resultant", "pass"}` |
| `pinsker_violations(slack, tol=1e-12) -> int` | `#(slack < −tol)` (§2.3; report only) |
| `entropy_diff(ha, hb) -> dict` | per-row difference `ha − hb`: `summary` of it (KC13 cross-check form) |

## 3. `hws_oracle.py` (≈230 lines): streams, sampling, per-row arrays, nulls, P4

| Name | Contract |
|---|---|
| `KS_SCREEN`, `KS_S0`, `KS_S3` | `(1, 2, 4, 8, 16, 32)`, `(1, 2, 3, 4, 8, 16, 32)` (choice 15), `(1, 2, 4, 6, 8, 12, 16, 24, 32)` |
| `NULL_NAMES` | `("m4_phase", "sha_suffix", "orth_1", "orth_2", "orth_4", "orth_8", "orth_16")` |
| `history_generator(stage, key, origin=None) -> Generator` | `SeedTree(0).generator("data", "hws-v1", stage, key)` for stage ∈ {S0, S1, X1, S2, S3, DRY}; `stage == "NULLCHK"` requires `origin` and gives `SeedTree(0).generator("data", "hws-v1", "NULLCHK", origin, key)`; any other stage → `ValueError` |
| `perm_generator(key) -> Generator` | `SeedTree(0).generator("hws-v1", "prefix_perm", key)` (§6.6) |
| `sample(proc, n, rng, layout=SequenceLayout()) -> uint8 [n, Lh]` | Exactly one call `HMMSampler(proc["T"], proc["E"], proc["pi"], layout).sample(n, rng)` (RC-5). `Lh = layout.n_obs − 1`. Returns `np.ascontiguousarray(tokens[:, :Lh], dtype=np.uint8)`; column w33 and the states are deleted at once and never returned or stored |
| `beliefs(proc, tok, Ks) -> dict[int, float64 [n, N]]` | `{K: oracle_profile.suffix_posterior(T, E, pi, tok, K)}` for every K in Ks plus `Lh` (full history) |
| `predictive(b, T, E) -> float64 [n, V′]` | `(b @ T) @ E` (q_K, §0.2) |
| `circ_marginal(q, n_axial) -> float64 [n, n_A]` | `q.reshape(n, n_A, n_axial).sum(axis=2)` (q^A, v = n_axial·g + b) |
| `x_marginal(b, W, Hh) -> float64 [n, W]` | `b.reshape(n, W, Hh).sum(axis=2)` (b^x; state id x·Hh + y) |
| `kl_rows(p, q) -> float64 [n]` | Σ_v p (log p − log q), terms with p = 0 are 0; q = 0 where p > 0, or a non-finite input → `HwsStop("FAIL_TECHNICAL/NUMERICAL", …)` (the `context_gain` convention, choice 9) |
| `entropy_rows(p) -> float64 [n]` | −Σ p log p, p = 0 terms 0 |
| `row_arrays(proc, tok, Ks) -> dict` | The per-row arrays of §4.7 step 3, keys below. `Lh = tok.shape[1]`; m_K = b_K @ features; D_K = `k4b_scores.phase_scores(k4b_scores.oracle_phase(m_L), m_L, m_K)`; rn_K = `scores.r4_norms(m_L, m_K)` |
| `prefix_permuted(tok, rng) -> uint8 [n, Lh]` | copy of `tok`; `out[:, :Lh−4] = rng.permuted(tok[:, :Lh−4], axis=1)` (one call; each row independently and uniformly permuted; w29..w32 kept) (choice 22) |
| `p4_rows(proc, tok, mL, rng) -> float64 [n]` | `‖mL − m_L(prefix_permuted(tok, rng))‖²` with the full-history filter (S3 only, rng = `perm_generator(key)`) |
| `world_look(proc, stage, n, Ks, origin=None, layout=SequenceLayout(), p4=False) -> dict` | `rng = history_generator(stage, proc["key"], origin)`; `tok = sample(proc, n, rng, layout)`; `rows = row_arrays(proc, tok, Ks)`; if `p4`: `rows["P4"] = p4_rows(...)`. Returns `{"tok": tok, "rows": rows, "stream": ["data", "hws-v1", stage, (origin,) key]}` |

**`row_arrays` keys** (every value float64 [n] unless stated; K ranges over `Ks` without `Lh`):
- `m[K]` float64 [n, 2] for every K in Ks and `Lh`; `D[K]`; `rn[K]` (‖r_K‖); `G[K]` = `kl_rows(q_Lh, q_K)` (G_1 is G_C rows); `G0` = `kl_rows(q_Lh, π T E)` (rowwise against the stationary predictive); `G4A` = `kl_rows(qA_Lh, qA_4)`; `IZ4` = `kl_rows(b_Lh, b_4)`; `IX4` = `kl_rows(bx_Lh, bx_4)`;
- entropies `Hq[K]`, `HqA[K]`, `Hb[K]`, `Hbx[K]` for K ∈ {4, Lh} (KC13 cross-checks);
- `Hb1` = `entropy_rows(b_1)` when 1 ∈ Ks (KC3's s);
- `m_norm` = ‖m_Lh‖; `phase` = `k4b_scores.oracle_phase(m_Lh)`;
- `nulls`: dict over `NULL_NAMES`: `m4_phase` = `phase_scores(k4b_scores.m4_phase(m_4), m_Lh, m_4)`; `sha_suffix` = `phase_scores(k4b_scores.sha_phase(tok), m_Lh, m_4)` (requires Lh = 32; on the tiny world it is omitted); `orth_K` = Σ_j m_K[:, j]·(m_Lh − m_K)[:, j] for K ∈ {1, 2, 4, 8, 16} ∩ Ks;
- `pinsker_slack` = 2·IX4 − rn[4]²;
- `gain_ind` = (G4A ≥ 0.005) as float64 (p_gain rows); `weak_ind` = (m_norm < 0.1) as float64 (p_weak rows); `m_sq` = m_norm² (R2 rows);
- `norm_err` = max over K of max |Σ b_K − 1| (scalar float; E6, ≤ 1e-12).

## 4. `hws_exact.py` (≈220 lines): exact per-world values, enumeration, spot checks, KC1

| Name | Contract |
|---|---|
| `symbol_law(proc) -> float64 [V′]` | `pi @ E` |
| `last_symbol_posteriors(proc) -> float64 [V′, N]` | r_w = π∘E[:, w] / p(w) |
| `mean_last_entropy(proc) -> float` | Σ_w p(w) H(r_w) (KC3) |
| `a_eff(proc) -> float` | exp(Σ_w p(w) H(r_w)) (§2.4) |
| `p_d2a(T, E, pi, alphabet=(0, 1, 2, 3, 4), Lh=32) -> float` | `s = E[:, alphabet].sum(axis=1)`; `a = pi * s`; then Lh − 1 times `a = (a @ T) * s`; return `float(a.sum())` = π·D_S·(T·D_S)^31·1 (§2.6). Alphabet symbols ≥ V′ are ignored |
| `e4_check(value, tau=Fraction(1, 2000000)) -> dict` | `{"status": "PASS" if Fraction(float(value)) <= tau else "INELIGIBLE/E4", "p_D2a": value}` (equality passes) |
| `exact_world(proc) -> dict` | `{"p_v": list, "min_p": float, "A_eff": float, "mean_last_entropy": float, "p_D2a": float, "V": V′, "n_A": int, "symmetry": dict, "e1", "e2", "e3", "e4", "status": first failing of E1..E4 else "PASS", "tier", "changed", "distance": str}` (§4.6 step 6; worlds failing E1 carry only the E1 record) |
| `enumerate_histories(proc, Lh) -> (int64 [V′^Lh, Lh], float64 [V′^Lh])` | every history in lexicographic order with its exact-up-to-float64 probability by the forward recursion (DR1, tiny world only; refuses V′^Lh > 10^6 with `ValueError`) |
| `exact_expectations(proc, Lh, Ks) -> dict` | Probability-weighted means of `hws_oracle.row_arrays` over `enumerate_histories`: `D[K]`, `B[K]` (= E rn), `V[K]` (= E rn²), `G[K]`, `G4A`, `IZ4`, `IX4`; plus the identity checks I1 (max over the suffix tables of |E[g(S_K) r_K]| for g the indicator of each suffix), I2 (0 ≤ D4 ≤ B4), I3 (V_K = E‖m_L‖² − E‖m_K‖², non-increasing), I4 (rowwise D ≤ rn), Proposition F (E KL(q_L ‖ f(S4)) ≥ G4 for f = q_4, uniform, π T E), row-wise Pinsker; each as `{"value", "pass"}` |
| `suffix_enumeration(proc, Ks=(1, 2, 3)) -> dict[int, dict]` | For each K: every suffix in {0..V′−1}^K, its stationary probability P(S_K) (`p_d2a`-type forward recursion without mask) and the posterior b_K; `{"E_m_sq": Σ P‖m_K‖², "E_Hq": Σ P H(q_K), "n_suffixes": V′^K}` (KC9) |
| `decimal_spot_check(proc, tok, Ks) -> dict` | `error_bound.reference_moments(T, E, pi, coords, tok, Ks)` against `m_K` from `oracle_profile.posterior_means`; gap per row and K by exact `Fraction` comparison (`Fraction(float(m)) − Fraction(ref)`); `{"max_gap": str(Fraction), "pass": max_gap ≤ error_bound.MOMENT_TOL_EXACT}`. W = 12 only (`ValueError` otherwise) |
| `bayes_cross_check(proc, tok) -> dict` | `BayesFilter(T, E, pi).belief_at(tok, Lh)` vs `suffix_posterior(T, E, pi, tok, Lh)`; `{"max_abs", "pass": max_abs ≤ 1e-12}` |
| `law_bound_report(proc, enclosure=None) -> dict` | Tier-0 report only (§8). Saves `process_law.LAW["sigma"]`, `LAW["neighbour"]`; sets them to `proc["sigma"]` and `(1 − proc["p"])/4` (Fractions); calls `(enclosure or process_law.process_law_bound)(T, E, pi, coords)` with the canonical (centre-order) E; restores both in `finally`. `decimal.Inexact` → `{"status": "UNAVAILABLE/NONTERMINATING_LOGIT", "reason"}`; any other exception propagates (technical failure). Never changes eligibility, ranking or selection (choices 27, 28) |
| `read_json(path) -> object` | the only file reader of KC1: refuses (`HwsStop("FAIL_TECHNICAL/KNOWN_CASE", …)`) any path whose suffix is not `.json`; records every path read in the module list `JSON_READS` (DR7 proof) |
| `expected_envelope(kind, seed=None, world_id=None) -> dict` | KC1 (d): `WorldSpec` → `{"config": asdict(WorldConfig("cylinder", (12, 12), "flat")), "parent_ids": [], "seed_map": {}}`; `TransitionSpec` → `{"config": asdict(TransitionConfig(p_stay=0.2)), "parent_ids": [world_id], "seed_map": {}}`; `EmissionSpec` → config `asdict(EmissionConfig("overlap", 36, 1.25, "grid"))` plus `replicate = seed`, `world_scope_master = 0`; seed map = the rebuild tree's `issued` plus `{"world_scope/" + k: v}` for a fresh `SeedTree(0)` after `seed("centers", "cylinder")`; parent_ids `[world_id]` |
| `kc1_identity(artifact_root, manifest_path, config_json_path, seeds=(1729, 2718, 3141)) -> dict` | §3 KC1 (a)–(d), JSON reads only through `read_json`, plus `hashlib.sha256` of those JSON files' bytes. Order per artifact: manifest file sha256 = config `inputs_sha256["INPUT_IDENTITIES.json"]`; meta.json sha256 = manifest `meta_sha256`; `meta.status == "complete"`; `meta.artifact_type` and `meta.artifact_id` as expected; `canonical_json(meta.config) == canonical_json(expected config)`; `make_artifact_id(type, meta.config, meta.parent_ids, meta.schema_version) == id`; `meta.parent_ids` and `meta.seed_map` as expected; `payload_checksum(spec.to_payload()[0], stored_extra) == meta.payload_sha256 == manifest sha256` (rebuild by the src builders of §3 KC1). Extra diff field by field (report only). Returns `{"status": "PASS" | "FAIL_TECHNICAL/KNOWN_CASE", "artifacts": {"<Type>/<id>": {"checks": {name: bool}, "extra_diff": [...]}}, "json_reads": [...]}` |

## 5. `hws_select.py` (≈250 lines): eligibility, criteria, classes, ranking, finalists, X1/S2, outcomes, pause

### 5.1 Thresholds and quantities

| Name | Contract |
|---|---|
| `C1_MIN`, `C2_MIN`, `G4_FLOOR_MIN`, `BELOW_3X_MIN`, `TAU_D2A` | `Fraction(3, 100)`, `Fraction(1, 10)`, `Fraction(39, 5000)` (= 0.0078), `Fraction(1, 50)`, `Fraction(1, 2000000)` |
| `CRITERIA` | `(("C1", "D4"), ("C2", "GC"), ("C3", "G4"), ("C4", "G4A"))` |
| `floors(g4_w0: float, g4A_w0: float) -> dict` | `{"D4": 0.03, "GC": 0.10, "G4": max(g4_w0, 0.0078), "G4A": g4A_w0}` (floats; g4*, g4A* of §2.4, frozen at S0) |
| `criteria(bounds: dict[str, dict], floors, which) -> dict` | `which` ∈ {"L1", "Uw", "L3", "Lw"}. `{"C1": bounds["D4"][which] >= floors["D4"], …}` (equality passes) |

### 5.2 Eligibility, classes, annotations

| Name | Contract |
|---|---|
| `eligibility(exact_status, e5_pass, e6_ok) -> str` | `e6_ok` False → raises `HwsStop("FAIL_TECHNICAL/E6", …)` (never a scientific exclusion, §5.1); else `exact_status` if not PASS; else `"INELIGIBLE/E5"` if not `e5_pass`; else `"ELIGIBLE"` |
| `classify(look, floors) -> dict` | `look`: `{"eligibility", "bounds"}` (screening). Returns `{"class", "failed": [C…]}`: INELIGIBLE/<f>; else `EXCLUDED/<first failing of C1..C4 under Uw>` (full list in `failed`; choice 12); else `CANDIDATE/CONFIDENT` if `L1` passes C1–C4; else `CANDIDATE/POSSIBLE` if `D4.mean ≥ 0.03`; else `CANDIDATE/MARGINAL` (§5.4, R-HWS-1) |
| `annotations(D4_bounds) -> list[str]` | `ORACLE_POSITIVE_BELOW_C_MARGIN` iff 0 < Lw ≤ Uw < 0.01; `ORACLE_POSITIVE_BELOW_SWEEP_REQUIREMENT` iff Lw > 0 and Uw < 0.03 (§7.3; on the latest look; never decision-bearing) |

### 5.3 Ranking, finalists, S3 evaluation

| Name | Contract |
|---|---|
| `rank_key(rec) -> tuple` | `(0 if CONFIDENT else 1, tier, changed, distance (Fraction), −bounds["G4"]["L1"], key)` (§5.5) |
| `finalists(records) -> dict` | `records`: the latest screening record per world. Ordinary: the first 16 of CONFIDENT ∪ POSSIBLE sorted by `rank_key`. If that set is empty: `fallback_only` = eligible worlds (choice 13) with `Uw(D4) ≥ 0.02` and Uw passing C2–C4, the 16 with the largest `D4.mean`, ties by ascending key (§5.6 item 2, RC-1). Returns `{"ordinary": [key…], "fallback_only": [key…]}` (at most one list non-empty) |
| `s3_evaluate(rec_s3, floors, kind) -> dict` | `kind` ∈ {"ordinary", "fallback_only"}. `ok = eligibility PASS (E1–E5 on S3 rows) and E6`; `qualifies = (kind == "ordinary") and ok and criteria(L3) all`; `below_3x = ok and C2–C4 pass at L3 and L3(D4) ≥ 0.02`; `at_3x = below_3x and L3(D4) ≥ 0.03`. Returns those booleans plus `criteria_L3` |
| `selection(finalists, s3) -> dict` | `selected` = the first ordinary qualifier in finalist order (no re-ranking); `fallback_list` = the next two ordinary qualifiers; fallback-only worlds never appear (§5.6 items 3–4) |

### 5.4 Extension, refinement and outcome rules

| Name | Contract |
|---|---|
| `x1_trigger(records) -> dict` | After S1 only. Fires iff no record is CANDIDATE/* and the eligible world with the largest `D4.mean` (ties by ascending key; choice 41) has p = 15/16 or σ = 3. Returns `{"fire", "world": key or None, "add_p": p == 15/16, "add_sigma": σ == 3}`; no eligible world → `fire` False, `world` None (RC-6) |
| `s2_worklist(records, cap=40) -> list[World]` | Fires iff ≥ 1 CANDIDATE/* after S1 (and X1). Lowest tier containing a candidate; every pair of eligible worlds in that tier differing only in p or only in σ at adjacent levels of the extended level lists (grid + X1 levels that ran) whose candidate status differs (CANDIDATE/* vs not; choice 14); midpoint from `S2_P_MID` / `S2_SIGMA_MID`; dedupe; sort by `(changed, distance, key)`; keep the first 40 (§6.2 item 2) |
| `outcome(state) -> dict` | `state`: `{"fail": reason or None, "complete": bool (every scheduled stage completed, no uncontinued pause, authority valid), "records": latest look per world, "finalists", "s3": {key: s3_evaluate}, "floors"}`. Precedence of §7.1: FAIL_TECHNICAL/<reason>; INCONCLUSIVE/RESOURCE_OR_AUTHORITY; HWS_SELECTED/T<tier of selected>; HWS_BELOW_3X (any S3 world with `below_3x`); HWS_NO_WORLD_CONFIRMED (some world not INELIGIBLE on its latest look with Uw passing C1–C4 on its latest look, RC-7); HWS_NO_SUITABLE_WORLD/HEADROOM (every evaluated world INELIGIBLE or EXCLUDED, ≥ 1 eligible world, every eligible world has Uw(D4) < 0.03) or /FILTER (otherwise). No branch applies → `FAIL_TECHNICAL/OUTCOME` (choice 35). Returns `{"outcome", "selected", "fallback_list", "below_3x_worlds", "at_3x_fallback_only", "absence_3x_shown", "unresolved", "max_D4": {"value", "key"}, "licence"}` |
| `absence_shown(records) -> bool` | True iff every evaluated world that is not INELIGIBLE has Uw failing ≥ 1 of C1–C4 on its latest look (BELOW_3X licence; choice 34) |
| `licence(outcome, fill) -> str` | CONTRACT `licences` template for the outcome head, `str.format(**fill)`; T1/T2 append `HWS_SELECTED_T1_T2_addendum` |

### 5.5 Budget and the 3× pauses (§9)

| Name | Contract |
|---|---|
| `rate(stage, w) -> int` | screening (S1, X1, S2): W 8 → 4, 12 → 8, 16 → 13; S3: W 8 → 70, W 12 tier 0 → 190, tier 1 → 160, W 16 → 235 (CONTRACT `cpu.rates_s`); S0 → `ValueError` |
| `forecast(stage, worklist) -> int` | S0 → 360; J1 → 540; else Σ `rate(stage, w)` over the actual worklist (computed when the worklist is fixed; never re-estimated) |
| `pause_check(stage_cpu, stage_fc, cum_cpu, cum_fc) -> dict` | `{"pause": stage_cpu > 3·stage_fc or cum_cpu > 3·cum_fc, "trigger": "STAGE" | "CUMULATIVE" | "BOTH" | None, …inputs}`. `cum_fc` is the cumulative central forecast through the end of the current stage (§9.3). Strict ">" (choice 26) |

## 6. `hws_driver.py` (≈340 lines): stages, records, report, SELECTION.json, freeze, CLI

### 6.1 Records

| Name | Contract |
|---|---|
| `append_stage_event(out, event: dict)` | appends `json.dumps(event, sort_keys=True, default=str)` + "\n" to `out/STAGES.jsonl` with `utc` (choice 25). Events: `STAGE_BEGIN {stage, worklist: [key…], forecast_s}`, `WORLD_COMPLETE {stage, key, files: {relpath: sha256}, cpu_s}`, `PAUSE {stage, check}`, `CONTINUE {stage, decision_sha256}`, `STAGE_COMPLETE {stage, files: {relpath: sha256}}`, `STOP {stage, status, reason}` |
| `look_record(proc, exact, look, stage, n) -> dict` | the per-world-look aggregate (§6.4 below); written by exclusive create to `stages/<stage>/worlds/<key>.json` |
| `save_hist(out, stage, key, tok, origin=None) -> Path` | `stage_records.save_npz(out/"hist"/stage/f"{key}.npz", canon32=tok)` (NULLCHK: `hist/NULLCHK/<origin>/<key>.npz`); tok uint8 [n, 32] (choice 24) |
| `tree_sha(out, prefixes) -> str` | sha256 of `canonical_json({relpath: sha256})` over every file under the given store subdirectories (S0 store hash; choice 39) |
| `archive_partial(out, stage) -> Path or None` | resume (RC-5): every file under `stages/<stage>/` or `hist/<stage>/` not listed in a `WORLD_COMPLETE` event of that stage moves to `superseded/<stage>-<utc>/` with a `SHA256SUMS` manifest (choice 40) |

### 6.2 Stage functions

| Name | Contract |
|---|---|
| `g0(out, root=ROOT) -> dict` | §6.6 G0: `seed_search(root, CONTRACT seeds.g0_needles)` then `classify_seed_hits`. Gate `G0` PASS or `FAIL_TECHNICAL/SEED_SCOPE` (choice 33) |
| `seed_search(root, needles) -> list[dict]` | text search of `*.json`, `*.jsonl`, `*.md`, `*.py`, `*.txt`, `*.yaml` under `root`, skipping `.git`, `.venv`, `__pycache__`, every `00_READ_ME_FIRST*` path and every `docs/research_summary/` path (never opened), and every binary or payload file. Hit `{"path", "needle", "line"}` |
| `classify_seed_hits(hits) -> dict` | kind `hws_declaration` for paths under `tools/hws/`, `tests/hws/` (any worktree), `agent-handoff/`, `hws-store/`, `topo-scratch/hws-dry/`; every other hit `unclassified`. PASS iff every hit is `hws_declaration`; else `FAIL_TECHNICAL/SEED_SCOPE` with every hit listed |
| `run_s0(out, auth) -> dict` | Requires FREEZE.json (§6.5) and an `auth` record covering S0 (choice 29); G0; builds w0, U, N; one `world_look` each (w0: 32,768 rows, `KS_S0`; U, N: 4,096 rows); KC1–KC14 as gates `KC1`…`KC14` in `GATES.jsonl`; nulls by §5.3 with NULLCHK on exceedance (a reproduced exceedance → `FAIL_TECHNICAL/KNOWN_CASE`); bootstrap seed 620101 over w0's report arrays. Writes `stages/S0/S0_RECORD.json` (keys §6.4). Any KC failure → STOP `FAIL_TECHNICAL/KNOWN_CASE`; no later stage |
| `run_sweep(out, auth, s0_accept) -> dict` | Requires FREEZE.json, `auth` covering S1–S3, and `s0_accept` (coordinator ACCEPT JSON `{"accept": true, "s0_record_sha256"}` equal to the sha256 of `stages/S0/S0_RECORD.json`); floors from the S0 record. S1 over `grid()`: exact filters for all 225 (records of INELIGIBLE worlds written without sampling), one `world_look` per world passing E1–E4 (n 4,096, `KS_SCREEN`), classification; then `x1_trigger` → X1; then `s2_worklist` → S2; then `finalists` → S3 (n 32,768, `KS_S3`, P4, bootstrap 620103 per world, spot checks of §8, `law_bound_report` for tier-0 finalists); then `outcome`, report, SELECTION.json. Pause checks at every world and stage boundary (§5.5). Resume: `archive_partial`, then continue at the first world without `WORLD_COMPLETE` (regenerated from its original stream) |
| `null_recheck(out, proc, stage, look, n, Ks) -> dict` | For a look with any `exceeds`: one `world_look(proc, "NULLCHK", n, Ks, origin=stage)`; its histories saved; `reproduced` = the same null name exceeds again. Reproduced → `HwsStop("FAIL_TECHNICAL/NULL")` (`/KNOWN_CASE` at S0); else recorded and the world's status unchanged (§5.3 item 5) |
| `run_dry(out=DRY_STORE) -> dict` | The synthetic dry run of §13 (DR1–DR13, `TEST_PLAN.md` §4) with the real records, selection and report code, streams `("data", "hws-v1", "DRY", <case>)`; writes `stages/DRY/DRY_REPORT.json` with `{"cases": {DRn: {"status": "PASS" | "FAIL" | "NOT_APPLICABLE", "details"}}, "implementation_sha256", "all_pass"}` |
| `freeze(out, repo, h_exec, dry_report) -> dict` | Writes `out/FREEZE.json` by exclusive create (§6.5) |
| `main(argv=None) -> int` | subcommands `s0`, `sweep`, `dry`, `freeze`; options `--out`, `--auth <json>`, `--s0-accept <json>`, `--continue <json>` (owner decision after a pause), `--h-exec`, `--dry-report`. Exit codes: 0 complete; 2 refused (missing authority/accept/freeze, nothing sampled); 3 STOP (FAIL_TECHNICAL); 4 PAUSE |

### 6.3 Store layout (§12.3; CONTRACT `store_layout`)

`X:/Downloads/projects/topo-pilot/hws-store/` (dry run: `X:/Downloads/topo-scratch/hws-dry/`): `FREEZE.json`; `GATES.jsonl`; `STAGES.jsonl`; `stages/<S>/` (S ∈ S0, S1, X1, S2, S3, NULLCHK, FINAL, DRY) with `stages/<S>/worlds/<key>.json` per world-look; `worlds/<key>.json` (one summary per evaluated world, written once at report time); `hist/<stage>/<key>.npz` (uint8 [n, 32] key `canon32`; NULLCHK under `hist/NULLCHK/<origin>/`); `SELECTION.json`; `superseded/`; `logs/`; `cpu_ledger.json` (meter, never reset; the J1 ledger is the dry store's). Histories of every stage, NULLCHK and superseded attempts are kept (§11 row 10, RC-8).

### 6.4 Record and report keys

- **World-look record** `stages/<S>/worlds/<key>.json`: `key`, `W`, `q`, `sigma`, `p` (Fraction strings), `tier`, `changed`, `distance`, `stage`, `n`, `Ks`, `stream`, `hist` (relpath), `hist_sha256`, `exact` (`exact_world` output), `eligibility`, `e5`, `e6` (`norm_err`, finiteness, nulls, pinsker_violations, spot checks), `bounds` (`screen_bounds` for `D4`, `GC`, `G4`, `G4A`; S3: `s3_bounds`), `profile` (`summary` per K of D_K, B_K = rn, V_K = rn², G_K), `report` (`G0`, `IZ4`, `IX4`, `H_star` = mean Hq[L], `R2`, `p_weak`, `p_gain`, `A_eff`, `p_D2a`, `perplexity_ratio` = e^{Ĝ4}, `entropy_diff` for G4, G4A, IZ4, IX4: KL-row mean, entropy-difference mean, their difference and its SE), `nulls` (`null_z` per name, plus `recheck`), `class`, `failed`, `annotations`, `cpu_s`. S3 adds `P4` (`mean(P4 rows)/mean(rn[4]²)`, or `"undefined"` when the denominator is 0), `L3` per criterion, `central95`, `s3_eval`, `spot_check`, `law_bound` (tier 0).
- **S0 record** `stages/S0/S0_RECORD.json`: `kc` (`KC1`…`KC14`: `{"status", "value", "reference", "tolerance", "s", "n_r"}`), `G4hat_w0`, `G4Ahat_w0`, `g4_star`, `g4A_star`, `per_row_sd_w0` (D4, rn4, GC, G4, G4A), `w0_record`, `U_record`, `N_record`, `s0_store_sha256` (= `tree_sha(out, ["stages/S0", "hist/S0", "hist/NULLCHK/S0"])` over the files written before the record), `protocol_sha256`, `freeze_sha256`.
- **Report** `stages/FINAL/REPORT.json`: `outcome`, `licence`, `selected`, `fallback_list`, `finalists` (`ordinary`, `fallback_only`), `s3` per finalist, `classes` (count per class), `worlds` (key → latest class, D4 bounds, annotations), `x1` (trigger record), `s2` (worklist), `below_3x_worlds`, `at_3x_fallback_only`, `absence_3x_shown`, `unresolved`, `max_D4`, `floors`, `z` (Z1, ZW, Z3, ZNULL values), `cpu` (per stage: forecast, measured, 3× thresholds, pauses), `nulls` (every exceedance and its recheck), `pinsker_flags`, `protocol_sha256`, `freeze_sha256`, `s0_record_sha256`. `worlds/<key>.json` per world: every look record path and sha256, latest class, bounds, annotations.
- **SELECTION.json** (written only for HWS_SELECTED, choice 32; §10.1): `world` (`key`, W, q, σ, p, `tier`), `configs` (`WorldConfig`, `TransitionConfig`, `EmissionConfig` for tier 0, else `centres`, `alias_labels`, `alias_sha256`), `canonical_label_order` = "v = 6g + b", `sha256` of `T`, `E`, `pi`, `coords` bytes (C order, float64), `source_commit` (h_exec), `freeze_sha256`, `streams` (discovery and S3 scopes), `effects` (S3 point, central 95 %, L3 for D_K, B_K, V_K at K ∈ {1, 2, 4, 6, 8, 12, 16, 24}; G_K, G_C, G_0, G4A, IZ4, IX4 in nats and bits, H*; `m_norm` quantiles (0, .05, .25, .5, .75, .95, 1), `phase_bins`, R2, p_weak, p_gain, A_eff, P4; per-row SDs of D4 and rn4; p_D2a), `stage_c` (`M` = 1/100, `D4_over_M`, `delta_max` = L3(D4)/3), `search_record` (path and sha256 of REPORT.json), `fallback_list`, `cpu_per_stage`.

### 6.5 FREEZE.json (CONTRACT `freeze_fields`)

`protocol` ("HWS-FROZEN-v1"), `protocol_sha256`, `contract_sha256`, `api_sha256`, `test_plan_sha256`, `h_exec` (commit), `implementation_files` (`{relpath: sha256}` of every `tools/hws/*.py` and `tests/hws/*` file at h_exec), `implementation_sha256` (sha256 of `canonical_json(implementation_files)`; choice 31), `reuse_sha256` (CONTRACT list, re-hashed, must equal), `dry_run_report_sha256`, `dry_run_report_path`, `environment` (python, numpy, scipy versions), `created_utc`. Every stage job verifies FREEZE.json against the working tree before any sampling; a mismatch is `FAIL_TECHNICAL/FREEZE` with nothing sampled.

## 7. `hws_meter_bind.py` (≈90 lines): meter binding (§9.2, RC-9)

| Name | Contract |
|---|---|
| `bind(job_id, task_sha256, out, worker_session) -> None` | `k4b_meter_bind.bind(job_id, task_sha256, out, worker_session)` unchanged, **then** `winjob.MEMORY_CAP = 8 * 1024**3` and `k4b_meter_bind.TEMP_ROOT = str(out)` (so `child_env(job)` gives TEMP/TMP/TMPDIR = `<out>/tmp-<job>`). Other values from K4b's bind stay: ledger, lock, logs under `out`; `CAP_S = STOP_NEW_S = inf`; `OUTPUT_CAP = 4 GiB` |
| `effective_settings() -> dict` | `{"memory_cap": winjob.MEMORY_CAP, "temp_root": k4b_meter_bind.TEMP_ROOT, "ledger": str(meter.LEDGER), "cap_s": meter.CAP_S, "output_cap": meter.OUTPUT_CAP, "thread_vars": list(meter.THREAD_VARS)}` (DR12 check) |
| `main() -> int` | argv: `--job`, `--task-sha256`, `--session`, `--out` (required), then the meter argv. `bind`; refuses (exit 3) when `RUN.lock` exists and does not name the session; `op_guard.archive_stale(out)` when `METER_ACTIVE.lock` is absent; `meter.limit_reason = k4b_meter_bind.make_limiter(op_marker=out/op_guard.MARKER)`; `os.environ.update(k4b_meter_bind.child_env(job))`; `sys.argv = [argv0] + k4b_meter_bind.rewrite_argv(rest)` (`--max-cpu inf --max-wall inf`); `return meter.main()` (choice 30). `disk_reason` (C: ≥ 2 GB, X: ≥ 30 GB) and `classify_stop` are used unchanged through the limiter |

## 8. Reused functions, unchanged (§12.2; real signatures at 1d629bc = 0a67c5a for these paths)

| Module (path) | Name and signature |
|---|---|
| `topo_pilot.world.registry` (`src/topo_pilot/world/registry.py:41`) | `build_world(cfg: WorldConfig) -> WorldSpec` |
| `topo_pilot.world.config` (`:10`) | `WorldConfig(family: str, dims: tuple[int, ...] = (12, 12), metric: "flat"|"graph" = "flat", params: Mapping = {})` |
| `topo_pilot.process.transition` (`:16`, `:46`) | `TransitionConfig(kind="max_degree_lazy_walk", p_stay: float = 0.2)`; `TransitionBuilder().build(world: WorldSpec, cfg: TransitionConfig) -> TransitionSpec` (fields `T`, `pi`, `p_stay`, `d_max`) |
| `topo_pilot.process.emission` (`:35`, `:130`, `:191`, `:203`) | `EmissionConfig(mode: str, V: int = 36, sigma: float | None = 1.25, center_strategy="grid", source_mode=None, metric="flat")`; `OverlapGaussian().build(world, cfg, rng_tree: SeedTree) -> EmissionSpec` (fields `E` named, `symbol_perm`, …); `Identical().build(...)`, `Unique().build(...)` (V = N) |
| `topo_pilot.process.centers` (`:47`) | `GridCenters().centers(world, n_centers: int, rng) -> float64 [V, 2]` (test reference only) |
| `topo_pilot.process._geometry` (`:67`) | `point_distances(world, points: float64 [V, D], metric="flat") -> float64 [N, V]` (public name in a private module; imported by name, choice 1) |
| `topo_pilot.contracts.base` (`:125`, `:170`) | `Artifact.to_payload() -> (arrays: dict, extra: dict)`; `payload_checksum(arrays, extra) -> str` |
| `topo_pilot.contracts.ids` (`:50`, `:73`, `:99`; all re-exported by `topo_pilot.contracts`) | `make_artifact_id(artifact_type: str, config: Mapping, parent_ids: Sequence[str], schema_version: str = SCHEMA_VERSION) -> str`; `canonical_json(obj) -> str`; `SeedTree(master: int)` with `.seed(name, *scope) -> int`, `.generator(name, *scope) -> np.random.Generator` (PCG64), `.issued: dict[str, int]` |
| `topo_pilot.contracts.layout` (`:13`) | `SequenceLayout(n_obs=33, context=32, analysis_position=32)` |
| `topo_pilot.dataset.sampler` (`:33`) | `HMMSampler(T, E, pi, layout).sample(n: int, rng) -> (tokens uint8 [n, n_obs] (uint16 if V > 255), states int16 [n, n_obs])` |
| `topo_pilot.oracle` (`_filter.py:30`, `_futures.py:80`) | `BayesFilter(T, E, pi)` with `.run(tokens) -> FilterResult(b [R, P, N], q, log_evidence, ce)` and `.belief_at(tokens, p) -> float64 [R, N]`; `context_gain(q_C, q_last) -> float` |
| `oracle_profile` (`tools/x4_oracle_profile/oracle_profile.py`) | `PERIOD = 12`; `ProfileError`; `circle_features(coords)` (:40); `canonical_emission(E_named, symbol_perm)` (:58); `validate_process(T, E, pi, tol=1e-12) -> dict` (:69); `suffix_posterior(T, E, pi, tokens, K) -> float64 [n, S]` (:128); `posterior_means(T, E, pi, tokens, Ks, features) -> {K: [n, 2]}` (:155) |
| `k4b_scores` (`tools/k4b/k4b_scores.py`) | `wrap_phase(phi)` (:27); `vector_phase(m)` (:35); `m4_phase(m4)` (:41); `oracle_phase(m32)` (:45); `sha_phase(canon32)` (:49, uses `row[28:32]`); `phase_scores(phi, m32, mK)` (:54) |
| `scores` (`tools/x4_circle_history/scores.py`) | `unit_vectors(phi)` (:65); `scores(u, m32, m4)` (:84); `r4_norms(m32, m4)` (:90); `sha256_phase(last4_row)` (:95) |
| `error_bound` (`tools/x4_circle_history/error_bound.py`) | `reference_moments(T, E, pi, coords, canonical32, Ks=(4, 32), cache=None, cache_only=False) -> list[{K: (Decimal, Decimal)}]` (:236); `MOMENT_TOL_EXACT = Fraction(1, 10**10)` (:287) |
| `process_law` (`tools/x4_circle_history/process_law.py`) | `LAW` dict (:25; `sigma` Fraction(5, 4), `neighbour` Fraction(1, 5)); `process_law_bound(T, E, pi, coords) -> dict` (:222; catches only `Mismatch`) |
| `stage_records` (`tools/x4_circle_history/stage_records.py`) | `sha256(path) -> str` (:31); `write_new(path, obj)` (:35); `save_npz(path, **arrays)` (:40); `record_gate(out, gate, status, **details) -> str` (:64) |
| `c1_means` (`tools/c1prime/c1_means.py`) | `tree_mean(X)` (:15); `bootstrap_means(arrays, seed, draws=5000) -> dict` (:31); `rank_for(p, draws=5000) -> int` (:57); `quantile_with_rank(values, p) -> (value, rank)` (:71) |
| `k4b_meter_bind` (`tools/k4b/k4b_meter_bind.py`) | `bind(job_id, task_sha256, out, worker_session)` (:30; sets `winjob.MEMORY_CAP = 12 GiB`, hence the RC-9 override); `disk_reason(usage, minima)` (:46); `make_limiter(op_marker, disk, legacy, clock)` (:57); `rewrite_argv(argv)` (:77); `child_env(job, base=None)` (:95; reads module `TEMP_ROOT`); `classify_stop(reason, state)` (:104); `TEMP_ROOT` (:26) |
| `meter`, `winjob`, `controls`, `op_guard` | job-0014 meter (`meter.main`, `THREAD_VARS`, `LEDGER`, `CAP_S`, `OUTPUT_CAP`); `winjob.MEMORY_CAP` (default 8 GiB, `winjob.py:9`); `op_guard.MARKER`, `archive_stale` |

## 9. Streams and seeds (§6.6; CONTRACT `seeds`)

| Stream | Scope |
|---|---|
| Histories | `SeedTree(0).generator("data", "hws-v1", stage, key)`, stage ∈ {S0, S1, X1, S2, S3, DRY} |
| Null re-check | `SeedTree(0).generator("data", "hws-v1", "NULLCHK", origin_stage, key)` |
| P4 permutation | `SeedTree(0).generator("hws-v1", "prefix_perm", key)` (S3) |
| Bootstrap | PCG64 620101 (S0, w0) and 620103 (each S3 world) through `c1_means.bootstrap_means` |
| Alias labels | deterministic, no seed |
| W = 12 emission | `SeedTree(1729)` (symbol names only; canonicalised away) |

Synthetic (DRY), discovery (S1, X1, S2), confirmation (S3) and re-check (NULLCHK) streams are distinct; no stream is extended; one `HMMSampler.sample` call per world-look.

## 10. Gates (`GATES.jsonl`, via `record_gate`)

S0 job: `FREEZE`, `AUTH`, `G0`, `KC1` … `KC14` (KC13, KC14 recorded `PASS` with report-only values), `S0_RECORD`. Sweep job: `FREEZE`, `AUTH`, `S0_ACCEPT`, then per stage `STAGE_<S>` (PASS at stage completion), `NULL_<stage>_<key>` for every exceedance and its recheck, `PAUSE_<stage>` when a trigger fires, `OUTCOME`. A refused job (missing FREEZE, AUTH or S0 ACCEPT) records the refusal gate and samples nothing.

## 11. Ledger and pauses

`cpu_ledger.json` is the meter's (`k4b_meter_bind.bind` → `out/cpu_ledger.json`), never reset; the study ledger starts at S0; J1 (implementation, tests, dry run) uses the dry store's ledger and the J1 trigger 1,620 s. At every world boundary the driver computes `stage_cpu` = Σ `charged_cpu_s` of earlier ledger entries labelled for this stage + `time.process_time()` of the running process since the stage began, and `cum_cpu` = ledger `cumulative_cpu_s` + the running process's CPU (choice 26), then `pause_check`. A fired trigger: no new world starts; `PAUSE` event and gate; exit 4; continuation only with a `--continue` owner-decision file `{"continue": true, "stage", "decision_sha256"}`; the revised forecast never replaces the original.

## 12. Exactness and numerics (§8)

No numerical certificate in stage A (MD-3). E6 per look: every row array finite; `norm_err ≤ 1e-12`; the null rule; S3 spot checks (W = 12: `decimal_spot_check` rows 0..3, K ∈ {4, 32}; W ≠ 12: `bayes_cross_check` rows 0..255); Pinsker count reported (non-zero = review flag, not a stop).

## 13. Dry-run interface

`run_dry` implements DR1–DR13 (expected answers in `TEST_PLAN.md` §4). Planted decision fixtures (DR9, DR10) are dicts of the shape of §6.4 records, labelled `"fixture": true`, fed to `hws_select` and to the report and licence writers; they never enter `hist/`. DR3's forced unanchored world passes `force=True` to a DRY-only evaluation path; the sweep code has no force argument.

## 14. Choices (where the protocol leaves something open; simplest option; the protocol wins)

1. **No config module.** Paths, CONTRACT loading, sys.path and constants live in `hws_worlds` (the protocol lists exactly seven modules). `point_distances` is imported by its public name from `topo_pilot.process._geometry`; the 4-line softmax of `_overlap_core` is mirrored, not imported (§12.2 item 3).
2. **Levels** are `Fraction`s; configs get `float(level)`; `TransitionConfig(p_stay=float(p))`, `EmissionConfig(..., sigma=float(σ))`. LAW rebinding uses the Fractions.
3. **Key order** for every "by key" tie-break is Python `str` order of the key (so `W12…` < `W16…` < `W8…`).
4. **Grid order** W, q, σ, p ascending; X1 and S2 worklists follow their own stated orders.
5. **E1** = a `StageFailure` from the src builders or a `ProfileError` from `validate_process`; any other exception during a build is `FAIL_TECHNICAL/BUILD`.
6. **Exact filters** E2 and E4 compare `Fraction(float(value))` with the exact threshold; equality passes.
7. **E3** checks every s ∈ 1..W−1 and c ∈ 0..W−1 on state permutations, tol 1e-9; E3-ineligible worlds are recorded and never sampled.
8. **Known-zero worlds** U (V = 144) use n_axial = 12 for q^A (circular label = x); N uses 6. Their nulls and beyond-K quantities are judged by KC11 (|x| ≤ 1e-12), not by z_null, and are not counted in N_null.
9. **q_K = (b_K @ T) @ E′; KL rows** follow the `context_gain` zero-support convention; G_C is the mean of the G_1 rows; `context_gain(q_32, q_1)` is computed once per look as an E6 cross-check (|difference| ≤ 1e-12).
10. **Mean** by `c1_means.tree_mean`, SD with ddof = 1, SE = SD/√n; a null with SE = 0 has z = 0 if its mean is 0, else ∞.
11. **E5 bins**: bin = min(⌊phase·12/2π⌋, 11) on `oracle_phase(m32)` ∈ [0, 2π); "≥ n/64" as `64·count ≥ n`; "≥ 0.95" as `100·count ≥ 95·n`; |mean v32| is the norm of the mean unit vector (phase 0 at an exact zero).
12. **EXCLUDED/<criterion>** names the first failing criterion in C1..C4 order; the record lists all.
13. **"Eligible"** (X1 trigger, fallback set, HEADROOM) means not INELIGIBLE on the latest look (E1–E5 passed there).
14. **S2 "candidate status"** is CANDIDATE/* vs any other class; X1 levels that ran join the level lists for adjacency.
15. **S0 adds K = 3** to its K grid (KC9 needs MC means at K = 3); screening grids are unchanged.
16. **KC3's s** is the sample SD (ddof 1) of the per-row H(b_1) over the S0 w0 rows.
17. **KC4–KC6 references** are taken at full precision from JSON records: job-0014 `PROFILE_TABLE.json` (pooled (3072·cal + 1024·val)/4096) and K4b `stages/S8/RESULT.json` (`fresh_B4.point`, `controls.delta4_orc.all.point`); they agree with the rounded values in the protocol.
18. **KC7 n_r = 4096** is confirmed from the E2 `OracleOutputs` meta.json shapes (q, q_last [4096, 36]); no array opened.
19. **Rows for spot checks** are the lowest row indices: KC10 rows 0..15 (Decimal) and 0..1023 (BayesFilter); S3 rows 0..3 (W = 12) and 0..255 (W ≠ 12).
20. **NULLCHK** uses the same n and Ks as the exceeding look; its rows serve only the re-check and are stored under `hist/NULLCHK/<origin>/`.
21. **Bootstrap**: every S3 world uses a fresh PCG64(620103) (one stream per world, shared by its arrays): D_K, B_K, V_K for K ∈ {1, 2, 4, 6, 8, 12, 16, 24}, G_K for the same K, G0, G4A, IZ4, IX4, Hq[32]. S0 bootstraps w0's arrays with 620101 (report intervals). Other report intervals are normal (`normal95`).
22. **P4 permutation**: one `rng.permuted(tok[:, :28], axis=1)` call per S3 world (rows independent, uniform); P4 = mean(rows)/mean(rn4²), "undefined" if that mean is 0.
23. **Per-look aggregates** go to `stages/<S>/worlds/<key>.json`; `worlds/<key>.json` is the per-world summary written once at report time (both exclusive create).
24. **History files** hold one array `canon32` (uint8 [n, 32]), a key the K4b/C2 readers already recognise.
25. **STAGES.jsonl** is written by HWS's own appender (same line format as `stage_records`; its private `_append` is not imported); `stage_records.begin/complete` (x4 stage order) are not used.
26. **CPU for the pauses** = the meter ledger's charged CPU of earlier runs plus `time.process_time()` of the running driver; "exceeds" is strict.
27. **Reviewed law enclosure** (RC-3) is not part of J1's specified code: `law_bound_report` takes an optional `enclosure`; with none, DR13's last clause is `NOT_APPLICABLE` (CONTRACT `open`).
28. **`process_law_bound`** receives the canonical (centre-order) E′; LAW is restored in `finally`.
29. **Authority files**: `--auth` JSON `{"job_id", "stages": [...], "owner_auth_sha256"}` written by the coordinator; a stage not listed → refusal (exit 2, gate `AUTH` = `INCONCLUSIVE/RESOURCE_OR_AUTHORITY`), nothing sampled. S0 ACCEPT and pause continuation are separate JSON files (§6.2, §11).
30. **Meter CLI** takes `--job`, `--task-sha256`, `--session`, `--out` (no release file; the protocol names none).
31. **Implementation hash** = sha256 of `canonical_json({relpath: sha256})` over `tools/hws/*.py` and `tests/hws/*` at h_exec; API/CONTRACT/TEST_PLAN/PROTOCOL have their own fields. The dry-run report is copied by the J1 worker to `agent-handoff/jobs/<job>/DRY_RUN_REPORT.json` and bound by sha256.
32. **SELECTION.json** exists only for HWS_SELECTED; other outcomes are in REPORT.json.
33. **G0 search** scope and classification as §6.2; the public research-summary paths are excluded from the search and never opened; any hit outside the declaration paths fails closed for coordinator review.
34. **"3× absence shown"** iff every evaluated, not-INELIGIBLE world has Uw failing at least one of C1–C4 on its latest look.
35. **Outcome fallthrough** (no §7.1 branch applies) is `FAIL_TECHNICAL/OUTCOME`.
36. **Rectangular centres** take `n_axial` so the DR1 tiny world (one axial row) uses the same code.
37. **Fallback-only set** uses the latest screening look (Uw on D4 ≥ 0.02 and C2–C4).
38. **Unanchored map** is defined only when (W/2) mod q = 0 (DR3 uses W = 12, q = 2: period 3).
39. **S0 store hash** = `tree_sha` over `stages/S0`, `hist/S0`, `hist/NULLCHK/S0` before the S0 record is written.
40. **Resume** archives unlisted partial files of the interrupted stage under `superseded/` and regenerates the interrupted world from its original stream (bit-identical rows expected).
41. **X1 trigger "largest D̂4"** ranges over S1 worlds not INELIGIBLE (EXCLUDED worlds included); ties by ascending key.
42. **E5 at screening** uses the screening rows' point values; for finalists, S3 rows decide.
43. **Exception map**: `HwsStop` keeps its status; `ProfileError`, `errors.Invalid`, `c1_records.C1GateFailure`, non-finite rows → `FAIL_TECHNICAL/NUMERICAL`; `StageFailure` outside a build → `FAIL_TECHNICAL/BUILD`; anything else → `FAIL_TECHNICAL/UNEXPECTED`.

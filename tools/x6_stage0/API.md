# tools/x6_stage0: written contract (job 0058; derived from X6-FROZEN-v1)

**Authority:** `tools/x6_stage0/PROTOCOL_X6_v1.md`, a byte-for-byte copy of `agent-handoff/planning/responses/X6-FROZEN-v1.md` (sha256 61DDA37BF5B23648894440B4016F80191C56B6626F04CD2D5A4178D46EF2B572). Section numbers (§n), gate ids (PF, S0, G0–G7, D), theorem names and test numbers refer to the protocol.

**Precedence:** the protocol is authoritative. This contract names the functions, inputs, outputs, report keys, seeds, files and records of the module, so that the independent tests (§10.4) can be written before the module exists. It changes no scientific choice: no parameter, value, tolerance, gate, stop rule, outcome rule or reading rule. Where this contract and the protocol differ, the protocol wins. Details the protocol leaves open are fixed under "Implementation choices" (end of file), always with the simplest option.

## 1. Files (§10.1)

| File | Contents | Planned size |
|---|---|---|
| `x6_model.py` | constants, seeds, S₃ helpers, index helpers, neighbour table, seam letters, labels and gauge arrays, `build_world`, punctured complex, `lift`, `emission`, `model`, face holonomies, flux, cover and its certificate, path statistics, closed-form oracle (Theorem 1), k-gram laws; `gate_G0`, `gate_G1` | ≈ 360 lines |
| `x6_dp.py` (**the optional fourth file: it exists**) | `segment_dp`, the ladder aggregation, anchor-avoidance counts, the total-mass identity, image-level ambiguity, the K-blk DP, Decimal conversion, KL/entropy in Decimal, the memo of §5.6 item 6, enclosures and the certification logic, `decimal_model`, the natural quantities, `gate_G4` | ≈ 370 lines |
| `x6_exact.py` | Fraction forward filter; G2 enumeration; witness templates and families; matched statistics; R_S keys; β table; challenge quantities; the 4×8 comparator; `gate_G2`, `gate_G3`; O1 and O2 | ≈ 340 lines |
| `x6_run.py` | Monte Carlo and per-row statistics (G6); numerical and Decimal cross-checks (G5); controls (G7); PoE; labels and `decide` (D); S0 (allowlist, dispatch record, store lineage); the rerun and lineage machinery of §10.8; `write_preflight`; `run`; report and NPZ writing; CLI | ≈ 395 lines |

Every module file is ≤ 400 lines (S6). If any file would exceed 400 lines, or a fifth module file would be needed, the module author stops and escalates (S6). No `src/` change; no import from `tools/d1_seam` or `tools/x2a_stage0`; no registered world.

**Import convention (D-1 / X2a pattern).** Each module computes `REPO = Path(__file__).resolve().parents[2]` and prepends `tools/x6_stage0`, `tools/x4_oracle_profile` and `tests/oracle_profile` (under `REPO`) to `sys.path` if absent. Tests import by bare name: `import x6_model as xm`, `import x6_dp as xd`, `import x6_exact as xe`, `import x6_run as xr`. Import order of dependencies: `x6_model` ← `x6_dp` ← `x6_exact` ← `x6_run`. Importing a module performs no I/O and no computation beyond module constants (the tables of §2 below). `run`, `gate_G2`, `gate_G3`, `gate_G4`, `natural`, `kblk` and the G5–G7 gates are expensive (minutes); `build_world`, `model`, `closed_form`, `fraction_filter`, `kgram_law` (k ≤ 5), `segment_dp` with small `n_max` and `gate_G0` are cheap.

## 2. Conventions (§0)

- **Vertices** `i ∈ 0..15`, `i = 4x + y`, `divmod(i, 4) = (x, y)`. **Lifted states** `s = state(i, x) = 3i + x ∈ 0..47`. The 16-vertex and 48-state indexings are never mixed: every 48-indexed array is indexed through `state`.
- **Tokens:** vertex tokens `tok(i) ∈ 0..14`; cue `15 + x`; `V = 18`. Under `E_nc` the alphabet is `0..15` (token `i` for vertex `i`, anchor included).
- **Histories** are sequences of ints `w_1..w_t` (tuple, list or a 1-D integer array); Python index 0 is `w_1`. `t` = number of observed symbols.
- **Permutations** are tuples of three ints `g = (g[0], g[1], g[2])`; `compose(g, h)[x] = g[h[x]]`. Holonomy of a path: start from `e`, then `g ← compose(label(v_{k−1} → v_k), g)` for k = 1..n (the latest edge applied last).
- **Exact numbers:** `fractions.Fraction`; exact matrices are lists of lists of `Fraction` (row-major), exact vectors lists of `Fraction`. Counts are Python `int` (never numpy fixed-width). Float arrays are numpy `float64`, each entry `float(Fraction)` (§2.5).
- **Event order:** emit, then transition; row vectors; start π = 1/48 (stationary). `q_t` = law of `w_{t+1}` given `w_{1:t}`; as in `BayesFilter`, `q_0 = πE` and `q_t = b_t T E`.
- **Names.** Arms: `"NA"`, `"AB"`, `"ZC"`, `"TRIV"`, `"ETA1"`, `"GAUGE-NA"`, `"GAUGE-TRIV"`, `"GAUGE-COV"`. NOCUE and TOKPERM are controls built as `model("NA", "E_nc")`, `model("TRIV", "E_nc")` and `model("NA", "E_sigma")`. Emission kinds: `"E"`, `"E_cov"`, `"E_nc"`, `"E_sigma"`. Ladder statistics `LADDER = ("empty", "parity", "counts", "H1", "Parikh")` ("empty" is ∅). Seam letters `"x+"`, `"x-"`, `"y+"`, `"y-"`. Permutation names `"e"`, `"a"`, `"b"`, `"c"`, `"c2"`, `"t"`.
- **Statuses:** gates `"PASS"`, `"FAIL"`, `"INVALID"`, `"NOT_RUN"`, and `"RESOURCE_LIMIT"` (G4 only, S8). Certified comparisons `"PASS"`, `"FAIL"`, `"UNCERTIFIED"`. Lineage checks `"PASS"` or `"INVALID/LINEAGE"`.
- Information in nats; natural logarithms.

## 3. x6_model.py

### 3.1 Constants

`L_SIDE = 4`, `N_V = 16`, `N_FIB = 3`, `N_S = 48`, `V = 18`, `V_NC = 16`, `ANCHOR = 10`, `ANCHOR_NB = frozenset({6, 9, 11, 14})`, `F_STAR_VERTICES = (0, 3, 12, 15)`, `F_STAR_ROW = (15, 12, 3, 0)`, `P_MOVE = Fraction(1, 5)`, `ETA = Fraction(1, 50)`, `T_STAR = 32`, `N_OBS = 33`, `WINDOWS = (1, 2, 4, 8)`, `BLOCKS = ((1, 8), (9, 16), (17, 24), (25, 32))` (inclusive positions; a transition belongs to the block of its destination position).

`ARMS = ("NA", "AB", "ZC", "TRIV", "ETA1", "GAUGE-NA", "GAUGE-TRIV", "GAUGE-COV")`, `ARMS_SEAM = ("NA", "AB", "ZC", "TRIV")` (the η = 1/50 seam-supported arms; ETA1 is seam-supported with NA's labels and is handled where stated), `LADDER` as above, `EMISSIONS = ("E", "E_cov", "E_nc", "E_sigma")`.

Seeds (§8.6): `MASTER_SEED = 420700`, `MC_STREAM = "x6s0_mc"`, `MC_ARMS = ("NA", "AB", "ZC", "TRIV", "ETA1", "NOCUE")`, `MC_ROWS = {"NA": 2**18, "AB": 2**16, "ZC": 2**16, "TRIV": 2**16, "ETA1": 2**16, "NOCUE": 2**14}`, `N_CHECK = 2**14` (G5, TOKPERM, NOCUE and PoE use the first `N_CHECK` rows), `BATCH = 2048`.

Thresholds and tolerances (§8.6, §8.7): `TV_MIN = Fraction(3, 10)`, `G_MIN = Fraction(1, 1000)`, `M_MIN = Fraction(1, 32)`, `THETA_ROW = Fraction(1, 100)`, `BETA_MAX = Fraction(1, 4)`, `TOL_STRUCT = 1e-15`, `TOL_NUM = 1e-12`, `TOL_LOGEV = 1e-10`, `TOL_G1_REL = 1e-12`, `TOL_DEC = Decimal("1e-45")`, `TOL_LOG = Decimal("1e-40")`, `MC_K = 4`, `MC_FLOOR = 2e-12`, `RATIO_5GRAM = 2`.

Bindings (§10.5, §8.1): `FAMILY = "_x6_torus_local"`, `PROTOCOL_ID = "X6-FROZEN-v1"`, `PROTOCOL_SHA256 = "61DDA37BF5B23648894440B4016F80191C56B6626F04CD2D5A4178D46EF2B572"`, `REQUEST_SHA256 = "18E77F7E5BAE48AACC08C8A48560DEEDC0A543531C11B2E09D8684B36C9EFBE1"`, `R_COMMIT = "f8e5f12b2f83ecf8b6a32189705a03ff98afa28d"`, `KERNEL_BASE = "c364f95e5573940cdc24b569b0fb7c6a16c97ab8"`, `STORE = "X:/Downloads/projects/topo-pilot/x6-stage0-oracle-store"`, `WORKTREE = "X:/Downloads/projects/topo-pilot/topo-pilot-x6"`, `SCRATCH_ROOT = "X:/Downloads/topo-scratch"`.

### 3.2 S₃ and index helpers (§0, §2.3)

- `S3_E = (0, 1, 2)`, `S3_A = (1, 0, 2)`, `S3_B = (0, 2, 1)`, `S3_C = (1, 2, 0)`, `S3_C2 = (2, 0, 1)`, `S3_T = (2, 1, 0)`; `S3_LIST = (S3_E, S3_A, S3_B, S3_C, S3_C2, S3_T)`.
- `compose(g, h) -> tuple`: `(g[h[0]], g[h[1]], g[h[2]])`. `inverse(g) -> tuple`: `inverse(g)[g[x]] = x`.
- `perm_name(g) -> str`: the name of g in `S3_LIST` order (`"e"`, `"a"`, `"b"`, `"c"`, `"c2"`, `"t"`).
- `state(i, x) -> int`: `3*i + x`. `split_state(s) -> (i, x)`: `divmod(s, 3)`.
- `tok(i) -> int`: `i` for `i < 10`, `i − 1` for `11 ≤ i ≤ 15`; `ValueError` for `i = 10` or outside `0..15`.
- `vertex(w) -> int`: the vertex of token `w` under E: inverse of `tok` for `w ≤ 14`, `ANCHOR` for `w ∈ {15, 16, 17}`; `ValueError` otherwise.
- `cue(x) -> int`: `15 + x`.
- `NEIGHBOURS`: tuple of 16 tuples `(+x, −x, +y, −y, stay)`, exactly the §2.5 table (`NEIGHBOURS[0] = (4, 12, 1, 3, 0)`). This successor order fixes every DFS and DP iteration order.
- `seam_letter(i, j) -> str | None`: exactly §2.4 (directed base edge `i → j`; `None` for interior edges and self-loops).

### 3.3 Labels and gauge arrays (§2.4)

- `H_COV`: tuple of 16 permutations, `S3_LIST[i % 6]` for i = 0..15 (`H_COV[10] = S3_C2`). `H_FIX`: `H_COV` with index 10 replaced by `S3_E`.
- `seam_labels(arm) -> dict`: `{"x+": g_x, "x-": inverse(g_x), "y+": g_y, "y-": inverse(g_y)}` for `"NA"` (a, b), `"AB"` (a, a), `"ZC"` (c, c), `"TRIV"` (e, e) and `"ETA1"` (NA's). `ValueError` for gauge arms.
- `edge_labels(arm) -> dict[(int, int), tuple]`: one entry for every `i` and every `j` in `NEIGHBOURS[i]` (80 keys, self-loops `(i, i)` included). Seam-supported arms: the `seam_labels` entry of `seam_letter(i, j)`, `S3_E` when it is `None`. `"GAUGE-NA"`: `H_FIX[j] ∘ g^NA_{i→j} ∘ H_FIX[i]⁻¹`; `"GAUGE-TRIV"`: `H_FIX[j] ∘ H_FIX[i]⁻¹`; `"GAUGE-COV"`: `H_COV[j] ∘ g^NA_{i→j} ∘ H_COV[i]⁻¹`. Self-loops are `S3_E` in every arm.
- `eta(arm) -> Fraction`: `Fraction(1)` for `"ETA1"`, else `ETA`.

### 3.4 World, complexes, kernel and emissions (§2.1, §2.2, §2.5, §2.6)

- `class _X6TorusBuilder(QuotientLatticeBuilder)`: exactly the §2.1 ClassVars. Never registered.
- `build_world() -> WorldSpec`: §2.1 steps 1–4 in order. Exceptions propagate (the runner maps them to INVALID, S2). Never mutates `WORLD_REGISTRY`; never calls `process._geometry.point_distances` or `is_x_periodic`.
- `kernel(spec) -> ndarray [16, 16]`: `TransitionBuilder().build(spec, TransitionConfig(p_stay=0.2)).T`.
- `f_star_index(spec) -> int`: the unique row r of `spec.cells[2]` with `sorted(row) == [0, 3, 12, 15]`.
- `punctured_complex(spec) -> CubicalComplex`: `CubicalComplex(16, {0: cells[0], 1: cells[1], 2: np.delete(cells[2], f_star, axis=0)})` (§2.2).
- `t_base_exact() -> list[list[Fraction]]` [16, 16]: `P_MOVE` at every `NEIGHBOURS` entry, 0 elsewhere.
- `lift(T_base, labels, eta) -> list[list[Fraction]]` [48, 48]: `T[state(i,x)][state(j,x′)] = T_base[i][j]·((1 − eta)·[x′ = labels[(i, j)][x]] + eta/3)` for `T_base[i][j] ≠ 0`, else 0. `T_base` is the exact 16×16 matrix; `labels` an `edge_labels` dict.
- `emission(kind) -> list[list[Fraction]]`: §2.6 exactly, entries `Fraction(0)` or `Fraction(1)`. `"E"`, `"E_cov"`, `"E_sigma"`: [48, 18]; `"E_nc"`: [48, 16]. E_cov: row `state(i, x′)` equals E's row `state(i, inverse(H_COV[i])[x′])`. E_sigma: `E_sigma[s][sigma_tok(w)] = E[s][w]`.
- `sigma_tok(w) -> int`: `(w + 7) % 15` for `w ≤ 14`, `w` for `w ∈ {15, 16, 17}`.
- `to_float(M) -> ndarray`: `float64` array of `float(entry)` (vector or matrix).
- `model(arm, kind=None) -> dict`: keys `"arm"`, `"kind"`, `"eta"`, `"labels"` (`edge_labels(arm)`), `"T"` (`lift(t_base_exact(), labels, eta(arm))`), `"E"` (`emission(kind)`), `"pi"` (48 × `Fraction(1, 48)`), `"Tf"`, `"Ef"`, `"pif"` (`to_float` of the three). `kind=None` means `"E_cov"` for `"GAUGE-COV"` and `"E"` otherwise. Builds no world.

### 3.5 Faces, flux and cover (Lemma 0, Lemma 0′)

- `face_cycle(row) -> tuple`: for a local-lexicographic square row `(r0, r1, r2, r3)` of `spec.cells[2]`, the closed vertex path `(r0, r2, r3, r1, r0)` (for f★, `(15, 3, 0, 12, 15)`: letters x⁺, y⁺, x⁻, y⁻).
- `holonomy(path, labels) -> tuple`: holonomy of a vertex path `(v_0, …, v_n)` (§2 convention); `holonomy((v,), labels) = S3_E`.
- `face_holonomies(spec, labels) -> list[tuple]`: `holonomy(face_cycle(row), labels)` for every row of `spec.cells[2]`, in row order (16 entries).
- `flux(spec, labels) -> tuple`: the entry at `f_star_index(spec)` (NA: `S3_C`; AB, ZC, TRIV: `S3_E`; ETA1 and GAUGE-NA: a 3-cycle).
- `cover_complex(spec, labels) -> CubicalComplex`: 48 vertices; 1-cells: for each row `(i, j)` of `spec.cells[1]` and each x (row-major, then x), `(state(i, x), state(j, labels[(i, j)][x]))`; 2-cells: for each row `(r0, r1, r2, r3)` of `spec.cells[2]` except f★ and each x, `(state(r0, x), state(r1, g01[x]), state(r2, g02[x]), state(r3, g23[g02[x]]))` with `g01 = labels[(r0, r1)]`, `g02 = labels[(r0, r2)]`, `g23 = labels[(r2, r3)]`. Counts (48, 96, 45) in seam-supported arms.
- `boundary_circles(cx) -> int`: the number of connected components of the graph formed by the 1-cells that lie in exactly one 2-cell.
- `cover_betti(cx) -> dict`: `{2: cx.betti(2), 3: cx.betti(3)}`.

### 3.6 Path statistics (§0, §5.1)

- `path_letters(path) -> list[str]`: seam letters of consecutive vertex pairs, in order, `None` omitted.
- `parikh(path) -> tuple`: `(k_x+, k_x-, k_y+, k_y-)`.
- `statistic(S, kappa)`: `"empty"` → `()`; `"parity"` → `sum(kappa) % 2`; `"counts"` → `(k_x+ + k_x-, k_y+ + k_y-)`; `"H1"` → `(k_x+ − k_x-, k_y+ − k_y-)`; `"Parikh"` → `kappa`.
- `ZC_WITNESS = ((10, 14, 2, 6, 6, 6, 6, 6), (10, 9, 5, 1, 13, 9, 5, 6))`: the two n = 7 segments of the §3 ZC corollary (anchor first).

### 3.7 Closed-form oracle (Theorem 1)

- `lam(m, eta=ETA) -> Fraction`: `(1 − eta)**m` (`lam(0) = 1`).
- `point_law(m, z, eta=ETA) -> tuple`: μ_m(z), three Fractions.
- `parse(tokens) -> dict`: keys `"t"`, `"path"` (v_1..v_t), `"s"` (1-based time of the last cue, or `None`), `"y"`, `"n"` (`t − s`), `"segment"` (`(v_s, …, v_t)`, starting at `ANCHOR`), `"prefix"` (`tuple(w_1..w_{s−1})`), `"v"` (v_t). With no cue, `"s"`, `"y"`, `"n"` and `"segment"` are `None` and `"prefix"` is the whole history. `ValueError` for a token outside 0..17 or a non-adjacent consecutive vertex pair.
- `closed_form(arm, tokens) -> dict` for `arm` in `ARMS_SEAM + ("ETA1",)` under E (else `ValueError`): `"fibre"` (P(x_t = · | w_{1:t}), 3 Fractions), `"b"` (48 Fractions: the fibre law at `state(v_t, x)`, 0 elsewhere), `"q"` (18 Fractions, law of w_{t+1}), `"P"` (P(w_{1:t}) by the Theorem 1 product), `"rho"` (segment holonomy or `None`), `"n"`, `"y"`. It uses ρ and λ only; it never runs a forward filter.
- `cue_normalised(q) -> tuple`: `q[15:18]` divided by its sum (exact).

### 3.8 k-gram laws (Corollary 4′, G1)

- `kgram_law(m, k) -> dict[tuple, Fraction]`: the stationary law of `(w_1..w_k)` under the model dict `m` (start `m["pi"]`), over reachable strings only (positive probability), exact, prefix-shared DFS.
- `five_gram(y, y2) -> tuple`: `(15 + y, 10, 8, 9, 15 + y2)`.

### 3.9 Gates

- `gate_G0(spec=None) -> dict`: builds the world if `spec` is None. Keys: `"status"`; `"counts"` (16, 32, 16); `"betti"` `{2: (1,2,1), 3: (1,2,1)}`; `"punctured"` `{"counts": (16, 32, 15), "chi": -1, "betti": {2: …, 3: …}, "closed": bool, "boundary_cycles": 1}`; `"t_base_max_err"` (float vs `t_base_exact`), `"t_base_support_ok"`; per arm in `ARMS`: `"lift_ok"[arm]` (exact formula, exact row and column sums), `"lift_max_err"[arm]` (float vs Fraction), `"validate_process"[arm]` (bool), `"faces"[arm]` (16 permutation names), `"flux"[arm]` (name); per seam-supported arm (`ARMS_SEAM`): `"cover"[arm] = {"counts", "betti", "circles", "closed"}`.
- `gate_G1() -> dict`: `"status"`, `"one_hot"` (per emission kind), `"tok_bijection"`, `"kgram_equal"` `{k: bool}` for k = 1..4 (NA, AB, ZC, TRIV), `"five_gram_ratio"` `{"A|B": Fraction}` for each pair of `ARMS_SEAM` (the maximum over (y, y′) of the larger/smaller probability of `five_gram(y, y′)`).

## 4. x6_dp.py

### 4.1 Integer DP and aggregation (§5.2, Theorem 7)

- `segment_dp(arm, n_max=31)`: generator yielding `(n, layer)` for n = 0..n_max. `layer` is a dict `{(v, kappa, g): int}`: the number of n-step paths from `ANCHOR` avoiding `ANCHOR` at steps 1..n, ending at v, with Parikh vector `kappa` and holonomy `g` under `edge_labels(arm)` (`arm` in `ARMS_SEAM` or `"ETA1"`). `layer_0 = {(10, (0, 0, 0, 0), S3_E): 1}`. Step: successors in `NEIGHBOURS` order, `j = ANCHOR` rejected, `kappa` incremented at the index of `seam_letter(v, j)` (order `x+, x-, y+, y-`), `g ← compose(labels[(v, j)], g)`. Only the current layer is kept by the generator.
- `classes(layer, S) -> dict`: `{(v, sigma): {g: int}}` with `sigma = statistic(S, kappa)` (aggregation of the one Parikh DP).
- `weights(cls, y) -> tuple`: w(z) = Σ_{g: g[y] = z} C(g) / Σ_g C(g), three Fractions (`cls` is one `{g: int}` value).
- `ambiguous(cls, y) -> bool`: at least two distinct images `g[y]` with positive count (Lemma I, image level).
- `avoid_counts(n_max=31) -> dict`: an anchor-avoidance recursion that uses no labels. `"A"`: `[A_0, …, A_{n_max}]` (A_0 = 1); `"B"`: `[B_0, …]` (paths ending in `ANCHOR_NB`; B_0 = 0); `"D"`: `[D_0, …, D_{n_max}]`, each `{v: int}` for v ≠ 10 (m-step paths from v avoiding `ANCHOR` entirely; D_0(v) = 1). All Python ints.
- `total_mass(t, counts) -> Fraction`: `1/16 + Σ_{n=1}^{t−1} A_n/(16·5^n) + Σ_{v≠10} D_{t−1}(v)/(16·5^{t−1})` (equals 1 by Theorem 7).

### 4.2 Decimal arithmetic and the memo (§5.6, §9.5)

- `DIV_PREC = {80: 90, 120: 130}`; `PRECS = (80, 120)`.
- `to_decimal(fr, prec) -> Decimal`: `Decimal(fr.numerator) / Decimal(fr.denominator)` in a local context of precision `prec` (high-precision rational division; `prec` is the division precision, 90 or 130).
- `kl_decimal(p, q, prec) -> Decimal`: Σ_{p_i > 0} `to_decimal(p_i, DIV_PREC[prec]) · ln(to_decimal(p_i / q_i, DIV_PREC[prec]))`, the ratio formed exactly as a Fraction; `ln` and the sum in a local context of `prec` digits. `p`, `q` are sequences of Fractions; `ValueError` if some `p_i > 0` has `q_i = 0`.
- `entropy_decimal(p, prec) -> Decimal`: −Σ_{p_i > 0} `to_decimal(p_i) · ln(to_decimal(p_i))`, same contexts.
- `memo_key(prec, kind, n, w, z) -> tuple`: `(prec, kind, n, tuple(Fraction(x) for x in w), z)` (Fractions are reduced).
- `kl_term_uncached(prec, kind, n, w, z) -> Decimal`: `kind = "next"`: `kl_decimal(point_law(n + 1, z), λ_{n+1}·w + (1 − λ_{n+1})·u, prec)`; `kind = "fibre"`: the same with λ_n and `point_law(n, z)`. η = 1/50 only. Cue-normalised (no factor 1/5).
- `kl_term(prec, kind, n, w, z) -> Decimal`: memoised `kl_term_uncached` under `memo_key`; a cached value is the identical Decimal. `MEMO` is the module-level dict; `memo_clear()` empties it. Keys carry `prec`, so 80- and 120-digit values never share entries.
- `decimal_model(arm, prec) -> (T, E, pi)`: nested lists of `Decimal`, each entry `to_decimal(Fraction, DIV_PREC[prec])` of `model(arm)`'s `"T"`, `"E"`, `"pi"` (§9.5 input rule). Never `Decimal(float)`.

### 4.3 Enclosures and certification (§5.6, §8.7 T12–T15)

- `enclosure(v80, v120, abs_sum, n_terms) -> dict`: `{"type": "enclosure", "v80", "v120", "abs_sum", "N": n_terms, "eps", "lo", "hi", "consistent", "n_ok"}` with `eps = 10**−60 · max(1, abs_sum)`, `lo = v80 − eps`, `hi = v80 + eps` (computed in a 200-digit context, so exactly), `consistent = |v80 − v120| ≤ eps`, `n_ok = (n_terms + 10)·10**−78 ≤ 10**−61` (evaluated exactly, i.e. `n_terms + 10 ≤ 10**17`).
- `enclose_sum(pairs) -> dict`: `pairs` iterates `(term80, term120)`; `v80` = Σ term80 in an 80-digit context, `v120` = Σ term120 in a 120-digit context, `abs_sum` = Σ |term80|, `N` = number of pairs; returns `enclosure(…)`.
- `certify(enc, theta) -> str`: `"PASS"` iff `lo ≥ theta`; `"FAIL"` iff `hi < theta`; else `"UNCERTIFIED"`. Comparisons are exact (`Fraction(Decimal)` against `Fraction(theta)`); `theta` may be a Fraction, int or Decimal.
- `mass_bounds(rows, theta) -> (Fraction, Fraction)`: `rows` iterates `(mass, enc)`; `M_lower` = Σ mass with `certify(enc, theta) == "PASS"`; `M_upper` = Σ mass with `certify(enc, theta) != "FAIL"`.
- `certify_mass(m_lower, m_upper, threshold) -> str`: `"PASS"` iff `m_lower ≥ threshold`; `"FAIL"` iff `m_upper < threshold`; else `"UNCERTIFIED"` (exact).

### 4.4 Natural quantities, K-blk and G4 (§5.3–§5.4, §6.2)

- `natural(arm, t_max=32) -> dict` for `arm` in `ARMS_SEAM` (one pass of `segment_dp`, enclosures at 80 and 120 digits): `"G"` `{S: {t: enc}}` for S in `LADDER`; `"pyth"` (the two Pythagorean identities per t, as enclosures of the residuals); `"J"` `{k: {t: enc}}`, `"J_fib"` `{k: {t: enc}}`, `"J_fib_full"` `{t: enc}`, `"I_fib"` `{k: {t: enc}}`, `"G_k"` `{k: {t: enc}}` for k in `WINDOWS`; `"masses"` (§5.4, exact Fractions per t: `"E_cue"`, `"age"`, `"E_nb"`, `"amb"` `{S: …}`, `"amb_nb"` `{S: …}`); `"M32"` `{"lower", "upper", "cert"}`; `"n_min"` `{"any", "nb"}`; `"null"` (the abelian integer statements: no class ambiguous under parity in AB, under H1 in ZC, under ∅ in TRIV); `"theorem4"` (bool: no Parikh class ambiguous at `ANCHOR_NB` with n ≤ 6, or at any v with n ≤ 3); `"tables"` `{S: {(n, v, sigma): {g: int}}}` for 1 ≤ n ≤ 31, v ≠ 10 (the retained class summaries used by G6); `"mean_G_parikh"` (enclosure of the mean over t = 1..32). ETA1 is not passed here: its G7 zeros are exact Fraction statements (every class's μ* equals μ_S because λ_m = 0 for m ≥ 1).
- `kblk(arm) -> dict` for `arm` in `ARMS_SEAM`: `"D_blk"` (enclosure of D_blk(32)), `"ambiguous_any"` (bool: some K-blk class ambiguous at some y), `"witness_ambiguous"` (bool: the Theorem 8 class is present and ambiguous), `"states_max"` (int).
- `gate_G4(arms=ARMS_SEAM) -> dict`: `"status"` (`"PASS"`, `"FAIL"` or `"RESOURCE_LIMIT"`), `"natural"` `{arm: natural(arm)}` without `"tables"`, `"kblk"` `{arm: kblk(arm)}`, `"checks"` `{name: "PASS" | "FAIL" | "NOT_RUN"}` (every §8.2 G4 check by name), and under S8 `"resource_limit"` `{"step": str, "completed": [names]}`.

## 5. x6_exact.py

### 5.1 Fraction forward filter and G2 (§9.2)

- `fraction_filter(T, E, pi, tokens) -> dict`: a generic exact forward filter (any sizes; sparse over the support; never uses labels or ρ). `"b"`: `[b_1, …, b_t]` (lists of Fractions); `"q"`: `[q_0, …, q_t]` (`q_0 = πE`, `q_t = b_t T E`); `"P"`: P(w_{1:t}). `ValueError` on a zero-probability history.
- `gate_G2(arms=ARMS_SEAM, t_max=6) -> dict`: `"status"`, `"nodes"` `{arm: int}`, `"mass"` `{arm: {t: Fraction}}` (Σ_h P(h), must be 1), `"mismatch"` `{arm: int}` (nodes where the belief, q or P differs from `closed_form`), `"A"` (A_1..A_5), `"tables_equal"` `{arm: bool}` (class tables for n ≤ 5 equal to `segment_dp`'s).

### 5.2 Witnesses (§4)

- `LOOPS = {"A+": (9, 13, 1, 5), "A-": (1, 13, 9, 5), "B+": (6, 7, 4, 5), "B-": (4, 7, 6, 5)}`; `P_LOOP = 5`.
- `ORDERINGS`: the 24 tuples `itertools.permutations(("A+", "A-", "B+", "B-"))`, in that order.
- `FAMILIES = ("W1", "W2", "W3", "W3p")` (W3p is W3′, t = 26).
- `members(family) -> tuple`: `("U", "D")`, `("AB", "BA")`, or `ORDERINGS` (W3, W3p).
- `witness_path(family, member) -> tuple`: the vertices v_2..v_t after the cue at `ANCHOR` (§4.1–§4.4): W1-U `(14, 15, 3, 0, 4, 5, 6)`; W2-AB `(9, 5) + A⁺ + B⁺ + (1, 2, 3, 7, 11, 15, 14)`; W3 `(6, 5) + (5,)*5 + loops + (5,)*7 + (6,)`; W3p `(9, 5) + loops + (1, 2, 3, 7, 11, 15, 14)`.
- `prefix_tokens(name, y0=0) -> tuple`: `"P0"` `()`, `"P1"` `(10,)`, `"P3"` `(6, 5, 9)`, `"P6"` `(15 + y0, 13, 12, 9, 5, 9)`.
- `witness_tokens(family, member, y, prefix="P0", y0=0) -> tuple`: `prefix_tokens(prefix, y0) + (15 + y,) + tuple(tok(v) for v in witness_path(family, member))`.
- `family_values(arm, family, prefix="P0", y0=0) -> dict` (exact, by `fraction_filter` on `model(arm)`; any arm in `ARMS`): `"t"`, `"n"`, `"members"` `{member: {"holonomy": name (segment holonomy under the arm's labels), "P": {y: Fraction}, "q": {y: 18 Fractions}}}`, `"equal_P"` (bool: within each y all members have equal P), `"tv_min"` (minimum over y and over member pairs of different holonomy of the cue-normalised TV; `None` if no such pair), `"spread"` (maximum over y and all member pairs of the full-vocabulary TV; 0 iff all q equal), `"multiplicity"` `{"e", "c", "c2"}` (member counts by holonomy name; W3 and W3p only).

### 5.3 Matched statistics and constancy (§4.7, OS 2)

- `matched(family, y=0) -> dict`: `{name: "equal" | "differs"}` for `"length"`, `"n"`, `"end"`, `"prefix"`, `"cue"`, `"parikh"`, `"h1"`, `"counts"`, `"parity"`, `"bag"`, `"bigram"`, `"trigram"`; plus `"tail"` (int: the length of the longest common token suffix) and `"trigram_diff"` (sorted list of trigrams whose multiplicities differ).
- `rs_key(S, tokens) -> tuple`: with a cue, `(False, prefix, n, y, v_t, statistic(S, parikh(segment)))`; with no cue, `(True, tuple(tokens), None, None, v_t, None)`.
- `constant_by_keys(keys) -> bool`: true iff `keys` is non-empty and all keys are equal.

### 5.4 β table (§4.9)

- `competitor_holonomy(kind, letters) -> tuple`: `letters` is the list of seam-edge labels in path order. `"rev"`: composition in reversed order (the first letter applied last); `"last"`: the last label; `"first"`: the first label; `S3_E` for an empty list.
- `beta(rows) -> Fraction | None`: `rows` iterates `(set_id, weight, q_star, q_alt)` with 3-Fraction cue laws. Within each `set_id`, `q_star` and `q_alt` are each centred by their own weighted mean. Returns Σ w⟨q̃_alt, q̃*⟩ / Σ w‖q̃*‖² over all rows; `None` if the denominator is 0.
- `beta_table() -> dict` (NA, Π0): `{family: {kind: {"pooled": Fraction, "per_y": [3 Fractions]}}}` for families W1, W2, W3 and kinds `"rev"`, `"last"`, `"first"`, `"set_constant"`; sets are the per-y families; weights 1 per member; W3 adds `"balanced"` per kind (identity orderings weighted 1/4).
- `family_label(beta_row) -> str`: `"DISCRIMINATING"` iff every listed competitor's pooled β ≤ `BETA_MAX`, else `"NOT_DISCRIMINATING"`.

### 5.5 Challenge and the 4×8 comparator (§4.8, §6.1)

- `set_gap(laws, prec=80) -> Decimal`: mean over the members (equal weights) of `kl_decimal(law, mixture, prec)`; `laws` are full-vocabulary Fraction laws.
- `challenge_values() -> dict` (NA, W3, Π0, per y): `"prior"` `{"e": 2/3, "c": 1/6, "c2": 1/6}` (Fractions, from the multiplicities), `"z_information"` (Decimal H(prior)), `"z_information_window"` `{k: Fraction(0)}` for k = 1..9 (exact: identical last-k tokens across members), `"q_bar"` (3 Fractions), `"delta_challenge"` (Decimal: `set_gap` of the 24 members), `"delta_cue"`.
- `block_posterior(prior, likelihoods) -> dict`: `prior` `{z: Fraction}`; `likelihoods` a list of `{z: Fraction}` (one per block); returns the normalised `prior·Π likelihoods`; `ValueError` if the total is 0.
- `block_comparator(y=0) -> dict` (NA, W3, Π0): `"block_likelihoods"` (per block j = 1..4: `{block tokens: {z: Fraction}}` by exact enumeration of the 24 orderings), `"posteriors"` `{ordering: {z: Fraction}}`, `"truth"` `{ordering: z}`, `"accuracy"` (Fraction: fraction of orderings whose argmax equals the truth), `"holonomy_logloss"` (Decimal: mean −ln r_add(truth)), `"regret"` (Decimal: Δ_add,8 = mean full-vocabulary KL(q*‖q_add)). `z` ∈ `{"e", "c", "c2"}`.

### 5.6 G3, O1, O2

- `gate_G3() -> dict`: `"status"`, `"families"` (`family_values` for every arm in `ARMS`, family and prefix of §8.2 G3), `"matched"`, `"keys_constant"` `{family: {S: bool}}`, `"beta"`, `"challenge"`, `"comparator"`, `"set_gaps"` (Decimals beside the closed forms), `"prefix_invariant"` (bool).
- `o1(g3) -> dict`: `{"status": "PASS" | "FAIL", "per_family": {family: {"tv": bool, "constant": bool, "zero_spread": bool}}}` for W1, W2, W3 (§8.3).
- `o2_combine(c1, c2) -> str`: `"PASS"` iff both are `"PASS"`; `"FAIL"` iff at least one is `"FAIL"`; else `"UNCERTIFIED"`.
- `o2(g4) -> dict`: `{"G_parikh": certify(G_Parikh(32), G_MIN), "M": certify_mass(M_lower, M_upper, M_MIN), "status": o2_combine(…)}` (NA).

## 6. x6_run.py

### 6.1 Monte Carlo (§9.6, G6)

- `sample(arm, n, tree) -> (tokens, states)`: `arm` in `MC_ARMS`; NOCUE uses `model("NA", "E_nc")`; one `HMMSampler(Tf, Ef, pif, SequenceLayout()).sample(n, tree.generator(MC_STREAM, arm))` call; tokens uint8 [n, 33], states int16 [n, 33].
- `indicator_se(p, n) -> float`: `sqrt(p(1 − p)/n)` from the exact p (a Fraction, converted by `float`).
- `mc_check(estimate, exact, se) -> bool`: `|estimate − exact| ≤ MC_K·se + MC_FLOOR`.
- `indicator_check(hits, n, p) -> dict`: `{"type": "mc", "estimate": hits/n, "exact": float(p), "se": indicator_se(p, n), "pass": mc_check(…)}`. (p = 0 with 0 hits passes; p > 16/(2¹⁸ + 16) with 0 hits in 2¹⁸ rows fails.)
- `sample_se(x) -> float`: sample SD (ddof = 1) over √n.
- `gate_G5(rows) -> dict`, `gate_G6(rows, g4) -> dict`, `gate_G7(rows, g3, g4, s8=False) -> dict`, `poe(rows) -> dict`. G7 returns `{"status", "items": {item: "PASS" | "FAIL" | "NOT_RUN"}}` over `G7_ITEMS`; with `s8=True` the `G7_DP_ITEMS` are `"NOT_RUN"` and the status is decided by the other items.
- `G7_ITEMS = ("AB.spread", "AB.ambiguity", "AB.G_S", "AB.D_blk", "AB.filter", "ZC.spread", "ZC.ambiguity", "ZC.G_S", "ZC.D_blk", "ZC.filter", "TRIV.spread", "TRIV.G_S", "TRIV.D_blk", "TRIV.filter", "ETA1.cue_uniform", "ETA1.G_S", "ETA1.filter", "GAUGE-NA.filter", "GAUGE-NA.exact", "GAUGE-TRIV.filter", "GAUGE-TRIV.noncommuting", "GAUGE-COV.filter", "GAUGE-COV.exact", "NOCUE", "TOKPERM", "FIXED-POINT", "SAME-HOLONOMY")`.
- `G7_DP_ITEMS = ("AB.ambiguity", "AB.G_S", "AB.D_blk", "ZC.ambiguity", "ZC.G_S", "ZC.D_blk", "TRIV.G_S", "TRIV.D_blk", "ETA1.G_S", "FIXED-POINT")` (§8.5 S8: the G_S, D_blk and class-ambiguity items of the AB, ZC, TRIV and ETA1 rows, and the FIXED-POINT row). `S8_NOT_RUN = ("G6",) + G7_DP_ITEMS`.

### 6.2 Labels and outcome (§8.3–§8.5)

- `ORDER = ("PF", "S0", "G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7")`; `GATES = ("G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "D")`.
- `OUTCOMES = ("GO_X6_NATURAL", "GO_X6_CHALLENGE_ONLY", "INCONCLUSIVE_NATURAL", "STOP_X6", "WITHHELD")`.
- `decide(statuses, o1, o2, s8=None) -> dict`. `statuses` maps every name in `ORDER` to a status (G4 may be `"RESOURCE_LIMIT"`); `o1` is a bool or `None`; `o2` is `"PASS"`, `"FAIL"`, `"UNCERTIFIED"` or `None`; `s8` is `None` or `{"completed_checks_pass": bool, "theorem4": bool}` (`"theorem4"`: the Theorem 4 integer checks completed and passed). Returns `{"verdict", "first_failed", "outcome", "window_clause", "not_run"}`. Rules, scanning `ORDER`:
  1. PF or S0 not `"PASS"` → verdict `"INVALID"`, first_failed that gate.
  2. A gate `"INVALID"` (including an S7 interruption: owner STOP, usage limit, disk floor or wall-limit kill) → `"INVALID"`; a gate `"FAIL"` → `"FAIL"`; a `"NOT_RUN"` with no earlier failure → `"INVALID"`, except as in rule 3.
  3. G4 `"RESOURCE_LIMIT"`: if `s8` is `None` or `s8["completed_checks_pass"]` is false → `"FAIL"` at G4 (S3, never INCONCLUSIVE_NATURAL). Otherwise S8 mode: G6 `"NOT_RUN"` is expected and not a failure; G5 and G7 must be `"PASS"` (G7 judged on its non-DP items); `not_run = list(S8_NOT_RUN)`.
  4. Any failure → `outcome = "WITHHELD"`, `window_clause = False`, `not_run` = every later name in `ORDER` plus `"D"`.
  5. No failure, not S8: `o1` false → `"STOP_X6"`; else `o2` `"PASS"` → `"GO_X6_NATURAL"`, `"FAIL"` → `"GO_X6_CHALLENGE_ONLY"`, `"UNCERTIFIED"` → `"INCONCLUSIVE_NATURAL"`. verdict `"PASS"`; `window_clause = True` except for STOP_X6 (False).
  6. No failure, S8 mode: verdict `"RESOURCE_LIMIT"`; `o1` true → `"INCONCLUSIVE_NATURAL"` with `window_clause = s8["theorem4"]`; `o1` false → `"STOP_X6"` (§8.4 STOP_X6 row, `window_clause = False`).
- `label_cert(cert, yes, no) -> str`: `yes` for `"PASS"`, `no` for `"FAIL"`, `"UNRESOLVED"` otherwise.
- `labels(g3, g4, poe_values) -> dict`: `"P1_link"` (`"LONG_HISTORY"`, `"SHORT_HISTORY"`, `"UNRESOLVED"`: LONG iff `J_8.hi ≤ ½·G_Parikh.lo`, SHORT iff `J_8.lo > ½·G_Parikh.hi`, at t = 32, NA); `"BLOCK"` (`"BLOCK_ORDER_NEEDED"`, `"BLOCK_ORDER_SMALL"`, `"BLOCK_UNRESOLVED"`; D_blk(32) NA vs `G_MIN`); `"INCENTIVE"` (`"ABOVE"`, `"BELOW"`, `"UNRESOLVED"`; `mean_G_parikh` vs `G_MIN`); `"HEADROOM"` (`"HEADROOM"`, `"NO_HEADROOM"`, `"UNRESOLVED"`; G_8(32) vs `G_MIN`); `"FAMILY"` `{family: {"label", "balanced_beta"}}`; `"PoE"` (the §6.3 reading inputs, descriptive).

### 6.3 S0 (§8.1)

- `PROTECTED_PATHS = ("src", "tools/x4_oracle_profile", "tools/d1_seam", "tools/x2a_stage0", "tools/check_file_sizes.py", "tools/x6_stage0", "tests/world", "tests/process", "tests/oracle", "tests/oracle_profile", "tests/dataset", "tests/d1_seam", "tests/x2a_stage0", "tests/x6_stage0", "pyproject.toml")`.
- **S0 allowlist** `ALLOWLIST = ("tools/x6_stage0/API.md", "tools/x6_stage0/x6_model.py", "tools/x6_stage0/x6_exact.py", "tools/x6_stage0/x6_run.py", "tools/x6_stage0/x6_dp.py", "tests/x6_stage0/test_x6_stage0.py", "tests/x6_stage0/test_x6_stage0_dp.py", "tests/x6_stage0/AUTHORSHIP.md")`, exactly §8.1 item 3.
- `KERNEL_DIFF_EXPECTED = ("A\tsrc/topo_pilot/learner/multihorizon.py", "M\tsrc/topo_pilot/learner/trainer.py")`.
- `allowlist_ok(lines) -> bool`: `lines` are the non-empty output lines of `git diff --no-renames --name-status R H -- <PROTECTED_PATHS>`; true iff every line is `"A\t<path>"` with `<path>` in `ALLOWLIST`.
- `kernel_diff_ok(lines) -> bool`: the non-empty lines of `git diff --no-renames --name-status KERNEL_BASE H -- src tools/x4_oracle_profile tests/oracle_profile` equal `KERNEL_DIFF_EXPECTED` as a set, with no other line.
- `s0_check(worktree, head, store, dispatch) -> dict`: `{"status": "PASS" | "INVALID", "items": {"1": bool, …, "6": bool}, "diff": […], "kernel_diff": […], "lineage": s0_lineage(store)}`: item 1 protocol sha256 (`docs/x6/PROTOCOL_X6_v1.md`, moved there by ruling X1 of job 0059, and `agent-handoff/planning/responses/X6-FROZEN-v1.md` both equal `PROTOCOL_SHA256`), item 2 request sha256 (`agent-handoff/planning/requests/coord-x6-stage0-20261015.md`), items 3 and 4 by the two functions above with R = `R_COMMIT`, item 5 the dispatch record's `meter_bind_sha256` equals the sha256 of `<store>/x6_meter_bind.py` and its `meter_import_dir` equals `<worktree>/tools/x4_oracle_profile` (path-normalised, case-insensitive), item 6 `s0_lineage(store)` PASS.

### 6.4 Store, lineage and per-gate records (§10.5, §10.8)

- **Store layout.** Root: `x6_meter_bind.py` and the meter's bookkeeping; `run/` (the active attempt); `superseded/<job>-a<k>/` (archived attempts). No `tmp/`. The dispatch record lives outside the store (in the mailbox job directory).
- `METER_FILES = ("x6_meter_bind.py", "cpu_ledger.json", "cpu_ledger.json.tmp", "cpu_ledger.emergency.jsonl", "RUN.lock", "METER_ACTIVE.lock")` at the store root, and every file under `logs/`: the **recognised meter bookkeeping**.
- `ATTEMPT_RE = r"^\d{4}-a[1-9]\d*$"`: the name of a recorded superseded attempt directory. Its manifest is `superseded/<name>/SHA256SUMS`.
- `sha256_file(path) -> str` (lowercase hex). `write_manifest(attempt_dir) -> Path`: writes `SHA256SUMS` with one line `"<sha256>  <relative posix path>\n"` per file under `attempt_dir` (sorted by path; the manifest itself excluded). `read_manifest(path) -> dict[str, str]`.
- `lineage_precheck(store) -> dict` (§10.8 item 7): `{"status", "run_absent", "attempts", "unrecognised", "missing", "mismatch"}`. PASS iff `run/` is absent and every file in the store is recognised meter bookkeeping, a `SHA256SUMS` of a directory matching `ATTEMPT_RE` directly under `superseded/`, or a file listed in such a manifest; and every listed file exists with its recorded sha256. A manifest need not list or hash itself. An absent store passes. Lists hold paths relative to the store (posix).
- `s0_lineage(store) -> dict` (§8.1 S0 item 6): as `lineage_precheck`, except that `run/` must exist and hold exactly one entry, the regular file `preflight.json` (any marker, `gates/` directory or `GATES.jsonl` gives INVALID/LINEAGE). Adds `"run_contents"`.
- `archive_attempt(store, job, ledger_entries=(), logs=()) -> Path` (§10.8 item 4): destination `superseded/<job>-a<k>` with the smallest k ≥ 1 not yet used; moves `run/` to `<dest>/run/`; writes `<dest>/ledger_entries.json` (canonical JSON list of the given ledger entries) and copies each path in `logs` to `<dest>/logs/<name>`; then `write_manifest(dest)`. Deletes and edits nothing else. `FileNotFoundError` if `run/` is absent.
- `compare_attempt(attempt_dir, run_dir, affected=()) -> dict` (§10.8 items 4 and 6): for every manifest entry `run/gates/<gate>/<file>` of `attempt_dir` with `<gate>` not in `affected` and the same file present under `run_dir/gates/<gate>/`, compares sha256. `{"status": "PASS" | "INVALID/LINEAGE", "compared": […], "mismatch": […], "missing": […]}`; any mismatch is INVALID/LINEAGE; files the new run has not (yet) produced are listed in `"missing"` only.
- `jsonable(obj)`: Fraction → `str(Fraction)` (`"p/q"` or `"p"`), Decimal → `str`, tuple → list, numpy scalar → Python scalar, numpy array → list, dict keys → `str` (tuple keys joined by `","` after `str` of each part).
- `canonical_json(obj) -> bytes`: `json.dumps(jsonable(obj), sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")`.
- `VOLATILE_KEYS = frozenset({"cpu_s", "wall_s", "utc", "started_utc", "finished_utc", "timestamp", "path", "out_dir", "store", "worktree", "tempdir", "basetemp"})`; also every key ending in `"_utc"`, `"_path"` or `"_dir"`. `strip_volatile(obj)`: recursive copy with every such dict key removed. `reports_equal(a, b) -> bool`: `strip_volatile(a) == strip_volatile(b)` after `jsonable`.
- `write_marker(run_dir, gate)`: creates `run_dir/gates/<gate>/` and the empty marker `STARTED` by exclusive create, before the gate starts. `gate` in `GATES` only.
- `write_gate(run_dir, gate, status, values) -> dict`: for `gate` in `GATES`, writes `run_dir/gates/<gate>/values.json` = `canonical_json(strip_volatile(values))` by exclusive create, then appends one line `canonical_json({"gate", "status", "files": {"STARTED": sha, "values.json": sha}}) + b"\n"` to `run_dir/GATES.jsonl`; returns the record. For `"PF"` and `"S0"` (only after S0 has finished) it writes no file or directory and appends `{"gate", "status", "files": {}}`.
- **Per-gate artifacts (§10.8 item 1):** for each of G0–G7 and D, exactly `gates/<gate>/STARTED` and `gates/<gate>/values.json`, plus the gate's line in `GATES.jsonl`. They contain no volatile field.

### 6.5 Preflight, run, report

- `scratch_ok(path, job) -> bool`: the resolved path lies under `SCRATCH_ROOT/<job>/` (case-insensitive).
- `write_preflight(store, record) -> dict`: runs `lineage_precheck(store)` first; if it is not PASS, writes nothing and returns `{"status": "INVALID", "lineage_precheck": …}`. Otherwise creates `run/` and writes `run/preflight.json` (canonical JSON) holding `record` plus `"lineage_precheck"` and `"status"`. `record` keys: `"job"`, `"head"`, `"head_expected"`, `"porcelain"` (list of lines), `"tempdir"` (from inside a metered child), `"basetemp"`, `"suites"` `{suite: returncode}`, `"new_tests"` (returncode), `"file_sizes"` (returncode). Status PASS iff `head == head_expected`, `porcelain == []`, both `scratch_ok`, every return code 0 and the precheck PASS.
- `run(store, dispatch) -> dict`: `dispatch` is the path of the dispatch record (JSON: `"job"`, `"head"`, `"worktree"`, `"meter_bind_sha256"`, `"meter_import_dir"`). Requires `run/preflight.json` with status PASS (else PF INVALID), then `s0_check`, then G0 → … → G7 → D with first-failure stops (§8.0, S8 exception), markers and per-gate records as in §6.4, then writes `run/report.json` (canonical JSON) and `run/model.npz`. Returns the report. CLI: `python x6_run.py precheck --store S`, `python x6_run.py preflight --store S --record R`, `python x6_run.py run --store S --dispatch D`.
- `model.npz` (`np.savez`, uncompressed): `"T_base"` (`to_float(t_base_exact())`), `"T_lift_<arm>"` for every arm in `ARMS` (`model(arm)["Tf"]`), `"E"`, `"E_cov"`, `"E_nc"`, `"E_sigma"` (float64). `model_sha256` = `{name: sha256 of array.tobytes()}` (C order); the npz file's own hash is not compared (zip metadata).
- **report.json keys:** `protocol` (`PROTOCOL_ID`), `protocol_sha256`, `verdict`, `first_failed`, `gates` (every name in `ORDER` and `"D"`: `{"status", …values}`), `exact` (G2 and G3 exact quantities), `natural` (G4: ladder, windows, masses, M_32, n_min), `challenge` (§4.8 values and the 4×8 comparator), `blocks` (K-blk per arm and PoE), `controls` (G7 items), `mc` (G6 comparisons and Monte Carlo summaries), `decimal` (G5 Decimal reference), `outcome` (`decide` output), `labels`, `seeds` (`tree.issued`), `model_sha256`, `cpu_s`.
- **Value types (§10.2 v3):** exact oracle values (Fractions, Python ints) are reported as `{"type": "exact", "value": str}`; logarithmic oracle values as the `enclosure` dict of §4.3 plus `"cert"` where a threshold applies; Monte Carlo estimates as `{"type": "mc", …}`; floating-point validation diagnostics as `{"type": "float", "value", "tol"}`; resource measurements as `{"type": "resource", …}`. Only `exact` and `enclosure` values are called exact or certified.
- **Volatile report fields** (excluded from every bit-identical comparison of §10.8): `cpu_s`, `wall_s`, timestamps (`utc`, `*_utc`, `timestamp`) and absolute paths (`path`, `*_path`, `*_dir`, `out_dir`, `store`, `worktree`, `tempdir`, `basetemp`), i.e. `VOLATILE_KEYS` and its suffix rules.

### 6.6 Seeds (§8.6)

One `SeedTree(MASTER_SEED)` per run. Streams are issued in `MC_ARMS` order, `tree.generator(MC_STREAM, arm)`, one `sample` call each, with `n = MC_ROWS[arm]`. GAUGE-NA, GAUGE-COV, TOKPERM and PoE reuse the NA rows; GAUGE-TRIV reuses the TRIV rows. `report["seeds"] = tree.issued`. A rerun never reseeds and never changes n.

## 7. Implementation choices (open in the protocol; simplest option)

1. The optional `x6_dp.py` exists and holds §4 of this contract (DP, aggregation, counts, K-blk, Decimal conversion, KL, memo, enclosures, certification, `decimal_model`, natural quantities, G4).
2. Permutations are tuples; exact matrices are lists of lists of Fractions; float arrays are `float(Fraction)` entrywise.
3. `NEIGHBOURS` order `(+x, −x, +y, −y, stay)` fixes every iteration order (DFS, DP, enumeration).
4. Face traversal `(r0, r2, r3, r1, r0)` of a local-lexicographic row; lifted squares transport from the row's first corner; lifted edges follow the orientation of the `spec.cells[1]` row.
5. k-gram laws are computed in exact Fractions (G1's relative tolerance is then met exactly).
6. In gauge arms, `family_values` reports holonomies under the arm's own labels; the ladder and K-blk are not computed there (§2.4).
7. A no-cue history's R_S key is `(True, tokens, None, None, v_t, None)`.
8. β weights: 1 per member (W3 balanced: identity orderings 1/4); each law centred by its own weighted set mean.
9. The memo serves η = 1/50 only; ETA1's zeros are exact Fraction statements.
10. Enclosure endpoints are computed in a 200-digit context; certification compares exactly through Fractions.
11. P1-link compares two enclosures (LONG iff `J_8.hi ≤ ½·G.lo`; SHORT iff `J_8.lo > ½·G.hi`). HEADROOM values are `HEADROOM`, `NO_HEADROOM`, `UNRESOLVED`; FAMILY values `DISCRIMINATING`, `NOT_DISCRIMINATING`.
12. Store lineage: the meter bookkeeping names of §6.4 (the job-0014 meter's files, `logs/` entire); attempt directories `<job>-a<k>`; manifests in `sha256sum` text format; markers `gates/<gate>/STARTED`; one `values.json` per gate; canonical JSON; the dispatch record outside the store.
13. `decide` under S8 with O1 false returns `STOP_X6` (the §8.4 STOP_X6 row has no O2 or S8 condition).
14. `model.npz` is described by per-array sha256 values.
15. (job 0059, ruling X1) The protocol copy lives at `docs/x6/PROTOCOL_X6_v1.md` (outside the protected paths, sha256 unchanged); `s0_check` item 1 hashes that path. Mentions of `tools/x6_stage0/PROTOCOL_X6_v1.md` above refer to it.
16. (job 0059) `natural` also returns `"I_fib_full"` `{t: enc}` (I^fib(t) = I^fib_t(t), used by G6), `"A_dp"`/`"B_dp"` (A_n, B_n summed from the DP layers), `"fixed_point"` (`{"amb_y": {y: bool}, "G_empty_y": {y: enc}}`: AB's FIXED-POINT inputs, ∅ classes at N(a★), t = 32) and `"zc_witness"` (`{name: count}` of the counts class (n = 7, v = 6, (1, 0))). `"masses"` is `{t: {"E_cue", "age", "no_cue", "E_nb", "amb", "amb_nb"}}`. M_t(θ) is computed at t = 32 only (the gated value). `"pyth"` is `{t: {"empty": enc, "H1": enc}}`, each the enclosure of G_S − G_Parikh − E KL(q_Parikh‖q_S).
17. (job 0059) Decimal sums: per DP layer n each quantity accumulates Σ W·KL (W the integer class weight of image z) in the 80- and 120-digit contexts, then is scaled by the exact coefficient 1/(240·5^n) (next-symbol, Pythagorean) or 1/(48·5^n) (fibre), converted by rational division. N counts every evaluated term; classes that are not ambiguous contribute exact zeros and are not summed. `abs_sum` is the sum of the absolute per-layer values.
18. (job 0059) `gate_G4` returns NA's class tables at the top-level key `"tables"` (the G6 input); `run` never writes them to `values.json`. A `MemoryError` sets RESOURCE_LIMIT with the step; checks whose inputs did not complete are `"NOT_RUN"`.
19. (job 0059) Value-identical caches: `MEMO`, the Pythagorean KL cache and an `ln` cache keyed by (precision, exact Fraction ratio) are cleared at every DP layer n (and every K-blk cue position), because every key carries n; `lam` and `point_law` are `lru_cache`d. A cached value is the identical Decimal or Fraction that recomputation returns (§5.6 item 6); memory stays bounded by one layer.

20. (job 0060) `x6_run` choices: the closed-form = BayesFilter checks (G5, G7 `*.filter`) compare b_t and q_t for t = 1..32 and q_0, with float closed-form vectors cached by (arm, w_t, fibre law); the §9.5 reference set uses NA, the edge case (iii) member `"AB"`, and repeats only the five edge cases at 120 digits; q_8 = `FutureOperator.F1(suffix_posterior(…, 8))`; G6 builds q_S from q* by replacing the cue entries with P_MOVE·(λ_{n+1}w_S + (1 − λ_{n+1})u) for n ≥ 1 at N(a★) (q_S = q* elsewhere); a gate exception gives INVALID with the error recorded (S2 for G0); gates that do not run get no marker; PoE and the labels are computed in D only when the outcome is released; `report.json` wraps Fractions as `{"type": "exact"}` (ints stay plain); `run` writes nothing if `run/` is absent, and PF is INVALID unless `preflight.json` is PASS with the dispatch record's head and job.
21. (job 0062; coordinator addendum 1 to X6-FROZEN-v1, rulings X5 and X5′, cut B) A fifth module file `x6_store.py` (≤ 400 lines) holds, moved byte-identical in behaviour from `x6_run.py`: the §6.2 outcome logic `ORDER`, `OUTCOMES`, `G7_ITEMS`, `G7_DP_ITEMS`, `S8_NOT_RUN`, `decide`, `label_cert`, `labels`; the §6.3 S0 names `MAILBOX`, `GATES`, `PF_SUITES`, `PROTECTED_PATHS`, `ALLOWLIST`, `KERNEL_DIFF_EXPECTED`, `allowlist_ok`, `kernel_diff_ok`, `s0_check`; the §6.4 store, lineage and record names `METER_FILES`, `ATTEMPT_RE`, `VOLATILE_KEYS`, `sha256_file`, `write_manifest`, `read_manifest`, `lineage_precheck`, `s0_lineage`, `archive_attempt`, `compare_attempt`, `jsonable`, `canonical_json`, `strip_volatile`, `reports_equal`, `write_marker`, `write_gate`; the §6.5 helpers `scratch_ok`, `write_preflight`, `_typed`; and the private helpers `_git`, `_norm`, `_lineage`, `_key`, `_volatile`, `_load`. `x6_run` re-exports every one of these names except `_git`, `_lineage`, `_key` and `_volatile` (used only inside `x6_store`), so `xr.<name>` stays valid. `x6_run.py` keeps §6.1 and the gates (Monte Carlo, G5, G6, G7, PoE), `run`, report and NPZ writing, and the CLI. Import order: `x6_model` ← `x6_dp` ← `x6_exact` ← `x6_store` ← `x6_run`. `ALLOWLIST` (and §8.1 item 3) adds `tools/x6_stage0/x6_store.py` (addendum item 2); this is the only content change among the moved lines.

## 8. Not covered by tests

The store-local meter binding `x6_meter_bind.py` (outside the repository) is bound by S0 item 5 and PF's record of the child environment (§10.4).

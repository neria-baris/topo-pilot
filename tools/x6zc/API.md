# tools/x6zc: written contract (job 0117; derived from X6ZC-DESIGN-v1)

**Authority.** `tools/x6zc/PROTOCOL_X6ZC_v1.md`, a byte-for-byte copy of `agent-handoff/planning/responses/X6ZC-DESIGN-v1.md` (sha256 `2a711d16d0c3b5e7cdfc0c96e7342a86c0e500b3f31592868ba5b661ef324193`, design freeze candidate). Owner addendum 29 (standing AUTH-IMPL and AUTH-RUN while the combined CPU of HWS, X6ZC and C2ND stays below 12 CPU-h); the §18 owner questions are answered with their defaults. Section numbers (§n), stage items (A1–A4, K0–K6, B1–B10, D2, D3), rules (G-R0 … R10) and growth rules (G1–G3) refer to the protocol.

**Precedence.** The protocol is authoritative. This contract fixes names, signatures, shapes, dtypes, random streams, file layouts, record and report schemas and the gate order, so that the independent tests can be written before any module exists. It changes no scientific choice. Where the protocol leaves a detail open, §18 "Choices" fixes the simplest option consistent with it. Where this contract and the protocol differ, the protocol wins and the difference is a contract defect (report it; never resolve it in code). `CONTRACT.json` holds the machine-readable values; the protocol wins over it as well.

**Nothing here authorises a run.** No model forward, sampling, oracle run, dry run or test run follows from this contract. Implementation, the independent tests and the synthetic dry run need owner go-ahead (a) (§15 step 3; covered by addendum 29); the real stages need the execution freeze and owner AUTH (b).

## 1. Files, budgets, imports (§14)

| File | Contents (sections of this contract) | Budget |
|---|---|---|
| `x6zc_core.py` | CONTRACT loading, constants and bindings (§3), fresh prefixes and variant construction (§4), exact geometry K0 and the q*_NA cache (§5), synthetic and analytic predictors (§6), pair terms and the K1, K2, K3/F1 checks (§7), paired cluster bootstrap, ratio intervals and B9 sizing (§8), the §9 decision, qualifiers, licences and reuse verdict (§9) | ≤ 400 lines |
| `x6zc_census.py` | A-audit, A4 exposure matching, K4 comparison, K5 independent checks, B3, B4, B6, B7, B10, D2, D3 and the Stage-B descriptive tier (§10) | ≤ 400 lines |
| `x6zc_run.py` | stages 0 (dry run), A, B, C; gates and stop handling; store writer (exclusive create); `EXPOSURE.jsonl`, `EVALUATIONS.jsonl`; the stage-1 store no-write check; meter binding; ledger and pause points; model chunk children; report and its schema check; CLI (§11) | ≤ 400 lines |
| `API.md`, `PROTOCOL_X6ZC_v1.md`, `CONTRACT.json`, `TEST_PLAN.md` | this contract; the protocol copy; machine-readable values; the test plan | — |
| store-local `x6zc_meter_bind.py` | outside the repository, in `x6zc-store/` (pattern of `x6-stage1-store/x6s1_meter_bind.py`) | — |

**Module split (OPEN-4, decided now).** The function list of §14 for `x6zc_core.py` (constants and bindings, `prefix_yields`, `fresh_prefixes`, `variant_arrays`, `oracle_geometry`, `audit_pairs`, `synthetic_predictor`, `pair_arrays`, `decompose`, `zc_profile`, `weighting_summaries`, `paired_cluster_boot`, `ratio_intervals`, `decide_x6zc`) plus the checks it implies (K1–K3, F1, B9, qualifiers, licences, the reuse verdict, K5, D2, B6, B7, B10, A4) exceeds 400 lines. The split therefore applies: the descriptive functions (A-audit, B3–B7, D2, D3) and the other census checks (A4, K4 comparison, K5, B10, descriptive tier) live in `x6zc_census.py`. No scientific change. Exactly these three modules; a fourth `.py` file or a file over 400 lines is a contract defect. No change to `src/`, `tools/x6_stage1/`, `tools/x6_stage0/` or any other existing file.

**Import convention.** `x6zc_core` computes `HERE = Path(__file__).resolve().parent`, `REPO = HERE.parents[1]`, prepends `HERE` and `REPO / "tools" / "x6_stage1"` to `sys.path` if absent, then imports `x6s1_data as sd` first (its import applies the X6S1 `sys.path` convention: `tools/x6_stage1`, `tools/x6_stage0`, `tools/x4_oracle_profile`, `tools/d2a`, `tools/k4b`, `tools/c1prime_registry`, `tests/oracle_profile`), then `x6_model as xm`, `x6_exact as xe`, `x6s1_pairs as sp`, `x6s1_eval as se`, `x6s1_stats as ss`, and `from topo_pilot.contracts import SeedTree, canonical_json`. `x6zc_census` imports `x6zc_core as zc` first; `x6zc_run` imports `x6zc_core as zc`, `x6zc_census as zs`, then `x6s1_stage_pre as pre`, `x6s1_ingest as si`, `x6s1_run as sr`, `x6s1_decide as sdc`, `x6s1_cloud as sc` lazily inside the functions that need them (torch-heavy imports are not paid by the decision tests). Dependency order (no cycles): `x6zc_core` ← `x6zc_census` ← `x6zc_run`. Importing a module performs no I/O beyond reading `CONTRACT.json` and no computation beyond small constants. Runs use `X:/Downloads/projects/topo-pilot/topo-pilot/.venv/Scripts/python.exe -s` with `PYTHONPATH=<worktree>/src` (the editable install points at main's `src`).

**Test imports.** A test file inserts `REPO / "tools" / "x6zc"` at `sys.path[0]` (REPO = `Path(__file__).resolve().parents[2]`) and imports `import x6zc_core as zc`, `import x6zc_census as zs`, `import x6zc_run as zr`. Reused code by bare name: `x6s1_pairs as sp`, `x6s1_eval as se`, `x6s1_stats as ss`, `x6s1_data as sd`, `x6_model as xm`, `x6_exact as xe`.

**Module split amended (R-0123-1; §20 C-52).** The three files above are split further into nine modules of at most 400 lines each; the names of §3-§11 stay reachable as `zc.<name>` (`x6zc_core`) and `zr.<name>` (`x6zc_run`) through re-exports. The module list and the import order are in §20 C-52, which supersedes the "exactly these three modules" sentence and the import convention above where they differ.

## 2. Conventions

- **Tokens.** Vocabulary 18 (vertex tokens 0..14 for vertices ≠ 10 via `xm.tok`; cue tokens 15 + y, y ∈ {0, 1, 2}); BOS = 18 (`se.BOS`). Histories are `uint8[n, 33]`, zero-padded after their length; the readout position `t` (`int16` or `int64[n]`) is the history length: the predictor reads `tokens[:, :t]` and predicts token t + 1 (`se.ModelPredictor._run` reads logits at index t of `[BOS] + tokens[:32]`).
- **Pairs.** A pair family array dict (the `sp.designed_arrays` layout) has keys `<key>_a`, `<key>_b` (`uint8[n, 33]`), `<key>_t` (`int16[n]`), `<key>_y` (`int8[n]`). For D, `<key>` ∈ `sp.PAIR_FAMILIES` = ("W2", "C1", "C2", "C3", "C4", "W1") plus the sets "W3", "W3p" (key `_a` only). For the fresh variants, one dict per family with `<key>` ∈ `VARIANT_ORDER` = ("PP", "MM", "PM", "MP") and an extra key `"prefix"` (`int32[n]`). Member a is the x-first ordering everywhere.
- **Row layout.** Prefix-major, then cue: row `3i + y` belongs to prefix i and cue y (the `sp.designed_set` order). The cluster of a row is its prefix index `i = row // 3`; clusters are prefix rows, not token strings (two equal prefix strings are two clusters; D3 groups them).
- **Predictors.** A predictor is a callable `pred(tokens: uint8[n, 33], t: int or int64[n]) -> float64[n, 18]` (rows sum to 1), with an attribute `name: str`. The exact q*-type laws are `tuple[Fraction] * 18`.
- **Cue normalisation and pair terms** are the X6S1 functions unchanged: `se.cue_normalise`, `se.pair_terms(ph, ph2, qh, qh2) -> (num float64[n], den float64[n])`, `se.beta_fsum(num, den) -> float` (NaN if Σden = 0), `se.beta_exact(num, den) -> Fraction`.
- **ρ.** For a pair set, ρ = mean_i‖Δp̂_c,i‖² / mean_i‖Δq*_c,i‖² with `math.fsum` means (the `designed_stats` `rho_W2` rule). For variant v of family F the denominator is that variant's own Δq*; for the C1–C4 control families the denominator is W2's (as `designed_stats` `rho_C`).
- **Dtypes.** float64 everywhere; exact values are `fractions.Fraction`; counts are Python `int`; per-pair arrays `float64[n]`; masks `bool[n]`.
- **Hashes.** Lowercase 64-hex sha256 of file bytes; comparisons with recorded values are case-insensitive.
- **JSON.** Records are written by exclusive create with `canonical_json` (sorted keys) after `se._clean` (non-finite floats → `null`); JSONL lines likewise, one per line, appended. Fractions are written as `"p/q"` strings, floats as JSON numbers (repr round trip).
- **UTC.** `"%Y-%m-%dT%H:%M:%SZ"`.
- **Check statuses (exact strings).** `"PASS"`, `"FAIL"`, `"NOT_RUN"`, `"DEFECT_CANDIDATE"`, `"ENV_DRIFT"` (K4 only), `"NUMERIC_DRIFT"` (K5a only), `"SETUP_ERROR"`.
- **Outcome strings** are exactly those of `CONTRACT.json` `outcomes` (§9 of this contract); qualifier strings are those of §9.4.

## 3. x6zc_core: constants and bindings

### 3.1 Loading
- `CONTRACT_PATH = HERE / "CONTRACT.json"`; `load_contract(path=CONTRACT_PATH) -> dict`: `json.loads` (utf-8); raises `ValueError` if `sha256(PROTOCOL_FILE bytes) != contract["protocol"]["sha256"]`. `CONTRACT = load_contract()` at import.
- `frac(s) -> Fraction` = `Fraction(str(s))` (exact for `"1/10"`, `"1e-9"`, `"0.05"`).
- `stream(name) -> np.random.Generator` = `SeedTree(X6ZC_MASTER).generator(*CONTRACT["constants"]["streams"][name])`; names `"boot_B"`, `"boot_C"`, `"sens_A4"`, `"sens_DPREFIX"`, `"perm_K5i"`. `dry_stream(*names)` = `SeedTree(X6ZC_MASTER).generator("x6zc", "dry", *names)`.

### 3.2 Names (values in `CONTRACT.json`)
- `PROTOCOL_ID = "X6ZC-DESIGN-v1"` (`"X6ZC-FROZEN-v1"` after the freeze), `PROTOCOL_FILE = HERE / "PROTOCOL_X6ZC_v1.md"`, `PROTOCOL_SHA256`.
- Paths (`str`): `PROJECT_ROOT`, `X6S1_STORE = ".../x6-stage1-store"`, `STORE = ".../x6zc-store"`, `WORKTREE = ".../topo-pilot-x6zc"`, `SCRATCH_ROOT = "X:/Downloads/topo-scratch"`, `DRY_STORE = SCRATCH_ROOT + "/x6zc-dry"`, `METER_IMPORT_DIR = WORKTREE + "/tools/x4_oracle_profile"`.
- `H3 = "213d1e2c0dbfd1609c7024eeb052310366562547"` (H‴), `MERGE_COMMIT = "1dc974934540b818ac64a927d0412bd5c387eff2"`, `CLOSURE = ("src", "tools/x6_stage1", "tools/x6_stage0", "tools/d2a", "tools/x4_oracle_profile", "tools/k4b", "tools/c1prime_registry", "tests/oracle_profile")`.
- `X6ZC_MASTER = 2026102670`.
- `FAMILIES = ("W2", "W1")`, `VARIANT_ORDER = ("PP", "MM", "PM", "MP")`, `VARIANT_SIGN = {"PP": 1, "MM": -1, "PM": 0, "MP": 0}` (s_v of §3.1).
- `VARIANTS = {"W2": {"PP": (("A+", "B+"), ("B+", "A+")), "MM": (("A-", "B-"), ("B-", "A-")), "PM": (("A+", "B-"), ("B-", "A+")), "MP": (("A-", "B+"), ("B+", "A-"))}, "W1": {"PP": ((14, 15, 3, 0, 4, 5, 6), (14, 15, 12, 0, 4, 5, 6)), "MM": ((6, 5, 4, 0, 12, 15, 14), (6, 5, 4, 0, 3, 15, 14)), "PM": ((14, 13, 12, 0, 3, 7, 6), (14, 13, 12, 15, 3, 7, 6)), "MP": ((6, 7, 3, 15, 12, 13, 14), (6, 7, 3, 0, 12, 13, 14))}}`: W2 entries are (member a letters, member b letters) over `xe.LOOPS`; W1 entries are (member a path, member b path) of vertices after the cue (the §3.1 table). `VARIANTS["W2"]["PP"] == sp.W2_LETTERS`; `VARIANTS["W1"]["PP"] == (xe.witness_path("W1", "U"), xe.witness_path("W1", "D"))`.
- `W1_TAIL = {"PP": 4, "MM": 2, "PM": 3, "MP": 3}` (shared token tail), `W1_CROSS_STEPS = {"PP": (3, 4), "MM": (5, 6), "PM": (4, 5), "MP": (4, 5)}` (1-based edge indices along `(ANCHOR,) + path`), `READOUT_OFFSET = {"W2": 18, "W1": 8}` (t = len(prefix) + offset), `LAMBDA_INDEX = {"W2": 18, "W1": 8}` (λ = `xm.lam(index)`).
- `ANSWERS`: `CONTRACT["constants"]["answers"]` (per variant: S3 element names for NA, ZC, AB, ZC_miss1, ZC_miss2, ZC_miss_both, members (a, b); the §3.1 tables).
- `CELLS = {"P": {"model": "ZC-s1", "family": "W2", "beta_D": 0.20930750050575797, "sign": 1, "b_q": (1/40, 39/40), "r_q": (1/120, 119/120), "z": 2.394}, "S3": {"model": "ZC-s3", "family": "W1", "beta_D": -0.13252283561285252, "sign": -1, "b_q": (1/80, 79/80), "r_q": (1/240, 239/240), "z": 2.638}, "S4": {"model": "ZC-s4", "family": "W1", "beta_D": -0.21837877479808415, "sign": -1, "b_q": (1/80, 79/80), "r_q": (1/240, 239/240), "z": 2.638}}` (quantile levels as Fractions); `CELL_ORDER = ("P", "S3", "S4")`. The β_D values are the stored `designed.json` values (protocol §8 cell table).
- `MODELS` (12, `sd.MODELS` order), `INITS = ("init-s1", …, "init-s4")`, `STAGE_B_ORDER = INITS + ("AB-s1", "AB-s2", "AB-s3", "AB-s4", "ZC-s2", "NA-s1", "NA-s2", "NA-s3", "NA-s4", "ZC-s3", "ZC-s4", "ZC-s1")` (§7 known cases first), `FOCAL = ("ZC-s1", "ZC-s3", "ZC-s4")`, `K5_MODELS = ("ZC-s1", "ZC-s3", "ZC-s4", "NA-s1", "init-s1")`, `NA_MODELS`, `K6_CONTROLS = {"W2": (11 names), "W1": (10 names)}`, `K6_MIN = {"W2": 10, "W1": 9}`.
- `T = {name: Fraction}`: every `CONTRACT["thresholds"]` string read with `frac` (`placebo` 1/10, `placebo_band` 1e-9, `material_change` 1/20, `ref_abs` 1e-12, `k5a_ok` 1e-12, `k5a_drift` 1e-9, `repeat_abs` 1e-12, `padding_abs` 1e-13, `k4_rel` 1e-9, `census_pair_diff` 1e-9, `precision_sensitive` 1e-5, `cue_mass_t` (3/20, 1/4), `cue_mass_tm1_max` 1/100, `r_band` (1/2, 3/2), `b_margin` 1/10, `lo_margin` 1/20, `undefined_max` 1/100, `h_target` 1/4, `se_floor` 1/20, `f1_min_distance` 1). Comparisons of a float with a threshold use the float comparison `x <= float(bar)` (resp. `<`, `>`, `>=` as written); counts are compared as integers; exact `Fraction` comparison only where both sides are exact (§20 E-1, ruling R-0120-1).
- `B_DRAWS = 5000`, `N_FLOOR = 512`, `N_LADDER = (1024, 2048)`, `N_D = 1030`.

## 4. x6zc_core: fresh prefixes and variant construction (A3, §3.1, §4.2)

- `prefix_yields(prefix_tokens, rnd_len) -> list[tuple[int, tuple[int, ...]]]`: the `sp.natural_prefixes` rule over **every** row with no 1,024 cap: for each row r (in order) draw `lmax = int(rnd_len.integers(1, 15))` (one call per row, skipped rows included); `ok = [L for L in 1..lmax if xm.vertex(row[L-1]) ∈ sp.NB ∪ {sp.ANCHOR}]`; if `ok`, yield `(r, tuple(row[:ok[-1]]))`.
- `fresh_prefixes(prefix_tokens, d_prefixes) -> dict` with `rnd = SeedTree(sd.DATA_MASTER).generator("x6s1", "prefix_len")` built inside (twice: once for `prefix_yields`, once for the check). Keys: `"n_rows"` (4096), `"n_yields"`, `"first_1024_equal"` (`[p for _, p in yields[:1024]] == sp.natural_prefixes(prefix_tokens, <fresh generator>)`), `"d_equal"` (the same list equals `[p for _, p in d_prefixes[6:]]`, D's natural prefixes; `d_prefixes` = `D["prefixes"]` of `sp.designed_set`, a list of `(name, tokens)`), `"r_star"` (row of the 1,024th yield), `"fresh"` (list of `(row, tokens)` for the yields with row > r_star, in order), `"n_avail"`, `"d_coincident"` (`bool[n_avail]`: the token string occurs among D's 1,030 prefixes), `"n_d_coincident"`, `"not_enough_data"` (`n_avail < 512`). Raises `ValueError` if fewer than 1,024 yields exist.
- `variant_path(family, variant, member) -> tuple[int, ...]`: the vertex path after the cue. W2: `(9, 5) + loops + (1, 2, 3, 7, 11, 15, 14)` with `loops = xe.LOOPS[l1] + xe.LOOPS[l2]` for the member's letters; W1: the `VARIANTS` path. `member ∈ ("a", "b")`.
- `variant_history(family, variant, member, prefix, y) -> tuple[int, ...]` = `tuple(prefix) + (15 + y,) + tuple(xm.tok(v) for v in variant_path(...))`. For PP it equals `sp.designed_history(prefix, letters, y)` (W2) and `sp._w1_history(prefix, "U"/"D", y)` (W1) exactly.
- `variant_arrays(prefixes, family) -> dict`: for each variant v in `VARIANT_ORDER`: `v_a`, `v_b` (`uint8[3P, 33]`, padded as `sp._pad`), `v_t` (`int16`, `len(prefix) + READOUT_OFFSET[family]`), `v_y` (`int8`); `"prefix"` (`int32[3P]`, the index into `prefixes`). Row layout as §2. `prefixes` is a list of token tuples.
- `d_cluster(n_rows) -> int32[n_rows]` = `arange(n_rows) // 3` (D's prefix index of a stored pair row; A-audit verifies it from content).

## 5. x6zc_core: exact geometry (K0) and the q*_NA cache

- `crossings(path) -> list[tuple[int, str]]`: for the path `(ANCHOR,) + path` the 1-based edge index and letter of every seam crossing (`xm.seam_letter`).
- `holonomy_missing(arm, segment, skip) -> tuple`: the `xm.holonomy` of `segment` under `xm.edge_labels(arm)` with the labels of the crossings whose order index (0-based among crossings) is in `skip` replaced by `xm.S3_E`.
- `missed_law(history, which) -> tuple[Fraction] * 18`: the ZC law with crossings skipped: `which ∈ ("miss1", "miss2", "miss_both")` (skip {0}, {1}, {0, 1}); equal to `sp.q_exact("ZC", history, t)` except the three cue entries, which are `P_cue · point_law(n + 1, g[y])` with `P_cue` the q*_ZC cue mass of the history, `n`, `y` from `xm.parse` and g = `holonomy_missing("ZC", segment, skip)` (§6 K0 item 3, RC-11). No new history is built.
- `answer_names(history) -> dict` keys `"NA"`, `"ZC"`, `"AB"`, `"ZC_miss1"`, `"ZC_miss2"`, `"ZC_miss_both"`: the `xm.perm_name` of the holonomy whose image of y carries the point law (the name of g, not of g[y]).
- `oracle_geometry(arrays, family, keys=VARIANT_ORDER) -> dict` (K0; exact Fractions through `sp.q_exact`): for every pair of every key: (1) `q*_ZC(a) == q*_ZC(b)` and `q*_AB(a) == q*_AB(b)`; (2) cue-normalised `Δq*_NA,c = λ(δ_{c²y} − δ_{cy})` with λ = `xm.lam(LAMBDA_INDEX[family])` and den = 2λ²; (3) `answer_names(a)`, `answer_names(b)` equal `ANSWERS[variant]`; (4) variant matching: W2 — token bag, directed-bigram bag, Parikh κ, (n, end vertex, y), last 8 tokens equal; W1 — the `xe._EQUAL_ROWS` statistics equal (length, n, end, prefix, cue, parikh, h1, counts, parity, computed as `xe.matched` does but on the variant paths), start and end vertices ∈ `xm.ANCHOR_NB`, adjacency legal (`xm.parse` raises otherwise), crossing letters as `ANSWERS`, end-vertex q*_NA cue mass 1/5, bags differing in exactly one visited vertex, shared tail `== W1_TAIL[v]` and crossing steps `== W1_CROSS_STEPS[v]`; (5) for fresh arrays, `q*_NA` of each (variant, member, y) identical across prefixes. A zero q*_NA cue mass at a readout position fails item 2 (no exception). Returns `{"status": "PASS" | "FAIL", "checks": {item: bool}, "counterexample": None | {"key", "row", "item", "detail"}, "n_pairs": int}`; the smallest counterexample (lowest key in `VARIANT_ORDER`, then row) is kept. For D's arrays the keys are `("W2",)` or `("W1",)` and are checked as variant PP (items 1–4), and for D's control pairs `("C1", "C2", "C3", "C4")` with items (1)–(2) replaced by: q* of a equals q* of b for NA, ZC and AB (recorded, not gated: §18 C-3).
- `coupling_table() -> dict` (on prefix Π0 = (), exact): `{family: {variant: {str(y): {member: {"zc": name, "cos2_e": "p/q", "sign_e": ±1|0, "cos_e": float, "miss1": {"to": name, "cos2": "p/q", "sign": int, "cos": float}, "miss2": {…}}}}}}` where d = Δq*_NA,c (a − b), e_z = δ_z − ⅓·1 for the member's ZC answer z, and a missed-crossing direction is δ_miss − δ_z. Cosines are reported for the member's own Δ (no sign flip for member b). PP, y any: cos_e = √3/2 (cos2 3/4), miss direction cos = −1 for member a.
- `class QStarCache`: `QStarCache.build(array_dicts: list[dict]) -> QStarCache` computes `se.qstar("NA", tok, t)` once per distinct `(bytes(tok[:t]), t)` over every `_a`/`_b` array in the dicts; `cache(tokens, t) -> (float64[n, 18], int16[n, 18])` looks rows up and raises `KeyError` for an uncached history. Its output is bitwise equal to `se.qstar("NA", tokens, t)` (a test). `cache.save(path)` / `QStarCache.load(path, sha256)` (npz: `keys` `<U64` hex of `sha256(bytes(tok[:t]) + int(t).to_bytes(2, "little"))`, `q`, `codes`). Built once in K0 over D (all families and sets) and the fresh variants; used by B1 and Stage C.

## 6. x6zc_core: synthetic and analytic predictors (K1, K3, dry run)

- `member_of(history) -> str`: `"a"` if the first seam crossing of the segment after the last cue is an x crossing, `"b"` if it is a y crossing; `ValueError` if the segment has fewer than two crossings.
- `class SyntheticPredictor(kind, **params)`: `__call__(tokens, t) -> float64[n, 18]` (float of `exact`), `exact(history) -> tuple[Fraction] * 18`, `name = f"{kind}{sorted params}"`. Laws (all built from exact q* laws of the history; `Z = sp.q_exact("ZC", h, t)`, `N = sp.q_exact("NA", h, t)`, `M_k = missed_law(h, k)`, member m = `member_of(h)`):
  - `"M0"(w)`: (1 − w)·Z + w·N.
  - `"M1"(kappa_a, kappa_b)`: Z with the cue entries replaced by `P_cue · ((1 − κ_m)/3 + κ_m·δ_z)`, z the ZC answer (point-law excess κ; §3.1 M1).
  - `"M2a"(pi_a, pi_b)`: (1 − π_m)·Z + π_m·M_miss1; `"M2b"`: the same with M_miss2.
  - `"M4"(pi, seam, member)`: in the given member only, the crossing of seam `"x"` or `"y"` is missed with rate π: (1 − π)·Z + π·M_k with k the order index of that seam's crossing; the other member is Z.
  - `"M6"(pi_a, pi_b)`: (1 − π_m)·Z + π_m·M_miss_both.
  - `"M0+M2a"(w, pi_a, pi_b)`: (1 − w − π_m)·Z + w·N + π_m·M_miss1 (the additive composite of the PARTIAL fixture: exact r_MM = 1/2, r_PM = 7/8, r_MP = 5/8 at w = 3/20, π = (0, 1/20)).
  - `"W1_token_identity"(eps)` (recorded K3 known case, W1 only): Z with the cue law (cue-normalised) shifted by +ε·(δ_y − ⅓·1) if vertex 3 is visited in the segment and by −ε·(δ_y − ⅓·1) if vertex 12 is visited (net; a member visiting both gets no shift); the cue mass is unchanged.
  - `"set_constant"`: cue entries 1/15 each (cue mass 1/5, cue law ⅓), vertex tokens 0..14 equal (4/75 each).
  - `"matched_key"`: K = `int(sha256(canonical_json([list(prefix), y, n, v, list(parikh)])).hexdigest()[:8], 16) % 1000` from `xm.parse` (prefix, y, n, end vertex v) and `xm.parikh(segment)`; cue mass m_K = (1 + K mod 7)/10; cue entries m_K·(K + 1 + z)/(3K + 6) for z = 0, 1, 2; the rest (1 − m_K)/15 on each vertex token.
  - `"mixture"(S, delta)`: (1 − δ)·`sp.q_stat(S, h, t)` + δ·N (DR16).
- `oracle(arm, kind) -> se.OraclePredictor` (unchanged reuse; `kind ∈ se.ORACLE_KINDS`).
- `sym_arrays(p_a, p_b) -> tuple[float64[n, 18], float64[n, 18]]` = both `(p_a + p_b) / 2` (sym(m), built from Stage-B readouts).

## 7. x6zc_core: pair terms and the K1, K2, K3/F1 checks

- `pair_arrays(pred, arrays, key, qstar_fn) -> dict`: `p_a = pred(arrays[key+"_a"], t)`, `p_b` likewise, `q_a, codes_a = qstar_fn(arrays[key+"_a"], t)`, `q_b, codes_b`; `num, den = se.pair_terms(p_a, p_b, q_a, q_b)`; raises `ValueError` if the `_a`, `_b`, `_t`, `_y` arrays differ in length (a mismatched join); keys `"p_a"`, `"p_b"`, `"q_a"`, `"q_b"`, `"codes_a"`, `"codes_b"`, `"num"`, `"den"`, `"y"`, `"t"`, `"cluster"` (`arrays["prefix"]` if present, else `d_cluster(n)`). `qstar_fn(tokens, t) -> (q, codes)` (a `QStarCache` or `lambda tk, t: se.qstar("NA", tk, t)`).
- `pair_stats(terms) -> dict`: `"beta"` = `se.beta_fsum(num, den)`; `"beta_y"` = per cue y ∈ {0, 1, 2}; `"rho"` (§2); `"max_pair_diff"` = max over pairs of ‖c_a − c_b‖∞ (cue-normalised p̂); `"nonfinite"`.
- `k1_check(terms) -> dict` `{"status", "beta", "rho", "num_zero", "beta_exact_zero"}`: PASS iff `beta == 0.0` and `rho == 0.0` as floats, every `num[i] == 0.0`, and `se.beta_exact(num, den) == 0`.
- `K1_PREDICTORS`: `oracle("ZC", "qstar")`, `oracle("AB", "qstar")`, `oracle("NA", k)` for k ∈ (q_empty, q_parity, q_counts, q_H1, q_Parikh), `SyntheticPredictor("set_constant")`, `SyntheticPredictor("matched_key")`, `oracle("NA", "q_8")` (W2 and its variants only), and sym(m) for m ∈ FOCAL (array level, Stage B).
- `k2_check(terms_by_ref: dict, family) -> dict`: references `"qstar"` (|β − 1| ≤ 1e-12 pooled and per cue), `"h_last"` (per cue (½, −1, ½), pooled |β| ≤ 1e-12), `"h_first"` (per cue (−½, 1, −½)), `"h_rev"` (pooled −1), all within 1e-12; returns `{"status", "values": {ref: {"beta", "beta_y"}}, "failed": [ref]}`. Runs on D's W2 and W1 and on the fresh PP of both families. `k2_exact_variants(family) -> dict`: the exact pooled and per-cue β of `h_last`, `h_first`, `h_rev` on MM, PM, MP on Π0 (`Fraction`; recorded, not gated).
- `beta_exact_pi0(law_fn, family, variant) -> Fraction`: Σ_y⟨Δp_c, Δq*_NA,c⟩ / Σ_y‖Δq*_NA,c‖² over y ∈ {0, 1, 2} on prefix Π0 = (), exact (`law_fn(history) -> tuple[Fraction] * 18`, cue normalisation in Fractions).
- `k3_grid() -> list[tuple[str, dict]]`: M0 (w ∈ {1/20, 1/5}); M1, M2a, M2b, M6 with (a, b) ∈ {(1/20, 1/5), (1/5, 1/20)}; M4 with π ∈ {1/20, 1/5} × seam ∈ {x, y} × member ∈ {a, b}; in this order.
- `k3_exact(family) -> dict` `{mech_id: {"kind", "params", "beta": {v: Fraction}, "r": {v: Fraction | None}}}` with `mech_id = f"{kind}|{params}"`; r_v = β_v/β_PP (None when β_PP = 0).
- `k3_float_check(family, arrays, qstar_fn) -> dict`: every K3 predictor through `pair_arrays` on the fresh variant arrays; `|β_v(float) − float(β_v(exact))| ≤ 1e-12` for every v.
- `f1(k3) -> dict` (per family): `"m0_ok"` (every M0 r_v == 1), for each sign-symmetric mechanism kind (M1, M2a, M2b, M4, M6): `"far"` (some r_v with |r_v − 1| ≥ 1) and `"r_mm_minus_one"` (r_MM == −1 exactly) over all its grid entries; `"passed"` (all true), `"failed"` (kinds failing, K3 order). F1 failure for a kind → NOT_DISCRIMINABLE(<kinds>) for that family, recorded before Stage B.

## 8. x6zc_core: bootstrap, ratios, B9 sizing (§5, §7 B5, B9, §8)

- `cluster_sums(values, cluster, P) -> float64[P]`: `math.fsum` of `values[cluster == i]` for i = 0..P−1.
- `paired_cluster_boot(num: dict[str, float64[P]], den: dict[str, float64[P]], B, gen) -> dict[str, float64[B]]`: for each draw b: one call `idx = gen.integers(0, P, size=P)`; for each key: `num[key][idx].sum() / den[key][idx].sum()` (numpy sum, the `ss.boot_beta` rule; a zero denominator gives NaN). One index array per draw serves every key (predictor × family × variant × statistic). With a single key it equals `ss.boot_beta(num, den, B, gen)` bitwise for an identically seeded `gen`. Keys are strings `"<model>|<family>|<variant>|<stat>"` with stat ∈ {`beta`, `beta_y0`, `beta_y1`, `beta_y2`, `rho`}; for `rho`, num = Σ‖Δp̂_c‖², den = Σ‖Δq*_c‖² per cluster.
- `interval(draws, q) -> tuple[float, float]` = `(ss.quantile(d, q[0]), ss.quantile(d, q[1]))`; raises `ValueError` if any draw is non-finite (§18 C-21).
- `ratio_interval(draws_v, draws_pp, sign, q) -> dict` `{"lo", "hi", "n_defined", "undefined", "undefined_frac"}`: a draw is defined iff `sign · draws_pp > 0`; ratios `draws_v / draws_pp` over defined draws only; quantiles by `ss.quantile`.
- `cell_statistics(point, draws, cell) -> dict` for `cell ∈ CELL_ORDER`, with `point[(model, family, variant)] = β_v` (fresh) and `draws` keyed as above: `"b"` = σ·β_PP, `"b_lo"`, `"b_hi"` (interval of σ·β_PP* at `b_q`), `"beta_pp"`, `"r"` = `{v: {"point": β_v/β_PP, "lo", "hi"}}` for v ∈ (MM, PM, MP) at `r_q`, `"undefined_frac"` (the largest of the three; the undefined set is the same for all three since it depends on β_PP* only), `"beta_sb"` = `{"point": ½(β_PP + β_MM), "lo", "hi"}` (95 %), and for cell P `"r_w1_p"` = `{"point", "lo", "hi", "undefined_frac", "label": "W2_ONLY" | "NA_BOTH_FAMILIES" | None}` (95 %; W2_ONLY iff hi < 1/2; NA_BOTH_FAMILIES iff 1/2 < lo and hi < 3/2; None if undefined_frac > 1/100).
- `halfwidth(n, se_d, beta_d, z) -> float` = `z·√2·se_d·√(1030/n) / max(|beta_d| − 2·se_d, 0.05)`.
- `choose_n(n_avail, se: dict[cell, float]) -> dict` `{"n", "status": "OK" | "UNDERPOWERED" | "NOT_ENOUGH_DATA", "candidates", "h": {cell: {str(n): float}}, "underpowered": {cell: bool}, "low_feasibility": ["S3"]}`: if `n_avail < 512`: NOT_ENOUGH_DATA, n = n_avail, every cell underpowered = False (R4a precedes); else candidates = sorted({1024, 2048, n_avail} ∩ [512, n_avail]) (only `n_avail` when 512 ≤ n_avail < 1024); n = the smallest candidate with h_P(n) ≤ 1/4; if none, status UNDERPOWERED, n = n_avail, underpowered P = True; S3, S4 underpowered iff h_S(n) > 1/4 at the chosen n. `se[cell]` = `np.std(draws, ddof=1)` of the B5 draws of the cell's β on D.

## 9. x6zc_core: decision (§9), qualifiers, licences, reuse verdict

### 9.1 Evidence record `ev` (input of `decide_x6zc`)
```
{"k0": "PASS"|"FAIL",
 "incomplete": bool,                         # G-R1: a stage did not complete after its G2 rerun
 "checks": {"A1", "A2", "A_audit", "K2", "K5": "PASS"|"FAIL"|"DEFECT_CANDIDATE"|"NOT_RUN",
            "K4": "PASS"|"ENV_DRIFT"|"DEFECT_CANDIDATE"|"NOT_RUN"},
 "rulings": [{"id": str, "check": str, "cause_identified": bool, "affects_beta": bool, "cause": str}],
 "k1": "PASS"|"FAIL", "a2_k5_pass": bool,
 "n_avail": int, "b9": <choose_n output>, "k6": {"W2": bool, "W1": bool},
 "f1": {"W2": <f1 output>, "W1": <f1 output>},
 "cells": {cell: <cell_statistics output> | None}}
```
A check with status DEFECT_CANDIDATE (or FAIL) needs a ruling (§11.2 `rulings/`) before `decide_x6zc` runs; a missing ruling raises `ValueError`.

### 9.2 `decide_x6zc(ev) -> dict`
Global rules, first match wins (G-R0 first):
1. **G-R0** `ev["k0"] == "FAIL"` → `"STOP_REPLAN"`.
2. **G-R1** `ev["incomplete"]` → `"INVALID"`.
3. **G-R2** a failed check among A1, A2, A_audit, K2, K4 (DEFECT_CANDIDATE), K5 with a ruling `cause_identified and affects_beta` → `"DEFECT_FOUND"`.
4. **G-R2′** a failed check with a ruling `not cause_identified` → `"UNEXPLAINED/IRREPRODUCIBLE"`.
5. **G-R3** `ev["k1"] == "FAIL"` and `ev["a2_k5_pass"]` → `"ESTIMATOR_ARTIFACT/NON_INVARIANT"`.
A ruling `cause_identified and not affects_beta` adds the qualifier `DEFECT_ELSEWHERE(<id>)` and does not pre-empt. A global outcome applies to every cell. Otherwise, per cell c ∈ CELL_ORDER with family F, statistics s and r-band (1/2, 3/2), first match wins:

| Rule | Condition (strict as written) | Cell P | Cells S3, S4 |
|---|---|---|---|
| R4a | `ev["b9"]["status"] == "NOT_ENOUGH_DATA"` | UNEXPLAINED/NOT_ENOUGH_DATA | same |
| R4b | `ev["b9"]["underpowered"][c]` | UNEXPLAINED/UNDERPOWERED | same |
| R5 | `not ev["k6"][F]` | UNEXPLAINED/FRESH_SET_UNSTABLE | same |
| R6 | `s.b_hi < 1/10 and s.b_lo <= 0` | ZC_NOT_COMMUTATIVE/NOT_REPLICATED | same |
| R7 | `s.b < 1/10 or s.b_lo <= 1/20` | UNEXPLAINED/WEAK_REPLICATION (licence `positive` iff `s.b_lo > 0 and s.b < 1/10`, else `ambiguous`) | same |
| R7b | `s.undefined_frac > 1/100` | UNEXPLAINED/UNSTABLE_RATIO | same |
| R8 | `s.r["MM"].hi < 0` | ZC_NOT_COMMUTATIVE/ZC_COORDINATE | ZC_NOT_COMMUTATIVE/NOT_NA_DIRECTION |
| R8b | some v: `s.r[v].hi < 1/2 or s.r[v].lo > 3/2` | UNEXPLAINED/NOT_NA_INVARIANT | same |
| R9 | `ev["f1"][F]["passed"]` and every v: `1/2 < s.r[v].lo and s.r[v].hi < 3/2` | ZC_NOT_COMMUTATIVE/NA_DIRECTION | same |
| R9′ | the R9 interval pattern and F1 failed | UNEXPLAINED/NOT_DISCRIMINABLE(<kinds>) | same |
| R10 | otherwise | UNEXPLAINED/PARTIAL | same |

Returns `{"global_rule": str | None, "global_outcome": str | None, "cells": {c: {"rule", "outcome", "licence_case": None | "positive" | "ambiguous", "descriptive": bool}}, "headline": <cell P outcome or the global outcome>, "defect_elsewhere": [id]}`. `"descriptive"` is True for R4a and R4b (Stage C ran descriptively). `<kinds>` = the failed kinds joined by `", "` in K3 order. Floats are compared with the float value of the bar as written (`x <= float(Fraction("1/20"))`; §20 E-1); a ratio interval that is undefined (`None`) never fires R8, R8b, R9 or R9′ (§20 E-2).

### 9.3 Licences
`licence(outcome, values, case=None) -> str`: the template `CONTRACT["licences"][key]` (key = outcome, `outcome + ":" + case` for WEAK_REPLICATION, `"UNEXPLAINED/*"` for the generic UNEXPLAINED rows, including NOT_DISCRIMINABLE, IRREPRODUCIBLE, UNSTABLE_RATIO, FRESH_SET_UNSTABLE, NOT_ENOUGH_DATA, UNDERPOWERED) filled with `str.format(**values)`; NA_DIRECTION on S3/S4 appends the `":W1_suffix"` text. Placeholders: `model`, `family`, `n`, `beta_d3` (β_D to 3 decimals), `b_label` (`"β_PP"` if σ = +1, `"−β_PP"` if σ = −1), `b`, `beta_pp`, `lo`, `hi`, `level` (`"95"` or `"97.5"`), `k`, `exceptions` (`""` or `"; exception: <names>"`), `r_mm`, `r_pm`, `r_mp`, `r_values`, `intervals`, `upper` (hi(r) × β_PP for the largest hi), `predictor`, `value`, `defect`, `corrected`, `outcome`, `descriptive` (`" (descriptive)"` or `""`), `numbers`. Numbers are formatted with 4 decimals; intervals as `[lo, hi]`. STOP_REPLAN and INVALID give `""`. `not_licensed(outcome) -> str` = `CONTRACT["not_licensed"]`. Every report also carries `CONTRACT["x6s1_statement"]` (§9.2 sentences) unchanged; a sentence about NA-s1's own designed numbers (β_W2 = 0.088 < 0.25; R_W2 = 0.0797 > 0.0458) may be added only with "the flag remains UNRESOLVED".

### 9.4 Qualifiers
`qualifiers(ev, decision, census) -> dict[cell, list[str]]`, in this order:
- every ZC_NOT_COMMUTATIVE outcome: `"ORIGIN_UNRESOLVED"`; the Stage-B qualifiers that fired for the cell's (model, family): `"READOUT_AMPLIFIED(<model>, <F>)"`, `"MULTIPLICITY_SENSITIVE(<model>, <F>)"`, `"LENGTH_WEIGHT_SENSITIVE(<model>, <F>)"`, `"PRECISION_SENSITIVE(<model>, <F>)"`; for cell P `"W2_ONLY"` or `"NA_BOTH_FAMILIES"` when labelled; `"SENSITIVITY_A4(<outcome>)"`, `"SENSITIVITY_D_PREFIX(<outcome>)"` when the sensitivity recomputation (§11.4) gives a different outcome;
- every cell: `"LOW_FEASIBILITY(S3)"` on S3; `"UNDERPOWERED(<cell>)"` when flagged; `"ENV_DRIFT"` when K4 was ENV_DRIFT; `"NUMERIC_DRIFT(<model>, <F>)"` from K5a; `"DEFECT_ELSEWHERE(<id>)"` per ruling; `"DESCRIPTIVE"` for R4a/R4b.

### 9.5 Reuse verdict (§9.4 of the protocol)
`reuse_verdict(ev, decision) -> dict` `{"axis1", "axis2", "amendments": [int], "amendment_1_mark": str | None, "statement": str | None}`:
- axis 1: `"NOT_FIT"` if the global outcome is DEFECT_FOUND or ESTIMATOR_ARTIFACT/NON_INVARIANT; `"UNDETERMINED"` if UNEXPLAINED/IRREPRODUCIBLE, INVALID or STOP_REPLAN; else `"VALID"` (A1, A2, A-audit, K0–K2, K5 PASS and K4 PASS or ENV_DRIFT; DEFECT_ELSEWHERE does not change it: §18 C-18).
- axis 2 (only if VALID, else `"NOT_ASSESSED"`): `"UNDETERMINED"` if cell P is ZC_NOT_COMMUTATIVE/NA_DIRECTION (takes precedence); else `"FIT_WITH_AMENDMENT"` (K0 confirmed the coupling for W1 and W2: K0 PASS).
- amendments: the union over cells P, S3, S4 of `CONTRACT["reuse"]["by_outcome"]` (ZC_COORDINATE or NOT_NA_DIRECTION → 1–4; NOT_NA_INVARIANT, NOT_REPLICATED, WEAK_REPLICATION, PARTIAL and every other UNEXPLAINED → 1–3; NA_DIRECTION → 2–3), sorted; for axis 2 UNDETERMINED the list is at least [2, 3]. `amendment_1_mark` = `CONTRACT["reuse"]["amendment_1_inconclusive_mark"]` iff 1 is listed and the headline is UNEXPLAINED/PARTIAL or a generic UNEXPLAINED outcome (not NOT_NA_INVARIANT or WEAK_REPLICATION).
- `statement` = `CONTRACT["reuse"]["statement"]` in every VALID case, else None.

## 10. x6zc_census (descriptive and independent checks)

- `audit_pairs(D_arrays, family, n_prefixes=1030) -> dict` (A-audit; content-based identity, never row position): for every W2 and W1 pair: both histories legal (`xm.parse`), stored t equals the unpadded length (last non-zero token position; padding all zero), same prefix before the cue, same cue and cue position, same n, end vertex and directed seam-crossing counts, member a crosses x first (`zc.member_of`); W2: token bag, directed-bigram bag and last 8 tokens equal; W1: last 4 tokens equal and bags differ in exactly vertex tokens of 3 vs 12; all three cues present for each prefix entry (rows 3i..3i+2 share the prefix and have y = 0, 1, 2); counts 3,090 pairs and 1,030 prefixes. Control families C1–C4: legality, same prefix and cue, t (recorded). Returns `{"status": "PASS" | "DEFECT_CANDIDATE", "counts", "counterexample"}` (smallest row).
- `exposure_matches(hist, t, pool_tokens) -> bool[n]` (A4): `hist[i, :t[i]]` equals `row[:t[i]]` byte for byte for some pool row, bucketed by t (one set of row-prefix bytes per distinct t). `exposure_report(variant_arrays_by_family, pools: dict[name, uint8[m, 33]]) -> dict` `{"matches": {family: {variant: {member: int}}}, "pair_mask": {family: {variant: bool[n]}} (a pair is matched if either member matched in any pool), "total": int}`.
- `k4_compare(stored: dict, got: dict) -> dict` (B1): keys of §7 B1 (`beta_W2`, `beta_W2_y`, `R_W2`, `Delta_W3`, `rho_C`, `rho_W2`, `cue_mass_median`, `beta_W1`, `beta_W3`, `beta_W3_bal`, `beta_W3p`, `nonfinite`); `"PASS"` if every float is equal (lists elementwise) and `nonfinite` equal; `"ENV_DRIFT"` if not, but every relative difference `|g − s| / max(|g|, |s|)` (0 when both are 0) ≤ 1e-9 and `nonfinite` equal; else `"DEFECT_CANDIDATE"`. Returns `{"tier", "max_rel", "keys": {key: rel}}`.
- K5 (B2), each returning `{"status", ...values}`:
  - `k5_independent(terms, beta_prod) -> dict` (a): pairs rebuilt from content (prefix tokens, cue, member by `zc.member_of`); p̂ and q* converted to exact Fractions; independent cue normalisation and pair terms; exact aggregation; `|float(β_exact) − beta_prod|` ≤ 1e-12 PASS, ∈ (1e-12, 1e-9] NUMERIC_DRIFT, > 1e-9 DEFECT_CANDIDATE; also `xe.beta` on rows (pair id, 1, q_c(member), p_c(member)) for both members (within-pair centring) must give the same Fraction.
  - `k5_swap(terms) -> dict` (b): `pair_terms(p_b, p_a, q_b, q_a)` num `==` num elementwise; `pair_terms(p_b, p_a, q_a, q_b)` num `== −num`.
  - `k5_padding(pred, tok, t) -> dict` (c): re-pad after t with token 5; max-abs difference of p̂ at t ≤ 1e-13.
  - `k5_batch(pred, tok, t) -> dict` (d): one row at a time vs the batched call ≤ 1e-12.
  - `k5_readout_index(pred, arrays, family) -> dict` (e): W2: median p̂ cue mass at t ∈ [3/20, 1/4], median at t − 1 ≤ 1/100, q*_NA cue mass at t − 1 exactly 0; W1: the two t − 1 conditions (§18 C-9).
  - `k5_two_loads(pred1, pred2, tok, t)` (g) ≤ 1e-12; `k5_scalar_vector(pred, tok, t)` (h): per-row scalar t vs vector t ≤ 1e-12; `k5_permutation(terms, gen)` (i): one joint row permutation (`zc.stream("perm_K5i").permutation(n)`) and its restoration leave β, ρ and per-cue β exactly equal; `k5_bos(model, tok, t)` (j): `[18] + tok[:32]` built independently, logits at index t, softmax, ≤ 1e-12 against `se.ModelPredictor._run`.
  - `structural_subset(t, y) -> int64[]`: the first pair row in each observed (t, y) cell, from metadata only (items g–j).
- `decompose(terms) -> dict` (B3): per pair d = Δq*_c, n_a = argmax d, n_b = argmin d, w the third cue; e₁ = (δ_{n_a} − δ_{n_b})/√2, e₂ = (2δ_w − δ_{n_a} − δ_{n_b})/√6; `"cos_agg"` = β/√ρ, `"beta2_over_rho"`, `"phi1"` = Σ(Δp̂·e₁)²/Σ‖Δp̂‖², `"e1_mean"`, `"e1_sd"`, `"e2_mean"`, `"e2_sd"` (ddof 1), `"frac_pos"` (⟨Δp̂, Δq*⟩ > 0), `"diff_quantiles"` (levels 0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1 of the per-pair max-abs full-vocabulary and cue-normalised differences), `"num_by_prefix"` (`float64[P]`), `"num_by_cue"` (3 floats).
- `zc_profile(terms, tables, arm) -> dict` (B4): per member and k ∈ {0, 1, 2}: mean cue-normalised p̂ share on g_k·y with g = (e, c, c²) for arms NA and ZC and (e, a, a·… third cue) for AB (`"own"`: shares on y, a·y and the remaining cue); per member own-arm regret = mean of `se.score(codes_arm, se.quantise(p), tables)` with `codes_arm` from `se.qstar(arm, tok, t)` (ZC for ZC models, AB for AB, NA for NA and inits).
- `d2_decompose(terms) -> dict` (D2): per pair m_a, m_b, m̄; term1 = (p_{a,c} − p_{b,c})/m̄, term2 = −(m_a − m_b)/(2m̄)·(c_a + c_b); contributions ⟨term_k, d_i⟩; `"identity_max_abs"` = max_i |⟨term1 + term2, d_i⟩ − num_i| (must be ≤ 1e-12); `"beta_fixed"` = Σ⟨5(p_{a,c} − p_{b,c}), d_i⟩/Σ‖d_i‖²; cue-mass `"min"`, `"median"`, `"p01"`, `"p05"`, `"p10"`, `"frac_below_0.10"` over both members; `"readout_amplified"` = |β − β_fixed| ≥ 1/20 and `crosses(β, β_fixed)`.
- `crosses(x, y, bar=1/10, band=1e-9) -> bool`: |x| and |y| lie on opposite sides of the bar outside [bar − band, bar + band] (§18 C-8).
- `weighting_summaries(terms, prefixes, named_mask) -> dict` (D3): β for the 6 named vs the 1,024 natural prefixes; per prefix length and for the bins {1–4, 5–9, 10–14}; four consecutive blocks of 256 natural prefixes; `"beta_distinct"` (weights 1/|group| by token-prefix string); `"beta_length"` (weights 1/count by prefix length); leave-one-distinct-prefix-out β (min, max, argmin, argmax); top-5 % prefix and top-10 % distinct-group shares of Σ|num| (per-prefix Σ|num_i|, ceil of the fraction); group multiplicities; `"multiplicity_sensitive"` and `"length_weight_sensitive"` = |β − β_alt| ≥ 1/20 and `crosses(β, β_alt)`.
- `similarity(dp: dict[model, float64[n, 3]]) -> dict` (B6): `{"models": [...], "cos": float[16][16]}` of the flattened stacked cue-normalised Δp̂ per family.
- `control_families(stats_by_family) -> dict` (B7): ρ per control family C1–C4 (denominator W2's mean‖Δq*‖²), per-cue β_W1,y and ρ_W1, β_W3, β_W3_bal, β_W3p (from `designed_stats`).
- `float32_replay(beta32, beta64) -> dict` (B10): `{"diff", "precision_sensitive": |β₃₂ − β₆₄| > 1e-5}`.
- `descriptive_tier(model, family, k4_tier, k1_ok, k5_ok, max_pair_diff, flags, betas) -> dict`: `CENSUS_NON_INVARIANT(<model>, <F>)` iff k4 ∈ {PASS, ENV_DRIFT}, K1 and K5 pass and `max_pair_diff > 1e-9`; qualifiers: READOUT_AMPLIFIED, MULTIPLICITY_SENSITIVE, LENGTH_WEIGHT_SENSITIVE, PRECISION_SENSITIVE where fired; `"ORIGIN_UNRESOLVED"` always; `"BAG_UNMATCHED"` on W1; `"FAMILY_PATTERN(beta_W1=<x>, beta_W2=<y>)"` (4 decimals). Trained controls only (AB-s1..s4, ZC-s1..s4). Never changes the registered tier.

## 11. x6zc_run

### 11.1 Store layout (`X:/Downloads/projects/topo-pilot/x6zc-store/`)
`FREEZE.json`, `AUTH.json`, `cpu_ledger.json` (meter-maintained), `x6zc_meter_bind.py`, `STAGES.jsonl` (one line per stage record: `{"stage", "record_sha256", "stop", "utc"}`), `EXPOSURE.jsonl`, `EVALUATIONS.jsonl`, `rulings/<id>.json`, `stages/0/record.json`, `stages/A/` (`record.json`, `qstar_NA.npz`, `x6s1_inventory_before.json`, `x6s1_inventory_after.json`), `stages/B/<model>/` (`designed.json`, `pairs.npz`, `chunk.json`) and `stages/B/record.json`, `stages/C/<model>/` (`variants.npz`, `chunk.json`) and `stages/C/record.json`, `report.json`, `logs/`. Every file is written by exclusive create (`xwrite(path, data: bytes) -> str` returns the sha256; `FileExistsError` on an existing file); the JSONL files are append-only. A G2 rerun of stage S writes under `stages/<S>-r1/` and leaves the first attempt in place (its `STAGES.jsonl` line carries the stop).

### 11.2 Records
- `EXPOSURE.jsonl`: line 1 is `CONTRACT["store"]["exposure_first"]` plus `"utc"` (id `E0-PREFIX-READ`), written at the start of Stage A if the file is absent. Every later line is written **before** the payload is opened: `{"id": "X<k>", "stage", "store": "x6-stage1-store", "artifact": <store-relative path>, "expected_sha256": <recorded hash> | None, "purpose": <item>, "utc"}`. `log_exposure(store, stage, artifact, expected_sha256, purpose) -> dict`.
- `EVALUATIONS.jsonl`: `{"model", "kind", "stage", "set": "D" | "fresh", "utc"}`, written before any model evaluation (`log_evaluation(store, model, kind, stage, set_name)`). Kinds: `"designed_D"` (B1), `"k5"`, `"b8_emergence"`, `"b10_float32"`, `"fresh_variants"` (Stage C). `guard(stage, set_name)` raises `RuntimeError` for a model evaluation with `set_name == "fresh"` outside Stage C; a fresh-set model entry before Stage C is a setup error.
- Stage record `stages/<S>/record.json`: `{"stage", "head", "env_local", "env_diff", "inventory": {"before_sha256", "after_sha256", "equal"}, "gates": {item: {"status", "values"}}, "values": {...}, "cpu_s", "cpu_cumulative_s", "pause": <pause_check output>, "stop": None | str, "utc"}`; `write_stage(store, stage, record) -> Path` writes it and appends `STAGES.jsonl`.
- `rulings/<id>.json` (coordinator, by CLI `ruling`): `{"id", "check", "stage", "cause_identified": bool, "affects_beta": bool, "cause", "defect_md": <mailbox path> | None, "utc"}`; also used for IRREPRODUCIBLE (cause_identified false) and setup errors (`"setup": true`, then the stage restarts under G2).

### 11.3 Guards and environment
- `x6s1_inventory(store=X6S1_STORE) -> dict[str, list[int]]`: relative POSIX path → `[size, mtime_ns]` for every file, by `os.walk` with the `sealed` directory pruned (its contents are never listed); the `sealed` directory itself is recorded as `"sealed/"` → `[0, st_mtime_ns of the directory]`. Taken before and after each stage; `inventory_equal(a, b) -> bool`; a difference is a setup error (the stage-1 store is read-only).
- `env_check(env) -> dict` `{"status": "PASS" | "SETUP_ERROR", "changed": [keys]}`: `sr.env_changed(env, ref)` with `ref` = `env_local` of `x6-stage1-store/stages/E3w5/ZC-s1/chunk.json`; PASS iff the changed keys ⊆ {"commit"}.
- `closure_diff(worktree) -> list[str]`: `git diff --name-status <H3> HEAD -- <CLOSURE>` lines; non-empty → setup error (A1 item 6).
- `master_fresh(project_root=PROJECT_ROOT, master=X6ZC_MASTER) -> dict` `{"fresh": bool, "hits": [path]}`: every `meta.json` under every `*store*` directory of the project root, by `os.walk` with `sealed`, `.git` and `.venv` pruned, whose `seed_map` or `config` holds the integer `master` (the `sr.seed_fresh` hit rule), plus the X6S1 masters 2026101861/2026101862 compared by value. Checked before the freeze.
- `meter_bind_check(path, expected_sha256, import_dir) -> None` (the `sr.meter_bind_check` pattern bound to `WORKTREE`): raises `RuntimeError` if the file sha256 differs or `import_dir` is not `METER_IMPORT_DIR`.
- `ledger_cpu(store) -> float`: `cumulative_cpu_s` of `cpu_ledger.json`. `pause_check(boundary, cumulative_s, stage_s, n=None) -> dict` `{"pause": bool, "cumulative_threshold", "stage_threshold"}` with thresholds of `CONTRACT["budget"]["pause"]` (boundary `"0"`, `"A"`, `"B"`, `"C"`; for C: n = 1024 → C_1024, n = 2048 → C_2048, any other n → 19,980 + 9.4921875·n and 9.4921875·n); pause iff measured > threshold (either). A pause is recorded in the stage record and the run stops at the boundary for the coordinator's plain-language report.

### 11.4 Stages and gate order
Every stage: meter binding check → `env_check` → `closure_diff` → inventory before → items → inventory after → record. A setup error stops the stage before any further payload is opened (§9.1 setup paragraph); the coordinator corrects it and restarts under G2.
- **Stage 0 (dry run, before the freeze; §12):** `dry(scratch=DRY_STORE)` builds the synthetic store and runs every `CONTRACT["dry_run"]["fixtures"]` item (§15) through the pipeline (input manifest → construction validation → predictor adapter → raw outputs → production statistics → independent reference → decision → report); writes `<scratch>/report.json` with `{"fixtures": [{"id", "expected", "got", "pass"}], "all_pass", "cpu_per_history_s"}`; fault injection (`faults` argument) is accepted only when the store path is under `SCRATCH_ROOT`. The stage-0 record in `x6zc-store/stages/0/` carries the dry-run report sha256 and the stage-0 CPU.
- **Stage A** (blind; no model output): A1 (items 1–6; item 6 first, before any payload) → A2 (the §17 table: every anchor string found in its cited line range at HEAD) → A-audit (reads `tables/designed.npz`, sha-checked against CONTRACT, logged) → A3 (`pre.load_obs(X6S1_STORE, "prefix")`, logged; `fresh_prefixes`) → K0 on D (W2, W1, controls) and on all N_avail fresh prefixes of both families (G-R0: a failure stops at once) → q*_NA cache saved → K1 (D W2/W1 and fresh variants; sym deferred to B) → K2 → K3, F1 → A4 (7 train pools, logged). Gate stops: K0 FAIL → stop (`stop: "STOP_REPLAN"`); every other failure is recorded and the stage continues (§18 C-17).
- **Stage B** (models on D only, known cases first): per model in `STAGE_B_ORDER`, one child (`chunk` CLI; ≤ 3 children; `sr.limits`, `sr.launch`, `sr.supervise`) computes `designed_stats` with the q*_NA cache and saves p arrays; parent: B1/K4 per model → B2/K5 (K5_MODELS, W2 and W1) → K1 of sym(m) → B3, B4, B5 (stream `boot_B`), D2, D3, B6, B7, B10 → descriptive tier → B9 (`choose_n`) → B8 only if G3 holds (Stage-B CPU to date ≤ 2,880 s) → Stage-B gate (Stage C runs only if no global rule fired, apart from DEFECT_ELSEWHERE, and every DEFECT_CANDIDATE has a ruling).
- **Stage C** (registered, once): the first n fresh prefixes (yield order) → `variant_arrays` for W2 and W1 → per predictor (16 models, q*_NA float reference, K3 synthetic predictors) one child writing `variants.npz` (p arrays, no statistic) → after **every** chunk completed: pair terms, β_v, ρ_v, per-cue β, B3/B4 summaries → K6 → bootstrap (stream `boot_C`, 5,000 draws, all keys) → `cell_statistics` → sensitivity lines (A4-matched pairs removed, stream `sens_A4`; D-coincident clusters removed, stream `sens_DPREFIX`) → `decide_x6zc` → report. G2: a failed chunk may be rerun once unchanged while no Stage-C statistic exists; afterwards a failure gives INVALID.

**Pure pipeline functions** (no I/O; shared by Stage C, the sensitivity lines and the dry run):
- `predict_variants(pred, arrays_by_family) -> dict[family, dict[variant, tuple[p_a, p_b]]]` (float64[n, 18] each).
- `stage_c_statistics(outputs: dict[name, <predict_variants output>], arrays_by_family, qstar_fn, gen, drop_pairs=None, drop_clusters=None) -> dict` with keys `"point"` (`{(name, family, variant): β_v}`), `"beta_y"`, `"rho"`, `"draws"` (`paired_cluster_boot` over every key, `B_DRAWS` draws), `"cells"` (`{cell: zc.cell_statistics(...)}`; a cell whose model is absent from `outputs` is None), `"k6"` (`{"W2": bool, "W1": bool, "values": {...}}` from |β_PP| ≤ 1/10 of `K6_CONTROLS`, counted against `K6_MIN`), `"n_clusters"`. `drop_pairs` (`{family: {variant: bool[n]}}`) removes pairs; `drop_clusters` (`bool[P]`) removes clusters.
- `decide_report(stats, ev_base, census=None) -> dict`: completes `ev_base` with `k6` and `cells` from `stats`, calls `zc.decide_x6zc`, `zc.qualifiers`, `zc.licence` per cell and `zc.reuse_verdict`; returns `{"decision", "qualifiers", "licences", "reuse_verdict"}`.
- `dry(scratch=DRY_STORE, fixtures=None, faults=None) -> dict`: the stage-0 driver (§15); `fixtures` selects ids (default all); returns and writes the dry-run report.

### 11.5 CLI
`python -s tools/x6zc/x6zc_run.py <command> [--store PATH] [--job ID] [--dispatch PATH]` with commands `dry`, `A`, `B`, `C`, `report`, `chunk --stage {B,C} --model NAME --out DIR`, `ruling --id ID --check NAME --stage S --cause-identified {0,1} --affects-beta {0,1} --cause TEXT [--defect-md PATH] [--setup]`, `master-check`. `main(argv=None) -> int` (0 on success, 2 on a stop, 1 on an error).

### 11.6 Report (`report.json`, schema `"x6zc-report-v1"`)
Top-level keys (all required): `schema`, `protocol_id`, `protocol_sha256`, `head`, `x6zc_master`, `outcome` (headline), `global_rule`, `cells` (`{P, S3, S4: {"model", "family", "rule", "outcome", "licence", "not_licensed", "qualifiers", "b", "b_interval", "beta_pp", "r", "undefined_frac", "beta_sb", "n", "descriptive"}}`), `r_w1_p`, `k6`, `f1`, `k0`, `coupling`, `stage_b` (`{"k4", "k5", "descriptive_tier", "qualifiers", "b9"}`), `reuse_verdict`, `x6s1_statement`, `descriptive` (every predictor's β_v, r_v, ρ_v, per-cue β, B3/B4 on the variants, the four NA models' r_v printed beside cells S3/S4), `exposure` (`{"a4_matches", "d_coincident"}`), `sensitivity`, `follow_up` (the NA_DIRECTION provenance-audit note when it applies), `budget` (`{"cpu_s": {"0", "A", "B", "C"}, "pauses"}`), `n`, `n_avail`, `r_star`, `stages` (record sha256 per stage), `env`. `validate_report(report) -> list[str]` returns the schema errors (missing keys, an outcome string outside `CONTRACT["outcomes"]`, a licence present for STOP_REPLAN/INVALID).

## 12. FREEZE.json and AUTH.json (§15 steps 4–5)
- `FREEZE.json` (coordinator, at the execution freeze; fields `CONTRACT["store"]["freeze_fields"]`): `schema` `"x6zc-freeze-v1"`, `protocol_id` `"X6ZC-FROZEN-v1"`, `protocol_sha256` (of `X6ZC-FROZEN-v1.md` = `tools/x6zc/PROTOCOL_X6ZC_v1.md` at the freeze), `protocol_frozen` (mailbox path), `api_sha256`, `contract_sha256`, `test_plan_sha256`, `head` (implementation commit), `branch`, `worktree`, `modules` and `tests` (`{path: {"sha256", "git_blob", "lines"}}`), `x6zc_master`, `thresholds` (the §13 pause table of `CONTRACT["budget"]["pause"]`), `dry_run` (`{"report_sha256", "stage_records": {path: sha256}, "cpu_per_history_s", "calibration": None | {...}}`), `meter_bind_sha256`, `meter_import_dir`, `coordinator`, `created_utc`.
- `AUTH.json` (after owner AUTH (b)): `schema` `"x6zc-auth-v1"`, `protocol_sha256`, `freeze_sha256`, `owner_record` (`{"path", "sha256", "granted_utc"}`), `local_budget` (central 2.75 CPU-h at n = 1,024; 3.65 at n = 2,048), `pause_thresholds`, `cpu_policy` ("measure-only, --max-cpu inf"), `coordinator`, `written_utc`. Stages A–C refuse to start without both files and a protocol sha256 match.

## 13. Budget and pause points (§13; CONTRACT `budget`)
Anchor 6.4 ms per history (job 0098). Central CPU-s: stage 0 720, A 3,060, B 2,880, C 3,240·n/1,024; total 9,900 at n = 1,024, 13,140 at n = 2,048. 3× pause points (CPU-s, cumulative / per stage): after 0: 2,160 / 2,160; after A: 11,340 / 9,180; after B: 19,980 / 8,640; after C at n = 1,024: 29,700 / 9,720; at n = 2,048: 39,420 / 19,440; any other n (incl. NOT_ENOUGH_DATA, UNDERPOWERED): 19,980 + 9.4921875·n / 9.4921875·n. Frozen at the freeze; never reset. Calibration before the freeze only, and only if the dry-run CPU per history lies outside [0.5×, 2×] of the anchor (recorded in FREEZE `dry_run.calibration`). G1 = B9's n; G2 = one unchanged technical rerun per stage; G3 = B8 only if Stage-B CPU ≤ 2,880 s. No other growth.

## 14. Stored values reproduced in B1 (from the `designed.json` files bound in CONTRACT)
The 16 stored dicts are `CONTRACT["x6s1_store"]["stored_designed"][name]["values"]`, read from `stages/E3w<wave>/<name>/designed.json` (sha256 in CONTRACT, from `chunk.json` `files`; the chunk sha256 from `GATES.jsonl` E3.A). init-s1 is `stages/E3w1/init-s1` (the copy E3z consumed); `stages/E3r2/init-s1` and `stages/E3r5/init-s1` are not used. A1 item 2 calls `sdc.ord_d(na, init, ab, zc, dw2_lo)` with `dw2_lo = Fraction(CONTRACT["x6s1_store"]["dw2_lo"])` (E0 `G0-ORC.lo.Delta_W2`, the value E3z used): expected UNRESOLVED, control_limited True, reason `"designed placebo ZC"` for s = 1 and FAIL for s = 2, 3, 4.

## 15. Dry-run fixtures (§12; CONTRACT `dry_run.fixtures`)
Scratch store `X:/Downloads/topo-scratch/x6zc-dry/`; synthetic prefix pool of 4,096 rows of random legal torus walks (adjacency only; a cue token 15 + y with y uniform at every anchor visit) from `zc.dry_stream("pool")`; the short pool is that pool truncated after the row of its 1,280th yield (N_avail = 256); synthetic D = `sp.designed_set(<pool>)`; two random-init `TransformerLM(sd.MODEL_CFG)` states (`zc.dry_stream("model", k)` seeds) saved as fake checkpoints with fake admission locks (exercising the `ModelPredictor` sha checks, the stage runner, the meter path and the ledger), evaluated on the first 64 prefixes of the synthetic D and on n = 128 fresh synthetic prefixes; analytic and planted predictors use full sizes. Expected results:

| Id | Fixture | Expected |
|---|---|---|
| DR01 | r_PM interval above 1.5 with r_MM ≈ 1 | UNEXPLAINED/NOT_NA_INVARIANT |
| DR02 | M0, w = 0.2, on ZC-s1 for both families (§18 C-49) | ZC_NOT_COMMUTATIVE/NA_DIRECTION (cell P; NA_BOTH_FAMILIES) |
| DR03 | M2a, π = (0.05, 0.25), on W2 | ZC_NOT_COMMUTATIVE/ZC_COORDINATE |
| DR04 | M2a with π_a > π_b, on W1 (negative cell sign) | ZC_NOT_COMMUTATIVE/NOT_NA_DIRECTION |
| DR05 | M1 (κ_a, κ_b) = (0.85, 0.55) on W2 | ZC_NOT_COMMUTATIVE/ZC_COORDINATE |
| DR06 | order response keyed to D-prefix ids only, absent on fresh | ZC_NOT_COMMUTATIVE/NOT_REPLICATED |
| DR07 | β_PP = 0.05 with a tight interval | UNEXPLAINED/WEAK_REPLICATION, positive-below-margin licence |
| DR08 | M0 (w = 0.15) + M2a (π_a = 0, π_b = 0.05) on W2; exact r_MM = 1/2, r_PM = 7/8, r_MP = 5/8 | UNEXPLAINED/PARTIAL |
| DR09 | σβ_PP* ≤ 0 in > 1 % of draws (bimodal: a few prefixes with large opposite-sign numerators; planted at the statistics level, §18 C-50, CONTRACT `dry_run.dr09_plant`) | UNEXPLAINED/UNSTABLE_RATIO |
| DR10 | two controls responding on fresh W2 | UNEXPLAINED/FRESH_SET_UNSTABLE |
| DR11 | N_avail < 512 pool | UNEXPLAINED/NOT_ENOUGH_DATA, Stage C descriptive |
| DR12 | SE so large that no candidate n qualifies | UNEXPLAINED/UNDERPOWERED |
| DR13 | deliberately a/b-swapped pipeline | DEFECT_FOUND (caught by K2 and K5) |
| DR14 | float path breaking exact commutativity | ESTIMATOR_ARTIFACT/NON_INVARIANT |
| DR15 | a K0-violating variant path | STOP_REPLAN |
| DR16 | (1 − δ)·q_Parikh + δ·q*, δ ∈ {0, 0.05, 0.10, 0.20, 0.25, 1} | β = δ exactly |
| DR17 | joint member swap / predictor-only swap / joint permutation and duplication | unchanged / sign flip / unchanged |
| DR18 | mismatched joins, wrong readout positions | rejected |
| DR19 | zero cue mass, non-finite output, zero denominator | INVALID or undefined, never 0 |
| DR20 | D2 identity on duplicate-prefix fixtures | holds within 1e-12 |
| DR21 | boundary fixtures inside and outside the 1e-9 band | the expected qualifier side |
| DR22 | a simulated ledger above a 3× threshold | a pause record |

Fixtures whose decision depends on an interval (DR01, DR02, DR03, DR04, DR05, DR07, DR08) multiply the planted parameters per prefix by (1 + u_i), u_i uniform on [−1/5, 1/5] from `zc.dry_stream("jitter", id)`, so the intervals are not degenerate (§18 C-14); the expected outcomes are unchanged. DR13 and DR14 supply the ruling `{"cause_identified": true, "affects_beta": true}` and a K1 failure with A2 and K5 passing respectively. Pass: every expected outcome reproduced exactly and `validate_report` returns no error; after any correction the whole synthetic path is rerun before the freeze.

## 16. Reused functions (unchanged; real signatures at HEAD 1d629bc ≡ 213d1e2 over the closure)

| Module (alias) | Function (line) and signature |
|---|---|
| `x6s1_pairs` (sp) | `natural_prefixes(prefix_tokens, rnd_len: np.random.Generator) -> list` (186); `_loops(letters) -> tuple` (196); `designed_history(prefix, letters, y) -> tuple` (200); `_w1_history(prefix, member, y) -> tuple` (205); `designed_set(prefix_pool) -> dict` (210); `_pad(rows) -> np.ndarray` (228); `designed_arrays(D) -> dict` (235); `designed_sha256(arrays) -> str` (249); `q_exact(arm, tokens, t) -> tuple` (277); `q_stat(S, tokens, t) -> tuple` (288); `q_window(tokens, t, k=8) -> np.ndarray` (299); `q_heuristic(kind, tokens, t) -> tuple` (310); constants `ANCHOR, NB` (29), `CONTROL_SETS` (31), `W2_LETTERS` (33), `_S7` (36), `PAIR_FAMILIES` (37) |
| `x6s1_eval` (se) | `BOS = 18` (35); `ORACLE_KINDS` (36); `set_threads() -> None` (42); `model_inputs(tokens) -> torch.Tensor` (57); `class ModelPredictor(ckpt_path, file_sha256, weights_sha256)` (67; `from_state(sd_, name)` 81; `__call__(tokens, t) -> np.ndarray` 94; `float32(tokens, t)` 97; `_run(model, tokens, t)` 105); `_law(arm, kind, h, t)` (117); `class OraclePredictor(arm, kind)` (129); `qstar(arm, tokens, t) -> tuple` (147, returns `(q float64[n,18], codes int16[n,18])`); `class QuantInvalid(ValueError)` (157); `quantise(s) -> np.ndarray` (161); `score(codes, k, tables) -> np.ndarray` (187); `kl_rows(q, p) -> np.ndarray` (194); `cue_mass(p) -> np.ndarray` (201); `cue_normalise(p) -> np.ndarray` (205); `pair_terms(ph, ph2, qh, qh2) -> tuple` (214); `beta_fsum(num, den) -> float` (220); `beta_exact(num, den, informative=None) -> Fraction` (225); `_fam(A, fam, pred, qstar_fn, tables) -> dict` (238); `designed_stats(pred, D_arrays, qstar_fn, tables) -> dict` (274); `_predictor(name, spec)` (408); `_clean(v)` (426); `_json(path, obj) -> str` (434) |
| `x6s1_stats` (ss) | `log_tables(Q=2**20, eps=sd.EPS) -> dict` (110; cross-check only); `quantile(x, level) -> float` (140); `boot_beta(num, den, B, gen) -> np.ndarray` (151) |
| `x6s1_data` (sd) | `MODEL_CFG` (83); constants 90–107 (`PLACEBO, RHO_MAX` 97, `THREADS, EVAL_BATCH, MAX_CHILDREN` 106, `PROCESS_MEM` 107; the protocol's "90–106"); `DATA_MASTER, MODEL_MASTER` (71); `run_key(name) -> tuple` (168); `init_state(name) -> dict` (252); `holonomy_classes(arm="NA", n_max=31) -> dict` (272); `token_digest(tokens) -> str` (232) |
| `x6s1_stage_pre` (pre) | `ostore(store) -> ArtifactStore` (64); `pools_index(store) -> dict` (66); `load_obs(store, name) -> ObservationSet` (67; re-checks the token digest) |
| `x6s1_ingest` (si) | `admitted(store, model)` (416); `verify_admitted(store, model) -> dict` (441; reads and hashes the admitted final checkpoint: payload access, logged) |
| `x6s1_decide` (sdc) | `ord_d(na, init, ab, zc, dw2_lo) -> dict` (107) |
| `x6s1_run` (sr) | `seed_fresh(seed_maps) -> bool` (118) and `_seed_maps(project_root, store) -> list` (127) as patterns only (`_seed_maps` rglobs into `sealed/`, so `master_fresh` re-implements the walk with pruning); `meter_bind_check(path, expected_sha256, import_dir) -> None` (147; pattern only: binds `sd.WORKTREE`); `env_local() -> dict` (231); `env_changed(a, b) -> list` (243); `write_gate(store, gate, status, values) -> dict` (282) and `write_stage(store, stage, record) -> Path` (289) as patterns (they bind X6S1 gate names and the X6S1 store); `limits(model_cpu_s=math.inf) -> Limits` (299); `launch(args, log_path)` (303); `supervise(children, limits, stage, clock=time.monotonic) -> dict` (310) |
| `x6_model` (xm) | `compose(g, h) -> tuple` (62); `inverse(g) -> tuple` (64); `perm_name(g) -> str` (66); `tok(i) -> int` (72); `vertex(w) -> int` (76); `cue(x) -> int` (80); `seam_letter(i, j)` (88); `seam_labels(arm) -> dict` (103); `edge_labels(arm) -> dict` (118); `holonomy(path, labels) -> tuple` (186); `parikh(path) -> tuple` (227); `statistic(S, kappa)` (232); `lam(m, eta=ETA) -> Fraction` (242); `point_law(m, z, eta=ETA) -> tuple` (245); `parse(tokens) -> dict` (248); `closed_form(arm, tokens) -> dict` (261); `cue_normalised(q) -> tuple` (286); constants `ANCHOR, ANCHOR_NB` (30), `P_MOVE, ETA` (32), `S3_*` (57–59), `_SEAM` (99), `NEIGHBOURS` (83) |
| `x6_exact` (xe) | `LOOPS` (89); `members(family) -> tuple` (95); `witness_path(family, member) -> tuple` (97); `prefix_tokens(name, y0=0) -> tuple` (105); `witness_tokens(family, member, y, prefix="P0", y0=0) -> tuple` (107); `matched(family, y=0) -> dict` (138); `competitor_holonomy(kind, letters) -> tuple` (169); `beta(rows)` (181); `beta_table() -> dict` (196); `_EQUAL_ROWS` (283) |

Not invoked: `sr.run_stage`, `se.eval_chunk`, the E3 schedule, `sr.store_lineage` (it hashes payloads including `sealed/`).

## 17. A2 code-audit table (written; anchors checked at Stage A)
Each row: id, file (lines at H‴ ≡ HEAD), anchor string that must occur in that line range, expected behaviour. A missing anchor or a behaviour contradicting the expectation → DEFECT_CANDIDATE.

| Id | File:lines | Anchor | Expected behaviour |
|---|---|---|---|
| a1-letters | `x6s1_pairs.py:33` | `W2_LETTERS = (("A+", "B+"), ("B+", "A+"))` | member a = A⁺B⁺ (x first) |
| a1-set | `x6s1_pairs.py:216–219` | `for fam, (la, lb) in (("W2", W2_LETTERS),)` | a built from `W2_LETTERS[0]`, b from `[1]`, t = len(prefix) + 18 |
| a1-w1 | `x6s1_pairs.py:220–222` | `_w1_history(pre, "U", y)` | W1 a = U (x+ then y+), t = len(prefix) + 8 |
| a1-stats | `x6s1_eval.py:281–282` | `pair_terms(w2["a"]["p"], w2["b"]["p"], w2["a"]["q"], w2["b"]["q"])` | the same a/b for p̂ and q* |
| a2-oracle | `x6s1_eval.py:455` | `lambda tk, t: qstar("NA", tk, t)` | q*_NA for every predictor |
| a3-inputs | `x6s1_eval.py:57–60` | `np.full((len(tok), 1), BOS, np.int64)` | BOS then raw ordered tokens[:32] |
| a3-run | `x6s1_eval.py:105–114` | `row = lg[torch.arange(b - a), torch.from_numpy(ts[a:b])]` | logits at index t (predicts token t + 1), softmax, batches of `EVAL_BATCH` |
| a3-norm | `x6s1_eval.py:205–211` | `out[ok] = c[ok] / m[ok, None]` | cue entries 15..17 divided by their sum; NaN when the mass is 0 or non-finite |
| fam | `x6s1_eval.py:238–246` | `q, codes = qstar_fn(tok, t)` | p̂ and q* on the same rows and t |
| pair_terms | `x6s1_eval.py:214–217` | `return (dp * dq).sum(1), (dq * dq).sum(1)` | num = ⟨Δp̂_c, Δq*_c⟩, den = ‖Δq*_c‖² |
| beta_fsum | `x6s1_eval.py:220–222` | `return math.fsum(np.asarray(num, np.float64)) / d if d else math.nan` | Σnum/Σden, NaN on Σden = 0 |
| cue_mass | `x6s1_eval.py:201–202` | `[:, 15:18].sum(1)` | cue mass = sum of tokens 15..17 |
| a4-lock | `x6s1_eval.py:70–78` | `if sc.weights_digest(sd_) != str(weights_sha256).lower():` | file sha and weights digest verified |
| bos | `x6s1_eval.py:35` | `BOS = 18` | BOS token 18 |
| e8-pos | `src/topo_pilot/learner/model.py:90` | `self.pos_emb = nn.Embedding(cfg.n_ctx, cfg.d_model)` | learned positions |
| e8-sum | `src/topo_pilot/learner/model.py:116` | `x = self.tok_emb(inputs) + self.pos_emb(pos)` | token + position embedding; no order-free pooling |
| e8-doc | `src/topo_pilot/learner/model.py:70` | `learned positional embeddings` | decoder-only, pre-LN |
| e8-loss | `src/topo_pilot/learner/trainer.py:70–72` | `F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1))` | next-token objective over all positions; no commutativity term |
| e8-cfg | `tools/x6_stage1/x6s1_data.py:83` | `MODEL_CFG = ModelConfig(vocab_in=19, vocab_out=18)` | one config for every arm; inputs are tokens only (no oracle or latent labels) |
| e8-forbid | `tools/x6_stage1/x6s1_ingest.py:38` | `"prefix"` | the prefix pool is excluded from every cloud bundle |

Arm and seed identities are checked against the admission records in A1 item 3.

## 18. Choices (§choices; where the protocol leaves a detail open)

- **C-1 Module split.** OPEN-4 applies (§1): `x6zc_core.py`, `x6zc_census.py`, `x6zc_run.py`.
- **C-2 Licence templates** live in `CONTRACT.json` (`licences`, `not_licensed`) with cell-generic placeholders; for cell P they reproduce the §9.3 sentences. For σ = −1 cells the replication statistic is labelled `−β_PP` (= b).
- **C-3 K0 on D's control pairs** (C1–C4): q* of a and b equal for NA, ZC and AB is computed and recorded, not gated (the protocol's required items name W1, W2 and the variants).
- **C-4 Coupling table** stores cos² as an exact Fraction plus the sign, and a float cosine; per member, without a sign flip for member b.
- **C-5 Sensitivity lines.** A4: pairs with a matched member (either member, any pool) are removed for every predictor; D-prefix: whole clusters whose prefix string occurs among D's 1,030 are removed. Each line recomputes the bootstrap on its own stream (`sens_A4`, `sens_DPREFIX`) and the full decision; a differing outcome becomes a qualifier.
- **C-6 SE_D** = sample SD (ddof = 1) of the 5,000 B5 draws.
- **C-7 UNDERPOWERED cell P**: Stage C runs at n = N_avail ("the largest available size").
- **C-8 Crossing 0.10** compares absolute values |β| (the placebo bar is two-sided).
- **C-9 K5(e) on W1** checks only the t − 1 conditions (the protocol's "the same holds on W1 at t − 1").
- **C-10 K5(g), (h)** use ≤ 1e-12 (§5 repeated-prediction row); K5(i) requires exact equality (fsum-based statistics are order-independent).
- **C-11 Matched-key predictor**: K from the sha256 of the canonical JSON of (prefix, y, n, end vertex, Parikh) mod 1000; cue mass (1 + K mod 7)/10; cue law (K+1, K+2, K+3)/(3K+6); remainder uniform on the 15 vertex tokens.
- **C-12 Set-constant predictor**: cue mass 1/5, cue law ⅓, remainder uniform on vertex tokens.
- **C-13 K3 grid**: unequal ordered pairs (1/20, 1/5) and (1/5, 1/20) for two-rate mechanisms (equal rates give β_PP = 0 and no ratio); M4 = one seam's crossing missed in one member only (both seams, both members); M2 on W1 = first/second crossing; the W1 token-identity known case as in §6.
- **C-14 Dry-run jitter**: interval-dependent planted fixtures carry a per-prefix multiplicative jitter (1 + u_i), u_i ∈ [−1/5, 1/5], so that no interval is degenerate at a strict boundary.
- **C-15 Stage-1 store inventory**: `sealed/` is never listed; only the directory's own `st_mtime_ns` is recorded (adding or removing a file changes it).
- **C-16 Master freshness** walks the stores with `sealed`, `.git`, `.venv` pruned instead of `sr._seed_maps` (which recurses into `sealed/`).
- **C-17 DEFECT_CANDIDATE** does not stop a stage (only K0 and setup errors do); every candidate needs a coordinator ruling before the next stage; Stage C never starts with an unruled candidate or a fired global rule.
- **C-18 Axis 1 with DEFECT_ELSEWHERE** stays VALID (the defect does not touch the β computation).
- **C-19 Amendments**: an NA_DIRECTION secondary cell contributes 2–3; amendment 1 carries the "Stage C inconclusive" mark only when the headline is PARTIAL or a generic UNEXPLAINED outcome.
- **C-20 r_W1|P**: undefined draws (β_W2,PP* ≤ 0) are excluded; over 1 % undefined → no label.
- **C-21 Non-finite bootstrap draws** (zero denominators) make the interval unavailable → G-R1 INVALID.
- **C-22 Store additions** beyond §14: `STAGES.jsonl`, `rulings/`, `stages/0/`, `x6zc_meter_bind.py`; `x6zc-store/` is created by the coordinator before the dry run with `cpu_ledger.json` only, so the ledger includes stage 0.
- **C-23 `E0-PREFIX-READ`** is written at the start of Stage A when `EXPOSURE.jsonl` does not exist.
- **C-24 B4 for AB** reports shares on y, a·y and the third cue; own-arm regret uses the model's own arm codes.
- **C-25 B3 distributions** are summarised by 9 quantile levels of the per-pair max-abs differences.
- **C-26 D3** blocks are four consecutive blocks of 256 natural prefixes; weights as §10; top shares use ceil(5 %·P) prefixes and ceil(10 %·G) groups.
- **C-27 B7** control-family ρ uses W2's Δq* denominator (`designed_stats` convention).
- **C-28 K4 relative difference** = |g − s| / max(|g|, |s|), 0 when both are 0.
- **C-29 Numbers in qualifiers and licences**: 4 decimals.
- **C-30 q*_NA cache** keyed by sha256 of `bytes(tok[:t]) + t (2 bytes, little-endian)`, saved in `stages/A/qstar_NA.npz`.
- **C-31 NOT_DISCRIMINABLE(<kinds>)** joins the failed kinds with ", " in K3 order.
- **C-32 Stage C chunks** write only p arrays; the parent computes every statistic after all chunks completed (G2).
- **C-33 A2** is the §17 table; its anchors are verified automatically at Stage A; the behaviour column is reviewed by the coordinator.
- **C-34 A1 item 5** = (i) `EVALUATIONS.jsonl` kinds ⊆ `CONTRACT x6s1_store.evaluation_kinds_seen` (no prefix-pool kind) and (ii) the lines of `tools/x6_stage1/*.py` at HEAD containing `"prefix"` are exactly `a1_prefix_sites`, whose only consumers are `x6s1_stage_pre.py:220` (first 1,024 yields) and `x6s1_registry.py:445` (digests).
- **C-35 Cluster sums** use `math.fsum`; bootstrap draws use numpy sums (the `ss.boot_beta` rule, for bitwise equality).
- **C-36 Dry-run randomness** comes from `SeedTree(X6ZC_MASTER).generator("x6zc", "dry", …)`.
- **C-37 Short pool** = the synthetic pool truncated after its 1,280th yield (N_avail = 256).
- **C-38 B9 candidates** = sorted({1024, 2048, N_avail} ∩ [512, N_avail]).
- **C-39 Init predictors** use `stages/E0/init/init_s<s>.pt` with the CLOUD-PREP `NA-s<s>` digests (file and weights), as X6S1's `stage_post._spec` does.
- **C-40 Protocol hash at the freeze**: when `X6ZC-FROZEN-v1.md` replaces the design copy, `PROTOCOL_X6ZC_v1.md`, `CONTRACT.json` `protocol` and `PROTOCOL_ID` are updated together in one commit before the implementation hash is taken.
- **C-41 Per-cue β** with a zero denominator is NaN; it occurs only in invalid fixtures (DR19).
- **C-42 K2 per-cue tolerance** is 1e-12, like the pooled one.
- **C-43 Stage-B order** fixes the evaluation and report order; every model is evaluated even if an earlier group fails K4 (the failure is a DEFECT_CANDIDATE for the ruling).
- **C-44 G3** reads Stage-B CPU from the ledger difference since the Stage-B start.
- **C-45 ρ_v on fresh** variants uses that variant's own Δq*_NA denominator.
- **C-46 Stage-C prefixes** are the first n fresh prefixes in yield order.
- **C-47 A4** runs at Stage A on the variant histories of all N_avail fresh prefixes (n is not yet known).
- **C-48 Exposure logging of `verify_admitted`**: its read of the admitted checkpoint is logged in `EXPOSURE.jsonl` before the call (Stage B), as every payload load.
- **C-49 DR02** plants M0 (w = 0.2) on ZC-s1 for both families, so cell P gives NA_DIRECTION with r_W1|P ≈ 1 (NA_BOTH_FAMILIES); M0 cannot give a positive b on the σ = −1 cells without leaving the probability simplex.
- **C-50 DR09** is planted at the statistics level (cluster numerators passed to `paired_cluster_boot`), because a large opposite-sign numerator in one prefix is not reachable by a probability law; the rest of the path (cell statistics → decision → report) is the production one.
- **C-51 Planted predictors and the simplex**: `stage_c_statistics` does not check that rows are probability vectors; the B3/B4 summaries of Stage C (B4's regret quantises with `se.quantise`, which refuses non-simplex rows) are computed for the 16 models only, not for the q*_NA reference or synthetic predictors.

## 19. OPEN values
- `CONTRACT paths.meter_bind_sha256`: the sha256 of the store-local `x6zc_meter_bind.py`, written by the coordinator before the dry run and recorded in `FREEZE.json`.
- Freeze-time values that are not contract values: implementation commit, module and test blob sha256, dry-run report and stage-record sha256, `CONTRACT.json` sha256 (FREEZE.json); owner AUTH (b) (AUTH.json).

## 20. Erratum E1 (job 0123; implementer; rulings R-0120-1..4 written in)

Procedural only: no threshold, rule or scientific choice changes. Each item fixes one reading of an `API-AMBIGUITY` note in `tests/x6zc/test_*.py` or of a ruling of `jobs/0120/review.md`, choosing the reading the independent tests already accept. Where this section and an earlier one differ, this section wins (the protocol still wins over both).

- **E-1 Boundary comparisons (R-0120-1; `test_x6zc_decide.py` notes at R7 and R7b).** A float statistic is compared with a bar written as a decimal or fraction in the protocol by the float comparison as written: `x <= float(bar)`, `x < float(bar)`, `x > float(bar)`. So a computed 0.05 meets "lo(b) ≤ 0.05" (R7) and 0.01 is not "more than 1 %" (R7b). Counts and proportions of counts are compared exactly as integers: `cell_statistics` also returns `"undefined"` (int) and `"n_draws"` (int), and R7b fires iff `100 * undefined > n_draws`; when a cell dict carries only `"undefined_frac"`, R7b fires iff `undefined_frac > 0.01` (float). `choose_n` compares `h <= 0.25` in float. Exact `Fraction` comparison applies only where both sides are exact rationals computed exactly (K0, K3, F1, `beta_exact`). §3.2 and §9.2 are amended accordingly.
- **E-2 Ratio with no defined draw (R-0120-2; `test_x6zc_dryrun.py` note at line 40).** No exception. When β_PP = 0 the point ratio is `None`; when a ratio has zero defined draws its `"lo"` and `"hi"` are `None` (with `"n_defined": 0` and `"undefined"` = the draw count). A `None` bound never satisfies R8, R8b, R9 or R9′; the cell is decided by the β rules (with b = 0 and interval [0, 0], R6 gives NOT_REPLICATED). The same holds for `r_w1_p` (label `None`). A focal model whose outputs equal q*_ZC (the dry-run tests' unplanted cells) is this case.
- **E-3 K5 (a) rebuilds the members from content (R-0120-3; `test_x6zc_dryrun.py` note at DR13).** `pair_arrays` also returns `"tok_a"`, `"tok_b"` (the member token arrays it read). `k5_independent(terms, beta_prod, tok_a=None, tok_b=None)` takes the member histories from those keys (or the arguments), decides member a and b of every row by `zc.member_of` on the content, checks that both members share the prefix and cue, recomputes q*_NA exactly with `sp.q_exact` and β in Fractions from p̂ and q* in that content order, and compares with `beta_prod` (the production value) under the §5 K5a tiers. In the dry run, DR13 is planted as a pipeline that swaps a and b on the predictor side of `pair_terms`; K2 fails (q*_NA gives −1) and the dry-run report records whether K5 (a) also flags it. The tests assert K2 only.
- **E-4 `k3_float_check` result (`test_x6zc_core.py` line 214).** `{"status": "PASS" | "FAIL", "max_abs": float, "failed": [[mech_id, variant], ...]}`.
- **E-5 Cache hash mismatch (`test_x6zc_core.py` line 315).** `QStarCache.load(path, sha256)` raises `ValueError` when the file sha256 differs.
- **E-6 Prime spellings (R-0120-4; `test_x6zc_decide.py` line 26).** Both `'` and `′` are accepted on input (CONTRACT keys stay `"G-R2'"`, `"R9'"`); `decide_x6zc` writes `"G-R2′"` and `"R9′"` (U+2032) in its output and records.
- **E-7 Licence cell and family (R-0120-4; `test_x6zc_decide.py` line 235).** `licence(outcome, values, case=None)` reads the cell from `values["cell"]` and the family from `values["family"]`; the `":W1_suffix"` text is appended to NA_DIRECTION when the cell is S3 or S4 (or, with no `"cell"`, when the family is W1). The generic `"UNEXPLAINED/*"` template is filled with `outcome` = the outcome passed.
- **E-8 Census argument of `qualifiers` (R-0120-4; `test_x6zc_decide.py` line 262).** `census` is `None` or `{"qualifiers": {"<model>|<family>": [str]}, "sensitivity": {"A4": {cell: outcome}, "DPREFIX": {cell: outcome}}, "numeric_drift": ["<model>|<family>"]}` (each key optional). Order for a ZC_NOT_COMMUTATIVE cell: `ORIGIN_UNRESOLVED`, the census qualifiers of the cell's (model, family) in their stored order, `W2_ONLY` / `NA_BOTH_FAMILIES` (cell P), `SENSITIVITY_A4(<outcome>)`, `SENSITIVITY_D_PREFIX(<outcome>)` (only when the sensitivity outcome differs); then for every cell `LOW_FEASIBILITY(S3)`, `UNDERPOWERED(<cell>)`, `ENV_DRIFT`, `NUMERIC_DRIFT(<model>, <F>)`, `DEFECT_ELSEWHERE(<id>)`, `DESCRIPTIVE`.
- **E-9 Unplanted focal cells.** `stage_c_statistics` treats every name in `outputs` alike; a focal model whose outputs are commutative gives β_v = 0 exactly and falls under E-2. `B_DRAWS` is read from `zc.B_DRAWS` at call time (tests may monkeypatch it). A cell whose interval cannot be formed (a non-finite draw, §18 C-21) is `None` in `"cells"` and named in `"cell_errors"`; `decide_report` then sets `incomplete` (G-R1, INVALID).
- **E-10 K0 item labels (`test_x6zc_dryrun.py` line 297).** `oracle_geometry` reports `"checks"` with keys `"item1"` … `"item5"` and a counterexample `{"key", "row", "item": int, "detail"}` with the item number 1..5. Items are checked in order per pair, so the first failing item of the smallest (key, row) is reported.
- **E-11 Records.** `log_exposure` never writes the `E0-PREFIX-READ` line itself (Stage A writes it first when `EXPOSURE.jsonl` is absent); its ids are `"X<k>"` with k one more than the number of existing `X` lines. `log_evaluation` calls `guard` first. `k5_permutation(terms, gen=None)` uses `zc.stream("perm_K5i")` when no generator is given. `validate_report` checks the top-level keys of §11.6, the cell keys of every cell P, S3, S4, every outcome string (the CONTRACT outcomes, with NOT_DISCRIMINABLE(<kinds>) as a pattern) and an empty licence for STOP_REPLAN and INVALID; it does not type-check values.
- **E-12 Meter binding template.** The store-local `x6zc_meter_bind.py` is not a repository file (§1: exactly three modules). Its text is the template `BIND_TEMPLATE` in `x6zc_run.py` (the x6s1/c2 store-local pattern: it puts `METER_IMPORT_DIR` first on `sys.path`, imports the project meter `meter.py` unchanged, rebinds its store globals (`OUT`, `LEDGER`, `EMERGENCY`, `LOCK`, `ACTIVE`, `LOG_DIR`, `WORKER_SESSION`) to `x6zc-store` and runs `meter.main()`; CPU policy measure-only, `--max-cpu inf`). The coordinator writes it with `x6zc_run.py bind-template --out <store>/x6zc_meter_bind.py --session <id>` (exclusive create) and records its sha256 as `meter_bind_sha256`.
- **C-52 Module split (ruling R-0123-1; procedural, OPEN-4 pattern; no logic change).** The 400-line rule of protocol §14 stays; `x6zc_core.py` and `x6zc_run.py` are split mechanically (bodies moved verbatim; the only code change is that the chunk children are launched with `RUN = HERE / "x6zc_run.py"` instead of the module's own `__file__`). Modules under `tools/x6zc/`:
  - `x6zc_const.py`: CONTRACT loading, names and bindings, `T`, `B_DRAWS`, streams (§3). It applies the X6S1 `sys.path` convention (imports `x6s1_data` first).
  - `x6zc_decide.py`: `cluster_sums`, `paired_cluster_boot`, `interval`, `ratio_interval`, `cell_statistics`, `halfwidth`, `choose_n` (§8) and `decide_x6zc`, `licence`, `not_licensed`, `qualifiers`, `reuse_verdict` (§9). Imports `x6zc_const` only.
  - `x6zc_core.py`: §4-§7 (variants, K0, `QStarCache`, synthetic predictors, pair terms, K1-K3/F1); re-exports every name of `x6zc_const` and `x6zc_decide`.
  - `x6zc_census.py`: unchanged (§10).
  - `x6zc_store.py`: records, guards, inventory, environment, closure and master checks, meter binding and `BIND_TEMPLATE`, ledger and `pause_check`, `_frozen`, `_head` (§11.1-§11.3).
  - `x6zc_pipeline.py`: `predict_variants`, `stage_c_statistics`, `licence_values`, `decide_report`, `validate_report` (§11.4, §11.6). `stage_c_statistics` reads `zc.B_DRAWS` at call time, so a patched `zc.B_DRAWS` takes effect.
  - `x6zc_dry.py`: `dry()` and its planted predictors (§15).
  - `x6zc_stage_a.py`: stage begin/finish, A1, A2, `stage_a`, `_children`, `chunk`.
  - `x6zc_stage_bc.py`: `stage_b`, the Stage-B gate, `stage_c`.
  - `x6zc_run.py`: the CLI (§11.5); re-exports every name of store, pipeline, dry, stage_a and stage_bc.
  Import order (no cycle at import time): `x6zc_const` <- `x6zc_decide` <- `x6zc_core` <- `x6zc_census`, `x6zc_store`, `x6zc_pipeline` <- `x6zc_dry`, `x6zc_stage_a` <- `x6zc_stage_bc` <- `x6zc_run`. Test imports (§1) are unchanged.
- **C-53 Meter binding (coordinator finding before the freeze; supersedes the E-12 template text).** `BIND_TEMPLATE` (now in `x6zc_store.py`) follows `c2-readout-store/c2_meter_bind.py`: standard library only, run with `-I`; the binding must lie in its store (`OUT` = the store baked in at generation); at launch it reads the dispatch record named by the environment variable `X6ZC_DISPATCH` (keys `job`, `task_sha256`, `worker_session`, `meter_bind_sha256` = the binding file's sha256, `meter_import_dir` = `<x6zc worktree>/tools/x4_oracle_profile`) and fails closed if any is missing or differs; it checks the sha256 of `controls.py`, `meter.py`, `winjob.py` (the C2 `METER_FILES` values) and that they are imported from that directory; it sets `controls.JOB_ID`, `controls.TASK_SHA256`, `meter.WORKER_SESSION`, the meter store paths, `CAP_S = STOP_NEW_S = inf`, `OUTPUT_CAP` 16 GiB, `winjob.MEMORY_CAP` 12 GiB; it forces `--max-cpu inf --max-wall inf`; it refuses the launch below the disk floors C: 2 GB / X: 30 GB and adds the periodic disk safe-STOP (every 8th poll). The worker session is no longer baked in: `bind_template(out, session=None, store, worktree)` ignores `session`, and the CLI's `--session` is accepted and ignored. The file's sha256 therefore does not depend on the run job.

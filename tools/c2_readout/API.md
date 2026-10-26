# tools/c2_readout: written contract (job 0100; derived from C2-FROZEN-v1)

**Authority:** `tools/c2_readout/PROTOCOL_C2_v1.md`, a byte-for-byte copy of `agent-handoff/planning/responses/C2-FROZEN-v1.md` (sha256 `4d97d8e258cfab906ccfe1d99564d4dd74202edd96dd63eb836abd64c277a3d8`), and its coordinator addendum 1 (`C2-FROZEN-v1.coordinator-addendum-1.md`, sha256 `2db09007a1ff9f9706ffe323c0c1d2c49197648473c481c1776a46ae884011a8`), which binds R = `d44548b073523d402cc31fbfc5440c0d6df37a23`. AUTH: owner addendum 22 (`archive/owner-decisions-20261015/OWNER_DECISIONS.addendum-22.md`, sha256 `5a8430f36eb1432030c3ca8c2b3fa3a152193a4d3d80931a73015c413b3fe786`). Section numbers (§n), gate rows (§7 rows 0–28), stop rules (S1–S14), tolerance ids (T1–T18), RC/NEW/MD numbers and test names (T-READOUT … T-SIZE) refer to the protocol.

**Precedence.** The protocol is authoritative. This contract fixes names, signatures, shapes, dtypes, random streams, sequence-id codes, file layouts, record schemas, report keys, the gate order and the frozen registry source and exclusion inventory (O-7, §14 D7), so that the independent tests (§13.3) can be written before any module exists. It changes no scientific choice: no threshold, tolerance, seed, grid, K, covariate, projector, site, donor step, chart, split size, gate, stop rule, outcome rule or licence. Where this contract and the protocol differ, the protocol wins and the difference is a contract defect (report it; never resolve it in code). Details the protocol leaves open are fixed in §19 "Choices", always with the simplest option. `CONTRACT.json` holds the machine-readable values; where `CONTRACT.json` and the protocol differ, the protocol wins.

**Nothing here authorises a run.** No sampling, model forward, oracle run or test run follows from this contract (S1; §7 row 0b). Module code comes after the independent tests (§13.3).

## 1. Files, budgets, imports (§13.2)

| File | Contents (sections of this contract) | Budget (planned) |
|---|---|---|
| `c2_config.py` | CONTRACT loading, constants, exact `Fraction` levels and ranks, seeds, paths, sys.path convention (§3) | ≤ 400 (≈ 150) |
| `c2_data.py` | sampling (scope `c2-v1`), ids, panels, σ donor, ρ_R and ρ^{(m)} index maps, ρ_R symmetry report, history tables with the H^R digest, coverage tally, namespace admission, store admission (§4) | ≤ 400 (≈ 340) |
| `c2_registry.py` | R and R′ sources (reusing `c1_registry_sources`, the K4b readers and the X6S1 readers), inventory scan against the frozen inventory, exclusion records, separation (§5) | ≤ 400 (≈ 300) |
| `c2_oracle.py` | process loading, H1 static checks, the oracle for the four histories, q̄, d (named order), G (x, y, rotation), nuisance covariates, κ_m, eligibility, zero-modulus flags, H3 composition and Decimal rows for H^R, the rotation oracle (§6) | ≤ 400 (≈ 310) |
| `c2_model.py` | model loading, three-hook pass, Q₀/M, closed form, M0 checks, SYMBOL-ORDER checks, X1 (ephemeral) and its attainability, patch wrappers (§7) | ≤ 400 (≈ 320) |
| `c2_code.py` | FWL (K = 1, 2, 3), Ledoit–Wolf, whitened-design checks, GLS (QR), Euclidean variant, identities, interchange, code phase, R1 wrapper with the zero-modulus rule, N2, Haar frames, S* masked features (§8) | ≤ 400 (≈ 340) |
| `c2_stats.py` (pre-allowlisted overflow) | GLS-REF (80-digit `Decimal`; Lemmas GR, INV), the L1 decoders D0/D_code/D_lin, P1 ladder wrappers and MDE reports (§9) | ≤ 400 (≈ 380) |
| `c2_attrib.py` | A partition, energies, r, ν_S, operator decomposition, ψ_max, E\|A_S\|, rotation arm and s_rot, C2-M quantities and descriptives (seed 620518), the other §2.12 descriptives, POST-DESC values (§10) | ≤ 400 (≈ 340) |
| `c2_decide.py` | family bounds, NUM guard, Lemma FW per-model rules, coarse statements, 2-of-3, endpoint statuses, qualifiers, Q-CODE licence fill (§11) | ≤ 400 (≈ 390) |
| `c2_driver.py` | stages S1–S5, the C2 `LogitPolicy`, sealing, gate and stage records, lineage, release binding, meter-binding check, CLI (§12) | ≤ 400 (≈ 400) |
| `API.md`, `PROTOCOL_C2_v1.md`, `CONTRACT.json`, `TEST_PLAN.md` | this contract; the protocol copy; machine-readable values; the test plan | — |
| store-local `c2_meter_bind.py` | outside the repository, in the store (§12.8) | — |

Exactly these ten modules (S14: an eleventh module, or a `.py` file over 400 lines, stops before writing). No `src/` change, no change to any existing file.

**Import convention.** Every module imports `c2_config` first. `c2_config` computes `HERE = Path(__file__).resolve().parent`, `REPO = HERE.parents[1]` and prepends, if absent, in this order: `tools/c2_readout`, `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x6_stage1`, `tools/x4_circle_history`, `tools/x4_oracle_profile`, `tests/oracle_profile` (all under `REPO`) to `sys.path`. Importing `c1_config` then applies its own convention (unchanged). `x6s1_registry` is imported only inside the reader-x6 functions of `c2_registry` (lazy import; it imports `x6s1_data`, whose import applies the X6S1 convention). Module dependency order (no cycles): `c2_config` ← `c2_data` ← `c2_oracle` ← `c2_model` ← `c2_code` ← `c2_stats` ← `c2_attrib` ← `c2_decide` ← `c2_registry` ← `c2_driver`. Importing a module performs no I/O beyond reading `CONTRACT.json` (and the C1′/K4b `CONTRACT.json` reads of the reused modules) and no computation beyond small constants.

**Test imports.** A test file inserts `REPO / "tools" / "c2_readout"` at `sys.path[0]` (REPO = `Path(__file__).resolve().parents[2]`), imports `c2_config` first, and imports the modules by bare name with these aliases: `import c2_config as cc`, `c2_data as cd`, `c2_registry as cg`, `c2_oracle as co2`, `c2_model as cm`, `c2_code as ck`, `c2_stats as cs`, `c2_attrib as ca`, `c2_decide as cdc`, `c2_driver as cdr`. Reused code by bare name: `c1_oracle`, `c1_chart`, `c1_fit`, `c1_gates`, `c1_endpoint`, `c1_means`, `c1_model`, `c1_data`, `c1_records`, `c1_config`, `chart`, `precision`, `scores`, `stage_records`, `c1_registry_sources`, `k4b_registry`, `k4b_registry_k`, `k4b_data`, `x6s1_registry`.

## 2. Conventions

- **Rows and roles.** A split holds n rows. Canonical histories are `uint8[n, 32]` (column 0 is w1; symbol c = 6a + b, a = x-column, b = y-row). The four roles of a row are `"H"`, `"Hp"` (H⁺ = H^{+1}), `"Hm"` (H⁻ = H^{−1}) and `"HR"` (H^R), in this order everywhere (`ROLES`). Donor arrays are `int64[n, 32]`. Pairs: `"x"` = (Hp, Hm) (arm 1 = Hp, arm 2 = Hm); `"y"` = (H, HR) (arm 1 = H, arm 2 = HR).
- **Symbol order (RC-1; one convention).** The oracle is canonical; model inputs and logits are named: named = `perm[canonical]`. Every logit array is `float64[n, 36]` in **named** order; every oracle predictive and every d is computed canonical and converted by `c1_oracle.named_from_canonical(x, perm)` before any contraction with logits. `canonical_from_named_cols` appears only in SYMBOL-ORDER (c) and the M0 two-route check.
- **Model inputs.** `c1_model.model_inputs(perm[canon])` → `int64[n, 33]` = [BOS = 36, named w1..w32]; position index 32 predicts w33.
- **Shapes.** d_model = 128; readout coordinates `y` are `float64[n, 127]`; `Q0` `[128, 127]`; `M` `[36, 127]`; `beta`, `gamma` `[128]`; `WU` `[36, 128]`; layer-2 states `a2` `[n, 128]`; oracle beliefs `b31`, `b32` `[n, 144]` (12 × 12 grid states, the WorldSpec order); predictives `q`, `qbar` `[n, 36]` canonical; `m32` `[n, 2]`; nuisance covariates `[n, 5]` in the order (ȳ, Var y, ‖m32‖, H(b32), |h₂|). A per-row statistic is `float64[n]`; masks are `bool[n]`. Row-vector convention throughout: `y = (u − beta) @ Q0`, `z = WUbeta + y @ M.T`, projectors act as `dy @ P.T`.
- **Dtypes.** float64 everywhere; torch single thread (`c1_model.load_model64` sets it). Exact numbers are `fractions.Fraction` (thresholds, levels, ranks) and `decimal.Decimal` (GLS-REF, H3 references). Counts are Python `int`.
- **Model keys.** Python `int` (1729, 2718, 3141) in memory; decimal strings (`"1729"`) as JSON keys. Order `MODELS = (1729, 2718, 3141)`.
- **Families and projector problems.** Families `FAMILIES = ("R", "M", "S*")`. Projector problems per model `PROBLEMS = ("R", "R_K1", "R_K2", "R_E", "M", "S*")`: R = K 3 GLS at `ln_final_out` coordinates (primary); R_K1, R_K2 = K 1, 2 GLS variants; R_E = K 3 Euclidean-complement variant (the R fit, metric I); M = K 3 GLS at `resid_post_2` (n = 128); S* = K 3 GLS on the masked oracle-phase features. `VARIANTS = ("R_K1", "R_K2", "R_E")`.
- **Indicator form (§6.1).** `ind(s, E) = np.where(E, s, 0.0)` (a non-finite s on an ineligible row becomes 0; on an eligible row it is an error, FAIL_TECHNICAL/NUMERICAL). Point estimates are eligible-row ratios = ratios of indicator-form means.
- **Hashes.** Lowercase 64-hex sha256 of file bytes ("blob sha256" = sha256 of `git show H:<path>` bytes, equal to the working file with `core.autocrlf false`); comparisons with protocol or owner hashes are case-insensitive.
- **JSON.** Records are written by `stage_records.write_new` (sorted keys, indent 1, exclusive create); JSONL lines by `stage_records.record_gate` / `_append` format (`sort_keys`). `Fraction` values are written as `"p/q"` strings, `Decimal` values as `str(x)`, floats as JSON numbers (`repr` round trip), non-finite floats as the strings `"inf"`, `"-inf"`, `"nan"`.
- **UTC.** ISO `"%Y-%m-%dT%H:%M:%SZ"` in record fields; `"%Y%m%dT%H%M%SZ"` in file names.
- **Statuses (exact strings).** Gate statuses: `"PASS"`, `"FAIL"`, `"INVALID"`, `"NOT_RUN"`, `"NUMERICALLY_UNRESOLVED"`, or a full status `"FAIL_TECHNICAL/<class>"`, `"INCONCLUSIVE/<reason>"`, `"EXCLUDED/<reason>"`, `"INVALID/<reason>"`. FAIL_TECHNICAL classes: `AUTHORITY` (G0 i–v, viii), `LINEAGE`, `PF`, `IDENTITY`, `ORACLE`, `MODEL`, `X1`, `NUMERICAL`. INCONCLUSIVE reasons (§10): `REGISTRY_INCOMPLETE`, `ELIGIBILITY`, `HEADROOM`, `NUMERICAL`, `CHART_UNAVAILABLE`, `PATCH_MODEL_DEGENERATE`, `LINK`, `MODEL_HEADROOM`, `NUISANCE_IN_S`, `UNDERPOWERED`, `TEST_GATE`, `PRECISION`, `RADIAL_SUPPORT`. EXCLUDED reasons: `CHART_UNAVAILABLE`, `PATCH_MODEL_DEGENERATE`, `NUMERICAL`, `LINK`, `MODEL_HEADROOM`, `NUISANCE_IN_S`, `TEST_GATE`, `UNDERPOWERED`, `RADIAL_SUPPORT`. INVALID reasons: `INTERRUPTED` (S11), `LEAKAGE` (S12), `LINEAGE` (§11 item 7 inside a running stage).
- **Per-model statuses** (keyed by model, no `_j` suffix): R and S*: `"USED"`, `"NOT_USED"`, `"LOW_ALIGNED"`, `"PARTIAL"`, `"INC"`, `"INC/NUMERICAL"`, `"CNHS"`, `"EXCLUDED/<reason>"`; M: `"ROUTED"`, `"UPSTREAM_USED"`, `"UPSTREAM_NOT_USED"`, `"UPSTREAM_LOW_ALIGNED"`, `"UPSTREAM_PARTIAL"`, `"INC"`, `"INC/NUMERICAL"`, `"CNHS"`, `"EXCLUDED/<reason>"`. Endpoint statuses: `"SCORED"`, `"NOT_RUN/<gate>"`, `"SEALED_UNSCORED/<gate>"`.
- **Family outcomes** (exact strings, §10): R: `"FAIL_TECHNICAL/<class>"`, `"INCONCLUSIVE/<reason>"`, `"CIRCLE_NOT_HISTORY_SENSITIVE"`, `"USED"`, `"NOT_USED"`, `"LOW_ALIGNED_SHARE"`, `"PARTIAL"`, `"MIXED"`; M: the R set with `"ROUTED_AROUND"`, `"UPSTREAM_USED"`, `"UPSTREAM_NOT_USED"`, `"UPSTREAM_LOW_ALIGNED"`, `"UPSTREAM_PARTIAL"`, `"CNHS-2"` in place of the R categories; S*: `"X_PHASE_USED"`, `"X_PHASE_NOT_USED"`, `"X_PHASE_LOW_ALIGNED"`, `"X_PHASE_PARTIAL"`, `"X_PHASE_NOT_HISTORY_SENSITIVE"`, `"MIXED"`, INCONCLUSIVE, FAIL_TECHNICAL. Study: `"VALID"` or `"INVALID/INTERRUPTED"`, `"INVALID/LEAKAGE"`.
- **Qualifiers** (exact formats): `"SPECIFICITY_NOT_ESTABLISHED"`, `"NEGATIVE_ALIGNED_CONTRIBUTION(1729)"`, `"PROJECTOR_DEPENDENT(1729)"`, `"HARMONIC_DEPENDENT(1729, 1)"`, `"PRECISION_LIMITED(1729)"`, `"DISSENT(1729: PARTIAL)"`; in that order, models ascending.

## 3. c2_config.py

### 3.1 Bindings and paths
`PROTOCOL_ID = "C2-FROZEN-v1"`, `PROTOCOL_FILE = HERE / "PROTOCOL_C2_v1.md"`, `PROTOCOL_SHA256` (above), `ADDENDUM1_SHA256` (above), `AUTH_PATH = "agent-handoff/archive/owner-decisions-20261015/OWNER_DECISIONS.addendum-22.md"`, `AUTH_SHA256` (above), `R_COMMIT = "d44548b073523d402cc31fbfc5440c0d6df37a23"`, `BASE_COMMIT = "967605c256bcb554f43d4681326d32efc95bfcc9"`. `CONTRACT_PATH = HERE / "CONTRACT.json"`; `CONTRACT = load_contract()`.

Paths: `PROJECT_ROOT = Path("X:/Downloads/projects/topo-pilot")`, `STORE = PROJECT_ROOT / "c2-readout-store"`, `WORKTREE = PROJECT_ROOT / "topo-pilot-c2"`, `MAILBOX = PROJECT_ROOT / "agent-handoff"`, `ARTIFACT_ROOT = PROJECT_ROOT / "topo-pilot" / "artifacts"`, `C1P_STORE = PROJECT_ROOT / "c1prime-store"`, `K4_FREEZE = PROJECT_ROOT / "x4-circle-history-feas-store-0015" / "FREEZE.json"`, `X6S1_STORE = PROJECT_ROOT / "x6-stage1-store"`, `SCRATCH_ROOT = Path("X:/Downloads/topo-scratch")`.

### 3.2 Functions
- `load_contract(path=CONTRACT_PATH) -> dict`: `json.loads` (utf-8); raises `ValueError` if `contract["protocol"]["sha256"] != PROTOCOL_SHA256`.
- `frac(s) -> Fraction`: `Fraction(str(s))` for a CONTRACT string (`"1/240"`, `"1e-9"`, `"0.75"`); exact.
- `chart_cfg() -> dict` = `c1_config.chart_cfg()` (the C1′ CONTRACT `f8df2e43…a379` chart block, unchanged).
- `status_of(full) -> tuple` = `c1_config.status_of`.
- `seed(name) -> int`: `CONTRACT["seeds"][name]` (names in §13.2).

### 3.3 Constants (values in `CONTRACT.json`; names fixed here)
`SCOPE = "c2-v1"`, `REG_VERSION = "c2-reg-v1"`, `MODELS = (1729, 2718, 3141)`, `ROLES = ("H", "Hp", "Hm", "HR")`, `PAIRS = {"x": ("Hp", "Hm"), "y": ("H", "HR")}`, `SITES = ("resid_post_2", "resid_post_3", "ln_final_out")`, `HOOK_KEYS = {"resid_post_2": "rp2", "resid_post_3": "rp3", "ln_final_out": "ln"}`, `INDEX = 32`, `BOS = 36`, `V = 36`, `N_STATES = 144`, `D_MODEL = 128`, `N_READ = 127`, `BLOCK = 4096`, `SPLIT_BLOCKS = {"fit": 2, "feas": 1, "val": 1}`, `TEST_K = (1, 2, 4)`, `N_LADDER = (4096, 8192, 16384)`, `PROCESS = ("cylinder", "overlap", "1.25")`, `K_PRIMARY = 3`, `K_VARIANTS = (1, 2)`, `N_NUIS = 5`, `M0_ROWS = 1024`, `X1_LOWID_ROWS = 1024`, `C0V_ROWS = 512`, `H3_ROWS = 4`, `FAMILIES`, `PROBLEMS`, `VARIANTS` (§2).

Levels (Fractions): `ALPHA = {"R": 1/240, "S*": 1/240, "M": 1/360}`, `VAL_ALPHA = 1/60` (0.05/3), `H5_ALPHA = 1/20`, `DESC_ALPHA = 1/40` (two-sided 95 %), `TEST_DRAWS = 20000`, `VAL_DRAWS = 5000`, `DESC_DRAWS = 5000`. Ranks (asserted at import against `c1_means.rank_for`): `(20000, 1/240) → (84, 19917)`, `(20000, 1/360) → (56, 19945)`, `(5000, 1/60) → (84, 4917)`, `(5000, 1/20) → 250`, `(5000, 1/40) → (125, 4875)`.

Thresholds (Fractions): `PSI_LOW = 1/10`, `PSI_HIGH = 1/2`, `V3 = 3/10`, `PLACEBO = 1/10`, `TAU_M = 1/10`, `E_ABS = 1/10`, `E_RAND = 127/60`, `RS_A = 887/344043`, `RS_B = 121/344043`, `RS_K = 6`, `KAPPA_M = 1/100`, `H4 = 9/10`, `H5 = 1/100`, `L1_R2 = 1/2`, `L1_RHO = 9/10`, `R1 = 3/4`, `N2_FLOOR = 1/20`, `N2_SLACK = 1/50`, `C0V_SUPPORT = (99, 100)` (`100·n_sup ≥ 99·512`), `C0V_FIDELITY = 4/5`, `C0V_BIN_MIN = 8`, `C0V_RESULTANT = 3/10`, `SUP_MIN = 99/100`, `F_DRIFT = 1/50`, `ZERO_MOD = 1e-12`, `ZERO_CODE = 1e-12`, `ROT_DOSES = ((1, π/6), (2, π/3))` (m, θ).

Tolerances (CONTRACT strings, read with `frac` for comparisons): `TAU_X1 = 1e-9` (× max(1, ‖z‖∞)), `X1_ATTAIN = 1e-10` (4·128·2⁻⁵³·κ_X1 ≤ 1e-10), `RANK_R = 1e-8`, `T_SYM = 1e-14`, `T_DEC_POST = 2e-12`, `T_DEC_SURPRISAL = 1e-10`, `T_DEC_G = 2e-11`, `T_NAMED = 4e-12`, `T_CROSS_G = 1e-12`, `T_QSUM = 1e-12`, `T_GLS_ID = 1e-10`, `COND_MAX = 1e8`, `SV_RATIO = 1e-6`, `LW_RATIO = 1e-12`, `GLSREF_PREC = 80`, `GLSREF_RHO = 1e-20`, `GLSREF_PROJ = 1e-8`, `GLSREF_INFLATE = 1e-70`, `T18 = 1e-12`, `GUARD_REL = 1e-9`.

## 4. c2_data.py

### 4.1 Sampling and identifiers (§5.2)
- `history_generator(split, block) -> np.random.Generator` = `SeedTree(0).generator("data", "c2-v1", split, int(block), "cylinder", "overlap", "1.25")`; `split ∈ ("fit", "feas", "val", "test")`.
- `sequence_ids(split, block) -> int64[4096]` = `make_sequence_ids(process_code("cylinder", "overlap", "1.25", f"c2-v1/{split}/b{int(block)}"), "test", 4096)`. The codes are listed in §14.
- `sample_block(T, E_canon, pi, split, block) -> (uint8[4096, 32], int64[4096])`: one `HMMSampler(T, E_canon, pi, SequenceLayout()).sample(4096, history_generator(split, block))` call; columns 0..31 kept; w33 and the latent states are deleted inside the function before it returns (as `c1_data.sample_block`).
- `sample_split(T, E_canon, pi, split, blocks) -> (uint8[n, 32], int64[n], int64[n])`: blocks `0..blocks−1` concatenated in block order; returns canonical, sequence ids and panels (`c1_data.panels(ids_b, b)` per block). FIT has 2 blocks (8 panels, §5.2), FEAS and VAL 1, TEST k (sampled at S5 only, after ACCEPT).
- `lowest(seq_ids, n) -> int64[n]` = `c1_data.lowest` (stable argsort of the ids).

### 4.2 Donors and index maps (§2.2, §2.11)
- `sigma(canonical) -> int64` (same shape): `6·(c // 6) + (5 − c % 6)`.
- `reflect_donor(canon32) -> int64[n, 32]`: columns 0..30 mapped by `sigma`, column 31 (w32) kept.
- `donors4(canon32) -> tuple[int64[n, 32] × 4]` = `(*c1_oracle.donors(canon32), reflect_donor(canon32))` in `ROLES` order.
- `rho_R_index(coords) -> int64[144]`: `idx[i]` = index of the state with coordinates `(x_i, 11 − y_i)` (coordinates rounded with `np.rint`, as `c1_oracle.rho_index`).
- `rho_m_index(coords, m) -> int64[144]`: `idx[i]` = index of `((x_i + m) mod 12, y_i)`, `m ∈ {−2, −1, 1, 2}` (one grid cell per unit; `rho_m_index(coords, 2·k)` equals `c1_oracle.rho_index(coords, k)`).
- `symmetry_report_R(T, E, pi, coords) -> dict` keys `"max_dev"`, `"symmetry_ok"` (max_dev ≤ 1e-14), `"exact_invariance"` (`T[ρ_R][:, ρ_R] == T` and `pi[ρ_R] == pi` bitwise), `"r_E"` (Fraction: max over z, v of \|F(E[ρ_R z, σ v]) / F(E[z, v]) − 1\|), `"eps_sym"` (`r_E/(1 − r_E)` or None): the ρ_R/σ analogue of `c1_oracle.symmetry_report` (§7 row 6).
- The ρ_R closed form is `c1_oracle.closed_form_b32(b31(H), T, E, w32, rho_R_index(coords))` with `c1_oracle.closed_form_tolerance(eps_sym^R)` (reused; no new function).

### 4.3 History tables and tally
- `history_table(canon32, seq_ids, panel) -> dict`: keys `"canonical"` uint8 `[n, 32]`, `"sequence_id"` int64, `"panel"` int64, `"digest_H"`, `"digest_Hp"`, `"digest_Hm"`, `"digest_HR"` (`<U64` arrays, `scores.history_digests` of each role, §5.3).
- `table_digests(table) -> set[str]`: the union of the four digest columns.
- `REASONS = ("S_PLUS", "S_MINUS", "S_REFL", "LIK_H", "LIK_PLUS", "LIK_MINUS", "LIK_REFL", "ZERO_MOD_H", "ZERO_MOD_PLUS", "ZERO_MOD_MINUS")` (oracle reasons) and `MODEL_REASONS = ("UNSUPPORTED_H", "UNSUPPORTED_PLUS", "UNSUPPORTED_MINUS", "ZERO_CODE_PLUS", "ZERO_CODE_MINUS", "R1_ZERO", "R1_UNSELECTED")` (per model and family; UNSUPPORTED only for R and M).
- `coverage_tally(flags: dict[str, bool[n]]) -> dict[str, int]`: counts per reason key in the given order (a row counts under every applicable reason; nothing is removed). Oracle flags come from `c2_oracle.reason_flags`; model flags are keyed `"<family>|<model>|<reason>"`.

### 4.4 Namespace and store admission (§5.2 G0 vi, §11 item 7)
- `namespace_scan(root=PROJECT_ROOT, pinned: dict[str, str], lineage: dict[str, str]) -> dict` `{"status": "PASS" | "FAIL_TECHNICAL/LINEAGE", "hits": [{"path", "sha256", "class"}], "scanned": int}`. Scanned files: every file whose name matches `CONTRACT*.json`, `FREEZE*.json`, `STAGES*.jsonl` or `GATES*.jsonl` anywhere under `root` (skipping `.git` and `.venv` directories), and every `*.json`, `*.jsonl`, `*.md`, `*.txt` or `*.py` file under every top-level `*-store*` directory. A hit is a file whose bytes contain `b"c2-v1"` (read in 1 MiB chunks with a 4-byte overlap; no size cap, since `registry_v1.json` alone is ≈ 300 MB). Classes: `"PINNED"` (path inside `WORKTREE/tools/c2_readout/`, or sha256 in `pinned`, the sha256 values of the files of `tools/c2_readout` at H), `"LINEAGE"` (path relative to the store, with sha256, in `lineage`; see §16.2), else `"FOREIGN"` → FAIL_TECHNICAL/LINEAGE.
- `store_admission(store, lineage, first_sampling: bool) -> dict` `{"status", "unrecognised": [path], "payload": [path]}`. `first_sampling`: PASS iff no file exists under `hist/`, `oracle/`, `fits/`, `stages/` or `sealed/` and every other file is recognised (§16.2). Otherwise every file must be recognised with its exact sha256. Status on failure: `"FAIL_TECHNICAL/LINEAGE"` at G0 (§19 item C-18).

## 5. c2_registry.py (§5.3; version `c2-reg-v1`)

### 5.1 Readers (sources a–e and the inventory components)
Reader tags and the reused functions (all unchanged):

| Tag | Function | What it yields |
|---|---|---|
| `a` | `k4b_registry.source_a(ARTIFACT_ROOT, store)` (= `c1_registry_sources.observation_set_sources`) | every ObservationSet under `topo-pilot/artifacts`, canonicalised by its EmissionSpec perm; sequence ids |
| `b` | `k4b_registry.source_b(PROJECT_ROOT)` (= `c1_registry_sources.store_sources`) | the C1′ (b) stores, empty ones as explicit empty records; coverage by `k4b_registry.revalidate_coverage` |
| `c` | `k4b_registry.source_c(MAILBOX)` (`validate_handoff_json`, then `c1_registry_sources.handoff_sources`) | 32/33-element integer lists in every mailbox JSON |
| `d` | `k4b_registry.source_d(C1P_STORE)` | `registry/registry_v1.json` digests (sha256 bound by the K4b CONTRACT) and the H, H⁺, H⁻ digest columns of every `HIST_*.npz` (protocol (d): `HIST_cal_b0`, `HIST_cal_b1`, `HIST_val_b0`; the 512 chart landmarks are cal-b0 rows) |
| `e` | `k4b_registry.source_e(PROJECT_ROOT / "d2a-store")` | permitted D-2a pools (raw tokens[:, :32]); sealed pools by sequence-id ranges and the predicate `"sealed_d2a"` (`k4b_data.predicate_check`), never opened |
| `f` | `k4b_registry.source_f(PROJECT_ROOT, inv, classes)` | ObservationSet roots outside `topo-pilot/artifacts` (added by `k4b_registry.classify`) |
| `k` | `k4b_registry_k.source_k(PROJECT_ROOT / "k4b-store")` | K4b stage tables (current and superseded) as tokens and digest columns; derived K-REG files listed; anything else → INCOMPLETE |
| `x6` | `x6_source(X6S1_STORE, run_dir)` (below) | the X6S1 bounded-memory digest set: `x6s1_registry.open_reg(X6S1_STORE, "X6-REG2")` as base plus every other history-bearing array of the store |

- `x6_source(store, run_dir) -> dict` `{"status": "PASS" | "INCONCLUSIVE/REGISTRY_INCOMPLETE" | "FAIL_TECHNICAL/LINEAGE", "digestset": x6s1_registry.DigestSet | None, "files": [{"path", "sha256", "keys", "rows"}], "other": [{"path", "reason"}], "base": {"manifest_sha256", "n", "digest_sha256"}}`. Steps: (1) `base = x6s1_registry.open_reg(store, "X6-REG2")` (re-hashes every run; its manifest sha256 must equal `CONTRACT["registry"]["x6_reg2_manifest_sha256"]`, else FAIL_TECHNICAL/LINEAGE); (2) for every `*.npz` and `*.npy` file under `store` except `registry/**`, in sorted path order, `x6s1_registry._headers(path)`; a file is history-bearing iff `x6s1_registry._history_bearing(path)`; for each history-bearing member (key in `k4b_registry_k.HISTORY_KEYS`, or an integer array with ndim ≥ 2 and last dimension 32 or 33) the first 32 columns of the array reshaped to `[-1, last]` are read as uint8 (raw, no canonicalisation) and digested by `x6s1_registry.row_digests`; members whose key starts with `digest` (hex `<U64`) are converted by `x6s1_registry.hex_to_digests`; (3) `DigestSet.build(chunks, run_dir, base=base)`; an unreadable array file → `other` → INCOMPLETE. ObservationSet payloads (`pools/ObservationSet/*/payload.npz`, key `tokens`) are read by this rule.
- `token_sources(root=PROJECT_ROOT) -> dict` `{"a": (sources, seqs), "b": [...], "c": [...], "e": {...}, "k": {...}, "problems": [str]}`: each reader called through a `_try` that turns an exception into a problem (`k4b_registry._try` semantics).

### 5.2 Inventory against the frozen table (§18)
- `INVENTORY: dict[str, dict]` = `CONTRACT["registry"]["inventory"]` (equal to §18).
- `inventory(root=PROJECT_ROOT) -> dict` `{"status", "inv", "classes", "unlisted": [name], "violations": [{"name", "reason"}]}`: `inv = k4b_registry.inventory(root, exclude=("agent-handoff", "c1prime-store", "d2a-store", "k4b-store", "x6-stage1-store", "c2-readout-store"))`; the entry `"c2-readout-store"` is removed from `inv` (own store, §18 row OWN); `classes = k4b_registry.classify(inv, readers)` with `readers = {s: ["b"] for s in c1_registry_sources.SCANNED_STORES} ∪ {"topo-pilot": ["a"], "agent-handoff": ["c"], "c1prime-store": ["d"], "d2a-store": ["e"], "k4b-store": ["k"], "x6-stage1-store": ["x6"]}` (tags added only for readers that succeeded, as `k4b_registry.build`). Rules: (i) a directory in `INVENTORY` with decision `READER` must be classed `SCANNED` with exactly the listed tags (plus `f` where listed); (ii) a directory with decision `EXCLUSION` must be classed `NOT_SCANNED`; (iii) a directory not in `INVENTORY` (`unlisted`) is allowed only if classed `NOT_SCANNED` with 0 history-bearing files, 0 identity references, 0 ObservationSet roots and 0 unreadable files (it is recorded as a new exclusion with the inventory's reason); (iv) any `INCOMPLETE` class. A violation of (i)–(iv) → `"INCONCLUSIVE/REGISTRY_INCOMPLETE"`; else `"PASS"`.

### 5.3 Builds, loading, separation
- `build(version, store, root=PROJECT_ROOT, extra=None) -> dict`: `version ∈ ("C2-REG1", "C2-REG2")`; refuses (`FileExistsError`) if any output exists. Token sources a, b, c, e (permitted pools), f, k go through `c1_data.build_registry` (frozen); digest sources (d, and the `digests` of k) are unioned into its digest set; `extra` (C2-REG2 only: the FIT, FEAS and VAL history tables) adds their four digest columns; the x6 component is built by `x6_source(root / "x6-stage1-store", store / "registry" / "runs" / version)`. Writes by exclusive create `registry/<version>_digests.npz` (`stage_records.save_npz`, keys `digests` `<U64` sorted unique, `seq_ids` int64 sorted unique) and `registry/<version>.json` (manifest, §16.3). Status: `"PASS"`, or `"INCONCLUSIVE/REGISTRY_INCOMPLETE"` if any problem, unreadable source (`build_registry` "missing"), coverage failure (`k4b_registry.revalidate_coverage`), handoff JSON failure, k or x6 `other` entry, or inventory violation; `"FAIL_TECHNICAL/LINEAGE"` for a binding mismatch (registry_v1 sha256, X6-REG2 manifest).
- `class Registry`: `Registry.load(store, version) -> Registry` re-hashes `<version>_digests.npz` against the manifest's `digest_file_sha256` and reopens the x6 runs (each run file re-hashed against the manifest, base runs against X6-REG2) (mismatch → `RuntimeError` with status `"FAIL_TECHNICAL/LINEAGE"` in `.status`); attributes `digests` (set of hex), `x6` (DigestSet), `sealed_ranges`, `predicates`, `manifest`; `contains(hex_digests) -> bool[n]` = membership in `digests` OR `x6.contains(hex_to_digests(...))`.
- `separation(reg, tables: dict[str, dict]) -> dict` `{"status", "collisions": {...}, "duplicates": {split: int}, "seq_ids": "PASS" | str, "predicate": {"hits": int}, "sealed_ranges": int}` for `tables` keyed by split (`"fit"`, `"feas"`, `"val"`; at S5 `"test"` with `reg` = C2-REG2): every split's union U (four roles) is disjoint from R (`reg.contains`) and from every other split's U (`collisions` keys `"<split>_R"` and `"<a>_<b>"`); sequence ids pairwise disjoint (`dataset.checks.check_disjoint`) and outside the D-2a sealed ranges; within-split duplicate digests counted and kept. A collision or seq-id overlap → `"FAIL_TECHNICAL/LINEAGE"`; a D-2a predicate hit on the canonical arrays of any role → `"INCONCLUSIVE/REGISTRY_INCOMPLETE"` (reason `"potential overlap with sealed D-2a histories"`, §19 item C-11); else `"PASS"`.
- `first_token_ok(table, T, E_canon, pi, split) -> bool` = `c1_data.first_token_ok(canonical[:, 0], pi @ E_canon, split)` per block.

## 6. c2_oracle.py

### 6.1 Process and H1 (§7 row 3)
- `load_process() -> dict` via `x4_oracle_profile.inputs.load_config()` and `inputs.load_process(cfg)` (unchanged; as the C1′ `_process`): keys `"T"` `[144, 144]`, `"pi"` `[144]`, `"coords"` `[144, 2]`, `"E_named"` `{j: [144, 36]}`, `"perm"` `{j: int64[36]}`, `"E_canon"` `{j: [144, 36]}` (`oracle_profile.canonical_emission`), `"ids_ok"` (config artifact ids equal `CONTRACT["models"]` and `CONTRACT["shared"]`), `"identity"`.
- `h1_static(proc) -> dict` `{"status", "checks": {"ids", "perms", "roundtrip", "E_identical", "order_b"}}`: ids_ok; every perm a permutation of 0..35; `argsort(perm)[perm[arange(36)]] == arange(36)`; `E_canon[j]` bitwise equal across models; SYMBOL-ORDER (b) = `c2_model.symbol_order_b(perm)` per model. Failure → `"FAIL_TECHNICAL/IDENTITY"`. The canonical emission used everywhere is `E = E_canon[1729]`.

### 6.2 Oracle rows
- `oracle_role(T, E, pi, tokens32) -> dict` from `c1_oracle.run_oracle`: `"b31"`, `"b32"` `[n, 144]`, `"q"` `[n, 36]` (raw), `"qbar"` (= q / q.sum(1, keepdims)), `"s"` `[n]` (surprisal of w32 given w1..w31), `"le"` `[n]` (log-evidence), `"m32"` `[n, 2]` (`c1_oracle.m32(b32, coords)`).
- `oracle_split(T, E, pi, coords, canon32) -> dict`: `{role: oracle_role(...)}` for the four roles plus `"G_x"`, `"d_x"` (`c1_oracle.G_hat(qbar_Hp, qbar_Hm)`: G and canonical d), `"G_y"`, `"d_y"` (`G_hat(qbar_H, qbar_HR)`), `"nuis"` = `nuisance5(b32_H, coords)`.
- `nuisance5(b32, coords) -> float64[n, 5]`: `c1_oracle.nuisance(b32, coords)` (ȳ, Var y, ‖m32‖) then the Shannon entropy `−Σ_z b log b` (natural log, `0·log 0 = 0`) and `|Σ_z b32(z) exp(2i·2π·x(z)/12)|` with `x = rint(coords[:, 0])`.
- `d_named(d_canon, perm) -> float64[n, 36]` = `c1_oracle.named_from_canonical(d_canon, perm)`.
- `s_max(s_fit_H) -> float` = `c1_oracle.s_max` (FIT q0.999, `inverted_cdf`; frozen at S1).
- `eligibility(o, smax) -> dict` `{"E_x": bool[n], "E_y": bool[n]}`: E_x = `c1_oracle.eligible(s_Hp, s_Hm, smax, le_H, le_Hp, le_Hm)`; E_y = `(s_HR ≤ smax) & isfinite(le_H) & isfinite(le_HR)`.
- `kappa_m(m32_H, m32_HR, E_y_fit, m32_H_fit) -> float`: mean over FIT E_y rows of ‖m32(H) − m32(H^R)‖² divided by `trace(np.cov(m32_H_fit.T, ddof=0))` (all FIT rows). `y_active(kappa_m) -> bool` = `kappa_m < 1/100` (exact: `Fraction(kappa_m) < Fraction(1, 100)`).
- `kappa_nu(o_fit, E_x_fit, coords) -> float` = `c1_oracle.kappa_nu(ν(b32_Hp), ν(b32_Hm), ν(b32_H), E_x)` with ν = `c1_oracle.y_marginal` (reported, §2.2).
- `phi_star(m32) -> (float64[n], bool[n])`: `atan2(m32[:, 1], m32[:, 0])` and `m_valid = ‖m32‖ > 1e-12`; on invalid rows the phase is the placeholder 0.0.
- `reason_flags(o, smax) -> dict[str, bool[n]]`: the §5.5 oracle reasons of `c2_data.REASONS` (S_* = surprisal > s_max; LIK_* = non-finite log-evidence; ZERO_MOD_* = ‖m32‖ ≤ 1e-12 for H, Hp, Hm).

### 6.3 H3 (§7 row 6; T1–T8)
- `h3(T, E, pi, coords, perms, E_named, splits: dict[str, (canon32, o, E_x, E_y, seq_ids)]) -> dict` `{"status", "checks", "symmetry": {"tau", "rho_R"}}`, the composition, in this order: (1) `c1_oracle.symmetry_report` and `c2_data.symmetry_report_R`: `symmetry_ok` and `exact_invariance` both (T1, T2); (2) closed forms for k = ±1 (`c1_oracle.closed_form_b32(b31_H, T, E, w32, c1_oracle.rho_index(coords, k))` vs `b32_Hp`/`b32_Hm`) and for ρ_R (vs `b32_HR`), relative agreement within `t + t²` of `c1_oracle.closed_form_tolerance` per row (T3; `None` tolerance → FAIL_TECHNICAL/ORACLE); (3) named = canonical: per model, `run_oracle(T, E_named[j], pi, perm[role])["q"]` gathered by `canonical_from_named_cols` agrees with the canonical q within 4e-12 relative (T7; four roles); (4) cross-model G: `c1_oracle.G_named(d, lam, perm)` vs canonical G ≤ 1e-12 absolute for the x and y pairs (T8); (5) `|Σ_v q_v − 1| ≤ 1e-12` on every row and role (raw q); (6) Decimal rows (below); (7) SYMBOL-ORDER (c) on the FIT d arrays (`c2_model.symbol_order_c`). Any failure of (1)–(5), (7) → `"FAIL_TECHNICAL/ORACLE"` ((7): `"FAIL_TECHNICAL/IDENTITY"`); (6) can also give `"INCONCLUSIVE/NUMERICAL"`.
- `decimal_rows(T, E, pi, canon32, o, rows, p0) -> str`: for each row in `rows` (the 4 lowest-sequence-id rows with E_x and E_y, per split) and each role: `ref = c1_oracle.decimal_reference(T, E, pi, role_tokens[i])`; b31, b32 and q compared by `c1_oracle.h3_compare(x_hat, x_dec, p1_ok, beta)` with `p1_ok = c1_cert.p1(ref0["nu_min"], ref0["finite"], p0["nu0"])[0]`, `ref0 = c1_cert.reference_oracle(T, E, pi, role_tokens[i:i+1])`, `beta = error_bound.posterior_envelope(32, p0["N"])` and `p0 = c1_cert.p0(T, [E], pi)` (the C1′ fast-path rule, §19 item C-7); surprisal `|ŝ − s̃| ≤ 1e-10` (T5); `|Ĝ − G̃| ≤ 2e-11·(1 + max_v |λ̂_v|)` for the x pair (G̃ = `c1_oracle.decimal_G(q32_Hp, q32_Hm)`) and the y pair (q32_H, q32_HR), λ̂ = log q̄¹ − log q̄² (T6). Returns the worst of `"PASS"`, `"INCONCLUSIVE/NUMERICAL"`, `"FAIL_TECHNICAL/ORACLE"`.

### 6.4 Rotation oracle (§2.11)
- `rotation_oracle(b31_H, T, E, w32, coords, m) -> dict` `{"b_plus", "b_minus", "q_plus", "q_minus", "d", "G"}`: `b_± = c1_oracle.closed_form_b32(b31_H, T, E, w32, c2_data.rho_m_index(coords, ±m))`; `q_± = normalise((b_± @ T) @ E)`; `d = q_+ − q_−` (canonical; convert with `d_named`); `G = G_hat(q_+, q_−)[0]`. At m = 2 `b_±` equals the closed form of b32(H^±) (T-ORACLE).

## 7. c2_model.py

### 7.1 Models and passes
- `load_models() -> dict[int, tuple]`: per model `(model64, state_sha)` from `c1_model.load_model64(store.load(Checkpoint, CONTRACT["models"][j]["checkpoint"], consumer="experiment"))` with `ArtifactStore(LocalFSBackend(ARTIFACT_ROOT))`.
- `activations3(model64, inputs, batch=1024) -> dict[str, float64[n, 128]]`: one forward per batch with `return_hooks=SITES`; returns `hooks[site][:, 32, :]` for the three sites; the logits are deleted unread.
- `natural_pass(model64, inputs, policy, kind, batch=1024) -> (dict, float64[n, 36])`: as `activations3` plus `logits[:, 32]`; calls `policy.require(kind)` first.
- `patched_logits(model64, inputs, site, rep, policy, kind, batch=1024) -> float64[n, 36]`: `policy.require(kind)`; `forward_with_patch(model64, inputs, site, 32, rep)` per batch, logits at index 32. `rep` is `float64[n, 128]`.

### 7.2 Readout coordinates (§2.1, Lemma R)
- `helmert(n=128) -> float64[n, n − 1]`: column k (1-based, k = 1..n−1) has entries `1/√(k(k+1))` in rows 1..k, `−k/√(k(k+1))` in row k+1, 0 below.
- `readout_basis(model64) -> dict` keys `"gamma"`, `"beta"` (`ln_final.weight`, `.bias`), `"WU"` (`unembed.weight`), `"N1"`, `"Q0"` (= `c1_fit.qr_pos(diag(gamma) @ N1)`), `"R_diag"` (`abs(diag(np.linalg.qr(diag(gamma) @ N1, mode="r")))`), `"rank_ok"` (`min R_diag > 1e-8·max R_diag`), `"M"` (= `WU @ Q0`), `"WUbeta"` (= `WU @ beta`), `"ln_eps"`.
- `readout_coords(u, basis) -> float64[n, 127]` = `(u − beta) @ Q0`; `closed_logits(y, basis) -> float64[n, 36]` = `WUbeta + y @ M.T`; `placed(y_hat, basis) -> float64[n, 128]` = `beta + y_hat @ Q0.T`.

### 7.3 M0 (§7 row 9)
- `identity_patch(model64, inputs, acts, policy) -> dict` `{site: bool}`: `patched_logits(..., site, acts[site], policy, "m0")` bitwise equal to the natural logits for the three sites.
- `readout_identity(z_net, y, basis) -> dict` `{"max_dev", "n_over", "ok"}`: per row `‖z_net − closed_logits(y)‖∞ ≤ 1e-9·max(1, ‖z_net‖∞)`.
- `kappa_x1(u, y, basis, z) -> float`: `S_iv = Σ_k |WU_vk|(|u_ik| + |beta_k|) + Σ_l (|WU| @ |Q0|)_vl |y_il|`; `κ = max_{i,v} S_iv / max(1, ‖z_i‖∞)`; `x1_attainable(κ) -> bool` = `4·128·Fraction(1, 2**53)·Fraction(κ) ≤ Fraction("1e-10")` (§19 item C-6).
- `two_route(d_canon, d_named, z_named, perm) -> dict` `{"max_ratio", "ok"}`: `s_n = 0.5·Σ_v d_named·z_named`, `z_c = canonical_from_named_cols(z_named, perm)`, `s_c = 0.5·Σ_v d_canon·z_c`; per row `|s_n − s_c| ≤ 1e-12·max(1, Σ_v |d_canon,v z_c,v|)` (T18). On M0 rows `d = d_x` of the row and `z = z_net(H)` (§19 item C-25).
- `symbol_order_a(named_inputs, canon32, perm) -> bool`: `c1_registry_sources.canonical32(named_inputs[:, 1:], perm)` equals `canon32` bitwise (the independent inverse route). `symbol_order_b(perm) -> bool`: `named_from_canonical(np.eye(36), perm)` equals `np.eye(36)[perm]` bitwise. `symbol_order_c(d_canon, perm) -> bool`: `canonical_from_named_cols(named_from_canonical(d, perm), perm)` equals `d` bitwise.
- `m0(model64, sha, contract_j, inputs, acts, z_net, basis, d_canon, perm, policy) -> dict`: the §7 row 9 checks in order (ids, `state_sha` = `CONTRACT["models"][j]["state_sha_f32"]`, round trip by `load_model64`, identity patch at three sites, rank, readout identity, two-route, attainability); failures → `"FAIL_TECHNICAL/MODEL"`, attainability → `"INCONCLUSIVE/NUMERICAL"`.

### 7.4 X1 (ephemeral; §2.7, §5.7)
- `x1(model64, arms: dict[str, tuple], basis, policy) -> dict`: `arms[name] = (inputs, y_hat, z_ref, seq_ids)` (`z_ref` None for a patched arm); for each arm `z = patched_logits(model64, inputs, "ln_final_out", placed(y_hat), policy, "x1")` and per row `‖z − closed_logits(y_hat)‖∞ ≤ 1e-9·max(1, ‖z‖∞)`; natural arms use `z_ref` (the natural forward logits of the arm's own history) in place of a patched forward. Returns only `{"arms": {name: {"max_dev", "n_over"}}, "ids_over": [sequence ids], "status": "PASS" | "FAIL_TECHNICAL/X1"}`; all logits are deleted before return; the function has no store access (T-POLICY). Interchange arms use arm 2's inputs (§19 item C-23). Arm names: `"nat_<role>"`, `"<problem>_<pair>_21"` (y_S^{2←1}) and `"<problem>_<pair>_12"` (y_S^{1←2}), `"rot_<m>_<sign>"`.

## 8. c2_code.py

### 8.1 FWL (§2.4)
- `harmonics(phi, K) -> float64[n, 2K]`: columns `(cos φ, sin φ, cos 2φ, sin 2φ, …, cos Kφ, sin Kφ)`.
- `standardise(z_fit) -> (mu, sd)` = `c1_fit.standardise_nuisance`; `zt = (z − mu)/sd`.
- `fwl(Y, w32, zt, f) -> dict`: `X = c1_fit.fwl_design(w32, zt, f)` (36 + 5 + 2K columns), `coef, _, rank, sv = np.linalg.lstsq(X, Y, rcond=None)`; keys `"alpha"` `[36, p]` (= coef[:36]), `"Gamma"` `[p, 5]` (= coef[36:41].T), `"B"` `[p, 2K]` (= coef[41:].T), `"rank"`, `"cond"` (sv[0]/sv[−1], inf if sv[−1] = 0), `"sv_B"`, `"resid"` `[n, p]`, `"K"`, `"p"`. `p` = 127 (R, R_K*, S*) or 128 (M).
- `f1_fwl(fit) -> str`: PASS iff rank = 41 + 2K, cond ≤ 1e8, sv_B[0] > 0 and sv_B[−1]/sv_B[0] ≥ 1e-6; else `"INCONCLUSIVE/PATCH_MODEL_DEGENERATE"`. No column is dropped.
- `ledoit_wolf(resid) -> float64[p, p]` = `x4f_scores.ledoit_wolf(resid)[1]`; `lw_ok(S) -> bool`: `λ_min > 1e-12·λ_max` (`np.linalg.eigvalsh`).
- `partial_r2(Y, w32, zt, f) -> float`: `1 − RSS(full)/RSS(base)` with base = `fwl_design(w32, zt, empty)` (the K-harmonic analogue of `c1_fit.partial_r2`).

### 8.2 GLS (§2.5; QR route)
- `gls(Gamma, B, Sigma=None) -> dict`: `Xn = [Gamma, B]`. GLS (Sigma given): `Lc = np.linalg.cholesky(Sigma)` (Σ = Lc Lcᵀ, R_Σ = Lcᵀ), `Xt = solve_triangular(Lc, Xn, lower=True)` (X̃ = R_Σ^{−ᵀ} X_n), `Qx, Rx = np.linalg.qr(Xt)` (reduced), `L = solve_triangular(Rx, solve_triangular(Lc, Qx, lower=True, trans="T").T)` (= R_x⁻¹ Q_xᵀ R_Σ^{−ᵀ}; `scipy.linalg.solve_triangular`); Euclidean (Sigma None): `Xt = Xn`, `L = solve_triangular(Rx, Qx.T)`. Keys `"L"` `[5+2K, p]`, `"L_G"` (rows 0..4), `"L_B"` (rows 5..), `"P_S"` (= B @ L_B), `"P_G"` (= Gamma @ L_G), `"P_rest"`, `"Xt"`, `"rank_Xt"` (`np.linalg.matrix_rank(Xt)`, default tolerance), `"cond_Xt"` (`np.linalg.cond(Xt, 2)`), `"status"` (PASS iff rank_Xt = 5 + 2K and cond_Xt ≤ 1e8, else `"INCONCLUSIVE/PATCH_MODEL_DEGENERATE"`).
- `gls_identities(g, Gamma, B, Sigma=None) -> dict` `{"max_abs", "ok"}`: the Lemma G1 identities (L Xn = I; P_S² = P_S; P_G² = P_G; P_S P_G = P_G P_S = 0; P_S Γ = 0; P_G B = 0; W P = Pᵀ W with W = Σ⁻¹, or I) by max-abs ≤ 1e-10.
- `interchange(y1, y2, P_S) -> (y_21, y_12)`: `y_21 = y2 + (y1 − y2) @ P_S.T` (arm 2 receives arm 1's code), `y_12 = y1 − (y1 − y2) @ P_S.T`.
- `code_pair(Y, alpha, w32, L_B) -> float64[n, 2K]` = `(Y − alpha[w32]) @ L_B.T`; `code_phase(Y, alpha, w32, L_B) -> (phi_c, modulus)` from its first two columns (`atan2`, Euclidean norm).
- `zero_code_threshold(mod_fit) -> float` = `1e-12·np.quantile(mod_fit, 0.5, method="inverted_cdf")` over the 8,192 FIT natural rows, per model and family.

### 8.3 R1 (§2.11, §6.6)
- `r1(phi_c_p, phi_c_m, mod_p, mod_m, m32_p, m32_m, thr_code) -> dict` `{"status": "PASS" | "FAIL", "agreement", "median", "n", "kappa_reg", "overrides": {"zero_mod": int, "zero_code": int}, "R1_ZERO": int, "R1_UNSELECTED": int}` on E_x rows: rows with ‖m32_p‖ ≤ 1e-12 or ‖m32_m‖ ≤ 1e-12 get both m32 inputs replaced by (1, 0); rows with mod_p ≤ thr_code or mod_m ≤ thr_code get both phase inputs replaced by 0.0; then `c1_gates.v1(phi_p, phi_m, m32_p, m32_m)` unchanged. PASS iff `Fraction(agreement) ≥ 3/4`. `kappa_reg = Σ δ_c·sign δ* / Σ |δ*|`. On rows without an override the wrapper passes `c1_gates.v1`'s inputs unchanged (bitwise). R1_ZERO counts selected rows with sign δ_c = 0 or sign δ* = 0; R1_UNSELECTED counts rows with |δ*| < median.

### 8.4 N2 (§2.10)
- `n2_fit(a2_fit, w32_fit) -> dict` `{"mu": [36, 128], "W": [128, 128], "q99": float, "status"}`: class means; `Σ_2w = x4f_scores.ledoit_wolf(a2 − mu[w])[1]`; `W = Σ^{-1/2}` (`eigh`, symmetric); `q99 = c1_gates.q99(dm(a2_fit, w32_fit))`. A class without FIT rows → status `"EXCLUDED/RADIAL_SUPPORT"`.
- `dm(h, w32, fit) -> float64[n]` = `‖(h − mu[w32]) @ W.T‖`.
- `n2_gate(fit, w32, D2: list, S: list, C: list) -> dict` `{"status", "F_D", "F_S", "F_C", "cap"}`: each list holds the (row, arm) states of the eligible rows (arms + and −); `F(·) = c1_gates.frac_beyond(dm(...), q99)` over the stacked pairs; `cap = max(1/20, F_D + 1/50)` (exact); PASS iff F_S ≤ cap and F_C ≤ cap, else `"EXCLUDED/RADIAL_SUPPORT"`.

### 8.5 Haar frames, S* features
- `haar_frames(j, count, p, Sigma) -> list[float64[p, p]]`: for r = 0..count−1, `Q = c1_fit.qr_pos(SeedTree(0).generator("c2-v1", "frame", int(j), int(r)).standard_normal((p, 6)))`, `P_R = S_half @ (Q @ Q.T) @ S_half_inv` with the symmetric square roots of Σ (`eigh`). R: count 32, p 127; M: count 8, p 128 (§19 item C-4).
- `fstar(m32, K) -> (float64[n, 2K], bool[n])` = `m_valid[:, None]·harmonics(phi_star, K)` with `(phi_star, m_valid) = c2_oracle.phi_star(m32)`; the L1* target is `fstar(m32, 1)[0]`.

## 9. c2_stats.py

### 9.1 GLS-REF (§2.5, §9.2; Lemmas GR, INV; T12)
- `dctx(prec=80) -> decimal.Context`: `ROUND_HALF_EVEN`, traps `Overflow`, `Underflow`, `Subnormal`, `DivisionByZero`, `InvalidOperation` (`Inexact`, `Rounded` not trapped).
- `D(M) -> list[list[Decimal]]`: exact `Decimal(float(x))` entries. `dmatmul(A, B)`, `dsub(A, B)`, `dabs(A)`, `frob(A) -> Decimal` (sqrt of the sum of squares in the context), `inflate(x) = x·(1 + 10⁻⁷⁰)`, `deflate(x) = x·(1 − 10⁻⁷⁰)`, `theta(q) = q·u_D/(1 − q·u_D)` with `u_D = ½·10^{1−p}`.
- `dsolve(A, Bm) -> list` (Gaussian elimination with partial pivoting, row pivot = largest |entry|, ties to the lowest index); `dinverse(A) -> list`.
- `enclosure(R_tilde, fixed, left, right, q) -> Decimal`: `inflate(frob(R_tilde)) + inflate(theta(q + 1)·frob(|fixed| + |left|·|right|))` (fixed may be None: `theta(q)·frob(|left|·|right|)`).
- `gls_ref(A, Gamma, B, P_S_hat, P_G_hat, euclidean=False, prec=80) -> dict` with keys (Decimal values as `str`): `"accepted"` (bool), `"status"` (`"PASS"`, `"EXCLUDED/NUMERICAL"`; the driver maps a variant to `"NOT_COMPUTED"`), `"trap"` (str or None), `"theta_A"`, `"theta_G"`, `"omega_A"`, `"omega_G"`, `"e_Y"`, `"e_L"`, `"L_star_norm"` (deflated), `"rho_ref"`, `"eps_P_S"`, `"eps_P_G"`, `"dev_S"`, `"dev_G"` (inflated ‖P̂ − P*‖_F), `"delta_P_S"` (= dev_S + eps_P_S), `"delta_P_G"`, `"gate_S"`, `"gate_G"` (bools: `delta_P ≤ 1e-8·deflate(‖P*‖_F)`), `"n"`, `"m"`. Steps exactly §2.5: Y* (`dsolve(A, Xn)`; Euclidean Y* = Xn), 𝒢* = Xnᵀ Y*, L* = `dsolve(𝒢*, Y*ᵀ)`, P*_S = B̂ L*_B, P*_Γ = Γ̂ L*_Γ; residuals R_A, R_C, R_G with enclosures (q = n, n, 5 + 2K); V_A = `D(np.linalg.inv(A))`, θ̄_A = enclosure of I − V_A A (q = n); V_G = `dinverse(𝒢*)`, e_G = ‖Xn‖_F e_Y + ‖R_C‖_F, θ̄_G = enclosure(I − V_G 𝒢*) + ‖V_G‖_F e_G; ω_A = ‖V_A‖_F / deflate(1 − θ̄_A), ω_G = ‖V_G‖_F / deflate(1 − θ̄_G); e_Y = ω_A ‖R_A‖_F; e_L per Lemma GR; ρ_ref = e_L / deflate(‖L*‖_F); ε*_P per §2.5. Accepted iff no trap, θ̄_A < 1 (GLS), θ̄_G < 1 and ρ_ref ≤ 10⁻²⁰. Every unverifiable condition counts as not accepted.

### 9.2 L1 decoders (§6.6)
- `class Decoder` (dataclass): `mu_F`, `s_F` (`x4f_scores.standardizer(F_fit)`), `W`, `b`, `lam`, `eq`, `tol`, `kappa`; `predict(F) -> float64[n, 2]` = `((F − mu_F)/s_F) @ W + b`.
- `fit_decoder(F_fit, Y_fit, panel_fit) -> Decoder`: `res = nested_ridge(F_fit, Y_fit, panel_fit, F_fit, Y_fit, grid=(1e-3, 1e-2, 1e-1, 1.0, 10.0))`; `Ft = (F_fit − mu_F)/s_F`; `probe = RidgeProbe([res.lam]).fit(Ft, Y_fit, Ft, Y_fit)`; `eq = max |probe.predict(Ft) − res.pred_val|`; `(tol, kappa) = c1_fit.equivalence_tolerance(Ft, res.lam, pred)`; equivalence holds iff `eq ≤ tol` (else F1 `"EXCLUDED/NUMERICAL"`).
- `decoder_features(kind, w32, zt, code=None, full=None) -> float64[n, ·]`: `"D0"` = `[onehot(w32), zt]` (41), `"Dcode"` = `[onehot, zt, code]` (41 + 2K, code = L_B y or L_{B₂} a₂ or L_{B*} y), `"Dlin"` = `[onehot, zt, full]` (41 + 127, or 41 + 128 for M).
- `decoder_arrays(dec) -> dict` / `decoder_from_arrays(d) -> Decoder` (npz round trip; keys as the dataclass fields).
- `l1(Y, pred0, pred_code, pred_lin) -> dict` `{"status", "SSE_0", "SSE_code", "SSE_lin", "R2_code_0", "rho_inc"}`: SSE sums over rows and both target coordinates; PASS iff SSE_0 > 0, SSE_0 − SSE_lin > 0, `Fraction(R2) ≥ 1/2` and `Fraction(rho) ≥ 9/10`; an undefined or nonpositive denominator → `"EXCLUDED/LINK"` (R2 and rho reported as None); else `"EXCLUDED/LINK"` on a failed threshold.
- `l1_complete_scores(Y, preds: dict, w32, class_means_fit) -> dict`: the descriptive R²_X = 1 − SSE_X / Σ ‖f₁ − f̄₁,w‖² and R²_code/R²_lin.

### 9.3 P1 (§6.7)
- `p1(family, arrays: dict[str, dict[int, float64[4096]]], afull: dict[int, float64[4096]], models, alpha) -> dict`: for each array name (R, S*: `"Z010"`, `"Z050"`; M: `"Ztau"`), `sd, _ = precision.sd_b4_draws(X=arrays[name], r4n=afull, models=models, seed=seed_sd, draws=5000, size=4096)`; for N in (4096, 8192, 16384): `e = precision.centered_draws(arrays[name], models, seed_c, 5000, N)`; `precision.precision_summary(sd, e, models, cfg)` with `cfg = {"alpha": float(alpha), "power": 0.80, "delta": 0.0, "alternative": 0.10·min_j mean(afull[j]), "projected_N": N}`. Seeds: R 620501 (sd) / 620502 (centred); M 620511 / 620507; S* 620512 / 620514 (§13.2). A model passes at N iff for every array `mde_upper ≤ alternative` and `power ≥ 0.80` in its `models[j]` entry. Returns `{"N_F": int | None, "pass": {N: [models]}, "status": "PASS" | "INCONCLUSIVE/UNDERPOWERED", "precision_limited": [models], "summaries": {name: {N: summary}}}` with N_F per §6.7.
- `mde_report(arrays, models, seed_sd, seed_c, alpha) -> dict`: the same kernels for the unrated arrays (energy, M-share), reported only.
- `n_test(N_by_family: dict) -> (int, int)`: N_test = max over alive families, k = N_test // 4096.

## 10. c2_attrib.py (closed forms; d = d_named; Δy = y¹ − y²)

- `half_dot(d, v) -> float64[n]` = `c1_endpoint.A_hat(d, v, np.zeros_like(v))` (½ Σ_v d_v v_v, ordered sum).
- `centre(v) = v − v.mean(axis=1, keepdims=True)`; `energy(v) = Σ centre(v)²`.
- `partition(d, M, dy, P_S, P_G) -> dict` `{"A_full", "A_S", "A_G", "A_rest"}` with `A_rest = A_full − A_S − A_G` (exact by definition).
- `energies(M, dy, P_S) -> dict` `{"e_full", "e_S"}`.
- `random_ref(M, Sigma, dy, e_full) -> dict` `{"r", "tau_K", "wtw"}`: `tau_K = trace(C M Σ Mᵀ C)`, `wtw = Δyᵀ Σ⁻¹ Δy` (Cholesky solve), `r = RS_A·e_full + RS_B·tau_K·wtw` (float of the Fractions).
- `null_projector(M) -> float64[127, 127]`: J = I − V_r V_rᵀ, V_r = the right singular vectors of C M for its `np.linalg.matrix_rank` rank (§19 item C-28).
- `decomposition(d, M, dy, P, J) -> dict` `{"A_vis", "A_null", "e_vis", "e_null"}` for P ∈ {P_S, P_G}; `nu_S(J, P_S, dy) -> float` = E‖J P_S Δy‖² / E‖P_S Δy‖².
- `psi_max(d, M, dy, E) -> float`: S = mean over all rows of `ind(Δy (Mᵀd)ᵀ)` (127 × 127), `sym = (S + Sᵀ)/2`, ψ_max = ½·(sum of the 6 largest eigenvalues)/mean(ind(A_full)).
- `cs_bound(d, e_S, E) -> float` = ½·(E‖d‖²)^{1/2}·(E e_S)^{1/2} (eligible rows); `abs_mean(A_S, E)`.
- `fisher_energy(M, dy, P_S, z_p, z_m) -> float64[n]`: v = C M P_S Δy, p̄ = ½(softmax(z_p) + softmax(z_m)).
- `affine_readouts(Y_fit, w32_fit, nu_fit) -> dict` `{"R_w": [127, 36], "R_nu": [127, 6]}` (OLS with intercept; §19 item C-26) and `readout_change(R, dy, P_S, E) -> float64[·]` = mean over E rows of `(Δy @ P_S.T) @ R`.
- Rotation: `rotation_block(K, theta) -> float64[2K, 2K]` (block k = [[cos kθ, −sin kθ], [sin kθ, cos kθ]]); `y_rot(Y, alpha, w32, B, L_B, theta) -> float64[n, 127]` = `Y + (f̂ @ (R_K(θ) − I).T) @ B.T`, `f̂ = (Y − alpha[w32]) @ L_B.T`; `rotation_arm(d_rot, M, y_p, y_m, G_rot, E) -> dict` `{"A_rot", "s_rot", "theta_rot"}` with `A_rot = half_dot(d_rot, (y_p − y_m) @ M.T)`, `s_rot = count(A_rot > 0 on E)/|E|`.
- C2-M: `cm_replacements(a2_H, a2_D, P2) -> dict` `{"F": a2_D, "S": a2_H + (a2_D − a2_H) @ P2.T, "C": a2_H + (a2_D − a2_H) @ (I − P2).T}`; `cm_quantities(d, z: dict, A_full) -> dict` `{"A_F", "A_S", "A_C", "e_F", "e_S", "e_C", "I_M", "A_ctx"}` from `z[X] = (z_X_plus, z_X_minus)`; `cm_placebo(dR, z_nat_H, z_S_R, z_F_R) -> dict` `{"AR_S", "AR_F"}`; `ln_scale_ratio(rep, a2_H, eps) -> float64[n]` = √(Var(rep) + eps)/√(Var(a2_H) + eps) (§19 item C-30).
- `desc_intervals(nums: dict[str, float64[n]], dens: dict[str, float64[n]], pairs: list[tuple[str, str]]) -> dict`: one `c1_means.bootstrap_means` call over all 24 arrays (seed 620518, 5,000 draws); per (num, den) pair the ratio of resampled means per draw; two-sided 95 % ranks 125 and 4,875 of the sorted ratio draws (`quantile_with_rank` at 1/40 and 39/40); `"UNDEFINED"` if the original or any resampled denominator is 0 or a value is non-finite (no draw discarded).
- `post_desc(arrays: dict) -> dict`: eligible-row point ratios only, each labelled `"unlicensed (gate <g>); computed after the outcome"`.

## 11. c2_decide.py

- `stream_bounds(arrays: dict[str, float64[n]], seed, alpha, draws=20000) -> dict[str, dict]`: one `c1_means.bootstrap_means(arrays, seed, draws)` call; per key `{"mean": c1_means.tree_mean(x), "L", "U", "rank_L", "rank_U"}` with `L, rank_L = quantile_with_rank(means, alpha)`, `U, rank_U = quantile_with_rank(means, 1 − alpha)`. Keys are `"<statistic>|<model>"` (statistics §11.1). Called twice per family on TEST with the same seed and n (RESP/SPEC first, then the endpoint arrays): the index streams are identical (T-BOOT). VAL gates call it with 5,000 draws and `VAL_ALPHA`.
- `guard(s, beta=0.0) -> float` = `1e-9·max(1, mean_i |s_i|) + beta`; `beta_A(d, M, dy, delta_P, coef) -> float` = `|coef|·max_i ½‖Mᵀd_i‖₂·δ_P·‖Δy_i‖₂`; `beta_E(M, dy, P_S, delta_P, coef) -> float` = `|coef|·max_i (2‖C M P̂_S Δy_i‖₂ + ‖CM‖₂ δ_P ‖Δy_i‖₂)·‖CM‖₂ δ_P ‖Δy_i‖₂` (§9.2; δ_P from the problem's GLS-REF as float of the Decimal upper bound). M statistics use `beta = 0` (§19 item C-44).
- `sign(b, g) -> int`: +1 iff b > g, −1 iff b < −g, else 0 (`NUMERICALLY_UNRESOLVED`).

### 11.1 Statistics (per model; indicator form; TEST)
R stream (seed 620503): `V3x` = ind(A_full − 0.30·G_x, E_x); `Y1` = ind(A^R_S − 0.10·A^R_full, E_y); `Z010`, `Z050` = ind(A_S − c·A_full, E_x); `Vabs` = ind(e_S − 0.10·e_full, E_x); `Vrand` = ind(e_S − (127/60)·r, E_x); `NEG` = ind(A_S, E_x); variants `<v>:Z010`, `<v>:Z050`, `<v>:Vabs`, `<v>:Vrand` for v ∈ VARIANTS (19 arrays per model). M stream (620513): `V3x`, `Ztau` = ind(A_M,F − 0.10·A_full, E_x), `ZM010`, `ZM050` = ind(A_M,S − c·A_M,F, E_x), `VM` = ind(e_M,S − 0.10·e_M,F, E_x), `Y2` = ind(A^R_M,S − 0.10·A^R_M,F, E_y), `NEG` = ind(A_M,S, E_x) (7). S* stream (620516): as R primary with the S* projector (`V3x`, `Y1*`, `Z010`, `Z050`, `Vabs`, `Vrand`, `NEG`; 7). Rotation (620517, 5,000 draws, report): `A_rot|<m>|<model>`, `G_rot|<m>|<model>` (12). Coefficients are the exact Fractions as floats.

### 11.2 Per-model and overall rules (§6.3–§6.5)
- `r_model(b: dict, y_active: bool) -> dict` `{"status", "resp", "spec", "coarse": {"gt010", "lt050"}, "negative", "unresolved": [str], "endpoint_formed": bool}` from the signed bounds of §11.1 (each `sign(L or U, g_s)`): rule 1 RESP undeclared (sign(L(V3x)) ≠ +1) → `"EXCLUDED/MODEL_HEADROOM"`; rule 2 Y1 active and SPEC undeclared (sign(U(Y1)) ≠ −1) → `"EXCLUDED/NUISANCE_IN_S"`; then the category of the §6.3 table (USED: L(Z050) > g and L(Z010) > g; PARTIAL: L(Z010) > g and U(Z050) < −g; NOT_USED: U(Z010), U(Z050), U(Vabs), U(Vrand) all < −g; LOW_ALIGNED: U(Z010) < −g and U(Z050) < −g and not both energy bounds < −g); else `"INC/NUMERICAL"` if any of L/U(Z010), L/U(Z050) is NUMERICALLY_UNRESOLVED, else `"INC"`. `negative` iff sign(U(NEG)) = −1 (after rule 1). `coarse` only when RESP and (SPEC or Y1 inactive) are declared. The same function serves S* (`Y1*`).
- `m_model(b, y2_active) -> dict`: §6.4 M rules 1–7 in order (RESP in the M stream; Y2 as SPEC; ROUTED iff U(Ztau) < −g; else if L(Ztau) > g the four UPSTREAM categories on ZM010, ZM050, VM; else `"INC"`/`"INC/NUMERICAL"`).
- `variant_category(b, variant, primary) -> str`: the R category rule on the variant arrays, with the primary RESP/SPEC declarations as prerequisites; feeds `PROJECTOR_DEPENDENT` (R_E) and `HARMONIC_DEPENDENT` (R_K1, R_K2); `"NOT_COMPUTED"` if the variant failed F1 or GLS-REF.
- `overall(family, statuses: dict[int, str], cnhs: list) -> str`: §6.5 rules 1–4 (M: ≥ 2 ROUTED → `"ROUTED_AROUND"` first).
- `endpoint_status(model, family, gate_history) -> str`: `"SCORED"`; `"NOT_RUN/<gate>"` for an exclusion before ACCEPT, at T-PRE or at RESP-SPEC, or a stopped family; `"SEALED_UNSCORED/<gate>"` only for arrays lawfully formed before a later stop.
- `qualifiers(family, per_model, variants, y_active, p1) -> list[str]` (§3.1 order).
- `licence(family, outcome, values) -> str`: the §3 sentence of the outcome, verbatim, with every bracket `[…]` replaced in order by the formatted value (`format(x, ".4g")` for numbers; models as `"1729, 2718"`; bounds as `"(L, U)"`), followed by one space and the family's Q-CODE clause verbatim (R: §3 text; M: "…defined by the layer-2 fit and projector…"; S*: "…defined by the oracle x-phase fit and projector…"). The NOT_USED sentence keeps "the contribution may be negative, i.e. opposing"; ROUTED_AROUND keeps the RC-5 sentence verbatim; no template contains "below 10% in magnitude". `values` keys per outcome are the bracket names of §3 (`k`, `list`, `other`, `psi_hat`, `lower`, `upper`, `tau_hat`, `psi_M_hat`, `gate`, `values`, `statuses`, `models`, `registration`, `R2_code_0`, `rho_inc`, `intervals`, `theta_rot`, `interval`, `s_rot`, `m`).

## 12. c2_driver.py

### 12.1 Gate order (§7; NEW-2) and the policy
`GATE_ORDER` (exact names; stage): `IMPL` (record), `AUTH-ADMIT` (S1), `G0`, `PF`, `H1`, `REG`, `H2`, `H3`, `H4`, `H5` (S1); `M0`, `C0c`, `F1` (S2); `C0v`, `L1`, `R1`, `N2`, `SURVIVAL` (S3); `X1`, `V3x`, `V3y`, `Y1`, `Y1*`, `Y2`, `P1` (S4); `ACCEPT` (coordinator record); `REG2` (REG′/H2′), `T-PRE`, `T-PRE-MODEL`, `RESP-SPEC`, `NUM`, `ENDPOINT`, `REPORT` (S5). Per-family gates carry the `family` field (`L1`/`R1` with family "M" are the protocol's L1-2/R1-2, with "S*" L1*/R1*); per-problem gates (`F1`) carry `problem`; per-model gates carry `model`.

`STAGE_ENTRY = ("AUTH-ADMIT", "G0")`: run at the start of every stage (S1–S5; G0 item (vii) with `first_sampling` only at S1), recorded with the `stage` field; they do not move the order position. `class LogitPolicy(done=())` (`done` = the distinct gate names of `GATES.jsonl` in first-record order, so a new process resumes the position): `begin(gate)` accepts a `STAGE_ENTRY` gate at a stage start, the last begun gate again (another model, family or problem of the same gate), or the next gate of `GATE_ORDER`; anything else, or a `begin` while another gate is current, raises `C1GateFailure("FAIL_TECHNICAL", …)`. Every gate of the order is begun, also when it is inactive or skipped (then recorded `NOT_RUN`); `ACCEPT` is entered by `release_ok` of `RELEASE_R5.json`. `end(gate)` closes the current gate whatever its status. `require(kind)` with `ALLOWED = {"m0": {"M0", "T-PRE"}, "x1": {"X1", "T-PRE"}, "val_gate": {"V3x", "V3y", "Y1", "Y1*", "Y2"}, "val_sealed": {"P1"}, "test_endpoint": {"RESP-SPEC", "NUM", "ENDPOINT", "REPORT"}}` (test_endpoint also requires `"T-PRE"` and `"T-PRE-MODEL"` in `done`); `require_write(kind)` refuses any endpoint-array or summary write while the current gate is `X1` or `T-PRE` (`"INVALID/LEAKAGE"`). Closed-form logits count as logits: no FEAS logit and no FIT logit outside the M0 rows are formed. `check_sequence(gates_jsonl) -> bool`: the recorded gate sequence is a prefix-consistent subsequence of `GATE_ORDER`. Refusals: SYMBOL-ORDER (a) before H2's sampling and separation, (c) before H3's FIT contrasts, the two-route check before M0, any FIT sampling before REG PASS (T-POLICY).

### 12.2 Stage functions
`run_stage(stage, ctx) -> dict` for `stage ∈ ("S1", "S2", "S3", "S4", "S5")`; `ctx` (dataclass `Ctx`: `store`, `worktree`, `head`, `job`, `task_sha256`, `session`, `release`, `policy`, `data`). Each stage: `begin_stage` → gates in order through `run_gate` → `complete_stage` → `write_manifest`. A study-scope non-PASS stops the stage (later gates `NOT_RUN`); model-scope results exclude the model from the named families (§7 scope rule, S5) and the family continues iff ≥ 2 models remain.
- `run_gate(ctx, gate, fn, scope, model=None, family=None, problem=None) -> dict`: calls `fn()`; an exception → `c1_records.classify_exception`; records one `GATES.jsonl` line via `stage_records.record_gate(store, gate, status_head, full_status=..., reason=..., values=..., stage=..., model=..., family=..., problem=...)` (`status_head` = `c2_config.status_of(full)[0]`); `scope ∈ ("study", "model", "family")`.
- `begin_stage(ctx, stage)`: refuses (STAGES.jsonl `"REFUSED"` event, `StageRefused`) a second attempt, a missing or mismatched release, an incomplete prerequisite stage, changed evidence of the prerequisite, or a prior study-scope stop. `complete_stage(ctx, stage, files)`: `"COMPLETED"` event with `evidence` {relpath: sha256}.
- S1 = AUTH-ADMIT, G0, PF, H1, REG, H2 (sampling FIT 2 blocks, FEAS, VAL; `separation`; `first_token_ok`; SYMBOL-ORDER (a)), H3 (oracle for FIT, FEAS, VAL; H3), H4 (f_x, f_y ≥ 0.90 on FIT, FEAS, VAL; tally), H5 (VAL lower 0.05 bounds of the eligible-row means of G_x over E_x and G_y over E_y, `c1_means.c1_bootstrap_means(G[E], PCG64(620505), 5000)` twice, rank 250, `> 1/100`; writes `oracle/ORACLE_FROZEN.json` with s_max, κ_ν, κ_m, `y_active`).
- S2 = per model M0; C0c; F1 for the six problems (FWL, LW, whitened design, identities, GLS-REF, decoders D0/Dcode/Dlin of R, M, S* with equivalence, N2 fit, m̃ thresholds, J, affine readouts).
- S3 = C0v, L1 (R, M, S*), R1 (R, M, S*), N2, SURVIVAL.
- S4 = X1, V3x (seed 620504), V3y (620508), Y1 (620509), Y1* (620515), Y2 (620510), P1 (sealing of the VAL endpoint bundle, §16.1).
- S5 = REG2 (C2-REG2, k TEST blocks, separation against C2-REG2, `first_token_ok`, SYMBOL-ORDER (a)), T-PRE (study, in the §7 row 23 order; H5 seed 620506), T-PRE-MODEL (Sup(TEST) ≥ 0.99; L1, R1 with the frozen FIT decoders; N2), RESP-SPEC, NUM, ENDPOINT (R, M, S*, variants, NEGATIVE, rotation), REPORT (licences, unsealing, descriptives, C2-M intervals 620518, POST-DESC).

### 12.3 G0 (§7 row 1) and AUTH-ADMIT (row 0b)
- `auth_ok(store) -> bool`: `AUTH.json` exists, parses, schema `"c2-auth-v1"`, `protocol_sha256` = PROTOCOL_SHA256, `owner_record.sha256` = AUTH_SHA256, every §16.2 AUTH field non-empty. Never raises for these cases.
- `g0(ctx) -> dict` items `"i"`…`"viii"` → `{"status", "detail"}` and `"status"` (PASS iff all PASS): (i) `PROTOCOL_C2_v1.md` sha256 = PROTOCOL_SHA256 and equal bytes to the mailbox file; (ii) `CONTRACT.json` sha256 = FREEZE.json `contract_sha256` and `CONTRACT["hashes"]["state_sha_f32"]` = the §4 strings; (iii) every `CONTRACT["hashes"]["reused_blobs"]` path's blob sha256 at H (the §13.1 values) and every `hashes.reused_extra` path's (values at R; §19 item C-46); (iv) K4 FREEZE sha256, kernel blobs, C1′ CONTRACT sha256; (v) chart NPZ sha256 (§2.4); (vi) `c2_data.namespace_scan`; (vii) `c2_data.store_admission(first_sampling = stage == "S1")`; (viii) dispatch identity (`task_sha256` = sha256 of `agent-handoff/jobs/<job>/task.md`, `session` non-empty, the release names this job and task sha256), `meter_bind_check`, import directory (`c2_config.__file__` under `<worktree>/tools/c2_readout`, `meter` module under `<worktree>/tools/x4_oracle_profile`). Failure classes: AUTHORITY (i–v, viii), LINEAGE (vi, vii). G0 runs at the start of every stage (S1 checks (vii) with `first_sampling=True`).
- `meter_bind_check(path, expected_sha256, import_dir) -> None`: raises `RuntimeError` if the store-local `c2_meter_bind.py` sha256 differs from FREEZE.json `meter_bind_sha256` or the meter would import from a directory other than `<worktree>/tools/x4_oracle_profile`.
- `pf(ctx) -> dict`: `python -s -m pytest tests/{learner, dataset, contracts, oracle, process, world, analysis, prediction, experiment, circle_history, c1prime, c1prime_registry, c2_readout} -p no:cacheprovider --basetemp <SCRATCH_ROOT>/<job>/pt` with `TEMP`, `TMP`, `TMPDIR` = `<SCRATCH_ROOT>/<job>/tmp`, `PYTHONPATH=<worktree>/src`; then `tools/check_file_sizes.py` and `tools/check_imports.py`; all exit 0 → PASS, else `"FAIL_TECHNICAL/PF"`; records the TEMP and basetemp paths (both outside `PROJECT_ROOT`).

### 12.4 Sealing
- `seal(ctx, name, arrays) -> str`: exclusive create `sealed/<name>.npz` (`stage_records.save_npz`), returns its sha256, recorded in `stages/S4/SEALED.json`; `require_write("val_sealed")` first.
- `unseal(ctx, name, sha256) -> dict`: refused (`RuntimeError`, `"INVALID/LEAKAGE"`) unless every alive family's ENDPOINT gate record exists (the fresh outcome is recorded) or a study stop record exists; the file must re-hash to `sha256`.

### 12.5 Lineage (§11)
- `write_manifest(ctx, stage) -> Path`: exclusive create `manifests/<job>.json` (§16.2). `recognised(store) -> dict[str, str]`: the lineage map {relpath: sha256} from FREEZE.json, AUTH.json, RELEASE_R*.json, the accepted manifests and `superseded/*/SHA256SUMS` (§16.2).
- `supersede(ctx, job, attempt, paths, ruling) -> Path`: moves the listed files to `superseded/<job>-a<k>/` (same relative layout), writes `SHA256SUMS` and `SUPERSEDED.json`; nothing is deleted.
- `regen_compare(ctx, path, archived_sha256) -> bool`: bit-identical regeneration check of an unaffected artifact (else FAIL_TECHNICAL/LINEAGE).

### 12.6 Release binding
`release_ok(ctx, stage) -> dict`: `RELEASE_R<k>.json` (k = stage number; R3 and R4 may be issued together, §19 item C-20) exists, parses, schema `"c2-release-v1"`, names the stage, this job, the task sha256, H, the protocol sha256 and the FREEZE.json sha256; R5 also carries `N_test`, `k` equal to the S4 P1 record and `accept_review_sha256`.

### 12.7 CLI
`main(argv=None) -> int`: `python -s tools/c2_readout/c2_driver.py <stage> --store <store> --job <id> --task-sha256 <hex> --session <id>` (stage ∈ S1–S5), normally under the meter: `python -I <store>/c2_meter_bind.py --label <stage>__run --max-cpu inf -- <venv python> -s tools/c2_readout/c2_driver.py …` with `PYTHONPATH=<worktree>/src` (§13.4). Exit 0 on a recorded result (including a model- or family-scope exclusion), 2 on a study-scope stop, 3 on a refusal (no gate record written).

### 12.8 Store-local `c2_meter_bind.py`
Placed by the coordinator before S1 (its sha256 in FREEZE.json), modelled on `tools/c1prime/c1_meter_bind.py` (`3c1439fc5e053091c683c863ad7b5f0b3fe56253eb2394c57e62fdb0c4b1458d`): standard library only, run with `-I`; rebinds module-level names of the unchanged job-0014 `meter`, `controls`, `winjob` (job id, task digest, store paths, `CAP_S = STOP_NEW_S = inf`, `--max-cpu inf --max-wall inf`, the disk floors C: 2 GB and X: 30 GB, the worker session); fail-closed if its own sha256 or the meter import directory differs. `cpu_ledger.json` is pre-created (schema `x4-oracle-profile-ledger-v1`).

## 13. Random streams, seeds and scope

### 13.1 Named streams (all `SeedTree(0)`; integer scope values as Python `int`)

| Use | Stream | Draws |
|---|---|---|
| Histories, split s, block b | `generator("data", "c2-v1", s, b, "cylinder", "overlap", "1.25")` | one `HMMSampler.sample(4096, rng)` |
| R Haar frame r of model j | `generator("c2-v1", "frame", j, r)`, r = 0..31 | `standard_normal((127, 6))` |
| M Haar frame r of model j | `generator("c2-v1", "frame", j, r)`, r = 0..7 | `standard_normal((128, 6))` |
| RFF decoder of f₁ from P_rest y (descriptive) | `c1_fit.fit_decoder(..., model_seed=j, target="c2-rest-f1")` (its own `SeedTree(0)` streams, §19 item C-27) | as `fit_decoder` |

No other stream. TEST blocks are sampled only after ACCEPT (RELEASE_R5.json present).

### 13.2 Bootstrap seeds (PCG64; `CONTRACT["seeds"]`)

| Name | Seed | Use |
|---|---|---|
| `val_p1_R_sd` / `val_p1_R_c` | 620501 / 620502 | VAL P1 for R (`sd_b4_draws` / `centered_draws`) |
| `test_R` | 620503 | TEST R family stream (19 arrays per model, §11.1) |
| `val_V3x` | 620504 | VAL V3x |
| `val_H5` / `test_H5` | 620505 / 620506 | H5 (G_x and G_y; two calls with the same seed) |
| `val_p1_M_c` / `val_p1_M_sd` | 620507 / 620511 | VAL P1 for M (centred / SD) |
| `val_V3y` | 620508 | VAL V3y |
| `val_Y1` | 620509 | VAL Y1 |
| `val_Y2` | 620510 | VAL Y2 and its activity check |
| `val_p1_S_sd` / `val_p1_S_c` | 620512 / 620514 | VAL P1 for S* (SD / centred) |
| `test_M` | 620513 | TEST M family stream |
| `val_Y1s` | 620515 | VAL Y1* |
| `test_S` | 620516 | TEST S* family stream |
| `test_rot` | 620517 | TEST rotation arm (5,000 draws, report) |
| `test_M_desc` | 620518 | TEST C2-M descriptive intervals (5,000 draws, 24 arrays) |

## 14. Sequence-id codes (§5.2)
`code = process_code("cylinder", "overlap", "1.25", f"c2-v1/{split}/b{block}")`; ids `make_sequence_ids(code, "test", 4096)` = `(code << 32) | (3 << 28) | index` (split code of `"test"` = 3).

| split/block | code | first id | last id |
|---|---|---|---|
| fit/b0 | 1330034805 | 5712455990822043648 | 5712455990822047743 |
| fit/b1 | 1413089761 | 6069174310612762624 | 6069174310612766719 |
| feas/b0 | 586295093 | 2518118251045584896 | 2518118251045588991 |
| val/b0 | 1860234253 | 7989645280339296256 | 7989645280339300351 |
| test/b0 | 1551631348 | 6664205895913701376 | 6664205895913705471 |
| test/b1 | 696827854 | 2992852844677169152 | 2992852844677173247 |
| test/b2 | 1649812666 | 7085891445801877504 | 7085891445801881599 |
| test/b3 | 1883241381 | 8088460142674182144 | 8088460142674186239 |

"Lowest-sequence-id rows" are taken over the whole split (FIT: both blocks).

## 15. Gate records and report keys

### 15.1 GATES.jsonl and STAGES.jsonl
Gate line keys: `gate`, `status` (head), `criterion_met` (`status == "PASS"`), `utc` (from `stage_records.record_gate`), plus `full_status`, `reason`, `stage`, `model` (int or null), `family` (or null), `problem` (or null), `scope`, `values` (JSON-safe; arrays of more than 64 entries as `"<array shape>"`). Stage lines: `stage`, `event` (`"STARTED"`, `"COMPLETED"`, `"REFUSED"`), `utc`, and `evidence` (COMPLETED) or `reason`, `integrity` (REFUSED).

### 15.2 Report `stages/S5/report.json`
Keys: `protocol_id`, `protocol_sha256`, `contract_sha256`, `R`, `head`, `study` (`"VALID"` or `"INVALID/…"`), `union_bound_display` (`"0.15"`), `families` → `{"R", "M", "S*"}` each `{"outcome", "licence", "qualifiers": [str], "coarse": {"gt010": {"count", "all3"}, "lt050": {…}}, "N_F", "per_model": {j: {"status", "endpoint_status", "bounds": {stat: {"mean", "L", "U", "rank_L", "rank_U", "g"}}, "signs": {stat: -1|0|1}, "point": {...}, "variants": {v: category}}}}`, with `point` holding the eligible-row ratios (R, S*: `psi`, `theta_full`, `psi_G`, `psi_rest`, `theta_S`, `eta_S`, `eta_R_bar`, `g`; M: `tau_M`, `psi_M`, `eta_M`, `psi_M_C`); `rotation` → `{j: {m: {"theta_rot", "interval", "s_rot"}}}`; `gates` (gate → list of `{model, family, status}`); `coverage` (split → tally); `descriptives` (`nu_S`, `psi_max`, `abs_A_S`, `cs_bound`, `decomposition`, `haar_shares`, `fisher_energy`, `y_partition`, `norm_ratio`, `partial_r2`, `l1_complete`, `rff_rest`, `readout_change`, `cm_intervals`, `cm_haar`, `ln_scale_ratio`); `val_unsealed` (VAL point values per family and model, secondary); `post_desc` (or null); `sealed_released` (name → sha256); `env` (python, numpy, torch versions, threads); `cpu_s`, `wall_s`.

## 16. Store layout, lineage manifest, registry manifest

### 16.1 Static output manifest (`c2-readout-store/`, §11 item 1)
Before S1 (coordinator): `FREEZE.json`, `AUTH.json`, `RELEASE_R1.json`, `c2_meter_bind.py`, `cpu_ledger.json`. Meter bookkeeping: `logs/**`, `cpu_ledger.json`, `RUN.lock`, `OPERATION_ACTIVE.json`, `OPERATIONS.jsonl`, `METER_ACTIVE.lock` (§19.5), `LOCK_RELEASED_*.json`.
- **S1:** `registry/C2-REG1.json`, `registry/C2-REG1_digests.npz`, `registry/runs/C2-REG1/run_*.npy`; `hist/HIST_fit_b0.npz`, `hist/HIST_fit_b1.npz`, `hist/HIST_feas_b0.npz`, `hist/HIST_val_b0.npz` (keys of `c2_data.history_table`); `oracle/ORACLE_<split>.npz` for fit, feas, val (keys `<role>_q`, `<role>_qbar`, `<role>_s`, `<role>_le`, `<role>_m32` for the four roles, `H_b31`, `H_b32`, `H_nuis`, `G_x`, `G_y`, `E_x`, `E_y`, `sequence_id`); `oracle/ORACLE_FROZEN.json`; `stages/S1/{record.json, pf.json, coverage.json}`.
- **S2:** `fits/FIT_<j>.npz` (`Q0`, `M`, `beta`, `gamma`, `WU`, `WUbeta`, `zt_mu`, `zt_sd`, `J`, `aff_w`, `aff_nu`, `n2_mu`, `n2_W`, and per problem p: `<p>_alpha`, `<p>_Gamma`, `<p>_B`, `<p>_Sigma` (absent for R_E), `<p>_L`, `<p>_P_S`, `<p>_P_G`, `<p>_mtilde`); `fits/FIT_<j>.json` (ranks, conds, LW ratios, identities, GLS-REF dicts, F1 statuses, `n2_q99`); `fits/DEC_<j>.npz` (`<family>_<D0|Dcode|Dlin>_<field>`); `stages/S2/ACT_FIT_<j>.npz` (`H_rp2`, `H_rp3`, `H_ln`, phases `H_phi`); `stages/S2/record.json`.
- **S3:** `CHART_CONSTRUCTIONS.json` (`c1_chart.ConstructionLedger`, role `"direct"` only, ≤ 3 claims); `stages/S3/DIRECT_<j>.npz` (`c1_chart.serialise(direct, None, "direct")`); `stages/S3/ACT_FEAS_<j>.npz` (`<role>_<hook>` for H, Hp, Hm; `<role>_phi`, `<role>_supported`); `stages/S3/{record.json, coverage.json}`.
- **S4:** `sealed/ACT_VAL_<j>.npz` (four roles × three hooks); `sealed/VAL_<family>_<j>.npz` (the endpoint arrays and the C2-M patched logits; family ∈ R, M, Sstar, ROT); `stages/S4/{record.json, gates.json, P1.json, coverage.json, SEALED.json}`.
- **S5:** `registry/C2-REG2.json`, `registry/C2-REG2_digests.npz`, `registry/runs/C2-REG2/…`; `hist/HIST_test_b<k>.npz`; `oracle/ORACLE_test.npz`; `stages/S5/ACT_TEST_<j>.npz`; `stages/S5/{tpre.json, bounds.json, report.json, record.json}`; `stages/S5/ENDPOINT_<family>_<j>.npz` (admitted models only); `stages/S5/POST_DESC.json` (only when run).
- Always: `GATES.jsonl`, `STAGES.jsonl` (append-only), `manifests/<job>.json`, `manifests/<job>.accepted.json` (coordinator), `superseded/<job>-a<k>/…`.

### 16.2 Lineage manifest schema
- `FREEZE.json` (coordinator, at H): `{"schema": "c2-freeze-v1", "protocol_id", "protocol_sha256", "addenda_sha256": [..], "R", "H", "branch", "worktree", "api_sha256", "contract_sha256", "test_plan_sha256", "modules": {name: {"sha256", "lines"}}, "tests": {path: sha256}, "protected_diff_R_H": [lines], "meter_bind_sha256", "meter_import_dir", "coordinator", "created_utc"}`.
- `AUTH.json` (coordinator): `{"schema": "c2-auth-v1", "protocol_sha256", "owner_record": {"path", "sha256", "owner_verbatim", "granted_utc"}, "budget": {"central_cpu_h": 2.1, "range_cpu_h": [0.9, 4.8], "cpu_policy": "measure-only, --max-cpu inf"}, "coordinator", "written_utc"}`.
- `RELEASE_R<k>.json` (coordinator): `{"schema": "c2-release-v1", "release", "stages": [..], "job", "task_sha256", "head", "protocol_sha256", "freeze_sha256", "N_test", "k", "accept_review_sha256", "coordinator", "utc"}` (the last three null before R5).
- `manifests/<job>.json` (job): `{"schema": "c2-manifest-v1", "job", "stage", "head", "files": {relpath: sha256}, "append_only": {"GATES.jsonl": sha256, "STAGES.jsonl": sha256}, "utc"}`; `manifests/<job>.accepted.json` (coordinator): `{"job", "manifest_sha256", "review_path", "review_sha256", "coordinator", "utc"}`.
- `superseded/<job>-a<k>/SHA256SUMS` (`<sha256>  <relpath>` lines) and `SUPERSEDED.json` (`{"job", "attempt", "defect", "ruling_path", "ruling_sha256", "moved": [relpath]}`).
- **Recognised files** (namespace "LINEAGE" class, store admission): the coordinator records above (by name, schema and the protocol sha256), meter bookkeeping (by path), every file of an accepted manifest with its sha256 (append-only files: the sha256 of the latest accepted manifest), and every superseded file listed in its `SHA256SUMS`.

### 16.3 Registry manifest `registry/C2-REG<v>.json`
`{"version", "registry_version": "c2-reg-v1", "status", "problems": [str], "n_digests", "digests_sha256" (sha256 of the sorted newline-joined hex digests), "seq_id_union_sha256", "digest_file_sha256", "x6": {"n", "digest_sha256" (DigestSet.sha256()), "base_manifest_sha256", "runs": [{"file", "sha256"}], "files": [...], "other": [...]}, "union_sha256" (sha256 of `digests_sha256 + "\n" + x6.digest_sha256`), "sources": [{"name", "path", "sha256", "kind", "n", "canonicalisation"}], "classes", "inventory": {"status", "unlisted", "violations"}, "sealed_ranges", "d2a_ranges", "predicates", "coverage", "handoff_validation", "k4b_store", "built_utc", "protocol_sha256"}`.

## 17. Gate table (§7; scope and failure statuses)

| # | Gate | Scope | Failure status |
|---|---|---|---|
| 0b | AUTH-ADMIT | study | do not run (refusal, exit 3) |
| 1 | G0 | study | FAIL_TECHNICAL/AUTHORITY or /LINEAGE |
| 2 | PF | study | FAIL_TECHNICAL/PF |
| 3 | H1 | study | FAIL_TECHNICAL/IDENTITY |
| 4 | REG | study | INCONCLUSIVE/REGISTRY_INCOMPLETE (FAIL_TECHNICAL/LINEAGE on a binding mismatch) |
| 5 | H2 | study | FAIL_TECHNICAL/LINEAGE; (a) FAIL_TECHNICAL/IDENTITY; predicate INCONCLUSIVE/REGISTRY_INCOMPLETE |
| 6 | H3 | study | FAIL_TECHNICAL/ORACLE, INCONCLUSIVE/NUMERICAL; (c) FAIL_TECHNICAL/IDENTITY |
| 7 | H4 | study | INCONCLUSIVE/ELIGIBILITY |
| 8 | H5 | study | INCONCLUSIVE/HEADROOM |
| 9 | M0 | study | FAIL_TECHNICAL/MODEL; INCONCLUSIVE/NUMERICAL (attainability) |
| 10 | C0c | model (R, M) | FAIL_TECHNICAL/AUTHORITY (hash, study); EXCLUDED/CHART_UNAVAILABLE |
| 11 | F1 | model (family of the problem) | EXCLUDED/PATCH_MODEL_DEGENERATE or EXCLUDED/NUMERICAL; variant NOT_COMPUTED |
| 12 | C0v | model (R, M) | EXCLUDED/CHART_UNAVAILABLE |
| 13 | L1 | model (family) | EXCLUDED/LINK |
| 14 | R1 | model (family) | CNHS |
| 15 | N2 | model (M) | EXCLUDED/RADIAL_SUPPORT |
| 16 | SURVIVAL | family | family stops (INCONCLUSIVE/<reason>, or CIRCLE_NOT_HISTORY_SENSITIVE / CNHS-2 / X_PHASE_NOT_HISTORY_SENSITIVE) |
| 17 | X1 | study | FAIL_TECHNICAL/X1 |
| 18 | V3x, V3y | model | V3x: EXCLUDED/MODEL_HEADROOM (all families); V3y: Y1/Y1*/Y2 inactive |
| 19 | Y1, Y1*, Y2 | model (family) | EXCLUDED/NUISANCE_IN_S |
| 20 | P1 | family | INCONCLUSIVE/UNDERPOWERED; PRECISION_LIMITED(j) |
| 21 | ACCEPT | study | stop (no RELEASE_R5.json) |
| 22 | REG2 | study | FAIL_TECHNICAL/LINEAGE; (a) FAIL_TECHNICAL/IDENTITY |
| 23 | T-PRE | study | INCONCLUSIVE/TEST_GATE (endpoints NOT_RUN/T-PRE); FAIL_TECHNICAL for identity, lineage, X1 |
| 24 | T-PRE-MODEL | model | EXCLUDED/TEST_GATE (endpoint NOT_RUN/T-PRE) |
| 25 | RESP-SPEC | model | EXCLUDED/MODEL_HEADROOM or EXCLUDED/NUISANCE_IN_S (endpoint NOT_RUN/RESP-SPEC) |
| 26 | NUM | model | INC/NUMERICAL for the affected statement |
| 27 | ENDPOINT | family | outcome |
| 28 | REPORT | — | — |

## 18. Frozen registry source and exclusion inventory (O-7, §5.3, §14 D7)

Inventoried on 2026-10-21 by file names and JSON metadata only (no array payload, no `sealed/` opened). Every top-level directory under `X:/Downloads/projects/topo-pilot/` is listed. **READER**: the named reader reads the history-bearing content at REG (and again at REG2). **EXCLUSION**: the directory holds no history tokens; the run-time inventory (`k4b_registry.inventory`, npz headers) must class it `NOT_SCANNED` or REG is INCOMPLETE (§5.2). A directory created later and absent from this table is admitted only if the run-time inventory finds nothing history-bearing in it (§5.2 rule iii). Machine-readable copy: `CONTRACT.json` `registry.inventory`.

| Directory | Decision | Reader / reason |
|---|---|---|
| `agent-handoff` | READER `c` | mailbox JSON (≈ 1,700 files): `k4b_registry.source_c` (parse check, then 32/33-element integer lists) |
| `c1prime-store` | READER `d` | C1′ HIST_cal_b0 (`d80ad5f42e333b4dc910667c0465cf03adc66518a22e961dec50a8eca2d5ba5e`, holds the 512 chart landmarks), HIST_cal_b1 (`7b33b3726ff26617b5ad86c55e6ed5a52da9c177d433aef5ea771fd47d19284a`), HIST_val_b0 (`97db9467927ba4edd9460a51cf537584d13afb2a5a002c5341f74ff7ed476616`), roles H, H⁺, H⁻, plus registry_v1 (`ebcebe186103d7a4ed01d8f011c05742419f9f418af03775549a80d0d5c77d9e`): `k4b_registry.source_d`. ORACLE/CERT/CHART npz hold oracle values, certificates and landmark activations of the same rows |
| `chart-diag-store-0023` | READER `b` | empty record (history ids of E4 panels; coverage-checked): `c1_registry_sources.store_sources` |
| `circular-audit-store` | EXCLUSION | one MetricRecords object (circ-audit-v1); no history arrays (K-REG2 class NOT_SCANNED) |
| `coord-scratch` | EXCLUSION | coordinator scripts, logs, JSONL; no array file |
| `d1-seam-oracle-store` | READER `b` | empty record: D-1 histories were exactly enumerated over a 5-symbol alphabet; no stored 32-symbol histories |
| `d2a-store` | READER `e` | permitted pools as raw tokens; sealed pools by sequence-id ranges and the `sealed_d2a` predicate, never opened: `k4b_registry.source_e`, `k4b_data.predicate_check` |
| `docs-0024-store` | EXCLUSION | ledger, meter binding, logs; no histories |
| `int-0021-store`, `int-0022-store` | EXCLUSION | ledgers, meter bindings, suite XML, logs; no histories |
| `k4b-store` | READER `k` | K4b stage tables `stages/S3/HIST_cal_b0`, `HIST_val_b0`, `stages/S7/HIST_test_b0` (and superseded copies); K-REG1/K-REG2 listed as derived: `k4b_registry_k.source_k` |
| `tmp-0027` | EXCLUSION | synthetic test fixtures under `pytest-of-pc2/` (≤ 1,024 rows; K4b R23 rule) |
| `tmp-0028` … `tmp-0047` (18 directories: 0028, 0029, 0031, 0032, 0033, 0034, 0035c, 0036, 0039, 0039c, 0041, 0042, 0042c, 0044, 0045, 0046, 0046r, 0047) | EXCLUSION | job temporaries; 0 history-bearing files (K-REG2) |
| `topo-pilot` (main) | READER `a` | 72 ObservationSets in `artifacts/` (E4 training/dev/test and exposed assets): `k4b_registry.source_a`, coverage by `revalidate_coverage`; `tests/` fixtures by the R23 rule; `docs/proposals/X5_G1_VERIFICATION_OUTPUTS/verification_arrays.npz` not history-bearing |
| `topo-pilot-c1p`, `topo-pilot-c2`, `topo-pilot-causal-planning-codex`, `topo-pilot-circle-history-k4`, `topo-pilot-d1`, `topo-pilot-d2a`, `topo-pilot-int`, `topo-pilot-k4b`, `topo-pilot-reorg`, `topo-pilot-verify`, `topo-pilot-x2a`, `topo-pilot-x4-history-feas`, `topo-pilot-x4b`, `topo-pilot-x6`, `topo-pilot-x6s1` | EXCLUSION | git worktrees (code and docs); the only array file is the `verification_arrays.npz` copy (not history-bearing); no ObservationSet root |
| `x2a-stage0-oracle-store` | READER `b` | empty record: model arrays, PH diagrams, summaries (T² process); no stored histories |
| `x4-circle-history-feas-store-0015` | READER `b` | `oracle_<j>.npz` calibration/validation canonical32; `REFERENCE_CACHE.json` K = 32 entries |
| `x4-history-feas-store` | READER `b` | `calibration.npz`, `validation.npz` tokens |
| `x4-oracle-profile-store-0014` | READER `b` | empty record (ids reference x4-history-feas; coverage-checked) |
| `x4b-research-store` | READER `b` | empty record (canonical_ids reference E4 ObservationSets; coverage-checked) |
| `x4b2-research-store` | READER `b` | `pool_{reference, repetition1..3}_tokens.npz` canonical tokens |
| `x4f-gates-research-store` | READER `b` | empty record (history_id references E4 HistoryIndex; coverage-checked) |
| `x5g1-research-store`, `x5g1t-research-store`, `x5g1t-fixture-run` | READER `f` | ObservationSet roots (X5 G1 arms; 237 OS objects in all), raw or canonicalised by their EmissionSpec: `k4b_registry.source_f` |
| `x5g1-techbench-store` | EXCLUSION | one `tech_ledger.json`; no array file |
| `x6-stage0-oracle-store` | EXCLUSION | `run/model.npz` holds float64 process arrays (`T_base`, `T_lift_<arm>`, `E*`), gate records hold scalars; no stored history. Its regenerated MC samples enter through X6-REG1 (`stage0_mc_*`), the base of reader `x6` |
| `x6-stage1-store` | READER `x6` | `X6-REG2` (`d5cc07487a4f7aa9841976cece483c4088095533ead08e9e6a7b44d92bcecf59`; base X6-REG1 `88c48a4bf6d307fcc6189cce14ef733747d57a9a8873d2af3b7e628c5a57c33b`: K-REG2, X6 stage-0 MC and constructed histories, K4b stage tables, the 32 non-test pools; 19,420,831 digests) opened by `x6s1_registry.open_reg`, plus every other history-bearing array: the three test-pool ObservationSets (`pools/ObservationSet/*`), `pools/npy/*.npy` (smoke and train copies), `stages/E0/partners_test_{NA,AB,ZC}_t32.npz` (`tokens`), `tables/designed.npz` (`<fam>_a`, `<fam>_b`), any history-bearing stage or superseded array; `cloud/**/ckpt/*.pt` (weights) and `registry/runs` (derived) contribute nothing: `c2_registry.x6_source` |
| `c2-readout-store` | OWN | this lineage's store: not a source of R; absent or lineage-recognised at G0; its FIT/FEAS/VAL tables enter R′ (REG2) |

**Top-level files** (not directories; outside the K4b inventory): `CODEX_PROMPT_owner_transfer_2026-10-14.md`, `conductor_prompts_2026-10-13.md`, `x4f-gates-run.log`, `x5g1t-fixture-run.log` (text); `topo_pilot_research_review_20261014.zip` (62 members) and `x4-history-feas-readonly-audit-20261014T140309Z.zip` (53 members), whose name lists hold no `.npz`, `.npy` or `.pt` member (JSON and Markdown records only). EXCLUSION: no array file; JSON outside `agent-handoff` is not a token source (K4b precedent, §19 item C-15).

**Not inventoried:** `X:/Downloads/topo-scratch/` (outside the project root; §5.3 (e) names the project root; open question Q3).

## 19. Choices (where the protocol leaves something open; simplest option)

- **C-1** Per-model statuses are strings without the `_j` suffix, keyed by model; qualifiers carry the model in parentheses.
- **C-2** Family keys `"R"`, `"M"`, `"S*"`; problem keys `PROBLEMS` (§2). File names use `Sstar` for `S*`.
- **C-3** SeedTree scope values: split names as strings, block, model and frame indices as Python `int`.
- **C-4** M Haar frames use the protocol's stream literally (`("c2-v1", "frame", j, r)`, r = 0..7, the same names as R frames 0..7) and draw `standard_normal((128, 6))`.
- **C-5** P1: one `sd_b4_draws`/`centered_draws` call per (family, array, N) with the family's seed pair; per-model pass read from `precision_summary`'s per-model entry (`mde_upper ≤ alternative` and `power ≥ 0.80`).
- **C-6** The X1 attainability rule is evaluated in its product form 4·128·2⁻⁵³·κ_X1 ≤ 1e-10 (exact rationals); "κ_X1 ≤ 1.76e3" is its rounded statement.
- **C-7** H3's "interval rule off the fast path" uses the C1′ fast-path determination unchanged: `c1_cert.p0`, `c1_cert.reference_oracle`, `c1_cert.p1` and `error_bound.posterior_envelope(32, p0["N"])`, only inside `c2_oracle.decimal_rows` (open question Q1: §13.2 lists `c1_cert` as not used).
- **C-8** H3 Decimal rows: the 4 lowest-sequence-id rows eligible under both E_x and E_y, per split (FIT, FEAS, VAL; TEST inside T-PRE).
- **C-9** R is two components: the token and digest sources through the frozen `c1_data.build_registry` (an in-memory digest set, as K4b), and the X6 component as an X6S1 on-disk `DigestSet` (bounded memory: the X6 store alone holds ≈ 20 million rows, which an in-memory set would not fit in the 4 GiB RAM bound).
- **C-10** R′ (REG2) is rebuilt from scratch from every source (version `C2-REG2`) with the FIT/FEAS/VAL tables as `extra`, as K4b's K-REG2.
- **C-11** A `sealed_d2a` predicate hit on any C2 row (any role) at H2 or REG2 → INCONCLUSIVE/REGISTRY_INCOMPLETE (K4b rule; the registry cannot decide disjointness from the sealed pools); the D-2a sealed sequence-id ranges are checked with the seq-id disjointness.
- **C-12** Run-time inventory versus the frozen table: §5.2 rules (i)–(iv).
- **C-13** `c2-readout-store` is removed from the run-time inventory before classification (own store; G0 vii governs it).
- **C-14** Scratch roots outside the project root are not inventoried (open question Q3).
- **C-15** JSON files are scanned for token lists only in `agent-handoff` (reader c), as in C1′/K4b; reader x6 reads arrays only.
- **C-16** Top-level files are excluded (no array member).
- **C-17** Namespace scan file set and permitted hits as §4.4 (pinned code also by sha256, so a byte copy of `tools/c2_readout` merged into main is admitted).
- **C-18** A G0 (vii) failure is recorded as FAIL_TECHNICAL/LINEAGE (the §7 row 1 class) with the §11 item 7 reason "INVALID/LINEAGE: unrecognised store file"; inside a running stage, an unrecognised write is INVALID/LINEAGE (open question Q2).
- **C-19** The dispatch identity (G0 viii) is checked without new dependencies: task sha256 of `agent-handoff/jobs/<job>/task.md`, a non-empty session id, and the release record naming both.
- **C-20** Releases: `RELEASE_R<k>.json` authorises stage S<k> (R3 and R4 may be one record with `"stages": ["S3", "S4"]`; R5 names N_test and k).
- **C-21** Lineage manifests per job (`manifests/<job>.json`), accepted by a coordinator record; append-only JSONL files are recognised by the sha256 of the latest accepted manifest.
- **C-22** VAL activations are sealed (`sealed/ACT_VAL_<j>.npz`), since the VAL endpoint means can be reconstructed from them; VAL gate statistics are computed in memory from them at S4.
- **C-23** X1 interchange arms run with arm 2's tokens (the patched output does not depend on the inputs, Lemma R(iv)).
- **C-24** C2-M: z_nat(H) is the closed form W_Uβ + M y(H) (equal to the network value within τ_X1, checked by X1); every patched logit comes from `forward_with_patch`.
- **C-25** The M0 two-route check uses d_x of each M0 row and the natural network logits of H.
- **C-26** The "affine w32 and y-marginal readouts" (§2.12) are OLS affine maps fitted on FIT natural rows from y to onehot(w32) and to the y-marginal ν(b32); the change under P_SΔy is reported as the full mean vector over TEST E_x rows.
- **C-27** The descriptive RFF decoder of f₁ from P_rest y uses `c1_fit.fit_decoder` unchanged (its own SeedTree streams, target label `"c2-rest-f1"`), fitted on FIT and scored on FEAS.
- **C-28** J (the projector onto ker(CM)) from the SVD of CM with `np.linalg.matrix_rank`'s default tolerance.
- **C-29** ψ_max = ½·(sum of the 6 largest eigenvalues of sym E[ind(Δy(Mᵀd)ᵀ)]) / E[ind(A_full)].
- **C-30** The block-3 LayerNorm scale ratio is √(Var(r) + ε)/√(Var(a₂(H)) + ε) of each S and C replacement, ε = block 3's first LayerNorm eps.
- **C-31** GLS by the QR route of §13.2 (Cholesky, triangular solves); the Euclidean variant by the QR of X_n.
- **C-32** X1 and the M0 readout identity use ‖z‖∞ of the network (patched or natural) logits in the tolerance.
- **C-33** Entropy in nats with 0·log 0 = 0; the second-harmonic modulus uses x = rint(coords[:, 0]).
- **C-34** Indicator form by `np.where(E, s, 0.0)`.
- **C-35** The k TEST blocks are sampled together at REG2 (blocks 0..k−1).
- **C-36** N2 with a symbol class absent from FIT → EXCLUDED/RADIAL_SUPPORT.
- **C-37** VAL sign gates (V3x, V3y, Y1, Y1*, Y2) use indicator-form arrays over all 4,096 VAL rows, the three models in one `bootstrap_means` call per seed; H5 uses the eligible-row G values (its 0.01-nat threshold is on the conditional mean).
- **C-38** INC/NUMERICAL iff a category-relevant bound (L or U of Z010, Z050; M: of ZM010, ZM050) is NUMERICALLY_UNRESOLVED and no category is declared.
- **C-39** Variant categories use the primary RESP/SPEC declarations and the same R stream (seed 620503).
- **C-40** `union_sha256` = sha256 of `digests_sha256 + "\n" + x6.digest_sha256`.
- **C-41** Rotation-arm values are computed on every TEST E_x row; its X1 arms run on the 1,024 lowest-id eligible rows.
- **C-42** C0v's ledger is the unchanged `c1_chart.ConstructionLedger` at `CHART_CONSTRUCTIONS.json`, used with role `"direct"` only (≤ 3 claims, one per model).
- **C-43** Process loading reuses `x4_oracle_profile.inputs.load_config`/`load_process` (unchanged; protected path), as C1′ did.
- **C-44** M statistics use β_s = 0 in the NUM guard: the P₂ error has no closed-form propagation through block 3 (its GLS-REF δ_P is recorded; open question Q4).
- **C-45** GATES.jsonl keeps the `stage_records.record_gate` line format; C2 does not use `stage_records.begin`/`c1_records.run_c1_gate` (they stop at the first non-PASS gate, which C2's model-scope rule forbids).
- **C-46** Reused files outside the §13.1 table (`c1_cert`, `error_bound`, `stage_records`, `independent_reference`, the job-0014 `inputs`/`oracle_profile`/`config.json` and meter files, the K4b and X6S1 registry readers and their imports, `x4f_probe`, `ridge`) have their blob sha256 at R in `CONTRACT.json` `hashes.reused_extra`, and G0 (iii) checks them at H too ("every reused file"); the §13.5 protected-path diff binds most of them already.

### 19.1 Readings fixed by the independent tests (erratum, ruling R-0101-1, job 0102)

Recorded before any module code (job 0102, step 1). Where this contract leaves a format open, the module adopts the reading of the test's `API-AMBIGUITY` or `API-ASSUMPTION` comment (`tests/c2_readout/test_*.py`, `AUTHORSHIP_A.md`, `AUTHORSHIP_B.md`). Where the protocol and this contract conflict, the protocol wins. No threshold, tolerance, seed, gate, stop rule, outcome rule or licence changes.

**Protocol wins over this contract (two cases).**
- **E-1 (A item 1, T-ORACLE grid).** The §13.3 "4 × 4 cylinder" is read as the smallest cylinder on which the frozen index maps act: 12 periodic x-cells by the mirror rows y = 5, 6 (24 states). `c2_data.rho_R_index`, `rho_m_index` and `symmetry_report_R` look states up by their rounded coordinates, so they accept any coordinate set that is closed under (x, y) ↦ (x, 11 − y) and ((x + m) mod 12, y).
- **E-2 (B, C2-M licences).** Every C2-M licence (§11.2 `licence`, family "M") carries the protocol §3.2 caveats as well as its sentence and Q-CODE: the words "radial support screen" (N2 assesses neither the joint law nor compatibility with the source prefix's keys and values) and "residual skip" (the residual skip is part of every M effect), plus "only position 32 is tested" and "self-repair can lower τ_M". No M licence uses the words "natural support" or "naturalness".

**Formats left open, fixed by the tests (author A).**
- **E-3 (A2, GLS-REF fixture 5).** `c2_stats.theta(q)` and `enclosure` take u_D = ½·10^{1−p} with p = the precision of the active `decimal` context (`decimal.getcontext().prec`); `gls_ref` runs inside `decimal.localcontext(dctx(prec))`.
- **E-4 (A3, GLS-REF fixtures 1, 2, 6).** `gls_ref` calls `dsolve` through the module attribute `c2_stats.dsolve` at call time (never a bound alias), with the first solve as `dsolve(A [n × n], X_n [n × m])` and the second as `dsolve(𝒢* [m × m], Y*ᵀ [m × n])`; `dinverse` may call `dsolve` with an m × m right-hand side. Tests replace `c2_stats.dsolve` and identify the two solves by these shapes.
- **E-5 (A4).** `c2_oracle.oracle_role(T, E, pi, tokens32, coords=None)`: the key `"m32"` is present only when `coords` is given; `oracle_split` passes `coords`, so every role of a split carries `"m32"`.
- **E-6 (A5, B).** `c2_decide.r_model(b, y_active)` and `m_model(b, y2_active)` take one model's `b = {statistic: {"mean", "L", "U", "rank_L", "rank_U", "g"}}`, keyed by the §11.1 statistic names without the model suffix (the report.json `per_model.bounds` layout of §15.2). Their outputs `resp`, `spec`, `negative`, `coarse.gt010`, `coarse.lt050` are Python booleans.
- **E-7 (A6, M rule 6).** When L(Ztau) > g and U(Ztau) < −g both fail and a bound of Ztau is NUMERICALLY_UNRESOLVED, the M status is `"INC/NUMERICAL"` (the guard hit is what left the transmission statement undeclared, §6.4 rule 3); otherwise `"INC"`. C-38 is extended by Ztau for M.
- **E-8 (A7).** `variant_category(b, variant, primary)`: `primary` is the model's `r_model` output. `qualifiers(family, per_model, variants, y_active, p1)`: `per_model = {model: r_model output}`, `variants = {model: {variant: category}}`, `p1` = the `c2_stats.p1` result (its `"precision_limited"` list).
- **E-9 (A8).** `endpoint_status(model, family, gate_history)`: `gate_history` is the list of GATES.jsonl records as dicts (§15.1). A T-PRE-MODEL exclusion gives `"NOT_RUN/T-PRE"` (protocol §7 row 24).
- **E-10 (A9).** `c2_attrib.post_desc(arrays)` takes `{name: {"num": float64[n], "den": float64[n], "E": bool[n], "gate": str}}` and returns `{name: {"value": float, "label": "unlicensed (gate <gate>); computed after the outcome"}}` with value = mean(num[E]) / mean(den[E]).
- **E-11 (A10).** `desc_intervals` returns, per (num, den) pair, the key `"<num>/<den>"` with `{"L": float, "U": float}` or the string `"UNDEFINED"`.
- **E-12 (A11).** `licence(family, outcome, values)` takes one dict of the §11.2 bracket names with scalar (or string) values; a bracket whose key is absent is filled with `"[ ]"`.
- **E-13 (A12).** `c2_stats.p1` and `mde_report` call `precision.sd_b4_draws`, `precision.centered_draws` and `precision.precision_summary` through the module attribute `precision` at call time, so tests can replace them.
- **E-14 (A13).** `n_test(N_by_family)` receives only the alive families, each with an integer N_F.

**Formats left open, fixed by the tests (author B).**
- **E-15.** `overall(family, statuses, cnhs)`: `cnhs` is the list of models with status CNHS (protocol §6.5 rule 2, §7 row 16).
- **E-16.** The N2 functions (`n2_fit`, `dm`, `n2_gate`) are dimension-agnostic: states are `float64[·, p]` for any p (128 at layer 2).
- **E-17.** `l1_complete_scores(Y, preds, w32, class_means_fit)`: `preds` is keyed by the decoder kinds `"D0"`, `"Dcode"`, `"Dlin"`; the result holds `"R2_D0"`, `"R2_Dcode"`, `"R2_Dlin"` and `"R2_code_over_lin"`.
- **E-18.** `GATE_ORDER` is a tuple of gate-name strings (exactly the §12.1 names, in order); the stage of each gate is the separate map `GATE_STAGE`.
- **E-19.** `check_sequence(gates_jsonl)` takes the path of a GATES.jsonl file.
- **E-20.** `Registry.sealed_ranges` (and the registry manifest's `sealed_ranges`) is `{pool: (lo, hi)}`, the K4b layout, half-open: an id is inside iff lo ≤ id < hi.
- **E-21.** `build(version, store, root, extra)`: `extra` is the dict `{split: history_table}` (the layout of `separation`'s `tables`).
- **E-22.** `release_ok(ctx, stage)` returns `{"ok": bool, "status": "PASS" | "REFUSED", "reason": str}`; it never raises for a missing or unparsable release.
- **E-23.** `supersede(ctx, job, attempt, paths, ruling)`: `ruling` is a dict with at least `"defect"`, `"ruling_path"` and `"ruling_sha256"` (other keys are ignored).

**Test assumptions the modules honour.**
- **E-24.** The `c2_config` path constants (`PROJECT_ROOT`, `STORE`, `WORKTREE`, `MAILBOX`, `ARTIFACT_ROOT`, `C1P_STORE`, `X6S1_STORE`, `K4_FREEZE`) and `CONTRACT` are read at call time through the `c2_config` module (default arguments are `None`, resolved inside the function), so a monkeypatch of `c2_config` (or of the same names on a module that holds them) takes effect.
- **E-25.** `g0(ctx)` returns its item dict and does not raise for a failed item.
- **E-26.** The policy seam: model code calls only `policy.require(kind)` before forming logits and `policy.require_write(kind)` before writing an endpoint array or summary, so a subclass of `LogitPolicy` overriding these two methods is a valid policy.

**Contract defect corrected.** §18: "`tmp-0028` … `tmp-0047` (19 directories: …)" names 18 directories; it now reads "18 directories". With `tmp-0027` the table has 19 `tmp-*` rows, which is what `CONTRACT.json` `registry.inventory` holds (unchanged).

### 19.2 Stage modules (erratum, ruling R-0103-1, coordinator addendum 3, job 0104)

Recorded before the stage-module code (job 0104, step 1). It supersedes §1 "exactly these ten modules" and the §12.2 statement that the stage bodies live in `c2_driver.py`. No threshold, tolerance, seed, gate, stop rule, outcome rule or licence changes.

- **Module set.** `MODULES` = 12: the ten of §1 plus `c2_stage_pre.py` and `c2_stage_post.py`, each ≤ 400 lines (total ceiling 4,800; T-SIZE). Dependency order: `c2_driver` ← `c2_stage_pre` ← `c2_stage_post` (the stage modules import the driver and every other module; the driver imports neither at import time).
- **Stage split (§7 stage column).** `c2_stage_pre.PLAN` holds `"S1"`–`"S4"`: rows 0b–20 (S1: `IMPL` record, `AUTH-ADMIT`, `G0`, `PF`, `H1`, `REG`, `H2`, `H3`, `H4`, `H5`; S2: entry, `M0`, `C0c`, `F1`; S3: entry, `C0v`, `L1`, `R1`, `N2`, `SURVIVAL`; S4: entry, `X1`, `V3x`, `V3y`, `Y1`, `Y1*`, `Y2`, `P1`), and the split-level checks that T-PRE reuses (sampling with separation, the H5 bound, L1, R1, N2, support). `c2_stage_post.PLAN` holds `"S5"`: entry, `ACCEPT` (row 21), `REG2`, `T-PRE`, `T-PRE-MODEL`, `RESP-SPEC`, `NUM`, `ENDPOINT`, `REPORT` (rows 22–28; POST-DESC inside REPORT, §5.7). The addendum's row numbers ("0b–17", "18 onward") are read through its words "up to and including the VAL stage" and "following §7's stage column": rows 18–20 (V3x/V3y, Y1/Y1*/Y2, P1) are VAL (S4) gates and stay in `c2_stage_pre`.
- **PLAN.** `PLAN: dict[str, tuple[tuple[str, Callable[[Ctx], dict], str], ...]]`, stage → ordered `(gate, fn, scope)` with `gate` a `GATE_ORDER` name and `scope ∈ ("study", "model", "family")`. `fn(ctx)` returns `{"status": <full status>, "values": dict, "reason": str (optional), "records": list (optional)}`. Without `"records"` the gate is one `GATES.jsonl` line; with it, one line per entry `{"status", "values", "model", "family", "problem", "scope" (optional; default the step's scope)}` (per-model, per-family and per-problem gates, §12.1). Step functions never write `GATES.jsonl` themselves.
- **Stage entry.** Every PLAN entry starts with `("AUTH-ADMIT", …, "study")` and `("G0", …, "study")` (§12.1 `STAGE_ENTRY`); S1 starts with `("IMPL", …)` (the code-freeze record: FREEZE.json `H` equals the run's head). S5 records `ACCEPT` right after G0 from `release_ok(ctx, "S5")` (RELEASE_R5.json), which moves the policy position past row 21 (§12.1 "ACCEPT is entered by release_ok").
- **Lazy dispatch `c2_driver.run_stage(stage, ctx)`.** (1) `stage ∈ PREREQ` (else `ValueError`); (2) `importlib.import_module(STAGE_MODULE[stage])` with `STAGE_MODULE` = S1–S4 → `"c2_stage_pre"`, S5 → `"c2_stage_post"`; (3) `begin_stage` (a refusal raises `StageRefused`; exit 3, no gate line); (4) `ctx.release = release_ok(ctx, stage)`, `ctx.policy = LogitPolicy(done = the distinct gate names of GATES.jsonl)`, `ctx.data["stage"] = stage`; (5) for each step: `policy.begin(gate)`, `run_gate(ctx, gate, lambda: fn(ctx), scope)`, `policy.end(gate)` (always). An exception inside `fn` is classified by `classify_exception` and recorded with scope `"study"`. After the first recorded study-scope line whose status is not PASS/NOT_RUN (`stop`, S4/S9), every later step of the stage is begun, recorded `NOT_RUN` and ended, except `REPORT`, which always runs (S4: values kept, the report is written; POST-DESC only under §5.7). (6) `stages/<stage>/record.json` (gate → statuses, `stopped`), `complete_stage(ctx, stage, ctx.data["files"])`, `write_manifest`. Returns `{"stage", "stopped"}`; `main` exits 2 iff `stopped`.
- **`ctx` keys.** `Ctx` fields as §12.2. `ctx.data` (one process, one stage): `"stage"`; `"files"` (store-relative paths this stage wrote: the COMPLETED evidence); `"stopped"`; caches loaded or formed once per process (the process, the models, history tables, ORACLE arrays, FIT arrays and decoders, per-model split activations, readout coordinates and phases; natural logits only from their pass to the end of X1 or T-PRE; the TEST stream arrays and bounds from NUM to REPORT). Across stages only store files carry data (§16.1); nothing is kept in memory between stages.
- **`pf` moves** from `c2_driver` to `c2_stage_pre` (row 2 is a gate body; the driver line budget). Its behaviour is §12.3 unchanged; `g0`, `auth_ok`, `release_ok`, `meter_bind_check`, sealing, records and lineage stay in the driver.

### 19.3 C2-FROZEN-v2 (erratum, job 0105; v2 §21 C-1..C-10, owner addendum 23, R-0104-1)

Recorded before the v2 code (job 0105, step 2). **Authority:** `tools/c2_readout/PROTOCOL_C2_v2.md`, a byte copy of `agent-handoff/planning/responses/C2-FROZEN-v2.md` (sha256 `51f78976a6d035b3e01dc2155ad66bb80cb870a4ae155cad17b6665d37f24583`); the v1 copy is removed (v2 §21, coordinator note 2). Every reference in this contract to C2-FROZEN-v1, `PROTOCOL_C2_v1.md`, H^R, ρ_R, σ, d^R, A^R, S_REFL, LIK_REFL, T2 or `"HR"` is read through this erratum; where an earlier section and this one differ, this one wins. No threshold, tolerance, seed, gate, stop rule, outcome rule or licence changes beyond v2 §21.

**Bindings (§3.1).** `PROTOCOL_ID = "C2-FROZEN-v2"`, `PROTOCOL_FILE = HERE / "PROTOCOL_C2_v2.md"`, `PROTOCOL_SHA256 = "51f78976…4583"`, `V1_SHA256` (superseded), `ADDENDUM1_SHA256`, `ADDENDUM2_SHA256`, `OWNER23_SHA256`. `AUTH_PATH` and `AUTH_SHA256` are read from `CONTRACT["protocol"]["auth"]`; they are `None` until the coordinator binds the owner AUTH addendum naming the v2 sha256 (v2 §14 D2, gate 0b), and `auth_ok` refuses while `AUTH_SHA256` is `None` (fail closed). `g0` item (i) compares `PROTOCOL_FILE` with `PROJECT_ROOT / CONTRACT["protocol"]["mailbox_file"]` (`agent-handoff/planning/responses/C2-FROZEN-v2.md`, relative to the project root; ruling R-0105-1). `auth_ok` reads `c2_config.AUTH_SHA256` at call time. Constants: `H4 = {"x": 9/10, "y": 17/20}` (was `H4 = 9/10`); `Y_MID = 11/2`; `T_SYM_R` removed; `MODULES` (the 14 module names of `CONTRACT["modules"]`).

**Roles and pairs (§2).** `ROLES = ("H", "Hp", "Hm", "HY")`, `PAIRS = {"x": ("Hp", "Hm"), "y": ("H", "HY")}`. "HY" (H^Y) replaces "HR" in every key: `digest_HY`, `HY_q`, `HY_qbar`, `HY_s`, `HY_le`, `HY_m32`, the X1 arm `nat_HY`, the activation keys `HY_<hook>`. The y-pair contrast is `d_y = q̄(H) − q̄(H^Y)` (canonical; named by `d_named`), and `G_y = G_hat(q̄(H), q̄(H^Y))`.

**The H^Y donor (§4.2; v2 §2.2, C-1, C-2; it mirrors `topo-scratch/0104/fy_alt.py`, sha256 0e1113ed…63aa).** Removed: `sigma`, `reflect_donor`, `rho_R_index`, `symmetry_report_R` (the y pair has no symmetry, closed form or ε_sym). New in `c2_data`:
- `OFF = 255`: the value of every position of an undefined H^Y row. It is an index error in `E[:, ·]` and `perm[·]`, so an unmasked use fails loudly; it is never a symbol.
- `k_y(b31, coords) -> int64[n]`: ȳ = `b31 @ coords[:, 1]` (the posterior mean of the cell row under the natural history's filter after 31 symbols); +1 where ȳ < 5.5, else −1 (ȳ = 5.5 gives −1).
- `y_donor(canon32, k) -> (int64[n, 32], bool[n])`: b = w mod 6 and a = w div 6 on w1..w31; `nb = b + k[:, None]`; `Y_def` = all(0 ≤ nb ≤ 5) per row; H^Y[:, :31] = 6a + nb and H^Y[:, 31] = w32. Rows with `Y_def` False are set to `OFF` in full (OFF_GRID_Y: never clamped, never wrapped).
- `donors4(canon32, k_y) -> (H, Hp, Hm, HY)` (`c1_oracle.donors` for the first three).
- `role_arrays(canon32, k_y) -> {role: (tokens int64[m, 32], rows int64[m])}`: every row for H, Hp and Hm; only the Y_def rows for HY. Every oracle run, digest, model forward and predicate check of H^Y goes through it, so no H^Y is formed on an OFF_GRID_Y row.
- `history_table(canon32, seq_ids, panel, k_y) -> dict` (k_y is required): keys `canonical`, `sequence_id`, `panel`, `k_Y` (int8), `Y_def` (bool), `digest_H`, `digest_Hp`, `digest_Hm`, `digest_HY` (`""` on OFF_GRID_Y rows). `table_digests(table)` is the union of the four columns without `""`. `table_roles(table)` = `role_arrays(table["canonical"], table["k_Y"])`.
- `REASONS = ("S_PLUS", "S_MINUS", "S_Y", "LIK_H", "LIK_PLUS", "LIK_MINUS", "LIK_Y", "OFF_GRID_Y", "ZERO_MOD_H", "ZERO_MOD_PLUS", "ZERO_MOD_MINUS")` (v2 §5.5). S_Y and LIK_Y are False on OFF_GRID_Y rows, where they are not evaluated.
- `c2_registry.separation` and `build` take the roles from `table_roles` (H^Y only where defined); `duplicates` = (3n + |Y_def|) − |U|.

**The Y-donor preparation in H2 and H2′ (v2 §7 note; NEW-10).** After REG (REG′) passes and a split's natural histories are sampled, the stage runs `c2_oracle.oracle_role(T, E, pi, canon32, coords)` on the natural histories only, computes `k_y` from its `b31`, builds the table with the defined H^Y donors, writes `hist/`, and caches the natural oracle result in `ctx.data["oH:<split>"]` for H3 (for T-PRE on TEST). Separation runs over every defined donor role before the gate returns. Nothing else is formed: no donor contrast, no fit, no model output. H3 (T-PRE) consumes the cache and validates it (the Decimal rows include H).

**The H^Y oracle (§6.2, §6.3; v2 §2.2, §7 row 6, C-4).**
- `oracle_split(T, E, pi, coords, canon32, k_y, o_H=None) -> dict`: H from `o_H` when it is given (the H2 cache), else computed; Hp and Hm on every row; HY by the exact oracle forward (`run_oracle`) on the Y_def rows only, scattered into n-row arrays with NaN elsewhere; `"Y_def"`, `"k_Y"`; `G_x`, `d_x`; `G_y`, `d_y` on the Y_def rows (NaN elsewhere); `nuis`.
- `eligibility(o, smax)`: E_y = Y_def ∧ s(H^Y) ≤ s_max ∧ finite log-evidence of H and H^Y. f_y = |E_y|/N over all rows, so OFF_GRID_Y rows count as ineligible.
- `x_leakage(o, E_x, E_y, coords) -> {"b31", "b32"}`: λ_x = mean_{E_y}‖m32(b(H^Y)) − m32(b(H))‖ / mean_{E_x}‖m32(b(H⁺)) − m32(b(H⁻))‖ at b31 and at b32 (v2 §2.12; descriptive, per split, recorded at H4 and T-PRE).
- `h3(...)`: the τ symmetry report, exact invariance and the closed forms for the x pair only (T1, T3); no ρ_R report (T2 is withdrawn); named = canonical, cross-model G and Σq = 1 on every defined row of every role (G_y included). Decimal rows: `decimal_rows(T, E, pi, canon32, o, rows_x, rows_y, p0)` checks H, H⁺, H⁻ and G_x on the 4 lowest-id E_x rows, and H, H^Y and G_y on the 4 lowest-id E_y rows (H is checked at both, which validates the H2 cache). SYMBOL-ORDER (c) runs on the FIT (TEST) d_x and on d_y's defined rows. This supersedes C-8.
- `kappa_m(m32_H, m32_HY, E_y_fit, m32_H_fit)`, and `reason_flags(o, smax)` with the v2 reasons.

**H4 (§12.2; v2 §5.4, C-3).** PASS iff f_x ≥ 9/10 and f_y ≥ 17/20 on FIT, FEAS and VAL (exact `Fraction` comparisons).

**The whitened G1 identity (§8.2; v2 §2.5, C-6).** `gls_identities(g, Gamma, B, Sigma=None) -> {"max_abs", "rel", "sym", "checks", "ok"}`, on the production L̂ and P̂ = X_n L̂:
- dimensionless, absolute ≤ 1e-10: ‖L̂X_n − I‖_max, ‖P̂_S² − P̂_S‖_max, ‖P̂_Γ² − P̂_Γ‖_max, ‖P̂_SP̂_Γ‖_max, ‖P̂_ΓP̂_S‖_max, ‖P̂_S + P̂_Γ − P̂‖_max and ‖P̂² − P̂‖_max (`max_abs` is their maximum);
- relative: ‖P̂_SΓ‖_max ≤ 1e-10·‖Γ‖_max and ‖P̂_ΓB‖_max ≤ 1e-10·‖B‖_max (`rel` holds the pairs (‖P̂_SΓ‖_max, ‖Γ‖_max) and (‖P̂_ΓB‖_max, ‖B‖_max), compared in exact rationals);
- whitened self-adjointness: with Σ = L_c L_cᵀ (`numpy.linalg.cholesky`, so R_Σ = L_cᵀ), P̃ = `solve_triangular(L_c, P̂ @ L_c, lower=True)` (= R_Σ^{−ᵀ}P̂R_Σᵀ, formed from P̂, never from X̃) and ‖P̃ − P̃ᵀ‖_max ≤ 1e-10 (`sym`); Euclidean: ‖P̂ − P̂ᵀ‖_max ≤ 1e-10.

A non-finite value fails. The check runs for every problem (R, R_K1, R_K2, R_E, M, S*); a failure is EXCLUDED/NUMERICAL (primary) or NOT_COMPUTED (variant).

**The 14-module stage split (§1, §12.2, §19.2; R-0104-1, v2 §13.2, C-7).** `MODULES` = 14: the ten of §1 plus `c2_stage_base.py`, `c2_stage_pre.py`, `c2_stage_val.py` and `c2_stage_post.py`, each ≤ 400 lines (ceiling 5,600; T-SIZE). It supersedes §19.2's 12-module set. Dependency order: `c2_driver` ← `c2_stage_base` ← `c2_stage_pre`, `c2_stage_val` ← `c2_stage_post`. A stage module imports the driver and the other modules; the driver imports no stage module at import time. The exact gate-row-to-module assignment (§7 rows):

| Module | `PLAN` stages | §7 rows (gates) |
|---|---|---|
| `c2_stage_base` | none (no `PLAN`) | The stage-entry step bodies shared by every `PLAN`: 0b `AUTH-ADMIT` and 1 `G0`. Also the store loaders, the `ctx` caches and the gate-history helpers (alive, prior, family stop); the per-model split state (activations, readout coordinates, phases, natural logits); and the split-level checks that later stages and T-PRE reuse: the H2/H2′ sampling with the Y-donor preparation and separation, the ORACLE writer, the H5 bound, L1, R1, N2, support, the X1 run, the closed-form stream compositions and the VAL/TEST bound wrapper |
| `c2_stage_pre` | `S1`, `S2`, `S3` | 0 `IMPL`, 2 `PF`, 3 `H1`, 4 `REG`, 5 `H2`, 6 `H3`, 7 `H4`, 8 `H5`; 9 `M0`, 10 `C0c`, 11 `F1`; 12 `C0v`, 13 `L1`, 14 `R1`, 15 `N2`, 16 `SURVIVAL` |
| `c2_stage_val` | `S4` | 17 `X1`, 18 `V3x` and `V3y`, 19 `Y1`, `Y1*` and `Y2`, 20 `P1` |
| `c2_stage_post` | `S5` | 21 `ACCEPT`, 22 `REG2` (REG′/H2′), 23 `T-PRE`, 24 `T-PRE-MODEL`, 25 `RESP-SPEC`, 26 `NUM`, 27 `ENDPOINT`, 28 `REPORT` (POST-DESC inside REPORT) |

`c2_driver.STAGE_MODULE = {"S1": "c2_stage_pre", "S2": "c2_stage_pre", "S3": "c2_stage_pre", "S4": "c2_stage_val", "S5": "c2_stage_post"}`. Everything else in §19.2 holds (the PLAN form, the step returns, the stage entry, the lazy dispatch, the `ctx` keys). Added `ctx.data` key: `"oH:<split>"` (the H2/H2′ natural-oracle cache).

**Helper placement (amendment, job 0105; line budget).** The gate rows are assigned as in the table above. The shared helpers are placed as follows: `c2_stage_base` holds the stage entry (rows 0b, 1), the store loaders, the `ctx` caches, the gate history, the per-model split state (`bundle`, `prob`, `afull`) and the split checks (`sample` with the Y-donor preparation, `save_oracle`, `h5_bounds`, `l1_check`, `r1_check`, `n2_check`, `support`). `c2_stage_val` also holds the helpers that S5 reuses: the C2-M patch arms (`cm_pair`, `placebo_m`), `closed_streams`, `x1_arms`, `x1_run`, the bound wrapper `bounds`/`sg`, and the REPORT descriptive compositions (`rotation`, `cm_intervals`, `describe`, `unsealed`). `c2_stage_pre.oracle_splits` (the four-role oracle from the H2/H2′ cache) is reused by T-PRE. Dependency order: `c2_driver` ← `c2_stage_base` ← `c2_stage_pre`, `c2_stage_val` ← `c2_stage_post`; `c2_stage_post` imports the other three.

**Outputs added or changed (§16.1).**
- `hist/HIST_<split>_b<k>.npz` adds `k_Y`, `Y_def` and `digest_HY`.
- `oracle/ORACLE_<split>.npz` holds `HY_*` (NaN on OFF_GRID_Y rows), `Y_def` and `k_Y`.
- `stages/S1/coverage.json` holds the oracle tally per split, with OFF_GRID_Y and λ_x.
- `stages/S3/coverage.json` and `stages/S5/coverage.json` hold the per-model, per-family tallies: UNSUPPORTED_H/PLUS/MINUS (R and M), ZERO_CODE_PLUS/MINUS, R1_ZERO and R1_UNSELECTED. S5 also holds the TEST oracle tally and λ_x.
- `stages/S3/L1_DESC.json` holds the complete-decoder scores (`l1_complete_scores`) and the RFF decoder of f₁ from P_rest y (C-27).
- `sealed/VAL_ROT_<j>.npz` holds the VAL rotation arm (A_rot and G_rot per dose). `sealed/VAL_M_<j>.npz` also holds the 8 VAL M Haar frames (ψ_M,R on the 1,024 lowest-id eligible rows) and the block-3 LayerNorm scale ratios (C-30).
- Activation arrays of HY are NaN on OFF_GRID_Y rows; no forward runs there.

**PF size scope (§7 row 2; E-0102-2, coordinator addendum 2, carried by v2 §21 C-9).** PF's file-size item passes iff no line of the `tools/check_file_sizes.py` report names a file under `tools/c2_readout/` or `tests/c2_readout/`. Other lines are recorded in `stages/S1/pf.json` as pre-existing, with their line counts. `check_file_sizes.py` itself is unchanged; the 14-module set and the 5,600-line ceiling are T-SIZE's.

### 19.4 G0 (vii) own pre-G0 records (erratum, defect D-0107-1, ruling R-0107-2, job 0108)

G0 (vii) rejected the store's own append-only records: by G0 the stage has already written its `STARTED` line (`begin_stage`, STAGES.jsonl) and its IMPL and AUTH-ADMIT lines (GATES.jsonl), and `recognised` knows both files only through an accepted manifest's `append_only` sha256 (none at S1; stale at S2-S5). New helper `c2_data.own_records(store, stage, lineage) -> dict[str, str]` returns `{name: sha256}` for `GATES.jsonl` and `STAGES.jsonl` when each file is an accepted prefix plus this stage's own pre-G0 suffix, and omits a file that is not. Accepted prefix: empty when the lineage has no `append_only` entry for the name, otherwise the leading lines (line boundary) whose sha256 equals that entry; no matching boundary means the file is omitted. Suffix in STAGES.jsonl: exactly one line `{"stage": <stage>, "event": "STARTED", ...}`. Suffix in GATES.jsonl: only lines with `stage` = the stage, `gate` in {IMPL, AUTH-ADMIT} and `scope` = "study". Anything else stays unrecognised (G0 FAIL_TECHNICAL/LINEAGE as before). Pure reads. `c2_driver.g0` item (vii) calls `cd.store_admission(store, {**lin, **cd.own_records(store, stage, lin)}, stage == "S1")`; `recognised` and `store_admission` are unchanged. The same rule serves every stage.

### 19.5 METER_ACTIVE.lock is meter bookkeeping (erratum, defect D-0109-1, ruling R-0109-1, job 0110)

G0 (vii) stopped S1 attempt 3 because the meter keeps `METER_ACTIVE.lock` at the store root during every metered run (x4_oracle_profile `meter.py` creates it and removes it at the end; the C2 binding sets `meter.ACTIVE = OUT / "METER_ACTIVE.lock"`), and neither `c2_data.METER_FILES` nor the §16.1 list named it, so `store_admission` reported it unrecognised at every stage S1-S5. Rule R-0109-1: `METER_ACTIVE.lock` at the store root is meter bookkeeping and joins the §16.1 meter-bookkeeping list (`logs/**`, `cpu_ledger.json`, `RUN.lock`, `OPERATION_ACTIVE.json`, `OPERATIONS.jsonl`, `METER_ACTIVE.lock`, `LOCK_RELEASED_*.json`); `c2_data.METER_FILES` gains `"METER_ACTIVE.lock"`. Only that exact root name is admitted; a similarly named file (`METER_ACTIVE.lock.bak`, `METER_ACTIVE.json`) stays unrecognised. `cpu_ledger.emergency.jsonl` is not added: it exists only after a meter emergency (an S11 matter). No other behaviour changes.

## 20. Open questions for the coordinator (not decided here)

- **Q1** §7 row 6 (H3 "interval rule off the fast path", "C1′ H3 unchanged") needs C1′'s fast-path test, which lives in `c1_cert` and `error_bound`; §13.2 field 2 lists `c1_cert` as not used. Choice C-7 reuses `c1_cert.p0/p1/reference_oracle` unchanged for H3 only (tools/c1prime is a protected path, so the R→H diff binds them; their blobs are recorded in `CONTRACT.json` `hashes.reused_extra`). Confirm, or rule the relative 2e-12 rule alone.
- **Q2** G0 (vii) failure class: §7 row 1 says FAIL_TECHNICAL, §11 item 7 says INVALID/LINEAGE. Choice C-18.
- **Q3** `X:/Downloads/topo-scratch/` (X6S1 cloud bundles and job temporaries) is outside the inventoried root (§5.3 (e) "under the project root"). Its X6 bundles are copies of x6-stage1-store pools (read by reader x6). Confirm that it stays out.
- **Q4** §9.2 defines β_s for A_S-type and e_S-type terms of the closed-form readout. For the C2-M patched statistics there is no closed form, so choice C-44 uses β_s = 0 (the 1e-9 term alone). Confirm.
- **Q5** §5.3 (a) names "the K4b stores" among the C1′ registry v1 sources (a)–(c); `c1_registry_sources` (job 0027) predates K4b and does not read `k4b-store`. The inventory reads it through reader k. Confirm that this is the intended reading.

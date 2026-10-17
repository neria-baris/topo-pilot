# K4b API v1: written contract (job 0045)

Authority: `tools/k4b/PROTOCOL_K4B_v1.md` (K4B-FROZEN-v1, sha256 957f0d5e70870bbd2323fbbae7bf5a8b814735b00a6525346562e7f1dd35b485). **The protocol wins on any conflict.** Values live in `tools/k4b/CONTRACT.json`; this file names every function, input, output, report key, seed, path and status. Section marks (§n) refer to the protocol.

This contract was written before any module code. It changes no scientific choice. Where the protocol leaves a detail open, the simplest option is listed under **Implementation choices** (§13 of this file).

## 0. Conventions

- **Twelve Python files** under `tools/k4b/` (§11.1), each at most 400 lines (`tools/check_file_sizes.py`). No existing file is edited. No private name (leading underscore) of a reused module is imported.
- **Import path.** Every module first imports `k4b_config`. That puts `tools/k4b`, `tools/c1prime`, `tools/c1prime_registry`, `tools/x4_circle_history` and `tools/x4_oracle_profile` on `sys.path` (insert-if-absent), then imports `c1_config`. Run with `PYTHONPATH=<worktree>/src` and the venv interpreter with `-s` (§11.6).
- **Model maps** are keyed by the **int** seeds 1729, 2718, 3141, everywhere (R11 lesson). A str key is a `FAIL_TECHNICAL/IDENTITY` defect.
- **Statuses** are full strings: `PASS`, `INCONCLUSIVE/<REASON>`, `FAIL_TECHNICAL/<REASON>`, `NOT_RUN`. Gate failures are raised as `c1_records.C1GateFailure(status, reason)`, where `status` is the full string. Other exceptions map through `c1_records.classify_exception` (chart gates first try `adapt_chart_exception`). `dataset.checks` SPLIT_OVERLAP maps to `FAIL_TECHNICAL/LINEAGE`.
- **Exact numbers.** Every certified bound, margin and decision comparison uses `fractions.Fraction`. A float enters a certified comparison only as `Fraction(float(x))`. Thresholds: `MARGIN = Fraction(1, 100)`, `CAP = Fraction(1, 10**4)`, `FLOOR = c1_bounds.FLOOR = Fraction(1, 10**9)`, `ALPHA = c1_means.P_THIRD = Fraction(5, 300)`, `MOMENT_TOL = error_bound.MOMENT_TOL_EXACT = Fraction(1, 10**10)`.
- **Writes** go only inside `stages/<stage>/` of the store, by exclusive create (`stage_records.write_new`, `save_npz`). The ledgers, `GATES.jsonl`, `STAGES.jsonl` and `SEALED_VALIDATION.json` are the exceptions; each has its single writer named below.
- **Splits** are named `"cal"`, `"val"` and `"test"`. Blocks are ints.

## 1. `k4b_config.py` (≈100 lines): contract and constants

| Name | Signature / value | Contract |
|---|---|---|
| `HERE`, `REPO` | `Path` | `tools/k4b` and the worktree root |
| `CONTRACT_PATH`, `PROTOCOL_PATH` | `HERE/"CONTRACT.json"`, `HERE/"PROTOCOL_K4B_v1.md"` | |
| `ROOT` | `Path("X:/Downloads/projects/topo-pilot")` | Project root (registry source f) |
| `STORE` | `ROOT/"k4b-store"` | Default store. Every function that touches a store takes `out` explicitly; `STORE` is only the driver default |
| `MODELS` | `(1729, 2718, 3141)` | int, in this order |
| `SITE`, `INDEX`, `BOS`, `D_MODEL` | `"resid_post_3"`, `32`, `36`, `128` | |
| `SCOPE` | `"k4b-sf-v1"` | |
| `PROCESS` | `("cylinder", "overlap", "1.25")` | |
| `BLOCK`, `PANEL` | `3072`, `512` | |
| `LADDER` | `(3072, 6144, 12288)` | |
| `KS` | `(1, 2, 4, 32)` | Oracle context lengths |
| `DRAWS` | `5000` | |
| `SEEDS` | `{"val_sd": 610101, "val_b4": 610102, "endpoint": 610103, "fresh_b4": 610104, "val_projection": 610105}` | |
| `RANKS` | `{"alpha": 84, "one_minus_alpha": 4917, "b4_lower": 250, "central_lo": 125, "central_hi": 4875}` | Checked at import against `c1_means.rank_for` (`P_THIRD`, `1 - P_THIRD`, `0.05`, `0.025`, `0.975`); a mismatch raises `C1GateFailure("FAIL_TECHNICAL/NUMERICAL", …)` |
| `MARGIN`, `CAP`, `FLOOR`, `ALPHA`, `P2_MAX_ABS` | see §0; `P2_MAX_ABS = 4` | |
| `load_contract(path=CONTRACT_PATH) -> dict` | | JSON; `chart.lift_cpu_cap_s` and `resources.cpu_cap_s` null → `float("inf")` |
| `CONTRACT` | `load_contract()` at import | Import reads only CONTRACT.json files (K4b's and, through `c1_config`, C1′'s) |
| `chart_cfg(contract=None) -> dict` | | `c1_config.chart_cfg(contract or CONTRACT)`: the kernel cfg (12 `CHART_KERNEL_KEYS`, `lift_cpu_cap_s = inf`, `native_operation_wall_s = 600.0`) |
| `check_chart_equality(k4b=None, c1=None) -> dict` | | `{"equal": bool, "cfg_diff": [key, …], "giant_equal": bool, "val_support_equal": bool}`. Compares `c1_config.chart_cfg(k4b)` with `c1_config.chart_cfg(c1)` key for key and value for value, and `chart.giant`, `chart.val_support` (§4.2, C2). Defaults: K4b CONTRACT, `c1_config.CONTRACT`. Used by G0 |
| `status_of(full) -> (head, tail)` | | `c1_config.status_of`, re-exported |
| `require_int_keys(d, what) -> dict` | | Returns `d` if its keys are exactly the ints of `MODELS`; otherwise raises `C1GateFailure("FAIL_TECHNICAL/IDENTITY", what)` |

## 2. `k4b_data.py` (≈220 lines): process, sampling, IDs, tables, separation

| Function | Contract |
|---|---|
| `load_process(cfg=None) -> dict` | Through `inputs.load_config()` and `inputs.load_process(cfg)`. Returns `{"T", "pi", "coords", "features", "E_named": {j: …}, "perm": {j: …}, "E_canon": {j: …}, "E_canon_shared", "specs"}`, int-keyed (§2.2). Each `perm[j]` must be a permutation of 0..35 with an exact round trip (`perm[inverse] == arange`). `E_canon[j] = oracle_profile.canonical_emission(E_named[j], perm[j])`. All three `E_canon[j]` must be bitwise identical (`np.array_equal` and equal bytes); `E_canon_shared` is that array. `features = oracle_profile.circle_features(coords)`. Any defect raises `FAIL_TECHNICAL/IDENTITY` |
| `history_generator(split, block) -> np.random.Generator` | `SeedTree(0).generator("data", SCOPE, split, int(block), *PROCESS)` (§3.1) |
| `sequence_ids(split, block) -> int64 [3072]` | `make_sequence_ids(process_code(*PROCESS, f"{SCOPE}/{split}/b{int(block)}"), "test", BLOCK)` |
| `sample_block(T, E_canon, pi, split, block) -> (canon32, seq_ids)` | One call `HMMSampler(T, E_canon, pi, SequenceLayout()).sample(BLOCK, history_generator(split, block))`. Column w33 and the states are dropped at once (`canon32 = tokens[:, :32]` as contiguous uint8). Rows are then sorted by ascending `sequence_id` (stable). Block content depends only on `(split, block)`, never on k |
| `named_from_canonical(canon32, perm) -> uint8 [n, 32]` | `perm[canon32]` (§2.2: named = perm_j[canonical]) |
| `model_inputs(canon32, perm) -> Tensor` | `c1_model.model_inputs(named_from_canonical(canon32, perm))`, i.e. `[BOS=36, named w1..w32]` |
| `digests(canon32) -> list[str]` | `scores.history_digests(canon32)` (sha256 of the uint8 row) |
| `lowest_rows(seq_ids, n=PANEL) -> int array` | Row indices of the n lowest sequence_ids, ascending (`c1_data.lowest`) |
| `duplicates(canon32) -> dict` | `{"n_rows", "n_unique", "n_duplicate_rows", "max_multiplicity"}` by digest. Duplicates are kept and counted, never removed |
| `history_table(canon32, seq_ids, split, block) -> dict` | Arrays `canon32` (uint8 [n, 32]), `seq_ids` (int64), `digest` (str), `landmark` (bool: the 512 lowest IDs; cal and val only), `ref_row` (bool: the 4 lowest IDs; cal only), `decoder_panel` (int8: −1 on landmarks, else rank among non-landmark rows by ascending id // 512; cal only). Written by the driver as `stages/S3/HIST_<split>_b<block>.npz` (test: `stages/S7/…`) |
| `separation_cal_val(U_cal, U_val, reg1) -> dict` | `c1_data.separation(U_cal, U_val, reg1)` unchanged: `{"collisions": {"cal_R1", "val_R1", "cal_val"}, "status"}`; status `PASS` or `FAIL_TECHNICAL/LINEAGE` |
| `separation_fresh(U_test, reg2) -> dict` | `{"collisions": {"test_R2": int}, "status"}` on every row; any collision → `FAIL_TECHNICAL/LINEAGE` |
| `seq_disjoint(blocks, frozen_union, frozen_ranges=()) -> dict` | `blocks`: `{name: int64 ids}`. Pairwise disjointness by `dataset.checks.check_disjoint(**blocks)`; also disjoint from the frozen sequence-ID union (a set or array of ints) and from every `(lo, hi)` half-open range in `frozen_ranges` (derived sealed D-2a ranges). Returns `{"status", "hits": {…}}`; SPLIT_OVERLAP or any hit → `FAIL_TECHNICAL/LINEAGE` |
| `sealed_d2a_predicate(canon32) -> bool [n]` | `True` where every one of the 32 symbols is in {0, 1, 2, 3, 4} (§3.4 e) |
| `predicate_check(canon32, predicates) -> dict` | `predicates`: the frozen conservative membership predicates of the registry (today one, `"sealed_d2a"`). `{"status", "hits": {name: count}}`; any row satisfying any predicate → `INCONCLUSIVE/REGISTRY_INCOMPLETE` with reason `"potential overlap with sealed D-2a histories"`. Rows are never removed or replaced |

## 3. `k4b_registry.py` (≈320 lines): exposure registry (§3.4, RC6, RC7)

Identity-only access: token arrays and identity columns only. Every function takes `root` (default `ROOT`) so that synthetic roots can be tested.

| Function | Contract |
|---|---|
| `inventory(root=ROOT, exclude=()) -> dict` | Recursive inventory of every top-level directory of `root` (worktrees, superseded attempts and temporary directories included). Per directory: `{"history_files": [...], "identity_refs": [...], "observation_set_roots": [...]}`. A history-bearing file is any `*.npz` holding a `tokens`, `canon32`, `named32`, `H` or `digest_*` key or an integer array with last dimension 32 or 33, plus any ObservationSet root (a directory holding an ObservationSet manifest readable by `ArtifactStore`). Reading is identity-only (npz key names, dtypes, shapes; token arrays only for scanned sources) |
| `classify(inv, scanned_readers) -> dict` | Each top-level directory → `{"class": "SCANNED" \| "NOT_SCANNED" \| "INCOMPLETE", "reason": str}`. NOT_SCANNED only when the inventory found no history-bearing file, identity reference or ObservationSet root, or only synthetic test fixtures (the reason cites the inventory). "Worktree", "temporary" or "not an ObservationSet" alone is never a reason. A history-bearing source with no reader, or an unreadable one, is `INCOMPLETE`, not NOT_SCANNED |
| `validate_handoff_json(root) -> dict` | Parses every `*.json` under `root` (the mailbox) with `json.loads` before `handoff_sources` runs. `{"ok": bool, "n_files": int, "failures": [{"path", "error"}]}`. Any failure → the registry is `INCONCLUSIVE/REGISTRY_INCOMPLETE`; a parse failure never becomes an empty contribution |
| `source_a(root_art, store=None) -> (sources, seqs)` | `c1_registry_sources.observation_set_sources(store, root_art)`. When `root_art` is not the module default `ART`, an `ArtifactStore(LocalFSBackend(root_art))` is built and passed explicitly (`store=None` with a non-default root is refused, `FAIL_TECHNICAL/REGISTRY`) |
| `source_b(root=ROOT) -> list` | `c1_registry_sources.store_sources(root)` unchanged |
| `source_c(root=ROOT/"agent-handoff") -> list` | `validate_handoff_json(root)` first (refuse on failure), then `c1_registry_sources.handoff_sources(root)` |
| `source_d(store=ROOT/"c1prime-store") -> list` | (d1) the digest list of `registry/registry_v1.json` (file sha256 must equal CONTRACT `registry.c1prime_registry_v1_sha256`); (d2) the `digest_H`, `digest_Hp`, `digest_Hm` columns of every `HIST_*.npz` under the store, `superseded/` included, read with `np.load(..., allow_pickle=False)` keys only. Each source `{"name", "path", "sha256", "digests": set}` |
| `source_e(store=ROOT/"d2a-store", pools_meta=None) -> dict` | Permitted pools (every CONTRACT `registry.d2a.pools` entry not in `sealed`): raw `tokens[:, :32]` uint8, no canonicalisation. Sealed pools (`test`, `testN`): **no token array is opened**; their sequence-ID ranges `[SEQ_CODE·2³², SEQ_CODE·2³² + n)` come from `pools.json` metadata (n per pool) and the CONTRACT pool order. Returns `{"sources": [...], "sealed_ranges": {pool: (lo, hi)}, "predicates": ["sealed_d2a"], "status"}`. An unresolved alphabet, pool inventory or sequence-ID identity → `INCONCLUSIVE/REGISTRY_INCOMPLETE` |
| `source_f(root, inv, classes) -> list` | Every SCANNED directory not covered by a–e: ObservationSet stores with a raw-token reader, plus the canonicalised digest when an EmissionSpec perm resolves |
| `revalidate_coverage(root_art, root=ROOT, extra_ids=None) -> dict` | `c1_registry_sources.history_index_ids(store, root_art)` and `coverage(seqs_a, hist_ids, root)` unchanged, then the expanded-inventory supplement: every referenced history or sequence ID must resolve to a covered source. `{"ok", "missing": [...]}`; missing → `INCONCLUSIVE/REGISTRY_INCOMPLETE` |
| `build(version, out_dir, root=ROOT, extra=None) -> dict` | `version` ∈ {`"K-REG1"`, `"K-REG2"`}. Builds from scratch: digest union (via `c1_data.build_registry` for token sources plus direct union of digest columns), sequence-ID union, sealed ranges, predicates, source hashes (each scanned file by content sha256, with canonicalisation metadata), the NOT_SCANNED table, coverage results. `extra`: for K-REG2, K4b's own cal b0 and val b0 history tables. Writes `out_dir/<version>.json` (manifest) and `out_dir/<version>_digests.npz` by exclusive create. Returns the manifest |
| Manifest keys | `version`, `status` (`PASS` or `INCONCLUSIVE/REGISTRY_INCOMPLETE`), `n_digests`, `digests_sha256` (sha256 of the sorted, newline-joined digests), `seq_id_union_sha256`, `sealed_ranges`, `predicates`, `sources` (list of `{name, path, sha256, kind, n, canonicalisation}`), `classes` (every top-level directory), `not_scanned`, `coverage`, `handoff_validation`, `built_utc`, `protocol_sha256` |
| `load(out_dir, version) -> (digests: set, seq_union: set, ranges: dict, predicates: list, manifest)` | Re-hashes the digest file against the manifest; mismatch → `FAIL_TECHNICAL/LINEAGE` |

## 4. `k4b_scores.py` (≈220 lines): oracle moments, X±, phases

| Function | Contract |
|---|---|
| `oracle_moments(T, E_canon, pi, canon32, features) -> {K: float64 [n, 2]}` | `oracle_profile.posterior_means(T, E_canon, pi, canon32, KS, features)`; keys are the ints of `KS` |
| `wrap_phase(phi) -> float64` | `np.mod(phi, 2π)`, then any value equal to 2π after rounding → 0.0. Non-finite → `FAIL_TECHNICAL/NUMERICAL` |
| `vector_phase(m) -> float64 [n]` | `wrap_phase(atan2(m[:,1], m[:,0]))`, with an exact (0, 0) row → 0.0 |
| `m4_phase(m4)`, `oracle_phase(m32)` | `vector_phase(m4)` (§9.1) and `vector_phase(m32)` (the operational Δ4^orc comparator, §9.6) |
| `sha_phase(canon32) -> float64 [n]` | `scores.sha256_phase(row[28:32])` per row (canonical w29..w32), wrapped |
| `phase_scores(phi, m32, mK) -> float64 [n]` | `scores.scores(scores.unit_vectors(phi), m32, mK)` |
| `endpoint_arrays(phi, supported, m32, m4) -> dict` | `{"X_minus", "X_plus", "r4n"}`. `r4n = scores.r4_norms(m32, m4)`; on supported rows `X_minus = X_plus = phase_scores(phi, m32, m4)`; on unsupported rows `X_minus = -r4n`, `X_plus = +r4n` (§1.4). Every row kept; `X_minus <= X_plus` rowwise is asserted |
| `secondary_arrays(phi, supported, m, K) -> dict` | The same with `m[K]` in place of m4 (Δ1, Δ2; descriptive) |
| `naive_scores(phi, m32, m4)` | `phase_scores` on every row with the extension phase (one completion; never decision-bearing) |
| `support_reasons(ext, R) -> dict` | From a `chart.Extension`: counts of unsupported rows with resultant < 0.2 only, 8th-NN distance > R only, both; duplicate-query count |
| `support_report(ext, R, r4n, phi, m32, m4, sealed) -> dict` | §10 keys: `n`, `n_supported`, `fraction`, `reasons`, `resultant_summary`, `d8_summary`, `missing_mass` = mean((1−A)·r4n) (tree mean), `width` = 2·missing_mass, `mean_r4_supported`, `mean_r4_unsupported`. If `sealed` is False it also has `supported_contribution` = mean(A·u·r4) and `supported_conditional_mean`; if `sealed` is True those two keys are absent (§7.5) |

## 5. `k4b_decoder.py` (≈120 lines): the descriptive suffix decoder (§9.4)

| Function | Contract |
|---|---|
| `one_hot_suffix(canon32) -> float64 [n, 144]` | One-hot of canonical w29..w32, position-major (column `36·p + symbol`, p = 0..3) |
| `fit(canon32, seq_ids, phi, model) -> dict` | Rows: the 2,560 non-landmark cal rows (caller passes exactly those). Steps: `X = one_hot_suffix`; `mu_in, s_in = x4f_scores.standardizer(X)`; `Xs = (X − mu_in)/s_in`; `ell, status = rbf_bandwidth(Xs, SeedTree(0).generator(SCOPE, "suffix_rbf_bw", model), 1024)` (unpack and check `status`); `Omega, b = rbf_map(144, 2048, ell, SeedTree(0).generator(SCOPE, "suffix_rbf", model))`; `F = rbf_features(Xs, Omega, b)`; `Y = (cos φ, sin φ)`; panels = rank by ascending sequence_id // 512 (values 0..4); `res = x4f_probe.nested_ridge(F, Y, panels, F, Y, (1e-3, 1e-2, 1e-1, 1.0, 10.0))`; `mean_F, scale_F = standardizer(F)`; `Ft = (F − mean_F)/scale_F`; `probe = RidgeProbe([res.lam]).fit(Ft, Y, Ft, Y)`; `equivalence = max|probe.predict(Ft) − res.pred_val|`; `eq_tol, kappa = equivalence_tolerance(Ft, res.lam, probe.predict(Ft))`. Returns `{"status": "AVAILABLE" \| "UNAVAILABLE", "reason", "lam", "ell", "mu_in", "s_in", "Omega", "b", "mean_F", "scale_F", "W", "bias", "equivalence", "eq_tol", "kappa"}`. A degenerate bandwidth (`status` not ok, or non-finite or non-positive ell) → `UNAVAILABLE` ("degenerate bandwidth"); `equivalence > eq_tol` → `UNAVAILABLE` ("equivalence"). No fallback family. Never raises a gate failure for these two cases |
| `equivalence_tolerance(Ft, lam, pred) -> (tol, kappa)` | `Xc = Ft − mean(Ft, axis=0)`; κ = largest/smallest eigenvalue of `Xc′Xc + λI` (`eigvalsh`; inf if the smallest ≤ 0); `tol = max(1e-10, 64·finfo(float64).eps·κ·max|pred|)` (R13 formula, §5.6) |
| `predict_phase(dec, canon32) -> float64 [n]` | Applies the saved `mu_in, s_in, Omega, b, mean_F, scale_F, W, bias` to `one_hot_suffix(canon32)`; ψ = `vector_phase(pred)` (exact zero → 0). Refuses an UNAVAILABLE decoder |
| `agreement(phi, psi, supported) -> float` | |mean exp(i(φ − ψ))| over supported rows (descriptive, §9.4 b) |
| `to_arrays(dec)`, `from_arrays(a)` | npz round trip, no refit |

## 6. `k4b_charts.py` (≈220 lines): ledgers, charts, C0 gates, determinism

| Name | Contract |
|---|---|
| `TRAINED_LEDGER`, `INIT_LEDGER` | `"CHART_CONSTRUCTIONS_trained.json"`, `"CHART_CONSTRUCTIONS_init.json"` under the store |
| `InitLedger(path)` | Wraps `c1_chart.ConstructionLedger(path)`. `.claim(model, role)` raises `C1GateFailure("FAIL_TECHNICAL", "role 'direct' refused on the step-0 ledger")` for any role other than `"production"`, then delegates (the class forbids a repeated (model, role) pair, so at most 3 claims). `.claims()` delegates |
| `open_ledgers(out) -> (ConstructionLedger, InitLedger)` | Trained ledger: unchanged class, MAX 6 |
| `build_chart(X, ids, m32, ledger, model, role, cfg, guard=None, timed=None, persist=None) -> dict` | `m32`: float64 [512, 2] oracle m32 of the 512 landmark rows (production role; ignored for direct). Claims `(model, role)` on `ledger` **before** fitting; then `c1_chart.fit_chart_lcc(X, ids, cfg, guard, timed, persist)`; for role production, `gauge = c1_chart.fit_production_gauge(ch, m32[C*])` (alignment finite and > 0, else CHART_UNAVAILABLE); for role direct, `gauge = c1_chart.IDENTITY_CARRIER`. Returns `{"status": "PASS" \| status, "reason", "chart", "gauge", "serial": c1_chart.serialise(ch, gauge, role_label), "diagnostics"}`; role_label is `"production"` or `"validation_only"`. Exceptions: `adapt_chart_exception` first, else `classify_exception`. Never retried |
| `c0_cal(models, X_cal, ids, m32_land, out, cfg, guard, timed, persist) -> dict` | Production chart per trained model (trained ledger). The first non-PASS ends the gate with that status. Returns `{"status", "per_model": {j: build result}}` |
| `init_charts(models, X_cal_init, ids, m32_land, out, cfg, ...) -> dict` | Step-0 production chart per model (step-0 ledger). A valid `INCONCLUSIVE/CHART_UNAVAILABLE` → `{"status": "INIT_UNAVAILABLE", "reason"}` for that model, non-gating. A `FAIL_TECHNICAL/*` raises `C1GateFailure` at once (shared-code defect stops the cohort, RC10) |
| `freeze_production(out, charts, init, decoders) -> dict` | Writes `stages/S4a/PRODUCTION_FROZEN.json` with the sha256 of every serialised production chart, gauge, step-0 chart and decoder file, before any validation activation. Returns the record |
| `require_frozen(out) -> dict` | Raises `C1GateFailure("FAIL_TECHNICAL/LINEAGE", …)` unless `PRODUCTION_FROZEN.json` exists and every listed file re-hashes equal. Called before any validation or test activation |
| `extend(prod, gauge, Q, cfg, timed=None) -> chart.Extension` | `c1_chart.extend_phase` unchanged; phases checked finite and in [0, 2π) (else `FAIL_TECHNICAL/NUMERICAL`) |
| `c0_val_gate(models, prod, val_X, ids_val, out, cfg, ...) -> dict` | `require_frozen(out)`; direct chart per model (trained ledger, role `"direct"`, own GIANT); then `c1_chart.c0_val(prod, gauge, val_X_panel, direct, cfg)` unchanged. Status `PASS` iff every model passes; else the first failing model's `INCONCLUSIVE/CHART_UNAVAILABLE` (or FAIL_TECHNICAL). `chart_gates` is not called |
| `init_val_diagnostics(prod_init, gauge_init, val_X_panel, cfg) -> dict` | Support on the 512 val panel, bins and resultant for step-0 charts (reported; no fidelity) |
| `determinism_check(stored, recomputed) -> dict` | Bitwise equality (`dtype`, `shape` and bytes) of the 3,072 cal b0 activations, per checkpoint (3 trained + 3 step-0). `{"status": "PASS" \| "FAIL_TECHNICAL/DETERMINISM", "mismatch": [labels]}` |

## 7. `k4b_cert.py` (≈250 lines): references, moment check, row bounds, Lemma N, B_num, F, guards

| Function | Contract |
|---|---|
| `envelopes(Ks=KS) -> {K: Fraction}` | ε_K = `error_bound.moment_envelope(error_bound.posterior_envelope(K, 144), 144)` |
| `references(T, E, pi, coords, canon32, cache=None) -> list[dict]` | `error_bound.reference_moments(T, E, pi, coords, canon32, Ks=KS, cache=cache)`; never `reference_check_rows` or `certify_rows` |
| `moment_check(m_hat, refs) -> dict` | For every row and K: gap = max over the two coordinates of `|Fraction(float(m̂)) − Fraction(M̃)|`, compared with `MOMENT_TOL` exactly. `{"ok": bool, "max_gap": Fraction, "n_fail": int}`. `ok` False → `FAIL_TECHNICAL/ORACLE` (the caller raises) |
| `isqrt_bracket(s, D=10**80) -> int` | `s` a non-negative Fraction a/b; returns `k = math.isqrt(a·D² // b)` (so k/D ≤ √s < (k+1)/D) |
| `norm_bound(n_hat, M32, M4, eps4, eps32) -> Fraction` | Lemma N: r̃ = M̃32 − M̃4 as Fractions, s = r̃x² + r̃y², k = `isqrt_bracket(s)`, n = `Fraction(float(n_hat))`, B_N = max(|n − k/D|, |n − (k+1)/D|) + (3/2)(ε4 + ε32). For K ≠ 4, the same with ε_K |
| `phase_bound(x_hat, phi, MK, M32, epsK, eps32) -> Fraction` | `error_bound.row_bound(x_hat, phi, MK, M32, epsK, eps32)["B"]` |
| `endpoint_bounds(arrays, supported, phi, refs, eps, K=4) -> dict` | Per row: supported rows `phase_bound` for both X− and X+; unsupported rows `norm_bound` for both. B4 array: `norm_bound` on every row. Returns `{"B_minus": [Fraction], "B_plus": [Fraction], "B_norm": [Fraction], "max": {"minus", "plus", "norm"}}` |
| `control_bounds(scores, phi, refs, eps, K=4) -> dict` | `phase_bound` on every row; `{"B": [...], "max": Fraction, "certified": max ≤ CAP}` |
| `cap_ok(max_b) -> bool` | `max_b <= CAP` exactly (1e-4 passes; anything above fails) |
| `p2_ok(X) -> bool` | Every value finite and `|X| <= 4` |
| `certify(primary: dict, controls: dict) -> dict` | Primary (gating) arrays: X−_j, X+_j for every trained model and n̂. Non-finite, trap or flag, phase-range or P2 defect → raise `FAIL_TECHNICAL/NUMERICAL`; any primary max above CAP → status `INCONCLUSIVE/NUMERICAL`. Controls and step-0 arrays are certified and reported, never gating (labelled "uncertified" above CAP). `{"status", "max_B": {name: Fraction}, "certified": {name: bool}}` |
| `b_num(max_b, max_abs, n) -> Fraction` | `c1_bounds.B_constant(max_b, max_abs, n)` (max_b an exact Fraction) |
| `margin(B_num, Z_bound) -> Fraction` | F = max(B_num, FLOOR) + Z_bound |
| `F_plan(Z_bound) -> Fraction` | max(B_constant(Fraction(1, 10**4), 4, 12288), FLOOR) + Z_bound (§7.1) |
| `b4_guard(r4n, B_norm_max, Z_bound, seed, n) -> dict` | B^H = `b_num(B_norm_max, max r4n, n)`; tree means of r4n over 5,000 draws (`c1_means.bootstrap_means({"r4n": r4n}, seed)`); `lower, k = c1_means.quantile_with_rank(draws, 0.05)` (k = 250); `status = c1_bounds.guard_H5(lower, B^H + Z_bound)`. `{"lower", "rank", "B_H", "Z_bound", "status", "point"}`. Validation (seed 610102) gates; fresh (seed 610104) is reported, flag `FRESH_B4_LOW` iff status ≠ PASS |
| `transport_bound(T, E, pi, coords) -> dict` | `process_law.process_law_bound(T, E, pi, coords)`; requires status `BOUNDED`; `Z_bound` as an exact Fraction |

## 8. `k4b_stats.py` (≈260 lines): bootstrap, ranks, statuses, ladder, sealing

| Function | Contract |
|---|---|
| `joint_bootstrap(arrays, seed, draws=DRAWS) -> dict` | `c1_means.bootstrap_means(arrays, seed, draws)` unchanged (one index stream for every array) |
| `bounds(draws_minus, draws_plus) -> dict` | `L = quantile_with_rank(draws_minus, ALPHA)` (rank 84), `U = quantile_with_rank(draws_plus, 1 − ALPHA)` (rank 4,917), and central 95% intervals (ranks 125, 4,875) for both. Rank-check failure → `FAIL_TECHNICAL/NUMERICAL` |
| `model_status(L, U, F_minus, F_plus) -> dict` | Exact rationals, strict inequalities (§8.1). `SUPPORT` iff L − F− > 1/100; `EXCLUDE` iff U + F+ < 1/100 and L − F− > −1/100; else `UNRESOLVED`, written `UNRESOLVED/NUMERICAL` when the status with F− = F+ = 0 would be SUPPORT or EXCLUDE. `labels` contains `NEGATIVE_ALIGNMENT` iff U + F+ < −1/100. Returns `{"status", "labels", "status_without_F"}`. SUPPORT and EXCLUDE never both hold |
| `overall(per_model: {j: status}) -> str` | `SUPPORT` if all three SUPPORT; `EXCLUSION` if all three EXCLUDE; `MIXED` if at least one definite and not all the same definite; otherwise `INCONCLUSIVE`, or `INCONCLUSIVE/NUMERICAL` if any model is `UNRESOLVED/NUMERICAL` |
| `sd_upper(X_minus, X_plus, r4n, seed=610101) -> {(j, s): float}` | Per side s ∈ {"-", "+"}: `precision.sd_b4_draws(X_s, r4n_dict, MODELS, seed, 5000, 3072)` with both arguments int-keyed dicts; only `sd_draws` is used; SD^U = `quantile_with_rank(column, 1 − ALPHA)` (rank 4,917) |
| `mde_ok(sdU, N, F_plan) -> bool` | Every `precision.mde(sd, {"delta": float(MARGIN + F_plan), "alpha": float(ALPHA), "power": 0.80, "projected_N": N}) <= 0.02` |
| `centered(X_dict, keys, N, seed=610105) -> ndarray [5000, 6]` | `precision.centered_draws(X_dict, keys, seed, 5000, N)`; keys are `(j, s)` in MODELS order, "-" before "+" |
| `projection(e, keys, F_plan) -> dict` | §7.2(2) in float with F_plan as float: quantiles q_α (rank 84) of each "-" column and q_{1−α} (rank 4,917) of each "+" column via `quantile_with_rank`. SUPPORT scenario: succ = 0.02 + e− + q_α(e−) − F_plan > 0.01. EXCLUSION scenario: succ = [e+ + q_{1−α}(e+) + F_plan < 0.01] ∧ [e− + q_α(e−) − F_plan > −0.01]. Returns `{"support": {"per_model": {j: int}, "joint": int}, "exclusion": {...}, "ok": bool}`; `ok` iff every per-model and joint count ≥ 4,000 in both scenarios |
| `width_diagnostic(D_bar, e, keys, F_plan) -> dict` | §7.6: succ^w = [D̄ + e+ + q_{1−α}(e+) + F_plan < 0.01] ∧ [−D̄ + e− + q_α(e−) − F_plan > −0.01]; per-model and joint counts. Never gated; never computes C̄ |
| `ladder(X_minus, X_plus, r4n, F_plan, D_bar) -> dict` | For N in LADDER order: qualifies iff `mde_ok` and `projection(...)["ok"]`. Returns `{"status": "PASS" \| "INCONCLUSIVE/UNDERPOWERED", "N": int \| None, "k": N // 3072 \| None, "sdU", "candidates": {N: {"mde_ok", "projection", "width_diagnostic"}}}`. Each candidate uses the same seeds |
| `SEALED_KEYS` | `("mean_X_minus", "mean_X_plus", "control_means", "init_means", "decoder_means", "delta1_mean", "delta2_mean", "delta4_orc_mean", "supported_contribution", "supported_conditional_mean", "endpoint_ratios")` |
| `write_sealed(out, arrays) -> str` | The only writer of `SEALED_VALIDATION.json` (exclusive create, once, at P1). Computes the sealed means internally and returns the file's sha256. Nothing else exports or logs them |
| `check_unsealed(report) -> None` | Recursively refuses (raises `C1GateFailure("FAIL_TECHNICAL/SEALING", key)`) a validation report containing any `SEALED_KEYS` key, anywhere. Called by the validation-report writer |

## 9. `k4b_driver.py` (≈380 lines): release A stages (G0 → P1)

| Name | Contract |
|---|---|
| `GATE_ORDER` | `("G0", "H1", "REG1", "H2", "ORACLE-VAL", "B4-VAL", "C0-CAL", "C0-VAL", "CERT-VAL", "P1")` (release A), then in `k4b_fresh`: `("H2-FRESH", "T-PRE", "ENDPOINT")` |
| `run_gates(out, steps) -> list[dict]` | `steps`: ordered `[(gate, fn)]`, each fn returning a details dict and raising `C1GateFailure` (or any exception) on failure. Runs in order; each result is recorded with `stage_records.record_gate(out, gate, status, **details)`. At the first non-PASS, every later gate is recorded `NOT_RUN` and no later fn is called. Returns the records |
| `begin_stage(out, stage)` / `complete_stage(out, stage, files)` | Writes the operation marker (`op_guard.write_marker`) and a STAGES.jsonl begin entry; at completion a `STAGE_COMPLETE` entry with the sha256 of every file in `stages/<stage>/` |
| `classify_seed_hits(hits) -> dict` | G0 RC5 rule. Each hit `{"path", "text", "kind"}` with kind ∈ {`"k4b_declaration"` (this lineage's specification, constants, synthetic tests or authorised regeneration), `"prior_issuance"`, `"unclassified"`}. Status `PASS` iff every hit is `k4b_declaration`; any `prior_issuance` → `FAIL_TECHNICAL/SEED_SCOPE`; any `unclassified` → `FAIL_TECHNICAL/SEED_SCOPE` (fails closed). Every hit is recorded |
| `g0(out, release, mailbox) -> dict` | Authority hashes (CONTRACT `authority`), W1 evidence by hash, W3 attestation and K-REG1 reservation in release A, seed classification, store absent or lineage-only (`k4b_release.lineage_ok`), K4 FREEZE hashes of chart.py, cochain.py, errors.py, `check_chart_equality`. Missing authority/evidence/attestation → `INCONCLUSIVE/AUTHORITY`; hash, scope or seed defect → `FAIL_TECHNICAL/<reason>` |
| `h1(out, proc) -> dict` | Six checkpoints through `c1_model.load_model64` (round trip), meta run_key/step/status/payload sha/init seed (CONTRACT `checkpoints`), `load_process` identities, int keys, perms, E_canon identical, `validate_process`, `transport_bound` (Z_bound beside job 0018's 2.12e-12, report only), `c1_cert.a1_selftest()`, environment identity and one thread. Any defect → `FAIL_TECHNICAL/IDENTITY` |
| `reg1(out, release) -> dict` | `k4b_registry.build("K-REG1", out/"registry")`; coordinator completeness certificate in release A |
| `sample_cal_val(out, proc, release) -> dict` | `k4b_release.verify_reservation` immediately before sampling; draws cal b0 and val b0; writes the history tables |
| `h2(out, ...)`, `oracle_val(out, ...)`, `b4_val(out, ...)`, `c0_cal_stage(out, ...)`, `c0_val_stage(out, ...)`, `cert_val(out, ...)`, `p1(out, ...)` | The gates of §6 rows 3–9, as in the protocol table. `c0_cal_stage` also runs `init_charts`, the decoder (`k4b_decoder.fit`) and `freeze_production`. `p1` runs `k4b_stats.ladder`, `write_sealed` and writes the validation report through `check_unsealed` |
| `main(argv=None) -> int` | `--release <path>` (required), `--out` (default STORE). Verifies the release (`k4b_release.verify_release(path, "A", …)`), then runs `run_gates` over GATE_ORDER |

## 10. `k4b_fresh.py` (≈330 lines): K-REG2, fresh test, endpoint, export

| Function | Contract |
|---|---|
| `kreg2_step(out, release_b_draft) -> dict` | Identity-only: `k4b_registry.build("K-REG2", out/"registry", extra=<cal b0, val b0 tables>)`, inside the W2 reservation |
| `require_release_b(out, release_path, session) -> dict` | Refuses any fresh access (`C1GateFailure("FAIL_TECHNICAL/AUTHORITY", "no release B")`) unless a verified release B binds k, N, the K-REG2 sha256 and source inventory, the reservation, the worker session and the W3 record, and the coordinator ACCEPT of the validation report. Called before any test sampling or test-row read |
| `sample_test(out, proc, release) -> dict` | `verify_reservation` immediately before the first row; draws test b0 … b(k−1) |
| `h2_fresh(out, ...) -> dict` | Reservation still valid; `separation_fresh`; `seq_disjoint` (all K4b blocks, frozen union, ranges); `predicate_check` |
| `t_pre(out, ...) -> dict` | Oracle and references on every test row with `moment_check`; `determinism_check` on all 3,072 cal b0 activations (6 checkpoints, identical call `activations(model64, inputs, batch=1024)`); extension by the frozen production charts (`require_frozen`); `certify`; fresh `b4_guard` (seed 610104, report only) |
| `endpoint(out, ...) -> dict` | One `joint_bootstrap` (seed 610103) over X±_j, the controls (m4-phase, SHA), the step-0 arrays, the decoder scores, Δ1, Δ2 and Δ4^orc. Per model: `bounds`, `b_num` per side with `max_b` = the side's max row bound and `max_abs` = max |X̂|, `margin`, `model_status`; then `overall`. Report keys in §11 |
| `export(out, result) -> Path` | Writes `stages/S8/RESULT.json`; opens `SEALED_VALIDATION.json` only after RESULT.json exists |
| `main(argv=None) -> int` | `--release <path>` (release B), `--out` |

## 11. Report keys

- **Gate record** (`GATES.jsonl`, via `record_gate`): `gate`, `status`, `utc`, plus details. Chart gates also carry `diagnostics` per model (b, d, r, ℓ_max, components, excluded IDs, lift kind, g, residual, alignment, fidelity, bins, resultant).
- **Validation report** (`stages/S5/VALIDATION_REPORT.json`): `gates`, `chart_diagnostics`, `support` (per model and split, sealed form), `B4` (point, lower, B_H, Z_bound, status), `reference_discrepancy` (max moment gap per K), `sdU`, `ladder` (candidates, projection counts, width diagnostic), `certificate` (max B per array), `F_plan`, `Z_bound`, `sealed_sha256`, `c1prime_disclosure`. Never any `SEALED_KEYS` key.
- **Fresh result** (`stages/S8/RESULT.json`): `per_model[j]`: `L`, `U`, `L_rank` = 84, `U_rank` = 4917, `F_minus`, `F_plus`, `B_num_minus`, `B_num_plus`, `status`, `labels`, `status_without_F`, `central95_minus`, `central95_plus`, `point_minus`, `point_plus`, `width`, `missing_mass`, `support`; `controls[name][j]` (point, central95, alpha and 1−alpha bounds, max B, certified) for `m4_phase`, `sha_suffix`, `init`, `decoder`, `delta1`, `delta2`, `delta4_orc`, `naive`; `decoder_agreement[j]`; `ratios` (E X−/B4 and E X−/Δ4^orc, `"undefined"` when the denominator is ≤ 0 or undefined); `fresh_B4` (with `FRESH_B4_LOW` if flagged); `init_qualifier[j]` (true iff L−_init,j − F_init,j > 0.01) or `"unavailable (<reason>)"`; `overall`; `Z_bound`; `N`, `k`; `c1prime_disclosure`.

## 12. `k4b_release.py` (≈220 lines) and `k4b_meter_bind.py` (≈140 lines)

### 12.1 `k4b_release.py`: releases, freeze, pin check, reservations, lineage

| Function | Contract |
|---|---|
| `verify_release(path, kind, task_sha256, session) -> dict` | `kind` ∈ {"A", "B"}. JSON with `kind`, `job_id`, `task_sha256`, `worker_session`, `protocol_sha256`, `freeze_sha256`, `reservation` and (B only) `N`, `k`, `kreg2_sha256`, `kreg2_sources`, `accept`. Every field must match; `authorized_worker(release, session)` must hold. Failure → `FAIL_TECHNICAL/AUTHORITY` |
| `authorized_worker(release, session) -> bool` | Re-implemented R10 check: `release["worker_session"] == session` (non-empty strings) |
| `pin_check(repo, r_ref, h_exec) -> dict` | Runs `git diff --no-renames --name-status r_ref h_exec -- <CONTRACT s0.protected_paths>`; `PASS` iff every line is `A` of a path under `tools/k4b/` or `tests/k4b/`; else `INVALID` with the offending lines. Also checks every `reuse_sha256` and `protected_sha256` at h_exec, the C1′ CONTRACT chart section at h_exec = at r_ref, and the GAP doc blob sha256 |
| `freeze(out, repo, h_exec) -> dict` | Writes `FREEZE.json` (exclusive create): protocol sha256, h_exec, every k4b file sha256, every reuse file sha256 (full 64 hex), environment identity |
| `start_reservation(path, scope, utc)`, `verify_reservation(path, release) -> dict` | Reservation record `{"id", "scope": "K-REG1" \| "K-REG2", "start_utc", "end_utc": null, "state": "ACTIVE", "interruptions": [], "job_states": {...}}`. `verify_reservation` requires the record named by the release, state ACTIVE and no interruption. Before the first row: breach → `{"status": "CANCEL_RELEASE"}`; after sampling began: `{"status": "STOP/LINEAGE_REVIEW"}` |
| `archive_attempt(out, job, files, record_suffixes) -> Path` | §11.8: moves a failed attempt's files and the appended record suffixes to `superseded/<job>/` with a `SHA256SUMS` manifest; the attempt's ledger claims move with it |
| `restore_records(out, verified) -> None` | Restores `GATES.jsonl`, `STAGES.jsonl` and the ledgers to their verified pre-attempt bytes (byte-equal check after restore) |
| `lineage_ok(out) -> dict` | `PASS` iff the store is absent, or every file in it is listed in this lineage's superseded manifests or recorded stage records; any unrecorded prior file → `FAIL_TECHNICAL/LINEAGE` (refusal) |
| `regenerated_identical(old_sha, new_path) -> bool` | Bit-identical regeneration check; a mismatch is `FAIL_TECHNICAL/LINEAGE` |
| `needs_owner(correction) -> bool` | True iff the correction would change an already computed outcome-bearing quantity, or such a quantity was computed at or after the declared failure point. Outcome-bearing: B4 bounds, chart-validation criteria, SD bounds, N, endpoint/control/descriptive means. An unchanged quantity computed before that point alone → False |

### 12.2 `k4b_meter_bind.py`: meter binding (§11.7, RC11)

| Function | Contract |
|---|---|
| `bind(job_id, task_sha256, out, worker_session) -> None` | `controls.JOB_ID = str(job_id)`, `controls.TASK_SHA256 = upper(task_sha256)`; `meter.OUT = out`, `LEDGER = out/"cpu_ledger.json"`, `EMERGENCY = out/"cpu_ledger.emergency.jsonl"`, `LOCK = out/"RUN.lock"`, `ACTIVE = out/"METER_ACTIVE.lock"`, `LOG_DIR = out/"logs"`; `meter.CAP_S = meter.STOP_NEW_S = inf`; `meter.OUTPUT_CAP = 4·1024³`; `winjob.MEMORY_CAP = 12·1024³`; `meter.WORKER_SESSION = worker_session` (from the verified release) |
| `DISK_MIN_FREE` | `{"C:\\": 2_000_000_000, "X:\\": 30_000_000_000}` |
| `disk_reason(usage=shutil.disk_usage, minima=DISK_MIN_FREE) -> str \| None` | `"disk safe-STOP: <drive> free <n> < <min> bytes"`; unreadable free space → `"disk safe-STOP: <drive> free space unreadable (<Exc>)"` |
| `make_limiter(op_marker, disk=disk_reason, legacy=None, clock=time.time)` | Returns `limit_reason(ledger, child, args, active_wall, polls, mailboxes)`. `legacy` defaults to the original `meter.limit_reason`, captured at import before any wrapper is installed. Order on **every** poll: (1) call `legacy` exactly once; if it returns a kill reason, return `(reason, state)` unchanged (STOP, INVALID); (2) else, if `op_marker` is set, `op_guard.overdue(op_marker, clock())` → `(reason, state)`; (3) else, if `polls % 8 == 0`, `disk()` → `(reason, state)`; (4) else `(None, state)`. `state` is always legacy's control state, never a literal CONTINUE. HOLD alone never kills; a resource reason may still kill under HOLD (state stays HOLD). The early-return order of `c1_meter_bind.make_limiter` is not copied |
| `rewrite_argv(argv) -> list` | Drops any `--max-cpu`/`--max-wall` and appends `--max-cpu inf --max-wall inf` |
| `child_env(job, base=None) -> dict` | Copy of `base or os.environ` with `TEMP`, `TMP`, `TMPDIR` = `X:/Downloads/projects/topo-pilot/k4b-store/tmp-<job>` and every `meter.THREAD_VARS` entry = `"1"` |
| `classify_stop(reason, state) -> str` | Resource reasons (operation overdue, disk safe-STOP, memory, output cap) → `INCONCLUSIVE/RESOURCE`; STOP/INVALID keep their control semantics (`STOP`, `INVALID`) |
| `main() -> int` | `--release <path>` popped from argv; `verify_release`; `bind(...)` with the release's job id, task sha and worker session; RUN.lock identity must match; installs `make_limiter(op_marker=meter.OUT/op_guard.MARKER)`; `rewrite_argv`; runs `meter.main()` with `child_env` |

`op_guard.timed_factory(out, 600, …)` wraps each native operation (one deadline per operation, never per stage).

## 13. Implementation choices (protocol details left open; no scientific choice changed)

1. **Sealed-D-2a predicate representation.** It is applied to the canonical w1..w32 of each K4b history, the representation used for every registry comparison (D-2a raw tokens enter the same digest space without canonicalisation, §3.4 e).
2. **D-2a permitted pools** = every CONTRACT pool except `test` and `testN`; sealed ranges from `pools.json` n and the CONTRACT pool order.
3. **MDE comparison** (§7.2 rule 1) uses `precision.mde` unchanged, in float, with `delta = float(1/100 + F_plan)` and threshold 0.02. The projection (§7.2 rule 2) and the width diagnostic use F_plan as a float. Both are planning steps, not certified decisions.
4. **Projection quantiles** q_α and q_{1−α} use `c1_means.quantile_with_rank` (inverted_cdf; ranks 84 and 4,917).
5. **Phase wrap**: `np.mod(φ, 2π)`, then 2π → 0. Exact zero vectors map to phase 0 (m4-phase, Δ4^orc, decoder).
6. **SHA phase input**: canonical w29..w32 as four uint8 values (`row[28:32]`).
7. **FRESH_B4_LOW** is set iff the fresh `guard_H5` status is not PASS (the certified lower bound minus B^H + Z_bound does not exceed 0.01).
8. **Rerun and lineage machinery** (§11.8) lives in `k4b_release.py`; the G0 seed classification lives in `k4b_driver.py`.
9. **Reservation records** are JSON files written by the coordinator in the mailbox and named by the release; the code verifies them and never writes them.
10. **Decoder input standardisation**: the one-hot input is standardised with `x4f_scores.standardizer` before `rbf_bandwidth` (the "saved one-hot-input standardisation" of RC13). Columns are position-major.
11. **Per-model status label** `UNRESOLVED/NUMERICAL` is a status string; `NEGATIVE_ALIGNMENT` is a label beside the status.
12. **Bootstrap array order** in `joint_bootstrap` is insertion order. The draws do not depend on it, because one index vector per draw is shared.
13. **Unsupported-row certificate**: X∓ = ∓n̂ is exact in float, so its row bound is Lemma N's B_N (§5.3).
14. **Validation-report sealing** is enforced by key name (`SEALED_KEYS`), recursively, at the report writer.
15. **Store paths**: every function takes `out` (the store root) as an argument, so tests use temporary stores.
16. **Coverage from populated source-(a) ids** (R26 D3, job 0052): `revalidate_coverage(root_art, root=ROOT, extra_ids=None, store=None, seqs_a=None)`. The pinned call stays valid. `crs.observation_set_sources` fills its `seqs` map lazily, inside each reader, so `build` passes `seqs_a` = the map its `build_registry` run populated, and source (a) is not read twice. With `seqs_a=None`, the source-(a) readers are run once inside the function, through `c1_data.build_registry`; a fresh, unread map is never used. `missing` lists the `crs.coverage` keys with missing ids, plus every uncovered x4b id and `extra_ids` entry by value (`"id <n>"`). x4f misses are reported by key only. Handoff JSON validation reads with `utf-8-sig`, as the reused reader does (R26 D2).

### 13.1 Pinned return formats (job 0046; ruling of jobs/0045/review.md; pinned before the module code)

Authors' readings, binding where §1–§12 are silent:

16. **`k4b_stats.bounds`** returns `{"L": (value, rank), "U": (value, rank), "L_rank": 84, "U_rank": 4917, "central95_minus": ((lo, 125), (hi, 4875)), "central95_plus": ((lo, 125), (hi, 4875))}`; each value is a float from `quantile_with_rank` (author A accepts a float or a `(value, rank)` tuple).
17. **`k4b_stats.width_diagnostic`** returns `{"per_model": {j: int}, "joint": int}` (author A); `D_bar` is `{j: float}`.
18. **`k4b_stats.model_status`**: `status_without_F` is the §8.1 status with F− = F+ = 0, i.e. `"SUPPORT"`, `"EXCLUDE"` or `"UNRESOLVED"` (author A). Reference-moment inputs may be Decimal pairs (A); they enter certified comparisons through `Fraction`.
19. **`k4b_charts.c0_cal`** returns `{"status", "per_model": {j: build result}}`; `freeze_production(out, charts, init, decoders)` and `c0_val_gate(models, prod, …)` take `c0_cal(...)["per_model"]`. `init_charts` returns `{"status", "per_model": {j: build result or {"status": "INIT_UNAVAILABLE", "reason"}}}` (author B reads `res.get("per_model", res)`).
20. **`k4b_release.needs_owner(correction)`**: `correction = {"defect": str, "quantities": [{"name", "outcome_bearing": bool, "changed": bool, "at_or_after_failure": bool}]}`; True iff some quantity is outcome-bearing and (changed or at_or_after_failure) (author B).
21. **`k4b_release.restore_records(out, verified)`**: `verified` maps a record file name (relative to `out`) to its verified bytes. **`archive_attempt(out, job, files, record_suffixes)`**: `files` is a list of paths inside `out`; `record_suffixes` maps a record file name to the appended suffix text; each suffix is written as `superseded/<job>/records/<name>.suffix` (author B).
22. **D-2a `pools.json`** is `{pool: {"n": n}}` (author B).

Items both authors left unpinned (simplest form consistent with the protocol):

23. **`k4b_stats.write_sealed(out, arrays)`**: `arrays` maps a `SEALED_KEYS` name to a 1-D float64 array, or to a dict (int model or str control name → array, nested at most twice). The file holds `{"protocol_sha256", "means": <same nesting, tree means as floats, keys as str>}`. Exclusive create; an existing file raises and is left byte-unchanged.
24. **`k4b_data.duplicates`**: `n_duplicate_rows = n_rows − n_unique` (the extra copies beyond the first of each digest).
25. **`k4b_meter_bind.disk_reason`** on unreadable free space: `"disk safe-STOP: <drive> free space unreadable (<type(exc).__name__>: <exc>)"`.
26. **`k4b_registry.source_d`** on a registry_v1 sha256 that differs from CONTRACT: raises `C1GateFailure("FAIL_TECHNICAL/LINEAGE", "registry_v1 sha256 mismatch")`.

## 14. Contract completion (job 0047; ruling R17 of jobs/0046/review.md). Signatures before code

Pure functions are side-effect free: they open no file and return plain dicts. The protocol wins on conflict. §14.4 lists open protocol questions; the signatures below do not decide them.

### 14.1 `k4b_driver`: checkpoint-meta check (§9 `h1`; §2.2)

| Function | Contract |
|---|---|
| `checkpoint_meta(artifact_root, artifact_id) -> dict` | Reads only `<artifact_root>/Checkpoint/<artifact_id>/meta.json` (JSON; no payload or state file). `artifact_root` = `ROOT/"topo-pilot"/"artifacts"`. Unreadable or malformed → `C1GateFailure("FAIL_TECHNICAL/IDENTITY", …)` |
| `expected_meta(model, step_label) -> dict` | From CONTRACT: `{"artifact_id": checkpoints[str(model)][step_label], "artifact_type": "Checkpoint", "run_key": [run_key[0], run_key[1], model], "step": steps["trained"] if step_label == "step5000" else steps["init"], "status": "complete", "init_seed_key": f"init/{run_key[0]}/{run_key[1]}/{model}", "init_seed": checkpoints[str(model)]["init_seed"], "payload_sha256": None (see §14.4 Q1)}`. `step_label` ∈ {"step5000", "step0"}; `model` is an int of MODELS |
| `check_checkpoint_meta(meta, expected) -> dict` | Pure. Compares each item exactly (`==` with `type(...) is` for ints, so a str seed, str step or str model fails): `meta["artifact_id"]`, `meta["artifact_type"]`, `meta["config"]["run_key"]` (a list `[family, mode, int model]`), `meta["config"]["step"]` (int), `meta["status"]`, `meta["seed_map"][init_seed_key]` against `init_seed`, and `meta["payload_sha256"]` against `expected["payload_sha256"]` when that is not None. A missing key is a mismatch. Returns `{"status": "PASS" \| "FAIL_TECHNICAL/IDENTITY", "mismatches": [{"field", "expected", "found"}], "checked": [field names in the order above]}` |
| `h1(out, ctx)` (addition) | For each model j and step_label in ("step5000", "step0"): `check_checkpoint_meta(checkpoint_meta(root, id), expected_meta(j, step_label))` **before** `c1_model.load_model64`. The first non-PASS raises `C1GateFailure("FAIL_TECHNICAL/IDENTITY", <mismatches as JSON>)`. The gate record carries every result under `checkpoint_meta` (`{"1729/step5000": result, …}`) |

### 14.2 `k4b_fresh`: control arrays, summaries, agreement, ratios, init qualifier, support (§9, §10, §11)

`CONTROL_NAMES = ("m4_phase", "sha_suffix", "init", "decoder", "delta1", "delta2", "delta4_orc", "naive")`.
- An entry is **two-sided** (`{"X_minus", "X_plus", "phi", "supported"}`: init, delta1, delta2) or **one-sided** (`{"X", "phi"}`: the others).
- Model-free controls (m4_phase, sha_suffix, delta4_orc) are keyed `"all"`; the others by int model.
- An unavailable entry is `{"unavailable": "<reason>"}`.

| Function | Contract |
|---|---|
| `control_arrays(m, canon32, ext, init_ext, decoders) -> dict` | Pure. Inputs: `m` = `{K: float64 [n, 2]}`, the test oracle moments (K ∈ KS); `ext` = `{j: chart.Extension}`, the frozen production charts on the test rows; `init_ext` = `{j: Extension or {"unavailable": reason}}`, the frozen step-0 charts; `decoders` = `{j: decoder dict}`. Returns `{name: {key: entry}}` with these entries:<br>• m4_phase: `{"X": phase_scores(m4_phase(m4), m32, m4), "phi"}`<br>• sha_suffix: `{"X": phase_scores(sha_phase(canon32), m32, m4), "phi"}`<br>• init[j]: `endpoint_arrays(init_ext[j].phase, init_ext[j].supported, m32, m4)` plus `phi`, `supported`<br>• decoder[j]: `{"X": phase_scores(ψ_j, m32, m4), "phi": ψ_j}` with ψ_j = `predict_phase(decoders[j], canon32)`, on every row<br>• delta1[j], delta2[j]: `secondary_arrays(ext[j].phase, ext[j].supported, m, K)` (K = 1, 2) plus `phi`, `supported`<br>• delta4_orc: `{"X": phase_scores(oracle_phase(m32), m32, m4), "phi"}`<br>• naive[j]: `{"X": naive_scores(ext[j].phase, m32, m4), "phi": ext[j].phase}` |
| `control_bounds_all(controls, refs, eps) -> dict` | Same keys; each entry is `{"max_B": Fraction, "certified": bool}`. One-sided: `k4b_cert.control_bounds(X, phi, refs, eps, K=4)`. Two-sided: `k4b_cert.endpoint_bounds(entry, supported, phi, refs, eps, K)` with K = 4 (init), 1 (delta1), 2 (delta2); `max_B` = the max of the minus, plus and norm maxima. `certified` = `cap_ok(max_B)` and `p2_ok` of every array. Never gating |
| `bootstrap_inputs(arrays, controls) -> dict` | The one ordered dict for the single `joint_bootstrap(…, 610103)`: first `f"X:{j}:-"`, `f"X:{j}:+"` for every j in MODELS order; then each available control entry in `CONTROL_NAMES` order, as `f"{name}:{key}:-"`/`f"{name}:{key}:+"` (two-sided) or `f"{name}:{key}"` (one-sided) |
| `control_summary(draws, controls, bounds_all) -> dict` | Pure. Per control entry: `{"point", "central95", "alpha_bound", "one_minus_alpha_bound", "max_B": str(Fraction), "certified": bool, "label"}`.<br>• `point`: tree mean of X, or the pair (mean X−, mean X+).<br>• `central95`: ((lo, 125), (hi, 4875)) per side.<br>• `alpha_bound`: `quantile_with_rank` of the X draws (or the X− draws), at ALPHA.<br>• `one_minus_alpha_bound`: the same for the X draws (or the X+ draws), at 1 − ALPHA.<br>• `label`: `"uncertified"` iff not certified, else absent.<br>Unavailable entries pass through unchanged. Rank checks as in `k4b_stats.bounds` |
| `decoder_agreement(ext, decoders, canon32) -> dict` | `{j: k4b_decoder.agreement(ext[j].phase, predict_phase(decoders[j], canon32), ext[j].supported)}`; an UNAVAILABLE decoder gives `"unavailable (<reason>)"` |
| `ratios(mean_X_minus, B4, delta4_orc_mean) -> dict` | Pure. Returns `{"EX_minus_over_B4": r1, "EX_minus_over_delta4_orc": r2}`, each a float numerator/denominator, or the string `"undefined"` when the denominator is None, non-finite or ≤ 0 (§9.6, §9.7). Called per model j with that model's mean X̂− |
| `init_qualifier(init_entry, L_init, F_init) -> bool \| str` | Pure. `"unavailable (<reason>)"` if the entry is unavailable; else `Fraction(L_init) − Fraction(F_init) > Fraction(1, 100)` (strict, exact; §9.3). `L_init` = the rank-84 bound of the init X− draws. `F_init` = `margin(b_num(max_B_init_minus, max abs X−_init, n), Z_bound)` (see §14.4 Q3) |
| `support_entries(ext, R, arrays, m) -> dict` | `{j: support_report(ext[j], R, arrays[j]["r4n"], ext[j].phase, m[32], m[4], sealed=False)}`. RESULT `per_model[j]["support"]` is that dict and `per_model[j]["missing_mass"]` is its `missing_mass` (on fresh rows the unsealed form is allowed) |

### 14.3 `k4b_fresh.endpoint`, `load_frozen` and `main` (E2, release B)

| Function | Contract |
|---|---|
| `endpoint(arrays, controls, bounds_all, fresh_b4, Z_bound, decoders, ext, canon32, m, R) -> dict` | **Inputs:** `arrays` = `{j: endpoint_arrays plus "bounds" (endpoint_bounds)}` from T-PRE; `controls` = `control_arrays(...)`; `bounds_all` = `control_bounds_all(...)`; `fresh_b4` = the `b4_guard` result with `FRESH_B4_LOW`.<br>**Computation:** one `joint_bootstrap(bootstrap_inputs(arrays, controls), 610103)`. Per model: `bounds`; B_num per side (`max_b` = the side's max row bound, `max_abs` = max abs X̂ of that side, n = test rows); `margin`; `model_status`. Then `overall`.<br>**Returns** the RESULT dict with exactly the §11 keys:<br>• `per_model[j]`: L, U, L_rank, U_rank, F_minus, F_plus, B_num_minus, B_num_plus, status, labels, status_without_F, central95_minus, central95_plus, point_minus, point_plus, width, missing_mass, support<br>• `controls[name][key]` (`control_summary`), `decoder_agreement`, `ratios[j]` (`ratios(point_minus_j, B4, delta4_orc point)`), `fresh_B4`, `init_qualifier[j]`, `overall`, `Z_bound`, `N`, `k`, `c1prime_disclosure`<br>Writes nothing; Fractions are given as str |
| `load_frozen(out) -> dict` | `k4b_charts.require_frozen(out)` first. Returns `{"prod": {j: {"chart", "gauge"}}, "init": {j: {"chart", "gauge"} or {"unavailable": reason}}, "decoders": {j: decoder}}`, read from `stages/S4a/CHART_<j>.npz`, `INIT_CHART_<j>.npz` (`chart.chart_from_arrays`) and `DECODER_<j>.npz` (`k4b_decoder.from_arrays`). No refit, no gauge |
| `main(argv=None) -> int` | **Flags:** `--release` (release B, required), `--session` (required), `--out` (default STORE), `--mailbox`.<br>**Steps:**<br>1. `require_release_b`.<br>2. `k4b_data.load_process()`.<br>3. The six checkpoints: `check_checkpoint_meta`, then `load_model64`.<br>4. The cal b0 and val b0 tables from `stages/S3/HIST_*.npz`, each re-hashed against its STAGE_COMPLETE record.<br>5. `load_frozen`.<br>6. `sample_test` (the reservation is verified first).<br>7. `run_gates` over `("H2-FRESH", "T-PRE", "ENDPOINT")`: T-PRE builds `controls` and `bounds_all`; ENDPOINT calls `endpoint`.<br>8. On ENDPOINT PASS, `export(out, result)`.<br>Returns 0 iff every fresh gate is PASS. K-REG2 is built earlier by `kreg2_step` (a W2 job), never by `main` |

### 14.4 Open protocol questions (not decided here)

- **Q1 (payload sha).**
  - §9 `h1` names "payload sha", but CONTRACT `checkpoints` binds only the artifact IDs, not a payload sha256.
  - The meta `payload_sha256` of `c3358e3c…` is `bcd024ef…`. That is not the byte sha256 of `payload.npz`, so the store's own hashing rule applies.
  - Question: which expected value binds? Either the ArtifactStore's load-time integrity check alone (`expected["payload_sha256"] = None`, as pinned above), or explicit values added to the contract.
- **Q2 (B4 in E X−/B4).** §9.7 reports E X−/B4. Is B4 the test point E‖r̂4‖ (`fresh_b4["point"]`), or a certified bound (lower or upper)? `ratios` takes B4 as an argument and does not choose.
- **Q3 (F_init).** §9.3 reads "L−_init,j − F_init,j > 0.01" without defining F_init. The signature above assumes the §5.5 rule applied to the init X− array, with the same Z_bound. Confirm, or name the intended F.
- **Q4 (two-sided control bounds).** For the identified-set controls (init, Δ1, Δ2), are the "α and 1 − α bounds" taken from the X− and X+ draws respectively, as for the endpoint (the signature's reading), or reported for both sides?

## 15. Coordinator rulings R19–R23 on the job-0047 questions and the dry inventory (coordinator 75dcd488, 2026-10-16; jobs/0047/review.md). Binding for job 0048 and for the author-B round

**R19, Q1 (payload sha).** Explicit values are bound.
- CONTRACT `checkpoints[j]["meta_payload_sha256"]` = {step5000, step0}. These are the `payload_sha256` fields read from the six `meta.json` files (metadata only).
- `expected_meta` sets `payload_sha256` from these values; it is never None.
- `check_checkpoint_meta` compares them exactly, as strings.
- The bytes are bound separately by the ArtifactStore load-time integrity check, which runs unchanged inside `load_model64`/`stage.load_model`.
- Protocol §6 row 1 requires the payload sha check. This makes it explicit.

**R20, Q2 (B4 in E X−/B4).** B4 is the fresh-test point value `fresh_b4["point"]` (the tree mean of ‖r̂4‖ over the test rows), and E X− is the test point mean of X−. The ratio is descriptive (§9.7); it is never a gate and carries no certificate claim. `ratios(mean_X_minus, fresh_b4["point"], delta4_orc_mean)`.

**R21, Q3 (F_init).** F_init,j is the §5.5 margin applied to the init X− array of model j:
- F_init,j = max(B_num(init X−_j), 1e-9) + Z_bound, with B_num from `c1_bounds.B_constant` on the init array's own row bounds and max |X̂|, using the same Z_bound as the endpoint.
- An init array whose B exceeds the cap is "uncertified", and then `init_qualifier` = "unavailable (uncertified)".

**R22, Q4 (two-sided controls: init, Δ1, Δ2).** Report as for the endpoint:
- the α bound from the X− draws and the 1 − α bound from the X+ draws;
- for each side separately, the point value and central 95% interval (`point_minus`/`point_plus`, `central95_minus`/`central95_plus`), with the certified B for each side.

No status is computed for a control.

**R23, registry classification (dry inventory, jobs/0047/report.md).** These rules are amendments to `k4b_registry.inventory`/`classify`/`build`. They tighten coverage and never loosen it.
1. **ObservationSet stores with their own payloads** (x5g1-research-store, x5g1t-research-store, x5g1t-fixture-run, and any directory of that shape):
   - they are SCANNED through source (f): `observation_set_sources(store=ArtifactStore(LocalFSBackend(<dir>/store or <dir>/study/store)), root=<that store root>)`;
   - they are canonicalised by their EmissionSpec perm when it resolves, otherwise they contribute raw `tokens[:, :32]`;
   - a history file that lies inside a scanned ObservationSet root counts as covered;
   - any other history file in the directory → INCOMPLETE.
2. **Synthetic-fixture classification ("only synthetic test fixtures", RC7).** A directory, or a subtree of main, is NOT_SCANNED with reason "synthetic test fixtures" only when **every** history-bearing, identity-bearing or unreadable file in it meets both conditions:
   - **(a)** its path contains a pytest basetemp segment: `pytest-of-*`, a directory whose name starts with `bt` or `pt-` directly under a `tmp-*` or `coord-scratch` directory, or a `--basetemp` root;
   - **(b)** every history array it holds has at most 1,024 rows, read from the header.

   Any file that fails (a) or (b) makes the directory INCOMPLETE. The manifest lists every such file, with its path and header shape.
3. **Main (`topo-pilot`) is also inventoried deep.** Reader (a) covers main's artifact store. Every other history-bearing file in main's tree, including `tests/` fixtures and `.venv`, must satisfy rule 2(a′): its path is under `tests/`, under a pytest basetemp segment, or under `.venv`, and it has at most 1,024 rows. Otherwise main is INCOMPLETE. The manifest states this explicitly.
4. **Unreadable files** (deliberately truncated fixtures) count under rule 2 only if they satisfy 2(a). Otherwise INCOMPLETE.
5. **The dedicated-reader directories stay excluded from the generic deep scan** (agent-handoff, c1prime-store, d2a-store), so no sealed D-2a payload is ever opened by the generic scan.

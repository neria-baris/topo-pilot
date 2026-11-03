# tools/hwsu: written contract, phase 2 (model phase, response family only; job 0223 phase 1; derived from HWSU-DESIGN-v1)

## Erratum E1 (R-0223-3..5, coordinator, RULINGS.md of job 0223)

- **R-0223-3 (OPEN-1 resolved, no phase-1 change).** Every phase-2 module lives in the new package `tools/hwsu/u2/` (same file names): `u2/__init__.py`, `u2/hwsu_model.py`, `u2/hwsu_known.py`, `u2/hwsu_registry.py`, `u2/hwsu_gates.py`, `u2/hwsu_driver.py`, `u2/hwsu_dry2.py`, plus the new phase-2 audit `u2/hwsu_bind_u2.py` (section 2.6; `audit_u2` moves there from `hwsu_known`). The frozen phase-1 audit globs `tools/hwsu/hwsu_*.py` non-recursively, so it never sees `u2/`. CONTRACT.json records the phase-2 allowlist (`binding.allowlist` phase-2 entries, `binding.allowlist_conditional_u2`) and `binding.conditional_reads_u2`, limited to `hwsc_gates.expected_meta_c`, `hwsc_registry_build._default_sources`, and `hwsb_train.train` / `hwsc_data.make_train_dev_c` in the DRU dry run only; any other forbidden read fails closed (`FAIL_TECHNICAL/BINDING`). Read lists re-derived from source at this erratum (equal to the spec's lists).
- **R-0223-4 (OPEN-2 resolved).** KFIT and FEAS feed only share gates and are not drawn under S3: added to section 12 (O-14 rewritten); removed from S3 `sample_e1`, H2-U, H3-U, the CONTRACT split sizes, store layout, DRU tiny sizes and the test plan.
- **R-0223-5 (OPEN-7 resolved).** No package is installed. Where a function cannot be imported for the read audit (`psutil` missing for `hwsc_registry_build.build`), the audit reads its source by path and parses it (AST) without importing it (section 2.6); DRU-REG equality is checked in the dry run.
- **OPEN-3..10** are accepted as written (coordinator, RULINGS.md); section 14 marks them.

**This file is the phase-2 `API.md` of protocol §11.1, written as a new file `API_U2.md`** (coordinator ruling R-0223-2, procedural, F-2). Protocol §11.1 names the phase-1 documents `API_OF.md`/`TEST_PLAN_OF.md` and reserves `API.md`/`TEST_PLAN.md` for phase 2; phase 1 committed its documents as `API.md`/`TEST_PLAN.md` (phase-1 API D-0). Phase 2 therefore never modifies or renames a phase-1 file: its documents are `API_U2.md` (this file), `CONTRACT.json` and `TEST_PLAN_U2.md`. Where the protocol says "API.md" or "TEST_PLAN.md" for phase 2, read these files.

**Authority.** `tools/hwsu/PROTOCOL_HWSU_v1.md` (byte copy of HWSU-DESIGN-v1, sha256 `9efbabdf…af88eb`). Owner addendum 43 (track U phase 2, response family only, approved through its real stages; no runtime approvals), addenda 41–42 (CPU pause lines released), addendum 44 (Claude agents write code and tests). Phase-1 result `hwsu-store/OF_ACCEPT.json`: **OF_PASS_RESPONSE_ONLY** (N_resp 4,096). Coordinator rulings R-0223-1 (response family only; §12 below lists every omitted design item), R-0223-2 (new files), R-0213-1, R-0213-2, R-0206-1 (folded in below).

**Precedence.** Protocol > `CONTRACT_OF.json` > `CONTRACT.json` > this file > `TEST_PLAN_U2.md`. The phase-1 `API.md` stays authoritative for every phase-1 module; this file never restates a phase-1 contract differently, it only calls it. A difference is a contract defect to report through the coordinator. Choices the protocol leaves open are listed in §10 (U-D-n); ambiguities for the response-only scope are §14 (OPEN-n).

**Nothing here authorises a run.** Implementation only: no checkpoint loaded on real scope, no real-process sampling, no metered run, no store write. Preflight, the DRU dry run, the execution freeze and the KC/E1/REG2/E2 stages are separate jobs.

## 0. Conventions (in addition to phase-1 API §0, which applies unchanged)

- **Phase-2 modules** (protocol §11.1, "Phase" = 2, restricted to the response family): `hwsu_model`, `hwsu_known` (without KU), `hwsu_registry`, `hwsu_gates`, `hwsu_driver`, `hwsu_dry2`, and the phase-2 audit `hwsu_bind_u2`, all files of the package `tools/hwsu/u2/` (E1, R-0223-3; plus `u2/__init__.py`, which appends the package directory to `sys.path` so that the modules import one another by their flat names). Each ≤ 400 lines (`tools/check_file_sizes.py`); a size split adds a module by an API erratum and keeps every name reachable as `<module>.<name>`. **No existing file is edited** (phase-1 files are bound by `FREEZE_OF.json`; protocol §4.1, F-2).
- **Import convention.** Each phase-2 module starts `from __future__ import annotations  # noqa: I001` then `import hwsu_config as uc` (which sets `sys.path`, phase-1 API §0) then `import u2  # noqa: F401` (the package `__init__` adds `tools/hwsu/u2` to `sys.path`). Phase-2 modules import phase-1 modules by name (`hwsu_records as ur`, `hwsu_pairs as up`, `hwsu_oracle as uo`, `hwsu_of as uof`, `hwsu_seed as us`, `hwsu_bind as ub`, `hwsu_freeze as ufz`, `hwsu_resv as urv`) and never re-implement a phase-1 name. Dependency order (no import-time cycle): phase-1 modules ← `hwsu_bind_u2` (imports `hwsu_bind` only) ← `hwsu_model` ← `hwsu_registry` ← `hwsu_known` ← `hwsu_gates` ← `hwsu_driver` ← `hwsu_dry2`. `c2_model` (torch) is imported only by `hwsu_model` and, lazily, by functions that need it.
- **Test import aliases** (TEST_PLAN_U2 §1): `hwsu_model as um2`, `hwsu_known as uk`, `hwsu_registry as ureg`, `hwsu_gates as ug`, `hwsu_driver as ud`, `hwsu_dry2 as udry2`, plus the phase-1 aliases.
- **Reuse only through the call allowlist.** A reused name is referenced as `<module>.<name>` and must be in CONTRACT `binding.allowlist` (phase-1 and phase-2 entries, merged) or `binding.allowlist_conditional_u2` (see §2.6). No phase-2 code references a name in `binding.never_called` or `binding.never_called_u2`. Every study-specific object (process, scope, seeds, sizes, masters, store, root, models) is passed as an argument.
- **Symbols.** Oracle quantities are canonical (phase-1 API D-1). Model quantities are **named** per model j: the model input is `[BOS = 36, perm_j[w1..w32]]` (`c1_model.model_inputs(perm_j[canon32])`), and every oracle vector that meets a logit or the readout is mapped by `c1_oracle.named_from_canonical(x, perm_j)` first (protocol §2.3). `perm_j = proc["perm"][j]` of `hwsb_data.build_process`.
- **Numbers.** As phase-1 API §0: thresholds are `Fraction`s; a float enters a comparison as `Fraction(float(x))`; means are `c1_means.tree_mean`; per-pair arrays are row-aligned in arm-1 sequence-id order (S2).
- **Statuses.** Phase-1 strings plus `NOT_RUN/SHARE_DROPPED` (a share-family gate under S3), `NOT_RUN/<gate>`, `EXCLUDED_j/<gate>`, `INC_j/NUMERICAL`. Errors are `c1_records.C1GateFailure(status, reason)`; `hwsu_records.status_of` maps exceptions.
- **Gate runner.** Every job uses `hwsu_records.run_gates_u(out, steps, continuing=CONTRACT gates_u2.continuing_statuses)` (`PASS`, `REPORTED`, `NOT_RUN/SHARE_DROPPED`). A share-family gate is a step whose function returns `{"status": "NOT_RUN/SHARE_DROPPED"}` without computing anything (§4.9).
- **Writes.** Only inside the `out`/`store` argument (exclusive create; arrays only through the phase-1 `hwsu_records.save_array`, phase-1 prefixes only: U-D-6), plus the append-only `GATES.jsonl`/`STAGES.jsonl`, the study ledger and `logs/`. HWSU never writes `hwsc-store`, `hwsd-store` or any other store.
- **Footprint (R-0213-2).** Implementation, tests and the dry run write no array file and no ArtifactStore artifact anywhere under `X:/Downloads/projects/topo-pilot/`. Pytest basetemp `X:/Downloads/topo-scratch/test_hwsu-<job>/pytest`; TEMP/TMP/TMPDIR and every DRU helper folder under `X:/Downloads/topo-scratch/test_hwsu-<job>/`; the DRU dry store is `X:/Downloads/topo-scratch/hwsu-dry-u2-<job>/` (OPEN-5); dry history files are `DRYHIST_*`.
- **Blindness.** Every direct file read goes through `hwsu_config.guard`/`read_json`/`read_bytes`/`sha256_file` (phase-1 API §1.3). Never opened: `hwsc-store/stages/S8/**` (RESULT.json: presence and hash only, from `STAGES.jsonl`), `stages/S5/**`, `stages/E1/L1.json`, `SEALED_*.json`, `sealed/**`, the TRAIN_RECORD key `dev_ce`, any track-D planning file, `HWSD-*`, any `hwsd-store` file other than its obligations, reservations and `reservations/*.END.json`.
- **OF values.** Phase-2 code reads `OF_ACCEPT.json` (keys of CONTRACT `authority_u2.of_accept.keys_read`) and, in KC6 and H5-U only, `OF_REPORT.json` `EG` (§2.3, §4.4). No OF value changes a threshold, margin, ladder or construction.

## 1. `hwsu_model.py` (≈ 300 lines): stage-C loading, the readout, activations, the response arrays, M0, X1, the logit policy

### 1.1 Stage-C identity and loading (protocol §3.1)

| Name | Contract |
|---|---|
| `TRAIN_KEYS` | `("checkpoint_ids", "checksums", "run_key", "status")` (CONTRACT `stage_c_u2.train_record_keys`) |
| `read_train_record(path, root=uc.ROOT) -> dict` | `raw = uc.read_bytes(path, root)`; `json.loads(raw.decode("utf-8-sig"), object_pairs_hook=hook)` where `hook` keeps only pairs whose key is in `TRAIN_KEYS` **at the top level** (nested dicts under kept keys are kept whole); every other top-level key (e.g. `dev_ce`) is dropped by the hook before any later access. A missing whitelisted key → `C1GateFailure("FAIL_TECHNICAL/IDENTITY", …)`. Returns the whitelisted dict |
| `stage_complete_sha(store, stage, relpath) -> str or None` | the `files[relpath]` value of the **last** `STAGE_COMPLETE` record of `stage` in `<store>/STAGES.jsonl` (read with `uc.read_bytes`, one JSON object per line); None when absent (mirror of `hwsc_gates._stage_complete_sha`) |
| `checkpoint_meta_u(artifact_root, artifact_id) -> dict` | `uc.read_json(<artifact_root>/Checkpoint/<artifact_id>/meta.json)`; not a dict or unreadable → `FAIL_TECHNICAL/IDENTITY` (mirror of `k4b_driver.checkpoint_meta`, never called) |
| `load_checkpoint_u(artifact_root, artifact_id)` | `ArtifactStore(LocalFSBackend(artifact_root)).load(Checkpoint, artifact_id, consumer="experiment")` with `topo_pilot.contracts.ArtifactStore`, `topo_pilot.contracts.Checkpoint`, `topo_pilot.contracts.backends.LocalFSBackend` (mirror of `k4b_driver.load_checkpoint`, never called) |
| `identity_c(hwsc_store, handoff, contract=None) -> dict` | **H1-U identity without loading** (also KC2). For each j in `MASTERS` (order 620301, 620302, 620303): (1) `rel = stage_c_u2.train_records[j].relpath`; `uc.sha256_file(store/rel)` must equal the CONTRACT sha256 **and** `stage_complete_sha(store, f"TRAIN_{j}", rel)`; (2) `rec = read_train_record(...)`, `rec["status"] == "COMPLETE"`, `rec["checkpoint_ids"]["5000"] == stage_c_u2.checkpoint_ids[j]`; (3) `exp = hwsc_gates.expected_meta_c(j, 5000, rec)` (unchanged; OPEN-1), `meta = checkpoint_meta_u(store/"artifacts", exp["artifact_id"])`, `k4b_config.check_checkpoint_meta(meta, exp)["status"] == "PASS"`. Then `hwsc_gates.exclusion_check(ids, handoff)["ok"]` (`handoff` = `hwsu_config.load_handoff_u()`). Any failure → `FAIL_TECHNICAL/IDENTITY`. Returns `{"records": {j: rec}, "meta": {j: check result}, "ids": {j: id}}` |
| `charts_identity(hwsc_store, contract=None) -> dict` | `PRODUCTION_FROZEN.json` re-hashes to `stage_c_u2.production_frozen.sha256`; `uc.read_json` of it; for each `CHART_<j>.npz`: `uc.sha256_file(store/"stages/S4a"/name)` equals both the record's `files[name]` and the CONTRACT copy; the record's `gauges` equal the CONTRACT copy exactly (JSON equality). No chart is loaded (np.load is never called on a chart; §12 item O-11). Failure → `FAIL_TECHNICAL/IDENTITY` |
| `load_stage_c(hwsc_store, ident, contract=None) -> dict` | requires `torch.get_num_threads() == 1` after `torch.set_num_threads(1)` (else `FAIL_TECHNICAL/IDENTITY`); for each j: `ck = load_checkpoint_u(store/"artifacts", ident["ids"][j])`; `model64, sha = c1_model.load_model64(ck)` (bitwise float64 round trip; it raises `FAIL_TECHNICAL/MODEL`). Returns `{j: {"model64", "state_sha": sha, "checkpoint_id"}}` |

### 1.2 Inputs, activations and the readout (protocol §2.4, §2.5; C2 Lemma R)

| Name | Contract |
|---|---|
| `named_inputs(canon32, perm) -> torch.Tensor [n, 33]` | `c1_model.model_inputs(np.asarray(perm)[np.asarray(canon32, dtype=np.int64)])` (BOS 36 first) |
| `basis_u(model64) -> dict` | `c2_model.readout_basis(model64)` (keys `gamma`, `beta`, `WU`, `N1`, `Q0`, `R_diag`, `rank_ok`, `M`, `WUbeta`, `ln_eps`) |
| `readout_y(model64, canon32, perm, basis, batch=1024) -> np.ndarray [n, 127]` | `acts = c2_model.activations3(model64, named_inputs(canon32, perm), batch)` (its logits are discarded unread by the reused pass); `y = c2_model.readout_coords(acts["ln_final_out"], basis)`; `acts` is deleted. **No logit is formed** (the policy does not apply) |
| `a_full(d_named, M, y1, y2) -> [n]` | `c2_attrib.half_dot(d_named, (y1 − y2) @ M.T)` — A_full = ½dᵀMΔy (protocol §2.5) with `d_named = named_from_canonical(d, perm_j)` |
| `response_arrays(A, G) -> dict` | `{"ZR010": A − 0.1·G, "ZR030": A − 0.3·G, "AF": A}` (float64; `0.1`, `0.3` = `float(RESP_LO)`, `float(RESP_HI)`) |
| `row_cross_check(q1bar_named, q4bar_named, y1, basis) -> [n]` | descriptive Lemma P2 single-row form: `z1 = c2_model.closed_logits(y1, basis)`; returns `np.sum((q1bar_named − q4bar_named) * z1, axis=1)` (E[zᵀρ4], protocol §2.6) |

### 1.3 The logit policy (protocol §2.10; the C2 `LogitPolicy` pattern, mirrored)

| Name | Contract |
|---|---|
| `GATE_ORDER_U` | `("BASIS", "M0", "X1", "P1", "T-PRE", "NUM", "ENDPOINT")` |
| `ALLOWED_U` | `{"basis": {"BASIS"}, "m0": {"M0", "T-PRE"}, "x1": {"X1", "T-PRE"}, "test_endpoint": {"NUM", "ENDPOINT"}}` |
| `class UPolicy(done=())` | `begin(gate)`: refuses (`FAIL_TECHNICAL/BINDING`) a gate not in `GATE_ORDER_U`, a gate earlier than one already begun, or a begin while another gate is current; `end(gate)` clears; `require(kind)`: the current gate must be in `ALLOWED_U[kind]`, and for `"test_endpoint"` `"T-PRE"` must be in `done` with status PASS (`mark_pass("T-PRE")`), else `FAIL_TECHNICAL/BINDING`. `c2_model.natural_pass`, `identity_patch` and `x1` call `policy.require(kind)`; an `UPolicy` is passed to them. Refusals in code: no FIT logit (KFIT and FEAS are not drawn, R-0223-4) except BASIS (κ_X1 on 1,024 FIT rows) and the M0 identity rows; X1 ephemeral; no TEST token before release B (driver, §5.4); no endpoint array before T-PRE passes |

### 1.4 BASIS, M0, X1 (protocol §6 rows 6, 11, 12)

| Name | Contract |
|---|---|
| `basis_gate(models, fit_canon, perm, policy) -> dict` | per j: `b = basis_u(model64)`; `b["rank_ok"]` (rank 127); on the 1,024 lowest-id FIT rows: `policy.begin("BASIS")`, `acts, z = c2_model.natural_pass(model64, named_inputs(fit[:1024], perm_j), policy, "basis")` (kind `"basis"`, allowed only at BASIS); `y = readout_coords(acts["ln_final_out"], b)`; `kappa = c2_model.kappa_x1(acts["ln_final_out"], y, b, z)`; `ok = c2_model.x1_attainable(kappa)`; `del z`; `policy.end("BASIS")`. Fail (rank or attainability) → `FAIL_TECHNICAL/MODEL` (study). Returns `{"per_model": {j: {"rank_ok", "R_diag_min_max", "kappa_x1", "attainable"}}}` |
| `m0_u(model64, sha, ident_j, inputs, acts, z_net, basis, d_canon, perm, policy) -> dict` | the `c2_model.m0` sequence (`c2_model.py:228-257`) with its identity step replaced: `checks["ids"] = ident_j["checkpoint_id"] == CONTRACT stage_c_u2.checkpoint_ids[j]`; `checks["state_sha"] = sha == ident_j["state_sha"]` (the value H1-U recorded in this job); `checks["roundtrip"] = True`; then unchanged calls `c2_model.identity_patch(model64, inputs, acts, policy)` (kind `"m0"`), `rank = basis["rank_ok"]`, `c2_model.readout_identity(z_net, y, basis)`, `c2_model.two_route(d_canon, named_from_canonical(d_canon, perm), z_net, perm)`, `kappa_x1`, `x1_attainable`; plus `c2_model.symbol_order_a(inputs, canon32, perm)` (requires `canon32`; passed in `ident_j["canon32"]`), `symbol_order_b(perm)`, `symbol_order_c(d_canon, perm)` (protocol §6 row 11). Status: any check other than `attainable` False → `FAIL_TECHNICAL/MODEL`; only `attainable` False → `INCONCLUSIVE/NUMERICAL`; else `PASS`. `c2_model.m0` is never called |
| `m0_gate(models, ident, val_a1, perm_of, d_canon, policy) -> dict` | on the 1,024 lowest-id VAL pairs' **arm 1** (U-D-3): `policy.begin("M0")`; per j: `inputs = named_inputs(a1[:1024], perm_j)`; `acts, z = c2_model.natural_pass(model64, inputs, policy, "m0")`; `m0_u(...)`; `del z`; `policy.end("M0")`. First non-PASS → raises with that status (study) |
| `x1_gate(models, val, perm_of, basis_of, policy) -> dict` | `policy.begin("X1")`; per j and per arm k ∈ (a1, a2) on **every** VAL pair: `acts, z = natural_pass(model64, named_inputs(arm_k, perm_j), policy, "x1")`; `y = readout_coords(acts["ln_final_out"], basis)`; `r = c2_model.x1(model64, {f"{j}:{k}": (inputs, y, z, ids_k)}, basis, policy)` (natural arms: `z_ref` given; no interchange arm, no KU head); every logit deleted. Any `r["status"] != "PASS"` → `FAIL_TECHNICAL/X1` (study). Returns `{"arms": {name: {"max_dev", "n_over"}}, "ids_over": [...]}` (identity diagnostics only) |

## 2. `u2/hwsu_known.py` (≈ 330 lines): binding, freeze, S0, authority, attestation, G0U, KC0–KC6

### 2.1 OF binding (R-0206-1)

| Name | Contract |
|---|---|
| `of_binding(store=uc.STORE, contract=None) -> dict` | `acc = uc.read_json(store/"OF_ACCEPT.json")` re-hashes to `authority_u2.of_accept.sha256`; only the keys of `of_accept.keys_read` are used; `acc["verdict"] == "ACCEPT"`; `acc["outcome"] == "OF_PASS_RESPONSE_ONLY"`; `acc["freeze_of_sha256"] == uc.sha256_file(store/"FREEZE_OF.json") == of_accept.freeze_of_sha256 == authority_u2.freeze_of.sha256`; `acc["N_resp"] == 4096`. Any failure → `INCONCLUSIVE/AUTHORITY`. Returns `{"status": "PASS", "outcome", "share_outcome": "INCONCLUSIVE/ORACLE_FEASIBILITY", "freeze_of_sha256", "of_accept_sha256"}`. This is the **only** source of the share outcome |

### 2.2 Execution freeze and S0 (protocol §4.1, §6 row S0)

| Name | Contract |
|---|---|
| `implementation_files_u(repo, h_exec, contract=None) -> dict` | `{relpath: sha256 of the git blob at h_exec}` for every CONTRACT `phase2_files` entry and every `tests/hwsu/test_a_u2_*.py`, `tests/hwsu/test_b_u2_*.py`, `tests/hwsu/AUTHORSHIP_A_U2.md`, `tests/hwsu/AUTHORSHIP_B_U2.md` present at h_exec (via `git ls-tree`/`git cat-file`, the `hwsu_freeze` helpers) |
| `freeze_u(store, repo, h_exec, dru_report, j_u_records, written_by) -> dict` | writes `store/FREEZE.json` (exclusive) with CONTRACT `freeze_u2_fields`: `protocol`, `protocol_sha256`, `contract_of_sha256`, `contract_sha256` (blob of `CONTRACT.json` at h_exec), `api_u2_sha256`, `test_plan_u2_sha256`, `freeze_of_sha256` and `of_accept_sha256` (from `of_binding`), `h_exec`, `r_ref` (CONTRACT `s0_u2.r_ref`), `implementation_files`, `implementation_sha256` (sha256 of the canonical JSON `json.dumps(obj, sort_keys=True, separators=(",", ":"))`), `reuse_sha256` (phase-1 `reuse_sha256` ∪ `reuse_sha256_u2`, re-hashed at h_exec; any mismatch → refused), `dry_run_report_path`, `dry_run_report_sha256` (refused unless the report's `implementation_sha256` equals the one computed here and `all_pass` is True), `j_u_records` (`[{"path", "sha256"}]`, re-hashed), `environment`, `written_by`, `created_utc`. Also refuses unless `hwsu_freeze.verify_freeze_of(store, repo)` passes. Refusals: `FAIL_TECHNICAL/FREEZE`, nothing written |
| `verify_freeze_u(store, repo) -> dict` | re-checks every hash of `FREEZE.json` against the working tree (file bytes) and `reuse_sha256` (both tables); `verify_freeze_of` too. Absent → `C1GateFailure("INVALID", "FREEZE.json absent")`; mismatch → `INVALID` |
| `s0_u(store, repo, r_ref=None) -> dict` | in order: (1) `verify_freeze_u`; (2) `git diff --no-renames --name-status <r_ref> <h_exec>` (r_ref default CONTRACT `s0_u2.r_ref` = 49ac9c9, the phase-1 h_exec): every line allowed by `s0_u2.allow` (status `A`: a `phase2_files` path, `tests/hwsu/test_a_u2_*.py`, `tests/hwsu/test_b_u2_*.py`, the two `AUTHORSHIP_*_U2.md`, `docs/code_index/**`; status `M`: `docs/code_index/**`); (3) both reuse tables equal at r_ref and h_exec; (4) `hwsu_bind_u2.audit_u2()["status"] == "PASS"`. Returns `{"status": "PASS", "h_exec", "diff", "audit"}`; any failure → `INVALID` |

### 2.3 Authority and the run approval

| Name | Contract |
|---|---|
| `auth_u(store, job, stage, mailbox=uc.MAILBOX, contract=None) -> dict` | `store/f"AUTH_U_{job}.json"` (coordinator-written; schema `hwsu-auth-v1`; fields `stage` ∈ {KC, E1, REG2, E2}, `job`, `owner_approval {path, sha256}`, `freeze_sha256`, `written_by`, `written_utc`): `stage` matches; `owner_approval` equals CONTRACT `authority_u2.run_approval` (path, sha256) and the mailbox file re-hashes; `freeze_sha256 == uc.sha256_file(store/"FREEZE.json")`. Failure → `INCONCLUSIVE/AUTHORITY` |

### 2.4 Reservation attestation with R-0213-1

| Name | Contract |
|---|---|
| `end_obligation_path(end_rec, end_path, root) -> Path or None` | R-0213-1. `store = end_path.parent.parent` (the store holding `reservations/`); `rel = end_rec["obligation_file"]`; candidates in order `store/rel`, `root/rel`; the first that **exists** and whose resolved path lies inside `store.resolve()` is returned; otherwise None (bounded to that store: a candidate outside the store is never used) |
| `w2_attestation_u2(root, own=None, w2_end=None, w2_end_sha256=None) -> dict` | identical to phase-1 `hwsu_resv.w2_attestation` (phase-1 API §5.5) except in rule (b): the obligation file is `end_obligation_path(...)` (None → the reservation counts as **live**). Same return keys. Used by G0U and KC0; the phase-1 function is not changed |

### 2.5 G0U and KC (protocol §6 rows KC and 0)

| Name | Contract |
|---|---|
| `g0_u(out, ctx, stage) -> dict` | the phase-1 `hwsu_seed.g0_of` order with these changes: (1) authority: CONTRACT `authority.addenda` and `authority_u2.addenda` re-hash; the design file and freeze record re-hash; `auth_u(out, ctx["job"], stage)` (in place of `AUTH_OF_<job>`); `of_binding(out)`; (2) records as phase 1 (namespace, W2 end record and its three bound files, joint rulings and addenda 1–3); (3) namespace as phase 1 (`hwsu_seed.namespace_overlap`); (4) store: `hwsu_records.lineage_u(out)`; (5) attestation: `w2_attestation_u2(ctx["root"], own=ctx["reservation_id"])` PASS; (6) needles: `hits = hwsu_seed.seed_search_u(ctx["root"], hwsu_seed.needles())`, `c = hwsu_seed.classify_hits_u(hits)`; writes `out/stages/<stage>/G0U.json` (exclusive) `{"status", "hits", "checks"}`. Failures as phase 1 (`INCONCLUSIVE/AUTHORITY`, `FAIL_TECHNICAL/SEED_SCOPE`, `FAIL_TECHNICAL/LINEAGE`) |
| `kc0(out, ctx)` | `g0_u(out, ctx, "KC")` |
| `kc1(ctx)` | `hwsu_of.of_p(ctx)` (phase 1, unchanged: in-memory w\* build and identity) |
| `kc2(ctx)` | `hwsu_model.identity_c(ctx["hwsc_store"], load_handoff_u())` plus `charts_identity(...)` (no checkpoint loaded) |
| `kc3(ctx)` | the synthetic known cases re-run in the job, in a helper folder `X:/Downloads/topo-scratch/test_hwsu-<job>/kc3/` (R-0213-2): `hwsu_dry.dro2(base)` (KS-PAIR), `hwsu_dry2.ks_p(base)` (KS-P), `hwsu_dry2.ks_rules(base)` (KS-RULES, response part); each must return `PASS` |
| `kc4(ctx)` | `audit_u2()` PASS |
| `kc5(out, ctx)` | registry rehearsal: `hwsu_registry.build_u("REHEARSAL", out/"registry"/"rehearsal", root=ctx["root"], scratch=uc.SCRATCH, handoff=hwsb HANDOFF dict, own=None)`; records `cpu_s`, `peak_memory_bytes`, the store size (sum of file sizes under `out`) and the projection `size_end = size_now + 2·(rehearsal registry bytes) + history bytes for 57,344 + 8,192·8 histories`; requires the rehearsal status PASS and `size_end ≤ output_cap_bytes / 2` (else `INCONCLUSIVE/RESOURCE_OR_AUTHORITY`, a resource erratum before E1) |
| `kc6(out, ctx)` | OF reproduction: reads `stages/OF/HIST_OF_eval_a1_b{0,1}.npz`, `HIST_OF_eval_a2_b{0,1}.npz` (own history tables; each re-hashed against the OF STAGE_COMPLETE), `o1 = hwsu_oracle.arm_oracle(…a1…)`, `o2 = …(a2)`, `G = hwsu_oracle.pair_core(o1, o2)["G"]`; `repr(float(tree_mean(G)))` must equal `OF_REPORT.json` `EG.point` (OF_REPORT re-hashes to `of_accept.of_report_sha256`). Failure → `FAIL_TECHNICAL/KNOWN_CASE` |
| `kc_report(out, records) -> Path` | `stages/KC/KC_REPORT.json` (exclusive) `{"schema": "hwsu-kc-report-v1", "gates", "rehearsal": {...}, "store_bytes", "projection", "written_utc"}` |

### 2.6 The phase-2 audit `u2/hwsu_bind_u2.py` (protocol §11.2; E1, R-0223-3, R-0223-5)

`u2/hwsu_bind_u2.py` (about 120 lines; imports `hwsu_config as uc`, `hwsu_bind as ub`, `ast`, `copy`, `importlib`, `pathlib`; no other phase-2 module) is the phase-2 counterpart of the phase-1 `hwsu_bind` and does not edit it. The phase-1 audit (`hwsu_bind.audit`, test `test_audit_real_phase1_files_pass`) globs `tools/hwsu/hwsu_*.py` non-recursively and so never reads `u2/`; it keeps passing unchanged.

| Name | Contract |
|---|---|
| `u2_files() -> list` | every `tools/hwsu/u2/*.py` (sorted), including `__init__.py` and `hwsu_bind_u2.py` itself |
| `merged_contract(contract=None) -> dict` | deep copy of the loaded CONTRACT with `binding.allowlist` ∪ `binding.allowlist_conditional_u2` (merged per module and function), `binding.never_called` + `binding.never_called_u2`, `binding.conditional_reads` + `binding.conditional_reads_u2` |
| `reads_by_path(module, qualname) -> dict` | the AST-by-path fallback (R-0223-5): locates `<module>.py` under `tools/`, parses it with `ast.parse` **without importing it**, finds the top-level function `qualname`, and returns `{"<module>.<name>": True}` for every `alias.name` attribute reference in that one function body whose alias is a module imported at the file's top level (alias resolved to the module name); nothing transitive. Used only for an allowlist entry that carries `"ast_by_path": true` |
| `function_reads_u2(module, qualname, entry) -> dict` | if `entry.get("ast_by_path")`: `reads_by_path`; otherwise import the modules of `entry.get("import_first", [])` in that order (needed for `hwsc_registry_build`, whose module cannot be imported first because of the `hwsc_registry` import cycle) and call `ub.function_reads(module, qualname)`. An `ImportError`/`ModuleNotFoundError` on an entry without `ast_by_path` is not swallowed: the audit returns `FAIL_TECHNICAL/BINDING` naming the missing module |
| `audit_u2(files=None, contract=None) -> dict` | `files` default: `u2_files()`. (1) Calls: `ub.audit_calls(files, merged_contract())`. (2) Reads: for every allowlisted function under `tools/` (phase-1 table, phase-2 table, conditional table) the key set of `function_reads_u2` equals its `call_time_reads` keys (for an `ast_by_path` entry: equals its `ast_refs`); a forbidden read is admitted only when `(function, read)` is in `binding.conditional_reads` or `binding.conditional_reads_u2`, which names exactly `hwsc_gates.expected_meta_c`, `hwsc_registry_build._default_sources`, `hwsb_train.train` and `hwsc_data.make_train_dev_c` (the last two referenced only from `hwsu_dry2`, the DRU dry run; a reference to them from any other `u2/` file fails). Any other forbidden read fails closed: `FAIL_TECHNICAL/BINDING`. Returns `{"status", "calls", "reads", "by_path"}`, where `by_path` lists the entries audited by path |

**`hwsc_registry_build.build` (R-0223-5).** `ub.function_reads` imports the modules a function mentions; `build` reaches `psutil` (imported inside `_peak_memory`), absent from the venv, and no package is installed. Its allowlist entry carries `"ast_by_path": true` and `ast_refs` (the `alias.name` references of its body, recorded at this erratum from the source). The audit parses `tools/hwsc/hwsc_registry_build.py` and compares the by-path set to `ast_refs`; equality of its result with `build_u` is checked in the dry run (DRU-REG), where the real call path runs. `build` is called only by `hwsu_dry2.dru_reg`.

## 3. `hwsu_registry.py` (≈ 390 lines): K-REG mirror and the U readers (protocol §8.2–§8.3)

| Name | Contract |
|---|---|
| `build_u(version, out_dir, root, scratch, handoff, own=None, extra=None, sources=None) -> dict` | **mirror of `hwsc_registry_build.build`** (`hwsc_registry_build.py:60-153`), line for line, with: `version` ∈ CONTRACT `registry_u2.versions` (REHEARSAL, K-REG1, K-REG2; `own` required for K-REG1/K-REG2, refused for REHEARSAL); `src_fn = hwsc_registry_build._default_sources(root, scratch, run_dir, handoff, out_dir.parent, None)` (OPEN-1) updated with `sources_u(...)` below (which replace `own`, `scratch` and `inventory` and add `hwsc`, `hwsu_dry`, `hwsd`, `kreg2_c`); tags `["c2", "c2sup", "c2scratch", "hws", "x6zc", "c2nd", "hwsb", "dry", "hwsc", "hwsu_dry", "hwsd"]` + (`["own"]` unless REHEARSAL); manifest `"registry_version": "hwsu-reg-v1"`, `"protocol_sha256"` = HWSU's; `"hwsu_sources"` = summaries of the added tags; the U8 union and the S-2 diagnostic (`"superset_diagnostic": {"n_missing", "missing_head"}`) computed before U8 is added; the digest file and manifest written as in the original (`stage_records.save_npz`, `write_new`); `peak_memory_bytes` by a local copy of `_peak_memory` (OPEN-7). Status `PASS` / `INCONCLUSIVE/REGISTRY_INCOMPLETE` / `FAIL_TECHNICAL/LINEAGE` |
| `sources_u(root, scratch, store, own_expected, contract=None) -> dict` | `{"hwsc": λ: source_hwsc(root/"hwsc-store"), "hwsu_dry": λ: source_own_dry(scratch), "hwsd": λ: source_hwsd(root, scratch), "own": λ: source_own_u(store, own_expected), "kreg2_c": λ: source_kreg2_c(root/"hwsc-store"), "scratch": λ readers_ok: hwsc_registry.scratch_check(scratch, table=scratch_table_u(), readers_ok=readers_ok), "inventory": λ readers: inventory_u(root, readers)}` |
| `source_hwsc(store, contract=None) -> dict` | **U2**, the joint layout reader (J1): (i) `hwsc_registry.source_own(store, expected=OBS_INVENTORY)` (unchanged), where `stages/TRAIN/OBS_INVENTORY.json` re-hashes to its `TRAIN_INVENTORY` STAGE_COMPLETE entry and to CONTRACT `stage_c_u2.obs_inventory.sha256`; (ii) each of `stage_c_u2.u2_hist` read by the K4b history-table reader (`canon32`, `seq_ids`, `digest` re-derived from `canon32` by `k4b_data.digests`) after its sha256 equals its S3/S7 STAGE_COMPLETE entry; (iii) classed without opening: `artifacts/{WorldSpec,TransitionSpec,EmissionSpec,Checkpoint}/**` and `superseded/*/artifacts/**` by `meta.json` `artifact_type`, `registry/**`, `stages/S4/ORACLE_*`, `stages/S4a/{ACTS,CHART,DECODER,INIT_CHART}_*`, `logs/**`, `tmp/**`; blinded and `sealed` paths never opened; (iv) any other array file, or a listed history file missing or not re-hashing → `INCONCLUSIVE/REGISTRY_INCOMPLETE`. Returns the `hwsc_registry._new/_close` record shape (`status`, `digests`, `seq_ids`, `files`, `other`, `non_history`, `present`) |
| `source_kreg2_c(store, contract=None) -> dict` | **U8**: `registry/K-REG2_digests.npz` re-hashes to `stage_c_u2.k_reg2.digest_file_sha256` (else INCOMPLETE); reads `digests` (`<U64`, sorted) and `seq_ids`; returns `{"status", "digests", "seq_ids", "n"}`. A digest file, not a history payload |
| `superset_diagnostic(union_sorted, kreg2_sorted, chunk=1_000_000) -> dict` | S-2: counts and lists (first 100) digests of `kreg2_sorted` not in `union_sorted`, comparing the two sorted arrays chunk by chunk (no second in-memory set); `{"n_missing", "missing_head"}`; never a status |
| `source_own_u(store, expected, contract=None) -> dict` | **U6**: every `HIST_*.npz` listed in a `STAGE_COMPLETE` of `store/STAGES.jsonl` (OF, and for K-REG2 the E1 tables), re-hashed against its entry, read by the K4b history-table reader; `expected` = the list of relpaths the caller requires present (K-REG1: the six OF tables; K-REG2: OF + E1 tables); an unlisted `HIST_*` file or a mismatch → INCOMPLETE |
| `read_obligation_u2(store, root, contract=None) -> dict` | J10 reader for another store: the phase-1 rule of `hwsu_resv.read_obligation` (newest by `written_utc` governs; closed classes and bases; sha256 re-hash; basis `artifact` Checkpoint never opened) applied with each obligation's **own** `name_rules`; returns `{"status", "problems", "history": [{"relpath", "class", "reader"}]}` |
| `source_hwsd(root, scratch, contract=None) -> dict` | **U5** (READER_IF_PRESENT; J3, J4, J10): `root/hwsd-store` absent → PASS with no digests; present → `read_obligation_u2` must PASS and every listed history file is read by its reader (`k4b_history_table` or `hwsb_registry.registry_digests` for ObservationSets); the same for every `scratch/hwsd-dry*` and `scratch/test_hwsd-*` directory that holds an array file. Track-D END records are read with R-0213-1 (`hwsu_known.end_obligation_path`). Only obligation, reservation and END files of `hwsd-store` are opened (blindness) |
| `source_own_dry(scratch, contract=None) -> dict` | **U2′**: each `scratch/hwsu-dry*` store by its own `REGISTRY_OBLIGATION.json` (`read_obligation_u2`; an array file without an obligation → INCOMPLETE); each `scratch/test_hwsu-*` root: EXCLUSION by the fixture rule (synthetic DRY-scope rows only): any `HIST_*`-named file, ObservationSet root or file holding a registered-scope sequence id → INCOMPLETE |
| `scratch_table_u(contract=None) -> dict` | stage C's `registry.scratch_inventory` (`tools/hwsc/CONTRACT.json`, read through `uc.read_json`) updated with CONTRACT `registry_u2.scratch_u2.rows` (TO_FREEZE); the reserved globs are routed to U2′/U5 and are not rows |
| `inventory_u(root, readers, contract=None) -> dict` | **U7**: mirror of `hwsc_registry.inventory_c` (`hwsc_registry.py:307`) with the table `root_table_u()` (stage C's `registry.inventory` with `registry_u2.root_table_u2.add` applied, `hwsc-store` → READER U2) and `deep_scan_exclude` + `deep_scan_exclude_add`; calls `k4b_registry.inventory(root, exclude)` and `k4b_registry.classify(inv, readers)`; R8 rule; returns `{"status", "inv", "classes", "unlisted", "violations"}` |
| `separation_u(reg, tables, seq_union) -> dict` | H2 requirements (protocol §8.3): every digest of every arm ∉ `reg` (`c2_registry.separation` pattern via `c2_registry.Registry.contains`), splits pairwise disjoint, sequence ids disjoint from `seq_union` and from each other; `{"collisions", "seq_overlap", "ok"}` |

## 4. `hwsu_gates.py` (≈ 390 lines): E1/E2 gates, P1, the decision table, outcomes, licences, sealing

Every gate function takes `ctx` and returns a details dict with `"status"` or raises `C1GateFailure` (study scope). Gate names in `GATES.jsonl` are the CONTRACT `gates_u2.jobs` names.

### 4.1 E1 gates (protocol §6 rows 0–15, response family)

| Gate / name | Computation | Pass | On failure |
|---|---|---|---|
| G0U `hwsu_known.g0_u(out, ctx, "E1")` plus release A present (`RELEASE_A.json`, §8.3) | §2.5 | all hold | as §2.5 |
| H1-U `h1_u(out, ctx)` | `identity_c`, `charts_identity`, `load_stage_c` (one torch thread), `hwsu_of.of_p(ctx)` (process identity; per-master `perm`), `hwsc_records.lineage_c(hwsc_store)` PASS (U-D-9), `hwsc-store/FREEZE.json` and `STAGES.jsonl` re-hash to CONTRACT, the S8 STAGE_COMPLETE lists `stages/S8/RESULT.json` with `stage_c_u2.result_presence.sha256` (never opened). Writes `stages/E1/H1U.json` (exclusive; ids, meta checks, `state_sha` per model, threads, process identity). Sets `ctx["models"]`, `ctx["ident"]`, `ctx["proc"]` | all | `FAIL_TECHNICAL/IDENTITY` |
| REG1 `reg1(out, ctx)` | `build_u("K-REG1", out/"registry", …, own=six OF tables)`; status PASS; release A's completeness certificate binds the KC5 rehearsal manifest sha256 | PASS | `INCONCLUSIVE/REGISTRY_INCOMPLETE` |
| RESERVATION | phase-1 `hwsu_of.reservation_check(ctx)` with `RES-HWSU-U` (or `-a<k>`) | PASS | `INCONCLUSIVE/AUTHORITY` |
| S3 `sample_e1(out, ctx)` | `begin_stage(out, "E1_S3")`; `ctx["rows_drawn"] = True` before the first draw; scope `hwsu-v1`: fit `sample_singles(…, "fit", b, 4096)` b ∈ {0, 1}; `sample_pairs(…, "val", 0, 4096)` (kfit and feas are not drawn, R-0223-4); tables `hwsu_pairs.history_table(canon32, ids, label, b)` (labels `fit`, `val-a1`, … as phase-1 §2.3) saved as `stages/E1/HIST_<split>_<arm>_b<b>.npz` (`fit_s`, `val_a1`, `val_a2`) in that order; `complete_stage(out, "E1_S3", files)` | — | sampler exception `FAIL_TECHNICAL/SAMPLER` |
| H2-U `h2_u(ctx)` | `separation_u(K-REG1, tables, seq_union)`; `k4b_data.predicate_check(stack of every arm, ("sealed_d2a",))`; `hwsc_data.p_d2a_check(proc, p_D2a)` and `hwsu_records.registry_risk_u(p_D2a, 24,576 + 32,768 + 8,192·8)` (the protocol's maximum count, an upper bound: kfit and feas are not drawn, R-0223-4) | 0 collisions, predicate false, risk ok | `FAIL_TECHNICAL/LINEAGE`; predicate → `INCONCLUSIVE/REGISTRY_INCOMPLETE` |
| H3-U `h3_u(ctx)` | per split (fit, val): `arm_oracle` per arm, `suffix_oracle([a1, a2])`, `pair_core`; OF-1 (i)–(v) exactly as phase-1 `hwsu_of.of_1` (suffix equal, q4/m4 bitwise and `m4_check`, finite log-evidence, KO identities with `readout_A(…, helmert(36))`, Decimal rows on the 4 lowest-id pairs) on val; on fit singles: finite `le`, Decimal `q32` on the 4 lowest-id rows; every arm: `max |Σ_v q̄ − 1| ≤ c2_config.T_QSUM`. KO categories are **not** run here (KC-U). Saves `stages/E1/ORACLE_E1_<split>.npz` (`G`, `le_a1`, `le_a2`, `d` for pairs; `le` for fit) | all | `FAIL_TECHNICAL/SAMPLER` (i–iii) or `/ORACLE` (iv–v, Σq) |
| H5-U `h5_u(ctx)` | `b = c2_decide.stream_bounds({"G": G_val}, 640113, float(ALPHA_HEADROOM), 5000)`; `rank_L == 250`; (a) `Fraction(float(b["G"]["L"])) > 1/100`; (b) the OF-2 re-check: `OF_REPORT.json` `EG.L` (bound by `of_report_sha256`) `> 1/50` (OPEN-3) | both | `INCONCLUSIVE/HEADROOM` |
| BASIS | `hwsu_model.basis_gate` on the 1,024 lowest-id FIT rows | all models | `FAIL_TECHNICAL/MODEL` |
| SUP, F1, L1, R1-U, DX | `share_dropped(ctx)` (§4.9) | `NOT_RUN/SHARE_DROPPED` | — |
| M0 | `hwsu_model.m0_gate` | PASS | `FAIL_TECHNICAL/MODEL` or `INCONCLUSIVE/NUMERICAL` |
| X1 | `hwsu_model.x1_gate` (natural arms, every VAL pair) | PASS | `FAIL_TECHNICAL/X1` |
| KC-U `kc_u(ctx)` | KO1–KO3 at VAL: `A_k = hwsu_oracle.readout_A(d, ko_logits(o1, s1, k), ko_logits(o2, s2, k), helmert(36))`; `hwsu_oracle.ko_identities(G, A)` all ok; `hwsu_oracle.ko_categories(G, A, 640112)` `ok` (KO1 RESPONDS; KO2 LOW_RESPONSE; KO3 WEAK_RESPONSE with rule 6) | all | `FAIL_TECHNICAL/KNOWN_CASE` |
| P1 | §4.2; then `write_sealed_u` (§4.7) | `N_RESP` exists | `INCONCLUSIVE/UNDERPOWERED` (before any TEST draw) |

After P1 (PASS or not): the validation report (§4.7), `complete_stage(out, "E1", [...])`, the obligation (§5.3). Under the response-only scope the model arrays at VAL are computed once, in P1's step: per j, `y1 = readout_y(model, val_a1, perm_j, basis_j)`, `y2 = …a2`, `A_j = a_full(named_from_canonical(d, perm_j), basis_j["M"], y1, y2)`; saved sealed-side only (`PAIR_E1_val.npz` members `A_<j>`, `ZR010_<j>`, `ZR030_<j>`; U-D-4).

### 4.2 P1 (protocol §2.9 "P1 precision ladder", response arrays only)

| Name | Contract |
|---|---|
| `p1_u(A, G, models, seeds, ladder=LADDER) -> dict` | `A = {j: A_j}` (VAL), `G` the VAL oracle array. `alt = 0.10 · min_j tree_mean(G)` (G is shared, so this is `0.10 · tree_mean(G)`). For X ∈ (ZR010, ZR030) in that order: `Xd = {j: response_arrays(A_j, G)[X]}`; `sd, _ = precision.sd_b4_draws(Xd, {j: G for j}, list(models), seeds["p1_sd"], 5000, len(G))`; for N in ladder: `e = precision.centered_draws(Xd, list(models), seeds["p1_centred"], 5000, N)`; `s = precision.precision_summary(sd, e, list(models), cfg)` with `cfg = {"alpha": 1/300, "power": 0.80, "delta": 0.0, "alternative": alt, "projected_N": N}`; model j **passes X at N** iff `s["models"][j]["mde_upper"] <= alt and s["models"][j]["power"] >= 0.80`. `N_RESP` = the smallest N at which every model passes both arrays; else the smallest N at which ≥ 2 models pass both (the others `PRECISION_LIMITED(j)`); else None → `INCONCLUSIVE/UNDERPOWERED`. `N = N_RESP` (share dropped at OF, protocol §2.9 last line); `k = N / 4096`. **No model mean enters**: `alt` uses G only; `centered_draws` centres each array; the decision uses only `mde_upper` and `power`. Returns `{"N_RESP", "N", "k", "passes": {X: {N: {j: bool}}}, "precision_limited": [...], "prec": arrays for PREC_E1.npz}` |

### 4.3 E2 gates (protocol §6 rows 16–20)

| Gate / name | Computation | Pass | On failure |
|---|---|---|---|
| RELEASE-B `release_b_check(out, ctx)` | `RELEASE_B.json` (§8.3) present; its `freeze_sha256`, `k_reg2` (manifest and digest-file sha256 re-hash), `reservation_id` (= ctx), `worker_session`, `N`, `k` (equal to the sealed P1 values in `stages/E1/VALIDATION_REPORT.json`), `accept_sha256` (`ACCEPT_VALIDATION.json` re-hash) | all | `INCONCLUSIVE/AUTHORITY` (nothing drawn) |
| S7 `sample_e2(out, ctx)` | test pairs b0 … b(k−1), 4,096 each, scope `hwsu-v1`, split `test`; tables `stages/E2/HIST_test_a1_b<i>.npz`, `HIST_test_a2_b<i>.npz`; `complete_stage(out, "E2_S7", files)` | — | `FAIL_TECHNICAL/SAMPLER` |
| H2-FRESH-U | `separation_u(K-REG2, test tables, seq_union)`, predicate, registry risk | 0 | as H2-U |
| T-PRE `t_pre(out, ctx)` | `policy.begin("T-PRE")`: H1-U re-check (`identity_c`, `charts_identity`, `state_sha` equal to E1's `H1U.json`, `lineage_c`); H3-U on test; H5-U on test (seed 640119, (a) only); M0 (`m0_u`) and X1 (natural arms) on the 1,024 lowest-id test pairs, ephemeral; `policy.mark_pass("T-PRE")` | all | `INCONCLUSIVE/TEST_GATE` (endpoints `NOT_RUN/T-PRE`) |
| NUM | per j: every decision bound of §4.4 clears its guard (`c2_decide.sign(b, g) != 0` for L(ZR010), U(ZR010), L(ZR030), U(ZR030), L(AF)) | — | `INC_j/NUMERICAL` (model) |
| ENDPOINT | §4.4–§4.6; `SEALED_OPENED.json` and the report hashed in the ENDPOINT `STAGE_COMPLETE` | — | rank-check failure `FAIL_TECHNICAL/NUMERICAL` |

### 4.4 The family stream and per-model statements (protocol §2.9, response rows)

| Name | Contract |
|---|---|
| `family_bounds(A, G, models, seed=640111, alpha=Fraction(1, 300), draws=20000) -> dict` | `arrays` in this insertion order: for j in models (master order), `f"{j}:ZR010"`, `f"{j}:ZR030"`, `f"{j}:AF"` = `response_arrays(A_j, G)` over all N test pairs; one call `b = c2_decide.stream_bounds(arrays, seed, float(alpha), draws)` (one shared index stream over every model and array); every `b[key]["rank_L"] == 67` and `rank_U == 19934`, else `FAIL_TECHNICAL/NUMERICAL`; per key `g = c2_decide.guard(arrays[key], 0.0)`. Returns `{key: {"L", "U", "mean", "rank_L", "rank_U", "g"}}` |
| `model_status(bj) -> dict` | `bj = {"ZR010": …, "ZR030": …, "AF": …}` (each with L, U, g). `cat = c2_decide._category({s: dict(bj[s]) for s in ("ZR010", "ZR030")}, "ZR010", "ZR030", ())` mapped USED→`RESPONDS_j`, PARTIAL→`WEAK_RESPONSE_j`, NOT_USED/LOW_ALIGNED→`LOW_RESPONSE_j`, `INC`→`INC_j`, `INC/NUMERICAL`→`INC_j/NUMERICAL`. `rule6 = sign(L(AF), g) == 1 and sign(U(ZR030), g) == −1`; coarse `"theta > 0.10"` iff `sign(L(ZR010), g) == 1`, `"theta < 0.30"` iff `sign(U(ZR030), g) == −1`. A mean exactly at a line is never declared; a bound inside its guard counts as neither sign. Returns `{"status", "rule6", "coarse": [...], "bounds"}` |
| `fw_events(theta_region) -> int` | Lemma FW-U response part: the number of coverage-failure events whose union contains "some declared response statement of model j is false", per truth region (θ ≤ 0; 0 < θ ≤ 0.10; 0.10 < θ < 0.30; θ = 0.30; θ > 0.30); ≤ 2 in every region (protocol §2.9) |

### 4.5 Aggregation and outcomes (protocol §2.9 overall rules, §7.1)

| Name | Contract |
|---|---|
| `response_outcome(per_model) -> dict` | `per_model = {j: status}` (EXCLUDED/NOT_RUN entries count for nothing). Fewer than 2 models not excluded → `INCONCLUSIVE/<study gate>` (the gate that excluded them). Else: `RESPONDS` if ≥ 2 `RESPONDS_j`; else `WEAK_RESPONSE` if ≥ 2 `WEAK_RESPONSE_j`; else `LOW_RESPONSE` if ≥ 2 `LOW_RESPONSE_j`; else `MIXED` if ≥ 2 models are resolved (status in the three categories); else `INCONCLUSIVE/PRECISION`. `DISSENT(j: status)` for every model whose status differs from a 2-of-3 category outcome. Rule 6: `"RESP_POSITIVE_BELOW_MARGIN in k models"` iff ≥ 2 declare it, `"in all three"` iff 3 |
| `share_outcome(of_bind) -> dict` | returns `{"outcome": "INCONCLUSIVE/ORACLE_FEASIBILITY", "source": "OF_ACCEPT.json", "of_accept_sha256"}` from `hwsu_known.of_binding` (never computed from data) |
| `study_outcome(records, resp, share) -> str` | precedence of CONTRACT `outcomes_u2.precedence`: the first gate record with `FAIL_TECHNICAL/*` gives it; else `INCONCLUSIVE/RESOURCE_OR_AUTHORITY` (authority, safe-STOP); else an `INCONCLUSIVE/<study gate>`; else `resp["outcome"]` (the share outcome is reported beside it, fixed) |
| `licences(resp, per_model, bounds, desc) -> dict` | fills CONTRACT `outcomes_u2.licences` (the response texts verbatim from protocol §7.2 with θ̂ point = `tree_mean(A_j)/tree_mean(G)` and the family lower bounds), each followed by `outcomes_u2.scope_clause` (Q-CODE-U); the share licence is `SHARE_INCONCLUSIVE_ORACLE_FEASIBILITY`; plus `disclosure` and the §7.3 list |

### 4.6 Descriptives at TEST (protocol §2.6, response part; never decision-bearing)

`descriptives(A, G, rowA, models) -> dict`: θ̂ intervals `c2_attrib.ratio_intervals({f"A_{j}": A_j}, {"G": G}, [(f"A_{j}", "G") for j], 640117, 5000)` (one call; two-sided 95 %); sign-agreement `mean(A_j > 0)`; the Lemma P2 single-row cross-check per j: `tree_mean(rowA_j)` (`row_cross_check` on arm 1) against `tree_mean(A_j)`; KO report at TEST: `ko_identities` and `ko_categories(G, A_KO, 640118)`; `hwsu_of.tails(G)`.

### 4.7 Sealing and the validation report (protocol §2.10)

| Name | Contract |
|---|---|
| `SEALED_KEYS_U` | `{"A_full", "AF", "ZR010", "ZR030", "theta", "theta_hat", "mean_A", "mean_ZR010", "mean_ZR030", "sign_agreement", "row_cross_check", "family_bounds", "per_model_status"}` |
| `write_sealed_u(store, arrays) -> str` | the only writer of `store/SEALED_VALIDATION.json`: exclusive create once; body `{"protocol_sha256": HWSU's, "means": {key: repr(float(tree_mean(arr)))}}` for `A_<j>`, `ZR010_<j>`, `ZR030_<j>` and `theta_<j>` (= mean A_j / mean G); `json.dumps(sort_keys=True) + "\n"`; returns its sha256 (mirror of `k4b_stats.write_sealed`) |
| `check_unsealed_u(report) -> None` | recursive: any key in `SEALED_KEYS_U` anywhere → `FAIL_TECHNICAL/SEALING` (mirror of `k4b_stats.check_unsealed`) |
| `validation_report(out, ctx, records) -> Path` | `stages/E1/VALIDATION_REPORT.json` (exclusive): `{"schema": "hwsu-validation-v1", "gates": {gate: status}, "G": {"mean", "L", "rank_L"}, "ko": {"identities", "categories" (PASS/FAIL per case only)}, "p1": {"N_RESP", "N", "k", "mde": {X: {N: {j: mde_upper}}}, "power": …, "precision_limited"}, "basis", "m0", "x1" (identity diagnostics), "h2", "h3", "registry": {"K-REG1": manifest sha256, "superset_diagnostic"}, "sealed_sha256", "share": "NOT_RUN/SHARE_DROPPED", "written_utc"}`; `check_unsealed_u(report)` before writing |
| `sealed_opened(out, ctx) -> Path` | inside the ENDPOINT stage, after the outcome is recorded: `stages/E2/SEALED_OPENED.json` `{"sealed_sha256", "means": the SEALED_VALIDATION means, "opened_utc"}`; listed (with `SEALED_VALIDATION.json`'s sha256 check) in the ENDPOINT `STAGE_COMPLETE` |

### 4.8 The report

`report_u(out, ctx, records) -> Path`: `stages/E2/REPORT.json` (exclusive) `{"schema": "hwsu-report-v1", "outcome" (study), "response": {"outcome", "per_model", "rule6", "coarse", "dissent", "qualifiers"}, "share": share_outcome, "family": {"alpha": "1/300", "fw_events_per_model": 2, "family_error": "0.02 <= 0.05"}, "bounds", "descriptives", "ko_test", "licences", "disclosure", "does_not_establish", "N", "k", "gates", "cpu_s", "protocol_sha256", "contract_of_sha256", "contract_sha256", "freeze_sha256", "freeze_of_sha256", "of_accept_sha256", "written_utc"}`.

### 4.9 Share-only entry points (R-0223-1: fail closed)

| Name | Contract |
|---|---|
| `share_dropped(ctx) -> dict` | the step function of SUP, F1, L1, R1-U, DX: returns `{"status": "NOT_RUN/SHARE_DROPPED", "reason": "OF_PASS_RESPONSE_ONLY (S3; R-0223-1)"}`; computes nothing |
| `share_family(*args, **kwargs)` | raises `C1GateFailure("FAIL_TECHNICAL/BINDING", "share family dropped at OF (S3; R-0223-1)")`. Every share-only name a caller might reach (`hwsu_known.ku_cases`, `hwsu_gates.share_arrays_u`, `hwsu_gates.haar_frames_u`) is bound to it |

## 5. `hwsu_driver.py` (≈ 300 lines): jobs KC, E1, REG2, E2; CLI

| Name | Contract |
|---|---|
| `build_ctx_u(out, job, attempt, stage, reservation_id=None, root=uc.ROOT, mailbox=uc.MAILBOX, hwsc_store=uc.HWSC_STORE, scope=uc.SCOPE_U, seeds=CONTRACT seeds.model_phase_reserved, dry=False) -> dict` | the gate context (phase-1 keys plus `stage`, `policy = UPolicy()`); `reservation_path = out/reservation_file(reservation_id)` when given |
| `run_job(stage, out, job, attempt=1, reservation_id=None, repo=uc.REPO, ledger_path=None, ctx=None, dry_continue=False) -> dict` | (1) `hwsu_known.s0_u(out, repo)` (failure → gate `S0` `INVALID`, exit 2, nothing written but the gate record); (2) `auth_u` (failure → `INCONCLUSIVE/AUTHORITY`, exit 2); (3) `begin_stage(out, stage)`; `t0 = time.process_time()`; (4) `records = run_gates_u(out, steps(stage), continuing=CONTRACT gates_u2.continuing_statuses, dry_continue)`; (5) stage report (`kc_report`, `validation_report`, `report_u`) of what was computed; (6) `complete_stage(out, stage, files)`; (7) obligation (§5.3); (8) **no pause check** (addenda 41–43; `pause_or_raise_u` is not called); the CPU is returned and the coordinator books it (`ledger_append`, label `<stage>-<job>-a<k>`). Exit codes CONTRACT `gates_u2.exit_codes` |
| `steps(stage, ctx) -> list` | the `(gate, fn)` list of CONTRACT `gates_u2.jobs[stage]` after S0/AUTH |
| `memory_cap_u2(stage) -> int` | CONTRACT `resources.u2_memory_cap_bytes[stage]` (J-U, DRU 8 GiB; KC, E1, REG2, E2 12 GiB); unknown → `ValueError` (phase-1 `hwsu_meter_bind.memory_cap` refuses these stages, as its tests require) |
| `job_paths_u2(job, kind) -> dict` | `kind` `"test"` and `"store"`: phase-1 `hwsu_meter_bind.job_paths(job, kind)`; `kind == "dru"`: `out = SCRATCH/f"hwsu-dry-u2-{job}"`, `temp_root = SCRATCH/f"test_hwsu-{job}"`, `basetemp = temp_root/"pytest"`; else `ValueError` |
| `meter_main(argv=None) -> int` | mirror of phase-1 `hwsu_meter_bind.main` (phase-1 API §8) with `--kind` ∈ {test, dru, store} resolved by `job_paths_u2` and `--stage` ∈ {J-U, DRU, KC, E1, REG2, E2}; the binding is phase-1 `hwsu_meter_bind.bind(...)` followed by `winjob.MEMORY_CAP = memory_cap_u2(stage)` (bind's own `memory_cap(stage)` call would refuse these stages, so `bind` is called with `stage="OF"` and the cap is overwritten at once; OPEN-10); `placement_ok` as phase 1 with the `dru` kind treated as `dry`. Everything else (lock, stale archive, limiter, env, argv rewrite `--max-cpu inf --max-wall inf`) is the phase-1 sequence |
| `main(argv=None) -> int` | subcommands `kc`, `e1`, `reg2`, `e2` (`--job`, `--attempt`, `--reservation`, `--out`, `--ledger`), `freeze` (`--h-exec`, `--dry-report`, `--j-u` repeatable, `--written-by`), `s0`, `audit`, `dry` (`--out`, `--only`). `--out` defaults to `STORE` (`dry`: `X:/Downloads/topo-scratch/hwsu-dry-u2-<job>`). Reservation, obligation, end-reservation, attest and ledger-append stay the phase-1 CLI (`hwsu_driver_of`) |

### 5.1 Reservations (protocol §8.2 item 3; S-3; J10 item 3)

`RES-HWSU-U` (`RESERVATION_U.json`, written by the coordinator with the phase-1 `reserve` CLI) is held from REG1 through the last test block and renewed per job by the job's `RESERVATION` gate. A drawing job (E1 at S3; E2 at S7) that stops after its reservation gate and before its first row writes a no-history obligation and ends `RES-HWSU-U` with `hwsu_records.end_reservation`; a rerun takes `RES-HWSU-U-a<k+1>`. The E2 job that completes the study writes `REGISTRY_OBLIGATION.json` and ends the reservation.

### 5.2 Releases

`RELEASE_A.json` (coordinator, before E1): `{"schema": "hwsu-release-a-v1", "job", "reservation_id", "reservation_sha256", "w2_attestation" (the KC G0U attestation), "g0u_sha256" (KC `stages/KC/G0U.json`), "completeness_certificate": {"rehearsal_manifest_sha256", "scratch_rows_sha256", "root_table_sha256", "coordinator"}, "freeze_sha256", "written_by", "written_utc"}`. `ACCEPT_VALIDATION.json` (coordinator ACCEPT of the validation report; no endpoint-reconstructing value). `RELEASE_B.json` (coordinator, after REG2): `{"schema": "hwsu-release-b-v1", "N", "k", "k_reg2": {"manifest_sha256", "digest_file_sha256"}, "reservation_id", "worker_session", "accept_sha256", "freeze_sha256", "written_by", "written_utc"}`.

### 5.3 Obligations (J10)

Every job that writes into `hwsu-store` (KC, E1, REG2, E2), including a stopped attempt, ends with the **phase-1** `hwsu_records.write_obligation(store, name, job, written_by, attempt=k, reservation_id=…)` — sufficient because phase-2 code writes only phase-1-prefixed arrays (U-D-6). Names: `REGISTRY_OBLIGATION_KC-a<k>.json`, `_E1-a<k>`, `_REG2-a<k>`, `_E2-a<k>` (stopped E2), `REGISTRY_OBLIGATION.json` (the E2 that completes the study). The job's `STAGE_COMPLETE` (or stop record) lists the obligation's sha256.

## 6. `hwsu_dry2.py` (≈ 330 lines): the model-phase dry run DRU (protocol §9), response family

Every case `dru<n>(base, ctx) -> {"status": "PASS" or "FAIL", "details"}` works under `base` (a helper folder `X:/Downloads/topo-scratch/test_hwsu-<job>/dru<n>/`, R-0213-2), scope `hwsu-dry-v1`, seeds `CONTRACT seeds.dry_u2`, synthetic roots only, no real checkpoint opened, nothing under the project root.

| Name | Contract |
|---|---|
| `tiny_models(store, proc) -> dict` | three tiny models (CONTRACT `dry_run_u2.tiny_model`, `tiny_train`; masters `dry_run_u2.tiny_masters` 649907–649909, OPEN-6) trained by `hwsb_train.train(store, {"train", "dev"}, m, plan=plan)` on ObservationSets from `hwsc_data.make_train_dev_c(store, proc, m, plan, scope=SCOPE_DRY)` (OPEN-1), `store` a `ArtifactStore(LocalFSBackend(base/"artifacts"))` under the helper folder |
| `ks_p(base)` | KS-P by exact enumeration on the phase-1 non-reversible chain (`hwsu_dry.nonreversible_chain`, L = 8): Lemma P2 pair moment = conditional-covariance form; E[G] = E[KL(q32‖q4)] + E[KL(q4‖q32)] (Lemma J); a suffix-only predictor gives A ≡ 0 (Fractions where exact) |
| `ks_rules(base)` | KS-RULES response part: `model_status` at every boundary (bounds at ±g, exactly at a line), `response_outcome` over every 3-model combination, rule 6, the `fw_events` grid ≤ 2 per region |
| `dru1` | full pipeline on the tiny world with `tiny_models`, synthetic stage-C fixtures (TRAIN_RECORD, meta, PRODUCTION_FROZEN, chart files as random bytes with their sha256) and a synthetic root: KC, E1, REG2, E2 jobs through `run_job` with `dry=True`; every gate returns a value; share gates `NOT_RUN/SHARE_DROPPED`; every record complete; no `HIST_*` name |
| `dru2` | real architecture (4 layers, d128, random init, `torch.manual_seed(649910)`), 2,048 in-memory w\* DRY pairs: `basis_u` rank, `m0_u`, `x1_gate`, `a_full` against `½dᵀ(z¹ − z²)` from closed logits (≤ 1e-9·max(1,‖z‖∞)); nothing persisted |
| `dru3` | planted-truth readouts on the tiny world, response part: a readout reading a planted beyond-four direction → RESPONDS; KS-IGNORE (suffix-only readout) → A ≡ 0, LOW_RESPONSE; the oracle dose λ = 1/5 → WEAK_RESPONSE with rule 6 |
| `dru4` | `ks_rules` plus the 2-of-3 aggregation with exclusions, `DISSENT`, `INCONCLUSIVE/PRECISION`, the fixed share outcome |
| `dru5` | `p1_u`: the ladder rule, ≥ 2-pass fallback with `PRECISION_LIMITED`, UNDERPOWERED; a fixture where only mean(A_full) differs gives an identical `N` |
| `dru6` | sealing: a validation report carrying a sealed key is refused; `SEALED_VALIDATION.json` exclusive once; `SEALED_OPENED.json` inside the ENDPOINT `STAGE_COMPLETE`; KO releases PASS/FAIL only |
| `dru7` | `audit_u2` catches a planted call to `c2_model.load_models`, `c2_oracle.load_process`, `c2_stats.p1`, `c2_model.m0`, `k4b_stats.write_sealed`, a C2-seed default, and a function reading an unlisted `c2_config` name |
| `dru_reg` | `build_u` equals `hwsc_registry_build.build` (bitwise manifest digests) on a synthetic root with stage C's source map (OPEN-7); U2 with planted missing, renamed, unreadable, re-hash-mismatched S3 tables → INCOMPLETE; planted Checkpoint `payload.npz` classed, never opened (access hook: zero opens); `sealed/` never opened; S-2: a K-REG2 digest file with one digest missing from the reader-built union → diagnostic lists it, K-REG1 holds it through U8, PASS; K-REG2 digest file sha mismatch → INCOMPLETE; `hwsd-dry*` without obligation → INCOMPLETE; conforming `hwsd-store` obligation → READER; a track-D-form END record with a **store-relative** `obligation_file` is accepted (R-0213-1) and one pointing outside its store is live; the DRO9 obligation fixtures through `read_obligation_u2`; an E1 attempt stopped before S3 (no-history obligation, `RES-HWSU-U` ended, rerun on `RES-HWSU-U-a2`); a KC `REGISTRY_OBLIGATION_KC-a1.json` accepted by a track-D-form reader fixture |
| `dru8` | stage-C binding on fixtures: a checkpoint id from `stage_c_exclusions` refused; a chart sha256 off by one byte refused; `dev_ce` never read (the `read_train_record` hook drops it; a key-access hook records zero reads); OF_ACCEPT with `freeze_of_sha256` ≠ FREEZE_OF sha256 refused (R-0206-1) |
| `dru9` | budget records: ledger labels unique per attempt; meter output cap and memory caps read from CONTRACT; no pause line is applied |
| `run_dru(out, only=None) -> dict` | refuses (`{"status": "REFUSED"}`) if `out` lies under `ROOT` or does not match `X:/Downloads/topo-scratch/hwsu-dry*` (`hwsu_config.dry_store_ok`); runs the cases; writes `out/stages/DRY/DRY_U2_REPORT.json` (exclusive) `{"cases", "all_pass", "implementation_files", "implementation_sha256", "h_exec", "tree_clean", "inventory_before", "inventory_after"}` (`hwsu_records.root_inventory(ROOT)` before and after; `all_pass` also requires them equal); then the dry store's `REGISTRY_OBLIGATION.json` (phase-1 writer, `dry=True`; J4) |

## 7. Reused functions (protocol §11.2–§11.3)

CONTRACT `binding.allowlist` (phase-2 entries merged in) and `binding.allowlist_conditional_u2` are authoritative, with their call-time reads from the AST audit at 49ac9c9 (TO_FREEZE at h_exec). Phase 2 adds: `c2_model.{readout_basis, readout_coords, closed_logits, activations3, natural_pass, identity_patch, readout_identity, kappa_x1, x1_attainable, two_route, symbol_order_a, symbol_order_b, symbol_order_c, x1}`; `c1_model.{load_model64, model_inputs}`; `c1_oracle.{named_from_canonical, canonical_from_named_cols}`; `hwsc_gates.exclusion_check`; `k4b_config.check_checkpoint_meta`; `hwsc_records.lineage_c`; `c2_registry.{Registry, separation, _ok_readers, _x6_manifest, _entry, _try}`; `hwsc_registry_build._summary`; `hwsc_registry.{source_own, scratch_check, scratch_scan}`; `hwsc_drystore.dry_class`; `hwsb_registry.registry_digests`; `k4b_registry.{inventory, classify, source_f, revalidate_coverage, validate_handoff_json, summary}`; `c1_data.build_registry`; `torch.{get_num_threads, set_num_threads}`; `topo_pilot.contracts.Checkpoint`; `topo_pilot.contracts.backends.LocalFSBackend`. Conditional (sanctioned forbidden reads; OPEN-1): `hwsc_gates.expected_meta_c` (`hwsc_config.SCOPE`), `hwsc_registry_build._default_sources` (`CONTRACT["registry"]` of c2/k4b/nd), `hwsb_train.train` and `hwsc_data.make_train_dev_c` (DRU1 only), and `hwsc_registry_build.build` (DRU-REG only; OPEN-7). Mirrors: CONTRACT `binding.mirrors_u2`. Never called: phase-1 `binding.never_called` plus `binding.never_called_u2`. Reused file hashes: phase-1 `reuse_sha256` (199 files) plus `reuse_sha256_u2` (`tools/c2_readout/c2_model.py`, `tools/hwsc/hwsc_drystore.py`), kept as a separate key because the phase-1 freeze code reads `reuse_sha256` (§14 OPEN-1 note).

## 8. Store layout, arrays, records

### 8.1 Layout (`hwsu-store/`, phase 2 additions)

CONTRACT `store_layout_u2`. Top level: `FREEZE.json`, `AUTH_U_<job>.json`, `RESERVATION_U.json` (`-a<k>`), `RELEASE_A.json`, `ACCEPT_VALIDATION.json`, `RELEASE_B.json`, `SEALED_VALIDATION.json` (listed in the E1 `STAGE_COMPLETE`), `REGISTRY_OBLIGATION_<job>-a<k>.json`, `REGISTRY_OBLIGATION.json`, `reservations/<id>.END.json`. `stages/KC/`, `stages/E1/`, `stages/E2/`; `registry/` (K-REG1, K-REG2, `rehearsal/`). Every non-exempt file is in a `STAGE_COMPLETE` (phase-1 `lineage_u` applies unchanged).

### 8.2 Arrays (U-D-6)

Through phase-1 `save_array` only: `HIST_*` tables (six members, phase-1 §2.3); `ORACLE_E1_<split>.npz`, `ORACLE_E2_test.npz` (`G`, `d` [n, 36] canonical, `le_a1`, `le_a2`; fit: `le`, `s`); `PAIR_E1_val.npz`, `PAIR_E2_test.npz` (`A_<j>`, `ZR010_<j>`, `ZR030_<j>`, `rowA_<j>` per model); `PREC_E1.npz` (`sd_<X>` [5000, 3], `e_<X>_<N>` [5000, 3]); `BOOT_E1.npz` (`headroom_G`), `BOOT_E2.npz` (the 20,000 family draws per key, `desc_*`, `headroom_G`). Registry digest files under `registry/` (basis `registry`). No `Y_*`, `ACTS_*` array is written (readout coordinates are recomputed from the frozen checkpoints).

### 8.3 JSON records

`stages/<stage>/G0U.json` (§2.5), `stages/E1/H1U.json`, `stages/KC/KC_REPORT.json`, `stages/E1/VALIDATION_REPORT.json`, `stages/E2/TPRE.json`, `stages/E2/ENDPOINT.json` (`family_bounds`, `per_model`), `stages/E2/REPORT.json`, `SEALED_VALIDATION.json`, `stages/E2/SEALED_OPENED.json`, `FREEZE.json`, `AUTH_U_<job>.json`, `RELEASE_*.json`, `ACCEPT_VALIDATION.json`, obligations, END records (phase 1).

## 9. Budget (protocol §10; owner addenda 41–43)

Measure-only (`--max-cpu inf --max-wall inf`) under `hwsu_driver.meter_main` (§5; the phase-1 binding plus the phase-2 memory caps: `--kind store` for KC, E1, REG2, E2; `--kind test` for J-U; `--kind dru` for DRU). **No pause lines**: addenda 41–43 released them; the phase-1 `pause_or_raise_u` is not called by phase-2 jobs. Runaway safeguards only: memory caps (12 GiB KC/E1/REG2/E2; 8 GiB J-U/DRU; CONTRACT `resources.u2_memory_cap_bytes`), disk floors (C: ≥ 2 GB, X: ≥ 30 GB), output cap 16 GiB over the whole out directory, native-operation wall 600 s, and a coordinator CPU watchdog (CONTRACT `resources.runaway_u2.watchdog_cpu_s`). Forecast centrals (reporting only): J-U 650, DRU 300, KC 1,000, E1 2,000, REG2 300, E2 300 + 700·k CPU-s; the actual CPU is booked in `agent-handoff/HWSU_CPU_LEDGER.json` (`hwsu_records.ledger_append`, unique labels `<stage>-<job>-a<k>`) and reported; the share computations are not run (protocol §10.2).

## 10. Implementation decisions (each open to a coordinator ruling)

- **U-D-1 (documents).** R-0223-2: new files `API_U2.md`, `CONTRACT.json`, `TEST_PLAN_U2.md`; phase-1 `API.md` §16 ("phase 2 appends here") is not used.
- **U-D-2 (contract keys).** The loader forbids overrides and treats lists as leaves, and several phase-1 functions read phase-1 keys of the merged CONTRACT. Phase-2 lists and tables that phase-1 code would read differently are therefore new keys: `binding.allowlist_conditional_u2`, `binding.conditional_reads_u2`, `binding.never_called_u2`, `reuse_sha256_u2` (phase-1 `hwsu_freeze` reads `reuse_sha256`), `resources.u2_memory_cap_bytes` (phase-1 tests expect `memory_cap("E1")` refused), `cpu.u2_*`, `name_rule_u2` (not `name_rule.phase2`: phase-1 tests expect `ACTS_` refused under the merged CONTRACT), `seeds.dry_u2`. The whole phase-1 suite `tests/hwsu` passes with this `CONTRACT.json` present (checked at 49ac9c9).
- **U-D-3.** M0 runs on arm 1 of the 1,024 lowest-id VAL pairs (protocol: "the 1,024 lowest-id VAL pairs"); X1 runs on both arms of every VAL pair.
- **U-D-4.** A_full is computed from the readout coordinates (closed form, no logit) for the endpoint; network logits are formed only in BASIS, M0, X1 and T-PRE and are deleted after their identity check.
- **U-D-5.** H3-U's KO identities run on every pair split; KO categories (seeded) run once in KC-U at VAL (seed 640112) and once in the TEST report (seed 640118).
- **U-D-6 (array names).** Phase-2 code writes only `HIST_*`, `ORACLE_*`, `PAIR_*`, `BOOT_*`, `PREC_*` arrays, so the phase-1 name rule, `save_array` and `write_obligation` cover phase-2 stores unchanged; the protocol's phase-2 prefixes are recorded in `name_rule_u2` and unused.
- **U-D-7.** The P1 alternative `0.10·min_j mean_VAL(G)` equals `0.10·mean_VAL(G)` (G is the oracle's, shared by the three models).
- **U-D-8.** The H2 registry-risk row count is the protocol's maximum (24,576 + 32,768 + 8,192·8 = 122,880) at E1 and the realised count at E2.
- **U-D-9.** `hwsc_records.lineage_c(hwsc-store)` runs in H1-U and T-PRE as the protocol requires (§3.1); it hashes every file of `hwsc-store` (payloads included) inside the metered job only; tests and the dry run call it on synthetic stores only.
- **U-D-10.** The share licence text `SHARE_INCONCLUSIVE_ORACLE_FEASIBILITY` (CONTRACT) is new wording within protocol §7.2 "MIXED / INCONCLUSIVE".
- **U-D-11.** No pause check in phase-2 jobs (addenda 41–43); the phase-1 ledger is still written.

## 11. Known cases, coverage (protocol §5, response part)

KC0–KC6 (§2.5), KO1–KO3 at VAL (KC-U) and in the TEST report, KS-PAIR/KS-P/KS-RULES (KC3, DRU), the planted readouts of DRU3. Coverage: every response category and the response rule-6 statement (KO1–KO3, DRU3); X1, BASIS, M0, the sampler: identities. Share coverage is omitted (§12).

## 12. Omitted under S3 (R-0223-1)

Not implemented in phase 2 (share family dropped at OF, protocol §4.1; coordinator ruling R-0223-1). Any entry point a caller might reach fails closed (§4.9).

| # | Design item | Protocol section |
|---|---|---|
| O-1 | U-SHARE estimand ψ_j = E[A_S]/E[A_full], θ_S, ψ_Γ, ψ_rest | §1.2, §2.5 |
| O-2 | The registered circle code (FWL K = 3, 5 nuisance covariates, GLS, P_S) refitted on FIT: problem R and its variants R_E, R_K1, R_K2; S\*; the SHA decoy code; problem O on FIT; problem K on KFIT | §2.4, §2.6, §6 row 8 (F1) |
| O-3 | The partition A_S, A_Γ, A_rest; energies e_full, e_S; the random-6-plane reference r | §2.5 |
| O-4 | Share arrays Z010, Z050, Vabs, Vrand, NEG and the report-only variant arrays v:Z010, v:Z050 in family stream U | §2.9 |
| O-5 | Share per-model statements USED/PARTIAL/NOT_USED/LOW_ALIGNED, SHARE_POSITIVE_BELOW_MARGIN, coarse ψ statements; the share 2-of-3 aggregation, INCONCLUSIVE/NOT_RESPONSIVE | §2.9, §7.1 row 6 |
| O-6 | Lemma FW-U share events (≤ 3 per model) | §2.9 |
| O-7 | Share P1 arrays (SDs of Z010, Z050; alternative 0.03·min_j mean G), N_SHARE, SHARE_PRECISION_LIMITED | §2.9 |
| O-8 | KU1 (planted reader), KU2 (D-NULL head, g = 1), KU3 (decoy code) constructions, their VAL prerequisites (seed 640112 α = 1/60 on A′_full), releases, KU MDEs, consequences (KNOWN_CASE_CONTRADICTED, EXCLUDED_j/KNOWN_CASE, DECOY_UNRESOLVED, DECOY_PARTIAL) | §5.3, §6 row 14 (KU part) |
| O-9 | DX (construction exactness of KU heads; `nd_decoy.dx`, `decoy_sha64`) | §6 row 13 |
| O-10 | X1 interchange arms y_S^{2←1}, y_S^{1←2} and KU-head arms | §6 row 12 |
| O-11 | SUP (chart support ≥ 0.99 via `k4b_charts.extend` on fit/kfit/feas; support on VAL; support_VAL in T-PRE); chart extension of any U row; `resid_post_3` activations | §2.4, §6 rows 7, 18 |
| O-12 | L1 link decoders on FEAS (`c2_stats.fit_decoder`, `l1`) and their T-PRE re-check | §6 rows 9, 18 |
| O-13 | R1-U beyond-four registration of the code on FEAS (seed 640116) and C2's sign-agreement R1; CNHS-U_j; its T-PRE re-check | §6 rows 10, 18 |
| O-14 | The KFIT and FEAS splits: not drawn, not gated, no table, no oracle file (they feed only share gates: KU construction, Sup, L1, R1-U; R-0223-4, OPEN-2 resolved) | §2.8, §6 "sampling S3" |
| O-15 | Share descriptives: E\|A_S\| and its Cauchy–Schwarz bound, A_S^vis/A_S^null decomposition, ψ_max, 32 Haar 6-frames (`haar_frames_u`, seed 640120), ψ_comp, the radial/tangential split, the axial/circular share (S1), ψ\*_j, the decoy TEST share ψ̂_dec (seed 640118 share part), the Haar percentiles beside USED/PARTIAL | §2.6, §5.3 |
| O-16 | The descriptive beyond-four fraction of code variance and of the chart unit vector u | §2.4 |
| O-17 | The fresh-pair chart statistic ½Δu·Δm32 and the S6 chart fidelity check on 512 FEAS rows (both need a chart extended on U rows; SUP is NOT_RUN) (OPEN-4) | §2.6 |
| O-18 | Share qualifiers PROJECTOR_DEPENDENT, HARMONIC_DEPENDENT, NEGATIVE_ALIGNED_CONTRIBUTION, SPECIFICITY_NOT_ESTABLISHED (carried by share licences only), DECOY_*; the share licences USED/PARTIAL/NOT_USED/LOW_ALIGNED_SHARE/SHARE_POSITIVE_BELOW_MARGIN; ψ_orc printed beside share outcomes | §7.1, §7.2, §4.3 |
| O-19 | Sealed share values (A_S, A_Γ, e_S, r, Z/V arrays, ψ̂, variants, S\*, decoy share, KU values, decomposition) | §2.10 |
| O-20 | DRU parts for the share: DRU2 head-edit decoys and interchange closed form; DRU3 KS-USE share categories, D-NULL, decoy code, DECOY_PARTIAL, dose → PARTIAL, T-COPY; DRU5 SHARE_PRECISION_LIMITED and the N = max(N_RESP, N_SHARE) rule; DRU6 KU releases | §9 |
| O-21 | KS-USE/KS-IGNORE/KS-DECOY share answers and KS-P1 share combinations | §5.1 |
| O-22 | The S\* oracle-phase code on the model readout (descriptive ψ\*_j) and the oracle comparator problem O at FIT | §2.6 |
| O-23 | The share family's model-scope gate outcomes INCONCLUSIVE/CHART_UNAVAILABLE, LINK, CNHS-U, KNOWN_CASE | §7.1 row 6 |

Kept although part of the share-era design: BASIS, M0, natural-arm X1, H1–H5, KO1–KO3, the response part of P1, the registry (all sources), the chart **identity** in H1-U (file hashes and gauges; no chart loaded), Q-CODE-U on every licence.

## 13. TO_FREEZE items (reviewed by the coordinator before `FREEZE.json`)

1. `binding.allowlist` / `allowlist_conditional_u2` call-time reads: re-run `hwsu_bind.function_reads` at h_exec (`hwsu_bind_u2.audit_u2`); `hwsc_registry_build.build` by path (R-0223-5).
2. `reuse_sha256_u2`: the phase-2 import closure at h_exec minus the phase-1 table (2 files at 49ac9c9).
3. `registry_u2.root_table_u2`: name-only re-listing (72 top-level directories at 2026-11-03: stage C's 68 plus `hwsd-store`, `hwsu-store`, `topo-pilot-hwsd`, `topo-pilot-hwsu`).
4. `registry_u2.scratch_u2.rows`: `hwsc_registry.scratch_scan` header scan of the directories new since 2026-10-29 (names listed in CONTRACT; 47 non-reserved names), rows READER/EXCLUSION with frozen_files.
5. `cpu.u2_central_s` (cost only).
6. `dry_run_u2.tiny_train` plan object.
7. `stage_c_u2.stages_jsonl` sha256 re-hashed at the freeze.

## 14. OPEN points (coordinator ruling requested before code)

- **OPEN-1 (audit of sanctioned forbidden reads): resolved by R-0223-3 (Erratum E1).** Phase-2 modules live in `tools/hwsu/u2/` with their own audit `u2/hwsu_bind_u2.py`; the phase-1 audit and tests are unchanged and the four sanctioned functions are admitted through `binding.conditional_reads_u2` (section 2.6).
- **OPEN-2 (KFIT and FEAS under S3): resolved by R-0223-4.** Not drawn; section 12, O-14.
- **OPEN-3 (H5-U "OF-2 re-check > 0.02 nat").** Read as: the OF report's recorded OF-2 bound `EG.L` (bound by sha256) is > 1/50, in addition to the VAL bound > 1/100. Alternative: the VAL bound itself must exceed 1/50. **Accepted (coordinator, RULINGS.md).**
- **OPEN-4 (chart descriptives).** The fresh-pair chart statistic and the S6 chart check are not share statistics but need a chart extended on U rows, whose support gate SUP is share-only; omitted (O-17). **Accepted (coordinator, RULINGS.md).**
- **OPEN-5 (DRU store name).** Protocol §9 says `scratch/hwsu-dry/`; the phase-1 meter binding `job_paths(job, "dry")` gives `hwsu-dry-of-<job>`. This spec uses `X:/Downloads/topo-scratch/hwsu-dry-u2-<job>` (matches the reserved glob `hwsu-dry*` and `hwsu_config.dry_store_ok`), metered through `meter_main --kind dru`. **Accepted (coordinator, RULINGS.md).**
- **OPEN-10 (meter binding for phase-2 stages).** Phase-1 `hwsu_meter_bind.bind` calls `memory_cap(stage)`, which refuses KC/E1/REG2/E2/J-U/DRU (and phase-1 tests require that). `meter_main` therefore calls `bind` with `stage="OF"` and overwrites `winjob.MEMORY_CAP` with `memory_cap_u2(stage)` immediately after. Alternative: a full phase-2 copy of `bind`. **Accepted (coordinator, RULINGS.md).**
- **OPEN-6 (DRU tiny masters).** No master seed is reserved for DRU tiny models; this spec uses 649907–649909 (unused DRY seeds of HWSU's reserved block 649901–649920; 649906 is phase 1's tiny world; 649910 the DRU2 init seed). **Accepted (coordinator, RULINGS.md).**
- **OPEN-7 (`hwsc_registry_build.build` read audit).** `hwsu_bind.function_reads` imports `psutil` (imported inside `_peak_memory`), absent from the venv, so `build` cannot be read-audited; DRU-REG's equality check calls `build`. Proposed: audit `build` with the `psutil` import treated as external, or compare against a stored synthetic-root manifest. **Resolved by R-0223-5: audit `build` by path (AST) without importing; no package installed; DRU-REG checks equality (section 2.6).**
- **OPEN-8 (P1 when fewer than 3 models are left).** P1 runs over the models not excluded; under the response family no model-scope exclusion exists before P1, so this is moot unless a ruling adds one. **Accepted (coordinator, RULINGS.md).**
- **OPEN-9 (`topo-pilot-hwsd` in the root table).** The HWSU root inventory must classify it without opening track-D files; proposed EXCLUSION with deep-scan exclusion (pruned unsearched), as phase 1's hygiene root rule. **Accepted (coordinator, RULINGS.md).**

## Erratum E3 (R-0223-7, coordinator)

- Size splits accepted: `hwsu_registry` readers -> `u2/hwsu_regsrc.py` (read_hist_table, source_hwsc, source_kreg2_c, superset_diagnostic, source_own_u, read_obligation_u2, source_hwsd, source_own_dry); `hwsu_gates` decision side -> `u2/hwsu_decide.py` (p1_u, family_bounds, model_status, fw_events, response_outcome, share_outcome, study_outcome, licences, descriptives, write_sealed_u, check_unsealed_u, SEALED_KEYS_U); `hwsu_gates` E2 gates -> `u2/hwsu_e2.py` (release_b_check, sample_e2, h2_fresh, t_pre, num_gate, endpoint, sealed_opened, report_u). Every name stays reachable as `<spec module>.<name>`.
- `c2_config.T_QSUM` added to `allowlist_conditional_u2` (H3-U q-sum tolerance, R-0223-7 e).

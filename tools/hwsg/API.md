# tools/hwsg: written contract (job 0224 phase 1; derived from HWSG-DESIGN-v1)

**Authority.** `tools/hwsg/PROTOCOL_HWSG_v1.md`, a byte-for-byte copy of `agent-handoff/planning/responses/HWSG-DESIGN-v1.md` (sha256 `3a673898e210e204febca4b688a1f93697606d843d76eb7a11b06e4a8c2d6989`; freeze record `agent-handoff/records/HWSG_DESIGN_FREEZE.json`). Owner addenda 43 (planning through the execution freeze; real stages after it without a further question), 44 (Claude agents write code and tests), 45 (the four owner-question defaults: three worlds; capture floor 1/2 registered, similarity descriptive; three models train together; other worlds continue). Section marks (§n), KG, DRG, O-, R-, X- rows refer to the protocol.

**Precedence.** Protocol > `CONTRACT.json` > this file > `TEST_PLAN.md`. A difference is a contract defect reported through the coordinator, never resolved in code or a test. `CONTRACT.json` holds every value (exact values as `str(Fraction)`); this file fixes names, signatures, shapes, record schemas, the binding, the registry composition, every gate's computation in order, outcomes, the cross-world rule and the meter binding, so that the two test authors can work from the protocol, this file, `CONTRACT.json` and `TEST_PLAN.md` alone. Where the design is ambiguous the reading closest to its text is fixed and marked **OPEN-n** (§17); each is open to a coordinator ruling.

**Nothing here authorises a run.** No training, real-scope draw, oracle stage, metered run or store write follows from this contract.

## 0. Conventions

- **Modules** under `tools/hwsg/` (protocol §11.1; each `.py` ≤ 400 lines, `tools/check_file_sizes.py`): `hwsg_config`, `hwsg_bind`, `hwsg_handoff`, `hwsg_oracle`, `hwsg_train`, `hwsg_registry`, `hwsg_ratio`, `hwsg_cross`, `hwsg_known`, `hwsg_records`, `hwsg_jobs`, `hwsg_dry`, `hwsg_dry2`. A split by size adds a module by API erratum; every name here stays reachable as `<module>.<name>` (re-export). **No existing file is edited**; reused code is changed only through the runtime binding (§2), restored in `finally`. No `.npz`/`.npy` is committed under `tools/hwsg` or `tests/hwsg`.
- **Import convention.** Every module starts `from __future__ import annotations  # noqa: I001` and imports `hwsg_config` first. `hwsg_config` computes `HERE = Path(__file__).resolve().parent`, `REPO = HERE.parents[1]` and prepends, if absent, `tools/hwsg`, `tools/hwsc`, `tools/hwsb`, `tools/hws`, `tools/k4b`, `tools/c1prime`, `tools/c1prime_registry`, `tools/x4_circle_history`, `tools/x4_oracle_profile`, `tools/c2_nd`, `tools/c2_readout`, `tools/x6_stage1` (in that resulting order) to `sys.path`, then imports `hwsc_config` (which imports `hwsb_config`, `k4b_config`). Import reads only CONTRACT.json files; it opens no store file. Dependency order: `hwsg_config` ← `hwsg_bind` ← `hwsg_handoff` ← `hwsg_oracle` ← `hwsg_registry` ← `hwsg_ratio` ← `hwsg_cross` ← `hwsg_records` ← `hwsg_train` ← `hwsg_known` ← `hwsg_jobs` ← `hwsg_dry` ← `hwsg_dry2` (lazy imports inside functions where a cycle would arise).
- **Call-time lookups.** HWSG code calls reused functions and reads reused constants through module attributes at call time (`hwsc_gates.l1(...)`, `k4b_data.SCOPE`), never a `from … import` copy, so the binding applies and tests may monkeypatch.
- **Test aliases** (TEST_PLAN §1): `import hwsg_config as gc`, `hwsg_bind as gb`, `hwsg_handoff as gh`, `hwsg_oracle as go`, `hwsg_train as gt`, `hwsg_registry as gr`, `hwsg_ratio as gq`, `hwsg_cross as gx`, `hwsg_known as gk`, `hwsg_records as grec`, `hwsg_jobs as gj`, `hwsg_dry as gd`, `hwsg_dry2 as gd2`.
- **Run** with `X:/Downloads/projects/topo-pilot/topo-pilot/.venv/Scripts/python.exe -s` and `PYTHONPATH=<worktree>/src`.
- **World tags and keys.** A world is named by its tag `"lo"`, `"mid"`, `"hi"` (CONTRACT `worlds_order`) or its key (`CONTRACT worlds[tag].key`). Functions taking `w` accept either; `gc.world(w) -> WorldDef` resolves it (unknown → `ValueError`).
- **Model keys** are the int masters of the world (lo 620611–620613, mid 620621–620623, hi 620631–620633), iterated in CONTRACT order. Model-and-step maps use K4b's `(j, "step5000")`, `(j, "step0")`; per-side maps `(j, "-")`, `(j, "+")`, in JSON `f"{j}:{s}"`.
- **Numbers.** Exact quantities (σ, p, neighbour, M, α, F, F_plan, Z_bound, δ, risk products, capture floor) are `Fraction`; JSON writes `str(Fraction)`. A float enters exact arithmetic as `Fraction(float(x))`. Means `c1_means.tree_mean`.
- **Statuses** are full strings: `PASS`, `FAIL`, `NOT_RUN`, `REFUSED`, `INVALID`, `INCONCLUSIVE/<REASON>`, `FAIL_TECHNICAL/<REASON>`, `RATIO_UNRESOLVED`. HWSG code raises `c1_records.C1GateFailure(status, reason)`; `hwsc_records.status_of` maps every exception to a status (reused unchanged).
- **Writes** only inside the directory passed (`out`, `world_dir`, or an explicit path), by exclusive create (`stage_records.write_new`, `stage_records.save_npz`), except `GATES.jsonl`, `STAGES.jsonl` (append), the study ledger (`hwsg_records.ledger_append`, atomic replace), registry run dirs, `logs/`, and marker files (retried atomic replace, coordinator-side driver only, §10.3).
- **Footprint.** Implementation, tests and the dry run write no array file and no ArtifactStore artifact under `X:/Downloads/projects/topo-pilot/`. Tests use `--basetemp X:/Downloads/topo-scratch/test_hwsg-<job>/pytest`, TEMP/TMP/TMPDIR under `X:/Downloads/topo-scratch/test_hwsg-<job>/`. Dry store `X:/Downloads/topo-scratch/hwsg-dry/` (or `hwsg-dry-<job>/`), where no file is named `HIST_*.npz` (dry histories are `DRYHIST_*.npz`).
- **No foreign payload access.** Registry readers (§6) do identity-only token reads of history arrays; nothing opens `state.pt`, `sealed/`, foreign checkpoints, effect reports, `payload.npz` of foreign checkpoints. Stage O opens the stage-A S3 history table of each chosen world (O4, KB5 pattern; named in the O AUTH, OPEN-2).

## 1. `hwsg_config.py`: constants, contract, worlds, plans, paths, blindness guard

### 1.1 Constants and paths

| Name | Value / signature |
|---|---|
| `HERE`, `REPO`, `CONTRACT_PATH`, `PROTOCOL_PATH`, `API_PATH`, `TEST_PLAN_PATH` | `HERE/"CONTRACT.json"`, `HERE/"PROTOCOL_HWSG_v1.md"`, … |
| `ROOT`, `STORE`, `SCRATCH`, `DRY_STORE`, `MAILBOX`, `STUDY_LEDGER` | `Path("X:/Downloads/projects/topo-pilot")`, `ROOT/"hwsg-store"`, `Path("X:/Downloads/topo-scratch")`, `SCRATCH/"hwsg-dry"`, `ROOT/"agent-handoff"`, `MAILBOX/"HWSG_CPU_LEDGER.json"` (defaults only; every store-touching function takes the path explicitly) |
| `HWS_STORE`, `HWSB_STORE`, `HWSC_STORE`, `HWSU_STORE`, `HWSD_STORE`, `REPORT_PATH`, `S3_DIR` | `ROOT/"hws-store"`, …, `HWS_STORE/"stages/FINAL/REPORT.json"`, `HWS_STORE/"stages/S3/worlds"` |
| `load_contract(path=CONTRACT_PATH) -> dict`; `CONTRACT` | UTF-8 JSON, loaded at import |
| `PROTOCOL_SHA` | CONTRACT `protocol_sha256`; `protocol_ok() -> bool` re-hashes `PROTOCOL_PATH` |
| `SCOPE` | `"hwsg-v1"` |
| `W_STAR` | `"W12-q1-s1.75-p0.2"` (context only; KG1, KG5) |
| `TAGS` | `("lo", "mid", "hi")` |
| `CROSS_SEED` | `620640` |
| `DRY_MASTERS`, `DRY_SEEDS` | CONTRACT `seeds.dry_masters_by_world` (620901–620909, three per tag), `seeds.dry_seeds` (620911–620915, K4b seed names) |
| `NEEDLES` | CONTRACT `seeds.kg0_needles` (43 strings) |
| `SIZES`, `BLOCK`, `LGATE_N`, `PANEL`, `LADDER`, `DRAWS`, `KS`, `N_C`, `MODEL_COUNT` | `{"train": 131072, "dev": 4096, "lgate": 4096, "cal": 3072, "val": 3072}`, 3072, 4096, 512, (3072, 6144, 12288), 5000, (1, 2, 4), 3072, 3 |
| `M`, `ALPHA`, `LEARN`, `CAP`, `FLOOR`, `F_PLAN_MAX`, `CAPTURE_FLOOR`, `RISK_MAX` | `Fraction(1,100)`, `Fraction(1,60)`, `Fraction(4,5)`, `Fraction(1,10**4)`, `Fraction(1,10**9)`, `Fraction(1,1000)`, `Fraction(1,2)`, `Fraction(1,100)`; M, ALPHA, CAP, FLOOR equal to `k4b_config` (checked at import; mismatch → `C1GateFailure("FAIL_TECHNICAL/BINDING")`) |
| `RANKS` | `{"alpha": 84, "one_minus_alpha": 4917, "b4_lower": 250, "central_lo": 125, "central_hi": 4875}` = `k4b_config.RANKS` (checked) |
| `O3_ROWS` | `22528` (= 4,096 + 3,072 + 3,072 + 12,288; protocol §7.1 O3 "(10,240 + 12,288)") |
| `HOLD_S`, `HOLD_FROM`, `STEPS` | `6006.6282`, `1000`, `5000` |
| `DISCLOSURE` | CONTRACT `disclosure` (protocol §7.5) |
| `EXCLUSIONS` | `tuple` of stage-B ids (read from HANDOFF at call time by `exclusions()`) plus CONTRACT `exclusions.stage_c_ids` |
| `exclusions(handoff_path=HWSB_STORE/"HANDOFF.json") -> tuple` | sha256 of the bytes = CONTRACT `w_star.handoff_sha256` (else `FAIL_TECHNICAL/IDENTITY`); returns `tuple(stage_c_exclusions) + stage_c_ids` (30 ids) |

### 1.2 Worlds

`WorldDef` (frozen dataclass): `tag`, `key`, `sigma: Fraction`, `p: Fraction`, `neighbour: Fraction`, `sigma_str`, `p_str`, `sigma_float`, `p_float`, `masters: tuple[int, int, int]`, `seeds: dict` (K4b names `val_sd`, `val_b4`, `endpoint`, `fresh_b4`, `val_projection`), `p1_seeds: tuple` (`(val_sd, val_projection)`), `process: tuple` (`PROC_w = ("cylinder", "overlap", sigma_str, p_str, key)`), `world_cfg`, `transition_cfg` (`TransitionConfig(p_stay=p_float)`), `emission_cfg` (`EmissionConfig("overlap", 36, sigma_float, "grid")`), `stage_a: dict` (CONTRACT `worlds[tag].stage_a`), `reservation_id`.

| Name | Contract |
|---|---|
| `WORLDS` | `{tag: WorldDef}` built from CONTRACT at import; `neighbour == (1 − p)/4` asserted exactly (else `FAIL_TECHNICAL/BINDING`); `sigma`, `p` from `Fraction(str)` (never `repr(float)`) |
| `world(w) -> WorldDef` | tag or key; else `ValueError` |
| `world_dir(store, w) -> Path` | `Path(store)/"worlds"/key` |
| `plan(w) -> hwsb_config.Plan` | `Plan("real", masters, hwsb_config.MODEL_CFG, hwsb_config.TRAIN_CFG, {"train": 131072, "dev": 4096}, "resid_post_3", key, PROC_w, 5000, 0)` |
| `dry_plan(w, case, kind="dry_tiny") -> Plan` | `dataclasses.replace(hwsb_config.dry_plan(kind, case), masters=DRY_MASTERS[tag], key=f"DRY-{tag}", process=("cylinder","overlap",f"dry-{tag}",case), sizes=…)` (sizes as `hwsc_config.dry_plan`) |
| `run_key(w, master) -> tuple` | `("hwsg-v1", key, int(master))` (real); `("hwsg-v1", "DRY", case, tag, int(master))` (dry) |

### 1.3 Blindness guard (§8; DRG11)

| Name | Contract |
|---|---|
| `blinded(path, root=ROOT) -> bool` | Pure. `p`, `r` resolved, lower-cased POSIX. True iff `p` (relative to `r`) equals a CONTRACT `blindness.files` entry; lies at or under a `blindness.dirs` entry; has a parent equal to a `blindness.globs[i][0]` and a name matching `globs[i][1]` (`fnmatch`, lower-cased); or lies under `agent-handoff/jobs/<n>` with 197 ≤ int(n) ≤ 223. Exceptions (never blinded): `blindness.allow` entries (exact path or glob on the relative path) |
| `public_summary(path) -> bool` | any component starting with `00_read_me_first`, or consecutive components `docs/research_summary` (lower-cased) |
| `guard(path, root=ROOT) -> Path` | `blinded` or `public_summary` → `C1GateFailure("FAIL_TECHNICAL/BLINDNESS", str(path))` before any open; else `Path(path)` |
| `read_json(path, root=ROOT)`, `read_bytes(path, root=ROOT)` | through `guard` |
| `prune(dirpath, dirnames, root=ROOT) -> None` | removes in place every `dirnames` entry whose path is blinded or public-summary (used by every `os.walk` of HWSG code before descent) |

Registry readers (§6) list directories by name through `prune`-aware walks; listing a blinded directory's names is not an open, but no file under it is opened (OPEN-9).

## 2. `hwsg_bind.py`: world rebinding and audit (§2.3; G3; DRG3)

| Name | Contract |
|---|---|
| `ACTIVE` | `None` outside, the active tag inside `world(...)` |
| `rows(w) -> list[dict]` | rows `{"module", "name", "old", "new"}` for CONTRACT `binding.rows_per_world` in that order. `old` = the attribute value at **import time** (captured once at `hwsg_bind` import into `_IMPORT_VALUES`, identity-held); `new` per CONTRACT `binding.new_values`: `hwsb_config.SCOPE`/`hwsc_config.SCOPE` `"hwsg-v1"`; `KEY` key; `PROCESS` `PROC_w`; `MASTERS` masters; `SIGMA`, `NEIGHBOUR` the exact Fractions; `hwsb_config.TRANS_CFG`, `EMIS_CFG` the world configs; `STORE` `ROOT/hwsg-store/worlds/<key>` (both configs); `hwsc_config.DRY_STORE` `SCRATCH/hwsg-dry`; `STUDY_LEDGER` both `MAILBOX/HWSG_CPU_LEDGER.json`; `hwsc_config.HANDOFF_PATH` `…/worlds/<key>/WORLD_HANDOFF.json`; `hwsb_config.REAL_PLAN` and `hwsc_config.HWSC_PLAN` `gc.plan(w)`; `hwsc_config.SEEDS` the world seeds; `P1C_SEEDS` `p1_seeds`; `RESERVATION_ID` the world's; `DISCLOSURE` the HWSG disclosure; `hwsc_config.load_handoff` → `hwsg_handoff.loader(key)`; `hwsc_data.build_process_c` → `hwsg_oracle.process_builder(key)`; `hwsc_data.process_identity` → `hwsg_oracle.identity_checker(key)` |
| `stage_c_table(w) -> list[dict]` | `hwsc_bind.load_table()` (the 21 stage-C rows) re-targeted: every `k4b_*` `MODELS` → masters; `k4b_config.SCOPE`, `k4b_data.SCOPE`, `k4b_decoder.SCOPE` → `"hwsg-v1/" + key` (OPEN-1); `k4b_*.PROCESS` → `PROC_w`; `k4b_*.SEEDS` → world seeds; `k4b_config.STORE` → world dir; `k4b_driver.ARTIFACTS` → world dir `/artifacts`; `k4b_config.CONTRACT` → `hwsg_config.k4b_view()` (= deep copy of `tools/hwsc/CONTRACT.json` `k4b_contract_view` with `protocol_sha256` = HWSG protocol sha and `authority.c1prime_disclosure` = HWSG disclosure); `k4b_config.CONTRACT_PATH`, `PROTOCOL_PATH` → `tools/hwsg/CONTRACT.json`, `PROTOCOL_HWSG_v1.md`; the three `hwsb_config` rows are dropped (`SCOPE`, `MASTERS` set by `rows(w)`; `DRY_MASTERS` set to the world's dry masters in dry use only). `old` values stay those of the stage-C table (import-time values), so `hwsc_bind.check_old` holds |
| `world(w, dry_case=None)` | context manager. Refuses when `ACTIVE is not None` (`C1GateFailure("FAIL_TECHNICAL/BINDING", "nested world binding")`) or when `hwsc_bind.ACTIVE` is True. Checks every row's current value `is` its import-time value (else `FAIL_TECHNICAL/BINDING`, "code drift", nothing set). Sets rows in order; then enters `hwsc_bind.bound_stage_c(stage_c_table(w))` (or, with `dry_case`, the dry re-target: masters `DRY_MASTERS[tag]`, SCOPE `f"hwsg-v1/DRY/{dry_case}/{tag}"`, seeds `DRY_SEEDS`, store/ARTIFACTS under the case dir). Yields `{"tag", "key", "rows": n, "table_sha256", "stage_c": <bound_stage_c info>}`. On exit (normal or exception) leaves `bound_stage_c`, then restores every row to the exact pre-entry object in reverse order; `ACTIVE = None` |
| `audit(w, modules=None, left_unchanged=None) -> dict` | the `hwsc_bind.audit` scan (same walk, recursion, hit kinds, top names) with the forbidden set CONTRACT `binding.audit.w_star_forbidden` and module dirs `binding.audit.module_dirs`. For `w = "mid"`, the float `0.2` and `Fraction(1, 5)` are the world's own values and are not hits (OPEN-5). Called inside `world(w)`. `PASS` iff every hit's `(module, top name)` is in `left_unchanged` (default CONTRACT `binding.audit.left_unchanged`, TO_FREEZE); else `FAIL_TECHNICAL/BINDING`. Returns `{"status", "hits", "unlisted", "modules", "n_hits"}` |
| `check_explicit(fn_name, kwargs) -> None` | refuses (`FAIL_TECHNICAL/BINDING`) a call of `hwsb_gates.ladder_pilot` without explicit `models`, `seeds`, `ladder`, and of `hwsb_law.law_bound` / `hwsb_data.build_process` without explicit σ/neighbour / configs (DRG3 stale-default trap); used by `hwsg_oracle` and by every HWSG call site |

**Copied-name hazard (§2.3).** `hwsc_data.build_process_c(store, masters=cc.MASTERS)` and `hwsb_data.build_process(..., emission_cfg=hc.EMIS_CFG, …)` captured w\* defaults at definition time; rebinding constants does not reach them. Hence `hwsc_data.build_process_c` and `hwsc_data.process_identity` are rebound to HWSG functions (rows above), and every HWSG call passes masters and configs explicitly. Parallel training uses separate processes, never two bindings in one process.

## 3. `hwsg_handoff.py`: WORLD_HANDOFF (§2.6)

| Name | Contract |
|---|---|
| `build(w, o_result) -> dict` | `{key, sigma, p, neighbour, Z_bound, F_plan, p_D2a, N_C: 3072, model_count: 3, process_identities, exclusions, protocol_sha256}` from the O record of the world (Fractions as str, `p_D2a` float, `exclusions` = `gc.exclusions()` as list) |
| `write(world_dir, handoff) -> str` | exclusive create of `world_dir/"WORLD_HANDOFF.json"`; returns its sha256 |
| `load(w, store=gc.STORE, expected_sha256=None) -> dict` | reads through `guard`; key set equal to CONTRACT `handoff.keys` exactly; no `handoff.forbidden_keys` at any depth; `key` equals the world key; `neighbour == (1 − p)/4` exactly; `F_plan == k4b_cert.F_plan(Z_bound)`; `expected_sha256` default = the sha256 recorded for that file by the O `STAGE_COMPLETE` event of `store/STAGES.jsonl` (absent → `FAIL_TECHNICAL/IDENTITY`); returns Fractions, ints, float as typed in CONTRACT. Any defect → `C1GateFailure("FAIL_TECHNICAL/IDENTITY", …)` |
| `as_hwsc(h) -> dict` | the view stage-C functions read: `{"Z_bound", "F_plan", "p_D2a", "N_C", "k_C": 1, "model_count", "stage_c_exclusions": tuple(h["exclusions"]), "registry_value": (10240 + N_C)*Fraction(p_D2a)}`. No HWSB_PASS record is fabricated: `outcome`, `report_sha256` are absent |
| `loader(key)` | returns a function with the `hwsc_config.load_handoff(path=None, expected_sha256=None)` signature returning `as_hwsc(load(key))` (bound into `hwsc_config.load_handoff` by `world`) |

## 4. `hwsg_oracle.py`: process, identity, stage O (§2.3, §2.6, §3; O0–O5)

| Name | Contract |
|---|---|
| `build_process_g(store, w, masters=None) -> dict` | `hwsb_data.build_process(store, masters=masters or W.masters, emission_cfg=W.emission_cfg, world_cfg=W.world_cfg, transition_cfg=W.transition_cfg)` (all explicit); then **override** `proc["sigma"] = W.sigma`, `proc["neighbour"] = W.neighbour` (stage A's exact Fractions; G5, R3) |
| `process_builder(key)` | `lambda store, masters=None: build_process_g(store, key, masters)` (bound into `hwsc_data.build_process_c`) |
| `identity(store, proc, w) -> dict` | checks: (a) `proc["sigma"] == W.sigma`, `proc["neighbour"] == W.neighbour` exactly, and `(1 − W.p)/4 == W.neighbour`; a neighbour from `repr(float(p))` (e.g. `(1 − Fraction(repr(5/6)))/4`) fails; (b) WorldSpec id = CONTRACT `world_common.WorldSpec_id_expected` and its payload sha256 equals `WorldSpec_payload_sha256` (via `hwsb_data.spec_checksums`); (c) `T` equals the max-degree lazy walk with `p_stay = W.p_float` from `src/topo_pilot/process/transition.py` rebuilt independently (`np.array_equal`); (d) `E_canon[m]` bitwise equal across masters; (e) `validate_process(proc, 1e-12)` passes; (f) `hwsb_data.arrays_sha256(proc)` (T, E, pi, coords). Returns `{"ok", "checks": {name: bool}, "ids": proc ids, "arrays_sha256", "transition_id", "spec_checksums"}` |
| `identity_checker(key)` | function `(store, proc) -> dict` (bound into `hwsc_data.process_identity`): `identity(store, proc, key)` plus equality of `ids` (world, transition, emission per master) and `arrays_sha256` with WORLD_HANDOFF `process_identities`; `ok` False on any difference |
| `selection(report_path=gc.REPORT_PATH, s3_dir=gc.S3_DIR) -> dict` | **O0.** sha256 of REPORT.json = CONTRACT `selection.report_sha256`, and each S3 world record's sha256 = CONTRACT `selection.s3_record_sha256[key]` (else `FAIL_TECHNICAL/BINDING`). Pool = `finalists.ordinary` without `W_STAR`, kept iff the S3 record `law_bound.status == "BOUNDED"` (an `UNAVAILABLE/*` status excludes). `lo = argmin L3.D4`, `hi = argmax` (`report["s3"][key]["L3"]["D4"]`), `mid = argmin over the rest of |ln L3 − (ln L3_lo + ln L3_hi)/2|` (`math.log`, float64); ties by `finalists.ordinary` order (first wins). Returns `{"pool", "L3": {key: float}, "lo", "mid", "hi", "registered_ok": (lo, mid, hi) == CONTRACT selection.registered}`; `registered_ok` False → `C1GateFailure("FAIL_TECHNICAL/BINDING", …)` |
| `law(proc, w) -> dict` | **O2.** `hwsb_law.law_bound(proc["T"], proc["E_canon_shared"], proc["pi"], proc["coords"], sigma=W.sigma, neighbour=W.neighbour)` (explicit). Requires `status == "BOUNDED"`, `kappa < 1`, `delta == 0`, `Z_bound == Fraction(stage_a.law_bound_Z_exact_upper)` (N8: the S3 record `law_bound.Z_bound.exact_upper`, read from the hash-checked S3 record), `F_plan = k4b_cert.F_plan(Z_bound) <= Fraction(1, 1000)`. Any exception → `FAIL_TECHNICAL/LAW_BOUND`. Returns `{"status", "Z_bound", "kappa", "delta", "F_plan", "Z_ref"}` |
| `d2a(proc) -> dict` | **O3.** `p = hws_exact.p_d2a(proc["T"], proc["E_canon_shared"], proc["pi"])`; `value = 22528 * Fraction(float(p))`; `ok = value <= Fraction(1, 100)` (equality passes). Failure → `INCONCLUSIVE/REGISTRY_RISK` |
| `reproduce(proc_hws, w, hist_path=None) -> dict` | **O4** (OPEN-2). (a) The stage-A S3 record (hash-checked) gives `hist_sha256`, `bounds.<q>.mean` for q ∈ {D4, GC, G4, G4A}. (b) Regenerate in memory: `look = hws_oracle.world_look(proc_hws, "S3", 32768, Ks, p4=False)` with `proc_hws = hws_worlds.build_process(<stage-A world spec of key>)` (stream `["data", "hws-v1", "S3", key]`). (c) The stored table `hws-store/hist/S3/<key>.npz`: `stage_records.sha256 == hist_sha256` and its `canon32` equals `look["tok"]` bitwise (KB5 pattern; the stored file is read only here and only in the real O job). (d) Means by the `hwsb_kb.kb5` formulas (`c1_means.tree_mean` of `he.d4_rows(he.moments(proc, tok))`, `kl_rows(q32, q1)`, `kl_rows(q32, q4)`, `kl_rows(circ(q32), circ(q4))`) on the regenerated tokens, each within `1e-12` (absolute) of the record mean. Failure → `FAIL_TECHNICAL/ORACLE`. In tests and the dry run `hist_path` points to a synthetic file |
| `headroom(w, report) -> dict` | **O5.** `report["s3"][key]["at_3x"] is True` and `report["s3"][key]["L3"]["D4"] >= 3 * float(M)`; else `INCONCLUSIVE/ORACLE_FEASIBILITY` |
| `run_o(out, auth, sched, job, store=None) -> dict` | the O job (§11.2). Writes `stages/O/O_RECORD.json`, per world `worlds/<key>/WORLD_HANDOFF.json` (passing worlds only) and one `complete_stage(out, "O", [O_RECORD, every WORLD_HANDOFF, every artifact file])` |

## 5. `hwsg_train.py`: parallel training children (G7; §9; DRG12, DRG13; KG4)

| Name | Contract |
|---|---|
| `child_argv(w, master, out, job, attempt) -> list[str]` | argv of one child: `[python, "-s", "-m", "hwsg_train", "child", "--world", key, "--master", str(master), "--out", str(out), "--job", job, "--attempt", str(attempt)]` with env from `child_env` |
| `child_env(job, out) -> dict` | `os.environ` copy with `PYTHONPATH` = `<worktree>/src` + tools paths, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS` = `"1"`, TEMP/TMP/TMPDIR = `out/"tmp"/f"tmp-{job}-{master}"` (store) or the test root (dry) |
| `ram_ok(n_children=3, free_bytes=None) -> dict` | `free_bytes` default from `psutil.virtual_memory().available`; `ok = free_bytes >= n_children * 1610612736 + 4294967296` (CONTRACT `resources.aggregate_ram_check`, OPEN-10). Refusal → no child launched, gate `RAM` `REFUSED` |
| `child(world_key, master, out, job, attempt) -> dict` | runs in its own process: `with hwsg_bind.world(key):` `store = ArtifactStore(LocalFSBackend(world_dir/"artifacts"))`; `proc = hwsg_oracle.build_process_g(store, key)`; identity vs WORLD_HANDOFF (`identity_checker`); `obs = hwsc_data.make_train_dev_c(store, proc, master, gc.plan(key), scope="hwsg-v1")`; `hwsb_train.set_threads(1)`; `hold = hwsb_train.HoldRule(world_dir/"stages"/"TRAIN"/str(master), cap_s=6006.6282, steps=5000, from_step=1000)`; `res = hwsb_train.train(store, {"train", "dev"}, master, plan=gc.plan(key), hold=hold)`; require `res["run_key"] == ["hwsg-v1", key, master]`, all 12 checkpoint steps, `steps_done == 5000`, finite losses; writes `TRAIN_RECORD.json` (exclusive) and the attempt record `logs/CHILD_<master>_a<attempt>.json` `{"master", "pid", "cpu_s", "peak_rss", "status", "utc"}`. Writes only under `world_dir/stages/TRAIN/<master>/`, `world_dir/artifacts/` (content-addressed) and its log. `StageFailure NONFINITE_LOSS` → status `FAIL_TECHNICAL/TRAINING`; a hold → `FAIL_TECHNICAL/RESOURCE` (report step, CPU, projection only, never dev CE) |
| `run_train(out, w, auth, sched, kc_accept, job, launcher=None) -> dict` | the TRAIN-w job: preflight (§9.1), `KC_ACCEPT`, WORLD_HANDOFF present (else refused); `ram_ok()`; launches the three children (`launcher` default `subprocess.Popen` with `child_argv`/`child_env`) concurrently, waits for all; each child's exit and record determine its model status; then `complete_stage(world_dir, f"TRAIN", [three TRAIN_RECORDs, HOLD files, new artifact files])` and, when all three are COMPLETE, `OBS_INVENTORY.json` = `hwsb_registry.history_inventory(world_dir)`. A killed child → that model `FAIL_TECHNICAL/RESOURCE`, siblings complete (DRG12); the world's outcome is then that status (no model is omitted). A rerun after a kill archives the attempt (`k4b_release.archive_attempt`) and reruns from scratch with identical seeds (X-3) |
| `aggregate(world_dir, job, ledger_path) -> dict` | coordinator-side, after all children terminate: reads the attempt records and appends one ledger entry per child (`label = f"{job}-TRAIN-{tag}-{master}-a{k}"`, each process charged once) |
| `main(argv=None) -> int` | subcommand `child` (above) |

## 6. `hwsg_registry.py`: composition adapter, readers b–d, inventory (§6; N6; DRG9; KG8)

Every source returns the `nd_registry._new` shape (`{"status", "digests": set[str], "seq_ids": set[int], "files", "other": [{"path", "reason"}], "non_history", "non_c2_format", "present", "known_gaps"}`); `other` non-empty → `INCOMPLETE`.

| Name | Contract |
|---|---|
| `CLASS_TO_READER` | CONTRACT `registry.class_to_reader` as `{(class, reader): function or None}`: `("K4b history table", "k4b_history_table") → read_k4b_history_table`; `("NON_HISTORY", None) → None` (never opened). Any other pair → INCOMPLETE |
| `read_k4b_history_table(path, entry, out) -> None` | `stage_records.sha256(path) == entry["sha256"]` (else `FAIL_TECHNICAL/LINEAGE`); `np.load(path, allow_pickle=False)`; keys `canon32`, `seq_ids`, `digest` required (else `other`); digests ← `digest` entries (`<U64`), `seq_ids` ← `seq_ids` int64 |
| `obligation_files(store) -> list[str]` | name-only listing of `REGISTRY_OBLIGATION*.json` |
| `latest_obligation(store, bound=None) -> dict` | `bound` = CONTRACT `registry.obligation_stores[store].obligation` path and sha256 once frozen (TO_FREEZE); until frozen, the file with the greatest `written_utc` (OPEN-3); sha256 checked against `bound`; schema `hws-registry-obligation-v1`; missing → `INCOMPLETE` ("missing phase-2 obligation") |
| `array_listing(store) -> list[dict]` | walk of `store` (with `gc.prune`), every `.npz`, `.npy`, `.pt` file: `{"relpath", "bytes"}` (stat only; nothing opened); superseded and scratch subfolders included |
| `source_obligation(store, bound=None, opener=None) -> dict` | **(c).** `obl = latest_obligation(store, bound)`; `listing = array_listing(store)`; compare by relpath: in listing not in obligation → `other` "new"; in obligation not in listing → `other` "missing"; bytes differ → `other` "resized"; every obligation entry's `(class, reader)` in `CLASS_TO_READER` (else `other` "unknown class/reader"); history entries read by their function (`opener` hook for tests, default `open`); NON_HISTORY recorded in `non_history` never opened. Metadata files (`.json`, `.jsonl`, `.md`, `.lock`, `.txt`, `.log`) listed separately under `metadata` (never classified as history) |
| `source_hwsc(store=gc.HWSC_STORE, expected=None) -> dict` | **(b).** ObservationSets via `hwsb_registry.registry_digests(store, expected)` (`expected` default = `read_json(store/"stages/TRAIN/OBS_INVENTORY.json")`); `HIST_*.npz` under `stages/S3`, `stages/S7` and `superseded/**` by the token reader (`hwsc_registry._token_file`, reused); CONTRACT `registry.hwsc_store.non_history_by_name` globs → `non_history` (never opened); `SEALED_*.json`, `sealed/**` name only; `stages/` subfolders named `hwsd-dry-*`, `hwsd-run-*` → `source_obligation(hwsd-store)` assignment, `hwsu-dry-of-*` → hwsu; any other unassigned array → `other` |
| `source_scratch_g(scratch=gc.SCRATCH, table=None) -> dict` | **(d).** every top-level scratch directory modified since 2026-10-29 must match a row of the frozen table (CONTRACT `registry.scratch_dirs_at_0224`, rows by exact name, with prefix rules `scratch_prefix_rules` as defaults); EXCLUSION rows are listed, not read; READER rows read by their reader; a `TO_FREEZE` row or an unmatched directory → `INCOMPLETE`; stage C's R6 rows (directories before 2026-10-29) via `hwsc_registry.source_scratch_c` |
| `source_own(store, worlds) -> dict` | **(f).** per world `hwsb_registry.registry_digests(world_dir, expected=OBS_INVENTORY)` (18 ObservationSets), superseded and interrupted attempts included |
| `inventory_g(root=gc.ROOT) -> dict` | **(e).** `hwsc_registry.inventory_c(root)` with the added rows (hwsc-store READER, hwsu-store/hwsd-store OBLIGATION, hwsg-store OWN, worktree rows); an unlisted top-level directory holding a history file, identity reference or ObservationSet root → `INCOMPLETE`; a wildcard non-history classification → `INCOMPLETE` |
| `sources(root, scratch, worlds, extra=None) -> dict` | the union: stage C's K-REG sources (`hwsc_registry_build._default_sources`, reused, R1–R8 with frozen readers) + (b) + (c) for both stores + (d) + (f) + `extra` (K-REG2: every world's lgate, cal, val tables drawn so far, failed worlds included) |
| `build(version, out_dir, root=None, scratch=None, worlds=gc.TAGS, extra=None, sources_fn=None) -> dict` | mirror of `hwsc_registry_build.build` (same manifest, digest file, run dir, CPU/peak-memory/bytes fields) over `sources(...)`; `version` ∈ CONTRACT `registry.versions`; REHEARSAL writes to `out_dir/"rehearsal"`; the manifest adds `certificate` (§6 below), `inventory_sha256`, `readers_version` (sha256 of the canonical JSON of CONTRACT `registry`), `obligations` `{store: {path, sha256}}`. Status: any source FAIL_TECHNICAL → that; any `other` → `INCOMPLETE`; else PASS |
| `certificate(manifest) -> str` | sha256 of canonical JSON `{inventory_sha256, readers_version, sources_sha256}` |
| `recheck(manifest, root=None) -> dict` | recomputes `inventory_g` and every obligation/listing comparison; certificate differs → `INCONCLUSIVE/REGISTRY_INCOMPLETE` (called immediately before every draw) |
| `separation_g(reg, tables_by_world) -> dict` | `hwsc_data.separation_c` per world against `reg`, plus every cross-world pair of blocks (`f"{w1}:{s1}_{w2}:{s2}"` digest intersections, sequence-id intersections); collision → `FAIL_TECHNICAL/LINEAGE`; predicate non-PASS → `INCONCLUSIVE/REGISTRY_INCOMPLETE` |

**Registry hygiene.** Outputs in `hwsg-store/registry/` (REHEARSAL under `rehearsal/`), metered separately (own 20 GiB output cap). The full needle search runs at most once per job (cached in-job). Readers never open `state.pt`, `sealed/`, foreign checkpoints or effect reports.

## 7. `hwsg_ratio.py`: capture ratio (§2.7; N1, N7; KG7, DRG10)

| Name | Contract |
|---|---|
| `D_KEY` | `"delta4_orc:all"` (N7: one-sided; `delta4_orc` is not in `k4b_cert.CONTROL_K`) |
| `draws(arrays, controls, seed) -> dict` | `k4b_stats.joint_bootstrap(k4b_fresh.bootstrap_inputs(arrays, controls), seed)` (5,000 draws, the endpoint seed of the world) |
| `ratio_draws(dr, j) -> dict` | `{"minus": dr[f"X:{j}:-"] / dr[D_KEY], "plus": dr[f"X:{j}:+"] / dr[D_KEY]}` float64 |
| `model_ratio(dr, j, point_minus, point_D) -> dict` | `rho = point_minus / point_D` (point = `c1_means.tree_mean` of the arrays); `rhoL`, `rhoU` = rank 84 and rank 4,917 of `ratio_draws(...)["minus"]` with `k4b_stats.bounds` rank checks (`(value, rank)`); central 95 % (ranks 125/4,875) of both minus and plus ratio draws; never clipped |
| `ratio_gate(ctx, result, world_b4_pass, seed) -> dict` | **RATIO** (E2 gate after ENDPOINT). `dr = draws(ctx["test_arrays"], ctx["controls"], seed)`; identity: for every j, `k4b_stats.bounds(dr[f"X:{j}:-"], dr[f"X:{j}:+"])` L and U equal `result["per_model"][j]["L"]`, `["U"]` bitwise (else `FAIL_TECHNICAL/NUMERICAL`). `D_L` = rank-84 value of `dr[D_KEY]`. Status `RATIO_UNRESOLVED` for all models iff not `world_b4_pass`, or `D_L <= 0`, or any `dr[D_KEY][d] <= 0` (OPEN-11); else `DEFINED`. Writes `stages/S8/RATIO.json` `{"status", "D_L", "D_point", "per_model": {j: model_ratio}, "seed", "identity": true}` and `stages/S8/RATIO_DRAWS.npz` (`rho_minus_<j>` float64[5000] per model, the world's `rho_bar` draws) — sha256s go into the S8 `STAGE_COMPLETE` with RESULT.json (OPEN-12) |

## 8. `hwsg_cross.py`: cross-world readings (§2.7, §7.1 X, §7.4; DRG7, DRG10, DRG14)

| Name | Contract |
|---|---|
| `load_world(store, w) -> dict` | the world's RESULT: `stages/S8/RESULT.json` (endpoint) or `stages/TERMINAL/RESULT.json` (stopped earlier); its sha256 must equal the hash in that world's latest `STAGE_COMPLETE` (else `FAIL_TECHNICAL/LINEAGE`); a registered world with neither → `FAIL_TECHNICAL/LINEAGE` (never treated as EXCLUSION). Endpoint worlds also load `RATIO.json`, `RATIO_DRAWS.npz` (hash-checked). Returns `{"tag", "outcome", "endpoint": bool, "p1_passed": bool, "per_model_status": {j: status}, "per_model": {j: {L, F_minus, …}}, "ratio": RATIO or None, "rho_draws": {j: array} or None}` |
| `general(worlds) -> dict` | `worlds` = list of `load_world` results for all three tags. `GENERAL` iff every outcome is `SUPPORT` and there are three; `NOT_GENERAL` iff some world has `p1_passed` and `endpoint` and some model status `EXCLUDE` (names worlds and models); else `GENERAL_UNAVAILABLE` with `reasons` (per world outcome). A MIXED world without EXCLUDE never yields NOT_GENERAL |
| `annotations(worlds) -> list` | `ALL_EXCLUSION` iff ≥ 2 endpoint worlds and every endpoint world `EXCLUSION`; `POSITIVE_EVERYWHERE` iff ≥ 1 endpoint world and every model of every endpoint world has `Fraction(float(L)) − Fraction(F_minus) > 0` |
| `capture(worlds) -> dict` | endpoint worlds only. `< 2` → `CAPTURE_UNAVAILABLE`. Else in order: `CAPTURE_BELOW_HALF` iff some DEFINED model has `Fraction(float(rhoU)) < 1/2`; `CAPTURE_AT_LEAST_HALF` iff every model of every endpoint world is DEFINED and `Fraction(float(rhoL)) >= 1/2` (equality passes); else `CAPTURE_UNRESOLVED` (OPEN-7). Returns `{"reading", "worlds_covered", "unavailable": [worlds or models not covered], "n_models"}` |
| `similarity(worlds, seed=620640) -> dict` | endpoint worlds with DEFINED ratios. `rho_bar_w` = mean of the world's model point ratios; per-draw `rho_bar*_w[d]` = mean over its models of `rho*_wj[d]`. `COMMON_FRACTION_COMPATIBLE` iff `max_j central_lo_j <= min_j central_hi_j` over all DEFINED models (central = ranks 125/4,875 of the minus ratio draws). Spread `S = max rho_bar − min rho_bar`; pairing: one `np.random.Generator(np.random.PCG64(620640))`; for each endpoint world in `worlds_order`, `perm = g.permutation(5000)` and `v_w = rho_bar*_w[perm]`; `S*[d] = max_w v_w[d] − min_w v_w[d]`; bound = rank 4,917 of `S*` (OPEN-8). Labels only |
| `licence(reading, fill) -> str` | CONTRACT `licences[...]` with `str.format_map` (missing keys `"n/a"`); NOT_GENERAL carries its error statement; CAPTURE_AT_LEAST_HALF names covered and unavailable worlds/models; the similarity sentence uses `compatible`/`not compatible` only |
| `run_cross(out, auth, sched, job) -> dict` | the CROSS job: `load_world` for all three registered worlds; writes `stages/CROSS/CROSS.json` `{"worlds": {tag: outcome}, "general", "annotations", "capture", "similarity", "licences", "error_statements", "disclosure", "does_not_establish", "w_star_context": "descriptive only"}`; rank-check failure → `FAIL_TECHNICAL/NUMERICAL` |

## 9. `hwsg_records.py`: records, preflight, freeze, ledger, safeguards (§7.1 S0/PF/WIN; §10.3)

| Name | Contract |
|---|---|
| `status_of`, `run_gates_c`, `lineage_c`, `record_gate_files`, `superseded_ok` | `hwsc_records` functions reused unchanged, called on the HWSG store or a world dir (inside `world(w)`) |
| `lineage_g(out) -> dict` | `hwsc_records.lineage_c` per world dir plus the top-level store with the HWSG record names (`FREEZE.json`, `KC_ACCEPT.json`, `OPERATION_ACTIVE.json`, `REGISTRY_OBLIGATION.json`, `AUTH_*`, `SCHED_*`, `ACCEPT_*`, `RELEASE_*`, `RESERVATION_*`, `WORLD_HANDOFF.json`), free dirs `logs`, `tmp`, `tmp-*` |
| `auth_ok(auth, stage, freeze=None) -> dict` | `stage in auth["stages"]`; `auth["owner_auth_sha256"]` = CONTRACT addendum-43 sha256; `auth["freeze_sha256"]` = sha256 of `FREEZE.json` (all stages after the freeze); missing → ok False |
| `window_ok(sched, root=gc.ROOT, stage=None) -> dict` | **WIN.** No `OPERATION_ACTIVE.json` with `active: true` in any store except this job's own; `sched["track_u_real_finished"] is True`; `sched["frozen_registries_awaiting_draw"] == []`; failure → gate `WINDOW` `REFUSED` (no outcome) |
| `preflight(out, stage, auth, sched, repo=gc.REPO) -> dict` | `verify_freeze_g`; `auth_ok`; `window_ok`; refusal records `AUTH`/`WINDOW` gates and returns `{"refused": True}` before any draw |
| `s0(repo, r_ref, h_exec) -> dict` | **S0 BINDING.** protocol sha256 = CONTRACT; request sha256 = CONTRACT; `git diff --no-renames --name-status r_ref h_exec` touches only `tools/hwsg/`, `tests/hwsg/`, `docs/code_index/` (added or modified); every CONTRACT `reuse_sha256` file at `h_exec` equal; `k4b_config.MARGIN == Fraction(1, 100)`; `k4b_config.check_chart_equality()` PASS and `tools/c1prime/CONTRACT.json` `chart` equal at both refs; hwsb CONTRACT `recipe` == hwsc CONTRACT `recipe`. `{"status": "PASS" or "INVALID", "checks"}` |
| `freeze_g(out, repo, h_exec, dry_report, pf_record) -> dict` | as `hwsc_records.freeze_c` with HWSG files (`tools/hwsg/*`, `tests/hwsg/*`) and no separate run approval (addendum 43 item 2) |
| `verify_freeze_g(out, repo)` | re-hash; mismatch → `FAIL_TECHNICAL/BINDING` |
| `ledger_read(path)`, `ledger_append(path, label, job, stage, cpu_s, source, world=None, master=None)` | study `"hwsg-v1"`; unique labels (duplicate → `FAIL_TECHNICAL/LEDGER`); atomic replace |
| `meter_caps(stage, k=None) -> dict` | `{"max_cpu": 5 * central(stage, k), "max_wall": 4 * central_wall(stage)}` from CONTRACT `cpu` (TRAIN child: `max_cpu = 6006.6282`); a kill → `FAIL_TECHNICAL/RESOURCE` |
| `central(stage, k=None) -> float` | CONTRACT `cpu.central_s[stage]` (`E2`: `900*k + 100`) |
| `output_cap(kind) -> int` | `"world"` 16 GiB, `"registry"` 20 GiB |
| `marker_replace(path, obj, retries=5, sleep_s=0.2) -> None` | write `path.with_suffix(".tmp")`, `os.replace`, retried on `PermissionError` (Windows); coordinator-side only |
| `terminal_result(world_dir, w, status, stage, gate, details, p1_passed) -> Path` | `stages/TERMINAL/RESULT.json` (exclusive) with CONTRACT `records.TERMINAL_RESULT` keys, licence by `hwsc_outcome.licence`, disclosure; one `complete_stage(world_dir, "TERMINAL", [it])` |
| `export_g(world_dir, result, oc, ann, fill, ratio_files) -> Path` | `hwsc_records.export_c` pattern: RESULT.json, SEALED_OPENED.json, RATIO.json, RATIO_DRAWS.npz in **one** `S8` `STAGE_COMPLETE` (D6) |
| `release_barrier(store) -> dict` | **R2.** For every registered tag: an accepted terminal outcome (`ACCEPT_TERMINAL.json` binding the TERMINAL RESULT sha256) or an accepted E1 validation (`ACCEPT_VALIDATION.json` binding `stages/S5/VALIDATION_REPORT.json`); `ok` False otherwise; release B present for every E1-accepted world before the first E2 |

## 10. `hwsg_known.py`: KG0–KG8 (§5)

| Name | Contract |
|---|---|
| `kg0(out, auth, sched, root=gc.ROOT, cache=None) -> dict` | authority records (addenda 25, 26, 37, 43, 44 by sha256; HWSG design freeze by sha256); `hwsc_known.seed_search_c(root, NEEDLES)` with `gc.prune` (one walk per job, result cached in `cache`); hits classified by CONTRACT `seeds.kg0_declaration_fragments`; any other hit → `FAIL_TECHNICAL/BINDING`; `hwsg-store` absent or holding only this lineage (FREEZE sha256 match); no foreign active `OPERATION_ACTIVE.json` |
| `kg1(store) -> dict` | inside `hwsg_bind.world` is **not** entered for w\*; instead a w\* `WorldDef` (σ 7/4, p 1/5, stage-C masters and seeds) through the same row builder: every rebound constant equals stage C's (`hwsc_config`, `hwsb_config` values), and `build_process_g(store, w*)` reproduces stage C's process identities (CONTRACT hwsc `world.WorldSpec`, `TransitionSpec`, `selection_sha256`) |
| `kg2() -> dict` | first 64 cal draws (`SeedTree(0)` generator draws, no histories) differ across the three worlds and from stage C's tag; lgate/cal/val sequence-ID sets (64 rows each, in memory) pairwise disjoint across worlds; a planted shared-σ pair collides under σ-only tags and not under `PROC_w` tags |
| `kg3(proc_w0) -> dict` | `hwsb_known.kb2_kb3(proc_w0)` (100 steps bitwise, one thread) |
| `kg4(out, launcher=None) -> dict` | three one-thread 100-step trainings on DRY masters 620901–620903 (tiny E4 data in a scratch case dir) as concurrent metered children and again sequentially: checkpoint payload sha256 equal bitwise |
| `kg5(proc_w0, proc_star, handoff, worlds_procs) -> dict` | w0 `law_bound(σ 5/4, nb 1/5)` Z_bound = CONTRACT `law.w0.Z_bound_ref` with δ = 0; w\* Z_bound and `F_plan` = HANDOFF exactly; per chosen world `hwsg_oracle.law` equality with the stage-A record (oracle computation, no draw) |
| `kg6(job) -> dict` | runs the CONTRACT `known_cases.kg6_suites` with pytest inside `hwsg_bind.world("hi")` ∘ `bound_stage_c` (the HWSC KC8 port: one pytest session in-process via `pytest.main([...], plugins=[binding plugin])`, basetemp under `test_hwsg-<job>`), plus the POSITIVE_BELOW_MARGIN cases of `tools/hwsc/API.md` §12.2; PASS iff exit code 0 |
| `kg7() -> dict` | synthetic fixture (TEST_PLAN §4 KG7 fixture): planted `X− = c·D` for c ∈ {1/2, 9/10, 3/2} gives `rho == c` (≤ 1e-12) and `rhoL ≤ c ≤ rhoU`; re-derived draws equal the endpoint's L, U bitwise on a seed-sensitive fixture; D ≤ 0 → `RATIO_UNRESOLVED`; ratio > 1 and negative numerator not clipped |
| `kg8(out) -> dict` | `hwsg_registry.build("REHEARSAL", out/"registry", root=gc.ROOT)`; CPU, peak memory and bytes recorded; PASS iff status PASS |
| `run_kc(out, auth, sched, job) -> dict` | KG0 → KG8 in CONTRACT order; first failure stops (KG0 keeps its status; others `FAIL_TECHNICAL/KNOWN_CASE`, all worlds); later items `NOT_RUN`; writes `stages/KC/KG_RECORD.json` and one `complete_stage(out, "KC", …)` |

## 11. The jobs and every gate's computation, in order (§7.1, §9)

Stage order (§9): `J-G1 + DRY` → execution FREEZE → **KC** → **O** → **TRAIN-lo/mid/hi** → **REG1** → **E1-lo/mid/hi** → ACCEPTs → **REG2** + release B per E2-eligible world → **E2-w** → **CROSS**. Each stage writes `<job>.accepted.json` (coordinator) before the next. Every job: S0 freeze check and the binding audit at dispatch (`BINDING_AUDIT`, inside `world(w)` for world jobs; non-PASS → `FAIL_TECHNICAL/BINDING`, nothing drawn); WIN gate before KC, REG1 and every draw. A world's first non-PASS gate ends that world (later gates `NOT_RUN`), writes `stages/TERMINAL/RESULT.json`, and other worlds continue (§7.3); a shared failure (KG, R1, R2) stops all.

### 11.1 KC job — §10

### 11.2 O job (one metered job; trains nothing; draws no evaluation row)

| # | Gate | Computation | Failure |
|---|---|---|---|
| O0 | `SELECTION` | `hwsg_oracle.selection()` | `FAIL_TECHNICAL/BINDING` (all) |
| per world in `worlds_order`: | | | |
| O1 | `PROCESS_IDENTITY_<tag>` | `store = ArtifactStore(LocalFSBackend(world_dir/"artifacts"))`; `proc = build_process_g(store, w)`; `hwsg_oracle.identity(store, proc, w)["ok"]`; WorldSpec unchanged; TransitionSpec id recorded | `FAIL_TECHNICAL/IDENTITY` (w dropped) |
| O2 | `LAW_BOUND_<tag>` | `hwsg_oracle.law(proc, w)` | `FAIL_TECHNICAL/LAW_BOUND` (w dropped) |
| O3 | `D2A_RISK_<tag>` | `hwsg_oracle.d2a(proc)` | `INCONCLUSIVE/REGISTRY_RISK` (w dropped) |
| O4 | `ORACLE_REPRO_<tag>` | `hwsg_oracle.reproduce(...)` | `FAIL_TECHNICAL/ORACLE` (w dropped) |
| O5 | `HEADROOM_<tag>` | `hwsg_oracle.headroom(w, report)` | `INCONCLUSIVE/ORACLE_FEASIBILITY` (w dropped) |
| — | handoff | passing worlds: `hwsg_handoff.build` + `write`; dropped worlds: `terminal_result(..., p1_passed=False)` | — |

### 11.3 TRAIN-w job — §5 (`run_train`). Gate `T_<tag>` PASS iff all three children COMPLETE with finite loss, 12 checkpoints, TRAIN_RECORD per master, run keys and recipe exact.

### 11.4 REG1 job (once, after all TRAIN jobs, before any E1 draw)

WIN; `m = hwsg_registry.build("K-REG1", STORE/"registry")`; coordinator completeness certificate written `REG1_CERTIFICATE.json` binding `m["certificate"]`. Non-PASS → `INCONCLUSIVE/REGISTRY_INCOMPLETE` for all worlds.

### 11.5 E1-w job (release A per world): stage-C gates 0–10 under `hwsg_bind.world(w)`

Context: `rel = k4b_release.verify_release(world_dir/"RELEASE_A.json", "A", task_sha256, session, STORE/"FREEZE.json")`; `handoff = hwsg_handoff.as_hwsc(hwsg_handoff.load(w))`; `ctx = {"release": rel, "reservation_path": world_dir/"RESERVATION_W2.json", "handoff": handoff}`; `rel["reservation"] == W.reservation_id`.

| # | Gate | Computation (reused, under the binding) |
|---|---|---|
| 0 | `G0C` | `hwsc_known.g0c(world_dir, "E1", auth, sched, rel)` with WIN and the cached KG0 search |
| 1 | `H1G` | `hwsc_gates.h1c(world_dir, ctx, handoff, store)`: TRAIN records bound; checkpoint meta (`expected_meta_c` reads `cc.SCOPE`, `cc.KEY` → `("hwsg-v1", key, j)`); exclusion check against the 30 ids; `build_process_c` → `build_process_g`; `process_identity` → `identity_checker`; `law_identity` (σ, neighbour rebound; Z_bound = WORLD_HANDOFF exactly); `a1_selftest`; threads 1; p_D2a relative ≤ 1e-12 |
| 2 | `REG1_LOAD` | `rel["kreg1_certificate"]` = REG1 certificate; `hwsg_registry.recheck(manifest)`; `ctx["reg1"] = c2_registry.Registry.load(STORE, "K-REG1")` |
| — | S3 sampling | `hwsc_data.h2c(world_dir, ctx)`: lgate b0 4,096 (via `sample_block_c`), cal b0, val b0 3,072 each, under the bound streams (§2) |
| 3 | `H2` | `hwsc_data.separation_c` per world + `hwsg_registry.separation_g` across worlds already drawn |
| 4 | `L1` | `hwsc_gates.l1(world_dir, ctx)` (all three; captured ≥ 4/5; G_C > 1e-6) |
| 5 | `ORACLE-VAL` | `k4b_driver.oracle_val` (Decimal moments ≤ 1e-10) |
| 6 | `B4-VAL` | `k4b_driver.b4_val` (seed `val_b4` of w; `lower − 0.01 > max(B_H + Z, 1e-9)`) |
| 7 | `C0-CAL` | `k4b_driver.c0_cal_stage` (one production chart, no retries) |
| 8 | `C0-VAL` | `k4b_driver.c0_val_stage` (≥ 507/512 support, fidelity ≥ 0.80, 12 bins ≥ 8, resultant ≤ 0.30) |
| 9 | `CERT-VAL` | `k4b_driver.cert_val` (row bound ≤ 1e-4, `|X̂| ≤ 4`) |
| 10 | `P1` | `hwsc_gates.p1c(world_dir, ctx, handoff)`: `p1c_ladder` → `hwsb_gates.ladder_pilot(models=cc.MASTERS, seeds=cc.P1C_SEEDS, ladder=cc.LADDER)` (explicit, rebound to w); `N_w = max(3072, N_P1)`; `write_sealed` → `world_dir/SEALED_VALIDATION.json`; registry risk at N_w; UNDERPOWERED before any test draw |

A non-PASS gate → `terminal_result` (with `p1_passed` False unless P1 PASS).

### 11.6 REG2 job (once, after the release barrier inputs exist)

`release_barrier(STORE)["ok"]`; `extra` = every world's `stages/S3/HIST_{lgate,cal,val}_b0.npz` tables drawn so far (failed worlds included); `m = hwsg_registry.build("K-REG2", STORE/"registry", extra=…)`. The coordinator then writes `RELEASE_B.json` per E2-eligible world (N_w, k_w, `kreg2_sha256`, reservation, session, seeds, certificate). Terminal worlds need none.

### 11.7 E2-w job (release B)

1. `RELEASE_B`: `k4b_fresh.require_release_b(world_dir, release_path, session)` + `release_barrier` holds.
2. `H1G_E2`: gate 1 again (no sampling).
3. S7 sampling: `k4b_fresh.sample_test(world_dir, proc, rel, reservation_path)` (bound streams; `HIST_test_b<b>.npz`), after `hwsg_registry.recheck`.
4. `H2-FRESH` (`hwsc_data.h2_fresh_c`), `T-PRE` (`k4b_fresh.t_pre`), `ENDPOINT` (`k4b_fresh.endpoint_gate`: one joint bootstrap with the world's endpoint seed, L− rank 84, U+ rank 4,917, F = max(B_num, 1e-9) + Z_bound(w); `model_status`/`overall`).
5. `RATIO`: `hwsg_ratio.ratio_gate(ctx, ctx["result"], b4_pass, W.seeds["endpoint"])`.
6. `OUTCOME`: `hwsc_outcome.annotations`, `outcome`; `export_g`.

### 11.8 CROSS job — §8 `run_cross`.

## 12. Outcomes per world and annotations (§7.2)

`hwsc_outcome.outcome(state)` and `state_from_gates` are reused with the HWSG reason sets: precedence CONTRACT `outcomes.precedence`; O-stage statuses (`FAIL_TECHNICAL/IDENTITY`, `/LAW_BOUND`, `/ORACLE`, `INCONCLUSIVE/REGISTRY_RISK`, `/ORACLE_FEASIBILITY`) and TRAIN statuses (`FAIL_TECHNICAL/TRAINING`, `/RESOURCE`) enter as `fail` or `k4b`-row equivalents: `hwsg_records.outcome_g(state)` = `hwsc_outcome.outcome` after mapping `INCONCLUSIVE/REGISTRY_RISK`, `/ORACLE_FEASIBILITY`, `/REGISTRY_INCOMPLETE` to rank 3 (returned unchanged, ahead of NOT_LEARNED). Annotations: `POSITIVE_BELOW_MARGIN_<j>` with kind EXCLUDE ("positive, certified below the margin") or UNRESOLVED ("positive, not resolved against the margin"); world-level when all three are positive and the world is not SUPPORT; `NEGATIVE_ALIGNMENT`, `INIT_UNAVAILABLE`, `FRESH_B4_LOW` as stage C. Exactly 0 is not positive; `math.nextafter(0, 1)` above F is.

## 13. Licences (§7.4) and disclosure (§7.5)

World SUPPORT and EXCLUSION use CONTRACT `licences.SUPPORT`/`EXCLUSION` with `{world}`, `{N}`; other heads the stage-C templates. Cross readings use `licences.GENERAL`, `NOT_GENERAL` (+ error statement), `GENERAL_UNAVAILABLE`, `CAPTURE_AT_LEAST_HALF`, `SIMILARITY`. Every report carries `DISCLOSURE` and `does_not_establish` (items 1–26).

## 14. Records and schemas

- **WORLD_HANDOFF.json**: §3. **O_RECORD.json**: `{"selection", "worlds": {tag: {"gates": {O1..O5: {status, value, reference, tolerance}}, "status", "process_identities", "law", "p_D2a", "repro"}}, "protocol_sha256"}`.
- **KG_RECORD.json**: `{"status", "kg": {"KG0".."KG8": {status, value, reference, tolerance}}, "binding_audit", "registry_rehearsal", "threads", "torch", "protocol_sha256", "freeze_sha256"}`.
- **TRAIN_RECORD.json** (per master): stage-C schema with `world` added. **CHILD_<master>_a<k>.json**: §5.
- **RELEASE_A/B.json** per world: K4b fields + stage-C fields + CONTRACT `records.RELEASE_B_extra`; `protocol_sha256` HWSG; `reservation` the world's id.
- **RESERVATION_W2.json** per world: `k4b_release.start_reservation(world_dir/"RESERVATION_W2.json", f"HWSG-{TAG}-W2", utc)`, from the TRAIN job through the last test block; must survive a pre-draw interruption (DRG12).
- **VALIDATION_REPORT.json**, **SEALED_VALIDATION.json**, **RESULT.json**, **SEALED_OPENED.json**: stage-C schemas per world; RESULT carries `world`.
- **TERMINAL RESULT.json**: CONTRACT `records.TERMINAL_RESULT`.
- **RATIO.json / RATIO_DRAWS.npz**: §7. **CROSS.json**: §8.
- **Study ledger** `agent-handoff/HWSG_CPU_LEDGER.json`: `{"study": "hwsg-v1", "entries": [{"label", "job", "stage", "world", "master", "cpu_s", "source", "utc"}], "cumulative_cpu_s"}`; labels `<job>-<stage>[-<tag>][-<master>]-a<k>`.
- **Store layout**: CONTRACT `store_layout`.

## 15. Budget and runaway safeguards (§10.2–§10.4)

No pause lines. Meter per job: `--max-cpu` = 5 × central (CONTRACT `cpu.central_s`; TRAIN child: the per-model hold 6,006.6282 s), `--max-wall` = 4 × central wall (TO_FREEZE). Per-model hold (stage C): hold iff `(step ≥ 1000 and cpu·5000/step > 6006.6282)` or `cpu > 6006.6282` → `FAIL_TECHNICAL/RESOURCE` for that model (report step, CPU, projection only). Output caps: 16 GiB per world dir, 20 GiB for `registry/`. Disk safe-STOP C: < 2 GB or X: < 30 GB; native operation wall 600 s. Memory caps CONTRACT `resources.memory_cap_bytes` (TRAIN child 8 GiB, others 12 GiB); aggregate RAM check before three children (OPEN-10). Extension rules X-1…X-4: N_w raise-only at P1; ≤ 2 corrections per defect; PASS stages immutable; superseded archive + SHA256SUMS; bit-identical regeneration. CPU reported to the owner after each stage; no approval step.

## 16. Reuse table (§11.2) and TO_FREEZE rows

| Part | Reused (unchanged) | HWSG addition | Regression checks |
|---|---|---|---|
| `tools/hws` | `hws_worlds.build_process`, `hws_oracle.world_look`, `hws_exact.p_d2a`, `law_bound_report`, `hws_driver.seed_search` (via `hwsc_known.seed_search_c`) | `hwsg_oracle.reproduce`, `selection` | O4; KG5 |
| `tools/hwsb` | `hwsb_train.train`, `HoldRule`, `set_threads`; `hwsb_data.build_process`, `spec_checksums`, `arrays_sha256`; `hwsb_law.law_bound`; `hwsb_eval`; `hwsb_registry.registry_digests`, `history_inventory`; `hwsb_gates.ladder_pilot`; `hwsb_known.kb2_kb3`, `w0_process`; `hwsb_kb.kb5` formulas | explicit kwargs + rebinding; σ/neighbour override | KG1, KG3, KG5, DRG3, DRG8 |
| `tools/hwsc` | `hwsc_bind.load_table`, `check_old`, `bound_stage_c`, `audit`; `hwsc_data.make_train_dev_c`, `sample_block_c`, `h2c`, `h2_fresh_c`, `separation_c`, `p_d2a_check`, `registry_risk`; `hwsc_gates.h1c`, `l1`, `p1c`, `law_identity`, `choose_N`; `hwsc_outcome.*`; `hwsc_records.*`; `hwsc_registry.*`, `hwsc_registry_build.build`/`_default_sources`; `hwsc_known.g0c`, `seed_search_c` | HWSG adapters only; no HWSC edit | KG1, KG6, DRG1, DRG3 |
| `tools/k4b` | estimand, chart, scores, certificate, `joint_bootstrap`, `bounds`, `model_status`, `overall`, `k4b_fresh.endpoint`/`bootstrap_inputs`/`sample_test`/`t_pre`, `k4b_driver` stage functions, `k4b_release` | `hwsg_ratio` re-running `joint_bootstrap` | KG6, KG7 |
| `tools/c2_*` | `c2_registry.Registry`, `nd_registry` sources | `hwsg_registry` obligation/hwsc sources | DRG9, KG8 |
| `src/topo_pilot` | world/process, sampler, SeedTree, learner, artifacts | none | PF suites |
| meter / records | `hwsc_meter_bind` pattern, `stage_records` | attempt-specific child records, coordinator aggregation | DRG12, DRG13 |

Each adapter that mirrors existing code says why direct reuse is unsafe and has an equivalence test on synthetic input: `build_process_g` (captured defaults, float-repr neighbour), `source_obligation` (no existing obligation reader), `export_g` (ratio files in the same S8 event).

**TO_FREEZE (filled by read-only listing / header scan before the execution freeze; contract erratum):**
- the final track-U phase-2 obligation and the hwsd obligation (path, sha256) (OPEN-3);
- one row per top-level scratch directory modified since 2026-10-29 (80 at job 0224: `hwsc-dry-0177…0194` (9), `hwsc-job-0181…0196` (10), `hwsd-dry`, `hwsd-dry-0203…0218` (6), `hwsd-run-0209…0222` (9), `hwsu-dry-of-0198…0205` (5), `hwsu-run-0200`, `hwsu-run-0206`, `paper`, `paper-edit`, `test_hwsc-*` (15), `test_hwsd-*` (14), `test_hwsg-0224`, `test_hwsu-*` (6)) with decision and `frozen_files` (array headers only);
- worktree rows `topo-pilot-hwsu`, `topo-pilot-hwsd`, `topo-pilot-hwsg`; the `hwsc-job-*`, `hwsu-run-*`, `hwsd-run-*`, `paper*` decisions;
- `binding.audit.left_unchanged` (static scan of the implementation); `law.w0.Z_bound_ref`; addenda 25/26/37 sha256; `cpu.central_wall_s`; `h_exec`, FREEZE, DRY_REPORT and PF record sha256.

## 17. OPEN points (reading chosen closest to the design text; for coordinator ruling)

- **OPEN-1 (streams, §2.4).** The design writes train/dev `("data", "hwsg-v1", KEY_w, role, m)` and blocks `("data", "hwsg-v1", KEY_w, role, b)`, and also requires reusing `k4b_data`/`k4b_fresh.sample_test` and `hwsc_data.make_train_dev_c` unchanged (§4, §11.2). Reused code fixes the tuple order: chosen tuples are train/dev `("data", "hwsg-v1", split, KEY_w, m)` and blocks `("data", "hwsg-v1/<KEY_w>", split, b, *PROC_w)`; the block sequence-ID string is exactly the design's `hwsg-v1/{KEY_w}/{role}/b{b}` with `PROC_w`. Both carry the full world key (G4). Alternative: HWSG mirrors of the samplers with the literal tuple (mirrors of reused real-run code).
- **OPEN-2 (O4).** "Regenerate … require its history sha256 = recorded hist_sha256" cannot hold by re-saving (npz zip timestamps differ). Chosen: hash the stored stage-A table (KB5 pattern), require its `canon32` = regenerated tokens bitwise, and means within 1e-12 of the S3 record's `bounds.<q>.mean` (REPORT.json `s3.<key>` holds only L3, not means).
- **OPEN-3 (latest obligation).** hwsd-store holds an unsuffixed `REGISTRY_OBLIGATION.json` (job 0215, 18 entries) and later attempt files (0222-a1, 162 entries). "Latest" = greatest `written_utc`, frozen by path and sha256 before REG1.
- **OPEN-4 (stage-C exclusions).** "The 6 stage-C checkpoint ids" read as steps 0 and 5000 of the three stage-C masters (TRAIN_RECORD `checkpoint_ids`); stage C wrote 36 checkpoints.
- **OPEN-5 (audit).** World mid shares p = 1/5 (and neighbour 1/5) with w\*; these values are not hits for mid; σ-specific and seed/path values remain forbidden.
- **OPEN-6 (dry seeds).** The dry run uses 620901–620915 only; DRG10's spread pairing uses 620640 on synthetic draws (no stream, no history), as HWSC R-0176-G5 allowed for P1 seeds.
- **OPEN-7 (capture order).** CAPTURE_BELOW_HALF is checked before CAPTURE_AT_LEAST_HALF (they cannot both hold when every ratio is DEFINED; with some unresolved models BELOW_HALF wins).
- **OPEN-8 (spread pairing).** "Index-paired draws; seed 620640 orders the pairing" read as one PCG64(620640) generator giving one permutation of 5,000 per endpoint world in `worlds_order`.
- **OPEN-9 (blindness vs registry listing).** Readers list blinded directories by name (needed for listing/obligation equality) but open no file in them.
- **OPEN-10 (aggregate RAM).** Threshold `3 × 1.5 GiB + 4 GiB` free; the design gives no number.
- **OPEN-11 (non-positive D draws).** A draw with D\* ≤ 0 makes ρ\* undefined; the world's ratios become RATIO_UNRESOLVED.
- **OPEN-12 (CROSS inputs).** CROSS re-derives readings from the endpoint's ratio draws persisted at E2 (`RATIO_DRAWS.npz`, hash-bound in the S8 event), not by recomputing scores.
- **OPEN-13 (O5 threshold).** O5 checks `at_3x` and also `L3.D4 ≥ 3M` explicitly.
- **OPEN-14 (KG1).** KG1 builds a w\* `WorldDef` and compares the row values rather than entering `world(W_STAR)` (w\* is not a registered world).

## 18. Erratum E1 (R-0224-1, R-0224-2)

process_code takes (family, mode, sigma, replicate). For six fields (family, mode, sigma_str, p_str, KEY_w, rep) hwsg_bind.process_code_g returns process_code(family, mode, f'{sigma_str}|{p_str}|{KEY_w}', rep); four fields pass through unchanged. Rebound inside world() in hwsb_data, hwsc_data and k4b_data (not CONTRACT rows; restored in finally). Sequence ids = make_sequence_ids(code, split, n) with split 'test' for blocks. Worked examples, rep = 'hwsg-v1/<KEY_w>/cal/b0': lo sigma field '1.25|0.8333333333333334|W12-q1-s1.25-p0.8333333333333334' code 896598705; mid '2.0|0.2|W12-q1-s2.0-p0.2' code 729926672; hi '2.5|0.5|W12-q1-s2.5-p0.5' code 761818423. Train/dev: rep 'hwsg-v1/<role>/<master>'. ACCEPT_TERMINAL.json binds the TERMINAL RESULT sha256 in field terminal_result_sha256 (also accepted: result_sha256, sha256); ACCEPT_VALIDATION.json binds VALIDATION_REPORT.json in validation_report_sha256 (also sha256); an optional verdict 'REJECT' refuses. release_barrier also returns release_b_missing (E1-accepted worlds without RELEASE_B.json).

## 19. Erratum E2 (TO_FREEZE fill; ruling R-0238-1, coordinator be2e199d, 2026-11-04)

CONTRACT `errata.E2` lists the filled rows (evidence: `coord-scratch/be2e199d/hwsg_tofreeze/`, job 0238). Rulings:
- **R1 (w0 reference):** as in CONTRACT `errata.E2`: `hwsb_known.w0_process` with definition-time defaults is the intended w0 reference for KG3/KG5 (payload checksums equal stage-B KB1/KB2); never used for lo, mid or hi.
- **A:** `hwsc-dry-*` scratch folders are EXCLUSION in `source_scratch_g`; their histories enter K-REG through the `dry` source (`hwsc_registry.source_dry`), which `hwsg_registry.build` already uses.
- **B:** `tests/hwsg/test_b_registry.py::test_scratch_to_freeze_row_is_incomplete` now uses a name with no row or rule (`hwsc-job-*` is frozen as EXCLUSION); the fail-closed property tested is unchanged.
- **C:** `registry.obligation_stores.*.obligation` records path and sha256; the run-time reader keeps the "greatest written_utc" rule (OPEN-3), which selects the same files while no hwsu/hwsd job runs. The coordinator checks both sha256 before REG1 and REG2. The hwsu row's `contract` field names the phase-1 contract, whose obligation format phase 2 reuses (API_U2 §5.3).
- **D:** `source_scratch_g` matches rows by name and decision only (as track U phase 2).
- **E:** the `test_hwsc-*` / `test_hwsg-*` reason texts are corrected; the decision (EXCLUSION) is unchanged.
- **F:** `binding.audit.left_unchanged` lists only names hit by the HWSG scan (48 rows); stage-C rows without a hit are not copied, so a new hit fails closed.
- **G:** KG3 runs `kb2_kb3` twice; cost only, no change.
- **Deferred:** `authority.h_exec`, FREEZE, DRY report and PF record sha256 are fixed by `freeze_g` after the PF + DRY rerun.

## 20. Erratum E3 (ruling R-0239-2, coordinator be2e199d, 2026-11-04)

KC attempt 1 (job 0239) stopped at KG6 `FAIL_TECHNICAL/KNOWN_CASE`: run inside `hwsg_bind.world("hi")`, the reused `tests/k4b` and `tests/hwsc` suites fail their own binding guard (`k4b_config` code drift; `MODELS` = the hi masters), 1 failed, 59 errors, 70 passed. Correction (first of at most two for this defect): `kg6(job)` runs CONTRACT `known_cases.kg6_suites` unbound and the new CONTRACT `known_cases.kg6_port_suites` (`tests/hwsg/test_a_kg6_port.py`, author A's port, which enters `world("hi")` with `bound_stage_c` itself and checks restoration); PASS iff both return 0. Basetemp `test_hwsg-<job>/test_hwsc-kg6/pytest-<i>` (R-0199-1 component). `returncode` is now the list of both codes. No other function changes; new freeze cycle before KC attempt 2.

## 21. Erratum E4 (ruling R-0241-1, coordinator be2e199d, 2026-11-04)

KC attempt 2 (job 0241) passed KG0–KG7 and stopped at KG8 `FAIL_TECHNICAL/KNOWN_CASE`: the rehearsal registry was INCOMPLETE because reader (b) `source_hwsc` left 91 hwsc-store array files unassigned. Cause (CONTRACT data, no code change): `registry.hwsc_store.non_history_by_name` held the brace glob `artifacts/{WorldSpec,TransitionSpec,EmissionSpec,Checkpoint}/**`, which `_glob_re` (fnmatch-style, no braces) never matches; two further non-history groups had no row: the specs of stage C's archived KC attempt (`superseded/0184-a1/artifacts/...`) and the digest files of the killed REG2 attempt (`logs/superseded-reg2-0192a1/**`, registry outputs like `registry/**`). Correction (first for this defect): the brace glob is expanded into four rows and three rows are added (`superseded/*/artifacts/{WorldSpec,TransitionSpec,EmissionSpec}/**`, `logs/superseded-reg2-*/**`, each written out). Checked before the re-freeze: readers hwsc/hwsu/hwsd/scratch_g all PASS, and a full `hwsg_registry.build("REHEARSAL", ...)` into scratch PASS (8,421,234 digests, no problems).

# tools/hwsd: written contract (job 0197 phase 1; derived from HWSD-DESIGN-v1)

**Authority.** `tools/hwsd/PROTOCOL_HWSD_v1.md` is a byte copy of `agent-handoff/planning/responses/HWSD-DESIGN-v1.md` (sha256 `938cebd599d2256b1ba4bb7d58c62a62c495d30b46cfb70c45215cca9b197775`; it becomes HWSD-FROZEN-v1 at the execution freeze). Owner addendum 37 authorises planning up to an execution freeze. **Running track D is not approved.** Owner questions Q1–Q6 (§14 of the protocol) are pending; this contract uses their registered defaults. Section marks (§n), D-C, RC, F, J, S, KD and DRD items refer to the protocol.

**Precedence.** Protocol > `CONTRACT.json` > this file > `TEST_PLAN.md`. A difference is a contract defect, reported through the coordinator. It is never resolved in code or in a test.
- `CONTRACT.json` holds the machine-readable values. Exact values are strings for `fractions.Fraction`.
- This file fixes, so that two independent test authors can write tests from it alone:
  - every module, name, signature, input, output, error and exact behaviour;
  - the binding, the registry composition, the record schemas and the store layout;
  - every gate's computation, pass reading, tolerance and failure action, in order;
  - the per-checkpoint statuses, onsets, ORDER rules and statements D1–D6;
  - the budget, the meter binding and the dry-run checks.
- Where the protocol leaves a detail open, §20 "Implementation decisions" fixes it (cited as "decision n"). Each is open to a coordinator ruling. §21 lists the TO_FREEZE items.

**Nothing here authorises a run.** No checkpoint is opened, no real-scope history is sampled, no metered run happens and no store is written because of this contract.

## 0. Conventions

- **Fifteen modules** under `tools/hwsd/`, each `.py` at most 400 lines (`tools/check_file_sizes.py`):

  | Module | Holds |
  |---|---|
  | `hwsd_config` | constants, paths, CONTRACT loader, effective registry tables, TRAIN whitelist reader, OBS_INVENTORY reader, blindness guard, dry plans |
  | `hwsd_bind` | the hwsd binding table on `hwsc_bind.bound_stage_c(table=…)`, the dry and identity tables, the audit |
  | `hwsd_data` | blocks and tables, H2-D separation, registry risk, ORACLE-D, reference persistence, B4-TEST, LGATE-ORACLE, shared controls, obligations, reservations, `end_reservation`, W2 attestation |
  | `hwsd_readers` | R9 (`hwsc-store` layout reader), R10 (obligation reader), the K4b table reader, the superset check |
  | `hwsd_registry` | `build_d`, the scratch scan and check mirrors, the hwsd-dry type rule, `inventory_d`, the wrapper record, `load_d` |
  | `hwsd_score` | the per-checkpoint scorer: learning, `chart_one`, `arrays_one`, `controls_one`, statuses, determinism, acceptance record |
  | `hwsd_statements` | pure statement logic: notation, onsets, ORDER, D1–D6, diagnostics |
  | `hwsd_summary` | SUMMARY: bootstraps, bounds, F, the 36-row table, outcome, report |
  | `hwsd_known` | G0d and `seed_search_d`, KD1, KD2, KD3 `repro_c`, KD5, KD6, `run_kd` |
  | `hwsd_records` | lineage, AUTH/SCHED, FREEZE, S0, preflight, budget and pauses, ledger, H-1 checks, archive |
  | `hwsd_driver` | the jobs KD, SAMPLE, SCORE, SUMMARY, CLOSE and the CLI |
  | `hwsd_dry`, `hwsd_dry2`, `hwsd_dry3` | DRD1–DRD7 and `seq_cases`; DRD8–DRD11; DRD12–DRD14 |
  | `hwsd_meter_bind` | the meter binding (hwsd caps and paths) |

  A further split by size is an API erratum. It keeps every name reachable as `<documented module>.<name>` (re-export).
- **No existing file is edited.** The binding is versioned (§2); stage-C and K4b functions are reused unchanged or mirrored here. No `.npz`/`.npy` is committed under `tools/hwsd` or `tests/hwsd`.
- **Import convention.** Every module imports `hwsd_config` first (`from __future__ import annotations  # noqa: I001`). `hwsd_config` sets `HERE = Path(__file__).resolve().parent` and `REPO = HERE.parents[1]`, inserts `str(REPO/"tools"/"hwsc")` and then `str(HERE)` at `sys.path[0]` if absent, then imports `hwsc_config` (which puts the reused tool folders on `sys.path`, as hwsc API §0). Import reads only CONTRACT.json files (hwsd's, and through `hwsc_config` stage C's, stage B's, K4b's and C1′'s) and computes constants. It never opens HANDOFF.json or a store file.
- **Dependency order** (no import-time cycle): `hwsd_config` ← `hwsd_bind` ← `hwsd_data` ← `hwsd_readers` ← `hwsd_registry` ← `hwsd_score` ← `hwsd_statements` ← `hwsd_summary` ← `hwsd_records` ← `hwsd_known` ← `hwsd_driver` ← `hwsd_dry`, `hwsd_dry2`, `hwsd_dry3`. `hwsd_known.run_kd` imports `hwsd_driver` and `hwsd_dry` lazily inside the function. `hwsd_meter_bind` imports only `hwsd_config` and the meter modules.
- **Call-time lookups.** hwsd code calls every reused function and reads every reused constant through its module attribute at call time (`k4b_data.SCOPE`, `hwsb_eval.b1(...)`), never through a `from … import` copy. So the binding applies, and tests may monkeypatch a reused function. hwsd modules other than `hwsd_config` hold no module-level reference to a CONTRACT dict.
- **Test import aliases:** `import hwsd_config as dc`, `hwsd_bind as db`, `hwsd_data as dd`, `hwsd_readers as drd`, `hwsd_registry as dr`, `hwsd_score as ds`, `hwsd_statements as dst`, `hwsd_summary as dsum`, `hwsd_known as dk`, `hwsd_records as drec`, `hwsd_driver as ddr`, `hwsd_dry as ddry`, `hwsd_dry2 as ddry2`, `hwsd_dry3 as ddry3`, `hwsd_meter_bind as dm`.
- **Run** with `X:/Downloads/projects/topo-pilot/topo-pilot/.venv/Scripts/python.exe -s` and `PYTHONPATH=<worktree>/src`. One torch thread.
- **Keys.**
  - Masters are ints (620301, 620302, 620303; dry 629951–629953), iterated in `MASTERS` order.
  - Steps are ints from `STEPS = (0, 50, 100, 200, 400, 700, 1000, 1500, 2000, 3000, 4000, 5000)`.
  - The checkpoint index is `k = 1 + STEPS.index(step)` (k = 1 is step 0, k = 12 is step 5000).
  - A checkpoint key is the tuple `(j, step)` in Python and the string `f"{j}:{step}"` in JSON.
- **Numbers.** Exact quantities (M, α, F, Z_bound, B_num, risk products) are `Fraction`s; JSON writes `str(Fraction)`. A float bound enters exact arithmetic as `Fraction(float(x))` (the `k4b_stats._fr` rule). Means are `c1_means.tree_mean`.
- **Statuses** are full strings: `PASS`, `FAIL`, `NOT_RUN`, `PAUSE`, `INCONCLUSIVE/<REASON>`, `FAIL_TECHNICAL/<REASON>`, and the per-checkpoint statuses of §16. hwsd code raises **`c1_records.C1GateFailure(status, reason)`**. `hwsc_records.status_of` maps every exception to a status (reused unchanged).
- **Writes** go only inside the directory passed as `out` (or an explicit path argument), by exclusive create (`stage_records.write_new`, `stage_records.save_npz`). The exceptions are: `GATES.jsonl` (`stage_records.record_gate`); `STAGES.jsonl` (`k4b_driver.begin_stage`/`complete_stage`); per-checkpoint construction ledgers (`c1_chart.ConstructionLedger`); the study ledger (atomic replace); the registry run folders; `logs/`; the op_guard marker and log.
- **Footprint.** Implementation, tests and the dry run write no array file and no ArtifactStore artifact anywhere under `X:/Downloads/projects/topo-pilot/`. Tests use pytest `tmp_path` with `--basetemp X:/Downloads/topo-scratch/test_hwsd-<job>/pytest`, and TEMP/TMP/TMPDIR under `X:/Downloads/topo-scratch/test_hwsd-<job>/`. The dry store is `X:/Downloads/topo-scratch/hwsd-dry/` (or `hwsd-dry-<job>/`); no file there is named `HIST_*.npz`.
- **Blindness.** hwsd code opens no path for which `hwsd_config.blinded(path)` or `public_summary(path)` holds (§1.4). Every direct file read of hwsd code goes through `hwsd_config.guard`, `read_json` or `read_bytes`. The two exempt readers are `read_train_record` and `read_obs_inventory`. Registry readers read store payloads only as §4 states.
- **No foreign payload access** beyond:
  - the registry readers of §4 and §5;
  - the read-only Checkpoint loads of the 36 rows (SCORE) and of the six step-0/5000 rows (KD3);
  - the KD3 stage-C files listed in CONTRACT `known_cases.KD3.reads`.

  Never a `state.pt` opened by a reader, never a `sealed/` path, never a Checkpoint payload hashed by a reader.
- **Binding.** Every job (KD, SAMPLE, SCORE, SUMMARY) runs its gates inside one `hwsd_bind.bound_hwsd()` for the whole job. KD2 and KD3 run under `hwsc_bind.suspended()` (the D-0184-1 lesson); KD3 then enters `hwsc_bind.bound_stage_c()` itself.

## 1. `hwsd_config.py`: constants, contract, readers, blindness guard

### 1.1 Constants and paths

| Name | Value / contract |
|---|---|
| `HERE`, `REPO`, `CONTRACT_PATH`, `PROTOCOL_PATH`, `API_PATH`, `TEST_PLAN_PATH` | `HERE/"CONTRACT.json"`, `HERE/"PROTOCOL_HWSD_v1.md"`, `HERE/"API.md"`, `HERE/"TEST_PLAN.md"` |
| `ROOT`, `SCRATCH`, `STORE`, `DRY_STORE`, `HWSC_STORE`, `HWSU_STORE`, `MAILBOX`, `STUDY_LEDGER`, `HANDOFF_PATH` | `Path("X:/Downloads/projects/topo-pilot")`, `Path("X:/Downloads/topo-scratch")`, `ROOT/"hwsd-store"`, `SCRATCH/"hwsd-dry"`, `ROOT/"hwsc-store"`, `ROOT/"hwsu-store"`, `ROOT/"agent-handoff"`, `MAILBOX/"HWSD_CPU_LEDGER.json"`, `ROOT/"hwsb-store"/"HANDOFF.json"`. Defaults only; every function that touches a store or ledger takes it explicitly |
| `load_contract(path=CONTRACT_PATH) -> dict`; `CONTRACT` | `json.loads` of the UTF-8 file, loaded at import |
| `PROTOCOL_SHA256` | CONTRACT `protocol_sha256` |
| `SCOPE`, `DRY_SCOPE`, `KEY`, `PROCESS`, `TINY_PROCESS` | `"hwsd-v1"`, `"hwsd-dry-v1"`, `"W12-q1-s1.75-p0.2"`, `("cylinder", "overlap", "1.75")`, `("cylinder", "overlap", "1.0")` |
| `MASTERS`, `DRY_MASTERS`, `STEPS`, `K_OF` | `(620301, 620302, 620303)`, `(629951, 629952, 629953)`, the 12 steps, `{step: 1 + i}` |
| `SEEDS`, `STRONG_SEED`, `DRY_SEEDS`, `DRY_STRONG_SEED` | CONTRACT `seeds.k4b_seed_names` (620411–620415), `620416`, `seeds.dry_seed_names` (629961–629965), `629965` (decision 14) |
| `NEEDLES` | the 16 strings of CONTRACT `seeds.g0_needles` |
| `SPLITS`, `SIZES`, `N`, `PANEL`, `LGATE_N` | `("lgate", "cal", "val", "test")`, `{"lgate": 4096, "cal": 3072, "val": 3072, "test": 3072}`, `3072`, `512`, `4096` |
| `DRAWS`, `STRONG_DRAWS`, `RANKS`, `STRONG_RANKS` | `5000`, `50000`, CONTRACT `thresholds.ranks`, `{"lo": 70, "hi": 49931}` |
| `M`, `ALPHA`, `LEARN`, `CAP`, `FLOOR`, `P_LO`, `P_HI`, `F_PLANTED` | `Fraction(1, 100)`, `Fraction(1, 60)`, `Fraction(4, 5)`, `Fraction(1, 10**4)`, `Fraction(1, 10**9)`, `Fraction(1, 720)`, `Fraction(719, 720)`, `Fraction(1, 10**9)` |
| `Z`, `Z_S` | `NormalDist().inv_cdf(1 - 0.05/4)`, `NormalDist().inv_cdf(1 - 1/720)` (floats) |
| `DISCLOSURE` | CONTRACT `disclosure` (= protocol §8.4) |
| `CHECKPOINTS` | `{(j, step): row}` from CONTRACT `checkpoints.rows` (36 rows `{"master", "step", "k", "id", "payload_sha256"}`) |
| `TRAIN_WHITELIST` | `("status", "run_key", "checkpoint_ids", "checksums", "process_ids")` |
| `RESERVATION_PREFIX` | `"RES-HWSD-W2-a"` |

**Import checks** (any mismatch → `C1GateFailure("FAIL_TECHNICAL/BINDING", …)`):
- `M == k4b_config.MARGIN`, `ALPHA == k4b_config.ALPHA`, `CAP == k4b_config.CAP`, `FLOOR == k4b_config.FLOOR`;
- `{k: RANKS[k] for k in ("alpha", "one_minus_alpha", "central_lo", "central_hi", "b4_lower")} == k4b_config.RANKS`; `DRAWS == k4b_config.DRAWS`; `PANEL == k4b_config.PANEL`; `N == k4b_config.BLOCK`;
- `c1_means.rank_for(P_LO, STRONG_DRAWS) == 70` and `c1_means.rank_for(P_HI, STRONG_DRAWS) == 49931`;
- `Z == hwsb_config.Z_B23` (float `==`);
- `len(CHECKPOINTS) == 36` and the keys are exactly `MASTERS × STEPS`;
- `CONTRACT["disclosure"] == CONTRACT["k4b_contract_view"]["authority"]["c1prime_disclosure"]`.

### 1.2 Effective registry tables (decision 3)

| Name | Contract |
|---|---|
| `inherited_sha_ok() -> bool` | `sha256(REPO/"tools"/"hwsc"/"CONTRACT.json" bytes)` equals CONTRACT `registry.scratch_inventory.inherit.sha256` (= `registry.inventory.inherit.sha256` = `identity.rows.hwsc_contract.sha256`) |
| `scratch_table() -> dict` | `inherited_sha_ok()` False → `C1GateFailure("FAIL_TECHNICAL/IDENTITY", …)`. Else a new dict: `copy.deepcopy(hwsc_config.CONTRACT["registry"]["scratch_inventory"])`, then `.update(CONTRACT registry.scratch_inventory.rows)`, then `.update(CONTRACT registry.scratch_inventory.pattern_rows)`. 181 + 10 + 6 = 197 keys |
| `root_table() -> dict` | the same sha check; `copy.deepcopy(hwsc_config.CONTRACT["registry"]["inventory"])` updated by CONTRACT `registry.inventory.rows` (68 inherited + 5 new = 73 keys: `hwsc-store` replaced by READER R9; new `hwsd-store` OWN, `hwsu-store` READER_IF_PRESENT R10 and the three TO_FREEZE worktree rows) |

### 1.3 Plans

| Name | Contract |
|---|---|
| `dry_plan(kind, case) -> hwsb_config.Plan` | `kind` ∈ {`"dry_tiny"`, `"dry_e4"`}, else `ValueError`. `base = hwsb_config.dry_plan(kind, case)`. `dry_tiny`: `dataclasses.replace(base, masters=DRY_MASTERS, sizes={"train": 4096, "dev": 512}, train_cfg=dataclasses.replace(base.train_cfg, checkpoint_steps=[0, 50, 100, 200]))`. `dry_e4`: `dataclasses.replace(base, masters=DRY_MASTERS[:1], sizes={"train": 2048, "dev": 256}, train_cfg=dataclasses.replace(base.train_cfg, steps=20, checkpoint_steps=[0, 20]))` |

### 1.4 Blindness guard (§9.2; DRD9, DRD13)

Paths are compared as `Path(p).resolve().as_posix().lower()` with the trailing `/` stripped. "Under `d`" means equal to `d` or starting with `d + "/"`. All functions here are pure (no file access).

| Name | Contract |
|---|---|
| `blinded(path, root=ROOT, scratch=SCRATCH) -> bool` | True iff any of: (1) `hwsc_config.blinded(path, root)` (the five stage-B rules); (2) under `<root>/hwsc-store/stages/train`; (3) under `<root>/hwsc-store/logs`; (4) equal to `<root>/hwsc-store/stages/e1/l1.json`; (5) the first component below `<scratch>` matches `fnmatch` `hwsc-job-*` (the folder and everything under it); (6) equal to `<root>/agent-handoff/jobs/0187/review.md`, `…/0188/review.md` or `…/0189/review.md`; (7) under `<root>/agent-handoff/planning/` and some component below `planning` contains `coord-hws-use-20261101` or starts with `hwsu-` |
| `search_pruned(path, root=ROOT, scratch=SCRATCH) -> bool` | `blinded(path, root, scratch)`, or `path` is under `<root>/hwsu-store` and is not a searchable path. The searchable paths are: the store folder itself; the folder `<root>/hwsu-store/reservations`; a file directly in the store whose name matches `registry_obligation*.json` or `reservation*.json`; a file directly in `reservations/` whose name ends with `.json` (J9) |
| `public_summary(path) -> bool` | `hwsc_config.public_summary(path)` |
| `guard(path, root=ROOT) -> Path` | `blinded(path, root)` or `public_summary(path)` → `C1GateFailure("FAIL_TECHNICAL/BLINDNESS", str(path))` before any open; else `Path(path)` |
| `read_bytes(path, root=ROOT) -> bytes`, `read_json(path, root=ROOT)` | through `guard` |

### 1.5 The two exempt readers (§3.2, J1; DRD9)

| Name | Contract |
|---|---|
| `read_train_record(master, store=HWSC_STORE) -> tuple` | The path is exactly `store/"stages"/"TRAIN"/str(int(master))/"TRAIN_RECORD.json"`. It reads the bytes directly (exempt from `guard`), sets `sha = sha256(bytes)`, parses JSON, and builds `rec = {k: obj[k] for k in TRAIN_WHITELIST}`; then `del obj`. A missing key or a non-object → `C1GateFailure("FAIL_TECHNICAL/IDENTITY", "TRAIN record <master>: <missing keys>")`. No other key or value is returned, logged, printed or written. Returns `(sha, rec)` |
| `read_obs_inventory(store=HWSC_STORE, expected_sha256=None) -> dict` | The path is exactly `store/"stages"/"TRAIN"/"OBS_INVENTORY.json"`. `expected_sha256` defaults to CONTRACT `identity.rows.obs_inventory.sha256`. sha256 of the bytes ≠ expected → `C1GateFailure("FAIL_TECHNICAL/IDENTITY", …)` before parsing. The parsed object must be a flat dict `{str: 64-lower-hex str}`, else `FAIL_TECHNICAL/IDENTITY`. Returns that dict (51 entries for the real file) |

## 2. `hwsd_bind.py`: the versioned binding (§3.3; KD2, DRD3)

| Name | Contract |
|---|---|
| `decode(value, repo=REPO)` | `hwsc_bind.decode` semantics, except that `{"__contract_view__": key}` returns `copy.deepcopy(hwsd_config.CONTRACT[key])` and `{"__repo__": rel}` returns `repo/rel` with this worktree's `REPO` |
| `load_table(which="hwsd", case=None, case_dir=None, process=None) -> list[dict]` | Rows `{"module", "name", "old", "new"}` decoded from CONTRACT `binding.table` (18 rows, in CONTRACT order). `which="hwsd"`: as decoded. `which="identity"`: `new` = the current live attribute (`getattr(importlib.import_module(module), name)`). `which="dry"`: `case` and `case_dir` are required (`ValueError` otherwise). The rows get new values: `MODELS` → `DRY_MASTERS`; `SCOPE` (k4b_config, k4b_data, k4b_decoder) → `f"hwsd-dry-v1/{case}"`; `PROCESS` → `tuple(process or TINY_PROCESS)`; `SEEDS` → `dict(DRY_SEEDS)`; `k4b_config.STORE` → `Path(case_dir)`; `k4b_driver.ARTIFACTS` → `Path(case_dir)/"artifacts"`. Two rows are appended: `hwsb_config.SCOPE` `"hwsb-v1"` → `"hwsd-dry-v1"` and `hwsb_config.DRY_MASTERS` `(629901, 629902)` → `(629951, 629952, 629953)`. Any other `which` → `ValueError` |
| `bound_hwsd(table=None)` | Context manager: `with hwsc_bind.bound_stage_c(table if table is not None else load_table()) as info: yield info`. Hence: the old values are checked first (drift → `C1GateFailure("FAIL_TECHNICAL/BINDING", "code drift: …")`, nothing set); the attributes are set in table order; they are restored to the identical objects in `finally` (also after an exception); entering twice nested fails; `hwsc_bind.ACTIVE` is True inside |
| `scope_modules() -> list` | every module in `sys.modules` whose `__file__` resolves to a file directly in one of `REPO/d` for `d` in CONTRACT `binding.audit.module_dirs`, sorted by `__name__` |
| `audit(modules=None) -> dict` | `hwsc_bind.audit(modules if modules is not None else scope_modules(), left_unchanged=CONTRACT binding.left_unchanged, forbidden=CONTRACT binding.audit.forbidden)`. Called **inside** `bound_hwsd()`. Outside it, the table's own old values are hits and the audit fails by design. Returns the `hwsc_bind.audit` dict (`status` PASS or `FAIL_TECHNICAL/BINDING`, `hits`, `unlisted`, `modules`, `n_hits`) |
| `never_called() -> tuple` | CONTRACT `binding.never_called` |
| `strong_seed() -> int` | `k4b_config.SEEDS == SEEDS` → `STRONG_SEED` (620416); `== DRY_SEEDS` → `DRY_STRONG_SEED` (629965); else `C1GateFailure("FAIL_TECHNICAL/BINDING", "strong seed outside a binding")` |

**The hwsd table** (CONTRACT `binding.table`; old → new):
- `k4b_config.{MODELS, SCOPE, PROCESS, SEEDS, STORE, CONTRACT, CONTRACT_PATH, PROTOCOL_PATH}` → `(620301, 620302, 620303)`; `"hwsd-v1"`; `PROCESS`; `SEEDS` (620411–620415); `ROOT/hwsd-store`; the `k4b_contract_view` section of the hwsd CONTRACT; `tools/hwsd/CONTRACT.json`; `tools/hwsd/PROTOCOL_HWSD_v1.md`.
- `k4b_data.{MODELS, PROCESS, SCOPE}`, `k4b_stats.MODELS`, `k4b_driver.{MODELS, SEEDS}`, `k4b_fresh.{MODELS, SEEDS}`: as above.
- `k4b_driver.ARTIFACTS` → `ROOT/hwsc-store/artifacts` (read-only Checkpoint loads).
- `k4b_decoder.SCOPE` → `"hwsd-v1"`.

The `k4b_contract_view` holds the hwsd protocol sha256, the K4b `chart` and `registry` sections (deep-equal to `tools/k4b/CONTRACT.json`; `k4b_config.check_chart_equality()["equal"]` is True inside the binding) and `authority.c1prime_disclosure` = the hwsd disclosure.

**Left unchanged** (CONTRACT `binding.left_unchanged`): the 44 stage-C rows plus 14 hwsd rows, each with its reason. The new rows are `hwsb_config.{SCOPE, MASTERS}`, `hwsc_bind._STACK`, `hwsc_config.{CONTRACT, SCOPE, SEEDS, P1C_SEEDS, NEEDLES, HWSB_STORE}`, `hwsc_data.{sequence_ids_c, make_train_dev_c}.__defaults__`, `hwsc_records.C`, `hwsc_registry.REG` and `hwsd_config.CONTRACT`. `hwsc_config.SCOPE = "hwsc-v1"` is the run-key scope of the checkpoints and is used only for identity.

**Forbidden** (CONTRACT `binding.audit.forbidden`): the stage-C list, plus the ints 620311–620315, the string `"hwsc-v1"` and the paths `ROOT/hwsc-store/stages/S3` and `ROOT/hwsc-store/stages/S7`.

**Audit scope:** `tools/{k4b, hwsb, hws, c1prime, c1prime_registry, hwsc, hwsd}`. A read-only import scan of the 62 reused modules inside the hwsd table (job 0197 phase 1) gave PASS with 309 hits, all covered (CONTRACT `binding.audit.static_scan_2026_11_01`). hwsd modules hold no forbidden value in a global or a function default, except `hwsd_config.CONTRACT`. A new hit found once they exist is a contract erratum.

## 3. `hwsd_data.py`: blocks, H2-D, oracle, B4, controls, obligations, reservations

### 3.1 Blocks and tables (§2.5)

| Name | Contract |
|---|---|
| `block_generator(split, scope=None, process=None)` | `hwsc_data.block_generator(split, 0, scope=scope or k4b_data.SCOPE, process=process or k4b_data.PROCESS)` |
| `block_ids(split, n, scope=None, process=None) -> int64 [n]` | `hwsc_data.block_ids(split, 0, n, scope=scope or k4b_data.SCOPE, process=process or k4b_data.PROCESS)` |
| `sample_block_d(T, E, pi, split, n, scope=None, process=None) -> (canon32, ids)` | Mirror of `hwsc_data.sample_block_c` with explicit scope and process. Exactly one `HMMSampler(T, E, pi, SequenceLayout()).sample(int(n), block_generator(split, scope, process))`; `canon32 = np.asarray(tokens[:, :32], dtype=np.uint8)`; `del tokens, states` at once; `ids = block_ids(split, n, scope, process)`; rows ordered by `np.argsort(ids, kind="stable")`; both returned contiguous. With `scope=k4b_data.SCOPE` and `process=k4b_data.PROCESS` it equals `hwsc_data.sample_block_c(T, E, pi, split, 0, n)` bitwise |
| `hist_name(split, dry=False) -> str` | `f"HIST_{split}_b0.npz"`, or `f"DRYHIST_{split}_b0.npz"` when `dry` |
| `sample_tables(proc, scope=None, process=None, sizes=None) -> dict` | For split in `SPLITS` order: `canon, ids = sample_block_d(proc["T"], proc["E_canon_shared"], proc["pi"], split, sizes[split], scope, process)`; `t = k4b_data.history_table(canon, ids, split, 0)`. `sizes` defaults to `SIZES`. Returns `{split: t}` in that order (lgate 4,096; cal, val, test 3,072; landmarks on cal and val; 4 reference rows on cal) |
| `save_tables(out, tables, dry=False) -> list[Path]` | `hwsc_data.save_table(out/"stages"/"S3"/hist_name(split, dry), tables[split])` for each split (exclusive create; the six K4b keys and dtypes). Returns the paths in `SPLITS` order |
| `load_tables(out, dry=False) -> dict` | `{split: k4b_fresh.load_recorded(out, "S3", hist_name(split, dry))}` (re-hashed against the latest STAGE_COMPLETE; a mismatch → `FAIL_TECHNICAL/LINEAGE`), each with `"split"` and `"block": 0` added |

### 3.2 H2-D and the registry risk (§4.2; §7 rows 3)

| Name | Contract |
|---|---|
| `separation_d(reg, tables) -> dict` | `r = hwsc_data.separation_c(reg, tables)` with `tables` in `SPLITS` order. The result has the same keys and the same status rule: any collision (`<split>_R` or a pair) → `FAIL_TECHNICAL/LINEAGE`; a sequence-id hit → `FAIL_TECHNICAL/LINEAGE`; a predicate hit → `INCONCLUSIVE/REGISTRY_INCOMPLETE`; else PASS. Adds `"rows": {split: n}` |
| `registry_risk_d(p_d2a) -> dict` | `rows = 13312`; `value = rows * Fraction(float(p_d2a))`; `ok = value <= Fraction(1, 100)` (equality passes). Returns `{"rows", "value": str(value), "ok"}` |

### 3.3 ORACLE-D, references, B4-TEST, LGATE-ORACLE, shared controls (§2.4 d; §7 rows 4–6)

| Name | Contract |
|---|---|
| `oracle_d(proc, tables) -> dict` | `p = proc`. For s in (`cal`, `test`): `m[s] = k4b_scores.oracle_moments(p["T"], p["E_canon_shared"], p["pi"], tables[s]["canon32"], p["features"])` (keys 1, 2, 4, 32; float64 [n, 2]). `refs_test = k4b_cert.references(p["T"], p["E_canon_shared"], p["pi"], p["coords"], tables["test"]["canon32"])` (all 3,072 rows). `r = tables["cal"]["ref_row"]`; `refs_cal = k4b_cert.references(…, tables["cal"]["canon32"][r])` (4 rows). `c_test = k4b_cert.moment_check(m["test"], refs_test)`; `c_cal = k4b_cert.moment_check({K: m["cal"][K][r] for K in m["cal"]}, refs_cal)`. Either not ok → `C1GateFailure("FAIL_TECHNICAL/ORACLE", "<n_fail> rows above MOMENT_TOL")`. Returns `{"moments": m, "refs_test": refs_test, "max_gap": str(max of both), "n_checked": 3076}` |
| `save_oracle(out, moments) -> list[Path]` | `stages/S4/ORACLE_cal.npz` and `ORACLE_test.npz`, keys `m1, m2, m4, m32` (float64 [n, 2]), exclusive |
| `refs_to_json(refs, proc, test_table_sha256) -> dict` | `{"schema": "hwsd-refs-v1", "identity": reference_cache.identity(T, E_canon_shared, pi, coords), "test_table_sha256", "Ks": [1, 2, 4, 32], "n": len(refs), "M": {str(K): [[str(mx), str(my)] for each row] for K in Ks}}`. No history content is stored (decision 5) |
| `refs_from_json(obj, proc, n, test_table_sha256) -> list` | Checks schema, `identity == reference_cache.identity(...)`, `test_table_sha256`, `n` and the length of every list; any failure → `C1GateFailure("FAIL_TECHNICAL/LINEAGE", …)`. Returns `[{K: (Decimal(mx), Decimal(my)) for K in Ks} for each row]`. `refs_from_json(refs_to_json(r, …), …) == r` exactly |
| `b4_test(m_test, refs_test, eps, Z, seed=None) -> dict` | Mirror of `k4b_driver.b4_val` on test rows: `r4n = scores.r4_norms(m_test[32], m_test[4])`; `Bn = max(k4b_cert.norm_bound(r4n[i], ref[32], ref[4], eps[4], eps[32]) for i, ref in enumerate(refs_test))`; `g = k4b_cert.b4_guard(r4n, Bn, Z, seed if seed is not None else k4b_config.SEEDS["fresh_b4"], len(r4n))`. Returns `dict(g, B_norm_max=Bn)`. `g["status"]` is PASS (certified one-sided 95 % lower bound of B4 > 0.01) or `INCONCLUSIVE/HEADROOM` / `INCONCLUSIVE/NUMERICAL`. It never raises on a non-PASS status (decision 9) |
| `lgate_oracle(proc, canon32) -> dict` | `q = hwsb_eval.oracle_predictives(proc, canon32, Ks=(1, 4))` (keys 1, 4, 32; float64 [n, 36]). Every value must be finite and every row sum within 1e-6 of 1, else `C1GateFailure("FAIL_TECHNICAL/NUMERICAL", …)`. Returns `q` |
| `save_lgate_q(out, q) -> Path` | `stages/S4/LGATE_Q.npz` keys `q1, q4, q32`, exclusive |
| `shared_controls(m_test, canon32) -> dict` | Exactly the `"all"` entries of `k4b_scores.control_arrays`: with `one(phi) = {"X": k4b_scores.phase_scores(phi, m[32], m[4]), "phi": phi}`: `{"m4_phase": {"all": one(k4b_scores.m4_phase(m[4]))}, "sha_suffix": {"all": one(k4b_scores.sha_phase(canon32))}, "delta4_orc": {"all": one(k4b_scores.oracle_phase(m[32]))}}` |
| `save_shared(out, shared, bounds) -> list[Path]` | `stages/S4/SHARED_CONTROLS.npz` keys `f"{name}_X"`, `f"{name}_phi"`; `stages/S4/SHARED_CONTROLS.json` `{name: {"max_B": str, "certified": bool}}`, where `bounds = k4b_cert.control_bounds_all(shared, refs_test, eps)` |

### 3.4 Obligations (J3, J4, J10; §4.3 item 3, §9.4)

| Name | Contract |
|---|---|
| `classify_file(store, rel) -> (cls, basis)` | For one array file of an hwsd store or dry store (`rel` POSIX relpath), the first matching rule: (1) `re.fullmatch` of CONTRACT `obligation.history_names["K4b history table"]` → `("K4b history table", None)`; (2) the ObservationSet regex, with sibling `meta.json` `artifact_type == "ObservationSet"` → `("ObservationSet", None)`; (3) `…/artifacts/<T>/<id>/(payload.npz|state.pt)` with T ∈ {WorldSpec, TransitionSpec, EmissionSpec, Checkpoint} and sibling `meta.json` `artifact_type == T` → `("NON_HISTORY", "artifact")`; (4) a component named `registry` before the file name → `("NON_HISTORY", "registry")`; (5) a CONTRACT `obligation.name_rules` regex fullmatch → `("NON_HISTORY", "name_rule")` (J11 bases: `artifact`, `registry`, `name_rule`). No match → `C1GateFailure("FAIL_TECHNICAL/LINEAGE", f"unclassifiable array file {rel}")` |
| `obligation_files(store) -> list[dict]` | A sorted `os.walk` of the whole store (`superseded/` included; `.git` never present). For every `.npz`/`.npy`/`.pt`: `{"relpath", "sha256", "bytes": file size, "class", "reader", "basis"}` from `classify_file`; `reader` is `"hwsb_registry.registry_digests"` for ObservationSet, `"k4b_history_table"` for a K4b history table, null for NON_HISTORY. The store's own files are hashed (`stage_records.sha256`), except a Checkpoint payload (`state.pt` / `payload.npz` under `artifacts/Checkpoint/`), whose `sha256` is null: it is classed by its sibling `meta.json` and never opened or hashed (J11) |
| `write_obligation(store, name, job, attempt, utc, reservation_id=None, dry_stores=(), written_by="hwsd") -> (Path, dict)` | `name` must be `"REGISTRY_OBLIGATION.json"` or match `REGISTRY_OBLIGATION_<job>-a<k>.json` with this `job` and `attempt`, else `ValueError`. Writes `store/name` by exclusive create: `{"schema": "hws-registry-obligation-v1", "store": str(store), "track": "D", "job", "attempt", "written_utc": utc, "written_by", "reservation_id", "name_rules": CONTRACT obligation.name_rules, "dry_stores": [str(p)], "files": obligation_files(store), "rule": "fail closed"}` |
| `stop_obligation(store, job, attempt, reservation_id, utc) -> dict` | J10 item 3: `write_obligation(store, f"REGISTRY_OBLIGATION_{job}-a{attempt}.json", …)`, then `end_reservation(store, reservation_id, utc, that path)`. Returns `{"obligation", "end"}` |

### 3.5 Reservations, `end_reservation`, W2 attestation (J8; §4.3 item 2, §9.5; DRD11)

| Name | Contract |
|---|---|
| `reservation_path(store, attempt) -> Path` | `store/"reservations"/f"RES-HWSD-W2-a{attempt}.json"` |
| `start_reservation_d(store, attempt, utc) -> (Path, dict)` | Refuses with `C1GateFailure("INCONCLUSIVE/AUTHORITY", …)` if any other non-END file in `store/reservations/` has state ACTIVE and `reservation_ended(...)["ended"]` is False. Else it creates the folder and calls `k4b_release.start_reservation(path, f"HWSD-W2-a{attempt}", utc)` (exclusive; id `RES-HWSD-W2-a<k>`) |
| `verify_reservation_d(path, reservation_id, sampling_began=False) -> dict` | `k4b_release.verify_reservation(path, {"reservation": reservation_id}, sampling_began)` |
| `end_reservation(store, reservation_id, utc, obligation_path, written_by="hwsd_data.end_reservation") -> dict` | J8 items 1–3. `res = store/"reservations"/f"{reservation_id}.json"`; `end = res.with_name(f"{reservation_id}.END.json")`. It refuses, raising `C1GateFailure("FAIL_TECHNICAL/LINEAGE", reason)` and writing nothing, when: `res` is missing or its `state` ≠ `"ACTIVE"`; `obligation_path` does not exist or does not lie in `store`; `end` exists. Otherwise it writes `end` by exclusive create: `{"schema": "hws-reservation-end-v1", "reservation_id", "reservation_file": "reservations/<id>.json", "reservation_sha256": sha256(res), "end_utc": utc, "obligation_file": relpath of obligation in store, "obligation_sha256", "written_by"}`. The reservation file is never edited. Returns the record |
| `reservation_ended(res_path, root=ROOT) -> dict` | J8 item 4, for one reservation file of the K4b schema. (a) `id == "RES-HWSC-W2"`: ended iff `ROOT/agent-handoff/records/HWSC_W2_END.json` exists with sha256 == CONTRACT `identity.rows.hwsc_w2_end.sha256` and its `reservation_file_sha256` == sha256 of `res_path`. (b) Otherwise: ended iff `<dir of res_path>/<id>.END.json` exists with schema `hws-reservation-end-v1`, `reservation_sha256` == sha256 of the current reservation file, and `obligation_sha256` == sha256 of the current file `<store>/<obligation_file>`. Here `<store>` is the parent of `reservations/`, or the folder of a top-level reservation file. Returns `{"ended": bool, "rule": "a" or "b" or None, "reason"}` |
| `w2_attest(root=ROOT, exclude=()) -> dict` | For every file matching CONTRACT `window.reservation_globs` under `root`, excluding `*.END.json` and the paths in `exclude`: a file that is not a JSON object with keys `id` and `state` → schema failure; `state != "ACTIVE"` → not live; `reservation_ended(f)["ended"]` → not live; else live. Status `PASS` iff there is no live reservation and no schema failure; else `INCONCLUSIVE/AUTHORITY`. Returns `{"status", "checked": [{"path", "id", "state", "ended", "rule"}], "live": [...], "schema_failures": [...]}` |

## 4. `hwsd_readers.py`: R9, R10, the K4b table reader, the superset check (§4.1, §4.4)

Every source returns the `hwsc_registry._new` shape: `{"status", "digests": set, "seq_ids": set, "files": [...], "other": [{"path", "reason"}], "non_history": [{"path", "basis"}], "non_c2_format": [], "present": bool, "known_gaps": []}`. It is closed by the `hwsc_registry._close` rule: LINEAGE if a lineage flag is set, else `INCONCLUSIVE/REGISTRY_INCOMPLETE` if `other` is non-empty, else PASS. (`_new` and `_close` are used through `hwsc_registry` as module attributes; decision 16.)

| Name | Contract |
|---|---|
| `read_k4b_table(path, expected_sha256=None) -> dict` | If `expected_sha256` is given, the file's sha256 must equal it, else `ValueError("sha256")`. `np.load(path, allow_pickle=False)`: `canon32` integer [n, 32]; `seq_ids` integer [n]; `digest` str [n]; and `digest.astype(str).tolist() == scores.history_digests(canon32.astype(np.uint8))`. Any defect → `ValueError`. Returns `{"digests": set, "seq_ids": set of int, "n": n}` |
| `os_digests(payload_path) -> list` | Mirror of `hwsc_registry._os_canonical`'s read for one ObservationSet payload: `root = payload_path.parent.parent.parent`; `st = ArtifactStore(LocalFSBackend(root))`; `obs = st.load(ObservationSet, id, consumer="experiment")`. The unique EmissionSpec parent (`st.meta(id).parent_ids` with `st.meta(p).artifact_type == "EmissionSpec"`) is required (none or several → `ValueError`). `spec = st.load(EmissionSpec, pid, consumer="experiment")`. Returns `scores.history_digests(hwsb_data.canonical32(obs.tokens, spec.symbol_perm))` |
| `stage_complete_sha(stages_jsonl, rel, stage=None) -> str or None` | The `files[rel]` of the latest `STAGE_COMPLETE` event (optionally only those of `stage`) of a `STAGES.jsonl`, read through `guard` |
| `source_hwsc(store=HWSC_STORE) -> dict` | **R9** (J1; CONTRACT `registry.r9`). In order: **(b′)** `inv = read_obs_inventory(store)`; `sha256(OBS_INVENTORY)` must equal `read_json(store/"RELEASE_A.json")["obs_inventory_sha256"]` and `stage_complete_sha(store/"STAGES.jsonl", "stages/TRAIN/OBS_INVENTORY.json", "TRAIN_INVENTORY")`, else lineage. **(a)** `own = hwsc_registry.source_own(store, inv)`, merged in. **(b)** For each of the four `registry.r9.b` files: its sha256 must equal `stage_complete_sha(store/"STAGES.jsonl", rel)` (else lineage); then `read_k4b_table` (a failure goes to `other`). **(d), (e), (e′)** A sorted `os.walk` of `store` that never enters `sealed`. `stages/TRAIN` and `logs` are entered for names only: no file there is opened. For every `.npz`/`.npy`/`.pt` with relpath `rel`: skip it if it was read under (a) or (b) (an `artifacts/ObservationSet/*/payload.npz`, or a `superseded/**/stages/S3|S7/HIST_*.npz`); under `stages/TRAIN/` → `other` ("array file in stages/TRAIN"); a fullmatch of a `registry.r9.non_history_rules` regex → `non_history`. The artifact rule also needs the sibling `meta.json` (read through `guard`) to have `artifact_type` equal to the type folder, else `other`. The logs rule is checked by name only, never opened. Anything else → `other`. Nothing under `stages/TRAIN/` is opened except by the two exempt readers; no `state.pt` or Checkpoint payload is opened or hashed |
| `superset_check(reg, store=HWSC_STORE) -> dict` | **R9 (f).** `reg` is the K-REG-D `c2_registry.Registry`. `m = read_json(store/"registry"/"K-REG2.json")`. The sha256 of `store/"registry"/"K-REG2_digests.npz"` must equal `m["digest_file_sha256"]`, else status `FAIL_TECHNICAL/LINEAGE`. `d2 = np.load(...)["digests"]` (str). `missing = count of ~reg.contains(d2)`, evaluated in chunks of 1,000,000. `t = read_k4b_table(store/"stages"/"S7"/"HIST_test_b0.npz")["digests"]`; `missing_test = count of ~reg.contains(sorted(t))`. Status PASS iff both are 0, else `INCONCLUSIVE/REGISTRY_INCOMPLETE`. Returns `{"status", "n_kreg2", "missing", "n_test", "missing_test"}` |
| `obligation_check(store, kind="store") -> dict` | **R10 for one store** (J10 item 1; decision 7). `kind` ∈ {`"store"`, `"dry"`}. (1) `files` = every `.npz`/`.npy`/`.pt` under `store` (sorted walk; names only at this step). (2) `obls` = the top-level `REGISTRY_OBLIGATION*.json` files. None → `other` "store present without an obligation" (also for an empty store). (3) The newest by `(written_utc, name)`; its schema must equal CONTRACT `obligation.schema`, it must have every `obligation.fields` key, every entry every `file_fields` key, and every `class` must be in `obligation.classes`, else `other`. `reader` must be `"hwsb_registry.registry_digests"` for ObservationSet, `"k4b_history_table"` for a K4b history table and null for NON_HISTORY. `basis` must be None for ObservationSet and K4b history table; for NON_HISTORY it must be one of: `artifact` (relpath of the form `…/artifacts/<T>/<id>/(payload.npz|state.pt)`, T ∈ {WorldSpec, TransitionSpec, EmissionSpec, Checkpoint}, sibling `meta.json` `artifact_type == T`); `registry` (a component `registry` before the file name); `name_rule` (some regex of the obligation's own `name_rules` fullmatches the relpath; every `name_rules` kind must be in `obligation.name_kinds`). `sha256` is null only for a Checkpoint payload. Else `other` "unknown basis" (a missing or extra key, an unknown value or a `name_rule` basis that no listed regex matches is `other` too). (4) Every array file is listed exactly once, and every listed file exists. An unlisted file, a listed missing file or a duplicate → `other`. (5) Reads: ObservationSet → `os_digests` (its sha256 must also equal the listed one); K4b history table → `read_k4b_table(path, listed sha)`; NON_HISTORY → sha256 equals the listed one, except a Checkpoint payload (listed sha256 null), which is never opened or hashed; a null sha256 on any other file is `other`. A mismatch or an unreadable file → `other`. Returns the source shape plus `{"obligation": name}` |
| `source_hwsu(root=ROOT, scratch=SCRATCH) -> dict` | **R10.** (1) `root/"hwsu-store"` present → `obligation_check(it, "store")`, merged. Absent → contributes nothing (present False). (2) For every top-level folder of `scratch` whose name starts with `hwsu-` (sorted): `hwsc_registry.source_dry(paths=[folder])`, the R5′ token reader file by file, merged. If the name starts with `hwsu-dry`, `obligation_check(folder, "dry")` is merged too: a `hwsu-dry*` store without its own obligation → INCOMPLETE (J4). `test_hwsu-*` folders are test roots and are not read. Returns the merged source with `"stores"` (names read) |

## 5. `hwsd_registry.py`: K-REG-D (§4.1; DRD8)

| Name | Contract |
|---|---|
| `BLINDED_TOP = "hwsc-job-"` | top-level scratch folders walked by name only |
| `scratch_scan_d(scratch=SCRATCH) -> dict` | Mirror of `hwsc_scratch.scratch_scan` with one change. A top-level folder whose name starts with `hwsc-job-` is walked by name only: every `.npz`/`.npy`/`.pt` there is listed with class `"blinded_array"` and shape None, and is never opened. Unchanged rules: top-level `test_*` folders are skipped, except `test_hwsb-*`; the stage-B folders (`hwsb-`, `hwsb-dry`, `test_hwsb-`) are walked completely; elsewhere `test_*` components are pruned before descent; classes come from `hwsc_scratch._classify` (headers only); `meta.json` under `ObservationSet/<id>/` is `os_root`. `"__top_level__"` lists the array files directly in `scratch` |
| `row_for_d(name, table) -> dict or None` | `table[name]` if present. Else the first pattern row whose prefix matches: `hwsc-dry-<job>` (`hwsc-dry-`), `test_hwsc-<job>` (`test_hwsc-`), `hwsd-dry-<job>` (`hwsd-dry-`), `hwsd-kd-<job>` (`hwsd-kd-`), `test_hwsd-<job>` (`test_hwsd-`), `test_hwsu-<job>` (`test_hwsu-`), `hwsu-*` (`hwsu-`). Else None |
| `dry_class_d(store, rel, rec) -> str or None` | The hwsd-dry type rule (CONTRACT `registry.dry_type_rule`). `parts = rel.split("/")`. It needs `len(parts) >= 3`, `parts[0]` a fullmatch of `DRD\d+` and `parts[1]` of `\d{8}T\d{6}Z`, else None. For `tail = parts[2:]` and `cls = rec["class"]`: **R5** if tail is `artifacts/ObservationSet/<id>/{meta.json, payload.npz}` with cls ∈ {os_root, history} and a single EmissionSpec parent in the same artifacts folder (the `hwsc_drystore._os_parent_ok` rule, mirrored), or `stages/S3/DRYHIST_<split>_b0.npz` with cls history and an integer `canon32` member of last dimension 32; **CHECKPOINT** if tail is `artifacts/Checkpoint/<id>/state.pt` (cls pt) or `…/payload.npz`; **REGISTRY_FIXTURE** if tail is `registry/K-REG1_digests.npz` with npz keys exactly {`digests` (kind U), `seq_ids`}, or `registry/runs/K-REG1/run_\d{5}\.npy` with a uint8 [n, 32] header. Else None. An unreadable header → None |
| `scratch_check_d(scratch=SCRATCH, table=None, readers_ok=None) -> dict` | Mirror of `hwsc_scratch.scratch_check` over `scan = scratch_scan_d(scratch)` with `table` (default `hwsd_config.scratch_table()`) and `row_for_d`. Per top-level name with listed files: no row → `other` "no inventory row". A row with decision TO_FREEZE or `frozen_files == "TO_FREEZE"` → `other` "row not frozen" (also when nothing is listed). A name starting `hwsc-dry` → `hwsc_drystore.check_store(scratch/name, listed, ok_tags, out)` (unchanged stage-C rule). A name starting `hwsd-dry` → for each listed file, `dry_class_d` None → `other` "not allowed by the hwsd-dry type rule"; class R5 needs `"R5"` in `readers_ok`. A name starting `hwsu-` → every listed file needs `"R10"` in `readers_ok`, else `other`. Every other row → `_check_row_d`, a line-for-line mirror of `hwsc_scratch._check_row`: frozen_files class equality, hash_frozen re-hash, covered reader tags, EXCLUSION fixture rule, READER tags. Under it a `blinded_array` file passes only if `frozen_files[rel] == "blinded_array"`. Returns the source shape plus `scan_counts` |
| `inventory_d(root=ROOT, readers=None, table=None) -> dict` | Mirror of `hwsc_registry.inventory_c`. `inv = k4b_registry.inventory(root, exclude=tuple(CONTRACT registry.deep_scan_exclude))`. Every OWN row of `table` (default `hwsd_config.root_table()`) is popped from `inv` (here `hwsd-store`). `classes = k4b_registry.classify(inv, readers)`. `frozen` = table without OWN rows. A READER_IF_PRESENT row absent from `inv` is skipped; if present it is checked as READER. A TO_FREEZE row → violation "row not frozen". Every other name → `c2_registry._violation(name, frozen.get(name), inv.get(name), classes.get(name), readers.get(name, []))`. Returns `{"status", "inv", "classes", "unlisted", "violations"}` |
| `build_d(out_dir, root=ROOT, scratch=SCRATCH, handoff=None, sources=None) -> dict` | `out_dir` must be `<store>/registry` (else `ValueError`); `K-REG-D.json` existing → `FileExistsError`. `handoff` defaults to `hwsc_config.load_handoff()`. `t0 = time.process_time()`. A closure keeps `state = {}`. The source overrides, merged with `sources` (tests and dry run only; same keys), are: `"own"`: `r9 = hwsd_readers.source_hwsc(root/"hwsc-store")`, `r10 = hwsd_readers.source_hwsu(root, scratch)`; `state` records both statuses; returns their merge, LINEAGE if either is LINEAGE, else INCOMPLETE if either is not PASS. `"dry"`: the merge of `hwsc_registry.source_dry()` and `hwsc_registry.source_dry(paths=sorted(scratch.glob("hwsd-dry*")))`. `"scratch"`: `lambda ok: scratch_check_d(scratch, readers_ok=set(ok) | {"R10"} if R10 PASS)`. `"inventory"`: `lambda readers: inventory_d(root, dict(readers, **{"hwsc-store": ["R9"] if R9 PASS, "hwsu-store": ["R10"] if R10 PASS}))`. Then `inner = hwsc_registry_build.build("K-REG1", out_dir, root=root, scratch=scratch, handoff=handoff, own_expected={"hwsd": "R9+R10"}, sources=overrides)`. Then `reg = c2_registry.Registry.load(out_dir.parent, "K-REG1")` and `sup = hwsd_readers.superset_check(reg, root/"hwsc-store")` (via the `"superset"` source key when given). Writes the wrapper `out_dir/"K-REG-D.json"` (exclusive): `{"registry_version": "hwsd-reg-v1", "protocol_sha256": PROTOCOL_SHA256, "inner_version": "K-REG1", "inner_manifest_sha256", "inner_digest_file_sha256", "inner_status", "status", "problems", "superset": sup, "r9": summary, "r10": summary, "known_label": CONTRACT registry.known_label, "cpu_s", "built_utc"}`. `status` = `inner["status"]` if it is not PASS, else `sup["status"]`. Returns the wrapper |
| `load_d(store=STORE) -> c2_registry.Registry` | The wrapper must exist and its `inner_manifest_sha256` must equal the sha256 of `registry/K-REG1.json`, else `C1GateFailure("FAIL_TECHNICAL/LINEAGE", …)`. Wrapper status not PASS → `C1GateFailure(status, …)`. Returns `c2_registry.Registry.load(store, "K-REG1")` |

## 6. `hwsd_score.py`: the per-checkpoint scorer (§2.4, §2.6; §7 rows 7–12; DRD6, DRD14)

**Context** `ctx` (built by the SCORE job, KD4 or the dry run):
- `proc`;
- `tables` (`load_tables`: lgate, cal, val, test);
- `moments` `{"cal", "test"}` (from `ORACLE_*.npz`);
- `refs_test` (list, or None when planted);
- `eps` (`k4b_cert.envelopes()`);
- `q` (`LGATE_Q.npz` → `{1, 4, 32}`);
- `Z` (Fraction);
- `cfg` (`k4b_config.chart_cfg()`);
- `out` (store root);
- `timed` (`op_guard.timed_factory(out, 600)`; decision 11);
- `planted` (bool).

| Name | Contract |
|---|---|
| `checkpoint_dir(out, j, step) -> Path` | `out/"stages"/"SCORE"/str(j)/f"s{step}"` |
| `ledger_for(out, j, step)` | `c1_chart.ConstructionLedger(checkpoint_dir(out, j, step)/"CHART_CONSTRUCTIONS.json")`. One file per checkpoint; at most two claims (production, then direct), each never retried. 36 checkpoints → at most 72 claims in total |
| `load_checkpoint_d(j, step) -> (ckpt, model64, state_sha)` | `row = CHECKPOINTS[(j, step)]`; `ckpt = k4b_driver.load_checkpoint(row["id"])` (`ARTIFACTS` bound to `hwsc-store/artifacts`; the store verifies the checksum and writes nothing); `model64, sha = c1_model.load_model64(ckpt)` |
| `acts_fn(model64, perm) -> callable` | `lambda canon32: c1_model.activations(model64, k4b_data.model_inputs(canon32, perm))` (float64 [n, 128] at `resid_post_3`, index 32) |
| `learning_one(ckpt, canon32, perm, q, z=Z, z_s=Z_S) -> dict` | `p = hwsb_eval.model_predictive(ckpt, canon32, perm)` (float32 path, never mixed with the float64 activations). `r = hwsb_eval.b1(q, p)`. `r["status"] == "INCONCLUSIVE"` or non-finite `captured` → `C1GateFailure("FAIL_TECHNICAL/NUMERICAL", …)`. `b2z = hwsb_eval.forcing(q[32], q[4], p, z)`; `b2s = hwsb_eval.forcing(q[32], q[4], p, z_s)`. Returns `{"captured", "regret", "G_C", "status": r["status"], "regret_sd", "regret_se", "G_C_sd", "n", "B2_z": b2z, "B2_zS": b2s, "z", "z_S", "learn_pass": r["status"] == "PASS", "B2_L_zS": b2s["L"]}` |
| `map_build(res, where) -> dict` | For a `k4b_charts.build_chart` result or a mapped `c0_val` exception. A status starting `FAIL_TECHNICAL` → `C1GateFailure(status, f"{where}: {reason}")`, which stops the run (row 9). A status `INCONCLUSIVE` whose reason starts with `native operation ` and contains ` wall` → `{"kind": "NATIVE_WALL", "text": f"NATIVE_WALL: {reason}"}`. Any other non-PASS → `{"kind": status, "text": f"{status}: {reason}"}` |
| `chart_one(j, acts, tables, m32_cal, ledger, cfg, out_dir, timed=None, skip_direct=False) -> dict` | The per-key bodies of `k4b_driver.c0_cal_stage` and `k4b_charts.c0_val_gate` with the checkpoint ledger. `acts(split)` returns the activations of that split's canon32. In this order: (1) `A = acts("cal")`; `land = tables["cal"]["landmark"]`; `ids = tables["cal"]["seq_ids"]`. (2) `prod = k4b_charts.build_chart(A[land], ids[land], m32_cal[land], ledger, j, "production", cfg, timed=timed)`; `map_build`. (3) If PASS: `ext = k4b_charts.extend(prod["chart"], prod["gauge"], A[~land], cfg)`; `dec = k4b_decoder.fit(tables["cal"]["canon32"][~land], ids[~land], ext.phase, j)`. Then **freeze**: `out_dir/"CHART.npz"` = `stage_records.save_npz(**prod["serial"])`; `out_dir/"DECODER.npz"` = `k4b_decoder.to_arrays(dec)`; `out_dir/"ACTS_cal.npz"` key `acts` = A; `out_dir/"FROZEN.json"` = `{"files": {name: sha256}, "gauge": [int sign, float shift, float alignment], "decoder_status", "c0_cal": "PASS"}`. (4) Only after the freeze, and only if PASS and not `skip_direct`: `V = acts("val")`; `vl = tables["val"]["landmark"]`; `direct = build_chart(V[vl], tables["val"]["seq_ids"][vl], None, ledger, j, "direct", cfg, timed=timed)`; `map_build`. If PASS: `c0 = c1_chart.c0_val(prod["chart"], prod["gauge"], V[vl], direct["chart"], cfg)`. An exception there is mapped by `c1_records.adapt_chart_exception`, else `classify_exception` (INCONCLUSIVE with a reason starting `CHART_UNAVAILABLE` → `INCONCLUSIVE/CHART_UNAVAILABLE`), then `map_build`. Returns `{"c0_cal": {"status", "reason", "diagnostics"}, "c0_val": None or {"status", "reason", "criteria", "n", "n_supported", "fidelity", "bins", "resultant", "direct_status", "direct_reason", "direct_diagnostics"}, "prod": {"chart", "gauge"} or None, "decoder": dec or None, "frozen": record or None, "acts_cal": A}`. **Bitwise contract (DRD14, KD2 a):** with a fresh ledger and the same inputs, `prod["serial"]` equals the serial that `k4b_charts.c0_cal` (one model) builds; `dec` equals the decoder `k4b_driver.c0_cal_stage` fits; and `c0_val` (`n`, `n_supported`, `fidelity`, `bins`, `resultant`, `criteria`, `status`) equals `k4b_charts.c0_val_gate(...)["per_model"][j]` |
| `arrays_one(prod, acts_test, m, refs, eps, cfg, planted=False) -> dict` | The per-key body of `k4b_fresh.t_pre`. `ext = k4b_charts.extend(prod["chart"], prod["gauge"], acts_test, cfg)` (phases finite in [0, 2π), else `FAIL_TECHNICAL/NUMERICAL`). `a = k4b_scores.endpoint_arrays(ext.phase, ext.supported, m[32], m[4])`. If `planted`: `b = None` and `cert = {"status": "PASS", "max_B": {"X_minus": Fraction(0), "X_plus": Fraction(0), "n_hat": Fraction(0)}, "certified": {…: True}, "planted": True}`. Else `b = k4b_cert.endpoint_bounds(a, ext.supported, ext.phase, refs, eps)` and `cert = k4b_cert.certify({"X_minus": {"X": a["X_minus"], "max_B": b["max"]["minus"]}, "X_plus": {"X": a["X_plus"], "max_B": b["max"]["plus"]}, "n_hat": {"X": a["r4n"], "max_B": b["max"]["norm"]}}, {})` (P2 failure raises `FAIL_TECHNICAL/NUMERICAL`; a primary above `CAP` → status `INCONCLUSIVE/NUMERICAL`). Returns `{"ext", "arrays": a, "bounds": b, "certificate": cert, "max_abs": {"X_minus": float(max|X−|), "X_plus": float(max|X+|)}}`. With the same chart and activations, `a` and `b` equal `t_pre`'s `arrays[j]` and `arrays[j]["bounds"]` |
| `controls_one(m, canon32, ext, decoder) -> dict` | The `control_arrays` families for one key, without `init` and without the shared families: `{"decoder": {"unavailable": str(reason)} if decoder status ≠ AVAILABLE else {"X": k4b_scores.phase_scores(k4b_decoder.predict_phase(decoder, canon32), m[32], m[4]), "phi": that phase}, "delta1": dict(k4b_scores.secondary_arrays(ext.phase, ext.supported, m, 1), phi=ext.phase, supported=bool array), "delta2": (the same with K = 2), "naive": {"X": k4b_scores.naive_scores(ext.phase, m[32], m[4]), "phi": ext.phase}}`. For every j of `k4b_config.MODELS`: `controls_one(m, c, ext[j], dec[j])[name] == k4b_scores.control_arrays(m, c, ext, init_ext, dec)[name][j]` (arrays bitwise) for name ∈ {decoder, delta1, delta2, naive} |
| `status_of_checkpoint(ch, cert) -> (status, label)` | §16 precedence: C0-CAL not PASS → `("CHART_UNAVAILABLE", "CHART_UNAVAILABLE/" + text)`. Else `cert["status"] != "PASS"` → `("UNCERTIFIED", f"UNCERTIFIED/{cert['status']}: " + ",".join(names with certified False))`. Else C0-VAL PASS → `("SCORED", "SCORED")`. Else `("SCORED_UNVALIDATED", label)`, where the label is `"SCORED_UNVALIDATED/" + text` when the direct chart is not PASS, and `"SCORED_UNVALIDATED/CRITERIA: " + ",".join(sorted(failing criteria))` when c0_val ran and failed |
| `archived_wall(out, j, step) -> dict or None` | X-3 and RC-8. Looks at the newest `out/"superseded"/<job>-a<k>/` (by k) that holds `stages/SCORE/<j>/s<step>/CHART_CONSTRUCTIONS.json`. Returns `{"role": the last claimed role, "label": marker label}` iff all three hold: (1) that ledger's last claim is `[j, role]`; (2) the same archived folder has no `stages/SCORE/<j>/s<step>/CHECKPOINT_RECORD.json`; (3) its archived `OPERATION_ACTIVE.json` has `"state": "active"`. Else None |
| `score_checkpoint(ctx, j, step, ckpt=None, model64=None, perm=None, acts=None, learn=None) -> dict` | In the §2.4 order. **(a)** If `learn` is None: `learn = learning_one(ckpt, ctx["tables"]["lgate"]["canon32"], perm, ctx["q"])`. **(b)** `acts` defaults to `lambda split: acts_fn(model64, perm)(ctx["tables"][split]["canon32"])`. `w = archived_wall(ctx["out"], j, step)`: with role production, C0-CAL is set to `{"status": "INCONCLUSIVE", "reason": "NATIVE_WALL: <label> (archived)"}` and no construction is attempted; with role direct, `chart_one(..., skip_direct=True)` runs and `c0_val` is recorded as NATIVE_WALL (archived). Otherwise `ch = chart_one(...)` with `ledger_for(...)`. **(c)** If a production chart exists: `T = acts("test")`; `r = arrays_one(ch["prod"], T, ctx["moments"]["test"], ctx["refs_test"], ctx["eps"], ctx["cfg"], ctx["planted"])`; `cons = controls_one(...)`; `cb = k4b_cert.control_bounds_all({name: {"k": e} for name, e in cons.items() if "unavailable" not in e}, ctx["refs_test"], ctx["eps"])` (skipped when planted); `sup = k4b_scores.support_report(r["ext"], ch["prod"]["chart"].support_radius, r["arrays"]["r4n"], r["ext"].phase, m[32], m[4], False)`; `agree = k4b_decoder.agreement(r["ext"].phase, k4b_decoder.predict_phase(dec, test canon32), r["ext"].supported)` if the decoder is AVAILABLE, else `f"unavailable ({reason})"`. **(d)** Writes in `checkpoint_dir`: `LEARN.json`; `ARRAYS.npz` (only with a production chart; keys `X_minus, X_plus, r4n, phi` float64 [3072], `supported` bool, `decoder_X, decoder_phi` when available, `delta1_X_minus, delta1_X_plus, delta2_X_minus, delta2_X_plus, naive_X`; no key from `k4b_registry.IDENTITY_KEYS`); `CHECKPOINT_RECORD.json` (§18). Returns the record |
| `run_checkpoints(ctx, j, pause=None) -> list` | For step in `STEPS` ascending: `ckpt, model64, _ = load_checkpoint_d(j, step)`; `score_checkpoint(...)` with `perm = ctx["proc"]["perm"][j]`; then `pause()` if given (the item boundary). Returns the 12 records |
| `determinism_d(ctx, j, records) -> dict` | Takes the first and the last record of master `j` with C0-CAL PASS. For each, it reloads the checkpoint, recomputes the cal activations and calls `k4b_charts.determinism_check({"acts": stored ACTS_cal}, {"acts": recomputed})`. A failure → `C1GateFailure("FAIL_TECHNICAL/DETERMINISM", …)`. With no production chart: PASS with `"n": 0`. Returns `{"status": "PASS", "n", "steps"}` |
| `acceptance(out, j, job, attempt, records, cpu_s, freeze_sha256) -> dict` | `{"job", "master": j, "attempt", "counts": {s: count for s in the four statuses}, "fail_technical": None, "files_sha256": {relpath: sha256 of every file under stages/SCORE/<j>/}, "cpu_s", "protocol_sha256", "freeze_sha256", "utc"}`. `hwsd_records.acceptance_check(rec)`, then writes `out/stages/SCORE/<j>/ACCEPTANCE.json` (exclusive) |

## 7. `hwsd_statements.py`: notation, onsets, ORDER, D1–D6 (§5; DRD5)

Pure functions; no file access, no binding needed (except that `sigma` calls `k4b_stats.model_status`, whose `MARGIN` is 1/100 in every binding).

**Input.** A per-model sequence `rows` is a list of K ≥ 1 dicts in checkpoint order (the real run has K = 12). The list position `i` gives `k = i + 1`, and `rows[-1]` is the final checkpoint ("σ(12)" reads σ(K)). A model table is `{j: rows}` for the three masters (any number of keys is accepted; the aggregate covers every key). Row fields:
- `status` (one of the four);
- `valid` (bool: C0-CAL and C0-VAL PASS);
- `L`, `U`, `L_S`, `U_S` (float or None);
- `F_minus`, `F_plus` (Fraction or None);
- `learn_pass` (bool);
- `B2_L_zS` (float or None);
- `step` (int; used only in texts).

A row with status SCORED, SCORED_UNVALIDATED or UNCERTIFIED has non-None `L`, `U`, `L_S`, `U_S`, `F_minus`, `F_plus`.

| Name | Contract |
|---|---|
| `est(row)`, `ok(row)` | `est`: status ∈ {SCORED, SCORED_UNVALIDATED}. `ok`: status == SCORED |
| `fr(x) -> Fraction` | `x` if a Fraction, else `Fraction(float(x))` |
| `sigma(row) -> str` | `"NA"` unless `ok(row)`; else `k4b_stats.model_status(row["L"], row["U"], row["F_minus"], row["F_plus"])["status"]` ∈ {SUPPORT, EXCLUDE, UNRESOLVED, UNRESOLVED/NUMERICAL} |
| `above_s(row)`, `below_s(row)`, `above_s_ok(row)` | `above_s`: `est(row) and fr(L_S) − F_minus > M`. `below_s`: `ok(row) and fr(U_S) + F_plus < M`. `above_s_ok`: `ok(row) and fr(L_S) − F_minus > M`. Exact, strict: equality is neither above nor below |
| `onsets(rows) -> dict` | With 1-based k and None for "undefined": `k_C` = min{k : valid}; `k_C_star` = min{k : valid at k and at every later k} (decision 18); `k_C_plus` = min{k ≥ 2 : valid(k) and not valid(k−1)}; `k_L` = min{k : learn_pass}; `k_P` = min{k : B2_L_zS is not None and B2_L_zS > 0}; `k_B` = min{k : sigma == "SUPPORT"}; `k_B_S` = min{k : above_s} |
| `n_pre(rows) -> int`, `pre_chart_max(rows) -> str or None` | `n_pre` = #{k < k_C : est}; when `k_C` is None, #{k ≤ K : est} (decision 19). `pre_chart_max` = `str(max(fr(U_S) + F_plus))` over the same k with est, or None |
| `order(rows, anchor, A=None) -> dict` | `anchor` ∈ {"chart", "learning"}. `A` defaults to `k_C` or `k_L`. The first matching rule applies: (1) A None → `"NO_CHART"` (chart) or `"NO_LEARNING"` (learning); (1a) anchor chart and A == 1 → `"CHART_AT_INIT"`; (2) some k < A with `above_s` → `"BEFORE"`; (3) `sigma(rows[A−1]) == "NA"` → `"LEARNING_BEFORE_CHART"` if anchor learning and (k_C None or k_C > A), else `"UNCERTIFIED_AT_ANCHOR"`; (4) σ(A) == SUPPORT → `"WITH"`; (5) σ(A) == EXCLUDE and σ(K) == SUPPORT → `"AFTER"`; (6) σ(K) == EXCLUDE → `"NEVER"`; (7) σ(K) == NA → `"FINAL_NA"`; else `"UNRESOLVED"`. Returns `{"anchor", "A", "category"}`. Passing `A` explicitly (used for k_C^+) never applies rule 1a unless A == 1 and the anchor is chart |
| `d1(rows)` … `d6(rows) -> dict` | Per-model readings `{"reading", "reason", "qualifier"}`, with reading ∈ {TRUE, FALSE, NOT_EVALUABLE, BY_CONSTRUCTION (D2 only)}. **D1:** σ(K) SUPPORT → TRUE; EXCLUDE → FALSE; UNRESOLVED or UNRESOLVED/NUMERICAL → NE `UNRESOLVED`; NA → NE `FINAL_NA`. **D2** (rules in this order): k_C == 1 → NE `CHART_AT_INIT`; k_C None → NE `NO_CHART`; order(chart) == BEFORE → FALSE; σ(K) ≠ SUPPORT → NE `FINAL_NOT_SUPPORT`; n_pre ≥ 1 → TRUE with qualifier `INFORMATIVE` iff some k < k_C with est has `fr(U_S) + F_plus < M` (strict), else `UNINFORMATIVE`; else BY_CONSTRUCTION. **D3:** c = order(chart): AFTER → TRUE; WITH or BEFORE → FALSE; else NE with reason c (NO_CHART, CHART_AT_INIT, UNCERTIFIED_AT_ANCHOR, NEVER, FINAL_NA, UNRESOLVED). **D4:** c = order(learning): AFTER → TRUE; WITH or BEFORE → FALSE; else NE with reason c (NO_LEARNING, LEARNING_BEFORE_CHART, UNCERTIFIED_AT_ANCHOR, NEVER, FINAL_NA, UNRESOLVED). **D5:** k_P None → NE `NO_PREDICTIVE_ONSET`; k_C None or k_C > k_P → FALSE; σ(k_P) EXCLUDE → FALSE; σ(k_P) SUPPORT → TRUE; σ(k_P) NA → NE `NA_AT_PREDICTIVE_ONSET`; else NE `UNRESOLVED`. **D6:** LOSS iff ∃ k1 < k2 with `above_s_ok(k1)` and `below_s(k2)` → FALSE; else ∃ k1 < K with `above_s_ok(k1)` → TRUE; else NE `NO_STRONG_CROSSING` |
| `aggregate(statement, per_model) -> dict` | If any model is FALSE → `"FALSE"`. **D2:** every model TRUE or BY_CONSTRUCTION and at least one TRUE with qualifier INFORMATIVE → TRUE. **D1, D3–D6:** every model TRUE → TRUE. Otherwise NOT_EVALUABLE with `reasons = {reason: [models]}` taken from the per-model NE readings. For D2 add: `BY_CONSTRUCTION` (all models) if every model is BY_CONSTRUCTION; `UNINFORMATIVE_PRE_CHART` (all models) if every model is TRUE or BY_CONSTRUCTION, not every model is BY_CONSTRUCTION and no TRUE is INFORMATIVE. Returns `{"statement", "reading", "reasons", "per_model"}` |
| `onset_order_line(table) -> dict` | Per j: `{"k_L_vs_k_C": c(k_L, k_C), "k_P_vs_k_C": c(k_P, k_C)}`, where c(a, b) is "<", "=", ">", or "undefined" if either is None (report-only, S1) |
| `diagnostics(table) -> dict` | Per j: `"mc"` = the steps with `L_S > L` or `U_S < U` (floats, rows with arrays; S2 suggestion); `"positive"` = the steps with est and `fr(L) − F_minus > 0`; `"est_loss"` = pairs (k1, k2), k1 < k2, with `above_s(k1)` and status(k1) == SCORED_UNVALIDATED and `below_s(k2)` (S3, labelled, never a reading); `"chart_at_init"` = when k_C == 1: `{"sigma_step0": sigma(rows[0]), "order_at_k_C_plus": order(rows, "chart", A=k_C_plus)["category"] if k_C_plus else "NO_CHART"}` (RC-4) |
| `evaluate(table, headroom_ok=True, resource_ok=True) -> dict` | `{"onsets": {j: onsets}, "n_pre": {j}, "pre_chart_max": {j}, "order": {j: {"chart": …, "learning": …}}, "statements": {D1…D6: aggregate(...)}, "onset_order_line", "diagnostics"}`. If `headroom_ok` is False, every statement is NOT_EVALUABLE with reasons `{"HEADROOM": all models}`; if `resource_ok` is False, `{"RESOURCE": …}` (precedence RESOURCE before HEADROOM). Onsets, ORDER and curves are still returned |

## 8. `hwsd_summary.py`: SUMMARY (§2.7, §5.1, §5.7, §7 rows 13–14, §8)

| Name | Contract |
|---|---|
| `load_scores(out, masters=MASTERS) -> dict` | For each j and step: `CHECKPOINT_RECORD.json`, `LEARN.json` and (if present) `ARRAYS.npz`, each re-hashed against the latest STAGE_COMPLETE of stage `f"SCORE_{j}"` (a mismatch → `FAIL_TECHNICAL/LINEAGE`). Returns `{(j, step): {"record", "learn", "arrays"}}` |
| `bootstrap_inputs_d(scores, shared) -> dict` | An ordered dict of float64 [3072] arrays. Per j in MASTERS, step ascending, for every checkpoint with arrays: `X:{j}:{step}:-`, `X:{j}:{step}:+`, `decoder:{j}:{step}` (if available), `delta1:{j}:{step}:-`, `delta1:{j}:{step}:+`, `delta2:{j}:{step}:-`, `delta2:{j}:{step}:+`, `naive:{j}:{step}`. Then `m4_phase:all`, `sha_suffix:all`, `delta4_orc:all` |
| `main_bootstrap(inputs, seed=None) -> dict` | `k4b_stats.joint_bootstrap(inputs, seed if seed is not None else k4b_config.SEEDS["endpoint"])` (5,000 draws; one `rng.integers(0, n, n)` per draw shared by every array) |
| `strong_bootstrap(scores, seed=None) -> dict` | `c1_means.bootstrap_means({X± keys only, in the same order}, seed if seed is not None else hwsd_bind.strong_seed(), 50000)` |
| `strong_bounds(draws_minus, draws_plus) -> dict` | The `k4b_stats._q` pattern: values must be finite, else `C1GateFailure("FAIL_TECHNICAL/NUMERICAL")`. `(v, k) = c1_means.quantile_with_rank(draws_minus, P_LO)` with `k == 70` and `c1_means.rank_check`; `(w, h) = quantile_with_rank(draws_plus, P_HI)` with `h == 49931`. A failure → `FAIL_TECHNICAL/NUMERICAL`. Returns `{"L_S": v, "L_S_rank": 70, "U_S": w, "U_S_rank": 49931}` |
| `f_sides(record, Z, n=N) -> (F_minus, F_plus)` | `record["planted"]` → `(F_PLANTED, F_PLANTED)`. Else `F_s = k4b_cert.margin(k4b_cert.b_num(Fraction(record["certificate"]["max_B"][side]), record["certificate"]["max_abs"][side], n), Z)` for side X_minus, X_plus (= max(B_num, 10⁻⁹) + Z) |
| `checkpoint_row(j, step, item, draws, sdraws, Z, controls_summary) -> dict` | The table row: `status`, `label`, `valid`, `step`, `k`. With arrays: `bd = k4b_stats.bounds(draws[X−], draws[X+])` gives `L = bd["L"][0]` (rank 84), `U = bd["U"][0]` (rank 4,917) and `central95_minus/plus` (125 / 4,875); `L_S`, `U_S` from `strong_bounds`; `F_minus`, `F_plus` from `f_sides`; `point_minus/plus = tree_mean`; `sigma`, `labels` and `status_without_F` from `k4b_stats.model_status` when ok; `support` (fraction, width, missing mass); `ratios` = `k4b_stats.ratios(point_minus, B4-TEST point, Δ4^orc point)`; `positive`; `controls` = the entries of the k4b_fresh-style summary for this key; `decoder_agreement`. Always: `captured`, `regret`, `regret_se`, `learn_pass`, `B2_z`, `B2_zS`, `B2_L_zS`, chart diagnostics |
| `control_summary_d(draws, controls, bounds) -> dict` | `k4b_fresh.control_summary(draws, controls, bounds_all)` with `controls = {name: {f"{j}:{step}" or "all": entry}}` and draw keys `f"{name}:{key}"` / `f"{name}:{key}:±"` as built above. The `init` family is absent and skipped |
| `outcome_d(state) -> dict` | §8.1 precedence over `state` keys `fail`, `resource`, `registry`, `headroom`, `partial` (decision 10): `fail` → that `FAIL_TECHNICAL/...` status (prefixed if missing); `resource` → `INCONCLUSIVE/RESOURCE_OR_AUTHORITY` (with `partial` = the masters whose SCORE completed); `registry` → `INCONCLUSIVE/REGISTRY_INCOMPLETE`; `headroom` → `INCONCLUSIVE/HEADROOM`; else `HWSD_REPORT`. Returns `{"outcome", "detail"}` |
| `fill_templates(evaluation, table) -> dict` | CONTRACT `statements.templates` filled by `str.format_map` with a dict that returns `"n/a"` for missing keys. One line per statement reading; D3 adds `D3_CHART_AT_INIT` when any model reads CHART_AT_INIT; D4_TRUE always carries its second sentence |
| `report(out, Z, shared, b4, stage_c=None) -> dict` | Builds the HWSD_REPORT (§18) from `load_scores`, both bootstraps, `checkpoint_row` for all 36, `hwsd_statements.evaluate(table, headroom_ok=b4 status == PASS)`, `fill_templates`, `error_statements`, `multiplicity`, `disclosure`, `does_not_establish` and `stage_c_reference` (RESULT.json `per_model.<j>.L`, `.U`, labelled "stage C, other rows"). Writes `stages/SUMMARY/REPORT.json` (exclusive) and `complete_stage(out, "SUMMARY", [it])`. The bootstrap draws are not persisted (decision 12) |

## 9. `hwsd_known.py`: G0d and KD (§6; DRD13, DRD14)

| Name | Contract |
|---|---|
| `needle_in` | `hwsc_known.needle_in` (reused): an all-digit needle matches only as a whole token; other needles as substrings |
| `seed_search_d(root, needles, scratch=SCRATCH) -> list` | Mirror of `hwsc_known.seed_search_c`. The only change is the prune predicate: a directory is pruned before listing, and a file is skipped before opening, iff `hwsd_config.search_pruned(path, root, scratch)` holds. Unchanged: `os.walk(root, topdown=True)`; skip `.git`, `.venv`, `__pycache__`, `sealed`, `00_read_me_first*`, `docs/research_summary`; text suffixes `.json .jsonl .md .py .txt .yaml`; `encoding="utf-8", errors="replace"`; hits `{"path", "needle", "line"}` in walk order. On a root with no pruned path it equals `hwsc_known.seed_search_c(root, needles)` (list `==`) |
| `needles_d(namespace) -> dict` | `{"own": NEEDLES, "other": the scopes of tracks.U plus str(i) for every i of every tracks.U seed block (inclusive)}` |
| `overlap_check(namespace) -> dict` | D's reserved tokens are the scopes, the store path, the two globs and every integer of D's blocks; U's are the same fields of track U. Any common token → status `FAIL_TECHNICAL/SEED_SCOPE`. Returns `{"status", "common"}` |
| `g0d(out, stage, auth=None, sched=None, root=ROOT) -> dict` | KD0 (stage `"KD"`) and SAMPLE gate 0 (stage `"SAMPLE"`), in order. (i) Each addendum of CONTRACT `authority.kd0_addenda` at `root/path`: absent → `INCONCLUSIVE/RESOURCE_OR_AUTHORITY`; sha differs → `FAIL_TECHNICAL/AUTHORITY`. The run approval: path TO_FREEZE or absent → `INCONCLUSIVE/RESOURCE_OR_AUTHORITY`; its sha256 must equal CONTRACT, `auth["run_approval_sha256"]` and FREEZE.json `run_approval_sha256`, else `FAIL_TECHNICAL/AUTHORITY`. The design-freeze record sha. (ii) Every `identity.rows` path re-hashed: absent → `INCONCLUSIVE/RESOURCE_OR_AUTHORITY`; differs → `FAIL_TECHNICAL/IDENTITY`. HANDOFF `Z_bound` == RESULT `Z_bound` == CONTRACT `identity.Z_bound` (exact Fraction), else IDENTITY. (iii) `ns = read_json(namespace)`; `overlap_check(ns)`; `hits = seed_search_d(root, own + other)`; `res = hwsc_known.classify_hits_c(hits, fragments=CONTRACT seeds.g0_declaration_fragments, job_scratch=[])`. (iv) `hwsd_records.lineage_d(out)` (an absent store passes; a store may hold only this lineage's recorded files). (v) Writes `stages/<stage>/G0D.json` = res (exclusive). `res` not PASS → raise `FAIL_TECHNICAL/SEED_SCOPE`. (vi) `hwsc_records.sched_ok(sched, stage)` not ok → `INCONCLUSIVE/RESOURCE_OR_AUTHORITY`. Returns the checks |
| `ident_d(masters=MASTERS, steps=STEPS, hwsc=HWSC_STORE, handoff=None) -> dict` | KD1, H1-D part 1 and SCORE-IDENT (§3.2); metadata only, no Checkpoint load. `rel_b = read_json(hwsc/"RELEASE_B.json")`. For each j: `sha, rec = read_train_record(j, hwsc)`; `sha == rel_b["train_records"][str(j)] == hwsd_readers.stage_complete_sha(hwsc/"STAGES.jsonl", f"stages/TRAIN/{j}/TRAIN_RECORD.json", f"TRAIN_{j}")`; `rec["status"] == "COMPLETE"`. For each step: `CHECKPOINTS[(j, step)]["id"] == rec["checkpoint_ids"][str(step)]` and `payload_sha256 == rec["checksums"][str(step)]`; `meta = k4b_driver.checkpoint_meta(hwsc/"artifacts", id)`; `k4b_config.check_checkpoint_meta(meta, hwsc_gates.expected_meta_c(j, step, rec))` PASS; the init seed `meta["seed_map"][init_seed_key]` is equal across the master's steps. Finally `hwsc_gates.exclusion_check(all ids, handoff)["ok"]`. Any failure → `C1GateFailure("FAIL_TECHNICAL/IDENTITY", …)`. Returns `{"n": len(masters) * len(steps), "per_master": {j: {"train_record_sha256", "init_seed"}}}` (no value) |
| `kd2() -> dict` | (a) Inside `bound_hwsd(load_table(which="identity"))`, on the KD2 synthetic fixture (decision 15), `chart_one`, `controls_one`, `arrays_one(planted=True)`, `k4b_stats.model_status`, `k4b_cert.F_plan`/`margin` and `sample_block_d` return `==`/bitwise what the unbound calls return. (b) Inside `bound_hwsd()`: `audit()` PASS; the first 64 `integers(0, 2**63)` of `k4b_data.history_generator("cal", 0)` equal those of `SeedTree(0).generator("data", "hwsd-v1", "cal", 0, *PROCESS)` and differ from the same with `"hwsc-v1"`. (c) After exit every table attribute `is` its pre-entry object. PASS iff all. When called inside a job binding, it runs under `hwsc_bind.suspended()` |
| `c0_val_line(gates_path) -> dict` | Reads `hwsc-store/GATES.jsonl` line by line (`json.loads`) and keeps the single line with `gate == "C0-VAL"`. Not exactly one → `C1GateFailure("FAIL_TECHNICAL/KNOWN_CASE")`. Every other line is discarded at once, never logged or returned. Returns that line's `c0_val` details (per-model fidelity, support, bins, resultant) |
| `repro_c(out, hwsc=HWSC_STORE) -> dict` | KD3. Runs under `hwsc_bind.suspended()`, then `hwsc_bind.bound_stage_c()`. A write guard (decision 13) refuses any write under `hwsc` with `FAIL_TECHNICAL/KNOWN_CASE`. Reads only CONTRACT `known_cases.KD3.reads`. Steps: `proc = hwsc_data.build_process_c(ArtifactStore(MemoryBackend()))`; tables S3 cal, val and S7 test via `read_k4b_table`-checked `np.load` (sha256 == STAGE_COMPLETE entry); `m32_cal = k4b_scores.oracle_moments(..., cal canon32, ...)[32]` (stage C's `ORACLE_cal.npz` not read); six models through `k4b_driver.load_checkpoint` with `ARTIFACTS = hwsc/artifacts` (the stage-C binding sets it). **(a0)** the hwsd activation path on the six step-0/5000 checkpoints and the S3 cal table is bitwise equal to the stored `ACTS_cal_b0.npz` keys `f"{j}_step5000"`, `f"{j}_step0"`. **(a)** `chart_one` with ledgers `out/stages/KD/REPRO/<j>/s<step>/CHART_CONSTRUCTIONS.json`: step 5000 serial == `CHART_<j>.npz` and decoder == `DECODER_<j>.npz` bitwise; step 0: 620301 == `INIT_CHART_620301.npz`; 620302 and 620303 give C0-CAL not PASS with the reason recorded in `PRODUCTION_FROZEN.json` `init_status`. **(b)** step-5000 C0-VAL fidelity, support, bins and resultant equal `c0_val_line(...)` per model. **(c)** X± on the S7 rows, `k4b_stats.joint_bootstrap({X:j:-, X:j:+ for the 3 models at step 5000}, 620313)` and `k4b_stats.bounds` give L, U equal (float `==`) to RESULT `per_model.<j>.L`, `.U`; for 620301 at step 0, equal to `controls.init.620301.alpha_bound`, `.one_minus_alpha_bound`. F is not recomputed. PASS iff all |
| `kd5() -> dict` | `w0 = hwsb_known.w0_process()`; `r = hwsb_kb.kb6(w0, None)`. Requires `r["ids_ok"]` and `abs(r["G_C"] − 0.2648737252067266) ≤ 1e-12`; the trained-checkpoint leg is not run (decision 17). Planted cases on q from `hwsb_eval.oracle_predictives(w0, the KB6 test canon32, (1, 4))`: `b1(q, q[32])["captured"]` within 1e-12 of 1; `b1(q, q[1])["captured"]` within 1e-12 of 0; `forcing(q[32], q[4], q[4])["d_mean"] == 0`. PASS iff all |
| `kd6(job) -> dict` | `python -s -m pytest tests/hwsd/test_a_known_bound.py -p no:cacheprovider -q --junitxml <basetemp>/kd6.xml --basetemp X:/Downloads/topo-scratch/test_hwsd-<job>/pytest` as a subprocess (`PYTHONPATH=<worktree>/src`, TEMP under the same folder). PASS iff exit code 0 and the junit file reports ≥ 1 test, 0 failures, 0 errors |
| `run_kd(out, auth, sched, job, attempt=1) -> dict` | Items in CONTRACT `known_cases.order`, each recorded as a gate: KD0 `g0d(out, "KD", auth, sched)`; KD1 `ident_d()`; KD2 `kd2()`; KD3 `repro_c(out)`; KD4 `hwsd_dry.seq_cases(out=out/"stages"/"KD"/"SEQ")` (in-memory rows; status PASS iff every case and sequence meets its expectation); KD5 `kd5()`; KD6 `kd6(job)`. A pause check runs at every item boundary. The first failure stops: KD0 keeps its own status, every other item gets `FAIL_TECHNICAL/KNOWN_CASE`, and later items are NOT_RUN. Writes `stages/KD/KD_RECORD.json`, `complete_stage(out, "KD", [KD_RECORD, G0D.json, the REPRO ledgers])`, then `write_obligation(out, f"REGISTRY_OBLIGATION_{job}-a{attempt}.json", …)` (no array file is expected; decision 8) |

## 10. `hwsd_records.py`: records, lineage, freeze, S0, preflight, budget, H-1

| Name | Contract |
|---|---|
| reused | `hwsc_records.status_of`, `run_gates_c`, `superseded_ok`, `sched_ok`, `record_gate_files`, `utc`, `ledger_append` (unchanged; called through the module) |
| `RECORD_FILES_D` | `k4b_release.RECORD_FILES` ∪ {`FREEZE.json`, `KD_ACCEPT.json`, `ACCEPT_SAMPLE.json`, `REGISTRY_OBLIGATION.json`}; patterns `AUTH_*.json`, `SCHED_*.json`, `ACCEPT_*.json`, `DECISION_*.json`, `REGISTRY_OBLIGATION_*.json`; free folders `logs`, `operations`, `tmp`, `tmp-*`; `reservations/` holds only files named `RES-HWSD-W2-a<k>.json` or `RES-HWSD-W2-a<k>.END.json` |
| `lineage_d(out) -> dict` | Mirror of `hwsc_records.lineage_c` with `RECORD_FILES_D`: an absent store → PASS; `superseded/<job>-a<k>/` is checked by its `SHA256SUMS` (`superseded_ok`); every other file must equal (sha256) a file recorded by a `STAGE_COMPLETE` event (later events win); else `C1GateFailure("FAIL_TECHNICAL/LINEAGE", "unrecorded files: …")`. A file in `reservations/` with any other name → LINEAGE |
| `auth_ok_d(auth, stage, freeze=None) -> dict` | `{"ok", "reason"}`. ok iff `stage in auth["stages"]`, `auth["owner_auth_sha256"] ==` CONTRACT addendum-37 sha256, and, for every stage except DRY, `auth["run_approval_sha256"] == freeze["run_approval_sha256"]`. A missing record → ok False |
| `implementation_files_d(repo, h_exec) -> dict` | `{path: sha256 of the git blob}` for every file of `tools/hwsd` and `tests/hwsd` at `h_exec` |
| `freeze_d(out, repo, h_exec, dry_report, pf_record, kd4_params, run_approval) -> dict` | Writes `out/FREEZE.json` (exclusive) with CONTRACT `freeze_fields`. The `freeze_c` rules apply: reuse files re-hashed at h_exec (mismatch → `FAIL_TECHNICAL/FREEZE`); the dry report's `implementation_sha256` must equal this one; `kd4_parameters_sha256` = sha256 of the KD4 parameter record fixed in DRD4 |
| `verify_freeze_d(out, repo=REPO) -> dict` | Every FREEZE hash re-checked against the working tree (implementation files, CONTRACT/API/TEST_PLAN, protocol); `git diff --name-only h_exec -- <s0.protected_paths>` empty. Missing FREEZE → `C1GateFailure("INCONCLUSIVE/RESOURCE_OR_AUTHORITY")`; a mismatch → `FAIL_TECHNICAL/FREEZE` |
| `s0_d(repo, r_ref, h_exec) -> dict` | CONTRACT `s0` rule. `{"status": "PASS" or "INVALID", "offending", "hash_mismatch", "protocol_sha256", "r_ref", "h_exec"}` (INVALID: do not run; not an outcome) |
| `preflight_d(out, stage, auth, sched, repo=REPO) -> dict` | The `hwsc_records.preflight` pattern with `verify_freeze_d` and `auth_ok_d`. A refusal records gate `FREEZE`, `AUTH` or `SCHED` = `INCONCLUSIVE/RESOURCE_OR_AUTHORITY` and returns `{"refused": True}` before anything is sampled or loaded |
| `central_d(stage)`, `cumulative_d(stage)` | CONTRACT `cpu.central_s[stage]`, `cpu.cumulative_central_s[stage]` (float); unknown stage → `ValueError` |
| `pause_check_d(stage, stage_cpu, cum_cpu, job_cpu=None) -> dict` | `st = 3·central_d(stage)`, `ct = 3·cumulative_d(stage)`; for SCORE also `mt = 3·800 = 2400` against `job_cpu`. `pause = stage_cpu > st or cum_cpu > ct or (stage == "SCORE" and job_cpu > mt)` (strict). `trigger` is the `+`-joined names of the true conditions among "STAGE", "CUMULATIVE", "MODEL", or None. Returns `{"pause", "trigger", "stage_cpu", "stage_threshold", "cum_cpu", "cum_threshold", "job_cpu", "model_threshold"}` |
| `pause_or_raise_d(out, stage, t0, ledger_path=None, cont=None) -> None` | `ledger_path=None` disables it (dry and tests). A `cont` JSON `{"stages": [...]}` naming the stage exempts it. `stage_cpu, cum_cpu = hwsb_driver.running_cpu(stage, ledger_path=ledger_path, t0=t0)`; `job_cpu = time.process_time() − t0`. On pause: STAGES event `PAUSE`, gate `f"PAUSE_{stage}"` status `PAUSE` with only the CPU fields of `pause_check_d` (no value), then `raise hwsb_driver.Paused` |
| `ledger_init(path) -> dict` | Absent → writes `{"study": "hwsd-v1", "entries": [], "cumulative_cpu_s": 0.0}` (exclusive). Present with another study → `C1GateFailure("FAIL_TECHNICAL/LEDGER")`. Returns the ledger |
| `ledger_append_d(path, label, job, stage, cpu_s, source, master=None) -> dict` | `ledger_init(path)`; `stage` must be in CONTRACT `cpu.stage_order` (`ValueError`); then `hwsc_records.ledger_append(...)` (a duplicate label → `FAIL_TECHNICAL/LEDGER`) |
| `no_value_check(obj) -> None` | Recursive over dicts, lists and tuples. Any dict key in CONTRACT `records.value_keys` → `C1GateFailure("FAIL_TECHNICAL/SEALING", key)` |
| `acceptance_check(rec) -> None` | The closed schema of CONTRACT `records.SCORE_ACCEPTANCE`. The top-level key set equals `keys`. `counts` has exactly the four statuses with int values summing to 12. `fail_technical` is None or a str starting `FAIL_TECHNICAL/`. `files_sha256` is a `{str: 64-hex}` map. Then `no_value_check(rec)`. Any defect → `FAIL_TECHNICAL/SEALING` |
| `archive_attempt_d(out, job, attempt, files, suffixes=None) -> Path` | `k4b_release.archive_attempt(out, f"{job}-a{attempt}", files, suffixes)` (X-3; SHA256SUMS) |

## 11. `hwsd_driver.py`: jobs and CLI

Every job: `preflight_d` (refusal → exit 2), then the whole job inside `bound_hwsd()` with gate `BINDING_AUDIT` = `hwsd_bind.audit()` first (non-PASS → recorded, then `C1GateFailure`). Gates run through `hwsc_records.run_gates_c` (the first non-PASS stops; later gates NOT_RUN). A pause check (`pause_or_raise_d`) runs after every gate and at every item boundary. Every job ends with its obligation (§3.4) and its stage-gate files recorded (`record_gate_files`).

| Name | Contract |
|---|---|
| `run_kd(out, auth, sched, job, attempt=1) -> dict` | preflight `"KD"`, then `hwsd_known.run_kd` inside `bound_hwsd()` |
| `run_sample(out, auth, sched, job, attempt, kd_accept, root=ROOT, scratch=SCRATCH) -> dict` | §15.2 |
| `run_score(out, auth, sched, job, attempt, master, accept_sample, cont=None) -> dict` | §15.3 |
| `run_summary(out, auth, sched, job, attempt, accepts) -> dict` | §15.4 |
| `run_close(out, status, reason, job, attempt) -> dict` | After an early stop: `stages/CLOSE/CLOSE.json` = `{"outcome": summary.outcome_d(state from GATES.jsonl), "reason"}` (no value); `complete_stage(out, "CLOSE", [it])`; obligation |
| `inventory(root, save=None, compare=None) -> dict` | `k4b_registry.inventory(root, exclude=CONTRACT registry.deep_scan_exclude)` reduced to `{top: {history_files, identity_refs, observation_set_roots, unreadable}}` (headers only). `save` writes it; `compare` reports added entries (the before/after check of the dry run) |
| `main(argv=None) -> int` | Subcommands `s0`, `audit`, `kd`, `sample`, `score`, `summary`, `close`, `dry`, `freeze`, `inventory`, `obligation` (the J10 item 4 recovery: writes the obligation of a given store; coordinator step). Options `--out` (default `STORE`), `--auth`, `--sched`, `--kd-accept`, `--accept`, `--master`, `--job`, `--attempt`, `--continue`, `--reason`, `--h-exec`, `--r-ref`, `--dry-report`, `--pf-record`, `--kd4-params`, `--run-approval`, `--save`, `--compare`, `--store`, `--only`. Record arguments are paths, loaded as JSON. `audit` enters `bound_hwsd()`, runs `audit()`, writes `<out>/AUDIT.json`, and exits 0 iff PASS. Exit codes: 0 complete; 2 refused (nothing loaded or sampled); 3 STOP (FAIL_TECHNICAL); 4 PAUSE; 5 INCONCLUSIVE |

## 12. `hwsd_dry.py`, `hwsd_dry2.py`, `hwsd_dry3.py`: the synthetic dry run (§10) and KD4

| Name | Contract |
|---|---|
| `drd1(out, ctx)` … `drd14(out, ctx)` | One function per case of TEST_PLAN §4. DRD1–DRD7 are in `hwsd_dry`, DRD8–DRD11 in `hwsd_dry2`, DRD12–DRD14 in `hwsd_dry3`. Each returns `{"status": "PASS" or "FAIL" or "NOT_RUN", "reading": "EXACT" or "VALUE", "details"}`. Streams come only from the dry scopes (`hwsd-dry-v1/<case>`), with masters 629951–629953 and seeds 629961–629965. DRD5 and DRD6-type checks also use 620413 and 620416 on synthetic arrays only (decision 14). Planted fixtures carry `"fixture": true` |
| `case_dir(out, case) -> Path` | `out/case/<utc YYYYMMDDTHHMMSSZ>`, created fresh |
| `fixture_root(job, case) -> Path` | `SCRATCH/f"test_hwsd-{job}"/"dry"/case`. Every synthetic project root, synthetic scratch root, planted unreadable or unknown array and synthetic stage-C dry case lives here, never in the hwsd-dry store (decision 6) |
| `in_memory_rows(case, n, splits=SPLITS, process=PROCESS) -> dict` | w\* DRY rows kept in memory: `sample_tables(proc_star, scope=f"hwsd-dry-v1/{case}", process=PROCESS, sizes={s: n for s in splits})` with `proc_star = hwsc_data.build_process_c(ArtifactStore(MemoryBackend()))`. Never persisted |
| `plant_acts(case_id, table, m, params) -> np.ndarray [n, 128]` | Planted float64 activations for a KD4 case. Coordinates 0 and 1 carry the signal; all 128 coordinates get isotropic Gaussian noise `params["noise"][case_id] · N(0, 1)` from `np.random.Generator(np.random.PCG64(params["seeds"][case_id]))`. `u(id) = int(sha256(str(id))[:16], 16) / 2**64` is a fixed function of the sequence id. **(i)** `x0 = u(id)`, `x1 = 0` (segment; noise ≤ 1e-6). **(ii)** `θ = k4b_scores.m4_phase(m[4])`. **(iii)** `θ = k4b_scores.oracle_phase(m[32])`. **(iv)** `θ = g(oracle_phase(m[32]))`, with g piecewise linear and monotone: `[0, 2π·a)` maps onto `[0, π/6)` and `[2π·a, 2π)` maps onto `[π/6, 2π)`, where `a = params["g_mass"]` (planned 0.01). **(v)** `θ = 2π·u(id)`. For (ii)–(v), `x0 = cos θ`, `x1 = sin θ` |
| `seq_cases(out, params=None, cases=None, sequences=None, rows=3072) -> dict` | KD4 and DRD4. Runs under `bound_hwsd(load_table(which="dry", case="KD4", case_dir=out, process=PROCESS))`. `params` defaults to the frozen KD4 parameter record (TO_FREEZE; DRD4 measures and records it). For each case it scores one checkpoint through the real `hwsd_score.score_checkpoint` with `acts = lambda split: plant_acts(case, tables[split], moments[split], params)`, `planted=True`, a planted `learn = {"learn_pass": False, "B2_L_zS": -1.0, …}` and a fresh ledger under `out/<sequence>/<k>/`. The moments for cal, val and test come from `k4b_scores.oracle_moments` on the in-memory rows. Each sequence of CONTRACT `known_cases.KD4.sequences` is built from its case checkpoints in order (`k = 1..K`) and summarised through `hwsd_summary.strong_bounds` / `k4b_stats.bounds` on the dry seeds with `F = F_PLANTED`; then `hwsd_statements.evaluate` runs with the same rows for all three dry masters. Expected readings are in §17.3. The result holds every case's status, label, point and SE and every sequence's ORDER and D2/D3/D6 readings, with `status` PASS iff all match |
| `run_dry(out=DRY_STORE, sched=None, only=None, job=None) -> dict` | Requires `hwsc_records.sched_ok(sched, "DRY")` (W2 only), else `{"status": "REFUSED"}` with nothing run or written. Runs the cases (or `only`) and writes `out/stages/DRY/DRY_REPORT.json` (exclusive): `{"cases", "all_pass", "implementation_files", "implementation_sha256", "h_exec", "tree_clean", "kd4_parameters", "inventory_before", "inventory_after"}`. Then `out/REGISTRY_OBLIGATION.json`, or for a later job in the same store `REGISTRY_OBLIGATION_<job>-a<k>.json` (J4). Never writes `HIST_*.npz`; never issues a real-scope stream or a real master |

## 13. `hwsd_meter_bind.py`: meter binding (§11.3; DRD12)

| Name | Contract |
|---|---|
| `job_paths(job, kind) -> dict` | `kind == "test"` (J-D1, DRY): `out = SCRATCH/f"test_hwsd-{job}"`, `temp_root = out`, `basetemp = out/"pytest"`. `kind == "store"` (KD, SAMPLE, SCORE, SUMMARY): `out = STORE`, `temp_root = STORE/"tmp"`, `basetemp = None`. Else `ValueError` |
| `memory_cap(stage) -> int` | CONTRACT `resources.memory_cap_bytes[stage]` (J-D1 8 GiB; DRY, KD, SAMPLE 12 GiB; SCORE, SUMMARY 8 GiB); unknown → `ValueError` |
| `bind(job_id, task_sha256, out, worker_session, stage, temp_root=None) -> None` | `k4b_meter_bind.bind(job_id, task_sha256, out, worker_session)`; `winjob.MEMORY_CAP = memory_cap(stage)`; `k4b_meter_bind.TEMP_ROOT = str(temp_root or out)`; `meter.CAP_S = meter.STOP_NEW_S = inf`; `meter.OUTPUT_CAP = CONTRACT resources.output_cap_bytes` (8 GiB, compared with the whole out folder) |
| `placement_ok(paths, root=ROOT) -> dict` | As `hwsc_meter_bind.placement_ok` with STORE = hwsd-store. Kind test: `out_outside_root`, `temp_outside_root`, `basetemp_outside_root`, `test_prefixed` (out directly under SCRATCH, name starting `test_hwsd-`). Kind store: `out_is_store`, `temp_under_store_tmp` |
| `child_env_d(job) -> dict` | `k4b_meter_bind.child_env(job)` with its TEMP folder created (the D-0177-1 fix) |
| `effective_settings() -> dict` | `{"memory_cap", "temp_root", "ledger", "cap_s", "output_cap", "thread_vars"}` |
| `main() -> int` | The `hwsc_meter_bind.main` pattern: `--job`, `--task-sha256`, `--session`, `--kind`, `--stage` are all required (missing or unknown → 2); exit 3 when `RUN.lock` names another session; `op_guard.archive_stale(out)` when `METER_ACTIVE.lock` is absent; `meter.limit_reason = k4b_meter_bind.make_limiter(op_marker=out/op_guard.MARKER)`; `os.environ.update(child_env_d(job))`; `sys.argv = [argv0] + k4b_meter_bind.rewrite_argv(rest)` (`--max-cpu inf --max-wall inf`); `return meter.main()`. Disk safe-STOP (C: ≥ 2 GB, X: ≥ 30 GB) and op-guard precedence are `k4b_meter_bind`'s |

## 14. Reused functions (unchanged; file hashes in CONTRACT `reuse_sha256`, blob bytes at e3710d2)

| Module | Names used under hwsd |
|---|---|
| `hwsc_bind` | `bound_stage_c(table)`, `suspended()`, `audit(modules, left_unchanged, forbidden)`, `decode` (pattern), `ACTIVE` |
| `hwsc_data` | `build_process_c`, `process_identity`, `block_generator`, `block_ids`, `save_table`, `separation_c`, `p_d2a_check` |
| `hwsc_gates` | `expected_meta_c`, `exclusion_check`, `law_identity` |
| `hwsc_registry`, `hwsc_registry_build`, `hwsc_scratch`, `hwsc_drystore` | `source_dry`, `source_own`, `source_c2nd`, `source_hwsb`, `source_scratch_c`, `_new`, `_close`, `ARRAYS`, `STAGE_B`; `build(version, out_dir, …, sources=…)`; `_classify` (via `scratch_scan_d`); `check_store`, `_os_parent_ok` (mirrored) |
| `hwsc_known` | `needle_in`, `classify_hits_c(hits, fragments, job_scratch)` |
| `hwsc_records` | `status_of`, `run_gates_c`, `superseded_ok`, `sched_ok`, `record_gate_files`, `utc`, `ledger_append` |
| `hwsc_config` | `load_handoff`, `blinded`, `public_summary`, `CONTRACT` (stage-C tables, read) |
| `k4b_charts` | `build_chart`, `extend`, `determinism_check` |
| `k4b_scores` | `oracle_moments`, `endpoint_arrays`, `secondary_arrays`, `naive_scores`, `phase_scores`, `m4_phase`, `sha_phase`, `oracle_phase`, `support_report` |
| `k4b_cert` | `references`, `moment_check`, `envelopes`, `endpoint_bounds`, `control_bounds_all`, `certify`, `b_num`, `margin`, `F_plan`, `b4_guard`, `norm_bound` |
| `k4b_decoder` | `fit`, `predict_phase`, `agreement`, `to_arrays`, `from_arrays` |
| `k4b_stats` | `joint_bootstrap`, `bounds`, `model_status`, `ratios` |
| `k4b_data` | `history_table`, `history_generator` (KD2), `model_inputs`, `seq_disjoint`, `predicate_check`, `duplicates` |
| `k4b_driver`, `k4b_fresh`, `k4b_release`, `k4b_registry`, `k4b_config` | `begin_stage`, `complete_stage`, `checkpoint_meta`, `load_checkpoint`; `load_recorded`, `control_summary`; `start_reservation`, `verify_reservation`, `archive_attempt`, `regenerated_identical`, `RECORD_FILES`; `inventory`, `classify`; `chart_cfg`, `check_chart_equality`, `check_checkpoint_meta` |
| `c1_chart`, `c1_means`, `c1_model`, `c1_cert`, `c1_records` | `ConstructionLedger`, `c0_val`, `serialise`; `bootstrap_means`, `tree_mean`, `quantile_with_rank`, `rank_for`, `rank_check`; `load_model64`, `activations`; `a1_selftest`; `C1GateFailure`, `adapt_chart_exception`, `classify_exception` |
| `hwsb_eval`, `hwsb_known`, `hwsb_kb`, `hwsb_driver`, `hwsb_config` | `model_predictive`, `oracle_predictives`, `b1`, `forcing`; `w0_process`; `kb6`; `running_cpu`, `Paused`; `dry_plan`, `Z_B23`, `Plan` |
| `c2_registry`, `reference_cache`, `op_guard`, `stage_records`, `scores` | `Registry`, `_violation`; `identity`; `timed_factory`, `archive_stale`, `MARKER`; `sha256`, `write_new`, `save_npz`, `record_gate`, `stages_so_far`, `gates_so_far`; `history_digests`, `r4_norms` |

**Never called under hwsd:** CONTRACT `binding.never_called`. This includes `k4b_driver.{g0, h1, reg1, h2, p1, c0_cal_stage, c0_val_stage, cert_val, oracle_val, b4_val}`, `k4b_fresh.{sample_test, h2_fresh, t_pre, endpoint, export}`, `k4b_charts.{c0_cal, init_charts, freeze_production, c0_val_gate}`, `k4b_scores.control_arrays`, `hwsc_data.{sample_block_c, sample_lgate, sample_eval}`, `hwsc_gates.h1c` (it reads a whole TRAIN record) and `hwsc_registry_build.obligation` (J1). These are named as bitwise references in tests and DRD14, which is allowed: they are never called by hwsd job code.

## 15. The jobs and every gate's computation, in order (§7)

Conventions: exact Fractions and strict inequalities. Run-level gates stop the job at the first non-PASS (later gates NOT_RUN), except B4-TEST (decision 9). Per-checkpoint statuses never stop the run. Every computed value is recorded in the job's stage files; the SCORE acceptance record carries none.

### 15.1 KD job (once, after the freeze and the run approval)

Gates `FREEZE`, `AUTH`, `SCHED` (preflight), `BINDING_AUDIT`, then KD0–KD6 as §9 `run_kd`. Failure statuses: KD0 → its own; KD1–KD6 → `FAIL_TECHNICAL/KNOWN_CASE`. Writes `stages/KD/*` and `REGISTRY_OBLIGATION_<job>-a<k>.json`. The coordinator then writes `KD_ACCEPT.json` `{"accept": true, "kd_record_sha256", "by", "utc"}`.

### 15.2 SAMPLE job

| # | Gate | Computation | Pass reading | On failure |
|---|---|---|---|---|
| — | FREEZE, AUTH, SCHED, BINDING_AUDIT | `preflight_d`; `audit()` | all PASS | refused (exit 2) / `FAIL_TECHNICAL/BINDING` |
| — | KD_ACCEPT | `kd_accept["accept"] is True` and `kd_record_sha256 == sha256(stages/KD/KD_RECORD.json)`, whose status is PASS | holds | refused, `INCONCLUSIVE/RESOURCE_OR_AUTHORITY` |
| 0 | G0D | `hwsd_known.g0d(out, "SAMPLE", auth, sched)` | PASS | as §9 |
| — | RESERVATION | `a = w2_attest(root)` must be PASS (else `INCONCLUSIVE/AUTHORITY`, nothing started); written to `stages/SAMPLE/W2.json`. Then `start_reservation_d(out, attempt, utc)` | started | `INCONCLUSIVE/AUTHORITY` |
| 1 | H1D | `ident_d()` (36 rows); `store = ArtifactStore(LocalFSBackend(out/"artifacts"))`; `proc = hwsc_data.build_process_c(store)`; `hwsc_data.process_identity(store, proc)["ok"]`; the EmissionSpec ids `proc["ids"]` per master equal every TRAIN record's `process_ids`; `law = hwsc_gates.law_identity(proc, handoff)` (BOUNDED, Z == HANDOFF Z_bound); `law["Z_bound"] == Fraction(CONTRACT identity.Z_bound) == Fraction(RESULT.json Z_bound)`; `k4b_cert.F_plan(Z) == handoff["F_plan"]`; `hwsc_data.p_d2a_check(proc, handoff["p_D2a"])["ok"]`; `c1_cert.a1_selftest()`; `torch.get_num_threads() == 1`. Writes `stages/SAMPLE/H1D.json` | all hold | `FAIL_TECHNICAL/IDENTITY` or `/LAW_BOUND`; then the stopped-job rule below |
| 2 | REGD | `w = hwsd_registry.build_d(out/"registry", root, scratch, handoff)` | `w["status"] == PASS` | `INCONCLUSIVE/REGISTRY_INCOMPLETE` or `FAIL_TECHNICAL/LINEAGE`, before any draw; then the stopped-job rule |
| — | S3D | `verify_reservation_d(res, rid)` PASS (else stop before any row); `begin_stage(out, "S3")`; `tables = sample_tables(proc)`; `save_tables(out, tables)`; `complete_stage(out, "S3", paths)`; `write_obligation(out, "REGISTRY_OBLIGATION.json", job, attempt, utc, reservation_id=rid)`; `end_reservation(out, rid, utc, that path)` | written, ended | a reservation breach before the first row: cancel (stopped-job rule); after the first row: `FAIL_TECHNICAL/LINEAGE`, the obligation is still written and the reservation ended before exit |
| 3 | H2D | `reg = hwsd_registry.load_d(out)`; `separation_d(reg, tables)`; `registry_risk_d(proc p_D2a)["ok"]`. Writes `stages/SAMPLE/H2D.json` | 0 collisions, 0 predicate hits, ids disjoint, risk ok | `FAIL_TECHNICAL/LINEAGE`; `INCONCLUSIVE/REGISTRY_INCOMPLETE` |
| 4 | ORACLE-D | `o = oracle_d(proc, tables)`; `save_oracle`; `stages/S4/REFS_test.json` = `refs_to_json(o["refs_test"], proc, sha256(HIST_test_b0.npz))`; `ORACLE_D.json` = `{"max_gap", "n_checked"}`; `complete_stage(out, "S4", files)` | every checked row ≤ MOMENT_TOL | `FAIL_TECHNICAL/ORACLE` |
| 5 | B4-TEST | `g = b4_test(o["moments"]["test"], o["refs_test"], k4b_cert.envelopes(), Z)` (seed 620414); `stages/S4/B4_TEST.json`; `shared = shared_controls(...)`; `save_shared` | `g["status"] == PASS` | recorded (`INCONCLUSIVE/HEADROOM` or `/NUMERICAL`); the job **continues**; SUMMARY reads it (decision 9) |
| 6 | LGATE-ORACLE | `q = lgate_oracle(proc, tables["lgate"]["canon32"])`; `save_lgate_q` | finite, rows sum to 1 within 1e-6 | `FAIL_TECHNICAL/NUMERICAL` |
| — | end | `record_gate_files(out, "SAMPLE", […])`; `complete_stage(out, "S4", …)` for the B4/LGATE/SHARED files; `write_obligation(out, f"REGISTRY_OBLIGATION_{job}-a{attempt}.json", …)` (decision 8) | — | — |

**Stopped-job rule (J10 item 3; F-1).** If the job stops after `start_reservation_d` and before the first row (H1D, REGD or the reservation check fails), it calls `stop_obligation(out, job, attempt, rid, utc)` before exit. A rerun uses `attempt + 1`, so a new reservation id and a new file.

The coordinator then writes `ACCEPT_SAMPLE.json` `{"verdict": "ACCEPT", "sample_files_sha256": {relpath: sha256 of the S3/S4/SAMPLE files}, "by", "utc"}`.

### 15.3 SCORE job (one per master, in MASTERS order)

| # | Gate | Computation | Pass reading | On failure |
|---|---|---|---|---|
| — | preflight, BINDING_AUDIT | as above | PASS | refused / BINDING |
| — | ACCEPT_SAMPLE | verdict ACCEPT and every listed file re-hashes | holds | refused |
| 7 | SCORE-IDENT | `s0_d` is the coordinator's dispatch check; here: `ident_d(masters=(j,))`; every ACCEPT_SAMPLE file and the S3/S4 files re-hash against STAGES (`k4b_fresh.load_recorded` pattern); `stages/SCORE/<j>/` must not hold a `CHECKPOINT_RECORD.json` (an interrupted attempt is first archived by `archive_attempt_d`, X-3). Writes `stages/SCORE/<j>/SCORE_IDENT.json` | all hold | `FAIL_TECHNICAL/IDENTITY` or `/LINEAGE` |
| 8–10 | CHECKPOINTS | `ctx` from `load_tables`, `ORACLE_*.npz`, `refs_from_json`, `LGATE_Q.npz`, `Z` from `H1D.json`, `cfg`, `timed = op_guard.timed_factory(out, 600)`; `run_checkpoints(ctx, j, pause)` (§6); the per-checkpoint status by §16 | recorded (not a gate); the gate status is PASS unless an exception was raised | `FAIL_TECHNICAL/*` (row 9 stop rule, non-finite phase, NaN predictive, P2) stops the run |
| 11 | DETERMINISM | `determinism_d(ctx, j, records)` | bitwise equal | `FAIL_TECHNICAL/DETERMINISM` |
| 12 | H-1 | `complete_stage(out, f"SCORE_{j}", every file under stages/SCORE/<j>/)`; `acceptance(...)` (closed schema and value-key check) | no value key, no per-checkpoint status list | `FAIL_TECHNICAL/SEALING` |
| — | end | obligation `REGISTRY_OBLIGATION_<job>-a<k>.json`. The printed output carries only the `counts`, any FAIL_TECHNICAL, the hashes and the CPU | — | — |

The coordinator writes `ACCEPT_SCORE_<j>.json` `{"verdict": "ACCEPT", "acceptance_sha256", "master", "by", "utc"}` after reading only `ACCEPTANCE.json`.

### 15.4 SUMMARY job

| # | Gate | Computation | Pass reading | On failure |
|---|---|---|---|---|
| — | preflight, BINDING_AUDIT, ACCEPT_SCORE | all three `ACCEPT_SCORE_<j>.json` verdict ACCEPT, each `acceptance_sha256` re-hashes | holds | refused |
| 13 | BOOTSTRAP | `inputs = bootstrap_inputs_d(load_scores(out), shared)`; `draws = main_bootstrap(inputs)` (seed 620413, 5,000 draws; ranks 84/4,917/125/4,875 through `k4b_stats.bounds`, each rank-checked); `sdraws = strong_bootstrap(scores)` (seed 620416, 50,000 draws, X± only; ranks 70/49,931 through `strong_bounds`) | finite, every rank check passes | `FAIL_TECHNICAL/NUMERICAL` |
| 14 | STATEMENTS | per checkpoint `checkpoint_row` (B_num, F, σ, strong bounds); `hwsd_statements.evaluate(table, headroom_ok=B4_TEST status == PASS)`; `report(...)` | report written | — |
| — | end | obligation | — | — |

**Outcome (§8.1).** `summary.outcome_d`: FAIL_TECHNICAL > INCONCLUSIVE/RESOURCE_OR_AUTHORITY (PARTIAL curves when one or two SCORE jobs completed; every statement NOT_EVALUABLE/RESOURCE) > INCONCLUSIVE/REGISTRY_INCOMPLETE > INCONCLUSIVE/HEADROOM (curves reported; statements NOT_EVALUABLE/HEADROOM) > HWSD_REPORT. A SCORE job's FAIL_TECHNICAL stops all later jobs until it is resolved under X-3.

## 16. Per-checkpoint statuses (§2.6, §7 row 9 and row 10)

| Status | Condition (in this order) | Label |
|---|---|---|
| CHART_UNAVAILABLE | C0-CAL not PASS (any non-PASS build status not starting with FAIL_TECHNICAL: INCONCLUSIVE, INCONCLUSIVE/CHART_UNAVAILABLE, INCONCLUSIVE/RESOURCE; gauge alignment not positive; native wall) | `CHART_UNAVAILABLE/<status>: <reason>`, or `CHART_UNAVAILABLE/NATIVE_WALL: <reason>` |
| UNCERTIFIED | production chart exists and `certify` status ≠ PASS (a primary row bound above 1e-4) | `UNCERTIFIED/<status>: <names>` |
| SCORED | C0-CAL PASS, certificate PASS, C0-VAL PASS | `SCORED` |
| SCORED_UNVALIDATED | C0-CAL PASS, certificate PASS, C0-VAL not PASS | `SCORED_UNVALIDATED/<status>: <reason>` (direct chart not PASS), `SCORED_UNVALIDATED/NATIVE_WALL: <reason>`, or `SCORED_UNVALIDATED/CRITERIA: <criteria>` |

- `valid` = C0-CAL PASS and C0-VAL PASS, independent of the certificate. `k_C` uses `valid`.
- A FAIL_TECHNICAL build or c0_val status, a non-finite phase, a P2 failure or a NaN predictive stops the run.
- The native wall: `timed` raises op_guard `Unresolved` after an operation that ran 600 s or longer. The construction is claimed and never retried.

## 17. Statements (§5; exact rules in §7 of this file)

### 17.1 How each status enters

- **SCORED:** everywhere.
- **SCORED_UNVALIDATED:** only through `above_s` (BEFORE at either anchor, D2 FALSE), through D2's INFORMATIVE qualifier (U^S + F+ < 1/100), and in the EST-loss diagnostic. σ = NA, so never WITH or AFTER, and never an onset (k_C uses `valid`, which is False).
- **CHART_UNAVAILABLE:** no arrays; never above or below; σ = NA; not counted in `n_pre`.
- **UNCERTIFIED:** NA everywhere (not est, not ok); UNCERTIFIED_AT_ANCHOR at an anchor; `valid` may still be True (k_C counts it).

### 17.2 Error statements and multiplicity

CONTRACT `statements.error_statements` and `statements.multiplicity` are copied verbatim into every report.

### 17.3 KD4 expected readings (each sequence evaluated with identical rows for all three dry masters)

| Sequence | ORDER at k_C | D2 | D3 | D6 |
|---|---|---|---|---|
| AFTER (i, ii, ii, iii, iii) | AFTER | NE BY_CONSTRUCTION | TRUE | TRUE |
| WITH (i, i, iii, iii) | WITH | NE BY_CONSTRUCTION | FALSE | TRUE |
| BEFORE (i, iv, iii, iii) | BEFORE | FALSE | FALSE | TRUE |
| NEVER (i, ii, ii) | NEVER | NE FINAL_NOT_SUPPORT | NE NEVER | NE NO_STRONG_CROSSING |
| NO_CHART (i, i, i) | NO_CHART | NE NO_CHART | NE NO_CHART | NE NO_STRONG_CROSSING |
| STEP0_CONTROL (ii, iii) | CHART_AT_INIT | NE CHART_AT_INIT | NE CHART_AT_INIT | NE NO_STRONG_CROSSING |

Case expectations:
- (i) CHART_UNAVAILABLE (NO_H1_BAR or GIANT).
- (ii) SCORED, EXCLUDE, point within ±4 SE of 0.
- (iii) SCORED, SUPPORT, point within ±4 SE of the Δ4^orc mean on the same rows.
- (iv) SCORED_UNVALIDATED (bins or resultant) and `above_s`.
- (v) SCORED, EXCLUDE.

A case whose measured status differs is redesigned in DRD4 before the freeze. If no planted fixture yields SCORED_UNVALIDATED through the unmodified chart code, the BEFORE route is checked by DRD5's planted tables only, and this is recorded in the KD4 parameter record.

## 18. Records and file schemas

- **AUTH** `AUTH_<stage>_<job>.json`: CONTRACT `records.AUTH`; **SCHED** `SCHED_<job>.json`: `records.SCHED`; **KD_ACCEPT**, **ACCEPT_SAMPLE**, **ACCEPT_SCORE_<j>**: as §15.
- **Reservation** `reservations/RES-HWSD-W2-a<k>.json`: `k4b_release.start_reservation` (`{"id", "scope", "start_utc", "end_utc": null, "state": "ACTIVE", "interruptions": [], "job_states": {}}`); **END** `reservations/RES-HWSD-W2-a<k>.END.json`: CONTRACT `reservation.end_fields`.
- **Obligation** `REGISTRY_OBLIGATION*.json`: CONTRACT `obligation` (§3.4).
- **G0D.json**: the `classify_hits_c` result. **H1D.json**: `{"identity": ident_d result, "process_identity" (ok, checks), "Z_bound": str, "F_plan": str, "p_D2a", "a1_selftest", "threads"}`. **H2D.json**: `separation_d` and the risk. **W2.json**: `w2_attest`.
- **ORACLE_D.json** `{"max_gap", "n_checked"}`; **B4_TEST.json** `{status, lower, rank, B_H, Z_bound, point, B_norm_max}` (Fractions as str); **REFS_test.json** §3.3; **SHARED_CONTROLS.json** §3.3.
- **LEARN.json**: CONTRACT `records.LEARN` (the `learning_one` dict; `B2_z`, `B2_zS` are the `forcing` dicts).
- **CHECKPOINT_RECORD.json**: CONTRACT `records.CHECKPOINT_RECORD`:
  - `{"master", "step", "k", "checkpoint_id", "status", "label", "valid"}`;
  - `"c0_cal": {"status", "reason", "diagnostics"}`, `"c0_val"` (§6 or null), `"decoder": {"status", "reason"}`;
  - `"certificate": {"status", "max_B": {X_minus, X_plus, n_hat as str}, "max_abs": {X_minus, X_plus}, "n", "planted"}` or null;
  - `"support"` (support_report) or null, `"decoder_agreement"`, `"controls_certified": {name: bool or {side: bool}}`;
  - `"arrays_sha256"`, `"frozen_sha256"`, `"learn_sha256"`, `"native_wall"`, `"planted"`.

  It is value-bearing: the coordinator does not open it before SUMMARY (H-1).
- **ACCEPTANCE.json**: CONTRACT `records.SCORE_ACCEPTANCE` (closed).
- **REPORT.json** (HWSD_REPORT): `{"outcome", "outcome_detail", "per_checkpoint": [36 rows], "onsets", "n_pre", "pre_chart_max", "order", "statements", "onset_order_line", "diagnostics", "readings_text", "error_statements", "multiplicity", "does_not_establish", "disclosure", "stage_c_reference", "B4_TEST", "seeds": {"main": 620413, "strong": 620416}, "ranks", "protocol_sha256", "freeze_sha256", "registry_obligation_sha256"}`.
- **KD_RECORD.json**: `{"status", "kd": {"KD0" … "KD6": {"status", "details"}}, "protocol_sha256", "freeze_sha256", "binding_audit"}`.
- **DRY_REPORT.json**: §12.
- **Study ledger** `agent-handoff/HWSD_CPU_LEDGER.json`: `{"study": "hwsd-v1", "entries": [{"label", "job", "stage", "cpu_s", "source", "master", "utc"}], "cumulative_cpu_s"}`.
- **Store layout**: CONTRACT `store_layout`.

## 19. Budget, pauses, caps (§11)

- Measure-only: `--max-cpu inf --max-wall inf`. Disk floors C: ≥ 2 GB, X: ≥ 30 GB. Native operation wall 600 s.
- Memory caps: J-D1 8 GiB; DRY, KD, SAMPLE 12 GiB; SCORE, SUMMARY 8 GiB. Output cap 8 GiB.
- Stage centrals (CPU-s): J-D1 700, DRY 250, REPEAT 3,800, KD 450, KD-REPEAT 450, SAMPLE 1,350, SCORE 2,400 (800 per master), SUMMARY 350. Cumulative centrals: 700 / 950 / 4,750 / 5,200 / 5,650 / 7,000 / 9,400 / 9,750.
- Triggers (strict >): stage CPU > 3 × central; running total > 3 × the cumulative central through the stage; for SCORE also the job's own CPU > 2,400. Checked at every item boundary (each KD item, each checkpoint, each gate). On a trigger no new item starts (exit 4); continuing needs the owner (`--continue`). Pause reports carry CPU fields only.
- Ledger stage labels: CONTRACT `cpu.ledger_stage_rule`. Labels are unique: `<job>-<stage>[-<master>]-a<k>`.

## 20. Implementation decisions (where the protocol leaves a detail open; each open to a coordinator ruling)

1. **Fifteen modules** instead of the ten of §12.1. `hwsd_readers` (R9/R10) is split from `hwsd_registry`, `hwsd_statements` (pure logic) from `hwsd_summary`, and `hwsd_records` from `hwsd_driver`; there are three dry modules. Each stays ≤ 400 lines, and every §12.1 name is reachable under its documented module.
2. **The inner registry lives at `hwsd-store/registry/K-REG1.json`**, not `registry/inner/`, because `c2_registry.Registry.load(store, version)` reads `<store>/registry/<version>.json`. The wrapper is `registry/K-REG-D.json`.
3. **The registry tables inherit the stage-C tables by reference.** They are bound by the sha256 of `tools/hwsc/CONTRACT.json` (af669ac2…), with hwsd rows overriding them, instead of copying 3.2 MB of `frozen_files`. A header-only re-scan on 2026-11-01 found no drift in the 175 inherited folder rows and the 9 `hwsc-dry-<job>` stores.
4. **hwsc-job-\* scratch folders** are blinded. The scratch scan lists their array files by name only (class `blinded_array`, never opened); their rows are TO_FREEZE for a coordinator name-only listing.
5. **Decimal test references are persisted** as `stages/S4/REFS_test.json` (schema `hwsd-refs-v1`), keyed by row position and bound to the sha256 of `HIST_test_b0.npz`, with no history content. `reference_cache.export_cache` is not used, because its entries contain history bytes, which would make a history-bearing JSON (J3 history format).
6. **Dry-run fixtures live outside the hwsd-dry store,** under `scratch/test_hwsd-<job>/dry/<case>/`: synthetic roots, planted unknown or unreadable arrays, and stage-C dry cases. Every array file in a hwsd-dry store is then classifiable under J10 and the hwsd-dry type rule.
7. **One obligation schema `hws-registry-obligation-v1`** (fields in CONTRACT `obligation`) is written by hwsd and read by R10 for track U. Its alignment with track U's writer is settled by joint ruling J11 (see section 22).
8. **SAMPLE writes two obligations:** `REGISTRY_OBLIGATION.json` right after the four tables (bound by the J8 end record) and `REGISTRY_OBLIGATION_<job>-a<k>.json` at job end, which also lists the later S4 arrays (J10 item 2). KD, SCORE, SUMMARY and CLOSE each write one at their end.
9. **B4-TEST does not stop the SAMPLE job.** It is recorded, LGATE-ORACLE still runs, SCORE and SUMMARY still run, and SUMMARY gives `INCONCLUSIVE/HEADROOM` with the curves and every statement NOT_EVALUABLE/HEADROOM. This reconciles §7 row 5 ("curves still produced") with the run-level stop rule.
10. **The outcome state** keys are `fail`, `resource`, `registry`, `headroom`, `partial` (§8.1 precedence).
11. **The native wall marker** is written at the job's store root (`op_guard.timed_factory(out, 600)`, out = the meter's `out`), so the meter's limiter (`op_marker = out/OPERATION_ACTIVE.json`) sees it. The protocol's "<job dir>" is read as the meter's out folder.
12. **Bootstrap draws are not persisted** (seeds and ranks are recorded; the draws are reproducible).
13. **KD3's write guard** wraps `stage_records.write_new`, `save_npz` and `Path.open` modes `w`, `x`, `a` for the duration of `repro_c`, refusing any target under `hwsc-store`.
14. **Dry strong-bound seed 629965** (the dry `val_projection` name, never used by hwsd code), so that no token outside the reserved list 629961–629965 is issued.
15. **KD2's synthetic fixture** is the HWSC KC7 fixture (§11.5 of the hwsc API: Dirichlet 12-state process from `default_rng(7)`, arrays from `default_rng(77)`). The chart, extension and decoder mirrors are compared on the planted circle activations of KD4 case (iii) built from 512 rows of that fixture.
16. **Private helpers reused** through module attributes, unchanged: `hwsc_registry._new`, `_close`, `hwsc_scratch._classify`, `c2_registry._violation` (the hwsc §0 list plus these). `hwsc_scratch._check_row`, `hwsc_drystore._os_parent_ok` and `hwsc_registry._os_canonical` are mirrored, not imported.
17. **KD5** reuses `hwsb_kb.kb6(w0, None)` for its identity and G_C legs only. The trained-checkpoint leg needs KB2's step-100 checkpoint, and track D trains nothing (§6 "Not run").
18. **k_C\*** (stable onset, report-only) uses `valid` (the gate predicate of k_C), not the status SCORED.
19. **n_pre with k_C undefined** counts every est checkpoint (report-only; D2 needs k_C).
20. **Statements are defined for any sequence length K ≥ 1** (σ(12) reads σ(K)), so KD4's short sequences use the same code.
21. **The W2 reservation globs** are fixed in CONTRACT `window`. The c2nd-store `RESERVATION_S*.json` files (another schema, a closed study) are not attested.
22. **The SAMPLE reservation starts after G0D and before H1D,** so an H1D or REGD stop is a stopped drawing job under J10 item 3.
23. **G0d searches the project root only** (the stage-C rule). The scratch fragments of J9 classify scratch paths when they occur in hits.
24. **The audit forbids `"hwsc-v1"`** in addition to the design's list, so that DRD3's planted `"hwsc-v1"` leftover is caught by the audit; `hwsc_config.SCOPE` is a listed left-unchanged row.
25. **`search_pruned` vs `blinded`.** The `hwsu-store` J9 rule prunes the seed search only. The registry readers R10 read track U's arrays and `meta.json` as data.
26. **Dry plans:** the tiny model's checkpoints are 0, 50, 100, 200 (DRD1), and DRD2 uses one master with checkpoints 0 and 20 (the protocol's "two 20-step checkpoints").
27. **Acceptance flow records** `KD_ACCEPT.json`, `ACCEPT_SAMPLE.json` and `ACCEPT_SCORE_<j>.json` gate each later job (the stage-C KC_ACCEPT / ACCEPT_VALIDATION pattern).
28. **R9 classes `logs/superseded-reg2-0192a1/**` arrays** as registry by name only (D-0192-1 archive). This is TO_FREEZE until the coordinator confirms the names.

## 21. TO_FREEZE items

- `authority.run_approval` (path, sha256): the owner's track-D run approval.
- `authority.h_exec`, FREEZE.json, the dry-run report sha256, the PF record sha256.
- **Registry rows (13), built by read-only listing on 2026-11-01:**
  - 10 scratch rows `hwsc-job-0181, 0184, 0186, 0187, 0188, 0189, 0191, 0192, 0195, 0196`: found by a name listing of the scratch root's top level and not entered (blinded); the coordinator freezes them by a name-only suffix listing (proposed EXCLUSION, `frozen_files` of `blinded_array`, expected empty);
  - 3 root rows `topo-pilot-hwsc-fix`, `topo-pilot-hwsd`, `topo-pilot-hwsu`: a header scan (k4b_registry.inventory semantics) found no history, identity or ObservationSet root, and only `docs/proposals/X5_G1_VERIFICATION_OUTPUTS/verification_arrays.npz` (non-history); `tools/hwsu` and `tests/hwsu` were not entered; proposed EXCLUSION.
- The R9 `logs/superseded-reg2-0192a1` rule (decision 28).
- `obligation.alignment` with track U: settled by J11; the coordinator confirms at the freeze.
- `known_cases.KD4.parameters`: g, noise scales, seeds, measured statuses (DRD4).
- Any `binding.left_unchanged` row found for the `tools/hwsd` modules by the implementation's audit.

## 22. J11 erratum (phase-1 erratum, job 0197 phase 2; joint ruling J11, `coord-hws-ud-20261101.joint-rulings-addendum-4`)

The obligation record is now exactly the J11 form, shared field for field with track U. It changes decision 7 and the rows of `classify_file`, `obligation_files`, `write_obligation` and `obligation_check`. J3, J8 and J10 are unchanged.
- **Top level (all required):** `schema` = `hws-registry-obligation-v1`, `store`, `track` (`"U"` or `"D"`; hwsd writes `"D"`), `job`, `attempt` (integer >= 1 or null for a dry store), `written_utc`, `written_by`, `reservation_id`, `name_rules`, `dry_stores`, `files`, `rule` = `fail closed`.
- **Per file (all keys):** `relpath`, `sha256`, `bytes`, `class` (`ObservationSet`, `K4b history table`, `NON_HISTORY`), `reader` (`hwsb_registry.registry_digests`, `k4b_history_table`, null), `basis` (null for the history classes; `artifact`, `registry` or `name_rule` for NON_HISTORY).
- **sha256** is null only for a Checkpoint payload, classed by its sibling `meta.json` and never opened or hashed.
- **Reader rule (both tracks):** the newest obligation by `written_utc` governs; a missing or extra key, an unknown value, an unlisted array file, a sha256 mismatch on any non-null sha256, or a `name_rule` basis that no listed regex matches makes the store `INCONCLUSIVE/REGISTRY_INCOMPLETE`.

## 23. Implementation errata (job 0197 phase 3; coordinator rulings RULINGS_PHASE2)

- **E-1 (archived killed construction).** An archived or live native-wall C0-CAL (`INCONCLUSIVE`, reason prefix `NATIVE_WALL:` or `native operation … wall`) gives the per-checkpoint status `CHART_UNAVAILABLE` with the label `CHART_UNAVAILABLE/NATIVE_WALL: <reason>` (protocol section 2.6, DRD6), never `CHART_UNAVAILABLE/INCONCLUSIVE: NATIVE_WALL: …`. A native-wall direct chart gives `SCORED_UNVALIDATED/NATIVE_WALL: <reason>`.
- **Reservation end record (supersedes the (b) row of `reservation_ended` in section 3.5).** The end record of any K4b-schema reservation, including a top-level file such as `hwsu-store/RESERVATION*.json`, is `<store>/reservations/<reservation_id>.END.json` (CONTRACT `window.ended_rule`, J8 item 2). `<store>` is the parent of `reservations/`, or the folder of a top-level reservation file.
- **`read_k4b_table`** raises `ValueError` on every defect, including a missing array (`seq_ids`, `canon32`, `digest`) or an unreadable file.
- **Obligation `store` and `dry_stores`** are written with forward slashes (`Path.as_posix()`), as J11 states; read `str(store)` in section 3.4 accordingly.
- **Refused jobs.** A job refused at preflight or at its accept check that wrote anything into the store (even `GATES.jsonl` lines) still ends by writing `REGISTRY_OBLIGATION_<job>-a<k>.json` (J10 item 2; `hwsd_driver.refuse_exit`); it may list zero array files. A refusal in an empty or absent store writes nothing.
- **Extra modules (size split; every name stays reachable under its documented module).** `hwsd_known2` holds `kd2`, `c0_val_line`, `repro_c` and the KD3 write guard (re-exported by `hwsd_known`). `hwsd_jobs` holds `run_score`, `run_summary` and `main` (re-exported by `hwsd_driver`). `hwsd_dry` resolves `drd2, drd3, drd5–drd14` lazily (module `__getattr__`) from `hwsd_dry2` and `hwsd_dry3`; DRD2, DRD3, DRD6 and DRD12–DRD14 live in `hwsd_dry3`, DRD5 and DRD7–DRD11 in `hwsd_dry2`, DRD1 and DRD4 in `hwsd_dry`.
- **KD4 parameters.** `seq_cases` uses, in order: the `params` argument; the JSON record named by the environment variable `HWSD_KD4_PARAMS`; `hwsd_dry.KD4_DEFAULT` (TO_FREEZE: g_mass 0.01, noise i 1e-7 and ii–v 0.01, seeds 629971–629975). It writes the parameters used to `<out>/KD4_PARAMS.json`; DRD4 returns them as `kd4_parameters`. The DRD4 record is to be written into CONTRACT `known_cases.KD4.parameters` as a contract erratum before the freeze. Every case of CONTRACT `known_cases.KD4.cases` (i–v) is scored once, in `<out>/cases/<id>/`.
- **E-2 (implemented shapes).**
  - `seq_cases` returns `{"parameters", "cases": {id: {"status", "label", "point", "se", "ok"}}, "sequences": {name: {"order", "readings": [D2, D3, D6], "ok"}}, "fallback_before", "status"}`.
  - `chart_one`'s `prod` is the whole `k4b_charts.build_chart` result (it includes `serial`); `c0_val` carries the extra key `reason` and `criteria` is `{name: bool}`.
  - `load_scores[(j, step)]["arrays"]` is the dict of `ARRAYS.npz` arrays (None when absent); `bootstrap_inputs_d` wants `shared` as `{name: {"all": {"X": array}}}`.
  - `evaluate(...)["order"][j]` is `{"chart": {"anchor", "A", "category"}, "learning": {…}}`.
  - `fill_templates` returns `{statement key: text}` (keys D2…D6 readings, plus `D3_CHART_AT_INIT`); statements without a registered template (D1, D4 FALSE, D6 FALSE) get a short generic line.
  - `CHECKPOINT_RECORD.json` has the closed key set of CONTRACT `records.CHECKPOINT_RECORD`; the control bounds needed by `control_summary_d` are written to a separate `CONTROLS_B.json` (JSON) in the checkpoint folder. `native_wall` is `{"role", "text"}` or null.
  - `f_sides` takes the planted flag from `record["planted"]` (or the certificate's).
  - `stop_obligation` returns `{"obligation": the obligation record dict, "end": the END record}`.

## 24. TO_FREEZE review (coordinator a944ef89, 2026-11-01; job 0197)

Review of the section 21 items at hwsd-impl e9dc68d; the record is CONTRACT `to_freeze_review`.
- **Scratch rows (10 `hwsc-job-*`): EXCLUSION**, `frozen_files` `{}`. A name-only suffix listing found one file and no array file in each.
- **Root rows: EXCLUSION** for `topo-pilot-hwsc-fix`, `topo-pilot-hwsd` and `topo-pilot-hwsu`. The owner removed `topo-pilot-hwsc-fix` (approved 2026-11-01); an absent EXCLUSION row raises no violation in `inventory_d`. The two live worktrees hold only the non-history `verification_arrays.npz` outside `.git`.
- **R9 `logs/superseded-reg2-0192a1` rule: CONFIRMED** by a name-only listing of `hwsc-store/logs/` (9 array files, all matched; decision 28).
- **Obligation alignment: CONFIRMED.** Field lists equal track U's; a track-U dry store passes `obligation_check(kind="dry")`, and a track-D-written store passes track U's `read_obligation`.
- **KD4 parameters: FROZEN** in CONTRACT `known_cases.KD4.parameters`: g 0.01, noise i 1e-7 and ii-v 0.01, seeds 629971-629975 (also CONTRACT `seeds.kd4_seeds`), measured statuses i CHART_UNAVAILABLE, ii SCORED, iii SCORED, iv SCORED_UNVALIDATED, v SCORED, and every sequence as expected. The record is `agent-handoff/jobs/0197/KD4_PARAMS.json` (equal to `hwsd_dry.KD4_DEFAULT`); author A's slow end-to-end test now runs without `HWSD_KD4_PARAMS`.
- **Binding:** `hwsd_bind.audit()` inside `bound_hwsd()` PASS (217 hits, 0 unlisted); no `left_unchanged` row added.
- **Open until the freeze:** `authority.run_approval` and the h_exec / FREEZE / dry-run / PF hashes.
- **Test erratum:** author B's `test_effective_tables` asserts `hwsc-job-0181` decision `EXCLUSION` (was `TO_FREEZE`).

## 25. D-0201-1 erratum (job 0202; ruling R-0201-1)

D-0201-1: DRD4's KD4 case outputs are written under the fixture root, per decision 6 (`fresh_fixture(job, "DRD4")`, `adhoc` when no job); no KD4 array file is left in the hwsd-dry store.

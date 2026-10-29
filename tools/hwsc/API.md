# tools/hwsc: written contract (job 0176 phase 1; derived from HWSC-DESIGN-v1)

**Authority.** `tools/hwsc/PROTOCOL_HWSC_v1.md`, a byte-for-byte copy of `agent-handoff/planning/responses/HWSC-DESIGN-v1.md` (sha256 `f0f2396c147985493b0f6399626ab8cef3ad95edcacf96b450671ae62a7100a9`; it becomes HWSC-FROZEN-v1 at the execution freeze). Authority for stage C: owner addendum 34 (planning up to an execution freeze; **running stage C is not approved**). Section marks (§n), KC, DRC, RC, C-rows and binding rows refer to the protocol. Owner questions Q1–Q6 are pending; this contract uses their registered defaults (protocol §12).

**Precedence.** Protocol > `CONTRACT.json` > this file > `TEST_PLAN.md`. A difference is a contract defect to report through the coordinator, never to resolve in code or in a test. `CONTRACT.json` holds the machine-readable values (exact values are strings for `fractions.Fraction`). This file fixes names, signatures, shapes, dtypes, streams, record schemas, the store layout, the binding, the registry composition, every gate's computation in order, the outcome precedence and the meter binding, so that the two independent test authors (`TEST_PLAN.md`) can write tests before any module exists. It changes no scientific choice. Where the protocol leaves a detail open, the simplest consistent option is fixed in §15 "Choices" (cited as "choice n"); each is open to a coordinator ruling. §16 lists the TO_FREEZE items and §17 the design gaps found while writing this contract.

**Nothing here authorises a run.** No training, real-process sampling, metered run or store write follows from this contract.

## 0. Conventions

- **Nine modules** under `tools/hwsc/` (§10.1): `hwsc_config`, `hwsc_bind`, `hwsc_data`, `hwsc_registry`, `hwsc_known`, `hwsc_gates`, `hwsc_driver`, `hwsc_dry`, `hwsc_meter_bind`; each `.py` at most 400 lines (`tools/check_file_sizes.py`). A split by size adds modules by an API erratum (the HWSB E1 pattern); every name of this file stays reachable as `<module>.<name>`. **No existing file is edited** (versioned binding only, §3.2). No `.npz`/`.npy` is committed under `tools/hwsc` or `tests/hwsc`.
- **Private names of reused modules.** Only these are used, unchanged, through module attributes (choice 16): `c2_registry._ok_readers`, `_violation`, `_x6_manifest`, `_entry`, `_try`, `_static_readers` (the helpers `nd_registry.build` itself calls) and `x6s1_registry._headers`, `_history_bearing` (as `nd_registry` uses them). No other private name is imported.
- **Import convention.** Every module imports `hwsc_config` first (`from __future__ import annotations  # noqa: I001`). `hwsc_config` computes `HERE = Path(__file__).resolve().parent`, `REPO = HERE.parents[1]` and prepends to `sys.path`, if absent, so that the resulting order is: `tools/hwsc`, `tools/hwsb`, `tools/hws`, `tools/k4b`, `tools/c1prime`, `tools/c1prime_registry`, `tools/x4_circle_history`, `tools/x4_oracle_profile`, `tools/c2_nd`, `tools/c2_readout`, `tools/x6_stage1` (under `REPO`). It then imports `hwsb_config` (which reads stage B's CONTRACT) and `k4b_config` (K4b's and C1′'s CONTRACTs). Import reads only CONTRACT.json files and computes small constants; it never opens HANDOFF.json or any store file. Dependency order (no import-time cycles): `hwsc_config` ← `hwsc_bind` ← `hwsc_data` ← `hwsc_registry` ← `hwsc_gates` ← `hwsc_known` ← `hwsc_driver` ← `hwsc_dry`; `hwsc_known.g0c` and `hwsc_known.run_kc` import `hwsc_driver` lazily inside the function (the `hwsb_known.kb0` pattern); `hwsc_meter_bind` imports only `hwsc_config` and the meter modules.
- **Call-time lookups.** Stage-C code calls every reused function and reads every reused constant through its module attribute at call time (`hwsb_eval.model_predictive(...)`, `k4b_data.SCOPE`), never through a `from … import` copy, so that the binding applies and tests may monkeypatch a reused function. Stage-C modules never copy a stage-C constant from another stage-C module into a default argument except the documented defaults of this file.
- **Test import aliases** (TEST_PLAN §1): `import hwsc_config as cc`, `hwsc_bind as cb`, `hwsc_data as cd`, `hwsc_registry as cr`, `hwsc_known as ck`, `hwsc_gates as cg`, `hwsc_driver as cdr`, `hwsc_dry as cdry`, `hwsc_meter_bind as cm`.
- **Run** with `X:/Downloads/projects/topo-pilot/topo-pilot/.venv/Scripts/python.exe -s` and `PYTHONPATH=<worktree>/src` (the editable install would otherwise import main's `src`).
- **Model keys.** Every per-model map is keyed by the **int** master (620301, 620302, 620303; dry 629911–629913), iterated in `MASTERS` order. Model-and-step maps use `(j, "step5000")` and `(j, "step0")` (the K4b labels, required by the reused stage functions). Per-(model, side) maps use `(j, s)`, `s` ∈ {`"-"`, `"+"`}; in JSON `f"{j}:{s}"` (stage-C records) or `f"{j}{s}"` (the reused K4b validation report keys).
- **Numbers.** Exact quantities (σ, neighbour, M, α, F, F_plan, Z_bound, δ, p_D2a products) are `Fraction`s; JSON records write `str(Fraction)`. A float bound enters exact arithmetic as `Fraction(float(x))` (the `k4b_stats._fr` rule). Gate statistics are float64. Means are `c1_means.tree_mean`; SDs `ddof=1`.
- **Statuses** are full strings: `PASS`, `FAIL`, `REPORTED`, `NOT_RUN`, `HOLD`, `CONTINUE`, `STOP`, `PAUSE`, `INCONCLUSIVE/<REASON>`, `FAIL_TECHNICAL/<REASON>`. Stage-C code raises **`c1_records.C1GateFailure(status, reason)`** (attributes `status`, `reason`; the K4b convention, choice 1). Reused stage-B code raises `hwsb_config.HwsbStop`, HWS code `hws_worlds.HwsStop`; `hwsc_driver.status_of` (§7.1) maps every exception to a status.
- **Writes** only inside the directory passed as `out` (or an explicit path argument), by exclusive create (`stage_records.write_new`, `stage_records.save_npz`), except: `GATES.jsonl` (`stage_records.record_gate`), `STAGES.jsonl` (`k4b_driver.begin_stage`/`complete_stage`), the chart ledgers (`k4b_charts.open_ledgers`), the study ledger (`hwsc_driver.ledger_append`, atomic replace), the registry run directories (`x6s1_registry.DigestSet.build`) and `logs/`. ArtifactStore writes go through `ArtifactStore.save` (content-addressed; identical content is idempotent; differing content `CHECKSUM_MISMATCH`). `cpu_ledger.json` is written only by the meter.
- **Footprint (RC-13).** Implementation, tests and the dry run write no array file and no ArtifactStore artifact anywhere under `X:/Downloads/projects/topo-pilot/`. Tests use pytest `tmp_path` with `--basetemp X:/Downloads/topo-scratch/test_hwsc-<job>/pytest`; TEMP/TMP/TMPDIR under `X:/Downloads/topo-scratch/test_hwsc-<job>/`. The dry store is `X:/Downloads/topo-scratch/hwsc-dry/` (or `hwsc-dry-<job>/`), where no file is named `HIST_*.npz` (dry history files are `DRYHIST_*.npz`, choice 29).
- **Blindness (§9.2, DRC11; R-0176-G1).** Stage-C code opens no path for which `hwsc_config.blinded(path)` or `hwsc_config.public_summary(path)` is true (§1.4); every direct file read of stage-C code goes through `hwsc_config.guard` or `hwsc_config.read_json`. The stage-B blindness list is exactly the five rules of CONTRACT `blindness.stage_b` (`jobs/0175/review.md` is the only blinded mailbox file; `jobs/0175/*.json` and `task.md` hold dispatch metadata and may be read, also by the frozen registry reader (c)). Stage-B quantities enter only through `hwsc_config.load_handoff()`.
- **No foreign payload access** beyond the registry readers of §4 (identity-only token reads of ObservationSets and history arrays by the frozen and new readers, never a `state.pt`, never a `sealed/` path) and the KC5 read of the hash-checked S3 w\* table of `hws-store` (named in the KC AUTH). Inside its own store, stage C hashes and reads its own ObservationSet payloads and history files (R7, `OBS_INVENTORY.json`; the stage-B ruling-c7 pattern).
- **Plans.** Data and training functions take a `hwsb_config.Plan`; `HWSC_PLAN` is the only plan that may touch `hwsc-store` (§1.3).

## 1. `hwsc_config.py` (≈160 lines): constants, contract, plans, HANDOFF, blindness guard

### 1.1 Constants and paths

| Name | Value / signature | Contract |
|---|---|---|
| `HERE`, `REPO`, `CONTRACT_PATH`, `PROTOCOL_PATH`, `API_PATH`, `TEST_PLAN_PATH` | `Path`s | `HERE/"CONTRACT.json"`, `HERE/"PROTOCOL_HWSC_v1.md"`, `HERE/"API.md"`, `HERE/"TEST_PLAN.md"` |
| `ROOT`, `STORE`, `SCRATCH`, `DRY_STORE`, `MAILBOX`, `STUDY_LEDGER` | `Path("X:/Downloads/projects/topo-pilot")`, `ROOT/"hwsc-store"`, `Path("X:/Downloads/topo-scratch")`, `SCRATCH/"hwsc-dry"`, `ROOT/"agent-handoff"`, `MAILBOX/"HWSC_CPU_LEDGER.json"` | defaults only; every function that touches a store or ledger takes it explicitly |
| `HANDOFF_PATH`, `HWS_STORE`, `HWSB_STORE`, `SELECTION_PATH` | `ROOT/"hwsb-store"/"HANDOFF.json"`, `ROOT/"hws-store"`, `ROOT/"hwsb-store"`, `ROOT/"hws-store"/"SELECTION.json"` | |
| `load_contract(path=CONTRACT_PATH) -> dict`; `CONTRACT` | `json.loads` of the UTF-8 file; loaded at import | |
| `SCOPE`, `KEY`, `PROCESS` | `"hwsc-v1"`, `"W12-q1-s1.75-p0.2"`, `("cylinder", "overlap", "1.75")` | CONTRACT `world` |
| `MASTERS`, `DRY_MASTERS` | `(620301, 620302, 620303)`, `(629911, 629912, 629913)` | ints |
| `SEEDS` | `{"val_sd": 620311, "val_b4": 620312, "endpoint": 620313, "fresh_b4": 620314, "val_projection": 620315}` | the K4b seed names (binding row 1) |
| `P1C_SEEDS` | `(620311, 620315)` | `ladder_pilot(seeds=...)` |
| `DRY_SEEDS` | `{"val_sd": 629921, "val_b4": 629922, "endpoint": 629923, "fresh_b4": 629924, "val_projection": 629925}` | dry binding only (choice 24) |
| `NEEDLES` | the 12 strings of CONTRACT `seeds.g0_needles` | G0c |
| `SIZES` | `{"train": 131072, "dev": 4096, "lgate": 4096, "cal": 3072, "val": 3072}` | |
| `BLOCK`, `LGATE_N`, `PANEL`, `LADDER`, `DRAWS`, `KS` | `3072`, `4096`, `512`, `(3072, 6144, 12288)`, `5000`, `(1, 2, 4, 32)` | |
| `SITE`, `INDEX`, `BOS`, `D_MODEL`, `GATE_STEP`, `INIT_STEP` | `"resid_post_3"`, `32`, `36`, `128`, `5000`, `0` | |
| `M`, `ALPHA`, `LEARN`, `CAP`, `FLOOR` | `Fraction(1, 100)`, `Fraction(1, 60)`, `Fraction(4, 5)`, `Fraction(1, 10**4)`, `Fraction(1, 10**9)` | equal to `k4b_config.MARGIN`, `ALPHA`, `CAP`, `FLOOR` (checked at import; mismatch → `C1GateFailure("FAIL_TECHNICAL/BINDING", …)`) |
| `RANKS` | `{"alpha": 84, "one_minus_alpha": 4917, "b4_lower": 250, "central_lo": 125, "central_hi": 4875}` | equal to `k4b_config.RANKS` (checked at import) |
| `SIGMA`, `NEIGHBOUR` | `Fraction(7, 4)`, `Fraction(1, 5)` | |
| `HOLD_S`, `HOLD_FROM`, `STEPS` | `6006.6282`, `1000`, `5000` | CONTRACT `cpu` |
| `DISCLOSURE` | CONTRACT `disclosure` (= `k4b_contract_view.authority.c1prime_disclosure`) | §6.4 text, carried by every report |
| `RESERVATION_FILE`, `RESERVATION_ID` | `"RESERVATION_W2.json"`, `"RES-HWSC-W2"` | choice 3 |

### 1.2 HANDOFF (§9.1)

| Name | Contract |
|---|---|
| `load_handoff(path=HANDOFF_PATH, expected_sha256=None) -> dict` | `expected_sha256` default CONTRACT `handoff.sha256`. Reads the bytes through `guard`; `sha256(bytes)` must equal it, the top-level key set must equal CONTRACT `handoff.keys` exactly, and no key of CONTRACT `handoff.forbidden_keys` may occur at any depth; any defect → `C1GateFailure("FAIL_TECHNICAL/IDENTITY", …)`. Returns a new dict with `Z_bound`, `F_plan`, `registry_value` as `Fraction(str)`, `N_C`, `k_C`, `model_count` as `int`, `p_D2a` as `float`, `stage_c_exclusions` as a `tuple` of str, the other keys unchanged. Never returns or reads any other stage-B file |

### 1.3 Plans and run keys

| Name | Contract |
|---|---|
| `HWSC_PLAN` | `hwsb_config.Plan("real", MASTERS, hwsb_config.MODEL_CFG, hwsb_config.TRAIN_CFG, {"train": 131072, "dev": 4096}, SITE, KEY, PROCESS, 5000, 0)` (E4 recipe; equal to CONTRACT `recipe`) |
| `dry_plan(kind, case) -> Plan` | `dataclasses.replace(hwsb_config.dry_plan(kind, case), masters=DRY_MASTERS, sizes=<sizes>)`; `kind` ∈ {`"dry_tiny"`, `"dry_e4"`}, else `ValueError`. Sizes: `dry_tiny` → `{"train": 4096, "dev": 512}`; `dry_e4` → `{"train": 2048, "dev": 256}` |
| `run_key(plan, master) -> tuple` | real: `(SCOPE, KEY, int(master))`; dry: `(SCOPE, "DRY", plan.key, int(master))`. Under `bound_stage_c()` it equals `hwsb_config.run_key(plan, master)` (asserted at TRAIN) |

### 1.4 Blindness guard (§9.2; DRC11)

| Name | Contract |
|---|---|
| `BLINDED` | CONTRACT `blindness.stage_b` (R-0176-G1), relative to `root`: file `hwsb-store/REPORT.json`; file `hwsb-store/GATES.jsonl`; directory `hwsb-store/stages/EVAL/` (and everything under it); glob `hwsb-store/CHART_CONSTRUCTIONS_*.json`; file `agent-handoff/jobs/0175/review.md`. Nothing else is stage-B-blinded (`agent-handoff/jobs/0175/task.json`, `request.before.json`, `task.md` and `hwsb-store/superseded/**` are readable) |
| `PUBLIC_SUMMARY` | CONTRACT `blindness.public_summary` (CLAUDE.md rule): any path component starting with `00_read_me_first` (case-insensitive); any path containing the consecutive components `docs/research_summary` |
| `blinded(path, root=ROOT) -> bool` | `p = Path(path).resolve()` as a lower-cased POSIX string; `r = Path(root).resolve()` likewise. True iff `p` equals one of the `BLINDED` file rules, lies at or under the `stages/EVAL` directory rule (path prefix followed by `/` or end), or its name matches the glob directly in `hwsb-store/` (`fnmatch` on the lower-cased name). Pure (no file access) |
| `public_summary(path) -> bool` | True iff a `PUBLIC_SUMMARY` rule matches the lower-cased POSIX path. Pure |
| `guard(path, root=ROOT) -> Path` | `blinded(path, root)` or `public_summary(path)` → `C1GateFailure("FAIL_TECHNICAL/BLINDNESS", str(path))` before any open; else `Path(path)` |
| `read_json(path, root=ROOT)` | `json.loads(guard(path, root).read_text(encoding="utf-8"))` |
| `read_bytes(path, root=ROOT) -> bytes` | `guard(path, root).read_bytes()` |

## 2. `hwsc_bind.py` (≈180 lines): the versioned binding (§3.1–§3.2)

| Name | Contract |
|---|---|
| `decode(value, repo=REPO)` | CONTRACT `binding.encoding`: a JSON list → `tuple`; `{"__path__": s}` → `Path(s)`; `{"__repo__": rel}` → `repo / rel`; `{"__dict__": d}` → `dict(d)`; `{"__contract_view__": key}` → `copy.deepcopy(CONTRACT[key])`; `{"__contract__": sha}` → a marker object for the old-value check; anything else unchanged |
| `load_table(contract=CONTRACT, which="stage_c", case=None, case_dir=None) -> list[dict]` | rows `{"module", "name", "old", "new"}` decoded. `which="stage_c"`: CONTRACT `binding.table` (21 rows). `which="identity"`: the same rows with `new = old` re-read from the live module (KC7 a). `which="dry"`: the stage-C rows with these new values: `MODELS` (k4b_config, k4b_data, k4b_stats, k4b_driver, k4b_fresh) → `DRY_MASTERS`; `SCOPE` (k4b_config, k4b_data, k4b_decoder) → `f"hwsc-v1/DRY/{case}"`; `PROCESS` → `("cylinder", "overlap", "1.0")`; `SEEDS` → `DRY_SEEDS`; `k4b_config.STORE` and `k4b_driver.ARTIFACTS` → the case directory and its `artifacts/` (argument `case_dir`, choice 24); hwsb rows as stage C. `case` and `case_dir` are required for `"dry"` (`ValueError` otherwise) |
| `check_old(rows) -> list` | for each row: `importlib.import_module(row["module"])`; the current attribute must equal the decoded old value with `type(cur) is type(old)` (a `Path` compares by POSIX string; `{"__contract__": sha}` passes iff the current value is a dict with `protocol_sha256 == sha`). Returns the mismatch list |
| `bound_stage_c(table=None)` | context manager (the `hwsb_law.bound_law` pattern). `table` default `load_table()`. On entry: `check_old(table)`; any mismatch → `C1GateFailure("FAIL_TECHNICAL/BINDING", "code drift: …")` and nothing is set (entering twice therefore fails). Then `setattr(module, name, new)` for every row in table order; yields `{"rows": n, "table_sha256": sha256 of the canonical JSON of the encoded table}`. On exit (normal or exception), every attribute is restored to the exact object held before entry (identity `is`), in reverse order. Module flag `ACTIVE` is True inside, False outside |
| `audit(modules=None, left_unchanged=None, forbidden=None) -> dict` | §3.2 item 3. `modules` default: every `sys.modules` entry whose `__file__` resolves under one of CONTRACT `binding.audit.module_dirs` of `REPO`; `left_unchanged` default CONTRACT `binding.left_unchanged`; `forbidden` default CONTRACT `binding.audit.forbidden`. Scans each module's globals (skipping modules and `__dunder__` names; callables are scanned only through their defaults) and, for every function and method **defined in that module** (`fn.__module__ == module.__name__`; classes defined in the module; `staticmethod`/`classmethod` unwrapped), `__defaults__` and `__kwdefaults__`. Recursion (depth ≤ 6, cycle-safe) into tuples, lists, sets, frozensets, dict keys and values and the fields of dataclass instances. A hit is a value equal to a forbidden tuple, a dict or set whose key set equals a forbidden key set, a forbidden string, a forbidden int (never a `bool`), a dict with `val_sd == 610101`, or a `Path`/`str` whose `/`-normalised form without trailing `/` equals a forbidden path. Each hit `{"module", "where", "kind": "global" or "default", "hit"}`; its **top name** is the global name or `"<qualname>.__defaults__"` / `"<qualname>.__kwdefaults__"`. Status `PASS` iff every hit's `(module, top name)` is in `left_unchanged`; else `FAIL_TECHNICAL/BINDING`. Returns `{"status", "hits", "unlisted": [hits not covered], "modules": [names], "n_hits"}`. Called **inside** `bound_stage_c()`: outside it, the table's own names are hits and the audit fails by design |
| `never_called() -> tuple` | CONTRACT `binding.never_called` |

**Binding table (CONTRACT `binding.table`; old → new).** `k4b_config.MODELS` (1729, 2718, 3141) → (620301, 620302, 620303); `k4b_config.SCOPE` "k4b-sf-v1" → "hwsc-v1"; `k4b_config.PROCESS` (…, "1.25") → (…, "1.75"); `k4b_config.SEEDS` 610101–610105 → 620311–620315 (same names); `k4b_config.STORE` `ROOT/k4b-store` → `ROOT/hwsc-store`; `k4b_config.CONTRACT` (K4b contract) → `CONTRACT["k4b_contract_view"]` (choice 2); `k4b_config.CONTRACT_PATH`, `PROTOCOL_PATH` → the `tools/hwsc` files; `k4b_data.{MODELS, PROCESS, SCOPE}`; `k4b_stats.MODELS`; `k4b_driver.{MODELS, SEEDS, ARTIFACTS}` (`ARTIFACTS` → `ROOT/hwsc-store/artifacts`); `k4b_fresh.{MODELS, SEEDS}`; `k4b_decoder.SCOPE`; `hwsb_config.SCOPE` "hwsb-v1" → "hwsc-v1"; `hwsb_config.MASTERS` (620201, 620202) → (620301, 620302, 620303); `hwsb_config.DRY_MASTERS` (629901, 629902) → (629911, 629912, 629913). The 44 "left unchanged, with reason" rows are in CONTRACT `binding.left_unchanged` (they include `k4b_stats.sd_upper.__defaults__` and `k4b_stats.centered.__defaults__` with the reason 'left unchanged: never called under stage C', and every stage-B, HWS and C1′ hit of the static scan). A read-only import scan of the 59 modules under the audit directories at af5e7b4 found exactly the hits covered by the two lists (no uncovered hit, no unused row).

## 3. `hwsc_data.py` (≈260 lines): process, train/dev mirror, blocks, H2, H2-FRESH, registry risk

### 3.1 Process and train/dev (§2.3; DRC4)

| Name | Contract |
|---|---|
| `build_process_c(store, masters=MASTERS) -> dict` | `hwsb_data.build_process(store, masters=tuple(masters))` (w\* configs; the hwsb process dict of hwsb API §2.1, including `ids`, `T`, `pi`, `coords`, `features`, `E_named`, `perm`, `E_canon`, `E_canon_shared`, `V`, `N`, `sigma`, `neighbour`) |
| `process_identity(store, proc) -> dict` | the KC1/H1-C identity (mirror of `hwsb_known.kb1`'s checks): `world_id`, `transition_id` equal CONTRACT `world.WorldSpec.id`, `world.TransitionSpec.id`; `hwsb_data.spec_checksums(store, proc)` World/Transition equal their `payload_sha256`; `SELECTION.json["sha256"]` (via `read_json`) equals CONTRACT `world.selection_sha256`; `hwsb_data.arrays_sha256(proc)[k]` equals it for `E`, `T`, `pi`, `coords`; every master's `E_canon[m]` hashed by the array rule equals SELECTION `E` (bitwise identity across masters and `validate_process` are enforced by `build_process`). Returns `{"ok": all, "checks", "ids", "spec_checksums", "arrays_sha256"}` |
| `sequence_ids_c(role, n, plan, master, scope=SCOPE) -> int64 [n]` | mirror of `hwsb_data.sequence_ids` for `role` ∈ {`"train"`, `"dev"`} only (else `ValueError`), with `scope` in place of the literal: first `hwsb_data.stream_record(role, plan, master)` (its role/master refusals); `rep = f"{scope}/DRY/{plan.key}/{role}/{master}"` for a dry plan, else `f"{scope}/{role}/{master}"`; returns `make_sequence_ids(process_code(*plan.process, rep), role, n)` |
| `make_train_dev_c(store, proc, master, plan, scope=SCOPE) -> dict` | line-for-line mirror of `hwsb_data.make_train_dev` with `sequence_ids_c(..., scope=scope)` in place of `hwsb_data.sequence_ids`; generators `hwsb_data.data_generator(split, plan, m, tree)` with `tree = SeedTree(m)` (so the streams are `("data", hwsb_config.SCOPE, split, KEY, m)` at call time); `check_disjoint(train=…, dev=…)`; ObservationSet config `{"family", "mode", "sigma": plan.process[2], "V", "N", "split", "n", "replicate": m, "study": hwsb_config.SCOPE, "key": plan.key}`, parents `[transition id, emission id of m]`, `seed_map = dict(tree.issued)`, consumer `"dataset"`. Returns `{"train": id, "dev": id, "streams": {split: stream_record}, "n": {split: n}, "replicates": {split: rep}}`. With `scope="hwsb-v1"`, unbound, and a stage-B dry plan, ids and payload checksums equal `hwsb_data.make_train_dev` on an identical `MemoryBackend` store (DRC4) |

### 3.2 Evaluation blocks (§2.4)

| Name | Contract |
|---|---|
| `block_generator(split, block, scope=None, process=None)` | `SeedTree(0).generator("data", scope or k4b_data.SCOPE, split, int(block), *(process or k4b_data.PROCESS))` (the `k4b_data.history_generator` pattern; under the binding `k4b_data.SCOPE == "hwsc-v1"`) |
| `block_ids(split, block, n, scope=None, process=None) -> int64 [n]` | `make_sequence_ids(process_code(*(process or k4b_data.PROCESS), f"{scope or k4b_data.SCOPE}/{split}/b{int(block)}"), "test", n)` |
| `sample_block_c(T, E_canon, pi, split, block, n) -> (canon32, ids)` | mirror of `k4b_data.sample_block` with an explicit `n`: exactly one `HMMSampler(T, E_canon, pi, SequenceLayout()).sample(n, block_generator(split, block))`; `canon32 = uint8 tokens[:, :32]`; tokens and states deleted at once; rows sorted by `block_ids(split, block, n)` (stable). For `n == BLOCK` it equals `k4b_data.sample_block` bitwise |
| `sample_lgate(proc) -> (canon32, ids)` | `sample_block_c(proc["T"], proc["E_canon_shared"], proc["pi"], "lgate", 0, LGATE_N)` |
| `sample_eval(proc, split, block=0) -> (canon32, ids)` | `split == "lgate"` → `sample_lgate`; `split` ∈ {`"cal"`, `"val"`, `"test"`} → `k4b_data.sample_block(proc["T"], proc["E_canon_shared"], proc["pi"], split, block)` (bound); else `ValueError` |
| `hist_name(split, block, dry=False) -> str` | `f"HIST_{split}_b{block}.npz"`, or `f"DRYHIST_{split}_b{block}.npz"` when `dry` (choice 29) |
| `sample_test_c(out, proc, release, reservation_path, dry) -> dict` | `dry=False` → `k4b_fresh.sample_test(out, proc, release, reservation_path)` unchanged (real run). `dry=True` → a line-for-line mirror of it whose only change is the file name `hist_name("test", b, dry=True)` (choice 29) |
| `save_table(path, table) -> Path` | `stage_records.save_npz(path, **{k: v for k, v in table.items() if isinstance(v, np.ndarray)})` (the `k4b_driver.h2` call): keys `canon32` uint8 [n, 32], `seq_ids` int64 [n], `digest` `<U64` [n], `landmark` bool [n], `ref_row` bool [n], `decoder_panel` int8 [n] |

### 3.3 H2 and H2-FRESH (§3.3, §5 rows 3 and 12)

| Name | Contract |
|---|---|
| `separation_c(reg, tables) -> dict` | `reg` a `c2_registry.Registry`; `tables` `{split: k4b_data.history_table dict}` in insertion order. (1) `collisions[f"{s}_R"] = int(np.count_nonzero(reg.contains(np.asarray(t["digest"], "<U64"))))`; (2) for every pair in insertion order `collisions[f"{a}_{b}"] = len(set(a digests) ∩ set(b digests))`; (3) `seq = k4b_data.seq_disjoint({s: t["seq_ids"]}, reg.seq_ids, list(reg.sealed_ranges.values()))`; (4) `pred[s] = k4b_data.predicate_check(t["canon32"], reg.predicates)`; (5) `dup[s] = k4b_data.duplicates(t["canon32"])`. Status in this order: any collision > 0 → `FAIL_TECHNICAL/LINEAGE`; `seq["status"] != "PASS"` → that status; any predicate non-PASS → `INCONCLUSIVE/REGISTRY_INCOMPLETE`; else `PASS`. Returns `{"status", "collisions", "seq_disjoint": seq, "predicates": pred, "duplicates": dup}` |
| `h2c(out, ctx) -> dict` | mirror of `k4b_driver.h2`: `k4b_release.verify_reservation(ctx["reservation_path"], ctx["release"])` non-PASS → `C1GateFailure("INCONCLUSIVE/AUTHORITY", …)` before any row; `k4b_driver.begin_stage(out, "S3")`; for split in `("lgate", "cal", "val")`: `canon, ids = sample_eval(ctx["proc"], split, 0)`, `t = k4b_data.history_table(canon, ids, split, 0)`, `save_table(out/"stages"/"S3"/hist_name(split, 0, ctx.get("dry", False)), t)`; `k4b_driver.complete_stage(out, "S3", files)`; `ctx["tables"] = {split: t}`; `r = separation_c(ctx["reg1"], ctx["tables"])`; non-PASS → `C1GateFailure(r["status"], json)`. Returns `r` without `status` |
| `h2_fresh_c(out, ctx) -> dict` | mirror of `k4b_fresh.h2_fresh`: `verify_reservation(..., sampling_began=True)` non-PASS → `C1GateFailure(res["status"], …)`; `reg2 = c2_registry.Registry.load(out, "K-REG2")`; `own = set(lgate ∪ cal ∪ val seq_ids)`; `blocks = {f"test_b{i}": seq_ids of block i} ∪ {"lgate", "cal", "val": seq_ids}`; checks in order: `separation = {"collisions": {"test_R2": count(reg2.contains(test digests))}, "status": "PASS" or "FAIL_TECHNICAL/LINEAGE"}`, `seq_disjoint = k4b_data.seq_disjoint(blocks, reg2.seq_ids − own, list(reg2.sealed_ranges.values()))`, `predicates = k4b_data.predicate_check(test canon32, reg2.predicates)`; the first non-PASS raises its status |

### 3.4 Registry risk (§3.4 "Registry-risk check")

| Name | Contract |
|---|---|
| `p_d2a_check(proc, p_ref) -> dict` | `p = hws_exact.p_d2a(proc["T"], proc["E_canon_shared"], proc["pi"])`; `rel = abs(p − p_ref)/abs(p_ref)`; `ok = rel <= 1e-12`. Returns `{"p_D2a", "p_D2a_ref", "rel_diff", "ok"}` |
| `registry_risk(p_d2a, N) -> dict` | `value = (LGATE_N + BLOCK + BLOCK + int(N)) * Fraction(float(p_d2a))`; `ok = value <= Fraction(1, 100)` (equality passes). Returns `{"N", "rows", "value": str(value), "ok"}` |

## 4. `hwsc_registry.py` (≈380 lines): K-REG1, K-REG2, REHEARSAL (§3.3–§3.4; RC-2, RC-3, RC-4)

Every source returns the `nd_registry._new` shape: `{"status": "PASS" | "INCONCLUSIVE/REGISTRY_INCOMPLETE" | "FAIL_TECHNICAL/LINEAGE", "digests": set[str], "seq_ids": set[int], "files": [...], "other": [{"path", "reason"}], "non_history": [{"path", "bytes"}], "non_c2_format": [...], "present": bool, "known_gaps": [...]}`; `other` non-empty → INCOMPLETE. Digests are sha256 hex strings of canonical uint8 32-token rows (`scores.history_digests`), or hex digests taken as stored.

| Name | Contract |
|---|---|
| `source_c2nd(store=ROOT/"c2nd-store", bound=None) -> dict` | **R2.** `bound` default CONTRACT `registry.c2nd.hist_bound` (five files). Each bound file must exist (else `other` "missing") and re-hash (`stage_records.sha256`) to its value (else status `FAIL_TECHNICAL/LINEAGE`); it is read with `np.load(allow_pickle=False)`: digests = union of the present columns of `digest_H, digest_Hp, digest_Hm, digest_HY` (`""` dropped; `digest_H, digest_Hp, digest_Hm` required, else `other`); `sequence_id` (int64) added to `seq_ids` when present, else `known_gaps.append({"path", "gap": "no sequence_id column"})` (S3; not a failure). Any further `hist/HIST_*.npz` is read by the same rule without a bound hash. A name-only walk of every other array file (`.npz`, `.npy`, `.pt`): a path with a `sealed` component → `non_history` (never opened; `bytes` from `stat`); a path matching a CONTRACT `registry.c2nd.non_history_patterns` glob (`fnmatch` on the POSIX relpath; `registry/**` = anything under `registry/`) → `non_history`; under `superseded/` → `other` (array file in superseded); anything else → `other`. Nothing outside `hist/` is opened |
| `source_hwsb(store=ROOT/"hwsb-store", expected=None) -> dict` | **R4.** `expected` = HANDOFF `store_inventory` (required). `reg = hwsb_registry.registry_digests(store, expected=expected)`; `reg["status"] != "PASS"` → `other` entries from `reg["failures"]`. Then a name-only listing of `store` that prunes `stages/EVAL/` **before** listing it (`os.walk` with `dirnames` edited; `blinded` paths never touched): every array file outside `artifacts/ObservationSet/`, `hist/`, `superseded/` is `non_history` iff it lies under `artifacts/<T>/<id>/` with `T` ∈ {WorldSpec, TransitionSpec, EmissionSpec, Checkpoint} and `<id>/meta.json` has `artifact_type == T` (meta.json read through `guard`), or matches `stages/S4a/CHART_*.npz` / `stages/S4a/INIT_CHART_*.npz`; any other array file → `other` |
| `source_dry(paths=None) -> dict` | **R5** (R-0176-G4, G9). `paths` default CONTRACT `registry.dry_stores.paths` plus every `SCRATCH/"hwsb-dry*"` and `SCRATCH/"hwsc-dry*"` directory found by globbing. `hws-dry`, `hwsb-dry`, `hwsb-dry-0169`, `hwsb-dry-0171` must exist (else `other` "missing"); `hwsc-dry*` may be absent. In `hws-dry`, files under `hist/` are skipped (R3's). The walk does not prune `test_*` components inside these stores. For every array file (sorted walk): a CONTRACT `planted_fixtures` path with equal size and sha256 → `non_history` with `"class": "PLANTED_FIXTURE"`; `payload.npz`/`state.pt` under `<artifacts root>/<T>/<id>/` → by `meta.json` `artifact_type`: **`ObservationSet` → canonicalised exactly as `hwsb_registry.registry_digests` does**: `store = ArtifactStore(LocalFSBackend(<artifacts root>))`, `obs = store.load(ObservationSet, id, consumer="experiment")`, the EmissionSpec parent = the unique `pid` in `store.meta(id).parent_ids` with `store.meta(pid).artifact_type == "EmissionSpec"` in the same artifacts root (none or several → `other`), `spec = store.load(EmissionSpec, pid, consumer="experiment")`, digests `scores.history_digests(hwsb_data.canonical32(obs.tokens, spec.symbol_perm))`; EmissionSpec payloads are read only for `symbol_perm` in that step; `WorldSpec`, `TransitionSpec`, `Checkpoint` payloads and every `state.pt` → `non_history` (never opened); `stages/S4a/CHART_*.npz`, `INIT_CHART_*.npz` → `non_history`; any other `.npz`/`.npy` → `np.load(allow_pickle=False)`, members with a key in `k4b_registry.HISTORY_KEYS` or an integer dtype of `ndim ≥ 2` and last dimension 32 or 33 → `tokens.reshape(-1, last)[:, :32]` digested (stage-B and stage-C dry `hist/<role>.npz` and `DRYHIST_*` tables hold canonical rows); members whose key starts with `digest` → hex values as stored; a file with no such member → `non_history`; an unreadable file → `other`. `.pt` outside artifacts → `other`. Only synthetic dry artifacts are read (never a real-store payload, never `state.pt`) |
| `source_scratch_c(scratch=SCRATCH) -> dict` | **R6 (a).** `nd_registry.source_scratch(scratch)` unchanged (C2ND row 9; `nd_config.SCRATCH_ROOT`-relative rules) |
| `scratch_scan(scratch=SCRATCH) -> dict` | **R6 header scan** (k4b_registry.inventory semantics, with `test_*` components pruned, which `k4b_registry.inventory`'s `rglob` cannot do): for each top-level directory `top` of `scratch` whose name does not start with `test_`, **and also every top-level `test_hwsb-*` directory (R-0176-G9)**: `os.walk(top)` with `dirnames` starting `test_` removed before descent, **except inside the stage-B folders `hwsb-*`, `hwsb-dry*` and `test_hwsb-*`, which are walked completely**; every `.npz`/`.npy` file: `heads = x6s1_registry._headers(f)` (an exception → class `unreadable`); class `history` iff `x6s1_registry._history_bearing(f)` (shape = the first history member's header shape), else `identity` iff a header key is in `k4b_registry.IDENTITY_KEYS`, else not listed; every `meta.json` whose parent's parent is named `ObservationSet` → class `os_root` (the artifacts root, as `k4b_registry.inventory`); every `.pt` → class `pt` (name only). Nothing beyond npz/npy headers and file names is read. Returns `{top: {relpath: {"class", "shape"}}}` plus `"__top_level__"`: the array files directly under `scratch` |
| `scratch_check(scratch=SCRATCH, table=None, readers_ok=None) -> dict` | **R6 (b)–(c).** `table` default CONTRACT `registry.scratch_inventory`; `readers_ok` the set of reader tags that returned PASS in this build. `scan = scratch_scan(scratch)`. Any `__top_level__` file → `other`. For each scanned top-level directory: no row (the pattern rows `hwsc-dry-<job>` and `test_hwsc-<job>` match by prefix) → `other` if any file was listed; a `TO_FREEZE` row → `other` ("row not frozen"); otherwise every listed file must appear in the row's `frozen_files` (`{relpath: class}`, written at the freeze from the header scan) with the same class, else `other`; A row with `frozen_files == {}` (an empty folder, e.g. `hwsb-0168`) admits no file at all (fail closed on any later addition); a `READER` row also needs every tag of `readers` in `readers_ok` (tag `R5` = `source_dry`, `c2scratch` = `source_scratch_c`, `hws` = R3). An `EXCLUSION` row with `fixture_max_rows` admits only `history` files whose first header dimension is ≤ that value and `identity`/`os_root`/`pt` files under a `pt-*`, `pt2-*`, `bt*` or `pytest-of-*` component (K4B R23 rule 2), or under a component listed in the row's `fixture_components` (e.g. `pytest` for `test_hwsb-*`); this is checked at the freeze review and re-checked here. Returns the source shape plus `{"scan_counts": {top: {class: n}}}` |
| `source_own(store, expected) -> dict` | **R7.** `reg = hwsb_registry.registry_digests(store, expected=expected)` (the six ObservationSets under `artifacts/` and `superseded/**/artifacts/`, canonicalised by their EmissionSpec parents); plus every `superseded/**/stages/S3/HIST_*.npz` and `superseded/**/stages/S7/HIST_*.npz` read with `np.load(allow_pickle=False)` (`digest` column re-checked against `scores.history_digests(canon32)`, `seq_ids` added) (choice 18) |
| `inventory_c(root=ROOT, readers=None) -> dict` | **R8.** Mirror of `nd_registry.inventory` with the stage-C table: `inv = k4b_registry.inventory(root, exclude=CONTRACT registry.deep_scan_exclude)`; `inv.pop("hwsc-store", None)`; `classes = k4b_registry.classify(inv, readers)`; `frozen` = CONTRACT `registry.inventory` without `OWN` rows; READER_IF_PRESENT rows absent from `inv` are skipped, present ones checked as READER; every name is checked with `c2_registry._violation(name, frozen.get(name), inv.get(name), classes.get(name), readers.get(name, []))`. Returns `{"status", "inv", "classes", "unlisted", "violations"}` |
| `build(version, out_dir, root=ROOT, scratch=SCRATCH, handoff=None, own_expected=None, extra=None, sources=None) -> dict` | `version` ∈ {`"K-REG1"`, `"K-REG2"`, `"REHEARSAL"`}; `extra` only for K-REG2; `own_expected` required for K-REG1/K-REG2 and refused for REHEARSAL (no R7); `ValueError` otherwise. `mpath = out_dir/f"{version}.json"`, `dpath = out_dir/f"{version}_digests.npz"`, `run_dir = out_dir/"runs"/version`; any existing → `FileExistsError`. Composition (a mirror of `nd_registry.build`): `src = c2_registry.token_sources(root)`; `x6 = c2_registry.x6_source(root/"x6-stage1-store", run_dir)`; `nd = {"c2": source_c2(root/"c2-readout-store"), "c2sup": source_c2_superseded(root/"c2-readout-store"), "c2scratch": source_scratch_c(scratch), "hws": source_parallel(root/"hws-store", "hws"), "x6zc": source_parallel(root/"x6zc-store", "x6zc")}` (C2ND readers, R1/R3); `new = {"c2nd": source_c2nd(root/"c2nd-store"), "hwsb": source_hwsb(root/"hwsb-store", handoff["store_inventory"]), "dry": source_dry()}` plus `"own": source_own(<store>, own_expected)` for K-REG1/K-REG2 (`<store>` = `out_dir.parent`), then `new["scratch"] = scratch_check(scratch, readers_ok={tags of the PASS sources among c2scratch, hws, R5})`. `readers = c2_registry._ok_readers(src, x6 PASS)`, then for `(name, tag)` in `{"c2-readout-store": "c2", "hws-store": "hws", "x6zc-store": "x6zc", "c2nd-store": "c2nd", "hwsb-store": "hwsb"}` append `tag` iff its source passed (c2 also needs c2sup PASS). `inv = inventory_c(root, readers)`; `tokens = a + b + c + e + k (+ f via k4b_registry.source_f(root, inv["inv"], inv["classes"]))`; `reg = c1_data.build_registry(tokens)`; digests = `reg["digests"]` ∪ d/k digest sources ∪ every nd and new source's digests ∪ (K-REG2) each extra table's `digest` column; seq union = d/k `sequence_ids` ∪ source (a) sequence ids ∪ every source's `seq_ids` ∪ extra `seq_ids`; `cov = k4b_registry.revalidate_coverage(...)` as `nd_registry.build`. Status: `FAIL_TECHNICAL/LINEAGE` if any lineage problem (token-source lineage, x6 LINEAGE, any source LINEAGE), else `INCONCLUSIVE/REGISTRY_INCOMPLETE` if any problem (token problems, unreadable, coverage, inventory violations, any source non-PASS), else `PASS`. Writes `dpath` (`digests` `<U64` sorted, `seq_ids` int64 sorted; `stage_records.save_npz`) and `mpath` (`write_new`) with the `nd_registry.build` manifest keys (`version`, `registry_version` = `"hwsc-reg-v1"`, `status`, `problems`, `n_digests`, `digests_sha256`, `seq_id_union_sha256`, `x6`, `union_sha256`, `sources`, `classes`, `coverage`, `predicates`, `inventory`, `sealed_ranges`, `d2a_ranges`, `handoff_validation`, `k4b_store`, `protocol_sha256` = stage-C protocol, `nd_sources`, `built_utc`, `digest_file_sha256`) plus `hwsc_sources` (`{tag: summary without digests}`), `known_gaps`, `cpu_s` (`time.process_time()` delta) and `peak_memory_bytes` (psutil peak working set if importable, else None). `sources` (dry and tests only) is a dict `{name: callable}` that replaces the named source callables (`token_sources`, `x6_source`, `c2`, `c2sup`, `c2scratch`, `hws`, `x6zc`, `c2nd`, `hwsb`, `dry`, `scratch`, `own`, `inventory`) for synthetic roots. For K-REG1 and K-REG2 (`out_dir = <store>/registry`) `c2_registry.Registry.load(<store>, version)` must load the result unchanged; REHEARSAL is a cost and completeness rehearsal and is never loaded for separation (choice 19) |
| `obligation(store, extra_paths) -> dict` | writes `store/"REGISTRY_OBLIGATION.json"` (exclusive): `{"store": str(store), "readers": {"ObservationSet": "hwsb_registry.registry_digests", "HIST_*.npz": "K4b history-table reader (canon32, seq_ids, digest)"}, "dry_stores": [...], "inventory": {relpath: sha256 of every file under artifacts/ObservationSet, stages/S3, stages/S7, superseded}, "rule": "every later registry lists hwsc-store, hwsc-dry and every hwsc-dry-<job>; fail closed"}` |

## 5. `hwsc_known.py` (≈290 lines): G0c and KC0–KC9 (§4)

| Name | Contract |
|---|---|
| `needle_in(needle, line) -> bool` | the D-0127-1 rule (mirror of `hws_driver._needle_in`): an all-digit needle matches only as `(?<![0-9A-Za-z_])needle(?![0-9A-Za-z_])`; other needles as substrings |
| `seed_search_c(root, needles, root_for_guard=None) -> list` | mirror of `hws_driver.seed_search` (R-0176-G2): `os.walk(root, topdown=True)`; prune directories named `.git`, `.venv`, `__pycache__`, `sealed`, starting with `00_read_me_first` (case-insensitive), `docs/research_summary`, and every directory for which `hwsc_config.blinded(dir, root_for_guard or root)` holds (i.e. `hwsb-store/stages/EVAL`), before listing it; files: skip names starting with `00_read_me_first`, keep suffixes `.json .jsonl .md .py .txt .yaml`, skip files for which `blinded` holds (never opened); read with `encoding="utf-8", errors="replace"`; hits `{"path", "needle", "line"}` in walk order. On a root containing no blinded path its result equals `hws_driver.seed_search(root, needles)` exactly (list `==`) |
| `classify_hits_c(hits, fragments=None, job_scratch=None) -> dict` | `hwsb_known.classify_hits(hits, fragments or CONTRACT seeds.g0_declaration_fragments, job_scratch or CONTRACT seeds.g0_job_scratch, label="hwsc_declaration")` |
| `g0c(out, stage, auth=None, sched=None, release=None, root=ROOT, mailbox=MAILBOX) -> dict` | KC0 (stage `"KC"`) and E1 gate 0 (stage `"E1"`). In order: (i) each addendum of CONTRACT `authority.kc0_addenda` exists at `root/<path>` (absent → `INCONCLUSIVE/RESOURCE_OR_AUTHORITY`) with equal sha256 (else `FAIL_TECHNICAL/AUTHORITY`); the run-approval file of CONTRACT `authority.run_approval.path` (frozen by erratum) exists (absent, or the path still `TO_FREEZE` → `INCONCLUSIVE/RESOURCE_OR_AUTHORITY`) and its sha256 equals CONTRACT `authority.run_approval.sha256`, `auth["run_approval_sha256"]` and FREEZE.json `run_approval_sha256` (else `FAIL_TECHNICAL/AUTHORITY`); (ii) `load_handoff()` passes and `HANDOFF["freeze_sha256"]` equals CONTRACT `authority.hwsb_freeze_json.sha256` and the sha256 of `hwsb-store/FREEZE.json`; SELECTION.json and the HWS FINAL report re-hash (else `FAIL_TECHNICAL/AUTHORITY`); (iii) `hits = seed_search_c(root, NEEDLES)`, `classify_hits_c(hits)` non-PASS → `FAIL_TECHNICAL/SEED_SCOPE`; writes `stages/<stage>/G0C.json` (exclusive; the caller records the gate: `KC0` in the KC job, `G0C` in E1); (iv) `hwsc_driver.lineage_c(out)` PASS (absent store PASS); (v) `hwsc_driver.sched_ok(sched, stage)` (W3 record, §9.4); (vi) with `release` (E1 only): release A has non-None `w3_attestation`, `kreg1_reservation`, `seed_hits`, `kreg1_certificate`, `train_records`, `obs_inventory_sha256` (else `INCONCLUSIVE/AUTHORITY`), `classify_hits_c(release["seed_hits"])` PASS (else its status), `k4b_config.check_chart_equality()` all equal (else `FAIL_TECHNICAL/IDENTITY`). Returns the checks |
| `kc1(store, masters=MASTERS) -> (proc, dict)` | mirror of `hwsb_known.kb1` with `masters` (kb1 cannot take them: its `build_process` default is stage B's masters): `proc = hwsc_data.build_process_c(store, masters)`; `r = hwsc_data.process_identity(store, proc)`. Record `{"status": "PASS" if r["ok"] else "FAIL_TECHNICAL/KNOWN_CASE", "checks", "ids", "spec_checksums", "arrays_sha256"}` |
| `kc4(proc_w0, proc_star, handoff) -> dict` | `r = hwsb_known.kb4(proc_w0, proc_star)`; `z_ok = Fraction(r["w_star"]["Z_bound"]) == handoff["Z_bound"]`; `f_ok = k4b_cert.F_plan(handoff["Z_bound"]) == handoff["F_plan"]` and `k4b_cert.F_plan(r["w_star"]["Z_bound"]) == handoff["F_plan"]`. PASS iff `r["status"] == "PASS"` and both |
| `kc7(table=None) -> dict` | (a) inside `bound_stage_c(load_table(which="identity"))`: on the synthetic fixture of §11.4, each bound K4b stage function used under stage C (`k4b_stats.model_status`, `overall`, `bounds`, `k4b_cert.F_plan`, `margin`, `k4b_data.sample_block` on a 12-state synthetic process with `n = BLOCK`, `history_table`, `k4b_decoder` seed scopes, `k4b_fresh.bootstrap_inputs`) returns `==`/bitwise what the unbound call returns; (b) inside `bound_stage_c()`: `audit()` PASS; `hwsc_gates.p1c_ladder(X−, X+, r4n, F, D)` equals `hwsb_gates.ladder_pilot(X−, X+, r4n, F, models=MASTERS, seeds=P1C_SEEDS, D_bar=D, ladder=LADDER)` on synthetic arrays (every value `==`); the audit's `left_unchanged` hits include `("k4b_stats", "sd_upper.__defaults__")` and `("k4b_stats", "centered.__defaults__")`; the first 64 `integers(0, 2**63)` draws of `k4b_data.history_generator("cal", 0)` equal those of `SeedTree(0).generator("data", "hwsc-v1", "cal", 0, "cylinder", "overlap", "1.75")`; (c) after exit every table attribute `is` its pre-entry object. PASS iff all |
| `kc8(job) -> dict` | runs `python -s -m pytest tests/hwsc/test_a_k4b_known_bound.py -p no:cacheprovider -q --junitxml <basetemp>/kc8.xml --basetemp X:/Downloads/topo-scratch/test_hwsc-<job>/pytest` as a subprocess (`PYTHONPATH=<worktree>/src`, TEMP under the same folder); PASS iff exit code 0 and the junit file reports ≥ 1 test, 0 failures, 0 errors |
| `kc9(out) -> dict` | `hwsc_registry.build("REHEARSAL", out/"registry"/"rehearsal", handoff=load_handoff())`; PASS iff status PASS; records `status`, `cpu_s`, `peak_memory_bytes`, `n_digests`, `problems` |
| `run_kc(out, auth, sched, job, store=None) -> dict` | items KC0 → KC9 in CONTRACT `known_cases.order`, each recorded as a gate; KC0 = `g0c(out, "KC", auth, sched)`; KC1 = `kc1(store)` (`store = ArtifactStore(LocalFSBackend(out/"artifacts"))`); KC2, KC3 = `hwsb_known.kb2_kb3(hwsb_known.w0_process())` (KB2 reading → KC2 status `PASS`, `PASS_WITH_NUMERIC_DRIFT` or `FAIL_TECHNICAL/KNOWN_CASE`; KB3 → KC3); KC4 = `kc4`; KC5 = `hwsb_kb.kb5(proc_star)`; KC6 = `hwsb_kb.kb6(proc_w0, ckpt100)`; KC7 = `kc7()`; KC8 = `kc8(job)`; KC9 = `kc9(out)`. Pause check (`hwsc_driver.pause_or_raise_c(out, "KC", t0)`) at every item boundary. The first failure stops: its status (KC0 keeps its own; every other `FAIL_TECHNICAL/KNOWN_CASE`), later items `NOT_RUN`. Writes `stages/KC/KC_RECORD.json` (§13) and `complete_stage(out, "KC", [KC_RECORD, G0C.json, every file created under artifacts/ by this job])` |

## 6. `hwsc_gates.py` (≈290 lines): H1-C, L1, P1, N, annotation, outcome, licence

| Name | Contract |
|---|---|
| `expected_meta_c(j, step, record) -> dict` | `{"artifact_id": record["checkpoint_ids"][str(step)], "artifact_type": "Checkpoint", "run_key": ["hwsc-v1", KEY, j], "step": step, "status": "complete", "init_seed_key": f"init/hwsc-v1/{KEY}/{j}", "init_seed": SeedTree(j).seed("init", "hwsc-v1", KEY, j), "payload_sha256": record["checksums"][str(step)]}` |
| `exclusion_check(ids, handoff) -> dict` | `bad = sorted(set(ids) & set(handoff["stage_c_exclusions"]))`; `{"ok": not bad, "excluded": bad}` |
| `law_identity(proc, handoff) -> dict` | `law = hwsb_law.law_bound(proc["T"], proc["E_canon_shared"], proc["pi"], proc["coords"], SIGMA, NEIGHBOUR)`; any exception → `C1GateFailure("FAIL_TECHNICAL/LAW_BOUND", repr)`; `law["status"] != "BOUNDED"` or `law["Z_bound"] != handoff["Z_bound"]` (exact Fraction) → `C1GateFailure("FAIL_TECHNICAL/LAW_BOUND", …)`. Returns `{"status": "PASS", "Z_bound": Fraction, "kappa", "delta", "sigma", "neighbour"}` |
| `h1c(out, ctx, handoff, store, stage="E1") -> dict` | §11.2 gate 1 (uses `exclusion_check`, `law_identity`, `hwsc_data.process_identity`, `hwsc_data.p_d2a_check`). Raises `C1GateFailure`; any other exception inside → `FAIL_TECHNICAL/IDENTITY` |
| `l1(out, ctx) -> dict` | §11.2 gate 4 |
| `p1c_ladder(X_minus, X_plus, r4n, F_plan, D_bar) -> dict` | `hwsb_gates.ladder_pilot(X_minus, X_plus, r4n, F_plan, models=MASTERS, seeds=P1C_SEEDS, D_bar=D_bar, ladder=LADDER)` |
| `choose_N(N_C, ladder_result) -> dict` | `N_P1 = ladder_result["N"]`; `N_P1 is None` → `{"status": "INCONCLUSIVE/UNDERPOWERED", "N": None, "k": None, "N_P1": None, "N_C": N_C}` regardless of `N_C`; else `N = max(int(N_C), N_P1)`; `N not in LADDER` → `C1GateFailure("FAIL_TECHNICAL/NUMERICAL", …)`; `k = N // BLOCK`; status PASS |
| `p1c(out, ctx, handoff) -> dict` | §11.2 gate 10 (line-for-line mirror of `k4b_driver.p1`; only the ladder call and the N rule differ) |
| `positive_below_margin(per_model) -> dict` | `per_model` the ENDPOINT `per_model` (`{j: {"L", "F_minus", "status", ...}}`, keys int or str). Per j: `pos = Fraction(float(L)) − Fraction(F_minus) > 0` (exact; `F_minus` a Fraction or its str); `kind = "EXCLUDE"` if pos and status == `EXCLUDE`; `"UNRESOLVED"` if pos and status ∈ {`UNRESOLVED`, `UNRESOLVED/NUMERICAL`}; else None. Returns `{"per_model": {j: kind}, "positive": {j: pos}, "models": [j with kind], "all_positive": all pos}` |
| `annotations(result) -> list` | from the ENDPOINT result: `f"POSITIVE_BELOW_MARGIN_{j}"` for each annotated j (`"…_EXCLUDE"`/`"…_UNRESOLVED"` kind kept in a sibling dict); `"POSITIVE_BELOW_MARGIN"` iff `all_positive` and `result["overall"] != "SUPPORT"`; `f"NEGATIVE_ALIGNMENT_{j}"` for labels; `"UNRESOLVED/NUMERICAL"` per model; `"FRESH_B4_LOW"` if set; init qualifiers as reported. Never changes the outcome |
| `outcome(state) -> dict` | §12.1 |
| `licence(oc, fill) -> str` | §12.3 |

## 7. `hwsc_driver.py` (≈380 lines): records, gate runner, jobs, ledger, pauses, CLI

### 7.1 Records, lineage, gate runner

| Name | Contract |
|---|---|
| `status_of(exc) -> str` | `C1GateFailure`, `hwsb_config.HwsbStop`, `hws_worlds.HwsStop` → `exc.status`; `StageFailure` with code `NONFINITE_LOSS` → `FAIL_TECHNICAL/NONFINITE`, `SPLIT_OVERLAP` → `FAIL_TECHNICAL/LINEAGE`; `hwsb_driver.Paused` → `PAUSE`; anything else → `c1_records.classify_exception(exc)[0]`. A result without `/` gets `"/UNEXPECTED"` appended (`"FAIL_TECHNICAL"` → `"FAIL_TECHNICAL/UNEXPECTED"`) |
| `run_gates_c(out, steps, dry_continue=False) -> list` | mirror of `k4b_driver.run_gates` with `status_of`: each `(gate, fn)`; after the first non-PASS, later gates are recorded `NOT_RUN` without calling `fn`, unless `dry_continue` (dry run only, choice 22), where they are still called and their status recorded. Gate details: `fn()` result minus `status`. A `PAUSE` stops the job (exit 4) after recording |
| `lineage_c(out) -> dict` | mirror of `k4b_release.lineage_ok` with the stage-C record files: top-level names in K4b `RECORD_FILES` plus `FREEZE.json`, `KC_ACCEPT.json`, `RELEASE_A.json`, `RELEASE_B.json`, `RESERVATION_W2.json`, `REGISTRY_OBLIGATION.json`, and the patterns `AUTH_*.json`, `SCHED_*.json`, `ACCEPT_*.json`, `DECISION_*.json`; free directories `logs`, `operations`, `tmp` and `tmp-*`; `superseded/<job>/` checked by its `SHA256SUMS`; every other file must equal (sha256) a file recorded by a `STAGE_COMPLETE` event (later events win); else `C1GateFailure("FAIL_TECHNICAL/LINEAGE", …)`. Absent store → PASS. Every read through `guard` |
| `auth_ok(auth, stage) -> dict` | `{"ok": stage in auth["stages"] and auth["owner_auth_sha256"] == CONTRACT addendum-34 sha256 and auth["run_approval_sha256"] == FREEZE.json run_approval_sha256 (TRAIN, E1, REG2, E2, KC), "reason"}`; missing record → ok False |
| `sched_ok(sched, stage) -> dict` | CONTRACT `records.SCHED`: `rule_w2 = sched["live_history_reservations"] == []`; `rule_w3 = sched["frozen_registries_awaiting_draw"] == []`; DRY needs `rule_w2`, every other stage both. Missing record → ok False |
| `preflight(out, stage, auth, sched, repo=REPO) -> dict` | `verify_freeze_c(out, repo)` (missing → refusal; mismatch → `FAIL_TECHNICAL/FREEZE`); `auth_ok`; `sched_ok`. A refusal records gate `AUTH` or `SCHED` = `INCONCLUSIVE/RESOURCE_OR_AUTHORITY` and returns `{"refused": True}` before anything is sampled |
| `freeze_c(out, repo, h_exec, dry_report, pf_record, run_approval) -> dict` | writes `out/FREEZE.json` (exclusive) with CONTRACT `freeze_fields`: protocol name and sha256, CONTRACT/API/TEST_PLAN sha256, `h_exec`, `implementation_files` (`{relpath: sha256 of the git blob at h_exec}` for every `tools/hwsc/*` and `tests/hwsc/*`), `implementation_sha256` (sha256 of the canonical JSON of that map), `reuse_sha256` (CONTRACT, re-hashed at h_exec; any mismatch refused), `dry_run_report_sha256`/`path` (refused if its `implementation_sha256` differs), `pf_record_sha256`, `run_approval_sha256`, `environment`, `created_utc` |
| `verify_freeze_c(out, repo) -> dict` | every FREEZE hash re-checked against the working tree and `reuse_sha256`; mismatch → `C1GateFailure("FAIL_TECHNICAL/FREEZE", …)` |
| `s0(repo, r_ref, h_exec) -> dict` | CONTRACT `s0`: `git diff --no-renames --name-status r_ref h_exec -- <protected_paths>`; every line must be `A` with a path under an allowlist prefix; `reuse_sha256` equal at `h_exec`; `tools/c1prime/CONTRACT.json` `chart` equal at both refs; protocol sha256 and request sha256 equal CONTRACT; `k4b_config.MARGIN == Fraction(1, 100)`. `{"status": "PASS" or "INVALID", …}` (INVALID: do not run; not an outcome) |

### 7.2 Budget (§8)

| Name | Contract |
|---|---|
| `central(stage, k=None, R=None) -> float` | CONTRACT `cpu.central_s[stage]`; for `E2`: `R + 1720.1*k` (`R` default the frozen value, else `cpu.E2_planning.R`) |
| `pause_check_c(stage, stage_cpu, cum_cpu, k=None) -> dict` | `stage_th = 3*central(stage, k)`; `cum_th = 3*(cumulative central through stage)` (E2: `11306.6 + central("E2", k)`); `pause = stage_cpu > stage_th or cum_cpu > cum_th` (strict); `trigger` ∈ {`"STAGE"`, `"CUMULATIVE"`, `"BOTH"`, None}; returns `{"pause", "trigger", "stage_cpu", "stage_threshold", "cum_cpu", "cum_threshold"}` |
| `ledger_read(path) -> dict` | `{"study": "hwsc-v1", "entries": [], "cumulative_cpu_s": 0.0}` when absent |
| `ledger_append(path, label, job, stage, cpu_s, source, master=None) -> dict` | appends `{"label", "job", "stage", "cpu_s", "source", "master", "utc"}`; recomputes `cumulative_cpu_s`; writes `path.with_suffix(".json.tmp")` then `os.replace`. A `label` already present → `C1GateFailure("FAIL_TECHNICAL/LEDGER", …)` (unique labels per attempt) |
| `pause_or_raise_c(out, stage, t0, ledger_path=None, cont=None, k=None) -> None` | `ledger_path=None` disables it (dry and tests). `stage_cpu, cum_cpu = hwsb_driver.running_cpu(stage, ledger_path=ledger_path, t0=t0)`; a `cont` JSON `{"stages": [...]}` naming the stage exempts it; on `pause`: `STAGES.jsonl` event `PAUSE`, gate `f"PAUSE_{stage}"` status `PAUSE` with **only** the CPU fields (S1: no gate value), raise `hwsb_driver.Paused` |

### 7.3 Jobs (§5; one metered stage per job)

| Name | Contract |
|---|---|
| `run_kc(out, auth, sched, job) -> dict` | preflight `"KC"`, then `hwsc_known.run_kc` inside `bound_stage_c()` with `binding_audit` recorded as gate `BINDING_AUDIT` first |
| `run_train(out, auth, sched, master, kc_accept, cont=None) -> dict` | §11.1 |
| `obs_inventory(out) -> dict` | requires the three `TRAIN_RECORD.json` with status `COMPLETE`; writes `stages/TRAIN/OBS_INVENTORY.json` = `hwsb_registry.history_inventory(out)` (exclusive) and `complete_stage(out, "TRAIN_INVENTORY", [it])`. Called at the end of the TRAIN job of the last master in `MASTERS` order when all three are COMPLETE; also a CLI subcommand |
| `run_e1(out, auth, sched, release_path, session, task_sha256, mailbox=MAILBOX) -> dict` | §11.2 |
| `run_reg2(out, auth, sched, accept_path) -> dict` | §11.3 |
| `run_e2(out, auth, sched, release_path, session) -> dict` | §11.4 |
| `export_c(out, result, oc, ann, fill) -> Path` | `d = out/"stages"/"S8"`; `RESULT.json` (exclusive) = `dict(result, outcome=oc["outcome"], outcome_detail=oc, annotations=ann, licence=hwsc_gates.licence(oc, fill), lineage_disclosure=DISCLOSURE, does_not_establish=CONTRACT licences.does_not_establish, protocol_sha256=…)`; then `SEALED_OPENED.json` (exclusive) = `json.loads((out/"SEALED_VALIDATION.json").read_text())` (missing → `C1GateFailure("FAIL_TECHNICAL/SEALING", …)`); then exactly one `k4b_driver.complete_stage(out, "S8", [RESULT.json, SEALED_OPENED.json])` (D6 fix, C8). Returns the RESULT path |
| `run_close(out, status, reason) -> dict` | after an early stop: writes `stages/CLOSE/CLOSE.json` with `hwsc_gates.outcome` of the recorded gates and the licence (no RESULT, no unsealing) and `complete_stage(out, "CLOSE", [it])` |
| `main(argv=None) -> int` | subcommands `s0`, `kc`, `train`, `obs-inventory`, `e1`, `reg2`, `e2`, `close`, `dry`, `freeze`, `inventory`; options `--out` (default `STORE`), `--auth`, `--sched`, `--kc-accept`, `--master`, `--release`, `--accept`, `--session`, `--task-sha256`, `--mailbox`, `--continue`, `--reason`, `--h-exec`, `--r-ref`, `--dry-report`, `--pf-record`, `--save`, `--compare`, `--job`. Exit codes: 0 complete; 2 refused (nothing sampled); 3 STOP (FAIL_TECHNICAL); 4 PAUSE; 5 INCONCLUSIVE (owner STOP at a hold, NOT_LEARNED, a K4b INCONCLUSIVE) |

## 8. `hwsc_dry.py` (≈380 lines): DRC1–DRC14 (§7)

| Name | Contract |
|---|---|
| `drc1(out, ctx)` … `drc14(out, ctx)` | one function per case of TEST_PLAN §4, each `{"status": "PASS" or "FAIL" or "NOT_RUN", "details"}`; streams only under the dry scopes (`("data", "hwsc-v1", "DRY", <case>, …)` for train/dev/blocks, `k4b_data` streams under `load_table(which="dry", case=…)`), masters 629911–629913, seeds `DRY_SEEDS` (DRC6 and the KC7-type check also use 620311/620315 on synthetic arrays, choice 24); planted fixtures labelled `"fixture": true` |
| `build_tiny_process_c(store, masters=DRY_MASTERS) -> dict` | `hwsb_dry.build_tiny_process(store, masters)` |
| `e4_eval_check_c(ckpt, proc, canon32, case_dir) -> dict` | R-0176-G3 (DRC2): the geometry-dependent paths on in-memory w\* DRY rows, items (a)–(e) of §18 R-0176-G3; returns `{item: {"reading": "EXACT" or "VALUE", "status", "details"}}` |
| `synthetic_root(base) -> dict` | builds under `base` a synthetic project root and scratch root for DRC1/DRC9 (every reader's store shape, §4), returns their paths; never the real roots |
| `run_dry(out=DRY_STORE, sched=None, only=None) -> dict` | requires `sched_ok(sched, "DRY")`, else `{"status": "REFUSED", "reason"}` without running or writing; runs the cases (or `only`); writes `out/stages/DRY/DRY_REPORT.json` `{"cases", "all_pass", "implementation_files", "implementation_sha256", "h_exec", "tree_clean", "inventory_before", "inventory_after"}`; never writes `HIST_*.npz`; never issues a real master, stream or K4b seed name value outside DRC6/KC7-type synthetic bootstraps |

## 9. `hwsc_meter_bind.py` (≈100 lines): meter binding (§8.3, RC-13; DRC13)

| Name | Contract |
|---|---|
| `job_paths(job, kind) -> dict` | `kind == "test"` (J-C1, DRY): `out = SCRATCH/f"test_hwsc-{job}"`, `temp_root = out`, `basetemp = out/"pytest"`; `kind == "store"` (KC, TRAIN, E1, REG2, E2): `out = STORE`, `temp_root = STORE/"tmp"`, `basetemp = None`; else `ValueError` |
| `memory_cap(stage) -> int` | CONTRACT `resources.memory_cap_bytes[stage]` (`REG2` uses `E2`'s); unknown → `ValueError` |
| `bind(job_id, task_sha256, out, worker_session, stage, temp_root=None) -> None` | `k4b_meter_bind.bind(job_id, task_sha256, out, worker_session)`; `winjob.MEMORY_CAP = memory_cap(stage)`; `k4b_meter_bind.TEMP_ROOT = str(temp_root or out)` (so `child_env(job)` gives TEMP/TMP/TMPDIR `<temp_root>/tmp-<job>` and thread vars "1"); `meter.CAP_S = meter.STOP_NEW_S = inf`; `OUTPUT_CAP = 4 GiB` |
| `placement_ok(paths, root=ROOT) -> dict` | as `hwsb_meter_bind.placement_ok` with `STORE` = hwsc-store and `SCRATCH`: kind test → `out_outside_root`, `temp_outside_root`, `basetemp_outside_root`, `test_prefixed` (`out` directly under `SCRATCH`, name starting `test_`); kind store → `out_is_store`, `temp_under_store_tmp` |
| `effective_settings() -> dict` | `{"memory_cap", "temp_root", "ledger", "cap_s", "output_cap", "thread_vars"}` |
| `main() -> int` | argv `--job`, `--task-sha256`, `--session`, `--kind`, `--stage` (all required; exit 2 if missing or unknown), then the meter argv; `bind(...)`; exit 3 when `RUN.lock` exists and does not name the session; `op_guard.archive_stale(out)` when `METER_ACTIVE.lock` is absent; `meter.limit_reason = k4b_meter_bind.make_limiter(op_marker=out/op_guard.MARKER)`; `os.environ.update(k4b_meter_bind.child_env(job))`; `sys.argv = [argv0] + k4b_meter_bind.rewrite_argv(rest)` (`--max-cpu inf --max-wall inf`); `return meter.main()`. Disk safe-STOP (C: ≥ 2 GB, X: ≥ 30 GB) and op-guard precedence are `k4b_meter_bind`'s (K4B §11.7) |

## 10. Reused functions, unchanged (§10.2; file hashes in CONTRACT `reuse_sha256`, blob bytes at af5e7b4)

| Module | Names used under stage C (signatures as in their own API.md) |
|---|---|
| `k4b_driver` | `begin_stage(out, stage)`, `complete_stage(out, stage, files) -> dict`, `checkpoint_meta(artifact_root, id)`, `load_checkpoint(id)` (reads `ARTIFACTS` at call time), `oracle_val(out, ctx)`, `b4_val(out, ctx)`, `c0_cal_stage(out, ctx)`, `c0_val_stage(out, ctx)`, `cert_val(out, ctx)`, `run_gates` (reference only) |
| `k4b_fresh` | `require_release_b(out, release_path, session)`, `sample_test(out, proc, release, reservation_path)`, `t_pre(out, ctx)`, `endpoint(...)`, `endpoint_gate(ctx)`, `load_recorded(out, stage, name)`, `load_frozen(out)`, `bootstrap_inputs`, `control_summary`, `init_qualifier` |
| `k4b_stats` | `model_status(L, U, F_minus, F_plus)`, `overall(per_model)`, `bounds`, `joint_bootstrap`, `write_sealed(out, arrays) -> sha`, `check_unsealed(report)`, `SEALED_FILE`, `SEALED_KEYS` |
| `k4b_cert` | `F_plan(Z)`, `margin(B_num, Z)`, `b_num`, `b4_guard`, `references`, `moment_check`, `envelopes`, `endpoint_bounds`, `certify`, `CAP`, `S_ENVELOPE` |
| `k4b_data` | `history_generator(split, block)`, `sequence_ids(split, block)`, `sample_block(T, E, pi, split, block)`, `history_table(canon32, ids, split, block)`, `model_inputs`, `seq_disjoint`, `predicate_check`, `duplicates`, `sealed_d2a_predicate` |
| `k4b_config` | `chart_cfg()`, `check_chart_equality()`, `check_checkpoint_meta(meta, expected)`, `MARGIN`, `RANKS`, `BLOCK`, `LADDER` |
| `k4b_charts`, `k4b_scores`, `k4b_decoder` | through the K4b stage functions above |
| `k4b_release` | `verify_release`, `verify_reservation(path, release, sampling_began=False)`, `start_reservation(path, scope, utc)`, `archive_attempt`, `regenerated_identical`, `needs_owner`, `RECORD_FILES` |
| `k4b_registry` | `inventory(root, exclude)`, `classify(inv, readers)`, `HISTORY_KEYS`, `IDENTITY_KEYS`, `source_f`, `revalidate_coverage`, `validate_handoff_json`, `summary` |
| `c2_registry` | `token_sources(root)`, `x6_source(store, run_dir)`, `Registry` (`load(store, version)`, `contains(hex)`, `seq_ids`, `sealed_ranges`, `predicates`), `separation` (reference), private helpers of §0 |
| `nd_registry` | `source_c2(store, bound=None)`, `source_c2_superseded(store)`, `source_scratch(root)`, `source_parallel(store, tag)` |
| `hwsb_config`, `hwsb_data`, `hwsb_registry` | `Plan`, `dry_plan`, `run_key`, `MODEL_CFG`, `TRAIN_CFG`; `build_process`, `spec_checksums`, `arrays_sha256`, `data_generator`, `stream_record`, `make_train_dev` (DRC4 reference); `registry_digests(store, expected)`, `history_inventory(store)` |
| `hwsb_train` | `train(store, obs_ids, master, plan, hold)`, `HoldRule(out_dir, cap_s, steps, from_step, cpu_fn, poll_s, sleep)`, `hold_check`, `set_threads(n)`, `torch_versions()` |
| `hwsb_eval` | `model_predictive(checkpoint, canon32, perm)`, `oracle_predictives(proc, canon32)`, `b1(q, p)` |
| `hwsb_gates` | `ladder_pilot(X_minus, X_plus, r4n, F_plan, models, seeds, D_bar, ladder)` |
| `hwsb_law` | `bound_law(sigma, neighbour)`, `law_bound(T, E, pi, coords, sigma, neighbour)` |
| `hwsb_known`, `hwsb_kb` | `classify_hits`, `w0_process`, `kb2_kb3`, `kb4`, `jsonable`; `kb5`, `kb6` |
| `hwsb_driver` | `running_cpu(stage, ledger_path, t0)`, `Paused`, `status_of` (reference) |
| `hws_exact`, `hws_driver` | `p_d2a(T, E, pi)`; `seed_search` (reference for `seed_search_c`) |
| `c1_model`, `c1_cert`, `c1_means`, `c1_records` | `load_model64`, `activations`, `model_inputs`; `a1_selftest()`; `tree_mean`, `quantile_with_rank`, `rank_for`; `C1GateFailure`, `classify_exception` |
| `stage_records` | `sha256`, `write_new`, `save_npz`, `record_gate`, `gates_so_far`, `stages_so_far` |
| `topo_pilot.contracts` | `ArtifactStore`, `LocalFSBackend`, `MemoryBackend`, `Checkpoint`, `ObservationSet`, `SeedTree`, `SequenceLayout`, `StageFailure`, `payload_checksum` |
| `topo_pilot.dataset` | `HMMSampler`, `checks.process_code`, `make_sequence_ids`, `check_disjoint` |

## 11. The jobs and every gate's computation, in order (§5)

The first non-PASS gate ends the cohort; later gates are recorded `NOT_RUN` (K4B §6). Every computed value is recorded. Every stage-C job runs S0's freeze check and the binding audit at dispatch (`BINDING_AUDIT` gate, inside `bound_stage_c()`; non-PASS → `FAIL_TECHNICAL/BINDING`, nothing sampled). All stage functions run inside one `bound_stage_c()` for the whole job.

### 11.1 TRAIN job (one per master, in `MASTERS` order)

1. Preflight `"TRAIN"`; `KC_ACCEPT.json` `{"accept": true, "kc_record_sha256", "six_thread_ruling": false}` must have `accept` true and `kc_record_sha256` equal to the sha256 of `stages/KC/KC_RECORD.json`, whose status is `PASS` (else refused, gate `KC_ACCEPT`). `stages/TRAIN/<master>/TRAIN_RECORD.json` existing → `FAIL_TECHNICAL/RERUN` (an interrupted attempt is first archived by `k4b_release.archive_attempt`; X-3).
2. `pause_or_raise_c(out, "TRAIN", t0, STUDY_LEDGER)`.
3. `store = ArtifactStore(LocalFSBackend(out/"artifacts"))`; `proc = build_process_c(store)`; world/transition ids equal CONTRACT (else `FAIL_TECHNICAL/IDENTITY`).
4. `obs = make_train_dev_c(store, proc, master, HWSC_PLAN)` (train 131,072 × 33, dev 4,096 × 33; streams `("data", "hwsc-v1", split, KEY, master)`; replicates `hwsc-v1/<split>/<master>`).
5. `threads = hwsb_train.set_threads(1)`; `hold = hwsb_train.HoldRule(out/"stages"/"TRAIN"/str(master), cap_s=6006.6282, steps=5000, from_step=1000)`.
6. `res = hwsb_train.train(store, {"train": obs["train"], "dev": obs["dev"]}, master, plan=HWSC_PLAN, hold=hold)`; require `res["run_key"] == ["hwsc-v1", KEY, master]` (= `hwsc_config.run_key`), checkpoints at exactly the 12 `checkpoint_steps`, `summary["steps_done"] == 5000`, every recorded train loss finite. `StageFailure NONFINITE_LOSS` → `FAIL_TECHNICAL/NONFINITE`; owner STOP at a hold → `INCONCLUSIVE/RESOURCE_OR_AUTHORITY` (record written with that status; never restarted from weights).
7. `TRAIN_RECORD.json` (§13); `complete_stage(out, f"TRAIN_{master}", [TRAIN_RECORD, HOLD_/DECISION_ files, every new file under artifacts/])`; gate `TRAIN_<master>` `PASS`. For the last master with all three COMPLETE: `obs_inventory(out)`.

### 11.2 E1 job (release A): gates 0–10 in order

Context: `rel = k4b_release.verify_release(release_path, "A", task_sha256, session, out/"FREEZE.json")`; `handoff = load_handoff()`; `ctx = {"release": rel, "reservation_path": out/RESERVATION_FILE, "handoff": handoff}`; `rel["reservation"] == RESERVATION_ID`.

| # | Gate | Computation |
|---|---|---|
| 0 | `G0C` | `hwsc_known.g0c(out, "E1", auth, sched, rel)` |
| 1 | `H1C` | (1) for j in MASTERS: `rec_j = read_json(out/"stages"/"TRAIN"/str(j)/"TRAIN_RECORD.json")`; its sha256 equals `rel["train_records"][str(j)]` and the latest `STAGE_COMPLETE` hash for `TRAIN_<j>`; `rec_j["status"] == "COMPLETE"`. (2) for step in (5000, 0): `meta = k4b_driver.checkpoint_meta(out/"artifacts", id)`; `k4b_config.check_checkpoint_meta(meta, expected_meta_c(j, step, rec_j))` PASS; the init seed of steps 0 and 5000 equal. (3) `exclusion_check(six ids, handoff)["ok"]` (else `FAIL_TECHNICAL/IDENTITY`). (4) `ckpts[(j, step)] = k4b_driver.load_checkpoint(id)`; `models[(j, "step5000" or "step0")] = c1_model.load_model64(ckpt)[0]` (exact round trip). (5) `proc = build_process_c(store)` (`store = ArtifactStore(LocalFSBackend(out/"artifacts"))`); `hwsc_data.process_identity(store, proc)["ok"]`. (6) `law = law_identity(proc, handoff)` (`hwsb_law.law_bound(T, E_canon_shared, pi, coords, 7/4, 1/5)` BOUNDED and equal to HANDOFF `Z_bound`, else `FAIL_TECHNICAL/LAW_BOUND`). (7) `c1_cert.a1_selftest()`; `torch.get_num_threads() == 1`. (8) `p_d2a_check(proc, handoff["p_D2a"])` ok (else `FAIL_TECHNICAL/IDENTITY`). `ctx.update(proc=proc, models=models, ckpts=ckpts, Z=law["Z_bound"], p_d2a=…)`; writes `stages/E1/H1C.json` |
| 2 | `REG1` | `rel["kreg1_certificate"]` present (else `INCONCLUSIVE/AUTHORITY`); `begin_stage(out, "REG1")`; `m = hwsc_registry.build("K-REG1", out/"registry", handoff=handoff, own_expected=read_json(out/"stages"/"TRAIN"/"OBS_INVENTORY.json"))` (its sha256 equal to `rel["obs_inventory_sha256"]`); `complete_stage(out, "REG1", [manifest, digest file, run files])`; status ≠ PASS → raise it; `ctx["reg1"] = c2_registry.Registry.load(out, "K-REG1")` |
| — | sampling S3 | inside `h2c`: reservation verified; lgate b0 (4,096), cal b0, val b0 (3,072 each) |
| 3 | `H2` | `hwsc_data.h2c(out, ctx)` |
| 4 | `L1` | `lg = ctx["tables"]["lgate"]["canon32"]`; `q = hwsb_eval.oracle_predictives(proc, lg)`; for **every** j in MASTERS: `p = hwsb_eval.model_predictive(ctx["ckpts"][(j, 5000)], lg, proc["perm"][j])`, `r_j = hwsb_eval.b1(q, p)`. Any `r_j["status"] == "INCONCLUSIVE"` or non-finite `captured` → `FAIL_TECHNICAL/NUMERICAL` (a `check_rows` failure raises the same). `failing = [j: r_j["status"] == "FAIL"]` (captured < 0.8; equality passes). Writes `stages/E1/L1.json` `{"per_model": {j: r_j}, "failing", "k"}`; `failing` → `C1GateFailure("INCONCLUSIVE/NOT_LEARNED", f"{k}/3: {failing}")` with details `k`, `models` |
| 5 | `ORACLE-VAL` | `k4b_driver.oracle_val(out, ctx)` (moments of cal and val, `stages/S4/ORACLE_{cal,val}.npz`, Decimal references on all 3,072 val rows, `moment_check`; `FAIL_TECHNICAL/ORACLE`) |
| 6 | `B4-VAL` | `k4b_driver.b4_val(out, ctx)` (seed `SEEDS["val_b4"]` = 620312 via the bound `k4b_driver.SEEDS`; `guard_H5(lower, B^H + Z)`; `INCONCLUSIVE/HEADROOM` or `/NUMERICAL`) |
| 7 | `C0-CAL` | `k4b_driver.c0_cal_stage(out, ctx)` (activations of all cal rows, models `(j, step5000)`, `(j, step0)`; 512 landmarks; `k4b_charts.c0_cal`, `init_charts`, decoders `k4b_decoder.fit`, `freeze_production`, `ACTS_cal_b0.npz`) |
| 8 | `C0-VAL` | `k4b_driver.c0_val_stage(out, ctx)` |
| 9 | `CERT-VAL` | `k4b_driver.cert_val(out, ctx)` (`B ≤ 1e-4`, `|X̂| ≤ 4`) |
| 10 | `P1` | `hwsc_gates.p1c(out, ctx, handoff)`: `a = ctx["val_arrays"]`; `F = k4b_cert.F_plan(ctx["Z"])`; `D = {j: float(np.mean(a[j]["X_plus"] − a[j]["X_minus"]) / 2)}`; `lad = p1c_ladder({j: X−}, {j: X+}, {j: r4n}, F, D)`; `sealed = k4b_stats.write_sealed(out, {"mean_X_minus": {j: X−}, "mean_X_plus": {j: X+}})`; `nc = choose_N(handoff["N_C"], lad)`; `risk = registry_risk(ctx["p_d2a"], nc["N"])` if `nc["N"]`; report = `{"gates": stage_records.gates_so_far(out), "support": ctx["support"], "B4": {k: str(v)}, "sdU": {f"{j}{s}": v}, "ladder": {"status", "N": nc["N"], "k": nc["k"], "N_P1", "N_C", "candidates"}, "certificate": {k: str(v)}, "F_plan": str(F), "Z_bound": str(Z), "sealed_sha256": sealed, "registry_risk": risk, "lineage_disclosure": DISCLOSURE}`; `k4b_stats.check_unsealed(report)`; `begin_stage(out, "S5")`; `write_new(out/"stages"/"S5"/"VALIDATION_REPORT.json", report)`; `complete_stage(out, "S5", [it])`; then `nc` status non-PASS → `INCONCLUSIVE/UNDERPOWERED`; `risk["ok"]` False → `INCONCLUSIVE/REGISTRY_INCOMPLETE`. Returns `{"N", "k", "N_P1", "N_C", "sealed_sha256"}` |

Pause check (`pause_or_raise_c(out, "E1", t0, STUDY_LEDGER)`) after every gate. A non-PASS gate → `run_close`.

### 11.3 REG2 job (row 11; books stage `E2`, choice 4)

`ACCEPT_VALIDATION.json` `{"verdict": "ACCEPT", "validation_report_sha256", "by", "utc"}` with the sha256 of `stages/S5/VALIDATION_REPORT.json` (else refused, gate `ACCEPT`); `k4b_release.verify_reservation(out/RESERVATION_FILE, {"reservation": RESERVATION_ID})` PASS; `tables = {s: k4b_fresh.load_recorded(out, "S3", hist_name(s, 0))}` for lgate, cal, val; `begin_stage(out, "REG2")`; `m = hwsc_registry.build("K-REG2", out/"registry", handoff=…, own_expected=…, extra=tables)` (extra digests = each table's `digest`, seq ids = `seq_ids`); `complete_stage(out, "REG2", [manifest, digest file, run files])`; gate `REG2` = `m["status"]`. The coordinator then writes `RELEASE_B.json` (N, k from VALIDATION_REPORT, `kreg2_sha256` = sha256 of `registry/K-REG2.json`, `kreg2_sources`, `accept`, `w3_attestation`).

### 11.4 E2 job (release B): sampling S7 and gates 12–14

1. `rel = k4b_fresh.require_release_b(out, release_path, session)` (protocol sha256 = the view's; N = 3,072·k ∈ LADDER; K-REG2 bound) — gate `RELEASE_B`.
2. `H1C_E2`: steps (1)–(7) of gate 1 again (no sampling); `Z` must equal HANDOFF.
3. `tables = {s: k4b_fresh.load_recorded(out, "S3", hist_name(s, 0))}`; `stored = k4b_fresh.load_recorded(out, "S4a", "ACTS_cal_b0.npz")`; `frozen = k4b_fresh.load_frozen(out)`.
4. Sampling S7: `test = hwsc_data.sample_test_c(out, proc, rel, out/RESERVATION_FILE, dry)` (real run: `k4b_fresh.sample_test` unchanged; blocks `test_b0 … test_b(k−1)`, `stages/S7/HIST_test_b<b>.npz`). Steps 3 and §11.3 use `hist_name(split, 0, dry)`.
5. `ctx = dict(frozen, release=rel, reservation_path=…, proc=proc, tables=tables, test=test, Z=Z, stored_cal_acts=stored, recompute_cal_acts=…, test_acts=…)` exactly as `k4b_fresh.main` (`acts(canon32, j, s) = c1_model.activations(models[(j, s)], k4b_data.model_inputs(canon32, proc["perm"][j]))`; `recompute_cal_acts` keys `f"{j}_{s}"` for j in MASTERS, s in ("step5000", "step0")).
6. Gates: `H2-FRESH` = `hwsc_data.h2_fresh_c(out, ctx)`; `T-PRE` = `k4b_fresh.t_pre(out, ctx)` (oracle and references on every test row, determinism of all 3,072 cal activations for 3 + 3 models bitwise, extension, certificate ≤ 1e-4, fresh B4 with seed 620314 report only); `ENDPOINT` = `k4b_fresh.endpoint_gate(ctx)` (one joint bootstrap, seed 620313, 5,000 draws; L− rank 84, U+ rank 4,917; `F = max(B_num, 10⁻⁹) + Z`; `k4b_stats.model_status`/`overall` under the binding).
7. `ann = hwsc_gates.annotations(ctx["result"])`; `oc = hwsc_gates.outcome(state)`; gate `OUTCOME` (status `PASS`, details `oc`); `export_c(out, ctx["result"], oc, ann, fill)`.

### 11.5 The KC7 synthetic fixture

A 12-state, 36-symbol row-stochastic process drawn from `np.random.default_rng(7)` (Dirichlet rows), `n = BLOCK` rows for `sample_block`; endpoint fixture arrays `X−`, `X+`, `r4n` float64 [3,072] from `default_rng(77)` with `X− ≤ X+`; `F = Fraction(1, 10**4)`; `D = {j: 0.01}`. The fixture is generated in memory and never persisted.

## 12. Outcome, annotation and licences (§6)

### 12.1 `outcome(state) -> dict`

`state` keys: `fail` (None or a status string), `resource` (None or a reason), `l1` (None or `{"k": int, "models": [j]}`), `k4b` (None or an `INCONCLUSIVE/<reason>` status of gates 0–14 other than L1), `criterion`, `models` (chart failures), `endpoint` (None or the ENDPOINT result). Rules in order (§6.1):

1. `fail` → `fail` if it starts with `"FAIL_TECHNICAL/"`, else `"FAIL_TECHNICAL/" + fail`.
2. `resource` → `INCONCLUSIVE/RESOURCE_OR_AUTHORITY`.
3. `l1` with `k ≥ 1` → `INCONCLUSIVE/NOT_LEARNED`, `k`, `models`, `label = f"INCONCLUSIVE/NOT_LEARNED ({k}/3)"`.
4. `k4b` → if its reason ∈ CONTRACT `outcomes.k4b_reasons`: `k4b` (with `criterion`, `models` for CHART_UNAVAILABLE); `INCONCLUSIVE/AUTHORITY` or `INCONCLUSIVE/RESOURCE` → `INCONCLUSIVE/RESOURCE_OR_AUTHORITY`; any other → `FAIL_TECHNICAL/OUTCOME`.
5. `endpoint` → `endpoint["overall"]` (`SUPPORT`, `EXCLUSION`, `MIXED`, `INCONCLUSIVE`, `INCONCLUSIVE/NUMERICAL`), with `annotations(endpoint)`.
6. Otherwise `FAIL_TECHNICAL/OUTCOME` (returned, never raised).

Returns `{"outcome", "label", "k", "models", "criterion", "annotations": [...], "pbm": positive_below_margin result or None}`. `state_from_gates(records, l1_record=None, result=None) -> dict` maps gate records: the first `FAIL_TECHNICAL/*` → `fail`; `INCONCLUSIVE/RESOURCE_OR_AUTHORITY`, `/AUTHORITY`, `/RESOURCE` → `resource`; gate `L1` `INCONCLUSIVE/NOT_LEARNED` → `l1` (from its details); any other `INCONCLUSIVE/*` → `k4b`; `result` → `endpoint`.

### 12.2 The POSITIVE_BELOW_MARGIN annotation (§6.1, addendum 25 rule 6)

Per model: `Fraction(float(L−_j)) − F_{j,−} > 0` and `status_j` ∈ {`UNRESOLVED`, `UNRESOLVED/NUMERICAL`, `EXCLUDE`}; kind `EXCLUDE` ('positive, and certified below the margin') or `UNRESOLVED` ('positive, not resolved against the margin'). Overall `POSITIVE_BELOW_MARGIN` iff `Fraction(float(L−_j)) − F_{j,−} > 0` in all three models and the overall outcome is not `SUPPORT`. Exactly 0 is not positive; the next float above (`math.nextafter`) is. It never changes the outcome; it is a one-sided bound at the same nominal α against 0, with no added family claim.

### 12.3 `licence(oc, fill) -> str`

Head: `FAIL_TECHNICAL` for any `FAIL_TECHNICAL/*`; `INCONCLUSIVE/RESOURCE_OR_AUTHORITY`; `INCONCLUSIVE/NOT_LEARNED`; `INCONCLUSIVE/CHART_UNAVAILABLE`; `INCONCLUSIVE/<K4b reason>` for the other K4b reasons; `SUPPORT`; `EXCLUSION`; `MIXED`; `INCONCLUSIVE` for `INCONCLUSIVE` and `INCONCLUSIVE/NUMERICAL`. Template CONTRACT `licences[head]` filled by `str.format_map` with `fill ∪ {"k", "models", "criterion"}` (missing keys → `"n/a"`). For EXCLUSION: `" " + EXCLUSION_ORACLE_SENTENCE` iff `fill["delta4_orc_certified"]` is True and `fill["delta4_orc_lower"] > 0.01` (strict; the `delta4_orc` `all` entry's `alpha_bound` in the control summary), then always `" " + EXCLUSION_TAIL`. With a per-model POSITIVE_BELOW_MARGIN: `" " + POSITIVE_BELOW_MARGIN` (models filled) then, per annotated model kind, the `_EXCLUDE` or `_UNRESOLVED` sentence. Every report also carries `DISCLOSURE`; scientific outcomes (row 5) carry `does_not_establish`.

## 13. Records and file schemas

- **AUTH** `AUTH_<stage>_<job>.json` (coordinator): `{"job_id", "stages", "owner_auth_sha256" (addendum 34), "run_approval_sha256", "hws_store_reads": ["KC5 S3 w* table"] (KC only)}`.
- **SCHED** `SCHED_<job>.json` (coordinator, dated): `{"record", "utc", "coordinator_session", "live_history_reservations": [], "frozen_registries_awaiting_draw": []}`.
- **KC_ACCEPT.json**: `{"accept": true, "kc_record_sha256", "six_thread_ruling": false}`.
- **RELEASE_A.json** / **RELEASE_B.json**: CONTRACT `records.RELEASE_A`/`RELEASE_B` (K4b `k4b_release.FIELDS`, `FIELDS_B` plus the stage-C fields; `protocol_sha256` = stage-C protocol; `freeze_sha256` = sha256 of `hwsc-store/FREEZE.json`; `reservation` = `"RES-HWSC-W2"`; `train_records` = `{str(j): sha256}`).
- **RESERVATION_W2.json**: `k4b_release.start_reservation(out/"RESERVATION_W2.json", "HWSC-W2", utc)` (id `RES-HWSC-W2`, state ACTIVE, `job_states` renewed per job by the coordinator) from the first TRAIN job through the last test block (§9.4).
- **KC_RECORD.json** (`stages/KC/`): `{"status", "kc": {"KC0" … "KC9": {"status", "value", "reference", "tolerance"}}, "reading" (KC2), "deviation_flags", "process_ids", "arrays_sha256", "law_w_star" (Fractions as str), "Z_bound_w_star", "F_plan", "threads", "torch", "binding_audit", "registry_rehearsal", "protocol_sha256", "freeze_sha256"}`.
- **TRAIN_RECORD.json** (`stages/TRAIN/<master>/`): `{"master", "status": "COMPLETE" or the stop status, "run_key", "observation_ids": {"train", "dev"}, "streams", "sequence_id_replicates", "checkpoint_ids": {step: id}, "checksums": {step: sha}, "summary", "threads", "holds", "process_cpu_s", "process_ids", "dev_ce": {step: float}}`; `dev_ce` never appears in a hold report.
- **HOLD_<step>.json** / **DECISION_<step>.json**: hwsb API §3 (`step`, `cpu_s`, `projected_s`, `trigger`, `utc` only; decision `CONTINUE` or `STOP`).
- **H1C.json**, **L1.json** (`stages/E1/`): the gate details. L1 values are not sealed (§2.6).
- **VALIDATION_REPORT.json** (`stages/S5/`): §11.2 gate 10; passes `k4b_stats.check_unsealed`; no endpoint-reconstructing quantity (K4B §7.5).
- **SEALED_VALIDATION.json**: `k4b_stats.write_sealed` (protocol sha256 = stage-C, through the view).
- **RESULT.json**, **SEALED_OPENED.json** (`stages/S8/`): §7.3 `export_c`; both in one `STAGE_COMPLETE` of stage `S8`.
- **Study ledger** `agent-handoff/HWSC_CPU_LEDGER.json`: `{"study": "hwsc-v1", "entries": [{"label", "job", "stage", "cpu_s", "source", "master", "utc"}], "cumulative_cpu_s"}`; `source` the meter ledger path; appended by the coordinator after each job.
- **REGISTRY_OBLIGATION.json**: §4 `obligation`; hashed in the final report.
- **FREEZE.json**: CONTRACT `freeze_fields`.
- **DRY_REPORT.json**: §8.
- **Store layout**: CONTRACT `store_layout`.

## 14. Budget, pauses, holds, caps (§8)

- Measure-only: `--max-cpu inf --max-wall inf`. Disk floors C: ≥ 2 GB, X: ≥ 30 GB. Memory caps (CONTRACT `resources.memory_cap_bytes`): TRAIN and J-C1 8 GiB; DRY, KC, E1, REG2/E2 12 GiB. Native operation wall 600 s.
- Stage centrals (CPU-s): J-C1 1,200; DRY 600; KC 1,500; TRAIN 6,006.6 (3 × 2,002.2); E1 2,000 (re-set from KC9, TO_FREEZE); E2 = R + 1,720.1·k (R = KC9's measured registry CPU, TO_FREEZE; planning 300), fixed at release B from the released k. Cumulative centrals 1,200 / 1,800 / 3,300 / 9,306.6 / 11,306.6 / 11,306.6 + E2.
- Triggers (strict >): stage CPU > 3 × its central; running total > 3 × cumulative central through the current stage; checked at every item boundary (each KC item, each model, each gate). On a trigger no new item starts (exit 4); continuing needs the owner (`--continue`).
- Training hold (R-0176-G12): per-model central = HANDOFF `training_forecast_s` / 3 = 2,002.2094 CPU-s (the larger measured stage-B model); hold = 3 × central = 6,006.6282 CPU-s (the protocol's 6,006.6; value unchanged): `HoldRule(cap_s=6006.6282, steps=5000, from_step=1000)`, CPU = `time.process_time()` of the training process (data generation included); CONTINUE exempts the rest of that model (hwsb choice 9); STOP → `INCONCLUSIVE/RESOURCE_OR_AUTHORITY`. Pause and hold reports carry CPU, step or item and projection only (S1).

## 15. Choices (where the protocol leaves something open; simplest option; the protocol wins)

1. **Exceptions.** Stage-C code raises `c1_records.C1GateFailure(status, reason)`, the convention of the reused K4b stage functions; `status_of` maps reused stage-B/HWS stops and `StageFailure` codes (§7.1).
2. **`k4b_config.CONTRACT` is bound to the `k4b_contract_view` section** (protocol sha256 of stage C; K4b's `chart` and `registry` sections deep-equal; `authority.c1prime_disclosure` = the §6.4 disclosure). These are the only keys reused K4b code reads at call time under stage C; the view holds no forbidden constant, so the audit stays clean.
3. **Reservation.** One W2 reservation file `hwsc-store/RESERVATION_W2.json` (id `RES-HWSC-W2`, created by `k4b_release.start_reservation`) from the first TRAIN job to the last test block; releases name the id; the driver resolves the path as `out/RESERVATION_FILE`.
4. **K-REG2 is its own metered job `REG2`** between the coordinator's ACCEPT and release B (release B must bind the K-REG2 sha256, which `require_release_b` checks); its CPU is booked under stage `E2`, so the E2 central `R + 1,720.1·k` covers both jobs.
5. **Gate runner.** `run_gates_c` mirrors `k4b_driver.run_gates` with `status_of`, so stage-B `HwsbStop` statuses are kept.
6. **G0c seed search** is a mirror of `hws_driver.seed_search` that prunes blinded paths before opening (the unchanged function would open `hwsb-store/REPORT.json`, `GATES.jsonl`, `stages/EVAL/` and `jobs/0175/`; gap G-2).
7. **Blindness guard scope** (settled by R-0176-G1). The guard covers every direct read of stage-C code. The stage-B blindness list is the five CONTRACT `blindness.stage_b` rules; the frozen R1 mailbox reader (c) and `k4b_registry.validate_handoff_json` may parse every `*.json` under `agent-handoff/`, including `jobs/0175/*.json` (dispatch metadata only).
8. **lgate block** uses `hwsc_data.sample_block_c` (a mirror of `k4b_data.sample_block` with n = 4,096), because `k4b_data.sample_block` fixes n = 3,072.
9. **HWSC_PLAN** is a `hwsb_config.Plan` with the stage-C masters and the E4 recipe; sizes hold only train and dev (blocks are K4b-style).
10. **Train/dev mirror** takes `scope` as an argument so that DRC4 compares it with `"hwsb-v1"` against `hwsb_data.make_train_dev`.
11. **Ledger and pauses** are stage-C mirrors (`ledger_read` with study `hwsc-v1`, `pause_check_c` over the stage-C CONTRACT); `hwsb_driver.running_cpu` is reused with `ledger_path` explicit; `hwsb_driver.pause_check`/`pause_or_raise` read stage B's forecasts and are never called.
12. **Hold cap** = HANDOFF `training_forecast_s` = 6,006.6282 s per model (protocol §8.3 "6,006.6").
13. **Memory caps**: J-C1 8 GiB (the HWSB J-B1 value); DRY 12 GiB (DRC9's ≥ 20 M digest scale case runs under the 12 GiB cap); TRAIN 8 GiB; KC, E1, REG2, E2 12 GiB.
14. **L1 mapping.** `hwsb_eval.b1` status `INCONCLUSIVE` (G_C ≤ 1e-6) or a non-finite captured value is `FAIL_TECHNICAL/NUMERICAL`; `FAIL` (captured < 0.8) is a not-learned model.
15. **Init seed in H1-C** is checked against `SeedTree(j).seed("init", "hwsc-v1", KEY, j)` and must be equal at steps 0 and 5000.
16. **Private helpers** of `c2_registry` and `x6s1_registry` are used unchanged where `nd_registry.build` uses them (listed in §0); the stage-C build mirrors `nd_registry.build`.
17. **R5 ObservationSet digests** (replaced by R-0176-G4, §18): each dry ObservationSet is canonicalised by the `symbol_perm` of its EmissionSpec parent in the same dry store, as `hwsb_registry.registry_digests` does.
18. **R7 also reads archived evaluation tables** (`superseded/**/stages/S3|S7/HIST_*.npz`), which `hwsb_registry.registry_digests` would not read.
19. **Registry paths.** K-REG1 and K-REG2 in `hwsc-store/registry/` (loadable by `Registry.load(hwsc-store, version)`); REHEARSAL in `hwsc-store/registry/rehearsal/` (protocol KC9), never loaded for separation.
20. **p_D2a placement.** The agreement check (1e-12 relative) is part of H1-C (`FAIL_TECHNICAL/IDENTITY` on failure); the bound `(4,096 + 3,072 + 3,072 + N)·p ≤ 1/100` is checked at P1 once N is chosen (`INCONCLUSIVE/REGISTRY_INCOMPLETE` on failure).
21. **TRAIN inventory.** `stages/TRAIN/OBS_INVENTORY.json` (`hwsb_registry.history_inventory` of hwsc-store) is written after the third TRAIN record and bound in release A (`obs_inventory_sha256`); it is R7's `expected`.
22. **DRC1 continuation** (confirmed by R-0176-G3). In the dry run only, `run_gates_c(dry_continue=True)` calls every gate after a failure; K4b gates that need the 12 × 12, V = 36 geometry may fail by design on the tiny world and pass by returning a recorded value; their computations are checked on in-memory w\* DRY rows in DRC2 (`e4_eval_check_c`). Each DRC case states its reading (TEST_PLAN §4).
23. **Outcome inputs** are derived from the gate records by `state_from_gates`; G0c's `INCONCLUSIVE/AUTHORITY` and the meter's `INCONCLUSIVE/RESOURCE` count as row 2.
24. **Dry binding.** The dry run binds the K4b names with `load_table(which="dry", case=…)`: masters 629911–629913, K4b scope `hwsc-v1/DRY/<case>`, process `("cylinder", "overlap", "1.0")`, seeds `DRY_SEEDS` 629921–629925 (new numbers, used only in scratch), the case directory as store. The real bootstrap seeds 620311/620315 appear in the dry run only in DRC6 and the KC7-type check on synthetic arrays, as DRC6 requires (gap G-5).
25. **Model-step labels.** `ctx["models"]` uses K4b's `(j, "step5000")`/`(j, "step0")` keys; `ctx["ckpts"]` uses `(j, 5000)`/`(j, 0)` (float32 path for L1 only; logits never mixed with float64 activations).
26. **Validation report disclosure key** is `lineage_disclosure` (C10); RESULT.json keeps K4b's `c1prime_disclosure` key, which under the binding holds the same §6.4 text.
27. **Release A extra fields** `train_records` and `obs_inventory_sha256` bind the TRAIN records and the R7 inventory used by H1-C and REG1.
28. **Lineage check** `lineage_c` extends K4b's record-file list with the stage-C coordinator records (AUTH, SCHED, ACCEPT, KC_ACCEPT, RELEASE, RESERVATION, DECISION) and the `tmp` folder.
29. **Dry history names** are `DRYHIST_<split>_b<b>.npz` (the dry store never holds `HIST_*` names; §9.3). `k4b_fresh.sample_test` hard-codes `HIST_test_b<b>.npz`, so the dry run alone uses the mirror `hwsc_data.sample_test_c(dry=True)` (gap G-11); the real run calls the reused function unchanged.
30. **REG2 accept record** `ACCEPT_VALIDATION.json` binds the VALIDATION_REPORT sha256 (the HWS S0_ACCEPT pattern).

## 16. TO_FREEZE items (measured or decided before the execution freeze)

- `authority.run_approval` path and sha256 (the owner's explicit stage-C run approval).
- The R6 scratch inventory: `frozen_files` of the 50 top-level scratch directories that need them (the 45 holding array files outside `test_*` components plus the five `test_hwsb-*` folders with array files, R-0176-G9), and the decision of the 38 of them whose decision is still `TO_FREEZE` (33 + those five) (proposed EXCLUSION as pytest fixtures with `fixture_max_rows` 1,024, cloud `.pt` checkpoints, X6ZC dry checkpoints, or open): measured by a read-only header scan with `k4b_registry.inventory` semantics over each top-level scratch directory (`test_*` components pruned; `.pt` by name only; `payload.npz`, `state.pt`, `sealed/` never opened beyond `k4b_registry.inventory`), reviewed as a contract erratum.
- `cpu.re_set.R` and the E1 central: KC9's measured registry CPU-s (after the KC job; cost, not data).
- `authority.h_exec`, FREEZE.json, the dry-run report sha256, the PF record sha256.
- Any binding-table addition found by the implementation's audit (contract erratum, reviewed before the freeze).

## 17. Design gaps and contradictions found (for the coordinator; the protocol still wins)

- **G-1 (§3.4 R1 vs §7 DRC11, §9.2).** R1 keeps C2ND's reader (c) unchanged, which parses every JSON under `agent-handoff/` including `jobs/0175/`; DRC11 says any attempt by stage-C code to open a path under `jobs/0175/` raises FAIL_TECHNICAL/BLINDNESS. Choice 7 scopes the guard to stage-C code; alternatives are excluding `jobs/0175/` from reader (c) (coverage loss) or a ruling that machine digest reads are not openings.
- **G-2 (§4 KC0 vs §9.2).** KC0 names `hws_driver.seed_search` over the root; unchanged, it opens the blinded stage-B files. Choice 6 mirrors it with pruning.
- **G-3 (§7 DRC1).** The K4b gates need the 12 × 12, V = 36 geometry (BOS 36, period 12, 144 states), so the tiny DRB1 world cannot pass ORACLE-VAL…ENDPOINT, while persisting w\* rows in the dry store is forbidden. Choice 22 (DRC1 records every gate; DRC2, DRC5–DRC7, DRC10 cover the PASS paths).
- **G-4 (§3.4 R5).** R5 reads ObservationSet tokens "for tokens only" but forbids opening EmissionSpec payloads, so canonicalisation is impossible; choice 17.
- **G-5 (§7 vs DRC6).** "The dry run never issues a real-scope … seed" vs DRC6 "p1c draws with 620311/620315"; choice 24.
- **G-6 (§3.2 item 1 vs §3.3).** The table rebinds `k4b_config.CONTRACT` to `tools/hwsc/CONTRACT.json`, but reused K4b code reads `protocol_sha256`, `chart`, `registry` and `authority.c1prime_disclosure` from it; the whole stage-C contract also holds the binding table's old values. Choice 2 (a view section).
- **G-7 (§3.2 "called with the argument given explicitly").** `hwsb_driver.pause_or_raise` reads stage B's CPU forecasts through `pause_check`, so an explicit `ledger_path` is not enough; choice 11.
- **G-8 (§5 row 11 vs §8.2).** K-REG2 must exist and be bound in release B before E2 can start (`require_release_b`), so it cannot run inside the E2 job; choice 4.
- **G-9 (§3.4 R4 / HANDOFF obligation).** HANDOFF `registry_obligation` names `hwsb-dry` only; the protocol adds `hwsb-dry-0169` and `-0171` (R5), and the scratch listing also shows `hwsb-0168`, `hwsb-0170`, `hwsb-0172` … `hwsb-0175` job folders (no array files on 2026-10-29; EXCLUSION rows, re-checked at REG).
- **G-11 (§9.3 vs §3.3).** "Dry stores never use `HIST_*` names", but the reused `k4b_fresh.sample_test` (and `k4b_driver.h2`, replaced anyway) write `HIST_*` names; choice 29.
- **G-12 (§8.3 vs HANDOFF).** The protocol's per-model hold "6,006.6 s" is the three-model training forecast (3 × 2,002.2) used per model; this contract uses HANDOFF's exact 6,006.6282 (choice 12). Not a conflict, recorded for the run approval.
- **G-10 (§3.4 R7).** `hwsb_registry.registry_digests` reads `hist/` and ObservationSets only; archived stage-C evaluation tables under `superseded/` would be missed; choice 18.

## 18. Rulings R-0176-G1…G12 (erratum)

Source: coordinator rulings `agent-handoff/jobs/0176/RULINGS_PHASE1.md`, sha256 2497f1127cbcd06237859228eb3901164bebf6dd90db44d8b12932dd96838f83. This erratum amends §0–§17. It makes no scientific change, and the protocol still wins.

- **R-0176-G1 (blindness list).** The stage-B blindness list is exactly these five paths (CONTRACT `blindness.stage_b`):
  - `hwsb-store/REPORT.json`;
  - `hwsb-store/stages/EVAL/**`;
  - `hwsb-store/GATES.jsonl`;
  - `hwsb-store/CHART_CONSTRUCTIONS_*.json`;
  - `agent-handoff/jobs/0175/review.md`.

  Fixed behaviour:
  - `hwsc_config.blinded` matches these five rules only (§1.4).
  - `jobs/0175/task.json`, `request.before.json` and `task.md` are readable.
  - Reader (c) and `validate_handoff_json` parse every `*.json` under `agent-handoff/`, including `jobs/0175/*.json`.
  - The public-summary paths stay refused, through `public_summary` (CLAUDE.md rule).
  - DRC11 tests exactly the five-rule list.

  Choice 7 is settled and gap G-1 is closed.
- **R-0176-G2 (KC0 seed search).** Choice 6 is adopted. Fixed behaviour: `hwsc_known.seed_search_c` prunes `hwsb-store/stages/EVAL/` before listing it, and skips the blinded files before opening them. On a synthetic root without blinded paths, its hit list equals `hws_driver.seed_search` exactly (TEST_PLAN B, DRC14).
- **R-0176-G3 (dry-run geometry).** The dry run drives the whole pipeline on the tiny world with `dry_continue=True` (choice 22). The K4b gates that need the 12 × 12, V = 36 geometry pass DRC1 by returning a recorded value (reading **VALUE**). DRC2 checks the geometry-dependent paths separately with `hwsc_dry.e4_eval_check_c(ckpt, proc, canon32, case_dir)`. It uses in-memory w\* DRY rows (never persisted) and the E4 architecture at 20 steps:
  - (a) `hwsb_data.model_inputs` has BOS 36 and shape [n, 33].
  - (b) `hwsb_eval.model_predictive` has 36 columns and rows summing to 1 within 1e-6. It equals, bitwise, the `ActivationExtractor` logits softmaxed as in s3.py and re-indexed canonically, with rows in index order (the HWSB E6/E7 rule).
  - (c) `c1_model.activations` of `load_model64(ckpt)` is float64 [n, 128] at resid_post_3.
  - (d) `k4b_scores.oracle_moments` runs on the rows, and `k4b_cert.moment_check` against `k4b_cert.references` on the 4 lowest-ID rows is ok. Reading **EXACT** (this path does not depend on the model).
  - (e) `k4b_charts.build_chart` runs on the 20-step activations of 512 in-memory rows, with a ledger in a fresh case directory, and returns a recorded status. Reading **VALUE**.

  Every DRC case states its reading (TEST_PLAN §4).
- **R-0176-G4 (R5 canonicalisation).** Choice 17 is replaced. Fixed behaviour:
  - `hwsc_registry.source_dry` canonicalises each dry ObservationSet by the `symbol_perm` of its EmissionSpec parent in the same dry store (the `hwsb_registry.registry_digests` rule; §4).
  - These synthetic dry artifacts may be read. `state.pt` files and real-store payloads are never read.
  - An ObservationSet without exactly one EmissionSpec parent → INCONCLUSIVE/REGISTRY_INCOMPLETE.
- **R-0176-G5 (DRC6 seeds).** Allowed. 620311 and 620315 are P1 bootstrap seeds and draw no history, and DRC6 uses them only on synthetic arrays. The rule "the dry run never issues a real seed" applies to data streams and masters. G0c classifies `hwsc-dry*` records as stage-C declarations (fragment `/topo-scratch/hwsc-dry`).
- **R-0176-G6, G7, G8, G10, G11.** Adopted as written:
  - G6: choice 2 (`k4b_contract_view`).
  - G7: choice 11 (stage-C ledger and pause mirrors).
  - G8: choice 4 (REG2 job).
  - G10: choice 18 (R7 reads archived evaluation tables).
  - G11: choice 29 (`DRYHIST_*` names; dry-only `sample_test_c` mirror).
- **R-0176-G9 (stage-B scratch folders).** Fixed behaviour:
  - R5 reads every `topo-scratch/hwsb-dry*` store.
  - R6 scans every `topo-scratch/hwsb-*`, `hwsb-dry*` and `test_hwsb-*` folder completely, with no `test_*` pruning inside them (§4 `scratch_scan`).
  - Folders without array files on 2026-10-29 (`hwsb-0168`, `hwsb-0170`, `hwsb-0172` … `hwsb-0175`, `test_hwsb-0168r`) have rows with `frozen_files: {}`. They fail closed on any later addition.
  - The `test_hwsb-*` folders with array files (`-0161`, `-0162`, `-0169`, `-0171`, `-main`) get `frozen_files` from the R6 scan (TO_FREEZE). Proposed class: EXCLUSION as stage-B pytest fixtures, with `fixture_max_rows` 1,024 and `fixture_components` ["pytest"].
- **R-0176-G12 (per-model hold).** Fixed behaviour:
  - CONTRACT `cpu.per_model_central_s` = HANDOFF `training_forecast_s` / 3 = 2,002.2094, the larger measured stage-B model.
  - `cpu.per_model_hold_s` = 3 × that = 6,006.6282 (the protocol's 6,006.6).
  - The value used by `HoldRule` is unchanged.
- **Choices 1–30.** All adopted except choice 17, which R-0176-G4 replaces.
- **TO_FREEZE items** stay open until measured:
  - the R6 scan erratum, reviewed by the coordinator, decides the 33 undecided scratch rows, starting from the proposed classes;
  - the KC9 cost;
  - the run approval;
  - the execution freeze.

## 19. Implementation erratum (phase 3)

Source: coordinator rulings `agent-handoff/jobs/0176/RULINGS_PHASE2.md` (R-0176-P1…P10) and the phase-3 fixes. This erratum amends §0–§18. It makes no scientific change, and the protocol still wins.

**Accepted interpretations (R-0176-P1…P9).**

- **P1 (modules split by size).** The tree has fifteen `.py` files. The six added modules hold code split out of the nine of §0. Every API name stays reachable under its documented module:

  | Module | Holds | Re-exported by |
  |---|---|---|
  | `hwsc_registry_build` | `build`, `obligation` | `hwsc_registry` |
  | `hwsc_outcome` | `positive_below_margin`, `annotations`, `outcome`, `state_from_gates`, `licence` | `hwsc_gates` |
  | `hwsc_records` | `status_of`, `run_gates_c`, `superseded_ok`, `lineage_c`, `auth_ok`, `sched_ok`, `preflight`, `freeze_c`, `verify_freeze_c`, `s0`, `central`, `pause_check_c`, `ledger_read`, `ledger_append`, `pause_or_raise_c`, `export_c`, `implementation_files`, `utc` | `hwsc_driver` |
  | `hwsc_jobs` | `run_e2`, `e2_context`, `run_close`, `main` | `hwsc_driver` |
  | `hwsc_dry2` | DRC5–DRC9 | `hwsc_dry.run_dry` (lazy lookup) |
  | `hwsc_dry3` | DRC10–DRC14 | `hwsc_dry.run_dry` (lazy lookup) |

  `hwsc_dry` keeps DRC1–DRC4, `e4_eval_check_c`, `synthetic_root`, `stub_sources`, `build_tiny_process_c` and `run_dry`.
- **P2 (private names).** `k4b_release._superseded_ok` is no longer imported. `hwsc_records.superseded_ok(out) -> list` mirrors it line for line: every file of `superseded/<job>/` must be listed in that folder's `SHA256SUMS` with an equal sha256, and the function returns the offending paths. `hwsc_registry._new` is the own module's helper and is allowed.
- **P3 (`coverage` source key).** `hwsc_registry.build(sources=…)` accepts one more key, `coverage`, a callable `(src, seqs) -> {"ok", "missing"}`. It is a test and dry-run seam only. Its default is the frozen `k4b_registry.revalidate_coverage(src["art"], root, store=src["store_a"], seqs_a=…)`, and the real CLI never passes `sources`.
- **P4 (signatures).**
  - `auth_ok(auth, stage, freeze=None)`: for every stage except DRY, `auth["run_approval_sha256"]` must equal `freeze["run_approval_sha256"]`.
  - `run_train(out, auth, sched, master, kc_accept, cont=None, plan=None)`: `plan` defaults to `HWSC_PLAN`.
  - `run_reg2(out, auth, sched, accept)`.
- **P5.** `hwsc_config.public_summary(path)` ignores `root`; its rules match path components only.
- **P6 (DRC1).** DRC1 drives the gates directly on a dry context (no FREEZE, AUTH or release records exist in a dry store), under R-0176-G3. Its details give the reading per gate: `readings` `{gate: "EXACT" for TRAIN_<m>, "VALUE" otherwise}`, plus `records` "EXACT" (one registered record per gate and no `HIST_*` name).
- **P7.** `DRY_REPORT.json` is written by exclusive create. Each dry rerun uses a fresh `hwsc-dry-<job>` store and the R-0157-1 set-aside rule.
- **P8.** The TRAIN job of the last master in `MASTERS` order writes `stages/TRAIN/OBS_INVENTORY.json` once all three TRAIN records are COMPLETE. The coordinator runs the `obs-inventory` subcommand only if a TRAIN job is rerun, and records that in the job review.
- **P9.** The E2 job repeats the H1-C checks as gate `H1C_E2`, writing `stages/E2/H1C_E2.json`, before sampling S7.

**Fixes (phase 3).**

- **R-0176-P10 (defect).** `run_e2` now stops on a non-PASS `BINDING_AUDIT` exactly as KC, TRAIN, E1 and REG2 do. All five jobs call `hwsc_driver._audit_gate`: a non-PASS audit is recorded and then raises `C1GateFailure(status)`, before any further gate.
- **REG2 gate order.** It now follows CONTRACT `gates.REG2`: FREEZE, AUTH, SCHED, `BINDING_AUDIT` (inside `bound_stage_c()`), `ACCEPT`, the reservation check, then `REG2`.
- **`run_gates_c` and `Paused`.** A gate that raises `hwsb_driver.Paused` is recorded with status `PAUSE`, and the exception is re-raised: the job stops, and the CLI exits with code 4.
- **Train/dev ObservationSet config.** The config's `study` field is now the `scope` argument of `make_train_dev_c`, so the artifact ids reflect the scope. The sequence-ID replicate also uses `scope`. The data streams keep following `hwsb_config.SCOPE` at call time (the binding). With `scope="hwsb-v1"` and the code unbound, everything equals `hwsb_data.make_train_dev` (DRC4).

**Clarifications for the test authors.**

- **Audit hits.** Each hit of `hwsc_bind.audit` is `{"module", "where", "kind", "hit", "top"}`; `top` is the top name used against `left_unchanged`.
- **Parsed records, not paths.** `run_train`'s `kc_accept` and `run_reg2`'s `accept` take parsed dicts; the CLI takes paths and loads them. `run_kc`, `run_train`, `run_e1`, `run_reg2` and `run_e2` take parsed `auth` and `sched` dicts.
- **`pause_or_raise_c`'s `cont`** takes a path to a JSON `{"stages": [...]}`, or None.
- **`registry_risk`'s 1/100 boundary** is evaluated on `Fraction(float(p_d2a))`, so equality at exactly 1/100 holds only at float resolution: `p` must be a float whose exact rational value times the row count equals 1/100.
- **`source_dry` with an absent `hwsc-dry`** reports `present: True`, because the flag describes the source as a whole, and an empty `other`. Only the four required stores make an absence a failure.
- **`auth_ok`'s positive case** needs the run-approval sha256 recorded in FREEZE.json (`run_approval_sha256`, TO_FREEZE). Before the freeze, tests use a synthetic FREEZE dict.

## 20. R6 scratch inventory frozen (erratum, job 0176)

On 2026-10-29, `hwsc_registry.scratch_scan` was run over `X:/Downloads/topo-scratch` at hwsc-impl 602eeb8. It reads npz/npy headers and file names only; it loads no array and opens nothing on the blindness list. `test_*` components were pruned as §4 and R-0176-G9 specify (stage-B folders walked completely).

From that scan, CONTRACT `registry.scratch_inventory` now holds `frozen_files` (`{relpath: class}`) and a one-line `reason` for every top-level folder that holds history, identity, ObservationSet-root, unreadable or `.pt` files: 50 folders, classed as follows.

- **READER, 12 folders.**
  - `hws-dry`: readers `hws` and `R5`.
  - `hwsb-dry`, `hwsb-dry-0169`, `hwsb-dry-0171`: reader `R5`. This includes the planted 10-byte fixture, classed `unreadable` in `frozen_files`.
  - The C2 and C2ND dry runs `0104`, `0105`, `0109-pre`, `0139`, `0148`, `0157`, `0158`, `0160`: reader `c2scratch`. Every history file there is either a C2-format `HIST_*.npz` table or a `registry/**` digest set derived from those tables, and every identity file is an `ORACLE_*` table.
- **EXCLUSION, synthetic fixtures with `fixture_max_rows` 1,024, 2 folders.**
  - `0126`: under `bt*` segments.
  - `test_hwsb-main`: with `fixture_components` `["pytest"]`.
- **EXCLUSION with row-specific fixture components, 2 folders (a judgement for coordinator review).**
  - `0075`: `chk1`, `chk2`, `tmp`; registry digest runs and check fixtures, all ≤ 384 rows.
  - `0078`: `sim`; C0 smoke snapshots of 256 rows and their `.pt` files.
- **EXCLUSION, short histories, 1 folder.** `0122` holds HWS TINY-world smoke copies with 8 tokens per row. These cannot equal a 32-token history (D-0139-1).
- **EXCLUSION, `.pt` only, 1 folder.** `x6zc-dry`: two initial checkpoints, classed by name.
- **Not classified, 32 folders (decision still `TO_FREEZE`).** These need a coordinator ruling and are listed in CONTRACT `registry.scratch_rules.unresolved`:

  `0050`, `0052`, `0054`, `0077`, `0079`, `0081`, `0082`, `0084`, `0086`, `0088`, `0089`, `0090`, `0091`, `0093`, `0094`, `0096`, `0111`, `codex-remediation-20261017`, `coord-C2H`, `coord-C2Hp`, `coord-C2Hpp`, `coord-H`, `coord-H2`, `coord-H3`, `coord-H4`, `p-review`, `pytest-x6merge`, `test_hwsb-0161`, `test_hwsb-0162`, `test_hwsb-0169`, `test_hwsb-0171`, `verify-1121df8`.

  Each holds files outside the fixture rule:
  - most hold history files of more than 1,024 rows inside pytest basetemps: 1,100-row fixture ObservationSets, 4,096-row C0 `smoke.npy`, and the `big.npz` planted fixtures of the K4b fixture-rule tests;
  - `0111`, `codex-remediation-20261017`, `coord-C2H`, `coord-H` and `verify-1121df8` also hold fixture stores, checkpoints and ObservationSet roots under `pt/` or `pytest-affected/` components, which the segment rule does not cover;
  - `0089`, `0093` and `0094` hold cloud training arrays (`train_*.npy`, 1,048,576 rows) and `0081` arrays of up to 2,097,152 rows, which no stage-C reader reads.

Folders without such files keep `frozen_files: {}` and fail closed on any later addition. With the frozen table, `scratch_check` on the current scratch root reports exactly the 32 unresolved folders ("row not frozen") and nothing else, so K-REG1, K-REG2 and REHEARSAL stay INCONCLUSIVE/REGISTRY_INCOMPLETE until the coordinator rules on those folders. These items remain TO_FREEZE: the run approval, KC9's cost and the execution freeze.

### 20.1 Ruling R-0176-R6 applied (the 32 unclassified folders)

Source: `agent-handoff/jobs/0176/RULINGS_R6.md`, sha256 6e0b2cbf4166ef6eefdf0f6eb538a7b3083f453d058a8df42e21ed4e111b5563. The two judgement calls of §20 (c2scratch coverage; the `0075`/`0078` fixture components) are accepted.

**How each of the 32 folders was resolved, file by file (first matching rule wins).**
1. **Covered by a reader:**
   - A C2-format `HIST_*.npz` outside any `test_*` component goes to `c2scratch`.
   - An ObservationSet store whose EmissionSpec parents lie in the same store goes to `R5`. These stores are listed in CONTRACT `registry.dry_stores.os_roots` and read canonically by `hwsc_registry.source_dry`, through `_os_roots`, with the `hwsb_registry.registry_digests` rule.

   Both kinds are recorded in the row's `covered` (`{relpath: tag}`).
2. **HASH_FROZEN:** every other listed file is recorded in the row's `hash_frozen` (`{relpath: {sha256, bytes, reason_class}}`). The reason class is one of:
   - `CHECKPOINT`: `.pt` files, hashed as scratch copies.
   - `FIXTURE_STORE`: `pt/`, `pytest-affected/` and `dry/` stores; the X6S1 implementation-job fixtures `0077`, `0081`, `0082`, `0084` (synthetic fixtures only, per their `task.md`); `0089/pf/`.
   - `PYTEST_FIXTURE_LARGE`: files under a pytest segment.
   - `OTHER_PROCESS_TRAINING`: the X6S1 owner cloud snapshots `cloud_bundle/`, `cloud_in/` and `partial-extract/` in `0089`, `0090`, `0093`, `0094` (jobs 0089–0094: E0, E0b, E1, E2).
3. **Not identified:** any other file stays in `registry.scratch_rules.unresolved` and blocks the freeze.

**Code (`feat(hwsc)`).** The R6 functions `_classify`, `scratch_scan`, `scratch_check` moved to the new module `hwsc_scratch` (split by size) and are re-exported by `hwsc_registry`. `scratch_check` calls `hwsc_registry.scratch_scan` at call time. Per row, `scratch_check` now applies two checks:
- every `hash_frozen` file is re-hashed (size and sha256, with a known reason class); any difference → `other` ("HASH_FROZEN sha256 differs");
- every `covered` file's tag must be PASS in the same build.

Rows without these fields behave as before. `source_dry()` called with its default paths also reads `os_roots`.

**Residual risk.** CONTRACT `registry.scratch_rules.residual_risk`, quoted from the ruling: HASH_FROZEN files are not digested; the stage-C test rows are fresh draws from w\* under new `hwsc-v1` scopes and no stage-C model reads scratch, so the residual risk is an accidental identity between a fresh w\* history and an undigested scratch row of another process. Any addition or change in these folders fails closed (`scratch_check`).

**R5 short histories (code).** A member with a key in `HISTORY_KEYS` and fewer than 32 tokens per row is recorded in `non_c2_format` and not digested, under the D-0139-1 rule (such a row cannot equal a 32-token history). This applies, for example, to the `hws-dry` DR12 superseded copies of shape [64, 8]. Before this change those files made `source_dry` INCONCLUSIVE.

**Verification on 2026-10-29.**
- `source_dry()` on the real scratch: PASS, 56,607 digests, with the 3 planted fixtures recognised and the 3 short-history files recorded.
- `scratch_check(readers_ok={c2scratch, hws, R5})` on the current scratch root: PASS, with no `other` entry and no "row not frozen".
- 93 of 319 candidate ObservationSet stores are R5-readable `os_roots`. The ObservationSets of the other stores are HASH_FROZEN.
- `registry.scratch_rules.unresolved` is empty.

## 21. Erratum (job 0177, coordinator 08ad4eaf)
- **D-0177-1.** `hwsc_meter_bind.child_env_c(job) -> dict`: `k4b_meter_bind.child_env(job)` with its `TEMP` folder (`<TEMP_ROOT>/tmp-<job>`) created; `main` uses it. Without the folder, `tempfile.gettempdir()` in the metered child fell back to C:. Regression test `tests/hwsc/test_r_0177_meter_tempdir.py` (coordinator-written).
- **Binding audit in J-C1.** The CLI has no `audit` subcommand (TEST_PLAN §5 wording). J-C1 runs the audit with the coordinator helper `coord-scratch/08ad4eaf/hwsc_audit.py`: `hwsc_bind.audit()` inside `hwsc_bind.bound_stage_c()`, result written to `<out>/AUDIT.json`, exit 0 iff PASS. Later jobs run the audit through their own `BINDING_AUDIT` gate.

## 22. Erratum: the hwsc-dry type rule (defect D-0178-1)

**Defect.** After the metered dry runs (jobs 0177 and 0178), `scratch_check` reported 80 "not in frozen_files" entries inside `hwsc-dry-0177/` and `hwsc-dry-0178/`. Each dry run writes a new store, so the frozen R6 table cannot list these files one by one.

**Fix: a type rule** for every top-level scratch folder whose name starts with `hwsc-dry`, and only those (CONTRACT `registry.dry_stores.type_rule`). The new module `hwsc_drystore` provides:
- `is_dry_store(name)`;
- `dry_class(store, rel, rec) -> class or None`;
- `check_store(store, listed, ok_tags, out)`.

**Paths.** Each listed file lies at `<store>/<DRCn>/<utc>/<tail>`. The classes are derived from what `hwsc_dry.run_dry` writes:
- **`R5`:**
  - `artifacts/ObservationSet/<id>/{meta.json, payload.npz}` whose single EmissionSpec parent lies in the same artifacts dir; digested canonically.
  - `stages/S3|S7/DRYHIST_*.npz` with a canon32 [n, 32] member.
  - DRC9 `syn/` and `syn2/` token files with a canon32 [n, 32] member.
- **`c2scratch`:** DRC9 `syn/**/HIST_*.npz` in the C2 table format, read by the C2ND scratch reader.
- **`CHECKPOINT`:** `artifacts/Checkpoint/<id>/state.pt`, never opened.
- **`REGISTRY_FIXTURE`** (non-history):
  - `registry/K-REG1|K-REG2_digests.npz` whose npz keys are exactly `{digests (<U), seq_ids}`;
  - DRC9 `scale/run_NNNNN.npy` and `registry/runs/<version>/run_NNNNN.npy` with a uint8 [n, 32] header (digest runs).
- **`PLANTED_FIXTURE`:** the four planted byte fixtures, matched by case, file name, size and sha256: DRC9 `ACT.npz`, `stray.npz`, `BAD.npz`; DRC11 `a.npz`.

**Behaviour.**
- **Fail closed:** any other listed file in a `hwsc-dry*` store → INCONCLUSIVE/REGISTRY_INCOMPLETE.
- **Readers:** an `R5` or `c2scratch` file also needs its reader to have returned PASS in the same build.
- **`source_dry`:** routes `hwsc-dry*` files through the same rule. It digests the `R5` files, records the other classes as non-history, and puts any other listed file in `other`.

**Other code changes.**
- `hwsc_scratch` now imports `hwsc_registry` lazily, which fixes an import cycle when `hwsc_scratch` is imported first.
- The `hwsc-dry` and `hwsc-dry-<job>` rows of `scratch_inventory` name the type rule.

**Regression test (coordinator-commissioned).** `tests/hwsc/test_r_0178_dry_store_rule.py`:
- a synthetic dry store with every allowed class passes;
- an unexpected array fails closed;
- a registry npz with an extra key fails closed;
- a changed planted fixture fails closed;
- reader classes need their reader;
- the rule applies only to `hwsc-dry*` folders.

**Verification on 2026-10-29.**
- `source_dry()` on the real scratch: PASS, 80,687 digests.
- `scratch_check(readers_ok={c2scratch, hws, R5})`: PASS with 0 `other`.
- tests/hwsc: 415 passed.

## 23. Erratum: the owner's run approval (ruling R-0179-1, coordinator 08ad4eaf)
- **CONTRACT `authority.run_approval`** is now fixed: path `agent-handoff/archive/owner-decisions-20261015/OWNER_DECISIONS.addendum-36.md` (relative to the project root), sha256 `c24bdf94156970859eda1c3cafd7da94e0b7a0dce731b4d066d3e8db7a6bff5e`. Addendum 36 records the owner's explicit stage-C run approval (2026-10-29) asked for by addendum 35 Q6.
- **Order (R-0179-1).** This erratum changes CONTRACT.json and so the implementation hash; J-C1 and the dry run are repeated once at the new h_exec, then the PF record and `freeze --run-approval <that file>`. KC0 (`g0c`) then finds path, CONTRACT sha256, AUTH `run_approval_sha256` and FREEZE.json `run_approval_sha256` equal.
- **Not changed:** `cpu.re_set` stays TO_FREEZE. The E1 and E2 centrals stay at the planning values (R = 300 s); KC9's measured registry cost is reported only, and a lower 3× threshold means an earlier pause that asks the owner. No CONTRACT change after the execution freeze.

## 24. Erratum: g0c checks lineage before writing G0C.json (defect D-0181-1)
- **Defect.** The §5 `g0c` row wrote `stages/<stage>/G0C.json` in (iii) and then ran `lineage_c(out)` in (iv). `G0C.json` is recorded only by the stage's `STAGE_COMPLETE`, so on any real store `lineage_c` found it unrecorded: KC0 of job 0181 ended `FAIL_TECHNICAL/LINEAGE: unrecorded files: ['stages/KC/G0C.json']`, with KC1–KC9 NOT_RUN. The same order would have failed G0C in E1. The dry run did not reach this path on a real store.
- **Fix.** (iv) `lineage_c(out)` now runs before the `G0C.json` write of (iii), after the seed search. It checks the store as found at the start of the stage. An unrecorded file still fails closed, and then `G0C.json` is not written. Code `hwsc_known.g0c`. Regression test `tests/hwsc/test_r_0181_g0c_lineage_order.py` (coordinator-written; it fails on the old order).
- **Correction count.** This is correction 1 of at most 2 for D-0181-1 (X-2). The KC attempt and the FREEZE it ran under move to `hwsc-store/superseded/0181-a1/`. J-C1 + DRY are repeated at the new h_exec before a new execution freeze (ruling R-0181-1).

# X5 G1 training-study API addendum v4.1 — pool input identity and provenance (job 0011)

This addendum is for the builder and the independent test writer. It adds to [API v4](X5_G1_TRAINING_API_V4.md) and the inherited API v3 §2 lineage, and changes nothing else.

* API v3, API v4 and protocol v3/v4 are unchanged. No change to architecture, optimiser, seeds, streams, namespaces, sequence-ID construction, grid, normalisers, thresholds or budget.
* **Why.** The root probe (job 0010 review) showed that `run_train` accepted a hash-valid **other-arm** train pool mapped to `train:a0:<m>` under a recomputed COMPLETE manifest. Hashes prove bytes, not meaning, so every used pool must also prove *which* pool it is.
* Every failure below raises `x5g1t_checks.IntegrityFailed` (CLI exit 3). It is raised before any sampler, model, oracle, scoring or result export that would use the input. A small truthful ledger or audit entry may remain; no scientific result is exported, and nothing is re-read or re-drawn to repair a failure.

## A. Provenance mapping (frozen)

New study pools (train, dev and the fresh test) are saved with metadata `config` equal to **exactly** the following, built by `x5g1t_lineage.study_pool_config(split, arm, master, execution_protocol)`:

```python
{"role": f"x5g1t-{split}",
 "lineage_protocol": "x5g1-train-v3",    # = lineage.PROTOCOL
 "execution_protocol": cfg.protocol,     # production "x5g1-train-v4"
 "arm": arm,
 "master": master,                       # int for train/dev; "shared" for test
 "stream": "/".join(stream(split)),
 "namespace_code": CODES[split]}
```

* **`lineage_protocol`** names the frozen version of the stream, namespace, seed and sequence-ID construction (API v3 §2). It is not the run contract.
* **`execution_protocol`** names the contract the run executes under. It is the validated `cfg.protocol`: in production, `"x5g1-train-v4"` (checked by `validate_config`); in a fixture, its SYNTHETIC protocol string.
* There is no bare `protocol` key in new pools. `run.json` still records `protocol` = `cfg.protocol`.
* `pool_config` and `PROTOCOL` stay unchanged for historical records and their tests.

## B. `x5g1t_checks.validate_pool(store, pool_id, sha, cfg, split, arm, master, V) -> dict`

Returns `{pool_id: (ObservationSet, sha)}`, for re-verification before the export. It raises `IntegrityFailed` unless **all** of these hold:

1. `meta.artifact_type == "ObservationSet"` and `meta.payload_sha256 == sha`.
2. `canonical(meta.config) == canonical(study_pool_config(split, arm, master, cfg.protocol))`.
   * `canonical` is the JSON form with sorted keys, in which lists and tuples are equal.
   * Any extra, missing or wrong field fails.
3. `tuple(meta.parent_ids) == tuple(sorted({cfg.sources["T"][arm][0], cfg.sources["E"][0]}))`. Another arm's kernel, or any other parent, fails.
4. The full payload hash via `verify_full` (the store re-hashes on load). The loaded `ObservationSet` must then have:
   * `split == split`;
   * `V == V` (the emission's symbol count, `E.shape[1]`);
   * `layout_version == "1"`;
   * `tokens.shape == (cfg.sizes[split], 33)`;
   * `sequence_id` exactly equal, **in order**, to `sequence_ids(split, arm, master, cfg.sizes[split])`.

   A pool for another master, another split or another arm, or with the wrong V, layout, row count or IDs, therefore fails even when every checksum is valid.

For the test split, `master` is `lineage.TEST_MASTER` (`"shared"`).

## C. Pool-table consistency

`complete_pools(cfg)` passes only when all of these hold:

* the pools export is COMPLETE (API v4 §4);
* `pools.json["pools"]` has **exactly** the keys `{f"{s}:{a}:{m}"}` for s in (train, dev), a in ARMS and m in `cfg.masters`, each with a 64-hex `pool_sha256`;
* the export's `run.json` has `protocol == cfg.protocol` and `mode == cfg.mode`.

Anything else raises `IntegrityFailed`.

## D. Stage application (exact)

| Stage | Identity checks (§B) | Placement |
|---|---|---|
| `pools` | every new pool | after its save, before the export |
| `train --arm A --master M` | `train:A:M` and `dev:A:M` | **before** `train_one`; re-hash both after training, before the export |
| `dev-analysis` | for each COMPLETE pair and arm: `dev:A:M` and `train:A:M` | before `validate_checkpoints`, the oracle and scoring |
| `final-test` | **every** train/dev pool in the table | before the collision check, any checkpoint use and the fresh draw |
| `final-test` | each new test pool (`test`, A, `"shared"`) | after its save, before its oracle and scoring |

**Collision inputs are inputs.**
* Every read-root `ObservationSet` loaded for the ID-collision check (in pools and final-test) has its `(ObservationSet, payload_sha256)` recorded at load and is re-verified with `verify_full` **before the result export**.
* A payload mutated after the load, with metadata unchanged, gives `IntegrityFailed` and no result export.
* The study's own train and dev pools used for the final-test collision check are covered by §B and re-hashed before the export.

Fresh-test IDs are still checked against the read roots and all study train/dev pools **before** the fresh draw. STOP still means no draw, and all batch, save and export guards of API v4 stay.

## E. Required independent regressions (actual stages, tiny fixtures, valid checksums)

1. **Root wrong-arm substitution, reproduced.** Map `train:a0:<m>` to the valid `train:a020:<m>` pool with a recomputed COMPLETE manifest. `run_train` raises `IntegrityFailed` and a `train_one` spy has **zero** calls; the CLI exits 3. On the untouched fixture, the same spy **is** reached with the intended pool IDs.
2. **Other valid substitutions**, each with a recomputed manifest: another master's pool; train and dev swapped; a pool saved with the wrong parents, wrong config (role, lineage or execution protocol, stream, namespace code, extra key), wrong IDs, wrong V, wrong layout or wrong row count. Each is refused before `train_one`.
3. **Dev and final paths.** A mismatched pool means no `oracle_q32` or `regret_rows` call (spies) in dev-analysis. A prerequisite identity or integrity failure in final-test means **zero** `draw_pair` calls.
4. **Collision inputs.** Mutate a read-root `ObservationSet` payload (metadata unchanged) after the collision load, via a spy on the loader or by changing the bytes between load and export. Also the study train/dev pools in final-test. The result: `IntegrityFailed` and no result export. Use a tiny old-ID reference store; never the real main store.
5. New pools record `lineage_protocol` and `execution_protocol` exactly as in §A.
6. The existing API v4 regressions stay meaningful and unweakened: no draw on STOP, request/control HOLD release, the per-512-row scoring and oracle guards, the checkpoint list/tuple case, and present-null usage files.

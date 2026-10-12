# `contracts`

## Purpose

The shared vocabulary of the project: artifact schemas, the content-addressed store and its access policy, ids and seeds, the sequence layout, errors, and tiny test fixtures. It contains no science and imports nothing else from the project (numpy and the standard library only; never torch).

## Logic

### Artifact identity

```
artifact_id = sha256(canonical_json([artifact_type, config, sorted(parent_ids), schema_version]))[:16]
```

`canonical_json` is the identity-defining serialisation. Dict keys become `str(k)` and are sorted. There is no whitespace. Tuples and lists serialise the same way. Numpy scalars become Python scalars, and numpy arrays become lists. Floats use `repr`, the shortest form that round-trips. Dataclasses become objects keyed by field name, and enums become their values. NaN and ±inf raise `INVALID_CONFIG`.

The id depends only on the *generating* config and lineage, never on the payload or on `created_utc`. A job run on another machine therefore produces the same id (docs/EXECUTION.md §1). Changing any of the config, the parents, or the schema version changes the id.

### Payload checksum

`payload_sha256` is computed over the content, not over the files. It hashes each array or blob in name order, together with its name, dtype, shape, and raw C-order bytes, followed by `canonical_json(extra)`. Zip timestamps inside `.npz` are therefore irrelevant: equal content always gives an equal checksum, and any change to a stored byte that `np.load` still reads is detected. A container that `np.load` can no longer read is also reported as `CHECKSUM_MISMATCH`.

### Store layout and write protocol

```
<ArtifactType>/<artifact_id>/meta.json     # envelope, DATA_SCHEMAS §1 (+ "consumer": who wrote it)
                             payload.npz   # np.ndarray fields, allow_pickle=False
                             extra.json    # every non-array field, canonical JSON
                             state.pt      # Checkpoint only: opaque torch blob
```

`save` runs these steps in order:

1. `validate()`;
2. check that every parent is stored (`MISSING_PARENT`);
3. derive the id;
4. if the id already exists, verify the stored payload against its checksum and compare it with the new checksum (`CHECKSUM_MISMATCH` on any difference), then return without writing;
5. otherwise write `meta(incomplete)`, then the payload files, then `meta(complete)`.

An interrupted write therefore leaves `status = incomplete`, which `load` refuses with `ARTIFACT_MISSING` (check `incomplete`). The next `save` of the same artifact overwrites it.

`load` checks, in order:

1. the access policy (`LEAKAGE`);
2. existence (`ARTIFACT_MISSING`);
3. completeness;
4. the major schema version (`SCHEMA_VERSION_MISMATCH`; a minor bump still loads);
5. the checksum (`CHECKSUM_MISMATCH`);
6. `validate()`.

Serialisation is generic. Each typed artifact is a frozen dataclass. Its `np.ndarray` fields go to the `.npz`, its `bytes` fields become blobs, and `WorldSpec.cells` is stored as arrays named `cells__<k>`. Every other field goes to `extra.json` and is coerced back by its type hint, so tuples survive the round trip.

### Access policy (DATA_SCHEMAS §7)

| Artifact | Allowed consumers |
|---|---|
| EvalSidecar | analysis, prediction, experiment |
| WorldSpec, TransitionSpec, EmissionSpec | process, dataset, oracle, analysis, experiment |
| ObservationSet | every module except world |
| Checkpoint | learner, activations, experiment |
| everything else | all |

The consumer is the module name passed to `load(..., consumer=...)`. `save` records the writer, but it does not check read rights, because a producer such as `world` writes types it is not allowed to read back.

### Bundles

`export_bundle(ids, dest, with_parents=True)` writes a deterministic `.tar.gz`: sorted entries, zero mtimes, and no filename in the gzip header, so equal content gives identical bytes. It holds `artifacts/<type>/<id>/...` for the ids and, by default, all their ancestors, plus `bundle_index.json` in dependency order.

`import_bundle` first verifies every artifact:

- the type is known and the status is complete;
- the major schema version matches;
- the id recomputes from its meta (`CHECKSUM_MISMATCH`);
- the payload checksum matches (`CHECKSUM_MISMATCH`);
- every parent is present in the bundle or the store (`MISSING_PARENT`);
- `validate()` passes.

Only after all checks pass does it write, skipping identical artifacts that already exist. Unsafe tar members (absolute paths, `..`) are refused.

### Seeds

`SeedTree(master).seed(name, *scope) = int(sha256(canonical_json([master, name, *scope]))[:8 bytes], big-endian) & (2^63 − 1)`. `generator` wraps the seed in `PCG64`. The result is identical on every OS and independent of `PYTHONHASHSEED`. Issued seeds are recorded per instance in `SeedTree.issued`, which stages store as the `seed_map`.

### Sequence layout

`SequenceLayout` is the only place that encodes alignment (the table in DATA_SCHEMAS §3 is reproduced in its docstring). `model_inputs(tokens, V)` takes `V` explicitly (D-008) and returns `[BOS=V, w_1..w_32]`. `targets(tokens)` returns `[w_1..w_33]`, and `history(row, p)` returns `w_1..w_p`.

### Validation scope

`validate()` checks everything that can be checked from the artifact alone. Three invariants need another artifact or a science convention, so the producing module enforces them at build time:

- ∂∂ = 0 needs the cubical sign convention (enforced by `world`);
- T's support on edges needs the world (enforced by `process`);
- the row multiset of a permuted emission needs its source (enforced by `process`).

## Data

Defines all artifact types in `docs/DATA_SCHEMAS.md`. It reads and writes nothing by itself; `ArtifactStore` is the single I/O point for every module.

## Public API

See `__init__.__all__`. The main entries are the errors (`ErrorCode`, `Status`, `StageFailure`), the 16 artifact classes plus the row types `MetricRow` and `GateCheck`, `ARTIFACT_CLASSES`, `canonical_json`, `make_artifact_id`, `tokens_hash`, `make_history_id`, `payload_checksum`, the backends (`ArtifactBackend`, `LocalFSBackend`, `MemoryBackend`, `MirrorBackend`), `AccessPolicy`, `DEFAULT_ACCESS_POLICY`, `MODULES`, `ArtifactStore`, `SeedTree`, and `SequenceLayout`.

The fixtures in `contracts.testing` are `tiny_world_spec`, `tiny_hmm`, `tiny_observations`, and `memory_store`.

## How to test

```powershell
.\.venv\Scripts\python.exe -m pytest tests/contracts -q     # or: .\tasks.ps1 test -Module contracts
```

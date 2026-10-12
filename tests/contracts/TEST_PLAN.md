# TEST_PLAN: contracts

Marker: `pytest.mark.contracts`. Budget: under 10 s.

| ID | Test | Kind |
|---|---|---|
| C01 | `make_artifact_id` is identical for configs with permuted keys and nested dicts | property |
| C02 | `make_artifact_id` changes when any of config, parents, or schema version changes | property |
| C03 | `canonical_json` is stable for floats (repr), numpy scalars, and tuples vs lists, as documented | known answer |
| C04 | Every artifact class survives the round trip `save` → `load` with arrays bit-identical | contract |
| C05 | Saving the same artifact twice is a no-op; tampering with the payload makes `load` or `save` raise `CHECKSUM_MISMATCH` | error path |
| C06 | An `incomplete` artifact is refused by `load` | error path |
| C07 | A major version bump in meta raises `SCHEMA_VERSION_MISMATCH`; a minor bump loads | error path |
| C08 | `DEFAULT_ACCESS_POLICY`: `learner` loading `EvalSidecar` raises `LEAKAGE`; `analysis` succeeds | error path |
| C09 | `SeedTree.seed` gives fixed hard-coded values for (1729, "init") and (1729, "train", 3) | known answer |
| C10 | `SeedTree.generator` streams with different names are different, and the same name repeats | property |
| C11 | `SequenceLayout`: on a hand-written row with V = 5, check the inputs `[5, w1..w32]`, the targets `[w1..w33]`, `history(p)`, and the analysis position | known answer |
| C12 | `export_bundle` → `import_bundle` into a fresh store gives the same ids and checksums; a missing parent raises `MISSING_PARENT` | contract |
| C13 | Each `validate()` rejects a hand-corrupted instance: a row sum ≠ 1 in TransitionSpec, `p_w = 0` in EmissionSpec, overlapping panels in HistoryIndex | error path |
| C14 | The `contracts.testing` fixtures are valid (`validate()` passes) and deterministic | contract |

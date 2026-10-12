# Conductor review checklist (per module)

Accept a module only if every box is checked. Otherwise return at most 5 concrete defects to the builder.

**Contract**
- [ ] The public API matches the SPEC exactly. `__init__.py` exports nothing else.
- [ ] Every invariant in the SPEC is enforced and raises the listed `ErrorCode`.
- [ ] No research decision was changed silently (compare with `docs/RESEARCH_SUMMARY.md`).

**Correctness**
- [ ] Math kernels are pure, and the formulas match the README Logic section and RESEARCH_SUMMARY notation.
- [ ] All randomness comes from injected generators. There is no global RNG and no wall-clock dependence.
- [ ] Shapes and dtypes match DATA_SCHEMAS.

**Isolation and leakage**
- [ ] `tools/check_imports.py` is clean: package-root imports only, plus the leakage rules.
- [ ] The module reads and writes artifacts only through `ArtifactStore`, with its own consumer name.

**Tests**
- [ ] `python -m pytest tests/<module> -q` is green in under 60 s.
- [ ] For critical modules, the tests were written by a different agent and cover every TEST_PLAN id.
- [ ] Error paths are tested.

**Docs and hygiene**
- [ ] The README has Purpose / Logic / Data / Public API / How to test, and Logic explains *why* the method is correct.
- [ ] Docstrings state the math, shapes, invariants, and raises.
- [ ] No file is over 400 lines. No dead code, debug prints, notes, or logs in the repository.

**After acceptance**
- one commit `<module>: …`;
- update the module row in `state/PROGRESS.md`;
- if a contract or schema changed, add a line to `state/DECISIONS.md` and run `tools/affected_tests.py`.

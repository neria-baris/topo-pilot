# Builder brief: `<module>` (wave W<k>)

> The conductor fills this template and sends it as the **entire** instruction. The brief must work for an agent that has never seen this project.

**Role:** you implement one module of a Python research package. You do not make research decisions. If the SPEC is ambiguous, choose the simplest reading, implement it, and flag it in your report.

**Read, in this order:**
1. `docs/CONVENTIONS.md` (all of it)
2. `src/topo_pilot/<module>/SPEC.md` (all of it; this is your contract)
3. `docs/DATA_SCHEMAS.md`: only the sections listed in the SPEC
4. `src/topo_pilot/contracts/__init__.py` and `contracts/testing.py` (the public types and fixtures you may use)
5. `tests/<module>/TEST_PLAN.md`

**You may write only to:**
- `src/topo_pilot/<module>/` (all `.py` files + `README.md`)
- `tests/<module>/`, **only if** this brief says "you also write the tests". Otherwise the tests are written by someone else; do not edit them.

**You may import only:** the standard library, the dependencies in `requirements.lock`, `topo_pilot.contracts`, and these modules' public APIs: `<list or "none">`.

**Must deliver:**
- [ ] the public API exactly as in SPEC §"Public API" (names, signatures, return types)
- [ ] every invariant and error code listed in the SPEC
- [ ] `README.md` with the sections Purpose / Logic / Data / Public API / How to test
- [ ] docstrings per CONVENTIONS §4
- [ ] `python -m pytest tests/<module> -q` passes (if tests exist), in under 60 s on CPU
- [ ] `python tools/check_imports.py` and `python tools/check_file_sizes.py` are clean

**Do not:**
- change the SPEC, contracts, configs, or other modules;
- add dependencies;
- write logs, notes, or transcripts into the repository;
- run tests outside `tests/<module>`.

**Finish** with a report in the exact format of `agents/REPORT_FORMAT.md`.

Extra context from the conductor (optional, at most 10 lines): `<…>`

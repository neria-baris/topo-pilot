# Test-writer brief: `<module>` (independent tests)

**Role:** you write the tests for a module that **someone else** is implementing at the same time. Work only from the contract, never from the implementation. Your tests are the independent check that the implementation means what the SPEC means.

**Read:**
1. `docs/CONVENTIONS.md` §6
2. `src/topo_pilot/<module>/SPEC.md`
3. `tests/<module>/TEST_PLAN.md`
4. `src/topo_pilot/contracts/testing.py` (fixtures)

**You may write only to:** `tests/<module>/`.

**Rules:**
- Implement every item in TEST_PLAN.md, and keep the item ids in the test names (e.g. `test_T03_permutation_invariance`).
- Known-answer tests use values you compute **by hand or by brute force inside the test**. Never take expected values from the implementation.
- Mark every file with `pytestmark = pytest.mark.<module>`; use `slow` only if a test is truly slow.
- Import only `topo_pilot.<module>` (its public API), `topo_pilot.contracts`, `pytest`, `numpy`, and `scipy`.
- If the implementation does not exist yet, your tests must fail at import or with `NotImplementedError`. That is expected.

**Finish** with a report in the format of `agents/REPORT_FORMAT.md`, listing every TEST_PLAN id you covered.

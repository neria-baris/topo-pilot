# D1-FROZEN-v1: coordinator addendum 2. Module binding amended to two files (S6 escalation, job 0019)

**Date:** 2026-10-15, ~04:45Z. **Coordinator:** c351b245. This changes an implementation binding only. **No scientific choice, gate, value, tolerance, stop rule or verdict semantics changes.**

## Context
- Job 0019 stopped under S6, as designed. The implementation needs about 600 lines, while §5.5/§6.2 bind a single module of at most 400 lines (the repository file-size limit, a mandatory preflight check).
- Report: jobs/0019/report.md (sha 3925EAC7…73C2).

## Ruling (option (a) of the 0019 report)
1. **§5.5/§6.2 bind two module files.** Each must be at most 400 lines and pass `tools/check_file_sizes.py`:
   - `tools/d1_seam/d1_seam.py`: constants, the exact model and its variants, the local unregistered Möbius builder, float_model, the exact filter and futures, the enumerator, gates G0, G0S, G0O, G1, G2 (including G2.11) and G3;
   - `tools/d1_seam/d1_seam_checks.py`: G4, G5, G6 and `run` (S0 re-check, preflight handling, stop rules, report.json and model.npz).
2. **`d1_seam.py` re-exports** the public names listed in tools/d1_seam/API.md, so the committed independent tests (`tests/d1_seam/test_d1_seam.py`, 70fc3a8) and the contract (6803a66) remain valid unchanged.
3. **No circular import:** `d1_seam_checks.py` imports from `d1_seam.py`, and the re-export is done lazily or at the end of the module.
4. **S0** checks the protocol hash 68EBD82F…0B21, addendum 1 (1EE0291D…2669) and this addendum (its sha256 is recorded in the 0020 task.json).
5. **The test author's literal readings** (0019 report §4) are confirmed as the intended readings:
   - the G0–G1 `values` keys are implementation-defined and documented in API.md;
   - the report shape is report["verdict"] and report["gates"][name]["status"], and report.json is written even on INVALID;
   - L2 is row (2,y) ← row (1,y);
   - the N3 ratio is P_C/P_M;
   - the Decimal-trap arm changes only T.

   Where API.md is silent, the implementer documents its choice in an API.md delta, committed **before** the module code.

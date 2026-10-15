# D1-FROZEN-v1: coordinator addendum (binding interpretation, not a protocol change)

**Date:** 2026-10-15, ~04:20Z. **Coordinator:** c351b245.

- **Protocol SHA256 (the freeze record value required by §5.5):** 68EBD82F9FD8E3C82114ADEF713F3AA9F7283BEBFF7AE38C5FFB266E62E10B21 (D1-FROZEN-v1.md).
- **Base-commit binding (§5.5, S0).** Base commit 4f219d6 is bound because it is the code state of the reused kernels. Main has since moved, by fast-forward only, to ab2be87. `git diff 4f219d6 ab2be87 -- src tools/x4_oracle_profile tests/oracle_profile` is empty, which the coordinator verified on 2026-10-15. The D-1 implementation branch therefore starts at ab2be87, which keeps main's history linear. **S0 is satisfied by:**
  - (i) the request hash;
  - (ii) the protocol hash above;
  - (iii) an empty diff between 4f219d6 and the execution HEAD over `src/`, `tools/x4_oracle_profile/` and `tests/oracle_profile/`.

  A non-empty diff on those paths fails S0. No scientific parameter changes.

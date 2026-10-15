NOT_CONFIRMED

1. **§3.6, proof step 2 — restrict the row-sum assertion.** “For each first symbol” is false for σ3, whose A/B entries sum to zero. Replace that paragraph with:

   > For each first symbol in {σ2, σ0}, the A and B entries sum to a² in both worlds, so the corresponding B differences are negatives of the A differences. Every entry whose second symbol belongs to {σ0, σ2, σ3} is world-independent, because the x-chain is world-free and band emissions depend only on x.

2. **§5.1, §5.3 and R8 — record coordinator ruling 8 explicitly.** The hashed file still leaves mandatory-check ordering unspecified and broadly assigns failed required criteria to FAIL. Insert in §5.1 and §5.3:

   > Run all mandatory checks of §6.1–§6.2 before G0. Any failure or inability to complete those checks gives overall INVALID; all oracle gates are recorded as NOT_RUN. This preflight rule takes precedence over S3–S5 for checks executed during preflight. After successful preflight, run G0 through G6 with the stated oracle-gate verdict and stop rules.

   In R8, replace “G0 runs first” with:

   > G0 is the first oracle gate after successful mandatory preflight.

3. **§7.3 item 2 — apply coordinator ruling 9 to the text.** The hashed file still contains undefined `𝓗_I⁺`. Replace:

   > a coverage plan for rare 𝓗_I⁺ histories

   with:

   > a coverage plan for decision-phase histories

   Remove the corresponding “Residual, not changed” flag from the protocol’s closing notes.

4. **§8.2, C13 — remove the remaining gating contradiction.** Replace its “Now” cell with:

   > h_max is not a Theorem E witness. It is a gated enumeration probe for Theorem F: G2.8 checks its stated values and G2.11 requires the max-branch count to be positive. Its [W] values were confirmed in review.

All other required changes are correctly applied. The supplied v2 SHA256 matches. Your coordinator rulings are accepted; no redesign is requested.
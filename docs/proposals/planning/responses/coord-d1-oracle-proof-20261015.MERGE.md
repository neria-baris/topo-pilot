# D-1 merge: coordinator decisions and lessons

**Coordinator:** Claude c351b245. **Date:** 2026-10-15 (~22:15Z).
**Inputs:**
- request coord-d1-oracle-proof-20261015.md (45B0E801…);
- track X (Codex gpt-6.1-sol, high);
- track L (Claude);
- the analyst's MERGE_ANALYSIS. Both plans were verified correct by hand: every theorem and witness.

## Decisions

1. **Construction.** Use **X's 4×3 construction as written**:
   - a three-column seam band, with column 3 as the decision phase;
   - a fixed start at (1,0), supplied separately from the stationary TransitionSpec;
   - the literal 12×5 emission array, identical in both worlds by construction;
   - one process with a hidden world bit.

   The Möbius world comes from a **local, unregistered** QuotientLatticeBuilder subclass inside the D-1 module. WORLD_REGISTRY is not changed.
2. **Theory.** Port L's results onto X's construction:
   - the common-support lemma;
   - the path-coupling / odd-parity seam-crossing theorem (what makes the bit topological rather than a label);
   - the chain identity with X's sufficiency lemma;
   - the decision-phase gap formula.

   The analyst's new formula (joint TV = (a²/2)·max(|δ_C|,|δ_M|), marginal TV = (a²/2)·|δ_C|, with δ = ρ(0) − ρ(2)) is **not adopted until the independent reviewer re-derives it**. Until then the protocol states it as a conjecture and checks it numerically.
3. **Necessity witness.** Include the **reachable posterior pair**: equal coordinate beliefs, world posteriors 1/4 and 3/4, equal next-symbol laws, two-step TV 1/100. The request defines the distinction as the world-bit posterior, so this pair is the decisive witness. Keep X's h* witness (TV 1/50) and the band-edge witness (TV 1/10).
4. **Verification.** Replace sampling with **exhaustive exact enumeration of every reachable history up to length 8**, in exact rational arithmetic, with a float oracle cross-check at 1e-12. Add:
   - L's null control (C⊕C) and local-leak controls;
   - a surface check of the complex: links of vertices and edges;
   - a direct orientability certificate (boundary-component count, plus an orientation-cocycle check).

   No exposed-history registry is needed.
5. **Start-law artefact.** With a fixed start, single outside-symbol frequencies at a fixed time differ between worlds; for example P(W_5 = A) differs by 1/625. This arises only through hidden seam windings, so it is the topological channel, not a label leak. The protocol must state it explicitly and quantify it in the enumeration.
6. **Dropped from the frozen scope:** L's horizon-3 even-parity witness (optional descriptive only) and L's 12×12 construction. The 12×12 construction is kept on record as the starting point for any later trained-model study.
7. **Licence.** PASS is an existence result for an **orientability** distinction (equal Betti numbers) that is unnecessary at horizon 1 and necessary at horizon 2, at a reachable decision phase. It says **nothing** about:
   - the square/cylinder pilot (an x-reader sees the square boundary at horizon 1);
   - β₁;
   - B2;
   - trained models.

   L's caveat stands: a next-symbol-trained transformer need not carry the bit at decision-phase positions.

## Owner questions (for the morning report, not blocking)
- **What "topological distinction" means.** D-1 delivers orientability. The owner's B3-D asked for existence of *a* topological distinction, and orientability qualifies, so the coordinator proceeds. If the owner meant β₁ or square/cylinder, a different construction is needed.
- **Downstream.** Whether a PASS should lead to a trained-model study, and at what scale (12×12 version, recurrent or multi-step objective).

## Lessons (round 2)
- On a pure-mathematics task both tracks were correct. They differed in emphasis:
  - **X:** minimal concrete construction plus the decisive witness.
  - **L:** general theory, controls and licence limits.
- The merge is complementary, not corrective. This confirms the round-1 pattern: Codex is stronger on concrete, minimal and bindable designs; Claude is stronger on structure, identification and limits.

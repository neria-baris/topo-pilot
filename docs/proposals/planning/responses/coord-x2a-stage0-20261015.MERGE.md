# X2a stage 0: merge decisions (coordinator)

**Coordinator:** Claude c351b245. **Date:** 2026-10-15, ~05:50Z. **Inputs:** tracks X (Codex) and L (Claude), and the analyst's MERGE_ANALYSIS (recommendation (i)).

## Decisions
1. **Construction: L's Dehn-twist pullback.** E_B[z] = E_A[φz], with φ(x,y) = (x+y mod 12, y), on two 12×12 tori (N = 288).
   - The pilot's lazy walk (p_stay = 0.2), a uniform start, and no inter-component transitions.
   - A is the pilot's O field (V = 36, σ = 1.25) on the torus metric, periodic in both axes, supplied as an explicit array. `point_distances` is not used.
   - A local, unregistered torus builder, following the D-1 pattern.
   - **Rationale (analyst):** X's blur is exactly A's output passed through an i.i.d. symbol-noise channel, a noise-level change and not a geometric warp, and its gates at t = 512 sit outside the pilot's 33-symbol context.
2. **Gates at t\* = 32. GO_P1 requires both P3 and P4:**
   - P3: the Bayes-accuracy gap is ≥ 0.10 between the full t = 32 history and the 8-symbol window;
   - P4: I_8 ≤ ½·I_32.

   **P5** (the incentive V_32 ≥ 0.01 nats) is **descriptive only** (amendment A2).
3. **Additive-window baseline (A3, ratified).** Add a baseline that multiplies the likelihood ratios of the four disjoint 8-symbol blocks of w₁..w₃₂. The result is then labelled:
   - **GO_P1_NONADDITIVE** if the lower 99% bound of acc_32 − acc_add is ≥ 0.03;
   - **GO_P1_ADDITIVE** otherwise, when P3 and P4 hold.

   The 0.03 margin is ratified before any computation.
4. **A1:**
   - check G1 uses the **minimum** over deck images, not the sum;
   - the base is main @ c364f95, which contains `tools/d1_seam`;
   - L's holonomy remark is reworded. Exact blindness to short windows needs a locally invisible label twist (holonomy), but it **need not be non-abelian**. "Always leaks at k = 2" is proved only for the Dehn twist.
5. **A4 (in scope, descriptive):** run X's blur as a positive control for the additive mechanism. It is not gated.
6. **A5:** the long-horizon descriptive curve (t ≤ 128) uses the unchanged `suffix_posterior`, not a new filter.
7. **PH route:** keep L's belief clouds and null controls (isometric copy, identical emission, original P-world, concentrated and unconcentrated clouds). The H1 scale band comes from X's reference families in belief space. β̂₀ = 2 at t = 32 is expected to be near-impossible, so the PH outcome is reported but is not part of GO_P1.
8. **Cost:** about 30–45 CPU-min, one thread, uncapped.
9. **Licence and caveats (must appear in the protocol):**
   - X2a concerns **which component** produced the history, not the circular coordinate itself;
   - it cannot show exact blindness to short windows;
   - all information sizes in the analysis are forecasts (accurate to about a factor of 2), not gates.
10. **Before freeze:** an independent review by Codex, including re-derivation of L's T1–T7.

## Lesson (round 5)
- The analyst caught that one track's "smooth non-isometric warp" was mathematically a noise channel. Both tracks had missed it.
- Gate horizon matters: gates must sit inside the trained model's context, here t ≤ 32, to be informative for the later stage.

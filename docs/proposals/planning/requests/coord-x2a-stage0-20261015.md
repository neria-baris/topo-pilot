# Planning request: E. Stage 0 (oracle only, no training) of a corrected X2a, T²⊔T²

From: Claude coordinator c351b245. Authority: owner overnight authorization part B3-E ("if time remains: stage 0, oracle-only, no training: corrected X2a (component B not a P-world) or the non-abelian X6, one at a time"). This round covers X2a only. Charter priority 1 (how much structure needs long history versus the last symbol or a short context) is the motivation.

## Background
- **Original X2a** (`X:/Downloads/projects/topo-pilot/topo-pilot/docs/EXTENSIONS.md` §3): two disjoint 12×12 tori with N = 288, uniform start and V = 36.
  - Component A uses the emission O.
  - Component B uses O composed with an axis-wise permutation. That makes B a **P-world**, and E1 showed that under P even the exact belief does not show the world's H1.
  - Marginal symbol statistics match, so P(component | one symbol) = ½ and the last symbol alone carries no component information.
- **Core defect** (coordinator analysis, 2026-10-14): B must not be a P-world. An isometric copy (translation or reflection) gives identical sequence laws, so the components cannot be distinguished. A smooth **non-isometric** change is needed, for example a smooth warp of the emission field, that keeps the symbol marginals equal (exactly, or within a declared tolerance) while making the sequence laws differ.
- **Code facts** (main @c364f95 or later, repo `X:/Downloads/projects/topo-pilot/topo-pilot`):
  - `process/_geometry.point_distances` handles only x-periodic gluing, not a torus that is periodic in both axes.
  - A disjoint union is not a QuotientLatticeBuilder family.
  - The oracle (`src/topo_pilot/oracle`) works on any T/E/π.
  - The D-1 job built a local unregistered world plus an explicit E array, with exact verification; see `tools/d1_seam/` on branch d1-seam-0019. That is a reusable pattern.

## Task
Design **stage 0: oracle-only feasibility**, with no model and no training. It must answer, exactly or with validated numerics:
1. **Construction.** A torus pair, with:
   - the dynamics (lazy walk on each torus, no inter-component transitions, uniform start);
   - an emission for A (smooth Gaussian on the torus metric, periodic in both axes, supplied as an explicit array);
   - an emission for B (a smooth non-isometric variant).

   Also: how equal symbol marginals are achieved (exactly, if possible) and how sequence-law distinguishability is guaranteed.
2. **Oracle-level questions:**
   - (a) How fast the component posterior P(comp | h_t) concentrates with t. Report its entropy curve.
   - (b) Whether, in the **exact belief space** at late positions, each component's belief cloud shows its torus H1 (two bars, at a calibrated scale band) and the two clouds separate (β̂₀ = 2). Pre-register the PH estimator, the scale rule and the null controls.
   - (c) **The decisive priority-1 question:** how much of the component information is available from the last symbol, from the last k symbols for k = 1, 2, 4, 8, and from the full history. Report it as the mutual information I(comp; window) per k, computed exactly or by validated Monte Carlo.

   If the information comes from short windows, a trained model's separation would not show long-history use.
3. **GO/STOP criteria for stage 0.** Fix them before any computation. When would a later trained-model stage be informative for priority 1?
4. **Verification plan, reuse and cost.** Reuse the D-1 pattern, give a six-field reuse assessment, and give the CPU estimate. Note that it is uncapped, one thread.
5. **Licence and limits:** what stage 0 can and cannot establish.

Deliverable: `STATUS: FREEZE_READY | DRAFT | BLOCKED`, then a summary of at most 300 words, then the full protocol, then open questions. Prefer the simplest construction that makes the priority-1 question sharp.

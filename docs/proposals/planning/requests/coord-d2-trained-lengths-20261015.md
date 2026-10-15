# Planning request: D-2. Trained-model study of the D-1 orientability distinction across varying lengths

From: Claude coordinator c351b245.
**Authority:** owner decision C (archive/owner-decisions-20261015/OWNER_DECISIONS.md): "Orientability is definitely an important measure, and I agree; in my view it is worth running experiments with varying lengths." (The owner's original wording is Hebrew; the archived record is binding.) Charter priority 3: distinctions unnecessary for the next symbol but necessary for longer horizons.

## Established (D-1, PASS; jobs/0020, D1-FROZEN-v1)
- In the 4×3 cylinder/Möbius seam-band construction with a hidden world bit, the bit is **provably unnecessary at horizon 1** on the decision phase and **necessary at horizon 2**.
- The decisive witness is a reachable pair with identical coordinate beliefs and world posteriors 1/4 vs 3/4. It has identical next-symbol laws and a two-step TV of 1/100.
- The 12×12 variant (track L, round 2) is on record as the starting point for trained studies.
- **Caveat (from D-1):** a next-symbol-trained transformer need not carry the bit at decision-phase positions.

## Task
Design a pre-registered study, D-2, on **trained** models. It must cover:
1. **The world.** 4×3, as in D-1 (exact oracle, cheap), or the 12×12 variant (closer to the pilot), or both. Justify the choice. Supply the exact process, reusing the d1_seam construction.
2. **The length axes ("varying lengths").** Define them precisely:
   - (i) **context/history length** L, the number of observed symbols before the decision phase;
   - (ii) the **training objective horizon** H: next-symbol only (H=1), plus multi-step targets (H=2, 3);
   - (iii) optionally the **evaluation horizon**.

   Give the grid, for example L ∈ {8, 16, 32, 64} × H ∈ {1, 2}. Give the number of models and seeds, and the CPU forecast. The pilot's tiny transformer is about 0.8M parameters; CPU is uncapped, one job at a time.
3. **The primary question** and its hypotheses. Does the representation at decision-phase positions carry the world posterior π(h), as a function of L and H? Prediction from D-1's theory: under H=1, the bit is unnecessary, so it may be absent. Under H≥2 it is necessary, so it should appear. Its learnability should grow with L, because the information about π accumulates through seam crossings.
4. **Measurement.** Exact oracle targets: π(h), the two-step law, and Q1.
   - Probes for π from activations: linear and a fixed nonlinear family, with the capacity fixed in advance.
   - A **behavioural** test: the model's two-step predictions against the oracle. Is the TV gap reproduced on the posterior-isolation pairs and similar pairs?
   - The difference between horizon-1 and horizon-2 losses.
   - Controls:
     - the C⊕C null, where π ≡ ½ and must not be decodable;
     - a label-shuffle;
     - an untrained or initialisation baseline;
     - last-symbol and short-window baselines.
5. **Decision rules** per cell and across cells: thresholds, precision method and seeds. Also what each outcome licenses. For example, "carries π only when H≥2" supports the horizon-necessity account of learned representations. It is not mechanistic and not causal.
6. **Reuse:** the learner/trainer (multi-step targets need a minimal extension; specify it), activations, the D-1 oracle code, and the meter. Give the six-field reuse assessment and the minimal new code.
7. **Staging:** an oracle-only feasibility step (decodability ceilings, posterior distribution, coverage of decision-phase positions), then training and analysis.

   Stop rules. Gates **inside** the trained context (the X2a lesson: gates must sit within the model's context).
8. **Risks:**
   - the rarity of informative decision-phase positions (the 1/4 vs 3/4 pairs are rare);
   - class imbalance;
   - whether the 4×3 model is too trivial;
   - multi-step targets leaking information.

Deliverable: `STATUS: FREEZE_READY | DRAFT | BLOCKED`, then a summary of at most 300 words, then the full protocol, then open questions. Prefer one clean, decisive design over a sprawling grid.

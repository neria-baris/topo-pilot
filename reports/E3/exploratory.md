# E3: discussion and exploratory notes (NOT pre-registered)

Written by the conductor on 2026-10-13, after `summary.md` and `condition_P.md` were generated and read for the first time. Nothing here changes a verdict, threshold, or rule. Each item reads numbers already in those files, or in the stored S6 records, or names a follow-up. A follow-up needs its own preregistration before it counts as evidence.

## 0. Approved at H4 (D-046)

Finding sentence, approved by the owner with the revised H4 clause:

> **Under the axis-permuted emission P, the trained models show no reliable cylinder–square H₁ contrast (F1 rule rejected under P: median D 0.021–0.034 below u_r 0.066–0.089, all learning gates passed). The preregistration declared this outcome uninformative, because under P the exact belief itself does not separate the worlds. Their activation geometry still tracks the 32-symbol belief well beyond initialisation and the mixing baselines (H3′ supported: ρ_s rises from 0.09 to 0.70, beating R2/R3 in 48/48 run-panels). Under O, the raw persistent-H₁ score rises at step 50 in both cylinder and square runs, before regret crosses the G_C threshold at step 100. Thus, the preregistered H4 timing rule is rejected. However, the cylinder–square contrast grows mainly between steps 100 and 200, after history use begins; this latter observation is exploratory and does not alter the H4 verdict.**

Interpretations the owner asked to keep (they restate §2–§5 and §8 below; nothing in them changes a rule, threshold, metric or verdict):

1. Under P, rejection of the F1 rule is uninformative about whether the model learned the world's topology, because the exact belief geometry itself does not separate the worlds reliably.
2. H3′ support shows alignment with the 32-symbol Bayesian belief geometry despite the absence of a reliable H₁ contrast. It does not establish that topological structure is causally necessary for prediction.
3. The strong last-symbol baseline (R1) under O remains an important limitation. The collapse of R1 under P does not establish whether the relevant structure comes from history integration or from learned symbol-level transition statistics.
4. The early rise of H₁ under O occurs in both worlds. The absolute H₁ score and the cylinder–square contrast are different quantities: the preregistered H4 rejection concerns the former and stands; the later timing of the contrast is exploratory.
5. The V3/V4 findings are representational, not causal. No intervention has established that preserving the detected topology improves prediction.

## 1. What was decided (recap, kept separate)

| item | status | result |
|---|---|---|
| H3 (F1 rule under P) | primary, one-sided (PREREGISTRATION §3) | REJECTED by the rule, with all learning gates passed; uninformative in this direction, by the reading fixed before training |
| H4 (D-034, cylinder runs under O) | primary | REJECTED: in all 3 cylinder runs, t_rise = 50 < t_history = 100 |
| H3′ (D-037) | approved decision rule | SUPPORTED under P for A = V0 and A = V1 (8/8 panels in all 6 runs) |
| X4 under P | secondary | F1 rule rejected under every view V0–V5; X4-a equal; X4-c "neither"; X4-d supported; X4-b rejected (descriptive under P); positive control passed |
| E2 finding (F1 under O) | unchanged | not revisited |

## 2. Does P change the reading of the R1 baseline seen under O?

Under O, the trained embedding of the last symbol (R1) reached 0.47–0.89 of the model's F1 contrast (E2). Under P it collapses: R1's median D is −0.035, 0.008 and 0.007 (panels D > 0: 0, 7, 6 of 8). The model's contrast collapses as well (median D 0.021–0.034, below u_r 0.066–0.089).

The two observations that matter:

- **The static emission geometry alone does not produce R1's contrast.** P keeps the emission field and the last-symbol posterior b¹ as the same point clouds, up to relabelling (E1: S 0.568 vs 0.108 and 0.324 vs 0.165 under both O and P). If R1's contrast under O were simply inherited from the geometry of the 36 emission centres, it would survive P. It does not. So the symbol embeddings must encode something learned from the sequences: under O, symbol co-occurrence follows world adjacency (smooth dynamics plus overlapping emissions); P breaks that alignment.
- **This does not settle the E2 caveat in favour of multi-step history integration.** Co-occurrence structure is learnable from short-range (bigram-level) statistics. Under O, the F1 contrast is already present at the `embed` hook (median D 0.104–0.110, layer sweep) and from `resid_post_0` onwards. Under O, F1 therefore remains compatible with a mostly symbol-level, dynamics-learned geometry. P cannot separate the two, because under P the exact belief b³² itself no longer separates the worlds (5/8 panels; E1). A model that tracked b³² perfectly would also fail the F1 rule under P. This is why the preregistration declared H3 one-sided.

So, in short: P moves the caveat from "emission geometry" to "symbol-level statistics learned from the dynamics". It does not remove it. The strong R1 baseline under O remains an important limitation of F1.

## 3. History integration under P (H3′, X4-d)

H3′ was designed for this case, and it is supported. Under P, ρ_s(d_A, d_B32) on all pairs goes from a median of 0.09 at initialisation to 0.70 at step 5000 (V0; V1: 0.07 → 0.71). It beats max(R2, R3) (0.35–0.44) in every panel of every run. Within pairs that share w₃₂, where R1 is constant, the model's ρ_s with b³² has a median of 0.82 (O: 0.96), and it beats R2 and R3 in 48/48 run-panels (X4-d). So under P the models still organise their activations by the 32-symbol belief, which is a pre-registered positive result about history use. They do so less tightly than under O, in line with the lower captured fraction (0.87–0.91 vs 0.985–0.992). The topological contrast disappears, but the belief-alignment does not. This fits "the model follows its belief state, and the belief state under P has no cylinder signature". It does not show that topology is computed per se, nor that topological structure is causally necessary for prediction.

## 4. H4: why it is rejected, and what the rejection does and does not mean

Rule outcome: in every cylinder run under O, S on panel 1 exceeds S₀ + u_r at step 50 (S 0.237–0.250, from 0.055–0.066). Regret first drops below G_C at step 100 (0.21 vs G_C 0.265). At step 50, regret is 0.53–0.55, still above G_C. H4 is rejected as registered. Readings, all post hoc:

- **Grid resolution.** The violation spans one checkpoint interval (50 → 100 steps). D-034 counts the same checkpoint as consistent, but adjacent checkpoints as a violation. The verdict stands; a finer grid would date the crossing more precisely.
- **The early rise is not specific to the cylinder; the absolute H₁ score is not the contrast.** The square runs rise at step 50 too (S 0.172–0.230 from 0.046–0.065), and so do all P runs. The world contrast S_cyl − S_sq on panel 1 is small at step 50 (+0.020 to +0.073). It grows mainly between steps 100 and 200 (+0.175 to +0.227), after t_history. The registered H4 measure is S_t − S₀ of the cylinder run alone, so it counts a world-unspecific rise as "S rises". A dynamics rule on the contrast D_t would be a different, new hypothesis. It would need its own preregistration, and these numbers cannot test it, because they suggested it.
- The checkpoint-order null is descriptive. Its p values for the O cylinder runs are 0.07–0.18.

## 5. X4 under P

- No view passes the F1 rule under P (V0–V5). This includes the LN-gauge-free stream (V1), so the null under P is not a normalisation artefact (X4-a: verdicts equal).
- **V5 reverses, as the oracle does.** The predictive cloud has D < 0 (median −0.024 to −0.063; panels D > 0: 0, 0, 2 of 8). Under P, the oracle's next-symbol future also separates the worlds in the reverse direction (1/8 panels; E1). The positive control is ρ_s(d_V5, d_future1) = 0.97 in every run. This is an observation, not a pre-registered expectation: the X4-b expectation was stated for O only. Read with caveat 3: oracle topology does not guarantee learned topology, and here the learned predictive geometry happens to follow the oracle's.
- X4-c is "neither" under P. V4 (readout-null) carries little belief alignment under P: Δgeom on all pairs has a median of 0.009 and is > 0 in 30/48 panels, against 0.059 and 48/48 under O.

## 6. Comparison with E2

The E2 finding (F1 supported under O; H2) is unchanged. E3 adds:
1. the contrast does not survive P (uninformative for H3 by design);
2. R1's contrast does not survive P either;
3. history alignment does survive P (H3′);
4. under O, S rises before history use by the registered measure (H4 rejected).

Together these make the most cautious reading of F1 the right one: training under O produces a cylinder-specific persistent H₁ signal that the representation shares with its belief state and with its symbol-level statistics. Which of the two drives it is not decided by this design.

## 7. Surprises

- G_C differs between O and P for the square (0.236 vs 0.325) and is almost equal for the cylinder (0.265 vs 0.266). P changes how much context helps.
- Regret at initialisation is about half under P (0.71–0.86 vs 1.42–1.58).
- The layer sweep under O shows the contrast at every hook, including `embed`. There is no "emergence with depth".

## 8. Limits on causal interpretation

- No intervention was run. Nothing here shows that the H₁ structure is used for prediction, or that preserving the detected topology improves prediction.
- V3 is logit-readout-visible, not proof of causal use. V4 is logit-readout-null, not evidence that the model never computes or uses that information elsewhere (addendum D-040).
- LayerNorm is exactly invariant to mean shifts, but not in general to positive scaling with eps > 0. A V0 ≠ V1 difference would show sensitivity to normalisation, not pure gauge dependence. Here V0 and V1 agree under both O and P.
- Oracle topology does not guarantee learned topology. The V5 agreement with the oracle under both O and P is empirical.
- 3 replicates, one architecture and size, two synthetic 12 × 12 worlds, σ = 1.25, dynamics on panel 1 only, and a 12-point checkpoint grid. The controls U and the extra N runs (S7), the sensitivity analyses, and the clean rerun (S8) have not run.

## 9. Follow-ups (each needs its own preregistration; none started)

- A contrast-based dynamics rule (D_t on panel 1, or on all 8 panels at a denser grid of early checkpoints), to date the world-specific rise against t_history.
- An embedding-level control: freeze or shuffle the learned symbol embeddings, or compare against a co-occurrence (bigram) model's embedding of the same symbols, to measure how much of F1 under O is symbol-level.
- Interventions on the V3/V4 subspaces (X4-causal), already listed as out of scope here.

# Current progress - 1 November 2026

Stage: **every authorised study has a terminal reviewed outcome; nothing is running.
Planning of two new tracks (U, D) started on 2026-11-01 (owner addendum 37).**
Scientific protocols, data and earlier decisions remain unchanged. Historical progress is
available in git; decisions and execution reviews are the durable research record.

## Accepted scientific outcomes
Earlier (unchanged since the 17 October record):
- E0-E4: unchanged; G-H FAIL remains (missing historical timing record).
- X4 B INCONCLUSIVE; B2 scoped NO-GO; Phase C/H4C-I NOT_RUN. X4-F closed INCONCLUSIVE/FAMILY_UNMATCHED.
- K8 oracle headroom FAIL; K4 closed INCONCLUSIVE at chart_calibration; original C1 blocked.
- X5 G1 H5 REJECTED; closed without fresh test (D-081). D-1 all gates PASS (0020); X2a stage 0 GO_P1_NONADDITIVE (0025).
- D-2a closed NOT_LEARNED (0033). C1prime closed INCONCLUSIVE/FAMILY_UNMATCHED at M2-cal (0044; R13 ratified, addendum 10).

Since 17 October (each with its terminal review):
- **K4b (E1 then E2): EXCLUSION, EXCLUDE in all three E4 models** (E1 all gates PASS, 0055; E2 0057).
  Covariance of the chart phase with r4 lies within (-0.01, 0.01) (bounds 0.0064-0.0089). Caveat kept: the
  phase-only oracle comparator is 0.0085, below the 0.01 margin, so this does not show that the learned phase
  lacks beyond-four information (it reaches 83-95 % of the comparator); INIT_UNAVAILABLE; record defect D6.
  Review: ../agent-handoff/jobs/0057/review.md (E1: jobs/0055/review.md).
- **X6 stage 0: GO_X6_NATURAL** (oracle-only; G_Parikh(32) = 2.636e-3 nats; a GO permits design, not training).
  Review: ../agent-handoff/jobs/0066/review.md.
- **X6 stage 1 (trained): INCONCLUSIVE (rule 9).** Natural order use mean beta 0.061 (LB 0.0595), below the
  registered 0.25 (C-ORD NOT_SUPPORTED); designed order use fails in seeds 2-4; seed 1 UNRESOLVED because the
  ZC-s1 designed placebo responded (beta_W2 0.209). Total 79.55 CPU-h. Review: ../agent-handoff/jobs/0099/review.md.
- **C2 (readout attribution, C2-FROZEN-v2): C2-R USED, C2-M UPSTREAM_USED, C2-S* X_PHASE_USED, 3/3 models each**,
  study VALID (psi-hat 0.851/0.854/0.856 for R). Concerns the frozen linear code only (Q-CODE). 0.87 CPU-h.
  Review: ../agent-handoff/jobs/0115/review.md.
- **HWS stage A (oracle world sweep): HWS_SELECTED/T0**, w* = W12-q1-s1.75-p0.2 (D4 L3 0.0457 >= 0.03). Oracle-only;
  no claim that any model learns the world. Review: ../agent-handoff/jobs/0136/review.md.
- **X6ZC (designed-placebo check): UNEXPLAINED/NOT_NA_INVARIANT** for ZC-s1 (W2); ZC-s3/s4 (W1)
  NOT_NA_DIRECTION; placebo reuse FIT_WITH_AMENDMENT; X6 stage 1 verdict unchanged.
  Review: ../agent-handoff/jobs/0155/review.md.
- **C2ND (necessity and decoy): N-R CODE_DOMINANT 3/3** (complement 14-15 %, PROJECTOR_/HARMONIC_DEPENDENT_NR);
  **D DECOY_NOT_USED 3/3** (specificity caveat on C2 lifted, C2 verdict unchanged); **N-M CODE_DOMINANT_M 3/3**.
  Review: ../agent-handoff/jobs/0167/review.md. Combined addendum-29 CPU 9.53 CPU-h.
- **HWS stage B (training pilot in w*): HWSB_PASS** (2 pilot models, 620201/620202; pilots never enter stage C).
  Review: ../agent-handoff/jobs/0175/review.md.
- **HWS stage C (full test in w*, 3 new models 620301-620303): SUPPORT in 3/3.** Lower bounds 0.0406/0.0395/0.0402
  above the margin 0.01; ratio to the oracle comparator 0.89-0.93; annotations INIT_UNAVAILABLE_620302/620303.
  Licence: the coordinate is not a function of the last four observations on its supported rows; it does not
  establish use by the prediction; K4b's EXCLUSION stands. About 18,586 CPU-s (5.2 CPU-h) in all.
  Review: ../agent-handoff/jobs/0196/review.md (freeze 17c5b574, h_exec 9761e52; merged 3adf567).

## Current execution
- Nothing is running; no job is dispatched (next job number 0197). The public research summary carries the
  stage-C result (main 8f89462).
- Planning of two tracks started 2026-11-01 under owner addendum 37 (planning, review, implementation with
  independent tests and a synthetic dry run, up to an execution freeze; no real-scope run):
  - **Track U (use):** in w*, on the three stage-C models, does the prediction actually use the beyond-four-symbol
    information carried by the circle (change only the history beyond the last four symbols and measure how much
    of the change in the prediction runs through the circle)?
  - **Track D (dynamics):** on the saved stage-C checkpoints, when does that information appear during training,
    relative to the circle? No new training.
  - Requests: planning/requests/coord-hws-use-20261101.md and coord-hws-dyn-20261101.md (agent-handoff);
    two clean-context writers were running at the time of this record.

## Next actions
1. Per track: result-blind review, rulings, v2, confirmation, design freeze candidate; then implementation with
   independent test authors, dry run, execution freeze, forecast to the owner.
2. Each real-scope run needs an explicit owner run approval after its execution freeze.
3. Candidate afterwards (not approved): generality of the full test across more worlds with different amounts
   of history information. Deferred: crossing-order scale-up, control placebo anomaly, orientability redesign.

Sources: ../agent-handoff/COORDINATOR_STATE.md (top CURSOR), the job reviews cited above, and owner
addenda 25-37 (archive/owner-decisions-20261015/), addendum 37 for the new tracks.

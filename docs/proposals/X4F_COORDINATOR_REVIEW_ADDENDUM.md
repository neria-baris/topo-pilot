# X4-F — coordinator review addendum and scoped closure of x4f-exec-v2

14 October 2026. Handoff job 0004. Branch `x5-g1-planning`, from 10ed372.

**Additive only.** The [gate report](X4F_FEASIBILITY_GATES_REPORT.md), the [frozen protocol](X4F_EXECUTION_PROTOCOL_V2.md), [X4F_GATES_OUTPUTS/](X4F_GATES_OUTPUTS/), D-061, D-062 and every earlier record are unchanged. Where this addendum corrects an interpretation in the gate report, the addendum governs.

## 1. Accepted outcome (coordinator ACCEPT, jobs/0003/review.md)

| Item | Status |
|---|---|
| G1 recoverability (m32 at resid_post_1/p32) | PASS ×3 |
| G2 frozen suffix / final-null | PASS ×3 |
| G3 erasure | PASS ×3, label **LINEAR_COMPONENT_ONLY** |
| G4 matched random family | **FAMILY_UNMATCHED** ×3 (0 of 10,000 draws in the 5% window) |
| G5 support | NOT_RUN (dependency) |
| Overall gate verdict | **INCONCLUSIVE** (not FEASIBLE) |
| H4C-F causal endpoint (fresh test, ΔR) | **NOT_RUN** |
| Scientific CPU ledger | 506.46 s accepted, including the post-hoc descriptive diagnostic (not a second confirmatory run) |

**Closure.** The x4f-exec-v2 formulation is **closed** after its gate stop:

* no further draws, no altered matching rule, and no site change;
* no damage profiles, and no fresh-test sampling under it;
* no design rescue is proposed now.

**General causal use of the coordinate stays unresolved.** Nothing in X4-F shows that the model uses or does not use it.

## 2. Corrections to the gate report's interpretation

### 2.1 "Unmatchable by construction" is withdrawn

The gate report and job 0003 report said the 5% window was "unreachable by construction" and that "more draws would not fix it". **That is not established, and it is withdrawn.**

* The primary eraser's own projector is an admissible rank-r projector in the retained whitened space R^k.
* Mean displacement is a continuous function of the subspace (on the Grassmannian of r-planes in R^k).
* So the positive window |D − D_t| ≤ 0.05·D_t contains an open neighbourhood of the primary's subspace.
* Haar-random subspaces, which the QR of a Gaussian matrix produces, have full support on that Grassmannian.
* The probability of a match is therefore positive. There is no impossibility theorem, and enough draws would eventually produce matches.

**What was observed is a rare-event outcome under a fixed budget:**

* 0 accepted draws in 10,000 per model;
* on the same seeded draws, the largest mean displacement was 3.8–4.3, against a primary of about 12.7.

The correct reading is: *matches did not occur within the frozen 10,000-draw budget and appear rare*. Their probability was not estimated.

### 2.2 The eigen-alignment explanation is a hypothesis

The report said m32 "is carried by the highest-variance directions" of resid_post_1 and that this explains the displacement gap. **No measurement quantified that alignment.** The cited top eigenvalues (about 120–140, 82–86 and 80, against a mean of about 3) and the displacement gap do not by themselves measure the overlap between the primary's subspace and those eigendirections.

The statement is retained only as an **unquantified hypothesis**. No new computation is made here to test it.

### 2.3 Scope of the r2 recovery

"r2 recoverable" (validation R² 0.35–0.42) means only the following:

* the specified residual r2 = m32 − m2 is linearly decodable from resid_post_1 on dev data, above its shuffled reference;
* m2 is the expectation under the two-symbol posterior with the stationary prior.

It does **not** establish:

* long memory;
* failure of an optimal two-token predictor;
* causal use;
* use of the PH coordinate;
* H1 necessity.

It is descriptive and dev-only.

### 2.4 Scope of the RBF result

The RBF probe recovering m32 after linear erasure (R² 0.998) shows **measured nonlinear recoverability with that one fixed probe**. It neither shows that all information was preserved, nor that removal of any information was achieved or failed beyond the linear component. Conversely, a low probe score would not have shown that nonlinear information was erased.

## 3. Dormant operational defects — blockers before any X4-F code reuse

These defects did not affect the accepted gate outcome. Each must be fixed and independently tested before the X4-F gate code is reused. **They are not repaired now**, because no reuse is planned.

1. **Random-map invariant validation.** `random_family` accepts draws without checking idempotence, rank loss or retained-range containment for each accepted map, although the protocol requires these per draw.
2. **Incomplete exports.** The frozen-control maps (shuffled, R1, m2, local, generic) and the accepted random maps are not exported or checksummed. Only the primary map is exported.
3. **Coarse STOP and budget polling.** These checks happen only between gates and models, not inside the expensive loops (shuffles, the 10,000-draw family loop, RBF refits).
4. **Ledger not crash-safe.** The ledger is written only on successful return, not in a `try/finally` covering failure or cancellation.

## 4. Status after closure

* **X4 overall:**
  - the practical Q2-gap branch is closed (D-055);
  - X4-F execution v2 is closed with an INCONCLUSIVE gate (D-062, this addendum);
  - the circular-baseline audit is descriptive only (D-057).
* **Selected follow-up:** **X5 G1**, beginning with an oracle and kernel feasibility contract only ([X5_G1_FEASIBILITY_PROTOCOL_DRAFT.md](X5_G1_FEASIBILITY_PROTOCOL_DRAFT.md)). No other follow-up is opened.

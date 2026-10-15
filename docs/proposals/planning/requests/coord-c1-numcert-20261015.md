# Planning request: the C1 numerical certificate (the blocker in review change 6)

From: Claude coordinator c351b245. Context:
- protocol `planning/responses/C1-MERGED-v2.md` (sha F9F679DC…12F6), §15.3, marked NOT_READY;
- the Codex review `planning/responses/coord-c1-merged-review-20261015.codex.md`, required change 6. Read it in full: it lists exactly what is missing.

Code: main @4f219d6 in `X:/Downloads/projects/topo-pilot/topo-pilot`. Relevant parts:
- `src/topo_pilot/oracle` (BayesFilter, FutureOperator; float64 filtering with normalisation);
- `src/topo_pilot/learner/model.py` (the forward pass and `return_hooks`);
- K4's accepted error machinery in `tools/x4_circle_history/error_bound.py` and `ERROR_BOUND.md` v2.2: per-row certificates, Decimal enclosures, outward rounding and the process-law bound. Reuse its ideas and code wherever valid.

## Task
Write a replacement §15.3 that a reviewer can accept: a **proved** numerical certificate for every eligible row and model. It must bound:
1. the oracle predictive errors in q± and log q±, through the 32-step filter and the T·E prediction, for the donor histories;
2. post-logit evaluation (log-softmax of the recorded float64 logits);
3. construction of A, G, Y and Z, per arm and per control frame mean;
4. the bootstrap-mean arithmetic;
5. the signed guards for the headroom (Ḡ lower > 0.01 nat) and the V3 thresholds.

Requirements, from the review:
- Bounds are analytic for the permitted computation, or validated per-row enclosures.
- Use componentwise or relative bounds where absolute L1 bounds become uninformative for tiny probabilities.
- State every assumption about elementary functions, BLAS reductions, underflow and normalisation.
- Round outward.
- η = 1e-12 and 2^-44 may be kept only with a source-specific derivation.
- Define b^Z_{j,i}, r^mean_j and B_num,j = max_i b^Z + r^mean, with the 1e-9 floor as an extra guard.
- **Prefer the simplest rigorous route:**
  - (i) a standard backward/forward floating-point analysis (Higham-style γ_n) of the normalised forward filter, giving componentwise relative bounds that grow linearly in the number of steps;
  - or (ii) a cheap validated enclosure, for example interval arithmetic on the filter, if its CPU cost is feasible for about 30k rows × 2 donors × 3 models.

  Give the cost estimate. CPU is uncapped, but keep it proportionate.
- The certificate must not make INCONCLUSIVE near-certain for ordinary scientific headroom. Show the expected bound magnitude compared with the 0.10·G margin, with G of order 1e-2 to 1e-1 nats.

## Deliverable
1. `STATUS: FREEZE_READY | DRAFT | BLOCKED`.
2. A summary of at most 250 words.
3. The full replacement text for §15.3, with proofs.
4. The exact edits needed in §13 step 2, §16, §20 item 14 and C-19.
5. A reuse note covering what comes from K4's error_bound and what is new.
6. Open questions.

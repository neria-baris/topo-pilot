# Planning request: a chart-construction redesign after K4 ended INCONCLUSIVE (for the owner's decision)

From: Claude coordinator c351b245. This is documents only. Any execution needs the owner's decision, because it changes a frozen method (owner policy part B6).

## Facts
- **K4 feasibility (job 0018)** ended **INCONCLUSIVE at chart_calibration, model 1729.** The frozen rule takes 512 raw 128-d `resid_post_3` p32 panel-1 vectors, Euclidean VR over F47, the largest finite H1 bar, and the midpoint scale. At that scale the 1-skeleton does not connect all 512 landmarks, so `primitive` (BFS normalisation) raised Unresolved. The exact integer lift itself succeeded.
  - Read: `agent-handoff/jobs/0018/report.md` and `review.md`; the frozen K4 protocol `topo-pilot/docs/proposals/CIRCULAR_HISTORY_K4_PROTOCOL_DRAFT.md`; code `tools/x4_circle_history/chart.py` and `cochain.py` (main @c2046fc, repo `X:/Downloads/projects/topo-pilot/topo-pilot`).
- **Not persisted:** the selected bar's birth/death and the component count. Nothing has been recomputed; no diagnostic has been run.
- **C1-FROZEN-v1 is blocked by its own freeze.** `agent-handoff/planning/responses/C1-FROZEN-v1.md` §14 stops C1 when K4's chart gate is INCONCLUSIVE.
- **E4 S7 did build descriptive circular coordinates** on the same models, with agreement 0.88–0.89 to the latent periodic coordinate, using a different construction: `src/topo_pilot/topology/circular.py`, plus the experiment code `src/topo_pilot/experiment/s7_circular.py` and `report_e4_s7.py`. Compare the two constructions exactly.
- **All panel-1/2 data is already exposed** (E4 test data). Anything new is exploratory unless validated on fresh data.

## Questions to answer
1. **Diagnosis without data.** From the code and the mathematics alone, what plausibly makes the midpoint-scale graph disconnected? Candidates: outliers, VR on a heavy-tailed cloud, a midpoint scale below some points' first connection, a short bar chosen as "largest", and anything else that applies. Which cheap, pre-declared diagnostic would discriminate between them (bar birth/death, component sizes, isolated points), with no fitting?
2. **Redesign options,** each with its exact rule, its identifiability, and the risk of "fitting the method to the failure". Candidates:
   - (a) the largest connected component, with an exclusion fraction gate;
   - (b) a scale rule guaranteeing connectivity (for example max(midpoint, connectivity threshold), or the death minus ε);
   - (c) maxmin landmarks plus extension;
   - (d) reusing E4's validated CircularCoordinates construction as the chart;
   - (e) a denoising or kNN-graph chart;
   - (f) stopping K4/C1 entirely and redirecting effort.

   For each: what changes in K4 and in C1, what stays frozen, and whether old results remain comparable.
3. **Recommendation.** One design, or a decision tree, that the owner can approve in the morning, with:
   - the pre-registration discipline: everything fixed before any new chart computation;
   - how to handle the fact that the data is exposed, for example evaluating on fresh histories;
   - cost;
   - an honest estimate of whether the redesign is worth it versus stopping. Priority 1 asks how much of the circle needs long history; priority 2 asks about causal use.
4. **The minimal diagnostic job** you would run first, if the owner approves diagnostics only.

Deliverable: `STATUS: PROPOSAL`, then a summary of at most 300 words, then the full analysis, then the questions for the owner. Be rigorous; prefer simple, robust and pre-declared.

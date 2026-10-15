# Planning request: C1 to freeze readiness, plus a D sketch

From: Claude coordinator c351b245-9ff3-4f5c-b324-60ee25725fd7 (sole coordinator since 2026-10-14T20:47:05Z; archive/incoming-claude-coordinator-20261014T204705Z/ASSUMPTION.json).
Authority: archive/owner-overnight-transfer-20261014/OWNER_MESSAGE.md (sha 13160D21...), parts B3-C/D and E.
Charter: NEXT_RESEARCH_AND_WORKFLOW.md, section "Owner research charter".
Inputs: your response owner-causal-protocol-c1-20261014.md (sha 1E101BB6...) and draft commit fc2c107 on planning-causal-state-forcing-20261014.

## Request 1 (priority): make C1 freeze-ready
Update the draft in your planning worktree. Documents only: no Python, no data access. Resolve every NOT_READY item you listed:
1. **Exact nonlinear probe family.** Specify the class, capacity, fit split and selection rule, all fixed in advance.
2. **Information-damage matching for the random controls.** Specify the metric, the matching tolerance and an early-stop gate. Also specify how intended nuisance changes are distinguished from damage.
3. **Support and counterfactual alignment.** Specify which rows are eligible, how the forced state is constructed (centroid curve), and the support check against the oracle counterfactual prefix that preserves the last symbol.
4. **Single endpoint.** Give the exact formula (regret advantage versus the controls, normalised by the oracle margin), the precision method for the ratio, and the decision rule with strictness. State explicitly what PASS and what FAIL each license, and what neither licenses.
5. **Seed maps and identities.** Cover seed maps, chart identity (reuse the K4 chart/gauge artifacts if K4 produces them, otherwise state the alternative), and the binding of model, checkpoint and panel IDs. The fresh test set must be new histories never exposed.
6. **Six-field reuse assessment** per the charter. State which existing modules and tools are reused unchanged. In particular reuse the meter, ledger and guards from tools/x4_oracle_profile and tools/x4_circle_history, and the oracle and activation extractors. State the minimal new code.
7. **Staged plan.** Cover written contract -> independent test authors -> implementation -> cal/val feasibility gates -> fresh single-endpoint test. Give rough CPU estimates per stage. Note that CPU is uncapped, with at most 4 threads and 12 GiB.

Return a planning response with the new commit and sha, and mark it FREEZE_READY or list what remains. An independent clean-context review will follow before any freeze.

## Request 2 (if credits remain): D sketch
Owner queue D asks for a mathematical, oracle-only check. Question: is there a hidden-world process, ideally close to the existing cylinder/square machinery, where a topological distinction is provably unnecessary for next-symbol prediction (horizon 1) but necessary at some horizon k > 1? The gap must hold by construction, not be an estimate.

Give one or two concrete constructions with proof sketches. Also give the oracle-only check that would confirm each, and its cost. Do not reopen B2 (D-055 scoped NO-GO).

## Notes
- Execution stays with the coordinator. Nothing waits on you for more than 60 minutes.
- If you run out of credits mid-way, commit what exists and say so in the response.

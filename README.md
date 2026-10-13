# topo-pilot: topology of a latent world in transformer representations

> **Status: exit level E1 reached** (2026-10-13): σ calibrated and the preregistration committed before any training ([`PREREGISTRATION.md`](PREREGISTRATION.md)). Implementation continues wave by wave following `ORCHESTRATOR_PROMPT.md`.

## Current finding (E1)

**With no model involved, the exact Bayesian belief and prediction spaces already separate the cylinder from the square under the smooth emission O (S_cyl > S_sq in 8/8 panels in every space; belief b³² median S 0.671 vs 0.321, Gaussian floor ≤ 0.10), while under the axis-permuted control P the belief space no longer separates them (5/8 panels).**

Median S over 8 panels of 512 histories each (Hellinger distances, VR over GF(2)); replicate 1729, σ = 1.25:

| space | O: cylinder vs square (panels cyl > sq) | P: cylinder vs square (panels cyl > sq) |
|---|---|---|
| belief b³² (exact filter) | 0.671 vs 0.321 (8/8) | 0.323 vs 0.310 (5/8) |
| last-symbol posterior b¹ | 0.324 vs 0.165 (8/8) | 0.324 vs 0.165 (8/8) |
| next-symbol future F₁ | 0.556 vs 0.189 (8/8) | 0.194 vs 0.241 (1/8) |
| two-symbol future F₂ | 0.614 vs 0.216 (8/8) | 0.202 vs 0.242 (2/8) |
| emission field (144 states) | 0.568 vs 0.108 | 0.568 vs 0.108 |

The rows for b¹ and the emission field are identical under O and P. P permutes the states, which leaves both point clouds unchanged up to relabelling. Consequence, pre-registered: H3 (structure under P) can only be decided in one direction. A failure under P is expected even for the ideal predictor.

### Earlier exit (E0, no model)

The PH pipeline recovers the known topology. Vietoris–Rips on the intrinsic metric gives one long H₁ bar for the cylinder (S = 0.299) and none for the square (S = 0.037), even though their transition graphs have 133 and 121 independent cycles. Graph cycles are not surface holes. Gate G-A passed with thresholds fixed in advance (D-016). Details: [`reports/E0/summary.md`](reports/E0/summary.md).

**Not run yet:** S3–S8 (training, F1 on activations, controls, dynamics, sensitivity). No claim is made about learned representations.

## Reproduce (Windows, CPU)

```powershell
python -m venv .venv; .\.venv\Scripts\python.exe -m pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.lock -e .
.\.venv\Scripts\topo-pilot.exe stage S0   # environment and contract sanity
.\.venv\Scripts\topo-pilot.exe stage S1   # worlds, kernels, emissions, PH calibration (~30 s)
.\.venv\Scripts\topo-pilot.exe stage S2   # data, exact oracle, baselines, σ, discriminability (~5 min)
.\.venv\Scripts\topo-pilot.exe prereg     # regenerates the S2 tables in PREREGISTRATION.md
.\.venv\Scripts\topo-pilot.exe report --level E0
```

## The question, in one paragraph

Train a small causal transformer from scratch to predict the next symbol of sequences emitted by a hidden random walk on a world whose topology is known: a **cylinder** versus a **square**. The two worlds have the same number of states, the same emission statistics, and the same dynamics rule. The **single finding** (F1) the project is built around: does training increase a persistent H₁ signal in the residual stream that distinguishes the cylinder from the square, beyond initialisation and consistently across seeds and sample panels?

Three ingredients make the answer interpretable:
- an exact Bayesian oracle;
- matched controls: an emission whose spatial smoothness is permuted away, and an emission that carries no information;
- representation baselines for known pitfalls: symbol mixing, per-state centroids, and the Gaussian noise floor.

The answer is interpretable **whether it is positive or negative**.

## How to use this package

1. Unzip, and open the folder as the working directory of a capable coding agent (the "conductor").
2. Give it `ORCHESTRATOR_PROMPT.md` as its instructions.
3. The conductor:
   - builds the modules wave by wave, with cheaper sub-agents working in parallel;
   - verifies each module in isolation;
   - runs the stages;
   - stops at four human checkpoints (H1–H4) for your approval.
4. You can stop after any stage and still have a working, reportable result (exit points E0–E4).

## Map

| Path | What it is |
|---|---|
| `ORCHESTRATOR_PROMPT.md` | the master prompt for the conductor model |
| `docs/RESEARCH_SUMMARY.md` | binding research decisions (English) |
| `docs/RESEARCH_PLAN_HE.md` | the full plan with rationale and literature (Hebrew) |
| `docs/STAGES.md` | build waves, run stages S0–S8, gates, exit points, budgets, cut paths |
| `docs/CONVENTIONS.md` | OOP, docs, tests, and logging rules |
| `docs/DATA_SCHEMAS.md` | every artifact, field, shape, and access rule |
| `docs/EXECUTION.md` | local vs external execution (bundles for any GPU machine; no cloud-drive dependency) |
| `docs/HANDOFF.md` | how another model or person resumes the work |
| `docs/EXTENSIONS.md` | X1 orientability, X2 unions of tori, X3 higher-dimensional holes |
| `agents/` | brief templates, report format, review checklist |
| `src/topo_pilot/<module>/SPEC.md` | the contract of each of the 12 modules |
| `tests/<module>/TEST_PLAN.md` | the separate test plan of each module; `tests/integration/` runs at gates only |
| `configs/` | `base.yaml` (closed decisions), `stages.yaml`, `extensions/` |
| `state/` | `PROGRESS.md` (overwritten), `DECISIONS.md` (append-only) |
| `tools/SPEC.md` | repository checks: affected tests, import and leakage rules, file sizes, state hygiene |

## Modules and dependencies

```mermaid
flowchart LR
  C[contracts] --> W[world] & P[process] & D[dataset] & O[oracle] & L[learner] & A[activations] & PR[prediction] & T[topology] & AN[analysis] & X[experiment] & EX[executors]
  W --> P --> D & O
  D -->|public tokens only| L --> A
  O --> PR & AN
  A --> PR & AN
  T --> AN
  PR & AN & EX --> X
```

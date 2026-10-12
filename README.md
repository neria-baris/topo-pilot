# topo-pilot: topology of a latent world in transformer representations

> **Status:** specification package. This repository contains no implementation yet. It holds:
> - an orchestration prompt;
> - binding research decisions;
> - per-module contracts and test plans;
> - data schemas, stage gates, and configs.
>
> The code is built by following `ORCHESTRATOR_PROMPT.md`.

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

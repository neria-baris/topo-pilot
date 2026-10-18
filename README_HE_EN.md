English translation of README_HE.md at commit 727af56 (job 0068). The Hebrew original is authoritative.

# A short guide for the owner

> **Scope of this translation.** This file translates only the content of `README_HE.md` that the English `README.md` does not already cover. The following sections of the Hebrew original are **not** repeated here, because `README.md` already carries them:
>
> - "Project status: exit point E4 reached (2026-10-13), with a failed and documented gate": the binding English finding is quoted verbatim from `README.md` ("Current finding (E4)"), and the five-point Hebrew summary is a free translation of `README.md`'s "How to read it" list.
> - "After E4": the table and the bullet list match `README.md` "After E4" item by item.
> - "License": matches `README.md` "License".
>
> Where the two differ, `README.md` is the binding English text for those sections.

This folder started as an **instruction package**. A strong model (the "conductor") built the project from it, with cheaper sub-agents. The code, the summarised data and the reports are now in the repository.

## Getting started

1. Open the folder as the working directory in a coding-agent environment, for example Claude Code.
2. Give the strong model the instruction:

   > Follow ORCHESTRATOR_PROMPT.md. Start with §13.

3. The model will stop and ask for your approval at four points:

   | Point | When |
   |---|---|
   | **H1** | after calibration and preregistration, before any training |
   | **H2** | before the training runs: the estimated time, and whether to run locally or externally |
   | **H3** | before any change to a closed decision |
   | **H4** | before the finding is written into the README |

## What is already built into the package

| Requirement | Where it is handled |
|---|---|
| A strong model as conductor, and cheap sub-agents for building | `ORCHESTRATOR_PROMPT.md` §2–3. The tier table is by role, so models can be swapped |
| Building and verifying each module separately; independent tests for the critical modules | §3, `agents/`, and `tests/<module>/` |
| OOP, abstract classes and registries for extension | `docs/CONVENTIONS.md` §3 |
| Parallel work in waves, without write conflicts | `docs/STAGES.md` §1, and the main document §4 |
| Documentation of the logic and the data | a README for each module, and `docs/DATA_SCHEMAS.md` |
| No bloated logs | The project state is kept only in `state/`, with a length limit. Sub-agent reports are limited to 150 words and are not kept |
| Switching to another model | `docs/HANDOFF.md` |
| Separate tests | `tools/affected_tests.py` runs only what changed |
| Running without a graphics card | The default assumes there is no GPU. The model is small, and by estimate one training run on an ordinary CPU takes 15–45 minutes, so the stages up to E2 are expected to take 2–5 hours. Stage S3 measures the actual speed: if the next stage is expected to take up to 8 hours, it runs locally on the CPU. Otherwise, the `executors` module packs each training run into a bundle that runs on a free GPU (Colab, Kaggle) or a rented one, and the results are imported back with verification. See `docs/EXECUTION.md` §5 |
| Stages and stopping points | E0–E4 in `docs/STAGES.md` §3 |
| Extensions | `docs/EXTENSIONS.md`. They can be added without changing the core |

## The extensions

- **X1, orientability:**
  - Möbius versus cylinder: they have the same homology, and the difference is in the number of boundary components.
  - Klein bottle and RP² versus torus and sphere: the difference shows when homology over $\mathbb{F}_2$ is compared with homology over $\mathbb{F}_3$.
- **X2, unions of tori:**
  - Disjoint union: uncertainty about *which world*.
  - Connected sum: a genus-2 surface.
- **X3, higher-dimensional holes:** $S^2$, $T^3$, $S^3$. The H₃ computation is approximate only, and is marked as such.

The full research plan, including the rationale and the literature, is in `docs/RESEARCH_PLAN_HE.md`.

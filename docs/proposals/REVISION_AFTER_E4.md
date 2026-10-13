# Revision after E4: evidence, changes and decision log

Revision date: 13 October 2026, Asia/Jerusalem. Source programme: the five Markdown documents in the separate E3 research worktree, based on `566d8438b8ad5293a8dd75d66aac2c7b5ebf39ea`. Revised repository snapshot: `f8afc2a5e43309aa4bf2d402f2be4e38470df180`. **Planning only: no feasibility audit, model fitting, new histories, intervention, training or experimental stage executed.** This is a proposal revision log, not an entry in `state/DECISIONS.md`.

## State reconciled before revising the five plans

**[R] Independently checked in the repository:** `state/PROGRESS.md`, D-047–D-050, both preregistrations, stage/extension definitions, E2/E3/E4 reports, README status, relevant contracts and code, git history and the annotated local E4 tag. Contrary to the conditional wording in the supplied request, approval/publication/tagging **have occurred**: D-050 and commit `f8afc2a` record owner acceptance of the E4 milestone and README publication; E4 points to that commit. This acceptance does not turn G-H into a pass.

The G-H artifact `01d88b2167c32252` records `verdict=fail`, `waiver_reason=null`; only `rerun_ok` fails. Its parent S8 records are rerun `f6c43ab3567c578f`, integrity `2f1d3b78b176d1c5`, and report reproduction `110dd1623d0288c3`. S7 records include dev extraction `13be28a051ce15b1`, probes `63ebd7ec1ba5f38a`, circular coordinates `a7a60592e32b26fb`, sensitivity `baff2c7a1e5294c9` and controls `0c524e243a82c7f3`. Metadata and relevant already-written result rows were inspected; no checksum rerun or new scientific calculation was performed here. No RunManifest files were found in the inspected artifact tree, so provenance uses recorded parent IDs, metadata, S8 result records and git history, not a claimed independently available job manifest.

**[R] Reproducibility scope, preserved exactly:** the completed report states 307/307 shared artifacts reproduced bitwise, all six gate verdicts matched, and 9/9 generated E0/E2/E3 report files matched byte-for-byte. One rerun-only historical `run_timing` MetricRecords (`d5f25f7e2968a602`) was absent from the original store because its writer was added after original S3 (D-032, commit `106d3b4`). G-H remains FAIL; nothing is backfilled, waived or reclassified. D-048/`compare_stores` exclude measured timing rows when comparing timed records and compare GateReports by verdict rather than full bytes. Preserve those declared comparison exceptions alongside the report's bitwise language. The rerun used the same machine/interpreter/environment, repeated only cylinder-O-1729 (one of 17 trainings), and did not test GPU/cross-machine determinism. The original temporary rerun clone was deleted by S8, so this revision verifies its stored account, not the deleted clone itself. I03/I05 remain unimplemented gaps.

## E4 impact matrix — prepared before editing the five plans

| E4 result | Previous assumption | What changes | Which proposal is affected |
|---|---|---|---|
| F1 O supported, P rejected; H2 remains sign-consistent and H3′ remains supported in their registered scope; H4 rejected | E3 was the latest established evidence | Preserve every verdict and the one-sided P interpretation. Belief geometry and an H1 contrast remain different properties. | Landscape, Roadmap; all interpretations |
| Chord/PCA-32/M256 preserve O/P F1 conclusions; sqrt-JS preserves H3′ | Sensitivity had to await E4 | Metric/sample-size fragility is less pressing within these tested single-factor variants. sqrt-JS does not change activation S/F1 by construction; it is not an independent fourth PH replication. | Landscape, X4, X6 |
| Cylinder O circular agreement 0.884–0.892, belief reference 0.915; P cylinder 0.049–0.054 | A periodic target might be absent/unstable | A periodic coordinate is a more plausible intervention target under O, but the result is privileged/descriptive and not causal. Intermediate-hook and out-of-sample validity remain untested. | X4-F, X6 boundary/transport |
| Initial cylinder 15/24 and trained square 24/24 panels exceed the circular permutation-null q95 | A permutation-null exceedance might be enough to qualify the target | Require R1/b1/axis/square/initialization comparisons and held-out history-specific gain; null exceedance alone is weak. | X4-F, X6 |
| No direct R1 circular baseline; r_w decoding under O R²=0.965–0.985 | Last-symbol PH was a caveat but circular correspondence might strengthen history attribution | Direct R1/embed, b1 and one-hot controls become mandatory before claiming circular history integration. R2/R3 remain controls. | X4, X6, Roadmap |
| U cylinder agreement 0.601; captured_U≈0.999, GC=0; one replicate | State visibility might act as a topology positive control | U shows a symbol/dynamics route to a circle without history inference. It is a dynamics sanity control, not a PH ceiling or a monotonicity test of ambiguity. | Landscape, X4-F, X6 |
| O activation→b32 R² median0.829 vs exact F1→b32 0.838; P 0.378 vs0.382; rival-beating pattern only1/6 per condition | Extra final-null information was a plausible immediate target | Expected additional effect is lower and ceiling probability higher. Gate Q2 before fitting; make nonlinear-Q1 and exact-belief comparisons mandatory secondary controls. This does not prove Q1 sufficient for Q2. | H4C-I, Landscape, Roadmap |
| O probe λ=0.001 at the fixed grid's lower edge | Existing linear-probe estimate might bracket its optimum | Preserve old probe results; note regularization/feature scaling limitation. Declare any future expanded-grid sensitivity prospectively; never repair S7. | X4-I and next-experiment contract |
| G-H failure has a specific provenance explanation; milestone accepted by owner | E4's completion/approval and rerun status were unknown | Provenance review is now documented, not a reason to repeat all training. Preserve FAIL and narrow reproducibility scope. | Landscape, Roadmap, all snapshot headers |
| No intervention, new-world or curvature experiments were run | Causal/X5/X6 work awaited authorization | These branches remain proposals. E4 supplies no causal topology evidence or optimization effect size. | X4-F, X5, X6 |

## Substantive revisions and approval consequences

| Original statement/assumption | Evidence or objection | Revision | Consequence / primary impact | Owner approval before execution? |
|---|---|---|---|---|
| Immediate audit then fresh decoder test, with a qualitative horizon gate | Ambient kernel can miss reachable support; no numerical gate has been evaluated | Separate B audit and C prospective stages with explicit GO/NO-GO/INCONCLUSIVE and coverage/precision requirements | H4C-I retained conditionally, not presumed worth executing | Yes: gate choices and an audit-only implementation scope |
| Nonlinear-Q1 comparator optional | Linear accessibility does not establish information insufficiency; E4 F1 probes are competitive | Mandatory capacity-budgeted nonlinear-Q1 secondary comparison plus equal-budget augmented nonlinearity and controls | Primary J and≥10% remain unchanged; stronger claim depends on additional evidence | Yes: auxiliary model family/budget, not a retrospective primary replacement |
| Existing dev extraction potentially reusable | S7 dev sets contain resid_post_3 only; no dev F2 persisted | Reuse raw dev residuals, derive u from matching weights, calculate dev F2 with existing kernels; verify hook inventory before extra extraction | Low implementation cost; no Transformer retraining | Yes for future calculations, extraction and auxiliary fitting |
| Coordinate erasure could support a topology-associated causal account | Erasure may remove ordinary position, symbol or predictive information | Add periodic/nonperiodic/local-position/last-symbol matched controls and A/B/C manipulation labels | H4C-F effect≥0.01 nat unchanged; claim limited to specified coordinate-associated use | Yes: expanded control contract and matching tolerances |
| Circular coordinate from leading cocycle qualifies a target | E4 lacks R1; permutation null weak; no out-of-sample extension | Add direct R1 circular statistic and a held-out same-last-symbol target-residual test | No history-origin claim without added predictive/coordinate accessibility beyond symbol | Yes before registration; not a change to original pilot |
| Functional geometry absent | Fisher pullback has established precedent and can complement erasure controls | Add an optional exploratory local Fisher/Jacobian diagnostic with explicit zero-null and finite-step limitations | No primary endpoint changes; no necessity or global topology conclusion | Separate optional scope; not required to start X4 |
| G1 effect can motivate curvature interest after a speed control | Mean jump rate does not fix gap, mixing, entropy or correlations | Require movement-rate/spectral/mixing diagnostics before even proposing curvature attribution; retain process-level claim if matching fails | H5≥250 steps unchanged and explicitly practical, not calibrated by E4 | Yes: process pair/training; curvature attribution needs a stronger design |
| Boundary test a possible minimal representation contribution | E4 strengthens symbol and spatial confounds | Treat first as feasibility; add R1 circular/spatial and oracle controls; require incremental evidence for stronger contribution | H6-B rule retained, interpretation narrowed; no new primary threshold | Yes for future selected boundary evaluation |
| Local chart disagreement may connect to gluing | Global computation exists; surrogate mismatch can be approximation error | Separate local error, compatibility residual, cycle inconsistency and a defined cohomology-class obstruction | Sheaf vocabulary confers no novelty by itself | Only after a precise cochain/task contract exists |
| Transport task sketched as a sign carried around a Möbius loop | Ordinary random walks need not expose it; local statistics/boundaries confound | Define a flat Z2 transport task on one fixed cylinder with anchor-only sign cues, exact observed-bigram matching and finite-history witness | Longer-term concrete candidate; not evidence that Transformers need topological representations | Yes, after mathematical/oracle feasibility; new training deferred |
| Three practical criteria:10%,0.01 nat,250 steps | No completed pilot calibrated their universal relevance | Retain all three, mark them as prospective minimum effects, and record any future changes for approval before registration | No silent amendment of any proposed primary hypothesis | Yes to adopt them; any change requires explicit approval |

The revised plans preserve canonical symbol remapping, trajectory-level uncertainty, three model replicates, frozen checkpoints, independent future test lineage, immutable sources, module/access boundaries, cost caps and negative/inconclusive outcomes. Eight documents are delivered; the older five-file package remains untouched in its original worktree.

## Revision verification boundary

The revision independently inspects published repository state, existing result records and interfaces. It does **not** independently replicate E4 experiments, verify all785 artifact payloads, calculate new ranks/reachable collisions, fit decoders, or test the proposed transport process. Proposed numeric gate settings and resource estimates are [H/S] design choices, not new findings. See [X4 next experiment](X4_NEXT_EXPERIMENT.md) for the exact audit/prospective stop boundary and [Roadmap](RESEARCH_ROADMAP.md) for the decision brief.


## Additional amendment: minimal reusable harness

The later “Reusable Mathematical Research Harness” patch adds an eighth document and takes precedence on package size. Added [RESEARCH_HARNESS_ARCHITECTURE.md](RESEARCH_HARNESS_ARCHITECTURE.md), with eight conceptual layers, six scientific gates, minimal existing-module adapters, ten-row compatibility matrix, four worked cases, and incremental stages. All five direction/landscape/roadmap documents map to it; [X4_NEXT_EXPERIMENT.md](X4_NEXT_EXPERIMENT.md) distinguishes immediate B interfaces from deferred C/D/future interfaces.

The minimal B harness is input/task metadata, existing exact kernels, pure feasibility functions and typed provenance/reporting. No platform, general learner, world/Oracle supertype, sheaf engine or automatic scheduler is required. Choose X5 G1 as a later architectural stress test because it retains HMM/task semantics; this is not authorization or a mandatory scientific follow-up.

One concrete same-base sign-transport task now has an analytic finite-history witness, matched stationary local observation laws and explicit unobservable controls. Actual Möbius base comparison remains confounded by boundary/adjacency unless within-base controls are used. The witness is a proposed mathematical construction, not a new experimental result. The constrained nonzero-section obstruction is kept distinct from absolute sheaf H1.

Final deliverable: **eight Markdown documents** under docs/proposals, plus a ZIP containing exactly those eight relative paths. No proposal execution, source/test/config/state/preregistration/report/artifact edits, merge or push.


## Delivered file inventory and document-only QA

The archive contains these eight files, preserving relative paths:

- docs/proposals/RESEARCH_LANDSCAPE.md
- docs/proposals/RESEARCH_ROADMAP.md
- docs/proposals/X4_CAUSAL.md
- docs/proposals/X5_GEOMETRY_OPTIMIZATION.md
- docs/proposals/X6_TOPOLOGICAL_INVARIANTS.md
- docs/proposals/REVISION_AFTER_E4.md
- docs/proposals/X4_NEXT_EXPERIMENT.md
- docs/proposals/RESEARCH_HARNESS_ARCHITECTURE.md

Document QA checks local file links, heading anchors, table column counts, code-fence balance, eight-file completeness and ZIP/source content equality. These are packaging checks, not experimental validation of any proposed method. The research worktree contains only new docs/proposals files; the active workspace has no changes. Existing five-document source package is retained. Bibliography uses primary linked records; proposed controls and analytic transport arguments remain separately labeled.

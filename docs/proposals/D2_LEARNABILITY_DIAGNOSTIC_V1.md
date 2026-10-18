# D2 development diagnostic v1 — proposed successor, not a rerun of D-2a

Date: 17 October 2026. Status: reviewable development plan; not frozen or executed.
Authority: owner request to repair the identified failures. D-2a remains NOT_LEARNED.
No data generation is dispatched while the K4b reservation is active.

## Question and competing explanations

The two D-2a H3 models completed training but did not beat the exact window-8 predictor
on the registered band-edge contrast. This does not establish whether the cause was
optimisation, capacity, supervision strength, or the combination of task and recipe.

Distinguish those explanations before training another 14-model grid:

| Observation | Interpretation permitted |
| --- | --- |
| A tiny fixed token fixture cannot be overfit | Model/loss/training plumbing remains suspect |
| Tiny fixture passes, natural task improves with learning rate only | Evidence for an optimisation limitation of the old recipe |
| Natural task improves with increased capacity only | Evidence for a capacity/recipe limitation; not a capacity theorem |
| A posterior-supervised diagnostic succeeds but all generative recipes fail | Target is accessible with privileged supervision; does not prove the generative objective should learn it |
| Every tested variant fails | No workable recipe established in this bounded development study |

## Reuse assessment

Reuse the D-1 process, oracle, D-2a token layout, multi-horizon head and loss, trainer,
RidgeProbe, exact window-8 predictor, band-edge statistic, and episode-cluster bootstrap.
Use the repaired process-tree supervisor. Historical D-2a pools/checkpoints may be inspected
as explicitly exposed development evidence, but their test pool is not read or reused.
Do not implement another sampler, filter, trainer or statistical decision engine.

The missing capability is a small diagnostic driver with explicit development fixtures,
recipe configurations and per-step auxiliary-loss reporting. It must not monkeypatch a
frozen runner or change D2A-FROZEN-v1. Implementation tests first verify the multihorizon
target ordering, masking, per-head gradients and H1 equivalence on fixed synthetic tokens.

## Stage A: technical fixtures, no scientific histories

Run two deterministic, hand-authored token fixtures, each with eight sequences: one with
a constant next-symbol rule and one with a fixed two-symbol dependency. Retain unique
input/target pairs so that no incompatible targets share an input. Report exact empirical
conditional-entropy floors and the training loss minus its own floor, separately per head.
Require finite gradients and loss, nonzero gradient in each trained head, and excess loss
below 0.05 nats by 1,000 updates. A failure stops the diagnostic for code inspection.
These are training-plumbing checks; they are not evidence about the D-1 natural task.

## Stage B: bounded development matrix

Use fresh, development-only natural pools after the active reservation closes. Propose
namespace `d2-development-v1`, data seeds 720101/720102 and model seeds 720201/720202;
these are candidates until the authoritative collision registry accepts them. The frozen
manifest must bind process/emission hashes, stream scopes, token ordering and source.

Per data seed: 131,072 training, 4,096 development and 4,096 selection-validation episodes;
none is a confirmatory test. Evaluate at 0, 1,000, 2,500, 5,000, 7,500 and 10,000 updates.
Keep the original architecture/optimiser schedule except the one specified variation:

| Recipe | Change from the old H3 recipe |
| --- | --- |
| R0 | Reference recipe, 4 layers, d=128, learning rate 1e-3 |
| R1 | Learning rate 3e-4; all other choices identical |
| R2 | Learning rate 3e-3; all other choices identical |
| R3 | d=256, heads=4, d_mlp=1024; original learning rate and four layers |

Two paired model seeds per recipe, eight runs total, fixed 10,000 updates. Use common
training pools and paired initialisation streams wherever shapes agree. Equal update
counts are not equal compute: record parameters, tokens, CPU and wall time for each run.
Before admitting the full matrix, benchmark synthetic fixtures and produce an end-to-end
resource forecast including scoring. Bind the CPU ceiling and scratch/output limits in
the reviewed manifest; a missing ceiling means NOT_RELEASED, never an unlimited run.

Report total loss, each head's loss, oracle regret, next-symbol beta1, window-8 beta1,
kappa1 and their paired episode-cluster intervals at every fixed checkpoint. Diagnose
target rarity and oracle headroom from development pools only. Do not select a checkpoint:
recipe qualification always uses step 10,000 and the unchanged D-2a learnability criteria.

Selection is deterministic: among recipes passing all criteria in both seeds, choose the
one with the smallest mean step-10,000 oracle regret on selection-validation. Break ties
by smaller parameter count, then recipe order R0/R1/R2/R3. If none qualifies, stop and
report NO_WORKING_RECIPE. Any subsequently proposed longer schedule is another development
version, with no silent extension of these runs.

## Optional diagnostic with privileged supervision

Only if Stage A passes and every Stage-B recipe fails, propose a separately labelled
development control: original trunk with an auxiliary posterior-prediction head trained
from exact oracle labels. Fix its loss weight and budget in the reviewed manifest before
running it. No privileged target enters any confirmatory model. Its success would show
accessibility under different supervision, not success of the original research hypothesis.

## What follows a successful recipe

Publish all eight runs, including failures, and lock exactly one recipe before creating
new confirmation pools. A successor protocol must use new data/model seeds, repeat the
learnability gate, define the H1/H2/H3 contrasts and multiplicity correction, and use a
single fresh test. Freeze resource forecasts and thresholds before data. Development
scores, conditional selection and hyperparameter exploration are disclosed. No development
confidence interval is presented as confirmatory evidence, and D-2a's verdict is unchanged.

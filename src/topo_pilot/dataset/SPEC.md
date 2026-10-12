# SPEC: `dataset` (wave W2)

## Purpose

1. Samples trajectories from (T, E, π) in the canonical emit-then-transition order.
2. Splits them by trajectory.
3. Produces the **public** observations and the **privileged** latent sidecar as separate artifacts.
4. Builds the fixed analysis panels.

This module is the leakage boundary.

## Public API

```python
@dataclass(frozen=True)
class DatasetConfig:
    n_train: int = 131_072; n_dev: int = 4_096; n_test: int = 4_096
    n_panels: int = 8; panel_size: int = 512; analysis_position: int = 32

class HMMSampler:
    def __init__(self, T: np.ndarray, E: np.ndarray, pi: np.ndarray, layout: SequenceLayout): ...
    def sample(self, n: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
        """tokens uint8[n,33], states int16[n,33]; z1~pi; emit w_t~E[z_t]; then z_{t+1}~T[z_t]."""

class PanelBuilder:
    def build(self, test: ObservationSet, cfg: DatasetConfig, rng: np.random.Generator) -> HistoryIndex: ...
    # 8 disjoint panels × 512 distinct test trajectories, end = 32, history_id per DATA_SCHEMAS

class PublicTokenDataset(torch.utils.data.Dataset):   # the ONLY loader the learner may use
    def __init__(self, obs: ObservationSet, layout: SequenceLayout): ...
    def __getitem__(self, i) -> tuple[torch.LongTensor, torch.LongTensor]: ...  # (inputs[33], targets[33])

class DatasetStage:   # I/O; consumer name "dataset"
    def run(self, transition_id: str, emission_id: str, cfg: DatasetConfig,
            seeds: SeedTree, store: ArtifactStore) -> dict[str, str]: ...
    # returns ids: obs_train, obs_dev, obs_test, sidecar_dev, sidecar_test, history_index
```

## Logic requirements

- **Sampling:** vectorised over trajectories. Use the inverse-CDF method on cumulative rows, with `rng.random`.
- **Seeds:**
  - split seeds come from `seeds.generator("data", split, world, condition, replicate)`;
  - the **test** split and the panels use a seed that does **not** depend on the replicate, so all replicates of a process share the same test histories;
  - the train and dev splits change per replicate.
- **Sequence ids:** globally unique per process. Encode `(process_hash, split, index)` into an int64 by a documented rule.
- **Sidecar:** `EvalSidecar` is written for dev and test only. Train latents are **never persisted**.
- **Learner access:** `PublicTokenDataset` accepts only `ObservationSet`. Its constructor raises `LEAKAGE` if it is given any other artifact type.

## Invariants and errors

| Condition | Error |
|---|---|
| overlapping `sequence_id` between splits | `SPLIT_OVERLAP` |
| tokens ≥ V, or states ≥ N | `ALIGNMENT_ERROR` |
| first-token frequencies differ from πE (χ², p < 1e-4) | `NUMERICAL_FAILURE` (detail: `sampler_bias`) |
| panels not disjoint, or not 512 distinct trajectories each | `ALIGNMENT_ERROR` |
| any latent field present in `ObservationSet` | `LEAKAGE` |

Identical token windows across splits can occur by chance and are **not** an error.

## Dependencies and forbidden information

`contracts` and torch (for the Dataset class only). Reads `TransitionSpec` and `EmissionSpec` through the store, as consumer `dataset`. Must not read checkpoints, the oracle, or results. Panel selection may not use latent information.

## Done when

The TEST_PLAN passes, and the README documents the seed scheme and the sequence-id rule.

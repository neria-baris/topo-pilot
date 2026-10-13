# SPEC: `prediction` (waves W2, W4, W5)

## Purpose

Predictive evaluation. It has no PH and does not touch the model.

| Part | Wave | Contents |
|---|---|---|
| (a) | W2 | n-gram baselines |
| (b) | W4 | NLL, regret, context gain, and the learning gate |
| (c) | W5 | ridge probes |

## Public API

```python
class NGramBaseline:                      # (a), fit on train tokens ONLY
    def __init__(self, order: int, smoothing: Literal["additive", "kneser_ney"], alpha: float | None = None): ...
    def fit(self, train: ObservationSet) -> "NGramBaseline": ...
    def select_smoothing(self, dev: ObservationSet, grid: Sequence[float]) -> float: ...  # min dev CE
    def predict(self, histories: np.ndarray) -> np.ndarray: ...   # [M, p] tokens -> [M, V]

class PredictiveMetrics:                  # (b) pure functions on aligned arrays
    @staticmethod
    def nll(probs: np.ndarray, targets: np.ndarray) -> np.ndarray: ...          # per row, nats
    @staticmethod
    def kl(p: np.ndarray, q: np.ndarray) -> np.ndarray: ...                     # rowwise KL(p||q), nats
    @staticmethod
    def regret(q_oracle, p_model) -> float: ...                                  # mean KL(q_C || p_model)
    @staticmethod
    def captured(regret: float, G_C: float) -> float: ...                       # 1 - regret/G_C
    @staticmethod
    def bootstrap_ci(values: np.ndarray, groups: np.ndarray, n: int, rng) -> tuple[float, float]: ...
    # resample whole trajectories (groups), never tokens

class LearningGate:
    def __init__(self, threshold: float = 0.8): ...
    def evaluate(self, captured: float) -> GateCheck: ...

class RidgeProbe:                         # (c) S7 only
    def __init__(self, lambdas: Sequence[float]): ...
    def fit(self, X_fit, Y_fit, X_val, Y_val) -> "RidgeProbe": ...  # affine, lambda chosen on val
    def score(self, X, Y) -> dict[str, float]: ...                  # MSE, R^2 (no KL on raw ridge output)

class PredictionStage:  # I/O, consumer "prediction"
    def run_baselines(self, obs_train_id, obs_dev_id, obs_test_id, history_index_id, store) -> list[str]: ...
    def run_metrics(self, activation_set_id, oracle_id, store) -> str: ...    # MetricRecords
    def run_probes(self, activation_set_ids, oracle_id, split_spec, store) -> str: ...
    # D-047: stays a NotImplementedError stub; the S7 probe I/O (dev panels, dev beliefs from the
    # oracle kernels, RidgeProbe per target) lives in experiment, see experiment/SPEC.md Stage S7
```

## Logic requirements

- **Units:** all metrics in nats.
- **Joins:** by `history_id` only, one-to-one.
- **Primary position:** the primary metrics are at p = 32. Per-position curves are secondary and use the oracle's CE over all positions.
- **Regret** is computed exactly from the oracle and model distributions. It is not the difference of two sampled NLLs. The empirical NLL difference may be negative, which is not an error.
- **Probes:**
  - fit on dev panels, choose λ on a held-out dev part, and evaluate once on test;
  - controls: shuffled labels, the r_w target, and an F1-decoding baseline;
  - probe accuracy on z is never claimed to exceed the oracle MAP.

## Invariants and errors

| Condition | Error |
|---|---|
| join cardinality mismatch | `JOIN_CARDINALITY` |
| probabilities not normalised (> 1e-6) | `NUMERICAL_FAILURE` |
| a probe fit touches test | `LEAKAGE` (detail: `probe_split`) |

`G_C ≤ 1e-6` gives status `INCONCLUSIVE` for the gate, not an exception.

## Dependencies and forbidden information

`contracts` only, reading artifacts through the store. May read `EvalSidecar` for secondary probe targets only, labelled as such.

## Done when

The TEST_PLAN passes.

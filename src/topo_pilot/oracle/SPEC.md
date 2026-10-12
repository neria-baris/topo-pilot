# SPEC: `oracle` (wave W2, critical, independent tests)

## Purpose

Exact Bayesian quantities **given the true process parameters and the visible tokens only**:
- filtered beliefs;
- next-symbol and two-symbol futures;
- the last-symbol posterior;
- context gain;
- observability.

The oracle never receives latent states.

## Public API

```python
class BayesFilter:
    def __init__(self, T: np.ndarray, E: np.ndarray, pi: np.ndarray): ...   # float64 copies
    def run(self, tokens: np.ndarray) -> FilterResult: ...
    """tokens [R, P] (P ≤ 33). Returns b [R, P, N] (posterior after w_t), q [R, P+1, V]
       (q[:,0] = pi E; q[:,t] = b_t T E), log_evidence [R], ce [R, P] = -log q_{t-1}[w_t]."""
    def belief_at(self, tokens: np.ndarray, p: int) -> np.ndarray: ...       # b_p [R, N]

class LastSymbolPosterior:
    def __init__(self, T, E, pi): ...
    def r(self, w: np.ndarray) -> np.ndarray: ...        # [R,N] = pi*E[:,w]/(pi E[:,w])
    def q_last(self, w: np.ndarray) -> np.ndarray: ...   # [R,V] = r T E

class FutureOperator:
    def __init__(self, T, E): ...
    def F1(self, b: np.ndarray) -> np.ndarray: ...       # [R,V]
    def F2(self, b: np.ndarray) -> np.ndarray: ...       # [R,V,V]; F2[i,j] = b T diag(E[:,i]) T E[:,j]
    def observability_singular_values(self, k_max: int = 3) -> list[np.ndarray]: ...

def context_gain(q_C: np.ndarray, q_last: np.ndarray) -> float: ...   # mean KL(q_C || q_last), nats

class OracleStage:   # I/O, consumer "oracle"
    def run(self, transition_id, emission_id, obs_test_id, history_index_id, store) -> dict[str, str]: ...
    # writes OracleOutputs (panels: b32, b1, q, q_last, F2, entropies, log_evidence; all test: ce per position)
    #        and ProcessDiagnostics (G_C, mean_H_b1, O singular values)
```

## Logic requirements

- **Filter:** the scaled forward filter of RESEARCH_SUMMARY §5, using row vectors and float64. Normalise at every step. Accumulate the log normalisers into `log_evidence`.
- **Impossible histories:** if a normaliser is 0 (an impossible history), raise `IMPOSSIBLE_HISTORY`. Never add an epsilon.
- **Reset per window:** every window starts from π. There is no state carried between trajectories.
- **Literature mapping:** the README must state that Shai et al.'s η equals our a_{p+1} = b_p T, with T^{(x)} = diag(E[:,x]) T.
- **F2:** compute F2 with einsum. Its row sums over j must reproduce F1 to within 1e-12.
- **Observability:** O_k stacks the maps b ↦ (all length-j future probabilities) for j ≤ k, built recursively from G_1 = T E. Report the singular values; do not threshold them.

## Invariants and errors

| Condition | Error |
|---|---|
| a belief or prediction row does not sum to 1 ± 1e-10 | `NUMERICAL_FAILURE` |
| evidence equals 0 | `IMPOSSIBLE_HISTORY` |
| P > 33, or the tokens' V differs from E's | `ALIGNMENT_ERROR` |

## Dependencies and forbidden information

`contracts` only, reading TransitionSpec, EmissionSpec, ObservationSet(test), and HistoryIndex. **Must not** load `EvalSidecar`, checkpoints, or activations. This is enforced by the policy: its consumer name has no sidecar access.

## Done when

The TEST_PLAN passes, including brute-force enumeration. The README contains the derivation of q_t and F2 and the literature mapping.

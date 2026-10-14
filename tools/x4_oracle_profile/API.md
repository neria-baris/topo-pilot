# x4_oracle_profile: written contract and API (job 0014)

Status: CONTRACT FOR INDEPENDENT TESTS. Written before any production implementation exists.
Production module: `tools/x4_oracle_profile/oracle_profile.py` (pure kernels, numpy only).
Independent tests/reference: `tests/oracle_profile/` (separate author; must not read production code).

## 1. Hidden Markov model conventions

- States `z in {0..S-1}`, symbols `w in {0..V-1}`.
- `T: [S, S] float64`, row-stochastic, `T[i, j] = P(z_next = j | z = i)`.
- `E: [S, V] float64`, row-stochastic, `E[i, w] = P(w | z = i)`.
- `pi: [S] float64`, stationary (`pi @ T == pi`), nonnegative, sums to 1.
- A history is a row of observed symbols `w_1 .. w_L` (L = 32 in the study). The generative law of a
  window of K consecutive observations is: `z_1 ~ pi`, emit `w_1 ~ E[z_1]`, then for each later step
  transition `z_{t+1} ~ T[z_t]` and emit. Exactly one emission per state; transitions only BETWEEN
  emissions; no transition after the last emission.
- Suffix posterior for suffix length K over a row of length L: the filtering distribution of the
  state at the LAST observation given ONLY the final K observations `w_{L-K+1} .. w_L`, with the
  window's first state drawn from the stationary `pi` (restart at the suffix boundary; earlier
  observations are ignored entirely):
  `post_K = P(z_L | w_{L-K+1:L})`, a length-S probability vector.
- Circular features: `c: [S, 2]`, `c[s] = (cos(2*pi*x_s/12), sin(2*pi*x_s/12))`, where `x_s` is the
  first world coordinate (`coords[s, 0]`, an integer 0..11). Posterior circular mean
  `m_K = post_K @ c` (length 2).
- Symbol permutation: stored histories are CANONICAL tokens. For a model's named emission matrix
  `E_named` and permutation `symbol_perm` (a permutation of 0..V-1), the canonical emission matrix is
  `E_canon = E_named[:, symbol_perm]` and named observations are `symbol_perm[canonical_tokens]`.
  Filtering canonical tokens with `E_canon` equals filtering named tokens with `E_named`.

## 2. Production API (`oracle_profile.py`)

All functions are pure (no I/O, no randomness except an injected `np.random.Generator`).

```python
class ProfileError(RuntimeError): ...   # every validation failure raises this

def circle_features(coords: NDArray) -> NDArray[np.float64]
    # coords [S, >=1]; uses coords[:, 0]; requires integer-valued finite entries in 0..11.
    # returns [S, 2] = (cos(2*pi*x/12), sin(2*pi*x/12)).

def canonical_emission(E_named: NDArray, symbol_perm: NDArray) -> NDArray[np.float64]
    # E_named[:, symbol_perm]; ProfileError unless symbol_perm is an integer permutation of 0..V-1.

def validate_process(T, E, pi, tol: float = 1e-12) -> dict
    # ProfileError unless: shapes consistent ([S,S], [S,V], [S]); all finite; all entries >= 0;
    # |row sums of T - 1| <= tol; |row sums of E - 1| <= tol; |sum(pi) - 1| <= tol;
    # max|pi @ T - pi| <= tol. Returns a dict of the observed maxima (floats) with keys
    # "T_row_sum_max_abs_err", "E_row_sum_max_abs_err", "pi_sum_abs_err", "stationarity_max_abs_err".

def suffix_posterior(T, E, pi, tokens: NDArray, K: int) -> NDArray[np.float64]
    # tokens: [n, L] integer dtype (signed or unsigned), every entry in 0..V-1, n >= 1, L >= 1.
    # K: Python int (or numpy integer), 1 <= K <= L.
    # Returns [n, S]: row r is post_K for tokens[r, L-K:], as defined in section 1.
    # Normalised per row (sum 1 within 1e-12). ProfileError for: non-2-D or empty tokens,
    # non-integer dtype, any token < 0 or >= V, K outside 1..L or bool K, and any row whose
    # suffix has zero probability under the model ("impossible history").
    # Must not mutate its inputs.

def posterior_means(T, E, pi, tokens, Ks: Sequence[int], features) -> dict[int, NDArray]
    # {K: suffix_posterior(T, E, pi, tokens, K) @ features} for each K in Ks; each [n, 2].

def residual_rows(means: dict[int, NDArray], full: int = 32) -> dict
    # r_K = means[full] - means[K] per row ([n, 2]) for every K in means;
    # returns {"r": {K: [n,2]}, "norm": {K: [n]}, "sq": {K: [n]}} with norm = ||r_K||_2 per row
    # and sq = sum(r_K * r_K) per row. ProfileError if full not in means or shapes differ.

def profile_point(norm: dict[int, NDArray], sq: dict[int, NDArray]) -> dict
    # {"B": {K: mean(norm[K])}, "V": {K: mean(sq[K])}} as Python floats.

def bootstrap_profile(norm, sq, Ks: Sequence[int], rng: np.random.Generator, draws: int) -> dict
    # Whole-row (trajectory) bootstrap within one split. Exactly this sampling order:
    #   for d in range(draws): idx = rng.integers(0, n, size=n)   # one call per draw
    #       B[d, k] = mean(norm[Ks[k]][idx]); V[d, k] = mean(sq[Ks[k]][idx])
    # The SAME idx is used for every K and for both B and V in a draw.
    # Returns {"B": [draws, len(Ks)] float64, "V": [draws, len(Ks)] float64}.
    # ProfileError if draws < 1, lengths differ across K, or n < 2.

def percentile_interval(samples: NDArray, probs: Sequence[float]) -> NDArray
    # np.quantile(samples, probs, axis=0, method="inverted_cdf").
```

## 3. Independent reference (to be written by the independent author, `tests/oracle_profile/`)

Required file `tests/oracle_profile/independent_reference.py` (pure Python + `decimal` +
`fractions` + `itertools`; numpy only for converting inputs/outputs; it must NOT call or copy the
production recurrence, and must not import anything from `tools/` or `topo_pilot`):

```python
def decimal_suffix_posterior(T, E, pi, suffix, digits: int = 60) -> list[Decimal]
    # Unnormalised forward SUMMATION in decimal arithmetic with context precision >= digits:
    # alpha_1(i) = pi(i) E(i, w_1); alpha_{t+1}(j) = sum_i alpha_t(i) T(i, j) E(j, w_{t+1});
    # posterior = alpha_K / sum(alpha_K). Inputs converted with Decimal(float) exactly.
    # Raises ValueError for an impossible suffix (zero total).

def decimal_circular_mean(posterior: Sequence[Decimal], features) -> tuple[Decimal, Decimal]
    # sum_s posterior[s] * features[s] using Decimal(float(feature)) exactly.

def enumerate_posterior(T, E, pi, suffix) -> list[Fraction]
    # Exhaustive sum over ALL state paths of length K (itertools.product) with exact
    # fractions.Fraction arithmetic (inputs given as Fractions or floats converted exactly):
    # P(z_K = s, w_1..w_K) = sum over paths ending in s of pi(z_1) E(z_1,w_1) prod T E.
    # Only for tiny S and K. Raises ValueError for an impossible suffix.
```

## 4. What the independent tests must cover (minimum)

1. A small ASYMMETRIC HMM (e.g. S=3 or 4, V=3), with nonuniform stationary pi (derived exactly, e.g.
   by solving with Fractions, then converted), non-symmetric T, nontrivial E including at least one
   zero entry so some tokens are impossible from some states. Exhaustively enumerate all observation
   strings for small L (e.g. L <= 4) and every K in 1..L: production `suffix_posterior` must match
   `enumerate_posterior` within 1e-12, and `decimal_suffix_posterior` must match
   `enumerate_posterior` within 1e-15.
2. Suffix boundary: tokens before the suffix must have NO effect (change them; posterior unchanged),
   and the restart must use pi (not the filtered belief from earlier tokens).
3. Indexing / orientation traps: production must DISAGREE with deliberately wrong variants that the
   test file itself defines (not production code): (a) transposed T, (b) emission indexed by the
   wrong permutation (canonical tokens with E_named), (c) an extra transition after the last
   emission, (d) the prefix instead of the suffix. Assert the trap differs from enumeration by more
   than 1e-6 on at least one constructed case while production matches.
4. Permutation: `canonical_emission` + canonical tokens equals `E_named` + named tokens
   (`symbol_perm[canonical]`) to 1e-12; non-permutations raise ProfileError.
5. Normalisation: every returned row sums to 1 within 1e-12 and is nonnegative.
6. Impossible histories and invalid inputs raise ProfileError (impossible suffix, token out of range,
   negative token, float dtype, K = 0, K = L + 1, bool K, 1-D tokens, empty tokens).
7. `validate_process`: accepts a valid HMM; rejects non-stationary pi, a non-stochastic row, a
   negative entry, NaN, inconsistent shapes; returned maxima are correct on a known case.
8. `circle_features`: known answers for x = 0, 3, 6, 9; rejects non-integer or out-of-range x.
9. `residual_rows`, `profile_point`: hand-computed known-answer case; r for K = full is exactly zero;
   B_K <= sqrt(V_K) on any input (Jensen) up to 1e-15.
10. `bootstrap_profile`: reproduces a manual re-implementation of the documented sampling order with
    an identically seeded `np.random.Generator(np.random.PCG64(seed))`; same idx used across K and
    for B and V (check via a constructed case where norm differs by K); shapes; error paths.
11. `percentile_interval` equals `np.quantile(..., method="inverted_cdf")`.
12. Decimal reference self-checks: matches enumeration; precision context >= 60 digits honoured.

Tests import production as a plain module from `tools/x4_oracle_profile/` by inserting that
directory into `sys.path` (pytest runs with `--import-mode=importlib`), and import the reference the
same way from `tests/oracle_profile/`. Every test file starts with `pytestmark = pytest.mark.oracle`.
No randomness except explicitly seeded `np.random.Generator(np.random.PCG64(seed))` in tests. No
sampled synthetic histories are needed: use exhaustive enumeration of observation strings.
Tests never read real artifacts, stores or histories. Suite must run in well under 60 CPU seconds.

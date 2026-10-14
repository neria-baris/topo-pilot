# x4_circle_history: test plan (job 0016)

These tests are synthetic only. Fixtures are explicit finite examples or deterministic geometric
arrays. Never use real artifacts, scored data, sampled scientific histories or model loading.
Tests are written from CONTRACT.json, API.md and ERROR_BOUND.md, and each author must not read
the production `.py` files.

Exact certificates are verified with EXPLICIT equations (triangle sums, congruences, Fractions,
hand-computed values). Never use production solver or matrix helpers, and never rely on success
flags.

Execution: the conductor runs every test through the job meter. Authors do not execute anything.

## Author A (independent): `tests/circle_history/test_cochain.py`, `test_chart.py`

- **A1.** edge_list and triangle_system on hand graphs: the exact edge and triangle lists, and
  D1 rows (+1 on (j,k), −1 on (i,k), +1 on (i,j)) checked against explicit sums.
- **A2.** integer_lift on hand complexes:
  - an already-closed cocycle returns kind centered_exact;
  - a modular cocycle with nonzero integer defect (a multiple of 47) is lifted. Verify closure,
    congruence and D1 z = b with explicit triangle sums. Production helpers may only produce the
    result, never check it.
- **A3.** A cochain that is not closed mod 47 raises Invalid. check_closure raises on a
  modular-but-not-integral cochain, and check_congruence raises on a non-congruent pair.
- **A4.** The local L1 passes on a hand case match a hand-computed final z, with strict
  decrease and lexicographic tie-breaking. They change only vertices < min(128, n).
- **A5.** Exhaustion paths, using an injected fake clock:
  - the CPU cap exceeded before the first bound raises Unresolved;
  - an unsatisfiable system within all bounds raises Unresolved, not Invalid.
- **A6.** primitive_class cases:
  - a cycle graph with a known period gives the expected g, beta and q, and g·beta + δq ==
    alpha;
  - zero periods (exact) raise Unresolved;
  - g divisible by 47 raises Unresolved;
  - a disconnected graph raises Unresolved;
  - BFS order follows ascending neighbour ids from root 0.
- **A7.** smooth_phase on cycle and path graphs gives the known least-squares solution with
  f[0] = 0, phases in [0, 2π), and the residual check. A forced bad input raises Invalid if one
  can be constructed; otherwise document why not.
- **A8.** select_h1_bar ties (birth, then death, then index), infinite and zero bars excluded,
  and none available raises Unresolved. cocycle_to_edges handles orientation sign, centring at
  p//2 and edges not in the list.
- **A9.** fit_chart on deterministic circle-like clouds (for example 40–80 points on a circle
  embedded in a few dimensions, with fixed small deterministic offsets). Check:
  - the chart exists;
  - phi is ascending around the circle up to reflection;
  - d8, sigma and support_radius are recomputed independently, with the 8th neighbour excluding
    self only and a duplicate landmark counting at distance 0;
  - unsorted or duplicate landmark ids raise Invalid;
  - n < 9 raises Invalid;
  - a zero bandwidth raises Unresolved.
- **A10.** fit_gauge sign selection, an exact tie choosing +1, shift removal, alignment 0
  raising Unresolved and nonfinite input raising Invalid. Gauge isolation: changing validation
  arrays cannot change the chart or the gauge.
- **A11.** extend:
  - stable nearest ties by landmark index;
  - the weighted mean formula;
  - an exact duplicate averaging ALL exact matches, and conflicting duplicates raising Invalid;
  - support boundaries |z| = 0.2 (supported) and eighth distance = R (supported) versus just
    outside them;
  - far queries unsupported;
  - extend never mutates chart or gauge;
  - extended phases of held-out circle points agree with the direct construction (agreement
    ≥ 0.99 on a clean synthetic circle).
- **A12.** agreement, phase_bin_counts and overall_resultant known answers. chart_gates
  boundaries: A = 0.8 passes; a bin with exactly 8 passes and 7 does not; resultant 0.30
  passes. Not met gives INCONCLUSIVE with criterion_met False. Also check the "overall" order.
- **A13.** chart_to_arrays and chart_from_arrays round trip exactly.

## Author B (independent): `tests/circle_history/test_scores_precision.py`, `test_error_bound.py`, `test_adapter.py`

- **B1.** canonical_from_named: inverse permutation, invalid permutations, and the named
  round-trip check. history_digests known values, and a shape other than [n, 32] rejected.
- **B2.** oracle_moments rejects 33 columns (w33) and any width other than 32. Its values equal
  `oracle_profile.posterior_means(K=(1,4,32))` on a tiny HMM.
- **B3. Suffix-only zero identity.** Use a tiny asymmetric stationary HMM with exact Fraction π.
  Exhaustively enumerate every history of length L (≥ 5) with suffix length k (≥ 2). Show
  E[g(suffix)·(m_L − m_k)] = 0 EXACTLY (Fractions) for arbitrary suffix functions g, including
  the three control constructions. Production float controls on the same enumeration give
  ≈ 0 within 1e-12.
- **B4.** control_vectors: an exact zero vector gives (1, 0); otherwise the unit norm. A known
  sha256_phase value (hand-derived from hashlib in the test). angular_instability boundaries.
- **B5. Precision.**
  - sd_b4_draws and centered_draws reproduce a manual loop with identically seeded
    Generator(PCG64(seed)), with ONE idx per draw shared by all models (a constructed case
    proves the sharing);
  - mde formula via statistics.NormalDist;
  - inverted_cdf quantiles;
  - decision boundaries: mde_upper = .02 with power = .80 is PASS; just over is INCONCLUSIVE;
    a B4 lower bound of exactly .01 is not PASS;
  - nonfinite input raises Invalid.
- **B6. Error bound.**
  - decimal_cos_sin against exactly known values: x = 0, and the cos²+sin² identity to 1e-70.
    Compare with independently computed rational or Decimal references at chosen binary
    floats. eps_v ≥ the actual error. A range violation raises Invalid.
  - exact_features values.
  - trapping_context raises on a constructed underflow.
  - posterior_envelope and moment_envelope match the ERROR_BOUND.md formulas evaluated
    independently.
  - certify_rows on a tiny HMM:
    - the exact float pipeline output is CERTIFIED;
    - x_hat shifted by 2e-4 is INCONCLUSIVE;
    - m_hat shifted by 1e-9 is FAIL_TECHNICAL;
    - split "scoring" without a release raises AccessDenied even when the other inputs are
      invalid, which proves no computation runs first;
    - "scoring" with a release token runs.
- **B6b. Spec v2.1 additions:**
  - reference_check_rows passes on exact pipeline moments and FAILs on a 1e-9 shift;
  - the exact-rational R in row_bound equals an independently assembled Fraction;
  - TAYLOR_N == 48, and the exact tail and ratio inequalities hold, recomputed in the test with
    Fractions;
  - certify_rows gives FAIL_TECHNICAL for phi = 2*np.pi (operational range) even though it lies
    inside the analytic interval;
  - the K1 four-lowest references are invoked through reference_check_rows with Ks = (1, 4, 32).
- **B7. Adapter.** Build synthetic ObservationSet, HistoryIndex and ActivationSet artifacts in
  `topo_pilot.contracts.testing.memory_store()`, with tiny sizes (for example panel_size 4,
  n_panels 3). Use `contracts` public classes and `store.save` (read src/topo_pilot/contracts
  SPEC/README for signatures). Check:
  - lineage passes;
  - a wrong parent, split, end, hook, history-id order or tokens_hash raises JoinError;
  - panels(1, 2) returns rows in history-id order without column 32;
  - panel 3 raises AccessDenied BEFORE any store.load (assert with a store wrapper that counts
    loads);
  - identity_report returns no arrays;
  - cross_model_join orders rows by sequence_id, and differing sequence sets or digests raise
    JoinError.

## Spec v2.2 additions (both authors; see API.md "Spec v2.2 clarifications")

- **A14 (author A).** integer_lift with an injected fake clock covers four points:
  - over the cap before the first call raises Unresolved;
  - a clock that jumps past the cap DURING a solver call raises Unresolved even though the solve
    succeeds;
  - a cap reached during the local passes raises Unresolved;
  - `cochain.HIGHS_PINNED` equals {"threads": 1, "parallel": False}.

  No 30-second real-time tests.
- **A15 (author A).** extend on a far query whose raw weights would all underflow: the result
  is finite and equals the exactly normalised weights computed independently in the test by
  log-sum-exp. It is unsupported by the radius rule. No floor-based value.
- **B8 (author B).** control_vectors and angular_instability on tiny normal and subnormal
  nonzero vectors and on an exact zero. Invalid for a non-finite input or a bad bound.
- **B9 (author B).** precision_summary and b4_summary raise Invalid for empty models, duplicate
  models, wrong draw shapes, non-finite draws and mismatched point keys.

## Spec v2.3 additions (author B; see API.md "Spec v2.3 clarifications")

- **B10.**
  - Scoring positive cases use a synthetic `errors.ScoringAuthority(owner_record_path="x",
    owner_record_sha256="0"*64, scope=("scoring",), release_job_id="0099")`.
  - Negative cases raise AccessDenied before any computation or load, for each of: None, False,
    True, {}, "token", object(), a ScoringAuthority with scope ("feasibility",), and one with a
    short sha.
  - Cover certify_rows, reference_check_rows, and RestrictedE4Adapter.panels with panel 3 (zero
    loads).

## Spec v2.4 additions (see API.md "Spec v2.4 clarifications" and ERROR_BOUND.md v2.2 sections 8-9)

Earlier test files and their revisions are preserved in git; new cases go into new files where
practical. Nothing deliberately takes 180 s or 30 s of real time: clocks and operation markers
are injected.

- **A16 (author A; integer_lift timer).** With an injected clock (an iterator of values):
  - the already-closed branch (zero defect) whose clock advances past lift_cpu_cap_s between
    entry and return raises Unresolved, although the returned lift would be exact;
  - the same branch with the clock below the cap returns the exact lift;
  - the corrected branch whose clock passes the cap only during the final exact checks raises
    Unresolved;
  - the FIRST clock call happens before any defect is formed (e.g. a clock that raises a marker
    exception on its first call propagates that exception for an input whose D1·a would also
    be malformed).
- **A17 (author A; fit_chart timed hook).** A recording timed sees exactly the labels
  "distance", "ph", "edges", "two_skeleton", "integer_lift", "primitive", "smoothing" in that
  order, and the chart equals the one with timed=None. A timed that raises Unresolved at
  "two_skeleton" propagates Unresolved and never sees a later label. extend with a recording
  timed sees "extension_distance".
- **B11 (author B; reference binding and exact gaps).**
  - process_digest changes when any of T, E, pi, coords changes by one ulp or a shape changes;
    an integer coords array and the equal float64 array give the SAME digest (inputs are
    converted to float64 first).
  - Cache-binding mutation: a cache filled under process P1 and then used with P2 (one E entry
    changed) produces no hit (the P2 result equals a fresh P2 computation).
  - Malformed-history collision: histories [.., 260, ..] (int64) and [.., 4, ..], float-dtype
    histories, bool histories, negative values and values ≥ V raise Invalid before any
    reference work; no two distinct valid histories share a key.
  - Exact-gap counterexample: an m_hat whose exact gap is Fraction(1, 10**10) passes; an m_hat
    whose exact gap is slightly above Fraction(1, 10**10) while float(gap) == 1e-10 fails
    (construct m_hat and M_ref as exact rationals around a float boundary).
  - cache_only=True with an empty cache raises Invalid("reference cache miss") and calls no
    reference (e.g. a T whose reference would itself trap shows the miss error, not the trap).
- **B12 (author B; reference_cache.py).** export_cache/load_cache round trip is exact (Decimal
  strings equal, no float). load_cache raises Invalid for: a schema change, any identity field
  change, an entry with another process_digest, a duplicate key, "NaN"/"Infinity"/garbage mx.
  verify_rows raises Invalid for a reordered history_id, one changed sequence_id, a changed
  panel, a changed history byte, a missing (model, split) record and a missing K entry; it
  passes on the exact table.
- **B13 (author B; process_law thresholds and grid law).**
  - threshold_law on hand-made rows with 2^-53-grid arithmetic: a monotone row ending at 1; a
    row whose raw cumsum exceeds 1 BEFORE the last positive entry (e.g. p = [0.5, 0.5 + 2^-52,
    0, 1e-17] style rows written as exact floats) where the clamped thresholds keep the law
    identical to direct counting; a hand-made non-monotone threshold row (not producible
    by the sampler, which is monotone after clamping) where q equals the comparison-count law
    derived in the test from the sorted thresholds and "monotone" is False; a negative
    threshold clamps to 0.
  - row_tv: "documented" is None for a non-monotone row and ≥ "grid" for a monotone one.
- **B14 (author B; process_law softmax and law).**
  - lattice_states rejects a permuted coords array, a non-integer coordinate and S != 144.
  - documented_transition: degree 3 on y = 0 and y = 11, degree 4 elsewhere, x wraps, y does
    not; ideal_identities passes on it and fails on a perturbed copy.
  - softmax_enclosure: logits are exact (d² for state (0, 0) and centre (1/2, 1/2) is 1/2,
    logit −4/25); for a few entries the exact interval contains an independent 80-digit test
    computation; lo < 1 < hi and hi − lo is below 1e-55.
  - process_law_bound on the exact documented law rounded to float64 (built in the test from
    the written equations, numpy float softmax) gives BOUNDED with 0 < kappa < 1e-12 and a
    finite Z_bound below 1e-9; with one T̂ zero-support change, a zero Ê entry, a permuted coords
    array, or kappa forced ≥ 1 it gives UNAVAILABLE with a reason naming the condition.
- **B15 (author B; controls).** control_scores equals u_c·(m32 − m4) per row for hand-made
  rows, including an exact (0, 0) m1 row mapped to (1, 0). control_summary reproduces, for a
  tiny n and draws, the means over indices from ONE rng.integers(0, n, size=n) call per draw
  shared by all controls and models (recomputed in the test with Generator(PCG64(seed))); the
  quantiles use inverted_cdf at .025, .975, .05/3 and 1 − .05/3; Invalid for non-finite values,
  unequal lengths, n < 2, duplicate or empty models and unknown control names.
- **B16 (author B; taxonomy).** The adapter's lineage and join failures raise JoinError (as
  before); the API text that JoinError is a technical defect is checked by asserting
  issubclass relations are unchanged and that no adapter failure raises Unresolved.

### Builder tests (v2.4)

- runner._run_gate records FAIL_TECHNICAL for Invalid and JoinError and INCONCLUSIVE for
  Unresolved; the e2e join mismatch now ends overall FAIL.
- stage_records: an out-of-order oracle/charts/precision call refuses with no gate record; a
  second call of a STARTED stage refuses (also after a simulated kill: STARTED without
  COMPLETED); an evidence hash change refuses with integrity true and export reports FAIL;
  export runs after a non-PASS.
- persisted reference: charts reloads the cache without recomputation (a counting stub shows no
  reference call), refuses a modified cache file, a modified ORACLE.json hash, a different
  process and a row-table mismatch; saved oracle IDs that differ from reloaded rows fail
  FAIL_TECHNICAL before any chart work.
- op_guard: marker and OPERATIONS.jsonl events for start/end/error; the post-return check with
  an injected clock raises Unresolved; the meter_bind limiter with a marker whose started_epoch
  is older than deadline_s returns the native-operation kill reason; one short real metered
  child (deadline 1 s, a marked sleep of a few seconds) is KILLED with that reason and its
  stale marker is archived as KILLED_<seq>.json by the next meter_bind call.
- integer_lift and fit_chart wiring from the runner: ctx.timed is used for every labelled
  operation.
- allocation: meter_bind syncs a ledger with the previous caps to the CONTRACT caps, keeps every
  entry byte-identical and records allocation_history; a ledger with unknown caps refuses.
- manifests: frozen_files contains src/topo_pilot/__init__.py, every contracts file and
  dataset/sampler.py; a changed contracts file or an extra one is refused before store access;
  an unfrozen project module loaded is refused.
- numerical identity: the probe record has the documented keys and is deterministic across two
  calls in one process; a changed package file digest (simulated record) is refused.
- precision: PRECISION.json is written after a B4 stop and contains controls, instability counts
  and Z_bound; a sequence_id or digest mismatch across models fails FAIL_TECHNICAL before any
  bootstrap.

## Builder tests (implementer; labelled non-independent): `tests/circle_history/test_builder_*.py`

- meter_bind: job and task binding, stage ceilings, and that the export cap of 80 s is
  enforced.
- release verification: a missing or mismatching release refuses.
- runner: refuses every scientific stage without a release, and imports have no side effects.
- A static scored-access audit (AST scan): panels 3–8 are reachable only through the
  release-gated branch.
- Cost probe: the job-0014 Decimal reference per-step time at S = 144 on a synthetic dense
  process, projected to 1024 histories × 36 steps.

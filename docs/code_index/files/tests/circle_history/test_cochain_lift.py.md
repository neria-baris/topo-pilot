# `tests/circle_history/test_cochain_lift.py`

- Source: [tests/circle_history/test_cochain_lift.py](../../../../../tests/circle_history/test_cochain_lift.py)
- Kind: python
- Lines: 329

## Module docstring

> Independent synthetic tests, author A (spec v2.3): cochain.integer_lift
> (TEST_PLAN A2, A3 lift part, A4, A5, A14).

## Imports

### Internal (repo files)

- `import cochain` -> [tools/x4_circle_history/cochain.py](../../tools/x4_circle_history/cochain.py.md) (line 35, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 36, via sys.path edit)

### External (third-party)

- `numpy` (lines 26)
- `pytest` (lines 27)
- `scipy` (lines 28)

### Standard library

- `__future__` (lines 20)
- `json` (lines 22)
- `pathlib` (lines 24)
- `sys` (lines 23)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 33: `str(PKG)` -> `tools/x4_circle_history`

## Imported by

- none

## Top-level constants

- `A_K4`
- `CHART_KEYS`
- `EXACT_K4`
- `G_K4`
- `K4_EDGES`
- `K4_SHIFT_EDGES`
- `K4_SHIFT_TRIS`
- `K4_TRIS`
- `P`
- `PKG`
- `REPO_ROOT`
- `SHIFT`
- `TRI`
- `TRI_EDGES`
- `Z_STAR`

## Classes and functions

- **function `make_cfg`** [L49-54]: `def make_cfg(**overrides)`
- **function `as_int`** [L57-58]: `def as_int(values)`
- **function `edge_index`** [L61-62]: `def edge_index(edges)`
- **function `triangle_sums`** [L65-70]: `def triangle_sums(c, edges, triangles)` - Explicit c(j,k) - c(i,k) + c(i,j) for every triangle, as Python ints.
- **function `reference_d1`** [L73-83]: `def reference_d1(edges, triangles)`
- **function `coboundary`** [L86-87]: `def coboundary(f, edges)`
- **function `lift`** [L90-95]: `def lift(a, edges, triangles, n, cfg=None, **kwargs)`
- **function `certified_correction`** [L98-109]: `def certified_correction(alpha, a, edges, triangles)` - Explicit closure, congruence and D1 z = b; returns z = (a - alpha) / p.
- **class `JumpClock`** [L112-120] - 0.0 for the first `zero_calls` readings, then `late` (far beyond the 30 s cap).
- **method `JumpClock.__init__`** [L115-116]: `def __init__(self, zero_calls, late=1000.0)`
- **method `JumpClock.__call__`** [L118-120]: `def __call__(self)`
- **class `SteppingClock`** [L123-132] - Reading k (k = 0, 1, ...) returns k * step.
- **method `SteppingClock.__init__`** [L126-127]: `def __init__(self, step)`
- **method `SteppingClock.__call__`** [L129-132]: `def __call__(self)`
- **class `FirstThenClock`** [L135-141]
- **method `FirstThenClock.__init__`** [L136-137]: `def __init__(self, first, rest)`
- **method `FirstThenClock.__call__`** [L139-141]: `def __call__(self)`
- **test `test_fixture_arithmetic`** [L157-163]: `def test_fixture_arithmetic()`
- **test `test_closed_cocycle_is_centered_exact`** [L167-177]: `def test_closed_cocycle_is_centered_exact()`
- **test `test_single_triangle_centred_modular_cocycle_is_lifted`** [L180-190]: `def test_single_triangle_centred_modular_cocycle_is_lifted()`
- **test `test_wheel_disk_lift_certificate`** [L193-204]: `def test_wheel_disk_lift_certificate()`
- **test `test_not_cocycle_mod_p_is_invalid_before_any_cap`** [L208-212]: `def test_not_cocycle_mod_p_is_invalid_before_any_cap()`
- **test `test_local_passes_hand_case`** [L216-223]: `def test_local_passes_hand_case()`
- **test `test_local_passes_follow_cfg`** [L232-235]: `def test_local_passes_follow_cfg(overrides, z_final)` decorators: @pytest.mark.parametrize('overrides, z_final', [({'local_vertices': 1}, [0, 0, -2, 1, 1, 1]), ({'local_vertices': 2}, [1, 0, -2, 0, 0, 1]), ({'local_passes': 1}, [1, 0, -2, 0, 0, 1]), ({'local_passes': 0}, Z_STAR)])
- **test `test_local_passes_stop_at_vertex_128`** [L238-246]: `def test_local_passes_stop_at_vertex_128()`
- **test `test_cap_exceeded_before_first_bound`** [L251-253]: `def test_cap_exceeded_before_first_bound(step)` decorators: @pytest.mark.parametrize('step', [31.0, 30.0])
- **test `test_cap_not_reached_succeeds`** [L256-258]: `def test_cap_not_reached_succeeds()`
- **test `test_unsatisfiable_within_all_bounds_is_unresolved`** [L261-267]: `def test_unsatisfiable_within_all_bounds_is_unresolved()`
- **test `test_guard_exception_propagates`** [L270-278]: `def test_guard_exception_propagates()`
- **test `test_a14_over_cap_before_first_call`** [L282-284]: `def test_a14_over_cap_before_first_call()`
- **test `test_a14_cap_passed_during_successful_solve_is_rejected`** [L287-313]: `def test_a14_cap_passed_during_successful_solve_is_rejected()` - The B=1 solve succeeds (unique z*), but the clock is past the cap afterwards.
- **test `test_a14_cap_reached_during_local_passes`** [L316-323]: `def test_a14_cap_reached_during_local_passes()`
- **test `test_a14_highs_options_pinned`** [L326-329]: `def test_a14_highs_options_pinned()`


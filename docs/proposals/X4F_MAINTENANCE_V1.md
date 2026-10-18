# X4-F prospective maintenance contract, 17 October 2026

Identifier: `x4f-maintenance-v1`. Scope: code repair and synthetic regression verification.
This version does not release scientific execution or reopen x4f-exec-v2. The original
protocol, committed gate tables, independent tests, external store and accepted INCONCLUSIVE
verdict remain historical records. Any future study must bind this source in its own freeze.

## Reuse and changes

Reuse `RunControls` from `experiment/x5g1_controls.py` for STOP, per-run and cumulative CPU
checks, ledger validation and atomic persistence on normal exit, STOP, budget exhaustion,
exceptions and KeyboardInterrupt. CPU includes the export stage. The ledger cannot recover
cost after a hard process kill or power failure; that cost remains unknown, not zero.

Guard every random-family draw, shuffle refit, ridge fold and solver, RBF refit and damage
profile, with before/after checks around model damage evaluation. Native numerical calls
are cooperative boundaries, not preemptively interruptible. Preserve random streams,
selection order, matching window, sample counts and scientific gate thresholds.

Before accepting a random map, check finite entries, idempotence and M+E=I (relative to
map scale, 1e-10, the existing idempotence threshold), rank loss (SVD relative cutoff 1e-8),
and left/right containment of the removed
component in the retained whitening range (relative 1e-8). A defective candidate returns
ERASER_INVALID, not a replacement draw. Rank/containment checks are only required for
otherwise accepted maps, avoiding an SVD on each rejected draw.

Export the primary map, every accepted random map (including partial unmatched families),
and the five fitted frozen-control maps. Each map has `map_<name>_M`, `_mu`, `_rank`, `_status`
arrays, readable without pickle. The npz export has a SHA256 entry in run.json; run.json
is covered by MANIFEST.json. A nonempty tables or exports directory is refused before
source inputs are loaded. The cumulative ledger is append-only in meaning, atomically
replaced on disk; `ledger_before_run` is explicitly a snapshot and `ledger_path` points to
the authoritative final ledger.

## Verification and remaining scientific limitation

Implementation-author regression tests are in `tests/experiment/test_x4f_maintenance.py`
and `tests/analysis/test_x4f_family_maintenance.py`. They inject invalid projectors, STOP
within inner loops, export/runtime errors, preserve previous ledger entries, refuse old
outputs, and round-trip all map exports with checksums. The original independent tests
are unchanged. These maintenance tests are not independent scientific acceptance.

The repaired runner still does not solve control-family rarity or nonlinear recoverability.
For a successor intervention use the separately developed C2 planning track. No scientific
data or accepted experimental outcome is changed by this maintenance contract.

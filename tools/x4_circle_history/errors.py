"""Error classes for x4_circle_history (API.md, errors.py)."""

from __future__ import annotations


class Invalid(RuntimeError):
    """Numerical, integrity or implementation defect: the runner reports FAIL_TECHNICAL."""


class Unresolved(RuntimeError):
    """Valid criterion not met, unsupported, or exhausted: the runner reports INCONCLUSIVE."""


class AccessDenied(RuntimeError):
    """Access to a scored panel or scored row attempted without a scoring release."""


class JoinError(RuntimeError):
    """Mismatch in cross-model pairing or artifact lineage: stop for review."""

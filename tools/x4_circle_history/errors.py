"""Error classes for x4_circle_history (API.md, errors.py)."""

from __future__ import annotations

from dataclasses import dataclass


class Invalid(RuntimeError):
    """Numerical, integrity or implementation defect: the runner reports FAIL_TECHNICAL."""


class CacheMiss(Invalid):
    """cache_only reference lookup missed (spec v2.4): raised, never folded into a status."""


class Unresolved(RuntimeError):
    """Valid criterion not met, unsupported, or exhausted: the runner reports INCONCLUSIVE."""


class AccessDenied(RuntimeError):
    """Access to a scored panel or scored row attempted without a scoring release."""


class JoinError(RuntimeError):
    """Mismatch in cross-model pairing or artifact lineage: stop for review."""


@dataclass(frozen=True)
class ScoringAuthority:
    """Positively verified owner scoring release (issued only by release.scoring_authority).

    The fields bind the immutable owner-approval record by path and sha256, and the scope must
    contain "scoring". Static audits forbid constructing it anywhere except release.py and
    synthetic tests.
    """

    owner_record_path: str
    owner_record_sha256: str
    scope: tuple
    release_job_id: str


def require_scoring(authority) -> None:
    """AccessDenied unless ``authority`` is a ScoringAuthority whose scope includes scoring."""
    ok = (
        isinstance(authority, ScoringAuthority)
        and "scoring" in tuple(authority.scope)
        and len(str(authority.owner_record_sha256)) == 64
        and bool(authority.owner_record_path)
    )
    if not ok:
        raise AccessDenied("scored access requires a positively verified ScoringAuthority")

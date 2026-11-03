"""Implementer test: hwsu_registry._violation mirrors c2_registry._violation (design 11.2)."""

import hwsu_config as uc  # noqa: F401, I001
import u2  # noqa: F401
import c2_registry
import hwsu_registry as ureg

REC = {"history_files": [], "identity_refs": [], "observation_set_roots": [],
       "unreadable": []}
CASES = [
    ("a", {"decision": "READER", "readers": ["c"]}, None, {"class": "SCANNED"}, ["c"]),
    ("a", {"decision": "READER", "readers": ["c"]}, REC, {"class": "SCANNED"}, ["c"]),
    ("a", {"decision": "READER", "readers": ["c"]}, REC, {"class": "SCANNED"}, []),
    ("a", {"decision": "READER", "readers": ["c"]}, REC, {"class": "NOT_SCANNED"}, ["c"]),
    ("a", {"decision": "EXCLUSION"}, REC, {"class": "NOT_SCANNED", "reason": "r"}, []),
    ("a", {"decision": "EXCLUSION"}, REC, {"class": "SCANNED", "reason": "r"}, []),
    ("a", None, REC, {"class": "NOT_SCANNED", "reason": "r"}, []),
    ("a", None, dict(REC, history_files=["x"]), {"class": "NOT_SCANNED", "reason": "r"}, []),
    ("a", None, REC, {"class": "INCOMPLETE", "reason": "r"}, []),
    ("a", {"decision": "EXCLUSION"}, None, None, []),
]


def test_violation_equivalent():
    for args in CASES:
        try:
            want = c2_registry._violation(*args)
        except Exception as exc:  # noqa: BLE001
            want = type(exc)
        try:
            got = ureg._violation(*args)
        except Exception as exc:  # noqa: BLE001
            got = type(exc)
        assert got == want, args

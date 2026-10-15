"""Materialise C1'-v1 = C1-FROZEN-v1 + the 33 anchored edits of C1PRIME-DELTA-FROZEN-v1 (job 0026).

Anchors and replacement/insertion texts are read verbatim from the delta's ```text fences; the
operation of each edit is the one its heading states (OPS below). Every anchor must occur exactly
once in the base and exactly once in the text at the moment its edit is applied.

Usage: python materialise_protocol.py <planning/responses dir> <out.md>
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

BASE_SHA = "D1DF1AEF98BB55DC8A7CE66039865AAAFF339DBDA9B9017CFEB556F048BA5DBA"
DELTA_SHA = "4556EB91CF57D20BE5A5BA4D7577114FBB1BE25FE8166952CBCDA3D32DE29A58"
# operation per edit, from each "### Edit N" heading of the delta
OPS = {1: "replace", 2: "before_para", 3: "replace", 4: "replace", 5: "before_para",
       6: "replace", 7: "replace", 8: "replace", 9: "after_line", 10: "after_para",
       11: "replace", 12: "replace", 13: "range", 14: "row", 15: "row", 16: "row",
       17: "replace", 18: "replace", 19: "replace", 20: "replace", 21: "after_line",
       22: "replace", 23: "replace", 24: "after_line", 25: "replace", 26: "replace",
       27: "replace", 28: "after_line", 29: "replace", 30: "replace", 31: "replace",
       32: "before_sep", 33: "replace"}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest().upper()


def parse(delta: str) -> dict:
    body = delta.split("## Numbered exact edits against C1-FROZEN-v1", 1)[1]
    body = body.split("## §15.3 numerical certificate", 1)[0]
    edits = {}
    for m in re.finditer(r"^### Edit (\d+):.*?(?=^### Edit |\Z)", body, flags=re.M | re.S):
        fences = re.findall(r"^```text\n(.*?)\n```$", m.group(0), flags=re.M | re.S)
        edits[int(m.group(1))] = fences
    return edits


def _line_span(text: str, anchor: str) -> tuple[int, int]:
    i = text.index(anchor)
    start = text.rfind("\n", 0, i) + 1
    end = text.find("\n", i)
    return start, (len(text) if end < 0 else end)


def apply(text: str, n: int, fences: list) -> str:
    op = OPS[n]
    anchors = fences[:2] if op == "range" else fences[:1]
    for a in anchors:
        if text.count(a) != 1:
            raise SystemExit(f"edit {n}: anchor count {text.count(a)} != 1: {a[:60]!r}")
    new = fences[-1]
    a = fences[0]
    if op == "replace":
        return text.replace(a, new, 1)
    if op == "range":
        i, j = text.index(fences[0]), text.index(fences[1]) + len(fences[1])
        if not i < j:
            raise SystemExit(f"edit {n}: range anchors out of order")
        return text[:i] + new + text[j:]
    if op == "row":  # replace the whole table row (line) that begins with the anchor
        s, e = _line_span(text, a)
        if not text[s:e].startswith(a):
            raise SystemExit(f"edit {n}: anchor does not begin its line")
        return text[:s] + new + text[e:]
    if op == "after_line":
        s, e = _line_span(text, a)
        return text[:e] + "\n" + new + text[e:]
    if op == "before_para":  # new paragraph, followed by one blank line, before the anchor
        i = text.index(a)
        return text[:i] + new + "\n\n" + text[i:]
    if op == "after_para":  # new paragraph, preceded by one blank line, after the anchor
        i = text.index(a) + len(a)
        return text[:i] + "\n\n" + new + text[i:]
    if op == "before_sep":  # insertion, one blank line, a --- line, one blank line, anchor
        i = text.index(a)
        return text[:i] + new + "\n\n---\n\n" + text[i:]
    raise SystemExit(f"edit {n}: unknown op {op}")


def main(resp_dir: Path, out: Path) -> dict:
    base_b = (resp_dir / "C1-FROZEN-v1.md").read_bytes()
    delta_b = (resp_dir / "C1PRIME-DELTA-FROZEN-v1.md").read_bytes()
    if sha(base_b) != BASE_SHA or sha(delta_b) != DELTA_SHA:
        raise SystemExit("base or delta sha256 mismatch")
    base, edits = base_b.decode("utf-8"), parse(delta_b.decode("utf-8"))
    if sorted(edits) != list(range(1, 34)):
        raise SystemExit(f"expected edits 1..33, got {sorted(edits)}")
    counts = {}
    for n, f in edits.items():
        need = 3 if OPS[n] == "range" else 2
        if len(f) != need:
            raise SystemExit(f"edit {n}: {len(f)} fences, expected {need}")
        for k, a in enumerate(f[:need - 1]):
            counts[f"{n}{'ab'[k] if need == 3 else ''}"] = base.count(a)
    if any(c != 1 for c in counts.values()):
        raise SystemExit(f"base anchor counts not all 1: {counts}")
    text = base
    for n in sorted(edits):
        text = apply(text, n, edits[n])
    out.write_bytes(text.encode("utf-8"))
    return {"base_sha256": BASE_SHA, "delta_sha256": DELTA_SHA, "anchors": len(counts),
            "anchor_counts_all_1": True, "c1prime_v1_sha256": sha(text.encode("utf-8")),
            "lines": text.count("\n")}


if __name__ == "__main__":
    print(main(Path(sys.argv[1]), Path(sys.argv[2])))

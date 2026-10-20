"""Tracked-file discovery, file kinds, line counts, hashes and one-line purposes."""
import hashlib
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
# Project rule: the public research summary is for external readers only. These prefixes are
# dropped from the file list before any file is opened.
EXCLUDE = ("00_READ_ME_FIRST_Research_Summary_So_Far/", "docs/research_summary/")
OUT_DIR = "docs/code_index"
CODE_EXT = {".py": "python", ".ps1": "powershell", ".sh": "shell", ".ipynb": "notebook"}
KINDS = {
    ".md": "markdown", ".json": "json", ".yaml": "yaml", ".yml": "yaml", ".csv": "csv",
    ".tex": "latex", ".pdf": "pdf", ".png": "png", ".ttf": "font", ".npz": "npz",
    ".txt": "text", ".toml": "toml", ".lock": "lock", ".sha256": "sha256", ".pt": "torch",
    ".jpg": "jpeg", ".jpeg": "jpeg", ".gif": "gif", ".zip": "zip",
}
BINARY_EXT = {".pdf", ".png", ".ttf", ".npz", ".pt", ".jpg", ".jpeg", ".gif", ".zip"}
_FORBIDDEN_WORDS = ("READ_ME_FIRST", "research_summary/")


def clean(text):
    """Remove mentions of the forbidden paths from free text copied out of sources."""
    for word in EXCLUDE + _FORBIDDEN_WORDS:
        text = text.replace(word, "[excluded]")
    return text


def list_tracked(root=REPO):
    out = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True,
                         check=True).stdout
    names = sorted(n for n in out.decode("utf-8").split("\0") if n)
    skip = EXCLUDE + (OUT_DIR + "/",)
    return [n for n in names if not n.startswith(skip)]


def kind_of(path):
    name = path.rsplit("/", 1)[-1]
    ext = Path(name).suffix.lower()
    if ext in CODE_EXT:
        return CODE_EXT[ext]
    if ext in KINDS:
        return KINDS[ext]
    if name == "Makefile":
        return "makefile"
    return ext[1:] if ext else "other"


def count_lines(data):
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def first_heading(text):
    fenced = False
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        elif not fenced:
            match = re.match(r"#{1,6}\s+(.*\S)", line)
            if match:
                return match.group(1).strip()
    return ""


def first_comment(text):
    lines = text.splitlines()
    for i, raw in enumerate(lines):
        line = raw.strip()
        if not line or line.startswith("#!") or line.lower().startswith("#requires"):
            continue
        if line.startswith("<#"):
            rest = line[2:].strip()
            j = i + 1
            while (not rest or rest.startswith(".")) and j < len(lines):
                rest = lines[j].strip()
                j += 1
            return rest.rstrip("#>").strip()
        if line.startswith("#"):
            return line.lstrip("#").strip()
        break
    return ""


def read_file(root, path):
    """Return a record dict (with transient `data` bytes) for one tracked file."""
    full = root / path
    if not full.is_file():
        return None
    data = full.read_bytes()
    ext = Path(path).suffix.lower()
    binary = ext in BINARY_EXT or b"\0" in data[:8000]
    if not binary:
        data = data.replace(b"\r\n", b"\n")
    rec = {
        "path": path, "kind": kind_of(path), "text": not binary,
        "sha256": hashlib.sha256(data).hexdigest(), "purpose": "", "data": data,
    }
    if binary:
        rec["bytes"] = len(data)
    else:
        rec["lines"] = count_lines(data)
        text = data.decode("utf-8", "replace").lstrip("﻿")
        if rec["kind"] == "markdown":
            rec["purpose"] = clean(first_heading(text))
        elif rec["kind"] in ("powershell", "shell"):
            rec["purpose"] = clean(first_comment(text))
    return rec


def sources_digest(records):
    h = hashlib.sha256()
    for path in sorted(records):
        h.update(f"{path}\0{records[path]['sha256']}\n".encode())
    return h.hexdigest()

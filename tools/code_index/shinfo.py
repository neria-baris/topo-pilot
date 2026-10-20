"""PowerShell / shell scripts: function definitions and invoked repo scripts (regex based)."""
import posixpath
import re

FUNC_PS = re.compile(r"^\s*function\s+([A-Za-z_][\w:-]*)", re.IGNORECASE)
FUNC_SH = re.compile(r"^\s*(?:function\s+)?([A-Za-z_][\w-]*)\s*\(\)\s*\{?|^\s*function\s+([\w-]+)")
SCRIPT = re.compile(r"[\w./\\-]+\.(?:py|ps1|sh)\b")


def extract(path, text, kind, code_files):
    """Return {functions: [{name, line}], invokes: [{line, token, target}]}."""
    func_re = FUNC_PS if kind == "powershell" else FUNC_SH
    here = posixpath.dirname(path)
    by_suffix = {}
    for f in code_files:
        by_suffix.setdefault(posixpath.basename(f), []).append(f)
    functions, invokes = [], []
    for no, line in enumerate(text.split("\n"), 1):
        match = func_re.match(line)
        if match:
            functions.append({"name": next(g for g in match.groups() if g), "line": no})
        if line.lstrip().startswith("#"):
            continue
        for token in SCRIPT.findall(line):
            tok = token.replace("\\", "/")
            while tok.startswith("./"):
                tok = tok[2:]
            target = None
            options = [tok, posixpath.normpath(posixpath.join(here, tok))]
            for opt in options:
                if opt in code_files and opt != path:
                    target = opt
                    break
            if target is None:
                cands = [f for f in by_suffix.get(posixpath.basename(tok), [])
                         if f.endswith("/" + tok) and f != path]
                target = cands[0] if len(cands) == 1 else None
            if target:
                invokes.append({"line": no, "token": tok, "target": target})
    return {"functions": functions, "invokes": invokes}

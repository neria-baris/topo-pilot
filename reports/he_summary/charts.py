"""SVG charts and diagrams for the Hebrew research summary (print, light mode).

Every number comes either from data/*.json (extracted read-only from the artifact store)
or from the committed reports (reports/E0..E4, README); the source is named next to it.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
DATA = HERE / "data"

# ---- tokens (dataviz reference palette, light mode) ----------------------------------------
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df", "#fcfcfb"
CYL, SQ, AQUA, VIOLET = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6"
CYL_T, SQ_T, AQ_T, NEU_T = "#e3eefb", "#fde9e0", "#e0f5ec", "#f1f0ec"
GOOD, BAD, WARN = "#1f7a3a", "#b42318", "#a15c00"
GOOD_T, BAD_T, WARN_T = "#e7f4ea", "#fbeceb", "#fdf1e0"
FONT = "David Libre"
HEB = re.compile(r"[֐-׿]")


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, s, anchor="middle", size=13, weight=400, fill=INK, italic=False, extra=""):
    """Text with a *visual* anchor: 'left' = text starts at x and runs right,
    'right' = text ends at x. Hebrew strings get direction=rtl."""
    rtl = bool(HEB.search(s))
    if anchor == "middle":
        ta = "middle"
    elif anchor == "left":
        ta = "end" if rtl else "start"
    else:
        ta = "start" if rtl else "end"
    d = ' direction="rtl"' if rtl else ' direction="ltr"'
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{ta}"{d} font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}"{st}{extra}>{esc(s)}</text>')


def ML(x, y, lines, size=13, lh=None, **kw):
    lh = lh or size * 1.2
    y0 = y - (len(lines) - 1) * lh / 2
    return "".join(T(x, y0 + i * lh, s, size=size, **kw) for i, s in enumerate(lines))


def svg(w, h, body, label=""):
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="{FONT}, Times New Roman, serif" role="img" aria-label="{esc(label)}">'
            f'<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
            f'fill="{INK2}"/></marker></defs>{body}</svg>')


def box(x, y, w, h, lines, fill=NEU_T, stroke=MUTED, size=13, weight=400, r=8, sw=1.2,
        dash=None, color=INK):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
           f'stroke="{stroke}" stroke-width="{sw}"{d}/>')
    if isinstance(lines, str):
        lines = [lines]
    return out + ML(x + w / 2, y + h / 2 + size * 0.35, lines, size=size, weight=weight,
                    fill=color)


def arrow(x1, y1, x2, y2, color=INK2, sw=1.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}" marker-end="url(#ar)"{d}/>')


def path_arrow(dpath, color=INK2, sw=1.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{dpath}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'marker-end="url(#ar)"{d}/>')


def chip(x, y, text, kind):
    fill, col = {"good": (GOOD_T, GOOD), "bad": (BAD_T, BAD), "warn": (WARN_T, WARN),
                 "neu": (NEU_T, INK2)}[kind]
    w = max(54, 7.2 * len(text) + 16)
    return (f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="20" rx="10" fill="{fill}" '
            f'stroke="{col}" stroke-width="0.8"/>' + T(x, y + 4, text, size=11.5, weight=700,
                                                         fill=col))


# ---- axis helpers ----------------------------------------------------------------------------
class Axis:
    def __init__(self, d0, d1, r0, r1, log=False):
        self.d0, self.d1, self.r0, self.r1, self.log = d0, d1, r0, r1, log

    def __call__(self, v):
        if self.log:
            v, a, b = math.log10(v), math.log10(self.d0), math.log10(self.d1)
        else:
            a, b = self.d0, self.d1
        return self.r0 + (v - a) / (b - a) * (self.r1 - self.r0)


def ygrid(ax, ticks, x0, x1, fmt="{:.2f}", size=11):
    out = ""
    for t in ticks:
        y = ax(t)
        out += f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>'
        out += T(x0 - 6, y + 4, fmt.format(t) if isinstance(fmt, str) else fmt(t),
                 anchor="right", size=size, fill=INK2)
    return out


def legend(x, y, items, size=12, gap=22):
    """items: [(label, color, kind)] laid out right-to-left starting at x (right edge)."""
    out, cx = "", x
    for label, color, kind in items:
        if kind == "line":
            out += f'<line x1="{cx - 18}" y1="{y - 4}" x2="{cx}" y2="{y - 4}" stroke="{color}" stroke-width="2.4"/>'
        elif kind == "dash":
            out += f'<line x1="{cx - 18}" y1="{y - 4}" x2="{cx}" y2="{y - 4}" stroke="{color}" stroke-width="1.6" stroke-dasharray="4 3"/>'
        elif kind == "dot":
            out += f'<circle cx="{cx - 7}" cy="{y - 4}" r="5" fill="{color}"/>'
        else:
            out += f'<rect x="{cx - 14}" y="{y - 11}" width="14" height="14" rx="3" fill="{color}"/>'
        out += T(cx - 24, y + 1, label, anchor="right", size=size, fill=INK)
        cx -= 24 + len(label) * size * 0.48 + gap
    return out


# =============================================================================================
# Diagrams
# =============================================================================================
def fig_pipeline():
    """Overall research flow: generator -> two branches (model / oracle) -> analysis -> verdicts."""
    W, H = 680, 610
    b = ""
    # row 1: generator chain (right to left)
    xs = [530, 360, 190, 20]
    labels = [["עולם סמוי", "גליל / ריבוע 12×12"], ["דינמיקה", "הליכה עצלה, p=0.2"],
              ["פליטה", "O · P · N · U, V=36"], ["רצפים", "33 סמלים למסלול"]]
    for x, l in zip(xs, labels):
        b += box(x, 40, 130, 56, l, fill=NEU_T, size=13)
    for i in range(3):
        b += arrow(xs[i] - 2, 68, xs[i + 1] + 132, 68)
    b += T(660, 24, "מחולל הנתונים (ידוע במלואו)", anchor="right", size=13, weight=700, fill=INK2)
    # branch split
    b += path_arrow("M85,96 L85,130 L190,130 L190,150")
    b += path_arrow("M85,130 L490,130 L490,150")
    # left: model branch ; right: oracle branch
    b += box(400, 152, 180, 58, ["Transformer קטן מאפס", "4 בלוקים, d=128, 5000 צעדים"],
             fill=CYL_T, stroke=CYL, size=13)
    b += box(100, 152, 180, 58, ["מנבא בייסיאני מדויק", "סינון HMM ב־float64"],
             fill=AQ_T, stroke=AQUA, size=13)
    b += arrow(490, 210, 490, 240)
    b += arrow(190, 210, 190, 240)
    b += box(400, 242, 180, 58, ["אקטיבציות ב־resid_post_3", "וקטורים ב־ℝ¹²⁸, 12 נקודות בדיקה"],
             fill=CYL_T, stroke=CYL, size=13)
    b += box(100, 242, 180, 58, ["מרחבי ייחוס", "אמונות, עתידים, שדה פליטה"],
             fill=AQ_T, stroke=AQUA, size=13)
    b += T(600, 186, "ענף הלמידה", anchor="left", size=12, fill=CYL, weight=700)
    b += T(80, 186, "ענף האורקל", anchor="right", size=12, fill=AQUA, weight=700)
    # panels
    b += arrow(490, 300, 400, 340)
    b += arrow(190, 300, 280, 340)
    b += box(200, 342, 280, 52, ["8 לוחות זרים × 512 היסטוריות (p=32)",
                                 "אותן היסטוריות בכל מרחב ונקודת בדיקה"], fill=NEU_T, size=13)
    b += arrow(340, 394, 340, 420)
    # analysis row
    ax = [500, 340, 180, 20]
    al = [["הומולוגיה מתמידה", "המדד S"], ["השוואת גאומטריות", "המדד Δgeom"],
          ["בסיסי ייצוג", "R0–R3, רצפה גאוסית"], ["ניתוחי S7", "probes ומעגליות"]]
    b += f'<rect x="10" y="420" width="660" height="80" rx="10" fill="none" stroke="{GRID}" stroke-width="1.2"/>'
    for x, l in zip(ax, al):
        b += box(x + 6, 434, 148, 54, l, fill="#ffffff", size=12.5)
    b += arrow(340, 500, 340, 528)
    b += box(150, 530, 380, 62, ["כללי הכרעה שהוקפאו מראש",
                                 "נתמך / נדחה / לא מכריע, לכל השערה"],
             fill="#ffffff", stroke=INK, size=13.5, weight=700, sw=1.6)
    return svg(W, H, b, "תרשים זרימה של המחקר")


def fig_stages():
    """Stages S0..S8, gates, owner checkpoints and exit points (vertical timeline)."""
    W, H = 680, 710
    rows = [
        ("S0", "סביבה וחוזים", "מאגר תוצרים ונעילת סביבה", "—", None),
        ("S1", "עולמות ו־PH על אמת ידועה", "בדיקת β, PH על העולם, כיול", "G-A", "E0"),
        ("S2", "נתונים, אורקל, כיול σ", "טבלת הבחנה, רישום מוקדם", "G-B · G-C · G-D", "E1"),
        ("S3", "ריצת ניסיון", "תפוקה, זיכרון, שער למידה", "G-E", None),
        ("S4", "ניסוי מרכזי תחת O", "שש ריצות ומודל N", "G-F", "E2"),
        ("S5", "בקרה מותאמת P", "שש ריצות נוספות", "G-F (P)", None),
        ("S6", "דינמיקת אימון", "עקומות לאורך 12 נקודות", "—", "E3"),
        ("S7", "בקרות, probes, רגישות", "בקרות U ו־N, מעגליות", "G-G", None),
        ("S8", "שחזור נקי", "שכפול טרי, מאגר ריק", "G-H נכשל", "E4"),
    ]
    holds = {"S2": "H1", "S3": "H2", "S5": "H3", "S8": "H4"}
    b = ""
    y0, dy = 70, 68
    b += T(650, 26, "שלב", anchor="right", size=12, weight=700, fill=INK2)
    b += T(470, 26, "תוכן", anchor="middle", size=12, weight=700, fill=INK2)
    b += T(250, 26, "שער אוטומטי", anchor="middle", size=12, weight=700, fill=INK2)
    b += T(140, 26, "אישור בעלים", anchor="middle", size=12, weight=700, fill=INK2)
    b += T(55, 26, "נקודת יציאה", anchor="middle", size=12, weight=700, fill=INK2)
    b += f'<line x1="625" y1="{y0}" x2="625" y2="{y0 + dy * 8}" stroke="{GRID}" stroke-width="3"/>'
    for i, (sid, title, sub, gate, ex) in enumerate(rows):
        y = y0 + i * dy
        b += f'<circle cx="625" cy="{y}" r="17" fill="#ffffff" stroke="{INK}" stroke-width="1.4"/>'
        b += T(625, y + 5, sid, size=13, weight=700)
        b += box(345, y - 26, 255, 52, [title, sub], fill=NEU_T, size=12.5, stroke=GRID)
        if gate != "—":
            fail = "נכשל" in gate
            b += f'<line x1="345" y1="{y}" x2="312" y2="{y}" stroke="{GRID}" stroke-width="1.2"/>'
            b += box(190, y - 15, 120, 30, gate, fill=BAD_T if fail else GOOD_T,
                     stroke=BAD if fail else GOOD, size=12.5, weight=700,
                     color=BAD if fail else GOOD, r=15)
        if sid in holds:
            b += (f'<polygon points="140,{y - 15} 155,{y} 140,{y + 15} 125,{y}" fill="{WARN_T}" '
                  f'stroke="{WARN}" stroke-width="1.2"/>') + T(140, y + 4.5, holds[sid], size=11.5,
                                                                 weight=700, fill=WARN)
        if ex:
            b += box(25, y - 16, 60, 32, ex, fill=CYL_T, stroke=CYL, size=14, weight=700,
                     color=CYL, r=6)
    b += T(340, 694, "יהלום = נקודת עצירה לאישור הבעלים (H1–H4); מלבן מעוגל = שער שנבדק אוטומטית",
           size=11.5, fill=INK2)
    return svg(W, H, b, "שלבי המחקר, שערים ונקודות יציאה")


def fig_decision():
    """F1 decision rule as a flow chart."""
    W, H = 680, 380
    b = ""
    b += box(220, 14, 240, 50, ["לכל חזרה ולכל לוח:", "D = ΔS_cyl − ΔS_sq"],
             fill=NEU_T, size=13.5, weight=700)
    b += arrow(340, 64, 340, 92)
    b += box(200, 94, 280, 46, "האם כל המודלים עברו את שער הלמידה?", fill="#ffffff", size=13.5)
    b += path_arrow("M200,117 L95,117 L95,300")
    b += T(150, 108, "לא", size=12, fill=INK2)
    b += arrow(340, 140, 340, 168)
    b += T(352, 158, "כן", anchor="left", size=12, fill=INK2)
    b += box(170, 170, 340, 46, "(1) D > 0 בלפחות 7 מתוך 8 לוחות, בכל אחת מ־3 החזרות?",
             fill="#ffffff", size=13.5)
    b += arrow(340, 216, 340, 238)
    b += T(352, 231, "כן", anchor="left", size=12, fill=INK2)
    b += box(170, 240, 340, 46, "(2) חציון D > u_r (מעטפת רעש הלוחות) בכל חזרה?",
             fill="#ffffff", size=13.5)
    b += path_arrow("M510,193 L590,193 L590,300")
    b += path_arrow("M510,263 L590,263")
    b += T(548, 185, "לא", size=12, fill=INK2)
    b += T(548, 255, "לא", size=12, fill=INK2)
    b += arrow(340, 286, 340, 302)
    b += T(352, 298, "כן", anchor="left", size=12, fill=INK2)
    b += box(255, 304, 170, 44, "F1 נתמך", fill=GOOD_T, stroke=GOOD, size=15, weight=700,
             color=GOOD)
    b += box(520, 304, 140, 44, "F1 נדחה", fill=BAD_T, stroke=BAD, size=15, weight=700,
             color=BAD)
    b += box(20, 304, 150, 44, ["לא מכריע", "(מדווח השער שנכשל)"], fill=WARN_T, stroke=WARN,
             size=13, weight=700, color=WARN)
    b += T(340, 372, "ארבעת ערכי S מדווחים תמיד לצד D; הסף u_r נגזר מהנתונים עצמם ולא מבקרת השלילה",
           size=11.5, fill=INK2)
    return svg(W, H, b, "כלל ההכרעה F1")


def fig_followups():
    W, H = 680, 470
    b = ""
    b += box(250, 12, 180, 46, ["E4 הושג", "שאלות פתוחות: מקור, סיבתיות"], fill=CYL_T,
             stroke=CYL, size=13.5, weight=700)
    groups = [
        (510, "האם המבנה נחוץ לחיזוי?", [("אופק עתידי (X4 B)", "לא מכריע", "warn"),
                                         ("כיסוי (X4 B2)", "NO-GO מוגבל", "bad")]),
        (340, "האם הוא בא מההיסטוריה?", [("קו־בסיס מעגלי", "תיאורי", "neu"),
                                          ("פרופיל אורקל (0014)", "חקרני", "neu"),
                                          ("מחזור K8", "FAIL מרווח", "bad"),
                                          ("היתכנות מעגלית (K4)", "לא מכריע", "warn")]),
        (170, "האם המודל משתמש בו?", [("מחיקה סיבתית (X4-F)", "לא מכריע", "warn")]),
        (0, "הרחבות", [("זמן למידה (X5 G1)", "H5 נדחתה", "bad"),
                        ("גליל מול מביוס (D-1)", "PASS", "good")]),
    ]
    for gx, title, items in groups:
        cx = gx + 85
        b += path_arrow(f"M340,58 L340,74 L{cx},74 L{cx},92")
        b += box(gx + 7, 94, 156, 44, title, fill=NEU_T, size=13, weight=700)
        for j, (name, verdict, kind) in enumerate(items):
            y = 160 + j * 72
            b += f'<line x1="{cx}" y1="{y - 22 if j == 0 else y - 16}" x2="{cx}" y2="{y}" stroke="{GRID}" stroke-width="1.4"/>'
            b += box(gx + 12, y, 146, 56, [name, ""], fill="#ffffff", size=12.5, stroke=GRID)
            b += chip(cx, y + 38, verdict, kind)
    b += T(340, 460, "כל המחקרים רשומים מראש למעט פרופיל האורקל; שום תוצאה כאן אינה משנה הכרעה של E0–E4",
           size=11.5, fill=INK2)
    return svg(W, H, b, "מפת מחקרי ההמשך")


def fig_world():
    """Square vs cylinder lattice with emission centres."""
    W, H = 680, 308
    b = ""
    for k, (ox, name, cyl) in enumerate([(380, "גליל: ציר x מחזורי, β₁ = 1", True),
                                          (40, "ריבוע: ללא הדבקה, β₁ = 0", False)]):
        c = 18
        b += T(ox + 6 * c, 26, name, size=13.5, weight=700)
        for i in range(12):
            for j in range(12):
                x, y = ox + i * c, 44 + j * c
                b += f'<circle cx="{x + c / 2}" cy="{y + c / 2}" r="2.1" fill="{MUTED}"/>'
        for i in range(12):
            y = 44 + i * c + c / 2
            b += f'<line x1="{ox + c / 2}" y1="{y}" x2="{ox + 11.5 * c}" y2="{y}" stroke="{GRID}" stroke-width="1"/>'
            x = ox + i * c + c / 2
            b += f'<line x1="{x}" y1="{44 + c / 2}" x2="{x}" y2="{44 + 11.5 * c}" stroke="{GRID}" stroke-width="1"/>'
        # emission centres (a, b) -> (0.5+2a, 0.5+2b)
        for a in range(6):
            for bb in range(6):
                x = ox + (0.5 + 2 * a) * c + c / 2
                y = 44 + (0.5 + 2 * bb) * c + c / 2
                b += f'<rect x="{x - 3.5}" y="{y - 3.5}" width="7" height="7" fill="{SQ if not cyl else CYL}" opacity="0.85" transform="rotate(45 {x} {y})"/>'
        if cyl:
            col = CYL
            for j in (2, 6, 10):
                y = 44 + j * c + c / 2
                b += (f'<path d="M{ox + 11.5 * c},{y} C{ox + 13.2 * c},{y - 26} {ox - 1.2 * c},{y - 26} '
                      f'{ox + c / 2},{y}" fill="none" stroke="{col}" stroke-width="1.3" '
                      f'stroke-dasharray="4 3" marker-end="url(#ar)"/>')
            b += T(ox + 6 * c, 44 + 12 * c + 22, "העמודה הימנית והשמאלית מודבקות (התפר)", size=12,
                   fill=col)
        else:
            b += T(ox + 6 * c, 44 + 12 * c + 22, "צעד אל מחוץ לשפה הופך להישארות במקום", size=12,
                   fill=INK2)
    b += T(340, 300, "נקודות = 144 מצבים; מעוינים = 36 מרכזי פליטה ברשת 6×6",
           size=11.5, fill=INK2)
    return svg(W, H, b, "שני העולמות")


def emission_grid(perm=False, a=0, bsym=2, sigma=1.25):
    xs = np.arange(12)
    cent = 0.5 + 2 * np.arange(6)

    def factor(periodic):
        d = np.abs(xs[:, None] - cent[None, :])
        if periodic:
            d = np.minimum(d, 12 - d)
        e = np.exp(-d ** 2 / (2 * sigma ** 2))
        return e / e.sum(1, keepdims=True)

    ex, ey = factor(True), factor(False)
    E = ex[:, a][:, None] * ey[:, bsym][None, :]  # [x, y]
    if perm:
        rng = np.random.default_rng(7)
        sx, sy = rng.permutation(12), rng.permutation(12)
        E = E[sx][:, sy]
    return E


def fig_emission():
    W, H = 680, 300
    b = ""
    Eo, Ep = emission_grid(False), emission_grid(True)
    vmax = Eo.max()
    ramp = ["#f2f7fd", "#d6e6f8", "#b1cff2", "#82b1e9", "#5592de", "#2a78d6", "#1d5aa6", "#123d73"]

    def col(v):
        return ramp[min(7, int(v / vmax * 7.999))]

    for ox, Ez, title in [(390, Eo, "O: פליטה חלקה"), (60, Ep, "P: אותן שורות, צירים מעורבבים")]:
        c = 17
        b += T(ox + 6 * c, 24, title, size=13.5, weight=700)
        for i in range(12):
            for j in range(12):
                b += (f'<rect x="{ox + i * c}" y="{40 + j * c}" width="{c - 1}" height="{c - 1}" '
                      f'fill="{col(Ez[i, j])}"/>')
        b += T(ox + 6 * c, 40 + 12 * c + 18, "x →", size=11.5, fill=INK2)
    # legend ramp
    for k, cc in enumerate(ramp):
        b += f'<rect x="{270 + k * 18}" y="268" width="18" height="10" fill="{cc}"/>'
    b += T(266, 278, "0", anchor="right", size=11, fill=INK2)
    b += T(270 + 8 * 18 + 4, 278, f"{vmax:.2f}", anchor="left", size=11, fill=INK2)
    b += T(340, 296, "הסתברות הפליטה של סמל יחיד מכל מצב בגליל (המחשה; הפרמוטציה כאן אקראית)",
           size=11.5, fill=INK2)
    return svg(W, H, b, "שדה הפליטה תחת O ותחת P")


def fig_ph():
    """Schematic: ring point cloud -> barcode -> S."""
    W, H = 680, 260
    rng = np.random.default_rng(3)
    th = rng.uniform(0, 2 * np.pi, 46)
    r = 1 + rng.normal(0, 0.09, 46)
    b = ""
    cx, cy, R = 560, 125, 72
    for t, rr in zip(th, r):
        b += f'<circle cx="{cx + R * rr * math.cos(t):.1f}" cy="{cy + R * rr * math.sin(t):.1f}" r="3.2" fill="{CYL}"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{R * 0.55:.1f}" fill="none" stroke="{GRID}" stroke-width="1" stroke-dasharray="3 3"/>'
    b += T(cx, 226, "ענן נקודות (היסטוריות)", size=12.5, weight=700)
    b += arrow(470, 125, 420, 125)
    b += T(445, 112, "VR", size=12, fill=INK2)
    # barcode
    x0, x1 = 120, 400
    b += T((x0 + x1) / 2, 30, "ברקוד פרסיסטנטי", size=12.5, weight=700)
    ax = Axis(0, 1, x0, x1)
    for k in range(10):
        y = 44 + k * 6
        d = 0.05 + 0.13 * rng.random()
        b += f'<line x1="{ax(0)}" y1="{y}" x2="{ax(d):.1f}" y2="{y}" stroke="{MUTED}" stroke-width="3"/>'
    b += T(x1 + 6, 74, "H₀", anchor="left", size=12, fill=INK2)
    for k, (u, v, colr, w) in enumerate([(0.22, 0.86, CYL, 5), (0.30, 0.38, MUTED, 3),
                                          (0.41, 0.47, MUTED, 3), (0.52, 0.56, MUTED, 3)]):
        y = 130 + k * 14
        b += f'<line x1="{ax(u):.1f}" y1="{y}" x2="{ax(v):.1f}" y2="{y}" stroke="{colr}" stroke-width="{w}"/>'
    b += T(x1 + 6, 156, "H₁", anchor="left", size=12, fill=INK2)
    b += f'<line x1="{x0}" y1="200" x2="{x1}" y2="200" stroke="{INK2}" stroke-width="1"/>'
    b += T((x0 + x1) / 2, 218, "סקאלה (רדיוס הפילטרציה)", size=11.5, fill=INK2)
    b += f'<line x1="{ax(0.22):.1f}" y1="118" x2="{ax(0.86):.1f}" y2="118" stroke="{CYL}" stroke-width="1" marker-end="url(#ar)"/>'
    b += T(ax(0.54), 112, "פס ארוך = מעגל יציב", size=11.5, fill=CYL)
    b += box(8, 92, 100, 72, ["S =", "אורך הפס", "חלקי הסקאלה"], fill=NEU_T, size=12)
    b += T(340, 250, "המחשה סכמטית: S הוא אורך פס ה־H₁ הסופי הארוך ביותר, מנורמל בסקאלת הענן",
           size=11.5, fill=INK2)
    return svg(W, H, b, "הומולוגיה מתמידה והמדד S")


def fig_dcontrast():
    W, H = 680, 210
    b = ""
    cells = [(470, 30, "גליל, אתחול", "S_cyl,init", CYL_T, CYL), (470, 110, "גליל, סוף", "S_cyl,final", CYL_T, CYL),
             (250, 30, "ריבוע, אתחול", "S_sq,init", SQ_T, SQ), (250, 110, "ריבוע, סוף", "S_sq,final", SQ_T, SQ)]
    for x, y, t, s, f, st in cells:
        b += box(x, y, 160, 56, [t, s], fill=f, stroke=st, size=13)
    b += arrow(550, 86, 550, 108)
    b += arrow(330, 86, 330, 108)
    b += T(560, 101, "ΔS גליל", anchor="left", size=12, fill=CYL)
    b += T(340, 101, "ΔS ריבוע", anchor="left", size=12, fill=SQ)
    b += box(20, 70, 190, 64, ["D = ΔS_cyl − ΔS_sq", "אותו לוח בשני העולמות"],
             fill="#ffffff", stroke=INK, size=12.5, weight=700, sw=1.5)
    b += path_arrow("M250,138 L222,120")
    b += T(340, 200, "ההפרש הכפול מנכה גם את מה שהארכיטקטורה מייצרת באתחול וגם הבדלים קבועים בין העולמות",
           size=11.5, fill=INK2)
    return svg(W, H, b, "הניגוד D")


# =============================================================================================
# Data charts
# =============================================================================================
def chart_e0():
    """reports/E0/summary.md"""
    W, H = 680, 250
    x0, x1, yb, yt = 70, 640, 200, 30
    ay = Axis(0, 0.35, yb, yt)
    b = ygrid(ay, [0, 0.1, 0.2, 0.3], x0, x1)
    groups = [("מטריקה שטוחה d_M", 0.299, 0.037), ("מטריקת גרף", 0.231, 0.067)]
    gw = (x1 - x0) / 2
    for k, (name, cyl, sq) in enumerate(groups):
        gx = x0 + k * gw + gw / 2
        for v, col, dx in [(cyl, CYL, -30), (sq, SQ, 30)]:
            bx = gx + dx - 22
            b += f'<rect x="{bx}" y="{ay(v):.1f}" width="44" height="{yb - ay(v):.1f}" rx="3" fill="{col}"/>'
            b += T(gx + dx, ay(v) - 6, f"{v:.3f}", size=12, fill=INK)
        b += T(gx, yb + 20, name, size=12.5, fill=INK)
    for v, lab in [(0.2, "סף הגליל: לפחות 0.2"), (0.1, "סף הריבוע: לכל היותר 0.1")]:
        b += f'<line x1="{x0}" y1="{ay(v):.1f}" x2="{x1}" y2="{ay(v):.1f}" stroke="{INK2}" stroke-width="1.2" stroke-dasharray="5 4"/>'
        b += T(x1, ay(v) - 5, lab, anchor="right", size=11.5, fill=INK2)
    b += f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{INK2}"/>'
    b += legend(x1, 244, [("גליל", CYL, "sq"), ("ריבוע", SQ, "sq")])
    b += T(18, 115, "S", size=13, italic=True, fill=INK2)
    return svg(W, H, b, "E0: S של העולמות")


def chart_e1():
    """README.md, E1 table (replicate 1729, σ = 1.25, 8 panels)."""
    rows = [(("b³²", "אמונה"), (0.671, 0.321), (0.323, 0.310)),
            (("b¹", "סמל אחרון"), (0.324, 0.165), (0.324, 0.165)),
            (("F₁", "עתיד 1"), (0.556, 0.189), (0.194, 0.241)),
            (("F₂", "עתיד 2"), (0.614, 0.216), (0.202, 0.242)),
            (("E", "פליטה"), (0.568, 0.108), (0.568, 0.108))]
    W, H = 680, 300
    b = ""
    for k, (cond, title, ox) in enumerate([("O", "O: פליטה חלקה", 360), ("P", "P: צירים מעורבבים", 30)]):
        x0, x1, yb, yt = ox + 30, ox + 300, 240, 40
        ay = Axis(0, 0.75, yb, yt)
        b += T((x0 + x1) / 2, 22, title, size=13.5, weight=700)
        b += ygrid(ay, [0, 0.25, 0.5, 0.75], x0, x1)
        gw = (x1 - x0) / len(rows)
        for i, (name, o, p) in enumerate(rows):
            cyl, sq = (o if cond == "O" else p)
            gx = x0 + i * gw + gw / 2
            for v, col, dx in [(cyl, CYL, -10), (sq, SQ, 10)]:
                b += f'<rect x="{gx + dx - 9:.1f}" y="{ay(v):.1f}" width="18" height="{yb - ay(v):.1f}" rx="2.5" fill="{col}"/>'
            sym, word = name
            b += T(gx, yb + 16, sym, size=12, fill=INK)
            b += T(gx, yb + 31, word, size=11, fill=INK2)
        b += f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{INK2}"/>'
    b += legend(660, 296, [("גליל", CYL, "sq"), ("ריבוע", SQ, "sq")])
    return svg(W, H, b, "E1: הבחנה במרחבים לא נלמדים")


def chart_f1_panels():
    """data/d.json (per-panel D, read from the store) + u_r from reports/E2, E3."""
    d = json.loads((DATA / "d.json").read_text())
    ur = {"O": {"1729": 0.0966, "2718": 0.0839, "3141": 0.0842},
          "P": {"1729": 0.0656, "2718": 0.0893, "3141": 0.0722}}
    W, H = 680, 306
    x0, x1, yb, yt = 70, 650, 236, 24
    ay = Axis(-0.1, 0.25, yb, yt)
    b = ygrid(ay, [-0.1, -0.05, 0, 0.05, 0.1, 0.15, 0.2, 0.25], x0, x1)
    b += f'<line x1="{x0}" y1="{ay(0):.1f}" x2="{x1}" y2="{ay(0):.1f}" stroke="{INK2}" stroke-width="1.3"/>'
    slots = [("O", s) for s in ("1729", "2718", "3141")] + [("P", s) for s in ("1729", "2718", "3141")]
    gw = (x1 - x0) / 6
    rng = np.random.default_rng(1)
    for k, (cond, seed) in enumerate(slots):
        gx = x0 + k * gw + gw / 2
        col = CYL if cond == "O" else VIOLET
        vals = d[cond][seed]
        jit = rng.uniform(-14, 14, len(vals))
        for v, j in zip(vals, jit):
            b += f'<circle cx="{gx + j:.1f}" cy="{ay(v):.1f}" r="4.6" fill="{col}" fill-opacity="0.8" stroke="{SURF}" stroke-width="1.2"/>'
        med = float(np.median(vals))
        b += f'<line x1="{gx - 26}" y1="{ay(med):.1f}" x2="{gx + 26}" y2="{ay(med):.1f}" stroke="{INK}" stroke-width="2.6"/>'
        u = ur[cond][seed]
        b += f'<line x1="{gx - 30}" y1="{ay(u):.1f}" x2="{gx + 30}" y2="{ay(u):.1f}" stroke="{BAD}" stroke-width="1.6" stroke-dasharray="4 3"/>'
        npos = sum(v > 0 for v in vals)
        b += T(gx, yb + 18, f"{cond} · {seed}", size=12, fill=INK)
        b += T(gx, yb + 34, f"{npos}/8 חיוביים", size=11.5, fill=INK2)
    b += f'<line x1="{x0 + 3 * gw}" y1="{yt}" x2="{x0 + 3 * gw}" y2="{yb + 36}" stroke="{GRID}" stroke-width="1.5"/>'
    b += T(22, 130, "D", size=13, italic=True, fill=INK2)
    b += legend(650, 300, [("לוח בודד, O", CYL, "dot"), ("לוח בודד, P", VIOLET, "dot"),
                           ("חציון", INK, "line"), ("u_r (מעטפת רעש)", BAD, "dash")])
    return svg(W, H, b, "הניגוד D לפי לוח")


def chart_baselines():
    """reports/E2/summary.md, ratio of baseline median D to model median D."""
    data = {"1729": (0.89, 0.17, 0.02), "2718": (0.47, 0.20, 0.10), "3141": (0.54, 0.19, 0.08)}
    W, H = 680, 240
    x0, x1, yb, yt = 70, 650, 190, 24
    ay = Axis(0, 1.0, yb, yt)
    b = ygrid(ay, [0, 0.25, 0.5, 0.75, 1.0], x0, x1, fmt="{:.2f}")
    gw = (x1 - x0) / 3
    cols = [AQUA, VIOLET, SQ]
    for k, (seed, vals) in enumerate(data.items()):
        gx = x0 + k * gw + gw / 2
        for j, (v, c) in enumerate(zip(vals, cols)):
            bx = gx + (j - 1) * 46 - 19
            b += f'<rect x="{bx:.1f}" y="{ay(v):.1f}" width="38" height="{yb - ay(v):.1f}" rx="3" fill="{c}"/>'
            b += T(bx + 19, ay(v) - 5, f"{v:.2f}", size=11.5)
        b += T(gx, yb + 18, f"חזרה {seed}", size=12.5)
    b += f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{INK2}"/>'
    b += legend(650, 236, [("סמל אחרון (R1)", AQUA, "sq"), ("ערבוב עם הסמל הקודם (R2)", VIOLET, "sq"),
                           ("ממוצע הקשר (R3)", SQ, "sq")])
    b += ML(26, 108, ["חלק", "מ־D", "של", "המודל"], size=11.5, fill=INK2, lh=13)
    return svg(W, H, b, "בסיסי ייצוג")


def chart_dynamics():
    """data/dyn.json (S6 MetricRecords, panel 1, primary hook)."""
    dyn = json.loads((DATA / "dyn.json").read_text())
    steps = [0, 50, 100, 200, 400, 700, 1000, 1500, 2000, 3000, 4000, 5000]
    W, H = 680, 520
    b = ""
    for k, (cond, ox) in enumerate([("O", 355), ("P", 25)]):
        x0, x1 = ox + 45, ox + 315
        ax = Axis(0, 11, x0, x1)
        # S panel
        yb, yt = 224, 54
        ay = Axis(0, 0.4, yb, yt)
        b += T((x0 + x1) / 2, 22, f"{cond}: ציון H₁ (S), לוח 1", size=13.5, weight=700)
        b += ygrid(ay, [0, 0.1, 0.2, 0.3, 0.4], x0, x1, fmt="{:.1f}")
        for key, ser in dyn[cond]["S"].items():
            col = CYL if key.startswith("cyl") else SQ
            pts = " ".join(f"{ax(steps.index(s)):.1f},{ay(v):.1f}" for s, v in ser)
            b += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="1.8" stroke-opacity="0.9"/>'
        for xs_, lab in [(1, "50"), (2, "100")]:
            b += f'<line x1="{ax(xs_):.1f}" y1="{yt}" x2="{ax(xs_):.1f}" y2="{yb}" stroke="{INK2}" stroke-width="1" stroke-dasharray="3 3"/>'
        b += T(ax(1) - 3, yt - 6, "S עולה", anchor="right", size=11, fill=INK2)
        b += T(ax(2) + 3, yt - 6, "regret < G_C", anchor="left", size=11, fill=INK2)
        b += f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{INK2}"/>'
        # regret panel (log)
        yb2, yt2 = 460, 280
        ay2 = Axis(0.001, 2, yb2, yt2, log=True)
        b += T((x0 + x1) / 2, 262, f"{cond}: regret (nats, סקאלה לוגריתמית)", size=13.5, weight=700)
        b += ygrid(ay2, [0.001, 0.01, 0.1, 1], x0, x1, fmt=lambda t: f"{t:g}")
        for key, ser in dyn[cond]["regret"].items():
            col = CYL if key.startswith("cyl") else SQ
            pts = " ".join(f"{ax(steps.index(s)):.1f},{ay2(max(v, 0.001)):.1f}" for s, v in ser)
            b += f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="1.8" stroke-opacity="0.9"/>'
        gc = {"O": (0.2649, 0.2360), "P": (0.2658, 0.3248)}[cond]
        for g, col in zip(gc, (CYL, SQ)):
            b += f'<line x1="{x0}" y1="{ay2(g):.1f}" x2="{x1}" y2="{ay2(g):.1f}" stroke="{col}" stroke-width="1.2" stroke-dasharray="5 4"/>'
        b += T(x1, ay2(max(gc)) - 5, "G_C", anchor="right", size=11, fill=INK2)
        b += f'<line x1="{x0}" y1="{yb2}" x2="{x1}" y2="{yb2}" stroke="{INK2}"/>'
        for i, s in enumerate(steps):
            if i in (0, 1, 2, 3, 4, 6, 8, 11):
                for yy in (yb, yb2):
                    b += T(ax(i), yy + 15, str(s), size=10.5, fill=INK2)
    b += T(340, 492, "צעד אימון (נקודות הבדיקה במרווחים שווים; הפריסה עצמה לוגריתמית)", size=11.5, fill=INK2)
    b += legend(560, 514, [("גליל (3 חזרות)", CYL, "line"), ("ריבוע (3 חזרות)", SQ, "line"),
                           ("G_C (מקווקו)", INK2, "dash")])
    return svg(W, H, b, "דינמיקת אימון")


def chart_layers():
    """reports/E3/summary.md layer sweep: median D per replicate, per hook."""
    hooks = ["embed", "resid_post_0", "resid_post_1", "resid_post_2", "resid_post_3", "ln_final_out"]
    O = [(0.110, 0.104, 0.105), (0.130, 0.153, 0.161), (0.148, 0.184, 0.162), (0.175, 0.186, 0.172),
         (0.158, 0.176, 0.173), (0.283, 0.290, 0.273)]
    P = [(-0.040, 0.025, -0.003), (-0.003, 0.008, 0.003), (0.013, 0.002, -0.006), (-0.004, 0.044, 0.005),
         (0.021, 0.034, 0.034), (0.016, 0.043, 0.013)]
    W, H = 680, 270
    x0, x1, yb, yt = 70, 650, 210, 24
    ay = Axis(-0.05, 0.3, yb, yt)
    b = ygrid(ay, [-0.05, 0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3], x0, x1)
    b += f'<line x1="{x0}" y1="{ay(0):.1f}" x2="{x1}" y2="{ay(0):.1f}" stroke="{INK2}" stroke-width="1.3"/>'
    gw = (x1 - x0) / len(hooks)
    for cond, data, col in (("O", O, CYL), ("P", P, VIOLET)):
        meds = []
        for i, vals in enumerate(data):
            gx = x0 + i * gw + gw / 2
            for j, v in enumerate(vals):
                b += f'<circle cx="{gx + (j - 1) * 8:.1f}" cy="{ay(v):.1f}" r="4.2" fill="{col}" fill-opacity="0.85" stroke="{SURF}" stroke-width="1"/>'
            meds.append((gx, float(np.median(vals))))
        b += '<polyline points="' + " ".join(f"{x:.1f},{ay(v):.1f}" for x, v in meds) + f'" fill="none" stroke="{col}" stroke-width="1.6" stroke-opacity="0.6"/>'
    for i, h in enumerate(hooks):
        gx = x0 + i * gw + gw / 2
        b += T(gx, yb + 18, h, size=11.5, fill=INK, weight=700 if h == "resid_post_3" else 400)
    b += T(22, 120, "D", size=13, italic=True, fill=INK2)
    b += legend(650, 262, [("O (3 חזרות)", CYL, "dot"), ("P (3 חזרות)", VIOLET, "dot")])
    return svg(W, H, b, "סריקת שכבות")


def chart_probes():
    """reports/E4/summary.md §4 (median test R² over 6 runs)."""
    rows = [("אקטיבציות בסוף האימון ← b³²", 0.829, 0.378), ("עתיד מדויק F₁ ← b³²", 0.838, 0.382),
            ("אקטיבציות באתחול ← b³²", 0.483, 0.167), ("הסמל האחרון (one-hot) ← b³²", 0.421, 0.144),
            ("אקטיבציות בסוף ← אמונת סמל אחרון", 0.974, 0.825), ("אקטיבציות ← b³² מעורבב (בקרה)", -0.010, -0.027)]
    W, H = 680, 330
    xl, xr = 40, 450
    ax = Axis(0, 1.0, xl, xr)
    b = ""
    for t in (0, 0.25, 0.5, 0.75, 1.0):
        b += f'<line x1="{ax(t):.1f}" y1="20" x2="{ax(t):.1f}" y2="290" stroke="{GRID}"/>'
        b += T(ax(t), 306, f"{t:.2f}", size=11, fill=INK2)
    for i, (name, o, p) in enumerate(rows):
        y = 30 + i * 44
        b += T(670, y + 16, name, anchor="right", size=12.5, weight=700 if i < 2 else 400)
        for j, (v, col) in enumerate(((o, CYL), (p, VIOLET))):
            yy = y + j * 15
            w = max(0, ax(v) - xl)
            b += f'<rect x="{xl}" y="{yy}" width="{w:.1f}" height="12" rx="2" fill="{col}"/>'
            b += T(xl + w + 5, yy + 10.5, f"{v:.3f}", anchor="left", size=11, fill=INK)
    b += T(245, 324, "R² על נתוני המבחן (חציון על 6 ריצות)", size=11.5, fill=INK2)
    b += legend(670, 324, [("O", CYL, "sq"), ("P", VIOLET, "sq")])
    return svg(W, H, b, "probes")


def chart_circular():
    """reports/E4/summary.md §5 (median agreement with the latent x angle)."""
    rows = [("O גליל, צעד 0", 0.069, CYL, 0.4), ("O גליל, צעד 5000", 0.891, CYL, 1),
            ("O גליל 5000, ציר y (בקרה)", 0.097, MUTED, 1), ("O ריבוע, צעד 5000", 0.256, SQ, 1),
            ("P גליל, צעד 5000", 0.053, VIOLET, 1), ("U גליל, צעד 5000", 0.601, AQUA, 1),
            ("אמונה מדויקת b³² (תקרה, O)", 0.915, INK2, 1)]
    W, H = 680, 330
    xl, xr = 40, 450
    ax = Axis(0, 1.0, xl, xr)
    b = ""
    for t in (0, 0.25, 0.5, 0.75, 1.0):
        b += f'<line x1="{ax(t):.1f}" y1="14" x2="{ax(t):.1f}" y2="300" stroke="{GRID}"/>'
        b += T(ax(t), 316, f"{t:.2f}", size=11, fill=INK2)
    for i, (name, v, col, op) in enumerate(rows):
        y = 22 + i * 40
        b += T(670, y + 15, name, anchor="right", size=12.5, weight=700 if i == 1 else 400)
        w = ax(v) - xl
        b += f'<rect x="{xl}" y="{y + 2}" width="{w:.1f}" height="18" rx="3" fill="{col}" fill-opacity="{op}"/>'
        b += T(xl + w + 5, y + 16, f"{v:.3f}", anchor="left", size=12)
    return svg(W, H, b, "קואורדינטות מעגליות")


def chart_oracle():
    """README 'After E4', oracle profile job 0014 (calibration)."""
    K = [1, 2, 4, 8, 16]
    B = [0.369, 0.198, 0.067, 0.0092, 0.00018]
    W, H = 680, 250
    x0, x1, yb, yt = 80, 640, 200, 20
    ax = Axis(1, 16, x0, x1, log=True)
    ay = Axis(0.0001, 1, yb, yt, log=True)
    b = ygrid(ay, [0.0001, 0.001, 0.01, 0.1, 1], x0, x1, fmt=lambda t: f"{t:g}")
    b += f'<line x1="{x0}" y1="{ay(0.01):.1f}" x2="{x1}" y2="{ay(0.01):.1f}" stroke="{BAD}" stroke-width="1.4" stroke-dasharray="5 4"/>'
    b += T(x1, ay(0.01) - 6, "ערך ייחוס 0.01", anchor="right", size=11.5, fill=BAD)
    pts = " ".join(f"{ax(k):.1f},{ay(v):.1f}" for k, v in zip(K, B))
    b += f'<polyline points="{pts}" fill="none" stroke="{AQUA}" stroke-width="2.2"/>'
    for k, v in zip(K, B):
        b += f'<circle cx="{ax(k):.1f}" cy="{ay(v):.1f}" r="5" fill="{AQUA}" stroke="{SURF}" stroke-width="1.5"/>'
        b += T(ax(k) + (8 if k < 16 else -8), ay(v) - 8, f"{v:g}", anchor="left" if k < 16 else "right", size=11.5)
        b += T(ax(k), yb + 17, f"K = {k}", size=11.5, fill=INK2)
    b += f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{INK2}"/>'
    b += T(340, 244, "סקאלה לוגריתמית בשני הצירים; בנקודה K = 32 הערך הוא 0 בהגדרה", size=11.5, fill=INK2)
    return svg(W, H, b, "פרופיל האורקל")


ALL = {
    "pipeline": fig_pipeline, "stages": fig_stages, "decision": fig_decision,
    "followups": fig_followups, "world": fig_world, "emission": fig_emission, "ph": fig_ph,
    "dcontrast": fig_dcontrast, "e0": chart_e0, "e1": chart_e1, "f1panels": chart_f1_panels,
    "baselines": chart_baselines, "dynamics": chart_dynamics, "layers": chart_layers,
    "probes": chart_probes, "circular": chart_circular, "oracle": chart_oracle,
}


def render_all() -> dict[str, str]:
    return {k: f() for k, f in ALL.items()}

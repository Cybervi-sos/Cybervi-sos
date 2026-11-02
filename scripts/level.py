"""Nível e XP ligados ao total de commits (curva progressiva).

Cada nível pede 25 commits a mais que o anterior:
Lv2 = 25, Lv3 = 75, Lv4 = 150, Lv5 = 250, Lv6 = 375 ...
"""
import re
from pathlib import Path
from textpath import paths

STEP = 25


def threshold(level):
    """Commits totais necessários para alcançar `level`."""
    return STEP * level * (level - 1) // 2


def level_info(commits):
    lv = 1
    while threshold(lv + 1) <= commits:
        lv += 1
    have = commits - threshold(lv)
    need = threshold(lv + 1) - threshold(lv)
    return lv, have, need


def _bar(x, y, w, h, frac, color, rx):
    fw = max(h, w * frac) if frac > 0 else 0
    cid = f"xpc{int(x)}{int(y)}"
    return (f'<rect x="{x}" y="{y}" width="{fw:.1f}" height="{h}" rx="{rx}" fill="{color}"/>'
            f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{fw:.1f}" height="{h}" rx="{rx}"/></clipPath>'
            f'<g clip-path="url(#{cid})"><rect class="lvsh" x="{x}" y="{y}" width="40" height="{h}" fill="#fff6d0" opacity=".6"/></g>')


STYLE = ('<style>.lvsh{animation:lvsh 3.5s ease-in-out infinite}'
         '@keyframes lvsh{0%{transform:translateX(-40px)}60%,100%{transform:translateX(330px)}}</style>')


def banner_fragment(commits):
    lv, have, need = level_info(commits)
    return (STYLE
            + paths(f"Lv. {lv:02d}", 924, 47, 22, "#f6dec0")
            + paths(f"{have} / {need} XP", 1202, 47, 18, "#f0dcc4", "end")
            + _bar(893, 58.5, 309, 12.5, have / need, "#df7d4e", 6))


def ficha_fragment(commits):
    lv, have, need = level_info(commits)
    return (STYLE
            + paths(f"Lv. {lv:02d}", 40, 312, 24, "#f3c77a")
            + paths(f"{have} / {need} XP", 266, 312, 20, "#c9a98a", "end")
            + _bar(42, 324, 222, 10, have / need, "#f3c77a", 5))


def inject(svg_path, fragment):
    p = Path(svg_path)
    s = p.read_text(encoding="utf-8")
    new, n = re.subn(r"<!--LV-->.*?<!--/LV-->", lambda m: f"<!--LV-->{fragment}<!--/LV-->", s, flags=re.S)
    if n != 1:
        raise SystemExit(f"marcador de nível não encontrado em {svg_path}")
    p.write_text(new, encoding="utf-8")


def apply(root, commits):
    inject(Path(root) / "assets" / "banner.svg", banner_fragment(commits))
    inject(Path(root) / "assets" / "library-ficha.svg", ficha_fragment(commits))
    return level_info(commits)

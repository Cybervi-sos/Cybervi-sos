"""Converte <text class="t ..."> em contornos (paths) da fonte VT323.

Imagens SVG exibidas com <img> (como no README do GitHub) às vezes são desenhadas
antes de a fonte embutida carregar, e o texto some. Com contornos, o texto aparece sempre.
"""
import re
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

_FONT = TTFont(str(Path(__file__).with_name("VT323-Regular.ttf")))
_UPM = _FONT["head"].unitsPerEm
_CMAP = _FONT.getBestCmap()
_GS = _FONT.getGlyphSet()
_HMTX = _FONT["hmtx"]

ENT = {"&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"'}


def _glyph(name):
    pen = SVGPathPen(_GS)
    _GS[name].draw(pen)
    return pen.getCommands()


def width(text, size):
    return sum(_HMTX[_CMAP.get(ord(c), _CMAP[ord("?")])][0] for c in text) * size / _UPM


def _attr(tag, name, default=None):
    m = re.search(rf'\s{name}="([^"]*)"', tag)
    return m.group(1) if m else default


def convert(svg):
    used = {}

    def repl(m):
        tag, raw = m.group(1), m.group(2)
        cls = _attr(tag, "class", "")
        if "t" not in cls.split():
            return m.group(0)
        text = raw
        for k, v in ENT.items():
            text = text.replace(k, v)
        x = float(_attr(tag, "x", "0")); y = float(_attr(tag, "y", "0"))
        size = float(_attr(tag, "font-size", "16"))
        anchor = _attr(tag, "text-anchor", "start")
        w = width(text, size)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        s = size / _UPM
        uses = []
        cx = x
        for ch in text:
            gname = _CMAP.get(ord(ch), _CMAP[ord("?")])
            if ch != " ":
                gid = "g" + str(_FONT.getGlyphID(gname))
                used[gid] = gname
                uses.append(f'<use href="#{gid}" transform="translate({cx:.1f} {y:.1f}) scale({s:.4f} {-s:.4f})"/>')
            cx += _HMTX[gname][0] * s
        keep = []
        for a in ("fill", "opacity", "transform", "style"):
            v = _attr(tag, a)
            if v is not None:
                keep.append(f'{a}="{v}"')
        other = " ".join(c for c in cls.split() if c != "t")
        if other:
            keep.append(f'class="{other}"')
        return f'<g {" ".join(keep)}>{"".join(uses)}</g>'

    svg = re.sub(r"<text(\s[^>]*)>(.*?)</text>", repl, svg, flags=re.S)
    defs = "".join(f'<path id="{gid}" d="{_glyph(name)}"/>' for gid, name in used.items())
    svg = re.sub(r"@font-face\{[^}]*\}", "", svg)
    return svg.replace("<style>", f"<defs>{defs}</defs><style>", 1)

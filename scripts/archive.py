"""Gera os painéis "The Archive" (estatísticas, idiomas, sequência e contribuições)
no mesmo tema do README. Depende apenas de fonttools (pip install fonttools).

Uso:
  GITHUB_TOKEN=... python scripts/archive.py Cybervi-sos     # dados reais (GitHub Actions)
  python scripts/archive.py --demo                           # dados de exemplo
"""
import json, os, random, sys, urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
sys.path.insert(0, str(Path(__file__).parent))
from textpath import convert  # noqa: E402
import level  # noqa: E402

C = dict(panel="#1f111b", line="#b9823f", line2="#5a3326", cream="#f6e3c3", gold="#f3c77a",
         amber="#ff9c3a", muted="#c9a98a", plum="#3a1f33", green="#7fd39a")
HEAT = ["#2a1822", "#5a3326", "#8a4b28", "#c98a3e", "#f3c77a"]
LANG_COLORS = ["#f3c77a", "#ff9c3a", "#e8768f", "#8fd6d8", "#c9a2f0", "#bfe39a"]

CSS = """.t{font-family:VT,'Consolas','Courier New',monospace}
.sp{animation:sp 2.6s ease-in-out infinite}@keyframes sp{0%,100%{opacity:.15;transform:scale(.4)}50%{opacity:1;transform:scale(1)}}
.du{opacity:0;animation:du ease-in-out infinite}@keyframes du{0%,100%{opacity:0;transform:translateY(0)}50%{opacity:.8;transform:translateY(-12px)}}
"""


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def spark(x, y, s, d=0):
    return (f'<path class="sp" style="animation-delay:-{d}s;transform-origin:{x}px {y}px" '
            f'd="M{x} {y-s}L{x+s*.28} {y-s*.28}L{x+s} {y}L{x+s*.28} {y+s*.28}L{x} {y+s}'
            f'L{x-s*.28} {y+s*.28}L{x-s} {y}L{x-s*.28} {y-s*.28}Z" fill="{C["gold"]}"/>')


def dust(w, h, n, rnd):
    return "".join(f'<rect class="du" x="{rnd.randint(30, w-30)}" y="{rnd.randint(30, h-30)}" width="3" height="3" '
                   f'fill="#ffe6a3" style="animation-duration:{rnd.uniform(3, 6):.1f}s;'
                   f'animation-delay:-{rnd.uniform(0, 6):.1f}s"/>' for _ in range(n))


def frame(w, h):
    corners = "".join(f'<rect x="{x}" y="{y}" width="10" height="10" fill="{C["line"]}" transform="rotate(45 {x+5} {y+5})"/>'
                      for x, y in ((6, 6), (w-16, 6), (6, h-16), (w-16, h-16)))
    return (f'<rect x="3" y="3" width="{w-6}" height="{h-6}" rx="14" fill="{C["panel"]}" stroke="{C["line"]}" stroke-width="3"/>'
            f'<rect x="12" y="12" width="{w-24}" height="{h-24}" rx="9" fill="none" stroke="{C["line2"]}" stroke-width="1.5"/>{corners}')


def header(sub, w):
    scroll = (f'<g transform="translate(36 26)"><rect x="4" y="0" width="30" height="38" rx="3" fill="#e0c79a"/>'
              f'<rect x="0" y="-4" width="38" height="8" rx="4" fill="{C["gold"]}"/><rect x="0" y="34" width="38" height="8" rx="4" fill="{C["gold"]}"/>'
              f'<path d="M10 10h18M10 17h18M10 24h12" stroke="#8a5a3a" stroke-width="2.5"/></g>')
    return (f'{scroll}<text x="86" y="52" class="t" font-size="34" fill="{C["gold"]}">The Archive</text>'
            f'<text x="262" y="52" class="t" font-size="26" fill="{C["muted"]}">· {esc(sub)}</text>'
            f'<path d="M30 70 H{w-30}" stroke="{C["line2"]}" stroke-width="2" stroke-dasharray="2 6"/>')


def svg(w, h, body, css="", label=""):
    return convert(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{esc(label)}"><style>{CSS}{css}</style>{body}</svg>')


def demo_tag(w, demo):
    if True:  # sem selo de exemplo nos painéis
        return ""
    return (f'<rect x="{w-262}" y="26" width="216" height="28" rx="6" fill="#120a0e" stroke="{C["line2"]}"/>'
            f'<text x="{w-154}" y="47" class="t" font-size="20" fill="{C["muted"]}" text-anchor="middle">DADOS DE EXEMPLO</text>')


# ------------------------------------------------------------------ dados
QUERY = """query($login:String!){user(login:$login){
 followers{totalCount}
 repositories(ownerAffiliations:OWNER,isFork:false,first:100,privacy:PUBLIC){totalCount nodes{name stargazerCount
  languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}}}
 contributionsCollection{totalCommitContributions totalPullRequestContributions totalIssueContributions
  contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""


def fetch(login, token):
    req = urllib.request.Request("https://api.github.com/graphql",
                                 data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
                                 headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    u = json.load(urllib.request.urlopen(req))["data"]["user"]
    langs = {}
    for r in u["repositories"]["nodes"]:
        if r["name"].lower() == login.lower():
            continue  # ignora o repositório do perfil (scripts da automação)
        for e in r["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    cc = u["contributionsCollection"]
    days = [(date.fromisoformat(d["date"]), d["contributionCount"])
            for wk in cc["contributionCalendar"]["weeks"] for d in wk["contributionDays"]]
    return dict(repos=u["repositories"]["totalCount"],
                stars=sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
                followers=u["followers"]["totalCount"], commits=cc["totalCommitContributions"],
                prs=cc["totalPullRequestContributions"], issues=cc["totalIssueContributions"],
                total=cc["contributionCalendar"]["totalContributions"], langs=langs, days=days)


def total_commits(login, token):
    """Soma os commits de todos os anos desde a criação da conta (o nível nunca cai)."""
    def q(query, variables):
        req = urllib.request.Request("https://api.github.com/graphql",
                                     data=json.dumps({"query": query, "variables": variables}).encode(),
                                     headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
        return json.load(urllib.request.urlopen(req))["data"]["user"]
    created = int(q("query($login:String!){user(login:$login){createdAt}}", {"login": login})["createdAt"][:4])
    now = date.today().year
    parts = [f'y{y}:contributionsCollection(from:"{y}-01-01T00:00:00Z",to:"{y}-12-31T23:59:59Z"){{totalCommitContributions}}'
             for y in range(created, now + 1)]
    u = q("query($login:String!){user(login:$login){" + " ".join(parts) + "}}", {"login": login})
    return sum(v["totalCommitContributions"] for v in u.values())


def demo_data():
    rnd = random.Random(4)
    end = date(2026, 11, 1)
    start = end - timedelta(days=end.weekday() + 1 + 52 * 7)
    days = []
    d = start
    while d <= end:
        recent = (end - d).days < 100
        p = .55 if recent else .12
        days.append((d, rnd.choice([1, 1, 2, 3, 4, 6]) if rnd.random() < p else 0))
        d += timedelta(days=1)
    for k in range(5):
        days[-1 - k] = (days[-1 - k][0], max(1, days[-1 - k][1]))
    return dict(repos=6, stars=3, followers=8, commits=sum(c for _, c in days) - 9, prs=4, issues=5,
                total=sum(c for _, c in days), days=days,
                langs={"Python": 42000, "HTML": 26000, "CSS": 14000, "JavaScript": 9000, "SQL": 5000})


def streaks(days):
    cur = best = run = 0
    for _, c in days:
        run = run + 1 if c else 0
        best = max(best, run)
    i = len(days) - 1
    if days and days[i][1] == 0:  # hoje ainda sem contribuição não quebra a sequência
        i -= 1
    while i >= 0 and days[i][1]:
        cur += 1
        i -= 1
    return cur, best


# ------------------------------------------------------------------ painéis
def panel_stats(d, demo):
    W, H, rnd = 1000, 360, random.Random(1)
    s = [frame(W, H), header("Estatísticas & Idiomas", W), demo_tag(W, demo)]
    icons = {
        "commit": f'<circle cx="0" cy="0" r="6" fill="none" stroke="{C["gold"]}" stroke-width="3"/><path d="M-14 0h8M6 0h8" stroke="{C["gold"]}" stroke-width="3"/>',
        "repo": f'<path d="M-9 -11h16v22h-16z" fill="none" stroke="{C["gold"]}" stroke-width="3"/><path d="M-9 6h16" stroke="{C["gold"]}" stroke-width="2"/>',
        "star": f'<path d="M0 -11l3.2 7 7.6.8-5.7 5.1 1.7 7.5L0 5.6l-6.8 3.8 1.7-7.5-5.7-5.1 7.6-.8z" fill="{C["gold"]}"/>',
        "pr": f'<circle cx="-6" cy="-8" r="3.5" fill="none" stroke="{C["gold"]}" stroke-width="2.5"/><circle cx="-6" cy="9" r="3.5" fill="none" stroke="{C["gold"]}" stroke-width="2.5"/><circle cx="7" cy="9" r="3.5" fill="none" stroke="{C["gold"]}" stroke-width="2.5"/><path d="M-6 -4v9M7 5v-9h-6" fill="none" stroke="{C["gold"]}" stroke-width="2.5"/>',
        "issue": f'<circle r="10" fill="none" stroke="{C["gold"]}" stroke-width="3"/><circle r="3" fill="{C["gold"]}"/>',
        "people": f'<circle cx="-5" cy="-5" r="5" fill="{C["gold"]}"/><circle cx="7" cy="-3" r="4" fill="{C["gold"]}" opacity=".7"/><path d="M-14 10q9-12 18 0M2 10q6-9 12 0" fill="none" stroke="{C["gold"]}" stroke-width="3"/>',
    }
    rows = [("commit", "Commits no último ano", d["commits"]), ("repo", "Repositórios", d["repos"]),
            ("star", "Estrelas recebidas", d["stars"]), ("pr", "Pull requests", d["prs"]),
            ("issue", "Issues abertas", d["issues"]), ("people", "Seguidores", d["followers"])]
    for i, (ic, lab, val) in enumerate(rows):
        col, row = i % 2, i // 2
        x, y = 40 + col * 236, 96 + row * 82
        s.append(f'<g class="tile" style="animation-delay:{i*.4}s"><rect x="{x}" y="{y}" width="222" height="70" rx="10" '
                 f'fill="{C["plum"]}" fill-opacity=".55" stroke="{C["line"]}" stroke-width="1.5"/></g>'
                 f'<g transform="translate({x+30} {y+35})">{icons[ic]}</g>'
                 f'<text x="{x+58}" y="{y+38}" class="t" font-size="34" fill="{C["cream"]}">{val}</text>'
                 f'<text x="{x+58}" y="{y+58}" class="t" font-size="18" fill="{C["muted"]}">{esc(lab)}</text>')
    # idiomas
    s.append(f'<path d="M530 92V330" stroke="{C["line2"]}" stroke-width="2" stroke-dasharray="2 6"/>')
    s.append(f'<text x="560" y="108" class="t" font-size="22" fill="{C["gold"]}">IDIOMAS DO GRIMÓRIO</text>')
    tot = sum(d["langs"].values()) or 1
    top = sorted(d["langs"].items(), key=lambda kv: -kv[1])[:6]
    if not top:
        s.append(f'<text x="560" y="150" class="t" font-size="22" fill="{C["muted"]}">Nenhum código público ainda.</text>')
    y = 136
    for i, (name, size) in enumerate(top):
        pct = size * 100 / tot
        w = max(4, 340 * pct / 100)
        col = LANG_COLORS[i % len(LANG_COLORS)]
        s.append(f'<text x="560" y="{y}" class="t" font-size="22" fill="{C["cream"]}">{esc(name)}</text>'
                 f'<text x="958" y="{y}" class="t" font-size="20" fill="{C["muted"]}" text-anchor="end">{pct:.1f}%</text>'
                 f'<rect x="560" y="{y+6}" width="398" height="10" rx="5" fill="#0d060b"/>'
                 f'<rect class="bar" style="animation-delay:{i*.15}s" x="560" y="{y+6}" width="{w*398/340:.1f}" height="10" rx="5" fill="{col}"/>')
        y += 38
    s.append(spark(W-60, 86, 6, .4) + spark(500, 330, 5, 1.3) + dust(W, H, 8, rnd))
    css = (".bar{animation:bar 3.6s ease-in-out infinite}@keyframes bar{0%,100%{opacity:1}50%{opacity:.6}}"
           ".tile rect{animation:tl 4.8s ease-in-out infinite;animation-delay:inherit}"
           "@keyframes tl{0%,80%,100%{fill-opacity:.55}10%{fill-opacity:1}}")
    return svg(W, H, "".join(s), css, "The Archive: estatísticas e idiomas")


def panel_activity(d, demo):
    W, H, rnd = 1000, 380, random.Random(2)
    days = d["days"]
    cur, best = streaks(days)
    s = [frame(W, H), header("Sequência & Contribuições", W), demo_tag(W, demo)]
    # contadores
    flame = (f'<g class="fire"><path d="M0 14c-12 0-16-10-10-20 2 6 6 6 6 1 0-8 6-12 6-18 8 6 14 16 10 26-2 7-6 11-12 11z" fill="{C["amber"]}"/>'
             f'<path d="M0 12c-5 0-7-5-4-10 2 3 4 2 4 0 0-3 2-5 2-7 4 4 5 9 3 13-1 3-3 4-5 4z" fill="#ffe08a"/></g>')
    boxes = [("Contribuições no último ano", d["total"], None), ("Sequência atual", f"{cur} dia" + ("" if cur == 1 else "s"), flame),
             ("Maior sequência", f"{best} dia" + ("" if best == 1 else "s"), None)]
    for i, (lab, val, ic) in enumerate(boxes):
        x = 40 + i * 312
        hl = i == 1
        s.append(f'<rect x="{x}" y="90" width="296" height="84" rx="10" fill="{C["plum"]}" fill-opacity="{.9 if hl else .55}" '
                 f'stroke="{C["gold"] if hl else C["line"]}" stroke-width="{2.5 if hl else 1.5}"/>')
        if ic:
            s.append(f'<g transform="translate({x+38} 134)">{ic}</g>')
        tx = x + (70 if ic else 22)
        s.append(f'<text x="{tx}" y="134" class="t" font-size="38" fill="{C["cream"]}">{esc(val)}</text>'
                 f'<text x="{tx}" y="160" class="t" font-size="20" fill="{C["muted"]}">{esc(lab)}</text>')
    # mapa de calor (estantes)
    weeks = []
    for dt, c in days:
        if not weeks or dt.weekday() == 6:
            weeks.append([])
        weeks[-1].append((dt, c))
    weeks = weeks[-53:]
    mx = max([c for _, c in days] + [1])
    cell, gap = 13, 4
    gx0 = (W - (len(weeks) * (cell + gap) - gap)) / 2
    gy0 = 214
    meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    last_m = None
    for wi, wk in enumerate(weeks):
        x = gx0 + wi * (cell + gap)
        m = wk[0][0].month
        if m != last_m and wi < len(weeks) - 2:
            s.append(f'<text x="{x}" y="{gy0-10}" class="t" font-size="18" fill="{C["muted"]}">{meses[m-1]}</text>')
            last_m = m
        for dt, c in wk:
            lvl = 0 if c == 0 else min(4, 1 + int(3 * c / mx))
            y = gy0 + ((dt.weekday() + 1) % 7) * (cell + gap)
            cls = ' class="cell"' if c else ""
            s.append(f'<rect{cls} x="{x:.1f}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{HEAT[lvl]}" '
                     f'style="animation-delay:{(wi*0.05):.2f}s"/>')
    ly = gy0 + 7 * (cell + gap) + 18
    s.append(f'<text x="{W-40-5*(cell+gap)-62}" y="{ly+11}" class="t" font-size="18" fill="{C["muted"]}" text-anchor="end">menos</text>')
    for i, col in enumerate(HEAT):
        s.append(f'<rect x="{W-40-5*(cell+gap)+i*(cell+gap)-52}" y="{ly}" width="{cell}" height="{cell}" rx="2" fill="{col}"/>')
    s.append(f'<text x="{W-40}" y="{ly+11}" class="t" font-size="18" fill="{C["muted"]}" text-anchor="end">mais</text>')
    s.append(f'<text x="{gx0}" y="{ly+11}" class="t" font-size="18" fill="{C["muted"]}">Cada quadradinho é um dia na biblioteca.</text>')
    s.append(spark(W-60, 86, 6, .4) + spark(40, 200, 5, 1.3) + dust(W, H, 8, rnd))
    css = (".fire{transform-origin:0 14px;animation:fi .7s ease-in-out infinite alternate}"
           "@keyframes fi{from{transform:scale(.92,.9) rotate(-3deg)}to{transform:scale(1.05,1.08) rotate(3deg)}}"
           ".cell{animation:ce 6s ease-in-out infinite}"
           "@keyframes ce{0%,12%,100%{filter:none}5%{filter:brightness(1.6)}}")
    return svg(W, H, "".join(s), css, "The Archive: sequência e contribuições")


def main():
    demo = "--demo" in sys.argv
    if demo:
        data = demo_data()
    else:
        login = next((a for a in sys.argv[1:] if not a.startswith("-")), os.environ.get("GITHUB_REPOSITORY_OWNER"))
        data = fetch(login, os.environ["GITHUB_TOKEN"])
    OUT.mkdir(exist_ok=True)
    (OUT / "archive-estatisticas.svg").write_text(panel_stats(data, demo), encoding="utf-8")
    (OUT / "archive-atividade.svg").write_text(panel_activity(data, demo), encoding="utf-8")
    commits = data["commits"] if demo else total_commits(login, os.environ["GITHUB_TOKEN"])
    lv, have, need = level.apply(ROOT, commits)
    print("ok", "demo" if demo else "dados reais", f"| {commits} commits -> Lv. {lv} ({have}/{need} XP)")


if __name__ == "__main__":
    main()

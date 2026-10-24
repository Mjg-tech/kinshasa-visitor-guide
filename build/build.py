# -*- coding: utf-8 -*-
"""Build the Kinshasa Visitor Guide.

  python build.py            -> ../index.html (standalone page, for GitHub Pages or any web host)
  python build.py --artifact <path>   -> also writes the fragment used for the claude.ai Artifact

Content lives in places.py and ui.py. Nothing here invents facts.
"""
import html
import pathlib
import re
import sys
import unicodedata
import urllib.parse

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import places as PL  # noqa: E402
import ui as U  # noqa: E402

NB, NNB = " ", " "


# ------------------------------------------------------------------ text helpers
def esc(s):
    return html.escape(s, quote=True)


def fr_typo(s):
    """French typography: no-break spaces before : ; ! ? » and inside numbers/units."""
    s = s.replace("« ", "«" + NNB).replace(" »", NNB + "»")
    s = re.sub(r" ([;!?])", NNB + r"\1", s)
    s = re.sub(r" (:)", NB + r"\1", s)
    s = re.sub(r"(\d) h (\d)", r"\1" + NB + "h" + NB + r"\2", s)
    s = re.sub(r"(?<=\d) (?=\d{3}(?!\d))", NB, s)
    s = re.sub(r"(?<=\d) (?=(?:h|km|m|ha|FC|\$|%)(?![A-Za-zÀ-ÿ]))", NB, s)
    return s


def bi(en_html, fr_html):
    return f'<span lang="en">{en_html}</span><span lang="fr">{fr_html}</span>'


def tx(pair):
    """(en, fr) plain text -> escaped bilingual spans."""
    return bi(esc(pair[0]), esc(fr_typo(pair[1])))


def tx_html(pair):
    """(en, fr) trusted HTML -> bilingual spans (French typography applied to text only via fr_typo)."""
    return bi(pair[0], fr_typo(pair[1]))


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def fr_num(s):
    return s.replace(".", ",")


# ------------------------------------------------------------------ rendering
SEP = '<span class="sep" aria-hidden="true">·</span>'


def map_url(p):
    """Google Maps search link: explicit query when given, else name + district + Kinshasa."""
    if isinstance(p["maps"], str):
        q = p["maps"]
    else:
        q = f'{p["name"]} {p["area"]}'.strip()
        if "kinshasa" not in q.lower():
            q += " Kinshasa"
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote_plus(q)


def render_link(kind, url, en, fr, name_html):
    label = (en, fr) if en else U.LINK_LABELS[kind]
    sr = f'<span class="sr"> — {name_html}</span>'
    return (f'<li><a class="lk lk-{kind}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">'
            f'{tx(label)}<svg class="ic" aria-hidden="true"><use href="#i-ext"/></svg>{sr}</a></li>')


def render_place(p, stats):
    stats["places"] += 1
    name_html = bi(esc(p["name"]), esc(fr_typo(p["name_fr"]))) if p["name_fr"] else esc(p["name"])
    badge_html = ""
    badge_text = []
    if p["badges"]:
        items = []
        for k in p["badges"]:
            en, fr, cls = U.BADGES[k]
            items.append(f'<li class="bd bd-{cls}">{tx((en, fr))}</li>')
            badge_text += [en, fr]
        badge_html = f'<ul class="badges">{"".join(items)}</ul>'

    meta = []
    if p["area"]:
        meta.append(f'<span>{esc(p["area"])}</span>')
    if p["kind"]:
        meta.append(tx(p["kind"]))
    if p["rating"]:
        score, n = p["rating"]
        meta.append(bi(esc(f"TripAdvisor ★ {score} ({n})"), esc(f"TripAdvisor ★ {fr_num(score)} ({n})")))
    if p["price"]:
        meta.append(f'<span>{esc(p["price"])}</span>')
    meta_html = f'<p class="meta">{SEP.join(meta)}</p>' if meta else ""

    facts_html = ""
    if p["facts"]:
        facts_html = f'<p class="facts"><strong>{tx(U.UI["facts"])}</strong>{tx(p["facts"])}</p>'

    links = []
    for lk in p["links"]:
        kind, url, en, fr = lk
        links.append(render_link(kind, url, en, fr, name_html))
        stats["links"].add(url)
    if p["maps"] is not False:
        url = map_url(p)
        links.append(f'<li><a class="lk lk-map" href="{esc(url)}" target="_blank" rel="noopener noreferrer">'
                     f'{tx(U.UI["map"])}<svg class="ic" aria-hidden="true"><use href="#i-pin"/></svg>'
                     f'<span class="sr"> — {name_html}</span></a></li>')
        stats["links"].add(url)

    blob = norm(" ".join(filter(None, [
        p["name"], p["name_fr"] or "", p["area"], *(p["kind"] or ()), p["en"], p["fr"], *(p["facts"] or ()), *badge_text,
        p["price"] or "", " ".join(f"{l[2] or ''} {l[3] or ''}" for l in p["links"]),
    ])))
    return (
        f'<article class="place" id="{esc(p["slug"])}" data-area="{esc(p["area"])}" data-q="{esc(blob)}">'
        f'<div class="place-head"><h4>{name_html}</h4>{badge_html}</div>'
        f'{meta_html}'
        f'<p class="desc">{bi(esc(p["en"]), esc(fr_typo(p["fr"])))}</p>'
        f'{facts_html}'
        f'<ul class="links">{"".join(links)}</ul>'
        f'</article>'
    )


def render_group(g, stats):
    more = ""
    if g.get("more"):
        en, fr, url = g["more"]
        stats["links"].add(url)
        more = (f'<p class="more"><a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{tx((en, fr))}'
                f'<svg class="ic" aria-hidden="true"><use href="#i-ext"/></svg></a></p>')
    items = "".join(render_place(p, stats) for p in g["items"])
    return (f'<div class="group" id="{g["id"]}"><h3 class="group-title">{tx(g["title"])}</h3>'
            f'<div class="grid">{items}</div>{more}</div>')


def render_section(s, stats):
    groups = "".join(render_group(g, stats) for g in s["groups"])
    return (f'<section class="sec" id="{s["id"]}" data-cat="{s["cat"]}" data-has-places>'
            f'<header class="sec-head"><h2>{tx(s["title"])}</h2><p class="sec-intro">{tx(s["intro"])}</p></header>'
            f'{groups}</section>')


def render_travel():
    blocks = "".join(
        f'<div class="adv-block"><h3>{tx(b["h"])}</h3><p>{tx_html((b["en"], b["fr"]))}</p></div>'
        for b in U.TRAVEL_BLOCKS)
    return (f'<section class="advisory" id="travel" aria-labelledby="travel-h">'
            f'<h2 id="travel-h">{tx(U.TRAVEL_H)}</h2><p class="adv-lead">{tx(U.TRAVEL_LEAD)}</p>'
            f'<div class="adv-grid">{blocks}</div></section>')


def render_changes():
    items = "".join(f'<li>{tx_html(c)}</li>' for c in U.CHANGES)
    return (f'<section class="changes" id="changes" aria-labelledby="changes-h"><h2 id="changes-h">{tx(U.UI["changes_h"])}</h2>'
            f'<ul>{items}</ul></section>')


def render_legend():
    rows = []
    for key, en, fr in U.LEGEND:
        b_en, b_fr, cls = U.BADGES[key]
        rows.append(f'<li><span class="bd bd-{cls}">{tx((b_en, b_fr))}</span><span>{tx((en, fr))}</span></li>')
    return (f'<details class="legend"><summary>{tx(U.UI["legend"])}</summary><ul>{"".join(rows)}</ul></details>')


def render_plan(stats):
    cols = []
    for head, links in U.PLAN:
        lis = []
        for en, fr, url in links:
            stats["links"].add(url)
            lis.append(f'<li><a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{tx((en, fr))}'
                       f'<svg class="ic" aria-hidden="true"><use href="#i-ext"/></svg></a></li>')
        cols.append(f'<div><h3>{tx(head)}</h3><ul>{"".join(lis)}</ul></div>')
    return (f'<section class="sec plan" id="plan" data-cat="national"><header class="sec-head"><h2>{tx(U.UI["plan_h"])}</h2></header>'
            f'<div class="plan-grid">{"".join(cols)}</div><p class="plan-note">{tx(U.UI["plan_note"])}</p></section>')


def area_options(sections):
    present = set()
    for s in sections:
        for g in s["groups"]:
            for p in g["items"]:
                if p["area"]:
                    present.add(p["area"])
    order = [
        ("Kinshasa", ["Gombe", "Lingwala", "Limete", "Bandalungwa", "Bandal", "Ngaliema", "Mont-Ngafula", "N’djili", "Nsele", "Maluku"]),
        ("Kongo Central", ["Zongo", "Kisantu", "Mbanza-Ngungu", "Matadi", "Muanda"]),
        ("Haut-Katanga", ["Lubumbashi"]),
    ]
    out = [f'<option value="" data-en="{esc(U.UI["all_areas"][0])}" data-fr="{esc(U.UI["all_areas"][1])}">{esc(U.UI["all_areas"][0])}</option>']
    seen = set()
    for label, areas in order:
        opts = [a for a in areas if a in present]
        seen.update(opts)
        if opts:
            out.append(f'<optgroup label="{esc(label)}">' + "".join(f'<option value="{esc(a)}">{esc(a)}</option>' for a in opts) + "</optgroup>")
    missing = present - seen
    if missing:
        raise SystemExit(f"Areas missing from the filter order: {sorted(missing)}")
    return "".join(out)


SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
<symbol id="i-ext" viewBox="0 0 16 16"><path d="M6 3h7v7M13 3 5 11" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="i-pin" viewBox="0 0 16 16"><path d="M8 14s4.5-4.2 4.5-7.5a4.5 4.5 0 1 0-9 0C3.5 9.8 8 14 8 14Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle cx="8" cy="6.5" r="1.6" fill="currentColor"/></symbol>
<symbol id="i-search" viewBox="0 0 20 20"><circle cx="9" cy="9" r="5.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m13.2 13.2 4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
<symbol id="i-x" viewBox="0 0 16 16"><path d="m4 4 8 8M12 4l-8 8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24"><path d="m12 2.5 2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6L2.5 9.4l6.6-.8z" fill="currentColor"/></symbol>
</svg>"""

CSS_DARK = """--bg:#0B1A1D;--surface:#11262A;--tint:#143036;--ink:#E6F0EE;--ink-2:#B6CBC7;--ink-3:#93ACA7;
--line:#27413F;--link:#7CCBE3;--link-h:#B5E6F5;--focus:#7CCBE3;--bar:rgba(11,26,29,.93);
--hero-a:#0B4E73;--hero-b:#082F47;--hero-soft:#BCDDEB;--red:#E0505F;--yellow:#F3C534;
--warn-bg:#352B0B;--warn-line:#6B5A1C;--warn-ink:#F4E3A6;--bad-bg:#3A141B;--bad-line:#7A3340;--bad-ink:#F6C3CA;
--info-bg:#10343F;--info-ink:#BDE4F0;--ok-bg:#12351F;--ok-ink:#BFE6CC;
--c-stay:#4FC3D8;--c-eat:#F08A50;--c-parks:#62C288;--c-wild:#E2B93B;--c-fun:#E27AB0;--c-culture:#9AA0F0;--c-trips:#6DB2F0;--c-regions:#7FB8C6;--c-national:#A4AEB8;"""

CSS = """
:root{--bg:#F2F7F6;--surface:#FFFFFF;--tint:#E8F1EF;--ink:#0E2724;--ink-2:#37524D;--ink-3:#52706A;
--line:#CFDDD9;--link:#0A5A73;--link-h:#05384A;--focus:#0A7BA5;--bar:rgba(242,247,246,.93);
--hero-a:#0A6C9E;--hero-b:#07496F;--hero-ink:#FFFFFF;--hero-soft:#D2EAF5;--red:#C9283A;--yellow:#F3C534;
--warn-bg:#FFF4D2;--warn-line:#E5C964;--warn-ink:#4A3800;--bad-bg:#FCE9EB;--bad-line:#E7A8B1;--bad-ink:#6F1220;
--info-bg:#E1F0F7;--info-ink:#094A63;--ok-bg:#E3F2E9;--ok-ink:#16532D;
--c-stay:#0B7285;--c-eat:#BF4A12;--c-parks:#2C7A4B;--c-wild:#8F6A00;--c-fun:#A3306B;--c-culture:#4A50B0;--c-trips:#1F6BB3;--c-regions:#3A6E7E;--c-national:#5C6670;
--f-display:"Bricolage Grotesque","Avenir Next","Segoe UI",system-ui,sans-serif;
--f-body:"Public Sans",system-ui,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){/*DARK*/color-scheme:dark}}
:root[data-theme="dark"]{/*DARK*/color-scheme:dark}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 1rem/1.6 var(--f-body)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:30;background:var(--bg)}
[hidden]{display:none!important}
html:not([data-lang="fr"]) [lang="fr"]{display:none}
html[data-lang="fr"] [lang="en"]{display:none}
h1,h2,h3,h4{font-family:var(--f-display);font-weight:700;line-height:1.14;margin:0;text-wrap:balance}
p{margin:0}
a{color:var(--link)}
a:hover{color:var(--link-h)}
:focus-visible{outline:3px solid var(--focus);outline-offset:2px;border-radius:4px}
.sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.ic{width:.85em;height:.85em;flex:none}
.wrap{max-width:1140px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.skip{position:absolute;left:12px;top:-60px;z-index:50;background:var(--ink);color:var(--bg);padding:10px 14px;border-radius:8px;text-decoration:none;font-weight:600}
.skip:focus{top:calc(env(safe-area-inset-top,0px) + 8px)}

/* hero: sky-blue field with the diagonal of the national flag */
.hero{position:relative;overflow:hidden;color:var(--hero-ink);background:linear-gradient(160deg,var(--hero-a),var(--hero-b))}
.hero .slash{position:absolute;top:-25%;bottom:-25%;right:7%;width:min(24vw,280px);transform:skewX(-22deg);
 background:linear-gradient(90deg,var(--yellow) 0 11%,var(--red) 11% 89%,var(--yellow) 89% 100%)}
.hero .wrap{position:relative;padding-block:clamp(34px,7vw,88px) clamp(30px,5vw,56px)}
.hero-text{max-width:clamp(280px,62%,41rem)}
.eyebrow{display:flex;align-items:center;gap:9px;font-size:.78rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--hero-soft)}
.eyebrow .star{width:20px;height:20px;color:var(--yellow)}
.hero h1{font-size:clamp(2.45rem,7.4vw,4.8rem);font-weight:800;letter-spacing:-.025em;margin:.55rem 0 1rem;color:#fff}
.lead{font-size:clamp(1.02rem,2.1vw,1.24rem);color:var(--hero-soft);max-width:34rem}
.hero-meta{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:22px;font-size:.86rem;font-weight:600;color:var(--hero-soft)}

/* sticky bar */
.topbar{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:var(--bar);-webkit-backdrop-filter:saturate(1.4) blur(10px);backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid var(--line)}
.topbar .wrap{display:flex;align-items:center;gap:12px;min-height:54px}
.nav{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none;flex:1;min-width:0;padding:6px 0}
.nav::-webkit-scrollbar{display:none}
.nav a{white-space:nowrap;padding:7px 12px;border-radius:999px;color:var(--ink-2);text-decoration:none;font-weight:600;font-size:.88rem}
.nav a:hover{background:var(--tint);color:var(--ink)}
.nav a[aria-current="true"]{background:var(--ink);color:var(--bg)}
.lang{display:flex;flex:none;border:1px solid var(--line);border-radius:999px;overflow:hidden}
.lang button{font:700 .8rem/1 var(--f-body);padding:9px 12px;background:transparent;color:var(--ink-2);border:0;cursor:pointer}
.lang button[aria-pressed="true"]{background:var(--ink);color:var(--bg)}

/* before you travel */
.advisory{margin-top:26px;background:var(--warn-bg);border:1px solid var(--warn-line);color:var(--warn-ink);border-radius:14px;padding:clamp(16px,3vw,28px)}
.advisory h2{font-size:clamp(1.35rem,3vw,1.75rem)}
.adv-lead{margin-top:6px;max-width:62ch}
.adv-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,400px),1fr));gap:22px 40px;margin-top:18px}
.adv-block{min-width:0}
.adv-block h3{font-family:var(--f-body);font-size:.78rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;margin-bottom:5px}
.adv-block p{font-size:.93rem;line-height:1.55}
.advisory a{color:inherit;font-weight:600;text-underline-offset:2px}
.changes{margin-top:16px;border:1px solid var(--line);background:var(--surface);border-radius:14px;padding:clamp(14px,2.6vw,22px)}
.changes h2{font-size:1.1rem}
.changes ul{margin:10px 0 0;padding-left:1.15rem;display:grid;gap:7px;font-size:.93rem}
.changes li{padding-left:2px;max-width:80ch}

/* search and filters */
.tools{display:flex;flex-wrap:wrap;gap:10px 12px;align-items:center;padding-block:26px 6px}
.search{position:relative;flex:1 1 280px;min-width:0}
.search .ic{position:absolute;left:13px;top:50%;transform:translateY(-50%);width:18px;height:18px;color:var(--ink-3);pointer-events:none}
.search input{width:100%;font:inherit;font-size:1rem;padding:12px 42px 12px 40px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--ink)}
.search input::placeholder{color:var(--ink-3)}
.clear{position:absolute;right:5px;top:50%;transform:translateY(-50%);width:34px;height:34px;border:0;border-radius:8px;background:transparent;color:var(--ink-2);cursor:pointer;display:grid;place-items:center}
.clear .ic{position:static;transform:none;width:14px;height:14px;color:inherit}
.tools select{font:inherit;font-size:1rem;padding:12px 12px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--ink);max-width:100%}
.count{flex:1 0 100%;font-size:.88rem;color:var(--ink-3);min-height:1.4em}
.legend{margin-top:6px;font-size:.88rem;color:var(--ink-2)}
.legend summary{cursor:pointer;font-weight:600;width:max-content;max-width:100%}
.legend ul{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:8px}
.legend li{display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px}

/* sections */
.sec{padding-block:clamp(30px,5vw,58px) 6px;scroll-margin-top:66px;--cat:var(--c-national)}
.sec[data-cat="stay"]{--cat:var(--c-stay)}.sec[data-cat="eat"]{--cat:var(--c-eat)}.sec[data-cat="parks"]{--cat:var(--c-parks)}
.sec[data-cat="wild"]{--cat:var(--c-wild)}.sec[data-cat="fun"]{--cat:var(--c-fun)}.sec[data-cat="culture"]{--cat:var(--c-culture)}
.sec[data-cat="trips"]{--cat:var(--c-trips)}.sec[data-cat="regions"]{--cat:var(--c-regions)}.sec[data-cat="national"]{--cat:var(--c-national)}
.sec-head{display:grid;gap:10px;max-width:64rem}
.sec h2{font-size:clamp(1.75rem,4.2vw,2.6rem);letter-spacing:-.015em}
.sec h2::before{content:"";display:inline-block;width:.5em;height:.5em;margin-right:.42em;background:var(--cat);border-radius:2px;vertical-align:.06em}
.sec-intro{color:var(--ink-2);max-width:66ch}
.group{margin-top:28px;scroll-margin-top:66px}
.group-title{display:flex;align-items:center;gap:12px;font-family:var(--f-body);font-size:.78rem;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:var(--ink-3);margin-bottom:6px}
.group-title::after{content:"";flex:1;height:1px;background:var(--line)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,330px),1fr));gap:0 44px}
.place{min-width:0;padding:16px 0 22px;border-top:3px solid var(--cat);display:flex;flex-direction:column;gap:8px;scroll-margin-top:70px}
.place:target{background:linear-gradient(var(--tint),var(--tint)) no-repeat;background-size:calc(100% + 16px) 100%;background-position:-8px 0}
.place-head{display:flex;flex-wrap:wrap;align-items:flex-start;gap:6px 10px}
.place h4{font-size:1.2rem;letter-spacing:-.005em}
.badges{display:flex;flex-wrap:wrap;gap:4px;margin:2px 0 0;padding:0;list-style:none}
.bd{display:inline-block;font-size:.68rem;font-weight:700;letter-spacing:.03em;padding:3px 9px;border-radius:999px;white-space:nowrap;line-height:1.35}
.bd-warn{background:var(--warn-bg);color:var(--warn-ink);box-shadow:inset 0 0 0 1px var(--warn-line)}
.bd-info{background:var(--info-bg);color:var(--info-ink)}
.bd-bad{background:var(--bad-bg);color:var(--bad-ink);box-shadow:inset 0 0 0 1px var(--bad-line)}
.bd-ok{background:var(--ok-bg);color:var(--ok-ink)}
.meta{font-size:.74rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-3);line-height:1.5}
.meta .sep{margin:0 .5em;opacity:.55}
.desc{color:var(--ink)}
.facts{font-size:.86rem;line-height:1.5;color:var(--ink-2);background:var(--tint);padding:9px 11px;border-radius:8px}
.facts strong{display:block;font-size:.68rem;letter-spacing:.11em;text-transform:uppercase;color:var(--ink-3);margin-bottom:2px}
.links{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 0;padding:0;list-style:none}
.lk{display:inline-flex;align-items:center;gap:7px;font-size:.82rem;font-weight:600;color:var(--link);text-decoration:none;padding:6px 12px;border:1px solid var(--line);border-radius:999px;background:var(--surface);line-height:1.2}
.lk:hover{border-color:var(--link);color:var(--link-h)}
.lk-map{color:var(--ink-2)}
.more{margin-top:14px}

/* plan and footer */
.plan-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:24px 40px;margin-top:20px}
.plan-grid h3{font-family:var(--f-body);font-size:.78rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);margin-bottom:8px}
.plan-grid ul{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.plan-grid a,.more a{font-weight:600}
.plan-grid a .ic,.more a .ic{margin-left:.4em;vertical-align:-.05em}
.plan-note{margin-top:20px;font-size:.88rem;color:var(--ink-3);max-width:62ch}
.foot{margin-top:52px;border-top:1px solid var(--line);padding-block:30px 60px;color:var(--ink-2);font-size:.9rem}
.foot h2{font-size:1.05rem;margin-bottom:8px;color:var(--ink)}
.foot p{max-width:78ch}
.foot .top{display:inline-block;margin-top:18px;font-weight:600}
.empty{padding:34px 0;color:var(--ink-2)}

@media (max-width:700px){
 .hero .slash{top:-18px;bottom:auto;height:176px;right:-30px;width:52px}
 .hero-text{max-width:100%}
 .nav{-webkit-mask-image:linear-gradient(90deg,#000 calc(100% - 26px),transparent);mask-image:linear-gradient(90deg,#000 calc(100% - 26px),transparent)}
 .nav a{padding:7px 10px}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{.topbar,.tools,.legend,.skip{display:none}.hero{background:none;color:#000}.hero h1,.lead,.eyebrow,.hero-meta{color:#000}.hero .slash{display:none}}
""".replace("/*DARK*/", CSS_DARK)

JS = r"""
(function(){
  var de=document.documentElement, KEY='kvg-lang';
  var btns=[].slice.call(document.querySelectorAll('[data-set-lang]'));
  var q=document.getElementById('q'), area=document.getElementById('area'), clr=document.getElementById('clear'), cnt=document.getElementById('count');
  var places=[].slice.call(document.querySelectorAll('.place'));
  var groups=[].slice.call(document.querySelectorAll('.group'));
  var secs=[].slice.call(document.querySelectorAll('.sec[data-has-places]'));
  var TXT={shown:{en:'places shown',fr:'lieux affichés'},none:{en:'No place matches. Try another word or choose all districts.',fr:'Aucun lieu ne correspond. Essayez un autre mot ou choisissez tous les quartiers.'}};
  function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
  function lang(){return de.getAttribute('data-lang')==='fr'?'fr':'en'}
  function update(){
    var terms=norm(q.value).split(/\s+/).filter(Boolean), a=area.value, n=0;
    places.forEach(function(p){
      var ok=true, hay=p.getAttribute('data-q');
      for(var i=0;i<terms.length;i++){ if(hay.indexOf(terms[i])<0){ok=false;break} }
      if(ok&&a){ok=p.getAttribute('data-area')===a}
      p.hidden=!ok; if(ok){n++}
    });
    var active=terms.length>0||!!a;
    groups.forEach(function(g){g.hidden=active&&!g.querySelector('.place:not([hidden])')});
    secs.forEach(function(s){s.hidden=active&&!s.querySelector('.place:not([hidden])')});
    clr.hidden=!q.value;
    var l=lang();
    cnt.textContent=n===0?TXT.none[l]:(active?(n+' '+TXT.shown[l]):'');
  }
  function setLang(l,save){
    de.setAttribute('data-lang',l); de.setAttribute('lang',l);
    btns.forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-set-lang')===l?'true':'false')});
    q.placeholder=q.getAttribute('data-ph-'+l);
    [q,area,clr].forEach(function(el){el.setAttribute('aria-label',el.getAttribute('data-label-'+l))});
    [].forEach.call(area.options,function(o){var t=o.getAttribute('data-'+l); if(t){o.textContent=t}});
    if(save){try{localStorage.setItem(KEY,l)}catch(e){}}
    update();
  }
  var l0=null; try{l0=localStorage.getItem(KEY)}catch(e){}
  if(l0!=='fr'&&l0!=='en'){l0=((navigator.language||'en').toLowerCase().indexOf('fr')===0)?'fr':'en'}
  btns.forEach(function(b){b.addEventListener('click',function(){setLang(b.getAttribute('data-set-lang'),true)})});
  q.addEventListener('input',update); area.addEventListener('change',update);
  clr.addEventListener('click',function(){q.value='';update();q.focus()});
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[href^="#"]'); if(!a){return}
    var t=document.getElementById(a.getAttribute('href').slice(1));
    if(t&&(t.hidden||(t.closest&&t.closest('[hidden]')))){q.value='';area.value='';update()}
  });
  /* highlight the section in view */
  var links={}; [].forEach.call(document.querySelectorAll('.nav a'),function(a){links[a.getAttribute('href').slice(1)]=a});
  if('IntersectionObserver' in window){
    var nav=document.querySelector('.nav');
    var io=new IntersectionObserver(function(es){es.forEach(function(e){
      if(!e.isIntersecting){return}
      Object.keys(links).forEach(function(k){links[k].removeAttribute('aria-current')});
      var a=links[e.target.id]; if(a){a.setAttribute('aria-current','true');
        try{nav.scrollTo({left:a.offsetLeft-nav.clientWidth/2+a.offsetWidth/2,behavior:'smooth'})}catch(x){}}
    })},{rootMargin:'-35% 0px -60% 0px'});
    Object.keys(links).forEach(function(k){var s=document.getElementById(k); if(s){io.observe(s)}});
  }
  setLang(l0,false);
})();
"""

FONTS = "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600..800&family=Public+Sans:wght@400;500;600;700;800&display=swap"
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%230A6C9E'/%3E"
           "%3Cpath d='M-2 30 22 -2h12L10 30z' fill='%23C9283A' stroke='%23F3C534' stroke-width='2'/%3E"
           "%3Cpath d='m8 4 1.4 2.9 3.1.4-2.3 2.2.6 3.1L8 11l-2.8 1.6.6-3.1L3.5 7.3l3.1-.4z' fill='%23F3C534'/%3E%3C/svg%3E")


def body_html(stats):
    sections = PL.SECTIONS
    nav = "".join(f'<a href="#{s["id"]}">{tx(s["nav"])}</a>' for s in sections) + f'<a href="#plan">{tx(("Links", "Liens"))}</a>'
    secs_html = "".join(render_section(s, stats) for s in sections)
    plan = render_plan(stats)
    n_places, n_links = stats["places"], len(stats["links"])
    ui = U.UI
    ph_en, ph_fr = ui["search_ph"]
    lab_en, lab_fr = ui["search_label"]
    al_en, al_fr = ui["area_label"]
    cl_en, cl_fr = ui["clear"]
    return f"""{SPRITE}
<a class="skip" href="#main">{tx(ui["skip"])}</a>
<header class="hero" id="top">
<div class="slash" aria-hidden="true"></div>
<div class="wrap"><div class="hero-text">
<p class="eyebrow"><svg class="star" aria-hidden="true"><use href="#i-star"/></svg>{tx(ui["eyebrow"])}</p>
<h1>{tx(ui["h1"])}</h1>
<p class="lead">{tx(ui["lead"])}</p>
<p class="hero-meta"><span>{tx(ui["checked"])}: {tx(U.CHECKED)}</span><span>{n_places} {tx(ui["places"])}</span></p>
</div></div>
</header>
<div class="topbar"><div class="wrap">
<nav class="nav" aria-label="Sections">{nav}</nav>
<div class="lang" role="group" aria-label="Language · Langue"><button type="button" data-set-lang="en" aria-pressed="true" aria-label="English">EN</button><button type="button" data-set-lang="fr" aria-pressed="false" aria-label="Français">FR</button></div>
</div></div>
<main id="main" class="wrap">
{render_travel()}
{render_changes()}
<div class="tools" role="search">
<div class="search"><svg class="ic" aria-hidden="true"><use href="#i-search"/></svg>
<input id="q" type="search" autocomplete="off" placeholder="{esc(ph_en)}" data-ph-en="{esc(ph_en)}" data-ph-fr="{esc(ph_fr)}" aria-label="{esc(lab_en)}" data-label-en="{esc(lab_en)}" data-label-fr="{esc(lab_fr)}">
<button id="clear" class="clear" type="button" hidden aria-label="{esc(cl_en)}" data-label-en="{esc(cl_en)}" data-label-fr="{esc(cl_fr)}"><svg class="ic" aria-hidden="true"><use href="#i-x"/></svg></button></div>
<select id="area" aria-label="{esc(al_en)}" data-label-en="{esc(al_en)}" data-label-fr="{esc(al_fr)}">{area_options(sections)}</select>
<p id="count" class="count" aria-live="polite"></p>
</div>
{render_legend()}
{secs_html}
{plan}
</main>
<footer class="foot"><div class="wrap"><h2>{tx(ui["foot_h"])}</h2><p>{tx(U.FOOTER)}</p>
<a class="top" href="#top">{tx(ui["top"])} ↑</a></div></footer>
<script>{JS}</script>"""


def build(standalone=True):
    stats = {"places": 0, "links": set()}
    body = body_html(stats)
    title = U.TITLE
    head_common = (f'<title>{esc(title)}</title>\n'
                   f'<link rel="stylesheet" href="{FONTS}">\n'
                   f'<style>{CSS}</style>\n')
    if standalone:
        return (
            '<!doctype html>\n<html lang="en" data-lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<meta name="description" content="{esc(U.META_DESC[0])}">\n'
            f'<meta property="og:title" content="{esc(title)}">\n'
            f'<meta property="og:description" content="{esc(U.META_DESC[0])}">\n'
            '<meta property="og:type" content="website">\n'
            f'<link rel="icon" href="{FAVICON}">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            + head_common + '</head>\n<body>\n' + body + '\n</body>\n</html>\n'), stats
    return ('<meta name="claude:viewport-fit-sides" content="cover">\n' + head_common + body + '\n'), stats


if __name__ == "__main__":
    out_dir = HERE.parent
    page, stats = build(True)
    (out_dir / "index.html").write_text(page, encoding="utf-8", newline="\n")
    print(f"index.html: {len(page):,} bytes, {stats['places']} places, {len(stats['links'])} distinct links")
    if "--artifact" in sys.argv:
        target = pathlib.Path(sys.argv[sys.argv.index("--artifact") + 1])
        frag, _ = build(False)
        target.write_text(frag, encoding="utf-8", newline="\n")
        print(f"artifact fragment: {target} ({len(frag):,} bytes)")

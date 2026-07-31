#!/usr/bin/env python3
# pyright: reportMissingImports=false
"""Build the Blue Trust one-page case library from the 25 presentation sources."""
from __future__ import annotations

from html import escape
from pathlib import Path
import re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PRESENTATIONS = ROOT / "presentations"
DOMAIN_META = {
    "source": {
        "label": "Source",
        "eyebrow": "SCOR Source",
        "icon": "ph-handshake",
        "statement": "Supplier decisions need shared definitions before they need automation.",
        "intro": "Performance, risk, capacity, compliance, and incoming quality depend on evidence that procurement, quality, and suppliers interpret the same way.",
    },
    "make": {
        "label": "Transform",
        "eyebrow": "SCOR Transform · MAKE",
        "icon": "ph-factory",
        "statement": "Factory analytics must survive contact with process physics.",
        "intro": "Cost, scheduling, maintenance, quality, digital twins, and OEE create value only when line teams can challenge the data and act on the result.",
    },
    "plan": {
        "label": "Plan",
        "eyebrow": "SCOR Plan",
        "icon": "ph-chart-line-up",
        "statement": "Planning models sharpen trade-offs; they do not own commitments.",
        "intro": "Forecasts, inventory policies, segmentation, S&OP, and risk analysis prepare choices that named leaders still have to make.",
    },
    "deliver": {
        "label": "Fulfill",
        "eyebrow": "SCOR Order · Fulfill",
        "icon": "ph-truck",
        "statement": "A prediction matters when someone changes the customer outcome.",
        "intro": "Service, fulfillment, network, freight, ETA, and routing analytics become operational only when exceptions, spend, and promises have clear owners.",
    },
}
DOMAIN_ORDER = ["source", "make", "plan", "deliver"]


def clean_text(tag) -> str:
    clone = BeautifulSoup(str(tag), "html.parser")
    for node in clone.select("i, script, style"):
        node.decompose()
    return " ".join(clone.get_text(" ", strip=True).split())


def section_content(section) -> str:
    """Flatten slide-layout markup into semantic headings, paragraphs and lists."""
    output: list[str] = []
    list_items: list[str] = []

    def leaf_text_div(tag) -> bool:
        if tag.name != "div":
            return False
        return not any(child.name not in {"i", "strong"} for child in tag.find_all(recursive=False))

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            output.append("<ul>" + "".join(f"<li>{escape(x)}</li>" for x in list_items) + "</ul>")
            list_items = []

    for tag in section.select("h3, h4, p, li, strong, blockquote, table, div, span"):
        if tag.find_parent("table") or tag.find_parent("blockquote"):
            continue
        if tag.name == "div" and not leaf_text_div(tag):
            continue
        if tag.name == "span":
            if tag.find_parent(["p", "li", "h3", "h4", "table", "blockquote", "strong"]):
                continue
            parent_div = tag.find_parent("div")
            if parent_div and leaf_text_div(parent_div):
                continue
        # Preserve standalone labels used by the slide cards, but avoid
        # duplicating strong text already carried by a paragraph/list item.
        if tag.name == "strong":
            if tag.find_parent(["p", "li", "h3", "h4"]):
                continue
            parent_div = tag.find_parent("div")
            if parent_div and leaf_text_div(parent_div):
                continue
        text = clean_text(tag)
        if not text or text in {"→", "|"}:
            continue
        if tag.name == "li":
            list_items.append(text)
            continue
        flush_list()
        if tag.name == "table":
            rows = []
            for row in tag.select("tr"):
                cells = [clean_text(cell) for cell in row.select("th, td")]
                if cells:
                    cell_tag = "th" if row.find("th") else "td"
                    rows.append("<tr>" + "".join(f"<{cell_tag}>{escape(cell)}</{cell_tag}>" for cell in cells) + "</tr>")
            if rows:
                output.append('<div class="table-wrap"><table>' + "".join(rows) + "</table></div>")
            continue
        if tag.name == "blockquote":
            output.append(f'<blockquote>{escape(text)}</blockquote>')
            continue
        if tag.name in {"div", "span"}:
            output.append(f'<p>{escape(text)}</p>')
            continue
        if tag.name in {"h3", "h4", "strong"}:
            output.append(f'<h4>{escape(text)}</h4>')
        else:
            output.append(f'<p>{escape(text)}</p>')
    flush_list()
    return "\n".join(output)


def parse_case(path: Path) -> dict:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    sections = soup.select("section.slide")
    title = clean_text(sections[0].find("h1"))
    subtitle_nodes = sections[0].find_all("p")
    subtitle = clean_text(subtitle_nodes[-1]) if subtitle_nodes else ""
    domain = path.parts[-3]
    slug = path.parent.name
    number = slug.split("-", 1)[0]
    content_sections = []
    summary = ""
    for section in sections[1:]:
        heading_tag = section.find("h2")
        if not heading_tag:
            continue
        heading = clean_text(heading_tag)
        if heading.lower() in {"related use cases", "explore source cases", "explore make cases", "explore plan cases", "explore deliver cases"}:
            continue
        body = section_content(section)
        if not body:
            continue
        if not summary and heading.lower() == "what is it?":
            first_p = BeautifulSoup(body, "html.parser").find("p")
            summary = first_p.get_text(" ", strip=True) if first_p else ""
        content_sections.append({"heading": heading, "body": body})
    if not summary:
        summary = subtitle or f"A practical analytics case for {title.lower()}."
    rel = path.relative_to(ROOT).as_posix()
    return {
        "domain": domain,
        "slug": slug,
        "anchor": f"case-{slug}",
        "number": number,
        "title": title,
        "subtitle": subtitle,
        "summary": summary,
        "sections": content_sections,
        "presentation": rel,
    }


def render_case(case: dict) -> str:
    search = " ".join(
        [case["title"], case["subtitle"], case["summary"]]
        + [s["heading"] + " " + BeautifulSoup(s["body"], "html.parser").get_text(" ", strip=True) for s in case["sections"]]
    ).lower()
    body = "\n".join(
        f'<section class="brief-section"><h3>{escape(s["heading"])}</h3>{s["body"]}</section>'
        for s in case["sections"]
    )
    return f'''<details class="case-card" id="{case['anchor']}" data-domain="{case['domain']}" data-search="{escape(search, quote=True)}">
  <summary>
    <span class="case-number">{case['number']}</span>
    <span class="case-heading"><span class="case-domain">{escape(DOMAIN_META[case['domain']]['eyebrow'])}</span><strong>{escape(case['title'])}</strong><span>{escape(case['summary'])}</span></span>
    <span class="case-toggle" aria-hidden="true"><i class="ph ph-plus"></i></span>
  </summary>
  <div class="case-body">
    <div class="case-actions"><a class="button secondary" href="{case['presentation']}"><i class="ph ph-presentation-chart"></i> Open slide version</a><a class="text-link" href="#top"><i class="ph ph-arrow-up"></i> Back to top</a></div>
    {f'<p class="case-subtitle">{escape(case["subtitle"])}</p>' if case['subtitle'] else ''}
    {body}
  </div>
</details>'''


def build() -> str:
    paths = sorted(PRESENTATIONS.glob("*/*/index.html"))
    cases = [parse_case(p) for p in paths]
    cases.sort(key=lambda c: int(c["number"]))
    if len(cases) != 25 or len({c["slug"] for c in cases}) != 25:
        raise RuntimeError(f"Expected 25 unique cases, found {len(cases)}")

    domain_sections = []
    for domain in DOMAIN_ORDER:
        meta = DOMAIN_META[domain]
        domain_cases = [c for c in cases if c["domain"] == domain]
        domain_sections.append(f'''<section class="domain-section" id="{domain}">
  <div class="section-intro">
    <span class="eyebrow"><i class="ph {meta['icon']}"></i> {escape(meta['eyebrow'])}</span>
    <h2>{escape(meta['statement'])}</h2>
    <p>{escape(meta['intro'])}</p>
  </div>
  <div class="case-list">
    {''.join(render_case(c) for c in domain_cases)}
  </div>
</section>''')

    counts = {d: sum(1 for c in cases if c["domain"] == d) for d in DOMAIN_ORDER}
    return TEMPLATE.replace("{{DOMAIN_SECTIONS}}", "\n".join(domain_sections)).replace("{{CASE_COUNT}}", str(len(cases))).replace(
        "{{DOMAIN_NAV}}",
        "".join(f'<a href="#{d}" data-filter="{d}"><i class="ph {DOMAIN_META[d]["icon"]}"></i>{DOMAIN_META[d]["label"]}<span>{counts[d]}</span></a>' for d in DOMAIN_ORDER),
    )


TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Operations Intelligence Case Library | Frank Kienle</title>
<meta name="description" content="Twenty-five supply-chain analytics case briefs on one searchable page, connected to Frank Kienle's AI in Operations decision map and human decision boundaries.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;650;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css">
<style>
:root{--primary:#2F2FE4;--active:#162E93;--soft:#E8EAFF;--indigo:#1A1953;--ink:#080616;--body:#4B5068;--muted:#74798F;--hair:#DDE2F0;--hair-soft:#EEF1F8;--canvas:#fff;--surface:#F6F7FB;--blue:#F1F4FF;--dark:#080616;--dark2:#12102B;--on-dark:#B7BCD1;--warm:#D89A2B;--max:1180px}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:112px}body{margin:0;background:var(--canvas);color:var(--ink);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.55}a{color:inherit}.site-nav{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.96);backdrop-filter:blur(12px);border-bottom:1px solid var(--hair-soft)}.nav-inner{max-width:var(--max);height:68px;margin:auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between;gap:24px}.brand{font-weight:700;text-decoration:none;letter-spacing:-.02em}.brand span{color:var(--primary)}.nav-links{display:flex;align-items:center;gap:22px;font-size:14px;font-weight:600}.nav-links a{text-decoration:none;color:var(--body)}.nav-links a:hover{color:var(--primary)}.nav-cta{padding:10px 16px!important;border-radius:100px;background:var(--soft);color:var(--active)!important}
.hero{background:var(--dark);color:#fff}.hero-inner{max-width:var(--max);margin:auto;padding:92px 24px 76px;display:grid;grid-template-columns:minmax(0,1.45fr) minmax(280px,.55fr);gap:64px;align-items:end}.eyebrow{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:100px;background:var(--soft);color:var(--active);font-size:12px;font-weight:750;letter-spacing:.1em;text-transform:uppercase}.hero .eyebrow{background:rgba(255,255,255,.1);color:var(--on-dark)}h1{font-size:clamp(3rem,6vw,5.4rem);font-weight:500;letter-spacing:-.055em;line-height:.96;margin:24px 0 22px;max-width:850px}.hero-lead{font-size:1.15rem;color:var(--on-dark);max-width:800px;margin:0}.hero-actions,.case-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}.button{display:inline-flex;align-items:center;gap:8px;padding:14px 20px;border-radius:100px;background:var(--primary);color:#fff;text-decoration:none;font-size:15px;font-weight:700}.button:hover{background:var(--active)}.button.secondary{background:var(--soft);color:var(--active)}.hero .button.secondary{background:#fff;color:var(--ink)}.hero-side{display:grid;grid-template-columns:1fr 1fr;gap:12px}.stat{padding:20px;border:1px solid rgba(255,255,255,.1);border-radius:18px;background:var(--dark2)}.stat b{display:block;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:1.65rem}.stat span{font-size:12px;color:var(--on-dark)}
.bridge{max-width:var(--max);margin:auto;padding:56px 24px}.bridge h2,.section-intro h2{font-weight:560;letter-spacing:-.035em;line-height:1.08}.bridge h2{font-size:clamp(2rem,4vw,3.15rem);max-width:900px;margin:18px 0 12px}.bridge>p{max-width:850px;color:var(--body)}.bridge-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}.bridge-card{border:1px solid var(--hair-soft);border-radius:28px;padding:26px;text-decoration:none;background:#fff}.bridge-card:hover{border-color:var(--primary)}.bridge-card i{font-size:26px;color:var(--primary)}.bridge-card strong{display:block;margin:14px 0 6px;color:var(--indigo)}.bridge-card span{display:block;color:var(--body);font-size:14px}
.library-tools{position:sticky;top:68px;z-index:40;background:rgba(246,247,251,.97);backdrop-filter:blur(12px);border-block:1px solid var(--hair-soft)}.tools-inner{max-width:var(--max);margin:auto;padding:14px 24px;display:flex;align-items:center;gap:18px}.search{position:relative;flex:1}.search i{position:absolute;left:15px;top:50%;transform:translateY(-50%);color:var(--muted)}.search input{width:100%;padding:13px 16px 13px 42px;border:1px solid var(--hair);border-radius:100px;background:#fff;color:var(--ink);font:inherit}.search input:focus{outline:3px solid var(--soft);border-color:var(--primary)}.domain-nav{display:flex;gap:8px}.domain-nav a{display:inline-flex;align-items:center;gap:7px;padding:10px 12px;border-radius:100px;text-decoration:none;color:var(--body);font-size:13px;font-weight:700;background:#fff;border:1px solid var(--hair-soft)}.domain-nav a:hover{border-color:var(--primary);color:var(--primary)}.domain-nav span{font-family:ui-monospace,monospace;color:var(--muted)}
.library{background:var(--surface);padding-bottom:80px}.domain-section{max-width:var(--max);margin:auto;padding:72px 24px 0}.section-intro{display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,.55fr);gap:38px;align-items:end;margin-bottom:26px}.section-intro .eyebrow{grid-column:1/-1;justify-self:start}.section-intro h2{font-size:clamp(2rem,4vw,3rem);margin:0;max-width:760px}.section-intro>p{margin:0;color:var(--body)}.case-list{display:grid;gap:12px}.case-card{background:#fff;border:1px solid var(--hair-soft);border-radius:22px;overflow:hidden;scroll-margin-top:140px}.case-card[open]{border-color:#C8CDF8;box-shadow:0 18px 50px rgba(8,6,22,.06)}.case-card>summary{list-style:none;cursor:pointer;padding:23px 24px;display:grid;grid-template-columns:50px 1fr 36px;gap:18px;align-items:start}.case-card>summary::-webkit-details-marker{display:none}.case-number{width:44px;height:44px;display:grid;place-items:center;border-radius:14px;background:var(--soft);color:var(--primary);font-family:ui-monospace,monospace;font-weight:700}.case-heading{display:grid;gap:4px}.case-domain{color:var(--active);font-size:11px;font-weight:750;letter-spacing:.09em;text-transform:uppercase}.case-heading strong{font-size:20px;color:var(--indigo);line-height:1.25}.case-heading>span:last-child{color:var(--body);font-size:14px;max-width:850px}.case-toggle{width:34px;height:34px;display:grid;place-items:center;border-radius:50%;background:var(--surface);color:var(--primary)}.case-card[open] .case-toggle{transform:rotate(45deg)}.case-body{border-top:1px solid var(--hair-soft);padding:0 24px 28px 92px}.case-actions{justify-content:space-between;align-items:center}.case-actions .button{padding:10px 14px;font-size:13px}.case-subtitle{margin:20px 0 0;padding:14px 16px;border-radius:14px;background:var(--blue);color:var(--indigo);font-size:14px;font-weight:650}.text-link{display:inline-flex;gap:6px;align-items:center;color:var(--primary);font-size:13px;font-weight:700;text-decoration:none}.brief-section{padding:24px 0;border-top:1px solid var(--hair-soft)}.brief-section:first-of-type{border-top:0}.brief-section h3{font-size:21px;color:var(--indigo);margin:0 0 12px}.brief-section h4{font-size:15px;color:var(--indigo);margin:18px 0 6px}.brief-section p,.brief-section li{color:var(--body);font-size:15px}.brief-section p{margin:8px 0}.brief-section ul{margin:8px 0;padding-left:1.25rem;columns:2;column-gap:32px}.brief-section li{break-inside:avoid;margin-bottom:6px}.brief-section blockquote{margin:14px 0;padding:18px 20px;border-left:4px solid var(--primary);border-radius:0 14px 14px 0;background:var(--blue);color:var(--indigo);font-weight:600}.table-wrap{overflow-x:auto;margin:14px 0}.brief-section table{width:100%;border-collapse:collapse;font-size:14px}.brief-section th,.brief-section td{padding:11px 12px;border:1px solid var(--hair);text-align:left;vertical-align:top}.brief-section th{background:var(--blue);color:var(--indigo)}.empty{display:none;max-width:var(--max);margin:0 auto;padding:48px 24px;color:var(--body)}
.footer{background:var(--dark);color:#fff}.footer-inner{max-width:var(--max);margin:auto;padding:54px 24px;display:flex;justify-content:space-between;gap:32px;align-items:center}.footer p{margin:0;color:var(--on-dark);max-width:700px}.footer-links{display:flex;gap:14px}.footer-links a{width:42px;height:42px;display:grid;place-items:center;border:1px solid rgba(255,255,255,.15);border-radius:50%;text-decoration:none}
@media(max-width:900px){.hero-inner,.section-intro{grid-template-columns:1fr}.hero-inner{gap:34px}.hero-side{grid-template-columns:repeat(4,1fr)}.tools-inner{align-items:stretch;flex-direction:column}.library-tools{position:relative;top:auto}.domain-nav{overflow-x:auto;padding-bottom:2px}.bridge-grid{grid-template-columns:1fr}.nav-links a:not(.nav-cta){display:none}.case-body{padding-left:24px}.brief-section ul{columns:1}}
@media(max-width:620px){.hero-inner{padding-top:64px}.hero-side{grid-template-columns:1fr 1fr}.case-card>summary{grid-template-columns:44px 1fr;gap:14px}.case-toggle{display:none}.case-heading strong{font-size:17px}.nav-cta{font-size:12px}.footer-inner{align-items:flex-start;flex-direction:column}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
</style>
</head>
<body id="top">
<nav class="site-nav" aria-label="Primary navigation"><div class="nav-inner"><a class="brand" href="https://kienlef.github.io/"><span>AI</span> in Operations</a><div class="nav-links"><a href="https://kienlef.github.io/">Home</a><a href="https://kienlef.github.io/operations-intelligence-map/">Decision map</a><a href="https://kienlef.github.io/operations-use-cases/">27 decisions</a><a class="nav-cta" href="https://github.com/kienlef/operations_use_case_selection"><i class="ph ph-github-logo"></i> Inspect source</a></div></div></nav>
<header class="hero"><div class="hero-inner"><div><span class="eyebrow"><i class="ph ph-books"></i> Public operations evidence library</span><h1>Twenty-five analytical cases. One page. No content maze.</h1><p class="hero-lead">Explore the analytics behind sourcing, production, planning, and delivery decisions without clicking through twenty-five separate presentations. Each brief keeps the practical methods, data questions, and KPIs visible—and links back to the decision owner and agent boundary.</p><div class="hero-actions"><a class="button" href="#library"><i class="ph ph-arrow-down"></i> Explore all cases</a><a class="button secondary" href="https://kienlef.github.io/operations-intelligence-map/"><i class="ph ph-graph"></i> Open decision map</a></div></div><div class="hero-side"><div class="stat"><b>{{CASE_COUNT}}</b><span>case briefs</span></div><div class="stat"><b>4</b><span>operating domains</span></div><div class="stat"><b>1</b><span>searchable page</span></div><div class="stat"><b>27</b><span>decision boundaries linked</span></div></div></div></header>
<section class="bridge"><span class="eyebrow"><i class="ph ph-path"></i> One connected learning system</span><h2>Move from operating relationship to decision boundary to analytical depth.</h2><p>The content now follows one deliberate path instead of behaving like three unrelated websites.</p><div class="bridge-grid"><a class="bridge-card" href="https://kienlef.github.io/operations-intelligence-map/"><i class="ph ph-graph"></i><strong>1 · See the operating system</strong><span>Use six lenses to understand how decisions connect to SCOR processes, roles, systems, data, and AI roles.</span></a><a class="bridge-card" href="https://kienlef.github.io/operations-use-cases/"><i class="ph ph-user-check"></i><strong>2 · Check ownership and boundaries</strong><span>Review twenty-seven decisions with a named human owner and a clear limit on agent authority.</span></a><a class="bridge-card" href="#library"><i class="ph ph-magnifying-glass"></i><strong>3 · Inspect the analytical case</strong><span>Read the full methods, data requirements, business objectives, and KPIs here on one page.</span></a></div></section>
<div class="library-tools" id="library"><div class="tools-inner"><label class="search"><i class="ph ph-magnifying-glass"></i><input id="case-search" type="search" placeholder="Search methods, KPIs, data, or case names" aria-label="Search case library"></label><nav class="domain-nav" aria-label="Case domains">{{DOMAIN_NAV}}</nav></div></div>
<main class="library">{{DOMAIN_SECTIONS}}<p class="empty" id="empty-state">No case matches that search. Try a process, method, KPI, or data source.</p></main>
<footer class="footer"><div class="footer-inner"><p>Public educational material by Frank Kienle. Examples use public, historical, educational, or synthetic information. No employer-, customer-, or supplier-confidential information is shared.</p><div class="footer-links"><a href="https://www.youtube.com/@frankkienle7312" aria-label="YouTube"><i class="ph ph-youtube-logo"></i></a><a href="https://github.com/kienlef" aria-label="GitHub"><i class="ph ph-github-logo"></i></a><a href="https://www.linkedin.com/in/frankkienle" aria-label="LinkedIn"><i class="ph ph-linkedin-logo"></i></a></div></div></footer>
<script>
const search=document.getElementById('case-search'),cards=[...document.querySelectorAll('.case-card')],sections=[...document.querySelectorAll('.domain-section')],empty=document.getElementById('empty-state');
function filterCases(){const q=search.value.trim().toLowerCase();let visible=0;cards.forEach(card=>{const show=!q||card.dataset.search.includes(q);card.hidden=!show;if(show)visible++});sections.forEach(section=>{section.hidden=![...section.querySelectorAll('.case-card')].some(c=>!c.hidden)});empty.style.display=visible?'none':'block'}
search.addEventListener('input',filterCases);
function openHash(){if(!location.hash.startsWith('#case-'))return;const card=document.querySelector(location.hash);if(card){card.open=true;requestAnimationFrame(()=>card.scrollIntoView({block:'start'}))}}
addEventListener('hashchange',openHash);openHash();
window.caseLibraryDebug=()=>({cases:cards.length,visible:cards.filter(c=>!c.hidden).length,open:cards.filter(c=>c.open).length,domains:sections.length,duplicateIds:cards.length-new Set(cards.map(c=>c.id)).size,horizontalOverflow:document.documentElement.scrollWidth>document.documentElement.clientWidth});
</script>
</body>
</html>
'''

if __name__ == "__main__":
    output = build()
    target = ROOT / "index.html"
    target.write_text(output, encoding="utf-8")
    print(f"Wrote {target} ({len(output):,} bytes)")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a readable HTML report from per-paper markdown summaries."""
import os, re, html, glob, sys, datetime

DATE = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
BASE = sys.argv[2] if len(sys.argv) > 2 else "."
SUMMARY_DIR = os.path.join(BASE, DATE, "paper_summary")
OUT = os.path.join(BASE, DATE, f"{DATE}_paper_summary.html")

TOPIC_COLORS = {
    "Egocentric Vision": "#0ea5e9",
    "Hand-Object Interaction": "#10b981",
    "Spatial Audio": "#6366f1",
}
def topic_color(t):
    for k, v in TOPIC_COLORS.items():
        if k.lower() in t.lower():
            return v
    return "#64748b"

def inline(text):
    # Protect TeX math spans ($$...$$ and $...$) from escaping/markdown mangling,
    # restore them afterwards so MathJax can render the delimiters.
    math_spans = []
    def stash(m):
        math_spans.append(m.group(0))
        return f"\x00MATH{len(math_spans)-1}\x00"
    text = re.sub(r"\$\$.+?\$\$|\$[^$\n]+?\$", stash, text)
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\[(.+?)\]\((https?://[^\s)]+)\)", r'<a href="\2" target="_blank">\1</a>', text)
    text = re.sub(r"(?<![\">=])(https?://[^\s<)]+)", r'<a href="\1" target="_blank">\1</a>', text)
    def unstash(m):
        raw = math_spans[int(m.group(1))]
        return raw.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\x00MATH(\d+)\x00", unstash, text)
    return text

def _split_row(s):
    """'| a | b |' -> ['a','b'] (leading/trailing pipes tolerated)."""
    s = s.strip()
    if s.startswith("|"): s = s[1:]
    if s.endswith("|"): s = s[:-1]
    return [c.strip() for c in s.split("|")]

_TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$")

def md_body_to_html(lines):
    """Convert body lines (after metadata) to HTML.
    Handles ##, ###, bullets, numbered, GFM tables, images, paragraphs."""
    out = []
    list_stack = []  # list of ('ul'/'ol', indent)
    def close_lists(to_indent=-1):
        while list_stack and list_stack[-1][1] > to_indent:
            tag = list_stack.pop()[0]
            out.append(f"</{tag}>")
    para = []
    def flush_para():
        if para:
            out.append("<p>" + " ".join(para) + "</p>")
            para.clear()
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip("\n")
        stripped = line.strip()
        if not stripped:
            flush_para(); close_lists(); i += 1; continue

        # --- GFM table: a '|...|' row followed by a '|---|---|' separator ---
        if stripped.startswith("|") and i + 1 < n and _TABLE_SEP.match(lines[i + 1]):
            flush_para(); close_lists()
            header = _split_row(stripped)
            i += 2  # consume header + separator
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(_split_row(lines[i])); i += 1
            ncol = len(header)
            norm_rows = [(r + [""] * ncol)[:ncol] for r in rows]
            # A column is "numeric" (right-aligned, tabular font) only if the
            # majority of its non-empty, non-placeholder cells are a number followed by
            # at most a short unit (%, °, dB, ms, p, ×, fps ...) and an optional trailing
            # parenthetical note. This keeps method-name columns like
            # "3DGS + stereo guidance" or metric labels like "1st object mAP" left-aligned.
            _placeholder = {"-", "–", "—", "n/a", "N/A", ""}
            def _isnum(v):
                s = re.sub(r"[*`]", "", v).strip()
                s = re.sub(r"\s*\([^)]*\)\s*$", "", s)   # drop a trailing (note)
                m = re.match(r"^[+\-–—]?\d[\d.,]*(.*)$", s)
                return bool(m) and len(m.group(1).strip()) <= 3
            numeric_col = []
            for c in range(ncol):
                vals = [norm_rows[k][c].strip() for k in range(len(norm_rows))
                        if norm_rows[k][c].strip() not in _placeholder]
                numeric_col.append(bool(vals) and
                                   sum(1 for v in vals if _isnum(v)) >= 0.5 * len(vals))
            def _cls(c):
                return ' class="num"' if numeric_col[c] else ""
            th = "".join(f"<th{_cls(c)}>{inline(h)}</th>" for c, h in enumerate(header))
            body_rows = []
            for r in norm_rows:
                body_rows.append("<tr>" + "".join(f"<td{_cls(c)}>{inline(cell)}</td>"
                                                   for c, cell in enumerate(r)) + "</tr>")
            out.append('<div class="tbl-wrap"><table><thead><tr>'
                       + th + "</tr></thead><tbody>" + "".join(body_rows)
                       + "</tbody></table></div>")
            continue

        # --- standalone image: ![caption](url) ---
        m_img = re.match(r"^!\[(.*?)\]\((\S+?)\)\s*$", stripped)
        if m_img:
            flush_para(); close_lists()
            alt, src = m_img.group(1), m_img.group(2)
            cap = f'<figcaption>{inline(alt)}</figcaption>' if alt else ""
            out.append(f'<figure class="fig"><img src="{html.escape(src)}" '
                       f'alt="{html.escape(alt)}" loading="lazy">{cap}</figure>')
            i += 1; continue

        m_h3 = re.match(r"^###\s+(.*)", line)
        m_h2 = re.match(r"^##\s+(.*)", line)
        m_bul = re.match(r"^(\s*)[-*]\s+(.*)", line)
        m_num = re.match(r"^(\s*)\d+\.\s+(.*)", line)
        if m_h2:
            flush_para(); close_lists()
            out.append(f'<h3 class="sec">{inline(m_h2.group(1))}</h3>'); i += 1; continue
        if m_h3:
            flush_para(); close_lists()
            out.append(f'<h4 class="subsec">{inline(m_h3.group(1))}</h4>'); i += 1; continue
        if m_bul or m_num:
            flush_para()
            indent = len(m_bul.group(1) if m_bul else m_num.group(1))
            content = (m_bul.group(2) if m_bul else m_num.group(2))
            tag = "ul" if m_bul else "ol"
            if not list_stack or indent > list_stack[-1][1]:
                out.append(f"<{tag}>"); list_stack.append((tag, indent))
            elif indent < list_stack[-1][1]:
                close_lists(indent)
                if not list_stack or list_stack[-1][1] != indent:
                    out.append(f"<{tag}>"); list_stack.append((tag, indent))
            out.append(f"<li>{inline(content)}</li>"); i += 1; continue
        # plain paragraph
        para.append(inline(stripped)); i += 1
    flush_para(); close_lists()
    return "\n".join(out)

def parse_file(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    title = "Untitled"; meta_arxiv = ""; topic = ""; link = ""; authors = ""
    pub_date = ""; venue = ""
    body_start = 0
    for i, l in enumerate(lines):
        if l.startswith("# "):
            title = l[2:].strip(); body_start = i + 1; break
    # scan metadata lines after title
    j = body_start
    while j < len(lines) and not lines[j].startswith("## "):
        l = lines[j]
        if "arXiv" in l and "주제 분류" in l:
            ma = re.search(r"arXiv\*\*:\s*([\d.]+)", l)
            mt = re.search(r"주제 분류\*\*:\s*([^|]+)", l)
            md = re.search(r"출판일\*\*:\s*([^|]+)", l)
            mv = re.search(r"학회\*\*:\s*([^|]+)", l)
            if ma: meta_arxiv = ma.group(1).strip()
            if mt: topic = mt.group(1).strip()
            if md: pub_date = md.group(1).strip()
            if mv: venue = mv.group(1).strip()
        elif "저자" in l or "소속" in l:
            authors = re.sub(r"\*\*.*?\*\*:?", "", l).strip()
        elif "링크" in l:
            mk = re.search(r"(https?://\S+)", l)
            if mk: link = mk.group(1).strip()
        j += 1
    # Separate the "한 줄 요약" section to render as a lead line under the title.
    rest = lines[j:]
    lead = ""
    body_lines = []
    k = 0
    n = len(rest)
    while k < n:
        l = rest[k]
        m = re.match(r"^##\s+(.*)", l)
        if m and ("한 줄" in m.group(1) or "한줄" in m.group(1)):
            k += 1
            buf = []
            while k < n and not rest[k].startswith("## "):
                buf.append(rest[k].strip()); k += 1
            lead = " ".join(x for x in buf if x).strip()
        else:
            body_lines.append(l); k += 1
    lead_html = inline(lead) if lead else ""
    body_html = md_body_to_html(body_lines)
    return dict(title=title, arxiv=meta_arxiv, topic=topic, link=link,
               authors=authors, pub_date=pub_date, venue=venue,
               lead=lead_html, body=body_html, fname=os.path.basename(path))

files = sorted(glob.glob(os.path.join(SUMMARY_DIR, "*.md")))
papers = [parse_file(p) for p in files]

# group by topic preserving order
from collections import OrderedDict
groups = OrderedDict()
for p in papers:
    groups.setdefault(p["topic"], []).append(p)

date_kr = DATE
gen_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

cards = []
toc = []
idx = 0
for topic, plist in groups.items():
    color = topic_color(topic)
    toc.append(f'<div class="toc-group"><span class="toc-badge" style="background:{color}">{html.escape(topic)}</span><ul>')
    for p in plist:
        idx += 1
        pid = f"paper{idx}"
        toc.append(f'<li><a href="#{pid}">{html.escape(p["title"])}</a></li>')
        meta_bits = []
        if p["arxiv"]:
            meta_bits.append(f'<a class="pill" href="https://arxiv.org/abs/{p["arxiv"]}" target="_blank">arXiv:{p["arxiv"]}</a>')
            meta_bits.append(f'<a class="pill pdf" href="https://arxiv.org/pdf/{p["arxiv"]}" target="_blank">PDF</a>')
            meta_bits.append(f'<a class="pill" href="https://arxiv.org/html/{p["arxiv"]}" target="_blank">전문 HTML</a>')
        authors_html = f'<div class="authors">{inline(p["authors"])}</div>' if p["authors"] else ""
        lead_html = f'<p class="lead">{p["lead"]}</p>' if p.get("lead") else ""
        pub_bits = []
        if p.get("pub_date"):
            pub_bits.append(f'<span class="pub-date">📅 {html.escape(p["pub_date"])}</span>')
        if p.get("venue"):
            pub_bits.append(f'<span class="pub-venue">🏛 {html.escape(p["venue"])}</span>')
        pubinfo_html = f'<div class="pubinfo">{" · ".join(pub_bits)}</div>' if pub_bits else ""
        cards.append(f'''
<article class="card" id="{pid}">
  <div class="card-head" style="border-left-color:{color}">
    <span class="topic-tag" style="background:{color}">{html.escape(topic)}</span>
    <h2>{html.escape(p["title"])}</h2>
    {lead_html}
    {authors_html}
    {pubinfo_html}
    <div class="meta">{" ".join(meta_bits)}</div>
  </div>
  <div class="card-body">
    {p["body"]}
  </div>
</article>''')
    toc.append("</ul></div>")

topic_summary = " · ".join(f'{t} ({len(pl)})' for t, pl in groups.items())

html_doc = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>arXiv 논문 정리 — {date_kr}</title>
<script>
  window.MathJax = {{
    tex: {{ inlineMath: [['$','$'],['\\\\(','\\\\)']],
            displayMath: [['$$','$$'],['\\\\[','\\\\]']], processEscapes: true }},
    options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }}
  }};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" id="MathJax-script" async></script>
<style>
  :root {{ --bg:#f8fafc; --card:#ffffff; --ink:#1e293b; --muted:#64748b; --line:#e2e8f0; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Apple SD Gothic Neo","Noto Sans KR",sans-serif;
    line-height:1.7; }}
  .wrap {{ max-width:1100px; margin:0 auto; padding:0 20px 80px; }}
  header.top {{ background:linear-gradient(135deg,#1e293b,#334155); color:#fff; padding:42px 20px 36px; }}
  header.top .inner {{ max-width:1100px; margin:0 auto; }}
  header.top .home-link {{ display:inline-block; margin-bottom:14px; color:#cbd5e1; text-decoration:none;
    font-size:13.5px; background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.2);
    padding:6px 14px; border-radius:999px; }}
  header.top .home-link:hover {{ background:rgba(255,255,255,.2); color:#fff; }}
  header.top h1 {{ margin:0 0 8px; font-size:30px; letter-spacing:-.5px; }}
  header.top .sub {{ opacity:.85; font-size:15px; }}
  header.top .chips {{ margin-top:16px; display:flex; flex-wrap:wrap; gap:8px; }}
  header.top .chip {{ background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.2);
    padding:5px 12px; border-radius:999px; font-size:13px; }}
  .layout {{ display:grid; grid-template-columns:260px 1fr; gap:32px; margin-top:32px; }}
  nav.toc {{ position:sticky; top:20px; align-self:start; font-size:13.5px; max-height:90vh; overflow:auto; }}
  nav.toc h3 {{ font-size:13px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); margin:0 0 12px; }}
  .toc-group {{ margin-bottom:16px; }}
  .toc-badge {{ display:inline-block; color:#fff; font-size:11.5px; padding:3px 9px; border-radius:6px; margin-bottom:6px; font-weight:600; }}
  nav.toc ul {{ list-style:none; padding:0 0 0 4px; margin:6px 0 0; }}
  nav.toc li {{ margin:4px 0; }}
  nav.toc a {{ color:var(--ink); text-decoration:none; }}
  nav.toc a:hover {{ color:#6366f1; text-decoration:underline; }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:14px; margin-bottom:26px;
    overflow:hidden; box-shadow:0 1px 3px rgba(15,23,42,.05); scroll-margin-top:20px; }}
  .card-head {{ padding:22px 26px 18px; border-left:6px solid; background:#fcfcfd; }}
  .topic-tag {{ display:inline-block; color:#fff; font-size:11.5px; font-weight:600; padding:3px 10px; border-radius:6px; }}
  .card-head h2 {{ margin:10px 0 6px; font-size:21px; letter-spacing:-.3px; }}
  .lead {{ margin:6px 0 10px; font-size:14.5px; color:#334155; font-weight:500;
    border-left:3px solid var(--line); padding-left:12px; }}
  .authors {{ color:var(--muted); font-size:13px; margin-bottom:10px; }}
  .meta {{ display:flex; flex-wrap:wrap; gap:8px; }}
  .pill {{ font-size:12.5px; text-decoration:none; color:#475569; background:#f1f5f9; border:1px solid var(--line);
    padding:3px 10px; border-radius:999px; }}
  .pill.pdf {{ background:#fee2e2; border-color:#fecaca; color:#b91c1c; }}
  .pill:hover {{ filter:brightness(.96); }}
  .card-body {{ padding:8px 26px 24px; }}
  .card-body h3.sec {{ font-size:16.5px; margin:22px 0 8px; padding-bottom:6px; border-bottom:2px solid var(--line);
    color:#0f172a; }}
  .card-body h4.subsec {{ font-size:14.5px; margin:16px 0 6px; color:#334155; }}
  .card-body p {{ margin:8px 0; }}
  .card-body ul, .card-body ol {{ margin:8px 0; padding-left:22px; }}
  .card-body li {{ margin:4px 0; }}
  .card-body code {{ background:#f1f5f9; padding:1px 6px; border-radius:5px; font-size:13px;
    font-family:"SF Mono",Menlo,Consolas,monospace; }}
  .card-body strong {{ color:#0f172a; }}
  .tbl-wrap {{ overflow-x:auto; margin:12px 0; -webkit-overflow-scrolling:touch; }}
  .card-body table {{ border-collapse:collapse; width:100%; font-size:13px; min-width:340px; }}
  .card-body thead th {{ background:#f1f5f9; color:#0f172a; text-align:left; font-weight:700;
    padding:8px 12px; border-bottom:2px solid #cbd5e1; white-space:nowrap; vertical-align:bottom; }}
  .card-body tbody td {{ padding:7px 12px; border-bottom:1px solid var(--line); text-align:left;
    vertical-align:top; }}
  .card-body tbody tr:nth-child(even) {{ background:#f8fafc; }}
  .card-body th.num, .card-body td.num {{ text-align:right; font-variant-numeric:tabular-nums;
    font-family:"SF Mono",Menlo,Consolas,monospace; white-space:nowrap; }}
  .fig {{ margin:14px 0; text-align:center; }}
  .fig img {{ max-width:100%; height:auto; border:1px solid var(--line); border-radius:8px;
    background:#fff; }}
  .fig figcaption {{ margin-top:6px; font-size:12.5px; color:var(--muted); line-height:1.5; }}
  .pubinfo {{ margin:6px 0 2px; font-size:12.5px; color:var(--muted); display:flex;
    flex-wrap:wrap; gap:4px 12px; }}
  .pubinfo .pub-venue {{ color:#0f172a; font-weight:600; }}
  footer {{ text-align:center; color:var(--muted); font-size:13px; margin-top:40px; }}
  @media (max-width:820px) {{ .layout {{ grid-template-columns:1fr; }} nav.toc {{ position:static; max-height:none; }} }}
</style>
</head>
<body>
<header class="top"><div class="inner">
  <a class="home-link" href="../../index.html">← 전체 주차 목록(홈)</a>
  <h1>📚 arXiv 논문 주간 정리</h1>
  <div class="sub">{date_kr} · 총 {len(papers)}편 · 주제별 균형 정리</div>
  <div class="chips">
    {"".join(f'<span class="chip">{html.escape(t)} · {len(pl)}편</span>' for t,pl in groups.items())}
  </div>
</div></header>
<div class="wrap">
  <div class="layout">
    <nav class="toc">
      <h3>목차</h3>
      {"".join(toc)}
    </nav>
    <main>
      {"".join(cards)}
      <footer>생성: {gen_time} · 적합성은 abstract로 판단, 요약은 논문 전문 기반 작성</footer>
    </main>
  </div>
</div>
</body>
</html>'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html_doc)
print("WROTE", OUT, len(html_doc), "bytes,", len(papers), "papers")

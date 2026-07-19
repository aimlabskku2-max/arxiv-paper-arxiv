#!/usr/bin/env python3
"""
build_papers.py — 모든 주차 디제스트를 스캔해 검색·필터 가능한
전체 논문 관리 리스트(papers.html)를 생성한다.

스캔 대상: {BASE}/weekly/*/paper_summary/*.md  (스킬이 매주 만드는 논문별 디제스트)
사용:      python3 build_papers.py [BASE_DIR]   (기본값: 현재 폴더)
"""
import os, re, glob, json, html, sys

BASE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()

TOPIC_COLORS = {
    "egocentric vision": "#0ea5e9",
    "hand-object interaction": "#10b981",
    "spatial audio": "#6366f1",
    "video-to-audio": "#8b5cf6",
    "hand trajectory": "#f59e0b",
    "visuotactile": "#ef4444",
}
def topic_color(t):
    for k, v in TOPIC_COLORS.items():
        if k in (t or "").lower():
            return v
    return "#64748b"

def parse_md(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    title = arxiv = topic = pub = venue = authors = lead = ""
    for l in lines:
        if l.startswith("# "):
            title = l[2:].strip(); break
    for l in lines:
        if "arXiv" in l and "주제 분류" in l:
            m = re.search(r"arXiv\*\*:\s*([\d.]+)", l);  arxiv = m.group(1).strip() if m else ""
            m = re.search(r"주제 분류\*\*:\s*([^|]+)", l); topic = m.group(1).strip() if m else ""
            m = re.search(r"출판일\*\*:\s*([^|]+)", l);   pub = m.group(1).strip() if m else ""
            m = re.search(r"학회\*\*:\s*([^|]+)", l);     venue = m.group(1).strip() if m else ""
        elif l.startswith("**저자") or l.startswith("**소속"):
            authors = re.sub(r"\*\*.*?\*\*:?", "", l).strip()
    # 한 줄 요약 -> lead
    for i, l in enumerate(lines):
        if re.match(r"^##\s+", l) and ("한 줄" in l or "한줄" in l):
            buf = []
            for l2 in lines[i + 1:]:
                if l2.startswith("## "): break
                if l2.strip(): buf.append(l2.strip())
            lead = " ".join(buf); break
    # week (YYYY-MM-DD) from path
    week = ""
    for p in path.replace("\\", "/").split("/"):
        if re.match(r"^\d{4}-\d{2}-\d{2}$", p): week = p; break
    return dict(title=title, arxiv=arxiv, topic=topic, pub=pub or week,
                venue=venue, authors=authors, lead=lead, week=week,
                report=f"weekly/{week}/{week}_paper_summary.html" if week else "")

files = sorted(glob.glob(os.path.join(BASE, "weekly", "*", "paper_summary", "*.md")))
papers = [parse_md(f) for f in files]
# 최신 주차 -> 최신 출판일 순
papers.sort(key=lambda p: (p["week"], p["pub"], p["arxiv"]), reverse=True)

# 색상 매핑(주제별) — JS로 넘김
topics = []
for p in papers:
    if p["topic"] and p["topic"] not in topics:
        topics.append(p["topic"])
colors = {t: topic_color(t) for t in topics}

DATA = json.dumps(papers, ensure_ascii=False)
COLORS = json.dumps(colors, ensure_ascii=False)

HTML = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>논문 리스트 — arXiv Paper Archive</title>
<style>
  :root {{ --bg:#f7f8fa; --card:#fff; --ink:#0f172a; --muted:#64748b; --line:#e2e8f0; --accent:#6366f1; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#0b1120; --card:#131b2e; --ink:#e8edf6; --muted:#94a3b8; --line:#243049; }}
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Apple SD Gothic Neo","Noto Sans KR",sans-serif; }}
  header.top {{ background:linear-gradient(135deg,#1e293b,#334155); color:#fff; padding:34px 20px 26px; }}
  header.top .inner {{ max-width:1040px; margin:0 auto; }}
  header.top a.home {{ color:#cbd5e1; text-decoration:none; font-size:13px; }}
  header.top a.home:hover {{ color:#fff; }}
  header.top h1 {{ margin:8px 0 4px; font-size:24px; }}
  header.top p {{ margin:0; color:#cbd5e1; font-size:13.5px; }}
  .wrap {{ max-width:1040px; margin:0 auto; padding:20px 20px 64px; }}
  .controls {{ display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin:6px 0 16px; }}
  #q {{ flex:1; min-width:220px; padding:10px 14px; border:1px solid var(--line); border-radius:10px;
    background:var(--card); color:var(--ink); font-size:14px; }}
  .chips {{ display:flex; flex-wrap:wrap; gap:6px; }}
  .chip {{ border:1px solid var(--line); background:var(--card); color:var(--ink); cursor:pointer;
    font-size:12.5px; padding:5px 11px; border-radius:20px; user-select:none; }}
  .chip.active {{ color:#fff; border-color:transparent; }}
  .count {{ color:var(--muted); font-size:13px; margin:0 0 10px; }}
  table {{ border-collapse:collapse; width:100%; background:var(--card); border:1px solid var(--line);
    border-radius:12px; overflow:hidden; font-size:13.5px; }}
  thead th {{ text-align:left; background:#f1f5f9; color:#0f172a; font-weight:700; padding:10px 12px;
    border-bottom:2px solid #cbd5e1; white-space:nowrap; cursor:pointer; }}
  @media (prefers-color-scheme: dark) {{ thead th {{ background:#1b2740; color:#e8edf6; }} }}
  tbody td {{ padding:10px 12px; border-bottom:1px solid var(--line); vertical-align:top; }}
  tbody tr:hover {{ background:rgba(99,102,241,.06); }}
  .tp {{ display:inline-block; color:#fff; font-size:11px; font-weight:600; padding:2px 8px; border-radius:6px; white-space:nowrap; }}
  .ttl {{ font-weight:600; }}
  .ttl .lead {{ display:block; color:var(--muted); font-weight:400; font-size:12px; margin-top:2px; }}
  .date {{ font-variant-numeric:tabular-nums; white-space:nowrap; color:var(--muted); }}
  .lk a {{ color:var(--accent); text-decoration:none; font-size:12.5px; margin-right:8px; white-space:nowrap; }}
  .lk a:hover {{ text-decoration:underline; }}
  .empty {{ text-align:center; color:var(--muted); padding:40px; }}
  footer {{ text-align:center; color:var(--muted); font-size:12.5px; margin-top:28px; }}
  footer a {{ color:var(--accent); text-decoration:none; }}
</style>
</head>
<body>
<header class="top"><div class="inner">
  <a class="home" href="index.html">← 메인으로</a>
  <h1>📄 전체 논문 리스트</h1>
  <p>모든 주차 디제스트의 논문을 한곳에서 검색·필터로 관리</p>
</div></header>
<div class="wrap">
  <div class="controls">
    <input id="q" type="search" placeholder="제목·저자·arXiv ID·학회 검색…" oninput="render()">
    <div class="chips" id="chips"></div>
  </div>
  <div class="count" id="count"></div>
  <table>
    <thead><tr>
      <th onclick="sortBy('week')">주차 ▾</th>
      <th onclick="sortBy('topic')">주제</th>
      <th onclick="sortBy('title')">제목</th>
      <th onclick="sortBy('pub')">출판일</th>
      <th onclick="sortBy('venue')">학회</th>
      <th>링크</th>
    </tr></thead>
    <tbody id="rows"></tbody>
  </table>
  <div class="empty" id="empty" style="display:none">조건에 맞는 논문이 없어요.</div>
  <footer><a href="index.html">메인 페이지</a> · <a href="https://github.com/aimlabskku2-max/arxiv-paper-arxiv">GitHub</a></footer>
</div>
<script>
const PAPERS = {DATA};
const COLORS = {COLORS};
let activeTopic = "ALL";
let sortKey = "week", sortDir = -1;

function esc(s) {{ return (s||"").replace(/[&<>"]/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c])); }}

function buildChips() {{
  const box = document.getElementById("chips");
  const topics = ["ALL", ...Object.keys(COLORS)];
  box.innerHTML = topics.map(t => {{
    const c = t === "ALL" ? "#334155" : COLORS[t];
    const style = t === activeTopic ? `background:${{c}}` : "";
    const cls = t === activeTopic ? "chip active" : "chip";
    return `<span class="${{cls}}" style="${{style}}" onclick="setTopic('${{t.replace(/'/g,"\\\\'")}}')">${{t==="ALL"?"전체":esc(t)}}</span>`;
  }}).join("");
}}
function setTopic(t) {{ activeTopic = t; buildChips(); render(); }}
function sortBy(k) {{ if (sortKey===k) sortDir*=-1; else {{ sortKey=k; sortDir=(k==="week"||k==="pub")?-1:1; }} render(); }}

function render() {{
  const q = document.getElementById("q").value.trim().toLowerCase();
  let list = PAPERS.filter(p => activeTopic==="ALL" || p.topic===activeTopic);
  if (q) list = list.filter(p => (p.title+" "+p.authors+" "+p.arxiv+" "+p.venue+" "+p.lead).toLowerCase().includes(q));
  list.sort((a,b) => {{ const x=(a[sortKey]||""), y=(b[sortKey]||""); return x<y?-sortDir:x>y?sortDir:0; }});
  const rows = document.getElementById("rows");
  rows.innerHTML = list.map(p => {{
    const c = COLORS[p.topic] || "#64748b";
    const links = [];
    if (p.arxiv) {{
      links.push(`<a href="https://arxiv.org/abs/${{p.arxiv}}" target="_blank">arXiv</a>`);
      links.push(`<a href="https://arxiv.org/pdf/${{p.arxiv}}" target="_blank">PDF</a>`);
    }}
    if (p.report) links.push(`<a href="${{esc(p.report)}}#${{""}}" target="_blank">리포트</a>`);
    return `<tr>
      <td class="date">${{esc(p.week)}}</td>
      <td><span class="tp" style="background:${{c}}">${{esc(p.topic)}}</span></td>
      <td class="ttl">${{esc(p.title)}}${{p.lead?`<span class="lead">${{esc(p.lead)}}</span>`:""}}</td>
      <td class="date">${{esc(p.pub)}}</td>
      <td>${{esc(p.venue)}}</td>
      <td class="lk">${{links.join("")}}</td>
    </tr>`;
  }}).join("");
  document.getElementById("empty").style.display = list.length ? "none" : "block";
  document.getElementById("count").textContent = `${{list.length}}편 / 전체 ${{PAPERS.length}}편`;
}}
buildChips(); render();
</script>
</body>
</html>
'''

out = os.path.join(BASE, "papers.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"WROTE {out}  ({len(papers)} papers, {len(topics)} topics)")

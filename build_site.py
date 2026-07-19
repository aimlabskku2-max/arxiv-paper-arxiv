#!/usr/bin/env python3
"""
build_site.py — 저장소 루트 통합 랜딩 index.html 생성기 (비파괴)

  topics/topics.json          (큐레이션 서베이 목록, 수동 관리)  +
  weekly/<YYYY-MM-DD>/ 폴더    (주간 디제스트, 자동 스캔)          ->  index.html

주간 디제스트를 매주 새로 추가해도 서베이 섹션이 보존된다.
weekly 폴더를 직접 스캔하므로 별도 매니페스트(weekly.json)는 필요 없다.
사용:  python3 build_site.py [BASE_DIR]   (기본값: 현재 폴더)
"""
import json, os, re, sys, html, glob
from datetime import datetime

BASE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()

# 주제 -> 색상 (주간 디제스트 리포트의 배지 색과 맞춤)
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
        if k in t.lower():
            return v
    return "#64748b"

def load_json(path, default):
    p = os.path.join(BASE, path)
    if not os.path.exists(p):
        return default
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def topics_from_report(rel_path):
    """리포트 HTML에서 topic-tag 배지 텍스트를 순서 유지·중복 제거로 추출."""
    p = os.path.join(BASE, rel_path)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        htmltext = f.read()
    seen, out = set(), []
    for m in re.findall(r'class="topic-tag"[^>]*>([^<]+)<', htmltext):
        t = m.strip()
        if t and t not in seen:
            seen.add(t); out.append(t)
    return out

surveys = load_json("topics/topics.json", [])

# 주간 디제스트: weekly/<YYYY-MM-DD>/ 폴더를 자동 스캔 (수동 매니페스트 불필요).
weekly = []
for d in sorted(glob.glob(os.path.join(BASE, "weekly", "*"))):
    if not os.path.isdir(d):
        continue
    date = os.path.basename(d)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        continue
    rel = f"weekly/{date}/{date}_paper_summary.html"
    n = len(glob.glob(os.path.join(d, "paper_summary", "*.md")))
    weekly.append({"date": date, "path": rel, "count": n or None,
                   "topics": topics_from_report(rel)})
weekly.sort(key=lambda w: w["date"], reverse=True)

def chip(t):
    c = topic_color(t)
    return f'<span class="chip" style="background:{c}">{html.escape(t)}</span>'

# ---- 서베이 카드 ----
survey_cards = []
for s in surveys:
    exists = os.path.exists(os.path.join(BASE, s.get("path", "")))
    cnt = s.get("count")
    badge = f'<span class="count">{cnt}편</span>' if cnt else ''
    missing = '' if exists else '<span class="missing" title="파일이 아직 없음">준비중</span>'
    survey_cards.append(f'''      <a class="card" href="{html.escape(s['path'])}">
        <div class="card-top"><h3>{html.escape(s['title'])}</h3>{badge}{missing}</div>
        <p>{html.escape(s.get('desc',''))}</p>
      </a>''')

# ---- 주간 디제스트 행 (월별 그룹) ----
weekly_rows = []
cur_month = None
for w in weekly:
    date = w["date"]
    month = date[:7]  # YYYY-MM
    if month != cur_month:
        cur_month = month
        y, m = month.split("-")
        weekly_rows.append(f'      <div class="wmonth">{y}년 {int(m)}월</div>')
    tops = w.get("topics") or topics_from_report(w.get("path", ""))
    exists = os.path.exists(os.path.join(BASE, w.get("path", "")))
    cnt = w.get("count")
    cntt = f'<span class="wcount">{cnt}편</span>' if cnt else ''
    chips = " ".join(chip(t) for t in tops) if tops else '<span class="chip" style="background:#94a3b8">주간 디제스트</span>'
    missing = '' if exists else '<span class="missing">준비중</span>'
    weekly_rows.append(f'''      <a class="wrow" href="{html.escape(w['path'])}">
        <span class="wdate">{html.escape(date)}</span>
        <span class="wchips">{chips}</span>
        <span class="wmeta">{cntt}{missing}<span class="arrow">→</span></span>
      </a>''')

updated = ""
if weekly:
    updated = f"최근 업데이트: {weekly[0]['date']}"

HTML = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>arXiv Paper Archive</title>
<style>
  :root {{
    --bg:#f7f8fa; --card:#ffffff; --ink:#0f172a; --muted:#64748b;
    --line:#e2e8f0; --accent:#6366f1;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#0b1120; --card:#131b2e; --ink:#e8edf6; --muted:#94a3b8; --line:#243049; }}
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;
    line-height:1.6; }}
  .wrap {{ max-width:960px; margin:0 auto; padding:0 20px 64px; }}
  header.top {{ background:linear-gradient(135deg,#1e293b,#334155); color:#fff;
    padding:48px 20px 40px; text-align:center; }}
  header.top h1 {{ margin:0 0 8px; font-size:30px; letter-spacing:-.02em; }}
  header.top p {{ margin:0; color:#cbd5e1; font-size:15px; }}
  header.top .foci {{ margin-top:14px; font-size:12.5px; color:#94a3b8; }}
  header.top .papers-link {{ display:inline-block; margin-top:18px; padding:9px 18px;
    background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.25); border-radius:22px;
    color:#fff; text-decoration:none; font-size:13.5px; font-weight:600; }}
  header.top .papers-link:hover {{ background:rgba(255,255,255,.22); }}
  section {{ margin-top:44px; }}
  section h2 {{ font-size:14px; text-transform:uppercase; letter-spacing:.09em;
    color:var(--muted); margin:0 0 16px; font-weight:700; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:14px; }}
  .card {{ display:block; background:var(--card); border:1px solid var(--line);
    border-radius:14px; padding:18px 18px 16px; text-decoration:none; color:inherit;
    transition:transform .12s ease, box-shadow .12s ease, border-color .12s ease; }}
  .card:hover {{ transform:translateY(-2px); box-shadow:0 8px 24px rgba(0,0,0,.10);
    border-color:var(--accent); }}
  .card-top {{ display:flex; align-items:center; gap:8px; margin-bottom:6px; flex-wrap:wrap; }}
  .card h3 {{ margin:0; font-size:16px; flex:1; min-width:60%; }}
  .count {{ background:var(--accent); color:#fff; font-size:11.5px; font-weight:600;
    padding:2px 8px; border-radius:20px; white-space:nowrap; }}
  .missing {{ background:#475569; color:#fff; font-size:11px; padding:2px 8px;
    border-radius:20px; }}
  .card p {{ margin:0; color:var(--muted); font-size:13.5px; }}
  .weekly {{ display:flex; flex-direction:column; gap:8px; }}
  .wmonth {{ font-size:12.5px; font-weight:700; color:var(--muted); letter-spacing:.03em;
    margin:14px 0 2px; padding-left:2px; }}
  .wmonth:first-child {{ margin-top:0; }}
  .wrow {{ display:flex; align-items:center; gap:14px; background:var(--card);
    border:1px solid var(--line); border-radius:12px; padding:14px 16px;
    text-decoration:none; color:inherit; transition:border-color .12s, transform .12s; }}
  .wrow:hover {{ border-color:var(--accent); transform:translateX(2px); }}
  .wdate {{ font-variant-numeric:tabular-nums; font-weight:700; font-size:14.5px;
    white-space:nowrap; }}
  .wchips {{ flex:1; display:flex; gap:6px; flex-wrap:wrap; }}
  .chip {{ color:#fff; font-size:11px; font-weight:600; padding:2px 9px; border-radius:6px;
    white-space:nowrap; }}
  .wmeta {{ display:flex; align-items:center; gap:8px; color:var(--muted); font-size:12.5px; }}
  .wcount {{ font-weight:600; }}
  .arrow {{ font-size:16px; }}
  footer {{ text-align:center; color:var(--muted); font-size:12.5px; margin-top:48px; }}
  footer a {{ color:var(--accent); text-decoration:none; }}
</style>
</head>
<body>
  <header class="top">
    <h1>arXiv Paper Archive</h1>
    <p>분야별 핵심 논문 서베이 &amp; 주간 최신 논문 디제스트</p>
    <div class="foci">Video-to-Audio · Egocentric Vision · Hand-Object Interaction · Spatial Audio · Tactile</div>
    <a class="papers-link" href="papers.html">📄 전체 논문 리스트 →</a>
  </header>
  <div class="wrap">

    <section>
      <h2>Topic Surveys</h2>
      <div class="grid">
{os.linesep.join(survey_cards)}
      </div>
    </section>

    <section>
      <h2>Weekly Digests</h2>
      <div class="weekly">
{os.linesep.join(weekly_rows)}
      </div>
    </section>

    <footer>
      {html.escape(updated)} · <a href="https://github.com/aimlabskku2-max/arxiv-paper-arxiv">GitHub</a>
    </footer>
  </div>
</body>
</html>
'''

out = os.path.join(BASE, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"WROTE {out}  ({len(surveys)} surveys, {len(weekly)} weekly)")

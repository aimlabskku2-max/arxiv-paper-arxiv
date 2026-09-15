#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the hand-in-wholebody survey HTML from cards/*.md."""
import os, re, html, glob

HERE = os.path.dirname(os.path.abspath(__file__))
CARDS = os.path.join(HERE, "cards")
OUT = os.path.join(HERE, "hand-in-wholebody_survey.html")

SLUG = "hand-in-wholebody"
TITLE = "전신 3D 포즈 추정에서의 손 통합 — 핵심 계보 서베이"
SUBTITLE = "Hand-in-Whole-Body 3D Pose: Integrating Hand Experts into Whole-Body Estimation"
ANCHOR = "arXiv:2603.14726 (Hand4Whole++, CVPR 2026)를 도착점으로, 그 선행 계보를 통합 관점에서 정리"

def parse_card(path):
    d = {"title": "", "meta": "", "link": "", "oneline": "", "contrib": "", "integration": ""}
    for line in open(path, encoding="utf-8"):
        s = line.rstrip("\n")
        if s.startswith("## "):
            d["title"] = s[3:].strip()
        m = re.match(r"- (\w+):\s*(.*)", s)
        if m and m.group(1) in d:
            d[m.group(1)] = m.group(2).strip()
    return d

def esc(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    # linkify bare arxiv abs urls inside text
    t = re.sub(r"(?<![\">=])(https?://[^\s<)]+)", r'<a href="\1" target="_blank">\1</a>', t)
    return t

def contrib_items(t):
    return [c.strip() for c in re.split(r"[;；]", t) if c.strip()]

# narrative structure: (group heading, description, [card stems])
GROUPS = [
    ("① 표현형 전신 모델의 토대",
     "손·얼굴·몸을 하나의 파라메트릭 모델로 묶어, 이후 모든 계보가 추정할 공통 언어(SMPL-X)를 정의한 출발점.",
     ["01_SMPL-X"]),
    ("② 분리 추정 → 통합: 모듈형 계보",
     "손을 전용 모듈로 잘 뽑은 뒤 몸에 이어 붙이는 전략과, 손목·정합을 정교화한 흐름.",
     ["02_FrankMocap", "03_Hand4Whole", "04_PyMAF-X"]),
    ("③ 단일 단계·스케일업 전신 모델",
     "손을 따로 크롭·재추정하지 않고 하나의 네트워크·대규모 학습으로 전신을 통째로 추정하는 방향.",
     ["05_OSX", "06_SMPLer-X", "09_AiOS"]),
    ("④ 손 전용 전문가 (frozen hand experts)",
     "손 크롭에 집중해 손을 매우 정밀하게 복원하지만 전신 맥락은 갖지 못하는, 통합의 '손 쪽' 재료.",
     ["07_HaMeR", "08_WiLoR"]),
    ("⑤ 경량 어댑터로 통합 — CHAM의 이웃과 도착점",
     "고정된 백본 위에 경량 어댑터를 얹어 손·몸을 결합하는 최신 흐름과, 이 서베이의 도착점.",
     ["10_HMR-Adapter", "00_Hand4Whole++"]),
]

cards = {os.path.splitext(os.path.basename(p))[0]: parse_card(p)
         for p in glob.glob(os.path.join(CARDS, "*.md"))}

sections = []
for gi, (gtitle, gdesc, stems) in enumerate(GROUPS, 1):
    body = [f'<h2 class="grp">{html.escape(gtitle)}</h2>',
            f'<p class="grp-desc">{esc(gdesc)}</p>']
    for stem in stems:
        c = cards.get(stem)
        if not c:
            continue
        anchor = stem == "00_Hand4Whole++"
        cls = "card anchor" if anchor else "card"
        meta = html.escape(c["meta"])
        link = c["link"].strip()
        title_html = html.escape(c["title"])
        if link.startswith("http"):
            title_html = f'<a href="{link}" target="_blank">{title_html}</a>'
        items = "".join(f"<li>{esc(x)}</li>" for x in contrib_items(c["contrib"]))
        badge = '<span class="anchor-badge">이 서베이의 도착점</span>' if anchor else ""
        sections.append("")  # spacer
        body.append(f'''
    <article class="{cls}">
      <div class="c-head">{badge}<h3>{title_html}</h3><div class="c-meta">{meta}</div></div>
      <div class="c-body">
        <p class="oneline">{esc(c["oneline"])}</p>
        <h4>핵심 기여</h4>
        <ul>{items}</ul>
        <h4>통합 관점에서의 위치</h4>
        <p>{esc(c["integration"])}</p>
      </div>
    </article>''')
    sections.append("\n".join(body))

n_papers = len([s for g in GROUPS for s in g[2]])

doc = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITLE)}</title>
<style>
  :root {{ --bg:#f8fafc; --card:#fff; --ink:#1e293b; --muted:#64748b; --line:#e2e8f0; --accent:#10b981; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Apple SD Gothic Neo","Noto Sans KR",sans-serif;
    line-height:1.7; }}
  header.top {{ background:linear-gradient(135deg,#064e3b,#10b981); color:#fff; padding:42px 20px 34px; }}
  header.top .wrap {{ max-width:960px; margin:0 auto; }}
  header.top a.home {{ display:inline-block; margin-bottom:16px; color:#fff; text-decoration:none;
    font-size:13.5px; background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.25);
    padding:6px 12px; border-radius:8px; }}
  header.top a.home:hover {{ background:rgba(255,255,255,.22); }}
  header.top h1 {{ margin:6px 0 8px; font-size:26px; letter-spacing:-.4px; }}
  header.top .sub {{ opacity:.92; font-size:15px; }}
  header.top .chips {{ margin-top:14px; }}
  header.top .chip {{ display:inline-block; background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.22);
    padding:4px 11px; border-radius:20px; font-size:12.5px; margin:3px 6px 3px 0; }}
  main {{ max-width:960px; margin:0 auto; padding:30px 20px 60px; }}
  .intro {{ background:var(--card); border:1px solid var(--line); border-left:5px solid var(--accent);
    border-radius:12px; padding:20px 24px; margin-bottom:28px; }}
  .intro h2 {{ margin:0 0 8px; font-size:18px; }}
  .intro p {{ margin:8px 0; }}
  .flow {{ display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:14px 0 2px; }}
  .flow span.step {{ background:#ecfdf5; border:1px solid #a7f3d0; color:#065f46; border-radius:8px;
    padding:5px 10px; font-size:12.5px; font-weight:600; }}
  .flow span.arrow {{ color:var(--muted); font-weight:700; }}
  h2.grp {{ font-size:19px; margin:34px 0 4px; padding-bottom:8px; border-bottom:2px solid var(--line); }}
  p.grp-desc {{ color:var(--muted); margin:6px 0 14px; font-size:14px; }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:13px; margin:14px 0;
    box-shadow:0 1px 2px rgba(0,0,0,.04); overflow:hidden; }}
  .card.anchor {{ border:2px solid var(--accent); box-shadow:0 3px 14px rgba(16,185,129,.15); }}
  .c-head {{ padding:16px 22px 10px; background:#fcfdfc; border-bottom:1px solid var(--line); }}
  .card.anchor .c-head {{ background:#ecfdf5; }}
  .c-head h3 {{ margin:4px 0 4px; font-size:17.5px; letter-spacing:-.2px; }}
  .c-head h3 a {{ color:#0f172a; text-decoration:none; }}
  .c-head h3 a:hover {{ color:var(--accent); text-decoration:underline; }}
  .c-meta {{ color:var(--muted); font-size:13px; font-variant-numeric:tabular-nums; }}
  .anchor-badge {{ display:inline-block; background:var(--accent); color:#fff; font-size:11.5px;
    font-weight:700; padding:2px 9px; border-radius:12px; }}
  .c-body {{ padding:12px 22px 18px; }}
  .c-body .oneline {{ font-size:15px; font-weight:500; color:#0f172a; margin:6px 0 10px; }}
  .c-body h4 {{ font-size:13.5px; color:#334155; margin:14px 0 4px; text-transform:none; }}
  .c-body ul {{ margin:6px 0; padding-left:20px; }}
  .c-body li {{ margin:4px 0; }}
  .c-body a {{ color:#0369a1; }}
  footer {{ max-width:960px; margin:0 auto; padding:20px; color:var(--muted); font-size:12.5px; border-top:1px solid var(--line); }}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <a class="home" href="../../index.html">← 메인으로</a>
  <h1>{html.escape(TITLE)}</h1>
  <div class="sub">{html.escape(SUBTITLE)}</div>
  <div class="chips">
    <span class="chip">📄 {n_papers}편</span>
    <span class="chip">통합 중심 계보</span>
    <span class="chip">{html.escape(ANCHOR)}</span>
  </div>
</div></header>
<main>
  <div class="intro">
    <h2>왜 이 주제인가 — "손을 몸 안에서" 복원하기</h2>
    <p>전신(whole-body) 3D 포즈 추정의 오랜 난제는 <strong>손</strong>이다. 전신 추정기는 몸 전체를 보지만 학습 데이터에 손 다양성이 부족해 손가락이 뭉개지고, 손 전용(hand-only) 추정기는 손을 정밀하게 복원하지만 팔·몸통과의 연결(전역 맥락)을 알지 못한다. 이 <strong>지도(supervision) 격차</strong>를 어떻게 메우느냐가 계보 전체를 관통하는 질문이다.</p>
    <p>아래는 그 질문에 답해 온 흐름을, 도착점 <strong>Hand4Whole++</strong>(고정된 전신·손 전문가를 경량 어댑터 CHAM으로 결합)를 기준으로 되짚은 것이다.</p>
    <div class="flow">
      <span class="step">SMPL-X (공통 표현)</span><span class="arrow">→</span>
      <span class="step">분리 추정 후 통합</span><span class="arrow">→</span>
      <span class="step">단일 단계·스케일업</span><span class="arrow">→</span>
      <span class="step">강력한 손 전문가</span><span class="arrow">→</span>
      <span class="step">어댑터로 결합 (CHAM)</span>
    </div>
  </div>
  {"".join(sections)}
  <div class="intro" style="margin-top:30px; border-left-color:#0ea5e9;">
    <h2>우리 연구실 관심과의 연결</h2>
    <p><strong>Hand-Object Interaction</strong>: 손·물체·몸이 함께 등장하는 조작 장면에서, 손 전용 정밀도와 전신 맥락을 동시에 확보하는 CHAM식 통합은 접촉·파지 추정의 안정적 전신 사전(prior)으로 쓸 수 있다.</p>
    <p><strong>Egocentric Vision</strong>: 1인칭 영상은 손이 크게 잡히고 몸은 거의 안 보이는 극단적 조건이라, "고정된 전문가 + 어댑터"로 손을 몸 맥락에 정합시키는 접근이 특히 유효하다.</p>
  </div>
</main>
<footer>자동 생성 · topics/{SLUG}/build_survey.py · 수치·링크는 각 논문 원문/arXiv에서 검증한 것만 포함.</footer>
</body>
</html>'''

open(OUT, "w", encoding="utf-8").write(doc)
print(f"WROTE {OUT}  ({n_papers} papers, {len(GROUPS)} groups)")

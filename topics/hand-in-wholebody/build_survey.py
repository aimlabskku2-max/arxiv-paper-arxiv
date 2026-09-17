#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the hand-in-wholebody survey HTML (scientific-report style) from cards/*.md."""
import os, re, html, glob

HERE = os.path.dirname(os.path.abspath(__file__))
CARDS = os.path.join(HERE, "cards")
OUT = os.path.join(HERE, "hand-in-wholebody_survey.html")

TITLE = "전신 3D 포즈에서의 손 통합 — 핵심 계보 서베이"
SUBTITLE = ("전신(whole-body) 추정기는 몸 전체를 보지만 손이 뭉개지고, 손 전용 추정기는 손을 정밀하게 "
            "복원하지만 몸 맥락을 모른다. 이 supervision 격차를 어떻게 메워 왔는지를, 도착점 "
            "Hand4Whole++(CVPR 2026)를 기준으로 되짚는다.")

def parse_card(path):
    d = {"title": "", "meta": "", "link": "", "oneline": "", "contrib": "", "hand": "", "integration": ""}
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
    t = re.sub(r"(?<![\">=])(https?://[^\s<)]+)", r'<a href="\1" target="_blank" rel="noopener">\1</a>', t)
    return t

def contrib_items(t):
    return [c.strip() for c in re.split(r"[;；]", t) if c.strip()]

# (kind, section label, heading, tag, [(stem, stream)])
#   kind: 'stage' = 본류(하나의 계보를 이루는 단계) | 'branch' = 별도로 발전해 합류하는 병렬 계열
#   stream: 'vision'(whole-body) | 'smell'(hand) | 'anchor'
GROUPS = [
    ("stage", "단계 01", "공통 표현의 토대",
     "손·얼굴·몸을 하나의 파라메트릭 모델로 묶어, 이후 이 계보 전체가 추정할 공통 언어(SMPL-X)를 정의한 출발점.",
     [("01_SMPL-X", "vision")]),
    ("stage", "단계 02", "분리 추정 → 통합 (모듈형)",
     "손을 전용 모듈로 잘 뽑은 뒤 몸에 이어 붙이는 전략과, 손목·정합을 정교화한 흐름.",
     [("02_FrankMocap", "vision"), ("03_Hand4Whole", "vision"), ("04_PyMAF-X", "vision")]),
    ("stage", "단계 03", "단일 단계·스케일업 전신 모델",
     "손을 따로 크롭·재추정하지 않고 하나의 네트워크·대규모 학습으로 전신을 통째로 추정하는 방향.",
     [("05_OSX", "vision"), ("06_SMPLer-X", "vision"), ("09_AiOS", "vision")]),
    ("branch", "병렬 계열 · 손 전문가", "따로 발전해 온 손 전용 복원",
     "이 줄기의 단계가 아니라, 손만을 대상으로 따로 발전해 온 별도 계열이다. 손은 매우 정밀하게 복원하지만 "
     "전신 맥락은 갖지 못하며, 아래 단계 04에서 ‘재료’로 합류한다.",
     [("07_HaMeR", "smell"), ("08_WiLoR", "smell")]),
    ("stage", "단계 04", "어댑터로 결합 — 두 계열의 합류점",
     "본류(전신)와 병렬 계열(손 전문가)이 만나는 지점. 고정된 백본 위에 경량 어댑터를 얹어 둘을 잇는 최신 흐름이자, "
     "이 서베이의 도착점.",
     [("10_HMR-Adapter", "vision"), ("00_Hand4Whole++", "anchor")]),
    ("next", "이후 · 2026~", "갈라지는 후속 흐름 — 시간축 · 도메인 · 데이터",
     "도착점 이후 나온 흐름은 하나의 다음 단계가 아니라 세 갈래로 갈린다. Hand4Whole++는 supervision 격차를 "
     "‘어댑터로 잇기’로 풀었는데, 이들은 각각 **시간축으로 메우기**(DanceHMR), "
     "**도메인을 1인칭으로 옮겨 다시 묻기**(ICIP 2026), **데이터로 정면 공략하기**(Human4K)로 답한다. "
     "다만 셋 다 2026년 9월 기준 Hand4Whole++를 인용하지는 않는다 — 직접 계승이 아니라 같은 격차에 대한 병렬 응답으로 읽어야 한다.",
     [("11_DanceHMR", "next"), ("12_EgoWholeBodyHMR", "next"), ("13_Human4K", "next")]),
]

cards = {os.path.splitext(os.path.basename(p))[0]: parse_card(p)
         for p in glob.glob(os.path.join(CARDS, "*.md"))}
n_papers = sum(len(g[4]) for g in GROUPS)

CSS = """
*{box-sizing:border-box}
:root{
  --bg:#FAFAF9; --surface:#FFFFFF; --surface-2:#F5F5F3;
  --ink:#171717; --muted:#666A70; --faint:#9A9DA1; --line:#E8E7E3;
  --smell:#A9662E; --vision:#176F78; --next:#5B4B8A;
  --best:rgba(23,111,120,.07); --best-line:#176F78;
  --shadow:0 1px 2px rgba(0,0,0,.025),0 8px 24px rgba(0,0,0,.035);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#131619; --surface:#1B1F23; --surface-2:#22272C;
  --ink:#ECEFF2; --muted:#A3ADB7; --faint:#6B7580; --line:#2B3138;
  --smell:#D8945A; --vision:#3FB6C0; --next:#A79AD8; --best:rgba(63,182,192,.13); --best-line:#3FB6C0;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 6px 22px rgba(0,0,0,.35);
}}
body{background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans",system-ui,sans-serif;
  line-height:1.62;margin:0;-webkit-font-smoothing:antialiased}
.wrap{max-width:980px;margin:0 auto;padding:60px 28px 110px}
a{color:var(--vision)}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:11px;font-weight:500;letter-spacing:.16em;
  text-transform:uppercase;color:var(--faint)}
.home{font-family:"IBM Plex Mono",monospace;font-size:12px;text-decoration:none;color:var(--muted);
  display:inline-block;margin-bottom:22px;border:1px solid var(--line);border-radius:7px;padding:5px 11px}
.home:hover{color:var(--vision);border-color:var(--vision)}
header{border-bottom:1px solid var(--line);padding-bottom:34px}
h1{font-size:clamp(30px,5vw,44px);font-weight:650;letter-spacing:-.03em;margin:.55rem 0 .6rem;text-wrap:balance}
.sub{color:var(--muted);font-size:16px;line-height:1.65;max-width:74ch;margin:0}
.meta-chips{margin-top:18px;display:flex;flex-wrap:wrap;gap:8px}
.chip{font-family:"IBM Plex Mono",monospace;font-size:11.5px;background:var(--surface-2);
  border:1px solid var(--line);border-radius:20px;padding:4px 11px;color:var(--muted)}
section{margin-top:64px;padding-top:4px}
.sec-head{display:block;margin-bottom:8px}
.sec-no{display:block;font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--vision);margin-bottom:5px}
.sec-no.branch{color:var(--smell)} .sec-no.next{color:var(--next)}
.branch-note,.next-note{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.06em;
  border-radius:20px;padding:1px 8px;display:inline-block;margin-bottom:6px}
.branch-note{color:var(--smell);border:1px solid var(--smell)}
.next-note{color:var(--next);border:1px solid var(--next)}
section.branch{border-left:2px dashed var(--smell);padding-left:22px;margin-left:2px}
section.next{border-top:1px solid var(--line);margin-top:72px;padding-top:34px}
h2{font-size:clamp(22px,3.4vw,27px);font-weight:620;letter-spacing:-.025em;margin:0}
.sec-tag{color:var(--muted);font-size:15px;line-height:1.6;margin:8px 0 26px;max-width:74ch}
/* two-stream schematic */
.qa-lab{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--faint);margin:30px 0 10px}
.legend{display:flex;gap:18px;flex-wrap:wrap;font-size:12.5px;color:var(--muted);margin:2px 0 6px}
.legend span{display:inline-flex;align-items:center;gap:7px}
.dot{width:9px;height:9px;border-radius:50%;display:inline-block}
.dot.v{background:var(--vision)} .dot.s{background:var(--smell)}
.flow-wrap{overflow-x:auto;padding:8px 0 12px;margin:14px 0 6px}
.merge,.flow{display:flex;align-items:center;min-width:min-content}
.streams{display:flex;flex-direction:column;gap:12px}
.stream{display:flex;align-items:center}
.node{background:var(--surface);border:1px solid var(--line);border-radius:9px;padding:11px 14px;
  min-width:150px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:3px}
.node.v{box-shadow:inset 0 2px 0 var(--vision),var(--shadow)}
.node.s{box-shadow:inset 0 2px 0 var(--smell),var(--shadow)}
.node .role{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--faint)}
.node .nm{font-size:13px;font-weight:600;line-height:1.25}
.node .tiny{font-size:11px;color:var(--muted)}
.arrow{padding:0 10px;color:var(--faint);font-size:16px;display:flex;align-items:center}
.out{background:var(--surface-2);border:1px dashed var(--line);border-radius:9px;padding:11px 15px;
  min-width:140px;display:flex;flex-direction:column;gap:3px}
.out .role{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint)}
.out .nm{font-size:13.5px;font-weight:700}
.out .tiny{font-size:11px;color:var(--muted)}
/* stage rail */
.rail{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:6px 0 2px}
.rail .step{font-family:"IBM Plex Mono",monospace;font-size:12px;font-weight:600;background:var(--surface-2);
  border:1px solid var(--line);border-radius:8px;padding:5px 11px;color:var(--ink)}
.rail .step.s{box-shadow:inset 0 2px 0 var(--smell)} .rail .step.v{box-shadow:inset 0 2px 0 var(--vision)}
.rail .step.n{box-shadow:inset 0 2px 0 var(--next)}
.rail .ar{color:var(--faint);font-weight:700}
.rail.sub{margin-top:8px;padding-left:2px}
.rail .merge-note{font-size:12px;color:var(--muted)}
/* paper cards */
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);
  padding:20px 22px;margin-top:18px;border-top:3px solid var(--line)}
.card.v{border-top-color:var(--vision)} .card.s{border-top-color:var(--smell)}
.card.next{border-top-color:var(--next)}
.card.next .take{border-left-color:var(--next)}
.card.next .take .lab{color:var(--next)}
.handnote{font-size:13.5px;color:var(--muted);margin:6px 0 0;padding:10px 13px;
  background:var(--surface-2);border-radius:8px}
.card.anchor{border:2px solid var(--best-line);border-top:3px solid var(--best-line);background:var(--best)}
.card .c-role{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase;
  color:var(--faint);display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.badge{font-family:"IBM Plex Mono",monospace;font-size:9.5px;font-weight:700;letter-spacing:.05em;
  text-transform:uppercase;background:var(--best-line);color:#fff;border-radius:12px;padding:2px 8px}
.card h3{font-size:18px;font-weight:620;letter-spacing:-.015em;margin:7px 0 5px;line-height:1.3}
.card h3 a{color:var(--ink);text-decoration:none}
.card h3 a:hover{color:var(--vision);text-decoration:underline}
.card .cmeta{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--muted);
  font-variant-numeric:tabular-nums;margin-bottom:12px}
.card .oneline{font-size:15px;font-weight:500;color:var(--ink);margin:8px 0 12px}
.card h4{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--faint);margin:14px 0 5px}
.card ul{margin:6px 0;padding-left:19px} .card li{margin:4px 0;font-size:14px}
.take{margin-top:14px;padding:13px 16px;border-left:2px solid var(--vision);background:var(--surface-2);
  border-radius:0 8px 8px 0;font-size:14px;line-height:1.6}
.card.s .take{border-left-color:var(--smell)}
.take .lab{font-family:"IBM Plex Mono",monospace;font-size:9.8px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--vision);display:block;margin-bottom:4px}
.card.s .take .lab{color:var(--smell)}
.closing{margin-top:40px}
.closing .take{border-left-color:var(--vision);background:var(--surface)}
.closing .take + .take{margin-top:12px}
footer{margin-top:70px;padding-top:22px;border-top:1px solid var(--line);font-size:12.5px;color:var(--faint);line-height:1.6}
@media(max-width:560px){.wrap{padding:40px 18px 76px}.streams{gap:9px}}
"""

def card_html(stem, stream):
    c = cards.get(stem)
    if not c:
        return ""
    is_anchor = stream == "anchor"
    cls = "card anchor" if is_anchor else f"card {stream}"
    role = {"anchor": "도착점 · anchor", "smell": "손 전용 전문가",
            "next": "후속 흐름 · 2026~", "vision": "전신 계보"}.get(stream, "전신 계보")
    badge = '<span class="badge">이 서베이의 도착점</span>' if is_anchor else ""
    title = html.escape(c["title"])
    link = c["link"].strip()
    if link.startswith("http"):
        title = f'<a href="{link}" target="_blank" rel="noopener">{title}</a>'
    items = "".join(f"<li>{esc(x)}</li>" for x in contrib_items(c["contrib"]))
    hand_block = (f'<h4>손 주석 관련</h4><p class="handnote">{esc(c["hand"])}</p>'
                  if c.get("hand") else "")
    take_lab = "후속 흐름에서의 위치" if stream == "next" else "통합 관점에서의 위치"
    return f"""
    <article class="{cls}">
      <div class="c-role">{role}{badge}</div>
      <h3>{title}</h3>
      <div class="cmeta">{html.escape(c['meta'])}</div>
      <p class="oneline">{esc(c['oneline'])}</p>
      <h4>핵심 기여</h4>
      <ul>{items}</ul>
      {hand_block}
      <div class="take"><span class="lab">{take_lab}</span>{esc(c['integration'])}</div>
    </article>"""

secs = []
for kind, label, heading, tag, members in GROUPS:
    body = "".join(card_html(stem, stream) for stem, stream in members)
    cls = f"section {kind}" if kind in ("branch", "next") else "section"
    no_cls = f"sec-no {kind}" if kind in ("branch", "next") else "sec-no"
    note = ""
    if kind == "branch":
        note = '<span class="branch-note">본류의 단계가 아닌 별도 계열</span>'
    elif kind == "next":
        note = '<span class="next-note">도착점 이후 · 직접 계승 아님</span>'
    secs.append(f"""
  <section class="{cls}">
    <div class="sec-head"><span class="{no_cls}">{html.escape(label)}</span>{note}<h2>{html.escape(heading)}</h2></div>
    <p class="sec-tag">{esc(tag)}</p>
    {body}
  </section>""")

doc = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITLE)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <a class="home" href="../../index.html">← 메인으로</a>
  <header>
    <div class="eyebrow">3D whole-body pose · lineage survey</div>
    <h1>{html.escape(TITLE)}</h1>
    <p class="sub">{html.escape(SUBTITLE)}</p>
    <div class="meta-chips">
      <span class="chip">{n_papers} papers</span>
      <span class="chip">anchor · arXiv:2603.14726</span>
      <span class="chip">Hand4Whole++ · CVPR 2026</span>
      <span class="chip">후속 흐름 3편 포함 (2026-09 기준)</span>
    </div>
  </header>

  <div class="sec-head" style="margin-top:48px"><span class="sec-no">System overview</span><h2>두 스트림을 어떻게 합치는가</h2></div>
  <p class="sec-tag">이 분야의 핵심은 두 전문가 — 전신(whole-body) 추정기와 손 전용 추정기 — 를 하나로 잇는 방법이다.
    도착점 Hand4Whole++는 둘을 모두 고정한 채 경량 어댑터 CHAM으로 손 특징을 전신 스트림에 주입한다.</p>
  <div class="qa-lab">Merge schematic</div>
  <div class="legend"><span><i class="dot v"></i> 전신 스트림 (whole-body)</span><span><i class="dot s"></i> 손 스트림 (hand expert)</span></div>
  <div class="flow-wrap"><div class="merge">
    <div class="streams">
      <div class="stream"><div class="node v"><span class="role">whole-body</span><span class="nm">SMPLer-X (frozen)</span><span class="tiny">전신 SMPL-X 특징</span></div></div>
      <div class="stream"><div class="node s"><span class="role">hand expert</span><span class="nm">HaMeR / WiLoR (frozen)</span><span class="tiny">정밀 손 특징</span></div></div>
    </div>
    <div class="arrow">→</div>
    <div class="node v"><span class="role">adapter</span><span class="nm">CHAM</span><span class="tiny">손 특징으로 전신 변조</span></div>
    <div class="arrow">→</div>
    <div class="out"><span class="role">output</span><span class="nm">Hand4Whole++</span><span class="tiny">몸과 정합된 손·손목</span></div>
  </div></div>
  <div class="qa-lab" style="margin-top:26px">Lineage at a glance</div>
  <div class="rail">
    <span class="step v">01 · 공통 표현 (SMPL-X)</span><span class="ar">→</span>
    <span class="step v">02 · 분리 추정 후 통합</span><span class="ar">→</span>
    <span class="step v">03 · 단일 단계·스케일업</span><span class="ar">→</span>
    <span class="step v">04 · 어댑터로 결합 (CHAM)</span>
  </div>
  <div class="rail sub">
    <span class="step s">병렬 계열 · 손 전용 전문가</span>
    <span class="ar">↗</span><span class="merge-note">따로 발전하다 단계 04에서 합류</span>
  </div>
  <div class="rail sub">
    <span class="merge-note">단계 04 이후 세 갈래로 분기 →</span>
    <span class="step n">시간축 · DanceHMR</span>
    <span class="step n">1인칭 · ICIP 2026</span>
    <span class="step n">데이터 · Human4K</span>
  </div>
{''.join(secs)}

  <section class="closing">
    <div class="sec-head"><span class="sec-no">Takeaways</span><h2>우리 연구실 관심과의 연결</h2></div>
    <div class="take"><span class="lab">Hand-Object Interaction</span>손·물체·몸이 함께 등장하는 조작 장면에서, 손 전용 정밀도와 전신 맥락을 동시에 확보하는 CHAM식 통합은 접촉·파지 추정의 안정적 전신 사전(prior)으로 쓸 수 있다.</div>
    <div class="take"><span class="lab">Egocentric Vision</span>1인칭 영상은 손이 크게 잡히고 몸은 거의 안 보이는 극단적 조건이라, ‘고정된 전문가 + 어댑터’로 손을 몸 맥락에 정합시키는 접근이 특히 유효하다.</div>
  </section>

  <footer>자동 생성 · topics/hand-in-wholebody/build_survey.py · 스타일: scientific-report(IBM Plex, light/dark) · 수치·링크는 각 논문 원문/arXiv에서 검증한 것만 포함.</footer>
</div>
</body>
</html>"""

open(OUT, "w", encoding="utf-8").write(doc)
print(f"WROTE {OUT}  ({n_papers} papers, {len(GROUPS)} groups)")

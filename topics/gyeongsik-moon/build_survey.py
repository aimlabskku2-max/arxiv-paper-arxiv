#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Gyeongsik Moon research-lineage survey (failure-narrative framing)."""
import os, re, html, glob

HERE = os.path.dirname(os.path.abspath(__file__))
CARDS = os.path.join(HERE, "cards")
OUT = os.path.join(HERE, "gyeongsik-moon_survey.html")

TITLE = "Gyeongsik Moon 연구 계보 — 실패 서사로 읽기"
SUB = ("한 연구자가 8년간 무엇을 의심해 왔는지를, 논문마다 "
       "‘문제 정의 → 나이브한 접근 → 실패 관찰 → 원인 가설 → 검증’ 다섯 단계로 되짚는다. "
       "각 단계는 논문이 Introduction·Related Work에서 실제로 주장한 내용에서만 뽑았다.")

KEYS = ["meta", "link", "short", "problem", "naive", "failure", "hypothesis", "method", "pattern"]

def parse_card(path):
    d = {k: "" for k in KEYS}
    d["title"] = ""
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

GROUPS = [
    ("시기 01", "서울대 박사 (2015–2021) — 표현을 의심하다",
     "출발점은 일관되게 ‘출력 표현’이었다. 좌표나 파라미터를 직접 회귀하는 당연한 관행을 의심하고, "
     "공간 정보를 보존하는 표현(voxel · lixel · positional pose)으로 갈아끼운다. "
     "이 시기 후반에는 병목이 모델이 아니라 데이터·주석이라는 인식이 겹쳐 들어온다.",
     ["01_V2V-PoseNet", "02_RootNet", "03_I2L-MeshNet",
      "04_InterHand2.6M", "05_NeuralAnnot", "06_Hand4Whole"]),
    ("시기 02", "Meta Reality Labs (2022–2024) — 야외로, 그리고 아바타로",
     "실험실에서 되던 것이 야외에서 깨지는 문제(도메인 간극)를 정면으로 다루고, "
     "이어서 관심이 ‘포즈를 맞히기’에서 ‘개인화된 아바타를 만들기’로 옮겨간다. "
     "이미 잘 되는 모델·사전(prior)을 얼린 채 잇고 개인화하는 방식이 이때부터 굳는다.",
     ["07_InterWild", "08_ReInterHand", "09_UHM", "10_ExAvatar"]),
    ("시기 03", "고려대 VCAI (2025–) — 고정하고 잇기의 완성형",
     "전신 속 손이라는, 박사 시절부터 붙들던 문제로 돌아오되 답이 달라졌다. "
     "이제는 아무것도 다시 학습시키지 않고 얇은 어댑터 하나만 학습한다.",
     ["11_Hand4WholePP"]),
]

PATTERNS = [
    ("A", "직접 회귀를 의심한다",
     "좌표·파라미터를 곧장 회귀하는 관행을 깨고, 공간 정보를 보존하는 표현으로 바꾼다.",
     "V2V-PoseNet · I2L-MeshNet · Hand4Whole · (UHM 일부)"),
    ("B", "병목이 데이터면 데이터를 만든다",
     "모델을 더 만지는 대신, 없는 데이터셋과 주석을 직접 만들어 문제의 바닥을 옮긴다.",
     "InterHand2.6M · NeuralAnnot · Re:InterHand"),
    ("C", "잘 되는 것은 고정하고 잇는다",
     "이미 잘 학습된 모델·사전을 재학습하지 않고, 도메인을 맞추거나 얇은 어댑터로 연결한다.",
     "InterWild · UHM · ExAvatar · Hand4Whole++"),
]

STEPS = [("problem", "01 문제 정의", "p"), ("naive", "02 나이브한 접근", "n"),
         ("failure", "03 실패 관찰", "f"), ("hypothesis", "04 원인 가설", "h"),
         ("method", "05 검증 · 방법론", "m")]

# 연도 | 약칭 | 제목 | 학회 | arXiv | 역할
TIMELINE = [
    ("2016", "—", "A Sequential Approach to 3D Human Pose Estimation", "ECCV 2016", "", "공저"),
    ("2017", "—", "Holistic Planimetric Prediction to Local Volumetric Prediction", "arXiv", "1706.04758", "1저자"),
    ("2018", "V2V-PoseNet", "Voxel-to-Voxel Prediction Network for 3D Hand and Human Pose", "CVPR 2018", "1711.07399", "1저자"),
    ("2019", "PoseFix", "Model-agnostic General Human Pose Refinement Network", "CVPR 2019", "1812.03595", "1저자"),
    ("2019", "MSA R-CNN", "Multi-Scale Aggregation R-CNN for 2D Multi-Person Pose", "CVPRW 2019", "1905.03912", "1저자"),
    ("2019", "RootNet", "Camera Distance-aware Top-down Approach for 3D Multi-person Pose", "ICCV 2019", "1907.11346", "1저자"),
    ("2020", "I2L-MeshNet", "Image-to-Lixel Prediction Network for 3D Pose and Mesh", "ECCV 2020", "2008.03713", "1저자"),
    ("2020", "DeepHandMesh", "Weakly-Supervised Framework for High-Fidelity Hand Mesh Modeling", "ECCV 2020 (Oral)", "2008.08213", "1저자"),
    ("2020", "InterHand2.6M", "Dataset and Baseline for 3D Interacting Hand Pose", "ECCV 2020", "2008.09309", "1저자"),
    ("2020", "Pose2Mesh", "GCN for 3D Human Pose and Mesh Recovery from a 2D Pose", "ECCV 2020", "2008.09047", "공동1저자"),
    ("2021", "TCMR", "Beyond Static Features for Temporally Consistent 3D Pose and Shape", "CVPR 2021", "2011.08627", "공저"),
    ("2021", "IntegralAction", "Pose-driven Feature Integration for Action Recognition", "CVPRW 2021 (Oral)", "2007.06317", "공동1저자"),
    ("2022", "NeuralAnnot", "Neural Annotator for 3D Human Mesh Training Sets", "CVPRW 2022", "2011.11232", "1저자"),
    ("2022", "Hand4Whole", "Accurate 3D Hand Pose Estimation for Whole-Body 3D Human Mesh", "CVPRW 2022 (Oral)", "2011.11534", "1저자"),
    ("2022", "HandOccNet", "Occlusion-Robust 3D Hand Mesh Estimation Network", "CVPR 2022", "2203.14564", "공동1저자"),
    ("2022", "3DCrowdNet", "Robust 3D Human Mesh from In-the-Wild Crowded Scenes", "CVPR 2022", "2104.07300", "공저"),
    ("2022", "ClothWild", "3D Clothed Human Reconstruction in the Wild", "ECCV 2022", "2207.10053", "공동1저자"),
    ("2022", "MonoNHR", "Monocular Neural Human Renderer", "3DV 2022", "2210.00627", "공동1저자"),
    ("2023", "MultiAct", "Long-Term 3D Human Motion Generation from Multiple Action Labels", "AAAI 2023 (Oral)", "2212.05897", "공동1저자"),
    ("2023", "—", "Rethinking Self-Supervised Pre-training for 3D Pose and Shape", "ICLR 2023", "2303.05370", "공저"),
    ("2023", "BlurHand", "Recovering 3D Hand Mesh Sequence from a Single Blurry Image", "CVPR 2023", "2303.15417", "공저"),
    ("2023", "InterWild", "Bringing Inputs to Shared Domains for 3D Interacting Hands in the Wild", "CVPR 2023", "2303.13652", "단독저자"),
    ("2023", "Three Recipes", "Three Recipes for Better 3D Pseudo-GTs of 3D Human Mesh", "CVPRW 2023", "", "1저자"),
    ("2023", "EANet", "Extract-and-Adaptation Network for 3D Interacting Hand Mesh", "ICCVW 2023 (Oral)", "", "공동1저자"),
    ("2023", "Re:InterHand", "A Dataset of Relighted 3D Interacting Hands", "NeurIPS 2023 (D&B)", "2310.17768", "1저자"),
    ("2024", "URHand", "Universal Relightable Hands", "CVPR 2024 (Oral)", "2401.05334", "공저"),
    ("2024", "CONTHO", "Joint Reconstruction of 3D Human and Object via Contact-Based Refinement", "CVPR 2024", "2404.04819", "공저"),
    ("2024", "UHM", "Authentic Hand Avatar from a Phone Scan via Universal Hand Model", "CVPR 2024", "2405.07933", "1저자"),
    ("2024", "ExAvatar", "Expressive Whole-Body 3D Gaussian Avatar", "ECCV 2024", "2407.21686", "1저자"),
    ("2024", "EBH", "3D Hand Sequence Recovery from Real Blurry Images and Event Stream", "ECCV 2024", "", "공저"),
    ("2024", "Codec Avatar Studio", "Paired Human Captures for Complete, Driveable, Generalizable Avatars", "NeurIPS 2024 (D&B)", "", "공저"),
    ("2025", "PARTE", "Part-Guided Texturing for 3D Human Reconstruction from a Single Image", "ICCV 2025", "2507.17332", "교신"),
    ("2025", "PERSONA", "Personalized Whole-Body 3D Avatar with Pose-Driven Deformations", "ICCV 2025", "2508.09973", "시니어"),
    ("2026", "Hand4Whole++", "Enhancing Hands in 3D Whole-Body Pose Estimation with CHAM", "CVPR 2026", "2603.14726", "단독저자"),
    ("2026", "DynaAvatar", "Zero-Shot Animatable 3D Avatars with Cloth Dynamics from a Single Image", "CVPR 2026", "2603.14772", "시니어"),
    ("2026", "SIGNER", "Temporally Grounded Sign Language Generation", "ECCV 2026", "2506.07460", "교신"),
]

cards = {os.path.splitext(os.path.basename(p))[0]: parse_card(p)
         for p in glob.glob(os.path.join(CARDS, "*.md"))}
n_cards = sum(len(g[3]) for g in GROUPS)

CSS = """
*{box-sizing:border-box}
:root{
  --bg:#FAFAF9; --surface:#FFFFFF; --surface-2:#F5F5F3;
  --ink:#171717; --muted:#666A70; --faint:#9A9DA1; --line:#E8E7E3;
  --fail:#A9662E; --vision:#176F78; --hyp:#5B4B8A;
  --shadow:0 1px 2px rgba(0,0,0,.025),0 8px 24px rgba(0,0,0,.035);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#131619; --surface:#1B1F23; --surface-2:#22272C;
  --ink:#ECEFF2; --muted:#A3ADB7; --faint:#6B7580; --line:#2B3138;
  --fail:#D8945A; --vision:#3FB6C0; --hyp:#A79AD8;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 6px 22px rgba(0,0,0,.35);
}}
body{background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans",system-ui,sans-serif;
  line-height:1.62;margin:0;-webkit-font-smoothing:antialiased}
.wrap{max-width:1000px;margin:0 auto;padding:60px 28px 110px}
a{color:var(--vision)}
.mono{font-family:"IBM Plex Mono",monospace}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--faint)}
.home{font-family:"IBM Plex Mono",monospace;font-size:12px;text-decoration:none;color:var(--muted);
  display:inline-block;margin-bottom:22px;border:1px solid var(--line);border-radius:7px;padding:5px 11px}
.home:hover{color:var(--vision);border-color:var(--vision)}
header{border-bottom:1px solid var(--line);padding-bottom:34px}
h1{font-size:clamp(30px,5vw,44px);font-weight:650;letter-spacing:-.03em;margin:.55rem 0 .6rem;text-wrap:balance}
.sub{color:var(--muted);font-size:16px;line-height:1.65;max-width:76ch;margin:0}
.meta-chips{margin-top:18px;display:flex;flex-wrap:wrap;gap:8px}
.chip{font-family:"IBM Plex Mono",monospace;font-size:11.5px;background:var(--surface-2);
  border:1px solid var(--line);border-radius:20px;padding:4px 11px;color:var(--muted)}
section{margin-top:62px}
.sec-head{display:block;margin-bottom:8px}
.sec-no{display:block;font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--vision);margin-bottom:5px}
h2{font-size:clamp(21px,3.3vw,26px);font-weight:620;letter-spacing:-.025em;margin:0}
.sec-tag{color:var(--muted);font-size:15px;line-height:1.62;margin:8px 0 24px;max-width:76ch}
.qa-lab{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint);margin:30px 0 10px}
/* 5-step rail */
.rail{display:flex;flex-wrap:wrap;gap:7px;align-items:center;margin:8px 0 2px}
.rail .st{font-family:"IBM Plex Mono",monospace;font-size:11.5px;font-weight:600;
  background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:5px 10px}
.rail .st.p{box-shadow:inset 0 2px 0 var(--faint)}
.rail .st.n{box-shadow:inset 0 2px 0 var(--muted)}
.rail .st.f{box-shadow:inset 0 2px 0 var(--fail)}
.rail .st.h{box-shadow:inset 0 2px 0 var(--hyp)}
.rail .st.m{box-shadow:inset 0 2px 0 var(--vision)}
.rail .ar{color:var(--faint);font-weight:700}
/* pattern cards */
.pat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin-top:16px}
.pat{background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:16px 18px;box-shadow:var(--shadow)}
.pat .k{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;
  color:#fff;background:var(--vision);border-radius:12px;padding:2px 9px;display:inline-block}
.pat.b .k{background:var(--fail)} .pat.c .k{background:var(--hyp)}
.pat h4{font-size:15.5px;font-weight:620;margin:10px 0 5px}
.pat p{font-size:13.5px;color:var(--muted);margin:0 0 9px}
.pat .who{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--ink);
  background:var(--surface-2);border-radius:7px;padding:6px 9px;display:block}
/* paper cards */
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);
  padding:20px 22px;margin-top:20px;border-top:3px solid var(--vision)}
.card .c-role{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--faint)}
.card h3{font-size:18px;font-weight:620;letter-spacing:-.015em;margin:7px 0 4px;line-height:1.3}
.card h3 a{color:var(--ink);text-decoration:none}
.card h3 a:hover{color:var(--vision);text-decoration:underline}
.card .short{font-family:"IBM Plex Mono",monospace;font-size:12.5px;font-weight:600;color:var(--vision)}
.card .cmeta{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--muted);
  font-variant-numeric:tabular-nums;margin:4px 0 14px}
.steps{display:flex;flex-direction:column;gap:0;border-left:2px solid var(--line);padding-left:0;margin-top:6px}
.srow{display:grid;grid-template-columns:132px 1fr;gap:14px;padding:11px 0 11px 16px;
  border-left:3px solid transparent;margin-left:-2px}
.srow .sl{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--faint);padding-top:3px}
.srow p{margin:0;font-size:14px}
.srow.p{border-left-color:var(--faint)}
.srow.n{border-left-color:var(--muted)}
.srow.f{border-left-color:var(--fail);background:color-mix(in srgb,var(--fail) 5%,transparent)}
.srow.f .sl{color:var(--fail)}
.srow.h{border-left-color:var(--hyp);background:color-mix(in srgb,var(--hyp) 6%,transparent)}
.srow.h .sl{color:var(--hyp)}
.srow.m{border-left-color:var(--vision)}
.srow.m .sl{color:var(--vision)}
.take{margin-top:15px;padding:13px 16px;border-left:2px solid var(--vision);background:var(--surface-2);
  border-radius:0 8px 8px 0;font-size:13.8px;line-height:1.6}
.take .lab{font-family:"IBM Plex Mono",monospace;font-size:9.8px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--vision);display:block;margin-bottom:4px}
/* timeline table */
.tbl-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;margin-top:16px}
table{border-collapse:collapse;width:100%;background:var(--surface);font-size:13px}
th,td{text-align:left;padding:9px 13px;border-bottom:1px solid var(--line);white-space:nowrap}
thead th{font-family:"IBM Plex Mono",monospace;font-size:9.8px;letter-spacing:.09em;text-transform:uppercase;
  color:var(--faint);font-weight:500;background:var(--surface-2)}
tbody tr:last-child td{border-bottom:none}
td.yr{font-family:"IBM Plex Mono",monospace;color:var(--muted);font-variant-numeric:tabular-nums}
td.ttl{white-space:normal;min-width:280px}
td.sh{font-weight:600}
tr.key td{background:color-mix(in srgb,var(--vision) 5%,transparent)}
.note-sm{font-size:12.5px;color:var(--muted);margin:10px 2px 0}
footer{margin-top:70px;padding-top:22px;border-top:1px solid var(--line);
  font-size:12.5px;color:var(--faint);line-height:1.6}
@media(max-width:620px){.wrap{padding:40px 18px 76px}.srow{grid-template-columns:1fr;gap:4px}}
"""

KEYPAPERS = {"V2V-PoseNet", "RootNet", "I2L-MeshNet", "InterHand2.6M", "NeuralAnnot",
             "Hand4Whole", "InterWild", "Re:InterHand", "UHM", "ExAvatar", "Hand4Whole++"}

def card_html(stem):
    c = cards.get(stem)
    if not c:
        return ""
    title = html.escape(c["title"])
    link = c["link"].strip()
    if link.startswith("http"):
        title = f'<a href="{link}" target="_blank" rel="noopener">{title}</a>'
    rows = "".join(
        f'<div class="srow {cl}"><span class="sl">{lab}</span><p>{esc(c[k])}</p></div>'
        for k, lab, cl in STEPS if c.get(k))
    return f"""
    <article class="card">
      <div class="c-role">{html.escape(c['short'])}</div>
      <h3>{title}</h3>
      <div class="cmeta">{html.escape(c['meta'])}</div>
      <div class="steps">{rows}</div>
      <div class="take"><span class="lab">반복 패턴</span>{esc(c['pattern'])}</div>
    </article>"""

secs = []
for label, heading, tag, members in GROUPS:
    body = "".join(card_html(s) for s in members)
    secs.append(f"""
  <section>
    <div class="sec-head"><span class="sec-no">{html.escape(label)}</span><h2>{html.escape(heading)}</h2></div>
    <p class="sec-tag">{esc(tag)}</p>
    {body}
  </section>""")

pat_html = "".join(
    f'<div class="pat {k.lower()}"><span class="k">패턴 {k}</span><h4>{html.escape(t)}</h4>'
    f'<p>{esc(d)}</p><span class="who">{html.escape(w)}</span></div>'
    for k, t, d, w in PATTERNS)

rows = []
for yr, sh, ttl, venue, aid, role in TIMELINE:
    key = ' class="key"' if sh in KEYPAPERS else ""
    link = f'<a href="https://arxiv.org/abs/{aid}" target="_blank" rel="noopener">{aid}</a>' if aid else '<span style="color:var(--faint)">—</span>'
    rows.append(f'<tr{key}><td class="yr">{yr}</td><td class="sh">{html.escape(sh)}</td>'
                f'<td class="ttl">{html.escape(ttl)}</td><td>{html.escape(venue)}</td>'
                f'<td class="mono">{link}</td><td>{html.escape(role)}</td></tr>')
table_html = "".join(rows)

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
    <div class="eyebrow">Researcher lineage · failure-narrative reading</div>
    <h1>{html.escape(TITLE)}</h1>
    <p class="sub">{html.escape(SUB)}</p>
    <div class="meta-chips">
      <span class="chip">핵심 {n_cards}편 정독</span>
      <span class="chip">전체 연표 {len(TIMELINE)}편</span>
      <span class="chip">SNU → Meta → 고려대 VCAI</span>
      <span class="chip">도착점 · Hand4Whole++ (CVPR 2026)</span>
    </div>
  </header>

  <div class="sec-head" style="margin-top:46px"><span class="sec-no">Reading frame</span><h2>왜 실패 서사로 읽는가</h2></div>
  <p class="sec-tag">좋은 논문은 대개 “무엇을 했는가”보다 <strong>“왜 그게 필요했는가”</strong>로 설명된다.
    ViT를 예로 들면 — 비전에는 CNN의 귀납 편향이 필수라는 당연한 가정을 의심하고(문제 정의), 이미지를 패치로 잘라
    트랜스포머를 그대로 써 보고(나이브), ImageNet 규모에서 ResNet보다 못한 결과를 만나고(실패), 귀납 편향이 약해
    데이터가 적을 때 학습 효율이 낮다고 짚은 뒤(가설), 대규모 사전학습으로 뒤집는다(검증).
    아래 논문들도 같은 다섯 칸에 넣어 읽는다.</p>
  <div class="rail">
    <span class="st p">01 문제 정의</span><span class="ar">→</span>
    <span class="st n">02 나이브한 접근</span><span class="ar">→</span>
    <span class="st f">03 실패 관찰</span><span class="ar">→</span>
    <span class="st h">04 원인 가설</span><span class="ar">→</span>
    <span class="st m">05 검증 · 방법론</span>
  </div>

  <section>
    <div class="sec-head"><span class="sec-no">Meta-pattern</span><h2>8년간 반복된 세 가지 수법</h2></div>
    <p class="sec-tag">논문 열한 편을 나란히 놓으면 같은 사고 습관이 반복된다.
      시기가 바뀌면 다루는 대상(손 → 전신 → 아바타)은 달라져도, 병목을 공략하는 방식은 아래 셋으로 수렴한다.</p>
    <div class="pat-grid">{pat_html}</div>
  </section>
{''.join(secs)}

  <section>
    <div class="sec-head"><span class="sec-no">Appendix</span><h2>전체 논문 연표</h2></div>
    <p class="sec-tag">여러 출처(ML Anthology · VCAI Lab · SNU CVLab · Korea Univ. Pure · arXiv)를 교차 확인한 목록.
      진한 배경은 위에서 정독한 핵심 {n_cards}편이다.</p>
    <div class="tbl-wrap"><table>
      <thead><tr><th>연도</th><th>약칭</th><th>제목</th><th>학회</th><th>arXiv</th><th>역할</th></tr></thead>
      <tbody>{table_html}</tbody>
    </table></div>
    <p class="note-sm">※ arXiv 칸의 “—”는 arXiv 판본을 확인하지 못한 경우다(존재 여부 미확인이며 추측하지 않았다).
      워크숍·챌린지 리포트 일부(NTIRE 2019 등 주 연구주제와 무관한 공저)는 생략했다.
      Pose2Pose→Hand4Whole, NeuralAnnot 초판→학회판은 같은 arXiv ID의 제목 변경 이력이다.</p>
  </section>

  <footer>자동 생성 · topics/gyeongsik-moon/build_survey.py · 다섯 단계는 각 논문의 Introduction·Related Work에서 저자가 실제로 편 주장만 옮겼고, 수치는 논문 표·본문에 있는 값만 인용했다.</footer>
</div>
</body>
</html>"""

open(OUT, "w", encoding="utf-8").write(doc)
print(f"WROTE {OUT}  ({n_cards} cards, {len(TIMELINE)} timeline rows)")

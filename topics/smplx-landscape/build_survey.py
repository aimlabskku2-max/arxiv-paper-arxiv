#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the SMPL-X ecosystem landscape map survey."""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "smplx-landscape_survey.html")

TITLE = "SMPL-X 생태계 지도 — 어디서 갈라지는가"
SUB = ("3D 인체 연구는 SMPL-X라는 공통 표현을 허브로 삼아 갈라진다. "
       "갈래를 가르는 것은 주제가 아니라 <b>SMPL-X를 향한 화살표의 방향</b>이다. "
       "읽어내는가(추정), 만들어내는가(생성), 보이게 하는가(아바타), 세상과 엮는가(상호작용) — "
       "그리고 그 모두를 떠받치는 데이터.")

# ── 지도: SMPL-X를 기준으로 한 5가지 관계 ────────────────────────────
RELATIONS = [
    ("est", "추정", "이미지 · 영상", "→", "SMPL-X", "세상에서 파라미터를 읽어낸다"),
    ("gen", "생성", "텍스트 · 음성 · 대화", "→", "SMPL-X", "없는 모션을 만들어낸다"),
    ("av", "아바타", "SMPL-X", "→", "픽셀 · 보이는 사람", "파라미터를 사람으로 렌더한다"),
    ("int", "상호작용", "SMPL-X", "+", "물체 · 사람 · 환경", "사람을 세상과 엮는다"),
    ("data", "데이터", "⊥", "", "위 모든 갈래", "네 갈래 전부의 상한을 정한다"),
]

# ── 갈래별: (id, 번호, 제목, 관계식, 설명, 대표논문[(제목,arxiv,venue,note)], 하위분기[(이름, [(약칭,arxiv,venue)])]) ──
BRANCHES = [
    ("est", "갈래 01", "추정 — 이미지·영상에서 SMPL-X를 읽어낸다",
     "이미지 · 영상 → SMPL-X",
     "이 저장소가 지금까지 가장 깊이 판 갈래다. 내부에서 다시 ‘무엇을 입력으로 보는가’에 따라 "
     "전신 통합 · 손 전용 · 시간축 · 1인칭 · 다중인물로 갈린다. "
     "출력이 곧 다른 갈래들의 원료가 되기 때문에, 여기의 정확도가 생태계 전체의 바닥을 이룬다.",
     [("Hand4Whole++ (CHAM)", "2603.14726", "CVPR 2026",
       "전신 추정기와 손 전용 추정기를 모두 얼린 채 경량 어댑터로 잇는다. 이 갈래 안에서도 "
       "‘전신’과 ‘손’이 서로 다른 데이터로 학습돼 갈라져 있다는 사실 자체를 문제로 삼은 논문."),
      ("SMPLer-X", "2309.17448", "NeurIPS 2023 D&B",
       "450만 인스턴스로 스케일업한 전신 파운데이션 모델. 아키텍처가 아니라 데이터·규모로 통합을 밀어붙인 쪽 대표."),
      ("HaMeR", "2312.05251", "CVPR 2024",
       "손만 보는 전용 전문가. 정밀하지만 몸 맥락이 없다. 뒤에서 보듯 생성 갈래가 학습 데이터를 만들 때 "
       "실제로 가져다 쓰는 부품이라, 이 갈래 밖으로 가장 멀리 퍼진 논문이기도 하다.")],
     [("전신 통합 (whole-body)", [("SMPL-X", "1904.05866", "CVPR 2019"), ("FrankMocap", "2108.06428", "ICCVW 2021"),
                              ("Hand4Whole", "2011.11534", "CVPRW 2022"), ("PyMAF-X", "2207.06400", "TPAMI 2023"),
                              ("OSX", "2303.16160", "CVPR 2023"), ("SMPLer-X", "2309.17448", "NeurIPS 2023"),
                              ("AiOS", "2403.17934", "CVPR 2024"), ("HMR-Adapter", "", "ACM MM 2024"),
                              ("Hand4Whole++", "2603.14726", "CVPR 2026")]),
      ("손 전용 (hand expert)", [("HandOccNet", "2203.14564", "CVPR 2022"), ("InterWild", "2303.13652", "CVPR 2023"),
                            ("HaMeR", "2312.05251", "CVPR 2024"), ("WiLoR", "2409.12259", "CVPR 2025")]),
      ("출력 표현의 전환", [("V2V-PoseNet", "1711.07399", "CVPR 2018"), ("I2L-MeshNet", "2008.03713", "ECCV 2020"),
                      ("Pose2Mesh", "2008.09047", "ECCV 2020")]),
      ("시간축 (video)", [("TCMR", "2011.08627", "CVPR 2021"), ("DanceHMR", "2605.18102", "프리프린트 2026")]),
      ("1인칭 (egocentric)", [("Egocentric WB-HMR", "2605.08606", "ICIP 2026"), ("EgoForce", "2605.12498", "SIGGRAPH 2026")]),
      ("다중인물 · 야외", [("RootNet", "1907.11346", "ICCV 2019"), ("3DCrowdNet", "2104.07300", "CVPR 2022")])]),

    ("data", "갈래 02", "데이터 · 주석 — 모든 갈래의 바닥",
     "⊥ 위 모든 갈래",
     "다른 네 갈래의 성능 상한을 여기서 정한다. 내부는 <b>획득 경로</b>로 갈린다. "
     "스튜디오 모션캡처(정확하지만 좁다), 영상에 추정기를 돌린 자동 주석(넓지만 추정기 품질에 묶인다), "
     "그리고 합성·릴라이팅(둘의 절충). 같은 SMPL-X 파라미터라도 어느 경로로 왔느냐에 따라 노이즈 성격이 전혀 다르다.",
     [("Re:InterHand", "2310.17768", "NeurIPS 2023 D&B",
       "자기 전작 InterHand2.6M을 ‘랩 데이터셋’의 대표로 세워두고 “images have monotonous appearances”라고 못 박은 뒤 "
       "릴라이팅으로 다시 만든다. 정확도와 다양성을 동시에 얻으려는 제3의 경로."),
      ("NeuralAnnot", "2011.11232", "CVPRW 2022",
       "야외 이미지에 3D 정답이 없다는 병목을, 사람이 아니라 신경망 주석기로 메운다. "
       "‘추정 결과를 정답처럼 쓴다’는 이 생태계의 습관이 여기서 제도화된다."),
      ("Human4K", "2607.13646", "프리프린트 2026",
       "8시점 4K · 600만 장 · Vicon 정밀 SMPL-X. Hand4Whole++가 어댑터로 우회한 supervision 격차를 "
       "데이터 쪽에서 정면으로 푸는 최신 시도.")],
     [("스튜디오 mocap", [("InterHand2.6M", "2008.09309", "ECCV 2020"), ("BEAT", "2203.05297", "ECCV 2022"),
                     ("BEAT2 (EMAGE)", "2401.00374", "CVPR 2024"), ("Human4K", "2607.13646", "프리프린트 2026"),
                     ("Codec Avatar Studio", "", "NeurIPS 2024 D&B")]),
      ("자동 pseudo-GT", [("NeuralAnnot", "2011.11232", "CVPRW 2022"), ("Three Recipes", "", "CVPRW 2023"),
                       ("Converse3D (ViBES)", "2512.14234", "CVPR 2026")]),
      ("합성 · 릴라이팅", [("Re:InterHand", "2310.17768", "NeurIPS 2023")]),
      ("전신 + 언어 라벨", [("Motion-X", "2307.00818", "NeurIPS 2023 D&B"), ("HumanML3D", "", "CVPR 2022")])]),

    ("av", "갈래 03", "아바타 · 렌더링 — 파라미터를 보이는 사람으로",
     "SMPL-X → 픽셀",
     "추정과 생성이 만들어낸 파라미터는 그 자체로는 뼈대일 뿐이다. 이 갈래가 그것을 사람으로 만든다. "
     "내부는 <b>무엇으로 표면을 표현하는가</b>로 갈린다 — 파라메트릭 메시, 신경 렌더링·3D Gaussian, 그리고 릴라이터블 모델.",
     [("ExAvatar", "2407.21686", "ECCV 2024",
       "SMPL-X 메시와 3D Gaussian Splatting을 결합해 표정·손까지 되는 전신 아바타를 만든다. "
       "‘파라미터 → 사람’ 변환의 현재 대표형이고, 생성 갈래가 비워둔 자리를 정확히 채운다."),
      ("UHM", "2405.07933", "CVPR 2024",
       "수십 대 카메라 스튜디오가 아니라 폰 스캔만으로 개인화한다. 아바타를 연구실 밖으로 꺼낸 전환점."),
      ("URHand", "2401.05334", "CVPR 2024",
       "시점·포즈·조명·ID에 걸쳐 일반화되는 릴라이터블 손 모델. 데이터 갈래의 릴라이팅 아이디어와 짝을 이룬다.")],
     [("파라메트릭 모델", [("SMPL-X", "1904.05866", "CVPR 2019"), ("DeepHandMesh", "2008.08213", "ECCV 2020"),
                    ("UHM", "2405.07933", "CVPR 2024")]),
      ("신경 렌더링 · 3DGS", [("MonoNHR", "2210.00627", "3DV 2022"), ("ExAvatar", "2407.21686", "ECCV 2024"),
                         ("PERSONA", "2508.09973", "ICCV 2025"), ("DynaAvatar", "2603.14772", "CVPR 2026")]),
      ("릴라이터블", [("URHand", "2401.05334", "CVPR 2024")])]),

    ("gen", "갈래 04", "생성 — 조건에서 SMPL-X를 만들어낸다",
     "텍스트 · 음성 · 대화 → SMPL-X",
     "추정과 화살표 방향이 정반대인 갈래. 내부는 <b>무엇을 조건으로 주는가</b>로 갈린다. "
     "여기서 가장 흥미로운 사실은 <b>손이 뒤늦게 합류했다</b>는 것이다. "
     "텍스트→모션은 HumanML3D의 22관절 몸통 표현이 사실상 표준이 되면서 약 2년간 손·얼굴을 아예 생성할 수 없었고, "
     "음성→제스처는 립싱크와 손짓이 과제의 본질이라 SMPL-X 전신으로 먼저 수렴했다.",
     [("EMAGE / BEAT2", "2401.00374", "CVPR 2024",
       "커스텀 BVH 스켈레톤으로 파편화돼 있던 co-speech gesture 분야를 SMPL-X + FLAME이라는 공통 표현으로 끌어올렸다. "
       "데이터는 옵티컬 mocap 마커에 MoSh++를 피팅한 것이라, 영상 추정 pseudo-GT와는 노이즈 성격이 완전히 다르다."),
      ("MoMask", "2312.00063", "CVPR 2024",
       "텍스트→모션의 discrete-token 계열 대표. 다만 HumanML3D 263차원 표현을 그대로 써서 "
       "<b>손도 얼굴도 생성하지 않는다</b> — 이 갈래가 오래 안고 있던 제약을 보여주는 표본."),
      ("ViBES", "2512.14234", "CVPR 2026",
       "대화를 조건으로 음성·표정·몸·손을 함께 계획하는 speech-language-behavior 모델. "
       "학습 데이터 Converse3D의 주력은 유튜브 영상에 SPECTRE·4D-Humans·<b>HaMeR</b>를 돌려 만든 pseudo-GT다. "
       "즉 이 갈래가 추정 갈래에 직접 의존한다는 가장 선명한 증거.")],
     [("텍스트 → 모션 (몸통만)", [("HumanML3D", "", "CVPR 2022"), ("MDM", "2209.14916", "ICLR 2023"),
                          ("MoMask", "2312.00063", "CVPR 2024")]),
      ("텍스트 → 모션 (전신 전환)", [("Motion-X", "2307.00818", "NeurIPS 2023"), ("HumanTOMATO", "2310.12978", "ICML 2024")]),
      ("액션 → 모션", [("MultiAct", "2212.05897", "AAAI 2023")]),
      ("음성 → 제스처", [("BEAT", "2203.05297", "ECCV 2022"), ("EMAGE", "2401.00374", "CVPR 2024")]),
      ("대화 → 행동", [("ViBES", "2512.14234", "CVPR 2026")]),
      ("수어 생성", [("SIGNER", "2506.07460", "ECCV 2026")])]),

    ("int", "갈래 05", "상호작용 — 사람을 물체·사람·환경과 엮는다",
     "SMPL-X + 물체 · 사람 · 환경",
     "가장 비어 있는 갈래다. 다른 갈래들이 ‘사람 하나’를 잘 다루는 데 집중하는 동안, "
     "접촉·파지·물리를 함께 푸는 일은 아직 조각나 있다. ViBES가 스스로 밝힌 한계에도 "
     "“explicit physical interaction의 부재”가 들어간다. 연구실의 Hand-Object Interaction 관심이 정확히 이 자리에 붙는다.",
     [("HOPformer / EPIC-Contact", "2606.30598", "ECCV 2026",
       "야외 1인칭 영상에서 손과 물체의 자세를 함께 예측하고, 조밀한 3D 접촉 대응까지 주석한 데이터셋을 낸다. "
       "추정 갈래와 상호작용 갈래가 만나는 지점."),
      ("CONTHO", "2404.04819", "CVPR 2024",
       "인체와 물체를 접촉 정보로 서로 보정하며 동시에 복원한다. 사람만 잘 맞히는 것으로는 부족하다는 문제의식."),
      ("InterWild", "2303.13652", "CVPR 2023",
       "사람-물체가 아니라 손-손 상호작용. 실험실 데이터로 배운 모델이 야외에서 깨지는 문제를 "
       "입력을 공유 도메인으로 보내 푼다.")],
     [("손 - 물체", [("TOUCH", "2510.14874", "2025"), ("AGILE", "2602.04672", "2026"),
                 ("ForeHOI", "2602.06226", "2026"), ("HOPformer", "2606.30598", "ECCV 2026"),
                 ("DreamHand", "2608.20308", "프리프린트 2026")]),
      ("인체 - 물체", [("CONTHO", "2404.04819", "CVPR 2024"), ("GraspDiffusion", "2410.13911", "2024")]),
      ("손 - 손", [("InterHand2.6M", "2008.09309", "ECCV 2020"), ("InterWild", "2303.13652", "CVPR 2023"),
                ("Re:InterHand", "2310.17768", "NeurIPS 2023")]),
      ("로봇 응용", [("Ego2Robot", "2608.02580", "2026"), ("SiMDex", "2608.04196", "2026")])]),
]

CROSSINGS = [
    ("추정의 출력이 생성의 연료다",
     "ViBES의 1,000시간 데이터셋 Converse3D는 주력이 모션캡처가 아니라 유튜브 영상에 "
     "SPECTRE(얼굴) · 4D-Humans(몸) · HaMeR(손)를 돌려 만든 pseudo-GT다. "
     "생성 모델의 손 품질 상한이 추정기의 품질에 그대로 묶인다는 뜻이고, "
     "논문도 한계로 “monocular in-the-wild reconstruction의 bias와 artifact”를 명시한다."),
    ("그런데 두 갈래가 서로를 읽지 않는다",
     "ViBES 참고문헌에 SMPLer-X · OSX · Hand4Whole · WiLoR · Gyeongsik Moon은 한 건도 없다. "
     "전신 추정 쪽이 십수 년 쌓은 ‘손을 몸에 정합시키는 법’이 생성 쪽에 아직 전달되지 않았다. "
     "ViBES가 몸(4D-Humans)과 손(HaMeR)을 따로 추정해 합치는 방식은, "
     "Hand4Whole++가 “순진하게 붙이면 물리적으로 불가능한 손 배치가 나온다”고 지목한 바로 그 방식이다."),
    ("같은 SMPL-X에 도달하는 두 경로",
     "BEAT2는 옵티컬 mocap 마커에 MoSh++를 피팅했고, Converse3D는 단안 영상에서 회귀했다. "
     "최종 표현은 똑같이 SMPL-X지만 정확도·다양성 트레이드오프가 정반대이고 노이즈 성격도 다르다. "
     "데이터 갈래를 ‘무엇을 담았나’가 아니라 ‘어떻게 얻었나’로 갈라 봐야 하는 이유."),
    ("손은 언제나 늦게 합류한다",
     "추정 갈래에서 손이 전신에 제대로 붙기까지 Hand4Whole(2022)→Hand4Whole++(2026)가 걸렸고, "
     "생성 갈래에서는 HumanML3D의 22관절 몸통 표현이 2년간 표준이라 손·얼굴 생성 자체가 불가능했다. "
     "Motion-X(2023-07, 데이터)와 HumanTOMATO(2023-10, 모델)에서야 전신으로 넘어간다. "
     "두 갈래 모두 ‘몸 먼저, 손 나중’이라는 같은 순서를 반복했다."),
    ("상호작용 갈래가 가장 비어 있다",
     "아바타는 사람을 보이게 만들었고 생성은 움직이게 만들었지만, 그 사람이 물건을 집는 일은 여전히 따로 논다. "
     "ViBES가 “explicit physical interaction의 부재”를 한계로 적은 것이 상징적이다. "
     "추정 쪽에서 손-물체 접촉 주석(EPIC-Contact)이 나오기 시작한 지금이 두 갈래를 잇기 좋은 시점이다."),
]

LAB = [
    ("Hand-Object Interaction", "int",
     "갈래 05에 정면으로 붙는다. 추정 쪽 접촉 주석과 생성 쪽 행동 계획 사이가 끊겨 있어, "
     "둘을 잇는 작업이 그대로 빈칸이다."),
    ("Egocentric Vision", "est",
     "갈래 01의 하위 분기. 손은 크게 잡히고 몸은 거의 안 보이는 극단적 조건이라, "
     "‘고정된 전문가 + 어댑터’ 접근이 특히 잘 맞는다."),
    ("Spatial Audio", "gen",
     "지도에서 가장 명확한 공백. ViBES는 3D 몸을 가진 대화 에이전트인데 목소리가 공간화되지 않는다. "
     "몸의 위치·방향과 소리를 함께 다루는 자리가 비어 있다."),
]

CSS = """
*{box-sizing:border-box}
:root{
  --bg:#FAFAF9; --surface:#FFFFFF; --surface-2:#F5F5F3;
  --ink:#171717; --muted:#666A70; --faint:#9A9DA1; --line:#E8E7E3;
  --est:#176F78; --gen:#5B4B8A; --av:#1F6F4A; --int:#A9662E; --data:#8A6D1F;
  --shadow:0 1px 2px rgba(0,0,0,.025),0 8px 24px rgba(0,0,0,.035);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#131619; --surface:#1B1F23; --surface-2:#22272C;
  --ink:#ECEFF2; --muted:#A3ADB7; --faint:#6B7580; --line:#2B3138;
  --est:#3FB6C0; --gen:#A79AD8; --av:#5FBE8E; --int:#D8945A; --data:#D4BC63;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 6px 22px rgba(0,0,0,.35);
}}
body{background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans",system-ui,sans-serif;
  line-height:1.62;margin:0;-webkit-font-smoothing:antialiased}
.wrap{max-width:1020px;margin:0 auto;padding:60px 28px 110px}
a{color:var(--est)}
.mono{font-family:"IBM Plex Mono",monospace}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--faint)}
.home{font-family:"IBM Plex Mono",monospace;font-size:12px;text-decoration:none;color:var(--muted);
  display:inline-block;margin-bottom:22px;border:1px solid var(--line);border-radius:7px;padding:5px 11px}
.home:hover{color:var(--est);border-color:var(--est)}
header{border-bottom:1px solid var(--line);padding-bottom:34px}
h1{font-size:clamp(30px,5vw,44px);font-weight:650;letter-spacing:-.03em;margin:.55rem 0 .6rem;text-wrap:balance}
.sub{color:var(--muted);font-size:16px;line-height:1.68;max-width:78ch;margin:0}
.sub b{color:var(--ink);font-weight:600}
.meta-chips{margin-top:18px;display:flex;flex-wrap:wrap;gap:8px}
.chip{font-family:"IBM Plex Mono",monospace;font-size:11.5px;background:var(--surface-2);
  border:1px solid var(--line);border-radius:20px;padding:4px 11px;color:var(--muted)}
section{margin-top:64px}
.sec-head{display:block;margin-bottom:8px}
.sec-no{display:block;font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.13em;
  text-transform:uppercase;margin-bottom:5px}
h2{font-size:clamp(21px,3.3vw,26px);font-weight:620;letter-spacing:-.025em;margin:0}
.formula{font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--muted);
  background:var(--surface-2);border:1px solid var(--line);border-radius:7px;
  padding:5px 11px;display:inline-block;margin:10px 0 0}
.sec-tag{color:var(--muted);font-size:15px;line-height:1.65;margin:12px 0 22px;max-width:78ch}
.sec-tag b{color:var(--ink);font-weight:600}
.qa-lab{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint);margin:28px 0 10px}
/* map */
.map{display:flex;flex-direction:column;gap:9px;margin-top:18px}
.rel{display:grid;grid-template-columns:96px 1fr;gap:14px;align-items:center;
  background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--line);
  border-radius:10px;padding:13px 16px;box-shadow:var(--shadow)}
.rel .nm{font-family:"IBM Plex Mono",monospace;font-size:12.5px;font-weight:600}
.rel .eq{font-family:"IBM Plex Mono",monospace;font-size:13.5px}
.rel .eq .hub{font-weight:700;padding:1px 7px;border-radius:5px;background:var(--surface-2)}
.rel .eq .ar{color:var(--faint);padding:0 6px}
.rel .ds{display:block;font-family:"IBM Plex Sans",sans-serif;font-size:13px;color:var(--muted);margin-top:3px}
.rel.est{border-left-color:var(--est)} .rel.est .nm{color:var(--est)}
.rel.gen{border-left-color:var(--gen)} .rel.gen .nm{color:var(--gen)}
.rel.av{border-left-color:var(--av)} .rel.av .nm{color:var(--av)}
.rel.int{border-left-color:var(--int)} .rel.int .nm{color:var(--int)}
.rel.data{border-left-color:var(--data)} .rel.data .nm{color:var(--data)}
/* representative cards */
.card{background:var(--surface);border:1px solid var(--line);border-radius:11px;box-shadow:var(--shadow);
  padding:16px 19px;margin-top:13px;border-top:3px solid var(--line)}
.card h3{font-size:16.5px;font-weight:620;margin:2px 0 3px;line-height:1.3}
.card h3 a{color:var(--ink);text-decoration:none}
.card h3 a:hover{text-decoration:underline}
.card .cmeta{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--muted);margin-bottom:8px}
.card p{margin:0;font-size:14px}
.card p b{font-weight:600;color:var(--ink)}
/* sub-branch lists */
.subs{margin-top:22px;border-top:1px solid var(--line);padding-top:16px}
.sub-row{display:grid;grid-template-columns:186px 1fr;gap:14px;padding:9px 0;border-bottom:1px dashed var(--line)}
.sub-row:last-child{border-bottom:none}
.sub-row .sname{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--faint);
  letter-spacing:.04em;padding-top:3px}
.plist{display:flex;flex-wrap:wrap;gap:6px}
.p{font-size:12.5px;background:var(--surface-2);border:1px solid var(--line);border-radius:7px;
  padding:3px 9px;text-decoration:none;color:var(--ink);display:inline-flex;gap:6px;align-items:baseline}
a.p:hover{border-color:var(--est)}
.p .v{font-family:"IBM Plex Mono",monospace;font-size:10.5px;color:var(--faint)}
/* crossings */
.cross{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--gen);
  border-radius:0 10px 10px 0;padding:15px 18px;margin-top:13px}
.cross h4{font-size:15.5px;font-weight:620;margin:0 0 5px}
.cross p{margin:0;font-size:14px;color:var(--ink)}
.cross p b{font-weight:600}
.num{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--gen);margin-right:7px}
/* lab hooks */
.lab-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:13px;margin-top:16px}
.lab{background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:16px 18px;box-shadow:var(--shadow)}
.lab .tag{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase;
  color:#fff;border-radius:12px;padding:2px 9px;display:inline-block}
.lab.int .tag{background:var(--int)} .lab.est .tag{background:var(--est)} .lab.gen .tag{background:var(--gen)}
.lab h4{font-size:15.5px;font-weight:620;margin:10px 0 5px}
.lab p{margin:0;font-size:13.5px;color:var(--muted)}
footer{margin-top:72px;padding-top:22px;border-top:1px solid var(--line);
  font-size:12.5px;color:var(--faint);line-height:1.6}
@media(max-width:640px){.wrap{padding:40px 18px 76px}.rel,.sub-row{grid-template-columns:1fr;gap:5px}}
"""


def paper_chip(name, aid, venue):
    label = f'<span>{html.escape(name)}</span><span class="v">{html.escape(venue)}</span>'
    if aid:
        return f'<a class="p" href="https://arxiv.org/abs/{aid}" target="_blank" rel="noopener">{label}</a>'
    return f'<span class="p">{label}</span>'


secs = []
for bid, no, title, formula, desc, reps, subs in BRANCHES:
    rep_html = ""
    for nm, aid, venue, note in reps:
        t = html.escape(nm)
        if aid:
            t = f'<a href="https://arxiv.org/abs/{aid}" target="_blank" rel="noopener">{t}</a>'
        meta = f'arXiv {aid} · {venue}' if aid else venue
        rep_html += (f'<article class="card" style="border-top-color:var(--{bid})">'
                     f'<h3>{t}</h3><div class="cmeta">{html.escape(meta)}</div><p>{note}</p></article>')
    sub_html = ""
    for sname, plist in subs:
        chips = "".join(paper_chip(*p) for p in plist)
        sub_html += (f'<div class="sub-row"><div class="sname">{html.escape(sname)}</div>'
                     f'<div class="plist">{chips}</div></div>')
    secs.append(f"""
  <section id="{bid}">
    <div class="sec-head"><span class="sec-no" style="color:var(--{bid})">{html.escape(no)}</span>
      <h2>{html.escape(title)}</h2></div>
    <div class="formula">{html.escape(formula)}</div>
    <p class="sec-tag">{desc}</p>
    <div class="qa-lab">대표 논문</div>
    {rep_html}
    <div class="subs"><div class="qa-lab" style="margin-top:0">이 갈래의 논문들</div>{sub_html}</div>
  </section>""")

map_html = ""
for cid, nm, left, op, right, ds in RELATIONS:
    if cid == "data":
        eq = f'<span class="ar">{html.escape(left)}</span> <span class="hub">{html.escape(right)}</span>'
    elif right == "SMPL-X":
        eq = f'{html.escape(left)} <span class="ar">{op}</span> <span class="hub">SMPL-X</span>'
    else:
        eq = f'<span class="hub">SMPL-X</span> <span class="ar">{op}</span> {html.escape(right)}'
    map_html += (f'<div class="rel {cid}"><div class="nm">{html.escape(nm)}</div>'
                 f'<div class="eq">{eq}<span class="ds">{html.escape(ds)}</span></div></div>')

cross_html = "".join(
    f'<div class="cross"><h4><span class="num">{i:02d}</span>{html.escape(t)}</h4><p>{d}</p></div>'
    for i, (t, d) in enumerate(CROSSINGS, 1))

lab_html = "".join(
    f'<div class="lab {cid}"><span class="tag">{html.escape(nm)}</span><h4>갈래 연결</h4><p>{d}</p></div>'
    for nm, cid, d in LAB)

n_papers = sum(len(pl) for _, _, _, _, _, _, subs in BRANCHES for _, pl in subs)

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
    <div class="eyebrow">3D human ecosystem · landscape map</div>
    <h1>{html.escape(TITLE)}</h1>
    <p class="sub">{SUB}</p>
    <div class="meta-chips">
      <span class="chip">5개 갈래</span>
      <span class="chip">논문 {n_papers}편 수록</span>
      <span class="chip">허브 · SMPL-X (CVPR 2019)</span>
      <span class="chip">2026-09 기준</span>
    </div>
  </header>

  <div class="sec-head" style="margin-top:46px"><span class="sec-no" style="color:var(--faint)">The map</span>
    <h2>무엇이 갈래를 가르는가 — 화살표의 방향</h2></div>
  <p class="sec-tag">주제로 나누면 경계가 흐려진다. SMPL-X를 기준으로 <b>화살표가 어느 쪽을 향하는가</b>로 나누면
    다섯 갈래가 깔끔하게 떨어지고, 갈래끼리 어디서 맞물리는지도 같이 보인다.</p>
  <div class="map">{map_html}</div>
{''.join(secs)}

  <section>
    <div class="sec-head"><span class="sec-no" style="color:var(--gen)">Crossings</span>
      <h2>갈래는 어디서 만나고, 어디서 끊기는가</h2></div>
    <p class="sec-tag">지도의 값어치는 칸을 나누는 데 있지 않고 칸 사이의 선에 있다.
      지금 이 생태계에서 가장 중요한 다섯 개의 선.</p>
    {cross_html}
  </section>

  <section>
    <div class="sec-head"><span class="sec-no" style="color:var(--int)">Our hooks</span>
      <h2>연구실 관심은 지도의 어디에 붙는가</h2></div>
    <div class="lab-grid">{lab_html}</div>
  </section>

  <footer>자동 생성 · topics/smplx-landscape/build_survey.py ·
    갈래 01의 전신·손 통합 계보는 별도 서베이
    <a href="../hand-in-wholebody/hand-in-wholebody_survey.html">Hand-in-Whole-Body</a>,
    추정 쪽 연구자 계보는 <a href="../gyeongsik-moon/gyeongsik-moon_survey.html">Gyeongsik Moon 계보</a>에서 더 깊이 다룬다.
    학회·arXiv ID는 원문에서 확인한 것만 실었고, arXiv 판본이 확인되지 않은 항목(HumanML3D · HMR-Adapter · Codec Avatar Studio · Three Recipes)은 링크 없이 두었다.</footer>
</div>
</body>
</html>"""

open(OUT, "w", encoding="utf-8").write(doc)
print(f"WROTE {OUT}  ({len(BRANCHES)} branches, {n_papers} paper entries, {len(CROSSINGS)} crossings)")

# ── 논문 리스트를 마크다운으로도 내보낸다 ──────────────────────────
LIST_OUT = os.path.join(HERE, "paper_list.md")
lines = ["# SMPL-X 생태계 — 갈래별 논문 리스트", "",
         f"자동 생성 · 총 {n_papers}편 · 2026-09 기준. arXiv 판본이 확인되지 않은 항목은 ID를 비워 두었다.", ""]
seen = set()
for bid, no, title, formula, desc, reps, subs in BRANCHES:
    lines += [f"## {no} · {title}", "", f"`{formula}`", "",
              "| 하위 분기 | 논문 | 학회 | arXiv |", "|---|---|---|---|"]
    for sname, plist in subs:
        for nm, aid, venue in plist:
            link = f"[{aid}](https://arxiv.org/abs/{aid})" if aid else "—"
            lines.append(f"| {sname} | {nm} | {venue} | {link} |")
            if aid:
                seen.add((aid, nm, venue))
    lines.append("")
lines += ["## 전체 (arXiv ID 기준 중복 제거)", "",
          "| arXiv | 논문 | 학회 |", "|---|---|---|"]
for aid, nm, venue in sorted(seen):
    lines.append(f"| [{aid}](https://arxiv.org/abs/{aid}) | {nm} | {venue} |")
lines.append("")
open(LIST_OUT, "w", encoding="utf-8").write("\n".join(lines))
print(f"WROTE {LIST_OUT}  ({len(seen)} unique arXiv entries)")

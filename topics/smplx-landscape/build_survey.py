#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the SMPL-X ecosystem landscape map survey (nested taxonomy with divergence axes)."""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "smplx-landscape_survey.html")
LIST_OUT = os.path.join(HERE, "paper_list.md")

TITLE = "SMPL-X 생태계 지도 — 어디서 갈라지는가"
SUB = ("3D 인체 연구는 SMPL-X라는 공통 표현을 허브로 삼아 갈라진다. "
       "갈래를 가르는 것은 주제가 아니라 <b>SMPL-X를 향한 화살표의 방향</b>이고, "
       "각 갈래 안에서 다시 갈라지는 데는 저마다 하나의 <b>축(axis)</b>이 있다. "
       "그리고 지도 바깥에는 몸을 명시적으로 표현하지 않는 <b>두 번째 허브 — world model</b>이 있어, "
       "1인칭에서 두 허브가 만난다. 이 지도는 칸보다 그 축과 다리를 기록하려고 만들었다.")

RELATIONS = [
    ("est", "Estimation", "이미지 · 영상", "→", "SMPL-X", "세상에서 파라미터를 읽어낸다"),
    ("gen", "Generation", "텍스트 · 음성 · 대화", "→", "SMPL-X", "없는 모션을 만들어낸다"),
    ("av", "Avatar", "SMPL-X", "→", "픽셀 · 보이는 사람", "파라미터를 사람으로 렌더한다"),
    ("int", "Interaction (in)", "세상", "→", "SMPL-X + 물체 · 사람", "세상을 보고 사람과 물체를 함께 복원한다"),
    ("sim", "Simulation (out)", "SMPL-X · MANO", "⇒", "세계의 반응 (비디오)", "몸을 행위자로 삼아 세상의 변화를 만든다 — 두 번째 허브로 가는 다리"),
    ("data", "Data", "⊥", "", "위 모든 갈래", "다섯 갈래 전부의 상한을 정한다"),
]

# 노드: dict(name, why, papers=[(약칭, arxiv, venue)], subs=[node...])
def N(name, why, papers=None, subs=None):
    return {"name": name, "why": why, "papers": papers or [], "subs": subs or []}

BRANCHES = [
    dict(id="est", no="Branch 01", title="Estimation — reading SMPL-X out of images and video",
         formula="images · video → SMPL-X",
         axis="이 갈래를 가르는 축은 <b>‘무엇을 보고, 무엇을 뽑는가’</b>다. 추정 대상의 범위(전신인가 손인가), "
              "출력을 어떤 형태로 낼 것인가, 한 장인가 영상인가, 3인칭인가 1인칭인가, 한 사람인가 여럿인가. "
              "축마다 이유가 다르고, 그 이유는 대부분 <b>학습 데이터가 어디서 끊겨 있는가</b>로 귀결된다.",
         desc="이 저장소가 가장 깊이 판 갈래. 출력이 다른 갈래들의 원료가 되므로 여기의 정확도가 생태계 전체의 바닥이다.",
         reps=[("Hand4Whole++ (CHAM)", "2603.14726", "CVPR 2026",
                "전신 추정기와 손 전용 추정기를 모두 얼린 채 경량 어댑터로 잇는다. ‘전신’과 ‘손’이 서로 다른 데이터로 학습돼 "
                "갈라져 있다는 사실 자체를 문제로 삼은 논문."),
               ("SMPLer-X", "2309.17448", "NeurIPS 2023 D&B",
                "450만 인스턴스로 스케일업한 전신 파운데이션 모델. 아키텍처가 아니라 데이터·규모로 통합을 밀어붙인 쪽 대표."),
               ("HaMeR", "2312.05251", "CVPR 2024",
                "손만 보는 전용 전문가. 정밀하지만 몸 맥락이 없다. 생성 갈래가 학습 데이터를 만들 때 실제로 가져다 쓰는 부품이라, "
                "이 갈래 밖으로 가장 멀리 퍼진 논문이기도 하다.")],
         subs=[
            N("By body scope — whole-body vs hand-only",
              "전신 데이터에는 손 다양성이 부족하고, 손 데이터에는 몸 맥락이 없다. 학습 데이터가 갈려 있으니 모델도 갈린다 — "
              "Hand4Whole++가 ‘supervision gap’이라 부른 그 분기.",
              subs=[
                N("Whole-body · by integration strategy",
                  "‘손 정확도’와 ‘몸과의 일관성’ 사이 트레이드오프를 <b>어디서</b> 해결하느냐로 다시 갈린다. "
                  "따로 뽑아 붙일 것인가, 특징 수준에서 섞을 것인가, 처음부터 한 네트워크로 갈 것인가, 데이터로 밀 것인가, 얼린 채 어댑터로 이을 것인가.",
                  subs=[
                    N("Separate-then-attach", "손 전문가의 정확도를 살리되 손목에서 어긋난다.",
                      [("FrankMocap", "2108.06428", "ICCVW 2021")]),
                    N("Feature-level fusion", "손목 회전에 손 쪽 특징을 써서 연결부를 정교화.",
                      [("Hand4Whole", "2011.11534", "CVPRW 2022"), ("PyMAF-X", "2207.06400", "TPAMI 2023")]),
                    N("One-stage joint", "손을 다시 크롭하지 않고 공유 특징맵에서 한 번에.",
                      [("OSX", "2303.16160", "CVPR 2023"), ("AiOS", "2403.17934", "CVPR 2024")]),
                    N("Scale-up", "아키텍처 대신 데이터·모델 크기로.",
                      [("SMPLer-X", "2309.17448", "NeurIPS 2023")]),
                    N("Frozen backbone + adapter", "잘 되는 것은 재학습하지 않고 얇은 다리만 놓는다.",
                      [("HMR-Adapter", "", "ACM MM 2024"), ("Hand4Whole++", "2603.14726", "CVPR 2026")]),
                  ]),
                N("Hand-only · by failure mode",
                  "손 하나는 잘 잡히니, 남은 문제는 ‘언제 깨지는가’다 — 가려질 때, 야외일 때, 두 손이 얽힐 때.",
                  subs=[
                    N("Occlusion-robust", "물체·다른 손에 가려진 손.", [("HandOccNet", "2203.14564", "CVPR 2022")]),
                    N("In-the-wild", "검출부터 복원까지 야외 다중 손.", [("HaMeR", "2312.05251", "CVPR 2024"), ("WiLoR", "2409.12259", "CVPR 2025")]),
                    N("Interacting hands", "두 손이 얽히면 자기 가림 + 크기 분포 불일치.", [("InterWild", "2303.13652", "CVPR 2023")]),
                  ]),
              ]),
            N("By output representation — regression vs spatial",
              "좌표·파라미터를 직접 회귀하면 공간 정보를 잃고 매핑이 비선형이 된다. 그래서 voxel·lixel·heatmap 같은 공간 표현으로 갈아탄다.",
              [("V2V-PoseNet", "1711.07399", "CVPR 2018"), ("I2L-MeshNet", "2008.03713", "ECCV 2020"), ("Pose2Mesh", "2008.09047", "ECCV 2020")]),
            N("By temporal scope — single image vs video",
              "프레임별 추정은 구조적으로 jitter를 피할 수 없다. 시간축을 넣어야 손이 떨리지 않는다.",
              [("TCMR", "2011.08627", "CVPR 2021"), ("DanceHMR", "2605.18102", "프리프린트 2026")]),
            N("By viewpoint — exocentric vs egocentric",
              "1인칭은 어안 왜곡, 몸이 거의 안 보임, SMPL-X 정답 없음. 3인칭 해법을 그대로 옮길 수 없어 갈린다.",
              [("Egocentric WB-HMR", "2605.08606", "ICIP 2026"), ("EgoForce", "2605.12498", "SIGGRAPH 2026")]),
            N("By scene — single vs multi-person",
              "root-relative 포즈만으로는 여러 사람을 한 공간에 놓을 수 없다. 카메라까지의 절대 거리가 따로 필요해진다.",
              [("RootNet", "1907.11346", "ICCV 2019"), ("3DCrowdNet", "2104.07300", "CVPR 2022")]),
         ]),

    dict(id="data", no="Branch 02", title="Data & annotation — the floor under every other branch",
         formula="⊥ all branches",
         axis="이 갈래의 축은 하나뿐이다: <b>‘어떻게 얻었는가’</b>. 같은 SMPL-X 파라미터라도 마커를 피팅했는지, 영상에서 회귀했는지, "
              "합성했는지에 따라 노이즈의 성격이 완전히 다르다. 무엇을 담았는지로 나누면 이 차이가 보이지 않는다.",
         desc="다른 네 갈래의 성능 상한을 여기서 정한다.",
         reps=[("Re:InterHand", "2310.17768", "NeurIPS 2023 D&B",
                "자기 전작 InterHand2.6M을 ‘랩 데이터셋’의 대표로 세워두고 “images have monotonous appearances”라고 못 박은 뒤 "
                "릴라이팅으로 다시 만든다. 정확도와 다양성을 동시에 얻으려는 제3의 경로."),
               ("NeuralAnnot", "2011.11232", "CVPRW 2022",
                "야외 이미지에 3D 정답이 없다는 병목을 신경망 주석기로 메운다. ‘추정 결과를 정답처럼 쓴다’는 습관이 여기서 제도화된다."),
               ("Human4K", "2607.13646", "프리프린트 2026",
                "8시점 4K · 600만 장 · Vicon 정밀 SMPL-X. Hand4Whole++가 어댑터로 우회한 격차를 데이터 쪽에서 정면으로 푸는 최신 시도.")],
         subs=[
            N("Studio motion capture — markers → MoSh++ → SMPL-X",
              "정확하다. 대신 실내·슈트·소수 화자라는 도메인에 갇혀 외형 다양성이 빈약하다.",
              [("InterHand2.6M", "2008.09309", "ECCV 2020"), ("BEAT", "2203.05297", "ECCV 2022"),
               ("BEAT2 (EMAGE)", "2401.00374", "CVPR 2024"), ("Human4K", "2607.13646", "프리프린트 2026"),
               ("Codec Avatar Studio", "", "NeurIPS 2024 D&B")]),
            N("Video pseudo-GT — estimator → parameters",
              "넓고 싸다. 대신 품질 상한이 <b>추정 갈래의 추정기</b>에 묶인다. 이 경로가 생성 갈래의 주식이 되면서 두 갈래가 의존 관계로 엮인다.",
              [("NeuralAnnot", "2011.11232", "CVPRW 2022"), ("Three Recipes", "", "CVPRW 2023"),
               ("SHOW (TalkSHOW)", "2212.04420", "CVPR 2023"), ("Converse3D (ViBES)", "2512.14234", "CVPR 2026")]),
            N("Synthesis & relighting",
              "위 둘의 절충. 정확한 정답은 스튜디오에서, 외형 다양성은 렌더링으로.",
              [("Re:InterHand", "2310.17768", "NeurIPS 2023")]),
            N("Language-labelled motion — body-only → whole-body",
              "텍스트 라벨이 ‘걷는다·점프한다’ 수준이라 손 라벨이 애초에 없었다. 이 데이터의 22관절 표현이 생성 갈래의 손 부재를 2년간 고착시켰고, "
              "Motion-X가 전신 주석을 넣으면서 풀린다.",
              [("HumanML3D", "", "CVPR 2022"), ("Motion-X", "2307.00818", "NeurIPS 2023 D&B")]),
         ]),

    dict(id="av", no="Branch 03", title="Avatar & rendering — turning parameters into a visible person",
         formula="SMPL-X → pixels",
         axis="두 개의 축이 겹친다. <b>‘무엇으로 표면을 표현하는가’</b>(파라메트릭 메시인가, 신경 렌더링인가, 조명까지 분리하는가)와 "
              "<b>‘개인화에 얼마가 드는가’</b>(스튜디오인가, 폰 스캔인가, 사진 한 장인가). 후자가 최근 이 갈래를 연구실 밖으로 끌어냈다.",
         desc="추정과 생성이 만든 파라미터를 사람으로 만드는 갈래.",
         reps=[("ExAvatar", "2407.21686", "ECCV 2024",
                "SMPL-X 메시와 3D Gaussian Splatting을 결합해 표정·손까지 되는 전신 아바타. ‘파라미터 → 사람’ 변환의 현재 대표형이고, "
                "생성 갈래가 비워둔 자리를 정확히 채운다."),
               ("UHM", "2405.07933", "CVPR 2024",
                "수십 대 카메라 스튜디오가 아니라 폰 스캔만으로 개인화한다. 아바타를 연구실 밖으로 꺼낸 전환점."),
               ("URHand", "2401.05334", "CVPR 2024",
                "시점·포즈·조명·ID에 걸쳐 일반화되는 릴라이터블 손 모델.")],
         subs=[
            N("By surface representation",
              "제어 가능성과 사실감이 반대로 간다. 메시는 다루기 쉽지만 사실감에 한계가 있고, 신경 렌더링은 사실적이지만 표정·손 제어가 어려워 결국 메시와 결합한다.",
              subs=[
                N("Parametric mesh", "저차원 파라미터로 뼈대+표면.", [("SMPL-X", "1904.05866", "CVPR 2019"), ("DeepHandMesh", "2008.08213", "ECCV 2020"), ("UHM", "2405.07933", "CVPR 2024")]),
                N("Neural rendering · 3D Gaussians", "사실감을 위해 메시 밖으로 — 대신 메시를 뼈대로 다시 붙인다.", [("MonoNHR", "2210.00627", "3DV 2022"), ("ExAvatar", "2407.21686", "ECCV 2024"), ("PERSONA", "2508.09973", "ICCV 2025"), ("DynaAvatar", "2603.14772", "CVPR 2026")]),
                N("Relightable", "조명이 바뀌면 외형이 깨지니 조명을 분리.", [("URHand", "2401.05334", "CVPR 2024")]),
              ]),
            N("By capture cost — studio → phone → single image",
              "스튜디오 자산을 전제하면 일상에서 못 쓴다. 입력을 싸게 만들수록 사전(prior)에 더 기대게 된다.",
              [("Codec Avatar Studio", "", "NeurIPS 2024"), ("UHM", "2405.07933", "CVPR 2024"), ("PERSONA", "2508.09973", "ICCV 2025"), ("DynaAvatar", "2603.14772", "CVPR 2026")]),
         ]),

    dict(id="gen", no="Branch 04", title="Generation — producing SMPL-X from a condition",
         formula="text · speech · dialogue → SMPL-X",
         axis="이 갈래의 첫 축은 <b>‘무엇을 조건으로 주는가’</b>다. 그런데 조건마다 <b>데이터가 어디서 왔는지가 달라서</b>, "
              "같은 조건 안에서 두 번째 축이 열린다 — 몸통만인가 전신인가, mocap인가 pseudo-GT인가. "
              "이 갈래에서 손이 늦게 합류한 이유는 전부 그 두 번째 축에 있다.",
         desc="추정과 화살표가 정반대인 갈래.",
         reps=[("EMAGE / BEAT2", "2401.00374", "CVPR 2024",
                "파편화된 co-speech gesture 분야를 SMPL-X + FLAME이라는 공통 표현으로 끌어올렸다. 데이터는 mocap 마커에 MoSh++를 피팅한 것."),
               ("MoMask", "2312.00063", "CVPR 2024",
                "텍스트→모션의 discrete-token 계열 대표. HumanML3D 263차원을 그대로 써서 <b>손도 얼굴도 생성하지 않는다</b>."),
               ("ViBES", "2512.14234", "CVPR 2026",
                "대화를 조건으로 음성·표정·몸·손을 함께 계획한다. 학습 데이터의 주력은 유튜브 영상에 4D-Humans·<b>HaMeR</b>를 돌린 pseudo-GT — "
                "생성이 추정에 직접 의존한다는 가장 선명한 증거.")],
         subs=[
            N("Text → motion",
              "텍스트 라벨이 몸통 수준이라 데이터(HumanML3D)가 22관절로 배포됐고, 그 표현이 벤치마크·평가기까지 세트로 굳었다. "
              "그래서 <b>출력 범위</b>로 갈린다 — 2023년 하반기 Motion-X(데이터)·HumanTOMATO(모델)에서야 전신으로 넘어간다.",
              subs=[
                N("Body-only (HumanML3D 22 joints)", "2022–2023 SOTA 라인 전체가 구조적으로 손·얼굴을 낼 수 없었다.",
                  [("HumanML3D", "", "CVPR 2022"), ("MDM", "2209.14916", "ICLR 2023"), ("MoMask", "2312.00063", "CVPR 2024")]),
                N("Whole-body (SMPL-X)", "전신 주석 데이터가 생기자 손·얼굴을 함께 생성하는 모델이 따라온다.",
                  [("Motion-X", "2307.00818", "NeurIPS 2023"), ("HumanTOMATO", "2310.12978", "ICML 2024")]),
              ]),
            N("Action label → motion",
              "텍스트보다 이산적이고, 여러 라벨을 이어 붙여 장기 시퀀스를 만드는 문제로 갈린다.",
              [("MultiAct", "2212.05897", "AAAI 2023")]),
            N("Speech → gesture (co-speech)",
              "립싱크와 손짓이 과제의 본질이라 <b>전신에 먼저 도달</b>했다. 대신 여기서는 데이터 획득 경로로 갈린다 — mocap이냐 영상 추정이냐.",
              subs=[
                N("Mocap-based", "정확하지만 스튜디오·화자 제한.", [("BEAT", "2203.05297", "ECCV 2022"), ("EMAGE / BEAT2", "2401.00374", "CVPR 2024")]),
                N("Video pseudo-GT-based", "야외 다양성 대신 추정기 품질에 묶임.", [("SHOW (TalkSHOW)", "2212.04420", "CVPR 2023")]),
                N("Real-time holistic", "지연 제약이 별도 축을 연다.", [("DiffSHEG", "2401.04747", "2024")]),
              ]),
            N("Dialogue → behaviour (agentic)",
              "‘무엇을 움직일지’만이 아니라 <b>‘언제, 왜 움직일지’</b>까지 결정한다. 번역이 아니라 에이전트가 되면서 조건이 대화 이력 전체로 넓어진다.",
              [("ViBES", "2512.14234", "CVPR 2026"), ("Motion-Omni", "2609.04250", "프리프린트 2026")]),
            N("Sign language",
              "손이 곧 의미를 실으므로 손 정밀도가 곧 정확도다. 다른 생성 과제와 달리 손을 뒤로 미룰 수 없다.",
              [("SIGNER", "2506.07460", "ECCV 2026")]),
         ]),

    dict(id="int", no="Branch 05", title="Interaction (inbound) — reconstructing the body together with objects, people, and scenes",
         formula="world → SMPL-X + objects · people",
         axis="축은 <b>‘무엇과 엮는가’</b>다. 상대가 물체인지 다른 손인지 다른 사람인지에 따라 제약의 종류가 달라진다 — "
              "가림의 원인이 다르고, 접촉 제약이 다르다. 화살표는 <b>들어오는</b> 방향이다: 세상을 보고 사람과 상대를 함께 복원한다. "
              "몸이 세상을 <b>바꾸는</b> 나가는 방향은 Branch 06으로 분리했다.",
         desc="한때 가장 비어 있던 갈래. ViBES가 스스로 밝힌 한계에 “explicit physical interaction의 부재”가 들어간다.",
         reps=[("HOPformer / EPIC-Contact", "2606.30598", "ECCV 2026",
                "야외 1인칭 영상에서 손·물체 자세를 함께 예측하고 조밀한 3D 접촉 대응을 주석. 추정과 상호작용이 만나는 지점."),
               ("CONTHO", "2404.04819", "CVPR 2024",
                "인체와 물체를 접촉 정보로 서로 보정하며 동시에 복원. 사람만 잘 맞히는 것으로는 부족하다는 문제의식."),
               ("InterWild", "2303.13652", "CVPR 2023",
                "손-손 상호작용. 실험실 모델이 야외에서 깨지는 문제를 입력을 공유 도메인으로 보내 푼다.")],
         subs=[
            N("Hand – object",
              "물체가 손을 가리고, 접촉이 손 자세를 제약한다. 손 단독 추정과 다른 문제가 된다.",
              [("TOUCH", "2510.14874", "2025"), ("AGILE", "2602.04672", "2026"), ("ForeHOI", "2602.06226", "2026"),
               ("HOPformer", "2606.30598", "ECCV 2026"), ("DreamHand", "2608.20308", "프리프린트 2026")]),
            N("Human – object (whole-body)",
              "전신 자세와 물체 배치가 서로를 제약한다. 손만이 아니라 몸 전체가 접촉에 참여.",
              [("CONTHO", "2404.04819", "CVPR 2024"), ("GraspDiffusion", "2410.13911", "2024")]),
            N("Hand – hand",
              "자기 가림에 더해, 한 손 데이터와 두 손 데이터의 크기 분포가 어긋난다.",
              [("InterHand2.6M", "2008.09309", "ECCV 2020"), ("InterWild", "2303.13652", "CVPR 2023"), ("Re:InterHand", "2310.17768", "NeurIPS 2023")]),
         ]),

    dict(id="sim", no="Branch 06", title="Embodied simulation (outbound) — the body as actuator, the world as output",
         formula="SMPL-X · MANO (action) ⇒ world response (video)",
         axis="이 갈래는 지도의 전제를 절반만 공유한다. 몸은 여전히 명시적으로 표현하지만, <b>세상은 암묵적으로</b>(비디오 잠재 공간) 표현한다 — "
              "즉 SMPL-X 허브에서 world model 허브로 건너가는 다리다. 그래서 첫 축은 <b>‘행동을 무엇으로 넣는가’</b>가 된다: "
              "손 메시를 렌더해 픽셀에 정렬할 것인가, 포즈 파라미터를 토큰으로 줄 것인가, 2D 마스크로 뭉갤 것인가. "
              "2026년 들어 두 번째 축이 열렸는데, <b>손의 움직임과 카메라(머리)의 움직임을 어떻게 분리하는가</b>다 — 1인칭에서는 둘이 같은 픽셀 흐름에 섞여 들어오기 때문이다.",
         desc="사람 메시의 네 번째 역할. 복원되는 대상도, 만들어지는 대상도, 렌더되는 대상도 아니라 <b>세상을 움직이는 제어 신호</b>다. "
              "현재 이 갈래의 출력은 전부 비디오이고, 3D를 직접 내는 논문은 아직 없다.",
         reps=[("DWM — Dexterous World Models", "2512.17907", "프리프린트 2025-12 (SNU)",
                "정적 3D 장면 렌더링 + 1인칭 손 메시 렌더링을 조건으로, 손이 움직이면 세상이 어떻게 변하는지를 비디오 확산으로 생성한다. "
                "배경 합성과 행동이 유발하는 역학을 분리했다는 게 고유성이고, 후보 행동의 결과를 미리 시뮬레이션해 고르는 데 쓴다. "
                "손은 출력이 아니라 <b>입력</b>이다."),
               ("PlayerOne", "2506.09995", "프리프린트 2025",
                "3인칭 카메라로 찍은 사용자의 실제 동작을 <b>SMPLest-X로 추정한 SMPL-X 파라미터</b>로 바꿔 1인칭 비디오를 생성한다. "
                "추정 갈래의 도구가 시뮬레이션 갈래의 행동 표현이 되는, 지도와 가장 직접 이어지는 형제."),
               ("PEVA", "2506.21552", "프리프린트 2025",
                "전신 3D 포즈 궤적을 행동으로 삼아 미래 1인칭 프레임을 예측한다. 손이 아니라 <b>전신</b>을 행동 공간으로 잡은 쪽 대표 — "
                "‘몸이 곧 행동’이라는 발상의 원형.")],
         subs=[
            N("By action representation — explicit geometry vs implicit 2D",
              "행동을 픽셀에 정렬된 기하로 줄수록 물체 역학이 정확해지고, 벡터로 줄수록 유연하지만 정렬이 약해진다. "
              "2D 마스크만 주면 손은 맞춰도 물체가 안 움직인다(DWM이 InterDyn을 그렇게 평가한다).",
              subs=[
                N("Rendered hand mesh (pixel-aligned)", "메시를 렌더해 넣으면 기하와 움직임이 픽셀 단위로 정렬된다.",
                  [("DWM", "2512.17907", "프리프린트 2025"), ("Hand2World", "2602.09600", "프리프린트 2026"), ("HandsOnWorld", "2607.02075", "프리프린트 2026")]),
                N("Pose parameter / joint vector", "SMPL-X 파라미터나 관절 좌표를 토큰으로 주입 — 표현이 가볍고 부위별 분리가 쉽다.",
                  [("PlayerOne", "2506.09995", "프리프린트 2025"), ("PEVA", "2506.21552", "프리프린트 2025"),
                   ("Generated Reality", "2602.18422", "프리프린트 2026"), ("EgoExo-WM", "2605.15477", "프리프린트 2026")]),
                N("2D mask (implicit)", "구동체의 실루엣만 주는 가장 약한 조건. 대형 비디오 모델을 암묵적 물리 시뮬레이터로 쓰는 발상의 출발점.",
                  [("InterDyn", "2412.11785", "CVPR 2025")]),
              ]),
            N("By camera–hand disentanglement",
              "1인칭에서는 머리가 돌아가도, 손이 움직여도 같은 픽셀 흐름이 생긴다. 이걸 분리하지 못하면 모델이 둘을 혼동한다 — "
              "2026년 작업들이 Plücker ray 같은 world-frame 표현으로 카메라를 따로 떼어낸 이유.",
              [("Hand2World", "2602.09600", "프리프린트 2026"), ("HandsOnWorld", "2607.02075", "프리프린트 2026"), ("Generated Reality", "2602.18422", "프리프린트 2026")]),
            N("By viewpoint — egocentric vs fixed third-person",
              "이 갈래는 거의 전부 1인칭이다. 손이 관측되는 몸이자 행동 그 자체인 시점이라 자연스럽다. 고정 3인칭은 InterDyn 하나.",
              [("InterDyn", "2412.11785", "CVPR 2025")]),
            N("Body → robot action (embodiment transfer)",
              "세상이 아니라 <b>로봇</b>이 출력이 되는 변형. 사람 손 메시를 로봇 관절 명령이나 로봇 손 이미지로 옮긴다 — 사람 손과 로봇 손의 형상이 달라 그대로는 못 쓴다.",
              [("HandEdit", "2608.12122", "프리프린트 2026"), ("Ego2Robot", "2608.02580", "2026"), ("SiMDex", "2608.04196", "2026")]),
         ]),
]

CROSSINGS = [
    ("추정의 출력이 생성의 연료다",
     "ViBES의 Converse3D는 유튜브 영상에 SPECTRE(얼굴) · 4D-Humans(몸) · HaMeR(손)를 돌려 만든 pseudo-GT다. "
     "생성 모델의 손 품질 상한이 추정기 품질에 묶이고, 논문도 “monocular in-the-wild reconstruction의 bias와 artifact”를 한계로 명시한다."),
    ("그런데 두 갈래가 서로를 읽지 않는다",
     "ViBES 참고문헌에 SMPLer-X · OSX · Hand4Whole · WiLoR · Gyeongsik Moon은 한 건도 없다. "
     "몸(4D-Humans)과 손(HaMeR)을 따로 추정해 합치는 방식은 Hand4Whole++가 “순진하게 붙이면 물리적으로 불가능한 손 배치가 나온다”고 지목한 바로 그 방식이다."),
    ("같은 SMPL-X에 도달하는 두 경로",
     "BEAT2는 mocap 마커에 MoSh++를 피팅했고, SHOW·Converse3D는 단안 영상에서 회귀했다. 최종 표현은 같지만 노이즈 성격과 다양성 트레이드오프가 정반대다. "
     "데이터 갈래를 ‘무엇을 담았나’가 아니라 ‘어떻게 얻었나’로 갈라야 하는 이유."),
    ("손은 언제나 늦게 합류한다",
     "추정에서는 Hand4Whole(2022)→Hand4Whole++(2026), 생성에서는 HumanML3D 22관절이 2년간 표준이라 손·얼굴 생성이 불가능했고 "
     "Motion-X(2023-07)·HumanTOMATO(2023-10)에서야 전신이 된다. 두 갈래 모두 ‘몸 먼저, 손 나중’이라는 같은 순서를 반복했다. "
     "예외는 손이 의미 자체인 과제(수어, co-speech)뿐이다."),
    ("상호작용은 비어 있다가, 반대 방향에서 채워지고 있다",
     "아바타는 사람을 보이게, 생성은 움직이게 만들었지만 그 사람이 물건을 집는 일은 여전히 따로 놀았다. "
     "그런데 채워지는 방향이 예상과 달랐다 — 세상을 보고 접촉을 복원하는 쪽(Branch 05)보다, "
     "몸으로 세상을 움직여 보는 쪽(Branch 06)이 2025~26년에 먼저 붐볐다."),
    ("두 허브 사이의 다리 — 명시적 메시 ↔ 암묵적 world model",
     "지도 바깥에는 몸을 메시로 표현하지 않는 두 번째 허브(비디오 world model)가 있고, 1인칭에서 둘이 만난다. "
     "다리는 양방향이다. <b>A→B</b>: DWM·PlayerOne이 손·몸 메시를 행동 조건으로 삼아 세상을 시뮬레이션하고, PlayerOne은 그 메시를 "
     "SMPLest-X — 추정 갈래의 도구 — 로 만든다(ViBES가 HaMeR에 기댄 것과 같은 의존 패턴). "
     "<b>B→A</b>: DreamHand는 비디오 확산 모델의 사전을 거꾸로 가려진 손 메시 복원에 쓴다. "
     "메시 연구의 역할이 ‘정확히 복원하는 최종 목표’에서 ‘world model이 소비하는 구조화된 행동 공간’으로 옮겨가는 중이며, "
     "그 메시가 계속 필요한지 아니면 암묵적 모델이 대체하는지가 지금 살아 있는 논쟁이다."),
]

LAB = [
    ("Hand-Object Interaction", "int", "Branch 05(들어오는)와 Branch 06(나가는) 사이에 걸친다. 접촉을 복원하는 쪽과 손으로 세상을 움직이는 쪽이 아직 서로를 안 읽어, 둘을 잇는 작업이 빈칸이다."),
    ("Egocentric Vision", "sim", "Branch 01의 viewpoint 축이자 Branch 06의 본거지. 1인칭에서는 손이 관측되는 몸이면서 행동 그 자체라, 명시적 메시와 암묵적 world model 두 허브가 여기서만 충돌한다."),
    ("Spatial Audio", "gen", "지도에서 가장 명확한 공백. ViBES·Motion-Omni는 3D 몸을 가진 대화 에이전트인데 목소리가 공간화되지 않는다. 몸의 위치·방향과 소리를 함께 다루는 자리가 비어 있다."),
]

CSS = """
*{box-sizing:border-box}
:root{--bg:#FAFAF9;--surface:#FFFFFF;--surface-2:#F5F5F3;--ink:#171717;--muted:#666A70;--faint:#9A9DA1;--line:#E8E7E3;
  --est:#176F78;--gen:#5B4B8A;--av:#1F6F4A;--int:#A9662E;--sim:#A3364A;--data:#8A6D1F;
  --shadow:0 1px 2px rgba(0,0,0,.025),0 8px 24px rgba(0,0,0,.035)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#131619;--surface:#1B1F23;--surface-2:#22272C;
  --ink:#ECEFF2;--muted:#A3ADB7;--faint:#6B7580;--line:#2B3138;
  --est:#3FB6C0;--gen:#A79AD8;--av:#5FBE8E;--int:#D8945A;--sim:#E07A8A;--data:#D4BC63;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 6px 22px rgba(0,0,0,.35)}}
body{background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans",system-ui,sans-serif;line-height:1.62;margin:0;-webkit-font-smoothing:antialiased}
.wrap{max-width:1040px;margin:0 auto;padding:60px 28px 110px}
a{color:var(--est)}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--faint)}
.home{font-family:"IBM Plex Mono",monospace;font-size:12px;text-decoration:none;color:var(--muted);display:inline-block;margin-bottom:22px;border:1px solid var(--line);border-radius:7px;padding:5px 11px}
.home:hover{color:var(--est);border-color:var(--est)}
header{border-bottom:1px solid var(--line);padding-bottom:34px}
h1{font-size:clamp(30px,5vw,44px);font-weight:650;letter-spacing:-.03em;margin:.55rem 0 .6rem;text-wrap:balance}
.sub{color:var(--muted);font-size:16px;line-height:1.68;max-width:78ch;margin:0}
.sub b,.sec-tag b,.axis b,.why b{color:var(--ink);font-weight:600}
.meta-chips{margin-top:18px;display:flex;flex-wrap:wrap;gap:8px}
.chip{font-family:"IBM Plex Mono",monospace;font-size:11.5px;background:var(--surface-2);border:1px solid var(--line);border-radius:20px;padding:4px 11px;color:var(--muted)}
section{margin-top:66px}
.sec-head{display:block;margin-bottom:8px}
.sec-no{display:block;font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.13em;text-transform:uppercase;margin-bottom:5px}
h2{font-size:clamp(21px,3.3vw,26px);font-weight:620;letter-spacing:-.025em;margin:0}
.formula{font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--muted);background:var(--surface-2);border:1px solid var(--line);border-radius:7px;padding:5px 11px;display:inline-block;margin:10px 0 0}
.sec-tag{color:var(--muted);font-size:15px;line-height:1.65;margin:12px 0 0;max-width:78ch}
.axis{margin:16px 0 0;padding:13px 16px;border-left:3px solid var(--line);background:var(--surface);border-radius:0 9px 9px 0;font-size:14.5px;line-height:1.65;max-width:80ch}
.axis .lab{font-family:"IBM Plex Mono",monospace;font-size:9.8px;letter-spacing:.12em;text-transform:uppercase;display:block;margin-bottom:4px}
.qa-lab{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);margin:28px 0 10px}
.map{display:flex;flex-direction:column;gap:9px;margin-top:18px}
.rel{display:grid;grid-template-columns:110px 1fr;gap:14px;align-items:center;background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--line);border-radius:10px;padding:13px 16px;box-shadow:var(--shadow)}
.rel .nm{font-family:"IBM Plex Mono",monospace;font-size:12.5px;font-weight:600}
.rel .eq{font-family:"IBM Plex Mono",monospace;font-size:13.5px}
.rel .eq .hub{font-weight:700;padding:1px 7px;border-radius:5px;background:var(--surface-2)}
.rel .eq .ar{color:var(--faint);padding:0 6px}
.rel .ds{display:block;font-family:"IBM Plex Sans",sans-serif;font-size:13px;color:var(--muted);margin-top:3px}
.rel.est{border-left-color:var(--est)}.rel.est .nm{color:var(--est)}
.rel.gen{border-left-color:var(--gen)}.rel.gen .nm{color:var(--gen)}
.rel.av{border-left-color:var(--av)}.rel.av .nm{color:var(--av)}
.rel.int{border-left-color:var(--int)}.rel.int .nm{color:var(--int)}
.rel.sim{border-left-color:var(--sim)}.rel.sim .nm{color:var(--sim)}
.rel.data{border-left-color:var(--data)}.rel.data .nm{color:var(--data)}
.card{background:var(--surface);border:1px solid var(--line);border-radius:11px;box-shadow:var(--shadow);padding:16px 19px;margin-top:13px;border-top:3px solid var(--line)}
.card h3{font-size:16.5px;font-weight:620;margin:2px 0 3px;line-height:1.3}
.card h3 a{color:var(--ink);text-decoration:none}.card h3 a:hover{text-decoration:underline}
.card .cmeta{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--muted);margin-bottom:8px}
.card p{margin:0;font-size:14px}.card p b{font-weight:600;color:var(--ink)}
/* taxonomy tree */
.tree{margin-top:22px;border-top:1px solid var(--line);padding-top:14px}
.node{padding:12px 0 12px 16px;border-left:2px solid var(--line);margin:6px 0}
.node.d2{margin-left:22px;border-left-style:dashed}
.node .nname{font-family:"IBM Plex Mono",monospace;font-size:12.5px;font-weight:600;color:var(--ink);letter-spacing:-.01em}
.node .why{font-size:13.5px;color:var(--muted);margin:4px 0 8px;max-width:78ch;line-height:1.6}
.node .why:before{content:"why · ";font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.plist{display:flex;flex-wrap:wrap;gap:6px}
.p{font-size:12.5px;background:var(--surface-2);border:1px solid var(--line);border-radius:7px;padding:3px 9px;text-decoration:none;color:var(--ink);display:inline-flex;gap:6px;align-items:baseline}
a.p:hover{border-color:var(--est)}
.p .v{font-family:"IBM Plex Mono",monospace;font-size:10.5px;color:var(--faint)}
.cross{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--gen);border-radius:0 10px 10px 0;padding:15px 18px;margin-top:13px}
.cross h4{font-size:15.5px;font-weight:620;margin:0 0 5px}.cross p{margin:0;font-size:14px}
.num{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--gen);margin-right:7px}
.lab-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:13px;margin-top:16px}
.lab{background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:16px 18px;box-shadow:var(--shadow)}
.lab .tag{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:#fff;border-radius:12px;padding:2px 9px;display:inline-block}
.lab.int .tag{background:var(--int)}.lab.est .tag{background:var(--est)}.lab.gen .tag{background:var(--gen)}.lab.sim .tag{background:var(--sim)}
.lab h4{font-size:15.5px;font-weight:620;margin:10px 0 5px}.lab p{margin:0;font-size:13.5px;color:var(--muted)}
footer{margin-top:72px;padding-top:22px;border-top:1px solid var(--line);font-size:12.5px;color:var(--faint);line-height:1.6}
@media(max-width:640px){.wrap{padding:40px 18px 76px}.rel{grid-template-columns:1fr;gap:5px}.node.d2{margin-left:10px}}
"""

def chip(name, aid, venue):
    label = f'<span>{html.escape(name)}</span><span class="v">{html.escape(venue)}</span>'
    if aid:
        return f'<a class="p" href="https://arxiv.org/abs/{aid}" target="_blank" rel="noopener">{label}</a>'
    return f'<span class="p">{label}</span>'

def node_html(n, depth, color):
    chips = "".join(chip(*p) for p in n["papers"])
    kids = "".join(node_html(k, depth + 1, color) for k in n["subs"])
    plist = f'<div class="plist">{chips}</div>' if chips else ""
    return (f'<div class="node d{depth}" style="border-left-color:{"var(--"+color+")" if depth==1 else "var(--line)"}">'
            f'<div class="nname">{html.escape(n["name"])}</div><p class="why">{n["why"]}</p>{plist}{kids}</div>')

def collect(n, out):
    out.extend(n["papers"])
    for k in n["subs"]:
        collect(k, out)

secs, all_papers = [], []
for b in BRANCHES:
    rep = ""
    for nm, aid, venue, note in b["reps"]:
        t = html.escape(nm)
        if aid:
            t = f'<a href="https://arxiv.org/abs/{aid}" target="_blank" rel="noopener">{t}</a>'
        meta = f'arXiv {aid} · {venue}' if aid else venue
        rep += (f'<article class="card" style="border-top-color:var(--{b["id"]})"><h3>{t}</h3>'
                f'<div class="cmeta">{html.escape(meta)}</div><p>{note}</p></article>')
    tree = "".join(node_html(n, 1, b["id"]) for n in b["subs"])
    for n in b["subs"]:
        collect(n, all_papers)
    secs.append(f"""
  <section id="{b['id']}">
    <div class="sec-head"><span class="sec-no" style="color:var(--{b['id']})">{html.escape(b['no'])}</span>
      <h2>{html.escape(b['title'])}</h2></div>
    <div class="formula">{html.escape(b['formula'])}</div>
    <p class="sec-tag">{b['desc']}</p>
    <div class="axis" style="border-left-color:var(--{b['id']})"><span class="lab" style="color:var(--{b['id']})">What splits this branch</span>{b['axis']}</div>
    <div class="qa-lab">Representative papers</div>{rep}
    <div class="tree"><div class="qa-lab" style="margin-top:0">Taxonomy · why each split happens</div>{tree}</div>
  </section>""")

map_html = ""
for cid, nm, left, op, right, ds in RELATIONS:
    if cid == "data":
        eq = f'<span class="ar">{html.escape(left)}</span> <span class="hub">{html.escape(right)}</span>'
    elif cid == "int":
        eq = f'{html.escape(left)} <span class="ar">{op}</span> <span class="hub">SMPL-X</span> + {html.escape(right.split("+",1)[1].strip())}'
    elif cid == "sim":
        eq = f'<span class="hub">{html.escape(left)}</span> <span class="ar">{op}</span> {html.escape(right)}'
    elif right == "SMPL-X":
        eq = f'{html.escape(left)} <span class="ar">{op}</span> <span class="hub">SMPL-X</span>'
    else:
        eq = f'<span class="hub">SMPL-X</span> <span class="ar">{op}</span> {html.escape(right)}'
    map_html += f'<div class="rel {cid}"><div class="nm">{html.escape(nm)}</div><div class="eq">{eq}<span class="ds">{html.escape(ds)}</span></div></div>'

cross_html = "".join(f'<div class="cross"><h4><span class="num">{i:02d}</span>{html.escape(t)}</h4><p>{d}</p></div>'
                     for i, (t, d) in enumerate(CROSSINGS, 1))
lab_html = "".join(f'<div class="lab {c}"><span class="tag">{html.escape(nm)}</span><h4>Where it attaches</h4><p>{d}</p></div>'
                   for nm, c, d in LAB)
n_entries = len(all_papers)
n_unique = len({a for _, a, _ in all_papers if a})

doc = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITLE)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<style>{CSS}</style></head>
<body><div class="wrap">
  <a class="home" href="../../index.html">← 메인으로</a>
  <header>
    <div class="eyebrow">3D human ecosystem · landscape map</div>
    <h1>{html.escape(TITLE)}</h1>
    <p class="sub">{SUB}</p>
    <div class="meta-chips"><span class="chip">6 branches</span><span class="chip">{n_entries} entries · {n_unique} unique arXiv</span>
      <span class="chip">hub A · SMPL-X (explicit)</span><span class="chip">hub B · world model (implicit)</span><span class="chip">as of 2026-09</span></div>
  </header>

  <div class="sec-head" style="margin-top:46px"><span class="sec-no" style="color:var(--faint)">The map</span>
    <h2>What splits the branches — the direction of the arrow</h2></div>
  <p class="sec-tag">주제로 나누면 경계가 흐려진다. SMPL-X를 기준으로 <b>화살표가 어느 쪽을 향하는가</b>로 나누면
    갈래가 깔끔하게 떨어지고, 갈래끼리 어디서 맞물리는지도 같이 보인다.
    상호작용은 화살표 방향이 둘이라 두 갈래로 나눴다 — 세상을 보고 복원하는 <b>들어오는</b> 방향(05)과,
    몸으로 세상을 바꾸는 <b>나가는</b> 방향(06). 06은 출력이 암묵적(비디오)이라 <b>두 번째 허브로 건너가는 다리</b>이기도 하다.</p>
  <div class="map">{map_html}</div>
{''.join(secs)}
  <section>
    <div class="sec-head"><span class="sec-no" style="color:var(--gen)">Crossings</span><h2>Where branches meet, and where they break</h2></div>
    <p class="sec-tag">지도의 값어치는 칸을 나누는 데 있지 않고 칸 사이의 선에 있다.</p>{cross_html}
  </section>
  <section>
    <div class="sec-head"><span class="sec-no" style="color:var(--int)">Our hooks</span><h2>Where the lab's interests attach</h2></div>
    <div class="lab-grid">{lab_html}</div>
  </section>
  <footer>자동 생성 · topics/smplx-landscape/build_survey.py · Branch 01의 전신·손 통합 계보는
    <a href="../hand-in-wholebody/hand-in-wholebody_survey.html">Hand-in-Whole-Body</a>, 추정 쪽 연구자 계보는
    <a href="../gyeongsik-moon/gyeongsik-moon_survey.html">Gyeongsik Moon 계보</a>에서 더 깊이 다룬다.
    arXiv 판본이 확인되지 않은 항목(HumanML3D · HMR-Adapter · Codec Avatar Studio · Three Recipes)은 링크 없이 두었다. 학회가 확인되지 않은 항목은 연도만 적었다.</footer>
</div></body></html>"""
open(OUT, "w", encoding="utf-8").write(doc)
print(f"WROTE {OUT}  ({len(BRANCHES)} branches, {n_entries} entries, {n_unique} unique arXiv)")

# ── paper_list.md: 중첩 분류 + why ────────────────────────────────
def strip(s):  # html → plain-ish for markdown
    return s.replace("<b>", "**").replace("</b>", "**")

L = [f"# SMPL-X 생태계 — 갈래별 논문 리스트", "",
     f"자동 생성 · {n_entries} entries / {n_unique} unique arXiv · 2026-09 기준. "
     "각 분기 아래 `why ·` 줄은 그 분기가 **무엇을 축으로, 왜 갈라지는지**다. arXiv 판본 미확인 항목은 ID를 비웠다.", ""]

def md_node(n, depth):
    L.append(f"{'#' * (depth + 2)} {n['name']}")
    L.append("")
    L.append(f"> why · {strip(n['why'])}")
    L.append("")
    if n["papers"]:
        L.append("| 논문 | 학회 | arXiv |"); L.append("|---|---|---|")
        for nm, aid, venue in n["papers"]:
            L.append(f"| {nm} | {venue} | {f'[{aid}](https://arxiv.org/abs/{aid})' if aid else '—'} |")
        L.append("")
    for k in n["subs"]:
        md_node(k, depth + 1)

for b in BRANCHES:
    L += [f"## {b['no']} · {b['title']}", "", f"`{b['formula']}`", "",
          f"**What splits this branch** — {strip(b['axis'])}", ""]
    for n in b["subs"]:
        md_node(n, 1)

L += ["## 전체 (arXiv ID 기준 중복 제거)", "", "| arXiv | 논문 | 학회 |", "|---|---|---|"]
seen = {}
for nm, aid, venue in all_papers:
    if aid and aid not in seen:
        seen[aid] = (nm, venue)
for aid in sorted(seen):
    nm, venue = seen[aid]
    L.append(f"| [{aid}](https://arxiv.org/abs/{aid}) | {nm} | {venue} |")
L.append("")
open(LIST_OUT, "w", encoding="utf-8").write("\n".join(L))
print(f"WROTE {LIST_OUT}")

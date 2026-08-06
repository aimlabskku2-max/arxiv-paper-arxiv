# HandX: Scaling Bimanual Motion and Interaction Generation

**arXiv**: 2603.28766 | **주제 분류**: Hand-Object Interaction | **출판일**: 2026-03-30 | **학회**: CVPR 2026
**저자/소속**: Zimu Zhang, Yucheng Zhang, Xiyan Xu, Ziyin Wang, Sirui Xu, Kai Zhou, Bing Zhou, Chuan Guo, Jian Wang, Yu-Xiong Wang, Liang-Yan Gui / University of Illinois Urbana-Champaign(UIUC), Specs Inc., Snap Inc.
**링크**: https://arxiv.org/abs/2603.28766

## 한 줄 요약

두 손(bimanual)의 섬세한 손가락 움직임과 손과 손 사이의 접촉(inter-hand contact)까지 담아낸 대규모 데이터셋과 자동 주석 방식, 손 중심 평가지표를 하나로 묶고, 데이터·모델을 키울수록 성능이 좋아지는 "스케일링(scaling)" 경향을 텍스트 기반 양손 동작 생성에서 처음으로 체계적으로 보인 연구다.

## 메인 그림

![HandX 개요: 대규모 양손·정교한 손동작 데이터셋과 세밀한 텍스트 주석, diffusion/autoregressive 두 벤치마크 모델, 유연한 조건부 생성, 그리고 데이터·모델을 키울수록 성능이 향상되는 스케일링 경향](https://arxiv.org/html/2603.28766v1/x1.png)

## 선행 연구

- **사람 전신(whole-body) 동작 생성**: 언어를 동작으로 바꾸는 연구는 초기 latent 변수/순환 신경망(RNN) 모델에서 시작해 autoregressive 모델과 diffusion 모델로 발전했다. 그러나 널리 쓰이는 데이터셋(Motion-X, InterAct 등)은 손을 SMPL의 "뻣뻣한 말단(rigid end-effector)"처럼 다루어 손가락의 관절 움직임(finger articulation)을 거의 담지 못한다.
- **손 중심(hand-centric) 동작 생성**: 음성에 맞춰 제스처를 만드는 co-speech gesture, 물체를 잡는 hand-object interaction, 수어(sign language) 생성 등이 있으나, 대부분 물체 중심(object-centric)이거나 소통용 제스처에 치우쳐 두 손의 협응(coordination)과 손끼리 접촉하는 상황을 충분히 다루지 못한다.
- **손 동작 데이터셋**: InterHand2.6M, HandDiffuse는 언어 주석이 없고, ARCTIC·H2O·GigaHands 같은 손-물체 데이터셋은 물체 조작 위주에 범주형(action label) 주석에 그친다. 최근 BOTH2Hands(양손 8.31시간), 단안(monocular) 복원 기반의 CLUTCH·BOBSL3DT 등이 규모 확장을 시도했지만, 각각 수어 특화, 대략적(action-level) 주석, 복원 노이즈 등의 한계가 있다.

## 문제 제기

기존 방법은 손을 "덤"처럼 취급해서, 정교한 손가락 움직임, 정확한 타이밍의 접촉, 매끄러운 양손 협응 같은 세밀한 단서를 놓친다. 근본 원인은 세 가지다.

1. **데이터 부족**: 세밀한 손가락 동역학과 풍부한 손끼리 접촉을 고품질로 담은 양손 시퀀스가 없다.
2. **통합의 어려움**: 데이터 출처마다 골격(skeleton), 프레임률(frame rate), 주석 방식이 달라 여러 데이터를 합치기 어렵다.
3. **평가지표 부재**: 기존 지표는 손의 사실성이나 양손 협응을 거의 평가하지 못해 실패 원인을 진단하고 진전을 측정하기 어렵다.

이 문제는 몰입형 미디어, 원격현전(telepresence), 체화 AI(embodied AI), 인간-컴퓨터 상호작용처럼 사실적 손동작이 필수인 응용에서 특히 걸림돌이 된다.

## 연구 주제

이 논문은 "자유로운 자연어 문장으로부터 세밀한 양손 동작을 생성"하는 문제(fine-grained bimanual text-to-hand motion generation)를 다룬다. 이를 위해 데이터, 주석, 평가를 아우르는 통합 기반(unified foundation)인 **HandX**를 제안하고, 그 위에서 대표적 생성 패러다임들의 스케일링 거동을 분석한다.

## 연구 방법

**1) 데이터셋 구축 (HandX)**

- **공개 데이터 통합**: 여러 양손/손-물체/에고센트릭 데이터셋(GigaHands, HOT3D, ARCTIC, H2O, HoloAssist 등)을 하나의 골격 표현과 좌표계로 표준화(canonicalize)하고, 품질이 낮은 시퀀스를 걸러낸다.
- **신규 모션캡처**: 36대 카메라의 OptiTrack 광학 모션캡처 시스템과 손당 25개의 반사 마커(reflective marker)로, 가림(occlusion)과 빠른 손가락 움직임이 있는 정교한 양손 상호작용을 새로 촬영한다. 마커 궤적에서 관절 중심을 추정하고 뼈 길이 등 해부학적 제약을 적용해 손 골격을 복원한다.
- **강도 인지 필터(intensity-aware filter)**: 관절 각속도(joint angular velocity) 기준으로 정적이거나 거의 움직이지 않는 구간을 제거해, 생성 모델이 "얼어붙는(freeze)" 현상을 막는다.

**2) 양손 동작 자동 주석 (decoupled captioning)**

수작업 주석은 규모상 불가능하므로, "동작 이해"와 "언어 생성"을 분리한 2단계 전략을 쓴다.

- (a) **운동학적 특징 추출**: 손가락 굽힘(finger flexion), 손가락-손바닥 거리, 두 손의 공간 관계 같은 구조화된 서술자(descriptor)를 계산하고, 시간에 따른 변화를 접촉(touch)·미끄러짐(slide)·놓기(release) 같은 이벤트로 분절해 JSON 형식으로 정리한다.
- (b) **LLM 추론으로 언어화**: 대규모 언어모델(LLM)이 이 구조화된 특징을 읽고, 왼손·오른손·손 사이 관계를 모두 다루며 접촉·분리·과신전(hyperextension) 같은 핵심 이벤트를 시간 순서대로 서술한다. 상세도가 다른 5단계 수준의 설명을 생성해 다양성을 확보한다.

**3) 생성 모델 벤치마크**

동작 시퀀스를 $\boldsymbol{p}=\{\boldsymbol{p}^{1},\dots,\boldsymbol{p}^{F}\}$($\boldsymbol{p}^{i}\in\mathbb{R}^{2J\times3}$, $J$는 손당 관절 수), 텍스트를 $T=\{T_L,T_R,T_I\}$(왼손·오른손·손 사이)로 정의하고 두 가지 대표 모델을 비교한다.

- **Diffusion 모델**: 각 관절을 3D 좌표에 1차원 회전 스칼라(rotation scalar)를 더해 $\boldsymbol{x}^{i}\in\mathbb{R}^{2J\times4}$로 표현한다. T5 텍스트 인코더로 세 종류의 텍스트를 따로 인코딩하고 각각 학습형 CLS 토큰을 붙여, 오른손 동작이 왼손에 잘못 배정되는 문제를 막는다. 세 임베딩을 노이즈 동작 임베딩과 교차어텐션(cross-attention)한 뒤 잔차 연결로 합쳐 깨끗한 신호를 예측한다.
- **Autoregressive(AR) 모델**: 유한 스칼라 양자화(Finite Scalar Quantization, FSQ)로 동작을 토큰화하고, 세 텍스트를 구분자 토큰으로 이어 붙인 "텍스트 프리픽스(text-prefix)" 뒤에 다음 동작 토큰을 예측하는 방식이다. 텍스트 토큰끼리는 양방향, 동작 토큰은 인과적(causal) 어텐션을 쓴다.
- **다목적 조건부 생성(versatile generation)**: diffusion의 추론 시점 부분 노이즈 제거(partial denoising)로 하나의 모델이 동작 사이 채우기(in-betweening), 키프레임 기반 생성, 손목 궤적 지정, 한 손을 고정한 손 반응 생성(hand-reaction), 장기(long-horizon) 생성까지 지원한다.

**4) 평가지표**

기존 FID, Diversity, R-Precision, Multimodal Distance(MM Dist)에 더해, 접촉 중심 지표로 **접촉 정밀도(precision) $C_{\mathrm{prec}}$, 재현율(recall) $C_{\mathrm{rec}}$, F1 점수 $C_{\mathrm{F1}}$**를 새로 도입한다(접촉 임계값 2cm).

## 실험 결과 / 연구 의의

**데이터셋 규모** — HandX는 기존 손 데이터셋 대비 세밀한(fine-grained) 다단계 주석과 접촉이 풍부한 양손 동작을 함께 제공한다.

| 데이터셋 | 길이(h) | 프레임(M) | 텍스트 세밀도 | 텍스트(K) |
| --- | --- | --- | --- | --- |
| Motion-X | 144.2 | 15.6 | 대략적(coarse) | 8.1 |
| InterAct | 30.7 | 3.3 | 대략적 | 48.6 |
| BOTH2Hands | 8.31 | 1.8 | 대략적 | 23.5 |
| GigaHands | 2.58 (34.0) | 0.28 (3.7) | 대략적 | 84 |
| **HandX (제안)** | **54.2** | **5.9** | **세밀함(fine-grained)** | **485.7** |

**스케일링 경향 (Diffusion, 텍스트→동작)** — 데이터 비율과 디코더 층 수를 함께 키울수록 텍스트 정합도(R-Precision)와 접촉 정확도(Intra-hand $C_{\mathrm{F1}}$)가 일관되게 향상된다. 최고 성능은 전체 데이터 + 12층에서 나온다.

| 데이터 비율 | 디코더 층 | R-Precision Top-1 ↑ | FID ↓ | Intra-hand $C_{\mathrm{F1}}$ ↑ |
| --- | --- | --- | --- | --- |
| Ground Truth | – | 0.854 | 0.000 | 0.984 |
| 0.05 | 4 | 0.142 | 2.574 | 0.523 |
| 1.0 | 4 | 0.168 | 2.219 | 0.517 |
| 1.0 | 8 | 0.285 | 1.617 | 0.571 |
| **1.0** | **12** | **0.427** | **1.349** | **0.641** |

**AR 모델 스케일링** — FSQ 코드북 크기와 모델 크기를 함께 키울 때 FID가 가장 좋아지고, 한쪽만 키우면 오히려 성능이 나빠질 수 있다. 가장 큰 설정(215.31M 모델 + 코드북 4096)에서 FID 1.721, R-Precision Top-1 0.281을 기록한다.

**계산량 스케일링 법칙** — R-Precision과 연산량(FLOPs) 사이에 뚜렷한 로그-선형(log-linear) 관계가 관찰되며, 상관계수가 높게 나타난다(Figure 4).

**연구 의의** — (1) 대규모 통합 코퍼스에 정교한 양손 모션캡처를 더한 손 중심 데이터 기반을 마련했고, (2) 특징 추출 + LLM 추론으로 확장 가능한 세밀한 주석 파이프라인을 제시했으며, (3) diffusion·AR 두 패러다임에서 데이터/모델 스케일링 경향을 처음으로 체계적으로 분석했다. 나아가 학습된 손기술이 정교한 로봇 손(dexterous robot hands)을 단 실제 휴머노이드로 전이될 수 있음을 보였다.

## 한계

- 논문에서 관찰된 스케일링은 유한한 데이터/모델 범위 안에서의 경향이며, AR 모델은 코드북과 모델 크기의 균형이 맞지 않으면 성능이 떨어지는 등 두 요소가 함께 커질 때만 이득이 안정적이다.
- 통합된 공개 데이터 중 상당수는 단안 복원 등에서 오는 노이즈와 주석 품질 편차가 있어, 표준화·필터링에 의존해야 한다.
- 시각화를 위한 MANO 파라미터는 사후 최적화(post-optimization)로 복원하는 방식이라 직접 손 메시(mesh)를 생성하지는 않는다.
- (본문 HTML에서 결론·정성 평가 세부 서술이 확인되는 범위까지만 반영했으며, 물체 자체의 동역학을 함께 생성하는 부분은 이 논문의 초점 밖이다.)

## 우리 연구와 연결되는 점

- **Hand-Object Interaction 연구의 데이터/평가 표준**: 손끼리의 접촉과 양손 협응을 정량화하는 접촉 기반 지표($C_{\mathrm{prec}}$, $C_{\mathrm{rec}}$, $C_{\mathrm{F1}}$)와 세밀한 다단계 텍스트 주석 방식은, 손-물체 상호작용을 다루는 후속 연구에서 재사용·확장할 수 있는 평가 틀을 제공한다.
- **자동 주석 파이프라인**: "구조화된 운동학적 특징 추출 → LLM 언어화"라는 분리형 전략은, 라벨이 부족한 상호작용 데이터에 저비용으로 의미가 풍부한 설명을 붙이는 데 응용할 수 있다.
- **스케일링 관점**: 데이터·모델·연산량을 함께 키울 때의 로그-선형 향상은, 상호작용 생성 모델을 설계할 때 자원 배분(데이터 확장 vs 모델 확장)의 근거로 삼을 수 있다.
- **로봇/휴머노이드 전이**: 생성된 정교한 손동작이 실제 로봇 손으로 전이 가능함을 보였다는 점은, 시뮬레이션-실물(sim-to-real) 혹은 모방학습 기반 조작 연구와 연결된다.

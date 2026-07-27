# LIME: Learning Intent-aware Camera Motion from Egocentric Video

**arXiv**: 2607.02417 | **주제 분류**: Egocentric Vision | **출판일**: 2026-07-02 | **학회**: 프리프린트
**저자/소속**: Boyang Sun, Jiajie Li, Yung-Hsu Yang, Chenyangguang Zhang, Tim Engelbracht, Sunghwan Hong, Cesar Cadena, Marc Pollefeys, Hermann Blum (ETH Zurich, Microsoft, University of Bonn)
**링크**: https://arxiv.org/abs/2607.02417

## 한 줄 요약

사람이 찍은 일상 1인칭(egocentric) 영상만으로, "자연어로 표현된 의도(intent)에 맞게 카메라를 어디로 움직여야 다음 관측이 더 유용한지"를 학습하는 vision-language 모델 LIME을 제안한다. 즉 카메라 움직임 자체를 하나의 독립된 행동(action)으로 다룬다.

## 메인 그림
![LIME: 수동적 인간 영상에서 의도 기반 카메라 모션을 학습해 로봇으로 전이](https://arxiv.org/html/2607.02417v1/image/teaser_v2.jpg)

현재 시점 이미지와 자연어 의도가 주어지면, LIME은 의도에 맞는 시각 증거를 얻기 위한 상대적 목표 카메라 자세(relative target camera pose)를 생성한다. 학습은 수동적으로 촬영된 인간 1인칭 영상에서 이뤄지고, 이를 로봇에 전이한다.

## 선행 연구

- **Active perception(능동적 지각)**: 더 좋은 관측을 얻기 위해 센서를 어떻게 움직일지 오래 연구되어 왔다. 다만 대부분 exploration(탐색), reconstruction(복원), object search(물체 탐색) 같은 미리 정해진 목표(task-specific utility)를 최적화한다.
- **Vision-Language Navigation(VLN, 시각-언어 내비게이션)**: 자연어 지시로 경로·목적지·랜드마크를 지정하고, 로봇의 이동(base motion)에 따라 시점이 부수적으로 바뀐다. 예: [Uni-NaVid](https://arxiv.org/abs/2412.06224).
- **Vision-Language-Action(VLA, 시각-언어-행동) 조작 모델**: 시각 관측으로 로봇 팔·그리퍼 제어를 조건화한다. 카메라 움직임은 몸체나 실행 정책에 종속된다. 예: [OpenVLA](https://arxiv.org/abs/2406.09246), [RT-2](https://arxiv.org/abs/2307.15818), [$\pi_0$](https://arxiv.org/abs/2410.24164).

## 문제 제기

기존 연구에서 "카메라를 어떻게 움직일까"는 항상 내비게이션이나 조작의 부산물이었지, 그 자체가 일급 행동(first-class action)으로 다뤄지지 않았다. 하지만 사람은 가림막 뒤를 보려고 몸을 기울이거나, 작은 디테일을 확인하려 다가가거나, 모퉁이를 돌기 전 살짝 들여다보는 등, **의도를 해소하기 위해 먼저 시점을 바꾼다.** 핵심 난점은 두 가지다.

1. **의도 의존성**: 같은 장면이라도 물체를 자세히 볼지, 가려진 영역을 드러낼지, 방에 들어갈지에 따라 움직여야 할 방향이 다르다.
2. **다중 해(multi-hypothesis)**: 같은 의도라도 유용한 증거를 주는 유효한 목표 자세가 여러 개일 수 있다. 따라서 이는 하나의 정답을 맞히는 회귀(regression) 문제가 아니라, 목표 카메라 자세들에 대한 **언어 조건부 분포(language-conditioned distribution)**를 예측하는 문제다.

게다가 이런 능동 지각 시연(teleoperated active-perception demonstration)은 수집 비용이 매우 커서 지도학습 데이터가 부족하다.

## 연구 주제

**Language-conditioned camera motion generation(언어 조건부 카메라 모션 생성)**을 새롭게 정식화한다. 현재 RGB 관측 $I_s$와 자유형 자연어 의도 $x$가 주어지면, 다음 관측을 얻기 위한 상대적 $SE(3)$ 목표 카메라 자세 $T_{gs}$의 분포를 예측한다($SE(3)$는 3D 병진 + 회전을 함께 표현하는 공간). 동시에 그 시점이 무엇을 새로 드러낼지 자연어로 요약한 **observation-gain(관측 이득) 설명 $g$**도 예측한다. 모델이 학습하는 것은:

$$p_{\theta}(g\mid I_s,x),\qquad p_{\theta,\phi}(T_{gs}\mid I_s,x,g)$$

## 연구 방법

**1) 수동 영상에서 능동 지각 지도(supervision) 채굴**

원격조작 시연 없이, 사람 1인칭 영상에서 시간적으로 떨어진 두 프레임 $(I_s, I_g)$을 짝지어 학습 신호를 만든다. 두 프레임 사이의 상대 카메라 변환이 모션 목표가 되고(자세가 없으면 [Depth Anything 3](https://arxiv.org/abs/2511.10647) 같은 도구로 복원), 사후(hindsight)에 목표 프레임과 상대 모션을 특권 정보(privileged context)로 준 VLM 라벨러가 그럴듯한 의도 집합 $\mathcal{X}_{s,g}=\{x_i\}$와 관측 이득 $g$를 생성한다. 라벨러에게 자유형 캡션 대신 **대조적 필드(motion type, 새로 보이는 물체/영역, 기존 내용의 개선된 뷰, 두 뷰 사이 공간 앵커 등)**를 요구해 실제 카메라 움직임에 근거를 묶는다. 이렇게 RoomTour3D(방 규모 walkthrough)와 Nymeria(신체 규모 1인칭 상호작용)에서 약 **3M(300만)개**의 의도 조건부 학습 예시를 만든다.

**2) LIME 모델 구조**

- **VLM 백본**: Qwen3-VL-4B-Instruct를 사용. vision encoder는 freeze하고 multimodal projector, 언어 모델, pose head를 학습.
- **언어 인터페이스(autoregressive)**: VLM 디코더가 관측 이득 $g$를 자기회귀적으로 생성. 이는 "이 움직임이 무엇을 드러낼지"를 VLM 고유의 출력 공간에 담아 hidden representation이 미래 시점의 증거를 미리 예상하도록 돕는 보조 지도 역할.
- **연속 pose head(flow-matching)**: 행동을 언어 토큰으로 표현하지 않고 별도의 연속 flow-matching head를 붙여 $SE(3)$ 기하 정보를 보존하고 여러 유효 목표 자세의 다중 분포를 모델링한다. 목표 변환은 3D 병진 + 회전 행렬 앞 두 열을 쓰는 연속 6D 표현으로 $y\in\mathbb{R}^9$로 파라미터화. flow time $t\sim\mathcal{U}(0,1)$과 노이즈로 $z_t=(1-t)\epsilon+t y$를 만들고, x-prediction 방식으로 깨끗한 목표 $\hat{y}_\phi$를 예측한다.
- **손실**: $\mathcal{L}=\mathcal{L}_{\mathrm{gain}}+\lambda_{\mathrm{pose}}\mathcal{L}_{\mathrm{pose}}$ (관측 이득의 next-token 예측 + pose의 flow matching). pose loss는 detach된 VLM hidden state를 써서 flow head와 투영만 갱신.
- **학습 비용**: 16 × NVIDIA GH200 GPU에서 bf16 1 epoch, 약 30시간. 추론 시 생성한 gain 토큰의 hidden state를 캐시해 재사용하여 VLM forward를 두 번 돌리지 않는다.

**3) 벤치마크**

InteriorGS(약 1K개 실내 3DGS 장면)에서 임의 카메라 자세로 photorealistic 렌더링이 가능한 벤치마크를 구축. 총 **425개** 예시를 세 의도 계열로 나눈다: Target-approaching(대상 접근), Exploration(탐색), Perspective-shift(시점 전환). 평가는 6m 병진 + 600도 회전의 공유 모션 예산 안에서 다단계로 진행하고, 성공은 "의도를 만족하는 뷰를 획득했는가"로 정의(정답 자세와의 일치가 아님). Gemini-3.1-Pro-Preview가 판정하며, 이동 경로가 점군에서 0.15m 이상 떨어져 충돌 없이 진행했는지도 요구하는 **CA-SR(Collision-Aware Success Rate)**을 함께 보고.

## 실험 결과 / 연구 의의

주요 지표는 성공률 SR(%)과 충돌 인지 성공률 CA-SR(%)이며, 3회 실행의 평균 ± 표준편차다.

| Method | Target SR | Target CA-SR | Exploration SR | Exploration CA-SR | Perspective SR | Perspective CA-SR | All SR | All CA-SR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JanusVLN | 2.0±0.0 | 1.3±0.0 | 34.5±0.6 | 27.5±0.6 | 31.3±0.6 | 31.3±0.6 | 21.9±0.2 | 19.3±0.3 |
| Uni-NaVid | 0.0±0.0 | 0.0±0.0 | 13.4±2.5 | 11.0±1.8 | 26.5±1.4 | 26.2±1.3 | 12.6±0.8 | 11.8±0.5 |
| VG-AVS | 8.6±0.0 | 6.6±0.0 | 30.0±0.9 | 11.7±0.9 | 36.4±0.4 | 33.1±1.0 | 24.3±0.2 | 16.5±0.0 |
| VLMnav | 0.0±0.0 | 0.0±0.0 | 4.5±0.7 | 3.8±0.7 | 8.4±0.6 | 8.4±0.6 | 4.1±0.3 | 3.8±0.3 |
| **Ours (LIME)** | **45.8±1.6** | **31.8±2.2** | **51.4±0.6** | **32.6±1.4** | **45.8±1.1** | **39.4±1.0** | **47.7±0.1** | **34.4±0.2** |

- LIME이 세 의도 계열과 전체에서 모두 최고 성능. 전체 SR 47.7%로 2위 VG-AVS(24.3%)의 약 2배.
- 벤치마크 장면에 대한 fine-tuning 없이 **오직 1인칭 영상으로만** 학습했는데도 렌더링 평가 환경에서 강하게 작동. CA-SR에서도 우위를 유지해, 1인칭 모션 지도가 통행 가능성(traversability) bias까지 제공함을 시사.
- Gemini 자동 판정은 90개 예시(450개 궤적 라벨)에 대한 인간 판정과 전체 91.3% 일치(계열별 85.3~98.0%).
- 같은 현재 이미지에서 언어 의도만 바꾸면 flow-matching head가 뽑는 5개 목표 자세 샘플이 서로 다른 의도 관련 증거 쪽으로 이동 → 장면 prior가 아니라 **의도에 조건화**됨을 확인. 목표가 시야에 있으면 샘플이 모이고, "방 나가기"처럼 모호하면 여러 방향으로 퍼져 불확실성도 포착.
- **실로봇 전이**: 팔 달린 Boston Dynamics Spot에 경량 LoRA 체크포인트로 배치해 "물체 아래 보기", "오븐 왼쪽 확인" 등 언어 조건부 시점 변경 성공. 조작 정책 [VidBot](https://arxiv.org/abs/2503.07135)과 결합해, 대상이 시야 밖일 때 LIME이 먼저 대상을 드러낸 뒤 조작을 수행하고 결과를 검증. 재사용 가능한 active-perception 모듈로서 manipulation, embodied QA, 다단계 로봇 행동을 지원함을 보임.

**의의**: 평범한 인간 1인칭 영상을 능동 지각 행동의 지도 데이터로 바꿔, 카메라 모션을 재사용 가능한 독립 행동 primitive로 학습한 첫 정식화 중 하나.

## 한계

- 논문 본문(Conclusion)이 HTML에서 잘려 저자가 명시한 한계 목록은 확보하지 못함. 아래는 방법·설정에서 드러나는 구조적 제약이다.
- **판정의 VLM 의존**: 성공 여부를 Gemini-3.1-Pro-Preview가 판정하므로 판정 모델의 편향이 지표에 반영될 수 있다(인간 일치 91.3%로 검증하긴 함).
- **자세 복원 의존**: 데이터셋에 카메라 자세가 없으면 off-the-shelf 복원 도구에 의존하며, 그 정확도가 모션 목표의 품질을 좌우.
- **실로봇은 LoRA 적응 필요**: 렌더링 벤치마크 학습본을 실제 로봇에 쓰려면 별도 LoRA 적응 체크포인트가 필요했고, 실험도 정성적 시연 수준.
- **평가가 렌더링/실내 중심**: InteriorGS·ScanNet++ 등 실내 3DGS 위주로, 실외·동적 환경 일반화는 검증 범위 밖.
- **의도 라벨의 사후 생성**: 학습 의도가 VLM 라벨러의 hindsight 추정이라, 실제 인간 의도와 다를 수 있는 라벨 노이즈 가능성.

## 우리 연구와 연결되는 점

- **1인칭 영상을 행동 지도로 재활용**: 수동적으로 촬영된 egocentric video에서 "무엇을 하려 했는가(intent)"와 "그 결과 무엇이 새로 보였는가(observation gain)"를 대조적으로 라벨링하는 방식은, egocentric vision에서 의도/attention을 모델링할 때 그대로 응용 가능한 데이터 큐레이션 전략이다.
- **언어 인터페이스 + 연속 행동 head의 결합**: VLM의 자기회귀 언어 출력(설명 가능한 중간 표현)과 flow-matching 연속 head(기하적으로 정확한 다중 분포 행동)를 분리·결합한 설계는, 시선/시점 예측이나 gaze-guided 태스크에 다중 가설 예측이 필요할 때 참고할 만한 아키텍처 패턴이다.
- **평가 프로토콜**: "정답 자세 일치"가 아니라 "의도 만족 뷰 획득"으로 성공을 정의하고, 공유 모션 예산 + 충돌 인지 지표(CA-SR)로 서로 다른 행동 인터페이스를 공정 비교하는 방식은, 정답이 여러 개인 능동 지각/시점 선택 문제를 평가할 때 유용한 틀이다.

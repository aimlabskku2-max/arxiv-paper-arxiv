# ReViV: Reconstructing the Viewer and the View in 4D from Monocular Egocentric Video

**arXiv**: 2607.17790 | **주제 분류**: Egocentric Vision | **출판일**: 2026-07-20 | **학회**: ECCV 2026
**저자/소속**: Xiaozhong Lyu*, Gen Li*, Zhiyin Qian, Xucong Zhang, Marc Pollefeys, Siyu Tang (*공동 1저자) — ETH Zurich / Delft University of Technology / Microsoft
**링크**: https://arxiv.org/abs/2607.17790

## 한 줄 요약
1인칭 RGB 영상 한 개만 넣으면 착용자의 몸·손·시선(viewer)과 주변 장면의 카메라 궤적·깊이(view)를 하나의 feed-forward 모델이 동시에 복원하는, 최초의 통합 egocentric 4D 재구성 프레임워크다.

## 메인 그림
![단일 1인칭 RGB 영상에서 body·hand·gaze와 camera·depth를 한 번에 복원](https://arxiv.org/html/2607.17790v1/x1.png)
Figure 1: 모노큘러 1인칭 영상을 입력하면 사람 중심 모달리티(몸 자세, 손 자세, 시선)와 장면 중심 모달리티(카메라 궤적, 깊이)를 함께 예측하고, 이를 시간적으로 일관된 하나의 viewer-view 4D 재구성으로 통합한다.

## 선행 연구
- **4D 재구성**: 여러 대의 동기화된 카메라로 동적 장면을 복원하는 연구가 성숙했고, Shape of Motion처럼 3D Gaussian과 모션 베이스로 장기 동역학을 다루는 방법, 그리고 테스트 시점 최적화를 없앤 feed-forward 방식이 등장했다. 다만 대부분 3인칭 혹은 멀티뷰 세팅을 전제한다.
- **1인칭 장면 재구성**: EgoM2P는 RGB·depth·gaze·카메라를 함께 학습하는 멀티태스크 사전학습을 제안했고, EgoGaussian은 3D 장면과 물체 움직임을 동시에 복원하며, EgoMono4D는 라벨이 부족한 1인칭 도메인에 자기지도 포인트클라우드 시퀀스 복원을 적용했다. 모두 장면·물체 기하에 초점이 있고 사람의 전신 움직임은 다루지 않는다.
- **1인칭 사람 모션 추정**: 어안 카메라 기반 전신 자세 추정, EgoEgo(머리 움직임 → 전신 모션), Ego-Pose(강화학습), HMD²·EgoAllo·UniEgoMotion(조건부 diffusion) 등이 있다. 정확도는 좋지만 SLAM 궤적, 3D 포인트클라우드, 외부 손 트래커 같은 **보조 입력**에 의존한다.
- **시선(gaze) 활용**: 2D 영상에서 3D 장면 내 미래 시선을 예측하거나, gaze로 정규화된 attention으로 VLM의 1인칭 행동 이해를 강화하는 연구가 있다.

## 문제 제기
1. **분리된 문제 취급**: 기존 방법은 "장면 인식"과 "착용자 ego-motion 모델링"을 따로 푼다. 그런데 1인칭 영상에서 카메라 움직임은 곧 사람 머리 움직임이라 둘은 강하게 얽혀 있다. 따로 풀면 장면 기하와 착용자 모션이 시간적으로 어긋난다.
2. **보조 입력 의존**: 미리 계산된 카메라 궤적(SLAM), 포인트클라우드, 전용 hand tracker가 필요해 특수 하드웨어가 있어야만 쓸 수 있다. 일반적인 in-the-wild 모노큘러 영상에는 적용이 어렵다.
3. **느린 추론**: 최적화 기반 방법이나 diffusion 기반 방법은 클립 하나에 수십~수백 초가 걸린다.
4. **근본적 관측 불가능성**: 1인칭 카메라는 착용자 자신의 몸을 거의 못 본다. 그래서 $f:\mathcal{X}\rightarrow\mathcal{Y}$ 형태의 결정론적 회귀는 ill-posed하다(해가 여러 개인 multimodal 문제).

## 연구 주제
단일 모노큘러 1인칭 RGB 영상만으로 **viewer(몸·손·시선)와 view(카메라 궤적·깊이)를 동시에, 시간적으로 일관되게, 빠르게** 복원하는 통합 4D 재구성. 결정론적 회귀 대신 멀티모달 신호 전체의 **결합 확률분포(joint probability distribution)** 학습으로 정식화한다.

$$p(\mathcal{X},\mathcal{Y})=p(\mathbf{x}_{\text{rgb}},\mathbf{y}_{\text{hand}},\mathbf{y}_{\text{body}},\mathbf{y}_{\text{gaze}},\mathbf{y}_{\text{depth}},\mathbf{y}_{\text{cam}})$$

추론 시에는 RGB만 관측(visible)으로 두고 나머지를 조건부 $p(\mathcal{Y}\mid\mathcal{X})$에서 샘플링한다.

## 연구 방법

### 1) 데이터 엔진 — 이질적인 1인칭 데이터셋을 하나로
서로 좌표계와 센서 구성이 다른 9개 데이터셋을 통합해 사전학습 코퍼스를 EgoM2P의 4B에서 **7B unique token**으로 확장했다(프로젝트 페이지 기준 600시간 이상의 1인칭 영상).

| 데이터셋 | RGB | Depth | Gaze | Camera | Hand | Body |
|---|---|---|---|---|---|---|
| EgoExo4D | O | X | O | O | X | X |
| HoloAssist | O | O* | O | O | O | X |
| HOT3D (Aria) | O | O* | O | O | O | X |
| HOT3D (Quest) | O | O* | X | O | O | X |
| ARCTIC | O | O* | X | O | O | X |
| TACO | O | O* | X | O | O | X |
| H2O | O | O | X | O | O | X |
| EgoGen | O | O | X | O | X | X |
| Nymeria | O | O* | O | O | X | O |

(O*: 논문에서 생성한 pseudo-label)

- **시간 일관성 있는 기하 pseudo-labeling**: depth가 없는 데이터셋에는 Video Depth Anything으로 시간적으로 일관된 비디오 depth pseudo-label을 자동 생성한다. 덕분에 손-물체 상호작용에 국한됐던 기하 supervision을 다양한 실환경으로 확장했다.
- **통합 kinematic 표현**: 손은 **카메라 공간**에 투영해(궤적과 무관한, 시점 상대 표현) 전역 이동과 분리된 조작(manipulation) prior를 학습시킨다. 몸은 **중력 정렬 전역 좌표계**를 쓴다 — 첫 프레임 카메라 포즈의 up-vector를 중력 반대 방향으로 맞춰 지면과 평행한 기준계를 만들어, 초기 카메라 기울기(pitch/roll) 아티팩트를 제거한다.

### 2) 통합 이산 표현 (Unified Discrete Representation)
픽셀 배열부터 희소한 관절 벡터까지 성질이 완전히 다른 모달리티를 연속 공간에서 같이 모델링하기 어려우므로, **모달리티별 VQ-VAE**로 모두 discrete token으로 바꾼다.

$$\mathbf{Z}=[\mathbf{z}_{\text{rgb}},\mathbf{z}_{\text{depth}},\mathbf{z}_{\text{cam}},\mathbf{z}_{\text{gaze}},\mathbf{z}_{\text{hand}},\mathbf{z}_{\text{body}}]$$

- **몸/손 tokenizer**: 통합된 전신 데이터가 부족하므로, body-only와 hand-only 데이터를 따로 쓸 수 있는 **dual-stream(분리형)** 설계. 2D convolution으로 국소 kinematic prior를 뽑고 12-block Transformer encoder로 210차원 latent에 투영한다. codebook collapse를 막기 위해 임베딩을 단위 구(unit sphere)에 투영하는 **spherical quantization** + EMA codebook 업데이트를 쓴다. 대칭 구조의 12-block Transformer decoder가 복원하며 $L_2$ 재구성 손실 + codebook commitment 손실로 학습.
- **RGB/Depth**: Cosmos Tokenizer로 양자화.
- **Gaze/Camera**: EgoM2P의 tokenizer를 7B 데이터셋에서 재학습.

### 3) Masked Generative Egocentric Transformer (MGET)
- T5 기반 encoder-decoder, encoder/decoder 각 **12 Transformer block**, hidden dimension **768**.
- 모달리티별 embedding layer + 학습 가능한 modality-type embedding + 고정 sinusoidal 시공간 위치 인코딩.
- 양자화로 잃는 미세 픽셀 디테일을 보완하려고, 원본 영상을 직접 인코딩하는 **학습 가능한 ViT 브랜치** $\mathbf{x}_{\text{ViT}}$를 추가 시각 컨텍스트로 붙인다.
- 학습 목표는 랜덤 마스킹된 토큰의 cross-entropy 하나:

$$\mathcal{L}_{\text{mask}}(\theta)=-\mathbb{E}_{\mathbf{Z},\mathbf{M}}\left[\sum_{i\in\mathcal{M},z_{i}\notin\mathbf{x}_{\text{ViT}}}\log p_{\theta}(z_{i}\mid\mathbf{Z}_{\mathcal{V}})\right]$$

  단일 손실이지만 사실상 멀티태스크로 작동한다. 같은 모달리티 내부를 가리면 **intra-modal 시간 동역학**(예: $p(\mathbf{z}_{\text{body},\mathcal{M}}\mid\mathbf{z}_{\text{body},\mathcal{V}})$)을, 모달리티를 가로질러 가리면 **cross-modal 상관**(예: $p(\mathbf{z}_{\text{body},\mathcal{M}}\mid\mathbf{z}_{\text{rgb}})$)을 배운다. 그 결과 별도의 해부학적 제약이나 smoothness regularizer 없이도 생체역학적으로 그럴듯하고 매끄러운 모션이 나온다.
- **추론**: $\mathbf{Z}_{\mathcal{V}}=\mathbf{Z}_{\mathcal{X}}$(RGB만 관측), $\mathbf{Z}_{\mathcal{M}}=\mathbf{Z}_{\mathcal{Y}}$(나머지 전부 마스킹)로 두고 iterative parallel decoding으로 한 번에 복원한다.
- **Metric alignment**: 모노큘러 depth는 스케일이 모호하므로 affine-invariant depth를 예측한 뒤, 복원된 장면 기하에서 **바닥 평면(floor plane)** 을 피팅해 metric 스케일을 잡는다. 바닥이 안 보이는 영상에는 VIPE의 metric depth를 선택적 기하 앵커로 쓴다.
- 사전학습 규모: 7B unique token 데이터셋에서 **500B 이상의 training token**으로 최적화.

## 실험 결과 / 연구 의의

**평가 설정**: 모든 시퀀스를 2초 클립으로 자르고, 영상 모달리티(RGB·depth)는 30 FPS → 8 FPS, 해상도 256×256으로 다운샘플. 카메라·gaze·body·hand는 원본 30 FPS 유지.

### 1인칭 전신 모션 복원 (Aria Digital Twin, 학습에서 완전히 제외된 미학습 데이터셋, 3,185 클립)

| Method | 입력 카메라 궤적 | GA-MPJPE ↓ | PA-MPJPE ↓ | Similarity ↑ | FID ↓ | Time (s) ↓ |
|---|---|---|---|---|---|---|
| EgoAllo | VIPE | 227.6 | 167.5 | 0.529 | 1.069 | 101.0 |
| EgoAllo | GT Cam | 198.4 | 136.8 | 0.556 | 1.160 | 72.5 |
| UniEgoMotion | VIPE | 130.5 | 98.4 | 0.572 | 1.087 | 37.6 |
| UniEgoMotion | GT Cam | 105.8 | 88.7 | 0.591 | 1.098 | 9.1 |
| **ReViV (Ours)** | **없음** | **111.5** | **88.6** | **0.751** | **0.442** | **0.7** |

핵심은 ReViV가 **카메라 궤적을 전혀 받지 않고도** GT 카메라를 받은 baseline보다 국소 자세 정확도(PA-MPJPE), 의미적 대응(Similarity), 모션 현실성(FID)에서 앞선다는 점이다. 전역 정렬(GA-MPJPE)만 GT 카메라를 쓴 UniEgoMotion이 약간 낫다. 속도는 EgoAllo 대비 100배, UniEgoMotion 대비 10배 이상 빠르다.

### 1인칭 손 모션 복원 (4개 벤치마크)
HoloAssist(검증 27,910 클립 중 3,000 샘플), HOT3D(1,519), ARCTIC(449), TACO(998).

| Method | Time (s) ↓ | HoloAssist GA ↓ | HoloAssist RA ↓ | HoloAssist PA ↓ | HOT3D GA ↓ | HOT3D RA ↓ | HOT3D PA ↓ |
|---|---|---|---|---|---|---|---|
| HaMeR | 72 | 59.5 | 57.9 | 32.9 | 94.4 | 74.1 | 48.1 |
| Dyn-HaMR | 280 | 49.6 | **31.5** | 23.0 | 107.7 | **46.9** | 32.0 |
| **ReViV (Ours)** | **0.7** | **23.5** | 29.7 | **10.5** | **38.2** | 48.1 | **13.6** |

| Method | Time (s) ↓ | ARCTIC GA ↓ | ARCTIC RA ↓ | ARCTIC PA ↓ | TACO GA ↓ | TACO RA ↓ | TACO PA ↓ |
|---|---|---|---|---|---|---|---|
| HaMeR | 72 | 95.9 | 39.2 | 28.6 | 52.0 | 39.3 | 29.1 |
| Dyn-HaMR | 280 | 76.9 | 33.3 | 22.4 | 48.0 | 32.5 | 23.5 |
| **ReViV (Ours)** | **0.7** | **35.1** | **33.0** | **13.7** | **20.3** | **25.2** | **9.4** |

HaMeR 대비 100배, Dyn-HaMR 대비 400배 이상 빠르면서 PA-MPJPE·GA-MPJPE에서 SOTA다. 특히 손이 시야에서 완전히 사라지는 구간에서도 baseline이 무너지는 것과 달리, 결합 분포에서 배운 시공간 prior 덕에 생체역학적으로 타당하고 시간적으로 안정된 손 움직임을 만들어낸다.

### 카메라 트래킹 / 시선 추정 / 깊이 추정 (ADT)

| Method | Time (s) ↓ | ATE ↓ | RTE ↓ | RRE ↓ | Gaze MSE ↓ | Abs Rel ↓ | $\delta_{1.25}$ ↑ |
|---|---|---|---|---|---|---|---|
| EgoM2P | 0.7 | 0.030 | 0.009 | 1.290 | 0.0311 | 0.458 | 30.3 |
| EgoMono4D | 14.2 | 0.051 | 0.015 | 1.307 | – | **0.150** | **83.9** |
| VIPE | 25.8 | **0.005** | 0.009 | 1.307 | – | – | – |
| **ReViV (Ours)** | **0.7** | 0.015 | **0.009** | **1.279** | **0.0211** | 0.265 | 56.5 |

- **카메라**: RTE·RRE는 전 방법 중 최저. ATE만 VIPE에 뒤지는데, VIPE는 클립 전체에 dense bundle adjustment를 돌리는 반면 ReViV는 기하 후처리 없이 단일 feed-forward로 예측하기 때문이라고 설명한다.
- **시선**: EgoM2P 대비 MSE가 뚜렷하게 낮다(0.0311 → 0.0211).
- **깊이**: EgoM2P는 크게 앞서지만 EgoMono4D에는 밀린다. 논문은 원인을 (1) EgoMono4D가 UniDepth 사전학습 가중치의 강력한 depth 전용 prior를 물려받는 반면 ReViV는 depth expert 초기화 없이 처음부터 학습했고, (2) Cosmos tokenizer의 이산화 양자화 오차가 미세한 depth 예측을 해친다는 두 가지로 명시한다. 다만 추론은 20배 이상 빠르다.

### 의의
- 1인칭 4D 재구성에서 **사람과 장면을 하나의 결합 분포로 묶은 최초의 통합 생성 프레임워크**. 중간 단계 카메라 트래킹의 오차 누적을 구조적으로 우회한다.
- **task-specific prior(외부 hand tracker, SLAM, depth expert) 없이** 대부분 태스크에서 SOTA에 도달 — 스케일 업된 마스킹 기반 사전학습이 전용 사전지식을 상당 부분 대체할 수 있음을 보였다.
- 클립당 0.7초 수준의 실시간급 추론으로, 최적화·diffusion 기반 파이프라인 대비 2~3자릿수의 속도 이득.
- 코드와 모델을 전면 공개(https://reviv4d.github.io/, https://github.com/lvsean/reviv4d).

## 한계
> 참고: 본문 Conclusion의 "Limitations and Future Directions" 절 원문은 이번 수집에서 확보하지 못했다(arXiv HTML 변환본이 5.6절 ablation 표 도중에 잘림). 아래는 논문 본문에서 저자들이 **명시적으로 인정한** 내용만 정리한 것이다.

- **깊이 정확도가 전용 모델에 못 미친다**: EgoMono4D 대비 Abs Rel 0.265 vs 0.150, $\delta_{1.25}$ 56.5 vs 83.9. 저자들이 밝힌 원인은 depth expert 사전학습 부재와 Cosmos tokenizer의 양자화 오차다. 즉 모든 모달리티를 discrete token으로 통일한 설계가 dense한 픽셀 단위 정밀도에서는 대가를 치른다.
- **전역 카메라 위치 정확도**: ATE에서 dense bundle adjustment를 쓰는 VIPE(0.005)에 뒤진다(0.015). 기하 후처리를 생략한 end-to-end 예측의 구조적 한계다.
- **전역 정렬 신체 자세**: GT 카메라를 받은 UniEgoMotion(GA-MPJPE 105.8)보다 약간 높다(111.5). 전역 ego-motion을 암묵적으로 학습하는 방식이 완벽한 외부 트래킹을 완전히 대체하지는 못한다.
- **metric 스케일의 조건부 의존**: 바닥 평면이 보이지 않는 영상에서는 metric 정렬을 위해 외부 VIPE metric depth를 선택적 앵커로 써야 한다. "외부 prior 불필요"라는 주장이 이 경우엔 완화된다.
- **평가 프로토콜상의 제약**: 사전학습 코퍼스에 ground-truth SMPL(-X) 주석이 없어 baseline을 동일 supervision으로 재학습할 수 없었고, 전신 모션 정량 평가는 ADT 한 데이터셋에만 의존한다.
- 2초 클립 단위 처리, 영상 8 FPS·256×256 다운샘플 설정에서 평가했다. 더 긴 시퀀스나 고해상도로의 확장은 논문에 명시적 언급이 확인되지 않았다.

## 우리 연구와 연결되는 점

**Egocentric Vision**
- ReViV는 EgoM2P(ICCV 2025)의 후속으로, "1인칭 멀티모달 사전학습"이 4B → 7B 토큰으로 스케일업되면서 body/hand kinematics까지 흡수하는 흐름을 보여준다. 1인칭 foundation model을 쓰려는 연구에서 바로 백본 후보가 된다.
- 실질적 매력은 **입력이 RGB 하나뿐**이라는 점이다. Aria/Quest 같은 특수 장비의 SLAM 스트림 없이도 카메라 궤적·깊이·시선·자세를 얻으므로, 일반 웨어러블이나 기존 1인칭 데이터셋(라벨 없는 영상 포함)에 그대로 적용할 수 있다.
- 마스킹 기반 결합 분포 학습이라 **임의의 조건부**를 쓸 수 있다. 논문은 RGB → 나머지 전부를 주 시나리오로 쓰지만, 원리상 일부 모달리티를 관측으로 주고 나머지를 채우는 사용법도 같은 모델로 가능하다(구체적 실험은 본문에서 확인되지 않음).
- Gaze MSE에서 EgoM2P를 앞선 결과는, 시선이 별도 태스크가 아니라 몸·손·장면과 함께 모델링될 때 이득을 본다는 근거로 쓸 수 있다.

**Hand-Object Interaction**
- 손 관절을 **카메라 공간**에 표현해 전역 이동과 조작 동작을 분리한 설계는, HOI 연구에서 "손-물체 상대 기하"를 안정적으로 다루려는 목적과 정확히 맞닿는다.
- 손이 시야를 벗어나거나 심하게 가려지는 구간을 시공간 prior로 메우는 능력은 1인칭 HOI의 고질적 문제(occlusion, out-of-view)에 대한 실용적 해법이다. ARCTIC·TACO·HOT3D·HoloAssist 네 벤치마크 모두에서 PA-MPJPE가 baseline의 절반 이하다.
- 클립당 0.7초 추론은 대규모 1인칭 영상에 손 pseudo-label을 뿌리는 **데이터 엔진**으로 쓰기에 충분히 빠르다. 논문 자신도 Video Depth Anything으로 depth pseudo-label을 만들어 스케일업했으므로, 같은 전략을 HOI 라벨 확장에 적용할 여지가 있다.

**Spatial Audio**
- 논문은 오디오를 전혀 다루지 않는다. 다만 관점상, MGET의 마스킹 목적함수는 모달리티에 무관하게 정의되어 있어(모달리티별 VQ-VAE로 토큰화 → 통합 시퀀스에 concat) **오디오 토큰을 하나 더 붙이는 형태의 확장이 구조적으로 자연스럽다**. 특히 ReViV가 이미 카메라 궤적(= 머리 포즈)과 metric 정렬된 장면 기하를 내놓으므로, binaural/ambisonic 신호의 방향 단서를 정렬할 좌표계가 공짜로 주어진다는 점이 매력적이다. 이는 논문에 근거가 없는 **잠재적 확장 방향**이며, 저자들이 언급한 바 없다.

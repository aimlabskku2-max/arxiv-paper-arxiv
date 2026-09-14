# VidParse: Online Parsing of Egocentric Procedures Like a Pro

**arXiv**: 2608.27562 | **주제 분류**: Egocentric Vision | **출판일**: 2026-08-27 | **학회**: ECCV 2026
**저자/소속**: Anubhav Gupta, Archit Kambhamettu, Vatsal Agarwal, Pulkit Kumar, Abhinav Shrivastava (University of Maryland, College Park)
**링크**: https://arxiv.org/abs/2608.27562

## 한 줄 요약
1인칭 영상을 실시간으로 "지금 몇 번째 조리 단계인가"로 쪼개는 문제를, 학습을 한 번도 하지 않고 frozen foundation model 특징 + 고전 신호처리 경계 검출 + task graph 제약 beam search만으로 푸는 프레임워크다.

## 메인 그림
![DINOv2 기반 유사도 행렬로 경계를 찾고, task graph로 제약된 beam search가 라벨을 붙여 인과적으로 타당한 분할을 만든다](https://arxiv.org/html/2608.27562v1/vidgraph_pk_teaser_v1.png)
Figure 1. (a) frozen DINOv2 특징으로 Temporal Similarity Matrix(TSM, 프레임끼리 얼마나 닮았는지 적어 놓은 행렬)를 만들고 대각선을 따라 checkerboard kernel을 미끄러뜨려 (b) 의미가 바뀌는 지점(peak)을 경계로 잡은 뒤, (c) task graph 제약 beam search로 라벨을 붙여 (d) 매끄럽고 절차적으로 타당한 분할을 얻는 전체 흐름.

---

## 선행 연구

이 논문이 딛고 선 흐름은 크게 세 갈래다.

**1) Temporal Action Segmentation (TAS, 영상을 행동 단위로 시간축에서 자르기)**

- 초기에는 영상 전체를 다 보고 자르는 **offline** 모델이 주류였다. MS-TCN(multi-stage temporal convolutional network), [ASFormer](https://arxiv.org/abs/2110.08568) 같은 모델이 대표적이다. 미래 프레임까지 쓸 수 있으니 애매한 구간을 뒤늦게 정정할 수 있다.
- 실시간 응용(AR 코치, 로봇 보조)에서는 **과거 프레임만 보고** 판단해야 하는 **Online Action Segmentation (OAS)** 이 필요하다. OnlineTAS, MATR(memory-augmented transformer), Mamba-OTR(state-space model 기반) 등이 메모리 뱅크나 sub-quadratic 시퀀스 모델로 온라인 제약을 버텨내려 했다.
- 데이터셋도 3인칭(50 Salads, Breakfast, [Kinetics](https://arxiv.org/abs/1705.06950), Something-Something, COIN, Cross-Task)에서 1인칭(EPIC-Kitchens, Ego4D, CaptainCook4D, EgoPER, HD-EPIC)으로 무게중심이 옮겨갔다.
- 학습 없이 하려는 시도로는 vision-language model을 test time에 적응시키는 T3AL, [FreeZAD](https://arxiv.org/abs/2501.13795) 등이 있다.

**2) 유사도 기반 경계 검출 (Generic Event Boundary Detection, GEBD)**

미리 정한 행동 목록 없이 "장면이 바뀌는 순간"만 찾는 계열이다. 최근에는 인지 모델(ESTimator), 동적 exit 구조(DyBDet), diffusion(DiffGEBD) 등으로 발전했다. 비지도(UBoCo, OTAS)나 약지도(ATBA) 방법도 결국 feature나 decoder를 상당히 최적화해야 한다.

원조 격인 고전 기법은 **self-similarity matrix(SSM) 위의 checkerboard kernel**이다. Foote(2000), Cooper & Foote(2001)가 오디오/영상 장면 경계 검출에 도입했다. 균질한 구간 사이의 전환이 SSM 대각선에서 체커보드 패턴으로 나타난다는 아이디어다.

**3) 문법·구조 기반 절차 파싱**

수 분짜리 절차 영상의 장거리 의존성을 다루려고 구조적 prior를 넣는 계열이다. [VideoGraph](https://arxiv.org/abs/1905.05143)가 latent unit-action들의 soft graph로 긴 활동을 모델링한 초기 작업이고, 이후 activity grammar 유도, progress 추정용 soft task graph(ProTAS 계열), LLM으로 논리를 뽑아 시공간 정렬에 쓰는 [LASER](https://arxiv.org/abs/2304.07647)·PHGC·KML, 일반화 task graph로 오류를 검출하는 GTG2Vid 등이 이어진다.

---

## 문제 제기

1인칭 영상은 특유의 시각적 노이즈가 심하다. 논문이 짚는 원인은 세 가지다.

- **heavy ego-motion(머리가 흔들려 시점 자체가 요동치는 현상)**: 프레임 단위 feature가 행동과 무관하게 확 바뀐다.
- **transient occlusion(손이나 물체가 잠깐씩 가려지는 현상)**: 증거가 순간적으로 사라진다.
- **high intra-class variability(같은 행동인데 사람마다 실행 방식이 크게 다른 현상)**: 대본 없이 수행하는 human-object interaction이라 "커피 내리기"의 모습이 매번 다르다.

그 결과 표준적인 프레임 단위 online 모델은 두 가지 방식으로 무너진다.

- **over-segmentation(하나의 행동을 잘게 토막 내는 현상)**: 경계 근처에서 라벨이 깜빡깜빡 흔들린다.
- **structural collapse(절차 구조 자체가 붕괴)**: 국소 오류가 쌓이면서 "물을 붓기 전에 차를 마신다" 같은 불가능한 순서가 나온다.

게다가 기존 online 방법들은 라벨이 붙은 학습 데이터에 크게 의존한다. 도메인이 바뀌면 다시 학습해야 하고, 주석이나 재학습이 현실적으로 불가능한 현장에서는 배포가 어렵다. 즉 **불안정한 저수준 지각(low-level perception)** 과 **고수준 절차 논리(procedural logic)** 사이가 비어 있다는 게 핵심 지적이다.

---

## 연구 주제

논문은 egocentric 활동 이해를 **"학습된 temporal filter를 쌓는 문제"가 아니라 "절차 제약이 지배하는 structured inference 문제"** 로 다시 정의한다.

핵심 관찰은 간단하다. 일상의 대부분의 작업은 일관된 구조적 의존성을 갖는다. 어떤 행동은 반드시 다른 행동보다 먼저 와야 하고, 어떤 행동은 동시에 일어날 수 없다. **국소 시각 증거가 애매해도 이 의존성을 쓰면 행동 시퀀스를 복원할 수 있다.**

기존 흐름과의 차이는 두 지점이 결정적이다.

| 축 | 기존 연구 | VidParse |
|---|---|---|
| temporal 모델 | 학습된 TCN/Transformer/SSM | 학습 없음, TSM + checkerboard kernel |
| graph 사용 방식 | 학습 중 soft regularizer | 추론 중 **hard constraint** (위반 transition에 $\infty$ 비용) |
| 처리 단위 | frame-level 분류 | segment-level 파싱 |
| 학습 필요성 | downstream 데이터로 학습/파인튜닝 | gradient update 0회 |
| 평가 | frame accuracy, Edit, F1@k | + **N-step transition AUC** (장거리 절차 일관성) |

여기서 "training-free"의 정의도 논문이 명시한다. **downstream 절차 파싱 데이터셋에서 task-specific 학습이나 fine-tuning을 전혀 하지 않는다**는 뜻이며, DINOv2나 hand-object detector 같은 frozen pretrained 부품에만 의존한다는 의미다. (단, action prototype과 task graph는 training split의 주석에서 유도한다 — 즉 gradient 학습이 없다는 뜻이지 라벨을 전혀 안 본다는 뜻은 아니다.)

---

## 연구 방법

### 전체 구조

- **Input**: 스트리밍 1인칭 영상 $\mathcal{V}$ (GTEA는 15 fps, EgoPER는 10 fps로 처리)
- **Output**: 시간순으로 정렬된 action step 시퀀스 (online, causal — 과거 프레임만 사용)
- **학습 목표**: 없음. 대신 **에너지 최소화(structured energy minimization)** 로 추론한다.

문제 정의는 MAP(Maximum A Posteriori) 추론이다. 온라인 boundary detector $\phi_{boundary}$가 스트림을 세그먼트 $\mathcal{S} = \{s_1, \dots, s_N\}$ 으로 나누고, 절차 그래프 $\mathcal{G}$ 아래에서

$$\mathbf{A}^* = \arg\max_{\mathbf{A}} P(\mathbf{A} \mid \mathcal{S}, \mathcal{G})$$

를 푼다. 파이프라인은 네 단계다.

### 1단계 — Manipulation-Anchored Features (MAFs)

**아이디어**: 1인칭 행동을 결정하는 정보는 화면 전체가 아니라 **손이 물체를 만지는 영역**에 있다. 배경을 다 넣으면 ego-motion 노이즈만 늘어난다.

**동작 방식**:
1. frozen [DINOv2](https://arxiv.org/abs/2304.07193) ViT-L/14 마지막 레이어의 patch token을 뽑는다 (Vision Transformer 구조는 [ViT](https://arxiv.org/abs/2010.11929)).
2. frozen Hand-Object Detector(HOD, Shan et al. 2020)로 손과 조작 중인 물체의 bounding box를 검출한다.
3. 검출된 박스들을 모두 감싸는 **minimum spanning box**(enclosing 전략)로 하나의 interaction 영역 $R_t = [p_{x1}, p_{y1}, p_{x2}, p_{y2}]$ 를 만든다.
4. 이 영역과 겹치는 $16 \times 16$ patch token들을 공간 평균해 프레임 표현을 얻는다.

$$\mathbf{f}_t = \frac{1}{|R_t|} \sum_{i=p_{y1}}^{p_{y2}} \sum_{j=p_{x1}}^{p_{x2}} \mathbf{P}_{t,i,j}$$

5. 검출이 하나도 없는 프레임은 **직전 유효 feature를 그대로 이어 쓴다**. 머리 움직임이나 짧은 occlusion이 feature stream에 가짜 변화를 만드는 것을 막는 단순한 temporal smoothing이다.

논문은 이 설계를 "video representation을 task-relevant trajectory에 한정하면 motion과 scene appearance가 분리된다"는 기존 발견(Trokens, Trajectory-aligned space-time tokens)의 **공간판(spatial version)** 이라고 설명한다.

### 2단계 — Training-Free Boundary Detection

학습된 boundary predictor 대신 고전 novelty detection을 쓴다.

**Gaussian-tapered checkerboard kernel**: 기본 체커보드 패턴 $\mathbf{C} = \begin{bmatrix} 1 & -1 \\ -1 & 1\end{bmatrix}$ 을 $L \times L$ 전체 1 행렬 $\mathbf{J}_L$ 과 Kronecker 곱한 뒤, 중앙을 강조하고 가장자리 노이즈를 억누르는 Gaussian 가중치 $\mathbf{G}$ 를 원소곱한다.

$$\mathbf{K} = (\mathbf{C} \otimes \mathbf{J}_L) \odot \mathbf{G}$$

**local novelty**: 최근 $2L$ 개 MAF만 담는 버퍼(= online 보장)로 local self-similarity matrix를 만든다.

$$S_{i,j} = \frac{\mathbf{f}_i^\top \mathbf{f}_j}{\|\mathbf{f}_i\| \|\mathbf{f}_j\|}, \qquad \Delta_t = \sum_{i=1}^{2L}\sum_{j=1}^{2L} S_{i,j} K_{i,j}$$

**boundary emission**: novelty가 국소 최대이면서 saliency threshold $h$ 를 넘으면 경계로 확정한다.

$$\tau = \{t \mid \Delta_t > \Delta_{t \pm k} \ \text{and} \ \Delta_t > h\}$$

over-segmentation을 막기 위해 직전 경계로부터 최소 간격 $d$ 를 강제한다. 경계가 잡히면 버퍼를 $\tau$ 까지 비우고 세그먼트를 추론 단계로 넘긴다.

이 단순한 선형 필터가 통하는 이유를 논문은 명확히 말한다. **DINOv2가 의미적으로 안정적이라서, "썰기" 같은 하나의 행동이 MAF 공간에서 균질한 block으로 나타나기 때문**이다. 예전에는 deep temporal network가 필요했던 일을 선형 필터가 해낸다는 것.

### 3단계 — Prototype-Based Action Matching

세그먼트에 의미 라벨을 붙이는 비모수(non-parametric) 단계다.

- 한 행동의 모든 인스턴스를 평균 내 하나의 global prototype을 만들면 **multi-phasic(여러 하위 국면으로 이뤄진) 행동의 구분이 뭉개진다**. 그래서 두 단계로 쪼갠다.
- 먼저 training example을 **agglomerative clustering**으로 "실행 스타일(execution style)"별로 묶고 centroid를 계산한다.
- 그 다음 각 클러스터 표현을 짧은 시간 창(EgoPER: 4초 구간 / 2초 stride, GTEA: 1.5초 구간 / 0.5초 stride)으로 겹쳐 자른다. 결과가 행동 $a$ 의 **micro-prototype 라이브러리** $\mathcal{P}_a$ 다. temporal warping 없이 국면별 의미를 보존한다.
- 온라인 추론 시, 세그먼트 $s_k$ 에서 HOD 마스크로 유효 interaction이 없는 프레임을 걸러내고 평균 descriptor $\mathbf{g}_k$ 를 계산한 뒤, 최근접 micro-prototype까지의 cosine distance를 매칭 비용으로 쓴다.

$$\phi(s_k, a) = \min_{p \in \mathcal{P}_a}\left(1 - \frac{\mathbf{g}_k^\top p}{\|\mathbf{g}_k\| \|p\|}\right)$$

### 4단계 — Structured Procedural Inference (graph-constrained beam search)

**Task graph 유도**: training 시퀀스의 step 순서 주석을 모아 만든다.
- 인접한 전이를 모두 기록하되 **첫 방문(first-visit)** 과 **재방문(revisit)** 을 구분한다.
- 각 행동의 첫 등장 이전에 관찰된 step들을 prerequisite 후보로 누적한다.
- 그 step 없이도 성립하는 시퀀스가 있으면 **omittable(선택적)** 로 표시한다.
- 최소 prerequisite 집합이 빈 행동은 **start node**로 두고, start node끼리는 전부 연결한다.

(보충자료에 따르면 노드 색으로 start(초록)/end(빨강)/optional(노랑)/필수(회색), 엣지로 first-visit(실선 검정)/revisit(점선 빨강)을 시각화한다.)

**에너지 함수**:

$$\mathbf{A}^* = \arg\min_{\mathbf{A}} \sum_{i=1}^{N} \left[ D_i \cdot \phi(s_i, a_i) + \lambda D_i (1 - \bar{M}_i) \right] + \Psi(\mathbf{A}, \mathcal{G})$$

- $D_i$: 세그먼트 길이 → 긴 세그먼트가 목적함수에 비례해 더 크게 기여
- $\bar{M}_i$: 세그먼트 내 평균 manipulation confidence → **visibility prior**, 즉 interaction 증거가 부실한 세그먼트에 페널티
- $\Psi$: 그래프 제약. 유효하지 않은 전이를 **완전히 잘라낸다**.

$$\Psi(a_{i-1}, a_i) = \begin{cases} 0 & (a_{i-1}, a_i) \in E_{\mathcal{G}} \\ \infty & \text{otherwise} \end{cases}$$

식은 전체 시퀀스로 적었지만 실제 추론은 **fixed-lag commitment**로 온라인 갱신한다. 몇 초보다 오래된 예측은 얼려서 미래 관측이 바꿀 수 없게 하고, 그래서 버퍼가 유한하게 유지된다.

**Low-Visibility Inertia와 배경 처리**: 손이 잠깐 화면을 벗어날 때, 이미 어떤 step을 추적 중이면 decoder가 **관성(inertia)** 을 적용해 작은 상수 비용으로 직전 행동을 연장한다. 반대로 시퀀스가 막 시작됐거나 이미 억제된 배경 상태라면 안전하게 background(BG)로 배정한다.

**Gap rectification**: 배경 세그먼트 뒤에 직전 행동으로 높은 확신으로 복귀하면, decoder가 **소급해서** 그 공백을 그 행동으로 메운다.

$$E_{\text{rectified}} = E_{\text{prev}} - \text{Cost}_{BG} + (D_{\text{gap}} \cdot \bar{\phi}_{a_{i-2}})$$

**Action-conditioned background suppression (보충자료)**: "전자레인지 X초 돌리기"처럼 손이 오래 프레임을 벗어나는 것이 정상인 step에서는 hand-visibility 페널티를 0으로 만들어 BG로 잘못 넘어가는 것을 막는다. 손-물체 상호작용이 다시 또렷해지면 자동 해제된다. 논문은 이 설정을 EgoPER의 "Microwave for X seconds" 행동에만 적용했다고 밝힌다.

**하이퍼파라미터**: checkerboard kernel 폭 $L$ = EgoPER 20프레임 / GTEA 10프레임, 클러스터 수 $k$ = GTEA 3 / EgoPER 9, beam width $B$ = EgoPER 10 / GTEA 5.

---

## 실험 결과 / 연구 의의

### 데이터셋과 평가 지표

- **GTEA**: 7개 주방 활동, 28개 영상. 15 fps로 처리.
- **EgoPER**: 5개 레시피, 정상 213개 + 오류 173개 영상. ProTAS 설정을 따라 **정상 영상만** 평가, 동일 split 사용. 10 fps로 처리.
- 지표: background 프레임 제외한 frame-wise Accuracy, Edit distance, F1@{0.1, 0.25, 0.5}.
- 새 지표 **N-Step Transition Accuracy**: 예측 시퀀스에서 $n$-step 전이를 모두 뽑아 GT와 비교한다. $\mathcal{H}_n(S) = \{(s_i, \dots, s_{i+n})\}$ 의 multiset을 만들고 겹치는 개수로 TP를 센다.
  $$TP_n = \sum_{h \in \mathcal{U}} \min(c(h, S_{\text{pred}}), c(h, S_{\text{gt}}))$$
  precision-recall 곡선의 AUC를 보고한다. 영상의 첫 {10%, 20%, …, 100%}만 파싱하는 **점진적 완성도(progressive completion)** 스윕도 함께 돌려, 증거가 쌓일수록 절차 상태를 일관되게 유지하는지 본다.

### 주 결과 (Table 1)

| Method | Inference | Train-Free | GTEA Acc | GTEA Edit | GTEA F1@0.1 | F1@0.25 | F1@0.5 | EgoPER Acc | EgoPER Edit | EgoPER F1@0.1 | F1@0.25 | F1@0.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MSTCN | Offline | ✗ | 79.35 | 84.46 | 86.54 | 83.79 | 71.86 | 87.52 | 92.34 | 92.60 | 91.81 | 86.12 |
| MSTCN | Online | ✗ | 47.28 | 60.26 | 66.75 | 60.12 | 40.29 | 25.40 | 44.81 | 44.09 | 31.78 | 15.72 |
| ProTAS | Online | ✗ | 73.19 | 71.81 | 72.89 | 68.94 | 54.87 | 76.61 | 65.50 | 64.26 | 62.59 | 51.31 |
| **VidParse (Ours)** | Online | ✓ | **89.1** | **87.4** | **91.9** | **89.9** | **80.5** | **80.7** | **88.7** | **91.1** | **88.5** | **77.6** |

읽는 법:
- MS-TCN을 그대로 online으로 돌리면 붕괴한다 (EgoPER F1@0.5가 86.12 → 15.72). 미래 컨텍스트가 얼마나 컸는지 보여주는 대조군이다.
- VidParse는 **gradient update 0회로 online SoTA**를 찍는다. GTEA에서는 offline MS-TCN마저 모든 지표에서 넘는다.
- 논문 본문 서술: ProTAS 대비 GTEA에서 모든 threshold의 F1을 15% 이상, F1@0.5는 최대 25%까지 개선. EgoPER에서는 F1과 Edit에서 약 25%, frame accuracy에서 4% 개선.

논문은 **자기 방식의 지표 해석 주의점**도 명시한다. frame-level 모델과 달리 segment 단위로 라벨을 커밋하기 때문에, 세그먼트가 GT와 잘 정렬돼도 경계가 조금만 어긋나면 frame accuracy가 손해를 본다. 따라서 이 설정에서는 **Edit와 F1@k가 분할 품질을 더 잘 반영**한다.

### 절차 파싱 일관성 (N-Step Transition, Fig. 4)

EgoPER에서 모든 transition 길이에 대해 ProTAS를 앞서고, **$n$ 이 커질수록 격차가 벌어진다. 5-step과 7-step 전이의 AUC는 baseline의 최대 $5\times$–$10\times$** (초록의 "10x improvement"가 이 수치다). 메시지가 분명하다. frame-level baseline은 국소 오류가 쌓여 장거리 전이를 깨뜨리고 절차 제약을 위반하지만, VidParse는 **행동을 따로따로 인식하는 게 아니라 기저 task graph를 재구성**한다.

### 경계 검출 거동

- 방출된 세그먼트 길이 분포: 약 **75%가 2–4초 구간**, **90% 이상이 5초 미만**. 온라인성(짧은 지연)을 보여준다.
- 경계 recall: kernel = 10에서 **90% 이상의 경우 2초 이내에 경계를 회수**한다 → 서로 다른 행동을 한 세그먼트에 뒤섞지 않는다는 근거.

| Boundary 방법 (EgoPER) | Acc | Edit | F1 |
|---|---|---|---|
| Adjacent Frame Similarity | 75.7 | 83.4 | 68.0 |
| Z-score | 78.5 | 85.1 | 69.9 |
| ABD | 78.5 | 88.1 | 72.2 |
| **Ours (checkerboard TSM)** | **80.7** | **88.7** | **77.6** |

### Ablation — Feature (Table 2, EgoPER Overall)

| Method | Feature | Train-Free | Acc | Edit | F1 |
|---|---|---|---|---|---|
| ProTAS | I3D | ✗ | 76.61 | 65.50 | 51.31 |
| ProTAS | DINO CLS | ✗ | 81.31 | 72.63 | 64.44 |
| ProTAS | DINO MAFs | ✗ | 83.31 | 70.87 | 67.26 |
| Ours | DINO CLS | ✓ | 69.09 | 82.68 | 61.42 |
| **Ours** | **DINO MAFs** | ✓ | **80.69** | **88.69** | **77.61** |

- MAF는 **다른 방법(ProTAS)에 꽂아 넣어도** 성능을 올린다 → feature 자체가 좋다.
- 같은 MAF 위에서 VidParse의 추론이 F1을 67.26 → 77.61로 더 끌어올린다 → 구조적 디코딩의 기여가 별개로 존재한다.
- 전체 프레임(DINO CLS)은 MAF보다 못하다 → **foreground를 명시적으로 집는 것이 필요**하다는 증거.

### Ablation — EgoVLPv2 비교 (Table 3 Right, EgoPER)

| Method | MAF | Clip-level | Acc | Edit | F1 |
|---|---|---|---|---|---|
| EgoVLPv2 | ✗ | ✗ | 78.1 | 89.4 | 73.0 |
| EgoVLPv2 | ✓ | ✗ | 80.3 | 91.5 | 77.5 |
| EgoVLPv2 | ✗ | ✓ | 53.4 | 62.8 | 43.7 |
| EgoVLPv2 | ✓ | ✓ | 60.1 | 70.6 | 52.1 |
| Ours (DINOv2) | ✗ | ✗ | 69.1 | 82.7 | 61.4 |
| **Ours (DINOv2)** | **✓** | ✗ | **80.7** | **88.7** | **77.6** |

egocentric video-language backbone인 EgoVLPv2의 frame-level feature는 DINOv2 MAF와 거의 대등하지만, **clip-level feature는 크게 떨어진다**. 시간적으로 뭉뚱그린 표현은 짧은 절차 전환을 놓친다는 뜻이다. 그리고 어느 backbone을 쓰든 **MAF 마스킹은 일관되게 이득**이다.

### Ablation — Prototype 방식 / 민감도 (Table 4, EgoPER)

| Prototype 방식 | Acc | Edit | F1 |
|---|---|---|---|
| Global mean | 78.5 | 88.8 | 74.5 |
| Medoids | 80.1 | 87.0 | 75.0 |
| **Centroids (Ours)** | **80.7** | **88.7** | **77.6** |

global mean은 feature 공간을 뭉개고, medoid는 실제 관찰된 인스턴스로만 한정된다. centroid가 둘 사이 균형을 잡는다.

| 최소 간격 $d$ | Acc | Edit | F1 |
|---|---|---|---|
| 10 | 81.0 | 84.1 | 73.5 |
| 15 | 81.7 | 87.9 | 75.7 |
| **20** | 80.7 | **88.7** | **77.6** |
| 25 | 78.1 | 87.7 | 72.8 |
| 30 | 76.1 | 87.7 | 71.3 |

$d$ 가 작으면 경계가 촘촘해져 살짝 over-segment하고, 크면 간격이 경직돼 빠른 전환을 놓친다.

prototype 개수 $p$ 는 3→11로 바꿔도 Accuracy·Edit 변동이 **1.2% 미만**이라, 클러스터링 기반 매칭이 견고하다.

### 추론 속도 (Table 3 Left, EgoPER, 영상당 평균 초)

| Method | HOD | Backbone | Method 단계 | Total | FPS | Acc | Edit | F1@0.5 |
|---|---|---|---|---|---|---|---|---|
| ProTAS | - | 79.5 | 706 | 785.5 | 4.5 | 76.6 | 65.5 | 51.3 |
| Ours ($B=1$) | 339 | 36.8 | 24.8 | 400.6 | 8.7 | 58.5 | 77.5 | 52.1 |
| Ours ($B=3$) | 339 | 36.8 | 28.2 | 404.0 | 8.7 | 76.3 | 86.0 | 72.4 |
| Ours ($B=5$) | 339 | 36.8 | 28.4 | 404.2 | 8.6 | 78.5 | 86.9 | 74.5 |
| **Ours ($B=10$)** | 339 | 36.8 | 32.8 | 408.6 | 8.6 | **80.7** | **88.7** | **77.6** |

MAF 추출에 HOD 비용(339초)이 붙는데도 전체는 **8.6 FPS로 ProTAS(4.5 FPS)보다 빠르다**. 더 인상적인 건 파싱·디코딩 단계인데, VidParse는 **AMD EPYC 7443 CPU에서 32.8초**면 끝나는 반면 ProTAS는 **NVIDIA RTX A4000 GPU에서 706초**가 필요하다. beam width로 속도-정확도를 매끄럽게 조절할 수 있다.

### 보충 실험 — 레시피별 task graph (GTEA)

보충자료는 더 엄격한 설정을 본다. 일반화된 action graph(동사만 모음: take, pour, place)가 아니라 **레시피별 task graph**, 즉 행동과 조작 대상 물체를 묶은("take bread" vs "take cup") 정밀한 순차 제약을 강제한다.

| Method | Feature | Overall Acc | Overall Edit | Overall F1 |
|---|---|---|---|---|
| ProTAS | I3D* | 46.11 | 46.60 | 21.63 |
| ProTAS | DINO CLS* | 41.82 | 45.89 | 19.75 |
| ProTAS | DINO MAFs* | 44.89 | 44.54 | 21.30 |
| Ours | DINO CLS* | 56.55 | 79.29 | 46.33 |
| **Ours** | **DINO MAFs\*** | **89.11** | **87.39** | **80.47** |

(* = 레시피별 task-graph 설정)

**ProTAS는 좋은 MAF feature를 줘도 F1 21.30에서 정체**하는 반면, 같은 feature로 VidParse는 **80.47**을 낸다. "Cheese" 레시피에서는 Acc 94.85 / Edit 100.00 / F1 100.00으로 거의 완벽한 구조 파싱을 달성한다. 강한 feature만으로는 부족하고, **hard constraint 기반 구조적 디코딩이 정밀한 절차 이해의 핵심**이라는 게 이 표의 메시지다.

### 연구 의의

1. **"학습 없이도 된다"의 실증**: frozen foundation model의 의미적 안정성이 충분히 좋으면, 2000년대 초 신호처리 기법(checkerboard kernel on SSM)이 deep temporal network를 대체할 수 있다. 학습 파이프라인 전체를 없애도 online SoTA가 가능하다.
2. **구조를 soft가 아닌 hard로**: 대부분의 선행 연구는 graph를 학습 중 regularizer로 썼다. 이 논문은 추론 시 $\infty$ 비용의 경직된 제약으로 쓰고, 그것이 local predictor 특유의 structural collapse를 막는 결정적 장치임을 보인다.
3. **평가 축의 확장**: frame accuracy와 F1@k만으로는 "장거리 절차 일관성"을 측정할 수 없다. N-step transition AUC는 이 공백을 겨냥한 지표이며, 여기서 격차가 가장 크게 벌어진다.
4. **배포 친화성**: CPU에서 디코딩이 끝나고 도메인별 재학습이 필요 없어, 주석 예산이 없는 현장에 바로 얹을 수 있다.

---

## 한계

논문이 본문(Sec. 6)과 보충자료(Sec. 6)에서 직접 밝힌 것들:

- **초저지연(ultra-low-latency) 응용에는 부적합**. global context는 필요 없지만 segment 단위로 처리하므로, 경계가 잡힐 때까지 라벨 확정이 지연된다. (측정치로 보면 세그먼트의 약 75%가 2–4초)
- **out-of-distribution 실행 순서에서 복구 불가**. task graph를 training 시퀀스에서 유도하고 위반 전이에 $\infty$ 비용을 주므로, 사용자가 **실제로는 유효하지만 학습에서 본 적 없는 새로운 순서**로 수행하면 decoder가 정답 경로를 잘라내고 알려진 그래프에 억지로 정렬시킨다. hard constraint의 장점이 곧 약점이다.
- **HOD 의존성**. 심한 occlusion, motion blur, 혹은 손을 쓰지 않는 행동(예: "전자레인지 사용")에서 hand-object detector가 틀리거나 늦는다. gap rectification과 inertia가 일시적 occlusion은 메우지만, **장기간 가려짐이나 순수 비수작업 행동**에서는 시각 증거가 무너져 엉뚱한 예측을 내거나 마지막 유효 feature에 과하게 기댄다.
- **exocentric(3인칭)으로의 확장은 조건부**. manipulation cue가 보이면 적용 가능하지만, 약하거나 없으면 성능이 떨어질 것으로 논문 스스로 예상한다.
- **task graph 자체는 주석 기반**. gradient 학습은 없지만 training split의 step 순서 주석이 그래프와 prototype 양쪽에 필요하다. 완전한 zero-shot은 아니다.
- **future work**: 확률적(probabilistic) 그래프로 open-world와 느슨하게 구조화된 작업을 다루는 방향.

---

## 우리 연구와 연결되는 점

### Egocentric Vision

- **online / causal 제약이 얼마나 비싼지**를 정량적으로 보여주는 좋은 레퍼런스다. MS-TCN이 EgoPER F1@0.5에서 offline 86.12 → online 15.72로 무너지는 수치는, 1인칭 실시간 시스템을 설계할 때 "미래 컨텍스트 없음"의 대가를 잡아주는 기준선이 된다.
- **frozen foundation model로 얼마나 멀리 갈 수 있나**에 대한 강력한 baseline. 새 egocentric 태스크를 시작할 때 학습 파이프라인을 짜기 전에 "DINOv2 patch token + 고전 novelty detection"을 먼저 돌려보는 것이 저비용 상한 추정이 된다. 특히 clip-level feature가 frame-level보다 크게 나쁘다는 ablation은 backbone 선택 시 바로 쓸 수 있는 교훈이다.
- **N-step transition AUC**는 그대로 차용할 만한 지표다. 절차·시퀀스가 중요한 egocentric 태스크(조리, 조립, 수술, 정비)에서 프레임 지표만 보면 "구조가 무너졌는데 숫자는 괜찮은" 상황을 놓친다.
- EgoPER, GTEA, CaptainCook4D, HD-EPIC 같은 절차 벤치마크 지형도를 Related Work가 잘 정리해 두어, 데이터셋 선택 시 참고하기 좋다.

### Hand-Object Interaction

- 이 논문의 **핵심 기여 자체가 HOI를 표현 학습의 앵커로 쓴 것**이다. MAF는 "손+조작 물체 박스로 patch token을 마스킹해 평균"이라는 극도로 단순한 연산인데, 전체 프레임 feature를 일관되게 이긴다. HOI를 명시적 spatial prior로 쓰는 아이디어의 저비용 검증판으로 읽을 수 있다.
- **HOI 검출기의 신뢰도를 downstream 추론의 신호로 재활용**하는 방식이 흥미롭다. 평균 manipulation confidence $\bar{M}_i$ 를 에너지 함수의 visibility prior로 쓰고, 검출 실패 시 inertia로 직전 행동을 연장하며, gap rectification으로 소급 수정한다. HOI detection의 불확실성을 버리지 않고 상위 추론에 넘기는 설계는 우리 파이프라인에도 옮길 수 있다.
- 다만 논문이 인정하듯 **HOD가 곧 병목**이다. 장기 occlusion과 비수작업 행동에서 무너진다. 더 강건한 hand-object contact 추정(3D hand pose, contact field, 양손 상호작용)을 MAF 자리에 끼워 넣으면 그대로 개선 여지가 된다.
- micro-prototype 설계(행동을 실행 스타일별로 클러스터링 → 짧은 창으로 슬라이스)는 **하나의 HOI 행동이 여러 하위 국면으로 이뤄진다**는 관찰의 실용적 구현이다. HOI 인식에서 클래스당 단일 prototype이 왜 부족한지에 대한 구체적 근거가 된다.

### Spatial Audio

- 이 논문은 순수 비전이며 오디오를 전혀 쓰지 않는다. 그런데 **한계 지점들이 오디오가 가장 잘 메우는 지점과 정확히 겹친다**는 점이 흥미롭다.
  - 손이 프레임을 벗어나거나 가려지는 구간: 소리는 계속 난다. 끓는 소리, 자르는 소리, 전자레인지 동작음.
  - "Microwave for X seconds"처럼 손이 없는 step을 위해 논문은 별도 수작업 억제 규칙을 만들어야 했다. 오디오가 있으면 이 규칙 없이 자연스럽게 해결될 가능성이 크다.
  - Spatial audio라면 소리가 나는 방향까지 알 수 있어, 시야 밖(off-screen)에서 진행 중인 step을 추적하는 데 직접 쓰인다.
- 방법론적으로도 이식이 쉽다. **TSM + checkerboard kernel은 원래 오디오 novelty detection에서 나온 기법**(Foote 2000)이다. 즉 audio feature stream에 똑같이 적용해 audio-side boundary를 뽑고, 두 modality의 novelty 신호를 합쳐 경계를 확정하는 확장이 자연스럽다.
- 에너지 함수 $\sum_i [D_i \phi(s_i, a_i) + \lambda D_i (1 - \bar{M}_i)] + \Psi$ 는 modality를 추가하기 쉬운 형태다. audio matching cost 항이나 audio-based visibility 항을 더하면 되고, graph 제약 $\Psi$ 는 그대로 유지된다. **training-free 상태를 유지한 채 multimodal로 확장**할 수 있다는 것이 실용적 매력이다.

### 즉시 실험해 볼 만한 것

- MAF 마스킹만 떼어내 우리 기존 egocentric 파이프라인의 feature 앞단에 붙여 보기 (논문의 Table 2가 보여주듯 ProTAS 같은 남의 방법에도 이득을 준다).
- N-step transition AUC를 기존 실험에 추가해, frame 지표로는 안 보이던 구조 붕괴가 있는지 점검.
- task graph를 hard constraint로 쓰는 beam search를 우리 online 디코더에 얹어, over-segmentation이 줄어드는지 확인.
- 프로젝트 페이지: https://learn2phoenix.github.io/VidParse (코드와 인터랙티브 정성 결과 제공)

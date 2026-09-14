# AdaDexGrasp: Adaptive Dexterous Grasping via 3D Visuo-Tactile Representation Fusion

**arXiv**: 2608.07600 | **주제 분류**: Hand-Object Interaction | **출판일**: 2026-08-06 | **학회**: ECCV 2026 (Accepted)
**저자/소속**: Xirui Liang, Jiaqi Liang\*, Jingkai Xu\*, Yuran Wang\* (Peking University), Ruochong Li (HKUST), Yuanpei Chen (Peking University), Masayoshi Tomizuka, Wei Zhan, Ruihai Wu† (UC Berkeley) — \*공동 1저자, †교신저자
**링크**: https://arxiv.org/abs/2608.07600

## 한 줄 요약
손가락·손바닥 ID를 촉각 신호에 묶어 물체 point cloud에 직접 새겨 넣는 visuo-tactile 표현을 만들고, 이를 써서 초기 grasp 생성 → 성공 여부 판정 → 실패 시 자세 보정까지 한 루프로 돌리는 dexterous grasping 프레임워크다.

## 메인 그림
![초기 grasp가 불안정하면 촉각 융합 표현으로 자세를 다시 잡는다](https://arxiv.org/html/2608.07600v1/Teaser.png)
Figure 1: (왼쪽) 손가락/손바닥 identity가 붙은 contact map을 point cloud에서 예측해 초기 손 자세를 만들고, (오른쪽 위) 그 자세가 접촉이 성기거나 불안정해 실패할 수 있으며, (오른쪽 아래) visuo-tactile 융합 표현으로 자세를 보정해 더 촘촘하고 안정적인 접촉을 만든다.

## 선행 연구
로봇 grasping 연구는 크게 세 갈래다. 강화학습(RL)은 시행착오로 조작 기술을 얻고, 모방학습(IL)은 사람 시연을 로봇으로 옮기며, object-centric 방식은 로봇의 proprioception(관절 위치 등 자기 상태 감각)과 RGB-D 관측으로 시각 기반 grasp 정책을 배운다. 대표적으로 UniDexGrasp++, DexGraspAnything, DexDiffuser, ContactDexNet, DexGraspVLA 같은 방법들이 있다.

visuo-tactile(시각-촉각) 융합 쪽은 다시 두 부류로 나뉜다.

- **학습 기반 융합**: 각 모달리티를 latent 표현으로 인코딩한 뒤 concat하거나 사전학습으로 정렬한다. 전역(global) feature 정렬에 집중한다.
- **원신호 기반 융합**: 시각과 촉각 신호를 신호 수준에서 바로 합친다.

일부 연구는 dexterous grasping에서 visuo-tactile 일반화를 시도했지만, 대부분 feature-level fusion에 머물렀다.

## 문제 제기
저자들이 지적하는 빈틈은 세 가지다.

1. **접촉 이후 적응이 없다.** 기존 grasping 방법 대부분은 RGB나 point cloud 같은 시각 입력만으로 초기 관측 시점에 손 자세를 정하고 끝낸다. 손이 물체에 닿은 뒤 미끄러짐(slipping)이나 구름(rolling)이 생겨도 이를 감지·수정할 수단이 없다. 시각 기하만 보면 멀쩡해 보이는 자세도 실제로는 실패하는 이유다.
2. **촉각만 쓰는 방법은 비효율적이다.** occlusion(물체가 카메라에 가려지는 현상) 상황에서 촉각만으로 적응적 grasping을 시도한 연구들이 있으나, 여러 번 더듬어 봐야 하고 이미 갖고 있는 시각 정보를 못 쓴다.
3. **feature-level 융합은 공간 정렬을 놓친다.** 시각과 촉각을 각자 인코딩해 붙이는 방식은 "어느 손가락이 물체의 어느 지점에 닿았는가"라는 **공간적 대응(spatial alignment)** 을 표현하지 못한다. 정밀하고 적응적인 grasp 제어에는 이 대응이 결정적인데도 그렇다.

덧붙여, 촉각 센서가 달린 dexterous hand용 시뮬레이션 환경이 마땅치 않아 연구 자체가 막혀 있었다는 점도 문제로 든다.

## 연구 주제
**촉각 센서가 달린 다지 손(dexterous hand)으로 안정적이고 적응적인 grasping을 학습하는 문제**를 다룬다.

형식적으로는, 물체 point cloud $\mathcal{P}_{obj}=\{(x_i,y_i,z_i,r_i,g_i,b_i)\}_{i=1}^{N_0}$ (RGB-D 카메라로 취득)와 촉각 신호 $\tau=\{\tau_i\}_{i=1}^{N_t}$ 가 주어졌을 때, grasp 성공 확률을 최대화하는 손 상태 $s^*$ 를 찾는 것이다.

$$s^{*}=\arg\max_{s}\; p(y=1 \mid \mathcal{P}_{obj},\tau,s)$$

여기서 손 상태는 $s=[p,q,\mathbf{j}]$ 로, $p\in\mathbb{R}^{3}$ 는 손바닥 위치, $q\in\mathbb{R}^{4}$ 는 손바닥 방향(쿼터니언), $\mathbf{j}\in\mathbb{R}^{22}$ 는 22개 구동 관절의 각도다. $y\in\{0,1\}$ 은 grasp 성공 여부, $N_t$ 는 촉각 센서 개수로 이 논문 설정에서는 6개(손가락 끝 5개 + 손바닥 1개)다.

핵심 난제는 **visuo-tactile 관측과 grasp 안정성 사이의 관계를 어떻게 모델링하느냐**다.

## 연구 방법

### 전체 구조 — 세 모듈 + 폐루프
프레임워크는 세 모듈로 구성되고, 이들이 반복 루프로 엮인다.

| 모듈 | 역할 | 핵심 입력 |
|---|---|---|
| Contact-Driven Grasp Pose Generator | 초기 grasp 자세 생성 | 물체 point cloud |
| Grasp Pose Classifier | grasp 성공 가능성 예측 | 촉각이 새겨진 point cloud + 손 자세 |
| Grasp Pose Adaptation Model | 실패로 판정된 자세를 보정 | 실패 상태의 visuo-tactile 표현 |

Figure 3의 설명에 따르면 초록색 블록(생성)은 PointNet++로 물체 point cloud를 처리해 visuo-tactile contact map과 초기 자세를 뽑고, 노란색 블록(분류)은 손과 visuo-tactile point cloud를 각각 인코딩하는 dual-encoder PointNet++ 뒤에 multi-head attention을 붙여 성공을 예측하며, 파란색 블록(적응)은 diffusion 기반 모듈로 자세를 반복 보정한다.

### 1) 의미가 담긴 contact map으로 초기 자세 만들기
기존 contact map은 "여기가 닿는다/안 닿는다"만 표시했다. 이 논문은 여기에 **손가락/손바닥 identity**를 붙인다. 모델 $h_\psi$ 가 물체의 각 점마다 6개 중 하나의 라벨을 예측한다.

$$\mathcal{M}=\{\mathcal{M}_i \mid \mathcal{M}_i \in \{1,2,3,4,5,6\},\ i=1,\dots,N_0\}=h_{\psi_1}(\mathcal{P}_{obj})$$

즉 "이 점은 엄지가 닿을 자리, 저 점은 손바닥이 받칠 자리"까지 담는 semantic contact map이다. 이걸 물체 point cloud feature에 합쳐 초기 자세를 디코딩한다.

$$s^{(0)}=h'_{\psi_2}(\mathcal{P}_{obj},\mathcal{M})$$

contact map은 cross-entropy $\mathcal{L}_{CE}(\mathcal{M},\mathcal{M}_s)=-\sum_i M_{s,i}\log M_i$ 로, 자세는 MSE $\mathcal{L}_{MSE}=\|s^{(0)}-s^{s}\|_2^2$ 로 학습한다. 이 단계에서는 아직 접촉이 없으므로 촉각 입력은 쓰지 않는다.

### 2) 촉각을 point cloud에 새겨 넣기 (tactile-mapped point cloud)
초기 자세 $s_0$ 를 실행한 뒤, 다섯 손가락 끝과 손바닥의 접촉력을 읽어 물체 point cloud에 주석을 단다. 각 접촉 영역에 어느 손 부위가 닿았는지 나타내는 고유 ID를 부여해 $\mathcal{P}_{vt}$ 를 만든다.

$$\mathcal{P}_{vt}=\{(x_i,y_i,z_i,r_i,g_i,b_i,k_i,\mathbf{c}_i)\mid i=1,\dots,N\}$$

$k_i\in\mathbb{R}$ 은 손-물체 접촉 상태, $\mathbf{c}_i\in[0,1]^6$ 은 다섯 손가락 끝과 손바닥에 대응하는 6차원 촉각 세기 벡터다.

논문은 $\mathcal{M}$ 과 $\mathcal{P}_{vt}$ 의 차이를 분명히 구분한다. $\mathcal{M}$ 은 실행 **전에** 물체 point cloud만 보고 **예측한** 사전분포이고, $\mathcal{P}_{vt}$ 는 접촉 **후에** 실제로 **측정한** 촉각 신호를 붙인 것이다. 앞의 것은 계획을 이끌고, 뒤의 것은 판정과 보정에 쓰인다.

### 3) 성공 판정
$\hat{y}=f_\theta(\mathcal{P}_{vt},s)$ 로 성공 확률을 예측한다. PointNet 계열 네트워크이며 binary cross-entropy $\mathcal{L}_{cls}=-[y\log\hat{y}+(1-y)\log(1-\hat{y})]$ 로 학습한다.

### 4) 실패 자세 보정
보정 모델 $g_\phi$ 는 실패 상태에서 수정량을 낸다.

$$\Delta s=g_\phi(\mathcal{P}_{vt}^{f},s^{f}),\qquad s^{f,\mathrm{new}}=s^{f}+\Delta s$$

학습 데이터는 (실패, 성공) 쌍으로 만든다. 물체마다 PPO rollout에서 **들어올리기 직전** 시점의 성공/실패 상태를 모아 같은 상호작용 단계로 맞추고, 물체 중심 좌표계로 옮겨 물체의 절대 배치 의존성을 없앤 뒤, 각 실패 상태를 가장 가까운 성공 상태와 짝짓는다. 거리는 다음과 같이 정의한다.

$$d(s,s')=10\sqrt{\|p-p'\|_2^2+\theta_{q,q'}^2}+\|\mathbf{j}-\mathbf{j}'\|_2$$

$\theta_{q,q'}$ 는 두 방향 사이의 geodesic 거리다. 손실은 "성공 자세에 가까워질 것 + 분류기가 매기는 성공 확률을 높일 것" 두 항을 합친다.

$$\mathcal{L}_{gen}=\|\Delta s-(s^{s}-s^{f})\|_2^2+\lambda\big(1-f_\theta(\mathcal{P}_{vt}^{f},s^{f}+\Delta s)\big)$$

### 5) 폐루프 최적화
초기 자세 $s_0$ 에서 시작해 매 스텝 $\hat{y}_k=f_\theta(\mathcal{P}_{vt}^{k},s^{(k)})$ 를 평가하고,

$$s_{k+1}=\begin{cases}s_k, & \hat{y}_k>\tau_{succ}\\ s_k+g_\phi(\mathcal{P}_k,s_k), & \text{그 외}\end{cases}$$

로 갱신하며, $\hat{y}_k>\tau_{succ}$ 이거나 최대 반복 $K$ 에 도달하면 멈춘다.

### 6) 학습 데이터 수집
UniDexGrasp의 1단계 PPO 설정을 따라 IsaacGym에서 데이터를 모은다. 같은 물체에 대해 다양한 grasp 자세를 만들면서도 최소한의 보정으로 안정적인 grasp을 유지하도록 하는 전략이다. 성공과 실패를 모두 수집해 촉각 데이터의 다양성을 확보한다. 손가락에 걸리는 힘이 임계값(실험에서 0.01N)을 넘으면 그 손가락을 active로 표시하고, 감지된 접촉마다 근처 물체 점들을 골라 해당 라벨을 붙인다.

## 실험 결과 / 연구 의의

### 실험 세팅
- **시뮬레이터**: IsaacGym. 작업은 reaching → grasping → lifting 3단계.
- **손**: ShadowHand 기반. 5지 22 DoF, 공간 이동용 6 DoF root pose를 포함하면 총 28 DoF.
- **물체**: UniDexGrasp++에서 6개 카테고리 50개 물체. 20개는 학습, 30개는 unseen-category 테스트.
- **성공 기준(시뮬)**: 들어올린 뒤 최소 1초 동안 미끄러짐 없이 유지.
- **평가 축**: Seen Objects / Unseen Objects(같은 카테고리, 학습에 없던 물체) / Unseen Categories.

### 베이스라인 비교 (Table 1, grasp 성공률)

| Method | Seen Objects | Unseen Objects | Unseen Categories |
|---|---|---|---|
| UniDexGrasp++ | 55% | 49% | 42% |
| DexGraspAnything | 77% | 72% | 67% |
| DexDiffuser | 71% | 69% | 55% |
| UniDexGrasp (PPO) | 52% | 46% | 40% |
| Robot Synesthesia | 33% | 29% | 22% |
| Intuitive Closed-Loop | 76% | 71% | 65% |
| ContactDexNet | 72% | 68% | 63% |
| DexGraspVLA | 69% | 60% | 58% |
| UniDexGrasp-CL | 59% | 52% | 46% |
| DexDiffuser-VT | 75% | 71% | 57% |
| **Ours** | **91%** | **82%** | **83%** |

세 축 모두에서 앞서고, 특히 unseen category에서 격차가 가장 크게 벌어진다(2위 DexGraspAnything 67% 대비 83%). 저자들은 베이스라인 실패 원인을 넷으로 정리한다. (1) 생성형 방법은 시각 기하만 보고 중간 semantic 대응이 없어 복잡한 물체에 실행 불가능한 자세를 낸다. (2) RGB를 행동으로 직접 매핑하는 end-to-end 모델은 기하 구조 이해가 부정확하다. (3) offline contact 모델링은 정적 예측만 주므로 실제 접촉 상태를 못 보고 2차 폐루프 조정을 못 한다. (4) 보정 단계에서, 순수 RL은 고차원 탐색 노이즈에 시달리고, distillation 모델은 국소 기하 변화에 취약하며, Intuitive Closed-Loop는 기하 인식 없이 무작정 손가락을 조인다. resampling 기반(UniDexGrasp-CL)은 같은 생성 분포 안에 갇혀 실패 모드를 못 벗어나고, DexDiffuser-VT는 Basis Point Set 인코딩이 전역 feature만 잡고 촉각이 의존하는 국소 point cloud 구조를 망가뜨려 융합이 약하다.

규모를 키워도 이득이 유지된다. DexGrasp Anything 데이터셋(15k개 이상 물체)에서도 87%를 달성했다.

### Ablation (Table 2)

| Method | Seen Objects | Unseen Objects | Unseen Categories |
|---|---|---|---|
| w/o contact id in adaptation | 84% | 72% | 73% |
| w/o contact id in generation | 79% | 75% | 69% |
| w/o adaptation | 81% | 78% | 59% |
| Object-only | 72% | 67% | 61% |
| Full Point Cloud w/o tactile | 78% | 74% | 67% |
| w/o PC (이미지에 촉각 라벨) | 74% | 71% | 64% |
| **Ours** | **91%** | **82%** | **83%** |

- **contact ID의 의미 정보**는 초기 생성과 이후 보정 양쪽에서 모두 필수다.
- **adaptation 모듈**의 기여가 가장 극적이다. unseen object는 78% → 82%, unseen category는 **59% → 83%** 로 뛴다. 처음 보는 카테고리일수록 초기 자세가 틀리기 쉬우니, 접촉 후 고쳐 잡는 능력이 일반화를 좌우한다는 뜻이다.
- 손 point cloud가 없으면 손-물체 관계를 모델링할 수 없고(Object-only 72/67/61), 촉각이 없으면 보정이 어려워진다(78/74/67).
- point cloud 대신 촉각 라벨이 붙은 이미지를 쓰면 물체의 기하 구조를 충분히 이해하지 못한다(74/71/64).

### 실제 로봇 실험 (Table 3)
고해상도 촉각 센서가 달린 Psibot 로봇 손으로, 기하·재질이 서로 다른 20개 이상 물체에 대해 평가했다. 성공 기준은 들어올린 뒤 3초 이상 안정적으로 유지.

| Method | Seen Objects | Unseen Objects | Unseen Categories |
|---|---|---|---|
| DexGraspAnything | 81% | 71% | 73% |
| DexDiffuser | 77% | 65% | 52% |
| DexGraspVLA | 64% | 57% | 55% |
| **Ours** | **90%** | **87%** | **81%** |

### 표현 선택에 대한 분석
저자들은 힘의 방향이나 전단력(shear force) 같은 더 촘촘한 촉각 모달리티도 시도했지만, 표현이 조밀해질수록 필요한 데이터가 훨씬 많아졌다고 보고한다. 소규모 데이터 실험에서 이 논문의 표현은 88%, 조밀한 모달리티는 81%였다. 또한 풍부한 모달리티는 실제 하드웨어 요구가 크고 촉각 표현의 sim-to-real gap도 커서, 시뮬레이션과 현실의 설정을 맞추기 어렵다고 밝힌다.

### 의의
핵심 메시지는 **"시각과 촉각을 latent에서 붙이지 말고 3D 공간에서 정렬하라"** 는 것이다. 촉각 신호를 손가락 identity와 묶어 물체 point cloud 위에 직접 새기면, 계획 단계에서는 "어느 손가락이 어디에 닿아야 하는가"를 예측할 수 있고 실행 단계에서는 "실제로 어디에 닿았는가"를 같은 좌표계에서 읽을 수 있다. 이 표현의 통일 덕에 생성·판정·보정을 하나의 폐루프로 묶을 수 있었고, 그 결과가 unseen category에서의 큰 성능 격차로 나타났다.

## 한계
- **촉각 표현이 의도적으로 단순하다.** 6차원 접촉 세기와 접촉 상태만 쓰고, 힘의 방향이나 전단력은 배제했다. 저자들 스스로 데이터 요구량과 sim-to-real gap 때문에 내린 절충이라고 설명한다. 미끄러짐 방향 판별이나 정밀 조작으로 확장하려면 이 부분이 발목을 잡을 수 있다.
- **평가 규모가 작다.** 시뮬레이션은 6개 카테고리 50개 물체(학습 20 / 테스트 30), 실제 실험은 20개 이상 물체 수준이다. 대규모 검증은 DexGrasp Anything 데이터셋에서 87%라는 단일 수치로만 보고된다.
- **grasping 자체에 국한된다.** 들어올려 유지하는 데까지가 대상이고, 잡은 뒤의 조작(in-hand manipulation)이나 물체를 사용하는 단계는 다루지 않는다.
- **성공 판정 임계값 $\tau_{succ}$ 와 최대 반복 $K$ 의 구체적 값**은 본문에서 확인하지 못했다(부록 "Training and Inference Details"에 있을 가능성이 있으나 본 정리에서는 확인하지 못함).
- **보정 반복의 실시간성**에 대해서는 별도 부록(Real-Time Feasibility)이 있으나 구체 수치는 이 정리에서 확인하지 못했다.
- 접촉력 임계값 0.01N 같은 하이퍼파라미터가 시뮬레이션 기준으로 정해져 있어, 실제 센서 특성이 다른 하드웨어로 옮길 때의 민감도는 논문에 명시적 언급 없음.

> 주: 본 정리는 arXiv HTML 전문 중 Section 4.5까지(Abstract, Introduction, Related Work, Method 전체, Experiments 4.1–4.5 및 Table 1–3)를 근거로 작성했다. Section 4.6(Deep Analysis in Tactile Signals), Section 5(Conclusion), References, Supplementary는 페이지 로드가 중간에 잘려 확인하지 못했다.

## 우리 연구와 연결되는 점

### Hand-Object Interaction
- **contact map에 "누가 닿는가"를 넣는다는 발상**이 가장 직접적으로 옮겨 붙는다. HOI 연구에서 흔히 쓰는 binary contact map은 접촉 여부만 표시하는데, 이 논문처럼 손가락/손바닥 identity를 per-point 라벨로 확장하면 hand-object 관계를 훨씬 촘촘하게 표현할 수 있다. 사람 손 재구성이나 grasp 합성에서 supervision 신호로 재활용할 여지가 있다.
- **실패-성공 쌍 구축 방식**도 참고할 만하다. 들어올리기 직전이라는 동일한 상호작용 단계에서 상태를 모으고, 물체 중심 좌표계로 정규화한 뒤 관절 거리로 최근접 성공 자세를 짝짓는다(식 8). HOI에서 "잘못 잡은 손"을 "제대로 잡은 손"으로 교정하는 refinement 모델을 학습할 때 그대로 쓸 수 있는 페어링 전략이다.
- **폐루프 refinement 구조**(생성 → 판정 → 보정 반복)는 단발성 예측이 지배적인 hand pose estimation / grasp synthesis 파이프라인에 붙일 수 있는 일반적 틀이다. 특히 unseen category에서 59% → 83%로 뛴 ablation 결과는, 일반화 성능을 모델 용량이 아니라 "고쳐 잡는 능력"으로 얻을 수 있다는 근거가 된다.

### Egocentric Vision
- 1인칭 시점에서는 손이 물체를 가려 occlusion이 심하고, 시각만으로는 접촉 여부를 확정하기 어렵다. 이 논문이 "시각 기하만으로는 멀쩡해 보여도 실제 접촉은 실패한다"고 짚은 지점이 egocentric HOI의 고질적 문제와 정확히 겹친다. 촉각 대신 **접촉 상태를 나타내는 latent 채널을 point cloud에 추가**하는 형태로, egocentric 3D hand-object 표현에 접촉 사전정보를 주입하는 설계를 생각해 볼 수 있다.
- 다만 egocentric 세팅에는 실제 촉각 센서가 없다. 이 논문의 $\mathcal{M}$(예측된 contact map, 접촉 전)과 $\mathcal{P}_{vt}$(측정된 촉각, 접촉 후)의 구분을 빌려오면, 촉각 센서가 없는 상황에서는 $\mathcal{M}$ 만 쓰되 이를 비디오의 시간적 문맥으로 갱신하는 방향이 자연스러운 대안이 된다.
- 표현 형식에 대한 실증도 유용하다. "촉각 라벨이 붙은 이미지"(74/71/64)보다 "촉각 라벨이 붙은 point cloud"(91/82/83)가 뚜렷하게 나았다는 ablation은, egocentric HOI에서도 2D 이미지 위 주석보다 3D 표현이 손-물체 관계 추론에 유리함을 시사한다.

### Spatial Audio
- 직접적인 접점은 없다. 다만 방법론적으로 옮길 만한 발상은 있다. 이 논문의 기여는 "서로 다른 두 모달리티를 latent에서 concat하지 말고, 공통의 3D 공간 좌표계 위에 정렬하라"는 것이다. spatial audio에서도 소리 원천의 방향 정보를 오디오 embedding으로만 두지 않고 **3D 장면 표현(point cloud나 voxel) 위에 소리 세기/방향을 per-point 채널로 새기는** 대응 설계가 가능하다.
- 접촉 순간에 나는 소리는 grasping의 성공/실패나 물체 재질과 상관이 크므로, 촉각 채널 $\mathbf{c}_i$ 자리에 접촉 음향 feature를 넣는 audio-tactile 확장도 상상해 볼 만하다. 이 논문에서 다룬 내용은 아니다.

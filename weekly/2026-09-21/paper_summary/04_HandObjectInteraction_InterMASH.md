# InterMASH: A Unified Geometric Representation for Grasp Synthesis

**arXiv**: 2609.18504 | **주제 분류**: Hand-Object Interaction | **출판일**: 2026-09-16 | **학회**: SIGGRAPH Asia 2026 Conference Papers (2026년 12월 1–4일, 쿠알라룸푸르)
**저자/소속**: Xuanze Yang, Yumeng Liu(교신저자), Haiyang Xin, Changhao Li, Haowei Shen, Ligang Liu (University of Science and Technology of China) / Kai Xu (Jiangsu Key Laboratory of AI for Industries, Institute of AI for Industries, Chinese Academy of Sciences) / Ruizhen Hu (Shenzhen University)
**링크**: https://arxiv.org/abs/2609.18504

## 한 줄 요약

물체를 감싸는 구(sphere) 위에 고정 앵커를 뿌리고, 각 앵커에 저차 구면조화함수(spherical harmonics) 계수로 **손 표면·물체 표면·접촉 정보를 한꺼번에** 담는 InterMASH라는 통합 토큰 표현을 제안하고, 이 토큰 공간에서 직접 동작하는 conditional Diffusion Transformer로 사람 손(MANO)과 여러 로봇 손(ShadowHand, Barrett, Allegro)의 파지(grasp)를 하나의 모델로 생성한다.

## 메인 그림

![InterMASH 개요: 사람 손과 여러 로봇 손이 앵커 인덱스로 정렬된 공통 토큰 공간에 올라가고, 각 앵커는 국소 물체 기하·손 기하·접촉을 함께 인코딩한다](https://arxiv.org/html/2609.18504v1/teaser_v5.png)

Fig. 1 (Overview of InterMASH). 서로 다른 사람·로봇 손 형태(embodiment)가 앵커 인덱스로 색인되는 하나의 InterMASH 토큰 공간에 매핑되고, 대응되는 앵커끼리 국소 물체 기하·손 기하·접촉 정보를 인코딩한다. 이 통합된 상호작용 공간에서 ShadowHand, MANO, Barrett, Allegro에 대한 cross-embodiment 파지 합성이 가능해진다.

---

## 선행 연구

이 논문이 딛고 선 흐름은 크게 두 갈래로 정리된다.

**1) Grasp synthesis (파지 합성) — 사람 손과 로봇 손이 따로 발전해 왔다**

사람 손 쪽에서는 초기에 운동학·기하 제약을 만족시키는 최적화 기반 방법이 쓰였고(Liu et al., 2021의 differentiable force closure), 기존 상호작용을 새 물체 카테고리로 옮겨 재사용하는 transfer 기반 접근(TOCH, PartHOI)도 나왔다. 다만 이런 방법은 소스 상호작용과 의미적으로 대응되는 물체 부위가 필요하고, 최적화 기반 리타기팅이라 확장성과 다양성이 제한된다. 이후 고품질 모션캡처 데이터셋(HO-3D, GRAB, OakInk, ARCTIC)에 힘입어 Grasping Field, FastGrasp, BimArt 같은 데이터 기반 생성 모델이 자연스러운 사람 손 파지를 만들어내기 시작했다.

로봇 쪽에서는 시뮬레이션 파이프라인으로 대규모 dexterous grasp 데이터셋을 만든다([GenDexGrasp](https://arxiv.org/abs/2210.00722), [DexGraspNet](https://arxiv.org/abs/2210.02697)). 확장은 쉽지만 물리적 실현 가능성과 안정성에 치우쳐 있어 "사람 같은" 손재주는 약하고, 그 위에서 학습한 UniDexGrasp 계열은 안정적이지만 부자연스러운 파지를 내놓곤 한다. 대안으로 human-to-robot 리타기팅(AnyTeleop)이나 원격조작(RealDex)으로 사람 정렬된 로봇 파지를 모으는 길이 있고, DexGrasp Anything은 그런 데이터로 학습하면 생성 품질이 크게 올라간다는 것을 보였다.

논문이 문제 삼는 지점은 여기다. 이 패러다임은 **사람 파지 사전지식(prior)을 간접적으로만, 그것도 특정 로봇 손에 대해 비싼 리타기팅/원격조작을 거친 뒤에야** 활용한다. 데이터 수집이 embodiment별로 묶이므로 확장이 어렵다.

**2) Geometric representations for interaction (상호작용의 기하 표현)**

초기에는 물체 중심 contact map이 주류였다(GraspTTA, GenDexGrasp, CPF). 물체 위 어디에 접촉이 생기는지는 예측하지만 **손의 기하 자체는 담지 않아** 운동학적 모호성이 남는다.

이후 손과 물체의 공간 관계를 명시적으로 잡는 interaction-centric 표현으로 옮겨갔다. She et al. (2024)은 Interaction Bisector Surface(IBS, 손과 물체 사이 등거리 경계면)로 인터페이스를 세밀하게 서술했지만 공간 분할 비용이 크다. [D(R,O) Grasp](https://arxiv.org/abs/2410.01702)는 암묵적 point-to-point 거리 표현으로 cross-embodiment 파지 합성을 가능하게 했으나 서술자 차원이 매우 높고, 거리장에서 뽑은 손 점군이 노이즈가 많아 기하 충실도가 떨어진다. G-HOP은 skeletal distance field로 손과 물체를 함께 모델링하지만 볼륨 표현이라 메모리를 많이 쓰고 미세 디테일이 뭉개진다. 동시기 연구인 [T(R,O) Grasp](https://arxiv.org/abs/2510.12724)는 로봇 링크 위 graph diffusion으로 효율을 올렸지만 강체 시스템에 한정돼 연속적인 손 변형을 모델링할 수 없고, 따라서 사람 상호작용 prior와 호환되지 않는다.

**3) 이 논문이 직접 차용한 두 표현**

- **BPS** (Prokudin et al., 2019, Basis Point Sets): 공간에 고정된 점 집합을 공유 색인 체계로 두고, 각 basis point마다 가장 가까운 표면까지의 **스칼라 변위 하나**를 저장한다.
- **MASH** (Li et al., 2025, Masked Anchored Spherical Distances, SIGGRAPH 2025): 표면을 앵커별 국소 패치의 합집합으로 본다. 각 앵커는 가상의 시점 $p_i$로서 구면 방향 $(\theta,\phi)$으로 레이를 쏴 첫 표면 교점까지의 거리 $d_i(\theta,\phi)$를 재고, 이를 저차 구면조화함수로 근사한다: $d_i(\theta,\phi) = \sum_{l=0}^{L}\sum_{m=-l}^{l} C^{(i)}_{l,m} Y_l^m(\theta,\phi)$. 가시성 변화로 생기는 불연속을 막기 위해 방위각마다 극각 범위를 제한하는 **vision mask**(일반화된 view cone $\alpha_i(\phi)$)를 두어 국소성을 강제하고, 덕분에 낮은 차수 SH만으로도 패치를 안정적으로 근사할 수 있다. 앵커는 $\mathcal{A}_i = \{p_i, v_i, \mathcal{C}_i, \mathcal{V}_i\}$(위치, 국소 방향, SH 계수, vision mask 파라미터)로 표현된다.

## 문제 제기

논문의 문제의식은 세 겹이다.

**❶ 사람 손과 로봇 손을 아우르는 통합 표현이 없다.** 손 형태(morphology)와 표면 모델링 방식이 다르기 때문에, 사람 손 상호작용 데이터를 로봇 파지 학습에 그대로 쓸 수 없고 별도 리타기팅 단계를 거쳐야 한다. 이 추가 처리가 대규모 생성에서 상당한 계산 부담이 된다.

**❷ 기존 상호작용 표현은 "불완전하거나" 아니면 "비싸고 중복적이다".** contact map은 접촉의 유무·위치만 담고 파지에 관여하는 손 기하를 명시하지 않는다. 반대로 dense한 기하 표현(점-점 거리, SDF 필드)은 쌍별 관계나 공간 필드로 상호작용을 서술하느라 **파지와 무관한 정보까지 잔뜩 끌고 온다**. 결국 어느 쪽도 세밀한 파지 모델링에 충분한 기하 서술과, 확장 가능한 생성 모델링을 위한 압축된 기반을 동시에 주지 못한다.

**❸ BPS와 MASH를 그대로 가져다 쓰는 것으로는 안 된다.** 논문은 두 가지 구체적 장애물을 짚는다.

- **앵커 인덱스와 손 표면 영역 사이에 내재적 의미 대응이 없다.** 앵커를 고정해도, 같은 인덱스가 손 종류에 따라 전혀 무관한 공간 영역에 매핑될 수 있다. 이 상태로 섞어 학습하면 모델 입장에서 토큰의 의미가 모호해진다.
- **공유 앵커 아래에서 손·물체 SH 계수를 동시에 피팅하는 것이 직접 최적화로는 불안정하다.** 특히 고주파 항이 초기 수렴을 망가뜨린다.

## 연구 주제

논문이 세우는 목표는 **"표현부터 다시 설계해 cross-embodiment grasp synthesis를 가능하게 하기"** 다. 파지 합성을 기하 조건부 생성 문제로 정식화한다: 목표 물체 $O$와 손 종류 $\tau$의 템플릿 손 기하 $H_\tau$가 주어질 때, 유효한 파지 손 기하의 조건부 분포 $p(H \mid O, H_\tau)$를 모델링한다.

요구되는 표현의 세 가지 성질은 명확하다.

1. **통합된 토큰 공간** — 서로 다른 손 형태가 같은 표현 공간을 공유할 것
2. **압축성(compactness)** — 앵커당 SH 계수 몇 개 수준
3. **표현력(expressiveness)** — 스칼라 하나가 아니라 세밀한 국소 기하를 서술할 것

기존 표현과의 차이를 한 문장으로 요약하면: BPS에서 "고정된 공유 색인"을 가져오되 스칼라 거리 대신 **국소 표면 패치 전체**를 담고, MASH에서 "SH 기반 앵커 파라미터화"를 가져오되 앵커를 인스턴스별로 최적화하지 않고 **물체 중심 좌표계에 고정**하며, 각 앵커가 단일 형상이 아니라 **손 기하·물체 기하·접촉을 함께** 인코딩한다.

## 연구 방법

전체 파이프라인은 3단계다 — (1) InterMASH 표현으로 손-물체 상호작용을 인코딩, (2) conditional DiT로 이 공간에서 직접 파지 기하와 접촉을 생성, (3) 역운동학(IK)으로 관절 포즈로 디코딩.

### A. InterMASH 표현 (Section 4.1)

**손-물체 결합 앵커.** 각 손-물체 쌍마다 공유 앵커 집합 $\{\mathcal{A}_i\}_{i=1}^{n}$을 둔다. 앵커 하나가 국소 손 패치와 국소 물체 패치를 동시에 인코딩한다:

$\mathcal{A}_i = \{p_i,\, v_i^h,\, \mathcal{C}_i^h,\, \mathcal{V}_i^h,\, v_i^o,\, \mathcal{C}_i^o,\, \mathcal{V}_i^o\}$

($h$=손, $o$=물체, $v$=국소 방향, $\mathcal{C}$=SH 계수, $\mathcal{V}$=vision mask 파라미터). 형상을 따로 표현하는 대신 **상호작용하는 두 표면의 국소 기하를 토큰 하나 안에** 담는 것이 핵심이다.

앵커 위치는 **물체를 중심으로 한 구 위에 Fibonacci 샘플링으로 고정**한다. 반지름은 경험적으로 $r = 0.2$로 두어 데이터의 모든 물체와 손을 감싸게 한다. 고정 앵커는 균일한 공간 커버리지를 줄 뿐 아니라 **embodiment에 무관한 기준 좌표계**를 정의하므로, 같은 앵커 인덱스가 손 형태가 달라도 비교 가능한 공간 영역을 가리키게 된다.

**일관된 앵커-패치 대응 (Fig. 4).** 앵커를 고정하는 것만으로는 손 표면 영역에 대한 의미적 순서가 정해지지 않는다. 논문은 **MANO를 기준(reference)으로 삼는 대응**을 만든다.

1. 앵커 위치와 MANO 템플릿 패치 중심 사이의 **LAP(선형 할당 문제)** 를 풀어 MANO 패치를 고정 앵커에 배정 → 기준 순서 확보.
2. 각 로봇 손 템플릿 $\tau$에 대해, 손마다 상동(homologous) 키포인트를 정의하고 패치 중심 $c_i^\tau$를 **골격 기반 거리 시그니처**로 표현한다: $\mathbf{g}^{\tau}(c_i^{\tau}) = [d_\tau(c_i^\tau, k_1^\tau), \ldots, d_\tau(c_i^\tau, k_K^\tau)]$ — 여기서 $d_\tau$는 손 골격을 따라가는 geodesic 유사 거리다.
3. 정규화된 시그니처 공간에서 MANO 기준과의 거리를 최소화하는 순열을 찾는다: $\pi_\tau^{*} = \arg\min_{\pi \in S_n} \sum_{i=1}^{n} \|\bar{\mathbf{g}}^{\mathrm{MANO}}(c_i^{\mathrm{MANO}}) - \bar{\mathbf{g}}^{\tau}(c_{\pi(i)}^{\tau})\|_2^2$

이 **한 번의 템플릿 정렬**이 ShadowHand, Barrett, Allegro의 패치를 MANO 패치 순서에 매핑하고, 결과 대응은 barycentric interpolation으로 모든 파지 인스턴스에 전이된다. InterMASH 피팅과 IK 단계가 이 대응을 공유한다.

**SH 파라미터의 단계적 최적화.** 모든 계수, 특히 고주파 항을 한꺼번에 최적화하면 초기 수렴이 불안정하다. 따라서 coarse-to-fine 스케줄을 쓴다 — 차수 $d_{\mathrm{sh}} = 0$에서 시작해 재구성 손실이 안정화되면 $d_{\max} = 2$까지 점진적으로 올린다.

**접촉 맵의 압축 표현.** 물체 표면에 접촉을 dense하게 표현하는 대신, 각 앵커에 **계수 4개짜리 절단된 SH 전개**로 국소 접촉장을 근사한다: $\mathcal{K}_i = \sum_{l=0}^{1}\sum_{m=-l}^{l} C_{l,m}^{(i)} Y_l^m(\theta,\phi)$. 접촉 강도 자체는 GraspTTA를 따라 물체 점 $P_{\mathrm{obj}}$에서 손 점군까지의 최근접 거리 $D(P_{\mathrm{obj}})$로 정의한다:

$\mathcal{K}(P_{\mathrm{obj}}) = 1 - 2\left(\mathrm{Sigmoid}(100 \cdot D(P_{\mathrm{obj}})) - 0.5\right)$

**접촉 서술자는 학습 시 보조 감독(auxiliary supervision)으로만 쓰이고 추론에는 필요하지 않다.**

### B. 확장 가능한 생성 모델 (Section 4.2)

앵커 하나가 저차원 토큰 하나에 대응하므로 표현이 transformer 생성 모델과 바로 맞물린다. 파지 합성을 InterMASH 공간에서의 조건부 시퀀스 모델링으로 다시 쓰고, **Diffusion Transformer(DiT)** 를 백본으로 쓴다. dense한 암묵적 상호작용 필드를 모델링하는 것보다 훨씬 효율적이라는 것이 논지다.

- **생성 대상** (DDPM의 clean state): $f_0 = \{v_i^h, \mathcal{C}_i^h, \mathcal{V}_i^h, \mathcal{K}_i\}_{i=1}^{n}$ — 즉 **손 쪽 MASH 파라미터와 물체 쪽 접촉 서술자를 함께** 생성한다. 접촉을 별도의 중간 신호로 예측한 뒤 후속 최적화에 넘기던 기존 방식(GraspTTA, UniDexGrasp)과 달라지는 지점이며, 형상과 접촉의 상호 일관성을 높이고 관통(penetration)을 줄이는 효과를 노린다.
- **조건**: $\mathbf{c} = \{v_i^o, \mathcal{C}_i^o, \mathcal{V}_i^o, v_i^\tau, \mathcal{C}_i^\tau, \mathcal{V}_i^\tau\}_{i=1}^{n}$ — 물체 기하와 템플릿 손 기하.
- **학습 목표**: 표준 noise prediction $\mathcal{L}_{\mathrm{recon}} = \mathbb{E}_{f_0,t,\epsilon}[\|\epsilon - \epsilon_\phi(f_t, \mathbf{c}, t)\|_2^2]$.
- **구조**: $N$개의 DiT 블록. 블록 안에서 timestep 임베딩과 조건 특징이 denoising을 변조하고, self-attention이 노이즈 파지 토큰 간 의존성을, cross-attention이 물체·템플릿 손의 기하 prior 주입을 담당한다. 앵커 위치 $p_i$는 **RoPE(회전 위치 임베딩)** 로 인코딩해 공간 배치를 보존하고, 나머지 스펙트럼 특징은 각각 별도 선형층으로 투영한다.

**Neighborhood-Enhanced Attention (N.E.A.).** 표준 attention은 이웃 패치 간 기하적 인접성을 무시한다. 템플릿 손 패치와 물체 패치의 $k$-최근접 이웃 그래프로부터 쌍별 attention bias $s_{ij}$를 만들어 로짓에 더한다:

$\alpha_{ij} = \mathrm{softmax}\left(q_i k_j^{\top}/\sqrt{d_h} + s_{ij}\right)$

구조적으로 인접한 영역에 주의를 모으면서도, 손-물체 추론에 필요한 장거리 상호작용은 유지한다.

**Physics-guided training & sampling.** 기하만으로는 물리적으로 그럴듯한 파지가 보장되지 않는다. DexGrasp Anything을 따라 학습과 샘플링 양쪽에 물리 가이던스를 넣는다.

- 학습: 생성된 InterMASH 토큰에서 복원한 점군 위에서 결합 물리 페널티 $\mathcal{L}_{\mathrm{phys}}$를 계산해 보조 제약으로 건다 — 안정적 접촉을 유도하고 관통과 자기 충돌을 줄인다.
- 샘플링: **노이즈 상태가 아니라 "깨끗한 기하 추정치" 위에서 물리적 타당성을 평가**하는 것이 핵심이다. denoising step $t$에서 $\hat{f}_0(f_t, t) = \frac{1}{\sqrt{\bar{\alpha}_t}}(f_t - \sqrt{1-\bar{\alpha}_t}\,\epsilon_\phi(f_t,\mathbf{c},t))$로 denoised 토큰을 추정하고, 여기서 손·물체 점군을 복원해 $\mathcal{L}_{\mathrm{phys}}(\hat{f}_0)$를 잰다. 이 추정은 저노이즈 구간에서 더 신뢰할 만하며, 그때 생성 기하가 데이터 매니폴드에 충분히 가까워 물리 페널티가 의미 있는 그래디언트를 준다. 그런 다음 DDPM posterior mean을 물리 페널티의 음의 그래디언트 방향으로 밀어준다:

$\widetilde{\mu}_\phi = \mu_\phi(f_t, \mathbf{c}, t) - s\,\Sigma_t \nabla_{f_t}\mathcal{L}_{\mathrm{phys}}(\hat{f}_0(f_t, t))$

($s$는 가이던스 스케일). DDPM 역과정 안에 머무르면서 각 스텝을 낮은 관통·적은 자기 충돌·안정적 접촉 쪽으로 조향한다.

### C. IK로 최종 손 포즈 복원 (Section 4.3)

생성 결과는 InterMASH 공간의 기하이므로 관절 포즈 $(\theta, R, \mathbf{p})$로 변환해야 한다.

1. 생성된 손을 패치별 점집합 $\{\hat{\mathcal{S}}_i\}_{i=1}^{P}$으로 복원한다.
2. 템플릿과 생성 패치 중심의 대응으로부터 **Umeyama 정렬**(닫힌 형태 해)로 전역 정렬 $(R, \mathbf{p})$을 초기화한다.
3. 확립된 앵커-패치 대응 하에서 포즈된 템플릿 손 패치를 생성 패치에 맞추어 관절 파라미터를 복원한다.

이 **patch-wise IK**는 앵커 의미를 보존해 전역 표면 피팅 대비 매칭 모호성을 줄인다. 필터링된 CMapDataset의 생성 ShadowHand 샘플에서 평균 total $\ell_1$ Chamfer 오차 **0.0125 m**, $\mathcal{L}_{\mathrm{CD}}^{\mathrm{total}} < 0.1$ m 기준 성공률 **99.5%**, 샘플당 평균 디코딩 시간 **0.39초**를 기록한다.

**구현.** PyTorch, 옵티마이저는 [Muon](https://arxiv.org/abs/2502.16982), 공식 train-test split 사용, **NVIDIA RTX 4090 8장**이 달린 Ubuntu 서버에서 전체 실험 수행.

## 실험 결과 / 연구 의의

평가 축은 네 가지다 — 단일 손 파지 생성 품질, cross-embodiment 합성, 사람 prior 전이, ablation.

**지표 읽는 법.** *Suc.6*은 6개 외란 방향 **전부**에서 파지가 유지된 비율, *Suc.1*은 **최소 한 방향**에서 유지된 비율(둘 다 높을수록 좋음), *Pen.*은 최대 관통 깊이(낮을수록 좋음), *Div.*는 국소 포즈 파라미터 표준편차 평균으로 잰 다양성(높을수록 좋음)이다. cross-embodiment 실험에서는 D(R,O) Grasp 프로토콜을 따라 Isaac Gym 시뮬레이터에서 6방향 외란 테스트를 통과한 비율을 *Success Rate*로, 성공한 파지들의 관절값 표준편차를 *Diversity*로 쓴다.

### 1) 단일 손 파지 생성 (Table 1, DexGraspNet / ShadowHand)

| Method | Suc.6 ↑ | Suc.1 ↑ | Pen. ↓ | Div. ↑ |
|---|---|---|---|---|
| UniDexGrasp (2023b) | 33.9 | 70.1 | 31.9 | 0.14 |
| GraspTTA (2021) | 18.6 | 67.8 | 24.5 | 0.13 |
| SceneDiffuser (2023) | 26.6 | 66.9 | 31.0 | 0.15 |
| UGG (2024) | 46.9 | 79.0 | 25.2 | 0.14 |
| DexGrasp Anything (2025) | **53.6** | 90.4 | 21.5 | **0.22** |
| D(R,O) Grasp (2024) | 46.9 | 89.7 | 17.5 | 0.20 |
| **InterMASH (Ours)** | 53.5 | **91.9** | **16.2** | 0.14 |

읽을 점: (a) **Suc.1과 Pen.에서 1위**다. 적어도 한 방향의 외란을 견디는 파지를 가장 많이 만들고, 관통도 가장 적다 — 손 기하와 접촉을 함께 모델링하고 물리 가이던스를 건 설계와 일치하는 결과다. (b) **Suc.6과 Div.에서는 최고가 아니다.** Suc.6은 DexGrasp Anything 53.6 vs InterMASH 53.5로 사실상 동률이지만, 다양성은 0.22 vs 0.14로 뚜렷하게 밀린다. 논문 스스로 이를 **quality-diversity trade-off**로 규정한다 — 제안 표현과 학습 목표가 모델을 "물리적으로 더 믿을 만한" 쪽으로 편향시키고, 그 대가로 다양성과 엄격한 6방향 기준의 성능을 조금 내준다는 것이다.

### 2) Cross-embodiment 합성 (Table 2, 필터링된 CMapDataset)

ShadowHand와 Barrett 서브셋으로 **단일 모델**을 학습한다.

| Method | Barrett Succ. (%) ↑ | Shadow Succ. (%) ↑ | Barrett Div. ↑ | Shadow Div. ↑ |
|---|---|---|---|---|
| DFC (2021) | 86.30 | 58.80 | **0.532** | 0.435 |
| GenDexGrasp (2022) | 67.00 | 54.20 | 0.488 | 0.318 |
| D(R,O) Grasp (2024) | 87.30 | **83.00** | 0.513 | **0.441** |
| InterMASH (Shadow only) | – | 57.62 | – | 0.416 |
| **InterMASH (Shadow+Barrett)** | **90.30** | 64.15 | 0.480 | 0.396 |

읽을 점: (a) **Barrett에서 최고 성공률(90.30%)** 을 달성한다. 데이터가 더 많고 자유도가 낮은(8 DoF) 손에서 이득이 두드러진다. (b) **ShadowHand에서는 D(R,O) Grasp(83.00%)에 크게 뒤진다(64.15%).** "경쟁력 있다"는 표현은 쓰지만 격차가 18.85%p로 작지 않다. (c) 가장 중요한 수치는 **mixed-hand training의 효과**다 — ShadowHand만으로 학습하면 57.62%인데 Barrett 데이터를 섞으면 **64.15%로 오르고**, 다양성은 0.416 → 0.396으로 소폭만 떨어진다. 형태가 다른 손의 데이터가 서로 도움이 된다는, 통합 표현의 존재 이유를 직접 뒷받침하는 결과다.

정성적으로는(Fig. 6) D(R,O) Grasp가 생성한 점군이 고정 해상도에 묶여 손 구조가 잘 드러나지 않는 반면, InterMASH는 더 손처럼 알아볼 수 있는 기하를 내놓고 연속적인 국소 패치 표현 덕에 임의 해상도 샘플링을 지원한다.

### 3) 사람 prior의 로봇 파지 전이 (Table 3)

DexGRAB(ShadowHand)로만 학습한 모델과, DexGRAB + MANO 기반 GRAB 샘플을 1:1로 섞어 파인튜닝한 모델을 동일한 DexGRAB 테스트 split에서 비교한다.

| Training Setting | Suc.6 ↑ | Suc.1 ↑ | Pen. (mm) ↓ | Div. ↑ |
|---|---|---|---|---|
| DexGRAB only | 25.8 | 64.2 | **14.9** | 0.450 |
| DexGRAB + GRAB fine-tune | **29.0** | **65.9** | 18.6 | **0.500** |

읽을 점: 성공률(25.8 → 29.0, 64.2 → 65.9)과 다양성(0.450 → 0.500)이 모두 오른다 — **사람 → 로봇 prior 전이가 실제로 이득이 된다**는 증거다. 다만 관통은 14.9 → 18.6 mm로 악화된다. 논문은 그 원인을 **소스 데이터의 기하 품질**로 돌린다: GRAB 학습 데이터의 평균 관통(24.6 mm)이 DexGRAB(11.34 mm)보다 높기 때문이다. 즉 전이의 품질은 소스 데이터 기하에 직접 좌우된다.

### 4) Ablation

**(a) 상호작용 표현 비교 (Table 4).** DiT와 IK 파이프라인을 동일하게 맞추고, 앵커/패치 수를 모두 128로 통일하며, 물리 가이던스와 N.E.A.를 끈 공정 비교다.

| Method | Barrett ↑ | Allegro ↑ | Shadow ↑ |
|---|---|---|---|
| Basis Point Set | 4.50 | 3.90 | 5.40 |
| Patch Emb. + Soft-Intro VAE | 33.20 | 11.10 | 14.30 |
| Patch Emb. + In-house VAE | 24.80 | 11.10 | 10.40 |
| **InterMASH (Ours)** | **52.70** | **15.90** | **20.00** |

**격차가 압도적이다.** BPS(앵커당 스칼라 하나)는 사실상 작동하지 않고(4~5%대), 학습된 patch embedding + VAE 계열도 InterMASH에 크게 못 미친다. "고정 앵커 대응 + 압축된 국소 패치 서술자 + 물체 쪽 접촉"의 조합이 이 논문 전체에서 가장 강한 근거를 제공하는 실험이다. 동시에 절대 성공률 자체는(Barrett 52.70, Shadow 20.00) 낮은데, 이는 물리 가이던스와 N.E.A.를 모두 끈 설정이기 때문이다.

**(b) 핵심 구성요소 (Table 5, mixed-hand 학습 설정).**

| Phys. Train | Phys. Samp. | N.E.A. | Barrett Suc. ↑ | Shadow Suc. ↑ | Barrett Div. ↑ | Shadow Div. ↑ |
|---|---|---|---|---|---|---|
| ✗ | ✗ | ✗ | 80.17 | 51.06 | **0.498** | **0.430** |
| ✓ | ✗ | ✗ | 86.10 | 59.50 | 0.496 | 0.426 |
| ✓ | ✓ | ✗ | 85.20 | 61.20 | 0.496 | 0.427 |
| ✓ | ✓ | ✓ | **90.30** | **64.15** | 0.480 | 0.396 |

읽을 점: (a) **physics-guided training의 기여가 가장 크다** — Barrett 80.17 → 86.10, Shadow 51.06 → 59.50. 명시적인 물리 감독이 파지 합성에 필수적이라는 확인이다. (b) physics-guided **sampling**은 ShadowHand에서만 개선(59.50 → 61.20)되고 Barrett에서는 오히려 소폭 하락(86.10 → 85.20)한다. (c) N.E.A.를 켜면 양쪽 모두 최고 성능(90.30 / 64.15)이 나온다. (d) **모든 구성요소가 다양성을 조금씩 깎는다**(Shadow Div. 0.430 → 0.396). 기하·물리 제약을 강하게 걸수록 다양성이 줄어드는 일관된 경향이며, Table 1의 quality-diversity trade-off와 같은 이야기다.

### 연구 의의 요약

1. **표현 설계 자체가 성능을 가른다.** Table 4의 BPS(5%대) vs InterMASH(20~53%) 격차는, 동일한 생성 백본·동일한 토큰 수 아래에서 "앵커당 무엇을 담는가"가 결정적임을 보여준다.
2. **형태가 다른 손의 데이터를 섞어 학습하면 서로 도움이 된다.** Barrett 데이터 추가로 ShadowHand 성공률이 57.62 → 64.15%로 올랐다. 리타기팅 없이 곧바로 mixed-hand 학습이 가능하다는 것이 통합 토큰 공간의 실질적 가치다.
3. **사람 파지 데이터(MANO/GRAB)를 로봇 파지 생성에 직접 투입할 수 있다.** 기존 패러다임처럼 embodiment별 리타기팅이나 원격조작을 거치지 않고, 같은 표현 공간에 올려 파인튜닝하는 것만으로 성공률과 다양성이 오른다.
4. **손 기하와 접촉의 동시 생성**이 형상-접촉 일관성과 물리적 타당성을 높인다 — Table 1의 Pen. 16.2로 최저.
5. 논문 결론은 이를 **"중간 수준의 기하적 상호작용 표현(intermediate geometric interaction representation)이 확장 가능한 파지 생성에 효과적인 설계 선택"** 이라는 일반적 주장으로 정리한다.

## 한계

**논문이 스스로 밝힌 것 (Limitation and Future Work)**

- **손 특화 귀납 편향(inductive bias)이 적다.** InterMASH는 D(R,O) Grasp 같은 방법에 비해 상대적으로 범용적인 앵커 색인 표현을 쓴다. 이 설계는 확장성을 높이고 데이터가 충분할 때(DexGraspNet 결과) 강하지만, **작은 mixed-hand 데이터셋에서 고자유도(high-DoF) 손에 대해서는 데이터 효율이 떨어진다.** 필터링된 CMapDataset에서 ShadowHand는 Barrett보다 샘플이 적고 행동 공간 차원이 높은데, 이런 조건에서는 내장된 대응 prior가 강한 방법이 여전히 유리하다는 것을 논문이 인정한다. Table 2의 Shadow 64.15% vs D(R,O) 83.00%가 정확히 그 지점이다.
- **future work**으로 InterMASH의 확장성에 데이터 효율적인 prior, 사전학습 목표(pretraining objective), 고자유도 embodiment용 hand-aware conditioning을 결합하는 방향을 제시한다.
- **좌우 손 혼합 학습에서 handedness ambiguity(좌/우 손 모호성)가 관찰된다**고 언급하며, 상세 논의는 보충자료로 미룬다.

**표·본문에서 드러나는 것**

- **다양성이 일관되게 약점이다.** Table 1에서 Div. 0.14로 DexGrasp Anything(0.22), D(R,O) Grasp(0.20)에 밀리고, Table 5에서도 구성요소를 켤수록 다양성이 단조 감소한다(Shadow 0.430 → 0.396). 논문은 이를 trade-off로 설명하지만 해소하지는 않는다.
- **physics-guided sampling의 효과가 손에 따라 엇갈린다.** Barrett에서는 86.10 → 85.20으로 오히려 떨어진다.
- **사람 prior 전이가 관통을 악화시킨다** (14.9 → 18.6 mm). 소스 데이터의 기하 품질에 결과가 좌우되므로, 임의의 사람 파지 데이터를 그냥 섞으면 되는 문제가 아니다.
- **하이퍼파라미터가 데이터에 맞춰져 있다.** 앵커 구 반지름 $r=0.2$는 "우리 데이터의 모든 물체와 손을 감싸도록" 경험적으로 정한 값이고, SH 최대 차수는 $d_{\max}=2$, 접촉 서술자는 계수 4개로 고정이다. 더 큰 물체나 더 세밀한 접촉 구조로의 일반화는 검증되지 않았다.
- **파이프라인이 IK 디코딩에 의존한다.** 생성된 기하를 관절 포즈로 바꾸는 단계가 별도로 필요하고, 샘플당 0.39초가 든다. Chamfer 오차 기준 성공률은 99.5%로 높지만, 생성-디코딩이 분리된 구조라 두 단계의 오차가 누적될 여지가 있다.
- **주요 실험이 시뮬레이션 기반이다.** 성공률은 Isaac Gym에서의 외란 테스트로 측정되며, 실제 로봇 하드웨어 실험은 논문에 없다.
- **보충자료 의존도가 높다.** 물리 페널티 $\mathcal{L}_{\mathrm{phys}}$의 정확한 형태와 가중치, Fibonacci 앵커 구성 세부, IK 목적함수와 정규화 항, cross-embodiment 평가 절차, staged SH 최적화의 검증이 모두 보충자료로 넘어가 있어 본문만으로는 재현이 어렵다.
- **시각 입력을 쓰지 않는다.** 입력은 물체 기하와 템플릿 손 기하뿐이며, RGB 이미지나 영상은 파이프라인에 없다.

## 우리 연구와 연결되는 점

**Hand-Object Interaction 관점 (가장 직접적)**

- **"앵커 + 저차 SH"는 HOI 표현을 다시 생각하게 하는 레시피다.** 지금까지 HOI 연구에서 접촉은 주로 물체 정점별 contact map이나 손 정점별 거리로 표현돼 왔다. InterMASH는 (1) 공간에 고정된 공유 색인을 두고, (2) 각 색인에 국소 표면 패치를 **스펙트럼 계수 몇 개로** 압축하며, (3) 손·물체·접촉을 **토큰 하나 안에** 묶는다. contact map을 예측하는 HOI 연구라면 "접촉 강도를 앵커별 4-계수 SH로 근사"하는 아이디어만 떼어 써도 표현 차원을 크게 줄일 수 있다.
- **LAP 기반 cross-embodiment 대응 절차가 재사용 가능하다.** MANO를 기준으로 삼고, 골격 geodesic 거리 시그니처 $\mathbf{g}^\tau(c_i^\tau)$ 공간에서 선형 할당을 풀어 패치 순서를 정렬하는 방식은 **"서로 다른 손 모델 사이에 의미적 대응을 만드는" 일반 문제**에 그대로 적용된다. MANO ↔ 로봇 손뿐 아니라, 서로 다른 손 파라메트릭 모델 사이나 손 ↔ 발 같은 다른 관절 구조 사이에도 이식 가능한 패턴이다.
- **"기하를 생성한 뒤 IK로 포즈를 뽑는" 2단계 구조**는 HOI 생성에서 자주 쓰이는 "포즈 파라미터를 직접 회귀"와 대비되는 선택지다. 패치별 대응을 유지한 채 IK를 풀면(patch-wise IK) 전역 표면 피팅보다 매칭 모호성이 줄어든다는 것이 이 논문의 주장이고, Chamfer 오차 0.0125 m / 성공률 99.5%라는 구체적 수치가 붙어 있다.
- **접촉을 "학습 시 보조 감독, 추론 시 불필요"로 두는 설계**가 실용적이다. 접촉 주석이 있는 데이터에서만 추가 신호를 얻고 추론 시에는 물체 기하만으로 동작하므로, 접촉 라벨이 부분적으로만 있는 HOI 데이터셋에서도 쓸 수 있다.
- **quality-diversity trade-off가 명시적 연구 기회다.** 물리 제약을 강하게 걸수록 다양성이 떨어진다는 것이 Table 1과 Table 5에서 일관되게 나타난다. 다양성을 유지하면서 물리적 타당성을 얻는 방법(예: 다양성 항을 명시적으로 넣거나, 물리 가이던스 스케일 $s$를 적응적으로 조절)은 이 논문이 남긴 열린 문제다.

**Egocentric Vision 관점**

- **직접적 연결은 약하다** — 이 논문에 영상 입력은 없고, 입력은 물체 메시와 템플릿 손 기하뿐이다. 1인칭 영상에서 손-물체 상호작용을 다루는 연구와는 문제 설정이 다르다. 아래는 근거 있는 추론이 아니라 **잠재적 관점**임을 밝혀둔다.
- 다만 InterMASH를 **표현 계층**으로 보면 ego 연구와 붙일 지점이 있다. 1인칭 영상에서 추정한 손 포즈와 물체 포즈를 InterMASH 토큰으로 인코딩하면, 손 종류·물체 종류에 무관한 고정 차원 상호작용 서술자가 된다. 파지 유형 분류, 상호작용 검색, 접촉 예측 같은 downstream 태스크의 공통 입력 표현 후보다.
- **물체 중심 구 위에 고정된 앵커 좌표계**($r=0.2$, Fibonacci 샘플링)는 카메라가 계속 움직이는 ego 세팅에서 "카메라 자세와 무관한 상호작용 표현"을 만드는 한 가지 방법이다. ego 연구에서 흔히 쓰는 손목 기준 정규화나 카메라 기준 좌표계와 달리, 물체를 기준으로 삼기 때문에 시점 변화에 불변이다.
- 역방향 활용도 생각해 볼 수 있다 — ego 영상에서 복원한 손-물체 상호작용을 InterMASH로 인코딩해 **로봇 손으로 리타기팅하는 파이프라인**이다. 논문의 Section 5.4가 이미 MANO 기반 GRAB 데이터로 그 전이가 가능함을 보였으므로, 소스를 모션캡처에서 ego 영상 기반 복원으로 바꾸는 것은 자연스러운 확장이다. 다만 Table 3이 보여주듯 **소스 데이터의 기하 품질이 그대로 전이 품질을 좌우하므로**(GRAB의 높은 관통 → 파인튜닝 후 관통 악화), 노이즈가 많은 영상 기반 복원을 쓸 때는 이 효과가 더 커질 위험이 있다.

**Spatial Audio 관점**

- **이 논문에 오디오는 전혀 없다.** 정적인 파지 기하 생성 문제이고, 시간축도 없다(단일 프레임 파지 합성). 따라서 직접적인 연결점은 논문에 명시적으로 존재하지 않는다.
- 굳이 이어 붙인다면 **표현 설계의 방법론 수준**이다. 이 논문의 핵심 움직임은 "공간의 고정 기저(fixed basis) 위에 국소 정보를 저차 구면조화함수로 압축한다"인데, **구면조화함수는 spatial audio에서 Ambisonics의 표준 기저**이기도 하다. 방향별 음장을 저차 SH 계수로 표현하는 것과, 앵커에서 본 방향별 표면 거리를 저차 SH 계수로 표현하는 것은 수학적으로 같은 도구다. 음장과 기하를 **동일한 SH 계수 공간에서 토큰화해 하나의 transformer에 넣는** audio-visual 구조는 이 대응을 이용한 잠재적 설계 방향이다 (논문에 언급된 바 없는, 순수하게 잠재적인 관점이다).
- 접촉이 소리를 낸다는 점도 개념적 연결 고리다. InterMASH는 접촉을 앵커별 SH 계수 4개로 압축하는데, 접촉 지점의 공간 분포는 곧 접촉음의 발생 위치 분포이기도 하다. 다만 이 논문은 정적 파지만 다루고 접촉음이 발생하는 동적 조작(manipulation)은 범위 밖이라, 실제로 연결하려면 시간축이 있는 후속 문제 설정이 필요하다.

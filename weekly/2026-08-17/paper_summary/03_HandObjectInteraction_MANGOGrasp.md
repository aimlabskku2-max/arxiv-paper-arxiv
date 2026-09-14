# MANGO-Grasp: Mahalanobis Fields over Geometry-Oriented 3D Gaussians for Cross-Embodiment Dexterous Grasping

**arXiv**: 2608.02014 | **주제 분류**: Hand-Object Interaction | **출판일**: 2026-08-03 | **학회**: 프리프린트 (IEEE 투고 중)
**저자/소속**: Heng Zhang (A*STAR I2R, NTU), Kevin Yuchen Ma (A*STAR I2R, NUS Show Lab), Mike Zheng Shou (NUS Show Lab), Weisi Lin (NTU), Yan Wu (A*STAR I2R) — Weisi Lin, Yan Wu 교신저자
**링크**: https://arxiv.org/abs/2608.02014

## 한 줄 요약
물체를 표면에 붙은 납작한 3D Gaussian 판(plate)들로, 손을 형태·운동 정보를 함께 담은 키포인트 기술자로 표현한 뒤, 둘 사이의 **마할라노비스 거리장(Mahalanobis field)** 을 예측해 여러 종류의 다지 로봇 손에 공통으로 쓰이는 파지(grasp)를 합성하는 프레임워크다.

## 메인 그림
![물체는 방향성을 가진 3D Gaussian, 손은 키포인트로 표현하고 둘 사이를 이방성 마할라노비스 장으로 잇는다](https://arxiv.org/html/2608.02014v1/x1.png)
제안하는 이방성(anisotropic) 상호작용 정식화의 개요 — 접선 방향 이동에는 둔감하고 법선 방향 이동에는 민감한 상호작용 장을 학습해, 학습에 쓴 손들은 물론 처음 보는 손으로도 zero-shot 전이한다.

## 선행 연구
크로스-임바디먼트(cross-embodiment) 정교 파지 연구는 크게 세 갈래로 나뉜다.

- **Hand-centric**: 물체 관측에서 특정 손의 관절 값을 직접 회귀한다 (UniDexGrasp, UniDexGrasp++, UniGraspTransformer, [MachaGrasp](https://arxiv.org/abs/2510.06068)). 손의 기구학이 크게 달라지면 전이가 잘 안 된다.
- **Object-centric**: 손과 무관한 접촉 지점을 예측한다 (UniGrasp, GenDexGrasp, Geometry Matching, GeoMatch++). 예측한 접촉점을 실제로 도달 가능한 손 자세로 옮기는 "실현 격차(realization gap)"가 남는다.
- **Interaction-centric**: 손과 물체의 공간 관계 자체를 모델링한다. DRO Grasp는 로봇 키포인트와 물체 점 사이의 **유클리드 거리 행렬**로, TRO Grasp는 손 링크와 물체 패치 사이의 **변환**을 그래프 확산으로 모델링한다. 임바디먼트 정보를 유지하면서도 전이 가능한 접촉 구조를 얻는다는 점에서 최근 가장 좋은 결과를 냈고, 이 논문도 여기에 속한다.

물체 표현 쪽으로는 3D Gaussian Splatting(3DGS)과 표면 정렬 변형인 SuGaR, 2D Gaussian Splatting을 참고했다. 다만 이들은 렌더링(외관 복원)이 목적이라는 점이 다르다.

## 문제 제기
기존 interaction-centric 방법에는 세 가지 표현상의 약점이 있다.

1. **물체 표현이 국소 표면 기하를 담지 못한다.** 균일 샘플링 점군이나 점군 패치는 기하 복잡도와 무관하게 표현 용량을 배분한다. 그래서 접촉에 중요한 곡률 높은 영역은 과소 표현되고, 넓은 평면은 과잉 샘플링된다. 게다가 표면의 접평면/법선 구조를 명시적으로 담지 않는다.
2. **접촉을 등방성(isotropic) 근접도로 환원한다.** 유클리드 거리는 모든 방향을 동등하게 취급하지만, 실제 정교 접촉은 방향에 의존한다. 표면을 따라 미끄러지는 **접선 방향 변위**와 표면에서 떨어지는 **법선 방향 변위**는 물리적 의미가 전혀 다르다.
3. **로봇 표현이 형태와 기구학을 함께 담지 않는다.** URDF에서 뽑은 링크 기하·자세를 넣거나(TRO), 자세 불변 키포인트 대응을 대조 학습으로 익히는(DRO) 식인데, "이 부위가 어떻게 생겼는가"와 "이 부위가 어떻게 움직일 수 있는가"를 명시적으로 결합하지 않는다. 파지 가능성은 둘 다에 달려 있다.

## 연구 주제
**크로스-임바디먼트 정교 파지 합성(cross-embodiment dexterous grasp synthesis)** 이다. 이질적인 다지 손 후보 집합에서 하나의 임바디먼트 $e$와 목표 물체가 주어질 때, 기구학적으로 실현 가능하고 안정적인 손 자세 $\mathbf{q}^{*}$(관절 각도 + 6자유도 손목 포즈)를 만드는 것이 목표다. 핵심은 손마다 따로 튜닝하지 않고 **모든 임바디먼트에 하나의 최적화 정식화와 동일한 하이퍼파라미터**를 쓰는 것이다.

## 연구 방법
전체 파이프라인은 네 단계다: (1) 물체 → 기하 지향 Gaussian, (2) 로봇 → morpho-kinematic 기술자 사전학습, (3) 상호작용 장 생성, (4) 최적화 기반 파지 실현.

### 1) 기하 지향 3D Gaussian 구성
물체 메시를 **고정 개수** $G=256$개의 프리미티브로 바꾼다. 각 프리미티브는

$$\mathcal{G}=\{g_{j}\}_{j=1}^{G},\quad g_{j}=(\boldsymbol{\mu}_{j},\mathbf{R}_{j},\boldsymbol{\sigma}_{j},\mathbf{n}_{j})$$

로, 중심 $\boldsymbol{\mu}_{j}\in\mathbb{R}^{3}$, 방향 $\mathbf{R}_{j}\in SO(3)$, 이방성 스케일 $\boldsymbol{\sigma}_{j}\in\mathbb{R}^{3}_{+}$, 바깥쪽 법선 $\mathbf{n}_{j}\in\mathbb{S}^{2}$를 갖는다. 네 단계로 만든다.

**(a) 기하 기반 밀도화.** 표준 3DGS는 광도(photometric) 손실로 densification을 유도해서, 질감은 화려하지만 기하는 단순한 영역에 프리미티브가 몰리는 문제가 있다. 이 논문은 대신 **메시의 표면 법선을 RGB로 인코딩한 이미지**를 supervision 타깃으로 쓴다. 법선을 색으로 바꾸면 곡면은 색 변화가 급하고 평면은 거의 균일하므로, 이미지 공간 gradient로 촉발되는 densification이 자연스럽게 기하 복잡도를 따라간다. 여기에 메시 깊이 맵의 곡률 가중치를 곱한다.

$$W(u,v)=1+\mathrm{Norm}\big(|\partial_{u}D^{\mathrm{gt}}(u,v)|+|\partial_{v}D^{\mathrm{gt}}(u,v)|\big)$$

$$\mathcal{L}_{\mathrm{photo}}=\lambda_{\mathrm{C}}\big\|W\odot|\hat{C}-C^{\mathrm{gt}}|\big\|_{1}+\lambda_{\mathrm{S}}\mathcal{L}_{\mathrm{D\text{-}SSIM}}(\hat{C},C^{\mathrm{gt}})$$

($\lambda_{\mathrm{C}}=0.8$, $\lambda_{\mathrm{S}}=0.2$). 중복 프리미티브는 불투명도 희소성 항 $\mathcal{L}_{\mathrm{opa}}=\frac{1}{T}\sum_{i=1}^{T}o_{i}$ ($\lambda_{\mathrm{opa}}=0.02$, 워밍업 후에만 적용)로 투명해지도록 눌러 표준 pruning에 걸리게 한다.

**(b) 고정 예산 선택.** $\mathrm{score}(g_{j})=o_{j}A_{j}(1+\beta H_{j})$ 상위 $G$개만 남긴다. $A_{j}$는 최대 투영 면적, $H_{j}\in[0,1]$은 가장 가까운 메시 정점의 정규화된 이산 평균 곡률이다. $o_{j}A_{j}$는 표면을 넓게 덮는 프리미티브를, $H_{j}$는 날카로운 특징을 선호한다. $\beta=0.2$로 곡률 보너스를 제한해 모서리 프리미티브가 평면 영역을 몰아내지 않게 한다.

**(c) 표면 정렬 정련.** 예산을 고정한 뒤 densification/culling을 끄고 기하 파라미터만 최적화한다.

$$\mathcal{L}_{\mathrm{refine}}=\mathcal{L}_{\mathrm{photo}}+\lambda_{s}\mathcal{L}_{\mathrm{surf}}+\lambda_{n}\mathcal{L}_{\mathrm{norm}}+\lambda_{p}\mathcal{L}_{\mathrm{plate}}$$

- $\mathcal{L}_{\mathrm{surf}}=\sum_{j}\|\boldsymbol{\mu}_{j}-\mathbf{x}_{j}\|^{2}$ : 중심을 가장 가까운 메시 점으로 끌어당긴다.
- $\mathcal{L}_{\mathrm{norm}}=\sum_{j}\big(1-|\mathbf{n}^{\mathrm{s}}_{j}\cdot\mathbf{n}^{\mathrm{m}}_{j}|\big)$ : 가장 짧은 주축을 표면 법선과 나란히 맞춰, 판의 넓은 면이 표면에 접하게 한다.
- $\mathcal{L}_{\mathrm{plate}}=\sum_{j}\big([s_{j}^{(1)}-\tau_{h}]_{+}+[\tau_{\ell}-s_{j}^{(1)}]_{+}+\sum_{k=2}^{3}[\tau_{f}-s_{j}^{(k)}]_{+}\big)$ : 두께를 $[\tau_{\ell},\tau_{h}]$ 좁은 구간에 가두고 면내 두 축은 $\tau_{f}$ 이상으로 늘려, 얇고 넓은 **판(plate)** 모양이 되게 한다.

**(d) 바깥 법선 부여.** 법선 정렬 손실은 방향만 맞추고 부호는 정하지 못하므로, 중심을 메시에 투영해 얻은 바깥 법선 $\mathbf{n}^{m}_{j}$의 부호를 빌려 $\mathbf{n}_{j}=\mathrm{sgn}(\mathbf{n}^{\mathrm{s}}_{j}\cdot\mathbf{n}^{m}_{j})\,\mathbf{n}^{\mathrm{s}}_{j}$로 확정한다.

### 2) Morpho-Kinematic 로봇 기술자
DRO를 따라 각 임바디먼트를 표준 자세의 링크 메시에서 farthest point sampling으로 뽑은 $N=256$개 표면 키포인트로 표현하고, 순기구학으로 자세 $\mathbf{q}$에서의 위치를 얻는다.

$$\mathcal{P}_{e}(q)=\{\mathbf{p}_{i}(q)\}_{i=1}^{N}\subset\mathbb{R}^{3}$$

DRO가 대조 학습으로 **자세 불변 형태 대응(morphology identity)** 만 학습한 것과 달리, 여기에 **기구학 인지(kinematic awareness) 목적함수**를 추가로 걸어 자세가 바뀔 때의 움직임까지 예측 가능한 기술자를 사전학습한다. 그래서 "어떻게 생겼는가 + 어떻게 움직이는가"를 함께 담는다는 뜻으로 morpho-kinematic이라 부른다.

### 3) 마할라노비스 상호작용 장
모델 $f_{\theta}$는 초기 자세 $\mathbf{q}^{0}$의 손 키포인트 $\mathbf{P}^{0}_{e}$와 물체 프리미티브 $\mathcal{G}$를 받아 행렬 $\hat{\mathbf{M}}\in\mathbb{R}_{+}^{N\times G}$을 낸다. 각 성분 $\hat{M}_{ij}$는 목표 파지 상태에서 키포인트 $i$와 프리미티브 $g_{j}$ 사이의 **마할라노비스 거리**다. 유클리드 거리와 달리 각 프리미티브의 국소 좌표계와 이방성 스케일을 그대로 쓰기 때문에

- **접평면 안에서는 완만하게**, **법선 방향으로는 급격하게** 값이 오르고,
- 넓적한 평면 프리미티브는 옆으로 여유를 크게 주고, 작고 조밀한 프리미티브는 위치를 엄격히 제한한다.

즉 "표면을 따라 조금 미끄러지는 것은 괜찮지만 표면에서 떨어지는 것은 안 된다"는 접촉의 방향 비대칭성을 거리 자체에 심었다.

네트워크는 프리미티브 중심 위의 KNN 그래프에서 동작하는 지역 어텐션 블록 스택 + 전역 self-attention으로 물체 특징 $\mathbf{F}^{O}$를 뽑고, 사전학습된 로봇 인코더가 $\mathbf{F}^{R}$을 뽑은 뒤, Interaction Fields Generator가 둘을 융합해 $\hat{\mathbf{M}}$을 만든다.

### 4) 최적화 기반 파지 실현
예측한 장을 안내 신호로 삼아 $\mathbf{q}^{0}$에서 출발해 최적화한다.

$$\mathbf{q}^{*}=\arg\min_{\mathbf{q}\in\mathcal{Q}_{e}}\mathcal{L}_{\mathrm{rec}}\big(\mathbf{q};\hat{\mathbf{M}},\mathcal{G}\big)$$

$\mathcal{Q}_{e}=\{\mathbf{q}\mid\underline{\mathbf{q}}_{r}\leq\mathbf{q}_{r}\leq\overline{\mathbf{q}}_{r}\}$는 회전 관절 한계이고, $\mathcal{L}_{\mathrm{rec}}$는 마할라노비스 장 안내 항에 관통(penetration)·자기 충돌(self-collision) 에너지를 더한 것이다. 이 최적화 설정과 하이퍼파라미터는 **모든 임바디먼트에서 동일하게** 쓴다.

## 실험 결과 / 연구 의의
평가는 CMAP(GenDexGrasp)과 MultiGripperGrasp 두 벤치마크, 학습에 쓴 손 3종(ShadowHand, Allegro, Barrett)과 처음 보는 손 1종(SharpaWave)으로 진행했다.

| 설정 | CMAP | MultiGripperGrasp |
|---|---|---|
| Seen hands (시뮬레이션 성공률) | 97.59% | 89.47% |
| Unseen hand: SharpaWave (zero-shot) | 84.17% | 81.47% |

- 학습에 쓴 손 기준으로 가장 강한 베이스라인 대비 최대 **8.24%p** 향상.
- 처음 보는 SharpaWave 손으로의 zero-shot 전이에서 가장 강한 zero-shot 베이스라인 대비 최대 **16.57%p** 향상.
- 실제 하드웨어(SharpaWave)에서 **실물 데이터 파인튜닝 없이 86% 성공률**.
- Ablation으로 제안한 각 구성요소의 기여를 검증했다고 보고한다.

의의는 세 가지다. 첫째, 렌더링용으로 만들어진 3DGS를 **접촉 모델링용 기하 표현**으로 재해석해, 기하 복잡도에 따라 표현 용량을 스스로 배분하면서 국소 접평면-법선 구조까지 보존하는 고정 크기 표현을 얻었다. 둘째, 접촉의 방향 비대칭성을 손실 함수가 아니라 **거리 정의 자체**에 넣어 이방성을 얻었다. 셋째, 손마다 튜닝하지 않고 하나의 최적화 설정으로 이질적 손 전반을 커버하며 실물까지 바로 배포된다는 것을 보였다.

## 한계
> 논문의 Conclusion 및 실험 상세(표·ablation 수치)는 본문 확보 과정에서 접근 제한(HTTP 429)으로 끝까지 읽지 못했다. 따라서 **저자가 명시한 한계는 확인하지 못했다.** 아래는 확보한 본문(Abstract~Sec. III-C)에 근거한 관찰이다.

- **완전한 물체 메시가 필요하다.** Gaussian 구성 파이프라인이 메시에서 렌더링한 법선 맵·깊이 맵을 supervision으로 쓰고, 표면 정렬 손실도 메시 위 최근접 점과 법선을 참조한다. 즉 실제 로봇이 카메라로 본 **부분 관측 점군만으로 바로 돌아가는 구조가 아니다.** 논문은 이 부분을 언급하지 않는다.
- **물체마다 별도의 3DGS 최적화가 선행된다.** 밀도화 → 선택 → 정련의 3단계를 물체별로 돌려야 하므로, 새 물체에 대한 온라인 지연이 있을 수 있다. 논문에 시간 비용에 대한 명시적 언급은 확보 범위 안에 없다.
- **고정 예산 $G=256$, 키포인트 $N=256$** 은 상호작용 행렬 크기를 고려해 경험적으로 정한 값이다. 매우 크거나 매우 복잡한 물체에서 이 예산이 충분한지는 확보 범위 안에서 검증되지 않는다.
- 실물 실험은 **미지의 손 SharpaWave 1종**에 대한 것이고, 시뮬레이션 미지 손도 1종뿐이다. 임바디먼트 다양성 측면의 일반화 폭은 제한적으로 보인다.
- 파지 실현이 **초기 자세 $\mathbf{q}^{0}$에서 출발하는 지역 최적화**이므로 초기화 의존성이 있을 수 있다. 논문에 명시적 언급 없음.

## 우리 연구와 연결되는 점
직접적인 연결은 **Hand-Object Interaction**이다. 이 논문은 사람 손이 아니라 로봇 손을 다루지만, 문제 구조는 우리가 다루는 HOI와 거의 같다.

- **접촉을 이방성으로 모델링한다는 발상이 사람 손에도 그대로 옮겨간다.** 지금까지 HOI 접촉 표현은 거의 다 "손 정점–물체 점의 유클리드 거리 < 임계값" 형태의 등방성 근접도였다. 접선 방향(미끄러짐)과 법선 방향(분리)을 구분하는 마할라노비스 장은 MANO 정점–물체 표면 관계에도 바로 정의할 수 있고, 접촉 맵 예측이나 관통/부유(floating) 아티팩트 완화에 쓸 여지가 있다.
- **고정 개수의 방향성 Gaussian 판**은 물체를 다루는 가벼운 중간 표현으로 쓸 만하다. 점군보다 개수가 적으면서 법선과 국소 스케일을 갖고 있어, 손–물체 어텐션 계산량을 줄이면서도 표면 방향 정보를 유지한다. HOI 재구성이나 접촉 추론 모듈의 물체 인코더를 대체할 후보다.
- **Morpho-kinematic 기술자**의 "형태 정체성 + 자세 변화 시 움직임"을 함께 학습한다는 아이디어는, 손 모델이 서로 다른 데이터셋(MANO / 실제 손 스캔 / 로봇 손)을 넘나들어야 하는 상황에서 손 표현을 공유하는 방법으로 참고할 만하다.
- **Egocentric Vision과의 연결은 잠재적 관점이다.** 이 논문은 1인칭 영상이나 부분 관측을 전혀 다루지 않고 완전한 물체 메시를 전제한다. 다만 egocentric HOI에서 물체 기하가 부분적으로만 복원되는 상황에 이 이방성 장을 확장하면, 불확실한 표면 영역은 스케일을 크게 주어 자연스럽게 "허용 오차"로 표현할 수 있다는 방향은 생각해 볼 수 있다.
- **Spatial Audio와는 직접적 접점이 없다.** 굳이 잇는다면 접촉 순간(법선 거리 0 교차)이 접촉음 이벤트와 대응한다는 정도인데, 논문에 근거는 없는 순수한 추측이다.

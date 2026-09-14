# From Where to How: Continuous 4D Interaction Forecasting from Egocentric Video

**arXiv**: 2609.08636 | **주제 분류**: Egocentric Vision | **출판일**: 2026-09-08 | **학회**: 프리프린트 (abs 페이지에 Comments/발표처 언급 없음)
**저자/소속**: Qiaohui Chu, Haoyu Zhang, Meng Liu, Haoxiang Shi, Dongmei Jiang, Liqiang Nie (arXiv HTML 판본에 소속 정보가 표기되어 있지 않음)
**링크**: https://arxiv.org/abs/2609.08636

## 한 줄 요약

1인칭 영상에서 "앞으로 손이 어디를 만질지(where)"를 연속 3D 좌표열로 먼저 예측하고, 그 좌표열을 기하학적 조건으로 삼아 "몸이 어떻게 움직여 그것을 실현할지(how)"를 이어서 예측하는 2단계 프레임워크 HIGFlow와, 두 목표가 시간·좌표계상 정렬된 23만 샘플 규모 데이터셋 Coherent4D를 제안한다.

## 메인 그림

![HIGFlow의 2단계 구조: 1단계에서 미래 상호작용 위치열을 예측하고, 2단계에서 그 위치열을 조건으로 시간 정렬된 전신 포즈를 예측한다](https://arxiv.org/html/2609.08636v1/framework.png)

Fig. 5 (Overview of HIGFlow). 왼쪽 1단계는 관측된 ego 프레임·환경 서술자·위치 히스토리·태스크 프롬프트를 받아 미래 상호작용 위치 시퀀스를 회귀하고, 오른쪽 2단계는 그 예측 위치열을 조건으로 deterministic anchor + residual Flow Matching을 거쳐 전신 SMPL 포즈 시퀀스를 내놓는 cascaded 구조를 보여준다.

---

## 선행 연구

이 논문이 올라선 흐름은 크게 세 갈래다.

**1) 3D interaction location forecasting (손이 앞으로 어디를 만질지 예측)**

초기 연구는 대부분 2D 이미지 평면에서 손 궤적을 예측했다. OCT는 미래 2D 손 궤적과 interaction hotspot(손이 닿을 가능성이 높은 물체 위 영역)을 함께 예측했고, Diff-IP2D와 MADiff는 diffusion 및 ego-motion(카메라 착용자 본인의 움직임) 인지 모델링으로 미래의 불확실성을 다뤘다. 이후 metric 3D 공간으로 확장된 연구들이 나왔다 — USST는 RGB만으로 egocentric 3D hand trajectory forecasting을 정립했고, MMTwin은 MADiff 계열 diffusion을 멀티모달 3D 손 궤적 예측으로 확장했으며, Uni-Hand는 2D/3D waypoint 예측을 통합했다.

여기에 semantic·VLM 기반 접근이 붙는다. [HandsOnVLM](https://arxiv.org/abs/2412.13187)은 좌표를 언어 토큰으로 그냥 직렬화(serialize)하는 방식으로는 부족하다는 점을 보이고, 전용 hand token과 trajectory decoder를 썼다. 또 [V-JEPA 2.1](https://arxiv.org/abs/2603.14482) 같은 latent world representation 계열은 짧은 구간의 시공간 동역학(short-horizon dynamics)을 포착한다.

**2) Full-body pose forecasting (전신 포즈 예측)**

관측된 포즈 히스토리와 문맥 단서로부터 미래 전신 모션을 예측하는 흐름이다. MoGaze는 gaze(시선)와 장면 문맥을, STARS는 deterministic anchor와 mode 내 변동을 분리하는 구조를, T2P는 예측된 global trajectory에 local pose를 조건화하는 방식을, GAP3DS는 gaze 기반 affordance(물체가 허용하는 행동 가능성) 단서를 사용했다. 다양성을 늘리는 쪽으로는 SLD-HMP(제어 가능한 semantic latent direction 학습), BeLFusion, CoMusion, SkeletonDiffusion(골격 구조 prior로 해부학적 타당성 보존), [PrediFlow](https://arxiv.org/abs/2512.13903)(Flow Matching residual로 coarse 예측 정제) 등이 있다.

**3) 데이터셋**

EPIC-KITCHENS와 Ego4D는 행동 이해·예측 감독 신호를 대규모로 제공하지만, 순서가 있는 연속 3D 상호작용 위치와 시간 동기화된 전신 포즈를 짝지어 주지는 않는다. hand-centric 계열로는 EgoPAT3D/EgoPAT3Dv2(3D action target 예측), USST와 함께 공개된 EgoHandTrajPred, [EgoH4](https://arxiv.org/abs/2504.08654)(양손 3D 궤적+포즈), [EgoHaFL](https://arxiv.org/abs/2511.18127)(언어 기반 손 상태·포즈·궤적 주석), [EgoMAN](https://arxiv.org/abs/2512.16907)(6-DoF 손 궤적) 등이 있고, pose-centric 계열로는 MoGaze, GIMO, HARPER, Real-IM이 있다.

가장 가까운 선행 연구는 **FIction** (CVPR 2025)이다. 상호작용 위치 추정과 포즈 예측을 하나의 데이터셋·태스크 안에 묶은 첫 시도로, 미래 상호작용 위치를 **voxel occupancy(공간을 격자로 나눠 어느 칸이 활성화되는지)** 로 표현하고 후보 위치에 포즈 예측을 조건화했다.

## 문제 제기

논문은 기존 흐름의 빈틈을 네 가지로 정리한다.

**❶ Decoupled task formulation (태스크가 분리돼 있음).** 위치 단서와 모션 단서가 둘 다 있어도, 기존 예측기들은 interaction localization과 pose forecasting을 독립적이거나 느슨하게만 연결된 목표로 다룬다. 그 결과 "연속적으로 예측된 상호작용 위치"가 이후 모션 예측의 기하학적 제약으로 명시적으로 전달되지 않는다. 어디서 상호작용이 전개되는지와 그것을 몸이 어떻게 물리적으로 실현하는지 사이의 협응이 끊긴다.

**❷ Spatiotemporal pairing gap (시공간 짝짓기 공백).** 기존 데이터셋은 순서가 있는 연속 3D 손 상호작용 위치를, **같은 미래 타임스탬프**에 **같은 metric 좌표계**로 표현된 전신 포즈와 짝지어 주는 경우가 거의 없다. 그래서 모델이 위치와 몸 동작이 어떻게 함께 변해가는지를 직접 학습하거나 평가할 수 없다.

**❸ Semantic-dynamic localization gap (의미 이해와 정밀 좌표 사이의 간극).** 정확한 위치 예측에는 태스크 수준의 semantic grounding(지금 무슨 작업 중이고 어떤 물체가 관련 있는지)과 미래 시점별 정밀한 연속 3D 좌표가 모두 필요하다. 그런데 VLM(vision-language model) 표현은 의미 추론에 최적화돼 있지 metric 좌표 회귀에 맞춰져 있지 않고, 짧은 구간의 시각적 동역학도 충분히 담지 못한다. 이 불일치가 "의미적으로는 그럴듯한데 공간적으로는 틀린" 예측을 낳는다.

**❹ Pose diversity-structure trade-off (다양성과 구조 안정성의 상충).** deterministic 포즈 예측은 골격 구조는 잘 지키지만 "다르게 해도 되는" 대안적 실행 방식을 눌러버린다. 반대로 stochastic 생성은 여러 가능한 미래를 포착하지만 골격 구조나 관절 일관성을 깨뜨릴 수 있다.

특히 FIction조차 위치를 이산 voxel로 표현하고 개별 후보 위치에 포즈를 조건화하기 때문에, 변해가는 상호작용 목표와 그것을 실현하는 몸 동작 사이의 **단계별(stepwise) 대응**은 여전히 미해결로 남는다.

## 연구 주제

이 논문이 새로 세우는 문제 정의는 **continuous 4D interaction forecasting** 이다. 여기서 "continuous"는 두 가지를 동시에 뜻한다 — (1) 모션 시퀀스의 시간적 연속성, (2) 이산 공간 격자가 아닌 연속 3D 좌표 사용.

기존 흐름과의 차이는 세 지점이다.

- **voxel → continuous metric 좌표.** FIction의 이산 occupancy 표현을 버리고 공유 좌표계 위의 연속 3D 좌표열로 문제를 다시 쓴다. 평가 지표도 voxel 정확도가 아니라 연속 공간의 mm 단위 오차로 바꾼다.
- **분리된 두 태스크 → cascaded where-to-how.** 위치 예측 결과를 포즈 예측의 명시적 기하 조건으로 흘려보내, 두 예측 사이에 직접적 의존성을 만든다.
- **개별 후보 위치 → 시간 정렬된 시퀀스 쌍.** 각 미래 스텝 $k$마다 상호작용 위치 $\mathbf{y}_k \in \mathbb{R}^3$와 그 시점의 SMPL 전신 상태 $\mathbf{X}_k$가 1:1로 붙어 있다.

## 연구 방법

### A. Coherent4D 데이터셋

**출처와 구성.** Ego-Exo4D의 동기화된 procedural take에서 구축한다. Aria ego 스트림이 예측 입력이고, 동기화된 exocentric(3인칭) 뷰는 오프라인 주석 생성·정제에만 쓴다(모델 입력 아님). 각 샘플은 30초 관측 윈도우에서 균일 샘플링한 **30장의 ego 프레임**, 구조화된 물체·환경 서술자, 관측된 상호작용 위치 히스토리와 SMPL 포즈 히스토리, 그리고 미래 위치·포즈 타깃으로 이루어진다.

**주석 파이프라인 (5단계, Fig. 3)**

1. **Scene object grounding.** Detic + LVIS vocabulary로 ego 프레임에서 물체를 검출하고, Ego-Exo4D SLAM 재구성으로 3D로 lift한 뒤 클러스터링해 oriented 3D bounding box를 얻는다. 각 물체는 의미 카테고리와 연속 3D box 속성(center, size, orientation)을 갖는다 — 환경을 voxel로 이산화하지 않는다.
2. **Shared coordinate construction.** 샘플 $n$마다 안정적인 ego 기준 pose $(\mathbf{R}_n^{\text{ref}}, \mathbf{t}_n^{\text{ref}})$를 정의하고, 세계 좌표 점 $\mathbf{p}_w$를 sample-local 좌표로 옮긴다: $\mathbf{p}_n^{\text{loc}} = (\mathbf{R}_n^{\text{ref}})^\top (\mathbf{p}_w - \mathbf{t}_n^{\text{ref}})$. 상호작용 위치, 물체 중심, SMPL root translation, 3D 관절에 모두 적용한다. 모델 입출력용으로는 $s = 5\,m$로 나눈 뒤 각 좌표를 $[-1, 1]$로 클리핑한다. 단, SMPL의 23개 body joint 회전은 부모 관절 기준 상대 표현을 그대로 유지한다.
3. **Location sequence construction.** 희소한 hand-object 상호작용 주석을 시간 순서의 연속 3D 위치열로 바꾼다. FIction을 따라 narration 타임스탬프 + Llama 3 기반 물체 매칭 + 손-물체 기하 일관성으로 후보 이벤트를 찾고, 손 mesh에서 연속 3D 위치를 복원한다. 오른손/양손 상호작용은 하나의 스트림으로 통합하고, 시간적으로 인접하면서 공간적으로 중복되는 이벤트는 병합한다.
4. **SMPL state attachment.** WHAM으로 인체 모션을 복원하고 주 행위자 트랙을 골라 Ego-Exo4D 좌표계에 정렬한다. 관측·미래 각 타임스탬프마다 가장 가까운 유효 SMPL 상태(root translation, root orientation, body joint rotation, 3D joint position)를 붙여 sample-local 좌표로 변환한다.
5. **Forecast sample generation.** 첫 미래 상호작용 타임스탬프 $t_{n,1}$을 시간 원점으로 삼고, 그 직전 30초를 관측 윈도우로 쓴다. 각 미래 스텝의 절대 시각, 상대 시각 $\Delta t_{n,k} = t_{n,k} - t_{n,1}$, 연속 위치, 정렬된 SMPL 상태를 보존한다. **상대 타임스탬프를 남겨 상호작용 이벤트 사이의 비균일한 간격을 그대로 유지**하는 점이 특징이다. 꼬리가 짧은 시퀀스는 padding + validity mask로 처리하고, take 단위로 split해 학습/검증/테스트 간 환경·절차 중복을 막는다.

**통계 (Table I)**

| Domain | Horizon | Takes | Train | Val | Test | Total | Targets | Obj. |
|---|---|---|---|---|---|---|---|---|
| Cooking | 10 | 331 | 136,079 | 15,435 | 14,527 | 166,041 | 1,337,589 | 428 |
| Health | 5 | 205 | 21,532 | 1,899 | 4,167 | 27,598 | 114,964 | 170 |
| Bike Repair | 4 | 251 | 35,987 | 3,150 | 1,052 | 40,189 | 141,633 | 197 |
| Total | – | 787 | 193,598 | 20,484 | 19,746 | 233,828 | 1,594,186 | 535 |

총 233,828 샘플, 787개 take, 535개 상호작용 물체 카테고리. 유효 미래 타깃 1,594,186개는 모두 narration과 정렬되며, 첫 동사 분포는 pick, place, hold, drop, move, pour, pass, turn 같은 조작 primitive를 덮는다(Fig. 4).

**연속 공간 평가 지표**

- 위치: **ADE**(유효 미래 스텝 평균 변위 오차), **ADE₉₀**(샘플별 ADE의 90번째 백분위수 — 상위 꼬리 오차), **FDE**(마지막 유효 스텝 오차). 모두 mm.
- 포즈: **MPJPE**(관절 위치 오차, $J_{\text{pos}}=19$ 관절), **PA-MPJPE**(Procrustes 정렬 후 오차 — 전역 위치/회전/스케일 어긋남을 제거한 관절 배치 정확도), **Root Trans.**(root translation 오차, 전역 몸 이동 정확도), **Body Geo.**(root 제외 $J_{\text{rot}}=23$ 관절의 geodesic 각도 오차, degree).
- 미래 모션의 multimodality를 반영해 **Single**(첫 후보)과 **Best-5**(5개 후보 중 샘플 단위 MPJPE가 가장 낮은 것)를 함께 보고한다. Best-5의 모든 지표는 동일하게 선택된 하나의 시퀀스에서 계산해 지표 간 일관성을 유지한다.

### B. HIGFlow 프레임워크

**문제 정식화.** 위치 단계 입력은 $\mathcal{C}_{\text{loc}} = (\mathcal{V}_{\text{obs}}, \mathcal{E}, \mathcal{O}_{\text{obs}}, \mathcal{T})$ = (ego 프레임, 구조화된 환경 서술자, 관측 위치 히스토리, 태스크 프롬프트). 출력은 $\hat{\mathcal{Y}} = \{\hat{\mathbf{y}}_k\}_{k=1}^{K}$. 포즈 단계는 $\hat{\mathcal{X}} = f_{\text{pose}}(\mathcal{H}_{\text{pose}}, \tilde{\mathcal{Y}})$이며, **학습 때는 $\tilde{\mathcal{Y}}$에 ground-truth 위치를, 추론 때는 1단계 예측 위치를 넣는다.** 각 $\hat{\mathbf{X}}_k \in \mathbb{R}^{147}$은 6D root orientation + 3D root translation + 23개 관절의 연속 6D 회전으로 구성된 SMPL 상태다.

#### B-1. Semantic-Dynamic Location Forecasting (where 단계)

핵심 아이디어는 **"의미 이해"와 "좌표 회귀"를 분리하고, 여기에 단기 시각 동역학을 따로 주입**하는 것이다.

- **Semantic context encoding.** Qwen3-VL-2B가 ego 프레임, 태스크 프롬프트, 위치 히스토리, 환경 서술자를 받는다. 위치·환경 인코더가 $\mathcal{O}_{\text{obs}}$와 $\mathcal{E}$를 dense feature로 바꿔 대응하는 placeholder embedding을 대체한다. 각 미래 스텝 $k$마다 `<hand_traj_k>` 위치의 hidden state $\mathbf{h}_k^Q$를 스텝별 semantic 표현으로 뽑는다.
- **Dynamic feature augmentation.** 얼어붙은(frozen) V-JEPA 2.1 ViT-Giant/384로 관측 영상을 인코딩해 Qwen hidden space로 투영하고 $M$개의 dynamic memory token으로 resample한다. 각 $\mathbf{h}_k^Q$가 학습된 step embedding $\mathbf{s}_k^{\text{loc}}$와 함께 이 메모리에 attend해 motion context $\mathbf{c}_k$를 얻고, **gated residual adapter**로 주입한다:

  $\mathbf{h}_k^F = \mathbf{h}_k^Q + g_k \Delta\mathbf{h}_k$, $\ \Delta\mathbf{h}_k = \alpha \tanh(D([\mathbf{h}_k^Q, \mathbf{c}_k, \mathbf{s}_k^{\text{loc}}]))$, $\ g_k = \text{sigmoid}(G([\mathbf{h}_k^Q, \mathbf{c}_k, \mathbf{s}_k^{\text{loc}}]))$

  $g_k \in (0,1)$이 동역학 기여도를 적응적으로 조절하고 $\alpha > 0$이 크기를 제한한다.
- **Continuous coordinate decoding.** 좌표 디코더가 $\mathbf{h}_k^F$를 정규화된 연속 3D 좌표 $\hat{\mathbf{y}}_k$로 직접 회귀한다. **metric 좌표를 텍스트 토큰으로 쓰지 않는다**는 점이 핵심 설계다.
- **학습 목표:** $\mathcal{L}_{\text{loc}} = \lambda_{\text{ADE}}\mathcal{L}_{\text{ADE}} + \lambda_{\text{S1}}\mathcal{L}_{\text{S1}} + \lambda_{\text{CE}}\mathcal{L}_{\text{CE}}$ — mask-aware ADE loss + Smooth L1 + 보조 language modeling loss. 가중치는 $(1.5, 0.6, 0.01)$. base predictor를 먼저 학습한 뒤 base/구조화 인코더/좌표 디코더를 얼리고 JEPA adapter만 따로 학습하는 순차 학습 방식을 쓴다.

#### B-2. Hand-Conditioned Residual Flow Matching (how 단계)

**"안정적인 결정론적 뼈대 + 그 주변의 제한된 확률적 변동"** 으로 diversity-structure 딜레마를 푼다.

- **Spatiotemporal conditioning.** 관측된 각 SMPL 상태를 root 1개 + 관절 23개 = **24-node 그래프**(골격 연결이 간선)로 표현해 graph propagation으로 물리적으로 연결된 부위 간 의존성을 잡고 SMPL 위상을 보존한다. 노드 feature를 frame-level pose token으로 pooling한 뒤 pose history Transformer에 넣어, 최종 CLS 토큰 상태 $\mathbf{h}$가 관측 모션 히스토리를 요약한다.
- **Future condition encoding.** 각 미래 스텝을 $\boldsymbol{\eta}_k = \text{MLP}_c([\tilde{\mathbf{y}}_k, \Delta\tilde{\mathbf{y}}_k, k/K])$로 인코딩(위치 + 변위 + 상대 스텝)하고 Transformer로 문맥화해 $\mathbf{f}_k$를 얻는다.
- **Deterministic anchor.** $\hat{\mathbf{X}}_k^a = \text{MLP}_a([\mathbf{h}, \mathbf{f}_k])$. 이 anchor는 최종 예측이 아니라, 상호작용 위치에 기하학적으로 뿌리내린 **기준 모션**이다. 학습 손실 $\mathcal{L}_{\text{anchor}}$는 6D 회전 $\ell_1$, 전체/루트/몸통 geodesic, translation, velocity, 3D joint position 항의 가중합이다. anchor 사전학습 후 pose history 인코더, future condition 인코더, anchor predictor는 **모두 동결**한다.
- **Residual Flow Matching.** anchor 대비 잔차 $\mathbf{r}_k^* = \text{Residual}(\hat{\mathbf{X}}_k^a, \mathbf{X}_k)$를 정의한다 — root/body 회전 보정은 상대 회전의 log map, root translation 보정은 뺄셈으로 계산해 3(root rot) + 3(root trans) + 69(23×3 body rot) = **75차원** 잔차 벡터가 된다.

  잔차 크기를 통제하기 위해 조건 $\mathbf{c}_k^{\text{flow}} = [\mathbf{h}, \mathbf{f}_k, P_a(\hat{\mathbf{X}}_k^a)]$에서 스텝별 게이트 $\boldsymbol{\gamma}_k = \boldsymbol{\gamma}_{\max} \odot \text{sigmoid}(\Gamma(\mathbf{c}_k^{\text{flow}}))$ (root 회전/root 이동/body 회전 3개 값)를 뽑고, 성분별 bound $\boldsymbol{\rho} = \text{concat}(\rho_R \mathbf{1}_3, \rho_t \mathbf{1}_3, \rho_B \mathbf{1}_{69})$로 클리핑하는 조절 연산자 $\mathcal{R}_k(\mathbf{x}) = \mathcal{B}_{\boldsymbol{\rho}}(\text{bcast}(\boldsymbol{\gamma}_k) \odot \mathbf{x})$를 적용한다.

  선형 probability path $\mathbf{x}_{\tau,k} = (1-\tau)\mathbf{z}_k + \tau \bar{\mathbf{r}}_k^*$ ($\tau \sim \mathcal{U}(0,1)$, $\mathbf{z}_k \sim \mathcal{N}(\mathbf{0}, \sigma_r^2 \mathbf{I}_{75})$) 위에서 conditional velocity field를 $\mathcal{L}_{\text{FM}} = \mathbb{E}[\|v(\mathbf{x}_{\tau,k}, \tau, \mathbf{c}_k^{\text{flow}}) - (\bar{\mathbf{r}}_k^* - \mathbf{z}_k)\|_2^2]$로 학습한다.
- **Endpoint 감독.** 중간 flow 상태에서 직접 추정한 잔차(direct)와, Gaussian prior에서 미분 가능한 $N_{\text{ODE}}$-step Heun rollout으로 얻은 잔차(roll)를 둘 다 anchor와 합성(Compose: 회전은 exponential map, translation은 덧셈)해 포즈 손실을 건다. 최종 목표는 $\mathcal{L}_{\text{pose}} = \lambda_{\text{FM}}\mathcal{L}_{\text{FM}} + \lambda_{\text{direct}}\mathcal{L}_{\text{direct}} + \lambda_{\text{roll}}\mathcal{L}_{\text{roll}} + \lambda_{\text{res}}\mathcal{L}_{\text{res}}$ ($\lambda_{\text{FM}} = \lambda_{\text{direct}} = \lambda_{\text{roll}} = 1.0$, $\lambda_{\text{res}} = 0.5$).
- **추론.** 독립적으로 $S=5$개의 residual prior를 샘플링해 각각 $N_{\text{ODE}}=4$ Heun step으로 적분하고 anchor와 합성해 5개의 그럴듯한 미래 모션을 만든다.

**구현 세부.** $M=64$ V-JEPA 메모리 토큰, $\alpha=0.1$, 3층 좌표 디코더, pose history/future condition Transformer 각각 4층/2층, $\sigma_r = 0.003$, AdamW, 전체 실험은 **NVIDIA A100 6장**에서 수행.

## 실험 결과 / 연구 의의

### 1) 상호작용 위치 예측 (Table II, 단위 mm, 낮을수록 좋음)

| Model | Health ADE | Health ADE₉₀ | Health FDE | Bike ADE | Bike ADE₉₀ | Bike FDE | Cooking ADE | Cooking ADE₉₀ | Cooking FDE |
|---|---|---|---|---|---|---|---|---|---|
| FIction | 40.30 | 62.62 | 40.58 | 88.55 | 143.21 | 98.61 | 100.61 | 184.63 | 107.11 |
| Qwen3-VL | 57.53 | 89.54 | 82.04 | 90.71 | 156.55 | 103.81 | 103.95 | 199.20 | 112.22 |
| V-JEPA | 45.18 | 69.49 | 46.26 | 86.50 | 142.43 | 96.33 | 102.33 | 194.80 | 107.35 |
| Diff-IP3D | 292.84 | 433.26 | 294.25 | 525.63 | 842.93 | 561.19 | 647.23 | 1268.28 | 662.71 |
| MMTwin | 290.45 | 437.88 | 285.21 | 429.71 | 690.80 | 480.29 | 513.75 | 957.17 | 556.40 |
| **HIGFlow** | **40.21** | **59.52** | 41.44 | **80.91** | **131.87** | **93.78** | **93.46** | **178.20** | **104.26** |

읽을 점: (a) HIGFlow가 대부분 지표에서 1위이며, Cooking ADE는 FIction 대비 100.61 → 93.46 mm, Bike Repair는 88.55 → 80.91 mm로 개선된다. (b) Health FDE만 FIction(40.58)이 근소하게 낫다. (c) 손 궤적 diffusion 계열(Diff-IP3D, MMTwin)은 이 설정에서 수백 mm 단위로 크게 무너진다 — 짧은 궤적 회귀에 맞춰진 모델을 비균일 간격의 "상호작용 이벤트 위치열" 예측으로 옮기면 잘 동작하지 않는다는 뜻이다. (d) Qwen3-VL 단독(semantic만)과 V-JEPA 단독(dynamics만) 모두 HIGFlow보다 못하다 — 두 신호를 합쳐야 한다는 논문 주장의 직접 근거다.

### 2) 전신 포즈 예측 (Table III, MPJPE/PA-MPJPE/Root Trans.는 mm, Body Geo.는 degree)

**(a) GT 위치로 조건화한 경우 (upper bound 성격의 통제 실험)**

| Domain / Model | MPJPE (Single) | MPJPE (Best-5) | PA-MPJPE (Single) | Root Trans. (Single) | Body Geo. (Single) |
|---|---|---|---|---|---|
| Health / FIction | 117.17 | 115.91 | 42.12 | 104.09 | 9.03 |
| Health / SkeletonDiffusion | 166.32 | 137.39 | 53.18 | 158.85 | 10.55 |
| Health / SLD-HMP | 421.56 | 88.38 | 44.79 | 403.30 | 8.76 |
| Health / **HIGFlow** | **95.25** | 93.45 | 43.79 | **80.93** | 8.80 |
| Bike / FIction | 295.34 | 284.52 | 78.95 | 292.07 | **13.60** |
| Bike / SkeletonDiffusion | 453.52 | 370.26 | 113.22 | 405.49 | 17.69 |
| Bike / SLD-HMP | 269.06 | 234.95 | 74.34 | 261.00 | 11.97 |
| Bike / **HIGFlow** | **213.65** | **210.09** | **70.07** | **224.19** | 15.05 |
| Cooking / FIction | 237.86 | 226.62 | 43.81 | 227.23 | 8.34 |
| Cooking / SkeletonDiffusion | 310.39 | 260.00 | 51.43 | 278.05 | 11.42 |
| Cooking / SLD-HMP | 184.42 | 167.19 | 43.41 | 174.33 | 7.67 |
| Cooking / **HIGFlow** | **143.98** | **143.41** | **39.45** | **139.26** | **7.53** |

**(b) 예측 위치로 조건화한 경우 (실제 forecasting 설정)**

| Domain / Model | MPJPE (Single) | MPJPE (Best-5) | PA-MPJPE (Single) | Root Trans. (Single) | Body Geo. (Single) |
|---|---|---|---|---|---|
| Health / FIction | 124.59 | 123.43 | 50.82 | 108.67 | **9.01** |
| Health / SkeletonDiffusion | 184.97 | 155.55 | 55.01 | 172.37 | 10.89 |
| Health / SLD-HMP | 402.76 | 92.15 | 48.66 | 381.66 | 8.56 |
| Health / **HIGFlow** | **119.96** | **118.14** | **47.06** | **94.19** | 9.33 |
| Bike / FIction | 351.64 | 341.06 | 86.75 | 325.06 | **14.14** |
| Bike / SkeletonDiffusion | 469.82 | 398.82 | 115.09 | 408.17 | 17.89 |
| Bike / SLD-HMP | 358.20 | 314.88 | 83.82 | 311.54 | 12.39 |
| Bike / **HIGFlow** | **306.92** | **303.07** | **82.26** | **287.24** | 16.07 |
| Cooking / FIction | 374.89 | 364.15 | 46.30 | 348.70 | 8.51 |
| Cooking / SkeletonDiffusion | 421.75 | 382.35 | 53.09 | 377.64 | 11.89 |
| Cooking / SLD-HMP | 358.92 | 342.11 | **44.86** | 332.74 | **7.83** |
| Cooking / **HIGFlow** | **340.72** | **340.24** | 45.65 | **312.56** | 8.50 |

읽을 점: (a) 실전 설정에서 HIGFlow가 MPJPE와 Root Trans.를 전 도메인에서 최소로 만든다 — 특히 Cooking Root Trans. 348.70 → 312.56 mm. (b) **Body Geo.(관절 회전 각도)에서는 HIGFlow가 최고가 아니다.** Bike Repair에서 SLD-HMP 12.39°, FIction 14.14° 대비 HIGFlow는 16.07°다. 즉 HIGFlow의 강점은 "몸이 어디로 가는가(전역 이동·관절 위치)"이고, 국소 관절 회전 미세도는 상대적 약점이다. (c) SLD-HMP는 Single과 Best-5 격차가 극단적이다(Health Single 402.76 vs Best-5 92.15) — 샘플 분산이 너무 커서 한 번 뽑아서는 쓸 수 없다는 뜻이고, HIGFlow는 Single ≈ Best-5(119.96 vs 118.14)로 안정적이다. 이것이 residual bounding의 효과를 가장 잘 보여주는 숫자다. (d) GT 위치 → 예측 위치로 바꾸면 모든 방법의 성능이 나빠진다 — **1단계 localization 품질이 2단계 포즈 예측을 직접 좌우한다**는 cascaded 구조의 특성이 그대로 드러난다.

### 3) Ablation

**V-JEPA residual fusion (Table IV, mm)**

| Domain | V-JEPA | ADE | ADE₉₀ | FDE |
|---|---|---|---|---|
| Health | – | 40.28 | 59.34 | 41.47 |
| Health | ✓ | 40.21 | 59.52 | 41.44 |
| Bike Repair | – | 81.18 | 134.10 | 94.03 |
| Bike Repair | ✓ | 80.91 | 131.87 | 93.78 |
| Cooking | – | 94.20 | 178.21 | 104.83 |
| Cooking | ✓ | 93.46 | 178.20 | 104.26 |

효과는 일관되지만 **폭은 작다**(Cooking ADE 0.74 mm, Bike ADE 0.27 mm). 논문은 Bike Repair에서 가장 두드러진다고 서술한다.

**표현/디코딩 ablation (Table VII, ADE만 발췌, mm)**

| Variant | LocEnc | EnvEnc | CoordDec | Health | Bike | Cooking |
|---|---|---|---|---|---|---|
| Qwen3-VL | – | – | – | 57.53 | 90.71 | 103.95 |
| w/o CoordDec | ✓ | ✓ | – | 57.11 | 99.64 | 113.87 |
| w/o LocEnc | – | ✓ | ✓ | 42.57 | 87.78 | 97.29 |
| w/o EnvEnc | ✓ | – | ✓ | 42.17 | 87.65 | 100.13 |
| **HIGFlow (Full)** | ✓ | ✓ | ✓ | **40.21** | **80.91** | **93.46** |

**CoordDec(연속 좌표 회귀 헤드)가 압도적으로 중요하다.** 좌표를 언어 인터페이스로 생성하면 Cooking ADE가 93.46 → 113.87 mm로 무너진다. HandsOnVLM이 지적한 "좌표를 텍스트로 쓰면 안 된다"는 관찰과 정확히 일치한다.

**입력 ablation (Table VIII, ADE만 발췌, mm)**

| Input | Health | Bike | Cooking |
|---|---|---|---|
| w/o Env. | 37.40 | 114.51 | 97.92 |
| w/o Loc. | 69.48 | 135.71 | 143.82 |
| w/o Frames | 51.91 | 143.90 | 145.86 |
| **Full** | 40.21 | 80.91 | 93.46 |

위치 히스토리와 프레임 입력을 빼면 성능이 크게 떨어진다. 환경 문맥은 **Bike Repair에서 특히 중요**하다(80.91 → 114.51). 흥미롭게도 **Health에서는 환경 문맥을 빼는 편이 더 낫다**(40.21 → 37.40) — 도메인마다 유용한 문맥이 다르다는 신호다.

**V-JEPA 토큰 예산 (Table VI).** $M \in \{16, 32, 64, 128\}$에서 성능이 단조 증가하지 않는다. $M=64$가 Bike Repair에서 최고(ADE 80.91)이고 나머지 도메인에서도 경쟁력 있어 기본값으로 채택.

**포즈 단계 component ablation (Fig. 7).** 미래 상호작용 위치 조건화를 없앨 때 성능 저하가 가장 크다 — **위치가 전신 모션의 기하학적 가이드로서 핵심**이라는 논문의 메인 주장을 뒷받침한다. anchor는 구조적 안정성을, residual flow matching은 추가적 모션 변동과 정확도를 담당하며, 둘의 결합이 가장 균형 잡혀 있다.

**ODE step (Fig. 8).** $N_{\text{ODE}} \in \{1,2,4,8,16\}$ 중 **4 step이 12개 도메인-지표 쌍 중 9개에서 최고**이고 평균 regret도 최소다. 스텝을 늘려도 오차가 일관되게 줄지 않는다.

### 4) 도메인별 개선 폭 차이의 이유 (Table V)

| Domain | Loc. Disp. (mm) | Root Disp. (mm) | Spatial pattern |
|---|---|---|---|
| Health | 153.86 | 59.45 | 공간 이동이 좁음 |
| Bike Repair | 293.53 | 195.71 | 도구 중심의 뻗기·수리 동작 |
| Cooking | 318.69 | 171.48 | 물체 중심의 넓은 이동 |

HIGFlow의 이득은 Cooking·Bike Repair에서 크고 Health에서 작다. 이유는 명확하다 — Health는 연속 스텝 간 변위가 작아(153.86 / 59.45 mm) 기존 방법도 이미 잘 하고, 개선 여지가 적다. 반대로 변위가 크고 기하·동역학 단서가 풍부한 도메인에서 HIGFlow의 설계가 힘을 발휘한다.

### 5) 정성 분석 (Fig. 6)

- **Bike Repair**: HIGFlow는 초기 예측 구간에서 구부린 작업 자세를 유지하다가 ground truth에 가까운 시점에 서는 자세로 전환한다. FIction은 너무 일찍 몸을 세운다.
- **Cooking**: HIGFlow가 예측 위치를 올바른 작업 공간에 더 자주 배치하고, 참조 모션에 가까운 몸 이동과 뻗기 자세를 낸다.

### 연구 의의 요약

1. **"where"를 "how"의 명시적 기하 조건으로 쓰면 실제로 도움이 된다** — 위치 조건화 제거가 포즈 단계 ablation 중 가장 큰 성능 저하를 일으켰다.
2. **VLM은 semantic grounding에만 쓰고 좌표는 전용 회귀 헤드로 뽑아야 한다** — CoordDec ablation이 가장 큰 폭의 근거.
3. **diversity와 structure는 "anchor + bounded residual"로 동시에 얻을 수 있다** — SLD-HMP의 Single/Best-5 격차 vs HIGFlow의 안정성 비교가 직접 증거.
4. **연속 metric 좌표계 + 시간 정렬 쌍 데이터셋**이 있어야 이 문제를 제대로 학습·평가할 수 있다는 것을 Coherent4D로 보였다.

## 한계

**논문이 스스로 밝힌 것**

- **오차 전파 (error propagation).** cascaded 구조 탓에 위치 예측 오차가 forecasting horizon을 따라 커지고, 그것이 포즈 단계로 그대로 넘어간다. Bike Repair 후반 프레임에서 예측된 몸이 참조의 기울이고 뻗는 동작을 따라가지 못하고 지나치게 곧게 선 상태로 남는 사례가 관찰된다.
- **위치는 맞지만 "어떻게 닿는지"는 틀린다.** Cooking에서 HIGFlow는 올바른 상호작용 영역을 자주 찾아내지만, **어느 손으로 닿는지, 접촉 높이, 팔 구성, 몸통 방향**이 ground truth와 다를 수 있다. 논문은 이를 "상호작용 위치 조건화가 coarse spatial alignment는 개선하지만 인간의 의도(intent), 물체 affordance, 세밀한 접촉 제약(contact constraint)은 충분히 포착하지 못한다"고 정리한다.
- Conclusion에서 future work으로 **human intent modeling**과 **contact-aware conditioning**을 통해 더 긴 horizon에서 물리적으로 일관된 예측을 하겠다고 밝힌다.

**표에서 명백하게 드러나는 것**

- **Body Geo.(관절 회전)에서 HIGFlow가 최고가 아니다.** Bike Repair 예측 위치 설정에서 HIGFlow 16.07° vs SLD-HMP 12.39°, FIction 14.14°. 전역 이동은 잘 맞추지만 국소 관절 각도는 경쟁 방법이 더 낫다.
- **V-JEPA residual fusion의 효과가 작다.** ADE 개선 폭이 0.07~0.74 mm 수준이라 ViT-Giant/384급 인코더를 붙이는 비용 대비 이득이 크다고 보기 어렵다.
- **Health 도메인의 이득이 미미하다.** ADE 40.30 → 40.21 mm (FIction 대비), FDE는 오히려 41.44 vs 40.58로 밀린다.
- **도메인별 하이퍼파라미터 튜닝 의존.** Bike Repair는 $\lambda_{\text{rootgeo}} = \lambda_{\text{bodygeo}} = 0$, 다른 batch size(12 vs 1), 다른 dropout(0.15 vs 0.10), 다른 residual bound를 쓴다. 도메인 간 전이 가능성은 검증되지 않았다.
- **데이터셋 주석이 파생적(derived)이다.** 상호작용 위치는 손 mesh에서, SMPL 상태는 WHAM 재구성에서 나온다. 즉 ground truth 자체가 off-the-shelf 모델의 추정 결과이며, 그 오차가 상한선으로 작용한다.
- **도메인 불균형.** Cooking이 166K 샘플로 전체의 71%를 차지하는 반면 Health는 27.6K다. Bike Repair 테스트셋은 1,052 샘플로 작다.
- **오디오를 전혀 쓰지 않는다.** Ego-Exo4D는 오디오를 포함하지만 이 연구의 입력에 오디오는 없다.

## 우리 연구와 연결되는 점

**Egocentric Vision 관점**

- **Ego-Exo4D 활용 방식이 참고할 만하다.** ego 스트림은 모델 입력, exo 뷰는 오프라인 주석 생성·정제 전용으로 쓰는 비대칭 설계다. 3인칭 뷰를 "학습 시 supervision 생성기"로만 쓰고 추론 시에는 완전히 ego-only를 유지하는 패턴은, ego 데이터에 고품질 3D 라벨을 붙이기 어려운 거의 모든 문제에 그대로 이식할 수 있다.
- **sample-local 공유 좌표계 구성**($\mathbf{p}_n^{\text{loc}} = (\mathbf{R}_n^{\text{ref}})^\top (\mathbf{p}_w - \mathbf{t}_n^{\text{ref}})$, $s=5\,m$ 정규화 후 $[-1,1]$ 클리핑)은 카메라가 계속 움직이는 ego 세팅에서 손·몸·물체·장면을 하나의 metric 공간에 올리는 실용적 레시피다.
- **VLM을 좌표 예측에 쓰는 올바른 방법**에 대한 명확한 실험 근거를 준다. Qwen3-VL의 hidden state를 뽑되 좌표는 전용 회귀 헤드로 디코딩해야 하고, 좌표를 텍스트로 생성하면 base VLM보다도 나빠질 수 있다(Cooking ADE 103.95 → 113.87). ego 영상에 VLM을 붙여 공간 예측을 하려는 모든 연구가 먼저 확인해야 할 지점이다.
- **비균일 시간 간격을 보존하는 설계.** 상대 타임스탬프 $\Delta t_{n,k}$를 유지해 "고정 fps 프레임 예측"이 아니라 "이벤트 단위 예측"으로 문제를 잡은 것이, 실제 procedural activity의 리듬에 더 가깝다.

**Hand-Object Interaction 관점**

- 이 논문은 손 궤적 예측(3D hand trajectory forecasting) 연구와 전신 모션 예측(human motion prediction) 연구를 잇는 다리를 놓는다. HOI를 연구한다면, 손만 보던 시야를 "손이 가는 곳 → 몸 전체가 그것을 어떻게 만드는가"로 넓히는 이 프레이밍 자체가 유용한 확장 축이다.
- 동시에 **가장 큰 한계가 바로 HOI의 핵심 부분**이라는 점이 역설적으로 연구 기회다. 논문 스스로 "올바른 영역은 찾지만 어느 손인지, 접촉 높이, 팔 구성, 몸통 방향은 틀릴 수 있다"고 인정한다. 즉 contact point, grasp type, affordance 수준의 정밀한 HOI 모델링을 이 cascaded 구조에 3단계로 덧붙이는 것은 곧바로 후속 연구가 된다.
- **anchor + bounded residual 패턴**은 HOI 생성 문제에 일반적으로 쓸 수 있다. 손 자세나 접촉 구성처럼 "구조는 반드시 지켜야 하지만 여러 답이 가능한" 출력에 적합하다. 특히 residual을 성분별 bound($\rho_R$, $\rho_t$, $\rho_B$)로 다르게 제한하고 스텝별 게이트로 크기를 조절하는 설계는, "회전은 조금만, 이동은 크게 허용" 같은 도메인 지식을 명시적으로 주입할 수 있게 해준다.
- SMPL 상태를 **24-node 골격 그래프**로 인코딩해 graph propagation을 쓰는 부분은 손 모델(MANO)의 관절 그래프에도 동일하게 적용 가능하다.

**Spatial Audio 관점**

- **이 논문에 오디오는 전혀 없다** — 입력은 ego 프레임, 환경 서술자, 위치 히스토리, 태스크 프롬프트뿐이다. 바로 그 부재가 기회다.
- Coherent4D의 소스인 Ego-Exo4D는 멀티채널 오디오를 포함한다. 요리·자전거 수리 같은 도메인에서 **상호작용은 소리를 낸다** — 도마 두드리는 소리, 렌치가 금속에 닿는 소리, 냄비 놓는 소리. 이 소리들은 (a) 상호작용이 **언제** 일어나는지에 대한 강한 시간 단서이고, (b) binaural/spatial cue가 있다면 **어디서** 일어나는지에 대한 방향 단서다. HIGFlow가 Table VIII에서 보인 "프레임 입력을 빼면 성능이 크게 떨어진다"는 결과는 동역학 단서에 대한 모델의 민감성을 보여주는데, 오디오는 물체가 가려지거나(occlusion) 시야 밖에 있을 때도 살아남는 상보적 동역학 신호다.
- 특히 **occlusion 상황**이 결정적이다. 1인칭 영상에서 손과 물체는 몸·팔·다른 물체에 자주 가려진다. 이때 시각 dynamics는 끊기지만 접촉음은 남는다. Spatial audio를 dynamic memory token(현재는 V-JEPA만 채우는 자리)에 함께 넣는 구조는 곧바로 시도해볼 수 있는 확장이다 — 현재 V-JEPA fusion의 이득이 작다는 점($\le 0.74$ mm)을 고려하면, 오디오가 더 큰 상보적 이득을 줄 여지가 있다.
- 논문이 사용한 **gated residual adapter**($\mathbf{h}_k^F = \mathbf{h}_k^Q + g_k \Delta\mathbf{h}_k$)는 새 modality를 얼어붙은 VLM backbone에 안전하게 주입하는 범용 패턴이다. $g_k$가 modality별 기여도를 적응적으로 조절하므로, 오디오처럼 "어떤 순간엔 결정적이고 어떤 순간엔 무의미한" 신호에 특히 잘 맞는다.
- 평가 관점에서도 유용하다. Coherent4D가 정의한 연속 공간 지표(ADE / ADE₉₀ / FDE, mm 단위)는 audio-visual 방법이 spatial localization에 정말 기여하는지를 voxel 정확도보다 훨씬 엄밀하게 잴 수 있는 틀이다.

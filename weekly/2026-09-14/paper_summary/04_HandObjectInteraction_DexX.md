# Dex-X: Learning Visual-Tactile Dexterous Manipulation From Human Videos with Simulated Interaction

**arXiv**: 2609.07747 | **주제 분류**: Hand-Object Interaction | **출판일**: 2026-09-07 | **학회**: 프리프린트 (프로젝트 웹사이트만 명시, 발표처 언급 없음)
**저자/소속**: Ruoqu Chen, Feixiang Ruan, Liu Cao, Zihao Wang, Botian Xu, Shiqin Tong, Jiajun Liu, Mingzhi Pei, Chenyu Zhang, Wanli Xing, Kaifeng Zhang, Mengdi Xu — Tsinghua University, Shanghai Qizhi Institute, Sharpa, Tongji University, Renmin University
**링크**: https://arxiv.org/abs/2609.07747

## 한 줄 요약
단안(monocular) 사람 영상에는 없는 촉각 정보를 시뮬레이션의 접촉 물리로 "채워 넣어", 로봇으로 데이터를 따로 모으지 않고도 실제 로봇에 바로 올라가는 visual-tactile dexterous manipulation 정책을 학습하는 프레임워크.

## 메인 그림
![사람 영상에서 복원한 hand-object 궤적을 시뮬레이션으로 옮겨 접촉력(촉각) 지도를 얻고, 이를 써서 학습한 정책을 실제 로봇에 zero-shot으로 전개하는 Dex-X의 전체 흐름](https://arxiv.org/html/2609.07747v2/system.png)
왼쪽의 사람 시연 영상 → 가운데 시뮬레이션 안의 손-물체 상호작용 재현(여기서 손끝 접촉력이 생성됨) → 오른쪽 실제 hand-arm 로봇의 grasping·tool use로 이어지는 파이프라인을 한 장에 보여준다.

---

## 선행 연구

이 논문은 크게 세 갈래의 흐름 위에 서 있다.

**(1) 사람 시연으로부터의 dexterous manipulation 학습.**
사람의 손 움직임은 로봇 손 정책을 학습시키는 좋은 재료라서, 오래전부터 demonstration-guided RL(시연을 강화학습의 힌트로 쓰는 방식)이나 human grasp affordance(사람이 물체를 어떻게 쥐는지에 대한 사전 지식)를 활용해 왔다. 대표적으로 [DAPG](https://arxiv.org/abs/1709.10087)가 시연과 RL을 결합하는 고전적 방식이고, DexMV·VideoDex처럼 영상에서 직접 정책을 배우려는 시도도 이어졌다.
핵심 난제는 **embodiment gap(사람 손과 로봇 손의 구조 차이)**이다. 이를 풀기 위해 motion retargeting(사람 손 관절을 로봇 손 관절로 옮기는 변환), trajectory optimization, 복원된 hand-object 궤적 위에서의 RL 등이 제안되었다. ManipTrans, [DexMachina](https://arxiv.org/abs/2505.24853), [ViViDex](https://arxiv.org/abs/2404.15709), [Object-centric dexterous manipulation](https://arxiv.org/abs/2411.04005), DexTrack 등이 이 계열이다.

**(2) Dexterous manipulation의 sim-to-real transfer.**
시뮬레이션에서 대규모 RL로 복잡한 행동을 학습한 뒤 실제 로봇으로 옮기는 접근은 DeXtreme, pen-spinning 등에서 성과를 냈다. 하지만 접촉 동역학(contact dynamics), 촉각 센싱, 구동기 특성의 시뮬-실제 불일치에 민감한 행동일수록 transfer가 어렵다는 점이 반복적으로 지적됐다. 최근에는 [DextrAH-RGB](https://arxiv.org/abs/2412.01791) 같은 대규모 grasping, [SimToolReal](https://arxiv.org/abs/2602.16863) 같은 object-centric goal tracking 기반 도구 사용으로 범위가 넓어지는 중이다.

**(3) Visual-tactile manipulation.**
시각만으로는 부족한 상황(손가락이 물체를 가려 보이지 않는 occlusion, 미끄러짐 감지 등)에서 촉각은 결정적이다. tactile representation learning, force-aware 정책 학습([Tactile-VLA](https://arxiv.org/abs/2507.09160) 등), 공간적으로 접지된 촉각 표현 연구가 있었다. 이 논문의 표현 방식과 가장 가까운 것은 [Robot Synesthesia](https://arxiv.org/abs/2312.01853)로, 촉각 정보를 하나의 point cloud 표현 안에 녹여 in-hand manipulation의 zero-shot sim-to-real을 달성했다.

## 문제 제기

문제의 출발점은 아주 단순한 관찰이다. **사람 영상에는 촉각이 없다.**

- 강화학습이나 모방학습으로 잘 동작하는 dexterous 시스템을 만들려면, 정교하게 설계된 시뮬레이션 환경에서의 대량 상호작용이거나, 전용 teleoperation 장비로 수집한 대규모 로봇 시연이 필요하다. 둘 다 비싸고, 실세계 상호작용의 다양성을 따라가기 어렵다.
- 특히 **촉각 시연을 모으려면 계측 장갑(instrumented glove)이나 맞춤 센싱 하드웨어가 필요**해서 비용과 복잡도가 한층 더 올라간다.
- 반면 사람 영상은 풍부하고 다양하며 자연스러운 환경에서의 손 조작 행동을 담고 있다. 확장성 면에서 가장 매력적인 데이터 소스다.

그래서 저자들이 던지는 질문은 이것이다. **"로봇 쪽 데이터 수집 없이, 사람 영상만으로 실제 배포 가능한 visual-tactile dexterous manipulation 정책을 배울 수 있는가?"**

이 질문에 답하려면 두 가지 난관을 넘어야 한다.

1. **촉각 결손.** 영상은 시각 관측은 주지만 접촉력(contact force)을 주지 않는다. 그런데 안정적인 grasp 유지와 지속적인 물체 상호작용에는 힘 피드백이 결정적이다.
2. **sim-to-real 간극.** 인지 노이즈, 구동 지연, 접촉 모델링 오차 때문에 시뮬에서 학습한 dexterous 정책을 실제 하드웨어로 옮기는 일 자체가 어렵다.

## 연구 주제

이 논문이 새롭게 내세우는 프레이밍은 **"시뮬레이션 = 촉각 완성 엔진(tactile completion engine)"** 이다.

기존 흐름과의 차이를 정리하면 이렇다.

- 기존 human-video 계열은 시뮬레이션을 주로 **motion을 재현·검증하는 무대**로 썼다. retargeting이 잘 됐는지, 궤적이 물리적으로 가능한지를 확인하는 용도다.
- Dex-X는 시뮬레이션을 **원본 데이터에 없던 감각 모달리티(촉각)를 생성하는 장치**로 쓴다. 사람의 hand-object 상호작용을 물리적으로 재현하면, 물리 엔진이 계산하는 접촉 동역학 자체가 곧 "영상에 없던 힘 신호"의 정답 라벨이 된다.
- 따라서 결과물은 단순히 motion을 흉내 내는 정책이 아니라, **실제 배포 시 진짜 손끝 촉각 센서 값을 받아 closed-loop로 반응하는 visual-tactile 정책**이다.

contribution은 세 가지로 정리된다.

1. 사람 영상으로부터 visual-tactile dexterous manipulation 정책을 학습하는 프레임워크 Dex-X. 핵심 아이디어는 시뮬레이션을 tactile completion engine으로 쓰는 것.
2. 사람 영상에서 뽑은 motion prior와 tactile-aware RL을 결합한 **teacher-student 학습 패러다임**. 추가 fine-tuning 없이 실제 로봇으로 zero-shot 전이되는 contact-rich 스킬을 얻는다.
3. **29-DoF hand-arm 플랫폼**에서 다양한 grasping·tool-use 과제에 대한 zero-shot sim-to-real 실증. 저자들이 아는 한, task-specific fine-tuning 없이 사람 영상만으로 학습한 실세계 visual-tactile dexterous tool use를 수행한 최초 수준의 시스템이라고 주장한다.

## 연구 방법

전체 파이프라인은 **3단계**다. (Figure 2)

### 0) 문제 정의

단안 사람 시연 데이터셋 $\mathcal{D} = \{\tau_i^h\}_{i=1}^N$ (각 $\tau_i^h = (I_0, I_1, \dots)$는 이미지 시퀀스)이 주어졌을 때, 목표는 **reference-conditioned 정책** $\pi(a_t \mid o_t, r_{t+1})$을 학습하는 것이다.

- **input (observation)**: $o_t = \{o_t^{\text{prop}}, o_t^{\text{vis}}, o_t^{\text{tac}}\}$ — proprioception(로봇 자기 관절 상태), 시각, 촉각
- **input (조건)**: $r_{t+1}$ — 다음 스텝의 retarget된 motion reference
- **output**: 행동 $a_t$

### 1) Motion Prior 추출 + Spatial Augmentation (Sec 3.2)

**Hand-Object Motion Reconstruction.** 단안 영상에서 30 Hz로 손-물체 움직임을 복원한다.
- 물체 6-DoF pose: [FoundationPose](https://arxiv.org/abs/2312.08344). 물체 메시는 3D 스캔 또는 단일 이미지 복원으로 미리 준비 (시연 촬영과 무관한 오프라인 단계).
- 손 pose: [WiLoR](https://arxiv.org/abs/2409.12259)로 초기 추정 후 MANO 파라메트릭 모델로 정제. 프레임별로 MANO pose $\theta_t^H \in \mathbb{R}^{45}$, root translation $t_t$, global rotation $R_t$를 2D 키포인트 재투영 오차 $\mathcal{L}_{\text{hand}} = \sum_{k=1}^{21}\|\pi(J_k(\theta_t^H,\beta,t_t,R_t)) - j_t^k\|^2$로 최적화.
- **시간적 정제**: 전체 시퀀스에 대해 MANO mesh vertex의 프레임 간 변화를 억제하는 smoothness 항을 추가($\mathcal{L}_{\text{batch}}$). AdamW 5000 iteration, lr $10^{-3}$, 1000 iteration마다 0.5배 감쇠.
- **joint hand-object 최적화**: 손과 물체를 따로 추정하면 서로 파고드는 interpenetration(관통)이 생긴다. SDF 기반 penetration loss + 초기 추정값 유지를 위한 registration loss + smoothness loss를 결합해 함께 정제한다. 먼저 registration·smoothness만 최적화하고, 그다음 penetration loss를 켜는 2단계 방식.

**Robot Embodiment Retargeting.** Franka FR3 팔 + Sharpa 손으로 2단계 최적화.
- **Stage 1 (팔만)**: 손은 기본 자세로 고정한 채, 복원된 손목 pose를 따라가도록 팔 관절 2~7만 최적화. 목적함수 $\mathcal{L}_{\text{stage1}} = 0.5\mathcal{L}_{\text{pos}} + 0.25\mathcal{L}_{\text{rot}} + 10^{-3}\mathcal{L}_{\text{vel}}^{\text{arm}}$ (회전 오차는 geodesic distance).
- **Stage 2 (팔+손 동시)**: 22개 손 관절 전부와 팔 관절을 함께 최적화. 로봇 손 키포인트를 MANO 타깃에 정렬시키되, **엄지·검지와 손끝(distal) 키포인트에 더 큰 가중치**를 준다. 가중치는 손가락별 가중치 × 레벨 스케일로 분해된다.

| 손가락 | 엄지 | 검지 | 중지 | 약지 | 소지 |
|---|---|---|---|---|---|
| Finger weight | 25 | 15 | 10 | 7 | 5 |

| Level | Tip | Distal | Intermediate | Proximal |
|---|---|---|---|---|
| Scale | 1.0 | 0.6 | 0.4 | 0.3 |

- 실제 손의 측정된 가동 범위로 관절 한계를 URDF보다 더 빡빡하게 조여, retargeting과 실제 배포가 같은 행동 공간을 쓰도록 맞춘다.
- 평균 end-effector 위치 추적 오차가 **8 cm를 넘는 augmented 변형은 "도달 불가"로 판정해 학습에서 제외**한다.

**Spatial Augmentation.** 시연 하나를 여러 개로 불리는 단계로, [DexMimicGen](https://arxiv.org/abs/2410.24185)·[MoMaGen](https://arxiv.org/abs/2510.18316) 계열의 데이터 증강을 따른다. 손목·MANO 타깃·물체 궤적 **전부에 동일한** 평면 이동과 yaw 회전을 적용해 상호작용 기하를 보존한다.

$\tilde{\mathbf{x}}_{xy} = \mathbf{R}_z(\Delta\psi)(\mathbf{x}_{xy} - \mathbf{c}_{xy}) + \mathbf{c}_{xy} + \Delta\mathbf{p}_{xy}$

여기서 $\mathbf{c}_{xy}$는 팔 베이스 위치, $\Delta\psi \sim \mathcal{U}(-10^\circ, 10^\circ)$, 평면 이동은 $\Delta\mathbf{p}_{xy} \sim \mathcal{U}([-5\text{cm}, 5\text{cm}]^2)$.

### 2) State Expert 학습 (Sec 3.3) — 촉각이 "생성되는" 단계

Retargeting은 **운동학적으로만** 타당한 궤적을 준다. 물체를 실제로 쥐고 버티는 물리적 상호작용은 담기지 않는다. 그래서 시뮬레이션 안에서 RL로 closed-loop expert를 학습한다.

- **알고리즘**: [PPO](https://arxiv.org/abs/1707.06347) + [asymmetric actor-critic](https://arxiv.org/abs/1710.06542)(critic만 특권 정보를 보는 구조). [IsaacLab](https://arxiv.org/abs/2511.04831)에서 4096개 병렬 환경, 30 Hz.
- **retarget 궤적 $\tau_r$의 역할**: 초기 상태 샘플링 + motion reference 조건화. 그 위에서 정책은 자유롭게 접촉을 탐색한다.

**여기가 핵심**: expert는 시뮬레이션 접촉 센서로부터 **손끝 5개의 스칼라 접촉력 크기**를 관측한다. 순간적인 접촉 스파이크를 줄이려고 최근 두 샘플을 평균낸다: $f_t^{\text{tac}} = \frac{1}{2}(f_{t,0}^{\text{raw}} + f_{t,1}^{\text{raw}})$. 즉 영상에 없던 촉각 신호가 물리 엔진에서 만들어져 학습 신호로 쓰인다.

**Observation 구조 (actor 557차원)**

| 그룹 | 구성 | 차원 |
|---|---|---|
| Proprioception | 손 관절 위치/cos/sin, 손목 quaternion·속도 등 | 79 |
| Wrist reference | 목표-현재 손목 위치/회전/속도 차이 | 23 |
| Hand reference | 목표-현재 키포인트 위치·속도 | 288 |
| Task reference | 목표 물체 위치(3) + quaternion(4) + 손끝-물체 거리(5) | 12 |
| Object geometry | [BPS](https://arxiv.org/abs/1908.09186) 물체 메시 인코딩 | 128 |
| Tactile | 손끝 force 크기(5) + 예약된 contact-position 채널(15, 기본 0) | 20 |
| Current object pose | 노이즈 섞인 위치+quaternion | 7 |
| **합계** | | **557** |

critic은 여기에 **148차원 privileged state**(정답 물체 상태, 5스텝 미래 목표 물체 상태, 손끝-물체 거리 등)를 더해 총 705차원을 본다.

**Action.** $a_t \in \mathbb{R}^{29}$ = 팔 관절 델타 7개 + 손 관절 위치 타깃 22개. 팔은 $q_{t+1}^{\text{arm}} = q_t^{\text{arm}} + \alpha a_t^{\text{arm}}$, $\alpha = 0.2$ rad로 스텝당 변화를 제한한다. 행동에는 0~3 스텝의 랜덤 지연, 팔/손에 각각 0.15/0.4 계수의 저역 필터가 적용된다.

**Reward.** $r_t = r_t^{\text{wrist}} + 2 r_t^{\text{hand,abs}} + r_t^{\text{hand,rel}} + r_t^{\text{object}} + r_t^{\text{contact}} + r_t^{\text{action}} + r_t^{\text{success}} + r_t^{\text{collision}}$

| 그룹 | 주요 항 | 가중치 |
|---|---|---|
| Wrist | 위치 / 회전 | 4.0 / 2.0 |
| Absolute hand | 엄지 / 검지 / 중지 tip | 0.9 / 0.8 / 0.75 |
| Object | 위치 / 회전 | 8.0 / 6.0 |
| Contact | 손끝 힘 / approach shaping / no-slip | 3.0 / 2.0 / 1.5 |
| Terminal | 최종 위치 / 회전 / approach | 30.0 / 5.0 / 1.0 |

approach shaping은 최소 손끝-물체 거리 $d_t^{\min}$에 대해 $r_t^{\text{approach}} = \frac{1}{1 + 5 d_t^{\min}}$.

**Domain Randomization.** 실제 하드웨어의 불확실성을 미리 겪게 한다.

| 파라미터 | 범위 | 목적 |
|---|---|---|
| 손 PD stiffness / damping | ×[0.5, 2.0] | 손 동역학 |
| 팔 PD gain | ×[0.8, 1.2] | 팔 동역학 |
| 물체 질량 | [0.01, 0.15] kg | 물체 동역학 |
| 물체 CoM 오프셋 | 축당 ±0.02 m | 물체 동역학 |
| 마찰 | ×[1.0, 2.5] | 접촉 동역학 |
| Action delay | 0–3 스텝 | 제어 지연 |
| 물체 pose 위치/회전 노이즈 | $\sigma$ = 8 mm / 0.06 rad | 프레임별 오차 |
| 물체 pose 위치 bias | 축당 $\mathcal{U}(-0.05, 0.05)$ m | 에피소드별 bias |
| 물체 pose latency / dropout | 2 스텝 / 스텝당 2% | 인지 지연·결손 |

촉각 쪽은 별도로 랜덤화한다: 곱셈형 가우시안 노이즈 $f \leftarrow \max(0, f(1 + 0.2\epsilon))$, **손가락별 5% dropout**(한 손가락 신호를 통째로 없앰), 원소당 0.005 확률의 hold-last(직전 값 유지, 지연 모사).

### 3) Distillation과 Sim-to-Real (Sec 3.4)

특권 정보를 보는 expert는 실제 로봇에서 그대로 쓸 수 없다. 그래서 [DAgger](https://arxiv.org/abs/1011.0686)로 **배포 가능한 student**로 증류한다.

- **student가 버리는 것**: BPS 물체 형상 인코딩(128) + 참조 손끝-물체 거리(5) + 노이즈 물체 pose 추정(7). $557 - 128 - 5 - 7 = 417$차원.
- **student가 새로 받는 것**: **visual-tactile point cloud**. 깊이에서 나온 장면 점 1024개 + 로봇 손 키포인트 6개(손목 + 손끝 5) + 촉각 표면 점 25개(손끝당 5). 각 점은 3D 좌표 + 점 종류 표시자 1 + 촉각 force 채널 1을 갖는다: $(1024 + 6 + 25) \times (3+1+1) = 1055 \times 5$.
  - 이 표현이 [Robot Synesthesia](https://arxiv.org/abs/2312.01853)와 가장 가까운 지점이다. **힘을 별도 벡터로 붙이는 게 아니라, 장면 기하 안의 해당 위치에 "공간적으로 심어 넣는다".**
- 공유 PointNet(masked max-pooling)이 이를 64차원 feature로 압축 → student 입력은 $417 + 64 = 481$차원, 출력은 동일한 29차원 행동.
- **DAgger 혼합**: $a_t^{\text{exec}} = \beta_k a_t^{\text{tea}} + (1-\beta_k) a_t^{\text{stu}}$, $\beta_0 = 1.0$에서 iteration마다 0.85배로 기하 감쇠. 30 iteration, iteration당 4096 rollout step, 버퍼 $2\times10^5$ transition, iteration당 8 epoch MSE 회귀.
- **배포**: student가 motion reference $r_{t+1}$ + 실시간 proprioception·depth·손끝 촉각을 받아 30 Hz로 관절 명령을 낸다. 33 ms 예산 안에 depth 촬영 ~5 ms, forward kinematics ~2 ms, 정책 추론 ~3 ms, ROS 2 publish ~1 ms, 하드웨어 SDK 통신 ~1 ms가 들어간다.
- **팔 동역학 캘리브레이션**: 0.2 Hz, 진폭 0.3 rad 사인 궤적을 각 관절에 재생해 실제 FR3와 시뮬을 맞춘다. 관절 1~3의 시뮬 damping을 약 40% 줄여 상호상관 0.996 초과, 지연 10 ms 미만이 되도록 조정.

## 실험 결과 / 연구 의의

**세팅.** Franka FR3 팔 + Sharpa Wave dexterous hand (한 팔 29 DoF, 양팔 구성 58 DoF). 고정형 RealSense depth 카메라, 손끝 촉각 센서. 6개 task 카테고리:

| Task 카테고리 | 물체 수 | 시연 수 |
|---|---|---|
| Pick-up (컵, 큐브) | 2 | 5 |
| Tool use (스퀴지, 망치) | 2 | 3 |
| Peg insertion | 1 | 2 |
| In-hand rotation | 1 | 2 |
| In-hand translation | 1 | 1 |
| Bimanual handover | 1 | 1 |

즉 **시연 총합이 14개**에 불과하다. 데이터 효율성이 이 논문의 숨은 강점이다.

### Q1. 시뮬레이션에서의 multi-task 성능 (Table 1)

단위: 성공률(%). Dex-X의 Reach/Grasp/Manip은 해당 단계에 진입한 경우의 성공률이고, 비교 대상들은 전체 성공률이다.

| Category | Dex-X Reach | Dex-X Grasp | Dex-X Manip | Dex-X Overall | DAPG | ManipTrans | Kin. Retarget |
|---|---|---|---|---|---|---|---|
| Pick Up | 99.2 | 97.4 | 89.9 | 89.6 | 66.7 | 1.5 | 1.8 |
| Peg Insertion* | 56.8 | 43.7 | 43.3 | 43.1 | 52.8 | — | 0.0 |
| Tool Use | 86.9 | 82.3 | 74.6 | 74.3 | 70.1 | 35.0 | 24.1 |
| In-hand Rotation | — | — | 36.8 | 36.8 | 0.7 | 56.9 | 0.0 |
| In-hand Translation | — | — | 64.8 | 64.8 | 12.5 | 11.5 | 0.0 |
| Bimanual Handover | 99.0 | 88.8 | 87.9 | 86.6 | — | 4.7 | — |
| **Average** | 85.5 | 78.0 | 66.2 | **65.9** | 40.6† | 21.9 | 5.2 |

\* Peg insertion은 1 cm 미만 기준. † DAPG 평균은 평가된 단일 손 5개 카테고리 기준(Dex-X는 같은 5개에서 61.7%).

메시지: **kinematic retargeting만으로는 거의 아무것도 안 된다(5.2%)**. 모방 기반 ManipTrans는 긴 상호작용 동안 안정적 접촉을 놓쳐 물체가 미끄러지거나 실패하는 패턴을 보인다. Dex-X는 학습 중 손끝 힘 피드백을 받으며 물리적 상호작용을 탐색하므로 조작 전 구간에서 closed-loop 적응이 가능하다. 격차가 특히 큰 곳은 contact-rich 과제들이다 — tool use(74.3 vs 35.0), in-hand translation(64.8 vs 11.5), bimanual handover(86.6 vs 4.7). 다만 in-hand rotation은 ManipTrans(56.9)가 Dex-X(36.8)보다 높다.

### Q2. 시각·촉각 표현의 역할

**시뮬레이션 ablation (Figure 4).** 성공 기준은 엄격(최종 물체 위치 3 cm 이내)과 완화(5 cm), 회전 과제는 30° 기준.

| 관측 구성 | 엄격 | 완화 |
|---|---|---|
| Point cloud + tactile | 44% | 58% |
| Point cloud, tactile 제거 | 논문에 명시적 언급 없음 | 45% |
| Depth 기반 | 32% | 논문에 명시적 언급 없음 |

즉 **명시적 3D 기하(point cloud)와 촉각 둘 다 성능에 기여**한다. 또 scalar force / binary contact / 3D force 세 가지 촉각 인코딩을 비교했는데 성능 차이가 비슷해서, 실제 센서와의 일관성을 위해 **scalar force magnitude**를 배포용으로 채택했다.

**실세계 modality ablation (Table 2, 큐브 집기 30회, 모두 같은 teacher에서 증류).**

| Observation | Success |
|---|---|
| Full Visual-Tactile | 28/30 (93.3%) |
| No Vision | 14/30 (46.7%) |
| No Tactile | 11/30 (36.7%) |
| Proprioception Only | 8/30 (26.7%) |

흥미롭게도 **촉각을 빼는 쪽(36.7%)이 시각을 빼는 쪽(46.7%)보다 더 나쁘다.** 실패는 주로 grasp 획득 중 물체를 놓치거나, 접촉 후 물체를 잃는 형태로 나타난다.

### Q3. 실세계 배포와 일반화

**Zero-shot 배포(추가 fine-tuning 없음), 과제당 30회:**

| Task | Success |
|---|---|
| Cube picking | 28/30 (93%) |
| Cup pouring | 24/30 (80%) |
| Cup lifting | 22/30 (73%) |
| Squeegee manipulation (table cleaning) | 16/30 (53%) |

단계별 분해(Figure 5)를 보면, 큐브는 G1(충돌 없는 grasp) → G2(파지) → G3(파지 후 충돌·낙하 없음) → G4(최종 성공) 전 구간에서 높은 성공률을 유지한다. 반면 스퀴지는 **grasp 획득 단계에서 가장 크게 떨어지고**, 실패 원인은 grasp 실패와 파지 후 충돌/낙하가 지배적이다. 상호작용 지평(horizon)이 길수록 어렵다는 뜻이다.

**Zero-shot 물체 일반화 (Table 3, 큐브 집기 정책 그대로):**

| Object | Success |
|---|---|
| Training Cube | 28/30 (93.3%) |
| Thin Cube (미학습) | 23/30 (76.7%) |
| Square Cube (미학습) | 8/30 (26.7%) |
| Big Duck (미학습) | 8/30 (26.7%) |
| Small Duck (미학습) | 7/30 (23.3%) |

형상 변화가 작으면 잘 버티지만(얇은 큐브 76.7%), 기하가 크게 달라지면 23~27%로 급락한다. 일반화가 "된다"와 "그 한계도 뚜렷하다"를 동시에 보여주는 표다.

### Sim-to-Real 전이의 정량 분석 (Appendix B) — 이 논문의 가장 설득력 있는 부분

- **손끝 힘 패턴 (Figure 6)**: 큐브 집기에서 5개 손끝의 접촉력을 시간축으로 시각화했더니, **접촉 시작 타이밍, 힘 크기, 손가락 간 힘 재분배 경향이 시뮬과 실제에서 매우 유사**했다. 실측은 센싱 불확실성 때문에 더 노이즈가 많지만 힘 프로파일의 전체 구조는 보존된다. 즉 정책이 motion만이 아니라 **접촉 전략(contact strategy) 자체를 전이**했다는 증거다.
- **손목 궤적 (Figure 7)**: 시뮬-실제 평균 추적 오차 **2.83 cm**, 실세계 rollout 간 표준편차 **0.46–0.82 cm**(재현성이 높다). 오차는 $x$축(전방 하중 방향)에 집중되고, 시간적으로 approach 1.1 cm → grasp 2.7 cm → lift 3.8 cm로 증가한다. $z$축에서는 실제 로봇이 시뮬보다 일관되게 약 **5.7 mm 더 높이** 든다. 저자들은 이를 팔 impedance controller의 하중에 따른 정상상태 컴플라이언스 오프셋 + 물체 배치 변동(에피소드당 최대 1 cm) + 카메라 외부 파라미터 캘리브레이션 오차로 해석한다. 즉 **잔여 gap은 학습된 motion의 차이가 아니라 체계적 하드웨어 요인**이라는 것.

### 연구 의의

한 문장으로: **"사람 영상에는 촉각이 없다"는 근본적 결손을, 별도의 센서나 장갑이 아니라 물리 시뮬레이션으로 메울 수 있음을 실제 로봇 배포까지 이어서 보여줬다.**

- 인터넷 규모의 사람 영상을 로봇 스킬 데이터로 쓰는 경로에서, 시뮬레이션이 단순 검증 무대가 아니라 **"빠진 물리적 감독(physical supervision)을 생성하는 장치"** 라는 역할 재정의.
- 시연 14개로 6개 카테고리를 커버하고 실세계 zero-shot까지 간다는 데이터 효율성.
- 촉각을 point cloud에 공간적으로 심는 통합 표현이 실제로 sim-to-real에 유효함을 modality ablation으로 검증.

## 한계

논문이 직접 밝힌 한계(Sec 6)와 실험에서 드러나는 한계를 함께 정리한다.

**논문이 명시한 한계**
1. **장기 지평(long-horizon) 상호작용과 폭넓은 일반화가 여전히 어렵다.** 성능이 인지 오차, 컨트롤러 불일치, 큰 기하·카테고리 변화에 민감하다.
2. **배포 정책이 여전히 retarget된 motion reference에 의존한다.** 즉 완전 자율적으로 "무엇을 할지"를 정하는 게 아니라, 사람 시연에서 온 참조 궤적이 항상 조건으로 들어간다. 새 스킬을 하려면 그에 맞는 시연이 필요하다.
3. **촉각 표현이 손끝당 스칼라 힘 크기 하나로 제한**된다. 압력 분포, 전단력(shear), 미끄러짐(slip), 접촉 패치(contact patch) 같은 풍부한 신호를 담지 못한다. 고해상도 촉각 센싱이 있으면 더 정밀한 접촉 추론과 힘 조절이 가능할 것이다.
4. 더 넓은 스킬로 확장하려면 더 다양한 시연, 더 많은 시뮬레이션 상호작용, 더 유연한 task conditioning이 필요하다.

**실험에서 드러나는 한계**
- 물체 일반화 급락: 미학습 square cube·오리 인형에서 23~27%로 떨어진다.
- Tool use(스퀴지) 실세계 53%는 실용 수준과 거리가 있고, 병목은 grasp 획득 단계다.
- In-hand rotation은 시뮬에서 36.8%로 ManipTrans(56.9%)에 밀린다. 모든 접촉 과제에서 우월한 건 아니다.
- 파이프라인이 물체 메시(3D 스캔 또는 단일 이미지 복원)를 오프라인으로 요구한다. 임의의 인터넷 영상에 바로 적용하기에는 전처리 부담이 남는다.
- 물체 pose 추정이 FoundationPose에, 손 추정이 WiLoR+MANO에 의존하므로 이들의 실패가 그대로 전파된다. Appendix B에서도 카메라 캘리브레이션 오차가 잔여 gap의 원인 중 하나로 지목됐다.

## 우리 연구와 연결되는 점

**Egocentric Vision 관점**

- Dex-X의 입력은 단안 RGB 영상에서 복원한 hand-object 궤적이다. 이건 egocentric video 연구에서 다루는 신호와 거의 동일한 재료다. **egocentric 영상을 "물리 시뮬레이션으로 리프팅"해서 그 안에서 없던 모달리티를 생성한다**는 발상은, 1인칭 영상 이해에서도 그대로 쓸 수 있는 템플릿이다.
- 다만 이 논문은 고정 3인칭 카메라 기반 시연을 쓴다. Egocentric으로 옮기면 카메라 자체가 움직이고 손이 프레임 밖으로 자주 나가며, 자기 손에 의한 occlusion이 훨씬 심하다. 현재 파이프라인(FoundationPose + WiLoR + 물체 메시 사전 준비)이 egocentric 조건에서 얼마나 버티는지가 자연스러운 후속 질문이다.
- "관측되지 않은 물리량을 시뮬레이션으로 라벨링한다"는 아이디어는 egocentric 데이터의 만성적 문제인 **ground-truth 부재**에 대한 일반적 해법이 될 수 있다. 힘뿐 아니라 접촉 시점, 파지 안정성, 물체 무게 같은 것도 같은 방식으로 유도해 볼 수 있다.

**Hand-Object Interaction 관점**

- 이 논문은 HOI 복원(reconstruction)과 HOI 활용(policy learning)을 하나의 파이프라인으로 잇는 좋은 사례다. 특히 **joint hand-object optimization에서 SDF penetration loss로 관통을 없애는 단계**는 순수 HOI 복원 연구에서도 흔히 쓰는 요소인데, 여기서는 "그렇게 정제하지 않으면 시뮬에서 물리적으로 재현이 안 된다"는 명확한 하류 동기가 붙는다. 복원 품질을 평가할 때 재투영 오차 대신 **"시뮬레이션에서 실행 가능한가"** 를 지표로 삼는 관점을 제공한다.
- Retargeting 가중치 표(엄지 25, 검지 15, 손끝 스케일 1.0)는 HOI에서 **어떤 키포인트가 상호작용에 실제로 중요한가**에 대한 실용적 힌트다. 손끝과 엄지/검지가 접촉의 대부분을 결정한다는 건 HOI 표현 설계에도 시사점이 있다.
- **접촉(contact)을 이진 레이블이 아니라 연속적인 힘으로 다룬다**는 점이 중요하다. 대부분의 HOI 데이터셋은 접촉을 있음/없음으로만 주는데, 이 논문은 힘의 시간적 변화와 손가락 간 분배까지 다루고(Figure 6), 그것이 실제 로봇에서도 재현됨을 보였다. HOI 어노테이션의 다음 단계가 어디인지를 시사한다.
- 흥미로운 반전: 실세계 ablation에서 **촉각 제거(36.7%)가 시각 제거(46.7%)보다 더 치명적**이었다. HOI를 순수 시각 문제로만 보는 시각에 대한 반례로 인용할 만하다.

**Spatial Audio 관점**

- 직접적 연결은 없다. 다만 방법론적 유비는 꽤 선명하다. **"한 모달리티에 없는 정보를 물리적 시뮬레이션으로 합성해 supervision을 만든다"** 는 구조는, room acoustics 시뮬레이션으로 mono 오디오에서 spatial audio 학습 데이터를 만드는 파이프라인과 정확히 같은 형태다 (이 주간 다이제스트의 spatial audio editing 논문들이 쓰는 controllable room simulation과 같은 논리).
- 한 걸음 더 나가면, contact force는 **contact sound의 물리적 원인**이다. 시뮬레이션이 접촉력을 알고 있다면 접촉음도 원리적으로 합성할 수 있다. egocentric video + 접촉음 + 손-물체 상호작용을 묶는 멀티모달 연구에서, 이 논문의 "시뮬레이션을 completion engine으로 쓴다"는 틀을 오디오 쪽으로 확장하는 건 자연스러운 방향이다.
- 또한 sim-to-real 검증 방식(Figure 6의 힘 분포 비교, Figure 7의 궤적 IQR 비교)은 **시뮬로 만든 신호가 실제와 정말 일치하는지를 정량적으로 보이는 프로토콜**로, 시뮬레이션 기반 오디오 데이터의 realism을 검증할 때도 참고할 만한 형식이다.

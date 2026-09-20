# SMPL-X 생태계 — 갈래별 논문 리스트

자동 생성 · 83 entries / 62 unique arXiv · 2026-09 기준. 각 분기 아래 `why ·` 줄은 그 분기가 **무엇을 축으로, 왜 갈라지는지**다. arXiv 판본 미확인 항목은 ID를 비웠다.

## Branch 01 · Estimation — reading SMPL-X out of images and video

`images · video → SMPL-X`

**What splits this branch** — 이 갈래를 가르는 축은 **‘무엇을 보고, 무엇을 뽑는가’**다. 추정 대상의 범위(전신인가 손인가), 출력을 어떤 형태로 낼 것인가, 한 장인가 영상인가, 3인칭인가 1인칭인가, 한 사람인가 여럿인가. 축마다 이유가 다르고, 그 이유는 대부분 **학습 데이터가 어디서 끊겨 있는가**로 귀결된다.

### By body scope — whole-body vs hand-only

> why · 전신 데이터에는 손 다양성이 부족하고, 손 데이터에는 몸 맥락이 없다. 학습 데이터가 갈려 있으니 모델도 갈린다 — Hand4Whole++가 ‘supervision gap’이라 부른 그 분기.

#### Whole-body · by integration strategy

> why · ‘손 정확도’와 ‘몸과의 일관성’ 사이 트레이드오프를 **어디서** 해결하느냐로 다시 갈린다. 따로 뽑아 붙일 것인가, 특징 수준에서 섞을 것인가, 처음부터 한 네트워크로 갈 것인가, 데이터로 밀 것인가, 얼린 채 어댑터로 이을 것인가.

##### Separate-then-attach

> why · 손 전문가의 정확도를 살리되 손목에서 어긋난다.

| 논문 | 학회 | arXiv |
|---|---|---|
| FrankMocap | ICCVW 2021 | [2108.06428](https://arxiv.org/abs/2108.06428) |

##### Feature-level fusion

> why · 손목 회전에 손 쪽 특징을 써서 연결부를 정교화.

| 논문 | 학회 | arXiv |
|---|---|---|
| Hand4Whole | CVPRW 2022 | [2011.11534](https://arxiv.org/abs/2011.11534) |
| PyMAF-X | TPAMI 2023 | [2207.06400](https://arxiv.org/abs/2207.06400) |

##### One-stage joint

> why · 손을 다시 크롭하지 않고 공유 특징맵에서 한 번에.

| 논문 | 학회 | arXiv |
|---|---|---|
| OSX | CVPR 2023 | [2303.16160](https://arxiv.org/abs/2303.16160) |
| AiOS | CVPR 2024 | [2403.17934](https://arxiv.org/abs/2403.17934) |

##### Scale-up

> why · 아키텍처 대신 데이터·모델 크기로.

| 논문 | 학회 | arXiv |
|---|---|---|
| SMPLer-X | NeurIPS 2023 | [2309.17448](https://arxiv.org/abs/2309.17448) |

##### Frozen backbone + adapter

> why · 잘 되는 것은 재학습하지 않고 얇은 다리만 놓는다.

| 논문 | 학회 | arXiv |
|---|---|---|
| HMR-Adapter | ACM MM 2024 | — |
| Hand4Whole++ | CVPR 2026 | [2603.14726](https://arxiv.org/abs/2603.14726) |

#### Hand-only · by failure mode

> why · 손 하나는 잘 잡히니, 남은 문제는 ‘언제 깨지는가’다 — 가려질 때, 야외일 때, 두 손이 얽힐 때.

##### Occlusion-robust

> why · 물체·다른 손에 가려진 손.

| 논문 | 학회 | arXiv |
|---|---|---|
| HandOccNet | CVPR 2022 | [2203.14564](https://arxiv.org/abs/2203.14564) |

##### In-the-wild

> why · 검출부터 복원까지 야외 다중 손.

| 논문 | 학회 | arXiv |
|---|---|---|
| HaMeR | CVPR 2024 | [2312.05251](https://arxiv.org/abs/2312.05251) |
| WiLoR | CVPR 2025 | [2409.12259](https://arxiv.org/abs/2409.12259) |

##### Interacting hands

> why · 두 손이 얽히면 자기 가림 + 크기 분포 불일치.

| 논문 | 학회 | arXiv |
|---|---|---|
| InterWild | CVPR 2023 | [2303.13652](https://arxiv.org/abs/2303.13652) |

### By output representation — regression vs spatial

> why · 좌표·파라미터를 직접 회귀하면 공간 정보를 잃고 매핑이 비선형이 된다. 그래서 voxel·lixel·heatmap 같은 공간 표현으로 갈아탄다.

| 논문 | 학회 | arXiv |
|---|---|---|
| V2V-PoseNet | CVPR 2018 | [1711.07399](https://arxiv.org/abs/1711.07399) |
| I2L-MeshNet | ECCV 2020 | [2008.03713](https://arxiv.org/abs/2008.03713) |
| Pose2Mesh | ECCV 2020 | [2008.09047](https://arxiv.org/abs/2008.09047) |

### By temporal scope — single image vs video

> why · 프레임별 추정은 구조적으로 jitter를 피할 수 없다. 시간축을 넣어야 손이 떨리지 않는다.

| 논문 | 학회 | arXiv |
|---|---|---|
| TCMR | CVPR 2021 | [2011.08627](https://arxiv.org/abs/2011.08627) |
| DanceHMR | 프리프린트 2026 | [2605.18102](https://arxiv.org/abs/2605.18102) |

### By viewpoint — exocentric vs egocentric

> why · 1인칭은 어안 왜곡, 몸이 거의 안 보임, SMPL-X 정답 없음. 3인칭 해법을 그대로 옮길 수 없어 갈린다.

| 논문 | 학회 | arXiv |
|---|---|---|
| Egocentric WB-HMR | ICIP 2026 | [2605.08606](https://arxiv.org/abs/2605.08606) |
| EgoForce | SIGGRAPH 2026 | [2605.12498](https://arxiv.org/abs/2605.12498) |

### By scene — single vs multi-person

> why · root-relative 포즈만으로는 여러 사람을 한 공간에 놓을 수 없다. 카메라까지의 절대 거리가 따로 필요해진다.

| 논문 | 학회 | arXiv |
|---|---|---|
| RootNet | ICCV 2019 | [1907.11346](https://arxiv.org/abs/1907.11346) |
| 3DCrowdNet | CVPR 2022 | [2104.07300](https://arxiv.org/abs/2104.07300) |

## Branch 02 · Data & annotation — the floor under every other branch

`⊥ all branches`

**What splits this branch** — 이 갈래의 축은 하나뿐이다: **‘어떻게 얻었는가’**. 같은 SMPL-X 파라미터라도 마커를 피팅했는지, 영상에서 회귀했는지, 합성했는지에 따라 노이즈의 성격이 완전히 다르다. 무엇을 담았는지로 나누면 이 차이가 보이지 않는다.

### Studio motion capture — markers → MoSh++ → SMPL-X

> why · 정확하다. 대신 실내·슈트·소수 화자라는 도메인에 갇혀 외형 다양성이 빈약하다.

| 논문 | 학회 | arXiv |
|---|---|---|
| InterHand2.6M | ECCV 2020 | [2008.09309](https://arxiv.org/abs/2008.09309) |
| BEAT | ECCV 2022 | [2203.05297](https://arxiv.org/abs/2203.05297) |
| BEAT2 (EMAGE) | CVPR 2024 | [2401.00374](https://arxiv.org/abs/2401.00374) |
| Human4K | 프리프린트 2026 | [2607.13646](https://arxiv.org/abs/2607.13646) |
| Codec Avatar Studio | NeurIPS 2024 D&B | — |

### Video pseudo-GT — estimator → parameters

> why · 넓고 싸다. 대신 품질 상한이 **추정 갈래의 추정기**에 묶인다. 이 경로가 생성 갈래의 주식이 되면서 두 갈래가 의존 관계로 엮인다.

| 논문 | 학회 | arXiv |
|---|---|---|
| NeuralAnnot | CVPRW 2022 | [2011.11232](https://arxiv.org/abs/2011.11232) |
| Three Recipes | CVPRW 2023 | — |
| SHOW (TalkSHOW) | CVPR 2023 | [2212.04420](https://arxiv.org/abs/2212.04420) |
| Converse3D (ViBES) | CVPR 2026 | [2512.14234](https://arxiv.org/abs/2512.14234) |

### Synthesis & relighting

> why · 위 둘의 절충. 정확한 정답은 스튜디오에서, 외형 다양성은 렌더링으로.

| 논문 | 학회 | arXiv |
|---|---|---|
| Re:InterHand | NeurIPS 2023 | [2310.17768](https://arxiv.org/abs/2310.17768) |

### Language-labelled motion — body-only → whole-body

> why · 텍스트 라벨이 ‘걷는다·점프한다’ 수준이라 손 라벨이 애초에 없었다. 이 데이터의 22관절 표현이 생성 갈래의 손 부재를 2년간 고착시켰고, Motion-X가 전신 주석을 넣으면서 풀린다.

| 논문 | 학회 | arXiv |
|---|---|---|
| HumanML3D | CVPR 2022 | — |
| Motion-X | NeurIPS 2023 D&B | [2307.00818](https://arxiv.org/abs/2307.00818) |

## Branch 03 · Avatar & rendering — turning parameters into a visible person

`SMPL-X → pixels`

**What splits this branch** — 두 개의 축이 겹친다. **‘무엇으로 표면을 표현하는가’**(파라메트릭 메시인가, 신경 렌더링인가, 조명까지 분리하는가)와 **‘개인화에 얼마가 드는가’**(스튜디오인가, 폰 스캔인가, 사진 한 장인가). 후자가 최근 이 갈래를 연구실 밖으로 끌어냈다.

### By surface representation

> why · 제어 가능성과 사실감이 반대로 간다. 메시는 다루기 쉽지만 사실감에 한계가 있고, 신경 렌더링은 사실적이지만 표정·손 제어가 어려워 결국 메시와 결합한다.

#### Parametric mesh

> why · 저차원 파라미터로 뼈대+표면.

| 논문 | 학회 | arXiv |
|---|---|---|
| SMPL-X | CVPR 2019 | [1904.05866](https://arxiv.org/abs/1904.05866) |
| DeepHandMesh | ECCV 2020 | [2008.08213](https://arxiv.org/abs/2008.08213) |
| UHM | CVPR 2024 | [2405.07933](https://arxiv.org/abs/2405.07933) |

#### Neural rendering · 3D Gaussians

> why · 사실감을 위해 메시 밖으로 — 대신 메시를 뼈대로 다시 붙인다.

| 논문 | 학회 | arXiv |
|---|---|---|
| MonoNHR | 3DV 2022 | [2210.00627](https://arxiv.org/abs/2210.00627) |
| ExAvatar | ECCV 2024 | [2407.21686](https://arxiv.org/abs/2407.21686) |
| PERSONA | ICCV 2025 | [2508.09973](https://arxiv.org/abs/2508.09973) |
| DynaAvatar | CVPR 2026 | [2603.14772](https://arxiv.org/abs/2603.14772) |

#### Relightable

> why · 조명이 바뀌면 외형이 깨지니 조명을 분리.

| 논문 | 학회 | arXiv |
|---|---|---|
| URHand | CVPR 2024 | [2401.05334](https://arxiv.org/abs/2401.05334) |

### By capture cost — studio → phone → single image

> why · 스튜디오 자산을 전제하면 일상에서 못 쓴다. 입력을 싸게 만들수록 사전(prior)에 더 기대게 된다.

| 논문 | 학회 | arXiv |
|---|---|---|
| Codec Avatar Studio | NeurIPS 2024 | — |
| UHM | CVPR 2024 | [2405.07933](https://arxiv.org/abs/2405.07933) |
| PERSONA | ICCV 2025 | [2508.09973](https://arxiv.org/abs/2508.09973) |
| DynaAvatar | CVPR 2026 | [2603.14772](https://arxiv.org/abs/2603.14772) |

## Branch 04 · Generation — producing SMPL-X from a condition

`text · speech · dialogue → SMPL-X`

**What splits this branch** — 이 갈래의 첫 축은 **‘무엇을 조건으로 주는가’**다. 그런데 조건마다 **데이터가 어디서 왔는지가 달라서**, 같은 조건 안에서 두 번째 축이 열린다 — 몸통만인가 전신인가, mocap인가 pseudo-GT인가. 이 갈래에서 손이 늦게 합류한 이유는 전부 그 두 번째 축에 있다.

### Text → motion

> why · 텍스트 라벨이 몸통 수준이라 데이터(HumanML3D)가 22관절로 배포됐고, 그 표현이 벤치마크·평가기까지 세트로 굳었다. 그래서 **출력 범위**로 갈린다 — 2023년 하반기 Motion-X(데이터)·HumanTOMATO(모델)에서야 전신으로 넘어간다.

#### Body-only (HumanML3D 22 joints)

> why · 2022–2023 SOTA 라인 전체가 구조적으로 손·얼굴을 낼 수 없었다.

| 논문 | 학회 | arXiv |
|---|---|---|
| HumanML3D | CVPR 2022 | — |
| MDM | ICLR 2023 | [2209.14916](https://arxiv.org/abs/2209.14916) |
| MoMask | CVPR 2024 | [2312.00063](https://arxiv.org/abs/2312.00063) |

#### Whole-body (SMPL-X)

> why · 전신 주석 데이터가 생기자 손·얼굴을 함께 생성하는 모델이 따라온다.

| 논문 | 학회 | arXiv |
|---|---|---|
| Motion-X | NeurIPS 2023 | [2307.00818](https://arxiv.org/abs/2307.00818) |
| HumanTOMATO | ICML 2024 | [2310.12978](https://arxiv.org/abs/2310.12978) |

### Action label → motion

> why · 텍스트보다 이산적이고, 여러 라벨을 이어 붙여 장기 시퀀스를 만드는 문제로 갈린다.

| 논문 | 학회 | arXiv |
|---|---|---|
| MultiAct | AAAI 2023 | [2212.05897](https://arxiv.org/abs/2212.05897) |

### Speech → gesture (co-speech)

> why · 립싱크와 손짓이 과제의 본질이라 **전신에 먼저 도달**했다. 대신 여기서는 데이터 획득 경로로 갈린다 — mocap이냐 영상 추정이냐.

#### Mocap-based

> why · 정확하지만 스튜디오·화자 제한.

| 논문 | 학회 | arXiv |
|---|---|---|
| BEAT | ECCV 2022 | [2203.05297](https://arxiv.org/abs/2203.05297) |
| EMAGE / BEAT2 | CVPR 2024 | [2401.00374](https://arxiv.org/abs/2401.00374) |

#### Video pseudo-GT-based

> why · 야외 다양성 대신 추정기 품질에 묶임.

| 논문 | 학회 | arXiv |
|---|---|---|
| SHOW (TalkSHOW) | CVPR 2023 | [2212.04420](https://arxiv.org/abs/2212.04420) |

#### Real-time holistic

> why · 지연 제약이 별도 축을 연다.

| 논문 | 학회 | arXiv |
|---|---|---|
| DiffSHEG | 2024 | [2401.04747](https://arxiv.org/abs/2401.04747) |

### Dialogue → behaviour (agentic)

> why · ‘무엇을 움직일지’만이 아니라 **‘언제, 왜 움직일지’**까지 결정한다. 번역이 아니라 에이전트가 되면서 조건이 대화 이력 전체로 넓어진다.

| 논문 | 학회 | arXiv |
|---|---|---|
| ViBES | CVPR 2026 | [2512.14234](https://arxiv.org/abs/2512.14234) |
| Motion-Omni | 프리프린트 2026 | [2609.04250](https://arxiv.org/abs/2609.04250) |

### Sign language

> why · 손이 곧 의미를 실으므로 손 정밀도가 곧 정확도다. 다른 생성 과제와 달리 손을 뒤로 미룰 수 없다.

| 논문 | 학회 | arXiv |
|---|---|---|
| SIGNER | ECCV 2026 | [2506.07460](https://arxiv.org/abs/2506.07460) |

## Branch 05 · Interaction (inbound) — reconstructing the body together with objects, people, and scenes

`world → SMPL-X + objects · people`

**What splits this branch** — 축은 **‘무엇과 엮는가’**다. 상대가 물체인지 다른 손인지 다른 사람인지에 따라 제약의 종류가 달라진다 — 가림의 원인이 다르고, 접촉 제약이 다르다. 화살표는 **들어오는** 방향이다: 세상을 보고 사람과 상대를 함께 복원한다. 몸이 세상을 **바꾸는** 나가는 방향은 Branch 06으로 분리했다.

### Hand – object

> why · 물체가 손을 가리고, 접촉이 손 자세를 제약한다. 손 단독 추정과 다른 문제가 된다.

| 논문 | 학회 | arXiv |
|---|---|---|
| TOUCH | 2025 | [2510.14874](https://arxiv.org/abs/2510.14874) |
| AGILE | 2026 | [2602.04672](https://arxiv.org/abs/2602.04672) |
| ForeHOI | 2026 | [2602.06226](https://arxiv.org/abs/2602.06226) |
| HOPformer | ECCV 2026 | [2606.30598](https://arxiv.org/abs/2606.30598) |
| DreamHand | 프리프린트 2026 | [2608.20308](https://arxiv.org/abs/2608.20308) |

### Human – object (whole-body)

> why · 전신 자세와 물체 배치가 서로를 제약한다. 손만이 아니라 몸 전체가 접촉에 참여.

| 논문 | 학회 | arXiv |
|---|---|---|
| CONTHO | CVPR 2024 | [2404.04819](https://arxiv.org/abs/2404.04819) |
| GraspDiffusion | 2024 | [2410.13911](https://arxiv.org/abs/2410.13911) |

### Hand – hand

> why · 자기 가림에 더해, 한 손 데이터와 두 손 데이터의 크기 분포가 어긋난다.

| 논문 | 학회 | arXiv |
|---|---|---|
| InterHand2.6M | ECCV 2020 | [2008.09309](https://arxiv.org/abs/2008.09309) |
| InterWild | CVPR 2023 | [2303.13652](https://arxiv.org/abs/2303.13652) |
| Re:InterHand | NeurIPS 2023 | [2310.17768](https://arxiv.org/abs/2310.17768) |

## Branch 06 · Embodied simulation (outbound) — the body as actuator, the world as output

`SMPL-X · MANO (action) ⇒ world response (video)`

**What splits this branch** — 이 갈래는 지도의 전제를 절반만 공유한다. 몸은 여전히 명시적으로 표현하지만, **세상은 암묵적으로**(비디오 잠재 공간) 표현한다 — 즉 SMPL-X 허브에서 world model 허브로 건너가는 다리다. 그래서 첫 축은 **‘행동을 무엇으로 넣는가’**가 된다: 손 메시를 렌더해 픽셀에 정렬할 것인가, 포즈 파라미터를 토큰으로 줄 것인가, 2D 마스크로 뭉갤 것인가. 2026년 들어 두 번째 축이 열렸는데, **손의 움직임과 카메라(머리)의 움직임을 어떻게 분리하는가**다 — 1인칭에서는 둘이 같은 픽셀 흐름에 섞여 들어오기 때문이다.

### By action representation — explicit geometry vs implicit 2D

> why · 행동을 픽셀에 정렬된 기하로 줄수록 물체 역학이 정확해지고, 벡터로 줄수록 유연하지만 정렬이 약해진다. 2D 마스크만 주면 손은 맞춰도 물체가 안 움직인다(DWM이 InterDyn을 그렇게 평가한다).

#### Rendered hand mesh (pixel-aligned)

> why · 메시를 렌더해 넣으면 기하와 움직임이 픽셀 단위로 정렬된다.

| 논문 | 학회 | arXiv |
|---|---|---|
| DWM | 프리프린트 2025 | [2512.17907](https://arxiv.org/abs/2512.17907) |
| Hand2World | 프리프린트 2026 | [2602.09600](https://arxiv.org/abs/2602.09600) |
| HandsOnWorld | 프리프린트 2026 | [2607.02075](https://arxiv.org/abs/2607.02075) |

#### Pose parameter / joint vector

> why · SMPL-X 파라미터나 관절 좌표를 토큰으로 주입 — 표현이 가볍고 부위별 분리가 쉽다.

| 논문 | 학회 | arXiv |
|---|---|---|
| PlayerOne | 프리프린트 2025 | [2506.09995](https://arxiv.org/abs/2506.09995) |
| PEVA | 프리프린트 2025 | [2506.21552](https://arxiv.org/abs/2506.21552) |
| Generated Reality | 프리프린트 2026 | [2602.18422](https://arxiv.org/abs/2602.18422) |
| EgoExo-WM | 프리프린트 2026 | [2605.15477](https://arxiv.org/abs/2605.15477) |

#### 2D mask (implicit)

> why · 구동체의 실루엣만 주는 가장 약한 조건. 대형 비디오 모델을 암묵적 물리 시뮬레이터로 쓰는 발상의 출발점.

| 논문 | 학회 | arXiv |
|---|---|---|
| InterDyn | CVPR 2025 | [2412.11785](https://arxiv.org/abs/2412.11785) |

### By camera–hand disentanglement

> why · 1인칭에서는 머리가 돌아가도, 손이 움직여도 같은 픽셀 흐름이 생긴다. 이걸 분리하지 못하면 모델이 둘을 혼동한다 — 2026년 작업들이 Plücker ray 같은 world-frame 표현으로 카메라를 따로 떼어낸 이유.

| 논문 | 학회 | arXiv |
|---|---|---|
| Hand2World | 프리프린트 2026 | [2602.09600](https://arxiv.org/abs/2602.09600) |
| HandsOnWorld | 프리프린트 2026 | [2607.02075](https://arxiv.org/abs/2607.02075) |
| Generated Reality | 프리프린트 2026 | [2602.18422](https://arxiv.org/abs/2602.18422) |

### By viewpoint — egocentric vs fixed third-person

> why · 이 갈래는 거의 전부 1인칭이다. 손이 관측되는 몸이자 행동 그 자체인 시점이라 자연스럽다. 고정 3인칭은 InterDyn 하나.

| 논문 | 학회 | arXiv |
|---|---|---|
| InterDyn | CVPR 2025 | [2412.11785](https://arxiv.org/abs/2412.11785) |

### Body → robot action (embodiment transfer)

> why · 세상이 아니라 **로봇**이 출력이 되는 변형. 사람 손 메시를 로봇 관절 명령이나 로봇 손 이미지로 옮긴다 — 사람 손과 로봇 손의 형상이 달라 그대로는 못 쓴다.

| 논문 | 학회 | arXiv |
|---|---|---|
| HandEdit | 프리프린트 2026 | [2608.12122](https://arxiv.org/abs/2608.12122) |
| Ego2Robot | 2026 | [2608.02580](https://arxiv.org/abs/2608.02580) |
| SiMDex | 2026 | [2608.04196](https://arxiv.org/abs/2608.04196) |

## 전체 (arXiv ID 기준 중복 제거)

| arXiv | 논문 | 학회 |
|---|---|---|
| [1711.07399](https://arxiv.org/abs/1711.07399) | V2V-PoseNet | CVPR 2018 |
| [1904.05866](https://arxiv.org/abs/1904.05866) | SMPL-X | CVPR 2019 |
| [1907.11346](https://arxiv.org/abs/1907.11346) | RootNet | ICCV 2019 |
| [2008.03713](https://arxiv.org/abs/2008.03713) | I2L-MeshNet | ECCV 2020 |
| [2008.08213](https://arxiv.org/abs/2008.08213) | DeepHandMesh | ECCV 2020 |
| [2008.09047](https://arxiv.org/abs/2008.09047) | Pose2Mesh | ECCV 2020 |
| [2008.09309](https://arxiv.org/abs/2008.09309) | InterHand2.6M | ECCV 2020 |
| [2011.08627](https://arxiv.org/abs/2011.08627) | TCMR | CVPR 2021 |
| [2011.11232](https://arxiv.org/abs/2011.11232) | NeuralAnnot | CVPRW 2022 |
| [2011.11534](https://arxiv.org/abs/2011.11534) | Hand4Whole | CVPRW 2022 |
| [2104.07300](https://arxiv.org/abs/2104.07300) | 3DCrowdNet | CVPR 2022 |
| [2108.06428](https://arxiv.org/abs/2108.06428) | FrankMocap | ICCVW 2021 |
| [2203.05297](https://arxiv.org/abs/2203.05297) | BEAT | ECCV 2022 |
| [2203.14564](https://arxiv.org/abs/2203.14564) | HandOccNet | CVPR 2022 |
| [2207.06400](https://arxiv.org/abs/2207.06400) | PyMAF-X | TPAMI 2023 |
| [2209.14916](https://arxiv.org/abs/2209.14916) | MDM | ICLR 2023 |
| [2210.00627](https://arxiv.org/abs/2210.00627) | MonoNHR | 3DV 2022 |
| [2212.04420](https://arxiv.org/abs/2212.04420) | SHOW (TalkSHOW) | CVPR 2023 |
| [2212.05897](https://arxiv.org/abs/2212.05897) | MultiAct | AAAI 2023 |
| [2303.13652](https://arxiv.org/abs/2303.13652) | InterWild | CVPR 2023 |
| [2303.16160](https://arxiv.org/abs/2303.16160) | OSX | CVPR 2023 |
| [2307.00818](https://arxiv.org/abs/2307.00818) | Motion-X | NeurIPS 2023 D&B |
| [2309.17448](https://arxiv.org/abs/2309.17448) | SMPLer-X | NeurIPS 2023 |
| [2310.12978](https://arxiv.org/abs/2310.12978) | HumanTOMATO | ICML 2024 |
| [2310.17768](https://arxiv.org/abs/2310.17768) | Re:InterHand | NeurIPS 2023 |
| [2312.00063](https://arxiv.org/abs/2312.00063) | MoMask | CVPR 2024 |
| [2312.05251](https://arxiv.org/abs/2312.05251) | HaMeR | CVPR 2024 |
| [2401.00374](https://arxiv.org/abs/2401.00374) | BEAT2 (EMAGE) | CVPR 2024 |
| [2401.04747](https://arxiv.org/abs/2401.04747) | DiffSHEG | 2024 |
| [2401.05334](https://arxiv.org/abs/2401.05334) | URHand | CVPR 2024 |
| [2403.17934](https://arxiv.org/abs/2403.17934) | AiOS | CVPR 2024 |
| [2404.04819](https://arxiv.org/abs/2404.04819) | CONTHO | CVPR 2024 |
| [2405.07933](https://arxiv.org/abs/2405.07933) | UHM | CVPR 2024 |
| [2407.21686](https://arxiv.org/abs/2407.21686) | ExAvatar | ECCV 2024 |
| [2409.12259](https://arxiv.org/abs/2409.12259) | WiLoR | CVPR 2025 |
| [2410.13911](https://arxiv.org/abs/2410.13911) | GraspDiffusion | 2024 |
| [2412.11785](https://arxiv.org/abs/2412.11785) | InterDyn | CVPR 2025 |
| [2506.07460](https://arxiv.org/abs/2506.07460) | SIGNER | ECCV 2026 |
| [2506.09995](https://arxiv.org/abs/2506.09995) | PlayerOne | 프리프린트 2025 |
| [2506.21552](https://arxiv.org/abs/2506.21552) | PEVA | 프리프린트 2025 |
| [2508.09973](https://arxiv.org/abs/2508.09973) | PERSONA | ICCV 2025 |
| [2510.14874](https://arxiv.org/abs/2510.14874) | TOUCH | 2025 |
| [2512.14234](https://arxiv.org/abs/2512.14234) | Converse3D (ViBES) | CVPR 2026 |
| [2512.17907](https://arxiv.org/abs/2512.17907) | DWM | 프리프린트 2025 |
| [2602.04672](https://arxiv.org/abs/2602.04672) | AGILE | 2026 |
| [2602.06226](https://arxiv.org/abs/2602.06226) | ForeHOI | 2026 |
| [2602.09600](https://arxiv.org/abs/2602.09600) | Hand2World | 프리프린트 2026 |
| [2602.18422](https://arxiv.org/abs/2602.18422) | Generated Reality | 프리프린트 2026 |
| [2603.14726](https://arxiv.org/abs/2603.14726) | Hand4Whole++ | CVPR 2026 |
| [2603.14772](https://arxiv.org/abs/2603.14772) | DynaAvatar | CVPR 2026 |
| [2605.08606](https://arxiv.org/abs/2605.08606) | Egocentric WB-HMR | ICIP 2026 |
| [2605.12498](https://arxiv.org/abs/2605.12498) | EgoForce | SIGGRAPH 2026 |
| [2605.15477](https://arxiv.org/abs/2605.15477) | EgoExo-WM | 프리프린트 2026 |
| [2605.18102](https://arxiv.org/abs/2605.18102) | DanceHMR | 프리프린트 2026 |
| [2606.30598](https://arxiv.org/abs/2606.30598) | HOPformer | ECCV 2026 |
| [2607.02075](https://arxiv.org/abs/2607.02075) | HandsOnWorld | 프리프린트 2026 |
| [2607.13646](https://arxiv.org/abs/2607.13646) | Human4K | 프리프린트 2026 |
| [2608.02580](https://arxiv.org/abs/2608.02580) | Ego2Robot | 2026 |
| [2608.04196](https://arxiv.org/abs/2608.04196) | SiMDex | 2026 |
| [2608.12122](https://arxiv.org/abs/2608.12122) | HandEdit | 프리프린트 2026 |
| [2608.20308](https://arxiv.org/abs/2608.20308) | DreamHand | 프리프린트 2026 |
| [2609.04250](https://arxiv.org/abs/2609.04250) | Motion-Omni | 프리프린트 2026 |

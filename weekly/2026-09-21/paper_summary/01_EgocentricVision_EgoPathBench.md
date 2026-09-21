# EgoPathBench: Evaluating Zero-Shot Egocentric Waypoint Decision-Making in Vision-Language Models

**arXiv**: 2609.16610 | **주제 분류**: Egocentric Vision | **출판일**: 2026-09-15 | **학회**: 프리프린트 (Comments: "18 pages, including supplementary material")
**저자/소속**: Yang Zhao, Zhuo Chen, Xubo Yang (Shanghai Jiao Tong University)
**링크**: https://arxiv.org/abs/2609.16610

## 한 줄 요약

1인칭 RGB 한 장 위에 번호가 붙은 waypoint(이동 후보 지점)를 겹쳐 놓고, "목표까지 갈 수 있는 순서 있는 경로를 고르라"는 단일 인터페이스로 VLM의 통합적 공간 지능을 재는 벤치마크 EgoPathBench를 제안한다. 아홉 개 최신 VLM 중 최고 EgoPath Score가 28.3에 불과하고, 몸 크기를 고려해야 하는 Embodied Path 성공률은 최고 2.9%로 무너진다.

## 메인 그림

![EgoPathBench의 개념적 동기: 같은 1인칭 장면에서 물체 인식과 국소 공간 질문은 맞히지만, 목표에 도달하는 완전한 경로를 구성하는 데는 실패한다](https://arxiv.org/html/2609.16610v1/fig_overview_zy.png)

Figure 1 (Conceptual motivation). 왼쪽은 같은 1인칭 장면에서 "저게 무엇인가", "무엇이 어디 있는가" 같은 익숙한 인식·국소 공간 질문에는 모델이 올바로 답하는 모습이다. 오른쪽은 목표에 실제로 도달하는 완전한 경로와, 경로/목표 조건을 위반하는 잘못된 경로를 나란히 놓는다. 논문의 출발점은 이 대비다 — 부분 능력이 있다고 해서 그것들이 하나의 행동 시퀀스 위에서 함께 작동한다는 보장은 없다.

![EgoPathBench 구축 파이프라인: 장면·시점·타깃 선정 → 가시 waypoint 및 point/embodied 내비게이션 그래프 생성 → 기하 검증된 참조 경로 → 질문·Spatial CoT 생성](https://arxiv.org/html/2609.16610v1/fig_construction_pipeline_zy.png)

Figure 2 (Construction pipeline). 기하 라벨(타깃, waypoint, 가능 간선, 도달 가능 목표 영역, 참조 경로)을 **먼저 고정한 뒤에야** 자연어 질문과 Spatial CoT를 생성한다. 언어가 기하 ground truth보다 항상 하류(downstream)에 놓이는 구조다.

---

## 선행 연구

이 논문이 올라선 흐름은 크게 세 갈래다.

**1) Vision-language navigation과 foundation-model 기반 내비게이션**

R2R, REVERIE, RxR, VLN-CE가 이산·연속 실내 환경에서 vision-language navigation(언어 지시를 따라 이동하는 문제)을 정립했다. 그 위에 foundation model 에이전트가 올라왔다 — NavGPT는 언어 추론으로 내비게이션을 명시적으로 풀었고, NaviLLM은 generalist embodied 모델을, NaVid는 영상 기반 다음 스텝 계획을 시도했다.

최근 zero-shot 시스템들은 "공간적 결정"을 서로 다른 인터페이스로 조직한다. SmartWay는 waypoint 예측에 history-aware backtracking을 결합했고, VLFM·InstructNav·CA-Nav는 occupancy/value map과 sub-instruction 제약을 쓴다. AgenticNav와 P2DNav는 픽셀 수준 또는 계층적 "방향→grounding" 행동을 노출하고, DreamNav는 개별 점 대신 궤적 자체를 예측한다. Open-Nav는 오픈소스 모델의 시공간 추론을, [Nav-R1](https://arxiv.org/abs/2509.10884)은 구조화된 내비게이션 trace 학습을, LHPR-VLN은 장기 horizon 서브태스크 간 결정 일관성을 다룬다.

핵심은 이 **완전한 내비게이션 시스템들의 성능이 candidate 생성, 매핑, 메모리, 제어, 재계획 등 여러 모듈의 조합에 달려 있다**는 점이다. 그래서 "foundation VLM 자체의 공간적 판단력"만 떼어내 재기가 어렵다.

**2) Spatial intelligence 벤치마크**

[SpatialVLM](https://arxiv.org/abs/2401.12168)과 SpatialEval은 거리·방향·공간 관계 판단을, [VSI-Bench](https://arxiv.org/abs/2412.14171)(Thinking in Space)는 영상 기반 공간 이해와 기억을, [ViewSpatial-Bench](https://arxiv.org/abs/2505.21500)는 다중 시점 공간 위치 파악을, 3DSRBench는 3D 구조 추론을 평가한다. 1인칭·embodied 관측으로 확장한 쪽은 EmbSpatial-Bench, [EgoThink](https://arxiv.org/abs/2311.15596), OpenEQA다. 더 최근에는 [Embodied3DBench](https://arxiv.org/abs/2605.29074)가 grounding·affordance·궤적 예측 같은 저수준 embodied 기술을, [CapNav](https://arxiv.org/abs/2602.18424)가 에이전트별 이동 제약을 조건으로 한 내비게이션을, [IndustryNav](https://arxiv.org/abs/2511.17384)가 동적 산업 환경에서의 능동 계획과 충돌 인지 내비게이션을 평가한다.

이들은 모두 **개별 판단을 고립시켜 측정**한다. 관계, 방향, 타깃을 따로따로 묻는다.

**3) 가장 가까운 선행 연구: NaviTrace**

[NaviTrace](https://arxiv.org/abs/2510.26909)는 실제 RGB 한 장, 내비게이션 지시, embodiment 설명을 주고 이미지 공간의 **연속적 trace**를 그리게 한다. 채점은 사람이 주석한 trace와의 Dynamic Time Warping 유사도, 끝점 오차, 픽셀 semantic에서 유도한 embodiment 페널티의 조합이다. 즉 **전문가 시연과의 일치도**를 잰다.

EgoPathBench는 여기서 갈라진다. 각 이미지가 3D 장면 표현에 등록(register)돼 있어 가시 waypoint, 에이전트별 feasibility, waypoint 간 직접 통행 가능성, 도달 가능 목표 영역이 모두 기하에서 유도된다. 덕분에 **임의의** 예측 경로를 "선택된 행동들의 기하학적 결과"로 채점할 수 있다. 참조 경로는 "해가 존재한다"는 증명서일 뿐, 반드시 모방해야 하는 유일한 정답이 아니다. NaviTrace가 시연 일치도를 잰다면, EgoPathBench는 **행동의 결과**를 잰다.

## 문제 제기

논문이 지적하는 빈틈은 명확하다.

**❶ 기존 공간 지능 벤치마크는 "고립된 판단"만 잰다.** 관계, 방향, 타깃을 개별 문항으로 물으면 그 능력들이 *함께* 작동하는지는 측정되지 않는다. 내비게이션 결정은 타깃 인식, 행동의 결과 평가, 거리 추정, 경로 계획을 **동시에** 요구한다.

**❷ 완전한 내비게이션 시스템 평가는 교란 요인이 너무 많다.** 매핑, 위치추정, 메모리, 제어, 재계획, 복구가 결과에 섞여 들어가므로 "VLM 자체의 공간적 결정 능력"을 분리할 수 없다.

**❸ 시연 기반 채점은 대안 해를 벌한다.** NaviTrace처럼 사람 시연과의 유사도로 채점하면, 기하학적으로 완벽히 타당하지만 시연과 다른 경로가 불이익을 받는다.

**❹ Embodiment(몸의 크기)가 행동 가능성을 바꾼다는 사실이 평가에 잘 반영되지 않는다.** 점(point) 에이전트에게 통과 가능한 좁은 틈이 지름 0.6 m 로봇에게는 막힌 길이다. 같은 화면, 같은 후보 지점인데 결과가 달라진다.

## 연구 주제

논문이 세우는 문제 정의는 **first-person waypoint decision-making** 이다. 핵심 아이디어는 waypoint 선택을 "통합된 공간 지능을 재기 위한 통제된 측정 기판(controlled measurement substrate)"으로 삼는 것이다.

인터페이스는 하나로 통일돼 있다.

- **입력**: 1인칭 RGB 이미지 + 번호가 겹쳐진 가시 waypoint 후보들 + 자연어 프롬프트
- **출력**: 표시된 display ID들의 JSON 배열 — traversability 과제는 순서 없는 집합, path 과제는 순서 있는 경로

형식적으로 하나의 예제는 관측 $o$, 표시된 waypoint 집합 $A$, 타깃 명세 $t$, 과제별 feasibility graph $G$로 구성된다. $A$의 모든 display ID는 3D 장면 좌표에 고정(anchor)돼 있다. 모델은 $A$의 부분집합 또는 $A$ 위의 순서열을 예측한다.

**Point 그래프**는 몸 너비를 고려하지 않은 기하학적 연결성만 담고, **Embodied 그래프**는 에이전트 footprint까지 반영한다. 따라서 **시각적으로 완전히 동일한 행동이 두 에이전트 모델 아래서 다른 결과를 낳는다** — 이 대비가 벤치마크 설계의 중심축이다.

## 연구 방법

### A. 다섯 개 과제 설계

다섯 과제는 공통 입출력 인터페이스를 유지하면서 target grounding, embodiment, 경로 구성 요구를 점진적으로 추가한다.

| Task | Goal | Agent | Output | 채점 제약 | 문항 수 |
|---|---|---|---|---|---|
| Point Traversability | – | Point | Set | Traversability | 146 |
| Embodied Traversability | – | Emb. | Set | Feasibility | 146 |
| Point Path | Explicit | Point | Route | Edges, endpoint | 309 |
| Embodied Path | Explicit | Emb. | Route | Footprint, edges, goal | 309 |
| Intent Path | Intent | Emb. | Route | Intent, footprint, edges | 201 |

- **Point Traversability**: 점 에이전트가 갈 수 있는 후보를 모두 고르기.
- **Embodied Traversability**: 같은 장면·같은 후보지만 에이전트 footprint를 고려해 충분한 여유 공간이 있는 곳만 고르기. 관측을 고정한 채 embodiment만 바꿔 행동 가능성이 어떻게 달라지는지 본다.
- **Point Path**: 명시적 타깃까지 점 에이전트 경로를 순서대로.
- **Embodied Path**: 타깃·시점·후보 공간을 그대로 두고 embodied feasibility로 채점.
- **Intent Path**: 물체 이름 대신 **의도(intent)와 시각적 단서**로 타깃을 기술한다. 모델은 먼저 무엇을 가리키는지 해소(resolve)한 뒤 embodied 경로를 골라야 한다.

프롬프트 예시(Table S2)를 보면 embodied 과제에서 몸 지름이 명시적으로 주어진다 — "your body diameter is 0.6 m. Start at display ID 1."

### B. 데이터 구축 파이프라인

**장면, 시점, 타깃.** InternScenes로 정규화된 시뮬레이션 가능 실내 자산을 쓴다. 원 출처는 3RScan, ScanNet, ARKitScenes, Matterport3D다. 저자들은 이 자산에서 기하와 렌더링만 가져오고, **1인칭 관측·waypoint 주석·경로 라벨·질문 데이터는 직접 구축**했다.

각 장면에서 통행 가능 공간에 1인칭 카메라를 샘플링하고, 카메라 바로 앞이 막힌 시점은 제거한다. 타깃 인스턴스는 frustum 투영, 관측 거리, 투영 크기, 가시 표면 증거로 필터링해 화면 밖이거나 너무 작거나 심하게 가려진 것을 뺀다.

**Waypoint와 기하 라벨.** 각 시점에 두 종류의 마커를 투영한다 — (a) 바닥 행동 후보, (b) 물체·구조물 표면 위 지점을 **통행 불가 음성 샘플(negative)** 로 쓴 것. Depth, ray-visibility, 마커 간격 검사로 모든 display ID가 서로 다른 장면 위치에 대응하도록 하면서 마커 겹침과 전경 가림을 줄인다.

여기가 중요하다. Traversability 예제는 **통행 가능한 바닥 행동 + 여유 공간에 민감한(clearance-sensitive) 바닥 행동 + 가시 표면 음성 샘플**을 섞는다. 그래서 **"전부 다 고르기" 전략으로는 풀 수 없다.**

**Paired route construction.** 각 경로 단위마다 이미지 아래쪽 가시 바닥에 시작점을 고정하고, 타깃 footprint 주변에 도달 가능한 목표 위치들을 생성한다. 그런 다음 point free space와 embodied free space를 **각각 따로** 탐색해 연속 경로를 sparse waypoint로 변환하고, 필요한 waypoint를 현재 이미지에 다시 투영한다. 연결성, 과제별 feasibility, 타깃 영역 도달, 필요한 waypoint의 표시 여부를 모두 검사하고 실패한 경로는 버린다. **모든 경로 문항은 최소 한 개의 장면 검증된 참조 경로를 보유한다.**

Point Path와 Embodied Path는 타깃·시작점·장면 시점을 공유하면서 각자의 에이전트 기하로 검증된 경로를 갖는다 — 통제된 쌍(paired) 비교가 성립한다.

**질문 텍스트와 Spatial CoT.** 타깃 정체, 표시 waypoint, 목표 영역, 참조 경로가 **언어 생성 이전에** 전부 고정된다. Intent Path는 시점별 후보 universe를 만들고 지원되는 관계·속성·색·거리 단서로 타깃 서술을 생성한 뒤, 그 서술이 현재 시점의 물체들 사이에서 **유일하게** 타깃을 지목할 때만 채택한다. Intent Path는 이미 승인된 Embodied Path 인스턴스에서 파생되므로, 언어 명세만 바뀌고 타깃·경로 기하는 동일하다.

학습 split에는 Spatial CoT가 추가된다. GPT-5.5가 고정된 타깃·후보·feasibility 라벨·가능 간선·참조 경로를 과제별 추론 텍스트로 말로 풀어내고, 내보낸 답은 형식 주석과 대조 검사한다.

### C. 품질 관리와 벤치마크 선정

기하와 시점-행동 검사를 **언어가 붙기 전에** 적용한다. 후보 위치, 경로 간선, 타깃 영역이 하나의 장면 좌표계를 공유하며, 끊긴 경로·충돌하는 경로·타깃 영역을 놓친 경로·필요한 display waypoint가 없는 예제는 제거한다. 이후 타깃·프롬프트·표시 waypoint·참조 경로·정답 전반에 대한 시각-언어 정렬 감사를 수행한다.

벤치마크는 전체 문항 풀에서 **어려운 부분집합**으로 고른다 — 장면 혼잡도, traversability 경계, point와 embodied의 feasibility 차이, 경쟁 타깃, 경로 구성을 강조한다. 선정은 **번들 단위**로 이뤄진다. Point/Embodied Traversability가 한 쌍, Point/Embodied Path가 타깃·후보 공간을 공유하는 한 쌍이며, 적격 Intent Path는 대응 embodied 경로와 함께 간다. 쌍의 한쪽만 남는 일을 막기 위해서다. Split은 source group 단위로 나눠 같은 원본 스캔이 train/val/benchmark를 넘나들지 않게 한다.

**최종 릴리스: 31,852 training / 1,345 validation / 1,111 benchmark 문항.**

| Split | Scenes | Views | Routes | Targets | Questions |
|---|---|---|---|---|---|
| Train | 2,942 | 6,483 | 7,843 | 6,144 | 31,852 |
| Val | 32 | 200 | 368 | 179 | 1,345 |
| Benchmark | 255 | 365 | 309 | 281 | 1,111 |

벤치마크 경로 구조 통계를 보면 문제가 쉽지 않다는 게 드러난다.

| Signal | N | Median | P90 | Max |
|---|---|---|---|---|
| Same-type target ambiguity | 819 | 4 | 8 | 16 |
| Reference segments (Point Path) | 309 | 1 | 2 | 3 |
| Reference segments (Body Path) | 309 | 2 | 3 | 9 |
| Reference segments (Intent Path) | 201 | 2 | 3 | 9 |
| Reference path length | 819 | 3.2 m | 4.8 m | 8.5 m |
| Embodied narrow-passage fraction | 510 | 40% | 81% | 100% |

같은 종류의 물체가 중앙값 4개 존재하고(타깃 모호성), embodied 경로는 길이의 중앙값 40%를 좁은 통로에서 보낸다.

### D. 평가 지표

- **Traversability**: **BA**(balanced accuracy, 통행 가능/불가 두 클래스의 평균 recall), **F1**(가능 후보에 대한 precision-recall 조화평균).
- **Route**: **VPR**(valid path rate, 경로 전체의 합법성), **SR**(success rate, 여기에 허용 가능한 끝점 도달까지 요구), **SPL**(success weighted by path length, 최단 합법 참조보다 긴 성공 경로를 할인하고 실패는 0).

$\text{BA} = \frac{\text{TPR} + \text{TNR}}{2}$, $\ \text{VPR} = \frac{1}{N}\sum_i V_i$, $\ \text{SR} = \frac{1}{N}\sum_i S_i$, $\ \text{SPL} = \frac{1}{N}\sum_i S_i \frac{\ell_i}{\max(\ell_i, p_i)}$

여기서 $V_i$는 예측 $i$가 파싱 가능하고, 유효 ID만 쓰고, 요구된 시작점에서 출발하며, 연속하는 모든 간선이 합법임을 뜻한다. $S_i$는 여기에 허용 끝점까지 요구한다. $\ell_i$는 허용 목표까지의 최단 합법 참조 길이, $p_i$는 예측 경로 길이다.

종합 지표는 **chance-adjusted** traversability와 route SR의 동일 가중 5과제 매크로 평균이다.

$\text{EgoPathScore} = \frac{100}{5}\left[(2\,\text{BA}_{\text{PT}} - 1) + (2\,\text{BA}_{\text{ET}} - 1) + \text{SR}_{\text{PP}} + \text{SR}_{\text{EP}} + \text{SR}_{\text{IP}}\right]$

$2\text{BA}-1$ 변환은 "무작위로 찍으면 0"이 되도록 맞춘 것이다.

**Route evaluator**는 정해진 순서로 검사를 통과시킨다 — Parse → Candidate(모든 ID가 가시·허용) → Start(첫 ID가 요구된 시작점) → Edge(연속 쌍이 모두 합법 직접 간선) → Endpoint(마지막 ID가 허용 목표) → Efficiency(SPL). SPL은 성공 이후에만 계산된다.

### E. 실험 설정

아홉 개 foundation VLM을 평가한다: claude-opus-4-8, gemini-3.1-pro-preview, gpt-5.5, grok-4.3-fast, kimi-k2.6, llama-4-maverick-17b-128e-instruct, MiniMax-M3, mistral-large-3-675b-instruct-2512, qwen3.6-plus. 모두 동일한 이미지·프롬프트·waypoint ID·JSON 출력 규약을 받고 같은 evaluator로 채점된다. 완성 토큰 예산 8,192, temperature 0, top-p 1(노출된 경우).

학습 자원 검증으로 **Qwen3.5-4B**를 LoRA(rank 8, alpha 16, dropout 0)로 vision tower를 동결한 채 파인튜닝한다. 1단계는 per-device batch 1, gradient accumulation 8, $10^{-4}$에서 cosine 스케줄, warmup 10%, 2 epoch, seed 42. 2단계는 최종 adapter에서 이어서 $\times 10^{-5}$로 2 epoch 더, warmup 5%. 둘 다 bfloat16, 4,096 토큰 cutoff, 최대 이미지 면적 262,144 픽셀. **NVIDIA A100 80GB 2장** 사용.

## 실험 결과 / 연구 의의

### 1) Zero-shot 리더보드 (Table 2, %)

**Traversability (BA / F1)**

| Model | Score | Point Trav. BA | Point Trav. F1 | Emb. Trav. BA | Emb. Trav. F1 |
|---|---|---|---|---|---|
| Gemini 3.1 Pro | **28.3** | 76.5 | **79.0** | 72.7 | 56.2 |
| GPT-5.5 | 27.3 | 74.1 | 77.1 | **77.3** | **62.5** |
| Claude Opus 4.8 | 25.6 | **77.9** | 74.3 | 73.5 | 59.6 |
| MiniMax M3 | 21.8 | 77.0 | 76.2 | 68.7 | 52.8 |
| Qwen 3.6 | 16.4 | 67.4 | 72.1 | 64.8 | 49.1 |
| Mistral L3 | 15.8 | 65.2 | 70.8 | 68.5 | 52.5 |
| Llama 4 | 14.9 | 66.8 | 66.5 | 66.0 | 49.8 |
| Kimi K2.6 | 9.7 | 60.2 | 69.8 | 57.8 | 44.2 |
| Grok 4.3 | 1.4 | 52.3 | 58.4 | 50.0 | 35.8 |

**Route (VPR / SR / SPL)**

| Model | Point VPR | Point SR | Point SPL | Emb. VPR | Emb. SR | Emb. SPL | Intent VPR | Intent SR | Intent SPL |
|---|---|---|---|---|---|---|---|---|---|
| Gemini 3.1 Pro | 63.7 | **35.9** | **28.7** | 9.1 | **2.9** | **2.4** | 10.4 | **4.0** | **3.3** |
| GPT-5.5 | 60.5 | 31.1 | 24.8 | 5.5 | 1.3 | 1.3 | 9.0 | 1.5 | 1.4 |
| Claude Opus 4.8 | **66.0** | 21.0 | 16.7 | **12.0** | 1.6 | 1.5 | **14.4** | 2.5 | 2.2 |
| MiniMax M3 | 50.8 | 13.3 | 8.7 | 5.5 | 1.9 | 1.7 | 9.0 | 2.5 | 2.3 |
| Qwen 3.6 | 49.2 | 15.2 | 10.9 | 2.6 | 1.0 | 0.9 | 5.0 | 1.5 | 1.3 |
| Mistral L3 | 35.6 | 11.0 | 5.8 | 0.3 | 0.0 | 0.0 | 3.5 | 0.5 | 0.5 |
| Llama 4 | 36.2 | 8.7 | 5.9 | 1.9 | 0.0 | 0.0 | 2.0 | 0.0 | 0.0 |
| Kimi K2.6 | 40.5 | 11.7 | 8.2 | 1.3 | 0.7 | 0.5 | 1.5 | 0.5 | 0.4 |
| Grok 4.3 | 18.4 | 2.6 | 1.2 | 5.2 | 0.0 | 0.0 | 3.5 | 0.0 | 0.0 |

읽을 점:

**(a) 후보 수준 판단과 완전한 경로 구성 사이의 격차가 극단적이다.** Point/Embodied Traversability 최고 BA는 77.9%와 77.3%인데, Point Path SR은 35.9%, Embodied Path SR은 **2.9%**, Intent Path SR은 **4.0%**다. 국소적으로 그럴듯한 행동을 고르는 것과, 합법적이고 목표에 도달하는 경로를 만드는 것은 완전히 다른 능력이다.

**(b) Embodiment 제약이 가장 큰 하락을 만든다.** 같은 장면·같은 타깃·같은 후보 공간인데 point → embodied로 바꾸는 순간 Gemini 3.1 Pro의 SR이 35.9% → 2.9%로 떨어진다. 모델은 "몸이 지나갈 수 있는가"를 경로 전체에 걸쳐 유지하지 못한다.

**(c) VPR과 SR의 격차가 크다.** Claude Opus 4.8은 Point Path VPR 66.0%로 1위지만 SR은 21.0%로 3위다. 즉 "합법적이지만 목표에 도달하지 않는" 경로를 자주 낸다. 반대로 Gemini 3.1 Pro는 VPR 63.7%로 2위인데 SR 35.9%로 1위다. 간선 합법성과 끝점 선택은 **서로 보완적인 별개 실패 모드**다.

**(d) SPL이 낮은 것은 대부분 성공 자체가 희소하기 때문이다** — 실패는 SPL 0을 받으므로.

**(e) 집계 방식에 강건하다.** Route SR을 SPL로 바꾸거나, traversability/route 두 family 안에서 먼저 평균 낸 뒤 두 family를 동일 가중해도 **아홉 모델의 순위가 그대로 보존된다**(두 대안 모두 Spearman $\rho = 1.0$).

### 2) 사람과의 동일 문항 비교 (Figure 4, Table S9)

다섯 과제에서 10문항씩 무작위로 50문항을 뽑아 자원자에게 동일 인터페이스로 풀게 했다.

| Evaluator | EgoPath Score | Valid path |
|---|---|---|
| Human calibration | **54.2** | **70.0** |
| GPT-5.5 | 28.6 | 26.7 |
| Claude Opus 4.8 | 26.6 | 23.3 |
| Gemini 3.1 Pro | 23.2 | 26.7 |
| Llama 4 | 18.9 | 20.0 |
| MiniMax M3 | 17.6 | 16.7 |
| Qwen 3.6 | 15.6 | 20.0 |
| Mistral L3 | 11.3 | 16.7 |
| Kimi K2.6 | 9.7 | 13.3 |
| Grok 4.3 | 0.8 | 10.0 |

세 경로 과제 평균에서 사람은 VPR 70.0% / SR 46.7%, 최강 VLM은 26.7% / 13.3%다. 사람이 **다섯 과제 축 전부에서** 우위이므로, 격차가 특정 과제나 지표 때문이 아니라 1인칭 공간 결정 능력 전반의 한계를 반영한다는 뜻이다. 논문은 이를 "population-level 인간 천장의 추정치가 아니라 같은 인터페이스의 참조점"이라고 명시적으로 한정한다.

### 3) 경로는 어디서 무너지는가 (Figure 3, 아홉 모델 통합)

논문의 가장 값진 분석이다. 경로 예측을 다섯 진단으로 분해한다.

| 진단 항목 | Point Path | Embodied Path | Intent Path |
|---|---|---|---|
| 평가 가능한(evaluable) 출력 | 96.3–96.8% 범위 (세 과제 공통) | | |
| 목표 일치 끝점 선택 | 28.9% | 4.8% | 5.2% |
| 첫 행동(first edge)이 합법 | 96.0% | 90.4% | 88.0% |
| 전체 경로 합법 | 46.8% | 4.8% | 6.5% |
| Joint success (합법 + 올바른 끝점) | 16.7% | 1.0% | 1.4% |

읽을 점:

- **출력 형식은 병목이 아니다.** 96.3~96.8%가 평가 가능한 경로다. JSON 규약을 못 지켜서 실패하는 게 아니다.
- **끝점 선택이 어렵다.** 목표 일치 끝점 비율이 Point 28.9%, Embodied 4.8%, Intent 5.2%. 논문의 해석이 날카롭다 — 모델은 **타깃 물체가 어디 있는지는 알아보면서도, 그 근처에서 해당 에이전트가 실제로 설 수 있는 종착 waypoint를 짚어내지 못한다.**
- **첫 행동은 잘 고르지만 그 국소 타당성이 시퀀스를 따라 이어지지 않는다.** 첫 간선이 합법인 예측 중 **51.3%(Point), 94.7%(Embodied), 92.7%(Intent)** 가 뒤쪽에 불법 간선을 포함한다.

**이 "suffix 실패"는 양 끝을 통제해도 남는다.** 첫 간선이 합법이고 끝점도 올바른 예측만 골라도, Point 42.2% / Embodied 75.8% / Intent 69.4%가 여전히 중간에 불법 간선을 갖는다.

| Task | 첫 간선 합법 + 끝점 정확 | 뒤쪽 불법 간선 | 전체 경로 합법 |
|---|---|---|---|
| Point | 805 | 340 (42.2%) | 465 (57.8%) |
| Embodied | 120 | 91 (75.8%) | 29 (24.2%) |
| Intent | 85 | 59 (69.4%) | 26 (30.6%) |

waypoint가 적은 절반의 문항으로 좁혀도 42.8% / 76.6% / 67.3%로 거의 변하지 않는다 — **조밀한 마커 오버레이가 원인이 아니다.**

**참조 경로 길이도 원인이 아니다.** 참조가 간선 1개뿐인 문항에서도 불법 간선 발생률이 Embodied 90.6%, Intent 88.4%이고, 간선 3개 이상에서 94.0%, 92.4%로 오른다. 길이는 악화 요인이지 근본 원인이 아니다.

| Task | Edges | N | End hit | Success | Illegal edge |
|---|---|---|---|---|---|
| Point | 1 | 250 | 29.5 | 17.8 | 47.2 |
| Point | ≥2 | 59 | 26.7 | 12.1 | 59.5 |
| Embodied | 1 | 135 | 4.4 | 1.6 | 90.6 |
| Embodied | 2 | 90 | 5.2 | 0.6 | 92.2 |
| Embodied | ≥3 | 84 | 4.9 | 0.5 | 94.0 |
| Intent | 1 | 91 | 5.4 | 2.3 | 88.4 |
| Intent | 2 | 56 | 7.5 | 1.4 | 90.1 |
| Intent | ≥3 | 54 | 2.5 | 0.0 | 92.4 |

결론: 두 개의 뚜렷한 한계가 드러난다 — **(1) 의도한 종착 waypoint 선택, (2) 현재 위치에서 그 끝점까지 에이전트별 feasibility 유지.**

### 4) 벤치마크 자체의 타당성 검증

**입력 의존성 (Table S5, route SR %, Point/Embodied/Intent).** 이미지를 빼거나 waypoint 오버레이를 어긋나게 바꾸면 성능이 무너진다 — 즉 모델은 프롬프트 텍스트만으로 푸는 게 아니라 실제로 **짝지어진 시각 입력에 의존**한다.

| Model | Full | Text only | Mismatched overlay |
|---|---|---|---|
| GPT-5.5 | 30.0/0.0/4.0 | 0.0/0.0/0.0 | 10.0/0.0/0.0 |
| Claude Opus 4.8 | 28.0/0.0/0.0 | 0.0/0.0/0.0 | 4.0/0.0/0.0 |
| Qwen 3.6 | 16.0/0.0/0.0 | 0.0/0.0/0.0 | 2.0/0.0/0.0 |

**Scene-consequence audit.** 기하학적으로 불법 간선을 최소 하나 포함한 5,563개 경로 예측(Point 1,377 / Embodied 2,559 / Intent 1,627)에서 각각 불법 간선 하나를 골라, 공식 0.30 m embodied 반지름으로 swept corridor를 0.05 m 간격 샘플링하고 정렬된 depth·object-index 렌더에서 장애물 증거를 찾았다. **4,934건(88.7%)** 에서 명시적으로 등록된 장애물이 복원됐다(4,662건 83.8%는 depth로, 추가 272건 4.9%는 object-index 렌더로). 나머지 629건(11.3%)은 보조 렌더로는 결론이 나지 않은 것이지 라벨이 틀렸다는 증거는 아니다. **"불법"이라는 라벨이 실제 물리적 충돌에 대응한다는 것을 보인 검증이다.**

**기하 민감도 (Table S8).** 공칭 0.30 m 반지름, 0.05 m occupancy grid, 0.10 m goal ring을 흔들어봐도 **아홉 모델 순위가 완전히 보존된다**(모든 변형에서 rank $\rho = 1.0$). 성공 flip은 최대 1.1%.

| Variant | Ref. 유지 | Edge flip | Success flip | Rank ρ |
|---|---|---|---|---|
| Radius 0.25 m | 100.0 | 2.4 | 0.2 | 1.00 |
| Radius 0.35 m | 67.6 | 8.5 | 0.5 | 1.00 |
| Grid 0.04 m | 91.6 | 5.3 | 0.9 | 1.00 |
| Grid 0.06 m | 89.5 | 6.0 | 1.1 | 1.00 |
| Goal ring 0.05 m | 99.8 | 0.0 | 0.1 | 1.00 |
| Goal ring 0.15 m | 100.0 | 0.0 | 0.1 | 1.00 |

**가시성 민감도 (Table S7).** 타깃 bbox 짧은 변 ≥64 px, 가시 표면 ≥50%를 요구하는 strict 부분집합에서도 결론이 유지된다 — Embodied 전체 4.8/1.0 vs strict 5.9/1.6(끝점 적중/전체 경로 성공). 즉 **"타깃이 잘 안 보여서" 실패하는 게 아니다.**

### 5) 학습 자원 검증

공개된 training split으로 Qwen3.5-4B를 파인튜닝한 결과가 인상적이다.

| Model | Score | PT BA | PT F1 | ET BA | ET F1 | PP VPR | PP SR | PP SPL | EP VPR | EP SR | EP SPL | IP VPR | IP SR | IP SPL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-4B base | 3.9 | 54.6 | 55.6 | 54.9 | 33.1 | 9.1 | 0.7 | 0.1 | 0.3 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| + EgoPathBench SFT | **38.9** | **89.3** | **89.2** | **83.4** | **71.2** | **77.0** | 31.4 | 28.6 | **34.9** | **7.1** | **6.9** | **44.8** | **10.4** | **10.0** |

EgoPath Score 3.9 → **38.9**. 4B 모델이 모든 zero-shot foundation VLM(최고 28.3)을 넘어선다. 특히 Embodied Path SR 0.0 → 7.1%, Intent Path SR 0.0 → 10.4%로, 어떤 zero-shot 모델보다도 높다.

**외부 벤치마크 전이 (Table 3, %)**

| Benchmark | Setting | Base | SFT | Δ |
|---|---|---|---|---|
| VSI-Bench Route Planning | Full | 29.38 | 33.51 | +4.13 |
| VSI-Bench Route Planning | Debiased | 20.18 | 24.56 | +4.38 |
| SpatialEval-VTQA | Full | 61.8 | 71.4 | +9.6 |
| 3DSRBench | Full | 58.0 | 59.4 | +1.4 |

네 개 평가 전부 개선됐고 폭은 1.4~9.6점이다. **EgoPathBench 데이터가 in-domain 과적합이 아니라 일반적 공간 능력에 기여한다**는 증거다.

### 연구 의의 요약

1. **"부분 공간 능력이 있다"는 것과 "그것들이 하나의 행동 시퀀스 위에서 함께 작동한다"는 것은 전혀 다르다.** Traversability BA 77%대 vs Embodied Path SR 2.9%라는 격차가 이 주장의 직접 증거다.
2. **Embodiment가 결정적 변수다.** 관측·타깃·후보 공간을 완전히 고정한 채 에이전트 기하만 바꾸는 paired 설계 덕분에, 성능 하락을 다른 요인 탓으로 돌릴 수 없다.
3. **실패 모드가 구체적으로 특정됐다** — 끝점 grounding과 중간 구간 feasibility 유지. 출력 형식, 마커 밀도, 경로 길이, 타깃 가시성은 모두 배제됐다.
4. **기하로 채점한다는 설계가 대안 해를 허용한다.** 참조 경로는 존재 증명이지 모방 대상이 아니다. NaviTrace식 시연 일치 채점과 근본적으로 다른 지점이다.
5. **평가 데이터가 곧 학습 자원이 된다.** 기하 검증된 정답 + Spatial CoT 감독이 4B 모델을 대형 모델 이상으로 끌어올리고 외부 벤치마크로도 전이된다.

## 한계

**논문이 스스로 밝힌 것**

- **사람 참조는 탐색적이다.** 자원자 한 명이 다섯 과제 × 10문항 = 50문항만 풀었다. 논문은 이것이 "population-level 인간 천장의 추정치가 아니라 같은 인터페이스의 참조점"이라고 직접 한정한다.
- **Scene-consequence audit의 11.3%는 결론 미정이다.** 4,934/5,563건에서 장애물 증거를 복원했지만 나머지 629건은 보조 렌더로 확인되지 않았다(라벨이 틀렸다는 증거는 아니라고 명시).
- **Conclusion에서 남은 방향으로 제시한 것**: 다단계 결정에 걸친 기하학적·목표 일관성의 지속적 유지가 향후 VLM 연구의 중심 과제라고 본다.

**설계상 명백하게 드러나는 것 (논문이 한계 절로 따로 정리하지는 않음)**

- **완전히 합성 환경이다.** InternScenes로 정규화된 실내 자산을 Blender 4.4로 렌더링한 이미지이며, 원 출처(3RScan, ScanNet, ARKitScenes, Matterport3D)가 실제 스캔이긴 하나 관측 자체는 렌더다. 실제 카메라 노이즈, 모션 블러, 조명 변화가 성능에 어떤 영향을 주는지는 측정되지 않았다.
- **단일 프레임, 단일 시점이다.** 시간 정보도 메모리도 없다. 현재 화면에 보이는 waypoint만 후보이므로, 시야 밖이나 가려진 공간으로 가야 하는 상황은 애초에 다루지 않는다. 논문은 이것을 "내비게이션 시스템에서 waypoint 선택만 분리한다"는 의도적 통제로 제시하지만, 반대로 실제 내비게이션으로의 외삽 범위를 제한한다.
- **Embodiment가 지름 0.6 m 원기둥 하나로 고정돼 있다.** 높이, 비원형 footprint, 관절 구조, 계단 오르기 같은 이동 능력 차이는 다루지 않는다.
- **실내 전용이다.** 옥외, 동적 장애물, 사람이 있는 환경은 없다.
- **학습 자원 평가가 단일 모델·단일 규모다.** Qwen3.5-4B 하나만 파인튜닝했으므로, 개선이 모델 규모나 계열에 얼마나 의존하는지는 알 수 없다. 외부 전이 이득도 3DSRBench에서는 +1.4점으로 작다.
- **Spatial CoT가 GPT-5.5 생성물이다.** 형식 주석과 대조 검사를 거치지만, 추론 텍스트 자체는 다른 모델의 산물이다.
- **오디오가 전혀 없다.** 입력은 RGB 이미지와 텍스트 프롬프트뿐이다.

## 우리 연구와 연결되는 점

**Egocentric Vision 관점**

- **"이미지 위 번호 마커 = 행동 어휘"라는 인터페이스 자체가 재사용 가능한 도구다.** 1인칭 화면 위에 후보 지점을 번호로 겹쳐 놓고 JSON ID 배열을 받는 방식은, VLM에게 연속 좌표를 회귀시키지 않으면서도 공간적 결정을 뽑아내는 우아한 우회로다. 좌표를 텍스트 토큰으로 내보내는 방식의 실패는 다른 연구들도 반복해서 지적한 문제인데, 이 논문은 "**가시 후보를 이산 어휘로 제시**"라는 다른 해법을 쓴다. Hand-object 문제에서도 "손이 다음에 닿을 지점"을 후보 마커 집합으로 제시하고 고르게 하는 식으로 그대로 이식할 수 있다.
- **기하를 먼저 고정하고 언어를 나중에 붙이는 데이터 구축 순서**가 핵심 교훈이다. 타깃·waypoint·가능 간선·목표 영역·참조 경로를 전부 확정한 뒤에야 GPT로 질문과 CoT를 생성하고, 생성물을 다시 형식 주석과 대조 검사한다. LLM으로 데이터를 만들면서도 ground truth의 신뢰성을 지키는 실무 레시피다.
- **Paired 설계로 교란 요인을 제거하는 방법.** Point Path와 Embodied Path가 장면·타깃·시작점·후보 공간을 완전히 공유하므로, 성능 차이를 오직 embodiment 탓으로 돌릴 수 있다. Ego 연구에서 "어떤 요인이 진짜 원인인가"를 논증할 때 쓸 수 있는 강력한 통제 설계다. 벤치마크 선정을 **번들 단위**로 해서 쌍의 한쪽만 남지 않게 한 디테일까지 배울 점이다.
- **실패를 단계별로 분해하는 진단 프레임.** 출력 유효성 → 끝점 선택 → 첫 행동 → 전체 경로 → joint success의 다섯 축으로 나누고, 각 축을 하나씩 통제해가며 "마커 밀도 때문인가? 경로 길이 때문인가? 타깃 가시성 때문인가?"를 전부 배제한 전개는 그 자체로 좋은 논증 템플릿이다. 단순히 "성능이 낮다"가 아니라 "**어떤 부분 능력이 없는가**"를 특정한다.
- **Suffix 실패라는 현상 자체가 흥미로운 연구 대상이다.** 첫 행동이 합법인 경우의 94.7%(Embodied)가 뒤쪽에서 무너진다. 이는 VLM이 "지금 여기서 한 발"은 판단하지만 "그 뒤에 자기가 어디 서 있게 될지"를 시뮬레이션하지 못한다는 뜻이다. Ego 영상에서 미래 상태를 내적으로 굴리는 능력(world model 성격)의 부재를 정량화한 셈이다.

**Hand-Object Interaction 관점**

- 이 논문의 embodiment는 **0.6 m 지름의 몸**이고 제약은 "통과할 수 있는가"다. HOI로 옮기면 **손의 크기·형태·grasp 가능성**이 정확히 같은 역할을 한다. "물체가 보인다"와 "이 손으로 저 자세에서 잡을 수 있다"는 다른 판단이며, VLM이 후자에서 무너지는 양상은 embodied traversability와 구조적으로 닮았을 가능성이 높다. Point/Embodied 쌍 설계를 "물체 인식 / 실제 grasp 가능성" 쌍으로 옮기는 것은 곧바로 실험이 된다.
- **Affordance를 "행동의 기하학적 결과"로 채점한다는 발상**이 이식 가능하다. 논문은 예측된 간선이 불법일 때 실제로 swept corridor에 장애물이 있음을 depth·object-index 렌더로 88.7% 확인했다. HOI에서도 "예측한 접촉점이 실제로 도달 가능한가"를 손 모델의 swept volume과 물체 기하로 검증하는 감사(audit)를 붙일 수 있다.
- **다만 이 논문에 손은 없다.** 에이전트는 바닥을 이동하는 원기둥이고 조작(manipulation)은 다루지 않는다. 타깃에 "도달"하는 것까지가 과제이고 그 다음에 무엇을 하는지는 범위 밖이다. 즉 navigation과 manipulation 사이의 다리는 비어 있으며, "경로 끝 waypoint에서 실제로 물체를 조작할 수 있는가"를 묻는 확장은 명백한 빈틈이다.

**Spatial Audio 관점**

- **이 논문에 오디오는 전혀 없다** — 입력은 렌더된 RGB 한 장과 텍스트 프롬프트뿐이다. 그 부재가 기회다.
- 가장 직접적인 연결점은 **끝점 grounding 실패**다. 목표 일치 끝점 비율이 Embodied 4.8%, Intent 5.2%다. 특히 Intent Path는 "무엇을 원하는지"를 의도에서 추론해야 하는데, 실제 환경이라면 소리가 타깃 후보를 크게 좁힌다 — 물 끓는 소리, TV 소리, 사람 말소리. Spatial audio라면 **방향과 대략적 거리**까지 준다. 단일 RGB 프레임의 시야 제약을 보완하는 가장 자연스러운 modality다.
- **단일 시점·단일 프레임이라는 이 벤치마크의 근본 한계가 곧 오디오의 강점이 있는 지점이다.** 화면 밖이나 가려진 곳의 정보는 시각으로는 원리적으로 접근 불가능하지만 소리는 벽을 돌아 들어온다. EgoPathBench를 "소리가 나는 타깃"으로 확장해 audio-visual waypoint decision을 묻는 것은 기존 인터페이스를 거의 그대로 두고 할 수 있는 확장이다.
- **평가 틀도 그대로 쓸 수 있다.** VPR / SR / SPL과 단계별 진단(끝점 적중, 첫 행동 합법, 전체 경로 합법, joint success)은 modality에 중립적이다. 오디오를 추가했을 때 **어느 단계가 개선되는지**를 분리해서 보일 수 있다 — 끝점 grounding만 좋아지는지, 중간 경로 feasibility까지 좋아지는지. 단일 종합 점수만 보고하는 벤치마크보다 훨씬 설득력 있는 ablation이 가능하다.
- **기하 민감도 검증 방식**도 참고할 만하다. 반지름·grid·goal ring을 흔들어도 모델 순위가 rank $\rho = 1.0$으로 보존됨을 보인 것처럼, audio-visual 벤치마크에서도 음원 위치 허용 오차나 SNR을 흔들어 결론의 강건성을 보이는 절차를 그대로 가져올 수 있다.

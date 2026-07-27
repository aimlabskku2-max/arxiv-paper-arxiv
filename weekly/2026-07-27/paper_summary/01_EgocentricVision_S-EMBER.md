# S-EMBER: A Large-Scale Benchmark for Streaming Egocentric Memory Retrieval

**arXiv**: 2607.02689 | **주제 분류**: Egocentric Vision | **출판일**: 2026-07-02 | **학회**: 프리프린트
**저자/소속**: Xiaodong Wang, Xuanyi Zhao, Pedro Rodriguez, Devendra Singh Sachan, Barlas Oguz, Seungwhan Moon, Shang-Wen Li, Gargi Ghosh, Xin Dong, Wen-Tau Yih 외 (FAIR, Meta / Reality Labs, Meta)
**링크**: https://arxiv.org/abs/2607.02689

## 한 줄 요약
Ray-Ban Meta 스마트 안경으로 촬영한 388시간짜리 1인칭 영상에 기반해, AI가 "스트리밍" 상황에서 과거 경험을 떠올리고(episodic memory) 그 근거가 되는 영상 구간까지 정확히 짚어내야 하는 새로운 벤치마크 S-EMBER를 제안한 논문이다.

## 메인 그림
![S-EMBER 벤치마크 주석 개요](https://arxiv.org/html/2607.02689v1/x1.png)
5~20분 길이의 1인칭 영상에서 특정 시점(스트리밍 상황)에 메모리 질문이 던져지고, 서로 다른 세 명의 작성자가 짧은/중간/긴 답변을 달며, 각 답변에는 근거가 되는 영상 구간 $[t_{start}, t_{end}]$(visual proof)이 표시되는 주석 구조를 보여준다.

## 선행 연구
1인칭(egocentric) 비디오 이해 분야는 Ego4D([arXiv:2110.07058](https://arxiv.org/abs/2110.07058))가 대규모 1인칭 활동 데이터를 제공하며 발전을 이끌었고, EgoSchema([arXiv:2308.09126](https://arxiv.org/abs/2308.09126)), EgoTempo, AMEGO 등이 그 위에서 시간적 인지와 장기 추론(long-range reasoning)을 평가해 왔다. 긴 영상 추론(long-form video reasoning)에서는 Video-MME, MLVU, LongVideoBench 같은 데이터셋이 수 시간짜리 영상까지 다루며 모델의 attention 한계를 밀어붙였다. 또한 StreamingBench, SVBench, MovieChat-1K 같은 스트리밍(streaming) 벤치마크는 "질문 시점까지의 과거와 현재만 볼 수 있다"는 인과적 제약(causal constraint)을 도입했다.

## 문제 제기
기존 벤치마크 대부분은 영상 파일 전체에 접근할 수 있는 오프라인(offline) 평가 방식이라, 웨어러블 기기가 실제로 겪는 "스트리밍" 현실을 반영하지 못한다. 즉, 상시 녹화되는 1인칭 영상에서 "지금 필요한 정보를 과거의 어느 시점에서 찾아야 하는가"를 능동적으로(active recall) 다루지 못한다. 또한 기존 1인칭 데이터셋은 연구용 대형 장비나 액션캠으로 촬영되어 실제 스마트 안경의 시선(자연스러운 gaze, 머리 방향 시야)과 다르고, 답을 맞혔더라도 그 근거가 실제 영상에 있는지(hallucination 여부)를 대규모로 검증할 수단이 없었다.

## 연구 주제
논문은 **Grounded Streaming Episodic Retrieval (GSER)**라는 새로운 과제를 정의한다. 이는 (1) 스트리밍 상황(질문 시점까지의 영상만 보고) 답을 생성하고, 동시에 (2) 답의 근거가 되는 시간 구간 $[t_{start}, t_{end}]$를 정확히 예측(temporal grounding)해야 하는 과제다. 여기서 "grounded"란 모델의 추론이 언어적 상식이나 추측이 아니라 실제 영상 근거에 anchor(고정)되어 있음을 요구한다는 뜻이다.

## 연구 방법
- **데이터**: Ray-Ban Meta 스마트 안경으로 613명의 사용자가 촬영한 3,141개 영상(총 388시간, 평균 7.4분, 5~20분 분포)을 사용한다. 스크립트 없는 일상의 "사이사이 순간"(in-between moments)을 우선 수집해 episodic memory가 자연스럽게 필요한 상황을 담았다.
- **주석 파이프라인(3단계, causal-first)**: (1) 실시간으로 영상을 보다가 "과거를 돌아봐야만" 답할 수 있는 질문 생성(현재 프레임만으로는 답 불가), (2) 세 그룹(surgeon-간결/chef-균형/architect-상세)이 서로 다른 상세도의 tri-tiered 정답 작성 + 근거 구간 표시, (3) 전문가 검수와 Blind-LLM(o3) 감사로 텍스트만으로 풀리는 지름길(shortcut) 질문 제거. 근거 구간은 핵심 증거 앞뒤 여유를 "증거 길이의 15% 또는 15초 중 작은 값"으로 엄격히 제한해 넓게 잡아 우연히 맞히는 것을 방지했다.
- **8개 인지 범주 taxonomy**: Visual Detail Recall, Sequential Action, Time Duration, Counting, Temporal Ordering, Object Comparison, Location Trace, Spatial Reasoning. 오디오는 시각 추론 격리를 위해 생성·답변 단계 모두에서 음소거된다.
- **두 평가 과제와 지표**: (1) Streaming Answer Generation — LLM-as-a-Judge로 tri-tiered 정답과 비교. clean accuracy($Acc_{cl}$, 근거 없는 정보에 페널티)와 overall accuracy($Acc_{ov}$, 부수적 세부는 허용)로 신뢰도의 상·하한을 잰다. 판정 편향을 줄이기 위한 5지선다(MCQ) 변형도 제공. (2) Temporal Grounding Retrieval — mIoU, Recall@1(IoU≥$\tau$), 그리고 정답과 정확한 근거 구간을 모두 요구하는 GQ@$\tau$(NExT-GQA에서 차용).
- **평가 대상**: Blind LLM(GPT-4o, 시각 없음), Socratic 파이프라인(0.2fps 프레임 캡션을 이어 붙여 long-context LLM으로 답), 그리고 native 멀티모달 모델들(Gemini 3.1 Pro, GPT-5.4, GPT-4o, InternVL3.5, Qwen3VL, LLaVA-OneVision) 및 인간 성능.

## 실험 결과 / 연구 의의
핵심 발견은 **localization paradox(위치 특정의 역설)**다. 모델 규모를 키우거나 프레임을 더 넣으면 "무슨 일이 있었는지"를 이해하는 의미 추론(semantic reasoning)은 좋아지지만, "언제 일어났는지"를 짚는 시간적 grounding은 거의 정체된다.

- 규모 스케일링: InternVL3.5를 4B→38B로 키우면 정확도 19.7%→26.1%, Qwen3VL 4B→32B는 21.8%→24.1%로 오르지만 grounding 개선은 미미.
- 프레임 밀도: Qwen3VL 프레임 32→768로 늘리면 정확도 8.8%→24.1%(약 3배)로 로그적 상승하나 grounding은 최대 2.5%에 머묾.
- 해상도: 240p→720p로 올리면 정확도 14.4%→24.2%로 오르지만 grounding은 완전히 평평(flat).
- Memory recency: 증거와 질문 사이 시간 간격이 커질수록 보편적 recall decay 발생. Gemini 3.1 Pro는 즉시 회상(0~30초) 50%에서 10분 이전 사건 22%로 하락하고, GPT-4o는 10분 지점에서 0%로 붕괴.

주요 모델 비교 (Table 3, 값이 클수록 좋음. Halluc.는 낮을수록 좋음):

| 모델 | Clean Acc ($Acc_{cl}$) | Overall Acc ($Acc_{ov}$) | Halluc.(↓) | MCQ Acc | mIoU | R@1≥.5 | GQ@.5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Human Ceiling | 91.43% | 91.43% | 0.00% | – | 0.777 | 0.858 | 0.698 |
| Gemini 3.1 Pro | 42.88% | 47.83% | 40.17% | 54.41% | 0.479 | 0.503 | 0.297 |
| GPT-5.4 | 23.77% | 37.92% | 58.90% | 41.82% | 0.333 | 0.313 | 0.117 |
| InternVL3.5-38B | 25.86% | 26.10% | 25.51% | 36.84% | 0.077 | 0.059 | 0.024 |
| Socratic Baseline | 23.04% | 32.25% | 54.36% | 31.21% | 0.393 | 0.406 | 0.129 |
| GPT-4o | 22.06% | 26.46% | 39.33% | 29.02% | 0.111 | 0.096 | 0.021 |
| Qwen3VL-32B | 19.75% | 24.19% | 47.44% | 31.21% | 0.047 | 0.025 | 0.011 |
| LLaVA-OneVision-7B | 16.62% | 18.55% | 47.35% | 29.56% | 0.104 | 0.078 | 0.005 |
| Blind LLM | 2.68% | 5.18% | 82.47% | 20.17% | – | – | – |

Blind LLM이 clean accuracy 2.68%에 그친 것은 이 벤치마크가 언어적 지름길을 성공적으로 걸러냈음을 보여준다. 최고 모델 Gemini 3.1 Pro조차 인간 천장(91.43%)과 GQ@.5(0.297 vs 0.698)에서 큰 격차를 보인다. 즉 상당수 모델이 "틀린 이유로 맞히는"(correct for the wrong reasons) 방식으로, 전역 장면 맥락과 언어적 사전지식에 의존해 답만 맞히고 근거 구간은 못 짚는다. 의의는 스마트 안경이라는 실제 하드웨어 기반으로, 차세대 웨어러블 AI를 위한 grounded·신뢰 가능한 episodic memory 연구의 진단적 토대를 제공한 데 있다.

## 한계
- **단일 모달리티**: 모달리티 격리를 위해 오디오를 영구 삭제(redact)했기 때문에, 실제 AI 비서에 중요한 음향 단서(acoustic cue)를 활용하는 능력이나 멀티모달 통합은 평가하지 못한다.
- **LLM-as-a-Judge 근사**: 인간 전문가와 높은 상관을 보이지만 여전히 근사치이며, verbosity bias(장황함 편향)나 미세한 뉘앙스를 놓칠 수 있어 평가 아티팩트 가능성이 남는다.
- 논문은 벤치마크·진단 연구이므로, 위 grounding 병목을 실제로 해결하는 새 아키텍처 제안까지는 나아가지 않는다(future work로 adaptive temporal indexing, hierarchical memory buffer, verification-aware 모델 등을 제시).

## 우리 연구와 연결되는 점
(Egocentric Vision / Hand-Object Interaction / Spatial Audio 관심 독자 관점)
- **Egocentric Vision**: 연구용 리그가 아닌 소비자용 스마트 안경(Ray-Ban Meta)의 자연스러운 머리 중심 시야로 촬영된 대규모 데이터라, 실제 착용 환경에서의 gaze·시야 정합성을 다루는 연구에 직접 활용 가능한 자원이다. Location Trace, Spatial Reasoning, Object Comparison 등 8개 범주는 hand-object interaction 이후의 "물건을 어디에 뒀는지" 같은 장기 추적 과제와 자연스럽게 맞닿는다.
- **Temporal Grounding**: "답은 맞혀도 언제인지 못 짚는" localization paradox는, 손-물체 상호작용의 정확한 시점 구간을 특정해야 하는 우리 관심 과제와 동일한 병목이다. adaptive temporal indexing과 생성 토큰-시간 인덱스를 잇는 cross-modal attention 방향은 참고할 만하다.
- **Spatial Audio**: 이 벤치마크는 오디오를 의도적으로 제거한 시각 전용 설정이다. 저자들도 한계로 명시했듯, 여기에 spatial audio를 결합해 소리 근거(acoustic evidence) 기반의 episodic recall을 평가·강화하는 것은 우리 연구가 채울 수 있는 명확한 빈틈이다. 즉 S-EMBER의 GSER 프레임(스트리밍 + 근거 구간 예측)을 오디오-비주얼로 확장하는 후속 연구의 출발점으로 삼을 수 있다.

# FoleyDesigner: Immersive Stereo Foley Generation with Precise Spatio-Temporal Alignment for Film Clips

**arXiv**: 2604.05731 | **주제 분류**: Spatial Audio | **출판일**: 2026-04-07 | **학회**: 프리프린트 (arXiv cs.CV, Comments 필드에 발표처 명시 없음)
**저자/소속**: Mengtian Li, Kunyan Dai, Yi Ding, Ruobing Ni, Ying Zhang (Shanghai Film Academy, Shanghai University / Shanghai Engineering Research Center of Motion Picture Special Effects), Wenwu Wang (University of Surrey, UK), Zhifeng Xie (Shanghai University) — Wang, Xie가 교신저자
**링크**: https://arxiv.org/abs/2604.05731

## 한 줄 요약
무성 영화 클립을 입력받아, 인간 폴리 아티스트의 작업 순서(장면 분해 → 음향 제작 → 믹싱)를 그대로 모듈로 옮긴 뒤 영상에서 뽑은 깊이·방위각 궤적으로 diffusion을 조건화해, 화면 속 움직임과 프레임 단위로 맞물리는 스테레오 Foley를 만들고 5.1 서라운드까지 내보내는 프레임워크.

## 메인 그림
![인간 폴리 디자이너의 작업 단계(좌)와 이를 그대로 모듈화한 FoleyDesigner의 대응 단계(우)](https://arxiv.org/html/2604.05731v1/image/teaser7.png)
Figure 1. 왼쪽은 실제 폴리 아티스트의 작업 흐름, 오른쪽은 각 단계에 대응하는 FoleyDesigner 모듈과 단계별 출력물로, 최종적으로 영화에 바로 쓸 수 있는 사운드트랙이 나온다.

## 선행 연구
Foley(영상에 맞춰 후시 녹음하는 효과음) 생성 연구는 크게 세 갈래로 발전해 왔다.

- **모노 오디오 생성**: AudioLDM2, Tango 2, [Make-an-Audio 2](https://arxiv.org/abs/2305.18474) 같은 latent diffusion 기반 text-to-audio 모델과 Frieren, [MMAudio](https://arxiv.org/abs/2412.15322) 같은 video-to-audio(V2A) 모델, 그리고 FoleyCrafter, Diff-Foley, [Video-Foley](https://arxiv.org/abs/2408.11915), MultiFoley 등 Foley 특화 모델들. 품질은 좋지만 출력이 단일 채널이라 공간 차원이 아예 없다.
- **스테레오/공간 오디오 생성**: Stable Audio는 파형 위에서 diffusion을 수행해 스테레오를 내지만 음원 위치를 명시적으로 제어하지 못한다. SpatialSonic, [See-2-Sound](https://arxiv.org/abs/2406.06612), OmniAudio는 텍스트·이미지·360도 영상으로 공간감을 조건화한다.
- **모노→스테레오 변환**: Sep-Stereo, Mono-to-Binaural 계열은 이미 존재하는 모노 음원을 공간화한다.

## 문제 제기
세 갈래 모두 영화 현장의 요구를 충족하지 못한다.

1. **모노 방식은 공간 정보가 없다.** 스테레오 폴리는 소리를 좌우 채널에 배치해 방향감을 만들고 관객의 시선과 감정을 유도하는 서사적 장치인데, 모노 출력으로는 이 기능 자체가 성립하지 않는다.
2. **스테레오 생성 방식은 프레임 단위 동기화가 안 된다.** 텍스트 조건은 "왼쪽에서" 정도의 거친 방향만 지정할 수 있어 연속적인 이동 궤적을 표현하지 못하고, 이미지 조건은 시간 정보가 아예 없다.
3. **모노→스테레오 변환은 원본 음원이 먼저 있어야 한다.** 제작 단계가 하나 더 늘고 창작 자유도가 떨어진다.

논문은 영화급 Foley를 만들려면 다음 세 가지를 동시에 풀어야 한다고 정리한다. (1) **밀집 중첩 사운드 이벤트** — 한 장면에 여러 소리가 시간·주파수 축에서 겹치는데, 단일 패스 생성 모델은 이를 분리하지 못해 뭉개진 결과를 낸다. (2) **정밀한 spatio-temporal grounding** — 현재 조건화 방식은 시각적 공간 단서에 근거를 두지 않는다. (3) **전문가 수준의 음향 품질** — 트랙 간 잔향 불일치, 주파수 마스킹, 라우드니스 불균형 때문에 중요한 소리가 믹스에 묻힌다.

## 연구 주제
무성 영화 클립으로부터 **시공간적으로 정렬된 스테레오 Foley를 생성하고, 실제 영화 후반작업 파이프라인에 그대로 투입 가능한 형태(5.1 서라운드)로 내보내는 것**. 아울러 이런 학습을 가능하게 하는 데이터셋 부재 문제를 함께 다룬다.

## 연구 방법

### 전체 구조 (3단계)
전문 폴리 팀의 협업 방식을 그대로 세 단계로 옮겼다.

**1단계. Fine-Grained Film Decomposition (장면을 소리 이벤트로 분해)**
- *FilmScribe*: 무성 영상 $\mathcal{V}$를 구조화된 텍스트 $\mathcal{T}$로 변환. generator 에이전트가 초안을 만들고 validator 에이전트가 검증해 $\text{Validator}(\mathcal{T},\mathcal{V})\rightarrow\text{True}$가 될 때까지 반복하는 폐루프 구조.
- *FoleyScriptWriter*: 영화 대본 $\mathcal{F}$까지 합쳐 계층적 Foley 스크립트 $\mathcal{S}=\{(e_i, l_i)\}$를 만든다. 각 사운드 이벤트 $e_i$에 전경(fg)/배경(bg) 레이어를 붙이는 것이 핵심으로, 겹친 이벤트를 개별로 쪼개 순차 생성함으로써 뭉개짐 문제를 회피한다. 대본을 쓰는 이유는 화면에 안 보이는 서사적 요소를 추론하기 위함.
- 후보 스크립트 탐색에는 Tree-of-Thought를 쓴다. Expand(후보 생성) → Score($\text{Score}=w_1 s_{\text{align}}+w_2 s_{\text{layer}}+w_3 s_{\text{emotion}}$, 즉 시청각 대응·레이어 분리·영화 정서 일치) → Prune(상위 $b$개 유지)를 반복하고, 점수가 임계값 $\tau$를 넘거나 깊이 한계에 닿으면 종료한다.

**2단계. Spatio-Temporal Foley Generation (공간·시간 조건부 생성)**
- *단서 추출*: 키프레임에서 VLM(Qwen2.5-VL)으로 음원 바운딩 박스를 찾고, Depth Anything v2로 깊이 $d_i$를 구한다. 방위각은 박스 중심의 가로 위치 $x_i$로부터 $\theta_i=\arctan\!\left(\frac{x_i-W/2}{d_i}\right)\cdot\frac{180^\circ}{\pi}+90^\circ$로 계산한다. 시간축으로는 이벤트 발생 여부를 나타내는 이진 벡터 $\mathbf{c}\in\{0,1\}^T$를 만들고, 키프레임 위치를 프레임 레이트에 맞춰 보간한 뒤 $\mathbf{p}_t=c_t\cdot\mathbf{x}_t$로 마스킹한다. 즉 **입력은 (깊이, 방위각) 궤적 + 이벤트 온/오프 타임라인 + 텍스트 프롬프트**.
- *생성*: 백본은 Stable Audio Open(DiT 기반 latent diffusion). 위치 벡터에 Fourier feature $\gamma(\mathbf{p}_t)$를 씌우고 이진 마스크로 변조하되 $\epsilon=0.1$을 남겨 비활성 구간에서도 약한 위치 정보를 유지한다. 1D conv + GroupNorm + SiLU 인코더로 오디오 latent의 시간 압축률에 맞춘 뒤, DiT 4블록마다(레이어 3, 7, 11, 15, 19, 23) **injection block**을 끼워 latent와 위치 임베딩 사이에 cross-attention을 건다. 이것이 논문이 말하는 position-aware injection mechanism이다.

**3단계. Foley Refinement and Professional Mixing (다중 에이전트 믹싱)**
- *분석 에이전트*: 각 트랙에서 $\mathbf{f}_i=[\mathbf{f}_{sem}, \mathbf{f}_{spec}, f_{rev}, f_{loud}]$ (Audio-LLM 의미 임베딩, Mel-spectrogram을 VLM으로 읽은 스펙트럼 패턴, 잔향 시간, 통합 라우드니스)를 뽑는다.
- *Mixing Planner*: 트랙별로 필요한 처리 $\mathcal{O}_i \subseteq \{\texttt{reverb}, \texttt{eq}, \texttt{dyn}\}$를 담은 믹싱 플랜을 짠다.
- *전문가 에이전트 3종*: 잔향 담당(장면 공간에 맞는 reverb 파라미터), EQ 담당(주파수 마스킹 최소화), 다이내믹스 담당(게인 조정으로 전경 소리가 묻히지 않게). 각 전문가는 해당 처리가 필요한 트랙을 한꺼번에 받아 믹스 전체의 일관성을 유지한다.
- *5.1 업믹싱*: ITU-R BS.775 규격에 맞춰 L/R을 FL/FR에 직접 매핑하고 C·SL·SR은 가중 믹스로, LFE는 $\mathbf{s}_{\text{LFE}}(t)=\text{LPF}(\mathbf{s}_{\text{mix}}(t),\ 120\,\text{Hz})$로 만든다.

### FilmStereo 데이터셋
공간 메타데이터와 정밀 타임스탬프를 **동시에** 갖춘 첫 스테레오 Foley 데이터셋.

- 8개 대분류 / 23개 소분류, 14,784 샘플, 166시간 (본문 기준. 부록의 통계 절에는 42.3시간으로 적혀 있어 수치가 서로 어긋난다).
- 전처리: 다중 이벤트 샘플 제거 → -40 dB 스펙트럼 노이즈 제거 → 8~10초로 루프 패딩 → CLAP 유사도 $\tau=0.35$ 미만 폐기.
- 공간 시뮬레이션: 방위각을 인간의 좌우 분해능에 맞춰 5구간($0^\circ$, $\pm15^\circ$, $\pm45^\circ$), 깊이를 근거리(0–2 m)·중거리(2–5 m)·원거리(5 m 초과) 3구간으로 이산화. gpuRIR로 양귀 간격 16–18 cm를 가정해 RIR을 생성하며, **HRTF와 head shadow는 고려하지 않았다**. 동적 음원은 궤적을 선형 보간으로 만든다. 잔향은 hall/room/chamber/plate 프리셋 적용.
- 어노테이션: GPT-4에 chain-of-thought 프롬프팅으로 방위각·깊이·잔향을 녹인 공간 캡션을 생성하고, 진폭 피크 검출로 이벤트 시작/끝 타임스탬프를 밀리초 단위로 붙인다.
- 구성 비율: 동적 음원 64% / 정적 36%, 큰 물체 40% / 중·소·초대형 각 20%.

학습은 (1) 스테레오 mel-spectrogram VAE, (2) 시공간 조건 주입을 포함한 DiT diffusion의 2단계로 진행하며, learning rate $3\times10^{-5}$, batch size 8, NVIDIA A6000 사용.

## 실험 결과 / 연구 의의

**오디오 품질** (스테레오를 모노로 평균 낸 뒤 측정)

| 방법 | IS ↑ | KL ↓ | FAD ↓ | CLAP ↑ |
|---|---|---|---|---|
| Stable Audio | 10.50 | 1.86 | 2.37 | 0.594 |
| SpatialSonic | 13.79 | 1.37 | 1.93 | 0.672 |
| FoleyDesigner (Ours) | 12.36 | 1.40 | 1.88 | 0.679 |

CLAP 0.679, FAD 1.88로 최고. IS는 SpatialSonic보다 낮은데, 논문은 IS가 품질이 아니라 샘플 다양성을 재는 지표라고 해명한다.

**시공간 정렬** (GCC/CRW는 공간 정확도, FSAD는 스테레오 품질, IoU는 시간 정밀도)

| 방법 | GCC ↓ | CRW ↓ | FSAD ↓ | IoU ↑ |
|---|---|---|---|---|
| Stable Audio | 61.17 | 51.44 | 0.343 | 24.5 |
| See2Sound | 60.03 | 51.17 | 0.291 | 21.3 |
| SpatialSonic | 49.20 | 36.87 | 0.163 | 27.8 |
| FoleyDesigner (Ours) | 48.79 | 34.23 | 0.138 | 32.2 |

전 지표 1위. 특히 IoU는 SpatialSonic 대비 15.8% 개선.

**영화 Foley 성능** (IB: ImageBind 점수, SRS: Sonic Richness Score, CCS: Cinematic Clarity Score — 뒤 둘은 이 논문이 새로 제안하고 audio-capable MLLM으로 평가)

| 방법 | IB ↑ | SRS ↑ | CCS ↑ | AV-Sync ↑ |
|---|---|---|---|---|
| Stable Audio | 0.216 | 5.31 | 5.8 | 0.512 |
| See2Sound | 0.105 | 3.03 | 3.0 | 0.601 |
| SpatialSonic | 0.251 | 5.91 | 4.5 | 0.545 |
| FoleyDesigner (Ours) | 0.402 | 8.27 | 6.2 | 0.726 |

ImageBind는 SpatialSonic 대비 60.2%, AV-Sync는 33.2%, SRS는 39.9%, CCS는 37.8% 향상. 논문은 SRS 향상을 1단계 장면 분해 덕분, CCS 향상을 3단계 다중 에이전트 믹싱 덕분으로 귀속시킨다.

**Ablation — 시공간 단서(STC) 제거**

| 구성 | GCC ↓ | CRW ↓ | FSAD ↓ | FAD ↓ |
|---|---|---|---|---|
| w/o STC | 62.02 | 55.89 | 0.297 | 2.14 |
| Full Model | 48.79 | 34.23 | 0.138 | 1.88 |

STC를 넣으면 GCC 21.3%, CRW 38.8%, FAD 12.1% 개선. 즉 공간 조건화가 공간 정확도뿐 아니라 지각 품질 자체도 끌어올린다.

**Ablation — 다중 에이전트 믹싱** (ER: Event Recall, LSD: 로그 스펙트럼 거리, LE: 라우드니스 오차, RT60E: 잔향시간 오차)

| 구성 | ER ↑ | LSD ↓ | LE ↓ | RT60E ↓ |
|---|---|---|---|---|
| Single-Stage | 68.5% | 34.20 | 7.63 | 0.92 |
| Ours | 84.2% | 18.42 | 2.86 | 1.08 |

이벤트 회수율이 68.5%→84.2%로 오르고 스펙트럼 명료도·라우드니스 균형이 크게 개선된다. 다만 **RT60 오차는 오히려 나빠졌고(0.92→1.08)**, 논문은 2D 시각 단서만으로 개방 공간의 잔향을 추정하는 것이 본질적으로 어렵기 때문이라고 인정한다.

**추가 베이스라인**: Diff-Foley(FAD 1.85), FoleyCrafter(FAD 1.69, ImgBind 0.430)는 모노 품질이 강하지만 공간 제어가 없어 GCC/CRW 측정 자체가 불가능하다. 모노 모델 Tango를 FilmStereo로 파인튜닝해도 FAD 2.26, GCC 54.82로 열세여서, 모노 구조를 그대로 미세조정하는 것만으로는 공간 Foley가 안 된다는 점을 보였다.

**인간 평가**: 오프라인은 ITU-R BS.775-3 규격 5.1 스튜디오에서 12명, 온라인 스테레오는 53명. 몰입감·정서 일치·시간 정렬·공간 정렬·음색 일관성 5개 축에서 평가했고, 정서 일치 61%, 몰입감 58%(온라인 선호율)로 최고를 기록했다.

**연산 비용** (A6000 1장, 3초 스테레오 클립 기준): 시각 분석 2s + 스크립트 분해 34s + 오디오 생성 8s + 정제 64s = **총 108s**. 엔드투엔드 모델의 약 5s와 비교하면 훨씬 느리며, 논문은 실시간성보다 정밀도·다중 트랙 분해·사람이 개입 가능한 제어를 우선한 설계라고 방어한다.

**의의**: 학술적 V2A 연구와 실제 영화 후반작업 사이의 간극을 정면으로 다뤘다는 점이 핵심이다. 결과물이 단일 오디오 파일이 아니라 레이어별 트랙 + 믹싱 파라미터 + 5.1 규격 출력이라, 사운드 디자이너가 이어받아 수정할 수 있는 형태로 나온다.

## 한계
논문이 직접 밝힌 한계:

- **밀집 중첩 장면에서 성능 저하.** 발소리·물체 상호작용·앰비언스가 동시에 발생하면 공간 정위 오류가 생긴다. 향후 과제로 더 강건한 다중 객체 추적과 계층적 추론을 제시한다.
- **잔향 추정의 부정확성.** 다중 에이전트 정제가 RT60 오차를 오히려 키웠으며, 2D 시각 단서에서 개방 공간의 잔향을 추정하는 한계를 인정한다.
- **느린 추론.** 3초 클립에 108초로, 실시간 응용에는 부적합하다.

논문이 명시적으로 한계라 부르지는 않았으나 방법 설명에서 확인되는 제약:

- FilmStereo의 공간 오디오는 **실제 녹음이 아니라 gpuRIR 시뮬레이션**이며, HRTF와 head shadow를 모델링하지 않았다. 따라서 좌우 채널 레벨/시간차 위주의 공간감이고, 정밀한 바이노럴 지각과는 차이가 있을 수 있다.
- 방위각이 **전방 반구($0^\circ$~$180^\circ$)로 제한**된다. 화면 밖이나 후방 음원은 이 정식화로 표현되지 않으며, 5.1의 서라운드 채널은 생성이 아니라 스테레오의 가중 믹스로 파생된다.
- 데이터셋 규모 수치가 본문(166시간)과 부록(42.3시간)에서 어긋난다.

## 우리 연구와 연결되는 점

**Spatial Audio (직접적)**
- 영상에서 (깊이, 방위각) 궤적을 뽑아 diffusion에 cross-attention으로 주입하는 방식은, 시각 기하를 공간 오디오 조건으로 삼는 가장 직접적인 레시피다. Depth Anything v2 + VLM 바운딩 박스라는 조합은 별도 학습 없이 바로 재현 가능하다.
- 이진 활성 벡터로 위치 벡터를 마스킹하되 $\epsilon=0.1$을 남겨 무음 구간의 위치 정보를 유지하는 트릭은, 공간 조건과 시간 조건을 하나의 텐서로 합칠 때 참고할 만한 설계다.
- FilmStereo는 시간 + 공간 어노테이션을 동시에 갖춘 드문 자원이라, 공간 오디오 생성/평가 벤치마크로 활용 여지가 있다. 다만 시뮬레이션 기반이고 HRTF가 없다는 점은 감안해야 한다.
- GCC-MAE, CRW-MAE, FSAD, IoU라는 평가 지표 세트는 공간 정확도와 시간 정확도를 분리해 재는 방식으로, 유사 과제의 평가 설계에 그대로 쓸 수 있다.

**Egocentric Vision / Hand-Object Interaction (잠재적 연결 — 논문에 명시적 언급 없음)**
- 이 논문은 3인칭 영화 클립을 전제로 하며 에고센트릭 영상이나 손-물체 상호작용을 다루지 않는다. 다만 관점을 옮기면 연결 고리가 보인다. 에고센트릭 영상에서는 카메라 착용자의 머리가 곧 청취자 위치이므로, 이 논문의 "화면 좌표 → 방위각" 변환이 오히려 더 자연스럽게 성립한다.
- Hand-object interaction은 접촉 순간이 명확한 시각 이벤트라, 논문의 이진 활성 벡터 $\mathbf{c}$를 손-물체 접촉 검출로 대체하면 프레임 단위 동기화 신호를 훨씬 정확히 얻을 수 있다. 반대로 이 논문이 약점으로 꼽은 "밀집 중첩 이벤트"는 손이 여러 물체를 빠르게 다루는 에고센트릭 상황에서 더 심각해질 가능성이 크다.
- 전방 반구로 제한된 방위각 정식화는 에고센트릭 환경(착용자 뒤쪽 소리가 흔함)에 그대로 적용하기 어렵고, 확장이 필요한 지점이다.

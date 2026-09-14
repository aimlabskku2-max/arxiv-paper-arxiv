# One-Stage Multi-Task Instruction-Guided 3D Spatial Audio Editing

**arXiv**: 2609.04975 | **주제 분류**: Spatial Audio | **출판일**: 2026-09-04 | **학회**: 프리프린트
**저자/소속**: Ke Lei, Chenyuhao Wen, Yu Zhang, Wenxiang Guo, Changhao Pan, Sashuai Zhou, Yongshi Li, Ruiqi Li, Ruofan Hu, Haorui Xu, Xiang Yin, Zhou Zhao (Zhejiang University, ByteDance)
**링크**: https://arxiv.org/abs/2609.04975

## 한 줄 요약

"앞쪽에 있던 군중을 오른쪽으로 옮기고 왼쪽에 기타 스트럼을 하나 넣어줘" 같은 복합 자연어 지시를 받아, 기존 FOA 3차원 음장을 중간 단계 없이 **한 번의 생성으로** 편집하는 최초의 멀티태스크 프레임워크 SwanWeave를 제안한다.

---

## 메인 그림

![자연어 지시를 받아 FOA 음장에서 지정된 이벤트만 이동·추가하고 나머지는 그대로 보존하는 SwanWeave의 편집 개념도](https://arxiv.org/html/2609.04975v2/teaser-5.png)

Figure 1. 왼쪽은 편집 전 FOA 장면(군중 소리가 정면, 기타 없음), 오른쪽은 "군중을 정면에서 오른쪽으로 옮기고 왼쪽에 스트럼을 추가하라"는 지시를 적용한 결과다. 핵심은 **지시가 가리키지 않은 이벤트들의 내용·궤적·잔향은 건드리지 않은 채** 요청한 변화만 음장에 반영한다는 점이다.

(참고로 모델 구조도는 Figure 2 `https://arxiv.org/html/2609.04975v2/model-3.png` 에 있다. 왼쪽 패널이 전체 학습·추론 파이프라인, 오른쪽 패널이 SE-MoE 모듈이다.)

---

## 선행 연구

이 논문은 크게 두 갈래의 흐름 위에 서 있다.

### 1) 언어 지시 기반 오디오 편집 (Audio Editing)

오디오 편집은 "기존 녹음에서 지시가 가리킨 부분만 바꾸고 나머지는 보존한다"는 문제다. 최근 text-to-audio 생성 모델([AudioLDM](https://arxiv.org/abs/2301.12503), [Stable Audio Open](https://arxiv.org/abs/2407.14358) 등)이 강력한 생성 prior를 제공하면서, 그 위에 편집 기능을 얹는 방식이 주류가 되었다.

| 방법 | 접근 | 편집 공간 |
|---|---|---|
| [AUDIT](https://arxiv.org/abs/2304.00830) | (입력 오디오, 지시, 편집된 오디오) 삼중항을 만들어 latent diffusion을 지도학습 | mono / semantic (add, drop, replace, inpainting, super-resolution) |
| [ZETA / ZEUS](https://arxiv.org/abs/2402.10009) | DDPM inversion을 이용한 zero-shot 편집. 텍스트 프롬프트 또는 비지도로 찾은 semantic 방향 사용 | mono / semantic |
| [AudioEditor](https://arxiv.org/abs/2409.12466) | Null-text inversion, EOT-suppression 등 이미지 편집 기법을 오디오에 이식한 학습 불필요(training-free) 편집 | mono / semantic |
| [SmartDJ](https://arxiv.org/abs/2509.21625) | Audio-Language Model이 상위 요청을 **atomic operation 시퀀스로 분해**하고, diffusion 편집기가 순차 실행 | stereo (2채널) |

이 중 SmartDJ가 본 논문과 가장 가깝다. 스테레오 장면까지 편집 공간을 넓혔고, "소리를 공간적으로 재배치"하는 조작도 다룬다.

### 2) 공간 오디오 생성 / Spatialization

또 다른 흐름은 공간 오디오를 **만들어내는** 쪽이다. 시각·기하 맥락에서 소리를 공간화하는 초기 연구(visual sound localization, SoundSpaces 류의 audio-visual navigation 환경), mono 오디오를 binaural로 변환하는 spatialization 연구(Neural Sound Field, BinauralGrad 등), 그리고 최근의 멀티모달 조건·스트리밍 공간 오디오 생성(OmniAudio, ViSAGe, ISDrama 등)이 여기 속한다.

표현 수준에서 공간과 언어를 잇는 연구로 [SALM](https://arxiv.org/abs/2507.16724)이 있다. SALM은 오디오 인코더를 semantic branch와 spatial branch로 분리해 구조화된 임베딩을 학습하고, 임베딩 공간에서 방향을 조작할 수 있게 한다. 다만 이는 **표현 공간(representation space) 조작**이지, 기존 FOA 파형을 직접 편집하는 waveform-level 편집기는 아니다.

---

## 문제 제기

저자들은 기존 연구의 공백을 두 가지로 정리한다.

### 문제 1. One-stage generation이 안 된다

기존 언어 지시 편집기들은 mono 또는 일반 오디오를 대상으로 하며, **3차원 공간 변수를 편집 가능한 control로 취급하지 않는다**. 가장 가까운 SmartDJ조차 (a) stereo 2채널에서 동작하고, (b) 상위 지시를 atomic operation으로 쪼개 **순차 실행**한다.

순차 실행 파이프라인의 근본 문제는 두 가지다.

- **복합 지시의 결합된 음향적 결과를 직접 학습하지 못한다.** "소리를 교체하면서 동시에 더 멀리 보내라"는 지시에서, 교체와 거리 이동은 파형 상에서 서로 분리되지 않는다. 에너지, 방향성, 잔향, 다른 음원과의 masking이 한꺼번에 바뀐다.
- **오류가 단계마다 누적된다.** 중간 출력을 다시 편집 입력으로 넣으므로 복원 오차와 공간 오차가 쌓인다.

### 문제 2. 태스크 커버리지가 좁다

Spatialization·공간 오디오 생성 연구들은 방향성·정위·비디오 조건 공간음 생성을 다루지만, **이미 존재하는 FOA 장면을 파형 수준에서 편집하는 문제**는 풀지 않는다. 저자들이 아는 한, 오디오 이벤트 편집 + 3D 재배치 + 동적 궤적 + 환경 변화를 모두 포괄하는 FOA 편집 연구는 선행 사례가 없다.

### 왜 중요한가

VR/AR, 텔레프레즌스, 게임, 영화 제작에서 공간 오디오는 이미 널리 쓰인다. 공간 오디오는 소리를 단순한 신호가 아니라 **장면(scene)** 으로 만든다. 음원이 위치를 점유하고, 시간에 따라 움직이며, 주변 공간과 상호작용한다. 실제 프로덕션에서 대부분의 장면은 "거의 원하는 결과에 가깝지만 한 군데만 고치면 되는" 상태다. 그렇다면 음장 전체를 처음부터 다시 만드는 것이 아니라, **기존 장면 위에서 요청된 변경만 적용**하는 편집이 자연스러운 인터페이스다.

---

## 연구 주제

논문이 새로 정의하는 문제는 **Instruction-Guided 3D FOA Spatial Audio Editing**이다.

First-Order Ambisonics(1차 앰비소닉스, 3차원 음장을 W/Y/Z/X 4채널로 표현하는 방식) 파형 $a_{\text{src}} \in \mathbb{R}^{4 \times T}$ 와 자연어 지시 $c$ 가 주어졌을 때, 편집된 FOA 파형을 직접 예측하는 함수를 학습한다.

$$\hat{a}_{\text{tgt}} = F_\theta(a_{\text{src}}, c)$$

기존 흐름과의 차별점은 세 가지다.

1. **stereo → FOA.** 2채널이 아니라 4채널 3차원 음장을 직접 모델링한다. 고도(elevation)와 위/아래 방향까지 편집 대상이 된다.
2. **sequential → one-stage.** 복합 지시를 단계로 쪼개지 않고, 소스에서 최종 타깃으로 가는 직접 변환으로 학습한다. 학습 데이터의 타깃은 **모든 요청 변경이 이미 적용된 최종 장면**이며, 중간 단계는 아예 관측시키지 않는다.
3. **편집 축을 4개로 명시적으로 정의한다.**

| 편집 축 | 포함 조작 |
|---|---|
| Audio events (오디오 이벤트) | add, remove, replace, extract, enhance(볼륨 증가), attenuate(볼륨 감소) |
| Spatial information (공간 정보) | azimuth(방위각), elevation(고도), distance(거리), source layout(음원 배치) |
| Dynamic changes (동적 변화) | 시변 게인 변화(volume fade), 각도 이동(angle motion), 거리 이동(distance motion) |
| Environmental information (환경 정보) | 체감 방 크기, 잔향(reverberation) 변경 — 단, 별도 지시가 없으면 장면 내용과 음원 배치는 유지 |

이 네 축은 파형 안에서 서로 **결합(coupled)** 되어 있다는 것이 논문의 핵심 주장이다. 음원을 멀리 보내면 에너지, 방향성, 잔향, 다른 음원과의 masking이 동시에 변한다. 따라서 복합 지시는 연산의 연쇄가 아니라 하나의 source-to-target 변환으로 학습해야 한다.

---

## 연구 방법

### 전체 구조

**Input**: 소스 FOA 파형 $a_{\text{src}} \in \mathbb{R}^{4 \times T}$ + 자연어 편집 지시 $c$
**Output**: 편집된 FOA 파형 $\hat{a}_{\text{tgt}} \in \mathbb{R}^{4 \times T}$

구성 요소는 (1) FOA 인코더, (2) 지시 인코더, (3) SE-MoE를 장착한 flow-matching latent 편집기다.

### 1) Latent 공간에서 편집하기

FOA 파형을 직접 생성하면 모델이 4채널 장신호 복원이라는 저수준 작업에 자원을 다 쓴다. 그래서 [Stable Audio Open](https://arxiv.org/abs/2407.14358)의 stereo FOA VAE로 연속 latent 공간에 매핑한 뒤 거기서 편집한다.

$$z_{\text{src}} = \mathcal{E}(a_{\text{src}}), \quad z_{\text{tgt}} = \mathcal{E}(a_{\text{tgt}})$$

여기서 $z_{\text{src}}, z_{\text{tgt}} \in \mathbb{R}^{L \times d}$ 이고 latent 차원 $d = 128$ 이다. 지시 $c$ 는 사전학습된 언어 인코더로 인코딩해 cross-attention으로 주입한다.

### 2) Diffusion Transformer + Conditional Flow Matching

백본은 [DiT(Diffusion Transformer)](https://arxiv.org/abs/2212.09748)다. 공간 편집은 이벤트 간, 시간 구간 간, FOA 채널 간의 조율이 필요하기 때문이다. $z_{\text{src}}$ 와 노이즈가 섞인 타깃 latent는 시간 길이가 같으므로, **feature 차원으로 concat**한 뒤 Transformer 입력 projection에 넣는다. 이러면 self-attention이 소스 장면과 생성 중인 latent 사이의 **프레임 단위 대응**을 학습할 수 있고, cross-attention은 지시 조건을 공급한다.

학습은 [conditional flow matching](https://arxiv.org/abs/2210.02747)이다. $z_1 = z_{\text{tgt}}$, $z_0 \sim \mathcal{N}(0, I)$, $t \sim \mathcal{U}(0,1)$ 에 대해

$$z_t = (1-t)z_0 + t z_1, \quad v = z_1 - z_0$$

$$\mathcal{L}_{\text{FM}} = \mathbb{E}_{z_0, t}\left[\|v - v_\theta(z_t, t, z_{\text{src}}, c)\|_2^2\right]$$

소스 latent가 벡터장에 **명시적 보존 조건**을 주고, 지시가 의도된 편집을 지정하는 구조다.

### 3) SE-MoE: 이중 라우팅 Spatial Edit Mixture-of-Experts

하나의 공유 FFN이 "이벤트 삽입 / 음원 재배치 / 궤적 변경 / 실내 음향 변경"을 전부 감당하기는 어렵다. 복합 지시에서 여러 편집 타입이 상호작용하면 특히 취약하다. 그래서 [Sparse MoE](https://arxiv.org/abs/1701.06538) 방식의 모듈로 모든 Transformer 층의 FFN 블록을 대체한다.

전문가(expert)는 세 종류다.

| 전문가 종류 | 선택 단위 | 역할 |
|---|---|---|
| Task expert | 지시 표현으로부터 선택, 샘플 내 모든 프레임에 고정 | 편집 계열(family)·복합 지시별 태스크 인지 전문가 조합 |
| Routed expert | latent 토큰마다 독립 선택 | 편집된 구간·음원에 대한 국소 적응 |
| Null expert | 프레임 라우터가 선택 가능 | 0 텐서 반환 — **변하지 않아야 할 구간이 불필요한 변환을 피하도록** |

Null expert가 이 설계의 영리한 부분이다. 편집의 본질은 "일부만 바꾸고 나머지는 보존"인데, 보존해야 할 구간이 명시적으로 "아무것도 하지 않음"을 고를 수 있게 만든 것이다.

프레임 레벨 라우터는 flow-matching 타임스텝 임베딩 $e_t$ 를 함께 받는다.

$$p_i = \text{softmax}(W_g(x_i + W_t e_t))$$

고정 top-$k$ 대신 **top-$p$ 라우팅**을 쓴다. 누적 확률이 임계값 $\rho$ 를 넘는 최소 전문가 집합 $\mathcal{S}_i$ 를 고른다. 덕분에 단순하거나 변경 없는 프레임은 더 적은 전문가를, 복잡한 편집 구간은 더 많은 전문가를 활성화한다.

태스크 레벨은 학습된 task query로 지시 상태를 pooling해 전문가 확률 $q(c)$ 를 얻고, 같은 top-$p$ 로 태스크 전문가 집합 $\mathcal{T}(c)$ 를 고른 뒤 정규화 가중치 $\beta_e$ 를 쓴다. 최종 출력은 둘의 합이다.

$$\text{SE-MoE}(x_i) = \sum_{e \in \mathcal{S}_i \cap \mathcal{E}_r} \alpha_{i,e} f^r_e(x_i) + \sum_{e \in \mathcal{T}(c)} \beta_e f^t_e(x_i)$$

라우팅 정규화 $\mathcal{L}_{\text{moe}}$ 는 세 항의 합이다(부록 B.1).

- $\mathcal{L}_{\text{bal}}$: load-balancing. 프레임/태스크 라우터 각각의 expert importance와 load에 대한 $\text{CV}^2$ 합으로 라우팅 붕괴 방지
- $\mathcal{L}_z$: router z-loss. 라우팅 logit의 수치 안정화
- $\mathcal{L}_{\text{null}}$: 합성 편집 메타데이터로 만든 이진 시간 마스크 $m_{b,i}$ 를 이용해, **변경 없는 구간은 null expert로, 편집 구간은 null expert를 피하도록** 유도하는 BCE 형태 손실

### 4) 단계적 학습 (Staged Training)

복잡한 편집 삼중항으로 바로 학습하면, 복합 지시 실패가 "편집 연산을 못 해서"인지 "장면 자체를 이해 못 해서"인지 구분이 안 된다. 그래서 커리큘럼을 나눈다.

1. **Text-to-FOA 사전학습**: 소스-타깃 쌍을 장면 수준 FOA-caption 예제로 분해해 학습. 기본적인 공간 오디오 생성 능력과 이벤트·공간 배치·움직임·실내 음향에 대한 언어 grounding을 확보.
2. **단일 연산 편집 학습**: 4개 축의 atomic 편집 능력 습득.
3. **복합 편집 학습**: 다중 연산 데이터를 추가해 joint training. **중간 편집 시퀀스가 아니라 최종 타깃 장면으로만** 지도한다.

### 5) SPO: Spatial Preference Optimization

지도 flow matching은 타깃을 지정하지만, **그럴듯한 실패 사례와 타깃을 명시적으로 대비시키지는 않는다**. 실제로 모델은 소스를 그대로 복사하거나, 엉뚱한 이벤트를 바꾸거나, 방향을 틀리게 배치할 수 있다.

이를 [DPO](https://arxiv.org/abs/2305.18290) 기반 정렬 목적함수로 해결한다. 핵심은 **편집 타입별로 설계한 negative target**이다.

- **wrong-edit negative**: 그럴듯하지만 틀린 편집 (잘못된 이벤트를 바꿈, 잘못된 방향으로 이동, 잘못된 궤적, 잘못된 실내 음향)
- **no-operation negative**: 소스 장면을 그대로 둠 (소스 복사 방지)

둘의 비율은 **2:1** (wrong-edit : no-op)이며, 편집 타입마다 **10K개의 선호 예제**를 만든다. 평균 길이는 약 **9.17초**.

정책 모델 $\theta$ 의 per-sample flow-matching loss $\ell^+_\theta, \ell^-_\theta$ 와 고정된 reference 모델의 $\ell^+_{\text{ref}}, \ell^-_{\text{ref}}$ 로부터

$$\Delta = \beta\left[(\ell^-_\theta - \ell^+_\theta) - (\ell^-_{\text{ref}} - \ell^+_{\text{ref}})\right], \quad \mathcal{L}_{\text{SPO}} = -\log \sigma(\Delta)$$

(flow loss는 낮을수록 선호되므로 부호가 이렇게 잡힌다.) 최종 정렬 손실은 positive 지도 손실을 유지한다.

$$\mathcal{L}_{\text{align}} = \mathcal{L}_{\text{SPO}} + \lambda_{\text{pos}} \ell^+_\theta + \lambda_{\text{moe}} \mathcal{L}_{\text{moe}}$$

SPO 학습 중 positive와 negative는 **같은 noise와 같은 timestep을 공유**한다. 샘플링 무작위성이 아니라 타깃 편집 자체에 선호 비교가 집중되도록 하기 위해서다.

### 6) Staircase CFG (추론 전략)

추론 시 소스 오디오와 지시는 서로 다른 guidance 강도가 필요하다. 소스 조건은 무관한 내용과 공간 맥락을 **보존**해야 하고, 지시 조건은 요청된 변화를 **강제**해야 한다. 합쳐진 조건에 단일 CFG scale을 걸면 이 둘을 따로 제어할 수 없다.

조건 dropout 덕분에 각 solver step에서 세 가지 속도 예측이 가능하다.

$$v_\emptyset = v_\theta(z_t, t, \emptyset, \emptyset), \quad v_{\text{src}} = v_\theta(z_t, t, z_{\text{src}}, \emptyset), \quad v_{\text{all}} = v_\theta(z_t, t, z_{\text{src}}, c)$$

$$\tilde{v}_\theta = v_\emptyset + s_{\text{src}}(v_{\text{src}} - v_\emptyset) + s_{\text{inst}}(v_{\text{all}} - v_{\text{src}})$$

$\emptyset \rightarrow z_{\text{src}} \rightarrow (z_{\text{src}}, c)$ 라는 계단식 경로가 먼저 생성을 소스 장면에 고정(anchor)하고, 그 다음 지시를 **잔차(residual) 편집**으로 적용한다. [InstructPix2Pix](https://arxiv.org/abs/2211.09800)류의 평면적 two-scale CFG에 비해 튜닝이 쉽고 보존-지시추종 간 충돌이 줄어든다는 것이 저자들의 주장이다.

### 7) 데이터 구축

| 항목 | 내용 |
|---|---|
| 원천 코퍼스 | AudioCaps, FSDKaggle2019, PicoAudio, LibriSpeech, Spatial LibriSpeech |
| 렌더링 | PyRoomAcoustics (방향·거리·이동 궤적·실내 반사 조건을 명시적으로 제어) |
| 장면 구성 | 예제당 2~4개 오디오 이벤트 |
| 학습 규모 | 단일 연산 태스크당 약 **125K** 삼중항, 복합 편집 **250K** 삼중항, 예제당 약 **8.9초** |
| 지시 다양화 | Gemini 2.5 Pro로 편집 지시당 **3개 패러프레이즈** 생성 (10~25 단어, 1문장) |
| 테스트셋 | 단일 연산 편집 타입별 **50개**, 2-/3-/4-연산 복합 편집 각 **50개**. 학습셋과 원본 클립 비중복 |
| FOA 채널 순서 | W, Y, Z, X |

방향은 10가지로 정의한다. right, front, left, back, front-right, front-left, back-left, back-right의 8개는 방위각 $[0°, 90°, 180°, 270°, 45°, 135°, 225°, 315°]$ 에 대응하고, above / below는 수직 방향을 뜻한다(정확히 머리 위/아래로 제한하지는 않음). 변동성을 위해 방위각·거리를 정한 뒤 그 위치를 중심으로 한 작은 구형 영역에서 최종 음원 위치를 랜덤 샘플링한다.

방 크기는 4단계다. small $[2,2,2]$, medium $[6,6,4]$, large $[21,21,10]$, extra-large $[100,100,100]$ 미터이며, extra-large는 개방 공간(open space)으로 간주한다. 기본값은 $[21,21,10]$.

렌더링은 Habitat 대신 PyRoomAcoustics를 썼는데, 그 이유가 흥미롭다. Habitat의 복잡한 장면 기하는 직접음 전파에 **폐색(occlusion)** 을 일으키고 강한 다중경로 반사를 만들어, 청취 위치에서의 방향 단서가 부정확해지기 때문이다.

### 학습 설정

- 베이스 text-to-FOA 모델: 975K 샘플로 **300K steps**
- 편집 모델: 베이스에서 초기화 후 **500K steps**
- SPO 후학습: **2 epochs**
- 조건 dropout: 소스 오디오와 텍스트를 각각 독립적으로 **10%** 확률로 빈 입력 대체 (staircase CFG의 세 분기를 가능하게 함)
- CFG scale: $s_{\text{src}} = s_{\text{inst}} = 3.0$ (모든 실험 공통)
- 모든 결과는 **단일 학습 run**에서 얻음

---

## 실험 결과 / 연구 의의

### 평가 지표

두 축으로 나뉜다.

- **의미/품질**: FD, FAD(사전학습 오디오 임베딩 공간에서의 분포 거리), KL(이벤트 수준 클래스 확률 불일치), LSD(스펙트럼 왜곡), [CLAP](https://arxiv.org/abs/2211.06687) score(편집 지시와 생성 오디오의 CLAP 임베딩 코사인 유사도 = 지시 추종도)
- **공간 충실도**: GCC MSE(GCC-PHAT 기반), CRW MSE(StereoCRW feature 기반), FSAD(Fréchet Stereo Audio Distance)

공정 비교를 위해 **모든 방법을 공통 2채널 스테레오 공간에서 평가**한다. SwanWeave는 FOA를 직접 생성하므로, 출력과 레퍼런스 모두 동일한 고정 FOA-to-stereo 디코더로 렌더링한 뒤 지표를 계산한다. 베이스라인은 스테레오 출력을 같은 파이프라인에 넣는다.

### 베이스라인

FOA를 직접 편집하는 선행 방법이 없으므로, FOA 결과를 스테레오 프록시로 디코딩해 비교한다. [AudioEditor](https://arxiv.org/abs/2409.12466)(백엔드를 Auffusion 대신 BEWO/SpatialSonic 공간 오디오 생성기로 교체해 binaural 출력 지원), [ZETA](https://arxiv.org/abs/2402.10009), [SDEdit](https://arxiv.org/abs/2108.01073)(ZETA와 함께 Stable Audio Open을 백본으로), [SmartDJ](https://arxiv.org/abs/2509.21625)(모든 편집 연산을 한 번의 추론에 동시 투입하는 one-stage 설정으로 적응)와 비교한다.

### Table 1. 전체 편집 타입 평균 객관 평가

HP는 각 베이스라인 대 본 방법의 쌍대 인간 선호도 분할이다.

| Method | Speed | FD ↓ | FAD ↓ | KL ↓ | LSD ↓ | CLAP ↑ | GCC ↓ | CRW ↓ | FSAD ↓ | HP (baseline-ours) |
|---|---|---|---|---|---|---|---|---|---|---|
| ZETA | 56.26s | 14.84 | 4.03 | 4.43 | 3.29 | 0.17 | 51.85 | 22.12 | 0.78 | 17.88% - 82.12% |
| AudioEditor | 119.97s | 8.66 | 3.19 | 2.46 | 2.89 | 0.19 | 28.19 | 44.50 | 0.55 | 25.67% - 74.33% |
| SDEdit | 32.28s | 8.60 | 2.03 | 2.41 | 2.72 | 0.18 | 24.19 | 25.48 | 0.40 | 23.30% - 76.70% |
| SmartDJ | 4.23s | 8.47 | 2.87 | 2.69 | 2.56 | 0.17 | 20.32 | 33.07 | 0.32 | 38.44% - 61.56% |
| **Ours (SwanWeave)** | **1.17s** | **5.47** | **1.16** | **1.67** | **1.07** | **0.21** | **12.39** | **18.80** | **0.31** | - |

읽을 점:

- **속도**: 평균 1.17초. 가장 빠른 베이스라인 SmartDJ(4.23s)보다 3.6배, ZETA(56.26s)보다 48배 빠르다. 반복적 diffusion 샘플링이나 순차 편집 연산이 필요 없는 one-stage latent 편집이라는 설계의 직접적 결과다.
- **공간 충실도**: GCC 12.39는 최고 베이스라인(SmartDJ 20.32)보다 낮다. FOA 채널에 인코딩된 방향 구조가 편집 후에도 더 잘 보존된다는 뜻이다. CRW 18.80은 FOA-to-stereo 디코딩 후 스테레오 공간 단서가 더 정확함을, FSAD 0.31은 타깃 분포에 더 가까운 공간 표현을 생성함을 시사한다.
- **지시 추종**: CLAP 0.21로 최고. 다만 절대값 차이는 크지 않다(베이스라인 0.17~0.19).
- **인간 평가**: 3명의 annotator가 소스 오디오 + 편집 지시 + 두 편집 결과를 듣고 오디오 품질과 지시-오디오 정합을 함께 고려해 더 나은 쪽을 고르는 쌍대 비교. 모든 베이스라인 대비 선호된다. 다만 SmartDJ 대비 61.56%는 다른 베이스라인(74~82%)보다 격차가 좁다.

### Table 2. 동적 편집(motion) 전용 비교

여기가 이 논문에서 가장 극적인 결과다. Dis Motion은 음원의 거리가 점진적으로 변하는 편집을 뜻한다.

| Operation | Method | FD ↓ | FAD ↓ | KL ↓ | LSD ↓ | GCC ↓ | CRW ↓ | FSAD ↓ |
|---|---|---|---|---|---|---|---|---|
| Angle Motion | SmartDJ | 6.70 | 2.40 | 1.92 | 2.36 | 23.25 | 50.16 | 0.29 |
| Angle Motion | **Ours** | **3.41** | **1.23** | **0.66** | **0.80** | **1.15** | **14.84** | **0.23** |
| Dis Motion | SmartDJ | 11.10 | 1.88 | 3.18 | 2.77 | 16.45 | 28.66 | 0.33 |
| Dis Motion | **Ours** | **5.54** | **0.93** | **1.25** | **0.86** | **1.74** | **11.32** | **0.22** |

Angle motion에서 GCC가 23.25 → 1.15로, CRW가 50.16 → 14.84로 떨어진다. Distance motion에서도 GCC 16.45 → 1.74, CRW 28.66 → 11.32. **방향과 거리의 정확한 시간적 변화가 요구되는 동적 공간 편집에서 격차가 가장 크게 벌어진다**는 것이 이 표의 메시지다.

### Table 3. Ablation

| Variation | FD ↓ | FAD ↓ | KL ↓ | LSD ↓ | CLAP ↑ | GCC ↓ | CRW ↓ | FSAD ↓ |
|---|---|---|---|---|---|---|---|---|
| w/o pretrain | 8.49 | 3.15 | 2.78 | 2.33 | 0.16 | 21.24 | 25.09 | 0.39 |
| w/o MoE | 6.84 | 2.72 | 2.34 | 1.66 | 0.21 | 14.05 | 19.51 | 0.29 |
| w/o task expert | 6.21 | 2.14 | 1.98 | 1.24 | 0.18 | 13.76 | 17.91 | 0.38 |
| w/o SPO | 5.94 | 1.82 | 1.85 | 1.10 | 0.21 | 15.45 | 19.89 | 0.32 |
| **Full (Table 1 기준)** | **5.47** | **1.16** | **1.67** | **1.07** | **0.21** | **12.39** | **18.80** | **0.31** |

- **사전학습 제거의 타격이 가장 크다.** FD 5.47 → 8.49, KL 1.67 → 2.78, CLAP 0.21 → 0.16. text-to-FOA 사전학습이 FOA 생성의 강한 초기화이자 의미 정렬의 기반임을 보여준다. 편집 전용 학습만으로는 장면 이해 자체가 부족해진다.
- **MoE 전체 제거** 시 FD, KL, LSD가 나빠진다. 공유 FFN 하나로는 이질적 공간 편집 연산을 모델링하기 어렵다.
- **task expert만 제거**하면 MoE 완전 제거보다는 낫다(프레임 수준 라우팅이 국소 시간 적응에 유용). 하지만 full 모델보다는 나쁘고, 특히 FSAD가 0.31 → 0.38로 오히려 MoE 완전 제거(0.29)보다도 나빠진다. 지시 조건 task expert가 **보완적인 지시 수준 특화**를 제공한다는 해석이다.
- **SPO 제거**는 지표 절대값 차이가 가장 작지만, 공간 지표에서 뚜렷하다(GCC 12.39 → 15.45, CRW 18.80 → 19.89). 지도 학습만으로는 소스 복사, 엉뚱한 이벤트 수정, 잘못된 공간 배치 같은 **그럴듯한 편집 실패**를 충분히 억제하지 못한다는 것.

### Table 4. One-stage vs Multi-stage (복합 편집 샘플)

2-, 3-, 4-연산 복합 편집 각 100개 테스트 예제를 대상으로, 복합 편집을 순차 실행한 경우와 최종 결과를 직접 예측한 경우를 비교한다.

| Method | Speed (s) ↓ | FD ↓ | FAD ↓ | KL ↓ | LSD ↓ | CLAP ↑ | GCC ↓ | CRW ↓ | FSAD ↓ |
|---|---|---|---|---|---|---|---|---|---|
| SmartDJ multi-stage | 10.73 | 9.88 | 3.12 | 2.82 | 2.99 | 0.17 | 27.99 | 47.99 | 0.44 |
| SmartDJ one-stage | 4.23 | 8.47 | 2.87 | 2.69 | 2.56 | 0.17 | 20.32 | 33.07 | 0.32 |
| Ours multi-stage | 3.96 | 7.16 | 1.67 | **1.36** | 1.82 | **0.23** | 19.45 | 22.29 | 0.37 |
| **Ours one-stage** | **1.17** | **5.47** | **1.16** | 1.67 | **1.07** | 0.21 | **12.39** | **18.80** | **0.31** |

이 논문의 핵심 가설을 직접 검증하는 표다. 순차 실행은 오디오·공간 충실도를 떨어뜨리면서 추론 시간을 크게 늘린다. 본 모델 기준 one-stage가 FD 7.16 → 5.47, FAD 1.67 → 1.16, LSD 1.82 → 1.07, GCC 19.45 → 12.39, CRW 22.29 → 18.80, FSAD 0.37 → 0.31로 개선된다. SmartDJ에서도 같은 방향의 열화가 관측된다.

**다만 저자들이 솔직하게 인정하는 부분**: KL(1.36 → 1.67)과 CLAP(0.23 → 0.21)은 multi-stage 쪽이 더 좋다. 즉 one-stage의 주된 이점은 **전반적 복원 품질과 공간 일관성**이지, 모든 의미(semantic) 지표를 일률적으로 개선하는 것은 아니다. 순차 실행이 각 연산을 명시적으로 밟기 때문에 이벤트 수준 의미 정합은 오히려 유리할 수 있다는 해석이 가능하다.

### Table 5. CFG scale 선택

각 scale 조합마다 40개 샘플을 생성해, 편집되지 않아야 할 소스 내용이 보존되었는지와 요청된 편집이 성공했는지를 수작업으로 평가했다. 항목은 (보존 성공 수 / 편집 성공 수) / 40이다.

| $s_{\text{src}}$ \ $s_{\text{inst}}$ | 1.5 | 3.0 | 4.5 |
|---|---|---|---|
| 1.5 | 36 / 23 | 33 / 28 | 28 / 30 |
| 3.0 | 36 / 24 | **36 / 31** | 30 / 31 |
| 4.5 | 38 / 20 | 33 / 29 | 31 / 33 |

보존과 편집 성공이 명확한 trade-off 관계임을 보여준다. $s_{\text{inst}}$ 를 올리면 편집 성공률이 오르지만 보존이 떨어지고, $s_{\text{src}}$ 를 올리면 반대다. $(3.0, 3.0)$ 이 균형점으로 선택되었다.

### 추가 실험: 지시 강건성

구어체·중복 표현·모호한 표현이 섞인 지시 50개로 평가한 결과, **지시 준수 44%, 소스 보존 76%**를 기록했다. 복잡도별 인간 평가에서는 SmartDJ 대비 평균 **62%** 선호를 얻었고, **편집 복잡도가 올라갈수록 우위가 커졌다**. (원문 C.2에서 모델을 "SPATIALEDIT"으로 지칭하는데, 익명화 과정의 잔재로 보인다.)

지시 준수 44%라는 수치는 솔직하게 낮다. 정제된 지시에서는 잘 동작하지만 **자연스러운 구어 지시에 대한 grounding은 여전히 절반 이하**라는 뜻이다.

### 연구 의의

1. **FOA 파형 수준 편집을 하나의 태스크로 정립했다.** 지금까지 공간 오디오 연구는 "생성"과 "이해"에 몰려 있었고, "기존 3D 장면을 언어로 수정"이라는 축은 비어 있었다. 이 논문은 4개 편집 축과 10종 이상 연산, 그리고 그에 맞는 paired supervision 구축 레시피를 함께 제시한다.
2. **복합 편집은 분해가 아니라 결합으로 풀어야 한다는 실증.** Table 4가 이를 직접 보여준다. 순차 실행의 오차 누적이 실제로 측정 가능한 크기로 존재한다.
3. **동적 공간 편집이 결정적 차별점.** Table 2의 GCC 20배 개선은 시간에 따라 변하는 방향·거리 궤적이 순차 파이프라인으로는 사실상 다루기 어려운 영역임을 시사한다.
4. **Null expert라는 설계.** "편집 = 일부 변경 + 나머지 보존"이라는 태스크 구조를 아키텍처에 직접 새겨 넣은 사례로, 다른 편집 도메인(비디오, 3D 장면)으로도 이식 가능한 아이디어다.
5. **Staircase CFG.** 보존 조건과 지시 조건을 분리해 잔차로 쌓는 방식은, multi-condition 편집 일반에 적용 가능한 추론 기법이다.

---

## 한계

### 논문이 명시한 한계

**1) 시뮬레이션 데이터 의존**
Paired supervision 전체가 PyRoomAcoustics 기반 controllable room simulation으로 만들어졌다. 정확한 source-target 정렬을 얻을 수 있다는 장점의 이면에, 실제 녹음의 음향적 복잡성을 충분히 담지 못한다. 저자들이 직접 꼽는 항목은 **마이크 특성, 배경 잡음, 폐색(occlusion), 매우 불규칙한 방 응답**이다. 실제 녹음 FOA 데이터로의 확장이 중요한 후속 과제로 남는다.

여기에 더해, 렌더링 자체가 shoebox room(직육면체) 가정이다. 실내 기하가 단순하고, RIR도 벽 흡수와 반사 차수로 결정된다. 실제 공간의 복잡한 기하·재질 다양성과는 거리가 있다.

**2) 장면 길이와 복잡도의 제약**
대부분의 예제는 소수의 사운드 이벤트를 담고 길이가 약 10초다(학습 삼중항 평균 8.9초, SPO 예제 평균 9.17초). 더 긴 장면, 더 촘촘한 이벤트 혼합, 겹치는 궤적, 더 개방적(open-ended)인 지시를 다루려면 **더 강한 long-context 모델링과 더 다양한 supervision**이 필요하다.

### 명백해 보이는 추가 한계

**3) 평가가 스테레오로 축약된다.** 공정 비교를 위해 FOA 출력을 고정 디코더로 스테레오 렌더링한 뒤 GCC/CRW/FSAD를 계산한다. 그런데 FOA의 가장 큰 이점 중 하나는 **고도(elevation), 즉 위/아래 방향**인데, 2채널 스테레오로 내려오면 이 정보가 상당 부분 소실된다. above/below 편집이 얼마나 정확한지는 현재 지표 체계로 직접 측정되지 않는다.

**4) 구어 지시에 대한 grounding이 약하다.** 부록 C.2의 44% 지시 준수율. 학습 지시는 Gemini 2.5 Pro가 "10~25 단어, 1문장"의 정형화된 스펙으로 생성한 것이라, 실제 사용자의 모호하고 장황한 발화와는 분포가 다르다.

**5) 인간 평가 규모와 구성.** annotator가 3명이며, 저자들의 연구 그룹에서 모집한 자원봉사 대학원생으로 금전적 보상이 없었다(부록 C.3). 평가 기준도 "오디오 품질과 지시 추종을 함께 고려"라는 단일 축 쌍대 비교라, 보존 실패와 편집 실패를 분리해 보기 어렵다.

**6) 단일 학습 run.** 모든 결과가 single training run에서 나왔다고 명시되어 있어, 분산(variance) 정보가 없다. Ablation의 작은 차이(예: SPO 제거 시 FD 5.47 → 5.94)를 얼마나 신뢰할지 판단할 근거가 부족하다.

**7) 시각 정보 부재.** 편집 지시가 순전히 텍스트다. 실제 프로덕션에서는 "화면 속 저 인물의 소리를" 같은 시각 참조가 자연스럽지만, 이 프레임워크는 시각 조건을 다루지 않는다.

**8) CLAP 지표의 한계.** 지시 추종을 CLAP 유사도로 측정하는데, CLAP은 기본적으로 semantic alignment 모델이지 **공간 속성을 평가하도록 학습되지 않았다**. "왼쪽으로 옮겨라"가 제대로 수행되었는지를 CLAP이 판별할 수 있다고 보기는 어렵다. 실제로 베이스라인 간 CLAP 차이(0.17~0.21)가 매우 작은 것도 이 지표의 해상도 한계를 시사한다.

---

## 우리 연구와 연결되는 점

### Spatial Audio 관점

- **편집이라는 새로운 축.** 지금까지 공간 오디오는 생성(generation), 공간화(spatialization), 이해(understanding)로 나뉘어 왔다. 이 논문은 "**기존 3D 음장의 언어 기반 수정**"을 네 번째 축으로 제안한다. 공간 오디오 연구 지형을 정리할 때 참조할 만한 프레이밍이다.
- **FOA를 latent로 다루는 실전 레시피.** stereo FOA VAE($d=128$)로 4채널을 압축하고 DiT + flow matching으로 편집하는 구조는, FOA를 직접 다루려는 어떤 연구에도 바로 재사용 가능한 백본 설계다. 소스 latent와 노이즈 latent를 feature 차원으로 concat해 self-attention이 프레임 대응을 학습하게 하는 트릭도 단순하고 효과적이다.
- **공간 편집의 평가 문제.** 이 논문이 쓴 GCC-PHAT / StereoCRW / FSAD 조합은 현재 공간 오디오 편집 평가의 사실상 표준에 가깝다. 동시에, FOA를 스테레오로 내려 평가할 수밖에 없었다는 점이 **FOA 네이티브 평가 지표의 부재**를 드러낸다. 고도 정확도, 궤적 정확도, 공간적 보존도를 4채널에서 직접 재는 지표는 아직 열려 있는 문제다.
- **Null expert 아이디어.** "변경 없는 영역은 0 텐서를 반환"이라는 명시적 설계와 이를 유도하는 $\mathcal{L}_{\text{null}}$ 마스크 손실은, 보존-편집 trade-off가 있는 모든 편집 태스크에 이식 가능하다.
- **Staircase CFG.** 보존 조건과 편집 조건을 분리해 잔차로 쌓는 추론 전략. 다중 조건 편집 모델을 다룬다면 바로 시도해볼 수 있는 저비용 개선이다.

### Egocentric Vision 관점

- **1인칭 오디오는 본질적으로 FOA와 궁합이 좋다.** 머리에 장착한 마이크 어레이는 청취자 중심 좌표계를 자연스럽게 정의한다. 이 논문이 "listener를 방 중심에 두고 source-listener 단위 벡터로 FOA를 인코딩"하는 방식은 egocentric 설정과 동형이다. Ego4D/Ego-Exo4D류 데이터에 공간 오디오를 결합하려는 연구라면 이 데이터 구축 파이프라인이 직접 참고가 된다.
- **10방향 언어 라벨 체계.** right/front/left/back/front-right/.../above/below의 10방향과 방위각 매핑은, egocentric 장면 기술(scene description)에서 공간 관계를 언어화할 때 그대로 쓸 수 있는 어휘 설계다.
- **동적 궤적이 1인칭의 핵심.** 1인칭 영상에서는 착용자가 계속 움직이므로 음원의 상대 방향·거리가 끊임없이 변한다. 이 논문이 angle motion / distance motion을 별도 태스크로 두고 그 축에서 가장 큰 성능 격차를 보였다는 사실은, **egocentric 공간 오디오에서 정적 정위보다 동적 궤적이 더 중요하고 더 어렵다**는 시사점을 준다.
- **빠진 연결고리: 시각 조건.** 이 프레임워크는 텍스트만 조건으로 쓴다. Egocentric vision 연구자 입장에서 가장 자연스러운 확장은 **1인칭 프레임을 조건으로 추가한 spatial audio editing**이다. "내가 보고 있는 저 소리를 키워라" 같은 gaze/시선 기반 참조는 아직 미개척 영역이다.

### Hand-Object Interaction 관점

- **접촉음의 공간 편집.** 손-물체 상호작용은 타격, 마찰, 파지 등 짧고 국소적인 접촉음을 만든다. 이런 이벤트는 (a) 시간적으로 sparse하고, (b) 손의 위치, 즉 청취자 기준 근거리에 정위된다. 이 논문의 add/replace/distance change 편집은 이런 접촉음을 조작하는 도구가 될 수 있다.
- **Null expert와 sparse 이벤트.** 접촉음처럼 짧은 이벤트를 편집할 때, 프레임 단위 라우팅과 null expert 조합은 "접촉 순간만 건드리고 나머지 프레임은 그대로"를 구현하는 자연스러운 메커니즘이다. HOI 오디오의 시간적 sparsity와 잘 맞는다.
- **한계도 그대로 물려받는다.** 이 논문의 학습 장면은 2~4개 이벤트, 약 10초, shoebox room이다. 실제 HOI 상황은 근거리 음원(near-field), 손·몸에 의한 폐색, 물체 재질별 방사 패턴이 지배적인데, 여기서 쓴 point source + 직육면체 방 시뮬레이션은 이런 요소를 담지 못한다. 저자들이 Habitat을 배제한 이유(폐색과 다중경로 반사가 방향 단서를 흐린다)가, 역설적으로 HOI 쪽에서는 **오히려 모델링해야 할 현상**이다.
- **Paired supervision 구축 전략의 이식.** "이벤트를 샘플링해 소스 장면을 합성하고, 편집 후 타깃을 다시 렌더링하며, 편집별로 wrong-edit / no-op negative를 설계한다"는 레시피는 도메인 독립적이다. HOI 오디오-비주얼 데이터에서 paired supervision을 만들 때 그대로 차용할 수 있다.

### 방법론 일반

- **DPO를 생성 모델 정렬에 쓰는 구체적 설계.** SPO의 핵심은 negative를 "임의로 망가뜨린 오디오"가 아니라 **태스크별 실패 모드(wrong-edit, no-op)로 설계**했다는 점이다. 특히 no-op negative는 "입력을 그대로 복사하는" 편집 모델의 고전적 실패를 정면으로 겨냥한다. 편집·변환 태스크에 선호 학습을 적용하려는 어떤 연구에도 바로 적용 가능한 패턴이다. 2:1 비율과 positive/negative가 **같은 noise·timestep을 공유**하도록 한 디테일도 재현에 중요하다.
- **Staged curriculum의 가치.** Ablation에서 사전학습 제거가 가장 큰 성능 하락을 낳았다. "생성 능력 → atomic 편집 → 복합 편집"으로 나누면, 복합 지시 실패의 원인을 장면 이해 부족과 편집 연산 실패로 분리해 진단할 수 있다. 멀티태스크 편집 모델 설계 시 기본으로 삼을 만한 원칙이다.
- **MoE의 task-level / token-level 이중 라우팅.** 태스크 식별자가 명시적으로 주어지지 않고 **자연어 지시에서 유도되는** task expert 선택은, 멀티태스크 조건부 생성 전반에 응용 가능하다. top-$k$ 대신 top-$p$ 라우팅으로 입력 복잡도에 따라 활성 전문가 수를 가변시키는 것도 계산 효율 측면에서 참고할 점이다.

### 리소스

- 데모: swanaigc/swanweave
- 코드: github.com/MM-Speech/SwanWeave

# PhysWave: Physics-Guided Latent Diffusion Models for Controllable Spatial Audio Generation

**arXiv**: 2608.29549 | **주제 분류**: Spatial Audio | **출판일**: 2026-08-30 | **학회**: EMNLP 2026 Main Conference
**저자/소속**: Lingfeng Yao, Chenpei Huang, Xingke Yang, Ziye Geng, Changqing Luo, Miao Pan (University of Houston), Hao Wang (Stevens Institute of Technology), Jiang Liu (Waseda University)
**링크**: https://arxiv.org/abs/2608.29549

## 한 줄 요약

텍스트로 3차원 공간 음향(FOA)을 만들 때, 소리의 방향과 거리가 지켜야 할 물리 법칙을 미분 가능한 손실 함수로 직접 학습에 집어넣고, 자연어와 좌표 궤적을 하나의 "웨이포인트-캡션" 표현으로 통합한 latent diffusion 모델이다.

## 메인 그림

![스페이셜 캡션을 LLM이 음향 캡션 + 웨이포인트 궤적으로 분해하고, 이를 조건으로 FOA latent diffusion을 학습하되 디코딩된 파형에 물리 일관성 손실을 거는 PhysWave 전체 구조](https://arxiv.org/html/2608.29549v1/framework.png)

Figure 2. 왼쪽에서 사용자의 공간 묘사 문장이 LLM 파서를 거쳐 "무슨 소리인가(acoustic caption)"와 "어디서 어떻게 움직이는가(waypoint trajectory)"로 갈라지고, 이 둘이 temporal token과 함께 DiT의 조건으로 들어간다. 오른쪽에서는 diffusion이 예측한 latent를 **다시 FOA 파형으로 디코딩해** 방향·거리 물리 손실을 계산하는 경로가 핵심이다. 보통의 latent diffusion이 latent 공간에서만 감독하는 것과 달리, 여기서는 파형까지 내려가야 물리량(채널 간 관계, 에너지 포락선)을 잴 수 있기 때문이다.

## 선행 연구

공간 음향 생성 연구는 출력 포맷을 기준으로 크게 세 갈래로 나뉜다.

**1) 모노(monaural) 텍스트-투-오디오.** AudioLDM 계열, [Make-An-Audio 2](https://arxiv.org/abs/2305.18474)를 포함한 Make-An-Audio 계열, TANGO 계열, Stable Audio 등은 오디오 품질(fidelity)과 텍스트-오디오 의미 정합(semantic alignment)을 크게 끌어올렸다. 하지만 출력이 한 채널이라 방향·거리·움직임 정보를 아예 담지 못한다.

**2) 스테레오/바이노럴(binaural) 생성.** 두 채널 사이의 시간차(ITD, Interaural Time Difference)와 레벨차(ILD, Interaural Level Difference)를 이용해 좌우 정위감을 만든다. [AudioSpa](https://arxiv.org/abs/2502.11219)와 DualSpec은 텍스트로 바이노럴 오디오를 만들고, SpatialSonic은 언어와 다른 모달리티로 스테레오 생성을 제어한다. 다만 바이노럴은 청자 중심(listener-centric) 포맷이라 3차원 음장 전체를 표현하지는 못한다.

**3) FOA(First-Order Ambisonics, 1차 앰비소닉스 — 3차원 음장을 $W, X, Y, Z$ 네 개의 구면 조화(spherical harmonic) 채널로 표현하는 방식) 생성.** FOA는 특정 스피커 배치에 묶이지 않고 헤드폰·스피커 어레이 어디로든 디코딩할 수 있어 device-agnostic한 포맷이다. Diff-SAGe는 음원 카테고리와 위치로 FOA를 생성하고, ImmerseDiffusion은 텍스트 조건 FOA 생성을 정적(static) 음원에 대해 다뤘으며, SonicMotion은 이를 움직이는 음원(원형 궤도)까지 확장했다. ViSAGe와 OmniAudio는 영상/360도 영상에서 FOA를 만든다.

**4) 물리 유도(physics-guided) 생성 모델.** PINN(Physics-Informed Neural Network)처럼 지배 방정식 위반을 패널티로 주는 흐름이 diffusion으로도 넘어와, 유체 흐름장 복원, 기온 다운스케일링, 적외선 영상 생성 등에 쓰였다. 음향 쪽에서는 파동 방정식·헬름홀츠 방정식 기반 prior로 음장 추정/복원(sound field estimation)을 다뤘지만, 이는 측정값으로부터의 역문제(inverse reconstruction)이지 텍스트 조건 생성이 아니다.

## 문제 제기

논문은 기존 text-to-FOA의 한계를 두 가지로 명확히 못 박는다.

**한계 1 — 물리적 일관성을 보장할 수 없다.**
FOA는 지켜야 할 관계식이 이미 알려져 있다. 방위각 $\theta$, 고도각 $\phi$에서 도착하는 점음원의 압력 신호 $s(t)$에 대해 FOA 인코딩은

$W(t) = \tfrac{1}{\sqrt{2}} s(t),\quad X(t) = s(t)\cos\phi\cos\theta,\quad Y(t) = s(t)\cos\phi\sin\theta,\quad Z(t) = s(t)\sin\phi$

로 정해진다. 즉 네 채널은 독립된 오디오 스트림이 아니라, **채널 간 비율 자체가 방향을 인코딩**한다. 거리 $r$에 대해서도 자유장(free field)에서 압력은 대략 $1/r$로 감쇠하고 에너지는 $1/r^2$ 꼴을 따른다. 그런데 기존 FOA 생성 모델은 이 관계를 데이터에서 **암묵적으로만** 배운다. 그 결과 귀로 들으면 그럴듯한데 FOA 채널에는 엉뚱한 방향이 박혀 있거나, 음원-청자 거리와 맞지 않는 에너지 포락선(energy envelope)이 나오는 일이 생긴다. 이 관계식들은 이미 알려져 있고 미분 가능하므로, 학습과 샘플링에 명시적 prior로 넣을 수 있는데도 활용하지 않았다는 것이 논문의 지적이다.

**한계 2 — 사용자 인터페이스가 갈라져 있다.**
ImmerseDiffusion과 SonicMotion은 제어 인터페이스를 둘로 분리해 제공한다. 파라메트릭(parametric) 모드는 방위각·고도각·거리·움직임 같은 수치를 직접 받아 정밀하지만, 사용자가 저수준 공간 변수를 일일이 지정해야 한다. 디스크립티브(descriptive) 모드는 자연어를 받아 쓰기는 쉽지만 방향·거리·시간에 따른 변화에 대해 제어가 거칠다. 사용자는 **쓰기 편함과 정밀함 사이에서 하나를 포기**해야 한다. 하나의 모델 안에서 두 방식을 모두 받아주는 통합 인터페이스가 필요하다.

여기에 데이터 문제도 겹친다. 정확한 음원 궤적이 라벨링된 실제 FOA 녹음을 대규모로 모으기는 어렵다.

## 연구 주제

PhysWave가 새로 정의하는 문제는 **"물리적으로 일관되며 동시에 궤적 수준으로 제어 가능한 text-to-FOA 생성"**이다. 기존 흐름과 다른 점은 세 축이다.

- **물리를 목적 함수로 승격.** 기존 FOA 생성이 "데이터에서 알아서 배워라"였다면, PhysWave는 구면 조화 방향 관계와 역제곱 거리 관계를 **미분 가능한 손실**로 만들어 학습 목표에 직접 더한다. 게다가 이 손실은 학습이 끝난 뒤에도 샘플링 단계의 gradient guidance로 재사용할 수 있어, **재학습 없이(training-free)** 공간 정확도를 더 끌어올리는 도구가 된다.
- **표현의 통합.** 자연어와 파라메트릭 제어를 두 개의 모드로 두지 않고, 둘 다 같은 **웨이포인트-캡션(waypoint-caption)** 표현으로 환원한다. 자연어는 LLM 파서를 거쳐 웨이포인트로 변환되고, 정밀 제어를 원하는 사용자는 웨이포인트를 직접 넣거나 파서 결과를 편집한다. 모델 입장에서는 언제나 같은 입력 형식이다.
- **동적(dynamic) 궤적으로의 일반화.** SonicMotion이 원형 궤도(circular)에 한정됐던 것과 달리, 정적·선형 통과·원형·접근/후퇴를 아우르는 일반 웨이포인트 궤적을 다룬다.

## 연구 방법

### 데이터셋 구축 (300K 클립 규모)

정확한 궤적 라벨을 가진 실제 FOA 녹음이 부족하므로, 캡션이 달린 모노 오디오를 궤적을 따라 공간화(spatialize)하는 합성 파이프라인을 만든다 (Figure 1).

**(a) 모노 소스 준비.** AudioCaps, WavCaps, Clotho에서 클립을 수집한다. 캡션이 지배적인(dominant) 단일 음향 이벤트를 묘사하는 클립을 우선 선별한 뒤, 16 kHz 리샘플링 → 에너지 기반 활동 구간 검출로 10초 구간 추출(활성 구간 1초 미만이면 폐기, 10초 미만은 제로 패딩, 초과분은 활성 프레임이 가장 많은 10초 윈도 선택) → EBU R128 라우드니스 정규화(목표 $-14$ LUFS, 파형은 $[-1, 1]$로 클리핑) → CLAP 유사도 0.3 미만 폐기 순으로 처리한다. Clotho는 캡션이 최대 5개이므로 가장 점수가 높은 것을 남긴다.

| 데이터 소스 | Train 클립 | Train 시간(h) | Test 클립 | Test 시간(h) |
|---|---|---|---|---|
| AudioCaps | 46,696 | 129.7 | 4,239 | 11.8 |
| WavCaps | 107,850 | 299.6 | – | – |
| Clotho | 2,863 | 8.0 | 1,021 | 2.8 |
| 모노 합계 | 157,409 | 437.2 | 5,260 | 14.6 |
| 렌더링된 FOA | 314,818 | 874.5 | 10,520 | 29.2 |

각 모노 클립은 정적 버전 1개 + 이동 버전 1개로 두 번 렌더링되어, 학습용 FOA 314,818개(약 874.5시간)가 나온다.

**(b) 궤적 샘플링.** 궤적은 청자 상대 좌표 $(\theta(t), \phi(t), r(t))$로 기술하고, 편집 가능하도록 웨이포인트 시퀀스 $\mathbf{W} = \{(t_i, \theta_i, \phi_i, r_i)\}_{i=1}^{M}$로 압축한다. 시뮬레이션 시에는 선형 보간으로 샘플 단위 방향·거리를 복원한다. 프레임 단위 궤적은 0.1초 간격으로 저장한다.

| 모션 패밀리 | 비율 | 샘플링 범위 | 설명 |
|---|---|---|---|
| Static | 50.0% | $\theta \in [-180°, 180°]$, $\phi \in [-35°, 35°]$, $r \in [0.5, 5]$ m | 방향·거리 고정 |
| Linear pass-by | 약 16.7% | $v \in [1, 25]$ m/s, $d_{\min} \in [1, 8]$ m | 방향과 거리가 함께 변함 |
| Circular | 약 16.7% | $r \in [0.5, 5]$ m, 각도 범위 $\geq 30°$ | 거리 거의 고정, 방향만 변함 |
| Approach/recede | 약 16.7% | $v \in [2, 6]$ m/s, $r \in [1, 60]$ m | 방향 고정, 거리만 변함 |

**(c) FOA 시뮬레이션.** 세 단계다. (i) **전파 지연** — 지연 시간 격자 $t_{\text{emit}} = t - r(t)/c$ ($c$는 음속) 위에서 소스 신호를 리샘플링한다. 이 과정에서 반경 방향 운동에 대해 도플러 효과 같은 주파수 변화가 자연스럽게 생긴다. (ii) **거리 감쇠** — 지연된 신호에 $1/r(t)$를 곱해 자유장 압력 감쇠를 모사한다. (iii) **FOA 인코딩** — 위의 구면 조화 식으로 네 채널에 투영한다. 최종 데이터는 {FOA 오디오, 프레임 단위 궤적, 원본 캡션} 삼중항이다.

### 모델 구조

**입력**: 공간 정보가 섞인 자연어 캡션(예: "왼쪽에서 다가오는 파도 소리") 또는 웨이포인트 시퀀스.
**출력**: 10초 길이 4채널 FOA 파형(16 kHz).

**(1) 통합 웨이포인트-캡션 조건화.** 얼린(frozen) LLM 파서가 공간 캡션을 두 갈래로 분해한다 — 공간 표현을 뺀 순수 음향 캡션, 그리고 궤적. 파서는 웨이포인트 배열을 직접 출력하지 않고 타입(`static`/`linear`/`arc`/`approach`/`recede`), 시작/끝 좌표, control point, 회전 방향, 속도 등 간결한 JSON을 내며, 결정적(deterministic) 후처리가 이를 $M=10$개의 웨이포인트 조건으로 변환한다. 좌표 규약은 방위각 0° = 정면, +90° = 왼쪽, $\pm 180°$ = 뒤이고, 거리 기본값은 "very close" 1 m, "close" 2 m, "normal" 8 m, "far" 25 m다. 시간이 명시되지 않으면 0–10초 전체를 쓴다.

음향 캡션은 사전학습된 T5-base 인코더(최대 128 토큰)로 text token이 된다. 웨이포인트는 모델이 물리 구조를 직접 보도록 프레임 단위 특징으로 펼친다.

$\mathbf{f}_k = [\underbrace{t_k/T}_{\text{시간}},\ \underbrace{n_x(t_k), n_y(t_k), n_z(t_k)}_{\text{방향}},\ \underbrace{1/r(t_k)^2}_{\text{거리}}]$

즉 각도를 그대로 넣는 대신 **단위 방향 벡터**와 **역제곱 거리 프로파일**이라는 물리량 형태로 주입한다. 이 시퀀스를 Q-Former 스타일 인코더가 16개 learnable query token으로 요약해 waypoint token을 만든다. 별도의 temporal 인코더가 클립 시작 시각과 길이 $(t_{\text{start}}, T)$를 temporal token으로 임베딩한다. 세 종류 토큰을 이어 붙인 joint condition $\mathbf{c}$가 cross-attention으로 DiT를 구동한다.

**(2) FOA latent diffusion 백본.** 4채널 FOA 파형을 연속 latent로 압축하는 FOA VAE를 먼저 학습한다(DAC 계열 1D 컨볼루션 구조, 입출력 채널을 $W, X, Y, Z$ 4채널로 변경, 다운샘플링 비율 1024, latent 채널 64, 2.05초 크롭). VAE 손실은 채널별 multi-resolution STFT 손실 + KL + adversarial + feature matching에 더해 **방향 일관성 손실 $\mathcal{L}_{\text{dir}}$까지 포함**한다. 가중치는 $\lambda_{\text{mrstft}}=1.0$, $\lambda_{\text{adv}}=0.1$, $\lambda_{\text{fm}}=5.0$, $\lambda_{\text{kl}}=10^{-6}$, $\lambda_{\text{dir}}=0.1$. 이후 VAE는 얼려 쓴다.

Diffusion은 코사인 노이즈 스케줄로 $\mathbf{x}_t = \alpha_t \mathbf{x} + \sigma_t \epsilon$를 만들고, DiT가 velocity target $\mathbf{v}_t = \alpha_t \epsilon - \sigma_t \mathbf{x}$를 예측한다(v-prediction). 기본 손실은 $\mathcal{L}_{\text{mse}} = \mathbb{E}[\|\hat{\mathbf{v}}_\theta(\mathbf{x}_t, t, \mathbf{c}) - \mathbf{v}_t\|_2^2]$.

**(3) 물리 유도 학습 목표 — 이 논문의 핵심.** latent 공간에서만 감독하는 대신, 예측된 velocity로 clean latent $\hat{\mathbf{x}}_0 = \alpha_t \mathbf{x}_t - \sigma_t \hat{\mathbf{v}}_\theta$를 복원하고 **얼린 VAE 디코더로 파형 $\hat{\mathbf{a}} = \mathcal{D}(\hat{\mathbf{x}}_0)$까지 되돌린 뒤** 두 가지 물리 손실을 건다.

*구면 조화 방향 일관성.* 각 프레임 $k$에서 FOA 인텐시티 벡터(intensity vector, 음의 흐름 방향을 추정하는 고전적 지표)를 계산한다.

$\hat{\mathbf{I}}_k = [\langle \hat{W}_k \hat{X}_k \rangle, \langle \hat{W}_k \hat{Y}_k \rangle, \langle \hat{W}_k \hat{Z}_k \rangle]^\top$

이를 목표 단위 방향 $\mathbf{n}_k$와 코사인 정렬시킨다.

$\mathcal{L}_{\text{dir}} = \frac{1}{K}\sum_{k=1}^{K}\left(1 - \frac{\hat{\mathbf{I}}_k^\top \mathbf{n}_k}{\|\hat{\mathbf{I}}_k\|\|\mathbf{n}_k\| + \varepsilon}\right)$

*역제곱 거리 일관성.* 전방향 $W$ 채널의 프레임 에너지 $\hat{E}_k = \langle \hat{W}_k^2 \rangle$를 목표 프로파일 $E_k^* = 1/r_k^2$와 비교한다. 절대 음량은 콘텐츠에 따라 달라지므로, 로그를 취하고 평균을 뺀 **정규화된 로그 에너지 모양**만 비교한다($\tilde{u}_k = \log(u_k + \varepsilon) - \frac{1}{K}\sum_j \log(u_j + \varepsilon)$).

$\mathcal{L}_{\text{dist}} = \frac{1}{K}\sum_{k=1}^{K}(\tilde{\hat{E}}_k - \tilde{E}_k^*)^2$

최종 목적 함수는 $\mathcal{L} = \mathcal{L}_{\text{mse}} + \lambda_{\text{dir}}\mathcal{L}_{\text{dir}} + \lambda_{\text{dist}}\mathcal{L}_{\text{dist}}$이다.

**구현 세부.** LLM 파서는 Qwen3.5-4B. 생성 백본은 Stable Audio Open을 따르되 VAE를 스테레오에서 4채널 FOA로 바꾸고, DiT는 24층 / hidden 768 / attention head 12. Q-Former 인코더는 입력 160 프레임, query token 16개, hidden 768, head 8, MLP hidden 256. 학습은 AdamW($lr = 1\times10^{-5}$, betas $(0.9, 0.99)$, weight decay $10^{-3}$), 선형 warm-up 후 $1\times10^{-6}$까지 코사인 감쇠, EMA decay 0.9999, classifier-free 조건 드롭아웃 확률 0.1, H100 1장에서 배치 64, bfloat16, 128K 스텝. 물리 손실 가중치는 $\lambda_{\text{dir}} = 1.0$, $\lambda_{\text{dist}} = 0.05$이며, 배치당 8개 샘플에 대해 40 ms 분석 프레임으로 계산하고 학습 시작부터 적용하되 denoising SNR로 가중한다. VAE는 RTX 3090 2장, 배치 12, 120K 스텝.

## 실험 결과 / 연구 의의

### 평가 지표

- **오디오 품질**: FD, FAD$_\text{CLAP}$, CLAP score, KL, IS. 표준 text-to-audio 지표는 단일 채널용이므로 FOA의 전방향 $W$ 채널에서 계산한다. FD·IS·KL은 사전학습 PANNs 분류기 기반, FAD$_\text{CLAP}$은 CLAP 임베딩 공간에서 계산.
- **공간 충실도(spatial fidelity)**: 인텐시티 벡터에서 프레임별 DoA(Direction of Arrival, 도래 방향)를 추정한 뒤 haversine 공식으로 구면 각도 오차(°)를 잰다. 거리 쪽은 $W$ 채널 에너지를 목표 $1/r_k^2$ 프로파일과 비교해 RMS 오차(InvSqErr, dB)와 피어슨 상관(InvSqCorr)을 보고한다. 무음 프레임의 영향을 막기 위해 $E_k \geq 10^{-3}\max_j E_j$인 활성 프레임만 사용한다.

### 선행 FOA 방법과의 공간 정확도 비교 (Table 2)

| 모델 | 제어 방식 | Static (°) ↓ | Moving (°) ↓ |
|---|---|---|---|
| ImmerseDiffusion-D | Static text | 7.07 | – |
| ImmerseDiffusion-P | Static param. | 2.79 | – |
| SonicMotion-D | Circular text | 20.82 | 31.09 |
| SonicMotion-P | Circular param. | 2.41 | 19.22 |
| **PhysWave** | Text + Waypoints | **1.73** | **5.78** |

공식 구현이 공개되지 않아 두 방법을 재현해 동일 프로토콜로 평가했다. 움직이는 음원에서 격차가 특히 크다 — SonicMotion은 서술형 조건에서 31.09°, 파라메트릭 조건에서도 19.22°인데 PhysWave는 5.78°다. 정적 음원에서도 1.73°로 가장 낮다. **"자연어로 편하게 쓰면서도 파라메트릭보다 정확하다"**가 이 표의 메시지다.

### 오디오 품질 ($W$ 채널, Table 3)

| 모델 | FD ↓ | FAD$_\text{CLAP}$ ↓ | CLAP ↑ | KL ↓ | IS ↑ |
|---|---|---|---|---|---|
| AudioLDM | 31.67 | 0.33 | 0.33 | 2.37 | 6.96 |
| AudioLDM 2 | 24.13 | 0.12 | 0.33 | 2.11 | 8.62 |
| Make-An-Audio | 15.44 | 0.11 | 0.37 | 1.93 | 8.79 |
| Make-An-Audio 2 | 13.86 | 0.14 | 0.40 | 1.73 | 10.85 |
| Stable Audio Open | 30.84 | 0.31 | 0.30 | 2.30 | 11.09 |
| ImmerseDiffusion | 20.45 | 0.14 | 0.35 | 1.66 | 9.55 |
| SonicMotion | 24.80 | 0.26 | 0.32 | 1.88 | 8.55 |
| **PhysWave** | 21.22 | 0.21 | 0.33 | **1.66** | 8.31 |

모노 baseline들은 FOA를 못 만들기 때문에, 같은 궤적 조건 렌더링 파이프라인으로 공간화한 뒤 비교했다. PhysWave는 KL에서 최고(1.66)이고 나머지 지표는 강한 모노 baseline들과 비슷한 수준을 유지한다. Make-An-Audio 2가 FD·CLAP·IS에서 더 좋지만 이 모델은 공간 제어 능력이 없다. **공간 제어를 추가하면서 콘텐츠 품질을 희생하지 않았다**는 것이 요지다.

### 절제 실험 (Table 1)

| 변형 | FD ↓ | FAD$_\text{CLAP}$ ↓ | CLAP ↑ | KL ↓ | IS ↑ | Static (°) ↓ | Moving (°) ↓ | InvSq Err. (dB) ↓ | InvSq Corr. ↑ |
|---|---|---|---|---|---|---|---|---|---|
| Trajectory text (웨이포인트 대신 궤적 서술문) | 23.13 | 0.20 | 0.32 | 1.74 | 8.05 | 7.33 | 17.62 | 4.59 | 0.62 |
| PhysWave (물리 손실 없음) | 21.92 | 0.20 | 0.33 | 1.69 | 8.22 | 2.05 | 6.50 | 5.15 | 0.48 |
| PhysWave (w/o $\mathcal{L}_{\text{dist}}$) | 21.79 | 0.20 | 0.33 | 1.68 | 8.15 | 1.75 | 4.81 | 4.79 | 0.59 |
| PhysWave (w/o $\mathcal{L}_{\text{dir}}$) | 21.34 | 0.20 | 0.33 | 1.67 | 8.25 | 2.47 | 6.60 | 3.78 | 0.74 |
| **PhysWave (전체)** | **21.22** | 0.21 | 0.33 | **1.66** | **8.31** | **1.73** | **4.65** | 4.06 | 0.73 |

읽어야 할 세 가지:

1. **웨이포인트 조건화가 결정적이다.** 궤적을 상세한 자연어로 바꿔 넣기만 해도 static 오차가 2.05° → 7.33°, moving 오차가 6.50° → 17.62°로 급증한다. 자유 형식 텍스트는 방향·거리·시간 변화를 정밀하게 지정하기에 부족하다는 뜻이다. 다만 LLM 파서가 사용자 텍스트와 구조화된 웨이포인트 사이의 다리를 놓아주므로 사용성은 유지된다.
2. **두 물리 손실은 서로 다른 축을 담당한다.** $\mathcal{L}_{\text{dir}}$은 각도 오차를 낮추고(moving 6.50° → 4.81°, static 2.05° → 1.75°) 역제곱 지표에는 별 영향이 없다. $\mathcal{L}_{\text{dist}}$는 거리 일관성을 담당해 InvSq Corr.을 0.48 → 0.74로, InvSq Err.을 5.15 dB → 3.78 dB로 개선한다. 둘 다 넣은 전체 모델이 각도(static 1.73°, moving 4.65°)에서 최고이고 거리도 강하다(InvSq Corr. 0.73).
3. **품질이 희생되지 않는다.** 변형들 사이에서 FD·CLAP·KL·IS가 거의 흔들리지 않는다. 보조 물리 손실이 공간 충실도만 골라서 올린다는 증거다.

(참고: Table 2의 moving 5.78°와 Table 1의 4.65°는 테스트 세트가 다르다 — 전자는 SonicMotion과 맞춘 원형 모션 세트, 후자는 절제 실험용 전체 이동 세트.)

### LLM 파서 비교 (Table 4)

GPT-4o를 judge로 써서 200개 공간 캡션에 대해 1–5점 척도로 평가했다(temperature 0).

| 파서 | Spatial Faithfulness ↑ | Semantic Preservation ↑ |
|---|---|---|
| Qwen3.5-0.8B | 1.89 ± 0.20 | 3.40 ± 0.38 |
| Llama-3.2-3B-Instruct | 2.40 ± 0.24 | 4.18 ± 0.29 |
| **Qwen3.5-4B** | **3.88 ± 0.28** | **4.72 ± 0.17** |

파서 규모가 공간 해석 정확도에 크게 영향을 준다. 작은 모델은 음향 내용 보존(semantic preservation)은 어느 정도 하지만 좌표 변환(spatial faithfulness)에서 무너진다.

### 주관 평가 (Table 5)

실제 녹음/실환경 FOA 100개 클립(STARSS23 등)에 음향 이벤트와 궤적을 수동 라벨링해 조건으로 주고, 참가자 14명이 1–5점으로 평가했다.

| 소스 | MOS-Event ↑ | MOS-Trajectory ↑ | MOS-Realism ↑ |
|---|---|---|---|
| 실제 FOA 녹음 (상한 참조) | 4.89 | 4.56 | 4.79 |
| AudioLDM2 | 2.70 | 2.07 | 2.07 |
| Stable Audio Open | 3.40 | 2.21 | 2.51 |
| **PhysWave** | **4.32** | **3.90** | **3.48** |

특히 MOS-Trajectory(공간 궤적 일치도)에서 baseline 대비 격차가 크다(3.90 vs 2.07/2.21). 다만 realism(3.48)은 실제 녹음(4.79)과 여전히 상당한 차이가 있다.

### 추론 시 물리 가이던스 (Figure 4)

학습된 모델을 건드리지 않고, 선택한 denoising 스텝에서 $\mathcal{L}_{\text{dir}}$과 $\mathcal{L}_{\text{dist}}$의 gradient로 샘플을 밀어주는 방식이다. 가이던스 스케일이 커질수록 static/moving 각도 오차가 줄고 InvSq Corr.이 올라가며, 특히 물리 손실 없이 학습한 모델("w/o physics")에서 개선 폭이 크다. 반대급부로 FAD$_\text{CLAP}$이 완만히 증가해 **공간 보정과 오디오 품질 사이의 트레이드오프**가 존재한다. 이 결과의 의의는 크다 — 같은 미분 가능 prior가 학습 목표이자 추론 시 제어 손잡이로 이중 역할을 한다는 뜻이고, 이미 학습된 FOA 생성 모델에 재학습 없이 얹을 수 있다.

### 부가 결과

- **FOA VAE 재구성 품질 (Table 9)**: STFT 1.44, Mel 1.11, L1($\theta$) 0.87°, L1($\phi$) 1.45°, $\Delta_\text{angle}$ 1.92°. 방향 손실을 VAE 학습에 넣은 덕에 latent 압축 단계에서 이미 공간 구조가 거의 보존된다. 다만 이 1.92°가 전체 파이프라인의 실질적 하한선 역할을 한다는 점도 읽힌다(최종 static 오차 1.73°가 이 값과 같은 자릿수).
- **정성 결과 (Figure 3, 8, 9)**: 물리 손실 없이 학습하면 생성된 궤적이 목표 움직임을 대략만 따라가고 특히 정적 정위와 원형 모션에서 눈에 띄게 흔들린다. 전체 모델은 네 가지 모션 패밀리 전반에서 GT에 더 잘 붙는다. Figure 9는 로그 에너지 포락선이 목표 역제곱 프로파일을 더 잘 따라감을 보여준다.

### 연구 의의

한마디로, **"아는 물리는 데이터로 배우게 두지 말고 손실로 넣어라"**를 공간 음향 생성에 적용해 확실한 이득을 보였다. 게다가 그 물리 prior가 (1) 학습 정규화, (2) 조건 특징 설계($1/r^2$, 단위 벡터 형태로 주입), (3) 추론 시 gradient guidance라는 세 지점에서 모두 재활용된다는 점이 설계적으로 깔끔하다. 사용성 측면에서는 자연어와 정밀 궤적 제어를 배타적 모드가 아닌 하나의 표현으로 합쳐, 사용자가 대충 말해도 되고 필요하면 숫자를 직접 고칠 수도 있게 했다. 300K 클립 규모의 동적 FOA 데이터셋도 후속 연구 자산이다.

## 한계

**논문이 스스로 밝힌 한계 (Limitations 절):**

- **단일 음원, 자유장(free-field) 가정.** 현재는 하나의 음원 궤적 제어에 한정되며, 직접 경로(direct-path) 시뮬레이션만 사용한다. 잔향(reverberation), 차폐(occlusion), 다중 경로(multi-path) 전파 같은 실내 음향 효과를 모델링하지 않는다. 다중 음원 장면과 현실적 실내 음향으로의 확장이 향후 과제다.

**명백히 드러나는 추가 한계:**

- **학습·평가가 대부분 합성 데이터.** FOA는 모노 클립을 물리 공식으로 렌더링해 만든 것이라, 물리 손실이 강제하는 관계식과 데이터 생성 규칙이 정확히 같다. 즉 "물리 prior가 잘 맞는다"는 결과에는 어느 정도 순환성이 있다. 주관 평가만이 실제 녹음 기반 조건을 썼고, 거기서 realism은 3.48(실제 4.79) 수준이다.
- **CLAP 필터로 걸러낸 단일 지배 음원 위주 데이터.** 실제 장면에 흔한 중첩 이벤트는 학습 분포에서 배제됐다.
- **baseline 재현 의존.** ImmerseDiffusion과 SonicMotion의 공식 구현이 없어 저자들이 재현한 결과와 비교했다. 재현 품질이 수치에 영향을 줄 수 있다.
- **추론 가이던스의 트레이드오프.** 공간 정확도를 올리면 FAD$_\text{CLAP}$이 나빠진다. 스케일을 어떻게 고를지는 여전히 수동 튜닝 영역이다.
- **파서가 병목.** 최상위 파서(Qwen3.5-4B)도 spatial faithfulness 3.88/5에 그친다. 즉 자연어 경로에서는 모델 자체가 완벽해도 파싱 오류가 최종 공간 정확도의 상한을 깎는다. 또 파서는 얼려 쓰므로 생성 모델과 함께 최적화되지 않는다.
- **고정된 길이·해상도.** 10초, 16 kHz, $M = 10$ 웨이포인트로 고정되어 있고 FOA도 1차(first-order)까지다. 고차 앰비소닉스(HOA)로 가면 채널 간 관계식이 훨씬 복잡해진다.
- **평가 지표의 한계.** 오디오 품질 지표를 $W$ 채널에서만 계산하므로 방향 채널의 아티팩트는 객관 지표에 잡히지 않는다.

## 우리 연구와 연결되는 점

**Spatial Audio 관점.**
이 논문의 가장 이식성 높은 부분은 모델 구조가 아니라 **미분 가능한 음향 prior**다. 인텐시티 벡터 $[\langle WX\rangle, \langle WY\rangle, \langle WZ\rangle]$와 목표 방향의 코사인 정렬, 그리고 정규화된 로그 에너지와 $1/r^2$의 MSE — 둘 다 구현이 매우 단순하고, FOA를 출력하거나 FOA에 조건을 거는 어떤 파이프라인에도 붙일 수 있다. 특히 "학습 없이 추론 시 gradient guidance로도 쓸 수 있다"는 결과는, 이미 가진 공간 오디오 생성/변환 모델을 재학습 없이 보정할 수 있다는 실용적 의미다. FOA VAE를 학습할 때 $\mathcal{L}_{\text{dir}}$을 넣어 latent 압축 단계부터 공간 구조를 보존한 설계도 참고할 만하다(재구성 각도 오차 1.92°).

평가 프로토콜도 그대로 가져다 쓸 수 있다 — DoA 각도 오차(haversine), InvSqErr/InvSqCorr, 그리고 무음 구간을 배제하는 에너지 게이트($E_k \geq 10^{-3}\max_j E_j$)는 "공간 정확도"를 정량화하려는 어떤 연구에도 필요한 도구다. 지금까지 공간 오디오 평가가 각도 오차에 편중돼 있었다면, **거리 일관성을 독립 지표로 분리**한 점이 새롭다.

**Egocentric Vision 관점.**
PhysWave의 궤적은 처음부터 **청자 상대(listener-relative)** 좌표 $(\theta(t), \phi(t), r(t))$로 정의된다. 이는 에고센트릭 비전의 카메라 중심 좌표계와 정확히 같은 프레임이다. 즉 1인칭 영상에서 추정한 물체의 방위·거리 궤적을 그대로 웨이포인트 조건으로 변환할 수 있는 구조다. 현재 PhysWave는 텍스트만 받지만, 조건 경로가 이미 "텍스트 토큰 + 웨이포인트 토큰 + 시간 토큰"으로 모듈화돼 있어 웨이포인트를 시각 추적 결과로 대체하거나, 텍스트 토큰 자리에 비주얼 토큰을 추가하는 확장이 자연스럽다. 논문이 Table 6에서 ViSAGe(영상→FOA)와 OmniAudio(360도 영상→FOA)를 비교 대상에 올려둔 것도 이 접점을 의식한 배치다. 다만 이들 영상 기반 방법에는 physics-guided 항목이 ✗로 표시되어 있다 — **영상 조건 공간 음향 생성에 물리 prior를 결합하는 자리는 아직 비어 있다.**

또한 에고센트릭 영상에서는 착용자가 움직이므로 음원의 상대 궤적이 착용자 자체 움직임(head/body motion)과 얽힌다. PhysWave가 다루는 네 모션 패밀리(정적/선형 통과/원형/접근-후퇴)는 사실 착용자가 고정 음원 주변을 돌거나 다가갈 때 생기는 상대 궤적과 같은 형태여서, 에고모션 기반 공간 음향 합성의 기초 블록으로 쓸 수 있다.

**Hand-Object Interaction 관점.**
직접적 연결은 약하지만 두 지점이 있다. 첫째, HOI에서 발생하는 접촉음(충돌, 마찰, 파지)은 **손의 3D 위치가 곧 음원 위치**다. 손 궤적 추정 결과를 웨이포인트로 변환하면, 접촉 이벤트에 물리적으로 일관된 공간 음향을 입히는 파이프라인이 된다. 특히 손은 대개 착용자 근거리(0.3~0.8 m)에 있어 $1/r^2$ 감쇠가 급격하게 변하는 영역인데, PhysWave의 샘플링 범위가 $r \geq 0.5$ m에서 시작한다는 점은 근거리 상호작용에 그대로 쓰기엔 보정이 필요함을 시사한다.

둘째, **"알려진 물리 관계를 미분 가능 손실로 학습에 주입한다"**는 메타 전략 자체가 HOI에 옮겨진다. 접촉 제약(contact constraint), 관통 방지(non-penetration), 마찰 원뿔(friction cone) 같은 HOI의 물리 법칙도 미분 가능하게 쓸 수 있고, PhysWave가 보여준 세 가지 활용 지점 — (a) 조건 특징을 물리량 형태로 설계, (b) 학습 목표에 추가, (c) 추론 시 gradient guidance로 재사용 — 이 그대로 대응된다. 특히 (c)는 HOI 생성 모델에서 "학습된 모델을 건드리지 않고 물리 위반을 사후 교정한다"는 형태로 자주 필요한 기능이다.

**공통 시사점.**
PhysWave의 "latent에서만 감독하지 말고 디코딩된 신호까지 내려가 물리를 재라"는 설계는, latent diffusion을 쓰는 모든 도메인에서 물리 제약을 걸고 싶을 때 마주치는 문제에 대한 구체적 답이다(얼린 디코더를 통과시키면 gradient가 흐르고, 배치 일부 샘플에만 적용해 비용을 줄이며, denoising SNR로 가중해 노이즈가 큰 스텝에서는 약하게 건다). Egocentric·HOI·Spatial Audio 어디서든 latent 생성 모델에 도메인 물리를 얹으려 할 때 참고할 레시피다.

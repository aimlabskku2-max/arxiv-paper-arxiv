# Residual Learning for Neural Ambisonics Encoders

**arXiv**: 2601.18322 | **주제 분류**: Spatial Audio | **출판일**: 2026-01-26 | **학회**: 프리프린트 (Comments 필드 없음)
**저자/소속**: Thomas Deppisch, Yang Gao, Manan Mittal, Benjamin Stahl, Christoph Hold, David Alon, Zamir Ben-Hur — 전원 Reality Labs Research, Meta (Deppisch는 Chalmers University of Technology, Mittal은 Stony Brook University 공동 소속)
**링크**: https://arxiv.org/abs/2601.18322

## 한 줄 요약
스마트글래스의 5채널 마이크 배열 신호를 Ambisonics로 변환할 때, 신경망이 선형 인코더를 대체하는 대신 그 출력에 더할 **보정항(residual)** 만 학습하도록 바꾸면 모든 지표에서 안정적으로 이득이 난다는 것을 실측 array transfer function 기반으로 보인 논문이다.

## 메인 그림
![Fig. 2: 제안하는 residual learning 프레임워크 — 선형 인코더와 신경망 인코더의 출력을 합산한 결과에서 손실을 계산해 신경망을 end-to-end로 학습시킨다](https://arxiv.org/html/2601.18322v1/x2.png)

입력 마이크 신호가 선형 인코더와 신경망 인코더로 **동시에** 들어가고, 두 시간영역 출력을 (처리 지연을 맞춘 뒤) 그냥 더한 것이 최종 Ambisonics 신호가 된다. 손실은 이 합쳐진 출력에서 계산되며, 신경망은 "선형 인코더가 틀린 부분"만 메우도록 학습된다.

제안 신경망 구조(Fig. 1)는 아래와 같다. 주파수별 $3\times3$ 컨볼루션 전처리 → 단일 헤드 attention → 2층 GRU → linear layer가 주파수별 인코딩 가중치를 내놓는다.

![Fig. 1: 제안한 attention-RNN 기반 신경 Ambisonics 인코더 구조](https://arxiv.org/html/2601.18322v1/x1.png)

## 선행 연구
- **Ambisonics**(소리의 방향 정보를 구면 조화 함수, spherical harmonics로 표현하는 기기 독립적 공간 음향 포맷)는 녹음·처리·재생 단계를 분리해 준다. 덕분에 같은 처리 알고리즘을 서로 다른 기기에 그대로 쓸 수 있고, 스피커 배열이든 HRTF 기반 헤드폰 바이노럴이든 재생 방식도 자유롭게 고를 수 있다.
- 기존 인코더는 **선형 최소자승(least-squares) 필터**가 표준이다. 측정된 무향실 ATF(array transfer function, 방향별 마이크 응답)와 그 방향의 구면 조화 함수 값을 맞추는 행렬을 푸는 방식이다. 머리에 쓰는 배열용으로 개선한 연구들도 여럿 있다([Gayer et al. 2025](https://arxiv.org/abs/2507.11091) 등).
- **신호 의존적(signal-dependent)** 접근은 음원의 도래 방향(DoA)을 추정하거나 직접음/잔향을 분리 처리해 한계를 넘으려 했다(parametric encoding 계열).
- 최근에는 **DNN 기반 인코딩**이 등장했다. UNet 계열(Heikkinen et al., ICASSP 2024/2025)과 가상 스피커 신호를 먼저 추정하는 2단계 설계(Qiao et al., ICASSP 2025)가 대표적이며, 모두 STFT 도메인에서 실수부/허수부를 별도 채널로 다룬다.

## 문제 제기
1. **선형 인코더의 물리적 한계.** 웨어러블에 필요한 소형 배열은 구경(aperture)이 작아 저주파 방향 분해능을 얻으려면 큰 게인이 필요하고, 그만큼 노이즈가 증폭되고 왜곡이 생긴다. 반대로 고주파에서는 공간 샘플링이 부족해 **spatial aliasing**이 발생한다.
2. **기존 신경망 연구의 비현실성.** 이상적인 무지향성 마이크와 shoebox room의 image-source 시뮬레이션만으로 평가돼, 실제 기기의 음향적 거동(머리·안경테에 의한 산란, 마이크 지향성)을 반영하지 못한다.
3. **분석의 부재.** 신경망 인코더를 SH 채널별·주파수별로 뜯어보고 선형 인코더와 나란히 비교한 연구가 없어서, 어디서 이득이 나고 어디서 손해가 나는지 알 수 없었다.

실제로 저자들이 확인해 보니 두 신경망 구조 모두 **저주파에서 선형 인코더보다 못했고**, 채널·주파수에 따라 성능이 들쭉날쭉했다.

## 연구 주제
"신경망 인코더가 선형 인코더를 **대체**해야 하는가, 아니면 **보완**해야 하는가"를 실측 스마트글래스 ATF 위에서 따진다. 그리고 in-domain / out-of-domain을 나눠 일반화 능력까지 평가한다.

## 연구 방법

### 문제 정의
평면파 분해에 따라 $M$개 마이크가 받는 음압 $p(t,f) \in \mathbb{C}^M$은 SH 도메인 평면파 밀도 계수 $a_n^m$과 배열 응답 벡터 $d_n^m$로 이렇게 쓸 수 있다.

$$p(t,f) = \sum_{n=0}^{\infty} \sum_{m=-n}^{n} d_{n}^{m}(f)\, a_{n}^{m}(t,f)$$

인코더가 하는 일은 유한 차수 $n \in [0,N]$까지의 계수 $\hat{a} \in \mathbb{C}^{(N+1)^2}$를 인코딩 행렬 $E$로 복원하는 것이다.

$$\hat{\boldsymbol{a}}(t,f) = \boldsymbol{E}(t,f)\,\boldsymbol{p}(t,f)$$

선형 인코더는 $E$를 최소자승 해로 한 번 구해 고정하고, 신경망은 $p \to a$의 비선형 매핑을 지도학습으로 배운다.

### 핵심 아이디어: Residual Learning
신경망 출력이 최종 답이 아니라 **선형 인코더 출력에 더해지는 보정**이 되도록 구조를 바꾼다. 두 경로를 병렬로 돌리고 시간영역 출력을 단순 합산하며, 지연은 맞춰 준다. 손실은 합쳐진 결과에서 계산해 end-to-end로 학습한다. SH 성분별 최적 합산 가중치를 학습시켜 봤지만 단순 합산 대비 이득이 없었다.

### 비교한 두 신경망 구조
| 구조 | 설계 | 파라미터 |
|---|---|---|
| UNet [Heikkinen et al.] | 주파수 bin별 2D 컨볼루션 전처리 + skip connection UNet, **복소수** 인코딩 행렬 | 8.1 M |
| AmbiNet (제안) | 주파수별 $3\times3$ 컨볼루션 → 단일 헤드 attention(인접 $B=5$ 주파수 bin + 전 채널 + 실/허부를 임베딩 차원으로) → 채널 합산 → 2층 단방향 GRU($H=512$) → linear layer, **실수** 가중치 | 7.9 M |

복소 가중치로 확장해 봤으나 개선은 미미하고 연산량만 크게 늘어 실수 버전만 사용했다.

### 손실 함수
STFT 도메인 MAE와 **SH coherence loss**를 결합한다. coherence는 SH 지향 패턴(directivity pattern)을 얼마나 정확히 재현하는지를 재는 값으로,

$$C_n^m(f) = 1 - \frac{\left|\sum_{t=1}^T a_n^m(t,f)^{*}\, \hat{a}_n^m(t,f)\right|^2}{\sum_{t'} |a_n^m(t',f)|^2 \sum_{t''} |\hat{a}_n^m(t'',f)|^2}$$

이고, 전체 손실은

$$L = \frac{1}{F} \sum_{f=1}^{F} \left( \alpha\, \mathrm{MAE}(f) + \frac{\beta(f)}{N+1} \sum_{n=0}^{N} \sum_{m=-n}^{n} \frac{1}{2n+1} C_{n}^{m}(f) \right)$$

로 정의된다. $\alpha=10$, $\beta(f)$는 주파수에 반비례해 옥타브 밴드마다 대략 균등한 가중이 걸리도록 했고(인간 청각과 유사), $1/(2n+1)$은 차수별 기여를 정규화한다. 전환 주파수를 명시하지 않아 배열별 튜닝 없이 여러 구성에 그대로 쓸 수 있다는 점이 UNet 원논문 손실과의 차이다.

### 데이터
- **In-domain**: pyroomacoustics로 shoebox 룸 80,000개(치수 $3\times3\times2$ m ~ $10\times10\times5$ m, 흡음률 0.2~0.95, image source order 40, 48 kHz) 시뮬레이션. 방마다 1~5개 음원. **실측 스마트글래스 5마이크 배열 ATF**(코 받침 1개 + 양쪽 템플 2개씩)를 조밀한 방향 그리드로 적용. 정답은 이상적 SH 리시버로 생성. 오디오는 학습에 DNS(음성 60%) + FUSS(비음성 40%), 테스트에 EARS + FUSS. 총 178시간, 80/10/10 분할.
- **Out-of-domain**: Treble 하이브리드 시뮬레이터(3.2 kHz 이하 파동 기반 + 그 위 레이 트레이싱, 주파수 의존 흡음, 가구 산란 포함)로 회의실·거실·침실·식당·아파트 등 20개 방, 방당 15개 수신 위치. 300 scene, 40분.
- SH 최대 차수 $N=1$ (마이크 5개로 선형 인코딩이 가능한 최대). 선형 인코더는 diffuse field equalization + 20 dB 게인 제한 적용. 250 epoch, 1초 세그먼트, batch 128, STFT 프레임 768 샘플(50% overlap), Adam(lr $10^{-3}$, plateau 시 0.3배 감쇠).

### 평가 지표
coherence(↑), mean magnitude spectral error(dB, ↓), SI-SDR(dB, ↑), SPME(spatial power map error, 구면상 $Q=1296$ 방향의 에너지 분포 오차, dB, ↓).

## 실험 결과 / 연구 의의

| 모델 | In: Coh.↑ | In: Mag.Err(dB)↓ | In: SI-SDR(dB)↑ | In: SPME(dB)↓ | Out: Coh.↑ | Out: Mag.Err(dB)↓ | Out: SI-SDR(dB)↑ | Out: SPME(dB)↓ |
|---|---|---|---|---|---|---|---|---|
| Linear Enc. | 0.44 | 11.0 | -7.4 | -0.4 | 0.39 | 13.3 | -9.7 | 9.5 |
| UNet | 0.49 | 11.0 | -6.8 | 8.4 | 0.37 | 17.9 | -11.4 | 9.8 |
| UResNet | **0.54** | **8.5** | -4.0 | -3.2 | **0.40** | **13.1** | -7.6 | 10.4 |
| UNet (mod.) | 0.50 | 9.4 | -0.2 | 7.2 | 0.32 | 15.3 | -5.4 | 8.7 |
| UResNet (mod.) | 0.53 | 8.7 | **1.0** | -2.4 | **0.40** | 14.2 | **-4.0** | **6.5** |
| AmbiNet | 0.49 | 10.4 | 0.0 | 2.2 | 0.36 | 13.6 | -5.0 | **6.5** |
| AmbiResNet | 0.52 | 8.6 | 0.2 | **-4.4** | **0.40** | 13.8 | -4.9 | 8.2 |

(In = in-domain, Out = out-of-domain. 굵게 표시한 값이 해당 지표 최고치.)

핵심 관찰:
- **Residual 없이는 신경망이 선형 인코더를 일관되게 이기지 못한다.** 단독 신경망(UNet, UNet mod., AmbiNet)은 in-domain SPME에서 선형(-0.4 dB)보다 크게 나쁘고(2.2~8.4 dB), out-of-domain에서는 coherence·magnitude error가 선형보다 떨어지는 경우가 잦다.
- **Residual을 붙이면 in-domain 전 지표에서 일관되게 개선된다.** coherence 0.44 → 0.52~0.54, magnitude error 11.0 → 8.5~8.7 dB, SI-SDR -7.4 → 최대 1.0 dB, SPME는 모든 residual 모델이 선형 baseline 아래로 내려간다(최저 -4.4 dB, AmbiResNet).
- **Out-of-domain에서는 이득이 작아진다.** coherence는 0.39 → 0.40으로 소폭, SI-SDR은 -9.7 → -4.0 dB로 유의미하게 개선되지만 SPME는 UResNet에서 오히려 악화(10.4 dB)된다. 즉 residual은 일반화 안정성을 높여 주지만 현실적 학습 데이터의 필요성을 없애 주지는 못한다.
- **채널별 분석(Fig. 3).** 단독 신경망은 특정 대역·채널에서만 선형을 넘는다(예: 400 Hz 이하의 $\hat{a}_0^0$). 반대로 100~500 Hz의 $\hat{a}_1^0$에서는 선형이 우세하다. Residual 변형은 **모든 채널·모든 주파수에서 선형 이상**을 유지한다. 마이크가 머리 앞/옆에만 있는 기하 때문에 위/아래 성분 $\hat{a}_1^0$와 앞/뒤 성분 $\hat{a}_1^1$는 선형·신경망 모두 성능이 낮다.
- 비공식 청취에서 residual 네트워크의 소리는 선형 인코더와 대체로 비슷했고, 정식 청감 실험을 정당화할 만한 차이는 아니었다고 밝힌다(바이노럴 예제는 온라인 공개).

**의의**: 신경망을 "대체재"가 아니라 "보정기"로 두는 단순한 재배치만으로 학습 기반 공간 음향 인코딩의 고질적 불안정성(도메인 이동 시 baseline보다 나빠지는 문제)을 상당 부분 해소했다. 구조에 무관하게(UNet이든 attention-RNN이든) 통하는 결론이라는 점, 그리고 실측 스마트글래스 ATF 위에서 검증했다는 점이 기여다.

## 한계
- **고주파 방향 정확도는 여전히 미해결.** coherence가 고주파로 갈수록 모든 구성에서 떨어지며, 저자들 스스로 "어떤 접근도 희소한 공간 샘플링에서 오는 오차를 실질적으로 극복하지 못한다"고 명시한다. 비선형 신경망도 spatial aliasing을 못 푼다.
- **Out-of-domain 이득이 미미하다.** in-domain 대비 개선 폭이 확연히 작고, 일부 지표(UResNet의 SPME)는 오히려 악화된다. 현실적인 학습 데이터가 여전히 필요하다는 뜻.
- **지각적 이득이 확인되지 않았다.** 비공식 청취 결과 선형 인코더와 큰 차이가 없어 정식 청감 실험을 하지 않았다. 지표 개선이 사람이 듣는 품질로 이어지는지는 미검증.
- **1차 Ambisonics($N=1$), 마이크 5개, 단일 배열 기하**에 한정된 결과다. 다른 기기·고차 Ambisonics로의 확장은 다루지 않았다.
- 저자들이 제시한 future work: 마이크 수가 제한된 상황에서의 **directional super-resolution** 네트워크 설계, 개별 음원을 식별하는 parametric encoding과의 결합(residual 프레임워크는 여기에도 유용할 수 있다고 언급).

## 우리 연구와 연결되는 점
> 아래는 논문에 명시된 내용이 아니라 egocentric vision / hand-object interaction / spatial audio 관점에서의 잠재적 연결 지점이다.

- **Egocentric 센싱 하드웨어가 곧 이 논문의 대상이다.** 스마트글래스 템플과 코 받침에 박힌 5개 마이크는 egocentric video를 찍는 바로 그 기기의 오디오 채널이다. Aria류 데이터셋으로 egocentric audio-visual 연구를 한다면, 원시 다채널 신호를 Ambisonics로 올리는 단계의 품질이 이후 모든 공간 추론의 상한을 결정한다. 이 논문은 그 상한이 어디쯤인지(1차 SH, 고주파에서 방향 정확도 붕괴) 정량적으로 알려 준다.
- **머리 기하가 만드는 비등방적 오차.** 위/아래($\hat{a}_1^0$)와 앞/뒤($\hat{a}_1^1$) 성분이 특히 약하다는 발견은 egocentric 관점에서 중요하다. 착용자 시야 밖(뒤쪽)이나 손이 놓인 아래쪽 방향의 음원 정위가 구조적으로 부정확하다는 뜻이므로, 시야 밖 사건을 소리로 잡으려는 태스크는 이 편향을 전제해야 한다. hand-object interaction 소리(테이블 위 물체 조작음)는 대체로 아래쪽에서 오므로 취약 방향과 겹친다.
- **"학습 모델은 baseline을 보정하게 하라"는 설계 교훈.** 도메인 이동에 취약한 신경망을 견고한 물리 기반 해에 얹는 residual 구성은 spatial audio 인코딩 밖에서도 재사용 가능한 패턴이다. egocentric 환경은 조명·장면·착용자마다 분포가 흔들리므로 특히 잘 맞을 법하다.
- **평가 지표 참고.** coherence, SPME 같은 방향성 중심 지표는 SI-SDR 같은 파형 지표가 놓치는 공간 정보 손실을 잡아낸다. spatial audio를 다루는 downstream 태스크의 전처리 품질을 진단할 때 그대로 가져다 쓸 수 있다.

# Visually-Guided Spatial Audio Generation for $360^\circ$ In-the-Wild Speech Scenes

**arXiv**: 2608.24579 | **주제 분류**: Spatial Audio | **출판일**: 2026-08-25 | **학회**: INTERSPEECH 2026
**저자/소속**: Qingyu Luo, Peng Zhang, Wenwu Wang, Philip J. B. Jackson — 영국 서리대학교(University of Surrey) CVSSP(Centre for Vision, Speech and Signal Processing)
**링크**: https://arxiv.org/abs/2608.24579

## 한 줄 요약
360도 영상과 무지향성(omnidirectional) 오디오 한 채널만 주어졌을 때, 영상 속 화자의 위치를 시각적으로 찾아 방향 정보를 담은 1차 앰비소닉스(FOA, First-Order Ambisonics) 음향을 복원하는 "국소화기-렌더러(Localizer-Renderer)" 프레임워크와, 이를 위한 실제 유튜브 기반 데이터셋 YT-SPEECH를 제안한 연구다.

## 메인 그림
![프레임워크 개요](https://arxiv.org/html/2608.24579v1/net_v12.png)

논문 Figure 2. 제안하는 Localizer-Renderer 파이프라인 전체 구조를 보여준다. 왼쪽에서 360도 영상(ERP 프레임)과 무지향성 오디오 $W$ 채널이 입력되고, Localizer(오디오-비주얼 분할 백본)가 화자 위치를 담은 공간 히트맵(spatial heatmap)을 만든다. 이 히트맵이 조건(condition)으로 들어가 오른쪽 Renderer(복소 영역 U-Net)가 빠져 있던 방향 성분 $(Y, Z, X)$를 복원해 완전한 FOA 신호를 만든다.

## 선행 연구
- **음성 공간화(speech spatialization)**: 대부분 모노(mono) 음성을 바이노럴(binaural)이나 스테레오로 렌더링하는 데 집중했고, 일부는 기하 정보나 텍스트를 추가 조건으로 사용했다. 그러나 바이노럴 출력은 청취자의 머리 방향에 고정되어 있다는 한계가 있다.
- **FOA(1차 앰비소닉스) 표현**: FOA는 장면 기반(scene-based) 표현이라 회전·재디코딩이 자유롭고 헤드 트래킹 바이노럴로도 변환 가능하다. 하지만 기존 FOA 음성 데이터셋은 대부분 시뮬레이션으로 만들어졌고 파노라마 영상과 짝지어진 경우가 드물다.
- **360도 영상→FOA 생성**: 크게 두 갈래로 나뉜다. (1) 명시적 공간 복원(explicit spatial reconstruction) — SpatialAudioGen(SAG)과 그 확장, Rana 등의 제로샷 방향 우선(direction-first) 파이프라인. (2) 종단간(end-to-end) 생성 — OmniAudio, ViSAGe처럼 대규모 데이터로 영상-음향을 직접 학습하되 정확한 공간 복원보다 의미적(semantic) 일관성을 강조한다.
- **오디오-비주얼 분할(AVS, Audio-Visual Segmentation)**: 소리를 내는 물체를 픽셀 단위로 찾아내는 기법으로, 본 연구는 이를 방향 복원의 공간 사전(prior)으로 재활용한다.

## 문제 제기
- 몰입형 360도 미디어에서 공간 음향은 핵심 요소지만, 실제 환경의 **음성 중심(speech-dominant) 장면**에서 고품질 공간 음향을 직접 녹음·확보하기는 여전히 어렵다.
- 인터뷰·대화·해설처럼 음성이 주가 되는 360도 영상이 매우 흔한데, 전경(前景) 음성의 위치 오류는 확산성 배경음보다 훨씬 두드러지게 들린다.
- 기존 데이터셋은 포맷(대부분 바이노럴), 규모, 시각적 접지(visual grounding) 세 측면에서 모두 부족해, 실제 환경의 "시각 유도 FOA 음성 공간화" 연구 자체가 제약을 받아 왔다.
- 자유로운 파노라마 영상에서의 신뢰할 만한 위치 추정도 어렵다. 기존 음원 위치 추정 모델은 거친 공간 격자나 이산적 도래각(DOA, Direction of Arrival) 추정에 의존하고, 화자 중심 파이프라인은 얼굴 검출·활성 화자 연결을 단계적으로 쌓아 실제 환경 일반화가 약하다.

## 연구 주제
정렬된 360도 영상 $\mathbf{V}$와 무지향성 FOA 채널 $W$가 주어졌을 때, 빠져 있는 방향 성분 $(Y, Z, X)$를 복소 STFT(short-time Fourier transform, 단시간 푸리에 변환) 영역에서 복원해 공간적으로 일관된 FOA 음향을 얻는 것이 목표다. 즉 명시적 공간 복원 계열의 "방향 우선" 전략을 따르되, 음성이 지배적인 실제 360도 장면에 특화한다.

## 연구 방법
**데이터셋 YT-SPEECH**: 유튜브의 FOA 음향 포함 360도 영상에서 다단계 필터링으로 수집했다. 채널 에너지 패턴으로 올바른 FOA 포맷만 남기고, 화자 분할(speaker diarization)과 Whisper ASR로 음성 구간을 검증하며, AudioSet 분류기로 음악·노래 위주 클립을 제거한다. YOLOv8-nano로 화면 속 인물을 검출해 화자가 실제로 보이는 구간만 남기고, 오디오-비주얼 정합 점수와 수동 검수로 마무리한다. 최종적으로 24 kHz, 5초 클립으로 구성된 **8.9시간**(197개 원본 영상) 규모이며, 영상 ID 기준으로 학습/검증/평가를 나눠 콘텐츠 누수를 막았다.

**Localizer(국소화기)**: AVS 백본(오디오 인코더 + 비디오 인코더 + 교차 모달 상호작용)을 얼려 놓고, 원래의 분할 마스크 헤드를 "공간 사전 헤드(Spatial Prior Head)"로 바꿔 미세조정한다. 등장방형 투영(ERP, Equirectangular Projection, 2:1 비율) 영상에 순환 패딩(circular padding)을 적용해 좌우가 이어지는 파노라마 연속성을 보존하고, 밀집(dense) 공간 활성화를 만든 뒤 정규화해 합이 1이 되는 $7 \times 14$ 공간 확률 분포 $\mathbf{P}_t$를 얻는다.

**Renderer(렌더러)**: 복소 STFT 영역에서 동작하는 U-Net으로, $W$의 스펙트럼을 보존한 채 방향별 복소 마스크 $\mathbf{M}_i$를 예측해 $\hat{\Phi}_i = \mathbf{M}_i \odot \Phi_W$로 각 방향 성분을 만든다. 위상(phase)까지 다루므로 채널 간 결합성(cross-channel coherence)이 유지된다.

**신뢰도 기반 게이팅(confidence-based gating)**: 공간 사전이 확산성·모호한 순간에는 부정확할 수 있으므로, 사전의 집중도(peak 기반)와 불확실성(entropy 기반)을 곱해 신뢰도 $g(t) \in [0,1]$를 계산한다. 이를 게이팅된 FiLM(feature-wise linear modulation) $\tilde{\mathbf{h}}_\ell = \mathbf{h}_\ell \odot (1 + g(t)\boldsymbol{\gamma}_\ell) + g(t)\boldsymbol{\beta}_\ell$로 반영해, 사전이 뚜렷할 때만 시각 유도 조건을 강하게 적용하고 애매할 때는 오디오 근거에 무게를 둔다.

**학습**: 손실은 신뢰도 가중치 $w(t) = \alpha + (1-\alpha)g(t)$로 가중한 다중 해상도 STFT 손실 $\mathcal{L}_\mathrm{MRS}$, 크기(magnitude) 손실 $\mathcal{L}_\mathrm{mag}$, 파형 $\ell_2$ 손실의 합이다($\lambda_1{=}1, \lambda_2{=}0.1, \lambda_3{=}0.2, \alpha{=}0.2$). 먼저 대규모 360도 오디오-비주얼 데이터셋 Sphere360으로 Renderer를 사전학습한 뒤, YT-SPEECH에서 요(yaw) 회전·수평 뒤집기 증강을 적용해 전체 파이프라인을 미세조정한다.

## 실험 결과 / 연구 의의
평가는 복원 충실도(ℓ2, $\mathcal{L}_\mathrm{mag}$, $\mathcal{L}_\mathrm{phs}$, $\mathcal{L}_\mathrm{MRS}$), 공간 정확도(DOA 기반 방위각 $\Delta_\mathrm{abs}\theta$·고도각 $\Delta_\mathrm{abs}\phi$·전체 각오차 $\Delta_\mathrm{ang}$), 음성 품질(PESQ, 그리고 청취자 9명이 매긴 주관 지표 MOS-Q·MOS-P)로 이뤄졌다.

**YT-SPEECH 벤치마크(Table 2, 주요 지표 발췌, 화살표는 방향; ↓ 낮을수록, ↑ 높을수록 좋음)**

| 모델 | ℓ2(×10³)↓ | Δang↓ | PESQ↑ | MOS-P↑ |
|---|---|---|---|---|
| NoVideo-Renderer (영상 미사용) | 1.59 | 0.73 | 2.50 | 2.28 |
| VidEnc-Renderer (영상 인코더 특징 조건) | 1.95 | 0.66 | 1.78 | 3.02 |
| FrozenLoc-Renderer (Localizer 동결) | 2.19 | 1.04 | 1.41 | 2.34 |
| Localizer-AmbiEnc (해석적 DOA 인코딩) | 1.55 | 0.83 | 3.35 | 2.97 |
| Ours (NoPT, 사전학습 제거) | 1.71 | 0.92 | 1.48 | 2.90 |
| **Ours (전체 모델)** | **1.15** | **0.64** | **3.42** | **3.16** |

전체 모델이 복원 오차 ℓ2와 각오차 $\Delta_\mathrm{ang}$에서 가장 낮고, PESQ와 MOS-P에서 가장 높다. Localizer를 얼리면 공간 지표(특히 고도각·전체 각오차)가 크게 나빠져 적응(fine-tuning)의 필요성이 드러난다. 해석적 DOA 렌더링(Localizer-AmbiEnc)은 크기·MOS-Q는 좋지만 단일 peak 방향에만 의존해 공간 오차가 크다. 대규모 사전학습을 빼면(NoPT) 복원·지각 품질이 함께 떨어진다.

**SAG 프로토콜 호환 비교(Table 3, STFT·ENV 거리, 낮을수록 좋음)**

| 데이터셋 | SAG (STFT / ENV) | Ours (STFT / ENV) |
|---|---|---|
| YT-ALL | 2.78 / 2.92 | 2.91 / 2.99 |
| YT-MUSIC | 4.46 / 3.77 | 3.38 / 3.17 |
| YT-CLEAN | 1.58 / 1.80 | 0.91 / 1.78 |
| YT-SPEECH | 1.14 / 2.18 | 0.85 / 1.71 |

음원이 시각적으로 뚜렷이 위치하는 YT-CLEAN·YT-SPEECH에서 가장 일관된 향상을 보이며, 여러 음원이 섞인 YT-MUSIC에서도 SAG를 앞선다. 다만 음성 외 콘텐츠가 다양한 YT-ALL에서는 격차가 작아, 음성 특화 사전의 이점이 덜 두드러진다. 정성 분석(Figure 3)에서도 야외·집단 대화 장면에서는 선명하고 잘 정렬된 활성화를 내지만, 시끄러운 배경에서는 잘못된 반응이 생겨 잡음이 주된 실패 원인으로 지목된다.

의의는 (1) 실제 환경 음성 중심 360도 영상-FOA 데이터셋 YT-SPEECH를 처음 제시했고, (2) 시각 사전을 신뢰도에 따라 조절해 복소 영역에서 위상까지 일관되게 복원하는 방향 우선 프레임워크를 제안해, 복원·공간·지각 품질 전반에서 개선을 보였다는 점이다.

## 한계
- 수집·정제한 데이터셋이 8.9시간으로 규모가 작다.
- 음원이 겹치는(overlapping sources) 상황이나 음향적으로 복잡한 장면에서 안정성이 떨어진다.
- 잡음이 많은 배경에서는 잘못된 위치 활성화가 생겨 국소화 일관성이 낮아진다.
- 향후 과제로 제어 가능한 음원 중첩·정답 라벨을 갖춘 합성/혼합 데이터, 개선된 증강 전략, 더 폭넓은 지각 평가를 제시한다.

## 우리 연구와 연결되는 점
- **공간 음향 생성 관점**: 무지향성 한 채널에서 방향 FOA 성분을 복원하는 문제 설정과, 복소 STFT 영역에서 위상까지 다루는 마스킹 방식($\hat{\Phi}_i = \mathbf{M}_i \odot \Phi_W$)은 앰비소닉스 기반 공간 오디오 합성 연구에 바로 참고할 수 있다. 단일 peak DOA 기반 해석적 렌더링과 학습형 렌더링의 절충 논의도 설계 지침이 된다.
- **멀티모달 오디오-비주얼 정합 관점**: AVS(오디오-비주얼 분할) 백본을 위치 추정용 공간 사전으로 재활용하고, 사전의 집중도·엔트로피로 신뢰도를 산출해 게이팅된 FiLM으로 반영하는 구조는, 모달리티 신뢰도에 따라 조건을 동적으로 조절하는 일반적 멀티모달 융합 기법으로 확장 가능하다.
- **데이터셋·실환경 일반화 관점**: 다단계 필터링(포맷 검증→화자 분할·ASR→인물 검출→오디오-비주얼 정합·수동 검수)으로 웹 크롤링 데이터를 정제하는 파이프라인은, in-the-wild 멀티모달 데이터 구축과 ERP 특성을 살린 순환 패딩·요 회전 증강 같은 360도 도메인 처리 노하우를 제공한다.

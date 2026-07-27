# ViSAudio: End-to-End Video-Driven Binaural Spatial Audio Generation

**arXiv**: 2512.03036 | **주제 분류**: Spatial Audio | **출판일**: 2025-12-02 | **학회**: 프리프린트 (arXiv, cs.CV)
**저자/소속**: Mengchen Zhang(Zhejiang University, Shanghai AI Laboratory), Qi Chen(Shanghai Jiao Tong University, Shanghai Innovation Institute), Tong Wu(Stanford University), Zihan Liu(Beihang University, Shanghai AI Laboratory), Dahua Lin(Shanghai AI Laboratory, The Chinese University of Hong Kong)
**링크**: https://arxiv.org/abs/2512.03036

## 한 줄 요약

무음 영상만 보고 곧바로 좌우 두 귀에 맞는 입체 음향(binaural spatial audio, 두 귀로 듣는 것처럼 방향감이 있는 소리)을 만들어 내는 최초의 end-to-end 프레임워크로, 기존의 "먼저 모노 소리를 만들고 나중에 공간화하는" 2단계 방식이 겪던 오차 누적과 시공간 불일치 문제를 해결한다.

## 메인 그림

(대표 이미지 URL 확보 실패 — arXiv HTML의 실제 `<img>` 경로를 신뢰성 있게 확인할 수 없어 링크 대신 텍스트로 서술한다.)

Figure 1 개요: (왼쪽) BiAudio 데이터셋은 360도 영상과 FOA(First-Order Ambisonics, 1차 앰비소닉스; 3D 음장을 4채널로 기록한 포맷) 오디오를 다양한 카메라 회전 궤적을 적용해 일반 시야(perspective) 영상과 바이노럴 오디오 쌍으로 변환한다. (가운데) end-to-end 파이프라인은 conditional flow matching과 dual-branch 생성 구조에 conditional spacetime module을 결합해 멀티모달 입력으로부터 공간감 있는 바이노럴 오디오를 만든다. (오른쪽) 생성 예시. 파도가 왼쪽에서 부서지는 장면에서는 왼쪽 채널이 더 크게 재생되고, 카메라가 오른쪽으로 회전하면 마림바 소리가 왼쪽으로 이동해 왼쪽 채널 진폭이 커지는 등 시점 변화에 동적으로 적응한다.

## 선행 연구

- **Video-to-Audio(V2A) 생성**: 초기에는 SpecVQGAN 같은 auto-regressive 모델이 개방형 도메인 V2A를 열었고, 이후 diffusion(Diff-Foley 등)과 flow matching(Frieren, MMAudio 등) 기반 모델이 발전을 이끌었다. 다만 이들은 대부분 **모노(mono) 오디오** 생성에 집중했다.
- **영상 기반 공간 음향 생성**: 크게 두 갈래다. (1) 영상에서 음원을 찾아 추적해 공간 음향을 합성하는 방식, (2) UNet 계열 구조로 모노 오디오에서 좌우 바이노럴 채널을 직접 예측하는 방식. 둘 다 **미리 만들어진 모노 오디오에 의존하는 2단계 파이프라인**이다.
- **최근의 end-to-end 공간 음향**: OmniAudio는 360도 영상에서 FOA를 생성하고, ViSAGe는 FoV(Field-of-View, 일반 시야각) 영상에서 카메라 방향을 조건으로 FOA를 생성한다. 그러나 이들은 360도 입력이나 카메라 방향 같은 추가 파라미터가 필요하다.

주요 참고 연구: [MMAudio](https://arxiv.org/abs/2412.15322), [ViSAGe](https://arxiv.org/abs/2504.04728)

## 문제 제기

- 기존 바이노럴 생성은 "모노 생성 → 별도 공간화"의 **2단계 방식**에 묶여 있어, 1단계 출력 품질에 성능이 좌우되고 **오차가 누적**되며 영상과의 시공간 정합이 어긋난다.
- 공간화 단계는 대개 **화면에 보이는 음원(visible)만** 고려하고, 화면 밖 소리(off-screen)나 위치를 특정할 수 없는 환경 소음(environmental noise)을 무시한다.
- end-to-end 방식이 등장했지만 360도 영상이나 카메라 방향에 의존해 **일반 시야(perspective) 영상에서 곧바로 공간 단서를 추출하는 방향은 거의 탐구되지 않았다**.
- 결정적으로 **데이터 희소성**: 기존 실세계 영상-바이노럴 데이터셋은 규모가 작고, 거리나 음악 같은 좁은 환경에 치우쳐 있으며, 대부분 카메라 시점이 고정되어 있다.

## 연구 주제

**무음 영상(과 선택적 텍스트)으로부터 직접, end-to-end로 바이노럴 공간 음향을 생성하는 과제**를 새롭게 정의한다. 생성된 소리는 공간적 몰입감을 주면서도 영상과 시공간적으로 일치해야 하고, 시점 변화, 음원의 움직임, 다양한 음향 환경에 적응해야 한다.

## 연구 방법

**1) BiAudio 데이터셋 구축 (반자동 파이프라인)**
- Sphere360 데이터셋의 FOA 오디오와 360도 영상을 재료로, 360도 영상을 90도 시야로 투영하고 FOA를 HRIR(Head-Related Impulse Response, 머리 모양에 따른 소리 전달 특성) 컨볼루션으로 바이노럴 신호로 렌더링한다.
- **공간 단서 강화(Spatial Cue Enhancement)**: 구면 조화 분해(spherical harmonics decomposition)로 음향 에너지가 최대인 방향을 계산해 카메라 초기 방향을 주요 음원 쪽으로 맞추고, 무작위 드리프트를 준 **다양한 카메라 회전 궤적**을 생성한다. 좌우 채널 차이가 0.01 미만인(공간감이 약한) 샘플은 버린다.
- **캡션 주석(2단계)**: Qwen2.5-Omni로 화면 안 소리와 배경음을 모두 서술한 뒤, Qwen3-Instruct-2507로 "Visible sound: <...>, Invisible sound: <...>" 형식의 간결한 캡션으로 정제한다.
- 규모: 약 97,000쌍, 각 8초, 총 215시간. 실세계 개방형 도메인, 카메라가 움직이는(Moving) 최초·최대 규모의 FoV 바이노럴 데이터셋이다.

**2) ViSAudio 모델** — 사전학습된 MMAudio를 파인튜닝해 강한 오디오 생성 능력을 물려받는다.
- **Conditional Flow Matching(CFM)**: 노이즈 $x_0$를 오디오 latent $x_1$로 점진 변환하는 속도장(velocity field)을 학습한다. 경로는 최적수송 보간 $x_t = t x_1 + (1-t) x_0$, 속도장은 $u = x_1 - x_0$. 학습 목표는 좌/우 채널로 확장되어 $\sum_{a \in \{l,r\}} \mathbb{E}\,\|v_\theta^a(t,\mathcal{C},x_t^a) - (x_1^a - x_0^a)\|^2$ 을 최소화한다.
- **Dual-Branch Audio Generation**: 스테레오 VAE가 공간 정보를 뭉개는 문제를 피하기 위해, 좌/우 채널의 latent $x_l, x_r$을 **서로 상관된 두 표현**으로 학습한다. $N_1$개의 Multimodal Joint Transformer Block에서 두 채널을 순차 갱신해 시간·의미 일관성을 유지하고, $N_2$개의 Single-Modal Branch Transformer Block(FLUX 스타일)에서 채널별 공간·시간 디테일을 다듬는다.
- **Conditional Spacetime Module**: 공간적으로 튜닝한 Perception Encoder로 좌/우 각각의 위치 임베딩($\mathbf{E}^l, \mathbf{E}^r$)을 활용해 정밀한 공간 특징 $F_{pe}$를 얻고, 이를 Synchformer 기반 동기화 특징 $F_{sync}$ 및 전역 컨디셔닝과 결합해 전역 시공간 특징 $F_{sp}$를 만든 뒤 adaLN으로 branch에 주입한다. 이로써 채널 일관성과 공간적 구별성을 동시에 확보한다.
- 특징 추출: CLIP(텍스트·시각 의미), Synchformer(사운드 이벤트 타이밍), Perception Encoder(공간 위치).

## 실험 결과 / 연구 의의

- 평가: In-distribution(BiAudio, MUSIC-21)과 Out-of-distribution(FAIR-Play). 지표는 분포 유사도 FD(VGGish/PANN)·KL(PANN), 시청각 동기 DeSync, 의미 정합 IB-Score. 비교군은 ThinkSound, AudioX(둘 다 공간 정보를 무시하는 스테레오 V2A), ViSAGe, See2Sound.
- **모든 데이터셋·모든 지표에서 SOTA**. BiAudio 테스트셋 주요 수치는 아래와 같다(↓는 낮을수록, ↑는 높을수록 좋음).

| Method | FD_VGG^avg ↓ | KL_PANN^avg ↓ | DeSync ↓ | IB-Score ↑ |
|---|---|---|---|---|
| ThinkSound | 5.949 | 2.480 | 0.903 | 0.191 |
| AudioX | 3.811 | 2.165 | 1.157 | 0.235 |
| ViSAGe | 14.432 | 3.483 | 1.159 | 0.123 |
| See2Sound | 9.904 | 3.427 | 1.244 | 0.088 |
| ViSAudio (Ours) | 2.479 | 1.360 | 0.788 | 0.299 |

- **주관 평가(User Study, MOS 1~5, 전문가 12명)**: 5개 항목 모두에서 최고. Spatial Impression 4.133, Spatial Consistency 4.100, Temporal Alignment 4.275, Semantic Alignment 4.292, Audio Realism 4.158로 baseline을 크게 앞선다.

| Method | Spatial Impression ↑ | Spatial Consistency ↑ | Temporal Align. ↑ | Semantic Align. ↑ | Audio Realism ↑ |
|---|---|---|---|---|---|
| ThinkSound | 3.250 | 2.875 | 3.483 | 3.400 | 3.067 |
| AudioX | 3.050 | 2.792 | 2.867 | 3.367 | 3.258 |
| ViSAGe | 1.658 | 1.517 | 1.700 | 1.725 | 1.492 |
| See2Sound | 2.033 | 1.517 | 1.742 | 1.725 | 1.650 |
| ViSAudio (Ours) | 4.133 | 4.100 | 4.275 | 4.292 | 4.158 |

- **Ablation(BiAudio)**: Pretrained(모노 복제) → Dual-Branch 추가 → Spacetime Module 추가 순으로 개선. Dual-Branch가 바이노럴 분포 학습으로 공간 생성 능력을 크게 끌어올리고(FD 4.482→2.803, U-SI 2.775→4.017), Spacetime Module은 시간 정합을 약간 희생하는 대신 공간 지각을 더 강화(U-SC 3.658→4.233, +0.575)한다.

| Model | FD_VGG^avg ↓ | DeSync ↓ | IB-S ↑ | U-SI ↑ | U-SC ↑ |
|---|---|---|---|---|---|
| Pretrained | 4.482 | 0.793 | 0.285 | 2.775 | 2.817 |
| w/ Dual only | 2.803 | 0.766 | 0.289 | 4.017 | 3.658 |
| Dual+Spt | 2.479 | 0.788 | 0.299 | 4.333 | 4.233 |

- 의의: 학습에 쓰지 않은 FAIR-Play에서도 우수해 **일반화 능력**을 입증했고, 2단계 방식을 우회한 end-to-end 시청각-공간음향 생성의 길을 열었다.

## 한계

- 현재 **짧은 클립(8초)**만 처리해 장기 시간 의존성과 복잡한 음향 이벤트를 담기 어렵다. 향후 더 긴 시퀀스로 확장 예정.
- BiAudio가 실세계 녹음 기반이라 오디오의 **배경 잡음이 생성 결과에 아티팩트**를 유발할 수 있다.
- 출력은 바이노럴 2채널에 한정되며, 향후 FOA 같은 **다채널 오디오 직접 생성**으로 확장을 계획.

## 우리 연구와 연결되는 점

- **모노를 넘어선 공간 음향 생성**: 시점 변화·음원 이동을 반영하는 좌우 채널 차이를 end-to-end로 학습하는 설계는, 시청각 공간 추론(audio-visual spatial reasoning)이나 몰입형 콘텐츠 생성 연구에서 공간 단서를 직접 다루려는 방향과 맞닿아 있다.
- **데이터 구축 파이프라인**: FOA→바이노럴 렌더링(HRIR), 구면 조화 분해로 음원 방향 추정, 카메라 회전 궤적 다양화, 그리고 visible/invisible 소리를 구분하는 캡션 주석은 공간 음향 데이터셋을 만들 때 그대로 참고할 만한 반자동 레시피다.
- **flow matching + 멀티모달 조건화**: MMAudio를 파인튜닝하며 CLIP·Synchformer·Perception Encoder로 의미·동기·공간 특징을 분리해 주입하는 방식은, 생성 모델에 공간 정보를 결합하려는 후속 연구의 모듈 설계에 응용 가능하다.
- FOA/360도나 별도 카메라 파라미터 없이 **일반 시야 영상만으로** 공간 단서를 뽑아낸다는 점에서, 실사용 시나리오(일반 촬영 영상)에 바로 붙이기 좋은 접근이다.

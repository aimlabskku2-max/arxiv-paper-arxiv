# FoleySpace: Vision-Aligned Binaural Spatial Audio Generation

**arXiv**: 2508.12918 | **주제 분류**: Spatial Audio | **출판일**: 2025-08-18 | **학회**: 프리프린트 (v2, 2025-08-21 개정)
**저자/소속**: Lei Zhao, Rujin Chen, Xiao-Lei Zhang (Northwestern Polytechnical University · TeleAI, China Telecom), Chi Zhang, Xuelong Li (TeleAI, China Telecom)
**링크**: https://arxiv.org/abs/2508.12918

## 한 줄 요약
무음 영상에서 소리가 나는 물체의 위치를 프레임 단위로 추정해 3D 이동 궤적을 만들고, 이를 사전학습된 비디오-투-오디오(V2A) 모델의 모노 오디오와 함께 확산 모델(diffusion model)의 조건으로 넣어, 영상 속 음원 방향과 일치하는 binaural(양이) 공간 음향을 생성하는 프레임워크다.

## 메인 그림
![FoleySpace 프레임워크 개요](https://arxiv.org/html/2508.12918v2/main_figure_v2.png)

Fig. 2. FoleySpace 전체 파이프라인으로 세 단계로 구성된다.
- **Stage A (추정)**: 위치 추정기가 각 프레임에서 음원의 2D 위치를, 깊이 추정기가 음원의 깊이(depth)를 뽑아낸다. 동시에 영상은 모노 생성기(MMAudio)에 들어가 의미적으로 정렬된 모노 오디오를 만든다.
- **Stage B (매핑)**: 추정된 2D 위치와 깊이를 청취자를 원점으로 하는 3D 음장(sound field) 좌표로 변환해 음원의 이동 궤적을 형성한다.
- **Stage C (생성)**: 모노 오디오와 3D 궤적을 조건으로 받아 확산 모델이 영상 속 음원 방향과 맞는 binaural 공간 음향을 생성한다.

## 선행 연구
- **V2A(비디오-투-오디오) 생성**: DiffFoley(대조 사전학습으로 시청각 정렬), Frieren(rectified flow matching + 1-step distillation), V2A-Mapper(CLIP-CLAP 매핑으로 AudioLDM 유도), MMAudio(대규모 학습 + 동기화 모듈), AudioX(멀티모달 마스킹 학습), ThinkSound(멀티모달 LLM 기반 Chain-of-Thought)까지 발전. 그러나 대부분 **모노(monaural) 오디오**만 생성한다.
- **오디오 공간화(audio spatialization)**: 2.5D visual sound 등은 이미 섞인 스테레오 오디오를 영상 정보로 다시 양이 오디오로 복원하는 과제로, 임의의 모노 오디오에는 일반화되지 않는다.
- **1차 앰비소닉스(FOA) 생성**: ImmerseDiffusion, Diff-SAGe, VISAGE, OmniAudio 등은 텍스트나 카메라 파라미터, 360도 영상 등 외부 정보에 의존한다.
- **See2Sound**: 이미지 분할 + Room Impulse Response(RIR, 실내 임펄스 응답) 모델링으로 공간 음향을 만들지만, 음질이 낮고 **정지 음원에만** 적용되어 시변(time-varying) 동적 음장을 다루지 못한다.

## 문제 제기
기존 V2A는 대부분 모노 오디오라 공간 지각(spatial perception)이 없다. AudioX·ThinkSound처럼 스테레오 VAE로 양이 오디오를 낸 경우도 영상과 오디오의 공간적 일치(spatial consistency)를 고려하지 않는다. 인간 청각은 좌·우 귀에 도달하는 소리의 차이 — 에너지 대비인 **ILD(interaural level difference, 양이 강도차)**와 시간 위상차인 **ITD(interaural time difference, 양이 시간차)** — 로 방향을 판단하는데, 기존 방법은 이런 단서를 영상 속 음원 위치와 맞추지 못한다. RIR 기반 See2Sound는 음질과 공간 일관성이 부족하고 움직이는 음원을 다룰 수 없다.

## 연구 주제
2D 일반 영상(무음)에서, 외부 좌표나 카메라 파라미터 없이 영상 자체에서 추정한 음원 위치만으로, 의미(semantic)·시간(temporal)·공간(spatial) 세 차원 모두에서 영상과 정렬된 binaural 공간 음향을 생성하는 것. 특히 정지 음원뿐 아니라 **움직이는 음원의 동적 음장**까지 다루는 것을 목표로 한다.

## 연구 방법
- **음원 위치 추정**: 개방 어휘(open-vocabulary) 객체 탐지 모델 YOLO-World로 프레임마다 음원의 바운딩 박스를 찾고 그 기하 중심을 2D 좌표 $(w_k, h_k)$로 삼는다. 오프라인 어휘를 쓰면 텍스트 입력 없이 신뢰도 최고 라벨을 자동 선택할 수 있다.
- **깊이 추정**: 단안 깊이 추정 모델 DepthMaster로 음원 픽셀의 깊이 $d_k$를 얻는다.
- **2D→3D 음장 매핑**: 영상 폭 기준의 매핑 계수 $\delta = \frac{2S_y}{W}$로 픽셀 좌표를 청취자 중심 3D 좌표 $(x_k, y_k, z_k)$로 변환한다. 깊이는 min-max 정규화 후 스케일 계수 $\gamma = \frac{W}{2}$로 절대 거리로 바꾼다. 이렇게 얻은 궤적 $\mathcal{T} = \{(x_k, y_k, z_k)\}_{k=1}^K$에서 프레임 간 이동량 $\Delta_k$의 상위 5%를 이상치로 제거하고 선형 보간으로 평활화($\tilde{\mathcal{T}}$)해 자연스러운 움직임을 만든다.
- **확산 기반 생성**: 모노 생성기로 MMAudio를 사용해 모노 오디오 $s_n^{mono}$를 만들고, 이것과 궤적 $\tilde{\mathcal{T}}$를 조건 블록(condition block)으로 통합해 백본인 DiffWave에 주입한다. 궤적을 시간축으로 복제·채널 결합해 입력하며, 입출력 합성곱 채널 수를 양이 처리에 맞게 조정했다.
- **coarse-grained(거친 입도) 변형**: 영상 평면을 5×3 격자(15칸)로 나눠 초당 한 번 음원이 속한 칸을 추정하고, 깊이를 5단계로 이산화해 총 5×3×5개 공간 위치를 쓴다. 음원 추정 정확도를 정량 평가하기 좋다.
- **학습 데이터 구축**: VGGSound에서 8초짜리 모노 클립 10,000개를 뽑고, HUTUBS HRTF 데이터베이스의 실측 **HRIR(Head-Related Impulse Response, 머리 전달 임펄스 응답)** 10명분(pp87~pp96)으로 컨볼루션해 binaural 오디오를 만든다. 고정 거리(1.47m)로 측정된 HRIR을 시간영역 리샘플링으로 0~6m 거리별로 확장하고, 모노 오디오를 M개 구간으로 나눠 궤적상 각 위치의 HRIR과 컨볼루션한 뒤 구간 사이를 보간(식 8)해 움직이는 음원을 시뮬레이션한다(fine: M=200, coarse: M=8).

## 실험 결과 / 연구 의의
평가: VGGSound에서 단일 음원 9,212개를 선별·격자 주석해 만든 VGGSound-Solo. 주관 평가는 32개 영상 × 6개 방법을 24명이 1~5점으로 PSS(공간감), SA(공간 정렬), TA(시간 정렬), SC(의미 일치), AQ(음질) 다섯 축으로 채점(MOS).

**사용자 연구 (MOS, 높을수록 좋음)**

| 방법 | PSS ↑ | SA ↑ | TA ↑ | SC ↑ | AQ ↑ |
|---|---|---|---|---|---|
| MMAudio* (모노) | 1.54 | 1.67 | 3.86 | 3.77 | 3.72 |
| See2Sound | 1.32 | 1.25 | 1.45 | 1.13 | 1.39 |
| AudioX | 2.76 | 2.79 | 2.77 | 2.92 | 2.90 |
| ThinkSound | 2.47 | 2.56 | 2.74 | 2.57 | 2.71 |
| FoleySpace (제안) | 3.72 | 3.85 | 3.79 | 3.81 | 3.69 |
| FoleySpace_coarse (제안) | 3.67 | 3.79 | 3.71 | 3.92 | 3.71 |

- 모노 MMAudio 대비 공간 관련 지표(PSS, SA)에서 크게 앞서면서, TA·SC·AQ는 모노와 대등해 음질을 지키면서 공간감을 더했다.
- 다른 다채널 방법(See2Sound·AudioX·ThinkSound)은 전 지표에서 능가. 흥미롭게도 공간 음향 방법 See2Sound가 여러 관심 영역 오디오를 단순 중첩해 청각적 혼잡을 일으켜 오히려 모노 MMAudio보다 PSS·SA가 낮았다.

**객관 지표 (VGGSound-Solo)**

| 방법 | FD_PANNs ↓ | FD_VGG ↓ | KL_PANNs ↓ | KL_PaSST ↓ | IS ↑ | IB-score ↑ | DeSync ↓ |
|---|---|---|---|---|---|---|---|
| MMAudio* (모노) | 4.57 | 0.94 | 1.73 | 1.48 | 18.32 | 31.74 | 0.46 |
| See2Sound | 51.19 | 9.21 | 4.34 | 3.91 | 3.42 | 7.95 | 1.28 |
| AudioX | 13.54 | 1.61 | 2.78 | 2.67 | 14.35 | 24.08 | 1.23 |
| ThinkSound | 8.42 | 1.40 | 1.95 | 1.75 | 11.57 | 23.32 | 0.57 |
| FoleySpace | 7.25 | 1.73 | 1.76 | 1.45 | 14.55 | 26.42 | 0.50 |
| FoleySpace_coarse | 6.81 | 1.58 | 1.77 | 1.43 | 15.24 | 26.71 | 0.51 |

- 다채널 방법 중 종합 1위(FD_VGG만 ThinkSound에 근소하게 뒤짐). 모노 MMAudio에는 약간 못 미치지만 격차는 작다.
- **HRIR vs RIR (Table IV)**: HRIR 기반 학습이 RIR 기반보다 모든 지표에서 압도적으로 우수(예: fine 스킴 FD_PANNs 7.25 vs 69.03, IS 14.55 vs 2.05). 인간 귀의 생리적 필터링을 정확히 모델링하는 HRIR이 음향 사실감의 핵심임을 보였다.
- **텍스트 라벨 영향 (Table III)**: 수동 텍스트 라벨 사용 시 $MAE_\alpha$=39.62°, $MAE_\varepsilon$=13.01°. 오프라인 어휘(COCO/ImageNet-1K/VGGSound/AudioSet)를 써도 방위각 차이가 10° 미만이라, 텍스트 입력 없이도 실용적임.
- 파형 시각화(Fig. 6)에서 화면 좌우로 이동하는 음원에 맞춰 좌·우 채널 볼륨이 실제로 이동하는 반면, 기존 방법들은 좌우 볼륨이 같거나 고정 차이만 있어 방향감이 없었다.

의의: 일반 2D 영상에서 외부 파라미터 없이 의미·시간·공간 정렬된 binaural 오디오를, 그것도 움직이는 음원까지 생성하는 첫 프레임워크를 제시하고, 콘텐츠 생성과 공간화를 분리하는 설계의 효과를 입증했다.

## 한계
- 콘텐츠 생성을 사전학습 V2A(MMAudio)에 의존하므로, 오디오 품질과 의미 정확도가 모노 생성기 성능에 상한이 걸린다(객관 지표에서 MMAudio에 소폭 뒤짐).
- 프레임당 하나의 지배적 음원을 가정하는 구조로, 다중 음원이 동시에 소리 내는 복잡한 장면 처리는 논문에서 다루지 않았다(평가도 단일 음원 VGGSound-Solo 기반).
- 위치·깊이 추정이 YOLO-World·DepthMaster의 정확도에 의존하며, 화면 밖(off-screen) 음원이나 시각적으로 드러나지 않는 음원은 다루기 어렵다.
- HRIR은 HUTUBS 10명분에서 합성한 학습 데이터라, 개인별 HRTF 차이나 실제 잔향 환경으로의 일반화는 검증되지 않았다.

## 우리 연구와 연결되는 점
- **Egocentric Vision**: FoleySpace의 2D→3D 음장 매핑은 화면 중심을 청취자 위치로 놓는 3인칭 관찰자 관점이다. 1인칭(에고센트릭) 영상은 카메라 자체가 청취자 머리에 가깝고 시점 이동·머리 회전이 큰 만큼, 이 매핑에 자기 운동(ego-motion)과 시야 밖 음원 처리를 결합하면 에고센트릭 공간 음향 생성으로 확장할 여지가 있다.
- **Hand-Object Interaction**: 손-물체 상호작용은 접촉음(두드림·마찰·긁힘 등)이 특정 물체 위치에서 발생하는 대표적 사례다. YOLO-World 기반 음원 위치 추정을 상호작용 중인 손/물체 위치 추정으로 대체하면, 상호작용 지점에 정확히 정위된 접촉음의 binaural 생성이 가능해진다 — 조작 데이터셋에 공간 음향 라벨을 붙이는 데 응용할 수 있다.
- **Spatial Audio**: 콘텐츠 생성(모노 V2A)과 공간화(궤적 조건 확산 + HRIR)를 분리한 모듈식 설계, 그리고 실측 HRIR 컨볼루션으로 이동 음원 학습 데이터를 합성하는 방식은, 우리가 시청각 데이터에서 ITD/ILD 기반 공간 단서를 다룰 때 바로 참고할 수 있는 파이프라인이다. VGGSound-Solo와 HUTUBS HRIR 활용 방식도 재사용 가치가 있다.

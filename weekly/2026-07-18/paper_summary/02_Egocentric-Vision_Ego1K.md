# Ego-1K – A Large-Scale Multiview Video Dataset for Egocentric Vision

**arXiv**: 2603.13741 | **주제 분류**: Egocentric Vision | **출판일**: 2026-03-14 | **학회**: 프리프린트
**저자/소속**: Jae Yong Lee, Daniel Scharstein, Akash Bapat, Hao Hu, Andrew Fu, Haoru Zhao, Paul Sammut, Xiang Li, Stephen Jeapes, Anik Gupta, Lior David, Saketh Madhuvarasu, Jay Girish Joshi, Jason Wither (전원 Meta Reality Labs 소속)
**링크**: https://arxiv.org/abs/2603.13741

## 한 줄 요약
사용자가 쓴 VR 헤드셋(카메라 4개)을 동기화된 카메라 12개로 빙 둘러싼 커스텀 rig로 촬영해, 시간이 맞춰진 egocentric(1인칭 시점) multiview 비디오 약 1,000개를 모은 데이터셋이다. neural 3D/4D video synthesis와 동적 장면 이해를 위한 벤치마크로 쓸 수 있다.

## 메인 그림
![fisheye 카메라 12개와 Quest 3 헤드셋(카메라 4개)을 결합한 동기화 multi-camera rig, 그리고 이 rig로 담은 동적 egocentric multiview 캡처 예시](https://arxiv.org/html/2603.13741v1/figs/teaser.jpg)

## 선행 연구
지금까지 egocentric 및 3D 재구성 연구는 크게 두 갈래의 데이터를 기반으로 발전해 왔다. 하나는 object-centric(물체 중심) multiview 데이터셋으로, 정지한 물체를 고정 카메라 여러 대로 찍어 novel view synthesis(NVS, 새로운 시점 영상 합성)를 학습하고 평가하는 흐름이다. 다른 하나는 카메라를 고정 배열(fixed-pose multiview video)로 두고 움직이는 장면을 찍는 흐름으로, Spacetime Gaussians, K-Planes, 3D Gaussian Splatting(3DGS) 같은 4D 재구성 기법이 여기서 나왔다. Egocentric vision 분야에서는 헤드마운트 카메라로 찍은 대규모 비디오 데이터셋이 hand-object interaction(손과 물체의 상호작용)과 일상 행동을 담아 왔다.

## 문제 제기
문제는 기존 데이터셋과 기법이 대부분 (1) object-centric이거나 (2) 카메라가 고정된 rig를 전제로 만들어졌다는 점이다. 하지만 실제 egocentric 환경에서는 **rig egomotion(착용자의 머리·몸 움직임)** 과 **손처럼 카메라에 바짝 붙은 동적 물체**가 동시에 나타난다. 카메라 가까이에서 물체가 움직이면 disparity(양안 시차)와 image motion이 커지는데, 이 때문에 기존 3D/4D NVS 기법을 그대로 쓰기가 어렵다. 결국 egomotion과 근거리 손 상호작용이 뒤섞인 이 영역을 제대로 담아내고 평가할 만한, 대규모이면서 시간이 동기화된 다시점 데이터가 없었다는 것이 핵심이다. 이는 AR/VR 헤드셋에서 실시간 3D 장면 재구성과 hand-object interaction 이해를 가로막는 직접적인 걸림돌이 된다.

## 연구 주제
이 논문은 egomotion과 근거리 동적 hand-object interaction이 함께 존재하는 조건에서 **egocentric multiview 3D/4D novel view synthesis와 동적 장면 재구성**을 어떻게 풀 것인가라는 문제를 새롭게 부각한다. 이를 위해 시간이 동기화된 대규모 multiview egocentric 데이터셋(Ego-1K)을 만들고, 이 영역에 맞는 표준 평가 프로토콜을 제안한다.

## 연구 방법
**수집 rig (input 관점)**: 카메라 16개를 60 Hz로 동기화했다. 바깥쪽 12개는 fisheye 카메라(8 MP, $2848 \times 2848$, global shutter, 대각 190° FOV, 스트리밍 시 6 MP $2448 \times 2448$로 크롭)로, 이들이 Quest 3 헤드셋의 카메라 4개(RGB rolling-shutter 2개 $2328 \times 1748$@60Hz, grayscale global-shutter SLAM 2개 $512 \times 640$@30Hz)를 둘러싼다. 여기에 Lucid Helios2 Wide iToF 센서 2개($640 \times 480$@30Hz)를 더했다. rig 무게는 약 6 kg으로, 백팩에 장착한 crane으로 받치고 wireless LTC timestamp로 동기화한다.

**데이터 규모/구성**: operator 5명이 lab, office, living room, bedroom, rooftop 등 다양한 환경에서 촬영했다. 처음 999개 중 43개를 버리고 최종 956개를 남겼다. 영상 하나는 8–10초, 카메라당 약 450–550 frame이다. 조명은 51–75 lux부터 1001 lux 이상까지 6개 illumination bin으로 다양하게 잡았다. 손 제스처, 타이핑, 물체 조작 같은 hand-object interaction이 중심이다.

**처리/캘리브레이션**: 원시 데이터는 초당 약 15 GB(uncompressed)로 쏟아지며, recording 하나당 평균 약 19 GB다. 대형 평면 Calibu 타깃 5개로 offline 캘리브레이션을 한 뒤, 여러 주에 걸친 촬영 동안 주기적으로 다시 캘리브레이션했다. Online calibration으로 recording마다 카메라 회전과 초점거리를 보정해 median absolute deviation(MAD)을 35% 줄였다. rig와 헤드셋 RGB 스트림 사이에는 global color matching을 적용했다.

**연구용 데이터셋 (output 관점)**: fisheye 영상은 rectified stereo pair(pinhole) 6개로 dewarp했으며, 해상도는 $1280 \times 1280$, 수평 130° FOV다. frame별 calibration과 pose를 담은 PNG로 제공한다. 연구용 17.5 TB를 공개하고, raw 88 TB는 요청 시 제공한다. recording마다 조명, 장면 유형·레이아웃, operator의 행동·의상, 든 물체·착용한 액세서리, 머리 움직임, 다른 사람의 등장 여부 등을 텍스트 라벨(메타데이터)로 붙였다. 데이터셋은 https://huggingface.co/datasets/facebook/ego-1k 에서 공개했다.

## 실험 결과 / 연구 의의
**Stereo consistency 평가** (MAD, SD 기준): Foundation Stereo가 가장 좋아서 주 depth source로 골랐다.

| 방법 | MAD (mm) | MAD<1mm 비율 | SD (mm) |
|------|----------|--------------|---------|
| Foundation Stereo | 1.6 | 74.0% | 42.5 |
| StereoAnywhere | 1.7 | - | - |
| BiDAStereo | 2.2 | - | - |
| Selective-Stereo | 8.0 | - | - |

**4D Novel View Synthesis 평가** (target pair는 카메라 3–4번, 나머지 카메라 10개로 학습, 데이터셋의 10%인 96개 recording으로 평가):

| 방법 | PSNR (dB) | SSIM | LPIPS |
|------|-----------|------|-------|
| 3DGS + stereo guidance | 29.12 | 0.830 | 0.115 |
| Spacetime Gaussians | 24.76 | 0.780 | 0.270 |
| 3DGS (per-frame) | 21.22 | 0.709 | 0.260 |
| K-Planes | 16.46 | 0.597 | 0.443 |

Stereo depth guidance를 준 3DGS는 기본 3DGS보다 PSNR이 +7.9 dB, Spacetime Gaussians보다 +4.4 dB, K-Planes보다 +12.7 dB 높았다. 정리하면 (1) 기존 3D/4D NVS 기법은 이 egocentric 영역에서 크게 고전하고, (2) **stereo depth guidance를 주면 재구성 품질이 확실히 크게 좋아진다**는 것이다.

## 한계
- iToF 센서 스트림은 motion과 phase ambiguity 탓에 신뢰도가 낮아 실험에서 뺐다.
- Quest 3 헤드셋 카메라는 shutter 방식, 해상도, color profile이 달라, 일관성을 위해 연구용 데이터셋에서 뺐다.
- 기존 3D/4D NVS 기법은 object-centric이거나 고정 pose multiview를 전제로 만들어져서, egomotion과 동적 hand interaction이 뒤섞인 이 영역에는 역부족이다.
- 성능은 멀리 있는 인물보다 가까이서 움직이는 물체(손)에서 더 크게 떨어진다.
- Future work: multiview/multi-baseline stereo로 고품질 per-frame depth(pseudo GT) 만들기, 카메라 subset ablation, HOI 중심 task 평가, stereo baseline 변화에 대한 robustness, temporal stability 벤치마크, pairwise consistency 기반 semantic·person segmentation 평가 등을 제안한다.

## 우리 연구와 연결되는 점
- **Egocentric Vision**: rig egomotion과 시간 동기화된 multiview를 함께 갖춘 대규모 데이터셋이라, egocentric 3D 재구성과 novel view synthesis 연구의 학습·평가 기반으로 바로 쓸 수 있다.
- **Hand-Object Interaction**: 데이터 자체가 hand motion과 hand-object interaction을 중심으로 설계됐고, 저자들도 HOI-focused task 평가를 future work로 밝혔다. 가까운 손을 동적으로 재구성하는 어려운 문제를 정량적으로 평가할 벤치마크로서 HOI 연구에 쓸모가 크다.
- **Spatial Audio**: 이 데이터셋은 시각·기하(멀티뷰 영상, depth, calibration/pose)가 중심이고, audio 모달리티는 논문에서 따로 언급하지 않는다. 다만 정확한 카메라 pose와 정밀한 공간 기하 정보는, 앞으로 spatial/binaural audio를 결합할 때 sound source의 3D 위치를 시각·기하와 맞추는 참조 기준으로 활용될 여지가 있다(잠재적 관점).

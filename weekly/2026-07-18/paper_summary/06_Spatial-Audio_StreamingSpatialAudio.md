# Towards Streaming Synchronized Spatial Audio Generation via Autoregressive Diffusion Transformer

**arXiv**: 2605.30940 | **주제 분류**: Spatial Audio | **출판일**: 2026-05 | **학회**: 프리프린트
**저자/소속**: Ke Lei, Yu Zhang, Changhao Pan, Xueyi Pu, Wenxiang Guo, Ruiqi Li, Zhou Zhao (Zhejiang University 등; 제공된 본문 excerpt에는 개별 소속이 명시적으로 표기되어 있지 않음)
**링크**: https://arxiv.org/abs/2605.30940

## 한 줄 요약
360도 파노라마 비디오와 텍스트를 입력받아 4채널 FOA(First-Order Ambisonics, 1차 앰비소닉스) 공간 음향을 낮은 지연으로 스트리밍 생성하는 causal autoregressive diffusion transformer 프레임워크 SwanSphere를 제안한다.

## 메인 그림
![SwanSphere 전체 개요: 파노라마 비디오와 텍스트를 받아 동기화된 FOA 공간 음향을 스트리밍으로 만들어내는 파이프라인](https://arxiv.org/html/2605.30940v1/x1.png)

## 선행 연구
- **Video-to-Audio (V2A) 생성**: latent diffusion 기반에서 autoregressive token 기반 방식으로 발전해 왔다. 최근 SoundReactor 등은 causal modeling을 써서 프레임 단위 온라인 V2A를 시도했다.
- **공간 음향(spatial audio) 생성**: 예전에는 mono를 먼저 합성한 뒤 spatialization을 덧붙이는 2단계 파이프라인을 썼지만, 이후 OmniAudio, ViSAGe처럼 파노라마 비디오에서 FOA를 바로 생성하는 end-to-end 방식으로 넘어갔다.

## 문제 제기
기존 공간 음향 합성에는 두 가지 핵심 병목이 있는데, 이는 실시간 상호작용이 필요한 immersive(VR/AR) 응용에 치명적이다.
1. **품질-지연 trade-off**: discrete codebook 방식은 양자화 손실(quantization loss)을 낳고, self-attention 기반 diffusion transformer는 multi-step denoising 탓에 연산이 오래 걸리며 첫 프레임 지연(first-frame latency)도 커서 실시간 스트리밍에 맞지 않는다.
2. **약한 cross-modal 정합**: CLIP 기반 encoder는 소리에 대한 감각(acoustic awareness)이 부족하고, global pooling이 음원 위치 파악에 필요한 spatial cue까지 걸러내 방향 정합이 약하다. (게다가 파노라마 비디오-공간 음향 짝 데이터셋도 부족하다.)

## 연구 주제
파노라마 비디오/텍스트에 동기화된 고품질 FOA 공간 음향을 양자화 손실 없이 낮은 첫 프레임 지연으로 스트리밍 생성하는 문제. 특히 azimuth(수평각)/elevation(수직각) 방향까지 정확히 맞추는, 방향을 인지하며 동기화된 생성을 새롭게 강조한다.

## 연구 방법
- **입력**: 360도 파노라마 비디오 및/또는 텍스트 caption. **출력**: 방향 정보를 담은 4채널 FOA 오디오.
- **분할 정복(divide-and-conquer) 2단계 구조**:
  - Stage 1 (Semantic Planning): causal language model이 video feature와 caption embedding을 조건으로 semantic embedding을 만든다.
  - Stage 2 (Local Rendering): Local Diffusion Transformer(LocDiT)가 앞 patch의 boundary context를 받아 patch 내부를 flow matching으로 고품질 합성한다. 이렇게 단계를 나눈 덕분에 전체 시퀀스에 attention을 걸지 않고도 스트리밍이 가능하다.
- **주요 모듈**:
  - **Spatial Video-Audio Contrastive Learning (SVAC)**: 서로 보완하는 4가지 목적으로 정합을 유도한다 — instance exchange(semantic), temporal offset(오디오를 시간 이동시킨 negative로 동기화), audio rotation(3D FOA 회전으로 만든 spatial negative), video rotation(파노라마 회전 기반 geometric consistency). symmetric InfoNCE loss를 쓴다.
  - **Multi-Objective Online DPO (ODPO)**: post-training 단계에서 병렬로 뽑은 8개 sample을 가중 reward로 순위 매긴다. reward는 spatial feedback(azimuth/elevation error), semantic similarity(ImageBind), fidelity(Audiobox aesthetics)로 이뤄지며 가중치는 spatial $0.4$, semantic $0.4$, fidelity $0.2$이다.
  - **VAE**: fine-tuning한 Stable Audio VAE가 4채널 FOA를 21.5 FPS, 프레임당 $d=128$짜리 continuous latent로 인코딩한다.
  - **Curriculum Learning**: 약 100만 개의 non-spatial audio를 pseudo-FOA로 바꿔 사전학습에 활용한다.
- **데이터셋(SwanSphere Corpus)**: Sphere360(288h), YT-Ambigen(142h), 새로 수집한 YouTube(138h)를 합쳐 약 165,000개의 video-FOA pair, 총 458h를 구성했다. spatial caption 약 3,100개는 acoustic intensity vector 분석을 기반으로 MLLM이 자동 annotation해 만들었다.

## 실험 결과 / 연구 의의
- **Video-to-Spatial 정량 비교** (품질, 방향 정합, 자연스러움 모두에서 앞선다):

| Metric | SwanSphere | OmniAudio | ViSAGe |
|---|---|---|---|
| FD ↓ | 120.28 | 157.67 | 232.17 |
| KL ↓ | 1.36 | 1.93 | 2.67 |
| Angular Error ↓ | 1.03° | 1.27° | 1.59° |
| MOS-SQ ↑ | 4.32±0.15 | 4.12±0.18 | 3.82±0.20 |
| MOS-AF ↑ | 4.44±0.20 | 4.27±0.17 | 3.78±0.26 |

- **속도**: full-sequence DiT보다 약 30배 빠르다.

| Metric | SwanSphere | Full-sequence DiT |
|---|---|---|
| First-chunk latency ↓ | 0.21s | 6.47s |
| Inference time ↓ | 0.21s | 9.13s |

- **Text-to-Spatial**:

| Metric | SwanSphere | Tango2+AS |
|---|---|---|
| FD ↓ | 142.80 | 235.71 |
| MOS-SQ ↑ | 4.31±0.18 | — |

- **Ablation**: SVAC는 angular error를 1.09° 낮추고, ODPO는 FD를 13.63 낮춘다. 모델 크기도 영향을 주는데, SwanSphere-S(0.43B)는 SwanSphere-L(1.09B)보다 성능이 눈에 띄게 떨어진다.
- **메시지**: 분할 정복형 causal AR diffusion에 방향을 인지하는 contrastive/preference 학습을 결합하면, 양자화 손실 없이도 저지연 스트리밍과 고품질, 정확한 방향성을 한꺼번에 달성할 수 있음을 보인다.

## 한계
- 저자들이 밝힌 한계: spatial caption이 대부분 가장 두드러진 음원만 기술하다 보니, 여러 악기가 동시에 연주되는 콘서트처럼 음원이 많은 상황을 충분히 모델링하지 못하고 세밀한 spatial disentanglement에도 제약이 있다.
- 향후 과제: 음원이 여러 개인 장면을 위한 데이터셋 확장, 학습에서 보지 못한 녹음 환경/설정에도 잘 일반화하는 방법 연구.

## 우리 연구와 연결되는 점
- **Spatial Audio**: 파노라마 비디오 기반 FOA 생성, azimuth/elevation 방향 정합, FOA rotation으로 만든 spatial negative를 쓰는 contrastive learning은 우리의 공간 음향 생성/정합 연구와 곧바로 이어진다. 스트리밍, 저지연 설계는 실시간 immersive(AR/VR) 응용에 그대로 쓸 수 있다.
- **Egocentric Vision / Hand-Object Interaction**: 논문에서 직접 언급하지는 않는다. 다만 egocentric 환경의 음원(손-물체 상호작용 등)에 대한 방향성 있고 동기화된 음향을 생성하거나 추론하는 문제로 확장한다면, 이 논문의 video-audio 동기화(temporal offset)와 방향 정합(SVAC) 아이디어를 참고할 만하다.

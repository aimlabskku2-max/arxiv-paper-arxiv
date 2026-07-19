# Probing Spatial Structure in Pretrained Audio Representations

**arXiv**: 2606.05544 | **주제 분류**: Spatial Audio | **출판일**: 2026-06-04 | **학회**: Interspeech 2026
**저자/소속**: Chuyang Chen, Sivan Ding, Adrian S. Roman, Juan Pablo Bello (Music and Audio Research Laboratory, New York University, USA) — Chen, Ding, Roman은 공동 1저자
**링크**: https://arxiv.org/abs/2606.05544

## 한 줄 요약
사전학습된 오디오 모델의 frozen embedding에 공간(spatial) 정보가 얼마나 담겨 있는지를, 가벼운 linear probing(표현 안에 어떤 정보가 들어 있는지 진단하는 방법)으로 요인별로 나눠 측정하는 SARL(Spatial Audio Representation Learning) 벤치마크를 제안한다.

## 메인 그림
메인 그림(Figure 1)은 7개 공간 task(azimuth, elevation, distance, class, RT60, volume, shape)에서 각 사전학습 인코더의 probing 성능을 random predictor 대비 얼마나 좋아졌는지로 나타내며, 모델을 입력 포맷별(왼쪽)과 학습 패러다임별(오른쪽)로 정렬해 보여준다. (믿을 만한 절대 이미지 URL을 구하지 못해 이미지는 넣지 않고 설명으로 대신한다.)

## 선행 연구
기존 오디오 representation 벤치마크(HEAR, SUPERB, X-ARES, MARBLE)는 대부분 monaural(단일 채널) 신호와 semantic task(이벤트 분류 등)에만 집중했고, 공간 정보는 거의 평가하지 않았다. 반대로 공간 오디오 쪽 벤치마크(DCASE, LOCATA, CHiME, REVERB)는 있지만, 이들은 end-to-end 시스템 전체의 성능만 재기 때문에 representation 자체의 품질을 따로 떼어 보지 못한다. 본 논문은 mono, stereo, binaural, First-Order Ambisonics(FOA) 같은 여러 입력 포맷과 self-supervised / supervised / codec 기반 학습 패러다임으로 사전학습된 공간 오디오 인코더 13개(예: [A-MAE](https://arxiv.org/abs/2207.06405), SELD-S/F, [EnCodec](https://arxiv.org/abs/2210.13438), [Spatial-AST](https://arxiv.org/abs/2402.01591), [wav-JEPA](https://arxiv.org/abs/2509.23238), [GRAM-B/F](https://arxiv.org/abs/2506.00934), AVSA, EINv2 등)를 평가한다.

## 문제 제기
두 갈래 모두 한계가 뚜렷하다. Semantic 중심 벤치마크는 sound source의 azimuth·elevation·distance나 room의 잔향 특성 같은 공간 속성을 거의 건드리지 않고, 공간 벤치마크는 시스템 전체 성능만 보기 때문에 "모델의 내부 표현에 실제로 어떤 공간 속성이 담겨 있는가"를 직접 확인할 방법이 없다. 그러다 보니 어떤 입력 포맷과 학습 방식이 공간 구조를 더 잘 담는지, source 속성과 room 속성 중 무엇이 더 잘 표현되는지가 여전히 불분명하다. spatial audio는 immersive media, robotics, embodied AI, acoustic scene understanding에서 핵심 역할을 하므로, 사전학습 표현이 공간 구조를 얼마나 담는지 진단할 수 있는 근거가 꼭 필요하다.

## 연구 주제
사전학습된 오디오 모델의 frozen embedding에서 공간 속성을 얼마나 읽어낼(decodable) 수 있는지를, 통제된 조건에서 요인별로 나눠 평가하자는 것이 이 논문의 핵심이다. 저자들은 평가의 초점을 task 중심 benchmarking에서 probing 기반 분석으로 옮겨야 한다고 주장하며, source-level 속성(azimuth, elevation, distance, event class)과 room-level 속성(RT60, volume, shape)을 나눠, 입력 포맷과 학습 패러다임에 따라 공간 인코딩이 어떻게 달라지는지를 밝힌다.

## 연구 방법
- **Input**: mono/stereo/binaural/FOA 같은 multi-channel audio를 각 encoder의 native sampling rate로 넣고, 인코더는 frozen 상태로 그대로 둔다.
- **Output**: frozen embedding을 mean-pooling해 scene-level 표현으로 모은 뒤, 그 위에 linear classifier만 얹어 학습한다.
- **데이터**: source 요인과 room 요인을 고르게 바꿔 가며 만든 시뮬레이션 기반 통제형 spatial audio 데이터셋(single-source scene)을 구축한다. 연속 factor는 구간으로 나눈다(azimuth 36 bins, elevation 12 bins, distance 20 bins, RT60 29 bins, volume 5 bins). 범주형 factor는 discrete하게 처리한다(event class 7 categories, room shape 4 categories).
- **Probing 학습/평가**: linear classifier는 cross-entropy로 학습하고, Adam optimizer, $lr = 1 \times 10^{-4}$, cosine decay, 20 epochs를 쓴다. 연속형 요인에는 Gaussian soft label, 범주형 요인에는 one-hot을 쓴다. 평가는 연속형에 normalized MAE, 범주형에 macro-F1을 쓰고, 집계할 때 baseline normalization을 적용한다.
- **Sensitivity 분석**: 한 factor 그룹만 다르게 한 scene embedding 쌍(paired scenes)의 cosine similarity를 random embedding 쌍 기준으로 정규화해, 표현이 각 공간 요인의 변화에 얼마나 민감하게 반응하는지 살펴본다.

## 실험 결과 / 연구 의의
- **입력 포맷 효과**: FOA 모델이 전반적으로 가장 좋은 성능을 내고, 특히 elevation과 room-level task에서 앞선다. 다만 공간 채널이 없는 mono 기반 A-MAE도 room-level task에서는 만만치 않은 결과를 낸다.
- **학습 패러다임 효과**: supervised localization 모델은 azimuth에서 뛰어나지만(direction-of-arrival을 명시적으로 학습한 결과) room factor에는 약하고, self-supervised 방식은 더 균형 잡힌 표현을 만든다.
- **Source–Room 격차**: 모든 인코더에서 source factor가 room factor보다 한결같이 잘 읽히며, localization·semantic 쪽 개선폭이 room 쪽 개선폭을 크게 앞선다.
- **Sensitivity 패턴**: 거의 모든 모델에서 source를 바꿨을 때가 room을 바꿨을 때보다 embedding이 더 크게 변하고, 성능이 강한 모델일수록 전체적인 sensitivity 크기는 오히려 작아지는 경향이 있다.
- **메시지**: 입력 구성과 학습 방식이 공간 인코딩을 크게 좌우하며, 지금의 사전학습 표현은 source 정보에 비해 room(공간·음향 환경) 정보를 상대적으로 덜 담고 있다는 것을, architecture에 얽매이지 않는 진단 프로토콜로 보여준다.

## 한계
- 통제된 합성 환경의 single-source scene만 다뤄, 실제 음향 환경의 복잡함(다중 음원, 실제 녹음)을 단순화했다.
- linear probing은 embedding에서 선형적으로 뽑아낼 수 있는 정보만 재기 때문에, 비선형적으로 담긴 정보는 잡아내지 못한다.
- 평가 대상 모델들을 원래 학습 조건과 다른 분포에서 평가했다.
- Future work으로는 실제 녹음과 다중 음원 환경으로의 확장, 그리고 다른 probing 전략을 제안한다.

## 우리 연구와 연결되는 점
- **Spatial Audio**: 우리 연구의 핵심 주제와 곧바로 이어진다. azimuth/elevation/distance와 RT60/room 속성을 얼마나 읽어낼 수 있는지, FOA와 binaural 입력 포맷 비교, source와 room 표현의 격차 같은 결과는, 공간 오디오 표현을 다루는 연구에서 사전학습 인코더를 고르고 진단(probing) 프로토콜을 설계할 때 좋은 참고가 된다.
- **Egocentric Vision / Hand-Object Interaction**: 논문에 직접 언급은 없다(우리가 볼 수 있는 잠재적 연결점). Egocentric 환경에서 착용자 주변 음원의 방향·거리를 파악하는 spatial audio는 시각과 합쳐 장면 이해나 상호작용 추론을 보강할 수 있고, 이 논문의 probing 방법론은 egocentric multimodal 표현이 공간 정보를 담는지 진단하는 틀로 넓혀 쓸 수 있다.

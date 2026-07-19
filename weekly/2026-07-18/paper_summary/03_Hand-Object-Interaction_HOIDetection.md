# Improving and Evaluating Hand-Object Interaction Detection

**arXiv**: 2606.17384 | **주제 분류**: Hand-Object Interaction | **출판일**: 2026-06-16 | **학회**: 프리프린트
**저자/소속**: Ahmad Darkhalil (University of Bristol), Dima Damen (University of Bristol), David Fouhey (New York University)
**링크**: https://arxiv.org/abs/2606.17384

## 한 줄 요약
Transformer 기반 HOI-DETR 하나로 손, 손이 직접 잡은 물체(1st object), 도구를 거쳐 조작되는 물체(2nd object)와 이들 사이의 상호작용 관계까지 한꺼번에 검출하고, 여기에 정제한 데이터셋과 프레임/비디오 단위 평가 프로토콜을 함께 제안한다.

## 메인 그림
![HOI-DETR: 손·1st object·2nd object와 손→1st, 1st→2nd 상호작용을 통합 검출하는 zero-shot 예시](https://arxiv.org/html/2606.17384v1/x1.png)

## 선행 연구
그동안 Hand-Object Interaction(HOI, 손-물체 상호작용) 연구는 손 검출(hand detection), 손-물체 분할(hand-object segmentation), 3D 재구성, 비디오 단위 분석 등 여러 갈래로 나뉘어 발전했다. 손 검출은 딥러닝 덕분에 성능이 크게 좋아졌지만, 정작 대부분의 HOI 방법은 오래되고 성능이 떨어지는 detector를 그대로 썼다. 게다가 일부 연구는 손이나 손에 쥔 물체(held object)만 다루다 보니 상호작용 전체를 포괄적으로 이해하는 데까지는 이르지 못했다.

## 문제 제기
일반적인 object detection은 물체가 무엇인지, 즉 semantic category(의미 범주)를 맞히는 데 집중한다. 반면 HOI detection은 물체가 상호작용 안에서 맡는 **맥락적 역할(contextual role)**까지 알아야 한다. 같은 물체라도 상황에 따라 background가 되기도 하고, 손이 직접 잡은 1st object가 되기도 하며, 도구를 거쳐 조작되는 2nd object가 되기도 하기 때문이다. 그런데 기존 방법들은 방법론과 데이터셋, 평가 어느 하나에 치우쳐 균형이 맞지 않았고, transformer 기반 최신 detector도 활용하지 못했다. 데이터셋마저 중복 박스 같은 오류를 안고 있어 믿을 만한 평가가 힘들었다. HOI는 action recognition, robotics, 3D 재구성 같은 응용의 토대가 되는 만큼 이 공백은 그냥 넘길 수 없는 문제다.

## 연구 주제
이 논문은 **"HOI Detection을 어떻게 개선하고 평가할 것인가"**라는 문제를 정면으로 파고든다. 손-물체뿐 아니라 물체-물체(1st→2nd) 관계까지 아우르는 상호작용 인식에 초점을 두고, (1) 방법론(최초의 transformer 기반 HOI detector), (2) 데이터셋(기존 데이터 정제와 신규 벤치마크), (3) 평가 프로토콜(프레임과 비디오의 시공간 일관성)이라는 세 축을 한꺼번에 다룬다.

## 연구 방법
**Input/Output**: 이미지 한 장을 입력받아, 역할 기반 클래스(hands, 1st object, 2nd object, background) 검출 결과와 함께 방향이 있는 유효 상호작용 쌍(hand→1st object, 1st object→2nd object)을 내놓는다.

**모델 구조 (Co-DETR 확장, HOI-DETR)**:
- Backbone/Encoder: Vision Transformer(ViT-L/16)로 패치 임베딩을 만든 뒤, multi-scale deformable attention으로 특징을 다듬어 latent representation(잠재 표현) $F$를 얻는다.
- Decoder: 디코더 6개 layer의 self/cross-attention으로 역할 기반 클래스를 예측하고, Hungarian matching으로 예측을 정답(GT)에 짝지운다. 예측은 의미(semantic)가 아니라 상호작용을 인식(interaction-aware)하도록 설계했다.
- Interaction Module(핵심 기여): 짝지은 디코더 임베딩 $[h_i \| h_j]$을 MLP head에 넣어 유효한 상호작용 쌍인지 아닌지를 이진 분류(binary classification)한다. 유효한 쌍은 hand→1st object와 1st object→2nd object뿐이고, hand→2nd object는 반드시 1st object를 거쳐야 하므로 제외한다.

**학습 목표**: encoder supervision(one-to-many 할당으로 공간 변별력 확보), decoder supervision(one-to-one 할당, classification+regression loss), interaction loss(유효 쌍에 focal loss), 그리고 auxiliary head를 함께 묶어 학습한다. loss 가중치는 $\lambda_1=1.0$, $\lambda_2=3.0$(interaction), $\lambda_3=2.0$(encoder)로 둔다. 추론할 때는 softmax scoring과 greedy thresholding, multi-class NMS를 거쳐 남은 검출에만 interaction module을 적용한다.

## 실험 결과 / 연구 의의
여러 벤치마크에서 mAP를 20%p 넘게 끌어올리며 state-of-the-art를 기록했다.

| 벤치마크 | 지표 | HOI-DETR | 비교 대상 |
|---|---|---|---|
| Refined Hands23 | 전체 mAP | 86.1 | 63.6 (baseline) |
| Refined Hands23 | 1st object mAP | 86.5 | +25p |
| Refined Hands23 | 2nd object mAP | 78.7 | - |
| Refined Hands23 | interaction F1 | 95.5 | - |
| HD-EPIC-HOI (신규 비디오 벤치마크) | Frame-AP | 72.6 | 46.9 (Hands23) |
| HD-EPIC-HOI (신규 비디오 벤치마크) | Video-AP | 60.2 | 16.1 (HOIST) |
| HD-EPIC-HOI (신규 비디오 벤치마크) | LTC | 61.0 | 27.2 (HOIST) |
| FineBio (out-of-distribution) | 전체 mAP | 71.2 | 50.2 (baseline) |
| FineBio (out-of-distribution) | 1st object mAP | 55.8 | +29.8p |
| HOIST | 1st object mAP | 76.6 | 70.7 (HOIST) |
| Hand detection (zero-shot 평균) | AP | 82.4 | - |

- **Hand detection 일반화**: HOI에 맞춰 최적화했는데도 6개 데이터셋 중 4개에서 hand-only 검출 최고 성능을 냈다(평균 zero-shot 82.4 AP).

데이터셋 측면에서는 Hands23의 중복 박스를 손으로 일일이 정제했고(26.2k 이미지, 그중 56.2%가 수정 대상, 중복 박스쌍 16,208개 제거), 새 벤치마크 HD-EPIC-HOI(검증 시퀀스 768개, 35.3k 이미지, 1st object 주석 22.2k개, SAM2 마스크 전파 정확도 97.83%)를 새로 만들었다. Ablation 결과, pretraining을 빼면 mAP가 33.4 떨어지고 encoder를 동결하면 14.5 떨어졌으며, 학습형 MLP가 IoU 휴리스틱보다 낫고(1st→2nd에서 F1 +19.2%), end-to-end 학습이 따로따로 학습하는 방식보다 나았다(hand→1st +14.4%, 1st→2nd +19.1%). 이렇게 각 설계 선택의 근거를 하나씩 입증했다. 요컨대 역할 기반의 상호작용 인식 transformer 검출과 믿을 수 있는 데이터·평가를 갖추면 HOI 성능이 크게 오른다는 것이 이 논문의 메시지다.

## 한계
논문이 직접 밝힌 실패 사례와 한계는 다음과 같다.
- 작거나 길쭉한 물체에서는 같은 물체를 중복 검출한다.
- 빠르게 움직이면 motion blur(움직임 흐림) 때문에 검출을 놓친다.
- 조명이나 색이 비슷하면 손과 1st object를 헷갈린다.
- 실제로 닿지 않았는데 공간적으로 가까이 있는 물체를 false positive로 잡는다(세밀한 연결 판단이 어렵다).
- 복잡한 양손(bimanual) 상호작용이나 many-to-many 상호작용을 제대로 평가할 벤치마크가 없다(모델은 여러 물체나 악수 같은 복잡한 상황도 처리하지만, 이를 평가할 자원이 부족하다).

## 우리 연구와 연결되는 점
- **Hand-Object Interaction**: 이 논문의 핵심 주제라 곧바로 연결된다. 손-물체와 물체-물체(도구 매개) 관계를 역할 기반으로 모델링하는 방식, 그리고 프레임/비디오 평가 프로토콜을 HOI 연구의 baseline이자 평가 기준으로 그대로 가져다 쓸 수 있다.
- **Egocentric Vision**: HD-EPIC-HOI에 egocentric 시퀀스가 들어 있고 평가 스위트가 egocentric과 exocentric을 모두 아우르므로, 1인칭 시점 상호작용 검출·추적 연구와 이어진다.
- **Spatial Audio**: 논문에서 직접 언급하지는 않는다. 다만 손-물체 접촉 시점(contact start/end)과 시공간 tube 정보를 오디오 이벤트에 맞춰 정렬하는 audio-visual 확장은 충분히 시도해 볼 만하다.

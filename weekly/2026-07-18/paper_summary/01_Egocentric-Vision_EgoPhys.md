# EgoPhys: Learning Generalizable Physics Models of Deformable Objects from Egocentric Video

**arXiv**: 2606.16202 | **주제 분류**: Egocentric Vision | **출판일**: 2026-06-15 | **학회**: 프리프린트
**저자/소속**: Hyunjin Kim, Ri-Zhao Qiu, Guangqi Jiang, Xiaolong Wang (UC San Diego)
**링크**: https://arxiv.org/abs/2606.16202

## 한 줄 요약
사람이 물체를 직접 만지며 촬영한 1인칭(egocentric) RGB 영상 한 편만으로 변형 물체(deformable object, 형태가 바뀌는 물체)의 물리적 디지털 트윈(physical digital twin, 실제 물체의 물리 거동을 그대로 재현하는 가상 모델)을 만들고, 코드북(codebook) 기반 물리 프라이어를 통해 처음 보는 물체에도 스프링별 재최적화 없이 곧바로 적용되는 물리 모델을 학습하는 프레임워크다.

## 메인 그림
![1인칭 상호작용 영상 한 편에서 재사용 가능한 물리 프라이어를 학습해, 처음 보는 변형 물체의 스프링 강성 필드를 촘촘하게(dense) 예측하는 EgoPhys 파이프라인](https://arxiv.org/html/2606.16202v1/x1.png)

## 선행 연구
로봇이 옷, 수건, 인형 같은 변형 물체를 다루려면 힘을 받았을 때 어떻게 변형될지 예측하는 세계 모델(world model)이 필요하다. 기존 연구는 크게 두 갈래로 나뉜다. (1) 생성 모델(generative model) 기반 방법은 시각적으로 그럴듯한 미래 영상을 만들어낸다. (2) 물리 기반(physics-based) 방법은 스프링-질량(spring-mass) 그래프 같은 명시적 물리 모델을 데이터에 맞춰, 해석이 가능하고 행동 조건부(action-conditioned) 예측까지 되는 트윈을 만든다. 이 논문은 후자를 대표하는 [PhysTwin](https://arxiv.org/abs/2503.17973), [Spring-Gaus](https://arxiv.org/abs/2403.09434) 계열을 토대로 삼는다.

## 문제 제기
기존 방법은 관측 조건과 일반화라는 두 측면에서 한계를 보인다. (1) 생성 모델은 명시적 물리가 없어 해석이 어렵고 행동 조건부 예측도 힘들다. (2) 물리 기반 방법은 미리 스캔한 기하 정보, 깨끗한 포인트 클라우드, depth 센싱과 정밀 캘리브레이션까지 갖춘 통제된 3인칭(third-person) 촬영을 요구하고, 대부분 강체(rigid, 형태가 변하지 않는 물체)나 관절체(articulated)에만 적용된다. 게다가 물체마다 스프링별(per-spring) 테스트 타임 최적화를 다시 돌려야 해서 비용이 크고 새로운 물체로는 일반화되지 않는다. 이 때문에 사람이 물체를 자연스럽게 다루며 남기는 흔한 데이터, 즉 웨어러블 카메라 영상을 그대로 쓰지 못하고, 변형 물체 조작을 위한 확장 가능한 world model을 확보하기도 어렵다.

## 연구 주제
이 논문은 "사람이 물체를 다루며 자연스럽게 촬영한 데이터만으로 변형 물체의 물리 트윈을 만들 수 있는가?"라는 질문을 던진다. 다시 말해 카메라가 흔들리고 손이 물체를 자주 가리는(hand-object occlusion, 손이 물체를 가려 안 보이는 현상) 1인칭 RGB 영상 한 편이라는 열악한 조건에서 물리 파라미터를 복원하고, 나아가 물체마다 다시 최적화하지 않고도 처음 보는 물체에 바로 적용되는(zero-shot) 물리 프라이어를 학습하는 것이 목표다. 통제된 다중 시점과 depth 환경을 전제하고 물체별 최적화에 의존하던 기존 물리 기반 방법과 달리, 이 논문은 egocentric RGB만 쓰는 입력과 재사용 가능한 재질 프라이어라는 두 축을 새롭게 내세운다.

## 연구 방법
전체 파이프라인은 세 단계로 이뤄진다.

1. **Egocentric 4D 재구성(Reconstruction)**: 입력은 웨어러블 카메라(Meta Project Aria)로 찍은 RGB 프레임 시퀀스 한 편이다. [VGGT](https://arxiv.org/abs/2503.11651)로 3D로 끌어올리고, [CoTracker3](https://arxiv.org/abs/2410.11831)로 추적하고, Grounded-SAM2로 세그멘테이션을 한 뒤 confidence 필터링과 기하 완성을 거친다. 이 과정에서 카메라 움직임과 손-물체 가림을 처리해 시간적으로 일관된(temporally coherent) 4D 포인트 클라우드를 얻는다.

2. **물체별 물리 초기화(Per-Object Physics Initialization)**: 재구성한 포인트 클라우드를 입력으로 받아 물체를 스프링-질량 그래프로 나타내고, CMA-ES(covariance matrix adaptation evolution strategy)로 피팅한다. 기하와 모션의 불일치를 최소화해 그래프 토폴로지와 전역 물리 파라미터의 대략적인(coarse) 추정값을 얻는다.

3. **코드북 기반 물리 프라이어(Codebook-Based Physics Prior)**: 정적 그래프 특징과 동적 변형 특징을 입력받아, 인장과 압축(tension/compression)에 각각 대응하는 두 프로토타입 뱅크 $C^{+}, C^{-}$에 대한 soft assignment를 거쳐 스프링마다 촘촘한(dense) 강성(stiffness) 값을 내놓는다. 코드북은 여러 물체에 걸쳐 학습하는데, 물체별 역물리(inverse-physics) 해를 dense log-stiffness 목표로 삼는 증류(distillation) 손실에 롤아웃(rollout) 재구성 손실과 모션 손실을 더해 함께 최적화한다. 테스트 타임에는 CMA로 대략 초기화한 뒤 코드북이 스프링별 그래디언트 정제 없이 dense 강성을 곧바로 예측하므로, 비싼 물체별 최적화를 없애고 처음 보는 물체에도 zero-shot으로 일반화할 수 있다.

## 실험 결과 / 연구 의의
- **데이터셋**: 인형, 수건, 천, 가방 등 변형 물체를 들기, 당기기, 밀기, 접기(lifting, pulling, pushing, folding)하는 동작을 담은 19개 egocentric 상호작용 시퀀스(각 약 7초). 학습 8개, held-out 평가 11개로 7:3 시간 분할(temporal train/test split)을 썼다.
- **베이스라인**: egocentric 입력에 맞게 손본 PhysTwin, Spring-Gaus.
- **평가 지표**: Chamfer distance, track error, IoU, PSNR, SSIM, LPIPS.
- **결과**: 재구성(reconstruction)과 미래 예측(future prediction) 모두에서 손본 베이스라인을 앞섰고, 특히 물리적 일관성(physical consistency) 지표에서 크게 개선됐다. 처음 보는 물체로의 zero-shot 일반화도 이뤄냈으며, ablation 실험에서 코드북 설계가 MLP를 바로 쓰는 방식보다 낫다는 점을 확인했다.
- **연구 의의**: 학습한 트윈을 실제 xArm6 매니퓰레이터에 sim-to-real로 옮겨, 변형 물체 계획(planning)을 위한 world model로 쓸 수 있음을 실제로 보였다. 통제된 촬영 없이 사람의 자연스러운 1인칭 영상만으로 재사용 가능한 변형 물체 물리 모델을 만들 수 있다는 것을 입증한 셈이다.

## 한계
논문이 밝힌 한계는 다음과 같다. (1) 데이터셋 규모가 작다(19개 시퀀스). (2) 촬영할 때 변형이 눈에 보여야 한다(visible deformation에 의존). (3) 재구성 품질에 민감하다. (4) 매우 복잡한 재질 거동은 파라미터 공간이 넓어 다루기 어려울 수 있다. 여기에 더해, egocentric 영상 특유의 가림과 통제되지 않은 손 상호작용에서 생기는 들쭉날쭉한 접촉 기하(contact geometry)도 풀어야 할 과제로 꼽는다.

## 우리 연구와 연결되는 점
- **Egocentric Vision**: 이 연구는 웨어러블 카메라(Project Aria)로 찍은 RGB 영상 한 편에서 손-물체 가림과 카메라 움직임을 처리하며 4D 구조를 복원하는 파이프라인(VGGT, CoTracker3, Grounded-SAM2)을 제시한다. 따라서 egocentric 영상에서 물리적으로 의미 있는 3D/4D 표현을 뽑아내려는 연구에 곧바로 참고가 된다.
- **Hand-Object Interaction**: 사람이 물체를 만져 변형시키는 상호작용을 물리 파라미터(강성 필드) 추정의 단서로 삼는다. 이 점에서 HOI를 단순한 자세나 접촉 인식을 넘어 물체의 물리적 성질을 추론하는 쪽으로 넓히는 관점과 이어질 여지가 있다.
- **Spatial Audio**: 논문에 직접 언급된 내용은 없다. 다만 접촉이나 변형 이벤트를 오디오 같은 다른 모달리티로 보강해, 가림이 심한 상황에서의 물리 추정을 개선하는 방향으로 활용해 볼 여지를 상상해 볼 수 있다.

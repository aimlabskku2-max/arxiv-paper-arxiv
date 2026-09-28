# MAND: Modality-Aware Novelty Detection for Open-World Egocentric Activity Recognition

**arXiv**: 2603.16970 | **주제 분류**: Egocentric Vision · Anomaly | **출판일**: 2026-03-17 | **학회**: 프리프린트 (arXiv, Comments 란에 발표처 표기 없음)
**저자/소속**: Hyejeong Im, Wonseon Lim, Dae-Won Kim (abs 페이지에 소속 미기재)
**링크**: https://arxiv.org/abs/2603.16970

## 한 줄 요약

1인칭 영상과 관성 센서를 함께 쓰는 활동 인식 모델이 처음 보는 활동(novel activity)을 걸러낼 때, 지금까지처럼 합쳐진 logit 하나만 보지 말고 각 modality가 따로 내는 증거를 신뢰도에 따라 가중해서 쓰자는 것이 MAND의 제안이다.

## 메인 그림

![학습 단계의 MoRST(모달리티별 head + logit distillation)와 추론 단계의 MoAS(신뢰도 기반 가중 합산 + 두 가지 페널티)로 구성된 MAND 전체 파이프라인](https://arxiv.org/html/2603.16970v2/overview.png)

Figure 2. 위쪽(MoRST, 학습): modality마다 별도의 head를 두어 per-modality logit을 만들고, replay 데이터로 modality별 logit distillation을 걸어 각 modality의 결정 경계가 task를 넘어가며 무너지지 않게 붙잡아 둔다. 아래쪽(MoAS, 추론): replay에서 뽑은 reference logit과의 거리로 modality별 신뢰도를 재고, 그 가중치로 modality logit을 main fused logit에 더한 뒤 deviation·disagreement 페널티를 빼서 최종 novelty score를 만든다.

## 선행 연구

1인칭(egocentric) 활동 인식은 착용형 카메라가 찍은 영상에 손목·머리의 움직임을 재는 IMU(inertial measurement unit, 자이로스코프와 가속도계를 묶은 관성 센서)를 함께 넣는 방향으로 발전해 왔다. RGB는 "무엇이 보이는가"라는 공간적 단서를, IMU는 "몸이 어떻게 움직이는가"라는 운동학적 단서를 주기 때문에 둘은 서로를 보완한다. 이런 시각-관성 융합은 UTD-MHAD(Chen et al., 2015), Berkeley MHAD(Ofli et al., 2013) 같은 초기 데이터셋에서부터 오래 연구된 흐름이고, 이후 EPIC-KITCHENS, Ego4D, ActionSense, Project Aria 같은 대규모 1인칭 데이터셋이 나오면서 본격화됐다.

여기에 continual learning(연속 학습, 새 클래스가 시간 순서대로 계속 들어오는 상황에서 모델을 갱신하는 문제)이 붙은 것이 MMEA-CL 계열이다. UESTC-MMEA-CL(Xu et al., TMM 2024)이 멀티모달 1인칭 연속 학습 벤치마크를 처음 제시했고, LwF, EWC, iCaRL 같은 고전적 연속 학습 기법이 베이스라인으로 함께 평가됐다. 이후 연구들은 주로 modality 간 불균형을 다뤘다. CMR-MFN은 확장 가능한 구조와 confusion mixup 정규화로 변해 가는 cross-modal 상관관계를 모델링했고, AID는 vision-sensor attention으로 센서 특징을 보강했으며, FGVIR은 modality imbalance를 줄여 장기 학습에서 더 일반화되는 표현을 얻으려 했다.

한편 "모르는 것을 모른다고 말하는" 쪽에는 별개의 계보가 있다. OOD(out-of-distribution, 학습 때 본 적 없는 분포에서 온 입력) 탐지의 표준 스코어들, 즉 [MSP](https://arxiv.org/abs/1610.02136)(softmax 최대 확률), MaxLogit, Entropy, Energy가 그것이다. 여기에 open-world recognition(Bendale & Boult, 2015)과 연속 학습을 합친 OWCL(Open-World Continual Learning) 흐름이 있다. Kim et al.(2025)은 novelty detection이 안정적인 class-incremental learning의 전제 조건임을 이론적으로 정리했고, Joseph et al.은 contrastive clustering으로 미지 객체를 찾았으며, MORE와 SHELS는 표현 분리(disentanglement)로, Pro-KT는 prototype 진화를 통한 open-world 지식 전이로 접근했다.

이 두 흐름을 처음 잇는 것이 MONET(Chee et al., ICCVW 2025)이다. MONET은 멀티모달 1인칭 환경에서 online replay, pseudo-OOD 기반 동적 임계값, EMA distillation을 결합해 OWCL을 시도했고, 이 논문에서 가장 직접적인 비교 대상이 된다.

## 문제 제기

기존 MMEA-CL 방법들은 거의 전부 closed-world 가정 위에 서 있다. 즉 테스트 시점에 등장하는 것은 이미 배운 클래스뿐이라고 본다. 그러나 실제 착용형 기기가 하루 종일 켜져 있는 상황에서 들어오는 1인칭 스트림에는 학습 라벨 공간에 없는 행동이 자연스럽게 섞인다. 모델이 그것을 아는 클래스 중 하나로 우겨 넣으면, 그 잘못된 예측이 그대로 다음 단계 학습에 흘러 들어가 오류가 누적된다.

OWCL로 넘어온 MONET조차 한 가지 결정적인 지점을 남겨 뒀다. novelty를 매길 때 오직 main fused logit, 즉 여러 modality를 합친 뒤 나오는 최종 출력 하나만 본다는 점이다. 문제는 이 fused logit이 사실상 RGB에 의해 끌려간다는 것이다. 논문의 Figure 1이 보여주는 관찰이 그 근거인데, 모든 modality를 다 쓴 ER(All)의 task별 평균 AUC 곡선이 RGB만 쓴 베이스라인 곡선을 거의 그대로 따라간다. modality를 세 개 넣었는데 성능 곡선이 RGB 하나짜리와 겹친다는 것은, IMU가 들어오긴 했지만 최종 판단에 실질적으로 기여하지 못하고 있다는 뜻이다.

이 불균형은 시간이 갈수록 나빠진다. catastrophic forgetting(새 task를 배우면서 이전 task 지식이 지워지는 현상)이 쌓이면 상대적으로 약한 modality의 표현부터 먼저 무너지기 때문이다. 결국 task 순서가 길어질수록 IMU의 기여도는 더 줄고, novelty 판정은 점점 RGB 단독 판정에 가까워진다. Table 1의 long sequence(2클래스씩 증가) 열에서 모든 베이스라인의 AUC가 short sequence 대비 눈에 띄게 떨어지는 것이 그 결과다.

왜 이것이 중요한가. 1인칭 활동에서 RGB와 IMU는 서로 다른 종류의 이상(novelty)에 민감하다. 낯선 물체가 시야에 들어오는 상황은 RGB가 잘 잡지만, 같은 장면에서 손이 평소와 다른 궤적으로 움직이는 상황은 IMU에만 흔적이 남는다. RGB에 지배된 스코어는 후자를 통째로 놓친다. 특히 FPR95(true positive rate 95%에서의 false positive rate, 즉 아주 엄격한 동작점에서 novel을 known으로 잘못 받아들이는 비율)로 보면 베이스라인들은 60~80%대에 머문다. 놓친 novel이 그대로 known 버퍼로 들어간다는 뜻이라 실사용에서는 치명적이다.

## 연구 주제

이 논문이 새로 정의하는 관점은 "modality-aware novelty detection"이다. OWCL을 멀티모달 1인칭으로 확장하는 것 자체는 MONET이 먼저 했으므로, MAND가 강조하는 차이는 novelty score를 **어느 신호로부터 만드느냐**에 있다. 기존 방식이 fused logit 하나를 스코어 함수에 통과시키는 단일 창구였다면, MAND는 main fused logit과 modality별 logit을 모두 증거로 취급하고, 샘플마다 어느 증거를 얼마나 믿을지를 그 자리에서 정한다.

두 번째 차이는 "modality-wise forgetting"을 명시적 학습 대상으로 올린 점이다. 기존 연속 학습 기법들의 distillation은 대체로 최종 출력 수준에서 작동한다. 그러면 fused logit은 보존되지만 개별 modality의 판별력이 유지된다는 보장은 없다. MAND는 각 modality head의 logit을 따로 보존 대상으로 삼는다.

세 번째는 문제를 평가하는 축을 둘로 분리해 본다는 점이다. novel activity를 잘 걸러내는 능력(AUC, FPR95)과 known class를 계속 잘 맞추는 능력(ACC, FGT)은 서로 상충하기 쉬운데, 논문은 두 축을 함께 올리는 것을 목표로 잡는다.

## 연구 방법

**문제 설정.** 학습자는 class-incremental task의 스트림 $\{D_t\}_{t=1}^{T}$를 순서대로 받는다. task마다 새 클래스가 추가되어 라벨 공간이 $Y_0 \subset Y_1 \subset \cdots \subset Y_T$로 커진다. 각 샘플은 세 modality $x = \{x_{rgb}, x_{gyro}, x_{acce}\}$로 이루어지고, 학습이 끝난 뒤 테스트 샘플은 현재 알고 있는 $Y_t$에 속할 수도, 그 바깥의 novel class일 수도 있다.

**구조.** modality encoder $F_m(\cdot)$이 임베딩 $f_m = F_m(x_m)$을 만들고, fusion module $G(\cdot)$이 이를 모아 $f_{main} = G(\{f_m\})$을 만들며, main classifier $C(\cdot)$이 $z_{main} = C(f_{main})$을 낸다. 여기에 MAND는 modality마다 별도의 head $H_m(\cdot)$을 두어 $z_m = H_m(f_m)$을 뽑는다. 이 modality-specific logit이 novelty scoring과 표현 안정화 양쪽에 재사용되는 핵심 재료다. 구현상 RGB는 ImageNet으로 사전학습한 BN-Inception, IMU는 짧고 긴 움직임 동역학을 함께 잡기 위한 DeepConvLSTM, 융합은 TBN(Temporal Binding Network)을 쓴다.

**MoAS (추론 시 modality 인지 적응 스코어링).** 출발점은 fused logit이 confidence 높은 한 modality에 지배되면 나머지 증거가 눌려 known-novel 분리도가 떨어진다는 관찰이다. MoAS는 replay 메모리 $R$의 exemplar를 현재 modality head에 통과시켜 reference logit 집합 $L_m$을 만들고, 입력의 modality logit이 이 집합에서 얼마나 떨어져 있는지로 신뢰도를 잰다. 정규화된 최근접 거리는

$$\tilde{d}_m(x) = \frac{\min_{v \in L_m} \lVert z_m(x) - v \rVert_2 - \mu_m}{\sigma_m}$$

이고, $\mu_m, \sigma_m$은 $L_m$ 내부 leave-one-out 거리의 평균과 표준편차다. 가까울수록(= 그 modality가 지금 이 샘플에 대해 익숙한 영역에 있을수록) 큰 가중치를 받도록 온도 $\tau$의 softmax를 씌운다.

$$\alpha_m(x) = \frac{\exp(-\tilde{d}_m(x)/\tau)}{\sum_{j \in M} \exp(-\tilde{d}_j(x)/\tau)}$$

최종 logit은 main에 가중된 modality logit을 더해 만든다.

$$z_{final,c}(x) = z_{main,c}(x) + \sum_{m \in M} \alpha_m(x)\, z_{m,c}(x)$$

여기에 두 가지 페널티가 붙는다. 하나는 known 분포에서 얼마나 벗어났는지를 재는 deviation penalty

$$P(x) = \frac{1}{|M|}\sum_{m \in M} \max(0, \tilde{d}_m(x))$$

이고, 다른 하나는 modality들의 예측이 서로 얼마나 엇갈리는지를 재는 disagreement penalty다. 평균 예측 분포 $\bar{q}(x) = \frac{1}{|M|+1}[q_{main}(x) + \sum_m q_m(x)]$에 대해

$$D_{KL}(x) = \frac{1}{|M|+1}\Big[KL(q_{main}(x)\,\Vert\,\bar{q}(x)) + \sum_{m \in M} KL(q_m(x)\,\Vert\,\bar{q}(x))\Big]$$

이다. 직관적으로는 "모두가 다른 말을 하고 있으면 그건 아마 처음 보는 행동"이라는 신호를 스코어에 넣는 것이다. 최종 novelty score는

$$s_{MoAS}(x) = \max_c z_{final,c}(x) - \eta P(x) - \gamma D_{KL}(x)$$

**MoRST (학습 시 modality 인지 표현 안정화).** 지도 손실은 main과 각 modality head를 함께 학습시킨다.

$$L_{Sup} = L_{CE}(z_{main}, y) + \lambda \cdot \frac{1}{|M|}\sum_{m \in M} L_{CE}(z_m, y)$$

여기에 replay exemplar에 대해 이전 모델의 modality logit $\tilde{z}_m$을 현재 모델이 따라가도록 modality별 distillation을 건다.

$$L_{KD} = \sum_{m \in M} \lVert \tilde{z}_m - z_m \rVert_2^2$$

최종 목적함수는 $L = L_{Sup} + \beta L_{KD}$다. 핵심은 distillation이 fused 출력이 아니라 **modality별 출력**에 걸린다는 점이고, 그래야 MoAS가 추론 때 기대는 modality logit 공간이 task를 건너가며 일관되게 유지된다. 두 모듈은 이렇게 짝을 이룬다.

**하이퍼파라미터.** $\lambda = 0.4$, $\beta = 0.005$, $\tau = 3$, $\eta = 3$, $\gamma = 4$. replay buffer는 모든 replay 기반 방법에 대해 320으로 고정했고, RGB encoder는 SGD, IMU encoder는 RMSProp으로 학습률 0.001에서 시작해 task마다 50 epoch, 10·20 epoch에서 학습률을 1/10로 감쇠시킨다.

## 실험 결과 / 연구 의의

**설정.** UESTC-MMEA-CL(Xu et al., 2024)에서 평가한다. RGB, 자이로스코프, 가속도계 스트림과 32개 활동 클래스로 구성된 멀티모달 1인칭 벤치마크다. task당 새로 들어오는 클래스 수를 8개(short), 4개(mid), 2개(long)로 바꿔 세 가지 class-incremental 설정을 만든다. novelty 탐지는 AUC와 FPR95로, known class 성능은 평균 정확도 ACC와 망각 정도 FGT로 잰다. 모든 수치는 5회 실행의 평균 ± 표준편차다.

**novel activity 탐지 (Table 1, 대표 행 발췌).**

| Method | Short AUC (↑) | Short FPR95 (↓) | Mid AUC (↑) | Mid FPR95 (↓) | Long AUC (↑) | Long FPR95 (↓) |
|---|---|---|---|---|---|---|
| iCaRL + MSP | 85.92 ± 0.84 | 57.86 ± 2.15 | 84.51 ± 0.68 | 63.83 ± 1.68 | 81.33 ± 0.86 | 66.60 ± 2.39 |
| iCaRL + Entropy | 85.69 ± 0.85 | 55.35 ± 1.68 | 85.02 ± 0.64 | 60.43 ± 1.36 | 81.75 ± 0.67 | 63.94 ± 2.36 |
| ER + MaxLogit | 86.37 ± 0.79 | 57.55 ± 5.18 | 85.06 ± 0.90 | 62.51 ± 3.03 | 82.02 ± 1.01 | 67.02 ± 1.32 |
| DER++ + Entropy | 82.67 ± 1.01 | 60.36 ± 2.52 | 82.33 ± 1.09 | 67.02 ± 2.53 | 78.99 ± 0.71 | 71.03 ± 1.00 |
| Foster + Entropy | 84.14 ± 0.76 | 58.67 ± 0.52 | 81.39 ± 0.49 | 66.78 ± 1.03 | 77.21 ± 0.45 | 71.55 ± 1.41 |
| CMR-MFN + MaxLogit | 79.40 ± 0.33 | 70.60 ± 1.39 | 73.29 ± 0.63 | 81.25 ± 1.77 | 63.34 ± 0.85 | 84.59 ± 1.40 |
| MONET + Entropy | 84.81 ± 0.26 | 57.77 ± 1.30 | 83.73 ± 0.61 | 64.64 ± 0.73 | 80.43 ± 0.57 | 66.90 ± 1.78 |
| **MAND (Ours)** | **89.43 ± 0.70** | **44.93 ± 2.78** | **89.59 ± 1.17** | **47.62 ± 4.27** | **86.02 ± 1.36** | **55.31 ± 3.50** |

논문은 이를 "설정·지표별 최고 베이스라인 대비 평균 AUC 4.5% 향상, FPR95 17.8% 감소"로 정리한다. FPR95 쪽 개선이 특히 의미 있다고 강조하는데, 엄격한 동작점에서 novel 활동이 known으로 잘못 받아들여지는 경우가 그만큼 줄었다는 뜻이기 때문이다. 흥미로운 대비는 CMR-MFN이다. 멀티모달 융합을 정교하게 설계한 방법인데 novelty 지표에서는 오히려 크게 무너져(long sequence AUC 63.34), 분류를 위한 융합 설계가 곧 novelty 분리로 이어지지 않는다는 점을 보여 준다. MONET도 MAND에 비하면 일반적인 replay 베이스라인과 큰 차이를 내지 못한다.

**스코어링 전략만 바꿔 본 비교 (Table 2).**

| Scoring Strategy | Short AUC (↑) | Short FPR95 (↓) | Mid AUC (↑) | Mid FPR95 (↓) | Long AUC (↑) | Long FPR95 (↓) |
|---|---|---|---|---|---|---|
| Main Only ($\alpha_m = 0$) | 86.82 ± 1.22 | 53.10 ± 4.37 | 87.01 ± 1.10 | 54.67 ± 3.83 | 83.50 ± 1.29 | 62.19 ± 1.71 |
| Uniform ($\alpha_m = 1/|M|$) | 87.17 ± 1.09 | 50.00 ± 3.59 | 87.77 ± 1.15 | 51.13 ± 2.54 | 84.50 ± 1.07 | 59.02 ± 1.90 |
| **MoAS (Ours)** | **89.43 ± 0.70** | **44.93 ± 2.78** | **89.59 ± 1.17** | **47.62 ± 4.27** | **86.02 ± 1.36** | **55.31 ± 3.50** |

이 표가 논문의 논지를 가장 깔끔하게 지지한다. Uniform이 Main Only를 이긴다는 것은 modality logit에 fused logit 너머의 보완 정보가 실제로 남아 있다는 증거이고, MoAS가 Uniform을 다시 이긴다는 것(평균 AUC +2.2%, FPR95 −7.7%)은 그 정보를 **샘플마다 다르게** 가중해야 효과가 커진다는 뜻이다. Figure 3의 스코어 분포에서도 Main Only와 Uniform은 known과 novel이 여전히 겹치는 반면 MoAS는 분리가 뚜렷하다.

**known class 성능 (Table 3).** novelty만 잘 잡고 본업을 놓치면 의미가 없는데, MAND는 양쪽을 동시에 올린다.

| Method | Short ACC (↑) | Short FGT (↓) | Mid ACC (↑) | Mid FGT (↓) | Long ACC (↑) | Long FGT (↓) |
|---|---|---|---|---|---|---|
| iCaRL | 85.96 ± 0.56 | 16.04 ± 0.93 | 82.90 ± 0.61 | 17.48 ± 0.83 | 78.85 ± 0.91 | 20.71 ± 1.11 |
| ER | 84.76 ± 1.29 | 17.56 ± 1.49 | 82.13 ± 1.66 | 18.61 ± 1.80 | 77.92 ± 0.91 | 21.85 ± 1.15 |
| DER++ | 81.84 ± 1.21 | 20.00 ± 1.52 | 79.16 ± 1.02 | 20.92 ± 1.45 | 75.15 ± 1.59 | 24.58 ± 1.59 |
| Foster | 79.48 ± 1.38 | 24.70 ± 1.92 | 73.16 ± 1.23 | 28.57 ± 1.53 | 67.66 ± 2.04 | 32.79 ± 2.10 |
| CMR-MFN | 75.25 ± 1.40 | 13.16 ± 1.31 | 61.28 ± 1.41 | 14.10 ± 1.11 | 26.40 ± 2.07 | 22.25 ± 1.91 |
| MONET | 85.26 ± 1.21 | 17.03 ± 1.33 | 82.29 ± 1.04 | 18.42 ± 1.18 | 78.83 ± 1.01 | 21.01 ± 1.02 |
| **MAND (Ours)** | **86.72 ± 1.03** | **15.68 ± 1.14** | **85.11 ± 1.14** | **15.39 ± 1.25** | **81.29 ± 1.45** | **18.55 ± 1.36** |

CMR-MFN의 FGT가 낮게 나오는 것은 망각을 잘 막아서가 아니라 애초에 ACC가 매우 낮아(long sequence 26.40) 잃을 것이 적기 때문이라는 점은 읽을 때 주의해야 한다.

**모듈 제거 실험 (Table 4).**

| Method | Short FPR95 (↓) | Short ACC (↑) | Mid FPR95 (↓) | Mid ACC (↑) | Long FPR95 (↓) | Long ACC (↑) |
|---|---|---|---|---|---|---|
| MAND (전체) | 44.93 ± 2.78 | 86.72 ± 1.03 | 47.62 ± 4.27 | 85.11 ± 1.14 | 55.31 ± 3.50 | 81.29 ± 1.45 |
| w/o MoRST | 45.66 ± 2.39 | 86.20 ± 0.93 | 51.14 ± 3.23 | 83.71 ± 1.55 | 57.14 ± 3.48 | 81.02 ± 1.48 |
| w/o MoAS | 53.10 ± 4.37 | 86.72 ± 1.03 | 54.67 ± 3.83 | 85.11 ± 1.14 | 62.19 ± 1.71 | 81.29 ± 1.45 |
| w/o MoAS & MoRST | 57.55 ± 5.18 | 84.76 ± 1.29 | 62.51 ± 3.03 | 82.13 ± 1.66 | 67.02 ± 1.32 | 77.92 ± 0.91 |

MoAS를 빼면 FPR95가 가장 크게 나빠지므로 탐지 성능의 주된 출처는 추론 쪽 스코어링이다. 반대로 MoRST는 ACC와 FGT, 즉 학습 안정성 쪽에 기여한다(mid sequence ACC 85.11 → 83.71). 그리고 MoRST 제거 시의 FPR95 악화 폭이 task 스트림이 길어질수록 커진다는 점(short 0.73%p, mid 3.52%p, long 1.83%p)은 modality 표현이 오래 유지되어야 MoAS의 거리 기반 신뢰도 추정도 제대로 작동한다는 앞의 주장과 맞아떨어진다.

**MoAS 내부 제거 실험 (Table 5).** 두 페널티는 각각 독립적으로 기여한다. 둘 다 빼면 short sequence FPR95가 44.93 → 51.00, AUC가 89.43 → 87.64로 떨어지고, KL 페널티만 빼도 48.82, 거리 페널티만 빼도 47.37이 된다.

| Method | Short AUC (↑) | Short FPR95 (↓) | Mid AUC (↑) | Mid FPR95 (↓) | Long AUC (↑) | Long FPR95 (↓) |
|---|---|---|---|---|---|---|
| MoAS (전체) | 89.43 ± 0.70 | 44.93 ± 2.78 | 89.59 ± 1.17 | 47.62 ± 4.27 | 86.02 ± 1.36 | 55.31 ± 3.50 |
| w/o KL Penalty | 88.84 ± 0.74 | 48.82 ± 3.00 | 89.19 ± 0.97 | 49.96 ± 2.88 | 85.73 ± 1.25 | 57.06 ± 2.55 |
| w/o Distance Penalty | 88.30 ± 1.05 | 47.37 ± 3.12 | 88.98 ± 1.19 | 47.88 ± 2.90 | 85.50 ± 1.23 | 56.53 ± 3.13 |
| w/o Distance & KL | 87.64 ± 1.12 | 51.00 ± 4.16 | 88.50 ± 1.01 | 50.27 ± 2.37 | 85.14 ± 1.14 | 58.47 ± 2.07 |

**의의.** 논문이 결론에서 내세우는 메시지는 간명하다. 멀티모달 1인칭 OWCL에서는 modality별 증거를 **보존하고(MoRST) 활용하는 것(MoAS)** 이 중요하다. 실무적으로 매력적인 점은 MoAS가 추론 시점 모듈이라 이미 학습된 멀티모달 모델 위에 비교적 가볍게 얹을 수 있다는 것이고, 별도의 OOD 학습 데이터나 외부 novel 샘플 없이 replay 버퍼만으로 신뢰도 기준을 세운다는 점이다.

## 한계

논문이 직접 밝힌 한계는 두 가지다. 첫째, modality-specific head와 저장해 두는 per-modality logit 때문에 추가 메모리 비용이 든다. 착용형 기기처럼 자원이 빠듯한 환경을 겨냥한 연구인데 메모리를 더 쓴다는 점은 그 자체로 긴장 관계를 만든다. 둘째, task 스트림이 길어질수록 replay의 품질에 성능이 의존할 수 있다. MoAS의 reference logit 집합 $L_m$이 exemplar에서 나오기 때문에, 버퍼가 클래스 분포를 제대로 대표하지 못하면 거리 기반 신뢰도 추정 자체가 흔들린다. 향후 방향으로는 더 메모리 효율적인 안정화 기법과, 센서 가용성이 바뀌거나 분포 변화가 더 심한 폭넓은 멀티모달 환경을 든다.

논문에 명시적 언급은 없지만 읽으면서 드러나는 제약도 있다. 평가가 UESTC-MMEA-CL 단일 벤치마크에 국한되고 32개 클래스 규모라, Ego4D급의 장시간·비정형 1인칭 스트림으로 갈 때 결론이 유지될지는 확인되지 않았다. 또 $\tau, \eta, \gamma, \lambda, \beta$ 다섯 개 하이퍼파라미터가 고정값으로 주어지는데, 이 값들을 어떤 검증 절차로 골랐는지와 설정별 민감도가 본문 범위에서는 보이지 않는다. novelty score가 replay 버퍼에 의존한다는 구조상, 버퍼 크기 320을 줄였을 때의 거동도 열린 질문이다. 마지막으로 이 설정의 "novelty"는 어디까지나 학습 라벨 공간 밖의 **정상적인 다른 활동**이며, 넘어짐이나 사고 같은 진짜 이상 사건(anomaly)과는 성격이 다르다.

## 우리 연구와 연결되는 점

가장 직접적인 접점은 egocentric anomaly detection이다. 이 논문의 novelty는 "라벨 공간 밖 클래스"이지 "위험하거나 비정상적인 사건"은 아니지만, 스코어링 구조 자체는 이상 탐지로 거의 그대로 옮겨진다. 특히 MoAS의 disagreement penalty $D_{KL}$은 이상 탐지 맥락에서 매력적인 발상이다. 넘어짐, 물건을 놓침, 갑작스러운 자세 붕괴 같은 사건은 영상에서는 평범한 실내 장면으로 보이지만 IMU에는 강한 흔적을 남긴다. 즉 modality 사이의 **불일치 자체가 이상의 신호**가 되는 전형적인 경우다. 반대로 본 적 없는 물체를 다루는 상황은 RGB만 반응한다. 두 종류를 하나의 스코어로 잡으려면 이 논문처럼 modality 간 엇갈림을 명시적으로 스코어에 넣는 설계가 필요하다.

RGB 지배(RGB dominance) 문제의 진단 방식도 우리 쪽에 그대로 쓸 수 있는 도구다. Figure 1에서 "전체 modality를 쓴 모델의 곡선이 RGB 단독 베이스라인 곡선과 겹치는가"를 보는 것은 아주 값싼 진단이다. 우리가 1인칭 이상 탐지나 멀티모달 파이프라인을 만들 때, 센서를 넣었다는 사실만으로 그것이 실제로 쓰이고 있다고 가정하지 말고 이런 곡선 비교를 sanity check로 넣어 볼 만하다.

Spatial Audio, 특히 착용형 기기의 공간 음향으로 확장해 보면 흥미로운 잠재적 관점이 나온다. 다만 이 논문은 오디오를 전혀 다루지 않으므로 어디까지나 우리 쪽 해석이라는 점을 분명히 해 둔다. 착용형 마이크 배열이 주는 binaural/ambisonic 신호는 IMU와 성격이 비슷하다. 시야 밖에서 벌어지는 일에 반응하고, RGB와 독립적인 증거를 주며, 그러면서도 fused logit에서는 눌리기 쉽다. MAND의 틀에 오디오를 네 번째 modality로 넣으면 "소리는 뒤쪽에서 무언가 떨어졌다고 말하는데 영상은 아무 일 없다고 말하는" 상황이 곧바로 높은 $D_{KL}$로 잡힌다. 시야 밖 이상 사건(off-screen anomaly)은 1인칭 특유의 문제이고 영상만으로는 원리적으로 접근이 안 되므로, 이 방향은 꽤 자연스럽다. 다만 오디오는 reference logit 분포가 환경 소음에 크게 흔들려 거리 기반 신뢰도 $\tilde{d}_m$의 정규화가 까다로울 수 있다.

egocentric hallucination(모델이 영상에 실제로는 없는 내용을 있는 것처럼 말하는 현상) 쪽으로는 연결이 조금 더 간접적이지만 시사점이 있다. hallucination의 상당수는 모델이 "모른다"를 표현할 통로가 없어 아는 것 중 가장 그럴듯한 답으로 밀어 넣는 데서 나온다. MAND가 하는 일은 정확히 그 통로를 만드는 것이다. 이를 비디오-언어 모델 맥락으로 옮기면, 답을 생성하기 전에 modality별 증거의 일치도를 재서 낮으면 abstention(답변 보류)이나 불확실성 표현으로 보내는 게이트를 둘 수 있다. 특히 착용형 어시스턴트처럼 연속 학습이 전제되는 환경에서는, 이 논문이 지적한 "시간이 갈수록 약한 modality의 표현이 먼저 무너진다"는 현상이 곧 "시간이 갈수록 hallucination이 늘어난다"로 나타날 가능성이 크다. MoRST식 modality별 distillation은 그 열화를 늦추는 실마리가 된다.

마지막으로 실용적인 이유 하나. MoAS는 추론 시점 모듈이라 backbone을 재학습하지 않고도 기존 모델 위에 얹을 수 있고, 외부 OOD 데이터 없이 replay 버퍼만으로 기준을 세운다. 우리가 이미 가진 1인칭 모델에 이상 탐지 능력을 붙여야 할 때 실험 비용이 낮은 출발점이 된다.

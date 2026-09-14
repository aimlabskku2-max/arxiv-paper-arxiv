# Single-Query Person-Centric Bimanual Hand-Object Interaction Detection

**arXiv**: 2609.12155 | **주제 분류**: Hand-Object Interaction | **출판일**: 2026-09-10 | **학회**: ECCV 2026
**저자/소속**: Jonghyun Kim, Junho Roh, Yubin Yoon, Hyotae Lee, Jongkuk Park, Taehwan Hwang, Jaechul Kim, Jungho Lee — LG전자 CTO부문 AI Lab (South Korea)
**링크**: https://arxiv.org/abs/2609.12155

## 한 줄 요약
손을 따로따로 검출하던 기존 방식 대신, **사람 한 명 = query 하나**로 묶어 사람 박스·자세·양손 박스·양손 접촉 상태·상호작용 대상까지 한 번에 예측하는 person-centric 프레임워크를 제안하고, 이를 위한 COCO 기반 데이터셋과 tuple 단위 평가 지표를 함께 만든 논문이다.

## 메인 그림
![단일 query가 사람 박스·pose·양손 박스를 동시에 내놓고, hand-to-query relation matrix로 각 손의 상호작용 대상을 검출된 query 집합에서 골라내는 전체 구조](https://arxiv.org/html/2609.12155v1/figures/oih_architecture.jpg)
Figure 2 (Model overview): backbone + transformer encoder가 top-$K$ query(+ off query)를 만들고, part-aware reference point를 쓰는 deformable decoder가 이를 정제해 detection box, body keypoint, hand box, hand-target relation을 동시에 뽑아내는 파이프라인.

보조 그림(Figure 1, 데이터셋 예시): https://arxiv.org/html/2609.12155v1/figures/oih_paper_vis.png — 사람 박스, keypoint, 좌/우 손 영역(점선), 상호작용 대상(실선)을 한 사람 단위로 묶어 annotate한 예시.

---

## 선행 연구

**Hand-object interaction(손-물체 상호작용) 이해 — hand-centric 계열**

이 분야의 주류는 "손 하나"를 예측 단위로 삼는 방식이다.

- **[100DOH](https://arxiv.org/abs/2006.06669)** (Shan et al., CVPR 2020): 손마다 (hand box, hand side(좌/우), contact state(접촉 상태), in-contact object box)를 예측한다. 인터넷 규모의 대형 데이터셋을 함께 공개해 이 분야의 표준 출력 포맷을 사실상 정의했다.
- **Hands23** (Cheng et al., NeurIPS 2023): 출력 공간을 더 넓혀 object segment(물체 분할 마스크), 도구를 통해 간접적으로 닿는 second object, grasp/contact 종류까지 예측한다.
- **ContactHands** (Narasimhaswamy et al., NeurIPS 2020): in-the-wild 환경에서 손 검출과 물리적 접촉 인식을 다룬다. 손 박스와 손 상태만 제공하고, 접촉 물체 annotation은 없다.

**Human-object interaction(HOI) detection 계열**

사람-물체 쌍과 그 사이의 action predicate(동작 술어)를 찾는 더 큰 흐름이다.

- **[HOTR](https://arxiv.org/abs/2104.13682)**, **HOI Transformer**: detection과 interaction 추론을 end-to-end set prediction 하나로 통합.
- 이후 predicate context 모델링 강화, open-vocabulary/open-world 확장(visual-semantic alignment, multi-modal prompt) 연구가 이어졌다.

**Entity set 위에서의 relation 예측**

검출된 entity(객체 query) 사이의 관계를 추론하는 scene graph generation 흐름이다.

- **[RelTR](https://arxiv.org/abs/2201.11460)**, **EGTR**: transformer object query 위에서 직접 relation을 모델링.
- 최근에는 vision-language 결합으로 닫힌 predicate 집합을 넘어서려는 시도가 있다.

**DETR 계열 detector**

- **[DETR](https://arxiv.org/abs/2005.12872)**: detection을 bipartite matching 기반 set prediction으로 재정의, NMS 같은 휴리스틱 후처리를 제거.
- **[Deformable DETR](https://arxiv.org/abs/2010.04159)**: sparse deformable attention으로 수렴 속도와 작은 물체 성능 개선.
- **[DINO](https://arxiv.org/abs/2203.03605)**: denoising 학습과 query 설계 개선.
- **[RT-DETR](https://arxiv.org/abs/2304.08069)**: 실시간 end-to-end transformer detection. 이 논문의 base detector.

---

## 문제 제기

**핵심 지적: 예측 단위(prediction unit)와 해석 단위(interpretation unit)가 어긋나 있다.**

기존 hand-centric 방법들은 손 하나하나를 **독립된 instance**로 다룬다. 그래서 좌/우 손을 "같은 사람에게 속한 한 쌍"으로 명시적으로 묶지 않는다. 이 설계가 낳는 구체적 문제는 다음과 같다.

1. **Ownership ambiguity(소유권 모호성)**: 여러 사람이 있는 장면에서 손 여러 개와 상호작용 여러 개를 다 검출해도, **어느 두 손이 같은 사람의 손인지**를 결정하지 못한다. 붐비는 장면에서 A의 왼손과 B의 오른손이 한 사람의 양손으로 잘못 묶이는 cross-person assignment가 발생할 수 있다.

2. **양손 상호작용(bi-manual interaction) 해석 불가**: "이 사람이 왼손으로 컵을 잡고 오른손으로 주전자를 들고 있다" 같은 person-level 해석은 두 손이 한 사람에 묶여야만 가능하다. 손 단위 출력만으로는 이런 구조를 복원할 수 없다.

3. **평가 지표도 이 문제를 못 잡는다**: 기존 hand-centric metric은 손 단위 검출/연관 정확도만 재기 때문에, ownership 불일치(cross-person 할당, 좌/우 슬롯 혼동)에 **아무 페널티를 주지 않는다**.

4. **데이터셋의 annotation 부족**: Table 1에서 정리하듯, 기존 hand-contact 데이터셋은 person-centric 구조 자체가 없다.

| Dataset | Person-centric | Hand box | Contact info | Object box | Object class | Human box | Body keypoint |
|---|---|---|---|---|---|---|---|
| Ours | O | O | O | O | O | O | O |
| ContactHands | X | O | O | X | X | X | X |
| 100DOH | X | O | O | O | X | X | X |
| Hands23 | X | O | O | O | X | X | X |

즉 기존 데이터셋 중 어느 것도 human box, body keypoint, object class를 함께 주지 않아, 사람 단위의 구조적 학습 자체가 불가능했다.

5. **상호작용 물체의 semantics 상실**: person query에서 상호작용 물체 박스를 **직접 regression**하면 위치는 나오지만 그 물체가 "무엇인지(class)"는 알 수 없다.

**왜 중요한가**: 어느 사람이 어느 손으로 어떤 물체를 조작하는지를 파싱하는 능력은 fine-grained action understanding, demonstration mining(사람 시연 데이터 수집), assistive perception(보조 인지), robot learning from observation(관찰 기반 로봇 학습)의 기반이 된다.

---

## 연구 주제

논문이 새로 정의하는 문제는 **person-centric bi-manual hand-object interaction detection**이다. 기존 흐름과의 차이는 세 층위로 나뉜다.

**(1) 표현(formulation)의 전환 — hand-centric → person-centric**

사람 instance를 1차 예측 단위로 삼고, 좌/우 손을 그 사람에 붙은 **두 개의 명시적 slot**으로 다룬다. Query 하나가 한 사람에 대한 구조화된 출력 전체를 담당한다:

- human box
- body pose (keypoint $\mathbf{\hat{K}}_i \in [0,1]^{J\times2}$)
- 좌/우 hand box ($\mathbf{\hat{b}}_i^L, \mathbf{\hat{b}}_i^R$)
- 좌/우 hand state (접촉 여부/유형)
- 좌/우 손 각각의 interaction target

이 구조는 person-centric pose estimation과 형태가 비슷하지만, 거기에 양손 상호작용 추론까지 붙인 확장이다.

**(2) HOI 계열과의 차이**

HOI detection도 detection과 relation을 통합하지만, 관계의 단위가 "사람-물체 쌍 + predicate"다. 이 논문은 **사람 내부의 손 단위(hand-specific)** 상호작용을 person 구조 안에서 다룬다. Scene graph generation과도 "entity set 위에서 relation을 뽑는다"는 관점은 공유하지만, 일반 predicate graph가 아니라 **각 손이 대상 하나를 고르는 compact한 selection** 문제로 좁힌다.

**(3) 평가 기준의 전환**

손 단위가 아니라 **완전한 human-hand-object tuple** 단위로 맞았는지를 재는 구조적 metric을 제안해, ownership 불일치에 실제로 페널티가 가도록 만든다.

---

## 연구 방법

### 전체 구조

Base는 RT-DETR 스타일 파이프라인이다. Backbone + transformer encoder → top-$K$ query 선택 → part-aware reference를 쓰는 deformable decoder → 여러 head로 구조화 출력.

- **Input**: 이미지 $\mathbf{x}$ 하나.
- **Output**: person-centric interaction tuple의 집합.

### 1) Query 설계: 사람도 물체도 같은 query 풀에서

$N$개의 object query를 쓰되, **각 query가 human instance일 수도 general object instance일 수도 있다**. 모든 query $i$에 대해 detector는 class 분포 $\mathbf{\hat{c}}_i \in \mathbb{R}^C$ (person 포함)와 박스 $\mathbf{\hat{b}}_i \in [0,1]^4$를 예측한다.

Person으로 분류된 query는 여기에 body keypoint, 좌/우 hand box, 그리고 relation 추론에 쓰이는 좌/우 hand embedding $\mathbf{h}_i^L, \mathbf{h}_i^R \in \mathbb{R}^d$를 더 뽑는다.

중요한 구현 디테일: **non-person query도 forward pass에서는 hand/pose head를 똑같이 통과한다.** 예측된 hand box와 pose가 decoder의 part-aware reference point를 만드는 데 쓰이기 때문이다. 다만 **loss는 human instance에 matching된 query에만 건다.** 즉 출력은 나오되 supervision은 없다.

### 2) Part-aware Deformable Attention — 하나의 query로 몸과 손을 동시에 보기

**문제**: 큰 사람 몸통과 작고 관절이 많은 손을 하나의 query가 동시에 정확히 잡아야 한다. 기존 구조적 human prediction 방법들은 instance query와 part query(예: human query + keypoint query)를 **따로** 두어 해결했다([ED-Pose](https://arxiv.org/abs/2302.01593), Group Pose 계열).

**해법**: task별 추가 query를 만들지 않고, **query 하나 안에서** interactive learning을 한다.

- *Head-wise decomposition*: 같은 query feature의 서로 다른 sub-representation(attention head 묶음)에 서로 다른 구조적 역할(몸통 / 좌손 / 우손 / body joint)을 할당한다.
- *두 층위의 interactive learning*: query 사이의 self-attention으로 instance-to-instance 상호작용을, query 내부 head 구조로 global-to-local 결합을 만든다.

**Reference point 구성**: 각 decoder layer에서 중간 예측으로부터 reference를 만든다.

$$\mathbf{p}_i^H = \phi(\mathbf{\hat{b}}_i), \quad \mathbf{p}_i^L = \phi(\mathbf{\hat{b}}_i^L), \quad \mathbf{p}_i^R = \phi(\mathbf{\hat{b}}_i^R)$$

$\phi(\cdot)$는 박스를 정규화 좌표의 2D reference point(예: 박스 중심)로 보내는 함수다.

Pose를 위해서는 $J$개의 **joint-specific reference region**을 추가로 만든다. 관절 $j$의 예측 위치 $\mathbf{\hat{k}}_i^j$를 중심으로 쓰고, 크기는 main box 크기 $(\hat{w}_i, \hat{h}_i)$에 **학습 가능한 파라미터** $\gamma_w^j, \gamma_h^j$를 곱해 정한다:

$$\mathbf{s}_i^j = (\gamma_w^j \hat{w}_i,\ \gamma_h^j \hat{h}_i), \quad \mathbf{p}_i^j = (\mathbf{\hat{k}}_i^j, \mathbf{s}_i^j)$$

Decoder attention head들을 이 part reference들에 분배해, 하나의 query가 박스 수준 / 손 수준 / 관절 수준 영역을 동시에 참조하게 만든다.

### 3) Hand-to-Query Relation Matrix — 상호작용 대상을 "고른다"

논문은 상호작용 표현 방식 두 가지를 비교한다.

**(i) DirectBox (직접 regression, 베이스라인)**: person query에서 손마다 상호작용 물체 박스 $\mathbf{\hat{b}}_i^{s,\text{obj}}$를 직접 회귀하고, 접촉 상태 label도 따로 예측한다. 회귀된 박스만으로는 접촉 여부도, 접촉의 의미적 종류도 알 수 없기 때문에 별도 label이 필수다. 그리고 **물체의 class를 알 수 없다.**

**(ii) Relation (제안 방식)**: 각 손이 **검출된 query 집합 + 학습 가능한 off token** 중에서 대상 하나를 고른다.

- 최종 query embedding $\{\mathbf{z}_i^T\}$를 relation embedding $\mathbf{r}_i \in \mathbb{R}^d$로 project하고, no-contact를 뜻하는 학습 가능한 off embedding $\mathbf{r}_0$를 둔다.
- Person query $i$, 손 방향 $s \in \{L, R\}$에 대해 hand embedding $\mathbf{h}_i^s$와 모든 target embedding $\{\mathbf{r}_0, \mathbf{r}_1, \ldots, \mathbf{r}_N\}$의 dot-product 점수를 구하고 $(N+1)$개 후보에 softmax를 건다. 예측 target index $\hat{t}_i^s$는 argmax.

**접촉 상태가 선택 결과에서 자동으로 파생된다는 것이 핵심이다:**

| 선택 결과 | 해석되는 contact state |
|---|---|
| $\hat{t}_i^s = 0$ (off token) | no-contact (접촉 없음) |
| $\hat{t}_i^s = i$ (자기 자신 query) | self-contact (자기 몸에 접촉) |
| $\hat{t}_i^s = j \neq i$ | 다른 entity와 접촉 (보통 object contact, 대상이 사람 query면 other-person contact) |

그리고 모든 query가 이미 박스와 class 분포를 예측하므로, $j$를 고르는 순간 **대상의 박스 $\mathbf{\hat{b}}_j$와 class $\arg\max \mathbf{\hat{c}}_j$를 그대로 가져올 수 있다.** 별도의 interacting-object regression head가 필요 없어진다.

### 4) 학습 목표

DETR 스타일 bipartite matching을 human/object instance 전체에 대해 수행하고, end-to-end로 학습한다. Loss는 표준 detection loss([GIoU](https://arxiv.org/abs/1902.09630) 포함)에 hand box, body pose(YOLO-Pose 계열 OKS loss), hand-object relation supervision을 더한 조합이다. 각 손은 matching된 query 집합 + off 옵션 중에서 자기 target을 고르도록 학습된다. (전체 loss 정의와 구현 디테일은 supplementary로 미뤄져 있다.)

**Inference**: detection confidence 기준 top-$K$ query를 남기고, person query는 pose·좌우 hand box·좌우 interaction target을 추가 출력한다. 유효한 target query를 고른 손은 그 query에서 박스와 class를 바로 retrieve한다.

### 5) 데이터셋 구축 — COCO + Hands23 결합

[COCO](https://arxiv.org/abs/1405.0312) 위에 만든 이유는 두 가지다. (a) 다인원 장면이 다양해 person-centric 추론에 적합하고, (b) 이미 object detection annotation과 human keypoint가 있어서 처음부터 다시 라벨링할 필요가 없다.

**단계 1 — Person-hand pair 구성 (wrist-guided geometric matching)**

COCO는 좌/우 손목 keypoint를, Hands23는 COCO 일부 이미지의 좌/우 hand box를 준다. 가시성이 0이 아닌 손목 $\mathbf{w}_p^s$에 대해 같은 방향의 hand box 중심 $\mathbf{c}_h$와의 거리를 재고,

$$d(p,h,s) = \|\mathbf{w}_p^s - \mathbf{c}_h\|_2$$

다음 두 조건을 모두 만족하면 매칭한다:

- $d(p,h,s) < k \cdot \text{diag}(h)$, with $k = 1.4$ (손 크기 대비 손목-손중심 거리가 충분히 가까움)
- $\mathbf{c}_h \in \text{Expand}(\mathbf{b}_p, l)$, with $l = 1.15$ (손 중심이 확장된 사람 박스 안에 있음)

여러 사람이 같은 손 박스에 대해 조건을 만족하면 $d$가 가장 작은 사람에게 할당한다.

**단계 2 — LLM/VLM 기반 검증**

규칙 기반 매칭은 심한 occlusion(가림)이나 사람들이 겹칠 때 틀릴 수 있다. 그래서 (i) 전체 이미지, (ii) 손 주변 local crop, (iii) [DepthAnythingV2](https://arxiv.org/abs/2406.09414)로 뽑은 relative depth map을 함께 주고 검증한다. Depth는 앞뒤 순서(front-back ordering)와 가림 여부에 대한 공간적 근거가 된다. Verifier는 **no-guessing 정책**을 따라 contact / no-contact / uncertain 중 하나만 내고, uncertain은 학습에서 제외한다.

**단계 3 — Interaction target 변환**

Contact taxonomy는 네 가지를 유지한다: `no_contact`, `self_contact`, `other_person_contact`, `object_contact`. (DirectBox 베이스라인과 hand-state 평가에서는 none vs. hold 이진 상태로 축약.)

Hands23의 contact-associated interaction box를 COCO entity와 **IoU $\ge 0.5$** 로 매칭한다.

- `object_contact` → COCO object box 중 최고 IoU 물체
- `other_person_contact` → 현재 사람을 제외한 COCO person box 중 최고 IoU
- `self_contact` → 현재 사람 instance 자신
- `no_contact` → off

매칭되는 COCO object가 없으면 interaction box를 그대로 pseudo target box로 쓰고 generic class `object`를 부여(학습용 placeholder). `other_person_contact`인데 매칭되는 사람이 없으면 애매한 supervision을 피하려고 **샘플을 버린다**.

**단계 4 — Validation set**

Hands23는 COCO val2017과 겹치지 않으므로, 사람이 최소 한 명 있는 COCO val2017 이미지 **약 2K장**을 직접 수작업 annotate해 human-verified validation split을 만들었다.

**Annotation 신뢰도** (770 샘플 수동 감사 결과):

| 항목 | 값 |
|---|---|
| uncertain 비율 | 1.3% |
| annotation 오류율 (rule-based) | 2.5% |
| annotation 오류율 (검증 후) | 2.1% |
| 두 annotator의 이중 라벨링 일치율 (500 샘플) | 98.4% |

남은 오류는 주로 흐릿하거나 해상도가 낮은 손, 아주 작은 손, occlusion, depth로 판별하기 어려운 배치 때문이다.

### 6) 평가 지표 — soft / medium / hard

세 지표 모두 먼저 예측/GT person instance를 one-to-one IoU matching하고, person-box IoU가 $\tau_p = 0.5$를 넘는 쌍만 남긴다.

**Soft**: 매칭된 사람들에 대한 hand-state 정확도.

$$\text{Acc}_{\text{soft}} = \frac{\sum_{(g,p)\in\mathcal{A}}\sum_{s\in\{L,R\}} m_g^s \cdot \mathbb{1}[\hat{y}_p^s = y_g^s]}{\sum_{(g,p)\in\mathcal{A}}\sum_{s\in\{L,R\}} m_g^s}$$

여기서 $m_g^s$는 해당 손 annotation이 존재하는지를 나타내는 availability mask다.

**Medium**: GT state가 hold일 때 **상호작용 물체 위치까지 맞아야** 한다 ($\tau_o = 0.5$). HOI 프로토콜에서 사람과 물체 localization을 모두 요구하는 방식을 따른다.

**Hard**: 여기에 더해 **hand box localization까지 맞아야** 한다 ($\tau_h = 0.5$).

본문은 좌/우 평균을 보고한다.

---

## 실험 결과 / 연구 의의

**설정**: 기본 detector는 RT-DETR-R50-m. 학습/평가는 제안한 COCO 기반 person-centric 데이터셋. 추가로 100DOH를 같은 person-hand merging 파이프라인으로 변환해 학습 데이터로 쓰고(100DOH엔 object detection·pose annotation이 없어 off-the-shelf detector [Co-DETR](https://arxiv.org/abs/2211.12860)와 pose 모델로 pseudo label 생성), ContactHands는 전체를 평가셋으로 사용한다. ContactHands는 접촉 물체 annotation이 없으므로 $\text{Acc}_{\text{soft}}$만 보고한다.

### 실험 1 — Relation vs. DirectBox, 그리고 pose 학습의 효과 (Table 2)

| Method | Rel. | Pose | Det. mAP | Pose AP | Acc_soft | Acc_mid | Acc_hard | ContactHands Acc_soft |
|---|---|---|---|---|---|---|---|---|
| DirectBox | X | X | 49.1 | N/A | 81.5 | 44.9 | 12.6 | 80.7 |
| DirectBox+Pose | X | O | 47.7 | 61.8 | 83.0 | 57.6 | 30.1 | 81.3 |
| Relation | O | X | 48.8 | N/A | 80.0 | 60.8 | 28.9 | 81.7 |
| Relation+Pose | O | O | 47.1 | 62.3 | **83.8** | **64.6** | **31.3** | **82.2** |

읽어낼 메시지:

- **Relation formulation이 tuple 정확도를 크게 끌어올린다.** Detection mAP는 거의 같은데(49.1 vs. 48.8), $\text{Acc}_{\text{mid}}$는 44.9 → 60.8 (+15.9), $\text{Acc}_{\text{hard}}$는 12.6 → 28.9 (+16.3). 즉 물체 박스를 직접 회귀하는 것보다 **이미 검출된 query 중에서 고르는 편이 훨씬 안정적**이다.
- 다만 relation만 쓰면 COCO $\text{Acc}_{\text{soft}}$가 81.5 → 80.0으로 약간 떨어진다. Relation modeling의 이득은 **target association과 localization**에 있지, 단순 hand-state 분류에 있는 게 아니라는 뜻이다. ContactHands에서는 오히려 80.7 → 81.7로 조금 오르므로, state 인식을 해치지는 않는다.
- **Pose supervision은 두 formulation 모두에서 일관되게 손 추론을 개선한다.** DirectBox는 $\text{Acc}_{\text{mid}}$ +12.7, $\text{Acc}_{\text{hard}}$ +17.5. Relation은 +3.8, +2.4. 사람의 구조적 이해가 손 위치 추정과 상호작용 추론을 돕는다는 가설을 뒷받침한다.
- **Detection mAP는 pose를 넣으면 조금 떨어진다** (49.1→47.7, 48.8→47.1). 논문은 이를 multi-task learning에서 흔한 task conflict(태스크 간 간섭)로 설명한다.

### 실험 2 — 100DOH 추가 supervision (Table 3)

| Method | +100DOH | Det. mAP | Pose AP | Acc_soft | Acc_mid | Acc_hard | ContactHands Acc_soft |
|---|---|---|---|---|---|---|---|
| Relation+Pose | X | 47.1 | 62.3 | 83.8 | 64.6 | 31.3 | 82.2 |
| Relation+Pose | O | 48.6 | 63.2 | 84.0 | 66.2 | 32.7 | 81.2 |

- COCO val2017에서는 전 지표 상승: mAP +1.5, pose AP +0.9, $\text{Acc}_{\text{soft}}$ +0.2, $\text{Acc}_{\text{mid}}$ +1.6, $\text{Acc}_{\text{hard}}$ +1.4.
- **증가폭이 soft보다 mid/hard에서 훨씬 크다.** 100DOH가 명시적 interacted-object box를 주기 때문에, 손-물체 localization과 association에 직접적인 supervision이 들어간 결과다. 즉 100DOH는 "완전한 hand-object tuple 복원 능력"을 강화한다.
- ContactHands $\text{Acc}_{\text{soft}}$는 82.2 → 81.2로 소폭 하락. ContactHands는 hand-state만 재는데 100DOH의 이득은 target-aware 추론 쪽이라 정렬이 어긋난 것으로 해석한다.

### 실험 3 — Part-aware reference allocation ablation (Table 4)

| Method | PartAware | Det. mAP | Pose AP | Acc_soft | Acc_mid | Acc_hard | ContactHands Acc_soft |
|---|---|---|---|---|---|---|---|
| DirectBox+Pose | X | 48.7 | 43.4 | 80.4 | 43.1 | 11.5 | 80.5 |
| DirectBox+Pose | O | 47.7 | 61.8 | 83.0 | 57.6 | 30.1 | 81.3 |
| Relation+Pose | X | 48.6 | 42.8 | 83.0 | 63.6 | 10.3 | 81.7 |
| Relation+Pose | O | 47.1 | 62.3 | 83.8 | 64.6 | 31.3 | 82.2 |

이 논문에서 가장 극적인 표다.

- Part-aware를 끄면 모든 decoder head가 main box reference 하나를 공유한다. 그러면 instance-level localization에 유리해 **detection mAP는 오히려 조금 높다** (48.7 vs. 47.7, 48.6 vs. 47.1).
- 그러나 part-level 추론은 붕괴한다. **Pose AP가 ~42대로 떨어진다** (DirectBox 43.4 → part-aware 61.8, +18.4 / Relation 42.8 → 62.3, +19.5).
- **$\text{Acc}_{\text{hard}}$는 완전히 다른 수준이 된다**: DirectBox 11.5 → 30.1 (+18.6), Relation 10.3 → 31.3 (+21.0). Hard metric은 hand box 정확도를 요구하므로, 손 주변 local 영역에 attention이 가는지가 결정적임을 보여준다.
- 흥미로운 대비: Relation+Pose의 $\text{Acc}_{\text{mid}}$는 63.6 → 64.6 (+1.0)으로 변화가 작다. Relation 방식은 검출된 query에서 target을 retrieve하므로 detection 성능 변동에 상대적으로 강건하다. 반면 DirectBox는 $\text{Acc}_{\text{mid}}$가 43.1 → 57.6 (+14.5)로 크게 흔들려, **직접 regression 방식이 decoder가 어디를 보는지에 극도로 민감함**을 드러낸다.
- 요약된 trade-off: 모든 head를 main box에 몰면 detection이 살짝 유리하지만, **정확한 pose와 신뢰할 수 있는 person-centric 양손 상호작용을 얻으려면 part-aware allocation이 필수**다.

### 실험 4 — 혼잡도(crowding) 분석 (Table 5)

COCO val2017을 이미지 내 사람 수로 나눈 결과다.

| # persons | Acc_soft | Acc_mid | Acc_hard |
|---|---|---|---|
| 1 | 90.28 | 79.42 | 54.00 |
| 2–4 | 86.58 | 67.31 | 33.09 |
| ≥5 | 75.84 | 56.17 | 22.02 |

- 1인 장면에서는 매우 높다 ($\text{Acc}_{\text{hard}}$ 54.00).
- 사람이 5명 이상인 극혼잡 장면에서는 뚜렷하게 떨어진다 ($\text{Acc}_{\text{hard}}$ 22.02). 심한 occlusion, 손 겹침, 보이는 손 영역이 작아지는 것이 주요 원인이다.
- 이 표 자체가 논문의 문제의식(ownership ambiguity)이 실제로 남아 있는 난제임을 정직하게 보여준다.

### 연구 의의

1. **Prediction unit을 해석 unit에 맞추면 구조적 정확도가 올라간다**는 것을 수치로 보였다. 단순히 성능을 올린 게 아니라, "무엇을 하나의 예측 단위로 볼 것인가"라는 설계 질문에 답을 준다.
2. **Relation-based target selection이 direct regression보다 근본적으로 낫다**: 위치뿐 아니라 class까지 공짜로 얻고, tuple metric에서 +15~16점 차이를 만든다.
3. **Detection·pose·hand interaction의 통합이 상호 보완적**임을 보였다. Pose를 배우면 손 추론이 좋아지고, part-aware attention을 쓰면 pose가 20점 가까이 좋아진다.
4. **평가 프로토콜을 문제 정의에 맞춰 재설계**했다. Soft/medium/hard의 계단식 엄격도는 "상태만 맞음 / 대상 위치까지 맞음 / 손 위치까지 맞음"을 분리해 보여주므로, 어느 단계에서 실패하는지 진단할 수 있다.
5. 이 프레임워크는 특정 detector에 묶이지 않는다. DETR 계열 발전과 **직교(orthogonal)**하는 표현 설계여서, 더 좋은 detector가 나오면 그 위에 얹을 수 있다.

---

## 한계

**논문이 직접 밝힌 것**

- **극혼잡 장면에서의 성능 저하**: 사람 5명 이상일 때 $\text{Acc}_{\text{soft}}$ 75.84, $\text{Acc}_{\text{hard}}$ 22.02로 1인 장면 대비 크게 떨어진다. 심한 occlusion, 손 겹침, 작은 손 영역이 여전히 주된 난제라고 명시한다.
- **Annotation noise**: 학습 라벨이 규칙 기반 COCO-Hands23 정렬로 생성되어, occlusion·겹침·심한 스케일 변화에서 noise가 남는다. VLM 검증 후에도 오류율 2.1%가 남고, uncertain 1.3%는 아예 버린다.
- **Multi-task conflict**: pose를 함께 학습하면 detection mAP가 떨어진다(최대 약 2점). Part-aware reference를 켜도 detection mAP는 소폭 손해다. 이 trade-off를 해소하지는 못했다.
- **Future work로 남긴 것**: 데이터셋 도메인·상호작용 유형 확장, 심한 occlusion/혼잡 장면 robustness 개선, contact 수준을 넘어선 풍부한 interaction semantics로의 확장.

**명백하지만 논문이 크게 다루지 않은 것**

- **접촉 수준(contact-level) 추론에 머문다**: "닿았다/안 닿았다 + 무엇에" 까지다. 어떻게 잡는지(grasp type), 무엇을 하는 중인지(action predicate)는 없다. Hands23가 제공하는 grasp/contact category나 tool을 통한 second object 같은 풍부한 신호도 쓰지 않는다.
- **단일 이미지, 정적 프레임 기반**: 비디오 시간 정보나 양손 협응의 시간적 구조를 전혀 쓰지 않는다.
- **2D만 다룬다**: 3D hand pose(MANO 등)나 물체와의 3D 공간 관계는 범위 밖이다. Depth는 데이터 검증 단계에서만 보조로 쓰인다.
- **Target 후보가 검출된 query 집합에 갇힌다**: relation 방식의 장점이 곧 제약이다. 대상 물체가 애초에 검출되지 않으면(COCO 80 class에 없거나 검출 실패) 올바른 target을 고를 수 없다. 데이터 구축에서도 매칭 안 되는 물체는 generic class `object`의 pseudo box로 때운다.
- **비교 대상이 사실상 자기 ablation뿐**: 100DOH/Hands23 같은 기존 방법과의 직접적인 head-to-head 비교표가 본문에 없다. 새 task와 새 metric을 정의했기 때문에 불가피한 면이 있지만, 기존 hand-centric 방법을 이 metric 위에 올려 비교했다면 person-centric의 이득이 더 분명했을 것이다.
- **COCO 도메인 편향**: 일상 사진 위주라 정밀 조작(fine manipulation)이나 1인칭 시점 데이터는 거의 없다.
- Loss 정의, interactive learning의 구체적 아키텍처, LLM verification 절차 등 상당 부분이 supplementary로 미뤄져 본문만으로는 재현이 어렵다.

---

## 우리 연구와 연결되는 점

### Hand-Object Interaction 관점

가장 직접적으로 이어진다.

- **"무엇을 하나의 query로 볼 것인가"는 그대로 가져올 수 있는 설계 원칙이다.** 손을 독립 instance로 보느냐, 사람에 붙은 slot으로 보느냐가 tuple 정확도를 15점 이상 가른다. 우리가 HOI 관련 모델을 설계할 때도 "예측 단위가 최종 해석 단위와 일치하는가"를 먼저 점검할 만하다.
- **Relation matrix + off token 패턴은 재사용 가치가 높다.** 회귀 대신 "이미 검출된 entity 중에서 고르기"로 바꾸면 (a) 대상의 class를 공짜로 얻고, (b) 별도 head가 사라지고, (c) contact state가 선택 결과에서 자동 파생된다. no-contact를 학습 가능한 off token으로 두는 것도 깔끔한 트릭이다. 이 구조는 손-물체뿐 아니라 "무언가가 무언가를 고르는" 모든 association 문제에 옮길 수 있다.
- **Part-aware reference allocation은 작은 대상을 다룰 때 결정적이다.** Pose AP +19, $\text{Acc}_{\text{hard}}$ +21이라는 ablation 수치는, 큰 instance와 작은 part를 하나의 표현으로 다룰 때 **어디를 sampling하느냐**가 표현력보다 중요할 수 있음을 보여준다. 손처럼 작고 자주 가려지는 대상을 다루는 우리 과제에 그대로 적용 가능한 교훈이다.
- **데이터셋 구축 레시피**가 실용적이다. 기존 데이터셋 두 개(COCO + Hands23)를 wrist-guided geometric matching으로 합치고, VLM + depth map으로 검증하고, uncertain은 버린다. 라벨링 비용 없이 새 구조의 supervision을 만드는 방법론으로 참고할 만하다. 특히 **depth map을 occlusion/front-back 판별의 근거로 VLM에 함께 주는 것**은 바로 따라 할 수 있다.
- **평가 지표 설계**: soft/medium/hard 3단계 계단식 엄격도는 실패 원인을 분해해 준다. 우리도 새 task를 정의할 때 이런 층위별 metric을 설계하면 "state는 맞는데 localization이 틀린다" 같은 진단이 가능해진다.

### Egocentric Vision 관점

이 논문은 3인칭(exocentric) COCO 이미지가 대상이지만, 1인칭 연구와의 접점은 분명하다.

- **관점의 대칭성**: Egocentric 영상에서는 카메라 착용자의 양손이 거의 항상 함께 등장하므로, "좌/우 손이 한 사람에 속한다"는 person-centric 구조가 **기본값**이다. 역으로 말하면 이 논문이 exocentric에서 힘들게 복원하려는 ownership은 egocentric에서는 대체로 주어진다. 대신 egocentric에는 **착용자의 손 vs. 상대방의 손**을 구분하는 문제가 있고, 이 논문의 `other_person_contact` 카테고리와 person query 간 relation 설계가 그 문제에 그대로 대응된다.
- **Exo → Ego 전이 데이터의 원천**: Egocentric 모델 학습에 3인칭 데이터를 쓰려면 3인칭 쪽에서 person-centric 구조가 있어야 한다. 이 논문의 데이터셋은 human box + pose + 양손 + 접촉 대상 + 물체 class를 다 갖춘 드문 리소스다. Exo-ego 공동 학습이나 view-invariant 손-물체 표현 학습의 supervision으로 쓸 수 있다.
- **Body pose가 hand reasoning을 돕는다는 발견**은 egocentric에도 시사점이 있다. 1인칭에서는 몸 전체가 잘 안 보이지만, 팔/어깨의 부분적 단서나 head pose가 유사한 구조적 prior 역할을 할 수 있는지 실험해 볼 만하다.
- 100DOH와 Hands23는 원래 egocentric 비중이 큰 데이터셋이다. 이 논문이 100DOH를 통합 포맷으로 변환하는 파이프라인을 만들어 두었으므로, 그 변환기를 ego 데이터 통합의 출발점으로 삼을 수 있다.
- **Crowding 분석의 교훈**: 사람이 많을수록 성능이 떨어진다는 결과는, 1인칭 사회적 상호작용 장면(여러 사람이 함께 요리하거나 조립하는 상황)에서 손 소유권 판별이 여전히 미해결 과제임을 뜻한다.

### Spatial Audio 관점

직접적 연결은 없지만(이 논문에 오디오는 전혀 등장하지 않는다), 구조적으로 빌려올 지점이 있다.

- **"Query가 대상을 고른다"는 association 패턴**은 audio-visual 대응 문제와 형태가 같다. 소리 하나가 화면 속 검출된 여러 음원 후보 중 하나를 고르고, "화면 밖 음원"을 off token으로 두는 설계를 곧바로 상상할 수 있다. Off token으로 no-contact를 표현한 방식이, off-screen sound source를 표현하는 데 그대로 대응된다.
- **접촉이 소리를 만든다**: 손-물체 접촉 순간은 impact sound의 물리적 원천이다. 이 논문이 주는 "누가, 어느 손으로, 어떤 class의 물체에, 접촉했는가"라는 구조화된 출력은 **소리 이벤트의 공간적·의미적 근거(spatial grounding)**로 쓸 수 있다. 접촉 대상의 박스 위치는 곧 음원의 화면상 위치 추정치가 된다.
- **Multi-task conflict 관찰**은 멀티모달 공동 학습 전반의 교훈이다. Pose를 추가하니 detection이 떨어졌듯, audio task를 붙일 때도 어느 지표가 희생되는지 미리 측정하고 trade-off를 명시적으로 관리해야 한다.
- **계단식 metric 설계 철학**도 audio-visual 과제에 옮길 수 있다. "이벤트 종류만 맞음 / 대략적 방향까지 맞음 / 정밀 위치까지 맞음" 같은 3단계로 나누면 모델의 실패 모드를 분리해 볼 수 있다.

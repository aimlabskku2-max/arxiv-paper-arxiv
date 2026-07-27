# ForeHOI: Feed-forward 3D Object Reconstruction from Daily Hand-Object Interaction Videos

**arXiv**: 2602.06226 | **주제 분류**: Hand-Object Interaction | **출판일**: 2026-02-05 | **학회**: 프리프린트 (arXiv, cs.CV)
**저자/소속**: Yuantao Chen, Jiahao Chang, Chongjie Ye, Chaoran Zhang, Zhaojie Fang, Chenghong Li, Xiaoguang Han — SSE, CUHK-Shenzhen / FNii-Shenzhen / SDS, CUHK-Shenzhen
**링크**: https://arxiv.org/abs/2602.06226 (프로젝트 페이지: https://tao-11-chen.github.io/project_pages/ForeHOI, 코드: https://github.com/Tao-11-chen/ForeHOI)

## 한 줄 요약
손에 가려진 물체를 담은 일상 단안(monocular) 영상에서, 전처리 없이 1분 안에 물체의 완전한 3D 형상을 한 번에 뽑아내는 최초의 feed-forward 모델. 2D 마스크 채우기(inpainting)와 3D 형상 완성(shape completion)을 한 네트워크 안에서 동시에 풀어 가림(occlusion) 문제를 해결한다.

## 메인 그림
![ForeHOI teaser](https://arxiv.org/html/2602.06226v1/x1.png)

*Figure 1: 복잡한 전처리에 의존하는 기존 방법과 달리, ForeHOI는 단안 HOI 영상에서 곧바로 3D 물체 형상을 복원하는 end-to-end 파이프라인이다.*

파이프라인 그림: ![pipeline](https://arxiv.org/html/2602.06226v1/figs/pipeline.png)

## 선행 연구
- **손 복원(3D hand reconstruction)**: MANO 파라메트릭 손 모델을 미분 가능한 모듈로 신경망에 넣는 흐름이 정착했고, WiLoR·HandOS 같은 대규모 데이터 기반 모델은 in-the-wild 영상에서도 튼튼하게 동작한다. 즉 "손"은 이미 상당히 풀린 문제다.
- **손에 든 물체 복원(hand-held object reconstruction)**:
  - *템플릿 기반*: 물체 CAD 모델을 미리 주고 6-DoF 자세만 맞춘다. Dynhor는 ChatGPT가 만든 텍스트 프롬프트로 3D 생성 모델을 돌려 템플릿을 만들지만, 텍스트만으로는 불확실성이 크다.
  - *템플릿 없는 방식*: HOLD는 물체 prior 없이 implicit field를 최적화하고, MagicHOI는 Zero-1-to-3 같은 novel view synthesis prior를 radiance field 최적화에 끼워 넣는다. EasyHOI는 문제를 단일 이미지로 단순화해 2D inpainting 모델 + 3D 생성 모델을 이어 붙인다.
- **생성 prior 기반 3D 복원**: Zero-1-to-3 계열의 2D 생성 prior는 multi-view 불일치 문제가 있고, TRELLIS·Hunyuan3D 같은 native 3D 생성 모델이 품질에서 앞선다. 최근 CUPID, ReconViaGen이 native 3D 생성 모델에 pose-grounded 생성과 reconstruction prior를 붙여 단일 이미지 복원에서 좋은 성능을 냈다. ForeHOI는 이 ReconViaGen 계열 설계를 영상 입력 HOI 상황으로 가져온다.
- **HOI 데이터셋**: 현존 최대 실제 데이터셋(HOI4D)이 물체 417개, 최대 합성 데이터셋(ObMan)이 2,772개에 그친다.

## 문제 제기
일상 영상에서 물체를 복원하기 어려운 이유는 두 가지다.
1. **관측이 근본적으로 불완전하다.** 손이 물체를 가리고(hand-induced occlusion), 물체 자신도 뒷면을 가린다(self-occlusion). 물체 전체를 본 적이 없으니 강한 물체 prior 없이는 복원 자체가 불가능하다.
2. **카메라·손·물체가 전부 동시에 움직인다.** 그래서 물체와 카메라의 상대 운동을 추정하기 어렵고, SfM(COLMAP) 같은 고전적 전처리가 자주 실패한다.

기존 접근의 구체적 한계:
- EasyHOI는 단일 이미지만 써서 영상의 시간·다시점 정보를 버린다.
- MagicHOI는 2D inpainting → novel-view 기반 3D 복원으로 이어지는 다단계 파이프라인이라 단계마다 view-inconsistent 오차가 누적되고, radiance field 최적화에 수 시간이 걸린다.
- "VGGT로 초기 복원 후 3D completion" 식의 조합은, 심한 가림 상황에서 VGGT의 초기 결과 자체가 무너져 최종 결과도 망가진다.
- HOLD·MagicHOI는 SfM 자세와 sparse point를 입력으로 요구해, SfM이 실패하면 파이프라인 전체가 실패한다.

## 연구 주제
**일상 hand-object interaction 단안 영상에서 3D 물체(형상 + 프레임별 자세)를 feed-forward로 복원하는 문제.** 별도 마스크·자세·SfM 같은 전처리 입력 없이 RGB 영상 클립만 받아 1분 안에 결과를 내는 것이 목표다.

핵심 통찰: **2D 마스크 inpainting과 3D shape completion을 하나의 feed-forward 프레임워크에서 함께 예측하면 심한 가림 문제를 효과적으로 풀 수 있다.** 데이터만 충분하면 최적화 기반 방법에 필적하거나 그 이상인 결과를 단일 신경망이 직접 학습할 수 있다는 주장이다.

## 연구 방법

### 1) 이미지 + 손 prior 인코딩
- DINOv2로 각 프레임의 이미지 특징을 뽑는다.
- 동시에 WiLoR(손 자세 추정 모델)의 ViT backbone patch feature $F_{hand} \in \mathbb{R}^{n \times 1024}$를 뽑아, DINOv2 patch feature와 patch-to-patch로 정렬해 얕은 MLP로 융합한다. 모델이 "손이 어디에 어떤 형태로 있는지"를 확정적으로 알게 하는 조건 입력이다.
- 이 특징들은 각 이미지에 픽셀 정렬(pixel-aligned)되어 로컬 카메라 공간 정보를 담으므로, 프레임 간 스케일 불일치 문제가 생기지 않는다.
- 덕분에 **추론 시 손/물체 마스크를 따로 줄 필요가 없다.**

### 2) 양방향 cross-attention (핵심 설계)
완전한 3D 형상을 한 번에 맞추는 건 너무 어려워서, 문제를 2D 완성과 3D 완성 두 축으로 쪼갠다. Diffusion transformer(DiT)를 **geometry 브랜치**와 **mask 브랜치**의 이중 구조로 놓고, 둘 사이에 양방향 cross-attention을 건다.

- **mask → geometry**: 각 뷰에서 "가려지지 않았다면 물체 윤곽이 어디까지였을지"를 알려줘, 3D 브랜치가 가려진 영역을 일관되게 상상하도록 돕는다. ReconViaGen처럼 다시점 이미지 특징을 3D latent에 weighted fusion으로 cross-attention하되, 원래의 입력 특징 대신 **mask 브랜치의 층별 특징**을 얕은 층부터 깊은 층까지 순서대로 넣는다.
- **geometry → mask**: ViLBERT식으로 3D 특징을 문맥 신호로 삼아 mask 브랜치에 되먹인다.

$$
y_{j+1}=\sum_{k=1}^{N} CrossAttn(Q(y_j'), K(x_i^n), V(x_i^n)) \cdot w_n, \quad x_{i+1} = CrossAttn(Q(x_i'), K(y_j), V(y_j))
$$

여기서 $M$은 geometry 브랜치 DiT 블록 수, $P$는 mask 브랜치 블록 수, $N$은 프레임 수, $w_n$은 $n$번째 프레임의 융합 가중치다. 다시점 특징을 concat이 아니라 **가중 cross-attention으로 융합**하기 때문에, VGGT나 Hunyuan3D처럼 이미지를 이어 붙이는 방식과 달리 메모리 증가를 조금만 감수하고 긴 시퀀스를 받을 수 있다.

### 3) 학습과 추론
- 3D latent와 2D mask를 **같은 timestep $t$로 동시에** conditional flow matching(CFM)으로 학습한다.
  $$\mathcal{L}_{CFM}(\theta) = \mathbb{E}_{t, x_0, \epsilon} \| v_\theta(x,t) - (\epsilon - x_0) \|_2^2, \qquad \mathcal{L} = \mathcal{L}_{CFM}^{2D} + \beta \mathcal{L}_{CFM}^{3D}$$
  $\beta$가 2D/3D 손실 균형을 잡는다.
- 추론 시 Euler sampling으로 $x(1) = x(0) + \int_0^1 v_\theta(x(t),t)\,dt$ 를 적분해 마스크와 형상을 동시에 denoise한다.
- voxel을 고품질 표면으로 올리는 2단계는 TRELLIS의 structured latent(SLat) flow를 따르되, **완전한 물체 이미지 대신 가려진 이미지를 입력**으로 쓰고, VGGT 특징 대신 DINOv2 특징을 쓴다(가림이 심하면 VGGT 특징이 신뢰할 수 없기 때문).

### 4) 물체 자세 추정 (post-processing)
- 구면상 균일 분포 시점에서 복원 메시를 30장 렌더링 → 입력 프레임과 함께 VGGT에 통과시켜 대략적 카메라 자세를 얻는다. 렌더 시점의 자세는 알고 있으므로 물체 좌표계로의 변환을 유도할 수 있다.
- 이후 렌더된 RGB·depth와 입력 프레임 사이 2D 대응점을 image matching(Mast3R)으로 찾고, depth와 카메라 파라미터로 2D–3D 대응을 만들어 PnP + RANSAC으로 자세를 정제한다. 이 과정을 여러 번 반복한다.

### 5) 대규모 합성 데이터셋
- MANO 손에 HTML 파라메트릭 손 텍스처 모델을 입히고 피부톤을 랜덤화.
- GraspXL(RL 기반 grasp 합성)이 Objaverse 물체에 대해 만든 파지 시퀀스 중 텍스처 품질과 움직임 정도를 보고 선별.
- Blender로 다시점 영상 렌더링. 물체와 손이 항상 화면 안에 있도록 카메라 궤적을 자동 생성하고, 조명 세기·방향도 랜덤화.
- 결과: **40만(400K) 개 클립**, 손 마스크 / 물체 마스크 / 손 자세 / 물체 자세 / depth map 주석 포함.

### 구현 세부
TRELLIS 아키텍처, PyTorch. 두 단계 DiT를 LoRA로 파인튜닝(rank 64, alpha 128, dropout 0, attention의 qkv projection과 output projection에만 삽입). 학습 시 입력 뷰 수는 2–6개 랜덤, 이미지는 518×518 (47×47 패치), 손 특징 추출기는 224×224 입력. Adam, lr 5e-4, batch size 32, **NVIDIA L20 40G 8장으로 4일** 학습.

## 실험 결과 / 연구 의의

### 평가 설정
- **학습**: 자체 합성 데이터셋 40만 클립만 사용. **실제 데이터로 파인튜닝하지 않음** — 데이터 prior의 강력함을 보이려는 의도.
- **HO3D**: HOLD와 같은 14개 시퀀스(HO3D-v3), MagicHOI를 따라 30프레임 클립으로 분할. 단일 이미지 방법(HORT, EasyHOI)은 프레임별로 돌려 평균.
- **HOT3D**: VR 헤드셋으로 찍은 egocentric 데이터셋. 저자들이 강조하는 점은, 다른 데이터셋이 복원을 위해 의도적으로 물체를 돌려 보여주는 것과 달리 HOT3D는 진짜 일상 상호작용을 담는다는 것 — 한 물체와의 상호작용이 **10–20 프레임**에 그치고 손 가림이 매우 빠르고 심하다. 전처리 후 5–15 프레임 길이의 짧은 클립 6개를 평가에 사용.
- **지표**: Chamfer distance(cm, ↓), F-score @5mm/@10mm(%, ↑), 자세는 ATE와 RPE.

### 형상 복원 (Table 2)

| Methods | HO3D CD(cm)↓ | HO3D F@5(%)↑ | HO3D F@10(%)↑ | HOT3D CD(cm)↓ | HOT3D F@5(%)↑ | HOT3D F@10(%)↑ | Avg Time(min) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EasyHOI | 1.83 | 46.35 | 69.24 | 1.21 | 18.46 | 34.25 | 175 |
| HOLD | 1.36 | 66.42 | 82.43 | N/A | N/A | N/A | 330 |
| HORT | N/A | N/A | N/A | 2.32 | 16.52 | 20.43 | 0.8 |
| MagicHOI | 0.86 | 64.53 | 91.87 | N/A | N/A | N/A | 58 |
| **Ours** | **0.79** | **68.95** | **93.72** | **1.03** | **60.5** | **89.1** | **1.1** |

- HO3D에서 모든 지표 1위이면서, 가장 가까운 경쟁자 MagicHOI(58분) 대비 **1.1분**으로 약 50배 이상 빠르다(초록의 "약 100배 speedup"은 최적화 기반 방법 전반 대비 표현).
- 특히 어려운 egocentric HOT3D에서 격차가 크다. F@5 기준 60.5% vs EasyHOI 18.46%, HORT 16.52%.
- HOLD와 MagicHOI는 HOT3D에서 N/A인데, 이는 SfM(COLMAP)이 sparse-view 클립에서 실패하기 때문이다(Figure 3의 "SfM Fails"). 일상 HOI 장면에서 SfM 의존이 얼마나 취약한지를 보여준다.

### 정성 분석 (Figure 3)
- HORT는 학습 데이터가 부족해 비슷한 물체에만 잘 되고, HOT3D의 미학습 물체나 복잡한 기하·특이한 시점에서는 완전히 실패한다.
- HOLD는 물체 prior가 없어 완전한 형상을 만들지 못한다.
- EasyHOI는 파이프라인이 길어 누적 오차 탓에 최종 3D가 원본 이미지에서 많이 벗어난다.
- MagicHOI는 가려진 영역을 채우고 관측 영역과도 잘 맞지만, 2D 다시점 생성의 태생적 불일치 때문에 물체 뒷면이 이상해지고 표면이 거칠고 울퉁불퉁하다.

### 물체 자세 추정 (Table 1, HO3D)

| Methods | RPE(cm)↓ | RPE(°)↓ | ATE(m)↓ |
| --- | --- | --- | --- |
| HOLD | 5.87 | 6.24 | 0.27 |
| Dynhor | 4.25 | 5.25 | 0.24 |
| **Ours** | **1.42** | **2.64** | **0.13** |

HOLD는 SfM 자세를 초기값으로 정제하는데, sparse-view 클립에서는 SfM 초기값이 나빠 결과도 나쁘다. ForeHOI는 먼저 복원한 메시를 템플릿 삼아 자세를 푸는 구조라 Mast3R의 강건한 매칭과 맞물려 훨씬 정확하다. (단, Dynhor의 정제 단계는 미공개라 첫 단계 자세로 비교했다고 저자들이 명시.)

### Ablation (정성 결과 기준)
논문은 세 가지를 검증한다.
- **자체 데이터셋의 필요성**: 일반 물체 데이터셋에 랜덤 마스크와 제한된 시점을 씌워 손에 든 상황을 흉내 내 학습해 봤지만, 실제 데이터에서 성능이 매우 나빴다. 이유는 두 가지 — (1) 3D 생성 모델의 의미 이해·완성은 object-centric 좌표계에 의존하는데, 테이블 위 물체는 방향이 대체로 정렬돼 있는 반면 손에 잡혀 회전된 물체는 완전히 낯선 상황이다. (2) 의미 없는 랜덤 가림으로는 hand-object interaction 자체를 학습하지 못한다. 이 관찰이 손 입력과 마스크 완성이라는 두 설계로 이어졌다.
- **손 특징(hand feature)**: 가림이 어디서 오는지를 모델에 직접 알려준다. 손 특징이 없으면 손이 닿은 부위에서 물체 표면이 눌린 듯한 **지문 자국(fingerprint indentation)** 형태로 잘못 복원되는 경우가 생긴다.
- **2D 마스크 완성 브랜치**: 손이 만드는 가림 마스크는 비교적 규칙적이고 상호작용 정보를 담고 있어, 손 특징만 있으면 전체 마스크를 채우는 건 쉬운 과제다. 하지만 이 쉬운 보조 과제가 모델의 hand-object interaction 이해를 끌어올려, 가림이 심한 상황의 성능을 크게 개선한다.

> 참고: Table 3(ablation 수치표)와 Conclusion, 부록(6·7절: 자세 추정 세부, hand-object alignment, 일반 방법과의 비교, 손 자세 결과, 자체 데이터셋 상세)은 arXiv HTML 본문 조회가 중간에 끊겨 수치를 확보하지 못했다. 위 ablation 서술은 본문의 정성적 설명에 근거한다.

### 의의
- **일상 HOI 영상에서 물체 3D 복원을 feed-forward로 푼 최초 사례.** 전처리(마스크, SfM, 물체 자세, 템플릿)를 전부 걷어냈다는 게 실용적으로 가장 크다.
- 최적화 기반 방법이 몇 시간 걸리던 작업을 1분대로 줄이면서 정확도까지 앞섰다 — "충분한 데이터가 있으면 신경망이 직접 학습할 수 있다"는 주장을 실증했다.
- 40만 클립 합성 HOI 데이터셋 공개는 이 분야 데이터 병목(실제 최대 417개 물체)을 직접 겨냥한다.
- Embodied AI / 로봇 조작 관점에서, 일상 영상을 3D 자산 + 자세 궤적으로 자동 변환하는 파이프라인이 된다.

## 한계
- **합성 데이터 의존.** 학습을 오직 자체 합성 데이터로만 했다. GraspXL + Objaverse + Blender 렌더링의 분포를 벗어난 재질·조명·손 외형에서 어떻게 되는지는 확인되지 않았다.
- **강체 가정.** GraspXL 기반 데이터와 "물체 자세" 개념 자체가 강체(rigid)를 전제한다. 관절형·변형 가능한 물체(가위, 천, 용기 뚜껑)는 다루지 않는다.
- **형상만, 텍스처는 없음.** 논문은 geometry 복원에 집중하며 물체 외형/텍스처 복원은 평가하지 않는다.
- **HOT3D 평가 규모가 작다.** 5–15 프레임짜리 클립 6개만 썼고, 전처리(물체별 크롭, undistort, 확대)도 수작업에 가깝다. egocentric 일반화 주장의 통계적 근거는 얇은 편이다.
- **자세 추정은 여전히 다단계 후처리.** 복원은 feed-forward지만, 자세는 렌더링 30장 + VGGT + 반복 매칭 + PnP/RANSAC이라는 별도 파이프라인이라 "완전한 end-to-end"는 아니다.
- **양손·다물체 상황 미논의.** 한 손이 한 물체를 잡는 설정을 전제한다.

## 우리 연구와 연결되는 점

**Egocentric Vision**
- HOT3D를 "진짜 일상 상호작용"의 대표 벤치마크로 세우면서, egocentric 영상의 본질적 어려움을 명확히 짚었다 — 한 물체와의 상호작용이 **10–20프레임**밖에 안 되고, 손 가림이 빠르고 심하며, 사용자가 물체를 복원용으로 친절히 돌려 보여주지 않는다. 우리가 egocentric 데이터를 다룰 때 클립 길이와 관측 다양성에 대해 어떤 가정을 하고 있는지 점검할 근거가 된다.
- SfM/COLMAP이 egocentric sparse-view 클립에서 그냥 실패한다는 실증(HOT3D에서 HOLD·MagicHOI 모두 N/A)은 중요하다. egocentric 파이프라인에서 SfM을 전제한 모듈이 있다면 그게 곧 실패 지점이다.
- 1분대 추론은 egocentric 스트림을 대량으로 처리해 3D 자산·상호작용 궤적 데이터베이스를 자동 구축하는 데 현실적인 속도다.

**Hand-Object Interaction**
- **손 prior를 물체 복원의 조건으로 쓰는 설계**가 핵심 아이디어다. WiLoR patch feature를 DINOv2 feature와 patch-to-patch로 정렬해 융합하면, 모델이 "가림의 원인"을 명시적으로 알게 된다. 손 정보를 다른 HOI 과제(접촉 추정, affordance, 조작 의도 예측)의 조건으로 넣을 때 그대로 옮길 수 있는 패턴이다.
- **2D 보조 과제로 3D를 돕는 구조**가 일반적으로 유용하다. "쉬운 2D 마스크 완성"이 "어려운 3D 형상 완성"의 성능을 끌어올린다는 결과는, 3D 과제가 어려울 때 픽셀 정렬된 2D supervision을 보조로 붙이는 전략의 근거가 된다.
- **랜덤 마스크로는 HOI를 학습할 수 없다**는 ablation 관찰이 데이터 설계에 직접적인 교훈이다. 가림은 의미론적 구조(손 모양, 파지 방식)를 가지므로, augmentation으로 흉내 내면 안 되고 실제 손 렌더링이 필요하다. 우리가 HOI 데이터를 합성/증강할 때 반드시 고려해야 할 지점.
- 공개된 40만 클립 데이터셋(손/물체 마스크, 손·물체 자세, depth 전부 포함)은 다른 HOI 과제의 사전학습 자원으로 재활용 가치가 크다.

**Spatial Audio**
- 직접적 접점은 없지만 구조적으로 옮길 만한 두 가지가 있다.
  1. **양방향 cross-attention을 통한 상호 보강**: 서로 다른 두 표현(2D mask ↔ 3D geometry)을 같은 diffusion timestep에서 함께 denoise하며 층별로 정보를 주고받는 설계는, audio latent와 visual/geometric latent를 결합하는 구조에 그대로 적용할 수 있다. 특히 "한쪽이 관측 가능하고 다른 쪽이 불완전할 때 관측 가능한 쪽이 guidance가 된다"는 논리는, 시각적으로 가려진 음원의 위치를 추정하는 문제와 형태가 같다.
  2. **가려진 것을 복원하는 문제 정식화**: 손이 물체를 가리듯, 시각적으로 보이지 않는 음원의 위치·형상을 공간 오디오로 보완하는 시나리오를 생각할 수 있다. ForeHOI가 복원한 물체 메시와 프레임별 자세는 접촉·충돌 이벤트의 3D 위치를 주므로, egocentric 영상에서 발생하는 상호작용 소리의 공간적 근거(sound source의 3D 위치와 방향)를 만드는 데 쓸 수 있다 — 즉 HOI 3D 복원이 spatial audio 지도학습용 라벨 생성기가 될 여지가 있다.

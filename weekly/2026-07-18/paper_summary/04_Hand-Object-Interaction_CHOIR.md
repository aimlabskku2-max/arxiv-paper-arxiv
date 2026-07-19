# CHOIR: Contact-aware 4D Hand-Object Interaction Reconstruction

**arXiv**: 2605.20992 | **주제 분류**: Hand-Object Interaction | **출판일**: 2026-05-20 | **학회**: 프리프린트
**저자/소속**: Hao Xu (The Chinese University of Hong Kong), Yilin Liu (University College London), Yinqiao Wang (The Chinese University of Hong Kong), Chi-Wing Fu (The Chinese University of Hong Kong), Niloy J. Mitra (University College London, Adobe Research)
**링크**: https://arxiv.org/abs/2605.20992

## 한 줄 요약
한 대의 카메라로 찍은 단안(monocular) RGB 영상만으로 손의 관절 움직임, 물체의 형상과 6D 포즈 궤적, 접촉(손이 물체에 닿는 지점)을 한꺼번에 복원한다. 이때 접촉을 손과 물체를 잇는 명시적 신호로 삼아 둘의 정렬과 물리적 자연스러움을 끌어올리는 open-world 4D Hand-Object Interaction 복원 프레임워크다.

## 메인 그림
메인(teaser) 그림은 CHOIR이 한 편의 단안 RGB 영상에서 3D 손 움직임, 3D 물체 형상, 6D 포즈 궤적, 접촉 증거를 open-world in-the-wild 장면에 대해 복원한 결과를 보여주고, 손과 물체의 접촉을 히트맵으로 시각화한다. (arXiv HTML의 이미지 경로가 표준 형식이 아니어서 믿을 만한 절대 URL을 확정하지 못해 이미지 임베드는 생략했다.)

## 선행 연구
기존 Hand-Object Interaction(HOI) 복원 연구는 크게 두 갈래다. 하나는 물체 템플릿을 미리 알거나 촬영 환경이 통제됐다고 가정하고 손과 물체를 따로따로 추정하는 방식이고, 다른 하나는 HaMeR(손 복원), SAM-3D-Objects(물체 형상), Dyn-HaMR(손 4D tracking) 같은 범용·특화 모델을 조합해 3D 초기값을 뽑는 방식이다. 비교 대상이 되는 최신 연구로는 HOLD, EasyHOI, MagicHOI 등이 있는데, 손과 물체를 따로 최적화하거나 특정 조건에서만 정렬을 맞춘다.

## 문제 제기
저자들은 in-the-wild 단안 영상에서 HOI를 복원할 때 서로 얽혀 있는 세 가지 어려움을 짚는다.
- **2D 인식 격차**: 범용 모델은 HOI의 의미(semantics)를 이해하지 못하고, 특화 검출기는 처음 보는 상황(unseen scenario)에서 무너진다.
- **3D 공간 모호성**: 단안 depth가 불확실하고 가림(occlusion)까지 겹쳐서, 손과 물체를 따로 추정하면 서로 어긋난다.
- **4D 물리적 복잡성**: 시간축 내내 물리적으로 자연스러운 접촉을 유지하면서 이미지 정렬까지 함께 맞춰야 한다.
핵심 통찰은 두 가지다. 접촉(contact)은 손과 물체의 결합을 알려주는 "드물지만 강력한 단서(sparse but strong cue)"라는 점, 그리고 이 단서는 공간 보정을 마친 뒤에야 믿을 수 있다는 점이다. 보정 전에 접촉을 그대로 쓰면 오히려 잘못된 정렬을 굳혀버리므로, 언제 접촉을 믿을지가 관건이 된다.

## 연구 주제
이 논문이 푸는 문제는 물체를 미리 알거나 장면이 통제됐다고 가정하지 않는 **open-world 4D HOI 복원**이다. 특히 접촉을 단순한 결과물이 아니라 손과 물체를 정렬시키는 **명시적 결합 신호(coupling signal)**로 보고, 공간 보정을 거친 뒤 접촉을 믿을 만한 제약으로 다시 끌어들이는 점을 새롭게 내세운다.

## 연구 방법
- **입력(input)**: 단안 RGB 비디오.
- **출력(output)**: 관절이 있는 손의 4D 움직임, 물체 형상 + 6D 포즈 궤적, 그리고 접촉 증거(contact evidence).
- **구조(module)**: 3단계 순차 파이프라인.
  - **Stage 1 — Open-World HOI Analysis**: 2D 상호작용 단서(손 bbox·관절·좌우 구분, 물체 bbox, modal/amodal mask)를 뽑고 → HaMeR/SAM-3D-Objects로 3D를 초기화한 뒤 → Dyn-HaMR(손)과 guarded pose tracking(물체)으로 4D tracking을 하고 → 손과 물체를 각각 따로 coarse fitting한다. 손 isolation loss는 $\mathcal{L}_{h}^{\mathrm{iso}}=\mathcal{L}_{2D}^{h}+\lambda_{\mathrm{depth}}\mathcal{L}_{\mathrm{depth}}^{h}+\lambda_{\mathrm{anat}}\mathcal{L}_{\mathrm{anat}}^{h}+\lambda_{\mathrm{prior}}\mathcal{L}_{\mathrm{prior}}^{h}+\lambda_{\mathrm{temp}}^{h}\mathcal{L}_{\mathrm{temp}}^{h}$ (이미지 정렬·depth 일관성·해부학·prior·시간 항)이고, 물체는 $\mathcal{L}_{o}^{\mathrm{iso}}=\lambda_{\mathrm{rep}}\mathcal{L}_{\mathrm{rep}}+\lambda_{\mathrm{attr}}\mathcal{L}_{\mathrm{attr}}+\lambda_{\mathrm{temp}}^{o}\mathcal{L}_{\mathrm{temp}}^{o}+\lambda_{\mathrm{stat}}\mathcal{L}_{\mathrm{stat}}^{o}$이다.
  - **Stage 2 — Generative HOI Spatial Rectification**: flow-matching 기반 생성 모델이 ray-depth 보정값을 예측해 공간 모호성을 바로잡는다. 물리 필터링을 거친 합성 grasping 데이터로 학습하고, depth 방향 불확실성을 부각하는 anisotropic perturbation을 모델링하며, 물체 mesh 위 barycentric anchor로 프레임마다 접촉 대응을 잡아준다. 보정 흐름은 $\frac{\mathrm{d}z_{\tau}}{\mathrm{d}\tau}=v_{\theta}(z_{\tau},\tau\mid\mathbf{J}^{h},\mathbf{r},s,\mathbf{P}^{o},\mathbf{n}^{o})$로 나타낸다.
  - **Stage 3 — Contact-Aware HOI Optimization**: 보정된 초기값에서 손과 물체 궤적을 함께 최적화하고, 최적화 도중 soft contact cache를 동적으로 다시 만든다. 목적 함수는 $\mathcal{L}_{\mathrm{HOI}}=\lambda_{\mathrm{con}}\mathcal{L}_{\mathrm{con}}+\lambda_{\mathrm{pen}}\mathcal{L}_{\mathrm{pen}}+\lambda_{\mathrm{sil}}\mathcal{L}_{\mathrm{sil}}+\lambda_{\mathrm{anc}}\mathcal{L}_{\mathrm{anc}}+\lambda_{\mathrm{temp}}\mathcal{L}_{\mathrm{temp}}$ (접촉·관통 penalty·silhouette·anchor·시간 항)이다.
- **학습 목표(큰 그림)**: 먼저 개별 fitting으로 좋은 초기값을 만들고(Stage 1), 생성 모델로 공간 어긋남을 바로잡은 뒤(Stage 2), 이제 믿을 수 있게 된 접촉을 제약으로 삼아 물리적으로 자연스럽고 이미지에 잘 맞는 4D 상호작용을 얻는다(Stage 3).

## 실험 결과 / 연구 의의
- **학습/평가 데이터**: 학습에는 physics 필터링으로 걸러낸 안정적 grasp 데이터([DexGraspNet](https://arxiv.org/abs/2210.02697) 기반 합성)를 쓴다. 평가는 통제 환경인 HO3D와 in-the-wild(TASTE-Rob + 직접 촬영한 100개 비디오)에서 진행한다.
- **HO3D (Table 1)**: CHOIR은 형상 정확도와 물리적 타당성을 동시에 잡는다. MagicHOI은 CD는 낮지만 penetration이 크고, HOLD은 CD와 penetration 모두 CHOIR보다 나쁘다.

| 방법 | Chamfer Distance (cm) | Penetration ratio (%) | F5 (%) | F10 (%) | MPJPE (mm) | mIoU (%) | Hand-object distance (cm) |
|---|---|---|---|---|---|---|---|
| CHOIR | 0.77 | 4.58 | 72.33 | 96.03 | 5.55 | 85.87 | 0.06 |
| MagicHOI | 0.87 | 14.11 | – | – | – | – | – |
| HOLD | 1.31 | 17.72 | – | – | – | – | – |

- **In-the-Wild (Table 2, 100개 비디오)**: CHOIR 자체 성능은 mIoU 76.65%(median 70.13%), penetration ratio 5.91%, hand-object distance 0.10 cm, hand acceleration 0.42 cm/fr², object acceleration 0.12 cm/fr²이다. mIoU에서 비교 방법들을 큰 차이로 앞선다.

| 비교 (subset) | CHOIR mIoU (%) | 비교 방법 mIoU (%) |
|---|---|---|
| HOLD 유효 30개 subset | 78.85 | 27.19 (HOLD) |
| MagicHOI 유효 22개 subset | 77.89 | 23.20 (MagicHOI) |

- **Ablation (Table 3)**: Stage 2 rectification을 빼면 hand-object distance가 나빠져, 공간 보정 단계가 정렬에 반드시 필요함을 보여준다.

| 설정 | Hand-object distance (cm) |
|---|---|
| CHOIR (full) | 0.10 |
| w/o Stage 2 rectification | 0.22 |
- **메시지**: 공간 보정을 마친 뒤 접촉을 믿을 만한 결합 신호로 다시 끌어들이는 설계 덕분에, 통제 환경은 물론 open-world에서도 정렬·물리적 타당성·시간적 일관성이 함께 좋아진다.

## 한계
- 물체를 형태가 변하지 않는 강체(rigid)로 가정한다.
- 가림이 극심하거나 물체 형상이 비정형일 때는 실패하는 경우가 있다(자세한 내용은 supplementary에 있다).
- Future work으로 형태가 변하는(deformable) 물체, 양손(bimanual) 상호작용, 더 복잡한 장면으로의 확장을 꼽는다.

## 우리 연구와 연결되는 점
- **Hand-Object Interaction**: 우리 주제와 곧바로 맞닿는다. 접촉을 결과가 아니라 최적화의 결합 신호로 쓰고 공간 보정을 마친 뒤에야 접촉을 믿는 "언제 접촉을 믿을지"라는 관점은, 손-물체 상호작용을 복원하고 이해하는 연구에 바로 적용할 수 있는 설계 원리다.
- **Egocentric Vision**: 논문 자체는 일반 단안 영상을 다루지만, 단안·가림·open-world 조건에서 손과 물체를 복원하는 파이프라인은 1인칭 영상(손이 자주 프레임에 잡히고 occlusion이 심함)으로 넓힐 여지가 크다(논문에 egocentric에 대한 직접 언급은 없으며, 우리 쪽에서 본 잠재적 접점이다).
- **Spatial Audio**: 논문에 직접 언급은 없다. 다만 접촉 이벤트(contact evidence)가 물체를 잡거나 놓는 순간과 맞물린다는 점에서, 접촉 타이밍을 소리 이벤트와 엮는 멀티모달 확장을 잠재적 관점으로만 생각해 볼 수 있다.

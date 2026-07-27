# HORT: Monocular Hand-held Objects Reconstruction with Transformers

**arXiv**: 2503.21313 | **주제 분류**: Hand-Object Interaction | **출판일**: 2025-03-27 | **학회**: ICCV 2025
**저자/소속**: Zerui Chen, Shizhe Chen, Cordelia Schmid (Inria, École normale supérieure, CNRS, PSL Research University), Rolandos Alexandros Potamias (Imperial College London)
**링크**: https://arxiv.org/abs/2503.21313

## 한 줄 요약

한 장의 RGB 이미지만으로 손에 쥔 물체의 3D 점군(point cloud, 물체 표면을 점들의 집합으로 나타낸 것)을 트랜스포머로 빠르고 정확하게 복원하는 방법으로, 성긴 점군에서 조밀한 점군으로 단계적으로 다듬는(coarse-to-fine) 전략과 손 기하 정보를 함께 활용해 기존 최고 성능(SOTA)을 능가하면서도 훨씬 빠른 추론 속도를 달성한다.

## 메인 그림
![Figure 1: ObMan 데이터셋에서의 추론 속도와 복원 품질 비교. HORT는 빠른 속도와 높은 품질을 동시에 달성한다.](https://arxiv.org/html/2503.21313v1/x1.png)

## 선행 연구

손에 쥔 물체(hand-held object)를 3D로 복원하는 연구는 크게 두 갈래로 나뉜다.

- **최적화 기반(optimization-based)**: 다중 시점 이미지, 비디오, 깊이 센서, 또는 이미 알려진 CAD 메시(mesh, 물체를 삼각형 면들로 표현한 것) 같은 추가 3D 입력을 이용해 물체의 6D 자세(pose)나 형상을 최적화한다. 정확하지만 복잡한 목적 함수와 반복 계산이 필요해 수 시간이 걸리고 실시간에 부적합하다. 최근 EasyHOI 등은 파운데이션 모델을 활용해 zero-shot 성능을 보였다.
- **학습 기반(learning-based)**: 신경망이 이미지에서 물체를 직접 복원한다. 초기 Hasson et al.(HO)이나 Tse et al.은 AtlasNet으로 물체를 메시 꼭짓점 집합으로 복원했으나 해상도가 낮았다. 이후 SDF(Signed Distance Function, 표면까지의 부호 있는 거리)나 DDF 같은 **암시적 함수(implicit function)** 기반 방법(AlignSDF, gSDF, DDF-HO 등)이 등장했다. 가장 최근의 SOTA인 D-SCO는 **확산 모델(diffusion model)**로 고해상도 물체 점군을 직접 복원한다.

## 문제 제기

기존 학습 기반 방법들의 두 가지 한계가 이 논문의 출발점이다.

- **암시적 함수 방법**은 표면이 지나치게 매끄럽게(overly smooth) 나와 세밀한 기하 디테일을 살리지 못한다. 게다가 학습된 암시적 필드에서 실제 3D 메시를 뽑아내려면 Marching Cubes 같은 후처리가 추가로 필요해 속도가 느려진다(그림 1에서 약 2초 소요).
- **확산 모델 방법(D-SCO)**은 품질은 좋지만, 여러 단계의 노이즈 제거(multi-step denoising)를 거쳐야 해서 고해상도 복원 시 매우 느리다. 복원 한 번에 13초 이상 걸려 암시적 방법보다도 느리다.

즉, 복원 **품질**과 **추론 속도**를 동시에 만족하는 방법이 없다는 것이 핵심 문제다.

## 연구 주제

단일 모노큘러(monocular, 단일 카메라) RGB 이미지에서 손에 쥔 물체의 **조밀한 3D 점군을 효율적으로(빠르게) 복원**하는 문제를 다룬다. 확산 모델의 반복적 디노이징 없이, 트랜스포머의 피드포워드(feed-forward, 한 번의 순전파) 방식으로 고해상도 복원과 빠른 속도를 함께 얻는 것이 목표다.

## 연구 방법

HORT는 네 개의 모듈로 구성되며 end-to-end로 함께 학습된다.

- **이미지 인코더(Image Encoder)**: 입력 이미지($224 \times 224$)를 DINOv2(large)로 인코딩해 257개의 시각 토큰($f_v \in \mathbb{R}^{257 \times 1024}$)을 얻는다. 사전학습 지식을 유지하면서 도메인에 적응시키기 위해 앞쪽 층은 동결(freeze)하고 마지막 12개 트랜스포머 층만 미세조정(fine-tune)한다.
- **손 인코더(Hand Encoder)**: 기성 손 자세 추정 모델로 MANO 손 메시(꼭짓점 $v_h \in \mathbb{R}^{778 \times 3}$)와 카메라 파라미터를 얻는다. 손 꼭짓점을 16개 관절 + 5개 손끝 + 1개 손바닥, 총 22개의 국소 좌표계로 변환하고 절대 꼭짓점 인덱스를 붙여 풍부한 기하 표현을 만든 뒤, PointNet으로 손 특징 $f_h \in \mathbb{R}^{1024}$를 추출한다. 손 형상이 물체 기하·위치에 대한 암시적 단서를 주기 때문에 이 정보로 모노큘러 복원의 모호성을 줄인다.
- **성긴 점군 디코더(Sparse Point Cloud Decoder)**: 물체 복원을 (1) 정준(canonical) 물체 점군 생성과 (2) 손바닥 기준 물체 위치 추정으로 분리한다. 회전은 물체 대칭성 때문에 ill-posed라 예측하지 않고 3D 이동(translation $t_o \in \mathbb{R}^3$)만 예측한다. 1개의 이동 토큰 + $N^s_p = 2{,}048$개의 점 토큰을 하나의 트랜스포머(self-attention 후 이미지·손 특징에 대한 cross-attention)로 처리해 물체 자세와 성긴 점군을 **동시에** 예측한다.
- **조밀 점군 디코더(Dense Point Cloud Decoder)**: 성긴 점군을 업샘플링해 $N^d_p = 16{,}384$개의 조밀 점군으로 만든다. 예측 카메라 파라미터로 각 점을 이미지 평면에 투영해 **픽셀 정렬(pixel-aligned) 특징**을 가져오고($f_o = F(\pi(p^s_o + t_p + t_o, K_{cam}), f^r_v)$), kNN($k=16$) 기반 국소 self-attention으로 손-물체 맥락을 통합한 뒤 각 점의 3D offset을 예측한다(2배, 4배 순차 업샘플).

학습 손실은 물체 이동에 대한 $\ell_1$ 손실과 성긴·조밀 점군에 대한 Chamfer Distance 손실을 결합한다: $L = \lambda_1 \times L_{pose} + \lambda_2 \times L^s_{cd} + L^d_{cd}$ ($\lambda_1 = \lambda_2 = 2$). ObMan에서 A100 4장으로 약 50시간 학습한다.

## 실험 결과 / 연구 의의

합성 데이터셋 ObMan과 실제 데이터셋 HO3D, DexYCB, MOW 네 가지에서 평가했다. 지표는 Chamfer Distance(CD, cm², 낮을수록 좋음)와 F-score(FS@5, FS@10, 높을수록 좋음), 그리고 상호작용 지표인 Contact Ratio, Penetration Depth를 사용한다.

ObMan에서 예측 손(predicted hand) 기준 SOTA 비교:

| Method | FS@5 ↑ | FS@10 ↑ | CD ↓ |
| --- | --- | --- | --- |
| HO | 0.23 | 0.56 | 6.4 |
| gSDF | 0.44 | 0.66 | 8.8 |
| DDF-HO | 0.55 | 0.67 | 1.4 |
| D-SCO | 0.61 | 0.81 | 1.1 |
| HORT (Ours) | 0.66 | 0.88 | 1.0 |

실제 데이터셋에서도 일관되게 우수하다. HO3D에서 D-SCO 대비 FS@10 14.3%, CD 23.5% 상대 개선을 보였다.

| Dataset | Method | FS@5 ↑ | FS@10 ↑ | CD ↓ |
| --- | --- | --- | --- | --- |
| HO3D | D-SCO | 0.41 | 0.63 | 3.4 |
| HO3D | HORT | 0.45 | 0.72 | 2.6 |
| DexYCB | D-SCO | 0.63 | 0.82 | 1.3 |
| DexYCB | HORT | 0.63 | 0.85 | 1.1 |

MOW에서도 두 학습 설정 모두 최고 성능을 기록했다(ObMan 파인튜닝 시 CD 10.2, 다중 데이터셋 학습 시 CD 5.4).

속도·효율 면에서 특히 강점이 크다. ObMan 기준 HORT는 258 GFLOPs만 사용하며 손+물체 복원을 포함해 **16.9 fps**(메시화 포함 시 4.8 fps)로 동작한다. 반면 암시적 방법들은 6000 GFLOPs 이상, D-SCO는 0.08 fps에 그친다.

| Method | GFLOPs ↓ | fps ↑ | CD ↓ |
| --- | --- | --- | --- |
| gSDF | 6.7k | 0.44 | 8.8 |
| DDF-HO | 8.9k | 0.35 | 1.4 |
| D-SCO | - | 0.08 | 1.1 |
| HORT (Ours) | 0.25k | 16.9 | 1.0 |

절제 실험(ablation)에서 손 인코더 추가(FS@5 0.45→0.53), 다중 관절 좌표계 인코딩(0.53→0.60), 자세·형상 공동 디코딩, 조밀 디코더의 픽셀 정렬 특징과 손 특징 통합이 각각 성능을 끌어올림을 확인했다. 또한 CORe50 및 휴대폰 촬영 등 in-the-wild 이미지에도 잘 일반화된다.

의의: 확산 모델 없이 단일 피드포워드 트랜스포머로 고해상도 점군 복원의 품질과 속도를 동시에 달성했고, 그 결과가 최적화 기반 방법의 강력한 초기값으로도 쓰일 수 있다는 점을 보였다.

## 한계

- 회전이 대칭성 때문에 ill-posed라는 이유로 물체의 3D **회전을 예측하지 않고 이동만** 복원한다. 즉 정준 좌표계 기준 형상과 손 상대 위치만 복원하며, 완전한 6D 자세는 다루지 않는다.
- 기성 손 자세 추정 모델의 출력에 의존하므로, 손 추정 품질이 물체 복원 정확도에 영향을 준다(실험에서도 예측 손보다 정답 손 사용 시 성능이 더 높다).
- 파라미터 수가 366M로 비교 방법들(24~35M)보다 훨씬 크다.
- 폐색(occlusion) 강건성과 실패 사례 분석은 본문이 아닌 부록으로 미룬다.

## 우리 연구와 연결되는 점

- 손 기하 정보를 물체 복원의 강력한 사전(prior)으로 쓰는 설계는, hand-object interaction 관련 연구에서 손 추정 결과를 물체·장면 추론에 재활용하는 파이프라인에 직접 응용할 수 있다.
- 확산 모델의 다단계 디노이징을 트랜스포머 피드포워드 + coarse-to-fine 업샘플링으로 대체해 속도를 크게 끌어올린 접근은, 실시간이 필요한 상호작용/로봇 조작(manipulation) 응용에서 참고할 만한 효율화 전략이다.
- 픽셀 정렬(pixel-aligned) 특징으로 3D 점을 이미지 관측에 다시 붙여 국소 디테일을 보강하는 기법은 단일 이미지 기반 3D 복원 전반에 재사용 가능한 모듈이다.
- 점군 복원 결과가 후속 최적화의 초기값으로 유용하다는 점은, 정확도가 더 중요한 태스크에서 HORT를 전처리 단계로 결합하는 하이브리드 설계를 시사한다.

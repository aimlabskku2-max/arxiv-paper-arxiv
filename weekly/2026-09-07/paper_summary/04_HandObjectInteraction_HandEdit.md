# HandEdit: A Unified Benchmark for Egocentric Human-to-Robot Dexterous Hand Image Editing

**arXiv**: 2608.12122 | **주제 분류**: Hand-Object Interaction | **출판일**: 2026-08-12 | **학회**: 프리프린트 (Technical Report, 프로젝트 페이지 https://handedit.github.io/)
**저자/소속**: Zhenjie Yang, Xingyu Jiao, Guopeng Zhong, Shuzhe Yang, Shi Che, Chao Wu, Chenyu Jiang, Dongjie Zhang, Yideng Zhang, Zheng Zhang, Muyun Jiang, Haisheng Su, Shuang Jin, Donghang Zhang, Chao Yang, Li Chen, Hongyang Li, Zuxuan Wu, Yu-Gang Jiang, Xiaosong Jia, Junchi Yan (주로 상하이교통대·푸단대·상하이 AI Lab 계열 저자군)
**링크**: https://arxiv.org/abs/2608.12122

## 한 줄 요약
1인칭(egocentric) 시점에서 촬영된 사람 손-팔 조작 영상을, 26종의 로봇 다관절 손/팔(dexterous hand) 형상으로 "이미지 편집"해 바꿔주는 대규모 데이터셋과 벤치마크를 구축하고, 상용·오픈소스 이미지 편집 모델 11종을 평가해 현재 모델들이 로봇 형상 충실도(embodiment fidelity)와 손-물체 상호작용 보존에서 크게 부족함을 보인 연구.

## 메인 그림
![HandEdit teaser](https://arxiv.org/html/2608.12122v1/fig1_teaser.png)

Figure 1 (teaser). 1인칭 시점의 사람 손-팔 조작 이미지를 입력받아, 목표 로봇 URDF(Unified Robot Description Format, 로봇의 링크·관절 구조를 기술하는 표준 포맷)가 지정하는 다양한 로봇 다관절 손/팔 형상으로 편집한 결과들을 보여준다. 장면·물체 상태·조작 의미는 유지한 채 손(및 팔) 영역만 로봇 형상으로 치환하는 것이 과제의 핵심이다.

(참고로 논문에는 데이터 생성 파이프라인 그림 `fig2_data_pipeline.png`, 기존 모델의 대표적 실패 사례 `fig3_data_composition.png`/`fig4_failure_modes.png`, VLM 평가 프로토콜 `fig5_vlm_metric.png` 등이 함께 실려 있다.)

## 선행 연구
- **로봇 조작 데이터 확보 방식**: 대규모 원격조작(teleoperation) 데이터셋, UMI류 시연 수집, 1인칭 사람 영상 세 갈래가 있다. 앞의 둘은 실제 로봇으로 바로 실행 가능한 시연을 주지만 하드웨어·실험실 환경·과제 설정에 묶여 수집 비용이 크고, 사람 영상은 풍부하고 다양하며 확장 가능하다는 점이 대비된다.
- **사람→로봇 변환(human-to-robot) 방법들**: H2R, Phantom, Masquerade, H2R-Grounder, MimicDreamer, Mitty, Human2Robot, DWM 등이 렌더링·인페인팅·합성·비디오 변환으로 시도했으나 대체로 평행 그리퍼(parallel gripper)나 고정된 로봇 플랫폼, 형상 특화 파이프라인에 한정되어 있었다. 사람 영상에서 조작 정책을 배우는 연구로는 DexVIP, DexArt, DexH2R, UniDex, MiVLA 등이 인용된다.
- **이미지 편집 벤치마크/데이터셋**: EditBench, InstructPix2Pix, MagicBrush, OmniEdit, Emu Edit, UltraEdit, SEED-Data-Edit, HQ-Edit, AnyEdit, VE-Bench, MotionEdit, EgoEdit 등과 비교표(Table 1)로 대조된다. 편집 방법론의 토대로 SDEdit, Prompt-to-Prompt, DiffEdit, ControlNet이 언급된다.
- **핵심 공백**: 1인칭 입력 + 로봇 다관절 손 + URDF 조건부 편집 + 다중 형상 평가를 동시에 지원하는 벤치마크는 이전에 없었다는 것이 저자들의 주장이다.

## 문제 제기
사람 손과 로봇 다관절 손은 외형·기하 구조·관절 구성(articulation)·기구학적 제약(kinematic constraint)·상호작용 방식이 근본적으로 다르다. 특히 손목과 팔까지 보이는 hand-arm 시스템에서는 팔 형상과 카메라 시점까지 목표 로봇 형태와 일치해야 하므로 격차가 더 커진다. 따라서 사람 1인칭 영상은 단순 스타일 변환이나 일반적 외형 편집으로 로봇 데이터로 바꿀 수 없다. 편집 결과는 (1) 장면·물체 상태·과제 의미·손-물체 접촉을 보존하면서 (2) 치환된 손/팔이 목표 URDF를 따르는 물리적으로 타당한 로봇 형상이어야 한다. 그러나 기존 일반 이미지 편집 모델은 이런 형상 특화 사전지식(embodiment-specific prior)이 없고, 사람→로봇 다관절 손 편집은 이미지 편집 문제로서 체계적으로 연구된 적이 없었다.

## 연구 주제
"1인칭 사람 손/팔 조작 이미지 → 목표 로봇 URDF 형상"으로의 embodiment-aware 이미지 편집을 대규모 데이터셋과 통일된 벤치마크로 정식화하는 것. 주요 기여는 다음과 같다.
1. 사람→로봇 다관절 조작 전이를 위한 최초의 대규모 embodiment-aware 이미지 편집 데이터셋(26 URDF, 2억+ 편집 인스턴스).
2. Hand-only / Hand-Arm 두 트랙과 URDF 조건부 평가를 지원하는 최초의 통일 벤치마크.
3. 일반 시각 유사도 + VLM(vision-language model) 판정 + embodiment-aware 지표를 결합한 종합 평가 스위트.
4. 상용·오픈소스 편집 모델 11종 벤치마킹과 지표 검증용 인간 평가.

## 연구 방법
**데이터 규모**: 5개 공개 손-물체 상호작용(HOI) 데이터셋에서 유래한 2억(200M)+ 이미지 단위 편집 인스턴스로, 30만(300K) 클립·600+ 장면·1.1K+ 물체·400+ 과제를 포괄하고, 26종 목표 URDF(13 hand-only, 13 hand-arm)를 다룬다.

**원본 데이터셋(Table 2)**: EgoDex(9,000만 프레임), ARCTIC, OakInk2, HOI4D, HO-Cap.

**데이터 큐레이션 파이프라인(Figure 2)**:

| 단계 | 처리 내용 |
|---|---|
| 분할(Segmentation) | 사람 손/팔 영역을 분할하고 전경 제거 (기본 SAM3 사용) |
| 배경 인페인팅 | 가려졌던 배경을 비디오 인페인팅으로 복원 (기본 ProPainter, 시간적 일관성 이유로 단일 이미지 인페인팅보다 선호) |
| 손 리타게팅 | MANO/3D 손 포즈를 로봇 관절 상태로 변환. 위치 기반·벡터 기반을 결합한 하이브리드 최적화로 대략 정렬 후 기구학 제약 하 위치 기반 리타게팅으로 정교화 |
| 팔 리타게팅 | 1인칭 영상에서 로봇 베이스가 안 보이므로 카메라 기준 가상 베이스(camera-relative virtual base)를 시퀀스별로 정의·고정. 수평 이동·yaw에 대한 형상 적응형 국소 탐색, IK 타당성·관절 한계·충돌·궤적 품질로 후보 평가 후 상위 3개 중 사람이 하나 선택(타당한 해가 없으면 시퀀스 제외) |
| 렌더링·합성 | 매칭된 1인칭 카메라 시점으로 목표 URDF를 렌더링해 복원된 장면에 합성 |
| 하모나이제이션 | Harmonizer(~20MB)로 조명·색·대비 등 외형만 조정(관절/손목/물체 상태 불변). 결과가 최종 pseudo-GT(유사 정답) |

각 단계마다 자동 QC + 사람 스크리닝을 거치고 실패 샘플은 제외한다.

**벤치마크 프로토콜**: Hand-only(손 영역만 로봇 손으로 치환)와 Hand-Arm(팔까지 편집, 더 큰 배경 보존·팔 기구학 요구로 더 어려움) 두 트랙. URDF 손 계열은 Ability, Allegro, DexHand(021), Inspire(RH56DFX·RH5DG2), Leap, OrcaHand, Revo2, Schunk SVH, Shadow Hand, Sharpa, Wuji, RoHand 등이고 팔 플랫폼은 Jaka, KUKA, Panda, RM(65·75), UR5, xArm. 각 트랙 테스트셋은 1K 이미지 × 13 목표 형상으로 구성되며, 모든 결과는 이미지 단위로 보고한다.

**평가 지표(3축)**:
1. **일반 유사도**: 전체 이미지·편집 ROI·배경 세 영역에서 PSNR↑, SSIM↑, LPIPS↓, FID↓.
2. **VLM 판정(GPT-4o)**: 의미 일관성 $SC$(형상 정확성·사람 손 제거·상호작용 보존·장면 일관성)와 지각 품질 $PQ$(자연스러움·아티팩트 부재·국소 일관성)를 [0,1]로 정규화해 $S_{vlm} = SC \cdot PQ$.
3. **Embodiment-aware 지표**: 사람 손 제거 $S_{rem}=1-N_{skin}(\hat{y},M)/N(M)$; 구조 충실도(DINOv2 특징 코사인 유사도), 정체성 충실도($S_{ID}=\lambda S_{ref}+(1-\lambda)S_{Lab}$, CLIP 기반 URDF 참조 일치 + CIELAB 색 일관성, $\lambda=0.5$, $\tau_{Lab}=25$); 상호작용 일관성 $S_{int}=1-\mathrm{LPIPS}(x\odot M_O, \hat{y}\odot M_O)$(물체 접촉 영역에서 측정).

**평가 대상 11종**: GPT-Image-2, Nano-Banana-2, GPT-Image-1.5, Seedream-4.5, Flux-2-Pro, Hunyuan-Image-3.0, Nano-Banana, Qwen-Image-Edit-2511, Flux-Kontext-Max, Omnigen2, FireRed-Image-Edit-1.1.

## 실험 결과 / 연구 의의
**Hand-only 트랙 주요 지표(Table 4에서 발췌, ↑ 좋음)**:

| 모델 | 손 제거 | 구조 충실도 | 정체성 충실도 | 상호작용 | VLM |
|---|---|---|---|---|---|
| GPT-Image-2 | 0.953 | **0.780** | 0.852 | **0.703** | 0.663 |
| GPT-Image-1.5 | 0.955 | 0.730 | **0.915** | 0.435 | **0.765** |
| Nano-Banana-2 | 0.925 | 0.746 | 0.792 | 0.617 | 0.692 |
| FireRed-Image-Edit-1.1 | 0.952 | 0.630 | 0.890 | 0.293 | 0.292 |
| Pseudo-GT (상한) | 0.964 | 1.000 | 0.964 | 0.821 | 0.623 |

**일반 유사도 대표값(Hand-only, Table 3)**: GPT-Image-2가 ROI LPIPS 0.482·ROI FID 99.71로 국소 편집 품질에서 최상위, 반면 하위권 모델들은 ROI FID가 130~149대로 크게 뒤진다.

**Hand-Arm 트랙(Table 6)**: 팔까지 편집하는 더 어려운 트랙에서 VLM 점수 최고는 GPT-Image-1.5(0.856), 구조 충실도·상호작용 최상위는 대체로 GPT-Image-2(구조 0.778, 상호작용 0.595). Pseudo-GT 상한 대비 정체성 충실도(모델 최고 0.6대 vs 상한 0.962)와 상호작용에서 격차가 두드러진다.

**핵심 발견**:
- **GPT-Image-2가 종합적으로 가장 강력**한 베이스라인으로, ROI LPIPS·FID, 구조 충실도, 상호작용 점수에서 두 트랙 모두 우위.
- **VLM 판정만으로는 불충분**: VLM 최고점(GPT-Image-1.5)이라도 구조 충실도·상호작용 보존은 최상이 아니다. VLM은 고수준 의미/지각 품질을 잘 잡지만, 미세한 형상과 접촉 수준 상호작용은 embodiment-aware 지표가 더 잘 반영한다.
- **지각적으로 자연스러움 ≠ 과제 성공**: FireRed-Image-Edit-1.1은 $PQ$가 가장 높지만 $SC$와 embodiment-aware 점수는 낮다.
- **진짜 병목은 embodiment-aware 편집**: 대부분 모델이 사람 손 제거(비교적 쉬움)에서는 0.9대 고득점이지만, 구조·정체성 충실도와 상호작용 보존에서 pseudo-GT 상한 대비 큰 격차를 보인다.
- 지표 타당성 검증용 블라인드 인간 평가도 수행(부록 F).

**의의**: HandEdit는 사람→로봇 다관절 손 이미지 편집을 위한 최초의 전용 데이터셋·벤치마크로, 이미지 편집과 로보틱스의 교차점 자원이다. 짝지어진 (사람 원본, 로봇 형상) 데이터로 사람→로봇 편집 모델을 학습시켜 사람 영상에서 로봇 중심 관측을 생성하면, 비싼 실로봇/원격조작 데이터 수집을 줄이고 확장 가능한 로봇 학습을 가능케 한다.

## 한계
본문에 별도 "Limitations" 절은 없다. 다만 구조상 내재된 제약을 정리하면: 목표가 실제 로봇 촬영이 아니라 리타게팅·렌더링·합성으로 만든 **pseudo-GT(유사 정답)**라는 점, 팔 리타게팅에서 가상 베이스 선택에 **사람 조작자가 개입**한다는 점, 카메라 기준 가상 베이스의 높이·roll·pitch를 직립 마운팅 가정으로 고정한다는 점 등이 있다. 저자들은 현재 모델의 약점(형상 사전지식 부족, 구조·정체성 충실도·상호작용의 어려움)을 한계 절이 아니라 동기·발견으로 제시한다.

## 우리 연구와 연결되는 점
- **Egocentric Vision**: 이 연구는 1인칭 손-물체 조작 프레임을 입력으로 삼아 손/팔 영역을 재합성하는 문제로, 1인칭 시점의 손 분할(SAM3)·배경 인페인팅(ProPainter)·시점 정합 파이프라인이 그대로 참고 가치가 있다. 1인칭 데이터의 확장성을 로봇 학습으로 잇는 관점은 egocentric 표현 학습·도메인 갭 완화 연구와 직접 맞닿는다.
- **Hand-Object Interaction**: MANO 손 포즈의 로봇 리타게팅, 접촉 영역($M_O$) 기반 상호작용 일관성 지표($S_{int}$), 손-물체 접촉 보존을 편집 품질의 핵심 기준으로 둔 설계는 HOI에서 접촉·조작 의미를 정량화하려는 우리 연구에 유용한 평가 틀을 제공한다. 특히 "지각적 자연스러움과 접촉 수준 정확도가 분리된다"는 발견은 HOI 생성/편집 평가 지표 설계에 시사점이 크다.
- **Spatial Audio**: 직접적 연관은 없으나, 조작 이벤트를 여러 모달리티로 정합할 때 접촉 시점·물체 상태 보존을 기준으로 삼는 발상(접촉 영역 마스크 기반 일관성)은 손-물체 접촉음 같은 공간 음향과 시각 조작을 동기화하는 과제로 확장해 생각해 볼 여지가 있다.

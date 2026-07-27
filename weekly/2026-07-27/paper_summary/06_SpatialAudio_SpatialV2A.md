# SpatialV2A: Visual-Guided High-fidelity Spatial Audio Generation

**arXiv**: 2601.15017 | **주제 분류**: Spatial Audio | **출판일**: 2026-01-21 | **학회**: 프리프린트
**저자/소속**: Yanan Wang, Linjie Ren, Zihao Li, Junyi Wang, Tian Gan (School of Computer Science and Technology, Shandong University / 산둥대학교)
**링크**: https://arxiv.org/abs/2601.15017

## 한 줄 요약

영상을 보고 소리를 만드는 Video-to-Audio(V2A, 영상→오디오 생성) 기술이 지금까지 놓쳤던 "공간감(spatial perception)"을 정면으로 다룬 연구다. 대규모 양이(binaural, 좌·우 두 채널로 방향감을 주는) 데이터셋 BinauralVGGSound를 새로 만들고, 영상 속 소리 위치 단서를 활용해 의미·시간 정합을 유지하면서도 입체적인 양이 오디오를 생성하는 SpatialV2A 프레임워크를 제안한다.

## 메인 그림

Figure 1: 기존 V2A와 제안 방법 SpatialV2A의 비교. (a) 전통적 V2A는 방향·위치 단서가 없는 mono(단일 채널) 오디오를 생성해 공간감을 전달하지 못한다. (b) SpatialV2A는 영상과 공간적으로 일치하는 binaural(양이) 오디오를 생성하여, 소리가 화면 속 사건의 위치·움직임과 맞물리도록 한다. (원문 HTML의 그림 이미지는 변환 아티팩트 경로로만 제공되어 유효한 절대 URL을 확보하지 못해 텍스트로 서술한다.)

## 선행 연구

V2A 생성 연구는 그동안 두 가지 정합(alignment)을 개선하는 데 집중해 왔다.

- **의미 정합(semantic alignment)**: 생성된 소리가 영상 속 사물·행동·장면과 맞는지. Im2Wav, MMAudio는 CLIP 인코더로 시각-텍스트 의미를 정렬하고, Diff-Foley는 대조학습(contrastive) 기반 오디오-비주얼 사전학습을 사용한다.
- **시간 정합(temporal alignment)**: 소리가 화면 사건과 시간적으로 동기화되는지. SpecVQGAN, Diff-Foley, Synchformer(어텐션 기반 세밀 동기화) 등이 대표적이며, V-AURA·MMAudio가 Synchformer를 통합해 효과를 검증했다.

한편 소리를 입체적으로 만드는 갈래로는, 시각 정보로 장면 기하와 음원 위치를 추론해 mono를 binaural로 바꾸는 **오디오 공간화(audio spatialization)** 연구가 있다. PseudoBinaural은 시각 정보로부터 양이 간 레벨차(ILD)·시간차(ITD)를 예측해 그럴듯한 스테레오/양이 오디오를 합성한다. 또한 음원 위치 추정(sound source localization)에서 ACL은 음원 위치뿐 아니라 프레임 단위 히트맵으로 소리 나는 영역의 상대 강도·분포까지 예측한다.

## 문제 제기

기존 V2A는 대부분 **mono 오디오**만 생성해 방향·위치 단서가 없어 실감 나는 공간감을 주지 못한다. 근본 원인은 학습에 쓰는 데이터셋(예: VGGSound)이 mono 오디오라 시각→공간 오디오 매핑을 배울 양이 정보 자체가 없기 때문이다. 반대로 See-2-Sound 같은 시각 기반 공간 오디오 생성 방법은 실제 오디오 신호를 활용하지 않고 시각만으로 공간 오디오를 만들어, 소리와 시각 장면 간 의미·시간 정합이 약하다.

즉 **의미 충실도 + 시간 일관성 + 공간 실재감**을 동시에 만족하는 V2A 프레임워크가 없다는 것이 핵심 문제다. 이를 풀려면 두 가지 난제를 넘어야 한다. (1) 시각 장면에서 공간 음향 단서를 직접 추론하는 명시적 공간화 모듈이 필요하고, (2) 대규모 양이 데이터셋이 부족한데 실제 양이 녹음은 전용 장비와 큰 비용이 들어 확장이 어렵다.

## 연구 주제

**공간 인지가 가능한(spatially aware) V2A 생성**을 목표로 한다. 구체적으로, 영상 입력으로부터 세밀한 공간 표현을 모델링해 좌·우 두 채널의 양이 스테레오 오디오를 생성하되, 기존 V2A가 확보한 의미·시간 정합을 훼손하지 않는 것을 지향한다.

## 연구 방법

### 1) 데이터셋 구축: BinauralVGGSound

실제 양이 녹음의 높은 비용을 우회하기 위해, 기존 mono 데이터셋 VGGSound를 시각 기반 공간화로 양이 오디오로 변환한다. 파이프라인은 두 부분이다.

- **데이터 전처리**: (1) 10초 미만 클립 제거(충분한 시간 맥락 확보), (2) 오디오 활동 검출로 80% 이상이 무음인 영상 제거, (3) Meta Audiobox Aesthetics Toolkit으로 품질 낮은 오디오 필터링.
- **Mono→Binaural 변환**: mono 신호 $s(t)$를 구면 조화(Spherical Harmonic, SH) 영역으로 표현해 가상 방향 성분 $s'_m(t)=(D^\top D)^{-1}D^\top \Psi(t)$로 투영한 뒤, HRIR(Head-Related Impulse Response, 머리 형상에 따른 소리 전달 특성) 기반 렌더링으로 의사 양이(pseudo-binaural) 신호를 만든다: $\hat{l}(t)=\sum_{m=1}^{M} h_l(\vartheta'_m)*s'_m(t)$, $\hat{r}(t)=\sum_{m=1}^{M} h_r(\vartheta'_m)*s'_m(t)$. 이 의사 양이 신호를 지도로 삼아 PseudoBinaural 방식(STFT 영역 U-Net 백본 + ResNet-18 시각 특징 주입 + APNet 분리 모듈)의 시각 기반 양이 생성 모델을 학습하고, 이를 VGGSound 전체에 적용해 최종 데이터셋을 만든다.

기존 데이터셋 대비 규모·다양성이 강점이다.

| 데이터셋 | 타입 | 클립 수 | 총 길이 | 클래스 수 | 캡션 |
|---|---|---|---|---|---|
| Fair-Play | Binaural | 1.9k | 5.2h | - | 없음 |
| SimBinaural | Binaural | 22k | 116.1h | 11 | 없음 |
| YouTube-Binaural | Binaural | 0.4k | 27h | - | 없음 |
| VGGSound | Mono | 199k | 550h | 309 | 있음 |
| **BinauralVGGSound (제안)** | **Binaural** | **187k** | **519h** | **309** | **있음** |

데이터 검증에서 양이 변환 후에도 원본 VGGSound와 비슷하거나 약간 높은 오디오 품질(CE/CU/PQ)을 유지하며, mono에는 전혀 없던 공간 지표(IACC, ILD, ITD, ISD, IPD)가 뚜렷하게 나타남을 확인했다.

| 데이터셋 | CE↑ | CU↑ | PQ↑ | IACC↓ | ILD↑ | ITD↑ | ISD↑ | IPD↑ |
|---|---|---|---|---|---|---|---|---|
| VGGSound | 3.71 | 5.39 | 6.07 | - | - | - | - | - |
| BinauralVGGSound (제안) | 3.74 | 5.44 | 6.09 | 0.93 | 3.08 | 1.70 | 0.07 | 0.32 |

### 2) 프레임워크: SpatialV2A

**Conditional Flow Matching(CFM)** 위에 시각 기반 공간 단서를 결합한 이중 분기(dual-branch) 구조다. CFM은 단순한 사전 분포에서 목표 데이터 분포로 샘플을 옮기는 조건부 속도장(velocity field)을 학습한다. 표준 CFM은 하나의 속도장 $v_\theta(x_t,t,\mathbf{C})$를 학습하지만, 여기서는 좌·우 채널별로 두 속도장 $v_\theta^l$, $v_\theta^r$을 학습한다. 양이 목표 $x_1=(x_1^l,x_1^r)$에 대해 채널별 중간 상태 $x_t^a=(1-t)x_0^a+tx_1^a$ ($a\in\{l,r\}$)를 두고, 목적함수는 다음과 같다:

$$\sum_{a\in\{l,r\}} \mathbb{E}\,\|v_\theta^a(x_t^a,t,\mathbf{C})-u(x_t^a\mid x_0^a,x_1^a)\|^2.$$

- **다중모달 결합 표현(Multimodal Joint Representation)**: MMAudio 설계를 따라 텍스트 $F_{\text{text}}$, 시각 $F_{\text{vis}}$, 동기화 $F_{\text{sync}}$ 특징(CLIP, Synchformer 사용)으로 의미·시간 정합의 공유 조건을 만든다. 전역 조건 $C_g=F_{\text{text}}\oplus F_{\text{vis}}\oplus e(t)$, 프레임 조건 $C_f=F_{\text{sync}}\oplus C_g$.
- **단일모달 이중 채널 표현(Unimodal Dual-Channel)**: 다중모달 단계 이후 좌·우 분기로 분리해 각 채널 고유의 공간 특성을 독립적으로 합성한다.
- **시각 기반 오디오 공간화 모듈(Visual-guided Audio Spatialization)**: 사전학습 ACL로 소리 나는 영역·마스크·히트맵을 뽑아 5개 공간 특징을 계산한다 — 수평 위치 $S_h$, 소리 영역 비율 $S_{\text{area}}$, 히트맵 분산 $S_{\text{var}}$, 좌우 에너지 편향 $S_{LR}$, 분포 형태 $S_{\text{shape}}$. 이를 이어붙인 $S_{\text{sound}}$를 ConvMLP+업샘플로 잠재 공간에 투영·정규화해 공간 조건 $C_s$를 만들고 flow-matching 과정에 주입한다.

학습·추론은 오디오를 사전학습 VAE로 잠재로 인코딩한 뒤 양이 CFM으로 학습하고, 추론 시 좌·우 채널을 가우시안 노이즈에서 시작해 양이 잠재로 변환한 후 VAE 디코딩 → BigVGAN 보코더로 파형을 만든다. 다중모달 결합 블록 $N_1=6$개, 단일모달 이중 채널 블록 $N_2=12$개, 16 kHz 샘플링, RTX 6000 3장에서 300K 스텝 학습.

## 실험 결과 / 연구 의의

VGGSound 테스트에서 무작위 추출한 3,000개 영상(BinauralVGGSound와 동일 ID)으로 SOTA V2A들과 비교했다.

**분포 정합 · 시간 · 의미 정합 (Table 3)**: SpatialV2A는 KL 발산과 DeSync(시간 비동기)에서 최저치를 기록하고 분포 지표에서 1위 또는 2위를 유지하며, MOS-T(주관적 시간 정합) 최고, MOS-Sem(주관적 의미 정합) 2위를 달성했다.

| 방법 | $KL_{PaSST}$↓ | $KL_{PANNs}$↓ | IB↑ | DeSync↓ | MOS-Sem↑ | MOS-T↑ |
|---|---|---|---|---|---|---|
| ReWaS | 2.47 | 2.51 | 0.18 | 1.19 | 2.31 | 2.21 |
| Frieren | 2.62 | 2.60 | 0.22 | 0.85 | 3.40 | 2.78 |
| Seeing&Hearing | 2.66 | 2.78 | 0.36 | 1.20 | 2.60 | 2.53 |
| MMAudio | 1.57 | 1.59 | 0.29 | 0.51 | 4.11 | 4.05 |
| SEE-2-SOUND | 3.36 | 4.39 | 0.07 | 1.27 | 1.60 | 1.51 |
| **SpatialV2A (제안)** | **1.56** | **1.55** | 0.28 | **0.49** | 4.08 | **4.14** |

(Seeing&Hearing이 IB 최고인 것은 추론 시 ImageBind 유사도를 직접 최적화하기 때문이라고 저자가 설명한다.)

**오디오 품질 · 공간 정합 (Table 4)**: SpatialV2A가 IS·CE·CU·PQ 등 품질 지표 전반에서 최고이며, 다른 baseline은 대부분 mono/비공간 오디오라 공간 지표 자체가 적용되지 않는다. 주관 평가에서 MOS-AQ 4.21, MOS-S(공간 인상) 3.90으로 가장 높다.

| 방법 | $IS_{PaSST}$↑ | CE↑ | CU↑ | PQ↑ | MOS-AQ↑ | MOS-S↑ |
|---|---|---|---|---|---|---|
| ReWaS | 7.86 | 3.54 | 4.82 | 5.34 | 2.29 | 1.26 |
| Frieren | 9.10 | 3.65 | 5.26 | 5.85 | 3.15 | 1.29 |
| Seeing&Hearing | 5.39 | 3.06 | 4.49 | 5.25 | 2.42 | 1.50 |
| MMAudio | 11.86 | 3.88 | 5.14 | 5.71 | 3.87 | 1.78 |
| SEE-2-SOUND | 1.52 | 3.03 | 4.83 | 5.39 | 1.74 | 2.49 |
| **SpatialV2A (제안)** | **14.36** | **4.09** | **5.77** | **6.07** | **4.21** | **3.90** |

**Ablation (Table 5)**: 공간화 모듈을 끄면(w/o Spat.) FAD는 약간 좋아지지만, 의미 정합(IB), 시간 동기(DeSync), 지각 품질(IS), 양이 공간 지표(IACC, ILD)는 전 항목에서 열화된다. 즉 시각 기반 공간화가 약간의 분포 변동을 감수하는 대신 시간·의미·공간 실재감을 크게 끌어올린다는 것을 보인다.

**의의**: V2A에서 소홀히 다뤄진 공간 인지를 정면으로 다뤄, 대규모 양이 데이터셋과 이중 분기 프레임워크로 의미·시간·공간 정합을 동시에 만족하는 고품질 양이 오디오 생성을 실증했다. 데이터셋·코드·체크포인트를 공개할 예정(데모: https://github.com/renlinjie868-web/SpatialV2A).

## 한계

- **의사 양이 지도(pseudo-binaural supervision)의 근본적 한계**: 실제 양이 녹음이 아니라 PseudoBinaural로 mono에서 합성한 신호를 학습 목표(ground-truth)로 삼는다. 따라서 데이터의 공간 정보는 시각 기반 추정과 SH/HRIR 렌더링 품질에 의존하며, 실제 물리적 양이 녹음이 가진 정확도와는 차이가 있을 수 있다.
- **의미 근거(semantic grounding)의 개선 여지**: 저자 스스로 WavCaps, AudioCaps 같은 캡션 데이터셋을 추가해 의미 근거를 강화하는 것을 향후 과제로 제시한다.
- **장기 시간 모델링 미해결**: 긴 영상에서 일관된 양이 합성을 위한 장기 시간 모델링용 고급 아키텍처 탐색이 future work로 남아 있다.
- 짧은(10초 미만) 클립을 걸러내 학습해, 짧은 구간에 대한 일반화는 확인되지 않았다.

## 우리 연구와 연결되는 점

- **공간 오디오 생성 파이프라인 설계**: 실제 양이 녹음 없이도 mono 대규모 데이터를 시각 기반 공간화로 양이로 확장하는 전략은, 데이터 확보가 어려운 공간 오디오 과제에서 재사용 가능한 데이터 부트스트래핑 방법론이다.
- **시각 단서의 명시적 공간 조건화**: ACL 히트맵에서 수평 위치·영역 비율·분산·좌우 에너지 편향·분포 형태 5개 특징을 뽑아 생성 모델에 조건으로 주입하는 설계는, 시각-오디오 정렬을 다루는 연구에서 "공간 조건 표현"을 어떻게 구성할지에 대한 구체적 레시피가 된다.
- **CFM의 이중 채널 확장**: 단일 속도장을 좌·우 채널별 속도장으로 나눈 이중 분기 flow-matching은, 다채널/멀티스트림 생성으로 확장할 때 참고할 수 있는 구조적 아이디어다.
- **평가 지표 세트**: 분포(FAD/KL), 의미(IB), 시간(DeSync), 품질(IS/CE/CU/PQ), 공간(IACC/ILD/ITD/ISD/IPD) + MOS 주관 평가로 이어지는 다차원 평가 프로토콜은 공간 오디오 연구의 벤치마크 설계에 바로 활용 가능하다.

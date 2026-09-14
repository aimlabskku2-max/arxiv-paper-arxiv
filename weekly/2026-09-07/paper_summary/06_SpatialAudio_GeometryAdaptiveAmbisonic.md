# Geometry-adaptive Ambisonic encoding for sparse microphone arrays of variable topology using physics-informed diffusion

**arXiv**: 2608.16240 | **주제 분류**: Spatial Audio | **출판일**: 2026-08-17 | **학회**: 프리프린트 (eess.AS / cs.SD)
**저자/소속**: Xiang Zhou, Zhengqiao Zhao, Zhengding Luo, Wen Zhang — Northwestern Polytechnical University(西北工业대, 지능음향·몰입형통신 센터, 중국 시안) 및 Nanyang Technological University(난양공과대, DSP Lab, 싱가포르)
**링크**: https://arxiv.org/abs/2608.16240

## 한 줄 요약
마이크가 몇 개 안 되고 배치도 제각각인 희소(sparse) 마이크 배열에서 고차 Ambisonics(앰비소닉스, 구면조화 기반 공간음향 표현)를 안정적으로 인코딩하기 위해, 물리 기반 투영 프런트엔드와 조건부 확산 모델(diffusion model)을 결합한 DiffM2A를 제안한 논문이다.

## 메인 그림
![DiffM2A 개요](https://arxiv.org/html/2608.16240v1/pic/Figure_1.png)

논문 Figure 1은 DiffM2A 전체 파이프라인을 보여준다. 왼쪽에서 희소 마이크 배열의 다채널 관측 $\mathbf{x}(t,f)$가 들어오면, GASHP 프런트엔드가 배열의 기하·경계 정보를 반영한 구면조화(SH) 모달 특징 $\mathbf{D}$를 만든다. 이어 조건화 분기(conditioning branch)가 원신호와 $\mathbf{D}$를 융합해 조건 $\mathbf{c}$를 만들고, 잡음화 분기(denoising branch)가 이 조건 아래에서 Ambisonic 계수 $\mathbf{a}_N$을 추정한다. 학습 시에는 목표 계수에 가우시안 잡음을 더해 $\mathbf{a}_N^{\sigma}$를 만들고, 추론 시에는 순수 가우시안 잡음에서 시작해 DPM-Solver로 반복적으로 잡음을 제거해 계수를 복원한다.

## 선행 연구
- **신호처리 기반 인코딩**: 최소자승·의사역행렬(pseudo-inverse) 기반 선형 인코더는 배열 전달함수가 정확하고 샘플링 행렬이 잘 조건화(well-conditioned)돼 있을 때 효과적이다. 정규화(regularization)로 수치 안정성을 높일 수 있지만 공간 정확도를 희생한다. 파라메트릭(parametric) 방식은 장면 의존 모델로 유연하지만 도래각(DOA) 추정과 희소 장면 가정에 의존한다.
- **신경망 인코더**: 마이크 신호에서 Ambisonic 계수로의 매핑을 학습한다. 기하 조건 U-Net(Gen-A), 공간 파워맵 지도학습(AmbiSpatial), 배열 전달함수에 대한 교차어텐션(cross-attention) 등이 대표적이다. 명시적 역필터링 부담을 줄여준다.
- **생성 모델 기반 접근**: DiffAU(FOA→HOA 업믹싱), SIRUP(스티어링 벡터 잠재확산 업믹서), Flow-HOA(플로우 매칭으로 인코딩용 FIR 필터뱅크 생성) 등이 과소결정(underdetermined) 공간음향 문제에 생성 사전(generative prior)의 잠재력을 보였다.

## 문제 제기
Ambisonics는 콤팩트한 장면 기반(scene-based) 공간음향 표현이지만, 고차 Ambisonics(HOA)의 견고한 획득은 여전히 어렵다. 특히 웨어러블·임베디드 기기는 (1) 마이크 수가 적고, (2) 위치가 산업 디자인 제약으로 정해지며, (3) 기하가 불규칙하고, (4) 기기별 경계조건(개방형 배열 vs. 강체 구면 배플)에 종속된다. 이 때문에 SH 도메인 인코딩이 조건불량(ill-conditioned)이 되어, 역필터링은 잡음을 증폭하고($\mathbf{A}^{\dagger}\mathbf{n}$에서 작은 특이값이 $1/\sigma_\ell$로 증폭), 결정론적 신경망은 배열별 응답에 과적합하거나 모호한 고차 성분을 뭉개버린다(과평활, over-smoothing). 또한 $M < (N+1)^2$이면 순방향 행렬이 널공간을 가져 해가 유일하지 않은데, 계수별 회귀 손실은 이 모호성을 평균화된 추정으로 얼버무리기 쉽다. 기존 재구성 손실은 채널을 독립으로 취급해 저차 음향 인텐시티 일관성이나 회전 등변성(rotational equivariance) 같은 공간 관계를 반영하지 못한다.

## 연구 주제
마이크 수 $M$은 고정하되 좌표 $\Omega$가 매번 달라지는 "가변 토폴로지(variable-topology)" 희소 배열에서, 복소 Ambisonic 계수를 추정하는 문제를 다룬다. 저자들은 이를 닫힌 형태의 역문제가 아니라 **관측 조건부 통계 추정(observation-conditioned estimation)** 문제로 재정의한다. 5개 마이크로 1차(FOA)·2차(SOA) Ambisonics를 인코딩하는, 본질적으로 과소결정된 설정을 대상으로 한다.

## 연구 방법
DiffM2A는 물리 기반 프런트엔드와 조건부 확산 백본을 결합한다.

- **GASHP (Geometry-Adaptive Spherical Harmonic Projection)**: 선택한 음향 경계 모델(개방형은 식 (2)의 구면 베셀 함수, 강체 구면은 식 (3)의 산란 반영 방사 응답)로 경계 인지 SH 스티어링 벡터를 구성한다. 의사역행렬 $\mathbf{B}^{\dagger}$를 계산하는 대신, 각 모드에 대해 에너지 정규화 정합필터 투영 $d_k(t,f) = \mathbf{b}_k^H \mathbf{x} / \lVert \mathbf{b}_k \rVert_2$을 적용한다. $\lVert \mathbf{b}_k \rVert_2^2$가 아니라 $\lVert \mathbf{b}_k \rVert_2$로 정규화하므로 결과는 모달 결합 행렬 $\mathbf{\Gamma}(f)$가 섞인 관측 $\mathbf{d} = \mathbf{\Gamma}(f)\mathbf{a}_N + \eta$가 되며, 이는 편향 없는 추정이 아니라 "결합된 모달 관측"이다. 대신 공간 백색 잡음에 대한 투영 후 분산이 $\sigma^2$로 유지되어(식 (20)) 의사역행렬 특유의 특이값 의존 잡음 증폭을 피한다. 남는 스케일링·교차모드 누설·경계 불일치는 하류 확산 모델이 처리한다.
- **이중 분기 조건부 확산 잡음제거기(Dual-Branch EDM)**: "이중 분기"는 조건화 분기와 잡음제거 분기의 분리를 뜻한다. 조건화 분기(Conditional U-Net)는 마이크 원신호 $\mathbf{x}$와 GASHP 특징 $\mathbf{D}$를 융합해 $\mathbf{c}=\mathcal{F}_{\text{cond}}(\mathbf{x},\mathbf{D})$를 만든다. 잡음제거 분기는 Karras 등의 EDM(Elucidated Diffusion Model) 전처리 파라미터화(식 (23)~(24))를 써서 $\mathbf{c}$ 조건 아래 계수를 추정하고, 가중 잡음제거 목적함수 $\mathcal{L}_{\text{EDM}}$(식 (25))로 학습한다. 복소 계수는 실부·허부를 채널 축으로 이어붙여 표현한다.
- **다단 공간 제약(Multi-Tiered Spatial Constraints)**: (1) 저차 단계는 능동 유사 인텐시티 벡터(IV) 손실 $\mathcal{L}_{\text{IV}}$로 FOA 부공간의 방향 에너지 흐름과 위상 민감 채널 관계를 제약한다. (2) 고차 단계는 $\mathrm{SO}(3)$ 회전에 대한 실수값 Wigner-D 행렬 변환 구조를 이용한 회전 일관성 손실 $\mathcal{L}_{\text{rot}}$로 SH 부공간의 등변 거동을 강제한다. 최종 목적함수는 $\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{EDM}} + \lambda_{\text{IV}}\mathcal{L}_{\text{IV}} + \gamma\lambda_{\text{rot}}\mathcal{L}_{\text{rot}}$이며, DOA 메타데이터 없이 동작한다.
- **구현**: 16 kHz, STFT를 $256\times256$로 자르거나 패딩. 입력은 5채널 실/허부(10채널), 출력은 FOA 8채널·SOA 18채널. 베이스 채널 32, 채널 배수 $\{1,2,4,8\}$인 2D U-Net에 4-head self-attention. Adam($\text{lr}=10^{-4}$), 200 에폭, 추론은 64-step DPM-Solver. 실환경 LOCATA에는 강체 구면 반경 $a=0.042$ m를 쓰고 30 에폭 미세조정(EMA decay 0.999).

## 실험 결과 / 연구 의의
**데이터셋**: 시뮬레이션(HARP 기반 RIR, 방 $4^3$~$12\times12\times8$ m, $T_{60}$ 0.05~0.9 s, 학습 5000장면×100배열, 검증/테스트 배열은 학습과 서로소), 반경 0.09 m 구 안에 마이크 5개 무작위 배치, 음원은 WSJ0. 실환경은 LOCATA(Eigenmike 32채널 중 5채널만 입력, 32채널 인코딩을 참조로 사용).

**시뮬레이션 성능 (Table 1, 단일 음원 기준)** — SI-SDR·Coherence는 높을수록(↑), Mag.Err·ILD.Err는 낮을수록(↓) 좋음:

| Task | Method | SI-SDR↑ (dB) | Coh↑ | Mag.Err↓ (dB) | ILD.Err↓ (dB) |
|---|---|---|---|---|---|
| FOA | Attention-based | 12.43 | 0.654 | 7.90 | 3.82 |
| FOA | **DiffM2A(제안)** | **15.42** | **0.687** | **6.42** | 3.57 |
| SOA | Attention-based | 10.64 | 0.311 | 8.47 | 4.89 |
| SOA | **DiffM2A(제안)** | **13.51** | **0.461** | **7.60** | **3.98** |

**실환경 LOCATA 성능 (Table 2, 이중 음원 SOA)**:

| Method | SI-SDR↑ (dB) | Coh↑ | Mag.Err↓ (dB) | ILD.Err↓ (dB) |
|---|---|---|---|---|
| Attention-based | 2.11 | 0.48 | 5.42 | 3.98 |
| **DiffM2A(제안)** | **5.62** | **0.71** | **3.35** | **2.48** |

- **주파수 범위**: 이중 음원 SOA에서 $-3$ dB 코히런스 임계 기준 유효 상한 주파수가 AmbiSpatial 1317 Hz, Gen-A 1631 Hz, Attention 1945 Hz, 파라메트릭 2133 Hz인 반면 DiffM2A는 3106 Hz까지 확장된다(다만 5 kHz 이상에서는 잡음 바닥에 접근).
- **센서 도메인 재투영 (Table 3, 이중 음원 SOA)**: 추정 SOA를 다시 5채널 마이크 공간으로 투영했을 때 DiffM2A가 SI-SDR 8.05 dB / Mag.Err 3.14 dB로 최고이며, 참조 GT SOA(6.86 dB)보다도 높다. 2차 HOA 표현 자체가 절단 오차로 마이크 신호를 완전히 담지 못하는 반면, DiffM2A는 생성 사전으로 관측에 더 부합하는 물리적으로 그럴듯한 계수를 복원한다.
- **어블레이션 (Table 4, 이중 음원 SOA)**: $\mathcal{L}_{\text{EDM}}$만 쓰면 SI-SDR 6.75 dB, +$\mathcal{L}_{\text{IV}}$ 7.32, +$\mathcal{L}_{\text{rot}}$ 8.54, 전부 결합 시 9.74 dB. GASHP 제거 시 7.16 dB로 하락. 확산 대신 결정론적 회귀(GASHP + U-Net)는 7.21 dB / 0.282에 그쳐, 확산 백본이 SI-SDR 2.53 dB·코히런스 0.123만큼 우위임을 확인.
- **미지 배열 일반화 (Table 5)**: 학습에 없던 원형·선형 배열 4종 평균 SI-SDR에서 DiffM2A 9.78 dB로, 다음으로 좋은 방법(7.41 dB) 대비 우위. GASHP 제거 시 7.47 dB로 하락. 파라미터 8.66 M.

**의의**: 물리 기반 경계 인지 투영(GASHP)이 배열별 변동성을 흡수해 공통 모달 표현을 만들고, 확산 모델이 과소결정 매핑의 모호성을 분포 인지 방식으로 해소함으로써, 희소·불규칙·가변 배열에서도 신호 충실도·공간 코히런스·바이노럴 큐(ILD) 보존을 동시에 개선했다. 경계 모델(개방형↔강체 구면)이 어긋난 상황에서도 성능이 유지된다.

## 한계
- **연산 비용**: 반복적 역방향 샘플링 때문에 4초/16 kHz 샘플당 추론 시간이 2.66 s로, 파라메트릭(0.35 s)이나 DL 베이스라인(0.93~1.36 s)보다 크게 느리다. 실시간·엣지 배포에는 부담. 저자들은 향후 빠른 샘플링과 모델 증류(distillation)를 제시한다.
- **고주파 한계**: 확장된 3106 Hz 이후 5 kHz 이상에서는 코히런스가 잡음 바닥에 접근한다.
- **경계 모델 확장 필요**: 현재 개방형·강체 구면 모델만 다루며, 웨어러블에 맞는 머리 산란·몸통 회절 등 세밀한 경계 모델은 향후 과제로 남겨둔다.
- **참조의 성격**: LOCATA 참조는 32채널 Eigenmike 인코딩 결과로, 이상적 연속 음장 GT가 아니라 배열 인코딩 참조다.

## 우리 연구와 연결되는 점
- **Spatial Audio 관점**: 희소·가변 배열이라는 현실적 제약 아래 HOA를 복원하는 문제 정의, 그리고 GASHP처럼 물리 순방향 모델(경계조건별 방사 응답, ACN/SN3D 규약)을 딥러닝 프런트엔드로 끌어들이는 설계는 웨어러블·모바일 공간음향 캡처 연구에 직접 참고가 된다. IV 손실·회전(SO(3)/Wigner-D) 등변 손실은 채널 독립 손실의 한계를 보완하는 공간 정규화 아이디어로 재사용할 수 있다.
- **생성/확산 모델 관점**: 과소결정 역문제를 결정론적 회귀 대신 조건부 확산으로 다뤄 과평활을 피하고, 오히려 참조 GT를 넘어서는 재투영 일관성을 얻은 사례다. 물리 기반 조건(관측 + 모달 특징 이중 조건화)과 EDM 전처리를 결합하는 틀은 다른 역문제형 신호 복원(예: 초해상, 음원 분리)에 이식 가능하다.
- **멀티모달/표현학습 관점**: 배열 기하가 매번 달라도 같은 $K=(N+1)^2$ 모달 채널로 사영해 입력 차원을 고정하는 GASHP의 "공통 표현화"는 도메인 시프트를 줄이는 조건화 전략으로, 이질적 센서·기하를 하나의 잠재 표현으로 정렬하려는 문제에 응용할 수 있다.

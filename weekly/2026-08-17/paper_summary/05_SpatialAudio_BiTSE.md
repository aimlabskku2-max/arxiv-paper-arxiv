# BiTSE: Binaural Target Speaker Extraction in Noisy Multi-Talker Environments for AR Glass Arrays

**arXiv**: 2608.10106 | **주제 분류**: Spatial Audio | **출판일**: 2026-08-10 | **학회**: APSIPA ASC 2026 (accepted, preprint 버전)
**저자/소속**: Selani A. Indrapala, Wageesha N. Manamperi (University of Moratuwa, Sri Lanka — Dept. of Electronic and Telecommunication Engineering)
**링크**: https://arxiv.org/abs/2608.10106

> **자료 확보 관련 주의**
> 이번 정리는 arXiv abs 페이지(초록·메타데이터)까지만 확보한 상태에서 작성했다. 전문 HTML(`https://arxiv.org/html/2608.10106v1`)과 PDF는 세션의 웹 페치 한도(HTTP 429)에 계속 막혀 1시간 넘게 재시도했지만 끝내 열지 못했다.
> 따라서 아래 내용 중 **구체적 수치, 표, ablation, 비교 대상 baseline 이름은 일절 싣지 않았다**(확인 불가 → 생략). 방법 설명은 초록에 명시된 범위까지이며, 그 밖의 문장은 "추정"임을 그때그때 밝혔다. 전문 접근이 가능해지면 연구 방법·실험 결과 절을 보강해야 한다.

## 한 줄 요약
AR 안경에 달린 마이크 어레이로 잡은 시끄러운 다중 화자 상황에서, 목표 화자의 **방향(DoA)**과 **말하는 구간(voice activity)** 두 단서를 함께 써서 그 사람 목소리만 양이(binaural) 신호로 뽑아내는 프레임워크를 제안한다.

## 메인 그림
전문 HTML을 열지 못해 **대표 그림의 이미지 URL을 확보하지 못했다.** 깨진 링크를 남기지 않기 위해 이미지는 싣지 않는다. 원본 그림은 https://arxiv.org/pdf/2608.10106 에서 확인할 수 있다.

초록에 서술된 구조를 기준으로 보면, 시스템의 뼈대는 **양이 신호 denoising 아키텍처** 위에 세 가지 모듈(DoA-aware attention, timestamp 기반 마스킹, 2단계 손실 학습)을 얹은 형태다. 다만 실제 Figure 1이 이 파이프라인 전체를 그린 것인지, 아니면 AR 안경 착용 시나리오를 그린 것인지는 확인하지 못했다.

## 선행 연구
> 참고문헌 목록을 확보하지 못해 **개별 선행 논문 이름과 arXiv ID는 적지 않는다.** 아래는 초록에서 이 논문이 스스로 위치시킨 연구 흐름만 정리한 것이다.

- **Target Speaker Extraction (TSE, 목표 화자 추출)**: 여러 사람이 동시에 말하는 혼합 신호에서, 어떤 단서(cue)를 주면 그 사람 목소리만 골라내는 문제. 기존에는 화자 등록 음성(enrollment)에서 뽑은 화자 임베딩을 단서로 쓰는 방식이 주류였다.
- **공간 단서 기반 분리**: 마이크 어레이가 있으면 도래 방향(direction-of-arrival, DoA)을 단서로 쓸 수 있다. 이 논문은 이 흐름 위에 있으며, DoA를 attention에 직접 주입하는 방식을 택한다.
- **AR 웨어러블 마이크 어레이 음성 향상**: SPEAR(SPeech Enhancement for Augmented Reality) 챌린지 데이터셋이 이 분야의 평가 기반으로 쓰이고 있고, 이 논문도 여기서 평가한다.
- **Binaural denoising 아키텍처**: 논문은 "binaural signal denoising architecture 위에 세운다(Built upon)"고 명시한다. 즉 완전히 새로운 백본을 설계한 것이 아니라, 기존 양이 잡음 제거 모델을 TSE로 확장한 구조다. 백본의 구체적 이름은 초록에 없다.

## 문제 제기
AR 안경 같은 웨어러블 기기에서 "지금 내가 듣고 싶은 그 사람" 목소리만 남기는 일은 다음 이유로 어렵다.

1. **시끄러운 다중 화자 환경**: 잡음 + 여러 화자가 겹치므로 단순 denoising으로는 목표 화자와 간섭 화자를 구분할 수 없다.
2. **단서의 부족**: 화자 등록 음성을 미리 받아두는 방식은 실사용 AR 시나리오에서 비현실적이다. 반면 AR 기기는 카메라·센서·트래킹으로 **누가 어느 방향에 있는지**는 비교적 쉽게 안다.
3. **양이 출력의 필요성**: AR에서는 단순히 깨끗한 mono 신호가 아니라, 착용자가 방향감을 그대로 느낄 수 있는 **양이 신호**로 되돌려줘야 한다. 즉 잡음 제거와 공간감 보존을 동시에 해야 한다.
4. **충실도 vs 지각 품질의 상충**: 신호 충실도(signal fidelity)를 목표로 학습한 모델이 사람이 듣기에 좋은 소리(perceptual quality)를 내지는 않는다는 점이, 논문이 2단계 손실을 도입한 배경으로 보인다(초록의 "first trains for robust denoising and then fine-tunes it to improve perceptual quality"에서 유추).

## 연구 주제
**Binaural Target Speaker Extraction (BiTSE)** — AR 안경 마이크 어레이 입력에서, 목표 화자의 **공간 단서(DoA)**와 **시간 단서(voice activity / timestamp)**를 조건으로 받아 목표 화자만 남긴 양이 신호를 출력하는 문제.

- 입력: AR 안경 어레이로 수음한 다중 화자 + 잡음 신호, 목표 화자의 DoA, 목표 화자의 발화 구간 정보
- 출력: 목표 화자만 남긴 양이(2채널) 신호

## 연구 방법
초록에 명시된 세 가지 구성 요소는 다음과 같다.

### (i) DoA-aware attention with cyclic positional embeddings
목표 화자의 도래 방향을 attention 메커니즘에 조건으로 주입한다. 핵심은 **순환 위치 임베딩(cyclic positional embedding)**이다. 방위각은 $0°$와 $360°$가 같은 방향을 가리키는 **원형(circular) 변수**인데, 일반적인 위치 임베딩은 이 둘을 가장 먼 값으로 취급해버린다. 순환 임베딩은 각도의 이런 주기성을 임베딩 자체에 반영해, 방향이 조금 틀려도 표현이 매끄럽게 이어지도록 만든다.

### (ii) Timestamp-based masking
목표 화자가 **말하고 있지 않은 구간**을 speaker activity 정보로 표시하고, 그 구간의 출력을 억제한다. 방향 단서만으로는 "그 방향에서 지금 소리가 나는가"를 구분하기 어려운데, 시간 단서를 곱해줌으로써 비목표 구간의 잔여 누설(leakage)을 줄이는 장치다. 즉 **공간(어디)과 시간(언제)을 곱해 목표를 좁히는** 설계다.

### (iii) 2단계 손실 최적화 (two-stage loss optimization)
- **1단계**: denoising에 강인해지도록 학습 (신호 충실도 중심 손실로 추정)
- **2단계**: 그 모델을 이어받아 **지각 품질(perceptual quality)** 개선을 목표로 fine-tuning

각 단계에서 정확히 어떤 손실 함수를 썼는지는 초록에 명시되어 있지 않아 적지 않는다.

## 실험 결과 / 연구 의의

### 평가 세팅
- 데이터셋: **SPEAR (SPeech Enhancement for Augmented Reality) challenge dataset**. AR 안경 마이크 어레이 시나리오를 대상으로 하는 공개 벤치마크다.

### 결과 (초록 수준)
논문은 제안한 BiTSE가 기존 접근(conventional approaches) 대비 **신호 충실도(signal fidelity)와 지각 품질(perceptual quality) 양쪽에서 일관되게 개선**된다고 보고한다.

> **주의**: 구체적 지표(SI-SDR, PESQ, STOI 등)의 수치와 비교 대상 baseline 목록, ablation 표는 전문에 있으나 이번에 확보하지 못했다. **수치를 지어내지 않기 위해 비교 표는 싣지 않는다.** 전문 접근이 가능해지면 이 절에 메인 결과 표와 ablation 표를 추가해야 한다.

### 의의
- AR 웨어러블이라는 구체적 폼팩터를 전제로, 기기가 **이미 알고 있는 메타정보**(누가 어느 방향에 있고 언제 말하는지)를 음성 분리의 조건으로 적극 활용한다. 즉 "등록 음성 없이도 되는 TSE"의 실용적 경로를 제시한다.
- 방위각의 원형 구조를 임베딩 설계에 반영한 점은, 공간 오디오 모델에서 각도를 다루는 일반적 레시피로 재사용할 여지가 있다.
- 충실도와 지각 품질을 하나의 손실로 억지로 합치는 대신 **학습 단계를 분리**한 전략은, 두 목표가 상충하는 다른 음성 향상 과제에도 옮겨쓸 수 있다.

## 한계
> 논문이 스스로 밝힌 한계(Conclusion / Limitations 절)를 확인하지 못했다. 아래는 **초록에서 드러나는 구조적 제약**이며, 저자의 주장이 아니라 정리자의 관점임을 밝힌다.

- **DoA와 voice activity를 외부에서 받아야 한다.** 두 단서가 모두 oracle(정답)으로 주어졌는지, 추정값을 썼는지는 확인하지 못했다. oracle이라면 실사용 성능은 DoA 추정기·VAD의 정확도에 좌우된다.
- **화자가 움직이거나 착용자가 고개를 돌리는 상황**에서의 강건성은 초록에 언급이 없다. AR 시나리오에서는 상대 방향이 계속 변하므로 중요한 변수다.
- **같은 방향에 두 화자가 겹치는 경우** DoA 단서가 무력해지는데, timestamp 마스킹이 이를 얼마나 보완하는지 초록만으로는 알 수 없다.
- 평가가 SPEAR 단일 데이터셋에 한정된다. 다른 어레이 형상·실내 환경으로의 일반화는 확인되지 않았다.
- 실시간 처리 가능성(지연, 연산량)은 초록에 언급 없음. AR 착용 기기에서는 결정적인 요소다.

## 우리 연구와 연결되는 점
> 이하는 독자의 관심 주제(Egocentric Vision / Hand-Object Interaction / Spatial Audio) 기준으로 정리자가 연결한 관점이며, 논문이 직접 주장한 내용이 아니다.

### Spatial Audio
- **양이 출력 유지**: 목표 화자만 뽑으면서도 2채널 양이 신호를 유지한다는 설정은, 방향감 보존이 필수인 공간 오디오 연구와 정확히 같은 제약을 공유한다. 같은 주간 정리의 **LuSeeL**(arXiv 2601.19153)이 "텍스트 질의 → 양이 추출 + 위치추정"을 다뤘다면, BiTSE는 반대로 **위치를 조건으로 주고 추출**한다. 두 논문을 나란히 놓으면 *DoA를 출력으로 볼 것인가, 입력으로 볼 것인가*라는 설계 축이 선명해진다.
- **각도의 순환성 처리**: cyclic positional embedding은 방위각 회귀·분류를 다루는 어떤 공간 오디오 모델에도 바로 적용 가능한 아이디어다. LuSeeL이 360개 빈 + 가우시안 소프트 라벨로 순환성을 우회했다면, BiTSE는 임베딩 자체에 주기성을 심는다.

### Egocentric Vision
- **시각으로 DoA를 얻는 자연스러운 결합**: BiTSE가 필요로 하는 두 단서(누가 어느 방향에 있는가, 언제 말하는가)는 egocentric 비전에서 흔히 얻는 정보다. 화자 검출 + 입술 움직임 기반 active speaker detection이 각각 DoA와 voice activity를 대신 공급할 수 있다. 즉 **egocentric video → BiTSE 조건 입력**의 파이프라인이 자연스럽게 그려진다.
- **1인칭 좌표계 공유**: AR 안경 어레이는 카메라와 같은 rig에 붙어 있으므로 시각과 청각이 동일한 head-centric 좌표계를 쓴다. 착용자의 head motion에 따라 두 모달리티가 함께 회전한다는 점은, 멀티모달 정합에서 오히려 강한 사전(prior)이 된다.

### Hand-Object Interaction
- 직접적 연결은 약하다. 굳이 잇는다면, 손 조작 소리(물체 접촉, 도구 사용)를 목표 신호로 바꾸는 확장 — 즉 "화자" 대신 "손-물체 상호작용 이벤트"를 방향+시간 단서로 추출하는 문제로의 일반화 정도다. **논문에 명시적 언급은 없다.**

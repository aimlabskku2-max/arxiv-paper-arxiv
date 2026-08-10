# Spatial Interpolation of Room Impulse Responses based on Deeper Physics-Informed Neural Networks with Residual Connections

**arXiv**: 2512.22915 | **주제 분류**: Spatial Audio | **출판일**: 2025-12 (프리프린트) | **학회**: 프리프린트 (IEICE Transactions on Fundamentals of Electronics, Communications and Computer Sciences 투고)
**저자/소속**: Ken Kurata, Gen Sato, Izumi Tsunokuni, Yusuke Ikeda (도쿄전기대학 / Tokyo Denki University, Japan)
**링크**: https://arxiv.org/abs/2512.22915

## 한 줄 요약
소수의 마이크 측정만으로 3차원 공간 전체의 RIR(공간 임펄스 응답, room impulse response)을 복원하기 위해, SIREN(사인 활성화 함수 기반 신경망)에 잔차 연결(residual connection)을 결합한 깊은 PINN(물리 정보 신경망, physics-informed neural network) 구조를 제안해 깊이를 늘려도 안정적으로 학습되고 반사음 성분까지 정확히 추정함을 보인 연구다.

## 메인 그림
논문의 Fig. 2가 핵심 그림이다. 절대 이미지 URL을 확보하지 못해 텍스트로 서술한다.

Fig. 2는 세 부분으로 구성된다. (a) 기존 PINN의 은닉층 구조로, 완전연결(linear) 층과 활성화 함수를 단순히 쌓은 형태다. (b) 제안하는 은닉층 구조로, ResNet-18 유형의 잔차 블록을 도입해 각 블록에서 입력을 출력에 더한 뒤 $\frac{1}{2}$을 곱해 SIREN이 요구하는 입력 범위 $[-1, 1]$을 유지한다. (c) 전체 네트워크로, 입력은 공간 좌표 $(x, y, z)$와 시간 $t$이며, $N$개의 은닉층을 통과해 각 위치·시각의 RIR $\hat{h}_m$을 출력한다. 이 출력과 측정 RIR $h_m$으로 손실을 계산하고, 파동 방정식 잔차까지 포함한 총 손실 Eq.(3)을 역전파로 최소화한다.

## 선행 연구
공간 상 소수 측정점에서 RIR을 복원하는 문제는 크게 세 갈래로 연구돼 왔다.
- 모델 기반 압축 센싱(compressed sensing): 음장을 평면파나 점음원의 희소(sparse) 조합으로 표현한다. 희소 등가 음원법(sparse equivalent source method), Verburg 등의 희소 평면파 모델, Koyama 등의 직접음(점음원) + 잔향(평면파 + 저계수 행렬) 분리 모델 등이 있다.
- 커널 능형 회귀(KRR, kernel ridge regression) 기반 최소제곱 해법: Ueno 등은 헬름홀츠 방정식을 KRR에 넣어 정확도를 높였고, Ribeiro 등은 직접음/초기 반사음용 커널과 잔향용 커널을 합쳐 사용했다.
- 딥러닝 기반: Lluís 등의 U-Net 초해상(super-resolution) 접근, Fernandez-Grande 등의 GAN 기반 복원이 있으나, 데이터 구동 방식은 대량의 학습 데이터를 필요로 한다.

이 한계를 줄이기 위해 물리 법칙을 손실 함수에 넣는 PINN이 도입됐다. 특히 사인 활성화를 쓰는 SIREN이 RIR 추정에 널리 쓰였고(Pezzoli 등, Olivieri 등의 3D 음장 복원), 저자들도 이전 연구에서 SIREN + 잔차 연결의 얕은(은닉층 4개, 256뉴런) 2D PINN을 제안한 바 있다.

## 문제 제기
기존 PINN 기반 RIR 추정 연구는 대부분 은닉층 수가 적은 얕은 구조로 실험했고, 네트워크 깊이(depth)가 성능에 미치는 영향은 체계적으로 검증된 적이 없다. 층을 단순히 늘리면 표현력은 커지지만, PINN에서는 기울기 소실·폭발로 학습이 불안정해져 오히려 정확도가 떨어질 수 있다. 또한 이 음향 역문제(acoustic-inverse problem)에서 tanh와 sin 중 어느 활성화 함수가 더 적합한지에 대한 직접 비교도 부족하다. 즉 "깊이를 늘리면 RIR 추정이 좋아지는가, 어떤 활성화가 최적인가"가 미해결로 남아 있다.

## 연구 주제
음원과 회절 물체가 없는 3차원 영역 $\Omega (\subset \mathbb{R}^3)$ 내부의 RIR을 소수 측정점에서 복원하는 역문제를 다룬다. 이 영역 안에서 RIR $h(\mathbf{x}, t)$는 동차 파동 방정식(homogeneous wave equation) $\frac{1}{c^2}\frac{\partial^2 h}{\partial t^2} - \nabla^2 h = 0$을 만족한다고 가정한다. 여기에 맞춰, 잔차 연결을 가진 깊은 SIREN 기반 PINN을 설계하고 활성화 함수·깊이·잔차 연결의 효과를 정량 비교하는 것이 주제다.

## 연구 방법
손실 함수는 측정점에서의 데이터 오차항과 파동 방정식 잔차항의 합이다.

$$\mathcal{L} = \mathcal{L}_{err} + \lambda \mathcal{L}_{pde}$$

- $\mathcal{L}_{err}$: 측정 RIR $h_m$과 추정 RIR $\hat{h}_m$의 평균제곱오차(MSE).
- $\mathcal{L}_{pde}$: 추정 영역 내 임의 점에서 파동 방정식 잔차의 크기. 필요한 2차 미분은 자동 미분(automatic differentiation)으로 계산한다.
- $\lambda = 1.0\times10^{-6}$로 데이터 충실도와 물리 일관성의 균형을 맞춘다.

네트워크는 좌표 기반 암묵적 표현(implicit neural representation)으로, 입력 $(t, x, y, z)$를 받아 RIR을 출력하는 MLP다. ReLU·tanh는 반복 미분 시 고차 도함수가 소실되거나 0이 되는 문제가 있어, 고차 도함수 계산에 유리한 SIREN(사인 활성화)을 채택한다.

핵심 제안은 **PINNs-SIREN-Res**로, SIREN에 잔차 연결을 넣은 깊은 구조다. ResNet-18 유형 블록을 쓰되, SIREN의 입력 범위 $[-1,1]$ 제약을 지키기 위해 입력과 출력을 더한 뒤 $\frac{1}{2}$을 곱하는 스케일링을 추가한다($R = N/2$개의 잔차 블록). 기존 SIREN+잔차 연구와는 입력을 주입하는 위치(input-injection point)가 다르다.

실험 설정:
- 방 크기 $6.0 \times 4.0 \times 2.7\,\text{m}^3$, 점음원 $(0, 1.5, 1.35)$, 잔향 시간 $T_{60} = 0.38\,\text{s}$.
- 추정 영역은 방 중앙의 $0.3\times0.3\times0.3\,\text{m}^3$ 정육면체. 마이크 $M=100$개를 반지름 0.15 m 구면에 약 0.05 m 간격으로 등간격 배치.
- 신호 길이 400 샘플, 표본화 주파수 8000 Hz. 측정 신호에 SNR 20 dB의 백색잡음을 더함. RIR은 이미지 소스법(image source method, 7차 반사까지)으로 SFS-toolbox를 사용해 생성.
- 층 수 $N = 6, 10, 14, 18$, 층당 256 뉴런. Adam으로 50,000 iteration, 학습률 $1.0\times10^{-4} \to 1.0\times10^{-6}$ 지수 감쇠. $\omega_0 = 7$.
- 평가: 추정 영역을 $14\times14\times14$ 격자(2744점)로 이산화, 잡음 없는 RIR을 정답으로 NMSE(정규화 평균제곱오차) 계산.
- 비교 대상: PINNs-tanh, PINNs-tanh-Res, PINNs-SIREN, 그리고 제안하는 PINNs-SIREN-Res.

## 실험 결과 / 연구 의의
각 방법의 여러 깊이 중 최저 NMSE 모델을 비교했다(값이 낮을수록 정확).

전체 추정 영역 NMSE (dB, 최적 깊이 모델):

| 방법 | NMSE [dB] |
| --- | --- |
| PINNs-tanh | -2.6 |
| PINNs-tanh-Res | -6.7 |
| PINNs-SIREN | -12.5 |
| PINNs-SIREN-Res (제안) | -14.2 |

- 제안 방법이 PINNs-tanh 대비 약 11.6 dB, PINNs-tanh-Res 대비 7.5 dB, PINNs-SIREN 대비 1.7 dB 우수.
- PINNs-SIREN은 $N=14$에서 $N=18$로 깊어질 때 성능이 약 0.2 dB 하락했으나, 제안 방법은 오히려 0.4 dB 개선돼 깊이를 늘려도 계속 좋아졌다.
- tanh 계열은 잔차 연결이 있어야 깊이의 이점을 얻는다(PINNs-tanh-Res는 $N=6 \to 18$에서 약 3.9 dB 개선). SIREN 계열이 tanh 계열보다 수렴이 빠르고 안정적이다.

보간(interpolation, 마이크 구 내부) 대 보외(extrapolation, 구 외부) NMSE (dB):

| 영역 | PINNs-tanh | PINNs-tanh-Res | PINNs-SIREN | PINNs-SIREN-Res |
| --- | --- | --- | --- | --- |
| 보간 | -2.6 | -6.7 | -13.1 | -15.0 |
| 보외 | -2.5 | -6.7 | -12.1 | -13.7 |

초기/후기 구간 NMSE (dB, 0.025 s 기준 분할):

| 구간 | PINNs-tanh | PINNs-tanh-Res | PINNs-SIREN | PINNs-SIREN-Res |
| --- | --- | --- | --- | --- |
| 초기(직접음 + 초기 반사) | -2.5 | -8.3 | -17.1 | -17.5 |
| 후기(후기 잔향) | -2.8 | -3.5 | -7.3 | -9.6 |

주파수 대역별 NMSE (dB):

| 대역 [Hz] | PINNs-tanh | PINNs-tanh-Res | PINNs-SIREN | PINNs-SIREN-Res |
| --- | --- | --- | --- | --- |
| 0 - 1000 | -7.2 | -13.2 | -21.2 | -23.7 |
| 1000 - 2000 | -1.3 | -5.5 | -12.7 | -14.6 |
| 2000 - 3000 | -1.0 | -4.8 | -10.2 | -12.0 |
| 3000 - 4000 | -0.8 | -3.9 | -8.1 | -9.4 |

의의: 제안 방법은 보간·보외 양쪽, 초기·후기 구간, 모든 주파수 대역에서 가장 정확했다. 특히 잔차 연결이 후기 잔향 성분 추정을 크게 개선했고(SIREN 대비 후기 구간 2.3 dB↑), SIREN이 초기 반사음까지 강한 정확도를 제공했다. SNR 20 dB 잡음에도 추정 신호가 백색잡음 같은 변동을 보이지 않아 잡음 강인성도 확인됐다. 결론적으로 음향 역문제용 "깊고 안정적인 PINN"을 설계하는 실용적 지침(활성화는 sin, 깊이 확장에는 잔차 연결)을 제시한다.

## 한계
- 저·중주파에서는 정확하지만, 파장이 짧아지는 고주파에서는 모든 방법의 정확도가 저하된다. 공간적으로 복잡한 고주파 음장 해상이 여전히 어렵다.
- 후기 잔향 추정 정확도는 초기 구간보다 낮아 개선 여지가 있다.
- 추정 영역이 0.3 m 정육면체로 좁고, 더 넓은 공간 영역으로의 확장은 향후 과제다.
- 이미지 소스법 시뮬레이션으로만 검증했고 실제 측정·실환경 적용은 검증되지 않았다.

## 우리 연구와 연결되는 점
- **Spatial Audio**: 소수 마이크로 3D 공간 전체의 RIR을 복원하는 것은 공간 오디오 렌더링과 음장 재현의 기반이다. 임의 위치의 RIR을 물리 제약으로 얻는 방식은 청취자 이동에 따른 6-DoF 공간 음향 합성이나 몰입형 오디오에 직접 활용할 수 있다.
- **Egocentric Vision / 멀티모달**: 좌표 $(x,y,z,t)$를 입력받아 물리량을 출력하는 좌표 기반 암묵적 표현(SIREN)은 NeRF류 신경 장면 표현과 같은 계열이다. 1인칭 시점 영상의 3D 공간 이해(scene geometry)와 음장(RIR)을 하나의 좌표 기반 표현으로 결합하면, 시청각 공간 정합(audio-visual spatial alignment)이나 시각 정보로 음향을 보강하는 멀티모달 표현 학습으로 확장할 수 있다.
- **Hand-Object Interaction**: 물리 법칙(파동 방정식)을 손실에 넣어 데이터가 적어도 물리적으로 일관된 예측을 얻는 PINN 아이디어는, 접촉·마찰 등 물리 제약이 있는 손-물체 상호작용 모델링에서 소량 데이터로 물리 타당한 궤적·힘을 추정하는 접근에 참고가 된다. 특히 깊이를 늘리면서도 잔차 연결로 학습을 안정화하는 설계 지침은 일반적인 물리 정보 신경망 응용에 폭넓게 적용 가능하다.

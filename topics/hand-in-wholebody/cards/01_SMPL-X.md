## Expressive Body Capture: 3D Hands, Face, and Body from a Single Image
- meta: arXiv 1904.05866 · Pavlakos 외 · 2019 · CVPR
- link: https://arxiv.org/abs/1904.05866
- oneline: 몸통, 손가락 관절, 얼굴 표정까지 하나로 묶은 전신 파라메트릭 인체 모델 SMPL-X와, 이를 단일 RGB 이미지에 맞춰 넣는 최적화 기법 SMPLify-X를 제안한 논문.
- contrib: 몸(SMPL)에 완전 관절형 손(MANO)과 표정 있는 얼굴(FLARE 계열)을 결합한 통합 모델 SMPL-X 정의; OpenPose로 검출한 몸·손·얼굴·발 2D 키포인트에 전신 모델을 한 번에 피팅하는 SMPLify-X; VAE 기반 신경망 포즈 사전확률(VPoser)과 빠르고 정확한 자기침투(interpenetration) 페널티, PyTorch 구현으로 기존 대비 8배 이상 속도 향상.
- integration: 손을 몸과 따로 다루지 않고, 손·얼굴·몸을 하나의 파라메트릭 모델 안에서 동시에 표현할 수 있게 만든 출발점이다. 즉 "전신에 손을 붙이는" 문제를 표현할 공통 언어(SMPL-X 파라미터)를 정의한 셈이며, 이후 FrankMocap, Hand4Whole, PyMAF-X, 그리고 Hand4Whole++(CHAM으로 고정된 전신·손 추정기를 통합)까지 모든 후속 계보가 결국 이 모델의 파라미터를 추정하는 문제로 귀결된다. 다만 본 논문은 이미지별 최적화(fitting) 방식이라 느리고, 이후 회귀 기반·모듈 통합 방식으로 발전하는 계보의 바로 전 단계에 해당한다.

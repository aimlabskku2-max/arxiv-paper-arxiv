## PyMAF-X: Towards Well-aligned Full-body Model Regression from Monocular Images
- meta: arXiv 2207.06400 · Zhang 외 · 2023 · IEEE TPAMI
- link: https://arxiv.org/abs/2207.06400
- oneline: 예측한 메시가 이미지에 잘 맞았는지(mesh-image alignment)를 되먹임(feedback) 받아 파라미터를 반복 보정하는 회귀 루프로, 정합이 잘 맞는 전신(몸·손·얼굴) 파라메트릭 모델을 복원하는 방법.
- contrib: 특징 피라미드에서 정합 근거를 뽑아 예측 파라미터를 명시적으로 교정하는 피라미드형 메시 정합 피드백(PyMAF) 루프 제안; 이를 전신으로 확장한 PyMAF-X로 표현력 있는 전신 모델 복원; 조밀한 대응(dense correspondence) 보조 지도와 공간 정합 어텐션으로 이미지-메시 정합을 강화해 몸·손·얼굴·전신 벤치마크에서 최신 성능 달성.
- integration: 손을 별도 모듈로 뽑든 함께 회귀하든, 전신에서 손·팔이 이미지와 어긋나 보이는 "정합 불량"이 핵심 병목임을 지적하고, 이를 피드백 보정으로 푸는 방향을 제시했다. 즉 계보의 관심을 "손을 어떻게 추정하나"에서 "추정한 손을 몸·이미지에 어떻게 잘 맞추나"로 옮긴 흐름에 속한다. Hand4Whole++가 고정된 전신·손 추정기를 CHAM으로 정합·통합하는 문제의식과 같은 축에 있으며, PyMAF-X는 그 정합 문제를 반복적 피드백 회귀로 다룬 대표 선행이다.

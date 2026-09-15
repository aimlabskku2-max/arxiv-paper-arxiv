## FrankMocap: A Monocular 3D Whole-Body Pose Estimation System via Regression and Integration
- meta: arXiv 2108.06428 · Rong 외 · 2021 · ICCVW (ICCV Workshops, ACVR)
- link: https://arxiv.org/abs/2108.06428
- oneline: 몸, 손, 얼굴을 각각 따로 회귀(regression)로 추정한 뒤 통합(integration) 모듈로 이어 붙여, 야외 단일 이미지에서 전신 3D 포즈를 빠르고 정확하게 뽑아내는 모듈형 시스템.
- contrib: 몸·손·얼굴을 독립적으로 추정하는 모듈식 설계로 각 분야의 최신 성능을 그대로 활용; 분리된 출력을 하나의 전신 포즈로 합치는 3종의 통합 모듈을 제안해 지연시간과 정확도 사이 절충을 제공; 최적화 기반 및 종단간(end-to-end) 방식보다 우수한 전신 포즈 성능을 실용적 속도로 달성.
- integration: 손을 몸과 별개의 전문 모듈로 추정한 다음 손목 등을 맞춰 몸에 이어 붙이는 "분리 추정 후 통합" 전략을 명확히 세운 대표작이다. 손 전용 추정기의 높은 정확도를 희생하지 않고 전신에 얹는다는 발상은 Hand4Whole++가 고정된 전신·손 추정기를 CHAM으로 결합하는 방향과 직접 이어지며, Hand4Whole++는 이 통합 단계를 손으로 짠 규칙 대신 학습된 정합 모듈로 대체·정교화한 후속으로 볼 수 있다.

## AiOS: All-in-One-Stage Expressive Human Pose and Shape Estimation

- meta: arXiv 2403.17934 · Sun 외 · 2024 · CVPR 2024
- link: https://arxiv.org/abs/2403.17934
- oneline: 별도의 사람 검출기 없이 다중 인물의 전신 메시를 DETR 기반 집합 예측(set prediction)으로 한 번에 복원하는 진정한 단일 단계(all-in-one-stage) 프레임워크.
- contrib: 외부 검출 모델 없이 다중 인물 전신 메시 복원을 점진적 집합 예측 문제로 정식화한 DETR 기반 구조 제안; 사람 위치 지역화 → 몸통 특징 추출 → 손·얼굴을 포함한 전신 정밀화로 이어지는 순차적 검출 단계 설계; 크롭에 따른 문맥 손실과 인물·부위 간 연관성 부족 문제를 완화해 혼잡 장면에서 강건성 확보.
- integration: 손을 따로 검출·크롭하지 않고, 인물 쿼리에서 몸통을 잡은 뒤 같은 파이프라인 안에서 손·얼굴 토큰을 순차적으로 정밀화하므로 전신 문맥이 손 추정에 그대로 흘러든다. 손 통합 계보에서 OSX의 단일 네트워크 아이디어를 다중 인물·검출기 없는(detector-free) 방향으로 밀어붙인 위치다. Hand4Whole++는 이런 end-to-end 재학습형 단일 단계 모델과 달리, 고정된 전신·손 추정기를 CHAM 어댑터로 이어 붙여 재학습 비용을 줄이는 대안적 통합 경로를 택한다.

## Accurate 3D Hand Pose Estimation for Whole-Body 3D Human Mesh Estimation
- meta: arXiv 2011.11534 · Moon 외 · 2022 · CVPRW (CVPR Workshops)
- link: https://arxiv.org/abs/2011.11534
- oneline: 전신 3D 메시 복원에서 유독 부정확했던 손을, 인체 운동 사슬(kinematic chain)과 관절별 특징을 제대로 활용해 크게 개선한 종단간(end-to-end) 방법 Hand4Whole.
- contrib: 관절 특징으로 3D 관절 회전을 예측하는 Pose2Pose 모듈 설계; 손목 회전에 크게 기여하는 손 MCP(손가락 밑마디) 관절 특징을 써서 3D 손목을 예측; 손가락 회전 예측 시 정보가 거의 없는 몸통 특징을 버리고 손 특징만 사용해, 기존 전신 메시 방법보다 훨씬 나은 3D 손 결과를 종단간 학습으로 달성.
- integration: FrankMocap이 몸·손을 완전히 분리했다면, Hand4Whole은 하나의 네트워크 안에서 손목을 몸이 아닌 손 쪽 특징으로 잡아 운동 사슬의 연결부(손목)를 정교하게 다룬 전환점이다. 손 정확도가 전신 품질을 좌우한다는 문제의식을 세웠고, 이 논문이 곧 Hand4Whole++(arXiv 2603.14726)의 직접적 뿌리다. 후속인 ++는 여기서 나아가 이미 잘 학습된 전신·손 추정기를 고정한 채 CHAM으로 통합해, 재학습 없이 손을 몸에 정합시키는 방향으로 계보를 잇는다.

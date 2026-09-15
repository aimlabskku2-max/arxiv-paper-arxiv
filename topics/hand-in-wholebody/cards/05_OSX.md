## One-Stage 3D Whole-Body Mesh Recovery with Component Aware Transformer

- meta: arXiv 2303.16160 · Lin 외 · 2023 · CVPR 2023
- link: https://arxiv.org/abs/2303.16160
- oneline: 몸통·손·얼굴을 별도 추정기 없이 하나의 컴포넌트 인지 트랜스포머(Component Aware Transformer, CAT)로 한 번에 복원하는 단일 단계(one-stage) 전신 메시 복원 기법.
- contrib: 전역 몸통 인코더가 몸통 파라미터와 고해상도 특징맵을 산출하고, 국소 얼굴·손 디코더가 이를 받아 부위별 메시를 복원하는 단일 네트워크 구조 제안; 특징 수준의 업샘플-크롭(upsample-crop) 방식으로 작게 잡히는 손·얼굴 영역의 고해상도 부위 특징을 추출; 키포인트 유도 변형 가능 어텐션(keypoint-guided deformable attention)으로 손·얼굴을 정밀 추정하고, 대규모 UBody 벤치마크를 함께 공개.
- integration: 손을 몸통과 분리된 크롭 이미지로 다시 처리하는 기존 다단계 방식과 달리, 몸통 인코더가 만든 공유 특징맵에서 손 영역을 특징 수준으로 잘라내 디코더가 정밀화하므로 전신과 손이 하나의 네트워크 안에서 함께 학습된다. 손 통합 계보에서 "분리 추정 후 병합"에서 "단일 단계 공동 추정"으로 넘어가는 전환점에 해당한다. Hand4Whole++는 반대로 이미 잘 학습된 전신·손 추정기를 고정한 채 CHAM 어댑터로 이어 붙이는 방향이라, 처음부터 하나로 합쳐 학습하는 OSX와는 통합 철학이 대비된다.

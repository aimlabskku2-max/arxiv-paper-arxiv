## WiLoR: End-to-end 3D Hand Localization and Reconstruction in-the-wild
- meta: arXiv 2409.12259 · Potamias 외 · 2024(arXiv) · CVPR 2025
- link: https://arxiv.org/abs/2409.12259
- oneline: 실시간 손 검출(localization)과 고정밀 트랜스포머 기반 3D 손 복원을 하나로 묶어, in-the-wild 다중 손 장면에서 MANO(손 파라메트릭 모델) 메시를 끝단간(end-to-end)으로 추정하는 파이프라인.
- contrib: 실시간 완전 합성곱(fully-convolutional) 손 검출기와 고충실도 트랜스포머 복원기를 결합한 단일 end-to-end 구조로 검출-복원 단절을 해소; 다양한 조명·가림 조건의 200만 장 이상 in-the-wild 손 이미지 대규모 데이터셋 공개; 시간(temporal) 모듈 없이도 단안 영상에서 부드러운 3D 손 추적을 달성하며 2D·3D 벤치마크에서 효율·정확도 모두 개선.
- integration: WiLoR는 검출부터 복원까지 손만을 대상으로 최적화돼 다중 손·in-the-wild 환경에서 빠르고 정밀한 손 메시를 내지만, 손 크롭 단위로 동작하므로 전신 맥락(global body context) — 팔·몸통과의 연결이나 몸 기준 손목의 전역 회전 — 은 알지 못한다. Hand4Whole++는 이런 손 전용 모델을 고정(frozen)한 채 그 특징을 전신 스트림에 주입하는 방식으로, 손 복원의 정밀도를 그대로 활용하면서 전신과 정합된 손목 방향까지 함께 맞춘다.

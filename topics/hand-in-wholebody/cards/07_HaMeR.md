## Reconstructing Hands in 3D with Transformers (HaMeR)
- meta: arXiv 2312.05251 · Pavlakos 외 · 2023(arXiv) · CVPR 2024
- link: https://arxiv.org/abs/2312.05251
- oneline: 대규모 데이터와 대용량 비전 트랜스포머(ViT, Vision Transformer)를 앞세워 단안(monocular) 영상에서 MANO(손 파라메트릭 모델) 기반 3D 손 메시를 강건하게 복원하는 완전 트랜스포머 파이프라인.
- contrib: 다수의 2D·3D 손 주석 데이터셋을 통합한 대규모 학습셋으로 정확도와 강건성을 크게 끌어올림; ConvNet 대신 대용량 ViT 백본을 채택해 데이터·모델 용량을 함께 스케일업; 어려운 자세·가림·조명을 포함한 in-the-wild 평가용 HInt 벤치마크를 함께 제안.
- integration: HaMeR는 크롭된 손 이미지에 집중해 손가락 관절과 손 메시를 매우 정밀하게 맞추지만, 입력이 손 주변 크롭이라 전신 맥락(global body context) — 팔·어깨와의 운동학적 연결이나 몸통 대비 손목의 전역 방향 — 정보는 갖지 못한다. Hand4Whole++는 이런 손 전용 모델을 고정(frozen)한 채 그 특징을 전신 스트림에 주입해, 손 자체의 정밀도는 살리면서 몸과 어긋나기 쉬운 손목 방향까지 전신 기준으로 정합시킨다.

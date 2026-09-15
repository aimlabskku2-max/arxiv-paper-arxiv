## SMPLer-X: Scaling Up Expressive Human Pose and Shape Estimation

- meta: arXiv 2309.17448 · Cai 외 · 2023 · NeurIPS 2023 (Datasets and Benchmarks)
- link: https://arxiv.org/abs/2309.17448
- oneline: 몸통·손·얼굴을 함께 추정하는 표현적 인체 포즈·형상 추정(expressive human pose and shape estimation, EHPS)을 대규모 데이터와 대형 모델로 확장한 최초의 제너럴리스트(generalist) 파운데이션 모델.
- contrib: ViT-Huge 백본과 최대 450만 개 인스턴스, 다양한 데이터 소스를 결합해 별도 미세조정 없이도 여러 벤치마크에서 일반화되는 EHPS 파운데이션 모델 구축; 데이터셋·백본 스케일링이 성능·전이성에 미치는 영향을 체계적으로 분석; AGORA·UBody·EgoBody·EHF 등 7개 벤치마크에서 최고 수준 결과(EHF 62.3mm PVE 등, 미세조정 없이) 달성.
- integration: 손을 위한 특별한 모듈을 두기보다, 트랜스포머 백본을 크게 키우고 대규모 다중 데이터로 학습해 전신 SMPL-X 파라미터(손 포즈 포함)를 통째로 회귀한다. 즉 손 통합을 아키텍처가 아니라 데이터·스케일로 끌어올린 계보다. Hand4Whole++는 바로 이 SMPLer-X를 고정된 전신 백본으로 채택하고, 그 위에 CHAM 어댑터를 붙여 손 부분만 보강하는 방식이라, SMPLer-X는 Hand4Whole++가 딛고 서는 토대 역할을 한다.

## HMR-Adapter: A Lightweight Adapter with Dual-Path Cross Augmentation for Expressive Human Mesh Recovery

- meta: arXiv 없음(미확인) · Author 외 · 2024 · ACM MM 2024
- link: (arXiv 판본을 확인하지 못해 링크 생략; ACM DL: 10.1145/3664647.3681641)
- oneline: 이미 학습된 대형 전신 메시 복원(human mesh recovery, HMR) 모델에 약 27M 파라미터짜리 경량 어댑터(adapter)를 덧붙여, 몸통과 손이 서로의 정보를 주고받는 양방향 교차 증강(dual-path cross augmentation)으로 표현적 HMR 성능을 끌어올리는 기법.
- contrib: 대형 HMR 모델 전체를 재학습하지 않고 약 27M 파라미터 어댑터만 미세조정해 목표 데이터셋에서 성능을 높이는 파라미터 효율적(parameter-efficient) 적응 방식 제안; 한 경로는 손 특징을 주입해 몸통 포즈를 정밀화하고 다른 경로는 몸통 가이드를 주입해 손 포즈를 개선하는 이중 경로 교차 증강 설계; 기존 대형 백본을 그대로 활용하면서 손·몸통 상호 보강으로 표현적 HMR을 향상.
- integration: 손을 별도 네트워크로 재추정하는 대신, 고정된 대형 전신 모델의 특징 위에 경량 어댑터를 얹어 몸통↔손 특징을 교차 주입한다는 점에서 CHAM과 가장 직접적으로 겹치는 경쟁 기법이다. 두 방법 모두 "고정된 백본 + 경량 어댑터로 손을 통합"한다는 계보에 속한다. 차이는 결합 방식에 있다: HMR-Adapter는 하나의 대형 HMR 모델 내부에 어댑터를 삽입해 몸통과 손을 양방향으로 상호 보강하는 반면, Hand4Whole++의 CHAM은 SMPLer-X 같은 전신 백본과 별도의 전용 손 추정기라는 두 개의 고정 모델을 어댑터로 이어 붙여 통합한다. 즉 HMR-Adapter가 단일 모델 내부의 교차 증강이라면, CHAM은 분리된 전신·손 전문가를 사후에 결합하는 브리지에 가깝다.

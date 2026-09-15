## Enhancing Hands in 3D Whole-Body Pose Estimation with Conditional Hands Modulator (Hand4Whole++)
- meta: arXiv 2603.14726 · Moon (Gyeongsik Moon) · 2026 · CVPR
- link: https://arxiv.org/abs/2603.14726
- oneline: 잘 학습된 전신(whole-body) 추정기와 손 전용 추정기를 둘 다 고정(frozen)한 채, 경량 어댑터 CHAM으로 손 특징을 전신 특징 스트림에 주입해 재학습 없이 손과 손목을 몸에 정합시키는 모듈형 프레임워크.
- contrib: 전신 추정기와 손 추정기 사이의 "지도(supervision) 격차" — 전신 데이터엔 손 다양성이 부족하고 손 데이터엔 몸 맥락이 없다 — 를 문제로 정식화; 고정된 전신 특징을 손 전용 특징으로 변조(modulate)해 손목 방향을 상체 운동학과 일치시키는 경량 모듈 CHAM 제안(학습 시 두 추정기는 얼리고 CHAM만 최적화); MANO 손 메시를 미분 가능한 강체 정합(differentiable rigid alignment)으로 전신 메시의 손목에 붙여 손가락 관절·손 형상까지 직접 이식.
- integration: 이 서베이의 도착점이자, 손 통합 계보의 최신 종합이다. FrankMocap의 "분리 추정 후 통합", Hand4Whole의 "손목을 손 특징으로", PyMAF-X의 "정합 보정", SMPLer-X의 "스케일업 전신 백본", HaMeR·WiLoR의 "강력한 손 전문가", HMR-Adapter의 "경량 어댑터 통합"을 하나로 엮되, 재학습 없이 두 고정 전문가를 사후 결합하는 브리지(CHAM)로 손목 방향의 전신 정합까지 해결한다. 우리 연구실 관심(Hand-Object Interaction, Egocentric Vision) 관점에서는, 1인칭 영상에서 손이 물체·몸과 함께 등장할 때 전신 맥락과 손 정밀도를 동시에 확보하는 실용적 설계로 바로 응용될 수 있다.

# arxiv-paper-arxiv — 저장소 구조 가이드

git 저장소 루트(예: `~/Research_Arxiv`) = GitHub Pages 루트
원격: `aimlabskku2-max/arxiv-paper-arxiv` · 사이트: `https://aimlabskku2-max.github.io/arxiv-paper-arxiv/`

## 이상적인 폴더 구조

```
arxiv-paper-arxiv/                     # = repo root (원하는 폴더 어디든; Dropbox 밖 권장)
├── index.html                         # ★ 통합 랜딩: 서베이 + 주간 디제스트 (자동 생성)
├── papers.html                        # ★ 전체 논문 관리 리스트: 검색·주제필터·정렬 (자동 생성)
├── build_site.py                      # index.html 생성기 (topics.json + weekly/ 스캔)
├── build_papers.py                    # papers.html 생성기 (weekly/*/paper_summary/*.md 스캔)
├── README.md                          # 저장소 개요
├── assets/
│   └── style.css                      # (선택) 공통 스타일
│
├── topics/                            # 큐레이션 토픽 서베이 (수동/반자동)
│   ├── topics.json                    # ★ 서베이 목록 매니페스트 (index 생성이 이걸 읽음)
│   ├── video-to-audio/
│   │   ├── video-to-audio_survey.html
│   │   └── papers/                    # 이 토픽에서 아카이빙한 논문(pdf 또는 .txt 링크)
│   ├── greatest-hits-foley/
│   │   └── greatest-hits-foley_survey.html
│   ├── egocentric-spatial-avqa/
│   │   └── egocentric-spatial-avqa_survey.html
│   └── tactile-representation/
│       └── tactile-representation_survey.html
│
└── weekly/                            # 주간 arXiv 디제스트 (스킬이 자동 생성)
    ├── 2026-07-18/
    │   ├── 2026-07-18_paper_summary.html
    │   ├── original_paper/            # 원본 PDF 또는 링크(.txt)
    │   └── paper_summary/             # 논문별 한국어 디제스트 .md
    ├── 2026-06-29/
    ├── 2026-06-22/
    └── 2026-06-16/
```

## 설계 원칙

1. **두 종류를 폴더로 분리**
   - `topics/` = 내가 직접 큐레이션하는 "분야별 핵심 논문 계보 서베이" (V2A, Foley 등). 자주 안 바뀜.
   - `weekly/` = 스킬이 매주 자동으로 쌓는 최신 논문 디제스트. 날짜 폴더로 누적.

2. **루트 `index.html`은 자동 생성 (비파괴)**
   - 서베이 정보는 `topics/topics.json` 매니페스트에서 읽고,
   - 주간 디제스트는 `weekly/` 하위 날짜 폴더를 스캔해서,
   - 두 섹션을 합쳐 루트 `index.html`을 다시 그린다.
   - → 매주 자동 갱신해도 **서베이 섹션이 절대 지워지지 않음** (지금 스킬의 문제 해결).
   - 메인 페이지 상단의 "📄 전체 논문 리스트" 버튼 → `papers.html`.

3. **`papers.html` = 전체 논문 관리 리스트 (자동 생성)**
   - `python3 build_papers.py`가 `weekly/*/paper_summary/*.md`를 전부 스캔해,
     모든 주차의 논문을 제목·주제·출판일·학회·arXiv/리포트 링크가 있는 표로 만든다.
   - 브라우저에서 **검색(제목·저자·arXiv·학회)**, **주제 필터 칩**, **열 클릭 정렬**이 된다(서버 불필요, 순수 HTML/JS).
   - 매주 디제스트가 쌓이면 자동으로 목록이 늘어난다.

## 매주 사이트 갱신 (2줄)

```bash
python3 build_site.py .     # 메인 랜딩(index.html) 갱신
python3 build_papers.py .   # 전체 논문 리스트(papers.html) 갱신
```

3. **경로 규칙**
   - 서베이 파일: `topics/<slug>/<slug>_survey.html`
   - 주간 리포트: `weekly/<YYYY-MM-DD>/<YYYY-MM-DD>_paper_summary.html`
   - slug은 소문자-하이픈 (예: `video-to-audio`).

## topics.json 예시 (서베이를 여기 등록하면 랜딩에 자동 노출)

```json
[
  {
    "slug": "video-to-audio",
    "title": "Video-to-Audio Generation — Core Lineage",
    "desc": "Diff-Foley 계보를 중심으로 한 V2A 핵심 논문 계보",
    "count": null,
    "path": "topics/video-to-audio/video-to-audio_survey.html"
  },
  {
    "slug": "greatest-hits-foley",
    "title": "Greatest Hits / Impact-Sound Foley",
    "desc": "임팩트 사운드 Foley 동기화 연구 계보",
    "count": null,
    "path": "topics/greatest-hits-foley/greatest-hits-foley_survey.html"
  },
  {
    "slug": "egocentric-spatial-avqa",
    "title": "Egocentric Spatial Audio-Visual VQA",
    "desc": "1인칭 공간 오디오-비주얼 QA 서베이",
    "count": 15,
    "path": "topics/egocentric-spatial-avqa/egocentric-spatial-avqa_survey.html"
  },
  {
    "slug": "tactile-representation",
    "title": "Tactile Representation Learning — Genealogy",
    "desc": "촉각 표현 학습 계보",
    "count": 19,
    "path": "topics/tactile-representation/tactile-representation_survey.html"
  }
]
```

## 스킬 연동 (weekly 자동화)

- 스킬(weekly-arxiv-paper-digest)이 BASE=저장소 루트를 받아 매주:
  1. 논문 6편 디제스트를 `weekly/{날짜}/`에 생성,
  2. `build_html.py`로 그 주 리포트, `build_site.py`로 `index.html`, `build_papers.py`로 `papers.html` 갱신,
  3. `git add -A && git commit && git push` → GitHub Pages 자동 반영.
- 세 스크립트는 스킬 안(`scripts/`)에 포함돼 있어 저장소에 따로 두지 않아도 된다(원하면 루트에 복사해 수동 실행도 가능).

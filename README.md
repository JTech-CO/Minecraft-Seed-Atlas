# Minecraft Java Seed Atlas

Minecraft Java Edition 26.2, 26.1, 1.21 계열의 독특한 바이옴·지형 시드 251개를 검색하고 복사할 수 있는 빌드 과정 없는 정적 웹사이트입니다.

## 기능

- 시드 설명·숫자 통합 검색
- Java 26.2 / 26.1 / 1.21 버전 필터
- 마을, 섬, 동굴, 산악, 구조물, 벚나무숲, 유황, 해양 등 지형 분류
- 시드 블록 클릭 또는 키보드 조작으로 클립보드 복사
- 원문 순서·설명·시드 숫자 정렬
- 현재 필터 내 무작위 시드 탐색
- 검색·필터 상태 URL 저장
- 모바일·태블릿·데스크톱 반응형 UI
- 외부 라이브러리, 프레임워크, 빌드 도구 불필요

## UI 수정 사항

- 검색·버전·지형 분류·정렬 컨트롤의 상단 기준선을 통일했습니다.
- Windows/Chrome 네이티브 선택 목록의 대비 문제를 피하도록 키보드 조작 가능한 커스텀 선택 목록을 적용했습니다.
- 히어로 제목의 행간과 그림자를 조정해 두 줄 제목이 겹치지 않도록 했습니다.
- 추상적인 삼각형 배경을 블록형 지형과 픽셀 나무 실루엣으로 교체했습니다.

## 폴더 구조

```text
minecraft-java-seed-atlas/
├─ index.html
├─ css/
│  └─ styles.css
├─ js/
│  ├─ seeds.js
│  └─ app.js
├─ assets/
│  ├─ favicon.svg
│  └─ hero-forest.svg
├─ data/
│  └─ minecraft_java_unique_biome_terrain_seeds_251.md
├─ tools/
│  └─ build_seed_data.py
├─ .nojekyll
└─ README.md
```

GitHub Pages는 저장소 루트에서 `index.html`을 찾아야 하므로 HTML은 루트에 두고, CSS와 JavaScript는 각각 별도 폴더로 분리했습니다.

## 로컬 실행

단순히 `index.html`을 열어도 주요 기능이 작동합니다. 로컬 서버에서 확인하려면 저장소 루트에서 다음 명령을 실행합니다.

```bash
python -m http.server 8080
```

그다음 브라우저에서 `http://localhost:8080`을 엽니다.

## GitHub Pages 배포

1. 새 GitHub 저장소를 만들고 이 폴더의 내용 전체를 저장소 루트에 업로드합니다.
2. 저장소의 `Settings` → `Pages`로 이동합니다.
3. `Build and deployment`의 Source를 `Deploy from a branch`로 선택합니다.
4. Branch는 `main`, 폴더는 `/(root)`로 설정하고 저장합니다.
5. 배포가 끝나면 `https://<계정명>.github.io/<저장소명>/`으로 접속합니다.

모든 내부 경로가 상대 경로이므로 사용자·조직 페이지와 프로젝트 페이지 양쪽에서 작동합니다.

## 시드 데이터 갱신

`data/minecraft_java_unique_biome_terrain_seeds_251.md`의 시드 표를 수정한 뒤 다음 명령을 실행합니다.

```bash
python tools/build_seed_data.py
```

스크립트는 버전별 개수, 전체 251개 여부, 중복 시드를 검사한 후 `js/seeds.js`를 다시 생성합니다. Java의 signed 64-bit 범위를 손실 없이 다루기 위해 모든 시드 값은 JavaScript 숫자가 아닌 문자열로 저장합니다.

## 데이터 기준

- Minecraft Java Edition 전용
- 버전: 26.2, 26.1, 1.21 계열
- 기본 월드 유형, 구조물 생성 활성화
- 지형 변경 데이터팩·모드 미사용
- 데이터 확인일: 2026-08-06

Minecraft는 Mojang Studios 및 Microsoft의 상표입니다. 이 프로젝트는 비공식 팬 프로젝트이며 Mojang 또는 Microsoft와 제휴하거나 보증받지 않았습니다.

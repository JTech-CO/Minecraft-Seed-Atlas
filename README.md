# Minecraft Java Seed Atlas

Minecraft Java Edition **26.3, 26.2, 26.1, 1.21 계열에 각 100개씩, 총 400개**의 독특한 바이옴·지형 시드를 검색하고 복사하는 정적 웹사이트입니다. 외부 라이브러리와 런타임 서버가 필요하지 않습니다.

## 2026-10-04 갱신

- 고유 시드 164개 추가: 26.3 100개, 26.2 16개, 26.1 48개.
- 기존 251개 가운데 출처 숫자·Java 버전·핵심 특징 근거가 부족하거나 부호가 충돌한 13개와 유사한 평탄 생존 섬 2개를 제외해 400개로 편성했습니다. 제외 사유는 `data/retired_seeds.json`에 기록했습니다.
- 출처에서 1.21.11까지만 지원한다고 명시한 기존 26.1 시드 2개를 1.21 계열로 정정했습니다.
- 26.3의 Dappled Forest(포플러 숲)·폐허 캠프, 버섯 들판 분류를 추가했습니다.
- 카드마다 개별 출처, 원문 버전, 원문 좌표, 확인 방식과 자료 확인일을 표시합니다.
- 26.3 공식 출시일은 2026-09-15입니다. 26.4 Snapshot 1은 이미 2026-09-22 공개됐으며 26.4 시드 호환은 이 목록에서 검증하지 않습니다.

| 버전 | 고유 시드 |
|---|---:|
| Java 26.3 | 100 |
| Java 26.2 | 100 |
| Java 26.1 | 100 |
| Java 1.21 계열 | 100 |
| 합계 | 400 |

## 확인 기준

**26.3 100개**는 MC Seed View 10개와 SeedLookout의 개별 시드 페이지 90개에서 정식 Java 26.3 게임 확인을 보고한 자료입니다. 출처가 공개한 확인 기록과 특징·숫자·좌표를 대조했습니다. 이 프로젝트에서 Minecraft를 실행해 모든 월드를 독립적으로 재검증한 것은 아닙니다.

현행 400개 모두 개별 출처가 있으며, Java 근거가 부족한 기존 항목은 제외했습니다. 출처의 버전 명시와 지도 계산 자료는 게임 확인 기록과 구분합니다.

현재 확인 방식별 집계는 출처의 게임 확인 기록 110개, 원문의 Java 버전 명시 282개, 지도 계산 자료 8개입니다. 미확인 기존 항목과 스냅샷 전용 항목은 현행 목록에 없습니다.

카드와 출처 필터에서 다음 상태를 구분합니다.

- **출처에서 게임 확인**: 원문 작성자가 해당 정식 버전에서 게임 확인했다고 명시.
- **출처에 버전 명시**: 정확한 숫자와 특징, Java 호환 버전을 원문에서 확인. 별도 게임 검증 기록은 보장하지 않음.
- **지도 계산 자료**: 원문이 시드 지도 계산에 근거. 실제 스폰과 생성 결과는 다를 수 있음.
- **스냅샷 자료**: 시험 버전만 확인한 경우에 사용할 상태. 이번 26.3 100개에는 포함하지 않았음.
- **기존 목록 · 개별 재확인 전**: 기존 시드의 숫자는 찾았지만 Java 에디션·버전·특징의 근거가 충분하지 않아 확인이 필요한 항목.

모든 숫자는 버전 간 중복 없이 한 번만 집계하며, 다른 버전에서 똑같이 생성된다는 의미가 아닙니다. 1.21 계열은 1.21.x 자료를 묶으므로 기본 1.21.0에서 모든 바이옴을 재현할 수 있다는 뜻이 아닙니다. 좌표는 원문의 관심 지점이며 스폰이 명시되지 않았다면 스폰 좌표로 해석하지 마세요. 시드 부호가 출처 간 충돌한 항목은 현행 목록에서 제외했습니다.

주요 출처: [MC Seed View 26.3](https://mcseedview.com/blog/best-minecraft-seeds-26-3), [SeedLookout](https://seedlookout.com/seeds/), [akirby80](https://akirby80.net/blog/top-100-minecraft-survival-island-seeds/), [Godlike](https://godlike.host/minecraft-seeds/), [WiseHosting](https://wisehosting.com/minecraft-seeds). 항목별 링크는 생성된 `data/minecraft_java_unique_biome_terrain_seeds.md`를 확인하세요.

## 기능

- 설명·시드 숫자·출처 이름·원문 버전·좌표 통합 검색
- 버전·지형·출처 확인 방식 필터
- 시드 버튼 클릭과 키보드 조작으로 복사
- 문서 순서·설명 가나다순·정확한 64비트 정수 정렬
- 현재 조건 내 무작위 시드 탐색
- 검색·필터·정렬 상태 URL 저장 및 새로고침 복원
- 모바일·태블릿·데스크톱 화면 지원
- 내용이 바뀌면 자산 URL의 해시를 갱신해 오래된 브라우저 캐시를 방지

## 로컬 실행

`index.html`을 직접 열거나 저장소 루트에서 실행합니다.

```bash
python -m http.server 8080 --bind 127.0.0.1
```

브라우저에서 [로컬 사이트](http://127.0.0.1:8080)를 엽니다. 직접 파일을 열 때 URL 상태 저장이나 자동 복사는 브라우저 정책에 따라 제한될 수 있습니다.

## 폴더와 데이터 갱신

```text
index.html                         정적 페이지
css/styles.css                     반응형 스타일
js/app.js                          검색·필터·복사
js/seeds.js                        생성된 브라우저 데이터
assets/                            SVG 아이콘과 지형 배경
data/minecraft_java_seeds.json      현행 원본 데이터
data/minecraft_java_unique_biome_terrain_seeds.md
                                   생성된 시드·출처 표
data/minecraft_java_unique_biome_terrain_seeds_251.md
                                   이전 251개 목록 보관
data/research-*.json                이번 갱신의 조사 기록
data/retired_seeds.json             제외 항목과 이유
tools/build_seed_data.py            검증·JS/MD/HTML 생성
tools/import_seed_research.py       2026-10 이관 재현용
tools/test_seed_data.py             데이터·생성기 회귀 검사
```

일반 갱신은 `data/minecraft_java_seeds.json`을 수정한 뒤 다음 명령을 실행합니다. 앱이나 CSS를 바꾼 뒤에도 생성기를 실행해 자산 해시를 갱신합니다.

```bash
python tools/build_seed_data.py
python tools/build_seed_data.py --check
python -m unittest discover -s tools -p "test_*.py" -v
```

생성기는 고정 총개수 대신 실제 데이터를 집계합니다. 중복, Java signed 64-bit 범위, 정수 문자열 형식, 버전·검증 상태, 출처 필수값과 HTTPS URL을 검사하고 JS·MD·HTML 통계 및 자산 해시를 갱신합니다. 숫자는 JavaScript `Number`로 변환하지 않습니다.

`tools/import_seed_research.py`는 이번 조사 파일과 이전 MD에서 **2026-10 편성을 재현**하는 도구입니다. 일반 편집 후 실행하면 현행 JSON을 이번 조사 상태로 덮어쓰므로 일상적인 갱신에는 사용하지 않습니다. 400개·각 100개 검사는 이번 편성의 회귀 기준이며 이후 편성을 바꾸면 해당 검사도 함께 갱신하세요.

## GitHub Pages

저장소의 `Settings → Pages`에서 `Deploy from a branch`를 선택하고 `main / (root)`를 지정합니다. HTML은 루트에 있으며 모든 내부 자산 경로는 상대 경로입니다. 저장소 루트의 `.nojekyll`을 유지합니다.

## 월드 설정

Java Edition의 원문 버전, 기본 월드 유형, 구조물 생성 활성화, 지형 변경 모드·데이터팩 미사용 기준입니다. 기존 월드에서 이미 생성한 청크는 상위 버전으로 열어도 다시 생성되지 않습니다.

Minecraft는 Mojang Studios 및 Microsoft의 상표입니다. 본 사이트는 비공식 팬 프로젝트이며 Mojang 또는 Microsoft와 제휴하거나 보증받지 않았습니다.

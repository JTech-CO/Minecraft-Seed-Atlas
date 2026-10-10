# Minecraft 이미지 출처

## 메인 배경 스크린샷

- 파일: `hero-landscape.jpg`
- 원본: <https://i.imgur.com/dN7XRiU.jpeg>
- 사용자가 사이트 배경용으로 지정한 Minecraft 스크린샷이며 원본 바이트를 그대로 저장했다.
- JPEG, 1920 × 1057. 촬영자·게임 버전·셰이더 정보는 제공되지 않았다.

## 블록 텍스처

Minecraft Java Edition **26.3**의 기본 게임 자산이다. Mojang Studios / Microsoft의 게임 자산을 추출한 [InventivetalentDev/minecraft-assets](https://github.com/InventivetalentDev/minecraft-assets) 미러의 `26.3` 브랜치에서 PNG 원본을 그대로 저장했다. 미러 README는 자산이 Minecraft JAR에서 추출되었음을 명시한다. 다운로드 확인일: 2026-10-10.

- [`dirt.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/dirt.png)
- [`grass_block_side.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/grass_block_side.png)
- [`grass_block_top.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/grass_block_top.png)
- [`grass_block_side_overlay.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/grass_block_side_overlay.png)
- [`stone.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/stone.png)
- [`deepslate.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/deepslate.png)
- [`deepslate_iron_ore.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/deepslate_iron_ore.png)
- [`deepslate_gold_ore.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/deepslate_gold_ore.png)
- [`deepslate_redstone_ore.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/deepslate_redstone_ore.png)
- [`deepslate_diamond_ore.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/deepslate_diamond_ore.png)
- [`deepslate_lapis_ore.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/deepslate_lapis_ore.png)
- [`bedrock.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/bedrock.png)
- [`netherrack.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/netherrack.png)
- [`soul_sand.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/soul_sand.png)
- [`nether_quartz_ore.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/nether_quartz_ore.png)
- [`lava_still.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/lava_still.png)
- [`end_stone.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/end_stone.png)
- [`obsidian.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/obsidian.png)
- [`purpur_block.png`](https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/26.3/assets/minecraft/textures/block/purpur_block.png)

블록 PNG는 16 × 16이다. `lava_still.png`는 16 × 320의 원본 애니메이션 스트립이다. 잔디의 상단·측면 오버레이는 게임에서 바이옴 색상을 입히는 회색 텍스처이므로 사이트에서도 색조 처리를 적용할 수 있다.

## 사이트용 SVG 지형 배치

`terrain-surface.svg`, `terrain-caves.svg`, `terrain-bedrock.svg`, `terrain-nether.svg`, `terrain-lava.svg`, `terrain-end.svg`와 `grass-border.svg`는 위 게임 PNG를 블록 단면 형태로 배치한 자체 SVG이다. 원본 PNG의 각 픽셀 색상과 투명도를 동일 색상별 SVG path로 옮겨 외부 파일이나 서버에 의존하지 않는다. 게임 스크린샷이나 게임이 생성한 실제 지형 지도로 소개하지 않는다.

- 기본 지형 타일맵: 768 × 1024, 블록 한 칸 64 × 64. 원본 16 × 16 PNG의 한 픽셀을 4 × 4 SVG 사각형으로 표현하고 픽셀 경계를 유지한다.
- 잔디 테두리: 768 × 64, 측면 원본과 초록색으로 색조 처리한 측면 오버레이를 합성한다.
- 동굴·네더의 공동, 광석맥, 엔드의 떠 있는 섬·기둥은 SVG의 블록 격자로 구성한 장식 배치이다.
- 용암은 16 × 320 원본 스트립의 첫 16 × 16 프레임만 벡터 패턴에 사용한다. 애니메이션을 사용하지 않는다.
- 재생성: `python tools/build_terrain_art.py`. Python 표준 라이브러리만 사용하며 원본 PNG를 수정하지 않는다.

이 사이트는 비공식 팬 프로젝트이다. Minecraft와 게임 자산은 Mojang Studios / Microsoft의 소유이며, 이 목록은 제휴나 보증을 뜻하지 않는다.

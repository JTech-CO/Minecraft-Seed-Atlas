"""Arrange the downloaded vanilla textures into self-contained decorative SVGs.

Run ``python tools/build_terrain_art.py`` from any directory. No third-party
packages or remote requests are needed; source PNG bytes remain unchanged.
Original pixel colors become SVG paths to avoid browser raster interpolation.
"""

from __future__ import annotations

from pathlib import Path
import random
import struct
from xml.etree import ElementTree
import zlib


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "images" / "minecraft"
BLOCK = 64
COLS, ROWS = 12, 16
WIDTH, HEIGHT = COLS * BLOCK, ROWS * BLOCK


def png_pixels(path: Path) -> tuple[int, int, list[tuple[int, int, int, int]]]:
    """Decode the noninterlaced grayscale/palette formats of our original PNGs.

    Supports PNG filter methods 0-4 and tRNS transparency. Other input formats
    are rejected explicitly rather than silently changing any source colors.
    """
    content = path.read_bytes()
    if content[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Not a PNG: {path}")
    position, palette, transparency, compressed = 8, b"", b"", []
    width = height = bits = color = 0
    while position < len(content):
        length = struct.unpack_from(">I", content, position)[0]
        kind = content[position + 4:position + 8]
        payload = content[position + 8:position + 8 + length]
        expected_crc = struct.unpack_from(">I", content, position + 8 + length)[0]
        if zlib.crc32(kind + payload) != expected_crc:
            raise ValueError(f"PNG chunk checksum failed: {path}")
        if kind == b"IHDR":
            width, height, bits, color, compression, filtering, interlace = struct.unpack(
                ">IIBBBBB", payload
            )
            if not (width == 16 and 0 < height <= 320 and compression == filtering == interlace == 0):
                raise ValueError(f"Unsupported PNG dimensions or encoding: {path}")
            if not ((color == 0 and bits == 8) or (color == 3 and bits in (4, 8))):
                raise ValueError(f"Unsupported PNG pixel format: {path}")
        elif kind == b"PLTE":
            palette = payload
        elif kind == b"tRNS":
            transparency = payload
        elif kind == b"IDAT":
            compressed.append(payload)
        elif kind == b"IEND":
            break
        position += length + 12

    row_bytes = (width * bits + 7) // 8
    decoded = zlib.decompress(b"".join(compressed))
    if len(decoded) != (row_bytes + 1) * height:
        raise ValueError(f"Unexpected PNG pixel data length: {path}")
    previous = bytearray(row_bytes)
    pixels: list[tuple[int, int, int, int]] = []
    gray_transparent = struct.unpack(">H", transparency)[0] if color == 0 and transparency else None
    for row in range(height):
        offset = row * (row_bytes + 1)
        filter_type = decoded[offset]
        current = bytearray(decoded[offset + 1:offset + 1 + row_bytes])
        for index in range(row_bytes):
            left = current[index - 1] if index else 0
            up, upper_left = previous[index], previous[index - 1] if index else 0
            if filter_type == 0:
                predictor = 0
            elif filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = up
            elif filter_type == 3:
                predictor = (left + up) // 2
            elif filter_type == 4:
                estimate = left + up - upper_left
                distances = (abs(estimate - left), abs(estimate - up), abs(estimate - upper_left))
                predictor = (left, up, upper_left)[distances.index(min(distances))]
            else:
                raise ValueError(f"Unsupported PNG row filter: {path}")
            current[index] = (current[index] + predictor) & 255
        for column in range(width):
            value = current[column] if bits == 8 else (current[column // 2] >> (4 if column % 2 == 0 else 0)) & 15
            if color == 0:
                pixels.append((value, value, value, 0 if value == gray_transparent else 255))
            else:
                red, green, blue = palette[value * 3:value * 3 + 3]
                alpha = transparency[value] if value < len(transparency) else 255
                pixels.append((red, green, blue, alpha))
        previous = current
    return width, height, pixels


def texture_paths(name: str) -> list[str]:
    """Group equal source RGBA colors into paths on an exact four-pixel grid."""
    width, height, pixels = png_pixels(ASSETS / f"{name}.png")
    if width != 16 or height < 16:
        raise ValueError(f"Texture must contain a 16x16 first frame: {name}")
    groups: dict[tuple[int, int, int, int], list[str]] = {}
    scale = BLOCK // 16
    for y in range(16):
        x = 0
        while x < 16:
            rgba = pixels[y * 16 + x]
            end = x + 1
            while end < 16 and pixels[y * 16 + end] == rgba:
                end += 1
            if rgba[3]:
                span = (end - x) * scale
                groups.setdefault(rgba, []).append(f"M{x * scale} {y * scale}h{span}v{scale}h-{span}z")
            x = end
    paths = []
    for (red, green, blue, alpha), commands in sorted(groups.items()):
        opacity = f' fill-opacity="{alpha / 255:.12g}"' if alpha != 255 else ""
        paths.append(
            f'<path fill="#{red:02x}{green:02x}{blue:02x}"{opacity} '
            f'd="{"".join(commands)}"/>'
        )
    return paths


class TileMap:
    def __init__(self, title: str, textures: tuple[str, ...], *, height: int = HEIGHT):
        self.height = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
            f'height="{height}" viewBox="0 0 {WIDTH} {height}" '
            'style="image-rendering:pixelated" shape-rendering="crispEdges">',
            f"<title>{title}</title>",
            "<defs>",
        ]
        for name in textures:
            self.parts.extend([
                f'<pattern id="{name}" width="{BLOCK}" height="{BLOCK}" '
                'patternUnits="userSpaceOnUse" shape-rendering="crispEdges">',
                *texture_paths(name),
                "</pattern>",
            ])
        self.parts.append("</defs>")

    def rect(self, x: int, y: int, width: int, height: int, fill: str, opacity: float = 1):
        transparency = f' opacity="{opacity:g}"' if opacity != 1 else ""
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'fill="{fill}"{transparency}/>'
        )

    def region(self, x: int, y: int, width: int, height: int, texture: str):
        self.rect(x * BLOCK, y * BLOCK, width * BLOCK, height * BLOCK, f"url(#{texture})")

    def tiles(self, cells: set[tuple[int, int]], texture: str):
        for x, y in sorted(cells, key=lambda cell: (cell[1], cell[0])):
            if 0 <= x < COLS and 0 <= y < ROWS:
                self.region(x, y, 1, 1, texture)

    def void(self, cells: set[tuple[int, int]], *, color: str = "#101214"):
        # Each cavity follows the square block grid, including its roof and floor.
        for x, y in sorted(cells, key=lambda cell: (cell[1], cell[0])):
            if 0 <= x < COLS and 0 <= y < ROWS:
                self.rect(x * BLOCK, y * BLOCK, BLOCK, BLOCK, color)
        for x, y in sorted(cells, key=lambda cell: (cell[1], cell[0])):
            if not (0 <= x < COLS and 0 <= y < ROWS):
                continue
            if (x, y - 1) not in cells:
                self.rect(x * BLOCK, y * BLOCK, BLOCK, 8, "#000000", 0.38)
            if (x, y + 1) not in cells:
                self.rect(x * BLOCK, (y + 1) * BLOCK - 8, BLOCK, 8, "#000000", 0.24)

    def shade(self, seed: int, count: int, opacity: float = 0.12):
        rng = random.Random(seed)
        for _ in range(count):
            x, y = rng.randrange(COLS), rng.randrange(max(1, self.height // BLOCK))
            self.rect(x * BLOCK, y * BLOCK, BLOCK, BLOCK, "#000000", opacity)

    def save(self, name: str):
        rendered = "\n".join([*self.parts, "</svg>"]) + "\n"
        ElementTree.fromstring(rendered)
        (ASSETS / name).write_text(rendered, encoding="utf-8", newline="\n")


def shape(*rows: tuple[int, int, int]) -> set[tuple[int, int]]:
    """Return grid cells from (row, first column, exclusive last column)."""
    return {(x, y) for y, start, stop in rows for x in range(start, stop)}


def surface():
    art = TileMap("Overworld soil and stone", ("dirt", "stone"))
    art.region(0, 0, COLS, ROWS, "dirt")
    stone = shape(
        (5, 0, 2), (6, 0, 3), (7, 0, 4), (8, 0, 3),
        (3, 8, 11), (4, 7, 12), (5, 8, 12),
        (7, 5, 7), (8, 4, 8), (9, 4, 9),
        (9, 0, 2), (10, 0, 4), (10, 8, 12),
        (11, 0, 12), (12, 0, 12), (13, 0, 12), (14, 0, 12), (15, 0, 12),
    )
    art.tiles(stone, "stone")
    art.tiles(shape((11, 4, 7), (12, 5, 8), (13, 6, 8), (14, 0, 2)), "dirt")
    art.shade(10, 24, 0.09)
    art.save("terrain-surface.svg")


def grass_border():
    art = TileMap(
        "Grass block border", ("grass_block_side", "grass_block_side_overlay"), height=BLOCK
    )
    art.parts.append(
        '<defs><filter id="biome-grass" color-interpolation-filters="sRGB">'
        '<feColorMatrix type="matrix" values="'
        '0.38 0 0 0 0.09  0 0.65 0 0 0.16  '
        '0 0 0.20 0 0.035  0 0 0 1 0"/></filter></defs>'
    )
    art.region(0, 0, COLS, 1, "grass_block_side")
    art.parts.append(
        f'<rect width="{WIDTH}" height="{BLOCK}" '
        'fill="url(#grass_block_side_overlay)" filter="url(#biome-grass)"/>'
    )
    art.save("grass-border.svg")


def caves():
    ores = (
        "deepslate_iron_ore", "deepslate_gold_ore", "deepslate_redstone_ore",
        "deepslate_diamond_ore", "deepslate_lapis_ore",
    )
    art = TileMap("Overworld caves and mineral veins", ("stone", "deepslate", *ores))
    art.region(0, 0, COLS, ROWS, "deepslate")
    art.tiles(shape(
        (0, 0, 12), (1, 0, 12), (2, 0, 12), (3, 0, 7), (3, 10, 12),
        (4, 0, 4), (4, 9, 12), (5, 0, 2), (5, 10, 12), (6, 0, 1),
    ), "stone")
    holes = shape(
        (1, 1, 3), (2, 0, 4), (3, 0, 5), (4, 1, 4),
        (3, 9, 11), (4, 8, 12), (5, 8, 12), (6, 9, 11),
        (8, 4, 7), (9, 3, 8), (10, 4, 9), (11, 5, 8),
        (12, 0, 2), (13, 0, 3), (14, 0, 2),
        (12, 10, 12), (13, 9, 12), (14, 10, 12),
    )
    art.void(holes)
    veins = (
        (ores[0], shape((6, 1, 3), (7, 2, 4), (1, 9, 11))),
        (ores[1], shape((8, 10, 12), (9, 10, 11), (13, 4, 5))),
        (ores[2], shape((10, 0, 2), (11, 1, 3), (7, 7, 8))),
        (ores[3], shape((14, 4, 6), (15, 5, 7), (10, 10, 11))),
        (ores[4], shape((7, 9, 11), (8, 9, 10), (12, 7, 9))),
    )
    for texture, cells in veins:
        art.tiles(cells - holes, texture)
    art.shade(20, 20, 0.08)
    art.save("terrain-caves.svg")


def bedrock():
    art = TileMap("Bedrock boundary", ("bedrock",))
    art.region(0, 0, COLS, ROWS, "bedrock")
    art.shade(30, 45, 0.16)
    art.rect(0, 0, WIDTH, HEIGHT, "#05060a", 0.13)
    art.save("terrain-bedrock.svg")


def nether():
    art = TileMap("Nether rock, soul sand and quartz", ("netherrack", "soul_sand", "nether_quartz_ore"))
    art.region(0, 0, COLS, ROWS, "netherrack")
    art.tiles(shape(
        (0, 0, 2), (1, 0, 3), (2, 0, 4), (3, 1, 3),
        (6, 9, 12), (7, 8, 12), (8, 9, 12), (9, 10, 12),
        (12, 1, 3), (13, 0, 4), (14, 0, 5), (15, 1, 4),
    ), "soul_sand")
    holes = shape(
        (3, 8, 10), (4, 7, 11), (5, 8, 12),
        (7, 0, 2), (8, 0, 3), (9, 0, 2),
        (10, 5, 7), (11, 4, 8), (12, 5, 7),
    )
    art.void(holes, color="#200b10")
    art.tiles(shape(
        (1, 6, 8), (2, 7, 9), (4, 1, 3), (5, 2, 3),
        (9, 6, 8), (12, 9, 11), (13, 10, 12), (15, 7, 9),
    ) - holes, "nether_quartz_ore")
    art.shade(40, 25, 0.13)
    art.rect(0, 0, WIDTH, HEIGHT, "#360716", 0.11)
    art.save("terrain-nether.svg")


def lava():
    art = TileMap("Still lava and obsidian islands", ("lava_still", "obsidian"))
    # Only the first 16x16 source frame is read into the vector pattern.
    art.region(0, 0, COLS, ROWS, "lava_still")
    art.tiles(shape(
        (2, 0, 2), (3, 0, 3), (4, 1, 3),
        (6, 9, 11), (7, 8, 12), (8, 9, 12),
        (12, 2, 4), (13, 1, 5), (14, 2, 4),
    ), "obsidian")
    art.rect(0, 0, WIDTH, HEIGHT, "#802508", 0.12)
    art.save("terrain-lava.svg")


def end():
    art = TileMap("End islands, obsidian pillars and purpur", ("end_stone", "obsidian", "purpur_block"))
    art.rect(0, 0, WIDTH, HEIGHT, "#171025")
    islands = shape(
        (0, 0, 12), (1, 0, 12), (2, 0, 5), (2, 8, 12),
        (3, 1, 4), (3, 9, 12), (4, 2, 3), (4, 10, 11),
        (7, 0, 4), (8, 0, 5), (9, 0, 4), (10, 1, 3),
        (11, 7, 12), (12, 6, 12), (13, 7, 12), (14, 8, 11), (15, 9, 10),
    )
    art.tiles(islands, "end_stone")
    art.region(1, 4, 1, 3, "obsidian")
    art.region(10, 7, 1, 4, "obsidian")
    art.region(9, 9, 3, 1, "purpur_block")
    art.region(10, 8, 1, 1, "purpur_block")
    art.region(0, 6, 2, 1, "purpur_block")
    art.region(1, 5, 1, 1, "purpur_block")
    art.rect(0, 0, WIDTH, HEIGHT, "#130823", 0.08)
    art.save("terrain-end.svg")


def main():
    for generate in (surface, grass_border, caves, bedrock, nether, lava, end):
        generate()
    for path in sorted(ASSETS.glob("*.svg")):
        print(f"{path.relative_to(ROOT)}: {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

ROOT = Path(__file__).resolve().parent
SESSION_FILE = ROOT / "demo_session.txt"
GIT_LOG_FILE = ROOT / "git_log.txt"
IMAGES_DIR = ROOT.parent / "02_source" / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# Try Windows Korean font first, fallback to default font.
font_paths = [
    Path("C:/Windows/Fonts/malgun.ttf"),
    Path("C:/Windows/Fonts/arial.ttf"),
    Path("C:/Windows/Fonts/consola.ttf"),
]
font = None
for fp in font_paths:
    if fp.exists():
        try:
            font = ImageFont.truetype(str(fp), 18)
            break
        except Exception:
            continue
if font is None:
    font = ImageFont.load_default()

LINE_WIDTH = 100
IMAGE_WIDTH = 1200
PADDING = 16


def format_text(text):
    lines = text.splitlines()
    wrapped = []
    for line in lines:
        if not line:
            wrapped.append("")
            continue
        wrapped.extend(textwrap.wrap(line, width=LINE_WIDTH) or [""])
    return wrapped


def render_image(lines, output_path):
    if not lines:
        return
    wrapped_lines = []
    for line in lines:
        wrapped_lines.extend(format_text(line))
    # calculate height
    _, line_height = font.getbbox("A")[2:]
    line_height += 8
    img_height = PADDING * 2 + line_height * len(wrapped_lines)
    image = Image.new("RGB", (IMAGE_WIDTH, img_height), "#1e1e1e")
    draw = ImageDraw.Draw(image)
    y = PADDING
    for line in wrapped_lines:
        draw.text((PADDING, y), line, fill="#f8f8f2", font=font)
        y += line_height
    image.save(output_path)
    print(f"Saved {output_path}")


with SESSION_FILE.open("r", encoding="utf-8") as f:
    session_lines = [line.rstrip() for line in f.readlines()]

sections = [
    ("menu.png", "=== 나만의 프롬프트 관리 ===", "=== 프롬프트 추가 ==="),
    ("add_prompt.png", "=== 프롬프트 추가 ===", "=== 프롬프트 목록 ==="),
    ("list.png", "=== 프롬프트 목록 ===", "=== 나만의 프롬프트 관리 ===", 2),
    ("search.png", "=== 프롬프트 검색 ===", "=== 나만의 프롬프트 관리 ===", 2),
    ("detail.png", "=== 프롬프트 상세 보기 ===", "=== 나만의 프롬프트 관리 ===", 2),
    ("favorite.png", "=== 즐겨찾기 목록 ===", "=== 나만의 프롬프트 관리 ===", 2),
    ("top3.png", "=== 인기 프롬프트 Top 3 ===", "=== 나만의 프롬프트 관리 ===", 1),
]

for filename, start_marker, end_marker, skip in [(s[0], s[1], s[2], s[3] if len(s) > 3 else 0) for s in sections]:
    try:
        start = next(i for i, line in enumerate(session_lines) if line.strip() == start_marker)
    except StopIteration:
        print(f"Marker not found: {start_marker}")
        continue
    try:
        end = next(i for i, line in enumerate(session_lines[start + 1 :], start + 1) if line.strip() == end_marker)
    except StopIteration:
        end = len(session_lines)
    selected = session_lines[start + skip : end]
    render_image(selected, IMAGES_DIR / filename)

# Git log image if exists
if GIT_LOG_FILE.exists():
    with GIT_LOG_FILE.open("r", encoding="utf-8") as f:
        git_lines = [line.rstrip() for line in f.readlines()]
    render_image(["Git Commit Log"] + ["" ] + git_lines, IMAGES_DIR / "git_log.png")
else:
    print("git_log.txt not found, skipping git_log.png")

# Dev env image if exists
DEV_ENV_FILE = ROOT / "dev_env.txt"
if DEV_ENV_FILE.exists():
    with DEV_ENV_FILE.open("r", encoding="utf-8") as f:
        dev_lines = [line.rstrip() for line in f.readlines()]
    render_image(dev_lines, IMAGES_DIR / "dev_env.png")
else:
    print("dev_env.txt not found, skipping dev_env.png")

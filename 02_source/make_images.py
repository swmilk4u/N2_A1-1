from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

base_dir = Path(__file__).resolve().parent
session_file = base_dir.parent / "demo_session.txt"
output_file = base_dir / "demo_session.png"

if not session_file.exists():
    raise FileNotFoundError(f"Session file not found: {session_file}")

lines = session_file.read_text(encoding="utf-8").splitlines()

# Try Windows Korean font first, fallback to default.
font_paths = [
    Path("C:/Windows/Fonts/malgun.ttf"),
    Path("C:/Windows/Fonts/arial.ttf"),
    Path("C:/Windows/Fonts/consola.ttf"),
]
font = None
for path in font_paths:
    if path.exists():
        try:
            font = ImageFont.truetype(str(path), 18)
            break
        except Exception:
            pass
if font is None:
    font = ImageFont.load_default()

try:
    bbox = font.getbbox("A")
    line_height = bbox[3] - bbox[1] + 6
except Exception:
    line_height = font.size + 6
img_width = 1200
img_height = line_height * max(len(lines), 10) + 24
image = Image.new("RGB", (img_width, img_height), "#1e1e1e")
draw = ImageDraw.Draw(image)
draw.rectangle([0, 0, img_width, img_height], fill="#1e1e1e")
text_color = "#f8f8f2"

# Wrap lines if wider than image
wrapped_lines = []
for line in lines:
    if line == "":
        wrapped_lines.append("")
        continue
    # approximate wrap by char count
    max_chars = 100
    while len(line) > max_chars:
        wrapped_lines.append(line[:max_chars])
        line = line[max_chars:]
    wrapped_lines.append(line)

for idx, line in enumerate(wrapped_lines):
    draw.text((12, 12 + idx * line_height), line, font=font, fill=text_color)

# Crop to content
content_height = min(12 + len(wrapped_lines) * line_height + 12, img_height)
image = image.crop((0, 0, img_width, content_height))
image.save(output_file)
print(f"Saved image: {output_file}")

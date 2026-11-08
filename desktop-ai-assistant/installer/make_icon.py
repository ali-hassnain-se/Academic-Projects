"""Creates assets/logo.png and assets/icon.ico (a simple blue round 'AI' logo).

Run from the project folder (venv active, Pillow is already in requirements.txt):
    python installer/make_icon.py

You can replace the two output files with a nicer logo later; keep the same names."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

SIZE = 512
BLUE = (37, 99, 235, 255)          # same blue as the floating bubble

img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.ellipse((16, 16, SIZE - 16, SIZE - 16), fill=BLUE)

font = None
for name in ("arialbd.ttf", "arial.ttf", "segoeuib.ttf"):
    try:
        font = ImageFont.truetype(name, 230)
        break
    except OSError:
        continue
if font is None:
    font = ImageFont.load_default()

text = "AI"
box = draw.textbbox((0, 0), text, font=font)
w, h = box[2] - box[0], box[3] - box[1]
draw.text(((SIZE - w) / 2 - box[0], (SIZE - h) / 2 - box[1]), text, font=font, fill="white")

img.save(ASSETS / "logo.png")
img.save(
    ASSETS / "icon.ico",
    sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
)
print("Created:", ASSETS / "logo.png")
print("Created:", ASSETS / "icon.ico")

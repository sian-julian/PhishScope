"""Generate Chrome extension icons from the PhishScope logo."""

from pathlib import Path
from PIL import Image

LOGO_SRC = Path(__file__).parent.parent / "frontend" / "src" / "assets" / "PhishScope-logo.png"
ICONS_DIR = Path(__file__).parent / "icons"
SIZES = [16, 48, 128]

img = Image.open(LOGO_SRC).convert("RGBA")

# The logo has a white background — crop to just the icon mark (top portion)
# by making white pixels transparent for a cleaner icon, then composite on transparent
width, height = img.size

for size in SIZES:
    resized = img.resize((size, size), Image.LANCZOS)
    out_path = ICONS_DIR / f"{size}.png"
    resized.save(out_path, "PNG")
    print(f"Saved {out_path} ({size}x{size})")

print("All icons generated successfully.")

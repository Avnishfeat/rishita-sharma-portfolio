from __future__ import annotations

import shutil
import zipfile
from pathlib import Path
from urllib.parse import quote

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist-freekit"
ZIP_PATH = ROOT / "freekit-site.zip"
PORTFOLIO = ROOT / "Portfolio"

KEEP_AS_IS = {
    "CV_Rishita Sharma.pdf",
    "Ensite Logo.png",
    "WattMonk Logo.webp",
}


def clean() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    (DIST / "Portfolio").mkdir()
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()


def convert_image(src: Path, dest: Path) -> None:
    with Image.open(src) as image:
        image.thumbnail((1400, 1400), Image.Resampling.LANCZOS)
        if image.mode in ("RGBA", "LA") or (
            image.mode == "P" and "transparency" in image.info
        ):
            canvas = Image.new("RGB", image.size, (255, 255, 255))
            if image.mode != "RGBA":
                image = image.convert("RGBA")
            canvas.paste(image, mask=image.getchannel("A"))
            image = canvas
        else:
            image = image.convert("RGB")
        image.save(dest, "JPEG", quality=84, optimize=True, progressive=True)


def copy_assets() -> dict[str, str]:
    replacements: dict[str, str] = {}
    for src in sorted(PORTFOLIO.iterdir()):
        if not src.is_file():
            continue

        if src.name in KEEP_AS_IS or src.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
            dest_name = src.name
            shutil.copy2(src, DIST / "Portfolio" / dest_name)
        else:
            dest_name = f"{src.stem}.jpg"
            convert_image(src, DIST / "Portfolio" / dest_name)

        replacements[src.name] = dest_name
    return replacements


def write_index(replacements: dict[str, str]) -> None:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for old_name, new_name in replacements.items():
        if old_name == new_name:
            continue
        html = html.replace(f"Portfolio/{quote(old_name)}", f"Portfolio/{quote(new_name)}")
        html = html.replace(f"Portfolio/{old_name}", f"Portfolio/{new_name}")
    (DIST / "index.html").write_text(html, encoding="utf-8")


def create_zip() -> None:
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(DIST.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(DIST).as_posix())


def main() -> None:
    clean()
    replacements = copy_assets()
    write_index(replacements)
    create_zip()
    size_mb = ZIP_PATH.stat().st_size / (1024 * 1024)
    print(f"Built {ZIP_PATH.name}: {size_mb:.2f} MB")
    if ZIP_PATH.stat().st_size > 10 * 1024 * 1024:
        raise SystemExit("FreeKit ZIP limit is 10MB; generated archive is too large.")


if __name__ == "__main__":
    main()

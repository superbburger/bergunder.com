#!/usr/bin/env python3
"""
generate_manifest.py
--------------------
Run this from the directory containing index.html to rebuild manifest.json
from whatever roll folders exist under ./rolls/.

Folder structure expected:
  rolls/
    roll-001/            ← folder name becomes the roll ID
      title.txt          ← optional display name
      001.jpg
      002.jpg
      ...
      thumbnails/        ← smaller versions for carousel display
        001.jpg
        002.jpg
        ...
    roll-002/
      ...

Usage:
  python3 generate_manifest.py

Thumbnails are matched to full-res frames by filename. If a thumbnail is
missing for a given frame, the full-res image is used as fallback.
"""

import json, re
from pathlib import Path

ROLLS_DIR  = Path("rolls")
MANIFEST   = Path("manifest.json")
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

def natural_sort_key(s):
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', str(s))]

def build_manifest():
    if not ROLLS_DIR.is_dir():
        print(f"[error] '{ROLLS_DIR}' directory not found. Create it and add roll subfolders.")
        return

    roll_dirs = sorted(
        [d for d in ROLLS_DIR.iterdir() if d.is_dir()],
        key=lambda d: natural_sort_key(d.name)
    )

    rolls = []
    for roll_dir in roll_dirs:
        roll_id = roll_dir.name

        # Optional title file
        title_file = roll_dir / "title.txt"
        title = title_file.read_text().strip() if title_file.exists() else roll_id

        # Full-res images (exclude the thumbnails subfolder)
        images = sorted(
            [f for f in roll_dir.iterdir()
             if f.is_file() and f.suffix.lower() in IMAGE_EXTS],
            key=lambda f: natural_sort_key(f.name)
        )

        if not images:
            print(f"[skip] {roll_id} — no images found")
            continue

        # Thumbnail lookup by filename (stem + any image ext)
        thumb_dir = roll_dir / "thumbnails"
        thumb_map = {}
        if thumb_dir.is_dir():
            for t in thumb_dir.iterdir():
                if t.is_file() and t.suffix.lower() in IMAGE_EXTS:
                    thumb_map[t.stem] = str(t.as_posix())

        # Build frame list: {src, thumb}
        frames = []
        missing_thumbs = 0
        for img in images:
            src   = str(img.as_posix())
            thumb = thumb_map.get(img.stem)
            if thumb is None:
                thumb = src   # fallback to full-res
                missing_thumbs += 1
            frames.append({"src": src, "thumb": thumb})

        rolls.append({"id": roll_id, "title": title, "frames": frames})

        note = f" ({missing_thumbs} thumbs missing, using full-res)" if missing_thumbs else ""
        print(f"[ok]   {roll_id} — '{title}' — {len(frames)} frames{note}")

    manifest = {"rolls": rolls}
    MANIFEST.write_text(json.dumps(manifest, indent=2))
    print(f"\nWrote {MANIFEST} with {len(rolls)} roll(s).")

if __name__ == "__main__":
    build_manifest()

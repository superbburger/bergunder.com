#!/usr/bin/env python3
"""
generate_manifest.py
--------------------
Run this from the directory containing index.html to rebuild manifest.json
from whatever roll folders exist under ./rolls/.

Folder structure expected:
  rolls/
    roll-001/       ← folder name becomes the roll ID
      001.jpg
      002.jpg
      ...
    roll-002/
      001.jpg
      ...

Usage:
  python3 generate_manifest.py

Optional: set a title for each roll in a file called "title.txt" inside the
roll folder. If absent, the folder name is used as the title.
"""

import json, os, re
from pathlib import Path

ROLLS_DIR   = Path("rolls")
MANIFEST    = Path("manifest.json")
IMAGE_EXTS  = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

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

        # Collect image files, sorted naturally
        images = sorted(
            [f for f in roll_dir.iterdir() if f.suffix.lower() in IMAGE_EXTS],
            key=lambda f: natural_sort_key(f.name)
        )

        if not images:
            print(f"[skip] {roll_id} — no images found")
            continue

        frames = [str(img.as_posix()) for img in images]

        rolls.append({"id": roll_id, "title": title, "frames": frames})
        print(f"[ok]   {roll_id} — '{title}' — {len(frames)} frames")

    manifest = {"rolls": rolls}
    MANIFEST.write_text(json.dumps(manifest, indent=2))
    print(f"\nWrote {MANIFEST} with {len(rolls)} roll(s).")

if __name__ == "__main__":
    build_manifest()

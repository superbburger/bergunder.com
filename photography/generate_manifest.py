#!/usr/bin/env python3
"""
generate_manifest.py
--------------------
Run this from the directory containing index.html to rebuild manifest.json
from whatever roll folders exist under ./rolls/.

Folder naming convention:
  YYYYMMDD-YYYYMMDD     e.g. 20240315-20240318
  (start date hyphen end date; use the same date twice for a single-day roll)

Folder structure expected:
  rolls/
    20240315-20240318/   <- folder name encodes the date range
      title.txt          <- optional display name
      001.jpg
      002.jpg
      ...
      thumbnails/        <- smaller versions for carousel display
        001.jpg
        002.jpg
        ...

Usage:
  python3 generate_manifest.py

Rolls are written newest-first (by start date, descending).
Thumbnails are matched to full-res frames by filename. If a thumbnail is
missing for a given frame, the full-res image is used as fallback.
"""

import json, re
from pathlib import Path

ROLLS_DIR  = Path("rolls")
MANIFEST   = Path("manifest.json")
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
DATE_RE    = re.compile(r'^(\d{8})-(\d{8})$')

def natural_sort_key(s):
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', str(s))]

def parse_dates(folder_name):
    """Return (date_start, date_end) as 'YYYYMMDD' strings, or (None, None)."""
    m = DATE_RE.match(folder_name)
    if m:
        return m.group(1), m.group(2)
    return None, None

def build_manifest():
    if not ROLLS_DIR.is_dir():
        print(f"[error] '{ROLLS_DIR}' directory not found. Create it and add roll subfolders.")
        return

    roll_dirs = [d for d in ROLLS_DIR.iterdir() if d.is_dir()]

    # Sort by start date descending (newest first); fall back to name for undated folders
    def sort_key(d):
        start, _ = parse_dates(d.name)
        return start if start else d.name  # lexicographic on YYYYMMDD works correctly

    roll_dirs = sorted(roll_dirs, key=sort_key, reverse=True)

    rolls = []
    for roll_dir in roll_dirs:
        roll_id = roll_dir.name

        date_start, date_end = parse_dates(roll_id)
        if not date_start:
            print(f"[warn] {roll_id} -- folder name doesn't match YYYYMMDD-YYYYMMDD, skipping date")

        # Optional title file
        title_file = roll_dir / "title.txt"
        title = title_file.read_text().strip() if title_file.exists() else roll_id

        # Full-res images (files only; excludes thumbnails/ subdir automatically)
        images = sorted(
            [f for f in roll_dir.iterdir()
             if f.is_file() and f.suffix.lower() in IMAGE_EXTS],
            key=lambda f: natural_sort_key(f.name)
        )

        if not images:
            print(f"[skip] {roll_id} -- no images found")
            continue

        # Thumbnail lookup by filename stem
        thumb_dir = roll_dir / "thumbnails"
        thumb_map = {}
        if thumb_dir.is_dir():
            for t in thumb_dir.iterdir():
                if t.is_file() and t.suffix.lower() in IMAGE_EXTS:
                    thumb_map[t.stem] = str(t.as_posix())

        frames = []
        missing_thumbs = 0
        for img in images:
            src   = str(img.as_posix())
            thumb = thumb_map.get(img.stem)
            if thumb is None:
                thumb = src
                missing_thumbs += 1
            frames.append({"src": src, "thumb": thumb})

        entry = {"id": roll_id, "title": title, "frames": frames}
        if date_start:
            entry["date_start"] = date_start
            entry["date_end"]   = date_end

        rolls.append(entry)

        note      = f" ({missing_thumbs} thumbs missing, using full-res)" if missing_thumbs else ""
        date_note = f" [{date_start} - {date_end}]" if date_start else ""
        print(f"[ok]   {roll_id}{date_note} -- '{title}' -- {len(frames)} frames{note}")

    manifest = {"rolls": rolls}
    MANIFEST.write_text(json.dumps(manifest, indent=2))
    print(f"\nWrote {MANIFEST} with {len(rolls)} roll(s), newest first.")

if __name__ == "__main__":
    build_manifest()

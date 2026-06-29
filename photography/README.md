# Film Archive — GitHub Pages Setup

A darkroom-styled film archive page with horizontal filmstrip carousels.

## File structure

```
your-repo/
  film/               ← or whatever path you want (can be root)
    index.html
    manifest.json
    generate_manifest.py
    rolls/
      roll-001/
        title.txt     ← optional: "Portland, March"
        001.jpg
        002.jpg
        ...
      roll-002/
        title.txt
        001.jpg
        ...
```

## Adding a new roll

1. Create a folder under `rolls/` — name it anything (e.g. `roll-003` or `london-june`)
2. Drop your scans in, named so they sort correctly (e.g. `001.jpg`, `002.jpg` …)
3. Optionally add a `title.txt` containing the display name (e.g. `London, June`)
4. Run the manifest generator:
   ```bash
   cd film/      # wherever index.html lives
   python3 generate_manifest.py
   ```
5. Commit and push — GitHub Pages will serve the updated archive

## Customising

In `index.html`, near the top of the `<script>` block:

```js
const FRAME_HEIGHT = 240;   // height of each image in the strip (px)
const FRAME_WIDTH  = 320;   // width of each image in the strip (px)
```

Adjust these to suit your scan aspect ratio (e.g. 6×6 medium format: set both to 260).

## Hosting on a sub-path

If your archive lives at `yourname.github.io/film/`, no changes needed —
`manifest.json` is loaded relative to `index.html`.

If you want the page at the repo root, move everything up one level and adjust
the `rolls/` paths accordingly (the generator will handle this automatically).

## Image tips

- Export scans as progressive JPEGs at ~85% quality for fast loading
- Name files with zero-padded numbers: `001.jpg` not `1.jpg`
- GitHub Pages has no file-size limit per se, but keep individual frames
  under ~2 MB for smooth scrolling on mobile

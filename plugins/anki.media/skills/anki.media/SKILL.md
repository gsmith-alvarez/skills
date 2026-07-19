---
name: Anki Media
description: Media on Anki cards — [sound:file.mp3], <img src="file.jpg">, static template media (leading-underscore naming), the collection.media folder, supported formats (MP3/MP4), importing media via text files, LaTeX-rendered images, and TTS. Use when adding audio, images, video, or generated media to cards.
---

# Anki Media

Media lives in the **collection.media** folder next to your collection. Anki
copies files in when you add/paste them, which makes backup and transfer easy.
Source: manual `media.md`, `importing/text-files.md` (Importing Media),
`templates/fields.md` (Media & LaTeX).

## References (go inside fields)

- **Sound**: `[sound:myaudio.mp3]` in a field.
- **Image**: `<img src="myimage.jpg">` in a field.
- **Video**: same mechanism as sound/image (mpv/mplayer backend).

## Static template media

For media identical on every card (e.g. a logo): name the file with a **leading
underscore** (`_logo.jpg`). The underscore marks it as template-owned so it is
exported with the deck and ignored by Check Media. Reference it directly in the
template: `<img src="_logo.jpg">`.

> **Never reference fields in template media.** `<img src="{{Expression}}.jpg">`,
> `[sound:{{Word}}]`, `[latex]{{Field}}[/latex]` are unsupported — they may fail
> to display and won't be counted for unused-media scans or import/export. Put
> the media tag **inside the field** instead.

## Filenames

Spaces/special chars (e.g. `hello 100%.jpg`) appear percent-encoded in the HTML
editor (`hello%20100%25.jpg`) but Anki uses the original on disk. Search/rename
with the **disk** name; export to text to see the raw form.

## Supported formats

Backend is mpv (mplayer fallback). A wide range works on desktop, but **MP3
audio and MP4 video are the most universally supported** across AnkiWeb and
mobile.

## Importing media in bulk

1. Copy files into `collection.media` — **no subdirectories** (some features
   break otherwise).
2. Reference them in a field: `<img src="myimage.jpg">` or `[sound:myaudio.mp3]`.
3. Enable **Allow HTML in fields** on import.
4. Or use Find&Replace in the browser: search `(.*)`, replace with
   `[sound:\1.mp3]` (regex on), to turn bare filenames into sound tags.
5. The *media import* add-on can auto-create notes from a folder of files.

## Manual additions & Check Media

After dropping files directly into `collection.media`, run **Tools → Check Media**
so filenames are encoded correctly (skipped files won't sync). Anki doesn't follow
symlinks in the media folder — copy real files (symlinks fail on mobile).

**Tools → Check Media** also reports unused media and missing-media references,
and can delete unused files or tag broken notes.

## LaTeX-generated images

LaTeX equations render to images stored in `collection.media`. Run Check Media to
bulk-generate them before studying on web/mobile.

## TTS

Text-to-speech tags (`{{tts en_US:Field}}`, `[anki:tts …]`) belong in templates —
see anki.card-templates.

## Pitfalls

1. Media references belong in **fields**, never as field references inside a
   template's `<img>`/`[sound:]`.
2. No subdirectories in `collection.media`.
3. Prefer MP3/MP4 for cross-platform safety.
4. After manual media drops, run Check Media or files may not sync.
5. Symlinks in the media folder break on mobile.

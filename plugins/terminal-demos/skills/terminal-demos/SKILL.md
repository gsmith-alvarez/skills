---
name: terminal-demos
description: "Use when recording TUI demos, screenshots or GIFs."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [vhs]
metadata:
  hermes:
    tags: [TUI, VHS, GIF, Screenshots, Documentation, Terminal]
---

# Recording terminal / TUI demos (screenshots + GIFs)

Produce README-quality PNGs and an animated GIF of a real terminal UI by driving it
through a PTY with [VHS](https://github.com/charmbracelet/vhs) (ttyd + Chromium + ffmpeg).
No ML vision, no mockups, no hand-edited images: the pixels come from the app itself.

## When to use

- A terminal app's README has screenshots that are stale, hand-cropped, or hosted as
  GitHub user-attachments instead of repo files.
- You need a short "watch it work" GIF for a TUI (debugger, editor, installer, dashboard).
- You need visual evidence of what a TUI actually draws, e.g. while chasing a layout bug.

## Setup

```bash
nix run nixpkgs#vhs -- --version     # bundles ttyd/ffmpeg/chromium, nothing else needed
brew install vhs                    # macOS
```

Optional compression: `pngquant` (flat-colour captures shrink ~4x) and `gifsicle`.
Verification helpers: `tesseract` (OCR the pixels), `ffmpeg`/`ffprobe` (sample frames).

## Layout that works

```
docs/
  demo.tape              # the animated tour
  screens.tape           # stills, runtime states (panes, modals)
  screens-zoom.tape      # stills that need a fresh session per zoom state
  render.sh              # rebuild binary -> run every tape -> compress
  demo/*.asm             # tiny sample programs the tapes load
  img/*.png, img/demo.gif
```

One session per "state family". Do not try to take 8 stills in one recording: focus and
modal state drifts and you get the wrong pane in the shot.

## The tape

See `templates/demo.tape` for a complete working example. The skeleton:

```
Output docs/img/demo.gif
Set FontFamily "JetBrains Mono"
Set FontSize 15            # 15-17px is right for GitHub; 1440x880 (gif) / 1760x1080 (png)
Set Width 1440
Set Height 880
Set Padding 24
Set BorderRadius 8
Set TypingSpeed 25ms
Set Framerate 24
Set Theme {"background": "#1e1e2e", "foreground": "#cdd6f4"}

Hide                        # do not record the shell setup
Type "cd /abs/path/to/demo"
Enter
Type "../../target/release/app sample.asm"
Enter
Sleep 2s
Show

Type "c"                    # drive real keybindings, one step per line
Sleep 1s
Screenshot docs/img/overview.png
```

## Rules that cost me a rerun each

1. **Tape paths are relative to VHS's cwd, not the tape file.** Start with an absolute
   `cd`, and remember `Output`/`Screenshot` paths resolve the same way. `Screenshot` with
   a quoted path containing spaces fails to parse — use relative, space-free paths.
2. **Count directory depth carefully.** `cd docs/demo` then `../target/...` points at
   `docs/target`. Wrong depth looks like a missing binary, not a path bug.
3. **Sleep ≥250 ms after every `Tab`/`Escape` before the next key.** Two keys arriving in
   one read get coalesced and the app handles only one — this silently produces "the zoom
   toggle did nothing" screenshots.
4. **A `Screenshot` can land after the next keystroke.** Put the shot last in a step, sleep
   ~700 ms after it, and never end a tape with `q` (a save-confirmation modal ends up in the
   image). VHS kills the shell when the tape ends.
5. **Hidden time is not recorded.** `Hide ... Show` setup makes the GIF shorter than the sum
   of your `Sleep`s; check `ffprobe -show_entries format=duration` and the frame timeline,
   not your arithmetic.
6. **Slow the app down for run animations.** A `:`-command like `:speed 20` (or equivalent
   in your app) turns an instant jump-cut into a visible multi-pane trace; at max speed the
   GIF is a single frame change.
7. **Focus-aware keymaps bite.** Vim-style TUIs often bind `p`/`P` to paste when the editor
   pane is focused and to "step back" elsewhere. Tab away first, or the tape edits the buffer
   and every later screenshot carries a `[*]` modified marker. Read the keymap before scripting.

## Verify without looking at the image

You cannot eyeball the PNG, so assert on the pixels:

```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=width,height -of default=nw=1 out.gif
ffmpeg -v error -ss 6 -i out.gif -frames:v 1 /tmp/f.png -y     # sample specific moments
TESSDATA_PREFIX=$(dirname $(find /nix/store -maxdepth 3 -name tessdata -type d | head -1)) \
  tesseract shot.png - | grep -iE "ZOOMED|Total|ERROR"      # OCR the frame
```

Checks that catch real mistakes: expected pane/modal title present, no `ERROR`/`NaN` strings
in the frame, `[ZOOMED] <Pane>` matches what you meant to shoot, image is 1760x1080, colour
count > ~10k (not a blank frame).

Better than OCR for layout: add a dev-only example that renders one frame through
`ratatui::backend::TestBackend` and prints it as text, with a comma-separated key script
(`"c,n,:,stack,<enter>"`). Same state, exact grid, greppable, no recording. Use it to work
out tab counts, then transcribe 1:1 into the tape.

## Finish

- Compress: `pngquant --force --quality=70-95 --output f.png -- f.png`,
  `gifsicle -O3 --lossy=60 --colors 200 demo.gif -o demo.gif`. Budget ~5 MB total.
- Reference repo-local paths in the README (`docs/img/overview.png`); GitHub rewrites them
  to `/raw/main/...` correctly, verified with `curl -sL <repo> | grep -o 'src="[^"]*docs/img[^"]*"'`.
- Ship `render.sh` so the next person regenerates instead of re-shooting by hand.
- Screenshots are a bug detector: if a frame shows `ERROR:` in a column that should hold an
  encoding, that is usually a render-time re-encode bug worth fixing before publishing.

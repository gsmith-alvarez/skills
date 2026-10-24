# Template: animated tour of a terminal UI -> docs/img/demo.gif
#   nix run nixpkgs#vhs -- docs/demo.tape
Output docs/img/demo.gif

Set Shell "bash"
Set FontFamily "JetBrains Mono"
Set FontSize 15
Set Width 1440
Set Height 880
Set Padding 24
Set BorderRadius 8
Set TypingSpeed 25ms
Set Framerate 24
Set Theme {"background": "#1e1e2e", "foreground": "#cdd6f4"}

Hide
Type "cd /abs/path/to/project/docs/demo"
Enter
Type "../../target/release/app sample.asm"
Enter
Sleep 2s
Show

# Compile / load: panes fill in.
Type "c"
Sleep 1.2s

# Single steps, spaced so the frame changes are visible at 24 fps.
Type "n"
Sleep 240ms
Type "n"
Sleep 240ms
Type "n"
Sleep 400ms

# Tab away from an editor pane before pressing p/P (often Vim paste there).
Tab
Sleep 300ms
Type "p"
Sleep 240ms
Type "p"
Sleep 500ms

# A modal worth showing.
Type ":"
Sleep 150ms
Type "stack"
Sleep 250ms
Enter
Sleep 1.8s
Escape
Sleep 500ms

# Slow the run down so the animation reads in a GIF, then finish.
Type ":"
Sleep 150ms
Type "speed 20"
Sleep 250ms
Enter
Sleep 400ms
Type "r"
Sleep 4.5s

# No trailing "q": VHS ends the session, and the quit prompt would land in the GIF.
Sleep 700ms

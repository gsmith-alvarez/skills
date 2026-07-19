---
name: Neovim Snippet API
description: Reference for vim.snippet in Neovim Lua (expand/jump/active/stop). Use when implementing or driving LSP/extensible snippet expansion and tabstop navigation in plugins or configs.
---

# Neovim Snippet API Reference

Reference for `vim.snippet`, Neovim's built-in snippet engine (0.10+). Use these to expand snippets and move between tabstops programmatically. (Signatures reflect Neovim 0.13; `available()` was removed — use `active()` instead.)

---

## snippet

```lua
vim.snippet.expand({body})
vim.snippet.jump({direction})
vim.snippet.active({opts})
vim.snippet.stop()
```

### notes
* `expand(body)` — expand the snippet string `body` at the cursor. Supports LSP-style `$1`, `${1:placeholder}`, and `${1|a,b|}` choices.
* `jump(direction)` — move to the next tabstop (`1`) or previous (`-1`).
* `active(opts)` — returns the active snippet session at the cursor, or `nil`. Replaces the older `available()`.
* `stop()` — terminate the active snippet session, leaving the final text in place.

---
name: nvim.utility
description: Reference for the miscellaneous vim.* helpers in Neovim Lua not covered by the other nvim skills — table helpers, json/mpack, inspect, iter, version, notify/log, string utils, validate/defer, options accessors, vim.system, vim.snippet, vim.highlight, and vim.ui. Use for general-purpose Lua helpers when writing plugins.
---

# Lua utility apis

Use the target Neovim installation’s help for version-specific signatures and behavior (start with `:help lua`). For other versions, consult the matching release’s documentation. The online [Lua utility APIs documentation](https://neovim.io/doc/user/lua.html) tracks current Neovim and may differ from the target. Relevant help topics: lua.

Prefer documented public APIs; names beginning with `_` are internal. Check `:help deprecated` before using older APIs.

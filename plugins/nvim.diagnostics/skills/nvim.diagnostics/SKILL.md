---
name: nvim.diagnostics
description: Reference for vim.diagnostic and diagnostic-namespace APIs in Neovim Lua (signs, virtual text/lines, goto next/prev, qf/loclist, enable/disable). Use when implementing diagnostics display or navigation.
---

# Diagnostic apis

Use the target Neovim installation’s help for version-specific signatures and behavior (start with `:help diagnostic`). For other versions, consult the matching release’s documentation. The online [diagnostic APIs documentation](https://neovim.io/doc/user/diagnostic.html) tracks current Neovim and may differ from the target. Relevant help topics: diagnostic.

Prefer documented public APIs; names beginning with `_` are internal. Check `:help deprecated` before using older APIs.

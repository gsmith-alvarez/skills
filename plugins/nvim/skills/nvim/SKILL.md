---
name: nvim
description: Reference for Neovim's Lua API surface (vim.api, vim.fn, and builtin helpers such as vim.schedule, vim.wait, vim.ui_*). Use when writing or editing Neovim Lua plugins/configs, or when an agent needs exact vim.api/vim.fn signatures.
---

# Api, vim.fn, builtin functions

Use the target Neovim installation’s help for version-specific signatures and behavior (start with `:help api`). For other versions, consult the matching release’s documentation. The online [api, vim.fn, builtin functions documentation](https://neovim.io/doc/user/api.html) tracks current Neovim and may differ from the target. Relevant help topics: api, lua, builtin.

Prefer documented public APIs; names beginning with `_` are internal. Check `:help deprecated` before using older APIs.

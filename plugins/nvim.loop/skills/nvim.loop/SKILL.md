---
name: nvim.loop
description: Reference for vim.loop / vim.uv (libuv) bindings in Neovim Lua — timers, spawned processes, filesystem, streams/pipes, OS queries, and handle lifecycle. Use when writing async I/O, timers, job runners, or file watchers.
---

# Libuv bindings

Use the target Neovim installation’s help for version-specific signatures and behavior (start with `:help vim.uv`). For other versions, consult the matching release’s documentation. The online [libuv bindings documentation](https://neovim.io/doc/user/luvref.html) tracks current Neovim and may differ from the target. Relevant help topics: vim.uv, luvref.

Prefer documented public APIs; names beginning with `_` are internal. Check `:help deprecated` before using older APIs.

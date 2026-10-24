---
name: nvim.keymap
description: Reference for vim.keymap in Neovim Lua (set/del and mapping options). Use when creating, modifying, or removing key mappings, buffer-local maps, or callback mappings.
---

# Neovim Keymap API Reference

Reference for `vim.keymap`, the Lua API for defining and removing key mappings. Prefer it over the lower-level `vim.api.nvim_set_keymap` because option handling (especially `desc` and `buffer`) is cleaner.

---

## keymap

```lua
vim.keymap.set({modes}, {lhs}, {rhs}, {opts})
vim.keymap.del({modes}, {lhs}, {opts})
```

* `modes` — a string (`"n"`) or table (`{"n", "v"}`) of mode prefixes (`n` normal, `i` insert, `v` visual+select, `x` visual, `s` select, `o` operator-pending, `t` terminal, `c` command-line, `!` insert+command-line, `""`/empty for all).
* `lhs` — the key sequence to map (use `<leader>`, `<C-x>`, `<Space>` notation).
* `rhs` — a string of Vimscript/`{rhs}` to execute, OR omit and pass `callback` in `opts` to run Lua.

### opts fields
* `desc` — human-readable description; shown by `:map` and which-key, and enables safe remapping/dedup.
* `buffer` — make the mapping buffer-local (a buffer number, or `0` for the current buffer).
* `remap` — if `true`, allow `rhs` to be a recursive remap (like `:map`); default `false` (`noremap`).
* `noremap` — inverse of `remap`; default `true`.
* `silent` — suppress command-line output (`<silent>`).
* `expr` — `rhs` (or `callback`'s return) is evaluated to a string before execution.
* `callback` — a Lua function called instead of a string `rhs`.
* `nowait` — skip waiting for further keys in the prefix (`<nowait>`).
* `unique` — error if a mapping with the same `lhs` already exists.

### examples
```lua
vim.keymap.set("n", "<leader>w", ":w<CR>", { desc = "Save", silent = true })
vim.keymap.set("n", "<leader>f", function() print("find") end, { desc = "Find" })
vim.keymap.set("n", "<C-h>", "<C-w>h", { remap = true, buffer = 0 })
```

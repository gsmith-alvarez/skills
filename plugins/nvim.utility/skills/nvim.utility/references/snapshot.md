# Neovim Utility (vim.*) API Reference

Catch-all reference for the `vim.*` helpers that are not covered by the dedicated `nvim`, `nvim.diagnostics`, `nvim.lsp`, `nvim.treesitter`, `nvim.loop`, `nvim.keymap`, and `nvim.fs` skills. Signatures reflect Neovim 0.13.

---

## tbl

Table helpers. (Note: `vim.tbl_islist` was removed — use `vim.islist(t)`.)

```lua
vim.tbl_extend({behavior}, {...})
vim.tbl_deep_extend({behavior}, {...})
vim.tbl_contains({t}, {value})
vim.tbl_count({t})
vim.tbl_keys({t})
vim.tbl_values({t})
vim.tbl_flatten({t})
vim.tbl_map({fn}, {t})
vim.tbl_filter({fn}, {t})
vim.tbl_get({t}, {...})
```

---

## json

```lua
vim.json.encode({obj})
vim.json.decode({str}, {opts})
```

---

## mpack

```lua
vim.mpack.encode({obj})
vim.mpack.decode({str})
vim.mpack.pack({...})
vim.mpack.unpack({str}, {offset})
vim.mpack.new_packer({opts})
```

---

## inspect

```lua
vim.inspect({obj}, {opts})
```

---

## iter

`vim.iter` wraps a list/iterator for lazy, chainable traversal (0.10+). The object is callable (`vim.iter(list)`). Common chain methods include `enumerate`, `map`, `filter`, `totable`, `nth`, `last`, `head`, `tail`, `fold`, `find`, `any`, `all`, `flatten`, `dedup`, `reverse`, `slice`, `consume`, and `into`.

```lua
vim.iter({list})
```

---

## version

```lua
vim.version()
vim.version.parse({str})
```

Version objects compare via `vim.version.eq/gt/ge/lt/le/ne(a, b)`.

---

## notify

```lua
vim.notify({msg}, {level}, {opts})
vim.notify_once({msg}, {level}, {opts})
vim.log.levels          -- table of levels (TRACE/DEBUG/INFO/WARN/ERROR)
```

---

## strings

```lua
vim.split({s}, {sep}, {opts})
vim.trim({s}, {mask})
vim.deepcopy({orig})
vim.pesc({str})
vim.regex({str})
```

---

## validation

```lua
vim.validate({spec})
vim.defer_fn({fn}, {timeout})
vim.cmd({cmd})
```

* `validate(spec)` — `spec` is a table of `{name, fn, ...}` entries asserting argument types; throws on mismatch.
* `defer_fn(fn, timeout)` — run `fn` once after `timeout` ms (does not block the loop).
* `cmd` is callable: `vim.cmd("w")` or `vim.cmd.w({...})`.

---

## options

Accessors for Neovim options and variables.

```lua
vim.opt              -- global options meta-table (vim.opt.number = true)
vim.o                -- string options (vim.o.shiftwidth = 2)
vim.wo[{winid}]      -- window-local options
vim.bo[{bufnr}]      -- buffer-local options
vim.g                -- global variables (vim.g.my_var = ...)
vim.env              -- environment variables (vim.env.PATH)
vim.v                -- v: variables (vim.v.count)
```

---

## system

See the dedicated `nvim.system` skill for the full `vim.system` reference (spawn, opts, and the returned handle's `wait`/`kill`/`pid`).

---

## snippet

See the dedicated `nvim.snippet` skill for the full `vim.snippet` reference (`expand`/`jump`/`active`/`stop`).

---

## highlight

```lua
vim.highlight.create({name}, {opts}, {priority})
vim.highlight.range({buf}, {ns}, {hl}, {srow}, {scol}, {erow}, {ecol})
vim.highlight.priorities
```

---

## ui

`vim.ui` provides the user-interaction prompts (select/input/open).

```lua
vim.ui.select({items}, {opts}, {on_choice})
vim.ui.input({opts}, {on_confirm})
vim.ui.open({target})
```

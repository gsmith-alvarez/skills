---
name: nvim.fs
description: Reference for vim.fs in Neovim Lua — path joining, dirname/basename/ext, normalization, mkdir/rm, find, and directory/parent iterators. Use when manipulating file paths or walking directories.
---

# Neovim Filesystem API Reference

Reference for `vim.fs`, path and filesystem helpers. Signatures reflect Neovim 0.13. `vim.fs.dir` and `vim.fs.parents` return iterators — consume them with `for ... in vim.fs.dir(path) do ... end`.

---

## fs

```lua
vim.fs.joinpath({...})
vim.fs.dirname({path})
vim.fs.basename({path})
vim.fs.ext({path})
vim.fs.normalize({path}, {opts})
vim.fs.abspath({path})
vim.fs.relpath({path}, {to})
vim.fs.mkdir({path}, {opt})
vim.fs.rm({path}, {opt})
vim.fs.find({name}, {opt})
vim.fs.root({path}, {marker})
```

### iterator helpers
* `vim.fs.dir({path}, {opt})` — iterate the entries of a directory, yielding `name, type` per entry.
* `vim.fs.parents({path}, {opt})` — iterate ancestor directories upward from `path` (used to walk up and find a project root).

### field notes
* `joinpath(...)` — joins path components with the OS separator; variadic.
* `normalize(path, opts)` — collapses `.`/`..`, makes absolute when `opts.ExpandEnv`/`opts.absolute` set; returns a canonical path string.
* `find(name, opt)` — search for `name` (string or list) under `opt.path` (default `cwd`), honoring `opt.limit`, `opt.type`, `opt.glob`; returns a list of matches or a single path when `opt.limit == 1`.
* `root(path, marker)` — walk parents (via `vim.fs.parents`) looking for `marker` (a filename, list of names, or predicate) and return the directory containing it, or `nil`.

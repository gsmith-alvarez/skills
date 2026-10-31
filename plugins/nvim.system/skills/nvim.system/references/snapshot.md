# Neovim System (process) API Reference

Reference for `vim.system`, the modern, libuv-backed process runner introduced in Neovim 0.10. It supersedes the old `system()`/`systemlist()` and is simpler than `vim.loop.spawn` for most command execution.

---

## system

```lua
vim.system({cmd}, {opts}, {on_exit})
```

### opts fields
* `cwd` — working directory for the child process.
* `env` — table of environment variables; replaces the parent env unless `clear_env` is set.
* `clear_env` — if `true`, start with an empty environment and only `env`.
* `stdin` / `stdout` / `stderr` — `"pipe"` (default) or `"null"`; when `"pipe"` the stream is captured.
* `text` — if `true`, treat streams as text (results are strings, not `userdata`) and enable line iterators.
* `timeout` — kill the process after this many milliseconds.
* `detach` — if `true`, detach the child from the Neovim process.

### returned handle
`vim.system` returns a handle table. It exposes:

```lua
handle:wait({timeout})   -- block until exit; returns { code, signal, stdout, stderr }
handle:kill({signal})    -- send a signal (default SIGTERM)
handle.pid               -- the child PID (number)
handle.cmd               -- the resolved command table
```

### examples
```lua
-- async, capture text output
local obj = vim.system({ "git", "status", "--porcelain" }, { text = true }, function(out)
  print(out.code, out.stdout)
end)
local result = obj:wait()   -- block for completion if needed

-- synchronous
local r = vim.system({ "ls" }, { text = true }):wait()
print(r.stdout)
```

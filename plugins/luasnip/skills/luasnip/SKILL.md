---
name: LuaSnip API
description: Reference for the LuaSnip snippet-engine API (require('luasnip')) — node constructors (s/sn/t/i/f/c/d/r), snippet opts (trig/wordTrig/regTrig/snippetType/condition/callbacks), events, add_snippets, and extras (fmt/rep/lambda/match). Use when authoring, editing, or debugging LuaSnip snippets and autosnippets in this plugin.
---

# LuaSnip API Reference

LuaSnip is a Lua snippet engine (Neovim 0.9–0.11). Snippets are built from
**nodes**. This skill covers the surface used to write/modify snippets in
`latex-tools.nvim` and the surrounding engine API. Signatures are drawn from
LuaSnip's bundled `doc/luasnip.txt` (v0.11).

> Every snippet authoring file should begin with the standard aliases. They are
> **not** global — define them per file or rely on `ls.setup({ snip_env = ... })`
> + `ls.setup_snip_env()` for the lua-loader.

```lua
local ls = require("luasnip")
local s   = ls.snippet
local sn  = ls.snippet_node
local isn = ls.indent_snippet_node
local t   = ls.text_node
local i   = ls.insert_node
local f   = ls.function_node
local c   = ls.choice_node
local d   = ls.dynamic_node
local r   = ls.restore_node
local ms  = ls.multi_snippet
local parse = require("luasnip.util.parser").parse_snippet

local events = require("luasnip.util.events")
local ai = require("luasnip.nodes.absolute_indexer")
local k  = require("luasnip.nodes.key_indexer").new_key
local opt = require("luasnip.nodes.optional_arg")

local extras = require("luasnip.extras")
local l   = extras.lambda
local rep = extras.rep
local p   = extras.partial
local m   = extras.match
local n   = extras.nonempty
local dl  = extras.dynamic_lambda
local fmt  = require("luasnip.extras.fmt").fmt
local fmta = require("luasnip.extras.fmt").fmta
local conds = require("luasnip.extras.conditions")
```

---

## Node constructors

Every node takes an optional `node_opts` table as its last arg. Common keys:
`key`, `node_ext_opts`/`merge_node_ext_opts`, `node_callbacks` (per-node events,
same shape as snippet `callbacks` but without the jump-index layer), `user_args`.

### `t(text, node_opts?)` — TextNode
Static text. `text` is a `string` or `string[]` (one entry per line). A blank
line is `""`. Multiline example: `t({ "line 1", "", "line 3" })`.

### `i(jump_index, text?, node_opts?)` — InsertNode
Editable text. `text` defaults to `""` (or a `string[]` for a default spanning
multiple lines). Receives the jump-index that decides tabstop order. `i(0)` is
the final exit node and may appear **only in the root snippet, never in a
snippetNode** (`sn`).

### `f(fn, argnode_references, node_opts?)` — FunctionNode
```lua
f(function(args, parent, user_args1, ...)
  return "text"          -- string or string[]
end, {2}, { user_args = {...} })
```
- `args`: `string[][]` — `args[j]` is the list of lines of argnode reference `j`
  (so `args[1][1]` is the first line of node `{2}`).
- `parent`: the node. `parent.snippet` is the containing snippet; for a
  `regTrig` snippet, `parent.snippet.captures` holds capture groups and
  `parent.snippet.trigger` the matched trigger.
- `argnode_references`: list of jump-indices (`{2}`, `{2,1}`) or absolute
  indexers (`ai[2]`, `ai[1]`).

### `sn(jump_index, nodes, node_opts?)` — SnippetNode
A nested snippet. `nodes` is a node or node list (same as `s`). **No `i(0)`** —
jump-indices restart at `1..n`. Used inside `c`, `d`, and `i` (as children).

### `isn(jump_index, nodes, indentstring, node_opts?)` — IndentSnippetNode
Like `sn` but re-indents its content; `$PARENT_INDENT` in `indentstring`
references the parent's indent.

### `c(jump_index, choices, opts?)` — ChoiceNode
`choices` is a list of nodes (text/insert/snippet/fragment). The **first** is
the initial choice and must be reachable (contain a jump point — an `i` or a
textNode, which is special-cased to stop at its start). If a choice is a
`sn(nil, {...})`, it **must** contain an `i(1)`. Cycle choices with
`ls.change_choice(1|-1)` / `<C-e>`/`<C-y>` style maps.

### `d(jump_index, fn, node_references, opts?)` — DynamicNode
```lua
d(2, function(args, parent, old_state, user_args)
  return sn(nil, { i(1, args[1]) })   -- returns a snippetNode, NOT a snippet
end, {1})
```
`fn` returns a `sn(nil, {...})` (a SnippetNode, position-less). `old_state`
carries prior state for re-expansion. Set `opts.snippetstring_args = true` to
pass args as snippetstring-style. Function nodes inside must not emit embedded
`\n` — build multiline text as `string[]` or use `fmt`.

### `r(jump_index, key, nodes?, node_opts?)` — RestoreNode
`restoreNode`s sharing the same `key` across a snippet share content. Provide a
default via the snippet's `stored` table:
```lua
s("trig", { c(1, { sn(nil, { t"(" , r(1,"x"), t")" }),
                   sn(nil, { t"[" , r(1,"x"), t"]" }) }) },
  { stored = { x = i(1, "default") } })
```

---

## The snippet constructor `s(context, nodes, opts?)`

`context` is a trigger string or a table:
```lua
s({ trig = "...", regTrig = true, wordTrig = false, priority = 100,
    snippetType = "autosnippet", condition = fn, show_condition = fn,
    dscr = "...", name = "...", docstring = "...", docTrig = "3", hidden = false },
  { ...nodes... },
  { callbacks = {...}, key = "..." })
```

Key `opts` (3rd arg / inside context table — do not set both):

| key | type | meaning |
|---|---|---|
| `trig` | string | trigger. Matched exactly by default (see `wordTrig`). |
| `wordTrig` | bool | (default `true`) require `[\%w_]+` before cursor to match trigger entirely. Set `false` for `regTrig`/postfix-style. |
| `regTrig` | bool | treat `trig` as a Lua pattern. Prefer `trigEngine = "pattern"` instead. |
| `trigEngine` | string/func | `"vim"` (default), `"lua"`, `"pattern"`, or a custom matcher. |
| `priority` | number | higher wins when triggers overlap. |
| `snippetType` | `"snippet"`\|`"autosnippet"` | auto-expand needs `ls.config.setup({ enable_autosnippets = true })`. Singular form required. |
| `condition` | `fn(line_to_cursor, matched_trigger, captures) -> bool` | gate manual expansion (`ls.expand()`). Return `true` to allow. |
| `show_condition` | `fn(line_to_cursor) -> bool` | gate completion-engine candidates. |
| `name` / `dscr` | string | internal name / description. |
| `docstring` / `docTrig` | string | override generated docstring (needed when `regTrig` captures are consumed as numbers). |
| `hidden` | bool | hide from completion. |
| `callbacks` | table | event callbacks (see below). |
| `resolveExpandParams` | `fn(snippet, line_to_cursor, matched_trigger, captures) -> table\|nil` | override trigger/captures/env at expand time (used by postfix/TS helpers). |

`condition` is the standard hook for context-gated math snippets:
`in_mathzone_not_text()` (math zone but not inside `\text{}`) etc.

---

## `callbacks` & events

`callbacks` maps a **jump-index** (node position, not jump-index) to a table of
event→function. The special index **`[-1]`** is the snippet itself — it fires
when the snippet is first entered (just expanded, cursor at the first insert
node). This is the mechanism `latex-tools` uses to enlarge enclosing brackets.

```lua
local events = require("luasnip.util.events")
callbacks = {
  [2] = { [events.enter] = function(node, event_args) ... end,
          [events.leave] = function(node, event_args) ... end },
  [-1] = { [events.enter]      = fn,        -- fires on first expansion
           [events.pre_expand] = function(snippet, event_args)
             return { env_override = { KEY = "val" } } end },
}
```
Per-node equivalents go in `node_callbacks` (no jump-index layer).

Events: `enter`/`leave` (on jump), `change_choice` (choice switched),
`pre_expand` (before expand; may return `env_override`). Access live
`node`/`event_args` via `require("luasnip").session.event_node` /
`.event_args`. Global hooks fire `User` autocommands
(`LuasnipInsertNodeEnter`, `LuasnipPreExpand`, `LuasnipChangeChoice`,
`LuasnipCleanup`, `LuasnipSnippetsAdded`).

> In `latex-tools`, `auto_brackets.enlarge_enclosing` is wired as
> `callbacks = { [-1] = { [events.enter] = auto_brackets.enlarge_enclosing } }`.
> The callback defers its buffer edit with `vim.schedule` so LuaSnip finishes
> wiring extmarks first.

---

## Registering snippets: `ls.add_snippets(ft?, snippets, opts?)`

```lua
ls.add_snippets("markdown", { s(...), s(...) })
ls.add_snippets("tex", auto_list, { key = "latex-tools-tex-auto", type = "autosnippets" })
ls.add_snippets("markdown", { mk, dm }, { key = "latex-tools-md-entry", type = "autosnippets" })
```

- `ft`: filetype string, or `nil` if `snippets` is `{ [ft] = list }`.
- `snippets`: flat list of addables (`s`, `ms`, `sp`) or a `{ft = list}` map.
- `opts`:
  - `type`: `"snippets"` (default) or `"autosnippets"`.
  - `key`: stable id. Re-registering with the **same key** replaces the previous
    set — use it for idempotent reloads (the repo keys every batch
    `latex-tools-<ft>-{auto,regular,extra,md-entry}`).
  - `refresh_notify`: bool.

`ls.filetype_extend("sh", {"zsh"})` makes `zsh` snippets available in `sh`.
`ls.cleanup()` wipes all snippets (fires `LuasnipCleanup`).

---

## Expansion / runtime API

| call | effect |
|---|---|
| `ls.expand(opts?)` | expand a snippet whose trigger matches text before cursor |
| `ls.expand_auto()` | expand a matching autosnippet |
| `ls.expand_or_jump()` | expand, else jump forward |
| `ls.snip_expand(snippet, opts?)` | expand an explicit snippet object |
| `ls.lsp_expand(body, opts?)` | expand an LSP-style string (`"[$1]($2)"`) |
| `ls.jump(dir)` | `1`/`-1` jump |
| `ls.choice_active()` / `ls.change_choice(val)` | choice-node introspection |
| `ls.unlink_current()` | detach current snippet from jumplist |
| `ls.get_snippets(ft?, {type})` | retrieve registered snippets |

Autosnippets only fire if `ls.config.setup({ enable_autosnippets = true })` was
called.

---

## Extras

- `fmt(template, nodes, opts?)` / `fmta(...)` — `fmt` interpolates `{node}`;
  `fmta` uses `<>` delimiters (handy in `{}`-heavy LaTeX). **Returns a list of
  nodes, not a snippet** — wrap in `s(...)`. `opts.delimiters` overrides;
  `opts.repeat_duplicates = true` repeats named nodes. Use `fmt` whenever a
  function/dynamic node would otherwise emit `\n`.
- `rep(jump_index)` — repeat a node's text (`extras.rep(1)`).
- `extras.lambda` (`l`) — `l._1`, `l._2` … reference argnodes for inline
  transforms; combinable with `m`/`dl`.
- `extras.match` (`m`) — `m(n, pattern, replacement)` inserts text if node `n`
  matches.
- `extras.partial` (`p`) — `p(fn, jump_index)` wraps a function.
- `extras.nonempty` (`n`) — `n(1, "if-present", "if-empty")`.
- `extras.dynamic_lambda` (`dl`) — `dl(2, l._1..l._1, 1)`.
- `extras.conditions` (`conds`) — `conds.expand.line_end`,
  `conds.expand.line_begin`, `trigger_not_preceded_by(...)`, combinable with
  `+`/`-`/`*`/`^`/`%` (or/and/not/xor/xnor) for `condition`/`show_condition`.

Standard snippet-string interpolation (`$1`, `${1:placeholder}`, `${1|a,b|}`)
is available via `parse` (`require("luasnip.util.parser").parse_snippet`) or
the `snip_env` `parse` alias.

---

## Pitfalls (frequent in this plugin)

1. **No embedded `\n` from `f`/`d` callbacks.** Return `string[]` lines or use
   `fmt`. A single string with `\n` corrupts extmarks. (Repo `AGENTS.md`.)
2. **`sn` has no `i(0)`.** Use `1..n` only.
3. **Jump-indices restart at 1** inside each nested `sn`.
4. **ChoiceNode first choice must be reachable** — every choice needs a jump
   point; `sn(nil,{...})` choices need an `i(1)`.
5. **`regTrig` autosnippets** need `wordTrig = false` (or `trigEngine =
   "pattern"`) and `enable_autosnippets = true`. A bare `pmat` must not steal
   `3*3pmat` — guard static snippets with a `not_dyn_matrix_autosnip_suffix()`
   condition.
6. **`restoreNode` keys are global per snippet** — shared content; provide
   defaults via `stored`.
7. **`dynamicNode` returns `sn(nil, {...})`**, not `s(...)`. Access regex
   captures defensively: `snip.captures or snip.snippet.captures` (the repo's
   `generate_matrix_body` does exactly this).
8. **`fmt` is not a snippet** — `s("trig", fmt("...{x}...", { x = i(1) }))`.
9. **Re-register by `key`** for idempotent reloads; otherwise duplicate
   registrations cause ordering bugs (commit `951b38b`).
10. **Triggers and categories** are keyed by the *original* trigger string (raw
    pattern for regex snippets) in the `overrides`/`disable`/`categories`
    pipeline — body/nodes are not patchable, only `trig`/`wordTrig`/`regTrig`.

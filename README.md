# omp-neovim-skills

Neovim Lua API reference skills, test-planning workflow skills, Anki card-generation skills, and a terminal-demo recording workflow, packaged as an [oh-my-pi](https://github.com/) marketplace. Each skill installs independently and is discoverable via `skill://<name>`.

## Install

Add the marketplace, then install plugins:

```
/marketplace add gsmith-alvarez/omp-neovim-skills
/marketplace install nvim@omp-neovim-skills
/marketplace install anki.cloze@omp-neovim-skills
/marketplace install nvim.system@omp-neovim-skills
```

CLI equivalent:

```
omp plugin marketplace add gsmith-alvarez/omp-neovim-skills
omp plugin install nvim@omp-neovim-skills
```

Local testing before publishing:

```
/marketplace add ./path/to/this/repo
```

## Plugins

| Plugin | Category | Description |
|---|---|---|
| `nvim` | development | vim.api / vim.fn / builtin surface |
| `nvim.diagnostics` | development | vim.diagnostic + diagnostic namespaces |
| `nvim.lsp` | development | vim.lsp / buf / util / codelens / semantic_tokens |
| `nvim.treesitter` | development | treesitter Lua APIs |
| `nvim.loop` | development | vim.loop / vim.uv (libuv) |
| `nvim.keymap` | development | vim.keymap set/del |
| `nvim.fs` | development | vim.fs path helpers |
| `nvim.utility` | development | misc vim.* helpers |
| `nvim.snippet` | development | vim.snippet expand/jump/active/stop |
| `nvim.system` | development | vim.system process runner |
| `luasnip` | development | LuaSnip engine: node constructors, snippet opts, events/callbacks, add_snippets, extras |
| `anki.note-types` | education | notes vs cards, fields, note types, built-in types, card-generation rules |
| `anki.card-templates` | education | template language: field replacement, conditionals, filters, special fields, HTML/CSS |
| `anki.cloze` | education | cloze deletion syntax, generation, nested clozes, per-card conditionals, Image Occlusion |
| `anki.math` | education | MathJax and LaTeX in cards, mhchem, cloze/LaTeX delimiter conflicts |
| `anki.media` | education | sound/image/video tags, static template media, collection.media, formats, import |
| `anki.import-export` | education | CSV/TSV import, file headers, duplicates/GUID, .apkg/.colpkg packaged decks |
| `prime-planning` | productivity | test-first planning |
| `regression-testing` | development | regression test protocol |
| `terminal-demos` | development | VHS recordings of TUIs -> README screenshots + GIF |

## Layout

```
.omp-plugin/marketplace.json     # omp catalog (preferred)
.claude-plugin/marketplace.json  # Claude Code-compatible fallback
plugins/
  <name>/
    skills/<name>/SKILL.md       # one skill per plugin dir
scripts/validate_marketplace.py  # catalog <-> disk consistency check
```

## Validate

```
python scripts/validate_marketplace.py
```

Checks: catalog parses, every plugin has a matching `skills/<name>/SKILL.md`, no duplicate plugin names.

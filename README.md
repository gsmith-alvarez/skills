# skills

A personal collection of agent skills, packaged as an oh-my-pi marketplace with a Claude Code-compatible manifest. Every skill installs independently and is discoverable via `skill://<name>`.

The collection spans Neovim/Lua API reference, Anki authoring, planning and testing workflows, terminal-demo recording, NixOS homelab operations, and third-party skill adoption. New domains are added as new plugins without changing the catalog identity.

## Install

Add the marketplace, then install the skills you want:

```
/marketplace add gsmith-alvarez/skills
/marketplace install nvim@skills
/marketplace install anki.cloze@skills
/marketplace install regression-testing@skills
/marketplace install homelab-server-delta@skills
```

CLI equivalent:

```
omp plugin marketplace add gsmith-alvarez/skills
omp plugin install nvim@skills
omp plugin install agent-skill-adoption@skills
```

Local testing before publishing:

```
/marketplace add ./path/to/this/repo
```

## Skills

### Neovim & Lua

| Skill | Description |
|---|---|
| `nvim` | vim.api / vim.fn / builtin surface |
| `nvim.diagnostics` | vim.diagnostic + diagnostic namespaces |
| `nvim.lsp` | vim.lsp / buf / util / codelens / semantic_tokens |
| `nvim.treesitter` | treesitter Lua APIs |
| `nvim.loop` | vim.loop / vim.uv (libuv) |
| `nvim.keymap` | vim.keymap set/del |
| `nvim.fs` | vim.fs path helpers |
| `nvim.utility` | misc vim.* helpers |
| `nvim.snippet` | vim.snippet expand/jump/active/stop |
| `nvim.system` | vim.system process runner |
| `luasnip` | LuaSnip engine: node constructors, snippet opts, events/callbacks, add_snippets, extras |

### Anki

| Skill | Description |
|---|---|
| `anki.note-types` | notes vs cards, fields, note types, built-in types, card-generation rules |
| `anki.card-templates` | template language: field replacement, conditionals, filters, special fields, HTML/CSS |
| `anki.cloze` | cloze deletion syntax, generation, nested clozes, per-card conditionals, Image Occlusion |
| `anki.math` | MathJax and LaTeX in cards, mhchem, cloze/LaTeX delimiter conflicts |
| `anki.media` | sound/image/video tags, static template media, collection.media, formats, import |
| `anki.import-export` | CSV/TSV import, file headers, duplicates/GUID, .apkg/.colpkg packaged decks |

### Planning & testing

| Skill | Description |
|---|---|
| `prime-planning` | feature planning and verification |
| `regression-testing` | focused regression verification |

### Terminal & documentation

| Skill | Description |
|---|---|
| `terminal-demos` | VHS recordings of TUIs → README screenshots + GIF |

### Infrastructure & operations

| Skill | Description |
|---|---|
| `homelab-server-delta` | NixOS homelab server: verified module map, Compose-to-NixOS corrections, snapshot gap |

### Agent tooling

| Skill | Description |
|---|---|
| `agent-skill-adoption` | surveying + auditing third-party agent skills and MCP servers before install |

## MCP servers

`mcp.json` contains personal server configuration. Entries use `exposure: "deferred"` to request on-demand tool exposure in clients that support it; this setting does not guarantee that a client delays starting the server or loading its tools. Check your client's MCP documentation and use its own lazy-loading or tool-search settings where available. Clients that ignore or reject these extra fields may need a client-specific configuration.

The Playwright and SQLite commands are machine-specific and those servers are listed as disabled; adjust their paths and enable them only where installed. The NixOS endpoint is a private network address. The `disabledServers` field is also client-specific. Do not assume these settings apply to every MCP client.

## Reference freshness

Neovim API skills point to official documentation and the target installation’s version-matched help. Other API and Anki reference skills can also age; check the target version's official documentation before relying on exact signatures or behavior. Homelab details describe a particular environment and should be verified against its current configuration.

## Layout

```
.omp-plugin/marketplace.json     # omp catalog
.claude-plugin/marketplace.json  # Claude Code-compatible mirror
mcp.json                         # central MCP server manifest (see below)
plugins/
  <name>/
    skills/<name>/SKILL.md       # one skill per plugin dir
skills/                          # flat shims -> plugins/<name>/skills/<name>
                                 # (one-level discovery roots scan only
                                 # <dir>/<name>/SKILL.md, so this flat view
                                 # lets omp/pi custom directories and pi's
                                 # user-skills path find every skill)
scripts/validate_marketplace.py  # catalog <-> disk consistency check
```

## Add a skill

1. Create `plugins/<name>/skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`). `name` must match the directory/plugin slug; it becomes the `skill://<name>` handle.
2. Add the plugin to both catalogs with `name`, `description`, `source: "./<name>"`, `category`, and `tags`.
3. Run `python scripts/validate_marketplace.py`.

## Validate

```
python scripts/validate_marketplace.py
```

Checks: catalog parses, every plugin has a matching `skills/<name>/SKILL.md`, its frontmatter `name` matches the plugin name, and no plugin names are duplicated.

---
name: nvim.lsp
description: Reference for vim.lsp, vim.lsp.buf, vim.lsp.util, vim.lsp.codelens, vim.lsp.semantic_tokens, and the LSP protocol APIs in Neovim Lua. Use when wiring language-server features (hover, definitions, references, code actions, formatting, completion, inlay hints).
---

# Language-server apis

Use the target Neovim installation’s help for version-specific signatures and behavior (start with `:help lsp`). For other versions, consult the matching release’s documentation. The online [language-server APIs documentation](https://neovim.io/doc/user/lsp.html) tracks current Neovim and may differ from the target. Relevant help topics: lsp.

Prefer documented public APIs; names beginning with `_` are internal. Check `:help deprecated` before using older APIs.

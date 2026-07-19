---
name: God-Tier Documentation
description: Rules and templates for maintaining high-quality, educational documentation in this Neovim configuration.
---

# God-Tier Documentation Standard

This skill defines the mandatory documentation and commenting standards for this Neovim configuration. Every file must be treated as an educational resource for the user, prioritizing the "Why" (intent) over the "What" (syntax).

## 1. Core Philosophy
- **Intent over Syntax**: Never just restate what the code does. Explain the architecture, the trade-offs, and the specific problem being solved.
- **Phased-Boot Context**: Always mention where a file sits in the `init.lua` boot sequence (Sync Phase 1, JIT, etc.).
- **Anti-Fragile Design**: Document how the configuration handles failures (e.g., `pcall`, fallback defaults).

## 2. File Header Standard
Every Lua file must begin with a structured header block:

```lua
-- [[ TITLE: path/to/file ]]
-- =============================================================================
-- Purpose: [1 sentence summary]
-- Domain:  [e.g., Core / UI / LSP]
--
-- Architecture: [Deep explanation of how this module interacts with others]
-- Philosophy: [The reasoning behind specific design choices]
--
-- Maintenance:
-- 1. [Common update task A]
-- 2. [Common update task B]
-- =============================================================================
```

## 3. Visual Grouping & Separators
Use consistent horizontal bars to logically group code blocks:

- **Major Sections**: `-- =============================================================================`
- **Minor Sub-sections**: `-- -----------------------------------------------------------------------------`

## 4. In-Line Commenting Style
- **Section Headers**: Use nested headers for logical blocks within `M.setup()` or the main script.
- **The "Rationale" Callout**: For non-obvious choices, explicitly use a `WHY:` or `RATIONALE:` prefix.
- **GitHub Alerts**: When drafting reports or artifacts for the user, use standard GitHub Markdown alerts (`> [!NOTE]`, `> [!IMPORTANT]`, etc.).

## 5. Metadata Maintenance
- When adding OR removing a file, you MUST update [docs/CONFIG_MAP.md](file:///home/gsmith-alvarez/dotfiles/nvim/docs/CONFIG_MAP.md) immediately.
- Use the status `[x]` or `[ ]` in the inventory to track documentation coverage.

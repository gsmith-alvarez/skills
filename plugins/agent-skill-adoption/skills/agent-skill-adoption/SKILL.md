---
name: agent-skill-adoption
description: Find, audit, and adopt third-party agent skills safely.
category: autonomous-ai-agents
version: 0.1.1
author: Giovanni (gsmith-alvarez), Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skills, adoption, audit, catalog, security]
    related_skills: [hermes-agent, hermes-agent-skill-authoring]
---

# Adopting third-party agent skills

Discovery plus audit of community skills/MCP servers before installing them. The answer is usually a small mix, not the top hit.

Bundled skill dirs (`~/.hermes/skills/autonomous-ai-agents/hermes-agent/` and other shipped skills) are read-only here; new depth goes into user-local skills or existing writable ones.

## When to Use

- "Are there any skills for X?", "what's out there for X?" — a survey request.
- "Which of these fits my setup?", "is a mix better?" — a selection request against a design doc or an existing stack.
- Before installing anything from the catalog or GitHub that will propose commands.
- Don't use for: authoring a skill in the Hermes repo (that's `hermes-agent-skill-authoring`), or general Hermes feature questions (that's `hermes-agent` + its docs index).

## 1. Discover

1. `manage_catalog(action="search", kind="skill", query="<term>")`. Run several query words (topic, product name, broader category) — one query returns ≤10 and ranking is fuzzy. Ids are `<owner>/<repo>/<skill>` for mirrored skills.sh entries and bare slugs for curated ones. `kind="plugin"` + `query=""` lists plugins.
2. GitHub second — the catalog is a mirror and misses most of the ecosystem:
   ```bash
   gh search repos "<topic> skills" --limit 15
   gh api repos/<o>/<r> --jq '"\(.full_name) | ⭐\(.stargazers_count) | pushed \(.pushed_at[0:10]) | \(.description)"'
   ```
3. Inspect without cloning. The `description:` frontmatter IS the trigger the model loads on, so judge from it, then read the body:
   ```bash
   gh api repos/<o>/<r>/git/trees/HEAD?recursive=1 --jq '.tree[].path' | grep 'SKILL.md$'
   gh api repos/<o>/<r>/contents/<path> -H 'Accept: application/vnd.github.raw' | sed -n '1,10p'
   ```
4. **Grep the body for the capability actually needed.** README claims are marketing: a Caddy skill with zero `ts.net` matches cannot help with Tailscale certificates however it is described. `gh api ... | grep -inE '<term>'` settles it in one call.

## 1b. Reading a bare-slug (clawhub) entry without installing

Bare-slug catalog ids (`zfs`, `homelab-ai`, `homelab-runbook`) come from **clawhub** and have empty `repo`/`path`, so `gh api` has nothing to read. Two ways in:

```bash
# the whole SKILL.md, plus stats (downloads/installs/versions) and updatedAt
curl -s https://clawhub.ai/api/v1/skills/<slug> \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["skill"]["description"])'
```

The local index cache enumerates every catalog entry with its `source`, `identifier`, and `repo` — use it to resolve how an id is sourced, or to count what exists:

```bash
python3 -c 'import json;d=json.load(open("'"$HERMES_HOME"'/skills/.hub/index-cache/hermes-index.json"));
print(len(d["skills"]));print([s for s in d["skills"] if s["identifier"]=="zfs"])'
```

`source` is one of `clawhub` (~80%), `skills.sh`, `github`, `lobehub`, `browse-sh`, `official`. Only `skills.sh`/`github`/`browse-sh` entries carry a repo path for direct inspection.

## 2. Judge — what decides against a skill

- **Wrong execution model.** A Compose-oriented skill applied to a declarative stack makes the agent propose `docker-compose.yml` where native modules exist. Check its verbs (`docker run`, `network_mode:`, `compose.yaml`).
- **Trust-model conflict.** Ops/MCP packages sometimes default to unprompted `switch` plus passwordless sudo. When the user's model is "agent proposes, human activates," install with privileged verbs disabled (build/check/eval/diff only) or not at all — say which verbs are safe rather than declining the whole package.
- **Generated doc dumps.** Auto-generated references stay stale silently (`pushed_at` is fresh because the generator ran, not because content changed), duplicate what local tooling answers better (`nix-index`/`comma`, `--help`, `--json`), and are usually the biggest context cost in the library.
- **Overlap with a local machine skill.** Instance skills (hostnames, paths, this user's flow) are not replaced by general ones; installing on top leaves two competing instruction sets. Frame the distinction as topic knowledge vs instance knowledge.
- **Single-author, low-star, inactive** — fine for a topic note, disqualifying for anything that proposes destructive commands.

## 3. Recommend

- Smallest set that covers real gaps, plus an explicit "skipping X because Y". Two installs with reasons beats a ranked list of ten.
- Lead the reply with the verdict, then a table mapping the user's own sections/needs to the pick, then the traps. This user wants the mechanism, not a catalogue.
- Name the concrete conflict when a popular skill is wrong for the stack — that is the part no README or star count conveys.
- State the security reality once, plainly: a skill is instructions loaded into context, so it shapes what gets executed with the user's hands. Read every `.md` before install.

## 4. Install

- Catalog: `manage_catalog(action="install", items=[{"kind": "skill", "id": "<id>"}])` — one approval card; the user can skip rows.
- Otherwise clone into `$HERMES_HOME/skills/<category>/<name>/`. Resolve `$HERMES_HOME`, never hardcode `~/.hermes`, so it lands in the active profile.
- Verify after install: the skill appears in `skills_list` next session (the loader is cached at session start, so a fresh install is invisible in the current session — expected, not a failure).

## Pitfalls

- Writing a support file into a bundled skill's `references/` fails with `PermissionError` — shipped skill dirs are read-only. Extend a user-local skill instead.
- Do not install a skill whose default behavior needs sudo just because its README is convenient; check the trust section before recommending.
- Do not summarize ten candidates equally. A survey with no verdict is the failure mode this user pushes back on.
- `skill_manage(action="delete")` is irreversible from the tool's side: it does not stage the file anywhere. If a skill's content only exists in context (it was never read from disk this session), deleting it destroys it. Patch, never delete, when editing.

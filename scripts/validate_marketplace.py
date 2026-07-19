#!/usr/bin/env python3
"""Validate the marketplace catalog against on-disk plugin layout."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, ".omp-plugin", "marketplace.json")


def main() -> int:
    with open(CATALOG, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    for field in ("name", "owner", "plugins"):
        if field not in data:
            print(f"FAIL: missing top-level field '{field}'")
            return 1
    if not data["owner"].get("name"):
        print("FAIL: missing owner.name")
        return 1

    plugin_root = data.get("metadata", {}).get("pluginRoot", "")
    plugins = data["plugins"]
    if not plugins:
        print("FAIL: no plugins listed")
        return 1

    seen = set()
    for plugin in plugins:
        name = plugin.get("name")
        if not name:
            print("FAIL: plugin missing name")
            return 1
        if name in seen:
            print(f"FAIL: duplicate plugin name '{name}'")
            return 1
        seen.add(name)

        source = plugin.get("source")
        if not source or not isinstance(source, str) or not source.startswith("./"):
            print(f"FAIL: plugin '{name}' needs a relative string source")
            return 1

        rel = source[2:]
        if plugin_root:
            rel = os.path.join(plugin_root, rel)
        skill = os.path.join(ROOT, rel, "skills", name, "SKILL.md")
        if not os.path.isfile(skill):
            print(f"FAIL: plugin '{name}' missing {skill}")
            return 1
        print(f"ok: {name}")

    print(f"valid: {len(plugins)} plugins")
    return 0


if __name__ == "__main__":
    sys.exit(main())

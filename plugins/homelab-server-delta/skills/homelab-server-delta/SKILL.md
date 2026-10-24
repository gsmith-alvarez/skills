---
name: homelab-server-delta
description: Use when implementing the homelab server plan — verified module map, Compose-to-NixOS corrections, open gaps.
category: devops
version: 0.1.1
author: Giovanni (gsmith-alvarez)
license: MIT
metadata:
  hermes:
    tags: [nixos, homelab, server, zfs, modules, caddy, gluetun]
    related_skills: [nixos, nixos-configuration, agent-skill-adoption]
---

# Homelab server — delta notes

The design document (supplied separately) is the source of **intent**: stack list, dataset layout, validation ladder, privilege model, secrets boundary, hot-swap workflow. This file deliberately does **not** restate any of it. It carries only what that document does not: which parts of it are Docker/Compose-shaped and do not survive contact with nixpkgs, which options actually exist in the pinned nixpkgs, two design points that no tool implements, and the commands to re-derive all of it so these notes cannot rot.

**Rule of use:** the plan wins on intent, this file wins on mechanism. When they disagree, say so and cite both — do not silently pick one.

Status: v0.1.1, checked against the nixpkgs rev pinned in `~/dotfiles` (see §1) and then independently audited against the same tree — that second pass corrected six factual errors (OMP *is* packaged as `pkgs.omp`, `withPlugins` hash semantics, `oci-containers` rootless support, Nextcloud's locking option, the servarr satellite paths, and `overseerr` being removed rather than renamed). Anything marked **SPIKE** is unverified by construction; do not present it as settled.

## 1. Re-derive before trusting any table here

```bash
NP=$(nix eval --raw --impure --expr '(builtins.getFlake "/home/giovanni/dotfiles").inputs.nixpkgs.outPath')

# 1. does a module exist at all?
grep -rl "services\.<name>" "$NP/nixos/modules" --include=*.nix

# 2. what is the exact option name? (differs from the service name more often than expected)
grep -nE "services\.[a-zA-Z-]+ = \{" <matched-file>
```

**False-negative trap (already produced a wrong answer once):** grepping `options.services.<name>` misses every module that declares its options inside a plain `options = { ... }` block. `audiobookshelf`, `calibre-web` and `homepage-dashboard` were all wrongly reported as having no module because of that pattern — they all have one. Grep `services.<name>`, then read the real option name out of the file.

A `services.<x>` hit in only one file can also be a rename shim: check `modules/rename.nix` before treating the name as current.

## 2. Verified module map

| Plan component | NixOS option | Module path under `nixos/modules/` | Delta |
|---|---|---|---|
| Seerr | `services.seerr` | `services/misc/seerr.nix` | `services.overseerr` is a `mkRemovedOptionModule` error stub in `rename.nix`, **not** a rename — there is no value migration, an old config has to be rewritten by hand. (Overseerr + Jellyseerr merged into Seerr) |
| Radarr / Sonarr / Prowlarr | `services.radarr`, `services.sonarr`, `services.prowlarr` | `services/misc/servarr/` | That directory also holds `lidarr`, `readarr`, `whisparr` and the shared `settings-options.nix`. `bazarr`, `tdarr/`, `recyclarr`, `nzbget`, `nzbhydra2` sit beside it in `services/misc/`, **not** inside `servarr/`. Quality profiles are app JSON, not Nix |
| qBittorrent | `services.qbittorrent` | `services/torrent/qbittorrent.nix` | Notable options `profileDir`, `webuiPort`, `torrentingPort`, `serverConfig`, `extraArgs`, plus `enable`, `package`, `user`, `group`, `openFirewall`. **No network-namespace option** — see §3.1 |
| Gluetun | — | — | No module anywhere in nixpkgs. Container only |
| Plex | `services.plex` | `services/misc/plex.nix` | |
| Audiobookshelf | `services.audiobookshelf` | `services/web-apps/audiobookshelf.nix` | `dataDir`, `host` (defaults `127.0.0.1`) |
| Calibre-Web | `services.calibre-web` | `services/web-apps/calibre-web.nix` | Distinct from `services.calibre-server`; do not confuse them |
| Vaultwarden | `services.vaultwarden` | `services/security/vaultwarden/default.nix` | |
| Nextcloud | `services.nextcloud` (+ `services.redis.servers.<name>`) | `services/web-apps/nextcloud.nix` | Locking **is** a Nextcloud option: `services.nextcloud.caching.redis` (or `configureRedis`) writes `memcache.locking`. `services.redis.servers.<name>` only declares the server |
| Syncthing | `services.syncthing` | `services/networking/syncthing.nix` | One `settings` submodule for the service user — there is no `services.syncthing.users.*` attrset |
| Immich | `services.immich` | `services/web-apps/immich.nix` | Has `mediaLocation`, `secretsFile`, `settings`, `database.createDB`, `redis.enable`, `accelerationDevices` — see §3.2 |
| SearXNG | `services.searx` | `services/networking/searx.nix` | |
| Caddy | `services.caddy` | `services/web-servers/caddy/default.nix` | `package`, `configFile`, `globalConfig`, `virtualHosts`, `dataDir`, `environmentFile` — see §4 |
| Prometheus / Grafana | `services.prometheus`, `services.grafana` | `services/monitoring/` | Exporters `services.prometheus.exporters.{smartctl,zfs,zfs-siebenmann}` all exist — the plan's smartd/`smartctl_exporter` and pool-health rules can be native |
| Homepage | `services.homepage-dashboard` | `services/misc/homepage-dashboard.nix` | **Not** `services.homepage` |
| Forgejo | `services.forgejo` | `services/misc/forgejo.nix` | |
| act_runner | `services.forgejo-runner` | `services/continuous-integration/forgejo-runner.nix` | `instances.<name>` attrset; `gitea-actions-runner.nix` is the legacy path |
| GitHub runners | `services.github-runners` (plural) | `services/continuous-integration/github-runners.nix` | The singular `services.github-runner` is a `mkRemovedOptionModule` that tells you to use the plural — the plan already has this right |
| ZFS | `boot.zfs.extraPools`, `boot.zfs.devNodes`; `services.zfs.{autoSnapshot,autoScrub,trim,expandOnBoot,zed}` | `tasks/filesystems/zfs.nix` | See §5 |
| Containers | `virtualisation.oci-containers` | `virtualisation/oci-containers.nix` | Root by default, but rootless **is** supported on the podman backend (`backend = "podman"` plus per-container `podman.user`) |
| Tailscale | `services.tailscale` | `services/networking/tailscale.nix` | Prerequisite for §4. Its `tailscaled-autoconnect.service` is the ordering hook for anything binding a tailnet IP |
| smartd | `services.smartd` | `services/monitoring/smartd.nix` | The plan's SMART schedule lives here; the `smartctl` **exporter** is a separate option |
| Zellij | — (user package) | — | Sessions are per-UID; two Unix accounts cannot attach to one (runtime behaviour, not a nixpkgs fact) |
| Hermes / OMP | `pkgs.omp` is in this pin | `pkgs/by-name/om/omp/` | OMP **is** packaged (`pname = "omp"`, homepage omp.sh), so the `llm-agents` input is a pinning choice, not a necessity. Hermes is not in nixpkgs and only comes from `llm-agents` |
| nexcanvas | — (container) | — | No module |

## 3. Compose language that does not survive NixOS

### 3.1 Gluetun network namespace — the biggest silent rewrite

`--network=container:gluetun` is a Docker flag. `services.qbittorrent` has no namespace option, so a *native* qBittorrent unit cannot be pointed at a container's netns declaratively. Two shapes, both **SPIKE**:

- **(a) both as containers.** qBittorrent and Gluetun as `virtualisation.oci-containers`, preserving Compose semantics. Cost: loses the native module's user/group/profileDir handling, and `oci-containers` is not rootless.
- **(b) native service, shared netns via systemd.** Something creates `/run/netns/<name>` (gluetun, or `ip netns add`), then `qbittorrent.service` gets `JoinsNamespaceOf=` (a `[Unit]` directive, so `systemd.services.qbittorrent.unitConfig`) and `PrivateNetwork=true` + `NetworkNamespacePath=` (`serviceConfig`). **The module hardcodes `PrivateNetwork = false` and `RestrictNamespaces = true` as plain assignments, so this shape needs `lib.mkForce` on both** — otherwise you get a conflicting-definition error. Whether the module's remaining hardening (`PrivateUsers`, empty `CapabilityBoundingSet`, `SystemCallFilter`) still permits a joined netns is the unresolved part.

Failure modes to test in either shape, in this order: qBittorrent starting before the netns exists (ordering); qBittorrent surviving a Gluetun restart with a dead tunnel; and whether the "firewall drops non-tunnel egress" claim actually holds — verify from inside the namespace, not from the host.

### 3.2 Immich — do not reach for OCI on version grounds by reflex

The module exposes the database and redis as sub-options, so the plan's "dedicated data path under `tank/appdata`" is `mediaLocation` plus the database directory, not a container volume. Before choosing the OCI route, compare `services.immich.package`'s version (evaluate it, don't assume) against what upstream requires for the schema you have; "the module doesn't track the version we need" is only true after that check.

## 4. Caddy and `*.ts.net` certificates

Plain Caddy cannot issue Tailscale certificates. Two mechanisms, and the plan's snippet assumes the second without noting the packaging work:

- **File-based.** `tailscale cert <host>.<tailnet>.ts.net` writes cert+key; serve them with `tls <cert> <key>`, refreshed by a timer. Fewer moving parts, two paths to keep alive.
- **Plugin.** The Caddyfile form `tls { get_certificate tailscale }` needs Caddy built with `github.com/tailscale/caddy-tailscale`. There is **no `caddy-tailscale` package in nixpkgs**; the lever is
  ```nix
  services.caddy.package = pkgs.caddy.withPlugins {
    plugins = [ "github.com/tailscale/caddy-tailscale@<tag-or-pseudo-version>" ];
    hash = "";   # fakeHash default: the first build reports the required hash
  };
  ```
  Plugins must carry a real tag, commit sha or pseudo-version (`@` is mandatory). `hash` is the sha256 `outputHash` of the plugin-fetch FOD; the sorted plugin list only seeds the derivation *name* (an md5), so reordering is normalised away and changes nothing, while adding, removing or version-bumping a plugin does invalidate `hash`.

**SPIKE:** whichever mechanism, confirm Caddy's service user can reach the tailscaled socket. Caddy runs as `User = cfg.user` (default `caddy`), not root, with `NoNewPrivileges` and `PrivateDevices`, and the module exposes **no** `SupplementaryGroups` option; `services.tailscale` never mentions a socket path or group at all. So nixpkgs offers no supported path here — you add `systemd.services.caddy.serviceConfig.SupplementaryGroups` yourself and confirm the socket's group at runtime. Test as the unit's user, not as your login shell.

## 5. Snapshot-before-migration — nothing implements it

Facts, verified, so this is not re-litigated:

- `services.zfs.autoSnapshot` is the OpenSolaris `zfs-auto-snapshot`: opt-in **per dataset** via `com.sun:auto-snapshot=true`, interval-based (frequent/hourly/daily/weekly/monthly), pruned by keep-count. Time-anchored, never change-anchored.
- `services.zfs.zed` exposes `enableMail` and `settings` (rendered as `zed.rc`). There is no hook-path option — custom sinks go through `zed.rc` variables or your own `zed.d` script. zed fires on pool events, not on planned upgrades.
- `nh` knows generations; the `nix-agent` MCP has no snapshot verb at all (`build/diff/switch/generations/eval_config/locate_option/check`).
- A generation rollback restores the closure. It does not revert a database migration the new closure already ran.

The missing piece is **sequencing**: a recursive snapshot taken between "new closure built" and "unit restarts against it", named for the target generation, covering exactly the datasets the migrating unit writes. Shape: wrap activation (`nsw` → `zfs snapshot -r tank/appdata@pre-<gen>` → `nh os switch`), retain by keep-count rather than time, and record the snapshot name next to the generation diff. An untested snapshot is not a backup: prove one restore (`zfs clone <snap> /tank/tmp/verify`, start the service against it) before you need it in an incident.

## 6. Dataset → service map: derive it, never infer it

§5 is blocked on knowing which unit writes which dataset, and that cannot be read off dataset names. Derive it:

```bash
nix eval --impure --json --expr 'let c = (builtins.getFlake "/home/giovanni/dotfiles").nixosConfigurations.<server>.config;
  in { immich = c.services.immich.mediaLocation; forgejo = c.services.forgejo.stateDir; };'
```

Read each module's default for anything the option does not expose. Until that map exists, any snapshot wrapper is guessing at coverage — this is the one input that needs the host, not research.

## 7. Claims a reviewing model should re-check

Each row is machine-checkable; a claim that fails here is a bug in this file, not in the plan.

| Claim | Command |
|---|---|
| Module map rows | `grep -rl "services\.<name>" $NP/nixos/modules --include=*.nix` |
| Exact option name per row | `grep -nE "services\.[a-zA-Z-]+ = \{" <matched-file>` |
| No Gluetun module exists | `grep -rl "services\.gluetun" $NP/nixos/modules` → no output |
| qBittorrent has no netns option | `grep -nE "^\s{4,10}[a-zA-Z]+ = mk" $NP/nixos/modules/services/torrent/qbittorrent.nix` |
| `caddy.withPlugins` exists, `hash` defaults to `fakeHash` | `grep -n "withPlugins\|fakeHash" $NP/pkgs/by-name/ca/caddy/package.nix $NP/pkgs/by-name/ca/caddy/plugins.nix` |
| No `caddy-tailscale` package in nixpkgs | `grep -rl "caddy-tailscale" $NP/pkgs` → no output |
| ZFS option names | `grep -nE "services\.zfs\.[a-zA-Z]+ = \{" $NP/nixos/modules/tasks/filesystems/zfs.nix` |
| zed exposes only `enableMail` + `settings` | `sed -n '613,690p' $NP/nixos/modules/tasks/filesystems/zfs.nix` |
| `autoSnapshot` is opt-in per dataset | `sed -n '444,470p' $NP/nixos/modules/tasks/filesystems/zfs.nix` |
| Seerr replaced Overseerr | `grep -n "seerr\|overseerr" $NP/nixos/modules/rename.nix` |

## 8. Non-goals — do not duplicate the plan here

The validation ladder, the agent privilege table, the sops/`/run/secrets` boundary, hot-swap by `/dev/disk/by-id/`, and the two-classes-of-rollback argument all live in the design document. Restating them here creates a second copy that drifts. If a mechanism note in this file contradicts the plan, surface the conflict with both citations instead of editing the plan from here.

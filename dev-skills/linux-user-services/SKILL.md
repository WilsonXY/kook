---
name: linux-user-services
description: Run daemons without root via user binaries and units.
version: 0.1.0
author: WilsonXY
license: MIT
platforms: [linux]
metadata:
  tags: [systemd, services, syncthing, no-root, daemons]
---

# Linux User Services

Pattern for installing and running long-lived daemons on the laptop WITHOUT root: official release binary into `~/.local/bin`, config under `~/.local/state/<app>`, a systemd user unit, and REST/local-API configuration. Validated end-to-end with Syncthing v2.1.3 (2026-09-04); generalizes to any single-binary Go/Rust daemon.

## When to Use

- Installing a daemon or background tool when `sudo` needs an interactive password the agent cannot provide
- Making a user-level service start at boot (linger is already enabled on this laptop)
- Configuring a daemon that exposes a localhost REST API

Don't use for: system services that genuinely need root (kernel modules, privileged ports, other users' data).

## Procedure

1. **Get the real latest release URL** — do not guess version numbers (a guessed URL 404s into a non-gzip tarball): resolve `https://github.com/<org>/<repo>/releases/latest` with `curl -sIL -o /dev/null -w '%{url_effective}'`, then derive the asset name from the tag. Completion: `file <download>.tar.gz` says gzip.
2. **Install user-local:** extract, copy the binary to `~/.local/bin/`, verify with `<binary> --version`. Completion: version prints.
3. **Bootstrap config:** many daemons have a generate subcommand (Syncthing: `<binary> generate --home ~/.local/state/<app>`), which creates keys + default config without starting a server. Completion: config dir exists with config/keys.
4. **Write a user unit** at `~/.config/systemd/user/<app>.service` with `ExecStart=%h/.local/bin/<binary> ...`, `Restart=on-failure`, `WantedBy=default.target`; then `systemctl --user daemon-reload && systemctl --user enable --now <app>`. Completion: `systemctl --user is-active <app>` prints `active`.
5. **Configure via REST**, not by editing XML of a running daemon: GET the API key from the config file, verify with a status endpoint (`/rest/system/status`), then POST/PATCH config resources and re-GET to confirm each field. Completion: every changed field re-reads as intended.
6. **End-to-end verify:** confirm the service survives `systemctl --user restart`, and for pair-up apps (sync, peer connections) confirm the remote side shows connected and completion 100%.
7. **Adding a new machine to a synced fleet (e.g. fresh dual-boot OS):** see `references/syncthing-pairing.md` for the REST-driven device-pairing recipe.

## Quick Reference

- Unit template: `ExecStart=%h/.local/bin/<bin> serve --home %h/.local/state/<bin> --no-browser --no-restart`
- `%h` expands to the user's home inside units; `SuccessExitStatus=3 4` tames Syncthing's exit codes
- REST auth header: `X-API-Key: <key from config.xml>`; base `http://127.0.0.1:8384/rest`
- Syncthing folder status: `/rest/db/status?folder=<id>`; per-device progress: `/rest/db/completion?device=<id>&folder=<id>`

## Pitfalls

- **Do not sit at sudo password prompts.** `sudo -n` fails non-interactively; a pty prompt is a dead end — kill it and pivot to the no-root binary route. (If the user is present and prefers apt, ask them to run the sudo command themselves.)
- **Agent shells often reject or kill foreground `&` jobs.** Start servers as detached/background processes (`nohup`, `setsid`, or a systemd unit) and health-check in a separate follow-up command; or use a generate/one-shot subcommand when one exists.
- **After POSTing `/rest/system/restart` on a `--no-restart` unit, the process exits and systemd leaves the unit dead** (the API restart just kills it) — immediately `systemctl --user is-active` and `start` the unit again; until you add `SuccessExitStatus=3 4` to the unit. A 'restarting' ok reply is not proof the daemon is back.
- **Get identity and topology from the REST API, not by hand-deriving.** Device ID = `myID` from `/rest/system/status`; the v2 CLI has no `--device-id` flag and computing the ID from the certificate yourself drifts off-by-one. GUI may lag the service start — if 8384 refuses, restart the unit once and retry.
- **POST to a collection endpoint applies immediately but returns 405** (Syncthing quirk — the write lands); use PATCH on the resource path (`/rest/config/folders/<id>`) for subresource updates like versioning, and never trust the status code alone — re-GET and verify.
- Config-file edits require a service restart to take effect; REST edits on Syncthing v2 apply live without restart.
- Keep daemon GUIs/APIs bound to 127.0.0.1; expose wider only deliberately (e.g. a Tailscale IP) and never with default credentials.
- Check `guiprompt`/first-run dialog settings at bootstrap, or the UI blocks on a prompt nobody can click on a headless host.
- **Never restart a service from inside a process that the service itself owns** (e.g. an agent running under that service): SIGTERM kills the command mid-flight. Launch the restart detached (`systemd-run --user`, or `setsid`/`nohup`) so it survives the parent.

## Verification

- `systemctl --user is-active <app>` → `active`, and `systemctl --user is-enabled <app>` → `enabled`
- Service survives a restart and (for pair-up apps) the remote peer reports connected/complete
- Config re-reads show exactly the intended fields — status codes alone are not proof

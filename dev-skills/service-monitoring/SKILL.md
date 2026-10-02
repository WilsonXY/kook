---
name: service-monitoring
description: Use when setting up downtime alerting for a hosted service.
---

# Service Monitoring

Procedure for making downtime visible to the service owner. Big picture first: there are two opposite architectures —

1. **Inbound poller** (UptimeRobot, Better Stack): an external service knocks on your URL and alerts if the answer looks wrong. Simple, zero server changes, but blocked by any auth wall (login redirect, SSO challenge) — the poller sees the wall, not the app, and cannot tell "down" from "locked out".
2. **Dead-man's switch** (Healthchecks.io, Dead Man's Snitch): the SERVER pings out "I'm alive" on a schedule; the provider alerts when the pings stop. Immune to auth walls (outbound traffic), but requires a cron on the server — it does not monitor anything by itself.

Default to the dead-man's switch for self-hosted services. It is the only pattern that works when the domain sits behind Cloudflare Access, SSO, or any login challenge, and it also catches the server being unreachable from outside (laptop down, tunnel dead) — which is usually the real failure mode.

## Steps

1. **Locate the origin.** Find where the app actually runs and its local port (`ss -tlnp`, systemd unit, process list). Identify the tunnel/wall in front of it (e.g. cloudflared config maps hostname → localhost:PORT). Confirm an external request really hits the wall: `curl -sI https://domain` returning a 302/403 to an auth host proves inbound polling is blocked.
2. **Create the check** (user does the account): free Healthchecks.io account, one check named after the service, schedule = ping period, plus a Discord/email integration. The period should be 2–5× the cron frequency; alert latency = period + grace.
3. **Store the ping URL out of chat and out of repos**: user saves it to a chmod-600 file in $HOME; never paste the raw ping URL into chat, cron config, or the vault (it is a bearer secret — leaking it lets anyone fake liveness).
4. **Install the cron** as the user who owns the service (check `crontab -l` first — coexist with existing entries):
   ```
   */5 * * * * curl -fsS --max-time 10 http://127.0.0.1:PORT/ >/dev/null 2>&1 && curl -fsS --max-time 10 "$(cat $HOME/svc-ping.txt)" >/dev/null 2>&1
   ```
   The `&&` is the whole design: a ping is only sent when the app actually answered. Cron's own schedule does the timing — never build long `sleep N` waits into a single foreground command (agent shells often kill them mid-wait); schedule verification for the next tick instead.
4b. **Prefer a logging wrapper script over the bare one-liner** once noise appears (or from the start): `*/5 * * * * $HOME/svc_ping.sh`. The script does the same two curls (each with `--max-time`), but on failure appends a timestamped line to `~/svc-ping.log` (which step, curl exit code, elapsed time, curl's message), also logs runs slower than ~3 s and runs that START late (seconds ≥ 5 past a 5-min mark), and caps the log (~1000 lines). The one-liner sends everything to /dev/null, so a single missed ping leaves zero evidence. Retry the OUTBOUND provider ping once after ~5 s (log each failed attempt and a RETRY-OK line) — transient network stalls to the provider are the usual cause of single missed pings, and one retry absorbs them without touching the app check. Test by hand (normal run silent/exit 0; wrong port via an env-overridable URL logs FAIL/exit 1), keep the old cron line as `#OLD#` comment, back up `crontab -l` first, then confirm the next scheduled run appears in `journalctl | grep CRON`.
5. **Verify end-to-end — a monitor that has never fired is a hope, not an alarm.** Confirm a manual ping shows green on the provider dashboard, then run a LIVE-FIRE TEST: tell the user, stop the service, stay down past period + grace, confirm the DOWN alert actually arrives (only the user can see this — ask them), restart, confirm UP/green. Skip only with the user's explicit say-so.
6. **Record the setup** in the project's docs (README/ADR/AGENTS.md): what monitors what, where the ping secret lives, alert latency, and the chosen pattern with its one-line rationale (usually "auth wall blocks inbound pollers").

## Pitfalls

- Monitor localhost, not the public URL, from the origin host — the public URL loops back through the auth wall and silently pings "alive" for a login page, or never pings at all.
- If a provider integration is configured but no test alert arrived, do not declare success — the integration may be silent until it fires; only the live-fire test proves the full chain (service → cron → provider → notification channel).
- If a poller MUST be used behind an auth wall instead, the options are: a bypass policy for a single secret health path, or a service-token policy with the two `CF-Access-Client-*` headers on the monitor. Both require an app health endpoint that does a real DB query — prefer adding it as a proper PR, never hand-edit prod.

## Diagnosing flapping DOWN/UP alerts ("down" ~4 min then recovers, app fine)

- Fixed duration is arithmetic, not an outage: with period 5 min + grace 1 min, ONE missed ping means the next arrives 10 min after the last good one; DOWN fires at ~6 min, UP at the next ping → always ≈ 3m58–59s. Each alert = exactly one skipped ping.
- Rule out cron not firing first (read-only): `journalctl --since '5 days ago' | grep 'CRON\[' | grep <marker>`, then check for gaps >6 min and late starts. Full coverage (~288/day) means the failure is inside the job (app check slow/failed, or ping to provider failed), not cron.
- Then suspect host stress (swap full, low free RAM → app answers >10 s) and network blips (`journalctl --user -u cloudflared | grep -i 'no recent network'`). Only the logging wrapper (step 4b) can tell which step failed: `FAIL step=hc-ping curl-exit=28` with the app check passing = network path to the provider; SLOW hc-ping lines (4–5 s) often precede it. Wait for the next real alert, then read the log around its time.
- Fix order: wrapper logging → one retry of the outbound ping → optionally raise grace to ~3 min (alert latency becomes period + grace ≈ 8 min). Grace alone hides the noise but not the cause.
- Wrapper install pitfalls: write the script as a file with your editor/file-write tool (a big heredoc in one shell command can trip approval scanners and time out unattended); a cleanup `pkill -f` pattern matching your own command line kills the tool shell, so read results in a separate call; after any script/grace change, update the documented figures (period/grace/latency appear in several notes).

## Known-good example

Example: self-hosted Next.js app on :5000 behind a Cloudflare tunnel + Access: user-systemd unit for the app, cron above pinging `http://127.0.0.1:5000/`, Healthchecks check at 5 min period + 1 min grace, Discord integration, ping URL in `~/svc-hc-ping.txt` (chmod 600). Verified with a real stop/restart: DOWN alert arrived within the expected window, UP alert and green dashboard after restart.

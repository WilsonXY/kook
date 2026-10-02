# Syncthing: pairing a new device into an existing synced folder

REST-driven, no GUI. Works for fresh OS installs / dual-boot sides. Both sides must be reachable (SSH or Tailscale); the API key lives in the config file of each side.

## Procedure

1. **Get the new device's ID** from its own REST API (`myID` in `/rest/system/status`), not by deriving it from the certificate.
2. **Server side (existing device):**
   - POST the new device to `/rest/config/devices` (deviceID, name, addresses `["dynamic"]`).
   - GET `/rest/config/folders/<id>`, append `{'deviceID': <new-id>, 'introducedBy': '', 'encryptionPassword': ''}` to `devices`, PUT it back to the folder resource path.
   - POST `/rest/system/restart`; **the unit may exit dead — start it again and verify `is-active`**.
3. **New-device side:**
   - POST the existing device to `/rest/config/devices`; use a direct Tailscale address (`tcp://<ts-ip>:22000`) as well as dynamic to speed up first contact.
   - Create the target directory **empty** — pointing Syncthing at a folder that already has files merges and pollutes both sides.
   - POST the folder to `/rest/config/folders` (same folder id, `type: sendreceive`, trashcan versioning 30 days to match the fleet).
   - POST `/rest/system/restart` and re-verify the unit is active.
4. **Verify:** on the new side GET `/rest/db/status?folder=<id>` → `state: idle`, `globalFiles == inSyncFiles`, `needBytes: 0`. Then diff the file lists across machines (`find . -type f | sort` both sides) — expect only `.stversions/` entries to differ (versioning history is per-device by design).
5. **Record it** in the vault project note that owns the sync infrastructure: dated Decisions line + checked status bullet.

## Diagnostics

- Config file `<home>/config.xml` holds the apikey; grep it out per side, never copy between sides.
- First start after `generate` can come up without the GUI listening and with duplicate processes — `systemctl --user restart <svc>` fixes both; check `journalctl --user -u <svc>` for `GUI and API listening`.
- A laptop that suddenly stops answering SSH mid-setup is usually suspending: wait, ping, and reconnect; the service config survives.
# NottAnotherMasterSetTrackerBackend

Backend for [nottdex.org](https://nottdex.org) — a Pokemon TCG master set tracker.

Two Cloudflare Workers:
- **downloader** — query card image metadata from D1
- **uploader** — upload card images to R2 and insert metadata into D1

## Structure

```
downloader/   # GET worker — search cards/sets
uploader/     # POST worker — upload card images
```

## Local Dev

Requires `uv` and `wrangler`.

```bash
cd downloader   # or uploader
uv venv && uv sync
wrangler dev
```

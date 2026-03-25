# uploader

Cloudflare Worker — uploads card images to R2 and inserts metadata into D1.

Uploads two R2 objects per image: full resolution (`{imageKey}`) and 25% resolution (`{imageKey}-low`).

## Dev

```bash
uv venv && uv sync
wrangler dev
```

## Request Format

`POST /` with `multipart/form-data`:

| Field | Type | Description |
|---|---|---|
| `image` | file | PNG image |
| `metadata` | JSON | Card metadata (see schema) |

## Example

```bash
curl -X POST http://localhost:8787 \
  -F "image=@card.png" \
  -F 'metadata={"cardTitle":"Pikachu", ...}'
```

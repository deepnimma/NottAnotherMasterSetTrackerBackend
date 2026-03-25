# downloader

Cloudflare Worker — queries card image metadata from D1.

## Dev

```bash
uv venv && uv sync
wrangler dev
```

## Query Parameters

| Param | Description |
|---|---|
| `q` | Search term (required). Comma-separated for multiple. |
| `set` | If present, searches by set name instead of pokemon. |
| `lang` | Language: `en` (default), `jp`, `cn`. |
| `cameo` | Include cameo appearances. |
| `trainer` | Search by trainer name. |
| `illustrator` | Search by illustrator name. |
| `descending` | Sort newest first. |

## Examples

```bash
# Pokemon search
curl "http://localhost:8787?q=pikachu"
curl "http://localhost:8787?q=pikachu&cameo=1"
curl "http://localhost:8787?q=ken-sugimori&illustrator=1"

# Set search
curl "http://localhost:8787?q=scarlet-violet&set=1"

# Language
curl "http://localhost:8787?q=pikachu&lang=jp"
```

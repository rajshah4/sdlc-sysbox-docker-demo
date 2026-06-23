# Playwright QA Report: Petstore Catalog Search

Status: pass

## Target

- URL: http://localhost:4173
- App: static Petstore web UI

## Browser Scenarios

- [x] Default catalog shows available pets and excludes pending pets
- [x] Species filter narrows results to available dogs
- [x] Name search finds a matching available pet
- [x] Pending pet remains hidden and shows the empty state

## Artifacts

- Screenshot: catalog-search.png
- Video: catalog-search.webm
- GIF preview: catalog-search.gif

## Commands

```bash
python3 skills/sdlc-qa/scripts/with_server.py \
  --server "python3 -m http.server 4173 --directory app/web" \
  --port 4173 \
  -- node app/web/tests/catalog-search.playwright.mjs \
     --url http://localhost:4173 \
     --artifact-dir /tmp/sdlc-petstore-playwright/catalog-search
```

## Notes

- This is the preferred browser-evidence path for UI-visible changes.
- If Playwright is unavailable in a remote automation runtime, fall back to dependency-free checks and say so explicitly.

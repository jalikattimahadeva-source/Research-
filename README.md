# Research Navigator (Vercel-ready)
AI-assisted research guidance platform. BGMIT Mudhol, Dept. of AI & ML.

## Structure
- `public/index.html`  frontend (HTML, CSS, JS)
- `api/index.py`       Flask REST API + in-memory SQLite + TF-IDF/cosine
- `api/data.py`        seed papers, topics, opportunities (edit, then redeploy)
- `vercel.json`        routes /api/* to the Flask function

## Deploy on Vercel
1. Push this folder to a GitHub repo
2. vercel.com -> Add New -> Project -> import the repo -> Deploy (no settings needed)
3. Open the URL Vercel gives you

## Run locally
`npm i -g vercel` then `vercel dev` inside this folder.

## Notes
- Vercel's disk is read-only, so data is seeded from `api/data.py` on each start.
- Opportunities are marked unverified until you check the official sites and set verified to 1.

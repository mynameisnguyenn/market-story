# Setup — running on another computer

Two ways to use market-story on a new machine, and **they stay in sync**.

## Option A — the hosted app (zero setup)

Open the public URL (in `README.md`) in any browser, on any computer or phone. The daily
GitHub Action keeps it fresh. Nothing to install — this is the easiest way to read your
brief from anywhere.

## Option B — run it locally

```bash
git clone https://github.com/mynameisnguyenn/market-story
cd market-story
python bootstrap.py          # installs deps + creates .env from the template
#   -> edit .env and paste your free keys (FRED, EIA — see the comments in the file)
python run.py                # build today's brief
python -m streamlit run app.py
#   then, in `claude` in this folder:  "narrate today's brief"
```

(On Windows with Anaconda, use the full interpreter path if `python` isn't the right one,
e.g. `C:\Users\<you>\anaconda3\python.exe`.)

## What syncs across machines — and what doesn't

| | Syncs via `git pull` / `push`? | Notes |
|---|---|---|
| All code | ✅ | the app itself |
| `data/briefs/` | ✅ | committed by the daily Action |
| `data/narratives/` | ✅ | your written logbook |
| `data/timeline.jsonl` | ✅ | the 3-year metrics history |
| `.env` (your keys) | ❌ gitignored | recreate from `.env.example`, or copy the 4 lines between your own machines |
| `data/history.db` | ❌ gitignored | a local cache; regenerable, and the timeline supersedes it |

So on a second computer: **clone → drop in your `.env` → done.** You get the same app and
the same accrued history (briefs, narratives, the metrics timeline) everywhere.

## Keys

All free, all optional — the dashboard degrades gracefully without them, but the energy
(EIA) and positioning panels need their fetchers to succeed. `.env.example` has a link to
where you get each. The **hosted** app reads the same keys from Streamlit Cloud secrets
(Settings → Secrets); **locally** they live in `.env`. See `DEPLOY.md` for hosting your own.

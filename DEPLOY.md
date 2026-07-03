# Running market-story on your laptop AND your phone

The read surface is a **framework-free static site**. Two ways to open it:

| Mode | How | Good for |
|---|---|---|
| **GitHub Pages** ★ | <https://mynameisnguyenn.github.io/market-story/> → install as an app | The morning read, anywhere — no login, no server, works offline |
| **Local build** | `python build_site.py` → open `site/index.html` | The dev loop: rebuild from the newest brief, tweak `src/site/`, preview offline |

The **daily email digest** is the push counterpart to the site — the day's read lands in
your inbox once the brief + narrative pair is committed. Setup lives in `SETUP.md`.

## The static site — GitHub Pages

The data changes once a day, so the read surface is a static build (`src/site/`, emitted by
`build_site.py`). `.github/workflows/pages.yml` runs the test suite as a deploy gate, then
builds and deploys the site to GitHub Pages on every push to `main` (including the daily
brief commit) — keyless, networkless, built from committed data only.

**One-time setup:** repo **Settings → Pages → Source = GitHub Actions**. After the next push, the
public URL appears there. Open it on any device and install it (laptop: the **Install** icon in the
address bar; iPhone: **Share → Add to Home Screen**) — it runs as an app with its own window/icon and,
thanks to the service worker, opens **offline** with the last build.

The live data, charts, sector map, headlines, and history archives all work hosted —
rendered from the committed briefs and `data/history/*.jsonl` archives at build time.
The narrative is written by Claude (locally on demand, or by the scheduled weekday
routine that commits it — see "Narration on a hosted site"), so a hosted device always
shows the latest committed story.

> **One app, every device.** Once it's hosted, you don't package anything per-device.
> You *install the web app* on each: on a laptop, Edge/Chrome shows an **Install** icon
> in the address bar → its own window + Start-menu/Desktop icon, no browser chrome. On
> an **iPhone**, Safari → **Share → Add to Home Screen** → a tappable full-screen icon.
> Both run the same hosted URL. (A native `.exe`/pywebview wrapper would be laptop-only
> and can't reach the phone — this is the better path.)

## Local build (the dev loop)

```bash
python build_site.py            # committed brief -> site/ (no network, no keys)
python -m http.server -d site   # serve locally — service workers need an http origin
```

Opening `site/index.html` directly as a file also works for a quick look (the PWA/offline
bits just stay inert without an http origin).

## Decommissioned: the Streamlit layer (2026-07-02)

The Streamlit dashboard (`app.py`), its hosted Streamlit Community Cloud deployment, and
the Hugging Face option were removed on 2026-07-02 — the static site is the only
interactive surface now. **One manual step remains: delete the old Streamlit Cloud
deployment at <https://share.streamlit.io>** (the code it served is gone from `main`).

Capability drops recorded honestly (intentional, no static replacement):

- **Learn the Markets page** — deleted with `src/learn.py`; no static equivalent.
- **Client-side headline search** (`filter_headlines`) — pure but had zero call sites in
  the static site; deleted.
- **Live-fetch Calendar panels** (earnings / SEC filings / 13F / econ calendar) — needed
  runtime network calls; out of scope for the static, offline-safe build.
- **Live refresh + interactive pickers** (the local Streamlit "workshop": refresh-data
  button, date pickers, series selects, watchlist editor) — the static site uses fixed
  lookbacks and stacked history sections instead.
- **The Streamlit-Cloud secrets bridge** (`_load_cloud_secrets`) — deleted with `app.py`;
  keys now live in `.env` locally and as GitHub repo secrets for the Actions.

Tested versions (for reproducibility if a dependency breaks): `yfinance 1.2`,
`pandas 3.0`, `plotly 6.5`, `feedparser 6.0`, `fredapi 0.5`.

---

## Narration on a hosted site

Because synthesis runs **through Claude Code on your machine**, a hosted site can't call
Claude. The "Story" tab handles this gracefully: with no narrative file it shows the raw
**facts brief**. To show the *written* narrative on the hosted site, pick one:

- **Commit the narrative (simplest).** After you ask Claude to narrate locally, commit
  that one file and push — the Pages workflow rebuilds and redeploys the site:
  ```bash
  git add data/narratives/narrative_<date>.md
  git commit -m "Add narrative <date>" && git push
  ```
- **Keep narration local.** Use the hosted site for data/charts/news on the go, and
  read the AI narrative on your PC. Lowest friction, no git per day.

**Scheduled pre-market run (built in).** `.github/workflows/daily-brief.yml` runs `python run.py`
every weekday at 12:00 UTC (and on demand from the **Actions** tab), then commits the fresh
brief — so a current brief is waiting each morning and the hosted site stays up to date.

Prefer it running on your own PC instead? Register a local task (PowerShell):
```powershell
$py  = "$env:USERPROFILE\anaconda3\python.exe"
$act = New-ScheduledTaskAction -Execute $py -Argument 'run.py' -WorkingDirectory "$env:USERPROFILE\market-story"
$trg = New-ScheduledTaskTrigger -Daily -At 7:30am
Register-ScheduledTask -TaskName 'Market Story brief' -Action $act -Trigger $trg
```

---

## Note on the home folder being a git repo

Your `C:\Users\nguye` is itself a git repo. Running `git init` inside the project creates a
**separate, nested** repo for just this project — clean and independent. I left git
untouched; nothing has been committed or pushed.

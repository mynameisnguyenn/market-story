# Running market-story on your laptop AND your phone

Two complementary ways to use this dashboard — use both:

| Mode | How | Good for |
|---|---|---|
| **Local (the workshop)** | Double-click **Market Story** on your Desktop (or `Launch Market Story.vbs`) | Refreshing data, running `/narrate` on demand, working **offline** |
| **Hosted (the read, on every device)** | Streamlit Community Cloud → **install as an app** on laptop + iPhone (below) | The morning read, anywhere — laptop, phone, tablet |

The **live data, charts, sector map, headlines, history archives, and the Learn page all
work hosted** — fetched at runtime or read from the committed `data/history/*.jsonl`
archives. The narrative is written by Claude (locally on demand, or by the scheduled
weekday routine that commits it — see "Narration on a hosted site"), so a hosted device
always shows the latest committed story.

> **One app, every device.** Once it's hosted (Option A), you don't package anything
> per-device. You *install the web app* on each: on a laptop, Edge/Chrome shows an
> **Install** icon in the address bar → its own window + Start-menu/Desktop icon, no
> browser chrome. On an **iPhone**, Safari → **Share → Add to Home Screen** → a tappable
> full-screen icon. Both run the same hosted URL. (A native `.exe`/pywebview wrapper would
> be laptop-only and can't reach the phone — this is the better path.)

---

## Option A — Streamlit Community Cloud (free, easiest)

Gives you a URL like `https://market-story.streamlit.app`.

1. **The project is already on GitHub** at `https://github.com/mynameisnguyenn/market-story`
   (repo: `C:\Users\Nguyen\market-story-git`), and the daily Action commits a fresh brief +
   narrative + history archives each weekday — so a hosted app stays current with no manual
   push. `.gitignore` excludes `.env` and live `data/briefs/`, so no secrets ship.

2. **Deploy (once).** Go to <https://share.streamlit.io> → *New app* → pick
   `mynameisnguyenn/market-story`, branch `main`, main file `app.py`. Under *Advanced
   settings* set **Python 3.12**. You get a URL like `https://<name>.streamlit.app` — that
   single URL is what you open (and install) on the laptop and the iPhone.

3. **(Optional) Secrets for full live refresh.** In *Settings → Secrets*, add any of:
   ```toml
   FRED_API_KEY = "your_key"
   EIA_API_KEY  = "your_key"
   SEC_USER_AGENT = "you you@email.com"
   ```
   None are strictly required: macro falls back to the keyless FRED CSV, and **energy now
   reads the committed `data/history/energy.jsonl` archive** (today's fix — the panel can't
   blank without a live key). `app.py`'s `_load_cloud_secrets` bridges these into the env.

## Install it as an app (do this on each device)

Once you have the `.streamlit.app` URL:

- **Laptop (Edge or Chrome).** Open the URL → click the **Install** icon at the right of
  the address bar (or ⋮ menu → *Apps → Install this site as an app*). You get a standalone
  window with its own taskbar/Start icon and no browser chrome.
- **iPhone (Safari).** Open the URL → tap **Share** (the square-with-arrow) → **Add to Home
  Screen** → *Add*. A tappable Market Story icon lands on your home screen and opens
  full-screen. (Needs internet — a hosted page has no offline mode; that's what the local
  app is for.)

Tested versions (for reproducibility if a dependency breaks): `streamlit 1.58`,
`yfinance 1.2`, `pandas 3.0`, `plotly 6.5`, `feedparser 6.0`, `fredapi 0.5`.

## Option B — Hugging Face Spaces (also free, no GitHub strictly needed)

Create a **Streamlit Space**, upload the project files (or push via the Space's git),
and it serves a public URL. Same `requirements.txt`/`app.py` entry point.

---

## Narration on a hosted site

Because synthesis runs **through Claude Code on your machine**, a hosted site can't call
Claude. The "Story" tab handles this gracefully: with no narrative file it shows the raw
**facts brief**. To show the *written* narrative on the hosted site, pick one:

- **Commit the narrative (simplest).** After you ask Claude to narrate locally, allow that
  one file into git and push — Streamlit Cloud auto-redeploys:
  ```bash
  git add -f data/narratives/narrative_<date>.md
  git commit -m "Add narrative <date>" && git push
  ```
  (The `-f` overrides the `data/` ignore for just that file.)
- **Keep narration local.** Use the hosted site for live data/charts/news on the go, and
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

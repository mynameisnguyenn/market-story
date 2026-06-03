# Deploying market-story as a public website

You have two ways to use this dashboard:

| Mode | How | AI narrative |
|---|---|---|
| **Local (now)** | Double-click **Market Story** on your Desktop | ✅ Full — Claude writes it locally |
| **Hosted (anywhere/phone)** | Streamlit Community Cloud (below) | ⚠️ See "Narration on a hosted site" |

The **live data, charts, sector map, headlines, and the Learn page all work hosted** —
they're fetched/bundled at runtime. The only nuance is the AI narrative, which is
written locally by Claude.

---

## Option A — Streamlit Community Cloud (free, easiest)

Gives you a URL like `https://market-story.streamlit.app`.

1. **Put the project on GitHub.** From the project folder:
   ```bash
   cd "C:\Users\nguye\Python Projects\market-story"
   git init
   git add .
   git commit -m "Initial market-story dashboard"
   ```
   Create a repo on github.com (private is fine — Streamlit Cloud can read private repos)
   and push:
   ```bash
   git remote add origin https://github.com/<you>/market-story.git
   git branch -M main
   git push -u origin main
   ```
   > `.gitignore` already excludes `data/`, `.env`, and caches, so nothing sensitive ships.
   > **I have NOT run any of this** — publishing is your call. Tell me and I'll do it with you.

2. **Deploy.** Go to <https://share.streamlit.io> → *New app* → pick your repo, branch
   `main`, main file `app.py`. Under *Advanced settings* set **Python 3.13**.

3. **(Optional) FRED key.** In the app's *Settings → Secrets*, add:
   ```toml
   FRED_API_KEY = "your_key"
   ```
   Not required — the keyless CSV path works without it.

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

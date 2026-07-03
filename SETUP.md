# Setup — running on another computer

Two ways to use market-story on a new machine, and **they stay in sync**.

## Option A — the static site (no server, no login) ★ recommended

The daily data only changes once a day, so the read surface is a **framework-free static
site** — plain HTML, no server, no framework runtime. Three ways to open it:

- **GitHub Pages (any device):** the `pages.yml` Action builds and deploys it on every push.
  One-time setup: repo **Settings → Pages → Source = GitHub Actions**; the URL then shows there.
  Open it on your phone and **Add to Home Screen** — it installs as an app (icon, own window,
  works offline).
- **Locally, no build:** open `site/index.html` in any browser.
- **Rebuild from the latest brief:** `python build_site.py` → writes `site/`. (Runs offline from
  committed data — no keys, no network.)

The static site is the only app surface — the Streamlit dashboard was decommissioned
2026-07-02. The dev/narrate loop is Option B below.

## Option B — run it locally

```bash
git clone https://github.com/mynameisnguyenn/market-story
cd market-story
python bootstrap.py          # installs deps + creates .env from the template
#   -> edit .env and paste your free keys (FRED, EIA — see the comments in the file)
python run.py                # build today's brief
python build_site.py         # render the static site -> open site/index.html
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

All free, all optional — the pipeline degrades gracefully without them, but the energy
(EIA) and positioning panels need their fetchers to succeed. `.env.example` has a link to
where you get each. **Locally** the keys live in `.env` only (see `.env.example`);
**GitHub Actions** reads the same keys from repo secrets (see
`.github/workflows/daily-brief.yml`). See `DEPLOY.md` for hosting your own.

## Daily email digest (optional, free)

The `send-digest.yml` Action emails the daily read (the call, watch grades, KPI tape,
stretched readings, watch triggers) to your inbox once the day's brief + narrative pair is
committed. Transport is the **Resend sandbox** — deliberately chosen so **no email-account
credential exists anywhere**: the sandbox sender (`onboarding@resend.dev`) can only deliver
to the Resend account owner's own verified address, so even a leaked API key can do nothing
but email you (≤100/day; this sends 1). Setup, ~3 minutes:

1. Sign up free at <https://resend.com> **using the email address you want the digest
   delivered to** (that's the only address the sandbox can reach). No domain, no card.
2. In the Resend dashboard: **API Keys → Create API key** (sending-only is enough).
3. Add two GitHub secrets (repo → Settings → Secrets and variables → Actions):
   `RESEND_API_KEY` = the key, `MAIL_TO` = the email you signed up with.
4. Done. Missing secrets → the step silently no-ops. The workflow only sends when the
   newest brief and narrative carry the same date (the brief's cron delay means the pair
   completes on the second push of the day), and `data/emails/.last_sent` guarantees at
   most one email per day. First send may land in Updates/Promotions — mark it "not spam"
   once. To revoke everything: delete the API key in Resend; to rotate: create a new key
   and update the secret.

## Phone alerts (optional, free)

The daily Action can push a phone notification when the VIX alert fires (level ≥ 25 **and**
≥ 80th percentile of its 1-year range — deliberately rare; it's the one signal the 28-year
validation study found a real edge behind). Setup, ~2 minutes:

1. Install the **ntfy** app (iOS/Android) and subscribe to a topic with a long random name
   you invent, e.g. `ms-alerts-<20 random characters>` — treat the name like a password:
   **the topic name is the only authentication ntfy has.**
2. Add it as a GitHub secret: repo → Settings → Secrets and variables → Actions →
   `NTFY_TOPIC` = your topic name.
3. Done. No secret → the step silently no-ops. The topic name is never printed in logs.

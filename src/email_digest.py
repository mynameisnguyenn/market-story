"""Render the daily brief as a sendable HTML email digest — email-safe, in-brand.

Pure rendering: takes the brief dict (+ the latest narrative, if any) and returns email-safe
HTML (table layout, inline styles) mirroring the market-story-design email kit — warm
near-black, cyan accent, serif "read" over mono data. No network and no sending: it produces
the HTML so it can be saved, previewed, or handed to any mailer (or committed for a hosted
"latest digest" page). Run `python -m src.email_digest` to write today's digest.
"""
from __future__ import annotations

import html as _html
import json
import re

from . import brief as brief_mod, config, formatting, signals

# Brand tokens (mirror styles.css :root and the design skill's colors_and_type.css).
_BG, _CARD, _BORDER, _GRID = "#0a0908", "#16120f", "#2b2620", "#241f1a"
_TEXT, _DIM, _ACCENT = "#f5f2ef", "#b3aaa0", "#7beafb"
_TONE = {"up": "#36c26f", "down": "#ff5c6c", "warn": "#f5a623", "neutral": _DIM}

# The KPI tape — three headline instruments (kept to 3 so it reflows cleanly on phones).
_KPIS = [("^GSPC", "S&P 500"), ("CL=F", "WTI crude"), ("GC=F", "Gold")]
EMAILS_DIR = config.DATA_DIR / "emails"
APP_URL = "https://github.com/mynameisnguyenn/market-story"   # CTA target (swap for the hosted app URL)


def _esc(value) -> str:
    return _html.escape(str(value))


def _narrative_text():
    path = brief_mod.latest_narrative_path()
    if not path or not path.exists():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


def _thesis(brief: dict) -> str:
    """The narrative's one-line thesis if present, else the derived lead (never blank)."""
    txt = _narrative_text()
    if txt:
        lines = txt.splitlines()
        for i, ln in enumerate(lines):
            low = ln.strip().lower()
            if low.startswith("##") and ("one line" in low or "thesis" in low):
                for body in lines[i + 1:]:
                    t = body.strip()
                    if t and not t.startswith("#"):
                        return t.lstrip("*->•_ ").strip()
                break
    lead = signals.derive_lead(brief)
    return lead["text"] if lead else "No thesis yet — run /narrate to write today's read."


def _watch_items(limit: int = 4) -> list[tuple[str, str]]:
    """(label, trigger) pairs parsed from the narrative's ```watch fenced block, if any."""
    txt = _narrative_text()
    if not txt:
        return []
    m = re.search(r"```watch\s*(.*?)```", txt, re.DOTALL)
    if not m:
        return []
    out = []
    for line in m.group(1).splitlines():
        line = line.strip().rstrip(",").lstrip("-*• ").strip()
        if not line or line in ("[", "]"):
            continue
        if line.startswith("{"):                       # the scorecard format: one JSON object/line
            try:
                obj = json.loads(line)
                label = obj.get("claim") or obj.get("label") or obj.get("text") or ""
                trig = obj.get("trigger") or obj.get("metric") or ""
                if label:
                    out.append((str(label).strip(), str(trig).strip()))
                    continue
            except Exception:
                pass
        for sep in ("|", "->", "→"):                    # fallback: "label <sep> trigger"
            if sep in line:
                label, trig = line.split(sep, 1)
                out.append((label.strip(), trig.strip()))
                break
        else:
            out.append((line, ""))
    return out[:limit]


def _kpi_cell(brief: dict, sym: str, name: str) -> str:
    row = signals._row(brief, sym)
    last = row.get("last") if row else None
    ch = row.get("change_pct") if row else None
    val = formatting.fmt_num(last) if last is not None else "n/a"
    if ch is None:
        delta, color = "", _DIM
    else:
        delta, color = formatting.fmt_pct(ch), (_TONE["up"] if ch > 0 else _TONE["down"] if ch < 0 else _DIM)
    return (
        f'<td class="kpi" width="33.3%" style="padding:8px;">'
        f'<div style="border:1px solid {_BORDER};border-left:3px solid {_ACCENT};border-radius:8px;padding:10px 12px;">'
        f'<div style="font-family:\'Hanken Grotesk\',Arial,sans-serif;font-size:10px;letter-spacing:.09em;'
        f'text-transform:uppercase;color:{_DIM};">{_esc(name)}</div>'
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:17px;color:{_TEXT};padding-top:3px;">{_esc(val)}</div>'
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:12px;color:{color};padding-top:2px;">{_esc(delta)}</div>'
        f'</div></td>'
    )


def _signal_rows(brief: dict, limit: int = 3) -> str:
    rows = []
    for s in signals.derive_signals(brief)[:limit]:
        color = _TONE.get(s.get("tone"), _DIM)
        rows.append(
            f'<tr><td style="padding:5px 0;color:{color};width:18px;vertical-align:top;">●</td>'
            f'<td style="padding:5px 0;">{_esc(s["text"])}</td></tr>'
        )
    return "\n".join(rows)


def _watch_rows() -> str:
    items = _watch_items()
    if not items:
        return ('<tr><td style="padding:11px 0;font-family:\'Hanken Grotesk\',Arial,sans-serif;color:%s;">'
                'No watch triggers yet — they appear once a narrative sets them.</td></tr>' % _DIM)
    rows = []
    for i, (label, trig) in enumerate(items):
        border = "" if i == len(items) - 1 else f"border-bottom:1px solid {_GRID};"
        rows.append(
            f'<tr><td style="padding:11px 0;{border}font-family:\'Hanken Grotesk\',Arial,sans-serif;color:{_TEXT};">'
            f'{_esc(label)}<br><span style="font-family:\'JetBrains Mono\',monospace;font-size:11px;color:{_DIM};">'
            f'grades next session</span></td>'
            f'<td align="right" style="padding:11px 0;{border}font-family:\'JetBrains Mono\',monospace;'
            f'font-size:11px;color:{_ACCENT};">{_esc(trig)}</td></tr>'
        )
    return "\n".join(rows)


def render_email(brief: dict) -> str:
    """Email-safe HTML digest of `brief` (+ the latest narrative). Pure; never raises on bad data."""
    thesis = _thesis(brief)
    when = f'{brief.get("date", "")} · {brief.get("session_label", "")}'.strip(" ·")
    kpis = "".join(_kpi_cell(brief, sym, name) for sym, name in _KPIS)
    pre = (thesis[:140] + "…") if len(thesis) > 140 else thesis
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="color-scheme" content="dark"/><title>Market Story — Daily Brief</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500&family=Hanken+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"/>
<style>body{{margin:0;padding:0;background:{_BG};}}a{{color:{_ACCENT};text-decoration:none;}}
@media (max-width:620px){{.container{{width:100%!important;}}.px{{padding-left:22px!important;padding-right:22px!important;}}.kpi{{display:block!important;width:100%!important;}}}}</style></head>
<body style="margin:0;padding:0;background:{_BG};font-family:'Hanken Grotesk',Arial,sans-serif;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:{_BG};">{_esc(pre)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{_BG};">
<tr><td align="center" style="padding:30px 14px;">
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:600px;background:{_CARD};border:1px solid {_BORDER};border-radius:14px;overflow:hidden;">
<tr><td class="px" style="padding:26px 34px 18px;border-bottom:1px solid {_BORDER};">
<table role="presentation" width="100%"><tr>
<td style="font-family:'Hanken Grotesk',Arial,sans-serif;font-weight:700;font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:{_TEXT};">Market Story<span style="color:{_ACCENT};">&#174;</span></td>
<td align="right" style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.06em;color:{_DIM};">{_esc(when)}</td>
</tr></table></td></tr>
<tr><td class="px" style="padding:28px 34px 8px;">
<div style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:{_ACCENT};margin-bottom:12px;">&#9679; Today's thesis</div>
<div style="font-family:'Newsreader',Georgia,serif;font-size:25px;line-height:1.32;color:{_TEXT};">{_esc(thesis)}</div>
</td></tr>
<tr><td class="px" style="padding:22px 30px 10px;"><table role="presentation" width="100%"><tr>{kpis}</tr></table></td></tr>
<tr><td class="px" style="padding:14px 34px 6px;">
<div style="font-family:'Hanken Grotesk',Arial,sans-serif;font-weight:600;font-size:13px;color:{_TEXT};padding-bottom:8px;">&#9889; Today's signal</div>
<table role="presentation" width="100%" style="font-family:'Hanken Grotesk',Arial,sans-serif;font-size:14px;color:{_TEXT};line-height:1.5;">{_signal_rows(brief)}</table></td></tr>
<tr><td class="px" style="padding:16px 34px 8px;">
<div style="border:1px solid {_BORDER};border-radius:10px;padding:4px 16px;">
<table role="presentation" width="100%" style="font-size:13px;">{_watch_rows()}</table></div></td></tr>
<tr><td class="px" align="center" style="padding:22px 34px 8px;">
<table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="border-radius:9px;background:{_ACCENT};">
<a href="{APP_URL}" style="display:inline-block;font-family:'Hanken Grotesk',Arial,sans-serif;font-weight:700;font-size:14px;color:#0d0c0c;padding:13px 26px;">Open the full brief &#8594;</a>
</td></tr></table></td></tr>
<tr><td class="px" style="padding:22px 34px 26px;border-top:1px solid {_BORDER};">
<div style="font-family:'JetBrains Mono',monospace;font-size:11px;line-height:1.7;letter-spacing:.04em;color:#7a726a;">
Gathered from yfinance &#183; FRED &#183; BLS &#183; EIA &#183; CFTC &#183; RSS. Synthesized by Claude with a risk lens.<br>
Equity prices may be prior close; commodities &amp; FX live intraday. &#183; Python &#183; Streamlit &#183; Claude</div>
</td></tr>
</table></td></tr></table></body></html>"""


def save_digest(brief: dict | None = None):
    """Render the latest brief to data/emails/digest_<date>.html and return the path."""
    brief = brief or brief_mod.load_latest_brief()
    if not brief:
        raise SystemExit("No brief found — run `python run.py` first.")
    EMAILS_DIR.mkdir(parents=True, exist_ok=True)
    path = EMAILS_DIR / f"digest_{brief.get('date', 'latest')}.html"
    path.write_text(render_email(brief), encoding="utf-8")
    return path


if __name__ == "__main__":
    print("Wrote", save_digest())

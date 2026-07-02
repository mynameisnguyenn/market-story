"""Render the daily brief as a sendable HTML email digest — email-safe, in-brand.

Pure rendering: takes the brief dict (+ the latest narrative and the prediction ledger)
and returns email-safe HTML (table layout, inline styles) mirroring the market-story-design
email kit — warm near-black, cyan accent, serif "read" over mono data. No network and no
sending here: `scripts/send_digest.py` owns the SMTP transport. Run
`python -m src.email_digest` to write today's digest for a local preview.
"""
from __future__ import annotations

import html as _html

from . import brief as brief_mod, calibration, config, formatting, ledger, scorecard, signals

# Brand tokens (mirror styles.css :root and the design skill's colors_and_type.css).
_BG, _CARD, _BORDER, _GRID = "#0a0908", "#16120f", "#2b2620", "#241f1a"
_TEXT, _DIM, _ACCENT = "#f5f2ef", "#b3aaa0", "#7beafb"
_TONE = {"up": "#36c26f", "down": "#ff5c6c", "warn": "#f5a623", "neutral": _DIM}

# The KPI tape — five headline instruments (the @media block stacks them on phones).
# "macro:" entries read brief["macro"] (latest/change in level); the rest read market rows.
_KPIS = [("^GSPC", "S&P 500"), ("macro:DGS10", "10Y yield"), ("CL=F", "WTI crude"),
         ("GC=F", "Gold"), ("DX-Y.NYB", "Dollar")]
EMAILS_DIR = config.DATA_DIR / "emails"
# TODO(one-time, before enabling send-digest.yml live): confirm in repo Settings > Pages
# that a deployment has succeeded and this URL serves — inferred from owner/repo, not live-checked.
APP_URL = "https://mynameisnguyenn.github.io/market-story/"

_STANCE_LABEL = {1: "&#9650; Long (+1)", -1: "&#9660; Short (&minus;1)", 0: "&#8594; Flat (0)"}
_STANCE_TONE = {1: _TONE["up"], -1: _TONE["down"], 0: _DIM}


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


def _prior_narrative_text():
    path = brief_mod.prior_narrative_path()
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


def _watch_items(limit: int = 4) -> list[dict]:
    """Real watch-item dicts from the narrative's fenced block ([] when no narrative yet)."""
    return scorecard.parse_watch(_narrative_text() or "")[:limit]


def _stance_today() -> dict:
    """Today's directional call from the newest narrative — explicit no-stance state, never
    omitted (a gap must never read as a normal day)."""
    st = scorecard.parse_stance(_narrative_text() or "")
    if st is None:
        return {"label": "No stance logged today", "color": _DIM, "notes": ""}
    notes = st.get("notes", "")
    if len(notes) > 160:
        notes = notes[:160] + "…"
    return {"label": _STANCE_LABEL[st["direction"]], "color": _STANCE_TONE[st["direction"]],
            "notes": notes}


def _last_settled_stance(ledger_rows: list[dict]) -> dict:
    """The previous session's call and how it went: settled P&L / settling / omitted / ''.
    Takes the latest stance row BEFORE the newest one by date — never cherry-picks the last
    flattering settled row."""
    stances = sorted((r for r in ledger_rows if r.get("kind") == "stance"),
                     key=lambda r: r.get("logged", ""))
    prior = stances[:-1] if len(stances) > 1 else []
    if not prior:
        return {"text": "", "color": _DIM}
    r = prior[-1]
    if r.get("status") == "settled":
        pnl = r.get("pnl_pct")
        if pnl is None:                             # flat call: no P&L by design
            return {"text": f"Y'day ({r.get('direction', 0):+d}): flat, no P&amp;L", "color": _DIM}
        color = _TONE["up"] if pnl > 0 else _TONE["down"] if pnl < 0 else _DIM
        return {"text": f"Y'day ({r.get('direction', 0):+d}): {pnl:+.2f}%", "color": color}
    if r.get("status") == "omitted":
        return {"text": "Y'day: no stance logged", "color": _DIM}
    return {"text": "Y'day's call: settling…", "color": _DIM}


def _regrade_summary(brief: dict, limit: int = 3) -> list[dict]:
    """Mechanical re-grade of the PRIOR narrative's watch block against today's brief.
    [] when fewer than two narratives exist. This is scorecard.grade's triggered/watching/
    unresolved — not the analyst's own 'Since last time' verdicts."""
    prior_txt = _prior_narrative_text()
    if not prior_txt:
        return []
    try:
        return scorecard.score_prior(prior_txt, brief)["graded"][:limit]
    except Exception:
        return []


def _track_record(ledger_rows: list[dict]) -> str:
    """One honest line on the watch record; sample-size gated by calibration.MIN_N."""
    s = ledger.stats(rows=ledger_rows)
    graded = s.get("graded") or 0
    if graded < calibration.MIN_N:
        return f"Building sample — {graded}/{calibration.MIN_N} watch calls graded"
    return f"Watch hit-rate {s['hit_rate'] * 100:.0f}% over {graded} graded calls"


def _extremes_rows(brief: dict, limit: int = 3) -> list[dict]:
    """Top stretched cross-asset readings (the brief sorts most-stretched first)."""
    rows = [e for e in (brief.get("extremes") or [])
            if e.get("name") and e.get("pct") is not None]
    return rows[:limit]


def _kpi_cell(brief: dict, sym: str, name: str) -> str:
    if sym.startswith("macro:"):
        sid = sym.split(":", 1)[1]
        row = next((m for m in brief.get("macro", []) if m.get("id") == sid), None)
        last = row.get("latest") if row else None
        ch = row.get("change") if row else None
        delta = formatting.fmt_bps(ch) if ch is not None else ""
    else:
        row = signals._row(brief, sym)
        last = row.get("last") if row else None
        ch = row.get("change_pct") if row else None
        delta = formatting.fmt_pct(ch) if ch is not None else ""
    val = formatting.fmt_num(last) if last is not None else "n/a"
    color = _TONE["up"] if (ch or 0) > 0 else _TONE["down"] if (ch or 0) < 0 else _DIM
    return (
        f'<td class="kpi" width="20%" style="padding:6px;">'
        f'<div style="border:1px solid {_BORDER};border-left:3px solid {_ACCENT};border-radius:8px;padding:10px 12px;">'
        f'<div style="font-family:\'Hanken Grotesk\',Arial,sans-serif;font-size:10px;letter-spacing:.09em;'
        f'text-transform:uppercase;color:{_DIM};">{_esc(name)}</div>'
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:16px;color:{_TEXT};padding-top:3px;">{_esc(val)}</div>'
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:11px;color:{color};padding-top:2px;">{_esc(delta)}</div>'
        f'</div></td>'
    )


def _call_badge(ledger_rows: list[dict]) -> str:
    st = _stance_today()
    prev = _last_settled_stance(ledger_rows)
    prev_cell = (f'<td align="right" style="font-family:\'JetBrains Mono\',monospace;font-size:11px;'
                 f'color:{prev["color"]};">{prev["text"]}</td>') if prev["text"] else ""
    notes = (f'<div style="font-family:\'Hanken Grotesk\',Arial,sans-serif;font-size:12px;'
             f'color:{_DIM};padding-top:6px;line-height:1.5;">{_esc(st["notes"])}</div>'
             if st["notes"] else "")
    return (
        f'<tr><td class="px" style="padding:22px 34px 0;">'
        f'<div style="border:1px solid {_BORDER};border-left:3px solid {st["color"]};border-radius:10px;padding:12px 16px;">'
        f'<table role="presentation" width="100%"><tr>'
        f'<td style="font-family:\'JetBrains Mono\',monospace;font-size:14px;font-weight:500;'
        f'color:{st["color"]};">{st["label"]}<span style="color:{_DIM};font-size:10px;letter-spacing:.09em;'
        f'text-transform:uppercase;"> &nbsp;the call</span></td>{prev_cell}'
        f'</tr></table>{notes}</div></td></tr>'
    )


_GRADE_STYLE = {"triggered": ("HIT", _TONE["up"]), "watching": ("WATCHING", _DIM),
                "unresolved": ("UNRESOLVED", _TONE["warn"])}


def _regrade_rows(brief: dict) -> str:
    graded = _regrade_summary(brief)
    if not graded:
        return (f'<tr><td style="padding:8px 0;font-family:\'Hanken Grotesk\',Arial,sans-serif;'
                f'color:{_DIM};">No prior watch items to grade yet.</td></tr>')
    rows = []
    for g in graded:
        label, color = _GRADE_STYLE.get(g.get("status"), ("?", _DIM))
        cur = formatting.fmt_num(g.get("current")) if g.get("current") is not None else "n/a"
        rows.append(
            f'<tr><td style="padding:5px 0;font-family:\'JetBrains Mono\',monospace;font-size:10px;'
            f'color:{color};width:86px;vertical-align:top;">{label}</td>'
            f'<td style="padding:5px 0;font-family:\'Hanken Grotesk\',Arial,sans-serif;font-size:13px;'
            f'color:{_TEXT};">{_esc(g.get("claim", ""))} '
            f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:11px;color:{_DIM};">'
            f'{cur} vs {_esc(g.get("trigger", ""))}</span></td></tr>'
        )
    return "\n".join(rows)


def _extremes_html(brief: dict) -> str:
    rows = _extremes_rows(brief)
    if not rows:
        return ""                                   # supplementary — omitted entirely when empty
    cells = []
    for e in rows:
        pct = e["pct"]
        color = _TONE["warn"] if (pct >= 90 or pct <= 10) else _DIM
        cells.append(
            f'<tr><td style="padding:4px 0;color:{color};width:18px;vertical-align:top;">&#9679;</td>'
            f'<td style="padding:4px 0;font-family:\'Hanken Grotesk\',Arial,sans-serif;font-size:13px;'
            f'color:{_TEXT};">{_esc(e["name"])} '
            f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:11px;color:{color};">'
            f'{pct:.0f}th %ile (1y)</span></td></tr>'
        )
    return (
        f'<tr><td class="px" style="padding:14px 34px 6px;">'
        f'<div style="font-family:\'Hanken Grotesk\',Arial,sans-serif;font-weight:600;font-size:13px;'
        f'color:{_TEXT};padding-bottom:6px;">&#128200; Stretched (1y percentile)</div>'
        f'<table role="presentation" width="100%">{"".join(cells)}</table></td></tr>'
    )


def _watch_rows() -> str:
    items = _watch_items()
    if not items:
        return ('<tr><td style="padding:11px 0;font-family:\'Hanken Grotesk\',Arial,sans-serif;color:%s;">'
                'No watch triggers yet — they appear once a narrative sets them.</td></tr>' % _DIM)
    rows = []
    for i, it in enumerate(items):
        label, trig = it.get("claim", ""), it.get("trigger", "")
        horizon = it.get("horizon") or "next session"
        border = "" if i == len(items) - 1 else f"border-bottom:1px solid {_GRID};"
        rows.append(
            f'<tr><td style="padding:11px 0;{border}font-family:\'Hanken Grotesk\',Arial,sans-serif;color:{_TEXT};">'
            f'{_esc(label)}<br><span style="font-family:\'JetBrains Mono\',monospace;font-size:11px;color:{_DIM};">'
            f'grades {_esc(horizon)}</span></td>'
            f'<td align="right" style="padding:11px 0;{border}font-family:\'JetBrains Mono\',monospace;'
            f'font-size:11px;color:{_ACCENT};">{_esc(trig)}</td></tr>'
        )
    return "\n".join(rows)


def render_email(brief: dict, ledger_rows: list[dict] | None = None) -> str:
    """Email-safe HTML digest of `brief` (+ narrative, stance, ledger). Pure; never raises
    on bad data."""
    if ledger_rows is None:
        ledger_rows = ledger.load()
    thesis = _thesis(brief)
    when = f'{brief.get("date", "")} · {brief.get("session_label", "")}'.strip(" ·")
    kpis = "".join(_kpi_cell(brief, sym, name) for sym, name in _KPIS)
    pre = (thesis[:140] + "…") if len(thesis) > 140 else thesis
    pre_pad = "&zwnj;&nbsp;" * max(0, (100 - len(pre)) // 8)   # keep Gmail's snippet on the thesis
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="color-scheme" content="dark"/>
<meta name="supported-color-schemes" content="dark light"/><title>Market Story — Daily Brief</title>
<style>body{{margin:0;padding:0;background:{_BG};}}a{{color:{_ACCENT};text-decoration:none;}}
@media (max-width:620px){{.container{{width:100%!important;}}.px{{padding-left:22px!important;padding-right:22px!important;}}.kpi{{display:block!important;width:100%!important;}}}}</style></head>
<body style="margin:0;padding:0;background:{_BG};font-family:'Hanken Grotesk',Arial,sans-serif;" bgcolor="{_BG}">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:{_BG};">{_esc(pre)}{pre_pad}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="{_BG}" style="background:{_BG};">
<tr><td align="center" style="padding:30px 14px;">
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" bgcolor="{_CARD}" style="width:600px;max-width:600px;background:{_CARD};border:1px solid {_BORDER};border-radius:14px;overflow:hidden;">
<tr><td class="px" style="padding:26px 34px 18px;border-bottom:1px solid {_BORDER};">
<table role="presentation" width="100%"><tr>
<td style="font-family:'Hanken Grotesk',Arial,sans-serif;font-weight:700;font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:{_TEXT};">Market Story<span style="color:{_ACCENT};">&#174;</span></td>
<td align="right" style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.06em;color:{_DIM};">{_esc(when)}</td>
</tr></table></td></tr>
{_call_badge(ledger_rows)}
<tr><td class="px" style="padding:22px 34px 8px;">
<div style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:{_ACCENT};margin-bottom:12px;">&#9679; Today's thesis</div>
<div style="font-family:'Newsreader',Georgia,serif;font-size:24px;line-height:1.32;color:{_TEXT};">{_esc(thesis)}</div>
</td></tr>
<tr><td class="px" style="padding:16px 34px 4px;">
<div style="font-family:'Hanken Grotesk',Arial,sans-serif;font-weight:600;font-size:13px;color:{_TEXT};padding-bottom:6px;">&#10003; Watch grades (auto)</div>
<table role="presentation" width="100%">{_regrade_rows(brief)}</table>
<div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:{_DIM};padding-top:4px;">Mechanical re-grade — see the full read for the analyst's actual call.</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:{_DIM};padding-top:2px;">{_esc(_track_record(ledger_rows))}</div>
</td></tr>
<tr><td class="px" style="padding:18px 30px 6px;"><table role="presentation" width="100%"><tr>{kpis}</tr></table></td></tr>
{_extremes_html(brief)}
<tr><td class="px" style="padding:14px 34px 8px;">
<div style="border:1px solid {_BORDER};border-radius:10px;padding:4px 16px;">
<table role="presentation" width="100%" style="font-size:13px;">{_watch_rows()}</table></div></td></tr>
<tr><td class="px" align="center" style="padding:22px 34px 8px;">
<table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="border-radius:9px;background:{_ACCENT};">
<a href="{APP_URL}" style="display:inline-block;font-family:'Hanken Grotesk',Arial,sans-serif;font-weight:700;font-size:14px;color:#0d0c0c;padding:13px 26px;">Open the full brief &#8594;</a>
</td></tr></table></td></tr>
<tr><td class="px" style="padding:22px 34px 26px;border-top:1px solid {_BORDER};">
<div style="font-family:'JetBrains Mono',monospace;font-size:11px;line-height:1.7;letter-spacing:.04em;color:#7a726a;">
Gathered from yfinance &#183; FRED &#183; BLS &#183; EIA &#183; CFTC &#183; RSS. Synthesized by Claude with a risk lens.<br>
Equity prices may be prior close; commodities &amp; FX live intraday. &#183; Python &#183; Claude</div>
</td></tr>
</table></td></tr></table></body></html>"""


def save_digest(brief: dict | None = None, ledger_rows: list[dict] | None = None):
    """Render the latest brief to data/emails/digest_<date>.html and return the path."""
    brief = brief or brief_mod.load_latest_brief()
    if not brief:
        raise SystemExit("No brief found — run `python run.py` first.")
    EMAILS_DIR.mkdir(parents=True, exist_ok=True)
    path = EMAILS_DIR / f"digest_{brief.get('date', 'latest')}.html"
    path.write_text(render_email(brief, ledger_rows=ledger_rows), encoding="utf-8")
    return path


if __name__ == "__main__":
    print("Wrote", save_digest())

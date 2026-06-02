#!/usr/bin/env python3
"""
Lucid by Vince — Report Generator
Reads data.json + narrative.json and produces index.html
Usage: python3 generate.py
"""

import json
import datetime
import os

# ─── LOAD DATA ─────────────────────────────────────────────────────────────────

def load_json(path, fallback={}):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    print(f"  ⚠ {path} not found — using fallback")
    return fallback

data       = load_json("data.json")
narrative  = load_json("narrative.json", {
    "month_title":    "The Month That Changed Everything",
    "snapshot":       [
        "Add your first snapshot bullet here.",
        "Add your second snapshot bullet here.",
        "Add your third snapshot bullet here.",
        "Add your fourth snapshot bullet here.",
        "Add your fifth snapshot bullet here.",
        "Add your sixth snapshot bullet here.",
    ],
    "stability_score":   34,
    "stability_verdict": "Cautious Instability",
    "stability_dims": [
        {"name": "Geopolitical tension (25%)",    "score": 22, "color": "#E8002D"},
        {"name": "Market volatility (20%)",        "score": 70, "color": "#007A3D"},
        {"name": "Economic predictability (20%)",  "score": 42, "color": "#9A5700"},
        {"name": "Social / consumer stress (15%)", "score": 20, "color": "#E8002D"},
        {"name": "Climate / physical risk (10%)",  "score": 45, "color": "#9A5700"},
        {"name": "Institutional integrity (10%)",  "score": 30, "color": "#E8002D"},
    ],
    "unusual_headlines": [
        {
            "title":  "Add unusual headline 1 here",
            "source": "Source · Date",
            "desc":   "Description of the unusual event.",
            "signal": "Your signal / takeaway"
        },
        {
            "title":  "Add unusual headline 2 here",
            "source": "Source · Date",
            "desc":   "Description of the unusual event.",
            "signal": "Your signal / takeaway"
        },
        {
            "title":  "Add unusual headline 3 here",
            "source": "Source · Date",
            "desc":   "Description of the unusual event.",
            "signal": "Your signal / takeaway"
        },
    ],
    "geopolitics": [
        {"flag": "🌍", "title": "Event 1", "tag": "Watch", "tag_color": "amber", "desc": "Description."},
        {"flag": "🌍", "title": "Event 2", "tag": "Active", "tag_color": "red",   "desc": "Description."},
        {"flag": "🌍", "title": "Event 3", "tag": "EU",     "tag_color": "blue",  "desc": "Description."},
    ],
    "climate_level": "Moderate",
    "climate_items": [
        {"flag": "🌧", "title": "Event 1", "tag": "Active", "tag_color": "red",   "desc": "Description."},
        {"flag": "🌊", "title": "Event 2", "tag": "Watch",  "tag_color": "amber", "desc": "Description."},
    ],
    "stoic_quote":    "Add your Stoic quote here.",
    "stoic_author":   "Author, Work",
    "stoic_context":  "One sentence connecting this quote to the month.",
    "month_question": "Add your philosophical question for the month here.",
    "question_body":  "Two to three sentences exploring the question.",
    "bias_name":      "Name of the cognitive bias",
    "bias_body":      "Explain the bias and connect it to this month's events.",
    "book_title":     "Book Title",
    "book_meta":      "Author · Year · Genre",
    "book_desc":      "Your 60-second summary of the book and why it matters this month.",
    "word":           "Word",
    "word_meta":      "Part of speech · Etymology",
    "word_desc":      "Definition and why it matters this month.",
    "album_title":    "Album Title",
    "album_meta":     "Artist · Year",
    "album_desc":     "Why this album matters this month.",
    "cosmic_event":   "Astronomical event of the month",
    "cosmic_desc":    "Description of the astronomical event.",
    "history_title":  "Today in History",
    "history_sub":    "Subtitle",
    "history_desc":   "What happened on this date in history.",
    "fear_greed_override": None,
})

# ─── SHORTCUTS ─────────────────────────────────────────────────────────────────

m   = data.get("markets", {})
s   = data.get("signals", {})
meta = data.get("meta", {})

def mkt(name, field, fallback="—"):
    return m.get(name, {}).get(field, fallback) or fallback

def color_pct(val):
    if val is None or val == "—":
        return "var(--muted)"
    if isinstance(val, str):
        val = val.replace("+","").replace("%","")
        try: val = float(val)
        except: return "var(--muted)"
    if val > 0: return "var(--up)"
    if val < 0: return "var(--dn)"
    return "var(--muted)"

def snap_bullets():
    bullets = narrative.get("snapshot", [])
    html = ""
    for i, b in enumerate(bullets, 1):
        html += f'''
        <div class="snap-item">
          <div class="snap-num">{i:02d}</div>
          <div class="snap-text">{b}</div>
        </div>'''
    return html

def stability_dims():
    html = ""
    for d in narrative.get("stability_dims", []):
        html += f'''
        <div class="dim-row">
          <div class="dim-top">
            <span class="dim-name">{d["name"]}</span>
            <span class="dim-val">{d["score"]}/100</span>
          </div>
          <div class="bar-bg"><div class="bar-fg" style="width:{d["score"]}%;background:{d["color"]};"></div></div>
        </div>'''
    return html

def unusual_headlines():
    html = ""
    for i, h in enumerate(narrative.get("unusual_headlines", []), 1):
        html += f'''
        <div class="hl-item">
          <div class="hl-eyebrow">Unusual &middot; No. {i}</div>
          <div class="hl-title">{h["title"]}</div>
          <div class="hl-source">{h["source"]}</div>
          <div class="hl-desc">{h["desc"]}</div>
          <div class="hl-signal">&#8594; {h["signal"]}</div>
        </div>'''
    return html

def geo_items():
    html = ""
    for g in narrative.get("geopolitics", []):
        html += f'''
        <div class="geo-item">
          <div class="geo-flag">{g["flag"]}</div>
          <div class="geo-body">
            <div class="geo-title">{g["title"]} <span class="tag tag-{g["tag_color"]}">{g["tag"]}</span></div>
            <div class="geo-desc">{g["desc"]}</div>
          </div>
        </div>'''
    return html

def climate_items():
    html = ""
    for c in narrative.get("climate_items", []):
        html += f'''
        <div class="geo-item">
          <div class="geo-flag">{c["flag"]}</div>
          <div class="geo-body">
            <div class="geo-title">{c["title"]} <span class="tag tag-{c["tag_color"]}">{c["tag"]}</span></div>
            <div class="geo-desc">{c["desc"]}</div>
          </div>
        </div>'''
    return html

# Fear & Greed
fg_score = narrative.get("fear_greed_override") or s.get("fear_greed_score")
fg_label = s.get("fear_greed_label", "—")
fg_display = str(fg_score) if fg_score else "—"

# Moon
moon_phase = s.get("moon_phase", "—")
moon_pct   = s.get("moon_pct", 0)
moon_icons = {"New Moon":"🌑","Waxing Crescent":"🌒","First Quarter":"🌓",
              "Waxing Gibbous":"🌔","Full Moon":"🌕","Waning Gibbous":"🌖",
              "Last Quarter":"🌗","Waning Crescent":"🌘"}
moon_icon  = moon_icons.get(moon_phase, "🌙")

report_month = data.get("report_month", meta.get("today", ""))
today_str    = meta.get("today", datetime.date.today().strftime("%B %d, %Y"))

# ─── BUILD HTML ────────────────────────────────────────────────────────────────

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Lucid by Vince &middot; {report_month}</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@1,400;1,700&display=swap" rel="stylesheet"/>
<style>
:root {{
  --white:#FFFFFF; --ink:#0A0A0A; --ink2:#1C1C1C; --red:#E8002D; --red2:#B5001F;
  --grey1:#F2F2F2; --grey2:#E0E0E0; --muted:#555555; --dim:#888888;
  --up:#007A3D; --dn:#E8002D; --warn:#9A5700;
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html{{scroll-behavior:smooth;}}
body{{background:var(--white);color:var(--ink);font-family:'Inter',sans-serif;font-size:14px;line-height:1.6;-webkit-font-smoothing:antialiased;}}
.masthead{{background:var(--ink);padding:0 56px;height:80px;display:flex;align-items:center;justify-content:space-between;}}
.logo-group{{display:flex;align-items:center;gap:18px;}}
.logo-wordmark{{font-family:'Bebas Neue',sans-serif;font-size:38px;color:var(--white);letter-spacing:0.06em;line-height:1;}}
.logo-sub{{font-size:10px;letter-spacing:0.32em;color:#666;text-transform:uppercase;margin-top:1px;}}
.masthead-date{{font-family:'Bebas Neue',sans-serif;font-size:22px;color:var(--red);letter-spacing:0.1em;line-height:1;text-align:right;}}
.masthead-label{{font-size:10px;color:#555;letter-spacing:0.18em;text-transform:uppercase;margin-top:3px;text-align:right;}}
.red-rule{{height:4px;background:var(--red);}}
.month-banner{{background:var(--grey1);border-bottom:1px solid var(--grey2);padding:14px 56px;display:flex;align-items:center;justify-content:space-between;}}
.month-title{{font-family:'Playfair Display',serif;font-style:italic;font-size:18px;color:var(--ink);}}
.month-meta{{font-size:11px;color:var(--dim);letter-spacing:0.1em;text-transform:uppercase;}}
nav{{background:var(--white);border-bottom:2px solid var(--ink);padding:0 56px;display:flex;overflow-x:auto;position:sticky;top:0;z-index:100;}}
nav a{{font-size:11px;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:var(--muted);text-decoration:none;padding:14px 18px;border-bottom:3px solid transparent;white-space:nowrap;}}
nav a:hover{{color:var(--red);border-bottom-color:var(--red);}}
.phil-strip{{background:var(--ink2);padding:28px 56px;display:grid;grid-template-columns:1fr 1px 1fr 1px 1fr;gap:40px;}}
.phil-divider{{background:#2A2A2A;}}
.phil-label{{font-size:9px;font-weight:600;letter-spacing:0.28em;text-transform:uppercase;color:var(--red);margin-bottom:10px;}}
.phil-quote{{font-family:'Playfair Display',serif;font-style:italic;font-size:15px;color:#E0E0E0;line-height:1.55;margin-bottom:8px;}}
.phil-attr{{font-size:11px;color:#555;letter-spacing:0.04em;margin-bottom:6px;}}
.phil-body{{font-size:12px;color:#777;line-height:1.65;}}
.sec-head{{background:var(--ink);padding:20px 56px;margin:0 0 32px;display:flex;align-items:center;justify-content:space-between;}}
.sec-head h2{{font-family:'Bebas Neue',sans-serif;font-size:52px;color:var(--white);letter-spacing:0.06em;line-height:1;}}
.sec-tag{{font-size:10px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:var(--white);background:var(--red);padding:5px 12px;}}
main{{padding:0 56px;max-width:1320px;margin:0 auto;}}
.section-block{{margin-bottom:56px;}}
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:56px;}}
.g3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:40px;}}
.g4{{display:grid;grid-template-columns:repeat(4,1fr);gap:32px;}}
.snap-item{{display:flex;gap:16px;padding:14px 0;border-bottom:1px solid var(--grey2);align-items:flex-start;}}
.snap-item:last-child{{border-bottom:none;}}
.snap-num{{font-family:'Bebas Neue',sans-serif;font-size:28px;color:var(--grey2);flex-shrink:0;width:32px;line-height:1;margin-top:2px;}}
.snap-text{{font-size:13px;color:var(--muted);line-height:1.6;}}
.snap-text strong{{color:var(--ink);font-weight:600;}}
.stab-number{{font-family:'Bebas Neue',sans-serif;font-size:140px;line-height:0.85;color:var(--ink);letter-spacing:-0.02em;margin-bottom:8px;}}
.stab-verdict{{font-family:'Bebas Neue',sans-serif;font-size:28px;color:var(--warn);letter-spacing:0.08em;margin-bottom:4px;}}
.stab-scale{{font-size:11px;color:var(--dim);letter-spacing:0.06em;margin-bottom:24px;text-transform:uppercase;}}
.dim-row{{margin-bottom:10px;}}
.dim-top{{display:flex;justify-content:space-between;margin-bottom:4px;}}
.dim-name{{font-size:11px;color:var(--muted);}}
.dim-val{{font-size:11px;font-weight:600;color:var(--ink);}}
.bar-bg{{height:3px;background:var(--grey2);}}
.bar-fg{{height:3px;}}
.hl-item{{padding:16px 0;border-bottom:1px solid var(--grey2);}}
.hl-item:last-child{{border-bottom:none;}}
.hl-eyebrow{{font-size:9px;font-weight:700;letter-spacing:0.24em;text-transform:uppercase;color:var(--red);margin-bottom:6px;}}
.hl-title{{font-size:15px;font-weight:700;color:var(--ink);line-height:1.35;margin-bottom:4px;}}
.hl-source{{font-size:10px;color:var(--dim);letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px;}}
.hl-desc{{font-size:12px;color:var(--muted);line-height:1.6;}}
.hl-signal{{font-size:11px;font-weight:600;color:var(--red);margin-top:6px;}}
.mkt{{width:100%;border-collapse:collapse;}}
.mkt thead tr{{border-bottom:2px solid var(--ink);}}
.mkt th{{font-size:10px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--dim);padding:8px 0;text-align:left;}}
.mkt th:not(:first-child){{text-align:right;}}
.mkt td{{padding:12px 0;border-bottom:1px solid var(--grey2);vertical-align:top;}}
.mkt td:not(:first-child){{text-align:right;}}
.mkt tr:last-child td{{border-bottom:none;}}
.mkt-name{{font-size:14px;font-weight:700;color:var(--ink);}}
.mkt-val{{font-size:13px;font-weight:500;color:var(--muted);}}
.mkt-note{{font-size:11px;color:var(--dim);}}
.sig-grid{{display:grid;grid-template-columns:repeat(4,1fr);}}
.sig-cell{{padding:20px 20px 20px 0;border-right:1px solid var(--grey2);border-bottom:1px solid var(--grey2);}}
.sig-cell:nth-child(4n){{border-right:none;}}
.sig-cell:nth-last-child(-n+4){{border-bottom:none;}}
.sig-label{{font-size:9px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:var(--dim);margin-bottom:6px;}}
.sig-val{{font-family:'Bebas Neue',sans-serif;font-size:32px;line-height:1;color:var(--ink);letter-spacing:0.04em;}}
.sig-note{{font-size:11px;color:var(--dim);margin-top:4px;}}
.geo-item{{display:flex;gap:14px;padding:16px 0;border-bottom:1px solid var(--grey2);align-items:flex-start;}}
.geo-item:last-child{{border-bottom:none;}}
.geo-flag{{font-size:22px;flex-shrink:0;width:28px;margin-top:1px;}}
.geo-body{{flex:1;}}
.geo-title{{font-size:14px;font-weight:700;color:var(--ink);margin-bottom:4px;line-height:1.3;}}
.geo-desc{{font-size:12px;color:var(--muted);line-height:1.6;}}
.tag{{display:inline-block;font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;padding:2px 7px;margin-left:7px;vertical-align:middle;}}
.tag-red{{background:#FFE8EC;color:var(--red2);}} .tag-amber{{background:#FFF3E0;color:var(--warn);}}
.tag-green{{background:#E6F4EC;color:var(--up);}} .tag-blue{{background:#E8F0FD;color:#1A3A8B;}}
.arcane-num{{font-family:'Bebas Neue',sans-serif;font-size:72px;line-height:0.9;letter-spacing:0.02em;margin:10px 0 4px;}}
.arcane-sub{{font-size:10px;font-weight:600;letter-spacing:0.16em;text-transform:uppercase;color:var(--dim);margin-bottom:12px;}}
.arcane-desc{{font-size:12px;color:var(--muted);line-height:1.65;}}
.arcane-warn{{font-size:10px;color:var(--dim);margin-top:12px;padding-top:12px;border-top:1px solid var(--grey2);font-style:italic;}}
.scale-row{{display:flex;gap:3px;margin:12px 0;}}
.scale-seg{{flex:1;padding:5px 3px;text-align:center;}}
.scale-seg-title{{font-size:8px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;}}
.scale-seg-range{{font-size:8px;color:var(--muted);margin-top:1px;}}
.cosm-icon{{font-size:32px;margin-bottom:10px;}}
.cosm-title{{font-size:15px;font-weight:700;color:var(--ink);margin-bottom:6px;line-height:1.3;}}
.cosm-sub{{font-size:11px;font-weight:600;color:var(--dim);letter-spacing:0.06em;margin-bottom:8px;text-transform:uppercase;}}
.cosm-desc{{font-size:12px;color:var(--muted);line-height:1.65;}}
.cult-eyebrow{{font-size:9px;font-weight:700;letter-spacing:0.24em;text-transform:uppercase;color:var(--red);margin-bottom:8px;}}
.cult-title{{font-size:20px;font-weight:700;color:var(--ink);line-height:1.25;margin-bottom:4px;}}
.cult-meta{{font-size:11px;color:var(--dim);letter-spacing:0.04em;margin-bottom:12px;}}
.cult-desc{{font-size:12px;color:var(--muted);line-height:1.7;}}
.bm-row{{display:flex;justify-content:space-between;align-items:baseline;padding:10px 0;border-bottom:1px solid var(--grey2);}}
.bm-row:last-child{{border-bottom:none;}}
.bm-label{{font-size:12px;color:var(--muted);}}
.bm-val{{font-family:'Bebas Neue',sans-serif;font-size:20px;letter-spacing:0.04em;color:var(--ink);}}
.em-big{{font-family:'Bebas Neue',sans-serif;font-size:64px;line-height:0.9;letter-spacing:0.02em;color:var(--ink);}}
.em-sub{{font-size:11px;color:var(--dim);letter-spacing:0.06em;text-transform:uppercase;margin-top:6px;margin-bottom:20px;}}
.col-div{{border-right:1px solid var(--grey2);padding-right:40px;margin-right:40px;}}
.col-div:last-child{{border-right:none;padding-right:0;margin-right:0;}}
footer{{background:var(--ink);margin-top:72px;padding:36px 56px;display:flex;align-items:center;justify-content:space-between;gap:32px;}}
.footer-wordmark{{font-family:'Bebas Neue',sans-serif;font-size:28px;color:#444;letter-spacing:0.06em;}}
.footer-tagline{{font-size:11px;color:#444;font-style:italic;margin-top:2px;}}
.footer-sources{{font-size:10px;color:#444;text-align:right;line-height:1.85;}}
</style>
</head>
<body>

<header class="masthead">
  <div class="logo-group">
    <svg width="52" height="52" viewBox="0 0 52 52" fill="none">
      <rect width="52" height="52" rx="9" fill="#1C1C1C"/>
      <path d="M6,26 Q26,7 46,26 Q26,45 6,26 Z" stroke="white" stroke-width="2" stroke-linecap="round" fill="none"/>
      <circle cx="26" cy="26" r="10" stroke="white" stroke-width="1.8" fill="none"/>
      <circle cx="26" cy="26" r="4" fill="white"/>
      <circle cx="30" cy="22" r="2.5" fill="#1C1C1C"/>
      <line x1="13" y1="14" x2="11" y2="7" stroke="#444" stroke-width="1.2" stroke-linecap="round"/>
      <line x1="26" y1="11" x2="26" y2="4" stroke="#444" stroke-width="1.2" stroke-linecap="round"/>
      <line x1="39" y1="14" x2="41" y2="7" stroke="#444" stroke-width="1.2" stroke-linecap="round"/>
    </svg>
    <div>
      <div class="logo-wordmark">LUCID</div>
      <div class="logo-sub">by vince &nbsp;&middot;&nbsp; intelligence report</div>
    </div>
  </div>
  <div>
    <div class="masthead-date">{report_month}</div>
    <div class="masthead-label">End of Month Wrap Up &amp; Stability Index</div>
  </div>
</header>

<div class="red-rule"></div>

<div class="month-banner">
  <div class="month-title">{report_month}: {narrative.get("month_title","")}</div>
  <div class="month-meta">Published {today_str} &nbsp;&middot;&nbsp; lucidbyvince.com</div>
</div>

<nav>
  <a href="#snapshot">Snapshot</a>
  <a href="#stability">Stability</a>
  <a href="#markets">Markets</a>
  <a href="#signals">Signals</a>
  <a href="#geopolitics">Geopolitics</a>
  <a href="#climate">Climate</a>
  <a href="#arcane">Arcane</a>
  <a href="#philosophy">Philosophy</a>
  <a href="#cosmic">Cosmic</a>
  <a href="#culture">Culture</a>
</nav>

<div class="phil-strip" id="philosophy">
  <div>
    <div class="phil-label">Stoic Provocation &middot; {meta.get("month_name","")}</div>
    <div class="phil-quote">"{narrative.get("stoic_quote","")}"</div>
    <div class="phil-attr">{narrative.get("stoic_author","")}</div>
    <div class="phil-body">{narrative.get("stoic_context","")}</div>
  </div>
  <div class="phil-divider"></div>
  <div>
    <div class="phil-label">Question of the Month</div>
    <div class="phil-quote">{narrative.get("month_question","")}</div>
    <div class="phil-body">{narrative.get("question_body","")}</div>
  </div>
  <div class="phil-divider"></div>
  <div>
    <div class="phil-label">Cognitive Bias of the Month</div>
    <div class="phil-quote">{narrative.get("bias_name","")}</div>
    <div class="phil-body">{narrative.get("bias_body","")}</div>
  </div>
</div>

<main>

  <div class="sec-head" id="snapshot">
    <h2>Executive Snapshot</h2>
    <div class="sec-tag">{report_month}</div>
  </div>
  <div class="g2 section-block">
    <div>{snap_bullets()}</div>
    <div>
      <div style="font-size:10px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--dim);margin-bottom:20px;">Three Most Unusual Headlines</div>
      {unusual_headlines()}
    </div>
  </div>

  <div class="sec-head" id="stability">
    <h2>Global Stability Score</h2>
    <div class="sec-tag">Proprietary Index</div>
  </div>
  <div class="g2 section-block" style="align-items:start;">
    <div>
      <div class="stab-number">{narrative.get("stability_score", 0)}</div>
      <div class="stab-verdict">{narrative.get("stability_verdict","")}</div>
      <div class="stab-scale">0 = complete chaos &nbsp;&middot;&nbsp; 100 = fully predictable</div>
      {stability_dims()}
      <div style="margin-top:28px;padding-top:20px;border-top:1px solid var(--grey2);">
        <div style="font-size:10px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--dim);margin-bottom:14px;">Historical Benchmarks</div>
        <div class="bm-row"><div class="bm-label">{report_month} — this month</div><div class="bm-val" style="color:var(--warn);">{narrative.get("stability_score",0)}</div></div>
        <div class="bm-row"><div class="bm-label">Mar 2020 — COVID crash (modelled)</div><div class="bm-val" style="color:var(--dn);">~18</div></div>
        <div class="bm-row"><div class="bm-label">Sep 2008 — Lehman (modelled)</div><div class="bm-val" style="color:var(--dn);">~12</div></div>
        <div class="bm-row"><div class="bm-label">Jan 2020 — pre-COVID baseline (modelled)</div><div class="bm-val" style="color:var(--up);">~68</div></div>
        <div class="bm-row"><div class="bm-label">Dec 2017 — calm bull market (modelled)</div><div class="bm-val" style="color:var(--up);">~74</div></div>
        <div style="margin-top:12px;font-size:11px;color:var(--dim);font-style:italic;line-height:1.6;">Historical scores are modelled approximations — not back-tested data.</div>
      </div>
    </div>
    <div>
      <div style="font-size:10px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--dim);margin-bottom:6px;">Fear &amp; Greed Index &middot; {today_str}</div>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:80px;line-height:0.9;color:var(--up);letter-spacing:0.02em;margin-bottom:6px;">{fg_display}</div>
      <div style="font-size:10px;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;color:var(--up);margin-bottom:12px;">{fg_label}</div>
      <div class="scale-row">
        <div class="scale-seg" style="background:#FFE8EC;"><div class="scale-seg-title" style="color:var(--dn);">Ext. Fear</div><div class="scale-seg-range">0&ndash;25</div></div>
        <div class="scale-seg" style="background:#FFF3E0;"><div class="scale-seg-title" style="color:var(--warn);">Fear</div><div class="scale-seg-range">26&ndash;44</div></div>
        <div class="scale-seg" style="background:var(--grey1);"><div class="scale-seg-title" style="color:var(--muted);">Neutral</div><div class="scale-seg-range">45&ndash;55</div></div>
        <div class="scale-seg" style="background:#E6F4EC;"><div class="scale-seg-title" style="color:var(--up);">Greed</div><div class="scale-seg-range">56&ndash;74</div></div>
        <div class="scale-seg" style="background:#C8ECD6;"><div class="scale-seg-title" style="color:var(--up);">Ext. Greed</div><div class="scale-seg-range">75&ndash;100</div></div>
      </div>
      <div style="font-size:11px;color:var(--muted);line-height:1.65;">7 equal-weight components: market momentum, price strength, breadth, put/call ratio, VIX, safe-haven demand, junk bond spread.<br/><span style="font-size:10px;color:var(--dim);font-style:italic;margin-top:4px;display:block;">Source: CNN Business / MacroMicro.</span></div>
    </div>
  </div>

  <div class="sec-head" id="markets">
    <h2>Markets</h2>
    <div class="sec-tag">Month-End &middot; {today_str}</div>
  </div>
  <div class="section-block">
    <table class="mkt">
      <thead><tr><th>Asset</th><th>Price</th><th>Year Start</th><th>MoM</th><th>YTD</th><th>Note</th></tr></thead>
      <tbody>
        <tr><td><div class="mkt-name">S&amp;P 500</div></td><td><div class="mkt-val">{mkt("sp500","price_fmt")}</div></td><td><div class="mkt-val">{mkt("sp500","year_start")}</div></td><td><div class="mkt-val" style="color:{color_pct(mkt('sp500','mom_pct'))}">{mkt("sp500","mom_fmt")}</div></td><td><div class="mkt-val" style="color:{color_pct(mkt('sp500','ytd_pct'))}">{mkt("sp500","ytd_fmt")}</div></td><td><div class="mkt-note">ATH territory</div></td></tr>
        <tr><td><div class="mkt-name">IBEX 35</div></td><td><div class="mkt-val">{mkt("ibex","price_fmt")}</div></td><td><div class="mkt-val">{mkt("ibex","year_start")}</div></td><td><div class="mkt-val" style="color:{color_pct(mkt('ibex','mom_pct'))}">{mkt("ibex","mom_fmt")}</div></td><td><div class="mkt-val" style="color:{color_pct(mkt('ibex','ytd_pct'))}">{mkt("ibex","ytd_fmt")}</div></td><td><div class="mkt-note">Verify via BME</div></td></tr>
        <tr><td><div class="mkt-name">Gold</div></td><td><div class="mkt-val">{mkt("gold","price_fmt")}</div></td><td><div class="mkt-val">{mkt("gold","year_start")}</div></td><td><div class="mkt-val" style="color:{color_pct(mkt('gold','mom_pct'))}">{mkt("gold","mom_fmt")}</div></td><td><div class="mkt-val" style="color:{color_pct(mkt('gold','ytd_pct'))}">{mkt("gold","ytd_fmt")}</div></td><td><div class="mkt-note">Spot price</div></td></tr>
        <tr><td><div class="mkt-name">Brent Crude</div></td><td><div class="mkt-val">{mkt("brent","price_fmt")}</div></td><td><div class="mkt-val">{mkt("brent","year_start")}</div></td><td><div class="mkt-val" style="color:{color_pct(mkt('brent','mom_pct'))}">{mkt("brent","mom_fmt")}</div></td><td><div class="mkt-val" style="color:{color_pct(mkt('brent','ytd_pct'))}">{mkt("brent","ytd_fmt")}</div></td><td><div class="mkt-note">Front month futures</div></td></tr>
        <tr><td><div class="mkt-name">Bitcoin</div></td><td><div class="mkt-val">{mkt("bitcoin","price_fmt")}</div></td><td><div class="mkt-val">{mkt("bitcoin","year_start")}</div></td><td><div class="mkt-val" style="color:{color_pct(mkt('bitcoin','mom_pct'))}">{mkt("bitcoin","mom_fmt")}</div></td><td><div class="mkt-val" style="color:{color_pct(mkt('bitcoin','ytd_pct'))}">{mkt("bitcoin","ytd_fmt")}</div></td><td><div class="mkt-note">USD spot</div></td></tr>
        <tr><td><div class="mkt-name">Ethereum</div></td><td><div class="mkt-val">{mkt("ethereum","price_fmt")}</div></td><td><div class="mkt-val">{mkt("ethereum","year_start")}</div></td><td><div class="mkt-val" style="color:{color_pct(mkt('ethereum','mom_pct'))}">{mkt("ethereum","mom_fmt")}</div></td><td><div class="mkt-val" style="color:{color_pct(mkt('ethereum','ytd_pct'))}">{mkt("ethereum","ytd_fmt")}</div></td><td><div class="mkt-note">USD spot</div></td></tr>
      </tbody>
    </table>
  </div>

  <div class="sec-head" id="signals"><h2>Signal Matrix</h2></div>
  <div class="section-block">
    <div class="sig-grid">
      <div class="sig-cell"><div class="sig-label">Fed Rate</div><div class="sig-val" style="color:var(--warn);font-size:20px;">{s.get("fed_rate","—")}</div><div class="sig-note">Current target range</div></div>
      <div class="sig-cell"><div class="sig-label">Fear &amp; Greed</div><div class="sig-val" style="color:var(--up);">{fg_display}</div><div class="sig-note">{fg_label}</div></div>
      <div class="sig-cell"><div class="sig-label">Moon Phase</div><div class="sig-val" style="font-size:20px;color:var(--ink);">{moon_icon}</div><div class="sig-note">{moon_phase} &middot; {moon_pct}% lit</div></div>
      <div class="sig-cell"><div class="sig-label">S&amp;P 500 YTD</div><div class="sig-val" style="color:{color_pct(mkt('sp500','ytd_pct'))};">{mkt("sp500","ytd_fmt")}</div><div class="sig-note">From Jan 1</div></div>
      <div class="sig-cell"><div class="sig-label">Bitcoin YTD</div><div class="sig-val" style="color:{color_pct(mkt('bitcoin','ytd_pct'))};">{mkt("bitcoin","ytd_fmt")}</div><div class="sig-note">From Jan 1</div></div>
      <div class="sig-cell"><div class="sig-label">Gold YTD</div><div class="sig-val" style="color:{color_pct(mkt('gold','ytd_pct'))};">{mkt("gold","ytd_fmt")}</div><div class="sig-note">From Jan 1</div></div>
      <div class="sig-cell"><div class="sig-label">Brent YTD</div><div class="sig-val" style="color:{color_pct(mkt('brent','ytd_pct'))};">{mkt("brent","ytd_fmt")}</div><div class="sig-note">From Jan 1</div></div>
      <div class="sig-cell"><div class="sig-label">ETH YTD</div><div class="sig-val" style="color:{color_pct(mkt('ethereum','ytd_pct'))};">{mkt("ethereum","ytd_fmt")}</div><div class="sig-note">From Jan 1</div></div>
    </div>
  </div>

  <div class="sec-head" id="geopolitics"><h2>Geopolitics &amp; Climate</h2></div>
  <div class="g2 section-block" style="gap:56px;">
    <div>{geo_items()}</div>
    <div>
      <div style="font-size:10px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--dim);margin-bottom:6px;">Climate Risk Level</div>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:40px;color:var(--warn);letter-spacing:0.06em;margin-bottom:20px;line-height:1;">{narrative.get("climate_level","—")}</div>
      {climate_items()}
    </div>
  </div>

  <div class="sec-head" id="arcane"><h2>Arcane Economics</h2><div class="sec-tag">Indicators Others Ignore</div></div>
  <div class="g3 section-block">
    <div class="col-div">
      <div style="font-size:10px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--dim);margin-bottom:4px;">Baltic Dry Index</div>
      <div class="arcane-num" style="color:var(--warn);">~1,380</div>
      <div class="arcane-sub">Approximate &middot; {report_month}</div>
      <div class="scale-row">
        <div class="scale-seg" style="background:#FFE8EC;"><div class="scale-seg-title" style="color:var(--dn);">Distressed</div><div class="scale-seg-range">&lt;600</div></div>
        <div class="scale-seg" style="background:#FFF3E0;border:2px solid var(--warn);"><div class="scale-seg-title" style="color:var(--warn);">Moderate &#8592;</div><div class="scale-seg-range">600&ndash;1,800</div></div>
        <div class="scale-seg" style="background:#E6F4EC;"><div class="scale-seg-title" style="color:var(--up);">Healthy</div><div class="scale-seg-range">1,800&ndash;3,500</div></div>
        <div class="scale-seg" style="background:#C8ECD6;"><div class="scale-seg-title" style="color:var(--up);">Boom</div><div class="scale-seg-range">&gt;3,500</div></div>
      </div>
      <div class="arcane-desc">Daily rate for dry bulk ships carrying iron ore, coal, grain across 20 global routes. No derivatives, no sentiment — actual ships. All-time high ~11,800 (May 2008). COVID low ~393 (2016).</div>
      <div class="arcane-warn">&#9888; Verify via Baltic Exchange or Hellenic Shipping News.</div>
    </div>
    <div class="col-div">
      <div style="font-size:10px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--dim);margin-bottom:4px;">Shiller CAPE Ratio</div>
      <div class="arcane-num" style="color:var(--dn);">~38&times;</div>
      <div class="arcane-sub">Cyclically Adjusted P/E &middot; approx.</div>
      <div class="arcane-desc">S&amp;P 500 divided by 10 years of real average earnings. At ~38&times; it sits well above the long-run average of ~17&times; and approaching dot-com era highs of ~44&times;.</div>
      <div class="arcane-warn">&#9888; Verify via multpl.com or GuruFocus before citing.</div>
    </div>
    <div class="col-div">
      <div style="font-size:10px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--dim);margin-bottom:4px;">Buffett Indicator</div>
      <div class="arcane-num" style="color:var(--dn);">~195%</div>
      <div class="arcane-sub">Total Market Cap / US GDP &middot; approx.</div>
      <div class="arcane-desc">Buffett called this "probably the best single measure of where valuations stand." At ~195% it signals significant overvaluation — above the 2021 peak of ~190%.</div>
      <div class="arcane-warn">&#9888; Verify via GuruFocus Buffett Indicator tool.</div>
    </div>
  </div>

  <div class="sec-head" id="cosmic"><h2>Cosmic Layer</h2><div class="sec-tag">Earth, Sky &amp; Time</div></div>
  <div class="g3 section-block">
    <div class="col-div">
      <div class="cosm-icon">{moon_icon}</div>
      <div class="cosm-title">Moon Phase &middot; {today_str}</div>
      <div class="cosm-sub">{moon_phase} &middot; ~{moon_pct}% illuminated</div>
      <div class="cosm-desc">{narrative.get("cosmic_desc","")}</div>
    </div>
    <div class="col-div">
      <div class="cosm-icon">&#9915;</div>
      <div class="cosm-title">{narrative.get("cosmic_event","Astronomical Event")}</div>
      <div class="cosm-desc">{narrative.get("cosmic_event_desc","")}</div>
    </div>
    <div class="col-div">
      <div class="cosm-icon">&#128336;</div>
      <div class="cosm-title">{narrative.get("history_title","Today in History")}</div>
      <div class="cosm-sub">{narrative.get("history_sub","")}</div>
      <div class="cosm-desc">{narrative.get("history_desc","")}</div>
    </div>
  </div>

  <div class="sec-head" id="culture"><h2>Culture Layer</h2><div class="sec-tag">Read &middot; Hear &middot; Know</div></div>
  <div class="g3 section-block">
    <div class="col-div">
      <div class="cult-eyebrow">Book in 60 seconds</div>
      <div class="cult-title">{narrative.get("book_title","")}</div>
      <div class="cult-meta">{narrative.get("book_meta","")}</div>
      <div class="cult-desc">{narrative.get("book_desc","")}</div>
    </div>
    <div class="col-div">
      <div class="cult-eyebrow">Word you should know</div>
      <div class="cult-title">{narrative.get("word","")}</div>
      <div class="cult-meta">{narrative.get("word_meta","")}</div>
      <div class="cult-desc">{narrative.get("word_desc","")}</div>
    </div>
    <div class="col-div">
      <div class="cult-eyebrow">Album of the month</div>
      <div class="cult-title">{narrative.get("album_title","")}</div>
      <div class="cult-meta">{narrative.get("album_meta","")}</div>
      <div class="cult-desc">{narrative.get("album_desc","")}</div>
    </div>
  </div>

</main>

<footer>
  <div style="display:flex;align-items:center;gap:14px;">
    <svg width="36" height="36" viewBox="0 0 52 52" fill="none">
      <rect width="52" height="52" rx="9" fill="#1C1C1C"/>
      <path d="M6,26 Q26,7 46,26 Q26,45 6,26 Z" stroke="#555" stroke-width="2" stroke-linecap="round" fill="none"/>
      <circle cx="26" cy="26" r="10" stroke="#555" stroke-width="1.8" fill="none"/>
      <circle cx="26" cy="26" r="4" fill="#555"/>
    </svg>
    <div>
      <div class="footer-wordmark">LUCID BY VINCE</div>
      <div class="footer-tagline">See what others miss.</div>
    </div>
  </div>
  <div class="footer-sources">
    Yahoo Finance &middot; FRED &middot; CNN Business &middot; MacroMicro &middot; Baltic Exchange &middot; GuruFocus &middot; multpl.com<br/>
    Data generated: {today_str} &middot; Market prices as of last available trading session<br/>
    Baltic Dry / CAPE / Buffett Indicator: approximate &mdash; verify before citing<br/>
    <span style="color:#333;font-style:italic;">&copy; Lucid by Vince &middot; {report_month} &middot; Not financial advice &middot; lucidbyvince.com</span>
  </div>
</footer>

</body>
</html>"""

# ─── SAVE HTML ─────────────────────────────────────────────────────────────────

with open("index.html", "w") as f:
    f.write(html)

print(f"\n✅ Generated index.html — {len(html):,} characters")
print(f"   Ready to deploy:")
print(f"   git add . && git commit -m '{report_month} report' && git push\n")

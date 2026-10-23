"""
Animus — sitio público / public site (English version).
Replica de landing.py en inglés, mismo theme.
"""
import base64
import os
import random

import streamlit as st

st.set_page_config(
    page_title="Animus — What you lived between sessions, on a map",
    page_icon=os.path.join(os.path.dirname(__file__), "favicon.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

NAVY = "#1f2947"
TEAL = "#3fb0a0"
CYAN = "#a9d6d9"
CORAL = "#e8725c"
ORANGE = "#f0a35e"
INK = "#22304e"
BODY = "#4a5468"
MIST = "#eef2f6"
LINE = "#dde3ec"

PAGES_DIR = os.path.join(os.path.dirname(__file__), "pdf_pages")
SHOTS_DIR = os.path.join(os.path.dirname(__file__), "app_shots")


def b64img(path: str) -> str:
    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def pg(i: int) -> str:
    return b64img(os.path.join(PAGES_DIR, f"p{i}.png"))


def shot(name: str) -> str:
    return b64img(os.path.join(SHOTS_DIR, name))


def hero_scatter(cols: int = 14, rows: int = 9, seed: int = 11) -> str:
    rnd = random.Random(seed)
    w, h = 470, 360
    parts = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    for r in range(rows):
        y = 30 + r * (h - 50) / rows
        for c in range(cols):
            if rnd.random() < 0.42:
                continue
            x = 12 + c * (w - 24) / cols + rnd.uniform(-7, 7)
            rad = rnd.choice([4, 5, 6, 7, 9, 11, 13])
            roll = rnd.random()
            col = TEAL if roll < 0.45 else (CYAN if roll < 0.72 else CORAL)
            parts.append(
                f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad}" '
                f'fill="{col}" fill-opacity="0.92"/>')
    parts.append("</svg>")
    return "".join(parts)


def mini_scatter(seed: int = 4) -> str:
    rnd = random.Random(seed)
    w, h = 640, 300
    x0, y0, x1, y1 = 66, 34, w - 24, h - 44
    bands = [(x0 + (x1 - x0) * 6 / 24, x0 + (x1 - x0) * 12 / 24, "Morning"),
             (x0 + (x1 - x0) * 12 / 24, x0 + (x1 - x0) * 18 / 24, "Afternoon"),
             (x0 + (x1 - x0) * 18 / 24, x0 + (x1 - x0) * 24 / 24, "Night")]
    parts = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">',
             f'<rect x="{x0 - 50}" y="{y0 - 6}" width="{x1 - x0 + 74}" '
             f'height="{y1 - y0 + 20}" rx="10" fill="#ffffff"/>']
    parts.append(f'<text x="{x0 - 16}" y="{y0 - 12}" font-size="11" '
                 f'fill="#7c8698" text-anchor="middle">Early</text>')
    for bx0, bx1, lab in bands:
        parts.append(f'<rect x="{bx0:.0f}" y="{y0 - 6}" width="{bx1 - bx0:.0f}"'
                     f' height="{y1 - y0 + 20}" fill="#eef2f6"/>')
        parts.append(f'<text x="{(bx0 + bx1) / 2:.0f}" y="{y0 - 12}" '
                     f'font-size="11" fill="#7c8698" text-anchor="middle">'
                     f'{lab}</text>')
    days = [f"{d:02d}/10" for d in range(7, 21)]
    for i, d in enumerate(days):
        y = y0 + i * (y1 - y0) / len(days)
        parts.append(f'<text x="{x0 - 58}" y="{y + 3:.0f}" font-size="9" '
                     f'fill="#98a2b3">{d}</text>')
        parts.append(f'<line x1="{x0 - 46}" y1="{y:.0f}" x2="{x1}" '
                     f'y2="{y:.0f}" stroke="#f0f3f7" stroke-width="1"/>')
        for _ in range(rnd.randint(2, 7)):
            xx = rnd.uniform(x0, x1)
            rad = rnd.choice([4, 5, 6, 7, 9])
            roll = rnd.random()
            col = TEAL if roll < 0.5 else (CYAN if roll < 0.75 else CORAL)
            parts.append(f'<circle cx="{xx:.0f}" cy="{y:.0f}" r="{rad}" '
                         f'fill="{col}"/>')
    for hh in (0, 6, 12, 18, 24):
        xx = x0 + (x1 - x0) * hh / 24
        parts.append(f'<text x="{xx:.0f}" y="{y1 + 34}" font-size="11" '
                     f'fill="#7c8698" text-anchor="middle">{hh} h</text>')
    legend = [("Pleasant", TEAL), ("Calm", CYAN), ("Unpleasant", CORAL),
              ("Other", "#b9c0cc")]
    lx = x0 + 20
    for lab, col in legend:
        parts.append(f'<circle cx="{lx}" cy="{h - 8}" r="5" fill="{col}"/>')
        parts.append(f'<text x="{lx + 10}" y="{h - 4}" font-size="10" '
                     f'fill="#5b6474">{lab}</text>')
        lx += 96
    parts.append("</svg>")
    return "".join(parts)


def wordmark(color: str = "#ffffff", size: int = 30) -> str:
    d = size * 0.44
    return f'''
    <span class="wm" style="display:inline-flex;align-items:center;gap:{d * .38:.0f}px">
      <span style="width:{d:.0f}px;height:{d:.0f}px;border-radius:50%;
            background:{TEAL};display:inline-block"></span>
      <span style="width:{d:.0f}px;height:{d:.0f}px;border-radius:50%;
            background:{CYAN};display:inline-block"></span>
      <span style="width:{d:.0f}px;height:{d:.0f}px;border-radius:50%;
            background:{CORAL};display:inline-block"></span>
      <span style="font-family:'Playfair Display',Georgia,serif;
            font-weight:700;font-size:{size}px;color:{color};
            margin-left:{d * .5:.0f}px">animus</span>
    </span>'''


# ------------------------------------------------------------------- CSS

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&display=swap');

    html {{ scroll-behavior: smooth; }}
    html, body, [class*="css"] {{
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
        color: {INK};
    }}
    .main .block-container {{ padding: 0; max-width: 100%; }}
    .stApp {{ background: {NAVY}; }}
    section[data-testid="stMainBlockContainer"] {{
        padding-left: 0; padding-right: 0;
    }}
    header[data-testid="stHeader"] {{ display: none; }}
    #MainMenu, footer {{ visibility: hidden; }}
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {{ display: none !important; }}

    .sec {{ padding: 76px 72px; }}
    .sec-navy {{ background: {NAVY}; color: #e8edf6; }}
    .sec-light {{ background: {MIST}; }}
    .sec-white {{ background: #fff; }}
    .kicker {{ color: {TEAL}; font-size: 14px; font-weight: 600;
               letter-spacing: .4px; margin-bottom: 10px; }}
    .sec h1, .sec h2 {{
        font-family:'Playfair Display',Georgia,serif;
        font-weight: 700; color: {NAVY}; margin: 0 0 14px;
        line-height: 1.12;
    }}
    .sec-navy h1, .sec-navy h2 {{ color: #fff; }}
    .sec h2 {{ font-size: 44px; }}
    .lede {{ font-size: 16.5px; color: {BODY}; line-height: 1.6;
             max-width: 620px; }}
    .sec-navy .lede {{ color: #b9c3d6; }}

    .hero-top {{
        display:flex; justify-content:space-between; align-items:center;
        padding: 34px 72px 0;
    }}
    .hero-nav a {{
        color: #dfe5f0; text-decoration:none; font-size:14.5px;
        margin-left: 34px;
    }}
    .hero-nav a:hover {{ color:#fff; }}
    .hero-grid {{
        display:grid; grid-template-columns: 1.05fr .95fr;
        gap: 40px; align-items:center;
        padding: 30px 72px 46px;
    }}
    .hero h1 {{
        font-family:'Playfair Display',Georgia,serif;
        font-size: 64px; font-weight:700; color:#fff;
        line-height:1.08; margin:0 0 22px;
    }}
    .hero-sub {{
        font-size:17.5px; color:#c3ccdc; line-height:1.6;
        max-width:480px; margin-bottom:34px;
    }}
    .cta-row {{ display:flex; gap:14px; align-items:center; }}
    .btn {{
        display:inline-block; text-decoration:none;
        padding:13px 30px; border-radius:999px;
        font-size:15px; font-weight:600;
    }}
    a.btn, a.btn:visited, a.btn:hover {{ text-decoration:none; }}
    a.btn-teal {{ background:{TEAL}; color:#fff !important; }}
    a.btn-ghost {{ border:1.5px solid rgba(255,255,255,.55);
                  color:#fff !important; }}
    a.btn-ghost-cyan {{ border:1.5px solid {CYAN}; color:{CYAN} !important; }}
    a.btn-white {{ background:#fff; color:{NAVY} !important; }}
    a.btn-coral {{ background:{CORAL}; color:#fff !important; }}
    .hero-note {{ font-size:13px; color:#8d97ad; margin-top:18px; }}
    .scatter-cap {{ font-size:12.5px; color:#98a2b6; text-align:right;
                    line-height:1.5; max-width:420px; margin-left:auto; }}

    .vs-wrap {{ display:flex; gap:26px; margin-top:38px; }}
    .vs-card {{
        flex:1; border-radius:14px; padding:30px 30px;
        font-family:'Playfair Display',Georgia,serif;
        font-size:23px; line-height:1.7; font-weight:600;
        text-align:center;
    }}
    .vs-card .vs-tag {{
        font-family:'Inter',sans-serif; font-size:16.5px;
        font-weight:700; display:block; margin-bottom:18px;
        text-align:left;
    }}
    .vs-out {{ background:#fff; border:1px solid {LINE}; color:{NAVY}; }}
    .vs-out .vs-tag {{ color:#98a2b6; }}
    .vs-in {{ background:{NAVY}; color:#fff; }}
    .vs-in .vs-tag {{ color:{CYAN}; }}
    .stats {{ display:flex; justify-content:space-between;
              margin-top:70px; }}
    .stat .num {{
        font-family:'Playfair Display',Georgia,serif;
        font-size:56px; font-weight:700; color:{CORAL}; line-height:1;
    }}
    .stat .cap {{ font-size:14px; color:{BODY}; margin-top:10px;
                 max-width:220px; line-height:1.5; }}
    .week-top {{ display:grid; grid-template-columns:1.05fr .95fr;
                 gap:48px; align-items:center; }}
    .shotfan {{ position:relative; height:470px; }}
    .shotfan img {{
        position:absolute; width:31%; border-radius:14px;
        box-shadow:0 18px 40px rgba(31,41,71,.30);
        border:3px solid {NAVY};
    }}
    .shotfan .s1 {{ left:0;   top:52px; transform:rotate(-7deg); }}
    .shotfan .s2 {{ left:35%; top:0;    transform:rotate(-1deg);
                    z-index:2; }}
    .shotfan .s3 {{ right:0;  top:58px; transform:rotate(6deg); }}

    .steps {{ display:grid; grid-template-columns:1fr 1fr 1fr;
              gap:56px; margin-top:56px; }}
    .stepnum {{
        width:70px;height:70px;border-radius:50%;
        background:{NAVY}; color:#fff;
        font-family:'Playfair Display',serif; font-size:34px;
        font-weight:700; text-align:center; line-height:70px;
        margin-bottom:26px;
    }}
    .steps h3 {{ font-family:'Playfair Display',serif; font-size:22px;
                 color:{NAVY}; margin:0 0 10px; }}
    .steps p {{ font-size:14.5px; color:{BODY}; line-height:1.6;
               margin:0 0 18px; max-width:300px; }}
    .chip {{
        display:inline-block; border:1px solid #cfd6e0; border-radius:999px;
        padding:6px 16px; font-size:13px; color:{BODY}; margin:0 8px 10px 0;
        background:#fff;
    }}
    .prompt-card {{
        background:{NAVY}; border-radius:14px; padding:24px 26px;
        color:#fff; max-width:330px;
    }}
    .prompt-card .pc-brand {{ font-size:13px; color:{CYAN}; margin-bottom:10px; }}
    .prompt-card .pc-q {{ font-family:'Playfair Display',serif;
        font-size:20px; line-height:1.4; margin-bottom:18px; }}
    .pc-btn {{ display:inline-block; border-radius:999px; padding:8px 22px;
               font-size:13.5px; font-weight:600; margin-right:10px; }}
    .pc-yes {{ background:{TEAL}; color:#fff; }}
    .pc-no {{ border:1.5px solid rgba(255,255,255,.6); color:#fff; }}
    .rulebar {{ margin-bottom:22px; }}
    .rulebar .rb-label {{ font-size:14.5px; font-weight:600; color:{INK};
                          margin-bottom:8px; }}
    .rulebar .rb-bar {{ height:14px; border-radius:99px; }}
    .rulebar .rb-cap {{ font-size:12.5px; color:#8d97ab; margin-top:7px; }}

    .report-grid {{ display:grid; grid-template-columns: .9fr 1.1fr;
                    gap:50px; align-items:center; }}
    .pagelist {{ list-style:none; padding:0; margin:34px 0 60px; }}
    .pagelist li {{
        font-size:19px; color:#eef1f7; margin-bottom:22px;
        display:flex; align-items:center; gap:16px;
        font-weight:500;
    }}
    .pagelist .dot {{ width:16px;height:16px;border-radius:50%;
                      flex-shrink:0; }}
    .fan {{ position:relative; height:460px; }}
    .fan img {{
        position:absolute; width:46%; border-radius:6px;
        box-shadow:0 14px 34px rgba(0,0,0,.35); background:#fff;
    }}
    .fan .f1 {{ left:0;  top:60px;  transform:rotate(-7deg); }}
    .fan .f2 {{ left:27%; top:0;    transform:rotate(-1deg); z-index:2; }}
    .fan .f3 {{ right:0; top:70px;  transform:rotate(6deg); }}
    .reportgal {{ margin-top:34px; text-align:center; }}
    .reportgal summary {{
        display:inline-block; list-style:none; cursor:pointer;
        background:{CORAL}; color:#fff; border:1.5px solid {CORAL};
        border-radius:999px; padding:15px 36px;
        font-size:16px; font-weight:700;
    }}
    .reportgal summary::-webkit-details-marker {{ display:none; }}
    .reportgal summary:hover {{ filter:brightness(.93); }}
    .galgrid {{ display:grid; grid-template-columns:repeat(3,1fr);
                gap:22px; margin-top:30px; }}
    .galgrid img {{ width:100%; border-radius:8px;
                    box-shadow:0 12px 30px rgba(0,0,0,.35);
                    background:#fff; }}

    .benefits {{ display:grid; grid-template-columns:1fr 1fr; gap:60px;
                 align-items:start; }}
    .benefit h4 {{ font-size:17px; font-weight:700; color:{NAVY};
                   margin:0 0 8px; }}
    .benefit p {{ font-size:15px; color:{BODY}; line-height:1.6;
                  margin:0 0 30px; max-width:460px; }}
    .sideimg {{ width:100%; max-width:400px; border-radius:10px;
                box-shadow:0 16px 40px rgba(31,41,71,.25); display:block;
                margin:0 auto; background:#fff; }}
    .sidecap {{ text-align:center; font-size:14px; color:{BODY};
                max-width:380px; margin:22px auto 0; line-height:1.6; }}
    .nochips {{ margin-top:44px; text-align:center; line-height:3.1; }}
    .nochips .chip {{ background:#fff; margin:0 6px; }}

    .mini {{ border-radius:12px; padding:20px 24px; }}
    .mini-navy {{ background:{NAVY}; color:#fff; }}
    .mini-navy .big {{ font-family:'Playfair Display',serif; font-size:34px;
                       font-weight:700; white-space:nowrap; }}
    .mini-navy p {{ color:#c3ccdc; font-size:13.5px; margin:6px 0 0; }}
    .mini-mist {{ background:{MIST}; }}
    .mini-mist .mt {{ font-weight:700; font-size:15px; color:{NAVY}; }}
    .mini-mist p {{ color:{BODY}; font-size:13.5px; margin:6px 0 0;
                    line-height:1.5; }}
    .twocard {{ display:grid; grid-template-columns:1fr 1fr; gap:18px;
                margin-top:18px; }}
    .dayrow {{ display:grid; grid-template-columns:repeat(4,1fr); gap:0;
        border-top:1.5px solid {LINE}; margin-top:64px; padding-top:30px;
    }}
    .dayrow > div {{ padding:0 26px; }}
    .dayrow > div:not(:first-child) {{ border-left:1.5px solid {LINE}; }}
    .dayrow > div:first-child {{ padding-left:0; }}
    .dayrow .dbar {{ height:4px; width:38px; border-radius:4px;
                     margin-bottom:14px; }}
    .dayrow h5 {{ font-size:15px; font-weight:700; color:{NAVY};
                  margin:0 0 6px; }}
    .dayrow p {{ font-size:13.5px; color:{BODY}; margin:0; }}

    .priv-cols {{ display:grid; grid-template-columns:repeat(5,1fr);
                  gap:44px; margin-top:44px; }}
    .priv-col .bar {{ height:4px; border-radius:4px; margin-bottom:18px; }}
    .priv-col h4 {{ color:#fff; font-size:16.5px; margin:0 0 8px;
                    font-weight:700; }}
    .priv-col p {{ color:#b9c3d6; font-size:13.5px; line-height:1.6;
                   margin:0; }}
    .isnot {{ display:grid; grid-template-columns:1fr 1fr; gap:40px;
              margin-top:76px; }}
    .isnot h4 {{ font-size:15px; font-weight:700; margin:0 0 20px; }}
    .isnot .yes h4 {{ color:{TEAL}; }}
    .isnot .no h4 {{ color:{CORAL}; }}
    .isnot ul {{ list-style:none; padding:0; margin:0; }}
    .isnot li {{ font-size:17px; padding:9px 0; font-weight:500; }}
    .isnot .yes li {{ color:#eef1f7; }}
    .isnot .no li {{ color:#aeb8cb; }}
    .priv-foot {{ color:#98a2b6; font-size:14px; margin-top:70px; }}

    .closing {{
        background: linear-gradient(95deg, {NAVY} 42%, #2f8f84 88%);
        color:#fff; padding:60px 72px 40px; text-align:center;
    }}
    .closing h2 {{
        font-family:'Playfair Display',serif; font-size:52px;
        font-weight:700; line-height:1.12; margin:70px auto 44px;
        max-width:700px;
    }}
    .closing .cta-row {{ justify-content:center; }}
    .closing .foot {{ color:#c9d3d2; font-size:12.5px; margin:110px auto 0;
                      max-width:720px; line-height:1.6; }}

    .faq h3 {{ font-family:'Playfair Display',serif; font-size:26px;
               font-weight:700; color:{NAVY}; margin:56px 0 30px;
               padding-top:44px; border-top:1.5px solid {LINE}; }}
    .faq h3:first-of-type {{ margin-top:10px; }}
    details.qa {{ max-width:860px; margin-bottom:14px;
                  border-bottom:1px solid {LINE}; padding-bottom:14px; }}
    details.qa summary::-webkit-details-marker {{ display:none; }}
    details.qa .q {{ font-family:'Playfair Display',serif; font-size:19px;
              font-weight:700; color:{NAVY}; margin:0;
              padding:6px 40px 6px 18px; border-left:4px solid {TEAL};
              line-height:1.3; cursor:pointer; list-style:none;
              position:relative; }}
    details.qa.alt .q {{ border-left-color:{CORAL}; }}
    details.qa .q::after {{
        content:"+"; position:absolute; right:8px; top:2px;
        font-family:'Inter',sans-serif; font-size:26px; font-weight:400;
        color:{TEAL};
    }}
    details.qa.alt .q::after {{ color:{CORAL}; }}
    details.qa[open] .q::after {{ content:"−"; }}
    details.qa .a {{ font-size:14.5px; color:{BODY}; line-height:1.65;
              padding:12px 22px 4px; margin:0; }}
    .qa .a b, details.qa .a b {{ color:{NAVY}; }}
    .scinote {{ background:{MIST}; border:1px solid {LINE};
                border-radius:14px; padding:24px 28px; margin-top:40px;
                max-width:900px; font-size:13.5px; color:{BODY};
                line-height:1.65; }}
    .scinote b {{ color:{NAVY}; }}
    .faq-foot {{ color:{BODY}; font-size:12.5px; margin-top:60px;
                 max-width:720px; line-height:1.6; }}

    .abc {{ display:grid; grid-template-columns:repeat(3,1fr);
            gap:26px; margin-top:56px; }}
    .abc-card {{
        background:#fff; border:1px solid {LINE};
        border-radius:14px; padding:30px 28px;
        border-top:5px solid {TEAL};
    }}
    .abc-card.b {{ border-top-color:{CYAN}; }}
    .abc-card.c {{ border-top-color:{CORAL}; }}
    .abc-card .letter {{
        font-family:'Playfair Display',serif; font-size:46px;
        font-weight:700; line-height:1; margin-bottom:6px;
    }}
    .abc-card .letter em {{
        font-style:normal; font-size:17px; font-weight:700;
        display:block; margin-top:6px; color:{NAVY};
        font-family:'Inter',sans-serif;
    }}
    .abc-card.a .letter {{ color:{TEAL}; }}
    .abc-card.b .letter {{ color:#7fb8bb; }}
    .abc-card.c .letter {{ color:{CORAL}; }}
    .abc-card .letter em {{ color:{NAVY}; }}
    .abc-card p {{ font-size:14px; color:{BODY}; line-height:1.6;
                    margin:12px 0 0; }}
    .abc-tag {{ font-size:12px; font-weight:600; letter-spacing:.6px;
                 text-transform:uppercase; margin-bottom:14px; }}
    .abc-card.a .abc-tag {{ color:{TEAL}; }}
    .abc-card.b .abc-tag {{ color:#7fb8bb; }}
    .abc-card.c .abc-tag {{ color:{CORAL}; }}

    .abc-split {{ display:grid; grid-template-columns:1.05fr .95fr;
                   gap:56px; margin-top:70px; align-items:center; }}
    .abc-why h3 {{ font-family:'Playfair Display',serif; font-size:28px;
                    font-weight:700; color:{NAVY}; margin:0 0 20px; }}
    .abc-why ul {{ list-style:none; padding:0; margin:0; }}
    .abc-why li {{ font-size:15px; color:{BODY}; line-height:1.65;
                    padding:11px 0 11px 26px; position:relative; }}
    .abc-why li::before {{ content:''; position:absolute; left:0;
                    top:19px; width:10px; height:10px;
                    border-radius:50%; }}
    .abc-why li:nth-child(1)::before {{ background:{TEAL}; }}
    .abc-why li:nth-child(2)::before {{ background:{CYAN}; }}
    .abc-why li:nth-child(3)::before {{ background:{CORAL}; }}
    .abc-why li:nth-child(4)::before {{ background:{ORANGE}; }}
    .abc-why li b {{ color:{NAVY}; }}
    .abc-close {{ margin-top:26px; font-family:'Playfair Display',serif;
                   font-size:17px; font-style:italic; color:{NAVY};
                   line-height:1.5; }}
    .shotfan4 {{ position:relative; height:400px; }}
    .shotfan4 img {{
        position:absolute; width:25%; border-radius:14px;
        box-shadow:0 16px 36px rgba(31,41,71,.30);
        border:3px solid {NAVY};
    }}
    .shotfan4 .t1 {{ left:0;   top:60px; transform:rotate(-7deg); }}
    .shotfan4 .t2 {{ left:25%; top:0;    transform:rotate(-2deg);
                      z-index:2; }}
    .shotfan4 .t3 {{ left:50%; top:56px; transform:rotate(4deg); }}
    .shotfan4 .t4 {{ left:75%; top:18px; transform:rotate(8deg); }}

    .abc-patterns {{ margin-top:64px; display:grid;
                      grid-template-columns:1fr auto; gap:64px;
                      align-items:center; }}
    .abc-logo {{ display:flex; align-items:center; }}
    .abc-patterns h3 {{ font-family:'Playfair Display',serif;
                         font-size:26px; font-weight:700; color:{NAVY};
                         margin:0 0 16px; }}
    .abc-patterns p {{ font-size:15px; color:{BODY}; line-height:1.7;
                        margin:0 0 16px; }}

    .abc-top {{ display:grid; grid-template-columns:1.05fr .95fr;
                 gap:48px; align-items:center; }}
    .abc-patterns .cols {{ display:grid;
                            grid-template-columns:1fr 1fr; gap:52px; }}


    .sitefoot {{ background:{NAVY}; padding:70px 7vw 40px; }}
    .foot-grid {{ display:grid; grid-template-columns:1.4fr 1fr 1fr;
                  gap:48px; max-width:1200px; margin:0 auto; }}
    .sitefoot .fnote {{ color:#8f9bb8; font-size:14px; line-height:1.6;
                        margin-top:18px; max-width:340px; }}
    .sitefoot h6 {{ font-family:'Playfair Display',serif; color:#fff;
                    font-size:15px; margin-bottom:16px; }}
    .sitefoot ul {{ list-style:none; }}
    .sitefoot li {{ margin-bottom:10px; }}
    .sitefoot a {{ color:#b9c3d6; font-size:14px; text-decoration:none; }}
    .sitefoot a:hover {{ color:#fff; }}
    .foot-base {{ max-width:1200px; margin:44px auto 0;
                  padding-top:22px;
                  border-top:1px solid rgba(255,255,255,.12);
                  display:flex; justify-content:space-between;
                  flex-wrap:wrap; gap:12px;
                  color:#7d89a8; font-size:12.5px; }}
    .mnav {{ display:none; }}
    .msent {{ position:fixed; top:0; left:0; width:0; height:0; }}
    @media (max-width: 900px) {{
        .sec {{ padding:56px 28px; }}
        .hero-top, .hero-grid {{ padding-left:28px; padding-right:28px; }}
        .hero-grid, .steps, .benefits, .report-grid, .isnot,
        .week-top {{
            grid-template-columns:1fr; }}
        .hero h1 {{ font-size:42px; }}
        .sec h2 {{ font-size:32px; }}
        .priv-cols {{ grid-template-columns:1fr 1fr; }}
        .dayrow {{ grid-template-columns:1fr 1fr; }}
        .galgrid {{ grid-template-columns:1fr 1fr; }}
        .abc {{ grid-template-columns:1fr; }}
        .abc-split {{ grid-template-columns:1fr; gap:30px; margin-top:16px; }}
        .shotfan4 {{ height:300px; }}
        .abc-top {{ grid-template-columns:1fr; }}
        .abc-patterns .cols {{ grid-template-columns:1fr; gap:0; }}
        .abc-patterns {{ grid-template-columns:1fr; gap:24px; }}
        .foot-grid {{ grid-template-columns:1fr; gap:32px; }}
        .abc-logo {{ justify-content:flex-start; }}
        .shotfan {{ height:360px; }}
        .stats {{ flex-wrap:wrap; gap:36px; }}
        .stat .num {{ font-size:44px; }}
        .closing h2 {{ font-size:36px; }}
        .hero-nav {{ display:none; }}
        html, body {{ overflow-x:hidden; }}
        svg {{ max-width:100%; height:auto; }}
        .wm {{ transform:scale(.8); transform-origin:left center; }}
        .sec3h2 {{ text-align:left !important; min-width:0 !important; }}
        [data-testid="stAppViewContainer"] {{ overflow-x:hidden; }}
        .fan, .shotfan, .shotfan4 {{ overflow:hidden; }}
        .twocard {{ flex-direction:column; }}
        .vs-wrap {{ flex-direction:column; }}
        .week-cards {{ grid-template-columns:1fr; }}
        .wordmark-wrap {{ flex-wrap:wrap; }}
    }}
    @media (max-width: 640px) {{
        .sec {{ padding:44px 20px; }}
        .hero-top {{ padding:52px 20px 36px; }}
        .hero-grid {{ padding:0 20px; }}
        .closing {{ padding:44px 20px 32px; }}
        .sitefoot {{ padding:44px 20px 32px; }}
        .hero h1 {{ font-size:34px; }}
        .sec h2 {{ font-size:28px; }}
        .closing h2 {{ font-size:30px; }}
        .stat .num {{ font-size:36px; }}
        .stats {{ gap:24px; }}
        .cta-row {{ flex-direction:column; align-items:stretch; }}
        .cta-row .btn {{ text-align:center; }}
        .shotfan {{ height:300px; }}
        .shotfan4 {{ height:260px; }}
        .fan {{ height:300px; }}
        .galgrid {{ grid-template-columns:1fr; }}
        .dayrow {{ grid-template-columns:1fr; }}
        .priv-cols {{ grid-template-columns:1fr; }}
        .steps {{ gap:36px; margin-top:20px; }}
        .abc-logo {{ transform:scale(.85); transform-origin:left; }}
        .wm {{ transform:scale(.62); }}
        .hero-top .wm {{ transform:scale(1.7); transform-origin:left center; }}
        .stats {{ justify-content:center; }}
        .stat {{ text-align:center; }}
        .stat .cap {{ margin-left:auto; margin-right:auto; }}
        .vs-card {{ font-size:17px; padding:24px 20px; }}
        .vs-card .vs-tag {{ font-size:14px; }}
        .mini .big {{ font-size:32px; }}
        .hero-sub {{ font-size:15px; }}
        details.qa .q {{ font-size:16px; }}
        .faq h3 {{ font-size:22px; }}
        .foot-base {{ flex-direction:column; }}
        .nochips {{ gap:10px; }}
        .chip {{ font-size:12px; }}
        .btn {{ padding:14px 26px; font-size:15px; }}

        /* stats fuera en teléfono */
        .stats {{ display:none; }}

        /* logo ABC: centrado y grande */
        .abc-logo {{ justify-content:center; transform:none; }}
        .abc-logo {{ overflow:hidden; }}
        div:has(> .wm) {{ max-width:100%; overflow:hidden; }}
        .abc-logo .wm {{ transform:scale(.9); transform-origin:center; }}

        /* pasos: número + título en una línea */
        .steps > div {{ display:flex; flex-wrap:wrap;
                        align-items:center; column-gap:16px; row-gap:14px; }}
        .stepnum {{ width:42px; height:42px; font-size:19px; flex:0 0 42px; line-height:39px; margin-bottom:0; }}
        .steps > div > *:nth-child(2) {{ flex:1; min-width:0; }}
        .steps > div > *:nth-child(n+3) {{ flex:0 0 100%; }}
        .steps h3 {{ margin:0; }}

        /* menos aire muerto */
        .benefits h2 {{ margin-bottom:24px !important; }}
        .sec h2 {{ margin-bottom:20px; }}
        .sec {{ padding:40px 20px; }}
        .shotfan {{ height:280px; }}
        .fan {{ height:280px; }}

        /* menú flotante: botón con los 3 puntos que despliega enlaces */
        .mnav {{ display:block; position:fixed; right:16px;
                 top:16px; z-index:9999; }}
        .mfab {{ width:56px; height:56px; border-radius:50%;
                 background:{NAVY};
                 display:flex; align-items:center; justify-content:center;
                 gap:6px; text-decoration:none;
                 border:2px solid rgba(255,255,255,.75);
                 box-shadow:0 8px 22px rgba(11,17,38,.5); }}
        .mfab i {{ width:9px; height:9px; border-radius:50%;
                   display:block; }}
        .mfab-x {{ display:none; color:{CYAN}; font-size:20px;
                   font-weight:700; font-family:sans-serif; }}
        .mlinks {{ display:none; position:absolute; right:0; top:66px;
                   flex-direction:column; min-width:196px;
                   background:#131b36;
                   border:1px solid rgba(255,255,255,.13);
                   border-radius:18px; padding:8px;
                   box-shadow:0 14px 34px rgba(11,17,38,.55); }}
        .mlinks a {{ display:block; color:#eef1f7; text-decoration:none;
                     font-size:15px; font-weight:600; padding:12px 16px;
                     border-radius:12px; }}
        .mlinks a:active {{ background:rgba(255,255,255,.09);
                            color:{ORANGE}; }}
        .mlinks a:last-child {{ color:{ORANGE}; }}
        #mopen:target ~ .mlinks {{ display:flex; }}
        #mopen:target ~ .mfab-open {{ display:none; }}
        #mopen:target ~ .mfab-x {{ display:flex; }}
        .sitefoot {{ padding-bottom:100px; }}
    }}
    header[data-testid="stHeader"] {{ display:none; }}
    [data-testid="stToolbar"], .stAppDeployButton,
    [data-testid="stDecoration"], #MainMenu,
    [data-testid="stStatusWidget"], [data-testid="stToolbarActions"],
    [data-testid="manage-app-button"], [class*="viewerBadge"],
    [class*="ViewerBadge"], [data-testid="stAppDeployButton"]
    {{ display:none !important; }}
    [data-testid="stMainBlockContainer"] {{ padding-top:1.4rem; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ===================== 1 · HERO (navy)

st.markdown(
    f"""
    <div class="sec-navy">
        <div class="hero-top">
            {wordmark()}
            <nav class="hero-nav">
                <a href="#informe">The report</a>
                <a href="#terapeutas">For therapists</a>
                <a href="#parati">For you</a>
                <a href="#privacidad">Privacy</a>
                <a href="#faq">FAQ</a>
                <a href="?lang=es" target="_self"
                   style="border:1.5px solid {ORANGE}; color:{ORANGE};
                          border-radius:999px; padding:5px 14px">ES</a>
            </nav>
        </div>
        <div class="hero hero-grid">
            <div>
                <h1>What you lived<br>between sessions,<br>finally on a
                    map.</h1>
                <div class="hero-sub">
                    Animus records what your body and your phone already
                    know, asks you at the right moment and turns it into
                    a report you and your therapist can read together.
                </div>
                <div class="cta-row">
                    <a class="btn btn-teal" href="#parati">I'm a client</a>
                    <a class="btn btn-coral" href="#terapeutas">I'm a
                        therapist</a>
                </div>
                <div class="hero-note">For Android. Your data stays on
                    your phone.</div>
            </div>
            <div>
                {hero_scatter()}
                <div class="scatter-cap">Sample data: each dot is a
                record, the color is the emotion and the size is its
                intensity. Each row is a day.</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 2 · "HOW WAS YOUR WEEK?" (mist)

st.markdown(
    f"""
    <div class="sec sec-light">
        <div class="week-top">
            <div>
                <h2>"How was your<br>week?" depends on<br>what you manage
                    to remember.</h2>
                <p class="lede" style="margin-top:26px">
                    The session arrives filtered by your memory, by your
                    mood on appointment day and by how you tell it.
                    Animus keeps what happened when it happened.
                </p>
            </div>
            <div class="shotfan">
                <img class="s1" src="data:image/jpeg;base64,{shot('ejercicios.jpg')}" alt="Exercises">
                <img class="s2" src="data:image/jpeg;base64,{shot('hoy.jpg')}" alt="Today">
                <img class="s3" src="data:image/jpeg;base64,{shot('metricas.jpg')}" alt="Metrics">
            </div>
        </div>
        <div class="vs-wrap">
            <div class="vs-card vs-out">
                <span class="vs-tag">What reaches the consulting room</span>
                What you remember<br>
                How you feel that day<br>
                How you manage to tell it
            </div>
            <div class="vs-card vs-in">
                <span class="vs-tag">What arrives with Animus</span>
                Records made in the moment<br>
                Situation, emotion and intensity<br>
                Every finding with its case count
            </div>
        </div>
        <div class="stats">
            <div class="stat"><div class="num">9 of 9</div>
                <div class="cap">Family records were
                    unpleasant</div></div>
            <div class="stat"><div class="num">44%</div>
                <div class="cap">of records in the afternoon, vs 16% at
                    night</div></div>
            <div class="stat"><div class="num" style="font-size:50px;
                white-space:nowrap">3 h 29 min</div>
                <div class="cap">median time to return to
                    calm</div></div>
            <div class="stat"><div class="num">14 of 30</div>
                <div class="cap">days with data in the period — the rest
                    are shown as absent, not as "zero"
                    days</div></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 3 · OBSERVA, PREGUNTA Y APRENDE (blanco)

st.markdown(
    f"""
    <div class="sec sec-white">
        <div style="display:flex;justify-content:space-between;
                    align-items:center;gap:48px;flex-wrap:wrap;
                    margin-bottom:20px">
            <div>{wordmark(color=INK, size=66)}</div>
            <h2 class="sec3h2" style="text-align:right;flex:1;min-width:300px">It watches,
                asks and learns.<br>You only answer the brief part.</h2>
        </div>
        <div class="steps">
            <div>
                <div class="stepnum">1</div>
                <h3>It watches your context</h3>
                <p>Sleep, steps, phone use and — with your permission —
                pulse and calendar. Everything stays on your device.</p>
                <span class="chip">Sleep</span>
                <span class="chip">Steps</span>
                <span class="chip">Phone use</span>
                <span class="chip">Pulse (with sensor)</span>
            </div>
            <div>
                <div class="stepnum">2</div>
                <h3>It asks in the moment</h3>
                <p>If your pulse changes at rest, it asks what happened
                and gives you the exact time to anchor the memory.</p>
                <div class="prompt-card">
                    <div class="pc-brand">Animus</div>
                    <div class="pc-q">Did something happen around
                        19:34?</div>
                    <span class="pc-btn pc-yes">Yes, it did</span>
                    <span class="pc-btn pc-no">It didn't</span>
                </div>
            </div>
            <div>
                <div class="stepnum">3</div>
                <h3>It learns your patterns</h3>
                <p>Every finding shows how many times it occurred. With
                fewer than 5 cases it's a hint, not a pattern.</p>
                <div class="rulebar">
                    <div class="rb-label">Family: 9 of 9 unpleasant</div>
                    <div class="rb-bar" style="width:100%;background:{CORAL}"></div>
                    <div class="rb-cap">Pattern, 9 cases</div>
                </div>
                <div class="rulebar">
                    <div class="rb-label">Money: 2 of 3 with anxiety</div>
                    <div class="rb-bar" style="width:33%;background:#c3ccd9"></div>
                    <div class="rb-cap">Hint, 3 cases</div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 3.5 · THE ABC IN ANIMUS (mist)

st.markdown(
    f"""
    <div class="sec sec-light">
        <div class="kicker">The record that orders everything</div>
        <div class="abc-top">
            <div>
        <h2>The ABC of your behavior,<br>recorded in real time.</h2>
        <p class="lede" style="margin-top:20px">
            Every episode in Animus is structured around the ABC
            model of functional behavior analysis (FBA): an approach
            backed by behavioral research that examines how events
            before and after a response influence its occurrence and
            repetition. Instead of relying on later recall, Animus
            records each episode with exact time, context and
            sequence — to surface real patterns between situations,
            emotions and consequences.
        </p>
            </div>
            <div class="shotfan">
                <img class="s1" src="data:image/jpeg;base64,{shot('hoy_ansiedad.jpg')}" alt="Anxiety">
                <img class="s2" src="data:image/jpeg;base64,{shot('hoy_neutro.jpg')}" alt="Today">
                <img class="s3" src="data:image/jpeg;base64,{shot('hoy_alegria.jpg')}" alt="Joy">
            </div>
        </div>
        <div class="abc">
            <div class="abc-card a">
                <div class="abc-tag">Antecedent</div>
                <div class="letter">A<em>What happened just before</em></div>
                <p>Record the situation, person, place or demand that
                preceded the episode. Animus already captures the
                time, sleep and activity automatically; you just
                describe the context in a short phrase or a tap.
                Antecedents are events that can evoke or increase the
                likelihood of an emotional or behavioral response.</p>
            </div>
            <div class="abc-card b">
                <div class="abc-tag">Behavior</div>
                <div class="letter">B<em>What you felt and did</em></div>
                <p>Record the emotion, its 0-to-10 intensity, the
                affected life area and the concrete response you had.
                Two taps when in a hurry, a note when you want more
                context. Behavior here means an observable, measurable
                response within a specific situation.</p>
            </div>
            <div class="abc-card c">
                <div class="abc-tag">Consequence</div>
                <div class="letter">C<em>How you ended up</em></div>
                <p>Record what happened right after and how the
                episode ended. Recovery time comes from this — an
                indicator you later compare between weeks.
                Consequences are fundamental in FBA: they can maintain,
                reinforce or reduce the likelihood of a response
                occurring again.</p>
            </div>
        </div>
        <div class="abc-patterns">
            <div>
            <h3>From isolated episodes to functional patterns</h3>
            <div class="cols">
            <p>A single record describes a moment; repeating the ABC
            reveals contingencies: which situations tend to precede
            your episodes, which responses appear most often and which
            consequences follow. This logic comes from
            observation-based behavioral assessment, used to
            formulate functional hypotheses about the
            environment-behavior relationship.</p>
            <p>Animus applies that principle to daily life: it turns
            your records into structured data to spot trends,
            anticipate difficult situations and evaluate change over
            time. It does not replace a clinical evaluation or an
            experimental functional analysis, but uses their
            conceptual frame to help you understand your behavior
            with more precision and evidence.</p>
                </div>
            </div>
            <div class="abc-logo">{wordmark(color=INK, size=60)}</div>
        </div>
        <div class="abc-split">
            <div class="abc-why">
                <h3>Not a form.<br>A method.</h3>
                <ul>
                    <li><b>Decades of evidence.</b> The
                    antecedent-behavior-consequence structure has been
                    used in clinics since Bijou, Peterson &amp; Ault
                    (1968) and underpins functional analysis (Iwata et
                    al., <i>Journal of Applied Behavior
                    Analysis</i>).</li>
                    <li><b>In the moment, not from memory.</b> Answering
                    when it happens is ecological momentary assessment
                    (Shiffman, Stone &amp; Hufford, <i>Annual Review of
                    Clinical Psychology</i>, 2008) — it reduces recall
                    bias.</li>
                    <li><b>Anchored to your biometrics and context.</b>
                    While you log, Animus cross-references the episode
                    with what the phone already knows: sleep, steps,
                    screen time, calendar and — with a wearable — pulse
                    and variability.</li>
                    <li><b>It learns from your records.</b> Every
                    episode feeds the map: repetitions turn hints into
                    patterns you can discuss in session.</li>
                </ul>
            </div>
            <div class="shotfan4">
                <img class="t1" src="data:image/jpeg;base64,{shot('abc_a.jpg')}" alt="Antecedent">
                <img class="t2" src="data:image/jpeg;base64,{shot('abc_situacion.jpg')}" alt="Situation">
                <img class="t3" src="data:image/jpeg;base64,{shot('abc_intensidad.jpg')}" alt="Intensity">
                <img class="t4" src="data:image/jpeg;base64,{shot('abc_c.jpg')}" alt="Consequence">
            </div>
        </div>
        <div class="abc-close" style="text-align:center; margin-top:56px;
             margin-left:auto; margin-right:auto; max-width:820px">
            Designed under the principles of functional behavior
            analysis — that's why the report reads like evidence, not
            like a mood diary.</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 4 · THE REPORT (navy)

st.markdown(
    f"""
    <div class="sec sec-navy" id="informe">
        <div class="report-grid">
            <div>
                <h2>A 6-page report<br>ready for the<br>session.</h2>
                <ul class="pagelist">
                    <li><span class="dot" style="background:{TEAL}"></span>
                        Cover and the three strongest findings</li>
                    <li><span class="dot" style="background:{CORAL}"></span>
                        Situations and emotions</li>
                    <li><span class="dot" style="background:{ORANGE}"></span>
                        Rhythm of the day</li>
                    <li><span class="dot" style="background:{CYAN}"></span>
                        Sleep and recovery</li>
                    <li><span class="dot" style="background:{TEAL}"></span>
                        Body and relationship with tracking</li>
                    <li><span class="dot" style="background:{CORAL}"></span>
                        To test and to bring to the session</li>
                </ul>
                <div class="lede" style="font-size:15px">
                    Generated on your phone. Share it by WhatsApp or
                    email, or print it.
                </div>
            </div>
            <div class="fan">
                <img class="f1" src="data:image/png;base64,{pg(1)}">
                <img class="f3" src="data:image/png;base64,{pg(6)}">
                <img class="f2" src="data:image/png;base64,{pg(3)}">
            </div>
        </div>
        <details class="reportgal">
            <summary>See the full 6 pages of the sample report</summary>
            <div class="galgrid">
                <img src="data:image/png;base64,{pg(1)}" alt="Page 1">
                <img src="data:image/png;base64,{pg(2)}" alt="Page 2">
                <img src="data:image/png;base64,{pg(3)}" alt="Page 3">
                <img src="data:image/png;base64,{pg(4)}" alt="Page 4">
                <img src="data:image/png;base64,{pg(5)}" alt="Page 5">
                <img src="data:image/png;base64,{pg(6)}" alt="Page 6">
            </div>
        </details>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 5 · FOR THERAPISTS (mist)

st.markdown(
    f"""
    <div class="sec sec-light" id="terapeutas">
        <div class="kicker">For therapists</div>
        <div class="benefits">
            <div>
                <h2 style="margin-bottom:60px">The session starts<br>with
                    data, not with<br>memory.</h2>
                <div class="benefit"><h4>Hypotheses that can be
                    tested</h4>
                    <p>Formulate a case hypothesis and contrast it with
                    the actual record of the period. The result arrives
                    separated: what held, what didn't and with how many
                    cases — your clinical impression is put to the test
                    without contaminating the record.</p></div>
                <div class="benefit"><h4>Questions for the session</h4>
                    <p>The last page pairs key data with questions drawn
                    from that client's map. Each question arrives with
                    the number that motivated it, so the conversation
                    starts with what most needs looking at.</p></div>
                <div class="benefit"><h4>Intervention follow-up</h4>
                    <p>You propose a change and the following week you
                    see whether the proportion in that time band
                    dropped. The same map serves as before/after: same
                    client, same bands, different period.</p></div>
                <div class="benefit"><h4>Complete episodes</h4>
                    <p>Antecedent, what was done afterwards, life area
                    and intensity, noted in the moment. What happened
                    before, the response and what came next stay chained
                    — the ABC already ordered for reading.</p></div>
                <div class="benefit"><h4>False positives in sight</h4>
                    <p>Every confirmed or dismissed signal is counted:
                    the instrument's precision is visible. When the
                    client dismisses a signal, the report shows how much
                    it was wrong — honesty is also measured.</p></div>
            </div>
            <div>
                <img class="sideimg" src="data:image/png;base64,{pg(6)}">
                <div class="sidecap">Not a remote monitor: you receive
                the report when the client decides to share it.</div>
            </div>
        </div>
        <div class="nochips">
            <span class="chip">Doesn't diagnose</span>
            <span class="chip">Doesn't replace your clinical
                judgment</span>
            <span class="chip">Doesn't detect emotions from pulse</span>
            <span class="chip">Doesn't infer causes — correlation isn't
                causation</span>
            <span class="chip">Doesn't send data without permission</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 6 · FOR YOU (blanco)

st.markdown(
    f"""
    <div class="sec sec-white" id="parati">
        <div class="kicker">For you</div>
        <div class="benefits">
            <div>
                <h2 style="margin-bottom:60px">Know yourself with<br>your
                    own numbers.</h2>
                <div class="benefit"><h4>You see what you don't
                    remember</h4>
                    <p>The situations that repeat stay in sight, even
                    when memory edits them.</p></div>
                <div class="benefit"><h4>You measure your recovery</h4>
                    <p>How long you take to return to calm is a number
                    you can compare between weeks.</p></div>
                <div class="benefit"><h4>Identify your moments</h4>
                    <p>Your best day and your heaviest day, side by
                    side.</p></div>
                <div class="benefit"><h4>Conduct-habit improvement
                    tips</h4>
                    <p>7-day experiments with a number to compare.</p></div>
            </div>
            <div>
                {mini_scatter()}
                <div class="twocard">
                    <div class="mini mini-navy">
                        <div class="big">3 h 29 min</div>
                        <p>median time to return to calm</p>
                    </div>
                    <div class="mini mini-mist">
                        <div class="mt">7-day experiment</div>
                        <p>A 10-minute pause before your hard time band.
                        Compare: does the afternoon's 44% drop?</p>
                    </div>
                </div>
                <div class="twocard">
                    <div class="mini mini-navy">
                        <div class="big">9 of 9</div>
                        <p>Family records were unpleasant</p>
                    </div>
                    <div class="mini mini-mist">
                        <div class="mt">Hint or pattern</div>
                        <p>With fewer than 5 cases it's a hint; with 5 or
                        more, a pattern you can discuss in session.</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="dayrow">
            <div><div class="dbar" style="background:{TEAL}"></div>
                <h5>Morning</h5>
                <p>How you slept and how you feel</p></div>
            <div><div class="dbar" style="background:{CYAN}"></div>
                <h5>During the day</h5>
                <p>Check-ins and episodes, only if something
                happens</p></div>
            <div><div class="dbar" style="background:{CORAL}"></div>
                <h5>Night</h5>
                <p>Calmer than this morning?</p></div>
            <div><div class="dbar" style="background:{ORANGE}"></div>
                <h5>Every week</h5>
                <p>Your report, in the app or as a PDF</p></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 6.5 · HOW IT STARTS (mist)

st.markdown(
    f"""
    <div class="sec sec-light" id="comoempieza">
        <div class="kicker">How it starts</div>
        <h2>From installing it to<br>bringing it to session:<br>three
            steps.</h2>
        <div class="steps">
            <div>
                <div class="stepnum">1</div>
                <h3>Install Animus on your Android</h3>
                <p>No accounts, no sign-up: the app asks for Health
                Connect and phone-usage access, and everything stays
                encrypted on your device. A watch or band adds pulse as
                context — not required.</p>
            </div>
            <div>
                <div class="stepnum">2</div>
                <h3>Live your week</h3>
                <p>Log moments in two taps whenever you like; Animus asks
                only when something might matter — a body signal, the
                end of a calendar event. Days without data are shown as
                absent, not as zeros.</p>
            </div>
            <div>
                <div class="stepnum">3</div>
                <h3>Bring the map to your session</h3>
                <p>The 6-page report is generated on your phone and you
                share it only if you decide to: WhatsApp, email or
                print. The conversation starts with data, not
                memory.</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 7 · PRIVACY (navy)

st.markdown(
    f"""
    <div class="sec sec-navy" id="privacidad">
        <h2>Your data is yours.</h2>
        <div class="priv-cols">
            <div class="priv-col">
                <div class="bar" style="background:{TEAL}"></div>
                <h4>Local first</h4>
                <p>Encrypted database on your phone, no server.</p>
            </div>
            <div class="priv-col">
                <div class="bar" style="background:{CYAN}"></div>
                <h4>Encrypted export</h4>
                <p>AES-256-GCM and PBKDF2-HMAC-SHA256, only if you ask
                for it.</p>
            </div>
            <div class="priv-col">
                <div class="bar" style="background:{CORAL}"></div>
                <h4>No accounts</h4>
                <p>No sign-up, no cloud and no usage analytics.</p>
            </div>
            <div class="priv-col">
                <div class="bar" style="background:{ORANGE}"></div>
                <h4>Local PDF</h4>
                <p>Generated and shared from your device.</p>
            </div>
            <div class="priv-col">
                <div class="bar" style="background:{TEAL}"></div>
                <h4>Open source</h4>
                <p>Available for audit.</p>
            </div>
        </div>
        <div class="isnot">
            <div class="yes">
                <h4>Animus is</h4>
                <ul>
                    <li>Observation of a single person</li>
                    <li>Evidence for the session</li>
                    <li>Your own contingencies</li>
                    <li>Local, encrypted data</li>
                    <li>Hint (under 5) or pattern (5 or more)</li>
                </ul>
            </div>
            <div class="no">
                <h4>Animus is not</h4>
                <ul>
                    <li>A diagnosis</li>
                    <li>A substitute for clinical judgment</li>
                    <li>A crisis predictor</li>
                    <li>A cloud service</li>
                    <li>A claim without evidence</li>
                </ul>
            </div>
        </div>
        <div class="priv-foot">Pulse is a context, not an emotion
            detector. Absence of signal does not imply absence of
            event.</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 8 · CLOSING (gradient)

st.markdown(
    f"""
    <div class="closing">
        {wordmark()}
        <h2>Start knowing yourself.<br>Start the next session<br>with a
            map.</h2>
        <div class="cta-row">
            <a class="btn btn-white" href="#">Download Animus</a>
            <a class="btn btn-ghost-cyan" href="#informe">See the sample
                report</a>
        </div>
        <div class="foot">Animus describes observations of a single
            person. It does not diagnose, does not predict crises and
            does not replace professional supervision or emergency
            services.</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 9 · FAQ (white, at the end)

st.markdown(
    f"""
    <div class="sec sec-white faq" id="faq">
        <div class="kicker">Frequently asked questions</div>
        <h2>What people ask before starting</h2>
        <p class="lede">Honest answers — including the uncomfortable
        ones.</p>
        <h3>For therapists</h3>
        <details class="qa"><summary class="q">What methodology does
        Animus use?</summary>
        <p class="a">It combines two traditions with decades of evidence.
        The first is <b>ecological momentary assessment (EMA)</b>:
        brief, repeated samples in real context, which reduce the
        recall bias that affects retrospective reports (Shiffman, Stone
        &amp; Hufford, <i>Annual Review of Clinical Psychology</i>,
        2008). The second is <b>ABC recording</b>
        (antecedent–behavior–consequence), the descriptive tool of
        functional behavior analysis (FBA) used in clinical practice
        since Bijou, Peterson and Ault (1968).</p>
        <p class="a">Every episode is saved with <b>exact time, context
        and temporal sequence</b> — not from memory: the antecedent
        (events that can evoke or raise the probability of a response),
        the behavior as an <b>observable, measurable response</b>
        (emotion, 0–10 intensity, life area) and the consequence, which
        in FBA can maintain, reinforce or reduce the chance of the
        response happening again — that's where <b>recovery time</b>
        comes from, an indicator you can compare across weeks.</p>
        <p class="a">A single record describes a moment; repeating the
        ABC reveals <b>contingencies</b>: which situations precede your
        episodes, which responses repeat and which consequences follow
        — the logic of observation-based behavioral assessment for
        building <b>functional hypotheses</b>. It is descriptive,
        hypothesis-oriented recording: it does not replace a clinical
        evaluation or an experimental functional analysis.</p></details>
        <details class="qa alt"><summary class="q">Why ask "in the
        moment" instead of a diary?</summary>
        <p class="a">Because autobiographical memory edits. EMA studies
        show that retrospective reports are distorted by mood on
        appointment day, by the most recent events and by narrative
        style. Asking when pulse changes at rest — or right after a
        calendar activity — captures the moment before memory rewrites
        it.</p></details>
        <details class="qa"><summary class="q">Does descriptive recording
        replace an experimental functional analysis?</summary>
        <p class="a"><b>No — and Animus says so openly.</b> Comparative
        research shows that ABC recording alone matches experimental
        functional analyses only in part of cases; its real role is to
        <b>generate well-documented hypotheses</b>. That's why every
        finding in the report shows its case count: under 5 it's
        presented as a <b>hint</b>, never a pattern. Interpretation and
        verification are clinical.</p></details>
        <details class="qa alt"><summary class="q">What advantage over
        asking the patient "to keep a diary"?</summary>
        <p class="a">Three: adherence (the question arrives on its own
        and is answered in seconds, without remembering to write),
        <b>time anchoring</b> (each record carries exact time, sleep,
        steps, phone use and pulse when a sensor is present), and
        <b>structure</b> (the report already includes contingencies,
        day bands and recovery — not loose notes).</p></details>
        <details class="qa"><summary class="q">Can I test my case
        hypotheses?</summary>
        <p class="a">Yes. Therapist mode lets you formulate hypotheses
        ("it gets worse on Sunday afternoons") that the report
        contrasts prospectively with the actual record of the period —
        in shadow mode, without contaminating the detector or turning
        expectation into conclusion.</p></details>
        <details class="qa alt"><summary class="q">How does the
        information reach the session?</summary>
        <p class="a">The 6-page report is generated on the client's
        phone. <b>They decide to share it</b> — by WhatsApp, email or
        printed. There is no remote monitor: no data reaches you unless
        the person hands it over.</p></details>
        <details class="qa"><summary class="q">What happens with days
        without data?</summary>
        <p class="a">They are reported as absent, with an explicit count
        on the data-quality page. Animus never treats absence of signal
        as absence of event — a distinction the instrument states in
        the report itself.</p></details>
        <details class="qa alt"><summary class="q">Does the patient need
        a watch or band?</summary>
        <p class="a">Not essential: Health Connect already provides
        sleep, steps and phone use. A wearable adds pulse and
        variability, enriching contextual signals — but the report
        works with the phone alone.</p></details>
        <details class="qa"><summary class="q">Does Animus diagnose or
        predict crises?</summary>
        <p class="a">No. It describes observations of a single person,
        organized for the clinical conversation. It is not a medical
        device, issues no diagnoses, predicts no crises and does not
        replace clinical judgment or emergency services.</p></details>
        <h3>For you, if you install it</h3>
        <details class="qa"><summary class="q">Is this another
        mood-tracking app?</summary>
        <p class="a">No. Animus combines what your phone already knows
        (sleep, steps, usage, activity) with brief questions only when
        needed, and turns it into a report designed to be read with
        your therapist. It's not an empty diary: it's a map.</p></details>
        <details class="qa alt"><summary class="q">How much time does it
        take per day?</summary>
        <p class="a">Seconds. A check-in is two taps; a full episode
        (what happened before, what you did, how you ended) takes under
        a minute. Passive collection requires nothing from you.</p></details>
        <details class="qa"><summary class="q">Who can see my
        data?</summary>
        <p class="a">Only you. Everything is stored encrypted on your
        phone — no accounts, no cloud, no analytics. The report is
        shared only when you decide, like any PDF.</p></details>
        <details class="qa alt"><summary class="q">What if I ignore a
        question?</summary>
        <p class="a">Nothing bad: it's logged as "no answer" and that's
        it. Days or moments without data appear as absent in the
        report — nobody invents them.</p></details>
        <details class="qa"><summary class="q">Does the app decide how I
        feel from my pulse?</summary>
        <p class="a">No — and that's an important design decision. Pulse
        is a <b>context</b>, not an emotion detector. It only serves to
        ask you "did something happen?" at a sensitive moment. The
        emotion is always yours to name.</p></details>
        <details class="qa alt"><summary class="q">Does it judge me if I
        have a bad week?</summary>
        <p class="a">The report describes, it doesn't evaluate. It shows
        what happened, where and how many times — no "good" or "bad"
        scores, no failed goals. It's conversation material, not a
        report card.</p></details>
        <details class="qa"><summary class="q">Is it useful if I don't
        go to therapy?</summary>
        <p class="a">Yes — the report is yours and helps you know
        yourself with your own numbers. Honestly: its full value
        appears when it's discussed with a professional, because hints
        ask for interpretation.</p></details>
        <details class="qa alt"><summary class="q">Does it drain battery
        or use mobile data?</summary>
        <p class="a">It doesn't use the network to work (everything is
        local) and passive readings are done by Android in the
        background. Extra consumption is marginal.</p></details>
        <details class="qa"><summary class="q">Can I delete
        everything?</summary>
        <p class="a">Yes. Data lives only on your phone: deleting the
        app deletes everything. No copy remains on any server because
        there is no server.</p></details>
        <div class="scinote"><b>Why an idiographic instrument.</b>
        The single-case (N-of-1) design tradition — from behavioral
        psychology to current clinical research — holds that the most
        useful patterns for intervention are <b>that</b> person's: what
        precedes, what follows, in which context. Animus doesn't
        compare your client to population averages; it compares the
        client to themselves.</div>
        <div class="faq-foot">Animus describes observations of a single
            person. It does not diagnose, does not predict crises and
            does not replace professional supervision or emergency
            services.</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 10 · FOOTER

st.markdown(
    f"""
    <div class="mnav">
        <span id="mopen" class="msent"></span>
        <span id="mclose" class="msent"></span>
        <nav class="mlinks">
            <a href="#informe">The report</a>
            <a href="#terapeutas">For therapists</a>
            <a href="#parati">For you</a>
            <a href="#privacidad">Privacy</a>
            <a href="#faq">FAQ</a>
            <a href="?lang=es" target="_self">ES · Español</a>
        </nav>
        <a class="mfab mfab-open" href="#mopen" aria-label="Open menu">
            <i style="background:{TEAL}"></i><i style="background:{CYAN}"></i><i style="background:{CORAL}"></i>
        </a>
        <a class="mfab mfab-x" href="#mclose" aria-label="Close menu">✕</a>
    </div>
    <div class="sitefoot">
        <div class="foot-grid">
            <div>
                {wordmark()}
                <div class="fnote">Structured behavioral observation
                for Android. Your data stays encrypted on your phone —
                no accounts, no cloud, and the report is shared only
                when you decide to share it.</div>
            </div>
            <div>
                <h6>Explore</h6>
                <ul>
                    <li><a href="#informe">The report</a></li>
                    <li><a href="#terapeutas">For therapists</a></li>
                    <li><a href="#parati">For you</a></li>
                    <li><a href="#privacidad">Privacy</a></li>
                    <li><a href="#faq">FAQ</a></li>
                </ul>
            </div>
            <div>
                <h6>This site</h6>
                <ul>
                    <li><a href="mailto:animusapp@protonmail.com">animusapp@protonmail.com</a></li>
                    <li><a href="https://instagram.com/animus.app"
                           target="_blank" rel="noopener">Instagram ·
                           @animus.app</a></li>
                    <li><a href="?lang=es" target="_self">Versión en español</a></li>
                </ul>
                <div class="fnote" style="margin-top:14px">No tracking
                cookies, no analytics. No accounts, no forms, no data
                collection.</div>
            </div>
        </div>
        <div class="foot-base">
            <span>Animus — an observation instrument, not a medical
            device.</span>
            <span>Does not diagnose · does not predict crises · does
            not replace professional supervision or emergency
            services.</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

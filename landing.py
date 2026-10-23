"""
Animus — sitio público de presentación.
Corre con:  streamlit run landing.py

Diseño: mockup Animus_Sitio_web_muestra.pdf (8 secciones).
Página pública: qué es Animus, para quién, qué hace, cómo se ve el
informe. No procesa datos ni pide credenciales.
"""
import base64
import os
import random

import streamlit as st

# Versión en inglés: ?lang=en carga landing_en.py.
if st.query_params.get("lang") == "en":
    import landing_en  # noqa: F401
    st.stop()

st.set_page_config(
    page_title="Animus — Lo que viviste entre sesiones, por fin en un mapa",
    page_icon=os.path.join(os.path.dirname(__file__), "favicon.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Meta tags para compartir (Open Graph). Streamlit los inyecta en el body;
# el título y favicon de la pestaña vienen de set_page_config.
st.markdown(
    """
    <meta property="og:title"
          content="Animus — lo que viviste entre sesiones, en un mapa">
    <meta property="og:description"
          content="Registro conductual idiográfico para consultante y
          terapeuta: datos del teléfono, preguntas breves en el momento y
          un informe de 6 páginas para la sesión. Local y cifrado.">
    <meta property="og:type" content="website">
    <meta name="description"
          content="Animus: observación conductual entre sesiones.
          Informe de 6 páginas para tu terapeuta. Datos locales y
          cifrados, sin cuentas ni nube.">
    """,
    unsafe_allow_html=True,
)

# Paleta del mockup / app
NAVY = "#1f2947"
NAVY_SOFT = "#2a3557"
TEAL = "#3fb0a0"
CYAN = "#a9d6d9"
CORAL = "#e8725c"
ORANGE = "#f0a35e"
INK = "#22304e"
BODY = "#4a5468"
MIST = "#eef2f6"
LINE = "#dde3ec"
WHITE = "#ffffff"

PAGES_DIR = os.path.join(os.path.dirname(__file__), "pdf_pages")


def b64img(path: str) -> str:
    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def hero_scatter(cols: int = 14, rows: int = 9, seed: int = 11) -> str:
    """Nube de puntos del hero: filas = días, color = emoción,
    tamaño = intensidad (dato de ejemplo)."""
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
    """'Tu semana, hora por hora' — la tarjeta clara de la sección Para ti."""
    rnd = random.Random(seed)
    w, h = 640, 300
    x0, y0, x1, y1 = 66, 34, w - 24, h - 44
    bands = [(x0 + (x1 - x0) * 6 / 24, x0 + (x1 - x0) * 12 / 24, "Mañana"),
             (x0 + (x1 - x0) * 12 / 24, x0 + (x1 - x0) * 18 / 24, "Tarde"),
             (x0 + (x1 - x0) * 18 / 24, x0 + (x1 - x0) * 24 / 24, "Noche")]
    parts = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">',
             f'<rect x="{x0 - 50}" y="{y0 - 6}" width="{x1 - x0 + 74}" '
             f'height="{y1 - y0 + 20}" rx="10" fill="#ffffff"/>']
    # banda de madrugada
    parts.append(f'<text x="{x0 - 16}" y="{y0 - 12}" font-size="11" '
                 f'fill="#7c8698" text-anchor="middle">Madrugada</text>')
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
    legend = [("Agradable", TEAL), ("Calma", CYAN), ("Displacentera", CORAL),
              ("Otra", "#b9c0cc")]
    lx = x0 + 20
    for lab, col in legend:
        parts.append(f'<circle cx="{lx}" cy="{h - 8}" r="5" fill="{col}"/>')
        parts.append(f'<text x="{lx + 10}" y="{h - 4}" font-size="10" '
                     f'fill="#5b6474">{lab}</text>')
        lx += 96
    parts.append("</svg>")
    return "".join(parts)


def wordmark(color: str = "#ffffff", size: int = 30) -> str:
    """Logo: tres puntos + 'animus' en serif."""
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


def pg(i: int) -> str:
    return b64img(os.path.join(PAGES_DIR, f"p{i}.png"))


SHOTS_DIR = os.path.join(os.path.dirname(__file__), "app_shots")


def shot(name: str) -> str:
    return b64img(os.path.join(SHOTS_DIR, name))


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
    .main .block-container {{
        padding: 0;
        max-width: 100%;
    }}
    .stApp {{ background: {NAVY}; }}
    section[data-testid="stMainBlockContainer"] {{
        padding-left: 0; padding-right: 0;
    }}
    header[data-testid="stHeader"] {{ display: none; }}
    #MainMenu, footer {{ visibility: hidden; }}
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {{ display: none !important; }}

    .serif {{ font-family:'Playfair Display',Georgia,serif; }}

    /* ---- bloques base ---- */
    .sec {{ padding: 84px 72px; }}
    .sec-navy {{ background: {NAVY}; color: #e8edf6; }}
    .sec-light {{ background: {MIST}; }}
    .sec-white {{ background: #ffffff; }}
    .kicker {{
        color: {TEAL}; font-size: 14px; font-weight: 600;
        letter-spacing: .4px; margin-bottom: 10px;
    }}
    .sec h1, .sec h2 {{
        font-family:'Playfair Display',Georgia,serif;
        font-weight: 700; color: {NAVY};
        margin: 0 0 14px; line-height: 1.12;
    }}
    .sec-navy h1, .sec-navy h2 {{ color: #fff; }}
    .sec h2 {{ font-size: 44px; }}
    .lede {{ font-size: 17px; color: {BODY}; line-height: 1.6;
             max-width: 560px; }}
    .sec-navy .lede {{ color: #b9c3d6; }}

    /* ---- hero ---- */
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

    /* ---- tarjetas comparación (sección 2) ---- */
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
    .footnote {{ font-size:12.5px; color:#9aa4b5; margin-top:34px; }}
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

    /* ---- pasos 1-2-3 ---- */
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

    /* ---- informe (sección 4, navy) ---- */
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

    /* ---- listas beneficios ---- */
    .benefits {{ display:grid; grid-template-columns:1fr 1.05fr;
                 gap:56px; align-items:start; }}
    .benefit {{ margin-bottom:30px; }}
    .benefit h4 {{ font-size:17.5px; color:{NAVY}; margin:0 0 6px;
                   font-weight:700; }}
    .benefit p {{ font-size:14.5px; color:{BODY}; margin:0;
                  line-height:1.6; max-width:400px; }}
    .sideimg {{ width:100%; border-radius:8px;
                box-shadow:0 8px 26px rgba(34,48,78,.16); }}
    .sidecap {{ font-size:13.5px; color:{BODY}; margin-top:14px;
                line-height:1.55; max-width:380px; }}
    .nochips {{ margin-top:44px; text-align:center;
                line-height:3.1; }}
    .nochips .chip {{ background:#fff; margin:0 6px; }}

    /* ---- tarjetas para-ti ---- */
    .twocard {{ display:flex; gap:22px; margin-top:20px; }}
    .mini {{ border-radius:14px; padding:26px 28px; flex:1; }}
    .mini-navy {{ background:{NAVY}; color:#fff; }}
    .mini-navy .big {{ font-family:'Playfair Display',serif;
        font-size:34px; font-weight:700; margin-bottom:8px;
        white-space:nowrap; }}
    .mini-mist {{ background:{MIST}; color:{INK}; }}
    .mini-mist .mt {{ font-weight:700; font-size:15px; margin-bottom:8px; }}
    .mini p {{ font-size:14px; margin:0; line-height:1.55; color:{BODY}; }}
    .mini-navy p {{ color:#c3ccdc; }}
    .dayrow {{
        display:grid; grid-template-columns:repeat(4,1fr);
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

    /* ---- privacidad ---- */
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

    /* ---- cierre ---- */
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

    /* ---- preguntas frecuentes ---- */
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
    details.qa[open] .q::after {{ content:"\2212"; }}
    details.qa .a {{ font-size:14.5px; color:{BODY}; line-height:1.65;
              padding:12px 22px 4px; margin:0; }}
    details.qa .a b {{ color:{NAVY}; }}
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
    /* esferas del logo que saltan en su lugar, nunca a la vez */
    @keyframes wmh {{
        0%, 18%, 100% {{ transform:translateY(0); }}
        9% {{ transform:translateY(-12px); }}
    }}
    .hero-top .wm > span:nth-child(1) {{ animation:wmh 2.3s ease-in-out infinite; }}
    .hero-top .wm > span:nth-child(2) {{ animation:wmh 3.1s ease-in-out infinite; }}
    .hero-top .wm > span:nth-child(3) {{ animation:wmh 2.7s ease-in-out infinite; }}
    @media (prefers-reduced-motion: reduce) {{
        .hero-top .wm > span {{ animation:none !important; }}
    }}
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
        .abc-patterns {{ grid-template-columns:1fr; gap:24px; margin-top:28px; }}
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
        .benefits {{ gap:24px; }}
        .benefit {{ margin-bottom:16px; }}
        .twocard .mini-navy {{ text-align:center; }}
        .vs-wrap {{ flex-direction:column; }}
        .week-cards {{ grid-template-columns:1fr; }}
        .wordmark-wrap {{ flex-wrap:wrap; }}
    }}
    @media (max-width: 640px) {{
        .sec {{ padding:44px 20px; }}
        .hero-top {{ padding:52px 20px 36px; }}
        .hero-grid {{ padding:0 20px; }}
        .closing {{ padding:44px 20px 32px; }}
        .closing h2 {{ margin-top:26px; margin-bottom:28px; }}
        .closing .foot {{ margin-top:38px; }}
        .priv-foot {{ margin-top:26px; }}
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
        .steps {{ gap:22px; margin-top:10px; }}
        .sec3-top {{ gap:12px !important; margin-bottom:4px !important; }}
        #observa {{ padding-top:26px; }}
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
        div:has(> .chip) {{ text-align:center; }}
        .prompt-card {{ text-align:center; }}
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


# ======================================================== 1 · HERO (navy)

st.markdown(
    f"""
    <div class="sec-navy">
        <div class="hero-top">
            {wordmark()}
            <nav class="hero-nav">
                <a href="#informe">El informe</a>
                <a href="#terapeutas">Para terapeutas</a>
                <a href="#parati">Para ti</a>
                <a href="#privacidad">Privacidad</a>
                <a href="#faq">Preguntas frecuentes</a>
                <a href="?lang=en" target="_self"
                   style="border:1.5px solid {ORANGE}; color:{ORANGE};
                          border-radius:999px; padding:5px 14px">EN</a>
            </nav>
        </div>
        <div class="hero hero-grid">
            <div>
                <h1>Lo que viviste<br>entre sesiones,<br>por fin en un
                    mapa.</h1>
                <div class="hero-sub">
                    Animus registra lo que tu cuerpo y tu teléfono ya saben,
                    te pregunta en el momento justo y lo convierte en un
                    informe que tu terapeuta y tú pueden leer juntos.
                </div>
                <div class="cta-row">
                    <a class="btn btn-teal" href="#parati">Soy consultante</a>
                    <a class="btn btn-coral" href="#terapeutas">Soy terapeuta</a>
                </div>
                <div class="hero-note">Para Android. Tus datos se quedan en
                    tu teléfono.</div>
            </div>
            <div>
                {hero_scatter()}
                <div class="scatter-cap">Datos de ejemplo: cada punto es un
                registro, el color es la emoción y el tamaño es su
                intensidad. Cada fila es un día.</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 2 · "¿CÓMO ESTUVO TU SEMANA?" (mist)

st.markdown(
    f"""
    <div class="sec sec-light">
        <div class="week-top">
            <div>
                <h2>“¿Cómo estuvo tu<br>semana?” depende de<br>lo que
                    alcanzas a recordar.</h2>
                <p class="lede" style="margin-top:26px">
                    La sesión llega filtrada por tu memoria, por tu humor
                    el día de la cita y por tu manera de contarlo. Animus
                    guarda lo que pasó cuando pasó.
                </p>
            </div>
            <div class="shotfan">
                <img class="s1" src="data:image/jpeg;base64,{shot('ejercicios.jpg')}" alt="Ejercicios">
                <img class="s2" src="data:image/jpeg;base64,{shot('hoy.jpg')}" alt="Hoy">
                <img class="s3" src="data:image/jpeg;base64,{shot('metricas.jpg')}" alt="Métricas">
            </div>
        </div>
        <div class="vs-wrap">
            <div class="vs-card vs-out">
                <span class="vs-tag">Lo que llega al consultorio</span>
                Lo que recuerdas<br>
                Cómo te sientes ese día<br>
                Cómo logras contarlo
            </div>
            <div class="vs-card vs-in">
                <span class="vs-tag">Lo que llega con Animus</span>
                Registro hecho en el momento<br>
                Situación, emoción e intensidad<br>
                Cada hallazgo con su número de casos
            </div>
        </div>
        <div class="stats">
            <div class="stat"><div class="num">9 de 9</div>
                <div class="cap">registros de Familia fueron
                    displacenteros</div></div>
            <div class="stat"><div class="num">44%</div>
                <div class="cap">de los registros de la tarde, frente al
                    16% de la noche</div></div>
            <div class="stat"><div class="num" style="font-size:50px;
                white-space:nowrap">3 h 29 min</div>
                <div class="cap">mediana para volver a la calma</div></div>
            <div class="stat"><div class="num">14 de 30</div>
                <div class="cap">días con datos del período — los demás se
                    muestran como ausentes, no como días "en
                    cero"</div></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 3 · OBSERVA / PREGUNTA / APRENDE (blanco)

st.markdown(
    f"""
    <div class="sec sec-white" id="observa">
        <div class="sec3-top" style="display:flex;justify-content:space-between;
                    align-items:center;gap:48px;flex-wrap:wrap;
                    margin-bottom:20px">
            <div>{wordmark(color=INK, size=66)}</div>
            <h2 class="sec3h2" style="text-align:right;flex:1;min-width:300px">Observa,
                pregunta y aprende.<br>Tú solo respondes lo breve.</h2>
        </div>
        <div class="steps">
            <div>
                <div class="stepnum">1</div>
                <h3>Observa en segundo plano</h3>
                <p>Pulso, variabilidad, sueño, pasos y uso del teléfono
                    llegan desde Health Connect, sin que hagas nada.</p>
                <div>
                    <span class="chip">Pulso</span><span class="chip">Sueño</span><span class="chip">Pasos</span><br>
                    <span class="chip">Uso del teléfono</span>
                </div>
            </div>
            <div>
                <div class="stepnum">2</div>
                <h3>Pregunta en el momento</h3>
                <p>Si tu pulso cambia en reposo, te pregunta qué pasó y te
                    da la hora para anclar el recuerdo.</p>
                <div class="prompt-card">
                    <div class="pc-brand">Animus</div>
                    <div class="pc-q">¿Pasó algo alrededor de las 19:34?</div>
                    <span class="pc-btn pc-yes">Sí, pasó</span>
                    <span class="pc-btn pc-no">No pasó</span>
                </div>
            </div>
            <div>
                <div class="stepnum">3</div>
                <h3>Aprende tus patrones</h3>
                <p>Cada hallazgo muestra cuántas veces ocurrió. Con menos
                    de 5 casos es una pista, no un patrón.</p>
                <div class="rulebar">
                    <div class="rb-label">Familia: 9 de 9 displacenteros</div>
                    <div class="rb-bar" style="width:100%;background:{CORAL}"></div>
                    <div class="rb-cap">Patrón, 9 casos</div>
                </div>
                <div class="rulebar">
                    <div class="rb-label">Dinero: 2 de 3 con ansiedad</div>
                    <div class="rb-bar" style="width:33%;background:#c3ccd9"></div>
                    <div class="rb-cap">Pista, 3 casos</div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 3.5 · EL ABC EN ANIMUS (mist)

st.markdown(
    f"""
    <div class="sec sec-light">
        <div class="kicker">El registro que ordena todo</div>
        <div class="abc-top">
            <div>
        <h2>El ABC de tu conducta,<br>registrado en tiempo real.</h2>
        <p class="lede" style="margin-top:20px">
            Cada episodio en Animus se estructura según el modelo
            ABC del análisis funcional de la conducta (AFC): un
            enfoque con respaldo en la investigación conductual que
            examina cómo los eventos que ocurren antes y después de
            una respuesta influyen en su aparición y repetición.
            En lugar de depender del recuerdo posterior, Animus
            registra cada episodio con hora exacta, contexto y
            secuencia temporal — para observar patrones reales entre
            situaciones, emociones y consecuencias.
        </p>
            </div>
            <div class="shotfan">
                <img class="s1" src="data:image/jpeg;base64,{shot('hoy_ansiedad.jpg')}" alt="Ansiedad">
                <img class="s2" src="data:image/jpeg;base64,{shot('hoy_neutro.jpg')}" alt="Hoy">
                <img class="s3" src="data:image/jpeg;base64,{shot('hoy_alegria.jpg')}" alt="Alegría">
            </div>
        </div>
        <div class="abc">
            <div class="abc-card a">
                <div class="abc-tag">Antecedente</div>
                <div class="letter">A<em>Qué pasó justo antes</em></div>
                <p>Registra la situación, persona, lugar o demanda
                que precedió al episodio. Animus ya captura
                automáticamente la hora, el sueño y la actividad; tú
                solo describes el contexto en una frase breve o con
                un toque. Los antecedentes son eventos que pueden
                evocar o aumentar la probabilidad de una respuesta
                emocional o conductual.</p>
            </div>
            <div class="abc-card b">
                <div class="abc-tag">Conducta</div>
                <div class="letter">B<em>Qué sentiste y qué hiciste</em></div>
                <p>Registra la emoción, su intensidad de 0 a 10, el
                área de vida afectada y la respuesta concreta que
                tuviste. Dos toques si vas rápido, una nota cuando
                quieras más contexto. La conducta se entiende como
                una respuesta observable y medible dentro de una
                situación específica.</p>
            </div>
            <div class="abc-card c">
                <div class="abc-tag">Consecuencia</div>
                <div class="letter">C<em>Cómo quedaste después</em></div>
                <p>Registra qué sucedió inmediatamente después y
                cómo terminó el episodio. De ahí surge el tiempo de
                recuperación, un indicador que luego comparas entre
                semanas. Las consecuencias son fundamentales en el
                AFC: pueden mantener, reforzar o reducir la
                probabilidad de que una respuesta vuelva a
                ocurrir.</p>
            </div>
        </div>
        <div class="abc-patterns">
            <div>
            <h3>De episodios aislados a patrones funcionales</h3>
            <div class="cols">
            <p>Un registro aislado describe un momento; la repetición
            del ABC permite identificar contingencias: qué situaciones
            suelen preceder tus episodios, qué respuestas aparecen con
            más frecuencia y qué consecuencias se asocian con su
            evolución. Esta lógica proviene de la evaluación
            conductual basada en observación directa, utilizada para
            formular hipótesis funcionales sobre la relación entre
            ambiente y conducta.</p>
            <p>Animus aplica ese principio a tu vida cotidiana:
            convierte tus registros en datos estructurados para
            observar tendencias, anticipar situaciones difíciles y
            evaluar cambios a lo largo del tiempo. No sustituye una
            evaluación clínica ni un análisis funcional experimental,
            pero utiliza su marco conceptual para ayudarte a
            comprender tu conducta con mayor precisión y
            evidencia.</p>
                </div>
            </div>
            <div class="abc-logo">{wordmark(color=INK, size=60)}</div>
        </div>
        <div class="abc-split">
            <div class="abc-why">
                <h3>No es un formulario.<br>Es método.</h3>
                <ul>
                    <li><b>Décadas de evidencia.</b> La estructura
                    antecedente-conducta-consecuencia se usa en clínica
                    desde Bijou, Peterson &amp; Ault (1968) y es la base
                    del análisis funcional (Iwata y cols.,
                    <i>Journal of Applied Behavior Analysis</i>).</li>
                    <li><b>En el momento, no de memoria.</b> Responder
                    cuando pasa es la evaluación ecológica momentánea
                    (Shiffman, Stone &amp; Hufford, <i>Annual Review of
                    Clinical Psychology</i>, 2008) — reduce el sesgo de
                    recuerdo.</li>
                    <li><b>Anclado a tu biometría y contexto.</b> Mientras
                    registras, Animus cruza el episodio con lo que el
                    teléfono ya sabe: sueño, pasos, tiempo de pantalla,
                    calendario y — con un wearable — pulso y
                    variabilidad.</li>
                    <li><b>Aprende de tus registros.</b> Cada episodio
                    alimenta el mapa: las repeticiones convierten pistas
                    en patrones que se pueden discutir en sesión.</li>
                </ul>
            </div>
            <div class="shotfan4">
                <img class="t1" src="data:image/jpeg;base64,{shot('abc_a.jpg')}" alt="Antecedente">
                <img class="t2" src="data:image/jpeg;base64,{shot('abc_situacion.jpg')}" alt="Situación">
                <img class="t3" src="data:image/jpeg;base64,{shot('abc_intensidad.jpg')}" alt="Intensidad">
                <img class="t4" src="data:image/jpeg;base64,{shot('abc_c.jpg')}" alt="Consecuencia">
            </div>
        </div>
        <div class="abc-close" style="text-align:center; margin-top:56px;
             margin-left:auto; margin-right:auto; max-width:820px">
            Diseñado bajo los principios del análisis funcional de la
            conducta — por eso el informe se lee como evidencia, no como
            un diario de ánimo.</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 4 · EL INFORME (navy)

st.markdown(
    f"""
    <div class="sec sec-navy" id="informe">
        <div class="report-grid">
            <div>
                <h2>Un informe de 6<br>páginas listo para<br>la sesión.</h2>
                <ul class="pagelist">
                    <li><span class="dot" style="background:{TEAL}"></span>
                        Portada y los tres hallazgos más fuertes</li>
                    <li><span class="dot" style="background:{CORAL}"></span>
                        Situaciones y emociones</li>
                    <li><span class="dot" style="background:{ORANGE}"></span>
                        Ritmo del día</li>
                    <li><span class="dot" style="background:{CYAN}"></span>
                        Sueño y recuperación</li>
                    <li><span class="dot" style="background:{TEAL}"></span>
                        Cuerpo y relación con el registro</li>
                    <li><span class="dot" style="background:{CORAL}"></span>
                        Para probar y para llevar a la sesión</li>
                </ul>
                <div class="lede" style="font-size:15px">
                    Se genera en tu teléfono. Compártelo por WhatsApp o
                    correo, o imprímelo.
                </div>
            </div>
            <div class="fan">
                <img class="f1" src="data:image/png;base64,{pg(1)}">
                <img class="f3" src="data:image/png;base64,{pg(6)}">
                <img class="f2" src="data:image/png;base64,{pg(3)}">
            </div>
        </div>
        <details class="reportgal">
            <summary>Ver las 6 páginas completas del informe de
                ejemplo</summary>
            <div class="galgrid">
                <img src="data:image/png;base64,{pg(1)}" alt="Página 1">
                <img src="data:image/png;base64,{pg(2)}" alt="Página 2">
                <img src="data:image/png;base64,{pg(3)}" alt="Página 3">
                <img src="data:image/png;base64,{pg(4)}" alt="Página 4">
                <img src="data:image/png;base64,{pg(5)}" alt="Página 5">
                <img src="data:image/png;base64,{pg(6)}" alt="Página 6">
            </div>
        </details>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 5 · PARA TERAPEUTAS (mist)

st.markdown(
    f"""
    <div class="sec sec-light" id="terapeutas">
        <div class="kicker">Para terapeutas</div>
        <div class="benefits">
            <div>
                <h2 style="margin-bottom:60px">La sesión empieza<br>con
                    datos, no con<br>memoria.</h2>
                <div class="benefit"><h4>Hipótesis que se pueden probar</h4>
                    <p>Formula una hipótesis del caso y contrástala con el
                    registro real del período. El resultado llega separado:
                    lo que se confirmó, lo que no y con cuántos casos — tu
                    impresión clínica queda a prueba sin contaminar el
                    registro.</p></div>
                <div class="benefit"><h4>Preguntas para la sesión</h4>
                    <p>La última página junta datos clave con preguntas que
                    salen del mapa de ese consultante. Cada pregunta llega
                    con el número que la motivó, así la conversación
                    empieza por lo que más necesita mirarse.</p></div>
                <div class="benefit"><h4>Seguimiento de intervenciones</h4>
                    <p>Propones un cambio y la semana siguiente ves si bajó
                    la proporción en esa franja. El mismo mapa sirve de
                    antes/después: mismo consultante, mismas franjas,
                    distinto período.</p></div>
                <div class="benefit"><h4>Episodios completos</h4>
                    <p>Antecedente, qué se hizo después, área de vida e
                    intensidad, anotados en el momento. Lo que pasó antes,
                    la respuesta y lo que vino después quedan encadenados
                    — el ABC ya ordenado para leer.</p></div>
                <div class="benefit"><h4>Falsos positivos a la vista</h4>
                    <p>Cada señal confirmada o descartada queda contada:
                    la precisión del instrumento es visible. Cuando el
                    consultante descarta una señal, el informe muestra
                    cuánto se equivocó — la honestidad también se
                    mide.</p></div>
            </div>
            <div>
                <img class="sideimg" src="data:image/png;base64,{pg(6)}">
                <div class="sidecap">No es un monitor remoto: recibes el
                informe cuando el consultante decide compartirlo.</div>
            </div>
        </div>
        <div class="nochips">
            <span class="chip">No diagnostica</span>
            <span class="chip">No sustituye tu juicio clínico</span>
            <span class="chip">No detecta emociones por el pulso</span>
            <span class="chip">No infiere causas — correlación no es
                causalidad</span>
            <span class="chip">No envía datos sin permiso</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 5.5 · TESTIMONIO (pendiente de cita real)
# Descomentar cuando haya una cita real de un terapeuta o consultante.
#
# st.markdown(
#     f"""
#     <div class="sec sec-white">
#         <div style="max-width:760px;margin:0 auto;text-align:center">
#             <div style="font-family:'Playfair Display',serif;font-size:30px;
#                  color:{NAVY};line-height:1.4;font-weight:600">
#                 “CITA_REAL_AQUI”</div>
#             <div style="margin-top:22px;font-size:14.5px;color:{BODY}">
#                 <b>Nombre</b> — Rol / contexto</div>
#         </div>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )


# ===================== 6 · PARA TI (blanco)

st.markdown(
    f"""
    <div class="sec sec-white" id="parati">
        <div class="kicker">Para ti</div>
        <div class="benefits">
            <div>
                <h2 style="margin-bottom:60px">Conócete con tus<br>propios
                    números.</h2>
                <div class="benefit"><h4>Ves lo que no recuerdas</h4>
                    <p>Las situaciones que se repiten quedan a la vista,
                    aunque la memoria las edite.</p></div>
                <div class="benefit"><h4>Mides tu recuperación</h4>
                    <p>Cuánto tardas en volver a la calma es un número que
                    puedes comparar entre semanas.</p></div>
                <div class="benefit"><h4>Identifica tus momentos</h4>
                    <p>Tu mejor día y tu día más cargado, lado a lado.</p></div>
                <div class="benefit"><h4>Consejos de mejora en hábitos de
                    conducta</h4>
                    <p>Experimentos de 7 días con un número para
                    comparar.</p></div>
            </div>
            <div>
                {mini_scatter()}
                <div class="twocard">
                    <div class="mini mini-navy">
                        <div class="big">3 h 29 min</div>
                        <p>mediana para volver a la calma</p>
                    </div>
                    <div class="mini mini-mist">
                        <div class="mt">Experimento de 7 días</div>
                        <p>Una pausa de 10 minutos antes de tu franja
                        difícil. Compara: ¿baja el 44% de la tarde?</p>
                    </div>
                </div>
                <div class="twocard">
                    <div class="mini mini-navy">
                        <div class="big">9 de 9</div>
                        <p>registros de Familia fueron displacenteros</p>
                    </div>
                    <div class="mini mini-mist">
                        <div class="mt">Pista o patrón</div>
                        <p>Con menos de 5 casos es una pista; con 5 o más,
                        un patrón que puedes discutir en sesión.</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="dayrow">
            <div><div class="dbar" style="background:{TEAL}"></div>
                <h5>Mañana</h5>
                <p>Cómo dormiste y cómo te sientes</p></div>
            <div><div class="dbar" style="background:{CYAN}"></div>
                <h5>Durante el día</h5>
                <p>Check-ins y episodios, solo si pasa algo</p></div>
            <div><div class="dbar" style="background:{CORAL}"></div>
                <h5>Noche</h5>
                <p>¿Más tranquilo/a que esta mañana?</p></div>
            <div><div class="dbar" style="background:{ORANGE}"></div>
                <h5>Cada semana</h5>
                <p>Tu informe, en la app o en PDF</p></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 6.5 · CÓMO EMPIEZA (mist)

st.markdown(
    f"""
    <div class="sec sec-light" id="comoempieza">
        <div class="kicker">Cómo empieza</div>
        <h2>De instalarla a llevarla<br>a la sesión: tres pasos.</h2>
        <div class="steps">
            <div>
                <div class="stepnum">1</div>
                <h3>Instala Animus en tu Android</h3>
                <p>Sin cuentas ni registro: la app pide acceso a Health
                Connect y al uso del teléfono, y todo queda cifrado en tu
                dispositivo. Si tienes un reloj o banda, el pulso se suma
                como contexto — no es imprescindible.</p>
            </div>
            <div>
                <div class="stepnum">2</div>
                <h3>Vive tu semana</h3>
                <p>Registra momentos en dos toques cuando quieras; Animus
                pregunta solo cuando algo puede importar — una señal del
                cuerpo, el final de un evento del calendario. Los días sin
                datos quedan como ausentes, no como ceros.</p>
            </div>
            <div>
                <div class="stepnum">3</div>
                <h3>Lleva el mapa a tu sesión</h3>
                <p>El informe de 6 páginas se genera en tu teléfono y lo
                compartes solo si tú decides: por WhatsApp, correo o
                impreso. La conversación empieza con datos, no con
                memoria.</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 7 · PRIVACIDAD (navy)

st.markdown(
    f"""
    <div class="sec sec-navy" id="privacidad">
        <h2>Tus datos son tuyos.</h2>
        <div class="priv-cols">
            <div class="priv-col">
                <div class="bar" style="background:{TEAL}"></div>
                <h4>Local primero</h4>
                <p>Base de datos cifrada en tu teléfono, sin servidor.</p>
            </div>
            <div class="priv-col">
                <div class="bar" style="background:{CYAN}"></div>
                <h4>Exportación cifrada</h4>
                <p>AES-256-GCM y PBKDF2-HMAC-SHA256, solo si tú la
                pides.</p>
            </div>
            <div class="priv-col">
                <div class="bar" style="background:{CORAL}"></div>
                <h4>Sin cuentas</h4>
                <p>Sin registro, sin nube y sin analítica de uso.</p>
            </div>
            <div class="priv-col">
                <div class="bar" style="background:{ORANGE}"></div>
                <h4>PDF local</h4>
                <p>Se genera y se comparte desde tu dispositivo.</p>
            </div>
            <div class="priv-col">
                <div class="bar" style="background:{TEAL}"></div>
                <h4>Código abierto</h4>
                <p>Disponible para auditoría.</p>
            </div>
        </div>
        <div class="isnot">
            <div class="yes">
                <h4>Animus es</h4>
                <ul>
                    <li>Observación de una sola persona</li>
                    <li>Evidencia para la sesión</li>
                    <li>Contingencias propias</li>
                    <li>Datos locales y cifrados</li>
                    <li>Pista (menos de 5) o patrón (5 o más)</li>
                </ul>
            </div>
            <div class="no">
                <h4>Animus no es</h4>
                <ul>
                    <li>Un diagnóstico</li>
                    <li>Un sustituto del juicio clínico</li>
                    <li>Un predictor de crisis</li>
                    <li>Un servicio en la nube</li>
                    <li>Una afirmación sin evidencia</li>
                </ul>
            </div>
        </div>
        <div class="priv-foot">El pulso es un contexto, no un detector de
            emociones. La ausencia de señal no implica ausencia de
            evento.</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 8 · CIERRE (degradado navy→teal)

st.markdown(
    f"""
    <div class="closing">
        {wordmark()}
        <h2>Empieza a conocerte.<br>Empieza la próxima sesión<br>con un
            mapa.</h2>
        <div class="cta-row">
            <a class="btn btn-white" href="#">Descargar Animus</a>
            <a class="btn btn-ghost-cyan" href="#informe">Ver el informe de
                ejemplo</a>
        </div>
        <div class="foot">Animus describe observaciones de una sola
            persona. No diagnostica, no predice crisis y no sustituye la
            supervisión profesional ni los servicios de emergencia.</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===================== 9 · PREGUNTAS FRECUENTES (blanco, al final)

st.markdown(
    f"""
    <div class="sec sec-white faq" id="faq">
        <div class="kicker">Preguntas frecuentes</div>
        <h2>Lo que preguntan antes de empezar</h2>
        <p class="lede">Respuestas honestas — incluidas las
        incómodas.</p>
        <h3>Para terapeutas</h3>
        <details class="qa"><summary class="q">¿Qué metodología usa Animus?</summary>
        <p class="a">Combina dos tradiciones con décadas de evidencia.
        La primera es la <b>evaluación ecológica momentánea (EMA)</b>:
        muestras breves y repetidas en el contexto real, que reducen el
        sesgo de recuerdo que afecta a los reportes retrospectivos
        (Shiffman, Stone &amp; Hufford, <i>Annual Review of Clinical
        Psychology</i>, 2008). La segunda es el <b>registro
        ABC</b> (antecedente–conducta–consecuencia), la herramienta
        descriptiva del análisis funcional de la conducta (AFC) que se
        usa en la práctica clínica desde Bijou, Peterson y Ault
        (1968).</p>
        <p class="a">Cada episodio se guarda con <b>hora exacta,
        contexto y secuencia temporal</b>, no de memoria: el
        antecedente (eventos que pueden evocar o aumentar la
        probabilidad de una respuesta), la conducta como respuesta
        <b>observable y medible</b> (emoción, intensidad de 0 a 10,
        área de vida) y la consecuencia, que en el AFC puede mantener,
        reforzar o reducir la probabilidad de que la respuesta vuelva
        a ocurrir — de ahí surge el <b>tiempo de recuperación</b>, un
        indicador comparable entre semanas.</p>
        <p class="a">Un registro aislado describe un momento; la
        repetición del ABC permite identificar <b>contingencias</b>:
        qué situaciones preceden tus episodios, qué respuestas se
        repiten y qué consecuencias siguen — la lógica de la evaluación
        conductual por observación directa para formular
        <b>hipótesis funcionales</b>. Es registro descriptivo orientado
        a hipótesis: no sustituye una evaluación clínica ni un análisis
        funcional experimental.</p></details>
        <details class="qa alt"><summary class="q">¿Por qué preguntar "en el
        momento" en vez de un diario?</summary>
        <p class="a">Porque la memoria autobiográfica edita. Los
        estudios de EMA muestran que el reporte retrospectivo se
        distorsiona por el estado de ánimo del día de la cita, por los
        eventos más recientes y por la forma de narrar. Preguntar cuando
        el pulso cambia en reposo — o justo después de una actividad del
        calendario — captura el momento antes de que la memoria lo
        reescriba.</p></details>
        <details class="qa"><summary class="q">¿El registro descriptivo reemplaza un
        análisis funcional experimental?</summary>
        <p class="a"><b>No — y Animus lo dice abiertamente.</b> La
        investigación comparativa muestra que el registro ABC por sí solo
        coincide con los análisis funcionales experimentales solo en una
        parte de los casos; su función real es <b>generar hipótesis</b>
        bien documentadas. Por eso cada hallazgo del informe muestra su
        número de casos: con menos de 5 se presenta como <b>pista</b>,
        nunca como patrón. La interpretación y la verificación son
        clínicas.</p></details>
        <details class="qa alt"><summary class="q">¿Qué ventaja tiene sobre pedirle
        al paciente "que lleve un diario"?</summary>
        <p class="a">Tres: adherencia (la pregunta llega sola y se
        responde en segundos, sin acordarse de escribir), <b>anclaje
        temporal</b> (cada registro lleva hora exacta, sueño, pasos, uso
        del teléfono y pulso si hay sensor), y <b>estructura</b> (el
        informe ya trae contingencias, franjas del día y recuperación
        calculadas — no hojas sueltas).</p></details>
        <details class="qa"><summary class="q">¿Puedo contrastar mis hipótesis del
        caso?</summary>
        <p class="a">Sí. El modo terapeuta permite formular hipótesis
        ("empeora los domingos por la tarde") que el informe contrasta
        prospectivamente con el registro real del período — en modo
        sombra, sin contaminar el detector ni convertir la expectativa en
        conclusión.</p></details>
        <details class="qa alt"><summary class="q">¿Cómo llega la información a la
        sesión?</summary>
        <p class="a">El informe de 6 páginas se genera en el teléfono
        del consultante. <b>Es él quien decide compartirlo</b> — por
        WhatsApp, correo o impreso. No hay monitor remoto: ningún dato
        llega a ti sin que la persona lo entregue.</p></details>
        <details class="qa"><summary class="q">¿Qué pasa con los días sin
        datos?</summary>
        <p class="a">Se reportan como ausentes, con su conteo explícito
        en la página de calidad del dato. Animus nunca trata la ausencia
        de señal como ausencia de evento — una distinción que el
        instrumento declara en el propio informe.</p></details>
        <details class="qa alt"><summary class="q">¿Necesita el paciente un reloj o
        banda?</summary>
        <p class="a">No es imprescindible: Health Connect ya aporta
        sueño, pasos y uso del teléfono. Con un wearable se suma pulso y
        variabilidad, que enriquecen las señales contextuales — pero el
        informe funciona solo con el teléfono.</p></details>
        <details class="qa"><summary class="q">¿Animus diagnostica o predice
        crisis?</summary>
        <p class="a">No. Describe observaciones de una sola persona,
        organizadas para la conversación clínica. No es un dispositivo
        médico, no emite diagnósticos, no predice crisis y no sustituye
        el juicio clínico ni los servicios de emergencia.</p></details>
        <h3>Para ti, si la instalas</h3>
        <details class="qa"><summary class="q">¿Esto es otra app de registrar el
        ánimo?</summary>
        <p class="a">No. Animus combina lo que tu teléfono ya sabe
        (sueño, pasos, uso, actividad) con preguntas breves solo cuando
        hacen falta, y lo convierte en un informe pensado para leerse con
        tu terapeuta. No es un diario vacío: es un mapa.</p></details>
        <details class="qa alt"><summary class="q">¿Cuánto tiempo me quita al
        día?</summary>
        <p class="a">Segundos. Un check-in son dos toques; un episodio
        completo (qué pasó antes, qué hiciste, cómo quedaste) toma menos
        de un minuto. La recolección pasiva no requiere que hagas
        nada.</p></details>
        <details class="qa"><summary class="q">¿Quién puede ver mis datos?</summary>
        <p class="a">Solo tú. Todo se guarda cifrado en tu teléfono —
        no hay cuentas, no hay nube, no hay analítica. El informe se
        comparte solo cuando tú decides compartirlo, como un PDF
        más.</p></details>
        <details class="qa alt"><summary class="q">¿Qué pasa si ignoro una
        pregunta?</summary>
        <p class="a">Nada malo: se registra como "sin respuesta" y ya.
        Los días o momentos sin datos aparecen como ausentes en el
        informe — nadie los inventa.</p></details>
        <details class="qa"><summary class="q">¿La app decide cómo me siento por el
        pulso?</summary>
        <p class="a">No — y es una decisión de diseño importante. El
        pulso es un <b>contexto</b>, no un detector de emociones. Solo
        sirve para preguntarte "¿pasó algo?" en un momento sensible. La
        emoción siempre la dices tú.</p></details>
        <details class="qa alt"><summary class="q">¿Me juzga si tengo una mala
        semana?</summary>
        <p class="a">El informe describe, no evalúa. Muestra qué pasó,
        dónde y cuántas veces — ni puntajes de "bien" o "mal", ni metas
        que fallaste. Es material de conversación, no un boletín.</p></details>
        <details class="qa"><summary class="q">¿Sirve si no voy a terapia?</summary>
        <p class="a">Sí — el informe es tuyo y te ayuda a conocerte con
        números propios. Dicho honestamente: su valor máximo aparece
        cuando se conversa con un profesional, porque las pistas piden
        interpretación.</p></details>
        <details class="qa alt"><summary class="q">¿Consume batería o datos
        móviles?</summary>
        <p class="a">No usa la red para funcionar (todo es local) y las
        lecturas pasivas las hace Android en segundo plano. El consumo
        extra es marginal.</p></details>
        <details class="qa"><summary class="q">¿Puedo borrarlo todo?</summary>
        <p class="a">Sí. Los datos viven solo en tu teléfono: borrar la
        app borra todo. No queda copia en ningún servidor porque no hay
        ningún servidor.</p></details>
        <div class="scinote"><b>Por qué un instrumento idiográfico.</b>
        La tradición del diseño de caso único (N-de-1) — de la psicología
        conductual a la investigación clínica actual — sostiene que los
        patrones más útiles para intervenir son los de <b>esa</b>
        persona: qué antecede, qué sigue, en qué contexto. Animus no
        compara a tu paciente con promedios poblacionales; compara al
        paciente consigo mismo.</div>
        <div class="faq-foot">Animus describe observaciones de una sola
            persona. No diagnostica, no predice crisis y no sustituye la
            supervisión profesional ni los servicios de emergencia.</div>
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
            <a href="#informe">El informe</a>
            <a href="#terapeutas">Para terapeutas</a>
            <a href="#parati">Para ti</a>
            <a href="#privacidad">Privacidad</a>
            <a href="#faq">Preguntas frecuentes</a>
            <a href="?lang=en" target="_self">EN · English</a>
        </nav>
        <a class="mfab mfab-open" href="#mopen" aria-label="Abrir menú">
            <i style="background:{TEAL}"></i><i style="background:{CYAN}"></i><i style="background:{CORAL}"></i>
        </a>
        <a class="mfab mfab-x" href="#mclose" aria-label="Cerrar menú">✕</a>
    </div>
    <div class="sitefoot">
        <div class="foot-grid">
            <div>
                {wordmark()}
                <div class="fnote">Observación conductual estructurada
                para Android. Tus datos se quedan cifrados en tu
                teléfono — no hay cuentas ni nube, y el informe se
                comparte solo cuando tú decides compartirlo.</div>
            </div>
            <div>
                <h6>Explorar</h6>
                <ul>
                    <li><a href="#informe">El informe</a></li>
                    <li><a href="#terapeutas">Para terapeutas</a></li>
                    <li><a href="#parati">Para ti</a></li>
                    <li><a href="#privacidad">Privacidad</a></li>
                    <li><a href="#faq">Preguntas frecuentes</a></li>
                </ul>
            </div>
            <div>
                <h6>Este sitio</h6>
                <ul>
                    <li><a href="mailto:animusapp@protonmail.com">animusapp@protonmail.com</a></li>
                    <li><a href="https://instagram.com/animus.app"
                           target="_blank" rel="noopener">Instagram ·
                           @animus.app</a></li>
                    <li><a href="?lang=en" target="_self">English version</a></li>
                </ul>
                <div class="fnote" style="margin-top:14px">Sin cookies de
                seguimiento ni analítica. Sin cuentas, sin formularios,
                sin recogida de datos.</div>
            </div>
        </div>
        <div class="foot-base">
            <span>Animus — instrumento de observación, no dispositivo
            médico.</span>
            <span>No diagnostica · no predice crisis · no sustituye la
            supervisión profesional ni los servicios de
            emergencia.</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

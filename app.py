"""
Animus Viewer — prototipo de reporte web (solo lectura, en memoria).

Flujo: el usuario sube su export .enc + escribe su PIN.
El archivo se descifra en memoria del servidor local, se renderiza
el reporte y se descarta. Nada se persiste.

Run:  streamlit run app.py
"""

import base64
import hashlib
import io
import json
import unicodedata
from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st
from Crypto.Cipher import AES

# ---------------------------------------------------------------- cifrado

def decrypt_export(file_bytes: bytes, pin: str) -> dict:
    """Sobre .enc: AES-256-GCM, PBKDF2-HMAC-SHA256 (mismo formato que
    ExportCrypto.kt). Lanza excepción si el PIN no corresponde."""
    env = json.loads(file_bytes)

    def b64d(s: str) -> bytes:
        return base64.b64decode(s + "=" * (-len(s) % 4))

    salt = b64d(env["salt_b64"])
    iv = b64d(env["iv_b64"])
    ct = b64d(env["ciphertext_b64"])
    key = hashlib.pbkdf2_hmac(
        "sha256", pin.encode("utf-8"), salt, env["kdf_iterations"], dklen=32
    )
    plain = AES.new(key, AES.MODE_GCM, nonce=iv, mac_len=16) \
        .decrypt_and_verify(ct[:-16], ct[-16:])
    return json.loads(plain)


# ------------------------------------------------------- vocabulario ánimo

CANONICAL = {
    "alegria", "sorpresa", "ansiedad", "miedo",
    "tristeza", "enojo", "asco", "calma", "verguenza", "vacio", "otra",
}

# label compleja → canónica (subconjunto del catálogo de la app)
LABEL_TO_CANONICAL = {
    "calma": "calma", "preocupación": "ansiedad", "preocupacion": "ansiedad",
    "estresado": "ansiedad", "estresado/a": "ansiedad", "inquieto/a": "ansiedad",
    "inquieto": "ansiedad", "angustiado/a": "ansiedad", "tenso/a": "ansiedad",
    "abrumado/a": "ansiedad", "intranquilo/a": "ansiedad", "alterado/a": "ansiedad",
    "motivado/a": "alegria", "contento/a": "alegria", "alivio": "alegria",
    "esperanza": "alegria", "emocionado/a": "alegria", "tranquilo/a": "calma",
    "ilusionado/a": "alegria", "satisfecho/a": "alegria", "pleno/a": "alegria",
    "molesto/a": "enojo", "enfurecido/a": "enojo", "resentido/a": "enojo",
    "fastidiado/a": "enojo", "colérico/a": "enojo", "colerico/a": "enojo",
    "harto/a": "enojo", "deprimido/a": "tristeza", "decaído/a": "tristeza",
    "decaido/a": "tristeza", "apagado/a": "tristeza", "decepcionado/a": "tristeza",
    "resignado/a": "tristeza", "apático/a": "tristeza", "apatico/a": "tristeza",
    "dolido/a": "tristeza", "asustado/a": "miedo", "aterrado/a": "miedo",
    "amenazado/a": "miedo", "vulnerable": "miedo", "acorralado/a": "miedo",
    "impactado/a": "sorpresa", "atónito/a": "sorpresa", "atonito/a": "sorpresa",
    "confundido/a": "sorpresa", "disgusto": "asco", "aversión": "asco",
    "aversion": "asco", "desagrado": "asco", "desprecio": "asco",
    "vergüenza": "verguenza", "verguenza": "verguenza", "vacío": "vacio",
    "vacio": "vacio", "cansancio": "otra", "agotado/a": "otra",
    "fatigado/a": "otra",
}

MOOD_CONTEXTS = {
    "emotion_checkin", "morning_mood", "evening_mood",
    "calendar_pre", "calendar_post",
}

SLEEP_SCALE = {"muy_mal": 1, "mal": 2, "regular": 3, "bien": 4, "muy_bien": 5}

EMOTION_COLORS = {
    "alegria": "#F5B642", "sorpresa": "#8E7CC3", "ansiedad": "#7FA6C9",
    "miedo": "#5C4E7A", "tristeza": "#4A6FA5", "enojo": "#E8553E",
    "asco": "#6B8F5A", "calma": "#7FBFB0", "verguenza": "#C98BA6",
    "vacio": "#8A8A8A", "otra": "#B0B0B0",
}

PROMPT_LABELS = {
    "scheduled": "Pregunta programada",
    "emotion_checkin": "Check-in espontáneo",
    "signal_contingent": "Señal (biometría)",
    "nightly_review": "Revisión nocturna",
    "morning_sleep": "Pregunta de sueño",
    "morning_mood": "Ánimo matutino",
    "calendar_pre": "Actividad (antes)",
    "calendar_post": "Actividad (después)",
    "therapist_reminder": "Recordatorio terapeuta",
}

VARIABLE_LABELS = {
    "heart_rate": "Ritmo cardíaco",
    "hrv_rmssd": "Variabilidad FC (RMSSD)",
    "steps": "Pasos",
    "sleep_minutes": "Sueño",
    "phone_usage_min": "Uso de teléfono",
}


def _strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def canonical_emotion(resp: dict) -> str | None:
    """Misma lógica que Métricas: mood_emoji canónico si existe; si no,
    free_text mapeado por label."""
    me = (resp.get("mood_emoji") or "").strip().lower()
    if me in CANONICAL:
        return me
    ft = (resp.get("free_text") or "").strip()
    if not ft:
        return None
    key = _strip_accents(ft.lower())
    if key in CANONICAL:
        return key
    return LABEL_TO_CANONICAL.get(ft.lower()) or LABEL_TO_CANONICAL.get(key)


def ts(s) -> pd.Timestamp | None:
    if not s:
        return None
    return pd.to_datetime(s, errors="coerce")


# ------------------------------------------------------------------- app

st.set_page_config(page_title="Animus — Reporte", page_icon="🫀",
                   layout="wide")
st.title("Reporte de dinámica emocional")
st.caption("Prototipo — el archivo se procesa en memoria y se descarta. "
           "Nada se almacena.")

with st.sidebar:
    st.header("Tus datos")
    enc_file = st.file_uploader("Export (.enc)", type=["enc"])
    pin = st.text_input("PIN de descifrado", type="password")

    # Solo para prototipo local: carga sample.enc + PIN del config del
    # proyecto sin tipear nada. En producción no existiría.
    use_sample = st.button("⚙️ Usar export de ejemplo (dev)")
    if use_sample:
        import os
        sample = os.path.join(os.path.dirname(__file__), "sample.enc")
        cfg = os.path.join(
            os.path.dirname(__file__), "..", "windsurf-project",
            "thcd-monitor", "app", "src", "main", "assets",
            "supabase_config.json")
        if os.path.exists(sample) and os.path.exists(cfg):
            enc_file = io.BytesIO(open(sample, "rb").read())
            pin = json.load(open(cfg))["master_pin"]
        else:
            st.error("sample.enc o config no encontrados")

    st.divider()
    days = st.select_slider("Período del reporte",
                            options=[7, 14, 30, 90, 0],
                            value=30,
                            format_func=lambda d: "Todo" if d == 0 else
                            f"Últimos {d} días")

if not enc_file:
    st.info("Sube tu archivo `datos_pasivos_*.json.enc` "
            "(se genera desde la app → Exportar datos).")
    st.stop()
if not pin:
    st.warning("Escribe tu PIN de descifrado.")
    st.stop()

try:
    data = decrypt_export(enc_file.getvalue(), pin)
except Exception:
    st.error("No se pudo descifrar — ¿el PIN es correcto?")
    st.stop()

# ------------------------------------------------------------- dataframes

responses = pd.DataFrame(data.get("ema_responses", []))
if not responses.empty:
    responses["dt"] = pd.to_datetime(responses["responded_at"],
                                     errors="coerce")
    responses["canonical"] = responses.apply(canonical_emotion, axis=1)

daily = pd.DataFrame(data.get("daily_summaries", []))
if not daily.empty:
    daily["dt"] = pd.to_datetime(daily["date"])
    anomalies = pd.DataFrame(
        [a | {"date": row["date"]}
         for _, row in daily.iterrows() for a in row.get("anomalies", [])]
    )
    if not anomalies.empty:
        anomalies["dt"] = pd.to_datetime(anomalies["ts"], errors="coerce")
else:
    anomalies = pd.DataFrame()

episodes = pd.DataFrame([
    {
        "dt": ts(e.get("timestamp_onset")),
        "emotion": (e.get("emotion") or {}).get("label"),
        "intensity": (e.get("emotion") or {}).get("intensity"),
        "other": (e.get("emotion") or {}).get("other_text"),
        "antecedent": (e.get("antecedent") or {}).get("type"),
        "antecedent_note": (e.get("antecedent") or {}).get("note"),
        "life_area": e.get("life_area"),
        "status": e.get("status"),
        "duration_min": e.get("duration_approx_min"),
        "confirmed_via": e.get("confirmed_via"),
    }
    for e in data.get("episodes", [])
])
if not episodes.empty:
    episodes["dt"] = pd.to_datetime(episodes["dt"], errors="coerce")

# filtro de período
if days and not responses.empty:
    cutoff = responses["dt"].max() - pd.Timedelta(days=days)
    responses = responses[responses["dt"] >= cutoff]
    if not episodes.empty:
        episodes = episodes[episodes["dt"] >= cutoff]
    if not daily.empty:
        daily = daily[daily["dt"] >= cutoff.tz_localize(
            responses["dt"].dt.tz, ambiguous="raise")
            .tz_localize(None)]
    if not anomalies.empty:
        anomalies = anomalies[anomalies["dt"] >= cutoff]

# ---------------------------------------------------------------- header

c1, c2, c3 = st.columns(3)
c1.metric("Paciente", (data.get("patient_id") or "?")[:12])
c2.metric("Generado", (data.get("generated_at") or "?")[:10])
c3.metric("Zona horaria", data.get("timezone", "?"))

mood = responses[responses["context"].isin(MOOD_CONTEXTS)] \
    if not responses.empty else responses
mood_canon = mood[mood["canonical"].notna()]

n_ep = len(episodes)
fired = anomalies[anomalies["decision"] == "fired"] \
    if not anomalies.empty else anomalies

k1, k2, k3, k4 = st.columns(4)
k1.metric("Check-ins de ánimo", len(mood_canon))
k2.metric("Episodios registrados", n_ep)
k3.metric("Respuestas totales", len(responses))
k4.metric("Señales que preguntaron", len(fired))

st.divider()

# ------------------------------------------------------ dinámica emocional

st.header("Dinámica emocional")
col_a, col_b = st.columns([1, 2])

with col_a:
    if not mood_canon.empty:
        counts = mood_canon["canonical"].value_counts().reset_index()
        counts.columns = ["emotion", "n"]
        fig = px.pie(counts, names="emotion", values="n", hole=0.55,
                     color="emotion", color_discrete_map=EMOTION_COLORS)
        fig.update_traces(textinfo="label+percent")
        fig.update_layout(showlegend=False, margin=dict(t=10, b=10),
                          height=340)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sin check-ins de ánimo en el período.")

with col_b:
    if not mood_canon.empty:
        tl = mood_canon.copy()
        tl["label"] = tl["free_text"].fillna(tl["canonical"])
        fig = px.scatter(
            tl, x="dt", y="canonical", color="canonical",
            color_discrete_map=EMOTION_COLORS, hover_data=["label", "context"],
            labels={"dt": "", "canonical": "Emoción"},
        )
        fig.update_layout(showlegend=False, margin=dict(t=10, b=10),
                          height=340)
        st.plotly_chart(fig, use_container_width=True)

    # intensidad cuando existe
    inten = mood_canon[mood_canon["activation_0_10"].notna()]
    if not inten.empty:
        st.caption(
            f"Intensidad media reportada: "
            f"**{inten['activation_0_10'].mean():.1f}/10** "
            f"(en {len(inten)} check-ins que la marcaron)"
        )

# ------------------------------------------------------------- adherencia

st.header("Respuestas a recordatorios")
if not responses.empty:
    ad = responses.groupby("prompt_type").size().reset_index(name="n")
    ad["tipo"] = ad["prompt_type"].map(
        lambda t: PROMPT_LABELS.get(t, t or "?"))
    ad = ad.sort_values("n", ascending=False)
    fig = px.bar(ad, x="n", y="tipo", orientation="h",
                 labels={"n": "respuestas", "tipo": ""})
    fig.update_layout(margin=dict(t=10), height=300)
    st.plotly_chart(fig, use_container_width=True)

    nightly = responses[
        responses["context"].astype(str).str.contains("calmer", na=False)]
    if not nightly.empty:
        calmer = Counter(
            json.loads(c)["calmer"] for c in nightly["context"]
            if c.startswith("{"))
        missed = sum(1 for c in nightly["context"]
                     if c.startswith("{") and
                     json.loads(c).get("missed_event"))
        st.caption(
            f"Revisión nocturna — ¿más tranquilo/a al final del día? "
            + " · ".join(f"{k}: {v}" for k, v in calmer.items())
            + f" · **{missed}** veces pasó algo que la app no observó"
        )

# --------------------------------------------------------- episodios ABC

st.header("Episodios (ABC)")
if not episodes.empty:
    show = episodes.copy()
    show["emoción"] = show["other"].fillna(show["emotion"])
    tbl = show[["dt", "emoción", "intensity", "antecedent", "life_area",
                "duration_min", "status"]].rename(columns={
        "dt": "fecha", "intensity": "intensidad",
        "antecedent": "antecedente", "life_area": "área",
        "duration_min": "duración (min)", "status": "tipo",
    }).sort_values("fecha", ascending=False)
    st.dataframe(tbl, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        em_ct = episodes["emotion"].value_counts().head(8).reset_index()
        em_ct.columns = ["emotion", "n"]
        fig = px.bar(em_ct, x="emotion", y="n", color="emotion",
                     color_discrete_map=EMOTION_COLORS)
        fig.update_layout(showlegend=False, margin=dict(t=10), height=280,
                          title="Emociones en episodios")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        la_ct = episodes["life_area"].value_counts().reset_index()
        la_ct.columns = ["area", "n"]
        fig = px.bar(la_ct, x="area", y="n")
        fig.update_layout(margin=dict(t=10), height=280,
                          title="Por área de vida")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Sin episodios en el período.")

# --------------------------------------------------------------- señales

st.header("Señales fisiológicas observadas")
if not anomalies.empty:
    an = anomalies.copy()
    an["var"] = an["variable"].map(VARIABLE_LABELS).fillna(an["variable"])
    c1, c2 = st.columns(2)
    with c1:
        dec = an.groupby(["var", "decision"]).size().reset_index(name="n")
        fig = px.bar(dec, x="var", y="n", color="decision",
                     color_discrete_map={"fired": "#E8553E",
                                         "suppressed": "#9AA5B1"},
                     labels={"var": "", "decision": "decisión"})
        fig.update_layout(margin=dict(t=10), height=300)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        out = an[an["outcome"] != "pending"]["outcome"].map(
            {"posible_tp": "confirmada por paciente",
             "posible_fp": "descartada por paciente"}
        ).value_counts().reset_index()
        out.columns = ["resultado", "n"]
        pending_n = (an["decision"] == "fired").sum() - out["n"].sum()
        st.markdown("**Desviaciones que preguntaron**")
        st.dataframe(out, hide_index=True, use_container_width=True)
        st.caption(
            f"{max(pending_n,0)} preguntas aún sin respuesta · "
            "una señal observada no implica que algo ocurrió — "
            "el paciente confirma o descarta."
        )
else:
    st.info("Sin eventos de señal en el período.")

# ----------------------------------------------------------------- sueño

st.header("Sueño")
c1, c2 = st.columns(2)
with c1:
    if not daily.empty:
        sd = daily[["date"]].copy()
        sd["horas"] = daily["sleep"].map(
            lambda s: round((s.get("sessions", 0) or 0) * 0, 1)
            if isinstance(s, dict) else 0)
        # sessions es un conteo en el export; si hubiera duración se usaría
        mins = daily["sleep"].map(
            lambda s: s.get("total_minutes") if isinstance(s, dict) else None)
        if mins.notna().any():
            sd["horas"] = (mins.astype(float) / 60).round(2)
        else:
            sd["sesiones"] = daily["sleep"].map(
                lambda s: s.get("sessions", 0) if isinstance(s, dict) else 0)
        if "horas" in sd.columns and sd["horas"].sum() > 0:
            fig = px.bar(sd, x="date", y="horas",
                         labels={"date": "", "horas": "horas medidas"})
            fig.update_layout(margin=dict(t=10), height=260,
                              title="Sueño medido (Health Connect)")
            st.plotly_chart(fig, use_container_width=True)
        elif "sesiones" in sd.columns:
            st.metric("Noches con sesión registrada",
                      int((sd["sesiones"] > 0).sum()))
with c2:
    if not responses.empty:
        sr = responses[responses["context"] == "morning_sleep_review"].copy()
        if not sr.empty:
            sr["valor"] = sr["free_text"].map(SLEEP_SCALE)
            sr["fecha"] = sr["dt"].dt.date.astype(str)
            fig = px.bar(sr, x="fecha", y="valor",
                         labels={"fecha": "", "valor": "1–5"},
                         title="Cómo dormiste según tu reporte")
            fig.update_yaxes(range=[0, 5.4])
            fig.update_layout(margin=dict(t=30), height=240)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sin reportes subjetivos de sueño.")

# --------------------------------------------------------------- patrones

st.header("Patrones observados por Animus")
st.caption("Reglas minadas de tus propios registros — tentativas, "
           "nunca diagnóstico. `n` = veces que aplicó; precisión = "
           "aciertos cuando disparó.")

rules = pd.DataFrame(data.get("learned_rules", []))
if not rules.empty:
    rules["confianza"] = (rules["precision"] * 100).round(0).astype(int)
    rules["estado"] = rules["state"].map(
        {"candidate": "candidata", "validated": "validada",
         "active": "activa", "rejected": "descartada"}).fillna(rules["state"])
    st.dataframe(
        rules[["description", "n_cases", "confianza", "estado"]]
        .rename(columns={"description": "regla", "n_cases": "n",
                         "confianza": "precisión %"}),
        hide_index=True, use_container_width=True)
else:
    st.info("Aún no hay reglas minadas — necesita más historia.")

sigs = pd.DataFrame(data.get("emotion_signatures", []))
if not sigs.empty:
    with st.expander("Firmas emoción → pulso (contextuales)"):
        st.caption("Mediana del cambio de pulso en reposo cuando registraste "
                   "cada emoción. Contexto, no detección.")
        st.dataframe(
            sigs[["emotion", "activity_bucket", "median_delta", "n",
                  "status"]].rename(columns={
                "emotion": "emoción", "activity_bucket": "actividad",
                "median_delta": "ΔFC mediana", "n": "n",
                "status": "estado"}),
            hide_index=True, use_container_width=True)

# ------------------------------------------------------- calidad de dato

with st.expander("Calidad del dato y cobertura"):
    if not daily.empty:
        dq = daily[["date"]].copy()
        dq["missingness"] = daily["missingness"].map(
            lambda m: m.get("events", 0) if isinstance(m, dict) else 0)
        st.markdown("**Eventos de datos faltantes por día**")
        fig = px.bar(dq, x="date", y="missingness",
                     labels={"date": "", "missingness": "eventos"})
        fig.update_layout(margin=dict(t=10), height=220)
        st.plotly_chart(fig, use_container_width=True)

    sources = (data.get("device_profile") or {}).get("sources") or []
    if sources:
        src = pd.DataFrame([{
            "tipo": VARIABLE_LABELS.get(s["record_type"], s["record_type"]),
            "disponible": "sí" if s.get("available") else "no",
            "cobertura %": s.get("coverage_pct"),
            "latencia mediana (min)": s.get("latency_median_min"),
            "origen": s.get("data_origin"),
        } for s in sources])
        st.markdown("**Fuentes**")
        st.dataframe(src, hide_index=True, use_container_width=True)

st.divider()
st.caption(
    "⚕️ Este reporte describe observaciones de una sola persona. "
    "No diagnostica, no predice crisis y no sustituye la supervisión "
    "profesional ni los servicios de emergencia."
)

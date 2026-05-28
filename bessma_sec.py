import streamlit as st
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SEC Capture CO₂",
    page_icon="🌬️",
    layout="wide"
)

# ─────────────────────────────────────────────────────────────
# STYLE
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

.stApp {
    background-color: #0f1117;
    color: #c9d6df;
}

h1,h2,h3 {
    font-family: 'IBM Plex Mono', monospace;
    color: #e8f4f8;
    text-align: center;
}

.card {
    background: linear-gradient(135deg, #1a2332, #16202e);
    border: 1px solid #2a3f55;
    border-left: 4px solid #00b4d8;
    border-radius: 8px;
    padding: 18px 22px;
    margin: 10px 0;
    font-family: 'IBM Plex Mono', monospace;
}

.card.total {
    border-left-color: #f77f00;
    background: linear-gradient(135deg,#1f1a0f,#1a1608);
}

.card-label {
    font-size:0.75rem;
    letter-spacing:0.12em;
    text-transform:uppercase;
    color:#6b8fa3;
    margin-bottom:4px;
}

.card-value {
    font-size:1.9rem;
    font-weight:600;
    color:#e8f4f8;
}

.card-unit {
    font-size:0.8rem;
    color:#6b8fa3;
    margin-top:2px;
}

.sec-header {
    font-family:'IBM Plex Mono',monospace;
    font-size:0.7rem;
    letter-spacing:0.18em;
    text-transform:uppercase;
    color:#00b4d8;
    border-bottom:1px solid #1e3448;
    padding-bottom:6px;
    margin:26px 0 14px 0;
}

.row {
    display:flex;
    justify-content:space-between;
    padding:8px 0;
    border-bottom:1px solid #1a2a3a;
    font-size:0.87rem;
    color:#8aa5bc;
}

.val {
    font-family:'IBM Plex Mono',monospace;
    color:#c9d6df;
    font-weight:600;
}

.info {
    background:#111827;
    border:1px solid #1e3448;
    border-radius:6px;
    padding:13px 17px;
    font-size:0.81rem;
    color:#6b8fa3;
    margin:8px 0;
    line-height:1.65;
}

.err {
    background:#1f0a0a;
    border:1px solid #8b1a1a;
    border-radius:6px;
    padding:12px 16px;
    color:#ff6b6b;
    font-size:0.85rem;
}

.formula {
    background:#0a1628;
    border:1px solid #1e3448;
    border-radius:6px;
    padding:12px 16px;
    font-family:'IBM Plex Mono',monospace;
    font-size:0.82rem;
    color:#48cae4;
    margin:8px 0;
}

.stButton>button {
    background:#00b4d8;
    color:#0f1117;
    font-family:'IBM Plex Mono',monospace;
    font-weight:600;
    border:none;
    border-radius:4px;
    padding:10px 28px;
    width:100%;
}

.stButton>button:hover {
    background:#48cae4;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# LOGO FIXE
# ─────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns([1,2,1])

with c2:
    st.image(
        "photo_2026-05-26_02-09-18.png",
        width=300
    )

# ─────────────────────────────────────────────────────────────
# TITRE
# ─────────────────────────────────────────────────────────────
st.markdown("# 🌬️ SEC Capture CO₂ — 8 760 valeurs horaires")

# ─────────────────────────────────────────────────────────────
# FORMULES
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="formula">

CI(h) = C*_CO₂(h) [kg/m³]

<br><br>

CI = ((P_atm − P_v) · x_CO₂ · M_CO₂)/(R · T_K)

<br><br>

SEC_elec(h) = ΔP · (1+ε)/(η_elec · CI · α · 3600)

<br><br>

SEC_th(h) = SEC_th[GJ/t] · 277.778 · (T_cible − T_air)/(η_th · T_cible)

<br><br>

SEC_total(h) = SEC_elec(h) + SEC_th(h)

</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PARAMÈTRES
# ─────────────────────────────────────────────────────────────
st.markdown(
    '<div class="sec-header">⚙️ PARAMÈTRES</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown("### ⚡ Électrique")

    delta_P = st.number_input(
        "ΔP ventilateur (Pa)",
        value=236.8
    )

    eps_pct = st.number_input(
        "ε pertes auxiliaires (%)",
        value=15.0
    )

    eta_elec = st.number_input(
        "η_elec",
        value=0.75
    )

    alpha = st.number_input(
        "α taux capture CO₂",
        value=0.70
    )

with c2:

    st.markdown("### 🌫️ CO₂")

    x_CO2 = st.number_input(
        "x_CO₂ fraction molaire",
        value=0.0004,
        format="%.4f"
    )

    SEC_th_GJ = st.selectbox(
        "SEC_th [GJ/t CO₂]",
        [2, 3, 4],
        index=1
    )

    T_cible = st.number_input(
        "T_cible (°C)",
        value=100.0
    )

with c3:

    st.markdown("### 🔥 Thermique")

    eta_th = st.number_input(
        "η_th",
        value=0.45
    )

# ─────────────────────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────────────────────
M_CO2 = 0.044011
R = 8.314

# ─────────────────────────────────────────────────────────────
# VÉRIFICATION HEURE 1
# ─────────────────────────────────────────────────────────────
st.markdown(
    '<div class="sec-header">🔢 VÉRIFICATION — HEURE 1</div>',
    unsafe_allow_html=True
)

Tc_v = 7.69
RH_v = 59.13
SP_v = 95490

Tk_v = Tc_v + 273.15

Pv_v = (
    RH_v/100
) * (
    610.94 * np.exp(17.625*Tc_v/(Tc_v+243.04))
)

CI_v = (
    (SP_v - Pv_v)
    * x_CO2
    * M_CO2
) / (
    R * Tk_v
)

SEC_elec_v = (
    delta_P * (1 + eps_pct/100)
) / (
    eta_elec * CI_v * alpha * 3600
)

SEC_th_v = (
    SEC_th_GJ
    * 277.778
    * (T_cible - Tc_v)
) / (
    eta_th * T_cible
)

SEC_tot_v = SEC_elec_v + SEC_th_v

a, b, c, d = st.columns(4)

with a:
    st.markdown(f"""
    <div class="card">
        <div class="card-label">CI</div>
        <div class="card-value">{CI_v:.7f}</div>
        <div class="card-unit">kg/m³</div>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown(f"""
    <div class="card">
        <div class="card-label">SEC_elec</div>
        <div class="card-value">{SEC_elec_v:.2f}</div>
        <div class="card-unit">kWh/t</div>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown(f"""
    <div class="card">
        <div class="card-label">SEC_th</div>
        <div class="card-value">{SEC_th_v:.2f}</div>
        <div class="card-unit">kWh/t</div>
    </div>
    """, unsafe_allow_html=True)

with d:
    st.markdown(f"""
    <div class="card total">
        <div class="card-label">SEC_total</div>
        <div class="card-value">{SEC_tot_v:.2f}</div>
        <div class="card-unit">kWh/t</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# IMPORT FICHIER
# ─────────────────────────────────────────────────────────────
st.markdown(
    '<div class="sec-header">📂 IMPORT FICHIER</div>',
    unsafe_allow_html=True
)

uploaded = st.file_uploader(
    "Importer fichier Excel ou CSV",
    type=["xlsx", "xls", "csv"]
)

if uploaded:

    try:

        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded, sep=None, engine="python")
        else:
            df = pd.read_excel(uploaded)

    except Exception as e:

        st.error(e)
        st.stop()

    df.columns = [c.strip().upper() for c in df.columns]

    aliases = {
        "T": ["T2M", "TEMP", "TEMPERATURE"],
        "SP": ["SP", "PRESSURE", "PATM"],
        "RH": ["RH", "HR", "HUMIDITY"]
    }

    col_map = {}

    for var, names in aliases.items():
        for name in names:
            if name in df.columns:
                col_map[var] = name
                break

    st.markdown(
        '<div class="sec-header">👁️ APERÇU</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    if st.button("▶ CALCULER LES 8 760 SEC"):

        Tc = df[col_map["T"]].astype(float).values
        SP = df[col_map["SP"]].astype(float).values
        RH = df[col_map["RH"]].astype(float).values

        Tk = Tc + 273.15

        Pv = (
            RH/100
        ) * (
            610.94 * np.exp(17.625*Tc/(Tc+243.04))
        )

        CI_h = (
            (SP - Pv)
            * x_CO2
            * M_CO2
        ) / (
            R * Tk
        )

        SEC_elec_h = (
            delta_P * (1 + eps_pct/100)
        ) / (
            eta_elec * CI_h * alpha * 3600
        )

        SEC_th_h = (
            SEC_th_GJ
            * 277.778
            * (T_cible - Tc)
        ) / (
            eta_th * T_cible
        )

        SEC_total_h = SEC_elec_h + SEC_th_h

        results = pd.DataFrame({

            "Heure":
            np.arange(1, len(df)+1),

            "T2m (°C)":
            np.round(Tc, 2),

            "SP (Pa)":
            np.round(SP, 1),

            "RH (%)":
            np.round(RH, 2),

            "CI (kg/m³)":
            np.round(CI_h, 7),

            "SEC_elec (kWh/t)":
            np.round(SEC_elec_h, 2),

            "SEC_th (kWh/t)":
            np.round(SEC_th_h, 2),

            "SEC_total (kWh/t)":
            np.round(SEC_total_h, 2)
        })

        # ─────────────────────────────────────────────
        # STATISTIQUES
        # ─────────────────────────────────────────────
        st.markdown(
            '<div class="sec-header">📊 STATISTIQUES</div>',
            unsafe_allow_html=True
        )

        s1, s2, s3 = st.columns(3)

        with s1:
            st.metric(
                "CI moyen",
                f"{np.nanmean(CI_h):.7f}"
            )

        with s2:
            st.metric(
                "SEC elec moyen",
                f"{np.nanmean(SEC_elec_h):.2f}"
            )

        with s3:
            st.metric(
                "SEC total moyen",
                f"{np.nanmean(SEC_total_h):.2f}"
            )

        # ─────────────────────────────────────────────
        # TABLEAU
        # ─────────────────────────────────────────────
        st.markdown(
            '<div class="sec-header">📄 RÉSULTATS</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            results,
            use_container_width=True,
            height=500
        )

        # ─────────────────────────────────────────────
        # EXPORT CSV
        # ─────────────────────────────────────────────
        csv = results.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Télécharger CSV",
            csv,
            "SEC_8760_resultats.csv",
            "text/csv"
        )

else:

    st.markdown("""
    <div class="info" style="text-align:center;padding:32px;">
    ⬆️ Importez votre fichier Excel ou CSV contenant :
    T2m · SP · RH
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("---")

st.markdown("""
<p style="
font-size:0.75rem;
color:#3a5068;
text-align:center;
font-family:'IBM Plex Mono',monospace;
">
USTHB · MASTER SCIENCES ET TECHNIQUES DE L’HYDROGÈNE VERT
</p>
""", unsafe_allow_html=True)

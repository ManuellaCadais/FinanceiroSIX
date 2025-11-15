import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import base64
from datetime import datetime
import os

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================
st.set_page_config(
    page_title="SIX Dashboard",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# PALETA SIX
# ==========================================================
PALETA_SIX = [
    "#F7DF0E", "#FFF48B", "#FFF9C4", "#FFFDE7",
    "#C6B80B", "#9B9108", "#9E931D",
    "#3C52FF", "#7383FF",
    "#0EF7A0", "#F70ECC"
]

PRIMARY_COLOR = "#F7DF0E"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#FFD700"

# ==========================================================
# FUNÇÃO PARA BACKGROUND
# ==========================================================
def get_image_base64():
    try:
        bg_path = os.path.abspath("SIX-BG.jpg")
        with open(bg_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

BG64 = get_image_base64()

# ==========================================================
# CSS
# ==========================================================
def load_css():
    st.markdown(f"""
    <style>

        .stApp {{
            background: url('data:image/jpeg;base64,{BG64}');
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}

        .stApp::before {{
            content: '';
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.65);
            z-index: -1;
        }}

        h1, h2, h3 {{
            color: {PRIMARY_COLOR} !important;
            text-shadow: 0 0 15px rgba(247,223,14,0.3);
        }}

        .metric-card {{
            background: rgba(0,0,0,0.55);
            border: 2px solid {PRIMARY_COLOR};
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}

        .metric-label {{
            color: {ACCENT_COLOR};
            font-size: 0.9em;
        }}

        .metric-value {{
            color: {PRIMARY_COLOR};
            font-size: 2em;
            font-weight: bold;
        }}

        .chart-container {{
            background: rgba(0,0,0,0.50);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid {PRIMARY_COLOR};
            margin-top: 15px;
        }}

    </style>
    """, unsafe_allow_html=True)

load_css()

# ==========================================================
# CARREGAR DADOS
# ==========================================================
@st.cache_data
def load_data():
    df_grandes = pd.read_excel("Base_Six.xlsx", sheet_name="Grandes Números")
    df_financeiro = pd.read_excel("Base_Six.xlsx", sheet_name="Financeiro")

    df_grandes.columns = df_grandes.columns.str.replace(r"\s+", " ", regex=True).str.strip()
    df_financeiro.columns = df_financeiro.columns.str.replace(r"\s+", " ", regex=True).str.strip()

    return df_grandes, df_financeiro

df_grandes, df_financeiro = load_data()

# ==========================================================
# LOGO
# ==========================================================
col1, col2, col3 = st.columns([1,1,1])
with col2:
    try:
        logo = Image.open("LogoPNG.png")
        st.image(logo, width=150)
    except:
        st.write("Logo não encontrada")

st.markdown("<h1 style='text-align:center;'>SIX DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; opacity:0.8;'>Análise Integrada de Dados</h3>", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR — FILTROS
# ==========================================================
st.sidebar.markdown(f"<h2 style='color:{PRIMARY_COLOR};'>🎯 Filtros</h2>", unsafe_allow_html=True)

# ---- Unidade ----
unidades = sorted(df_grandes["Unidade"].unique())
unidade_selecionada = st.sidebar.multiselect(
    "Selecione a Unidade:",
    unidades,
    default=unidades
)

df_grandes_filtrado = df_grandes[df_grandes["Unidade"].isin(unidade_selecionada)]

# ---- Meses ----
df_financeiro["Mês"] = pd.to_datetime(df_financeiro["Mês"])
df_financeiro["Mes_Nome"] = df_financeiro["Mês"].dt.month.map({
    8: "Agosto",
    9: "Setembro",
    10: "Outubro"
})

meses_unicos = ["Agosto", "Setembro", "Outubro"]

meses_selecionados = st.sidebar.multiselect(
    "Selecione o(s) Mês(es):",
    options=meses_unicos,
    default=meses_unicos
)

df_financeiro_filtrado = df_financeiro[
    (df_financeiro["Unidade"].isin(unidade_selecionada)) &
    (df_financeiro["Mes_Nome"].isin(meses_selecionados))
]

# ==========================================================
# ABAS
# ==========================================================
tab1, tab2, tab3 = st.tabs(["📊 Visão Geral", "💰 Financeiro", "👥 Clientes"])


# ==========================================================
# TAB 1 – VISÃO GERAL
# ==========================================================
with tab1:
    st.markdown("## Visão Geral das Unidades")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Ativos</div><div class='metric-value'>{df_grandes_filtrado['Ativos'].sum():,}</div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Adimplentes</div><div class='metric-value'>{df_grandes_filtrado['Adimplentes'].sum():,}</div></div>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Inadimplentes</div><div class='metric-value'>{df_grandes_filtrado['Inadimplentes'].sum():,}</div></div>", unsafe_allow_html=True)

    with col4:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Personal</div><div class='metric-value'>{df_grandes_filtrado['Personal'].sum():,}</div></div>", unsafe_allow_html=True)

    with col5:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>VIP</div><div class='metric-value'>{df_grandes_filtrado['VIP'].sum():,}</div></div>", unsafe_allow_html=True)

    with col6:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Suspensos</div><div class='metric-value'>{df_grandes_filtrado['Suspensos'].sum():,}</div></div>", unsafe_allow_html=True)


# ==========================================================
# TAB 2 – FINANCEIRO
# ==========================================================
with tab2:
    st.markdown("## Indicadores Financeiros")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Faturamento Total</div><div class='metric-value'>R$ {df_financeiro_filtrado['Faturamento'].sum():,.0f}</div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Lucro Operacional</div><div class='metric-value'>R$ {df_financeiro_filtrado['Lucro Operavional'].sum():,.0f}</div></div>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Reinvestimentos</div><div class='metric-value'>R$ {df_financeiro_filtrado['Reinvestimentos'].sum():,.0f}</div></div>", unsafe_allow_html=True)

    with col4:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Retirada de Sócios</div><div class='metric-value'>R$ {df_financeiro_filtrado['Retirada de Sócios'].sum():,.0f}</div></div>", unsafe_allow_html=True)


    # -------- LUCRO MENSAL --------
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)

    df_lucro = df_financeiro_filtrado.groupby("Mes_Nome")["Lucro Operavional"].sum().reset_index()
    df_lucro = df_lucro.sort_values(by=["Mes_Nome"], key=lambda x: x.map({"Agosto":1,"Setembro":2,"Outubro":3}))

    fig_lucro = px.bar(
        df_lucro,
        x="Lucro Operavional",
        y="Mes_Nome",
        orientation="h",
        title="Lucro Mensal",
        color="Mes_Nome",
        color_discrete_sequence=PALETA_SIX
    )
    fig_lucro.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.3)",
        font_color=TEXT_COLOR
    )

    st.plotly_chart(fig_lucro, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


    # -------- FATURAMENTO AGRUPADO --------
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)

    df_fat = df_financeiro_filtrado.groupby(["Mes_Nome", "Unidade"])["Faturamento"].sum().reset_index()
    df_fat = df_fat.sort_values(by=["Mes_Nome"], key=lambda x: x.map({"Agosto":1,"Setembro":2,"Outubro":3}))

    fig_fat = px.bar(
        df_fat,
        x="Mes_Nome",
        y="Faturamento",
        color="Unidade",
        barmode="group",
        title="Faturamento por Unidade",
        color_discrete_sequence=PALETA_SIX
    )
    fig_fat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.3)",
        font_color=TEXT_COLOR
    )

    st.plotly_chart(fig_fat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================
# TAB 3 – CLIENTES
# ==========================================================
with tab3:
    st.markdown("## Comparativo de Planos")

    dfp = df_grandes_filtrado.copy()

    # ---------- Gráfico comparativo ----------
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)

    df_long = dfp.melt(
        id_vars="Unidade",
        value_vars=["Ativos", "Adimplentes", "Inadimplentes", "Personal", "VIP", "Suspensos"],
        var_name="Categoria",
        value_name="Quantidade"
    )

    fig_comp = px.bar(
        df_long,
        x="Categoria",
        y="Quantidade",
        color="Categoria",
        barmode="group",
        title="Comparativo de Planos",
        color_discrete_sequence=PALETA_SIX
    )
    fig_comp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.3)",
        font_color=TEXT_COLOR
    )

    st.plotly_chart(fig_comp, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Pizza Adimplentes vs Inadimplentes ----------
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)

    total_ad = dfp["Adimplentes"].sum()
    total_inad = dfp["Inadimplentes"].sum()

    fig_pie = px.pie(
        names=["Adimplentes", "Inadimplentes"],
        values=[total_ad, total_inad],
        color=["Adimplentes", "Inadimplentes"],
        title="Planos Ativos",
        color_discrete_sequence=["#3C52FF", "#F70ECC"]
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color=TEXT_COLOR
    )

    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================
# FOOTER
# ==========================================================
st.markdown(f"""
<hr>
<p style='text-align:center; opacity:.7;'>
SIX Dashboard © 2025 — Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M')}
</p>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── PÁGINA ────────────────────────────────────────────────────
st.set_page_config(
    page_title="People Analytics",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DESIGN SYSTEM ─────────────────────────────────────────────
C = {
    "bg":     "#060810",
    "bg2":    "#0a0e1a",
    "bg3":    "#0d1220",
    "bg4":    "#131b2e",
    "border": "rgba(255,255,255,0.06)",
    "blue":   "#4f8ef7",
    "teal":   "#2dd4bf",
    "pink":   "#f472b6",
    "amber":  "#fbbf24",
    "green":  "#4ade80",
    "red":    "#f87171",
    "purple": "#a78bfa",
    "cyan":   "#22d3ee",
    "text":   "#e2e8f0",
    "text2":  "#64748b",
    "text3":  "#2d3748",
}

PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color=C["text2"], size=11),
    margin=dict(l=4, r=4, t=8, b=4),
    hoverlabel=dict(bgcolor=C["bg3"], font_color=C["text"], bordercolor=C["border"]),
)

# ── CSS PREMIUM ───────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@600;700;800&display=swap');

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

/* Base */
.stApp {{ background-color: {C["bg"]}; }}
.main .block-container {{
    padding: 24px 36px 48px !important;
    max-width: 100% !important;
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {C["bg2"]} 0%, {C["bg"]} 100%);
    border-right: 1px solid rgba(79,142,247,.12);
}}
section[data-testid="stSidebar"] > div:first-child {{
    padding: 24px 18px 20px;
}}
section[data-testid="stSidebar"] .stSelectbox label {{ display:none; }}
section[data-testid="stSidebar"] .stSelectbox > div > div {{
    background: rgba(255,255,255,.03) !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    border-radius: 8px !important;
    color: {C["text"]} !important;
    font-size: 12px !important;
    padding: 6px 10px !important;
}}
section[data-testid="stSidebar"] .stSlider label {{ display:none; }}
section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {{
    margin-top: 4px;
}}

/* ── Metric nativo ── */
[data-testid="metric-container"] {{
    background: {C["bg3"]} !important;
    border: 1px solid {C["border"]} !important;
    border-radius: 10px !important;
    padding: 12px 14px !important;
}}
[data-testid="metric-container"] label {{
    font-size: 9px !important;
    text-transform: uppercase !important;
    letter-spacing: .12em !important;
    color: {C["text3"]} !important;
    font-family: 'Inter', sans-serif !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    font-size: 18px !important;
    font-weight: 700 !important;
    color: {C["text"]} !important;
    font-family: 'Syne', sans-serif !important;
}}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {{
    font-size: 10px !important;
    color: {C["text2"]} !important;
}}

/* ── Border containers (card visual) ── */
[data-testid="stVerticalBlockBorderWrapper"] > div {{
    background: {C["bg3"]} !important;
    border: 1px solid {C["border"]} !important;
    border-radius: 14px !important;
}}

/* ── Dataframe ── */
[data-testid="stDataFrameContainer"] {{
    border: 1px solid {C["border"]} !important;
    border-radius: 10px !important;
    overflow: hidden;
}}

/* ── Progress ── */
.stProgress > div > div {{
    background: rgba(255,255,255,.05) !important;
    border-radius: 4px !important;
    height: 5px !important;
}}
.stProgress > div > div > div {{
    border-radius: 4px !important;
    height: 5px !important;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: {C["bg3"]};
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
    border: 1px solid {C["border"]};
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent;
    border-radius: 7px;
    color: {C["text2"]};
    font-size: 11px;
    font-weight: 500;
    padding: 6px 16px;
}}
.stTabs [aria-selected="true"] {{
    background: {C["bg4"]} !important;
    color: {C["text"]} !important;
}}

/* ── Divider ── */
hr {{ border-color: {C["border"]} !important; margin: 20px 0 !important; }}

/* ── Branding off ── */
#MainMenu, footer {{ visibility: hidden; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: {C["bg"]}; }}
::-webkit-scrollbar-thumb {{
    background: rgba(79,142,247,.2);
    border-radius: 4px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: rgba(79,142,247,.4);
}}
</style>
""", unsafe_allow_html=True)

# ── HELPERS HTML ──────────────────────────────────────────────
def kpi_card(icon, label, value, sub, accent):
    return f"""
<div style="background:linear-gradient(135deg,{C['bg3']} 0%,{C['bg4']} 100%);
border:1px solid {C['border']};border-top:2px solid {accent};
border-radius:12px;padding:16px 18px;min-height:90px;">
  <div style="font-size:9px;text-transform:uppercase;letter-spacing:.13em;
  color:{C['text3']};margin-bottom:9px;">{icon}&nbsp;&nbsp;{label}</div>
  <div style="font-size:22px;font-weight:700;color:{C['text']};line-height:1.1;
  font-family:'Syne',sans-serif;">{value}</div>
  <div style="font-size:10px;color:{C['text2']};margin-top:5px;">{sub}</div>
</div>"""

def section_header(title, accent):
    return f"""
<div style="display:flex;align-items:center;gap:12px;margin:28px 0 16px 0;">
  <div style="width:3px;height:20px;background:{accent};
  border-radius:2px;flex-shrink:0;"></div>
  <span style="font-size:10px;font-weight:600;text-transform:uppercase;
  letter-spacing:.14em;color:{C['text2']};">{title}</span>
  <div style="flex:1;height:1px;background:rgba(255,255,255,.04);"></div>
</div>"""

def chart_title(t):
    return f"""<p style="font-size:9px;font-weight:600;text-transform:uppercase;
letter-spacing:.13em;color:{C['text3']};margin:0 0 10px 0;padding:0;">{t}</p>"""

def progress_bar(label, val, pct, color):
    return f"""
<div style="margin-bottom:12px;">
  <div style="display:flex;justify-content:space-between;align-items:center;
  margin-bottom:5px;">
    <span style="font-size:11px;color:{C['text2']};">{label}</span>
    <span style="font-size:11px;font-weight:600;color:{C['text']};
    font-family:'Syne',sans-serif;">{val} <span style="color:{C['text3']};
    font-size:10px;font-weight:400;">· {pct:.0f}%</span></span>
  </div>
  <div style="height:4px;background:rgba(255,255,255,.05);border-radius:4px;">
    <div style="height:4px;width:{pct:.1f}%;background:{color};
    border-radius:4px;transition:width .4s ease;"></div>
  </div>
</div>"""

# ── DADOS ──────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_parquet("dados_rh.parquet")
    except Exception:
        df = pd.read_excel("Base_dados_rh.xlsx")
        def parse_sal(x):
            try:
                parts = str(x).rsplit('-', 1)
                sal = float(parts[0].replace(',', '.').replace(' ', ''))
                cargo = parts[1].strip() if len(parts) > 1 else ''
                return sal, cargo
            except Exception:
                return None, ''
        df[['Salario', 'Cargo']] = pd.DataFrame(
            df['Salario-Cargo'].apply(parse_sal).tolist(), index=df.index)
        from datetime import date
        hoje = date(2026, 3, 23)
        df['Idade'] = df['Data de Nascimento'].apply(
            lambda x: (hoje - x.date()).days // 365 if pd.notna(x) else None)
        def faixa(i):
            if i is None: return 'N/A'
            if i <= 29: return 'Até 29'
            if i <= 39: return '30-39'
            if i <= 49: return '40-49'
            return '50+'
        df['Faixa Etaria'] = df['Idade'].apply(faixa)
        df['Tempo de Casa'] = df['Data de Contratação'].apply(
            lambda x: 2026 - x.year if pd.notna(x) else None)
        df['Ano Contratação'] = df['Data de Contratação'].dt.year
        def nivel(c):
            c = str(c).lower()
            if 'diretor'    in c: return 'Diretoria'
            if 'gerente'    in c: return 'Gerência'
            if 'analista'   in c: return 'Analista'
            if 'assistente' in c: return 'Assistente'
            return 'Auxiliar'
        df['Nivel'] = df['Cargo'].apply(nivel)
    return df

df_full = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
<div style="padding:0 0 20px;">
  <div style="font-size:22px;font-weight:800;letter-spacing:-.02em;
  font-family:'Syne',sans-serif;color:{C['text']};">
    ◈ People<span style="color:{C['blue']};">Analytics</span>
  </div>
  <div style="display:flex;align-items:center;gap:7px;margin-top:8px;">
    <div style="width:6px;height:6px;background:{C['green']};border-radius:50%;
    box-shadow:0 0 7px {C['green']};"></div>
    <span style="font-size:9px;color:{C['text3']};letter-spacing:.1em;">
    164 COLABORADORES · ATIVOS</span>
  </div>
</div>
<div style="height:1px;background:rgba(255,255,255,.05);margin:0 -18px 22px;"></div>
""", unsafe_allow_html=True)

    st.markdown(f'<p style="font-size:9px;text-transform:uppercase;letter-spacing:.13em;color:{C["text3"]};margin-bottom:5px;">▸ Departamento</p>', unsafe_allow_html=True)
    deps = ["Todos"] + sorted(df_full["Departamento"].dropna().unique().tolist())
    dep_sel = st.selectbox("dep", deps, label_visibility="collapsed")

    st.markdown(f'<p style="font-size:9px;text-transform:uppercase;letter-spacing:.13em;color:{C["text3"]};margin:14px 0 5px;">▸ Performance</p>', unsafe_allow_html=True)
    perf_opts = ["Todos"] + sorted(df_full["Performance"].dropna().unique().tolist())
    perf_sel = st.selectbox("perf", perf_opts, label_visibility="collapsed")

    st.markdown(f'<p style="font-size:9px;text-transform:uppercase;letter-spacing:.13em;color:{C["text3"]};margin:14px 0 5px;">▸ Satisfação mínima</p>', unsafe_allow_html=True)
    sat_min = st.slider("sat", 1.0, 5.0, 1.0, 0.5, label_visibility="collapsed")

    st.markdown(f'<p style="font-size:9px;text-transform:uppercase;letter-spacing:.13em;color:{C["text3"]};margin:14px 0 5px;">▸ Recrutamento</p>', unsafe_allow_html=True)
    rec_opts = ["Todos"] + sorted(df_full["Recrutamento"].dropna().unique().tolist())
    rec_sel = st.selectbox("rec", rec_opts, label_visibility="collapsed")

    st.markdown(f"""
<div style="height:1px;background:rgba(255,255,255,.05);margin:24px -18px 18px;"></div>
<div style="font-size:9px;color:{C['text3']};line-height:1.8;">
  <span style="color:{C['text2']};">Fonte</span> · Base_dados_rh.xlsx<br>
  <span style="color:{C['text2']};">Referência</span> · Março 2026<br>
  <span style="color:{C['text2']};">Versão</span> · 2.0
</div>
""", unsafe_allow_html=True)

# ── FILTRO ─────────────────────────────────────────────────────
df = df_full.copy()
if dep_sel  != "Todos": df = df[df["Departamento"] == dep_sel]
if perf_sel != "Todos": df = df[df["Performance"]  == perf_sel]
if rec_sel  != "Todos": df = df[df["Recrutamento"]  == rec_sel]
df = df[df["Satisfação"] >= sat_min]
n = len(df)

# ── HEADER ─────────────────────────────────────────────────────
col_h, col_badge = st.columns([5, 1])
with col_h:
    st.markdown(f"""
<div style="padding:4px 0 20px;">
  <div style="font-size:30px;font-weight:800;font-family:'Syne',sans-serif;
  letter-spacing:-.03em;line-height:1.1;
  background:linear-gradient(90deg,{C['text']} 0%,{C['text2']} 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
    Mapa de Colaboradores
  </div>
  <div style="font-size:11px;color:{C['text3']};margin-top:7px;letter-spacing:.04em;">
    People Analytics &nbsp;·&nbsp; Força de trabalho &nbsp;·&nbsp; Referência Março 2026
  </div>
</div>
""", unsafe_allow_html=True)
with col_badge:
    st.markdown(f"""
<div style="text-align:right;padding-top:10px;">
  <div style="display:inline-flex;align-items:center;gap:7px;
  background:rgba(74,222,128,.07);border:1px solid rgba(74,222,128,.18);
  border-radius:20px;padding:6px 14px;">
    <div style="width:5px;height:5px;background:{C['green']};border-radius:50%;
    box-shadow:0 0 6px {C['green']};"></div>
    <span style="font-size:10px;color:{C['green']};font-weight:600;
    letter-spacing:.07em;">{n} ATIVOS</span>
  </div>
  <div style="font-size:9px;color:{C['text3']};margin-top:6px;
  letter-spacing:.08em;">MAR 2026</div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ───────────────────────────────────────────────────────
total_folha = df["Salario"].sum()
media_sal   = df["Salario"].mean()
mediana_sal = df["Salario"].median()
sat_media   = df["Satisfação"].mean()
alta_sat    = (df["Satisfação"] >= 4).sum() / n * 100 if n else 0
exc         = (df["Performance"] == "Excelente").sum()
reg         = (df["Performance"] == "Regular").sum()
ruim        = (df["Performance"] == "Ruim").sum()
score_perf  = (exc * 3 + reg * 2 + ruim * 1) / n if n else 0
tempo_medio = df["Tempo de Casa"].mean() if n else 0
vet_pct     = (df["Tempo de Casa"] >= 5).sum() / n * 100 if n else 0

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.markdown(kpi_card("◉", "Colaboradores",    str(n),                         "100% ativos",                    C["blue"]),   unsafe_allow_html=True)
k2.markdown(kpi_card("◈", "Total folha",      f"R${total_folha/1000:.0f}k",   f"Média R${media_sal:,.0f}",      C["teal"]),   unsafe_allow_html=True)
k3.markdown(kpi_card("◆", "Satisfação média", f"{sat_media:.2f}/5",           f"{alta_sat:.0f}% alta sat.",     C["green"]),  unsafe_allow_html=True)
k4.markdown(kpi_card("▲", "Score perf.",      f"{score_perf:.2f}/3",          f"{reg/n*100:.0f}% Regular" if n else "—", C["amber"]), unsafe_allow_html=True)
k5.markdown(kpi_card("◷", "Tempo de casa",    f"{tempo_medio:.1f}a",          f"{vet_pct:.1f}% veteranos",      C["purple"]), unsafe_allow_html=True)
k6.markdown(kpi_card("◐", "Mediana salarial", f"R${mediana_sal:,.0f}",        "R$1.550 – R$17.758",             C["pink"]),   unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SEÇÃO 1 — FORÇA DE TRABALHO
# ══════════════════════════════════════════════════════════════
st.markdown(section_header("Força de trabalho", C["blue"]), unsafe_allow_html=True)

col_a, col_b, col_c = st.columns([1.5, 0.85, 1.7])

with col_a:
    with st.container(border=True):
        st.markdown(chart_title("Distribuição por departamento"), unsafe_allow_html=True)
        dep_count = df["Departamento"].value_counts().reset_index()
        dep_count.columns = ["Departamento", "Count"]
        dep_count["Pct"] = (dep_count["Count"] / n * 100).round(1)
        fig_dep = px.bar(
            dep_count, x="Count", y="Departamento", orientation="h",
            text=dep_count.apply(lambda r: f"{r['Count']}  {r['Pct']:.0f}%", axis=1),
            color="Departamento",
            color_discrete_sequence=[C["blue"], C["teal"], C["pink"], C["amber"]],
            height=155,
        )
        fig_dep.update_layout(**PLOTLY_BASE, showlegend=False, bargap=0.35)
        fig_dep.update_traces(textposition="outside", textfont_size=10,
                              marker_line_width=0)
        fig_dep.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig_dep.update_yaxes(showgrid=False, tickfont_size=11)
        st.plotly_chart(fig_dep, use_container_width=True,
                        config={"displayModeBar": False})

        st.markdown(f'<div style="height:1px;background:{C["border"]};margin:4px 0 14px;"></div>', unsafe_allow_html=True)
        st.markdown(chart_title("Canal de recrutamento"), unsafe_allow_html=True)
        rec_count = df["Recrutamento"].value_counts().reset_index()
        rec_count.columns = ["Canal", "Count"]
        rec_count["Pct"] = (rec_count["Count"] / n * 100).round(1)
        fig_rec = px.bar(
            rec_count, x="Count", y="Canal", orientation="h",
            text=rec_count.apply(lambda r: f"{r['Count']}  {r['Pct']:.0f}%", axis=1),
            color="Canal",
            color_discrete_sequence=[C["pink"], "#e879a0", "#d4537e", "#b5336a"],
            height=155,
        )
        fig_rec.update_layout(**PLOTLY_BASE, showlegend=False, bargap=0.35)
        fig_rec.update_traces(textposition="outside", textfont_size=10,
                              marker_line_width=0)
        fig_rec.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig_rec.update_yaxes(showgrid=False, tickfont_size=11)
        st.plotly_chart(fig_rec, use_container_width=True,
                        config={"displayModeBar": False})

with col_b:
    with st.container(border=True):
        st.markdown(chart_title("Distribuição de gênero"), unsafe_allow_html=True)
        gen_count = df["Sexo"].value_counts()
        masc = gen_count.get("M", 0)
        fem  = gen_count.get("F", 0)
        fig_gen = go.Figure(go.Pie(
            labels=["Masculino", "Feminino"],
            values=[masc, fem],
            hole=.74,
            marker_colors=[C["blue"], C["pink"]],
            textinfo="none",
            hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
        ))
        fig_gen.update_layout(**PLOTLY_BASE, height=185,
            annotations=[dict(
                text=f"<b style='font-size:18px'>{n}</b><br><span style='font-size:10px'>total</span>",
                x=.5, y=.5, showarrow=False,
                font=dict(size=14, color=C["text"]))])
        st.plotly_chart(fig_gen, use_container_width=True,
                        config={"displayModeBar": False})

        for label, val, color in [("Masculino", masc, C["blue"]), ("Feminino", fem, C["pink"])]:
            pct = val / n * 100 if n else 0
            st.markdown(progress_bar(label, val, pct, color), unsafe_allow_html=True)

        st.markdown(f'<div style="height:1px;background:{C["border"]};margin:10px 0 14px;"></div>', unsafe_allow_html=True)
        st.markdown(chart_title("Faixa etária"), unsafe_allow_html=True)
        faixa_order = ["Até 29", "30-39", "40-49", "50+"]
        fat_count = df["Faixa Etaria"].value_counts().reindex(
            faixa_order, fill_value=0).reset_index()
        fat_count.columns = ["Faixa", "Count"]
        fig_fat = px.bar(
            fat_count, x="Count", y="Faixa", orientation="h",
            text=fat_count["Count"],
            color="Count",
            color_continuous_scale=[[0, "rgba(251,191,36,0.2)"], [1, C["amber"]]],
            height=155,
        )
        fig_fat.update_layout(**PLOTLY_BASE, showlegend=False,
                              coloraxis_showscale=False, bargap=0.35)
        fig_fat.update_traces(textposition="outside", textfont_size=10,
                              marker_line_width=0)
        fig_fat.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig_fat.update_yaxes(showgrid=False, tickfont_size=11)
        st.plotly_chart(fig_fat, use_container_width=True,
                        config={"displayModeBar": False})

with col_c:
    with st.container(border=True):
        st.markdown(chart_title("Contratações por ano"), unsafe_allow_html=True)
        anos = df["Ano Contratação"].value_counts().sort_index().reset_index()
        anos.columns = ["Ano", "Count"]
        cores_anos = [C["amber"] if a == 2020 else C["teal"] for a in anos["Ano"]]
        fig_anos = px.bar(anos, x="Ano", y="Count", text="Count",
            color="Ano",
            color_discrete_sequence=cores_anos,
            height=390,
        )
        fig_anos.update_layout(**PLOTLY_BASE, showlegend=False, bargap=0.3)
        fig_anos.update_traces(textposition="outside", textfont_size=10,
                               marker_color=cores_anos, marker_line_width=0,
                               textfont_color=C["text2"])
        fig_anos.update_xaxes(showgrid=False, type="category",
                              tickfont_size=11, zeroline=False)
        fig_anos.update_yaxes(showgrid=True,
                              gridcolor="rgba(255,255,255,.04)",
                              zeroline=False, tickfont_size=10)
        st.plotly_chart(fig_anos, use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown(f"""<p style="font-size:9px;color:{C['text3']};margin:4px 0 0;text-align:center;">
        <span style="color:{C['amber']};">▌</span> 2020 — pico de contratações
        &nbsp;·&nbsp;
        <span style="color:{C['teal']};">▌</span> demais anos</p>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SEÇÃO 2 — PERFORMANCE & SATISFAÇÃO
# ══════════════════════════════════════════════════════════════
st.markdown(section_header("Performance & satisfação", C["green"]), unsafe_allow_html=True)

col_p, col_s, col_seg = st.columns([1, 1.3, 1])

with col_p:
    with st.container(border=True):
        st.markdown(chart_title("Performance geral"), unsafe_allow_html=True)
        fig_perf = go.Figure(go.Pie(
            labels=["Excelente", "Regular", "Ruim"],
            values=[exc, reg, ruim],
            hole=.74,
            marker_colors=[C["green"], C["amber"], C["red"]],
            textinfo="none",
            hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
        ))
        fig_perf.update_layout(**PLOTLY_BASE, height=190,
            annotations=[dict(
                text=f"<b>{score_perf:.2f}</b><br><span style='font-size:9'>score</span>",
                x=.5, y=.5, showarrow=False,
                font=dict(size=16, color=C["amber"]))])
        st.plotly_chart(fig_perf, use_container_width=True,
                        config={"displayModeBar": False})

        st.markdown(f'<div style="height:1px;background:{C["border"]};margin:4px 0 12px;"></div>', unsafe_allow_html=True)
        for label, val, color in [
            ("Excelente", exc,  C["green"]),
            ("Regular",   reg,  C["amber"]),
            ("Ruim",      ruim, C["red"]),
        ]:
            pct = val / n * 100 if n else 0
            st.markdown(progress_bar(label, val, pct, color), unsafe_allow_html=True)

with col_s:
    with st.container(border=True):
        st.markdown(chart_title("Satisfação dos colaboradores (escala 1–5)"), unsafe_allow_html=True)
        sat_vals = df["Satisfação"].value_counts().sort_index().reset_index()
        sat_vals.columns = ["Nota", "Count"]
        def cor_sat(nota):
            if nota <= 2: return C["red"]
            if nota < 4:  return C["amber"]
            return C["green"]
        sat_vals["Cor"] = sat_vals["Nota"].apply(cor_sat)
        fig_sat = px.bar(sat_vals, x="Nota", y="Count", text="Count",
            color="Nota",
            color_discrete_sequence=sat_vals["Cor"].tolist(),
            height=270,
        )
        fig_sat.update_layout(**PLOTLY_BASE, showlegend=False, bargap=0.3)
        fig_sat.update_traces(
            textposition="outside", textfont_size=11,
            marker_color=sat_vals["Cor"].tolist(),
            marker_line_width=0,
            textfont_color=C["text2"],
        )
        fig_sat.update_xaxes(showgrid=False, type="category",
                             tickfont_size=12, zeroline=False)
        fig_sat.update_yaxes(showgrid=True,
                             gridcolor="rgba(255,255,255,.04)",
                             zeroline=False, tickfont_size=10)
        st.plotly_chart(fig_sat, use_container_width=True,
                        config={"displayModeBar": False})

        sa1, sa2 = st.columns(2)
        sa1.metric("Média geral", f"{sat_media:.2f}")
        sa2.metric("Alta satisfação", f"{alta_sat:.0f}%")

with col_seg:
    with st.container(border=True):
        st.markdown(chart_title("Segmentação de satisfação"), unsafe_allow_html=True)
        baixa = (df["Satisfação"] <= 2).sum()
        media = ((df["Satisfação"] > 2) & (df["Satisfação"] < 4)).sum()
        alta  = (df["Satisfação"] >= 4).sum()
        for label, val, color in [
            ("Alta  (≥ 4)",  alta,  C["green"]),
            ("Média (3–3,9)", media, C["amber"]),
            ("Baixa (≤ 2)",  baixa, C["red"]),
        ]:
            pct = val / n * 100 if n else 0
            st.markdown(progress_bar(label, val, pct, color), unsafe_allow_html=True)

        st.markdown(f'<div style="height:1px;background:{C["border"]};margin:12px 0 16px;"></div>', unsafe_allow_html=True)
        st.markdown(chart_title("Score de performance"), unsafe_allow_html=True)
        st.markdown(f"""
<div style="margin:8px 0 12px;">
  <span style="font-size:48px;font-weight:800;color:{C['amber']};
  font-family:'Syne',sans-serif;line-height:1;">{score_perf:.2f}</span>
  <span style="font-size:16px;color:{C['text3']};margin-left:4px;">/ 3,0</span>
</div>
<div style="height:5px;background:rgba(255,255,255,.05);border-radius:4px;">
  <div style="height:5px;width:{score_perf/3*100:.1f}%;
  background:linear-gradient(90deg,{C['amber']}aa,{C['amber']});
  border-radius:4px;"></div>
</div>
<p style="font-size:9px;color:{C['text3']};margin-top:7px;">
{score_perf/3*100:.0f}% do score máximo &nbsp;·&nbsp; Exc=3, Reg=2, Ruim=1</p>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SEÇÃO 3 — SALÁRIOS & NÍVEIS
# ══════════════════════════════════════════════════════════════
st.markdown(section_header("Salários & níveis hierárquicos", C["purple"]), unsafe_allow_html=True)

col_nv, col_sal, col_cargo = st.columns([1, 1.4, 1])

with col_nv:
    with st.container(border=True):
        st.markdown(chart_title("Nível hierárquico"), unsafe_allow_html=True)
        nivel_order = ["Diretoria", "Gerência", "Analista", "Assistente", "Auxiliar"]
        nv_count = df["Nivel"].value_counts().reindex(
            nivel_order, fill_value=0).reset_index()
        nv_count.columns = ["Nivel", "Count"]
        nv_count["Pct"] = (nv_count["Count"] / n * 100).round(0)
        fig_nv = px.bar(nv_count, x="Count", y="Nivel", orientation="h",
            text=nv_count.apply(lambda r: f"{r['Count']}  {r['Pct']:.0f}%", axis=1),
            color="Count",
            color_continuous_scale=[[0, "rgba(167,139,250,0.2)"], [1, C["purple"]]],
            height=290,
        )
        fig_nv.update_layout(**PLOTLY_BASE, showlegend=False,
                             coloraxis_showscale=False, bargap=0.3)
        fig_nv.update_traces(textposition="outside", textfont_size=10,
                             marker_line_width=0)
        fig_nv.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig_nv.update_yaxes(showgrid=False, tickfont_size=11,
                            categoryorder="array",
                            categoryarray=nivel_order[::-1])
        st.plotly_chart(fig_nv, use_container_width=True,
                        config={"displayModeBar": False})

with col_sal:
    with st.container(border=True):
        st.markdown(chart_title("Faixa salarial"), unsafe_allow_html=True)
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Mínimo",  f"R${df['Salario'].min():,.0f}")
        s2.metric("Máximo",  f"R${df['Salario'].max():,.0f}")
        s3.metric("Mediana", f"R${mediana_sal:,.0f}")
        s4.metric("Média",   f"R${media_sal:,.0f}")

        st.markdown("<br>", unsafe_allow_html=True)
        fig_hist = px.histogram(df, x="Salario", nbins=20,
            color_discrete_sequence=[C["teal"]], height=185,
            labels={"Salario": "Salário (R$)", "count": "Colaboradores"},
        )
        fig_hist.update_layout(**PLOTLY_BASE, bargap=0.08)
        fig_hist.update_traces(marker_line_width=0,
                               marker_color=C["teal"],
                               opacity=0.85)
        fig_hist.update_xaxes(showgrid=False, zeroline=False,
                              tickfont_size=10,
                              tickprefix="R$", tickformat=",.0f")
        fig_hist.update_yaxes(showgrid=True,
                              gridcolor="rgba(255,255,255,.04)",
                              zeroline=False, tickfont_size=10)
        st.plotly_chart(fig_hist, use_container_width=True,
                        config={"displayModeBar": False})
        st.metric("Total folha mensal", f"R${total_folha:,.0f}")

with col_cargo:
    with st.container(border=True):
        st.markdown(chart_title("Top 10 cargos"), unsafe_allow_html=True)
        top_cargos = df["Cargo"].value_counts().head(10).reset_index()
        top_cargos.columns = ["Cargo", "Count"]
        fig_cargo = px.bar(top_cargos, x="Count", y="Cargo", orientation="h",
            text="Count",
            color="Count",
            color_continuous_scale=[[0, "rgba(251,191,36,0.2)"], [1, C["amber"]]],
            height=340,
        )
        fig_cargo.update_layout(**PLOTLY_BASE, showlegend=False,
                                coloraxis_showscale=False, bargap=0.28)
        fig_cargo.update_traces(textposition="outside", textfont_size=10,
                                marker_line_width=0)
        fig_cargo.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig_cargo.update_yaxes(showgrid=False, tickfont_size=10,
                               autorange="reversed")
        st.plotly_chart(fig_cargo, use_container_width=True,
                        config={"displayModeBar": False})

# ══════════════════════════════════════════════════════════════
# SEÇÃO 4 — RETENÇÃO & TABELA
# ══════════════════════════════════════════════════════════════
st.markdown(section_header("Retenção & amostra de colaboradores", C["teal"]), unsafe_allow_html=True)

col_ret, col_tab = st.columns([1, 1.2])

with col_ret:
    with st.container(border=True):
        st.markdown(chart_title("Retenção e tempo de casa"), unsafe_allow_html=True)
        vet_n = (df["Tempo de Casa"] >= 5).sum()
        nov_n = (df["Tempo de Casa"] < 2).sum()
        r1, r2, r3 = st.columns(3)
        r1.metric("Tempo médio",   f"{tempo_medio:.1f}a")
        r2.metric("Veteranos ≥5a", f"{vet_pct:.1f}%", f"{vet_n} colab.")
        r3.metric("Novatos <2a",   f"{nov_n/n*100:.0f}%", f"{nov_n} colab.")

        st.markdown("<br>", unsafe_allow_html=True)
        anos_hist = df_full["Ano Contratação"].value_counts().sort_index().reset_index()
        anos_hist.columns = ["Ano", "Count"]
        cores_tl = [C["amber"] if a == 2020 else C["teal"] for a in anos_hist["Ano"]]
        fig_tl = px.bar(anos_hist, x="Count", y="Ano", orientation="h",
            text="Count", color="Ano",
            color_discrete_sequence=cores_tl,
            height=310,
        )
        fig_tl.update_layout(**PLOTLY_BASE, showlegend=False, bargap=0.3)
        fig_tl.update_traces(textposition="outside", textfont_size=10,
                             marker_color=cores_tl, marker_line_width=0,
                             textfont_color=C["text2"])
        fig_tl.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig_tl.update_yaxes(showgrid=False, type="category",
                            autorange="reversed", tickfont_size=11)
        st.plotly_chart(fig_tl, use_container_width=True,
                        config={"displayModeBar": False})

with col_tab:
    with st.container(border=True):
        st.markdown(chart_title("Amostra de colaboradores"), unsafe_allow_html=True)
        cols_show = ["Colaborador", "ID", "Departamento", "Cargo",
                     "Recrutamento", "Satisfação", "Performance", "Nivel",
                     "Tempo de Casa"]
        df_show = df[cols_show].copy()
        df_show["Tempo de Casa"] = df_show["Tempo de Casa"].apply(
            lambda x: f"{x:.0f}a" if pd.notna(x) else "—")
        st.dataframe(
            df_show.head(20),
            use_container_width=True,
            height=440,
            hide_index=True,
            column_config={
                "Satisfação":    st.column_config.NumberColumn(format="%.1f ★"),
                "Performance":   st.column_config.TextColumn(),
                "Tempo de Casa": st.column_config.TextColumn("Tempo"),
            }
        )

# ── FOOTER ────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
margin-top:32px;padding:18px 24px;
background:{C['bg3']};border:1px solid {C['border']};
border-radius:12px;">
  <div style="font-size:9px;color:{C['text3']};letter-spacing:.08em;">
    ◈ PEOPLE ANALYTICS
  </div>
  <div style="font-size:9px;color:{C['text3']};letter-spacing:.06em;">
    Base_dados_rh.xlsx &nbsp;·&nbsp; {n} colaboradores &nbsp;·&nbsp; Março 2026
  </div>
  <div style="font-size:9px;color:{C['text3']};letter-spacing:.06em;">
    Streamlit &nbsp;+&nbsp; Plotly &nbsp;·&nbsp; v2.0
  </div>
</div>
""", unsafe_allow_html=True)

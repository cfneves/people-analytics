import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── CONFIGURAÇÃO DA PÁGINA ─────────────────────────────────────
st.set_page_config(
    page_title="People Analytics — Mapa de Colaboradores",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── TEMA / CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

/* Fundo geral */
.stApp { background-color: #07090f; }
section[data-testid="stSidebar"] { background-color: #0e1219; border-right: 1px solid rgba(255,255,255,.07); }

/* Métricas */
[data-testid="metric-container"] {
    background: #0e1219;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 12px;
    padding: 14px 18px;
}
[data-testid="metric-container"] label { font-size: 10px !important; text-transform: uppercase; letter-spacing: .09em; color: #7a8599 !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 700 !important; color: #e8edf5 !important; }
[data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size: 11px !important; }

/* Títulos */
h1 { font-size: 22px !important; font-weight: 700 !important; color: #e8edf5 !important; }
h2 { font-size: 13px !important; font-weight: 600 !important; color: #7a8599 !important; text-transform: uppercase; letter-spacing: .1em; }
h3 { font-size: 12px !important; font-weight: 600 !important; color: #7a8599 !important; }

/* Sidebar labels */
.sidebar-label { font-size: 10px; text-transform: uppercase; letter-spacing: .09em; color: #3d4a60; margin-bottom: 4px; }

/* Divisor */
hr { border-color: rgba(255,255,255,.07) !important; margin: 8px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── CORES ──────────────────────────────────────────────────────
COLORS = {
    "blue":   "#4f8ef7",
    "teal":   "#2dd4bf",
    "pink":   "#f472b6",
    "amber":  "#fbbf24",
    "green":  "#4ade80",
    "red":    "#f87171",
    "purple": "#c084fc",
    "text":   "#e8edf5",
    "text2":  "#7a8599",
    "bg3":    "#141a26",
    "bg4":    "#1a2236",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color=COLORS["text2"],
    font_family="Syne",
    margin=dict(l=0, r=0, t=10, b=0),
    colorway=[COLORS["blue"], COLORS["teal"], COLORS["pink"], COLORS["amber"], COLORS["green"]],
)

# ── DADOS ──────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_parquet("dados_rh.parquet")
    except:
        import re
        df = pd.read_excel("Base_dados_rh.xlsx")
        def parse_sal(x):
            try:
                parts = str(x).rsplit('-', 1)
                sal = float(parts[0].replace(',', '.').replace(' ', ''))
                cargo = parts[1].strip() if len(parts) > 1 else ''
                return sal, cargo
            except:
                return None, ''
        df[['Salario', 'Cargo']] = pd.DataFrame(df['Salario-Cargo'].apply(parse_sal).tolist(), index=df.index)
        from datetime import date
        hoje = date(2026, 3, 23)
        df['Idade'] = df['Data de Nascimento'].apply(lambda x: (hoje - x.date()).days // 365 if pd.notna(x) else None)
        def faixa(i):
            if i is None: return 'N/A'
            if i <= 29: return 'Até 29'
            if i <= 39: return '30-39'
            if i <= 49: return '40-49'
            return '50+'
        df['Faixa Etaria'] = df['Idade'].apply(faixa)
        df['Tempo de Casa'] = df['Data de Contratação'].apply(lambda x: 2026 - x.year if pd.notna(x) else None)
        df['Ano Contratação'] = df['Data de Contratação'].dt.year
        def nivel(c):
            c = str(c).lower()
            if 'diretor' in c: return 'Diretoria'
            if 'gerente' in c: return 'Gerência'
            if 'analista' in c: return 'Analista'
            if 'assistente' in c: return 'Assistente'
            return 'Auxiliar'
        df['Nivel'] = df['Cargo'].apply(nivel)
    return df

df_full = load_data()

# ── SIDEBAR ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 People Analytics")
    st.markdown("**Mapa de Colaboradores**")
    st.markdown("---")

    st.markdown('<p class="sidebar-label">Departamento</p>', unsafe_allow_html=True)
    deps = ["Todos"] + sorted(df_full["Departamento"].dropna().unique().tolist())
    dep_sel = st.selectbox("", deps, label_visibility="collapsed")

    st.markdown('<p class="sidebar-label">Performance</p>', unsafe_allow_html=True)
    perf_opts = ["Todos"] + sorted(df_full["Performance"].dropna().unique().tolist())
    perf_sel = st.selectbox(" ", perf_opts, label_visibility="collapsed")

    st.markdown('<p class="sidebar-label">Satisfação mínima</p>', unsafe_allow_html=True)
    sat_min = st.slider("", 1.0, 5.0, 1.0, 0.5, label_visibility="collapsed")

    st.markdown('<p class="sidebar-label">Recrutamento</p>', unsafe_allow_html=True)
    rec_opts = ["Todos"] + sorted(df_full["Recrutamento"].dropna().unique().tolist())
    rec_sel = st.selectbox("  ", rec_opts, label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"<p style='font-size:10px;color:#3d4a60;'>Fonte: Base_dados_rh.xlsx<br>Referência: Mar 2026</p>", unsafe_allow_html=True)

# ── FILTRO ─────────────────────────────────────────────────────
df = df_full.copy()
if dep_sel  != "Todos": df = df[df["Departamento"] == dep_sel]
if perf_sel != "Todos": df = df[df["Performance"] == perf_sel]
if rec_sel  != "Todos": df = df[df["Recrutamento"] == rec_sel]
df = df[df["Satisfação"] >= sat_min]
n = len(df)

# ── HEADER ─────────────────────────────────────────────────────
c_title, c_meta = st.columns([4, 1])
with c_title:
    st.markdown("# People Analytics — Mapa de Colaboradores")
with c_meta:
    st.markdown(f"<div style='text-align:right;padding-top:8px;font-size:11px;color:#3d4a60;font-family:monospace;'>Mar 2026 · {n} colab.</div>", unsafe_allow_html=True)

st.markdown("---")

# ── KPIs ───────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)

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

k1.metric("Total colaboradores", n, "100% Ativos")
k2.metric("Total folha", f"R${total_folha/1000:.0f}k", f"Média R${media_sal:,.0f}")
k3.metric("Satisfação média", f"{sat_media:.2f}/5", f"{alta_sat:.0f}% alta sat.")
k4.metric("Score performance", f"{score_perf:.2f}/3", f"{reg/n*100:.0f}% Regular" if n else "—")
k5.metric("Tempo médio de casa", f"{tempo_medio:.1f} anos", f"{vet_pct:.1f}% veteranos")
k6.metric("Mediana salarial", f"R${mediana_sal:,.0f}", f"R$1.550 – R$17.758")

st.markdown("---")

# ══════════════════════════════════════════════════════════════
# SEÇÃO 1 — FORÇA DE TRABALHO
# ══════════════════════════════════════════════════════════════
st.markdown("## Força de trabalho")

col_dep, col_gen, col_fat, col_anos = st.columns([2.5, 1, 1, 1.6])

with col_dep:
    # Departamentos
    dep_count = df["Departamento"].value_counts().reset_index()
    dep_count.columns = ["Departamento", "Count"]
    dep_count["Pct"] = (dep_count["Count"] / n * 100).round(1)
    fig_dep = px.bar(
        dep_count, x="Count", y="Departamento", orientation="h",
        text=dep_count.apply(lambda r: f"{r['Count']} · {r['Pct']:.0f}%", axis=1),
        color="Departamento",
        color_discrete_sequence=[COLORS["blue"], COLORS["teal"], COLORS["pink"], COLORS["amber"]],
        height=160,
    )
    fig_dep.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    fig_dep.update_traces(textposition="outside", textfont_size=10)
    fig_dep.update_xaxes(showgrid=False, showticklabels=False)
    fig_dep.update_yaxes(showgrid=False)
    st.markdown("### Departamentos")
    st.plotly_chart(fig_dep, use_container_width=True, config={"displayModeBar": False})

    # Recrutamento
    rec_count = df["Recrutamento"].value_counts().reset_index()
    rec_count.columns = ["Canal", "Count"]
    rec_count["Pct"] = (rec_count["Count"] / n * 100).round(1)
    fig_rec = px.bar(
        rec_count, x="Count", y="Canal", orientation="h",
        text=rec_count.apply(lambda r: f"{r['Count']} · {r['Pct']:.0f}%", axis=1),
        color="Canal",
        color_discrete_sequence=[COLORS["pink"], "#e879a0", "#d4537e", "#b5336a"],
        height=160,
    )
    fig_rec.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    fig_rec.update_traces(textposition="outside", textfont_size=10)
    fig_rec.update_xaxes(showgrid=False, showticklabels=False)
    fig_rec.update_yaxes(showgrid=False)
    st.markdown("### Canal de recrutamento")
    st.plotly_chart(fig_rec, use_container_width=True, config={"displayModeBar": False})

with col_gen:
    gen_count = df["Sexo"].value_counts()
    masc = gen_count.get("M", 0)
    fem  = gen_count.get("F", 0)
    fig_gen = go.Figure(go.Pie(
        labels=["Masculino", "Feminino"],
        values=[masc, fem],
        hole=.72,
        marker_colors=[COLORS["blue"], COLORS["pink"]],
        textinfo="none",
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
    ))
    fig_gen.update_layout(**PLOTLY_LAYOUT, height=180,
        annotations=[dict(text=f"<b>{n}</b><br><span style='font-size:9'>total</span>",
                          x=.5, y=.5, showarrow=False, font_size=14, font_color=COLORS["text"])])
    st.markdown("### Gênero")
    st.plotly_chart(fig_gen, use_container_width=True, config={"displayModeBar": False})
    st.markdown(f"<p style='font-size:11px;color:{COLORS['text2']};'>Masc. <b style='color:{COLORS['text']}'>{masc}</b> · {masc/n*100:.0f}%<br>Fem. <b style='color:{COLORS['text']}'>{fem}</b> · {fem/n*100:.0f}%</p>", unsafe_allow_html=True)

with col_fat:
    faixa_order = ["Até 29", "30-39", "40-49", "50+"]
    fat_count = df["Faixa Etaria"].value_counts().reindex(faixa_order, fill_value=0).reset_index()
    fat_count.columns = ["Faixa", "Count"]
    fig_fat = px.bar(
        fat_count, x="Count", y="Faixa", orientation="h",
        text=fat_count["Count"],
        color="Count",
        color_continuous_scale=[[0, COLORS["amber"]+"44"], [1, COLORS["amber"]]],
        height=180,
    )
    fig_fat.update_layout(**PLOTLY_LAYOUT, showlegend=False, coloraxis_showscale=False)
    fig_fat.update_traces(textposition="outside", textfont_size=10)
    fig_fat.update_xaxes(showgrid=False, showticklabels=False)
    fig_fat.update_yaxes(showgrid=False)
    st.markdown("### Faixa etária")
    st.plotly_chart(fig_fat, use_container_width=True, config={"displayModeBar": False})

with col_anos:
    anos = df["Ano Contratação"].value_counts().sort_index().reset_index()
    anos.columns = ["Ano", "Count"]
    cores_anos = [COLORS["amber"] if a == 2020 else COLORS["teal"] for a in anos["Ano"]]
    fig_anos = px.bar(anos, x="Ano", y="Count", text="Count",
        color="Ano",
        color_discrete_sequence=cores_anos,
        height=320,
    )
    fig_anos.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    fig_anos.update_traces(textposition="outside", textfont_size=9, marker_color=cores_anos)
    fig_anos.update_xaxes(showgrid=False, type="category")
    fig_anos.update_yaxes(showgrid=True, gridcolor=COLORS["bg4"])
    st.markdown("### Contratações por ano")
    st.plotly_chart(fig_anos, use_container_width=True, config={"displayModeBar": False})

st.markdown("---")

# ══════════════════════════════════════════════════════════════
# SEÇÃO 2 — PERFORMANCE & SATISFAÇÃO
# ══════════════════════════════════════════════════════════════
st.markdown("## Performance & satisfação")

col_perf, col_sat, col_seg = st.columns([1.4, 1.1, 1.5])

with col_perf:
    fig_perf = go.Figure(go.Pie(
        labels=["Excelente", "Regular", "Ruim"],
        values=[exc, reg, ruim],
        hole=.72,
        marker_colors=[COLORS["green"], COLORS["amber"], COLORS["red"]],
        textinfo="none",
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
    ))
    fig_perf.update_layout(**PLOTLY_LAYOUT, height=200,
        annotations=[dict(text=f"<b>{score_perf:.2f}</b><br><span style='font-size:9'>score</span>",
                          x=.5, y=.5, showarrow=False, font_size=16, font_color=COLORS["amber"])])
    st.markdown("### Performance")
    st.plotly_chart(fig_perf, use_container_width=True, config={"displayModeBar": False})
    c1, c2, c3 = st.columns(3)
    c1.metric("Excelente", exc, f"{exc/n*100:.0f}%")
    c2.metric("Regular",   reg, f"{reg/n*100:.0f}%")
    c3.metric("Ruim",      ruim, f"{ruim/n*100:.0f}%")

with col_sat:
    sat_vals = df["Satisfação"].value_counts().sort_index().reset_index()
    sat_vals.columns = ["Nota", "Count"]
    def cor_sat(nota):
        if nota <= 2: return COLORS["red"]
        if nota < 4:  return COLORS["amber"]
        return COLORS["green"]
    sat_vals["Cor"] = sat_vals["Nota"].apply(cor_sat)
    fig_sat = px.bar(sat_vals, x="Nota", y="Count", text="Count",
        color="Nota",
        color_discrete_sequence=sat_vals["Cor"].tolist(),
        height=280,
    )
    fig_sat.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    fig_sat.update_traces(
        textposition="outside", textfont_size=10,
        marker_color=sat_vals["Cor"].tolist(),
    )
    fig_sat.update_xaxes(showgrid=False, type="category")
    fig_sat.update_yaxes(showgrid=True, gridcolor=COLORS["bg4"])
    st.markdown("### Satisfação (escala 1–5)")
    st.plotly_chart(fig_sat, use_container_width=True, config={"displayModeBar": False})

with col_seg:
    st.markdown("### Segmentação de satisfação")
    baixa = (df["Satisfação"] <= 2).sum()
    media = ((df["Satisfação"] > 2) & (df["Satisfação"] < 4)).sum()
    alta  = (df["Satisfação"] >= 4).sum()
    for label, val, cor in [("Alta (≥ 4)", alta, COLORS["green"]), ("Média (3–3,9)", media, COLORS["amber"]), ("Baixa (≤ 2)", baixa, COLORS["red"])]:
        pct = val / n * 100 if n else 0
        st.markdown(f"<div style='display:flex;justify-content:space-between;margin-bottom:3px;font-size:11px;color:{COLORS['text2']}'><span>{label}</span><span style='color:{COLORS['text']};font-family:monospace'>{val} · {pct:.0f}%</span></div>", unsafe_allow_html=True)
        st.progress(pct / 100)
    st.markdown("<br>", unsafe_allow_html=True)
    sa1, sa2 = st.columns(2)
    sa1.metric("Média geral", f"{sat_media:.2f}")
    sa2.metric("Alta satisfação", f"{alta_sat:.0f}%")
    st.markdown("---")
    st.markdown("### Score de performance")
    st.markdown(f"<div style='font-size:44px;font-weight:700;color:{COLORS['amber']};line-height:1'>{score_perf:.2f}<span style='font-size:16px;color:{COLORS['text2']}'> / 3,0</span></div>", unsafe_allow_html=True)
    pct_score = score_perf / 3
    st.progress(pct_score)
    st.markdown(f"<p style='font-size:10px;color:{COLORS['text2']};margin-top:4px'>{pct_score*100:.0f}% do score máximo · Exc=3, Reg=2, Ruim=1</p>", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════
# SEÇÃO 3 — SALÁRIOS & NÍVEIS
# ══════════════════════════════════════════════════════════════
st.markdown("## Salários & níveis hierárquicos")

col_nivel, col_sal, col_cargos = st.columns([1, 1.4, 1])

with col_nivel:
    nivel_order = ["Diretoria", "Gerência", "Analista", "Assistente", "Auxiliar"]
    nv_count = df["Nivel"].value_counts().reindex(nivel_order, fill_value=0).reset_index()
    nv_count.columns = ["Nivel", "Count"]
    nv_count["Pct"] = (nv_count["Count"] / n * 100).round(0)
    fig_nv = px.bar(nv_count, x="Count", y="Nivel", orientation="h",
        text=nv_count.apply(lambda r: f"{r['Count']} · {r['Pct']:.0f}%", axis=1),
        color="Count",
        color_continuous_scale=[[0, COLORS["purple"]+"44"], [1, COLORS["purple"]]],
        height=260,
    )
    fig_nv.update_layout(**PLOTLY_LAYOUT, showlegend=False, coloraxis_showscale=False)
    fig_nv.update_traces(textposition="outside", textfont_size=10)
    fig_nv.update_xaxes(showgrid=False, showticklabels=False)
    fig_nv.update_yaxes(showgrid=False, categoryorder="array", categoryarray=nivel_order[::-1])
    st.markdown("### Nível hierárquico")
    st.plotly_chart(fig_nv, use_container_width=True, config={"displayModeBar": False})

with col_sal:
    st.markdown("### Faixa salarial")
    s1, s2 = st.columns(2)
    s1.metric("Mínimo",  f"R${df['Salario'].min():,.2f}")
    s2.metric("Máximo",  f"R${df['Salario'].max():,.2f}")
    s3, s4 = st.columns(2)
    s3.metric("Mediana", f"R${mediana_sal:,.2f}")
    s4.metric("Média",   f"R${media_sal:,.2f}")
    st.markdown("<br>", unsafe_allow_html=True)
    fig_hist = px.histogram(df, x="Salario", nbins=20,
        color_discrete_sequence=[COLORS["teal"]], height=180,
        labels={"Salario": "Salário (R$)", "count": "Colaboradores"},
    )
    fig_hist.update_layout(**PLOTLY_LAYOUT)
    fig_hist.update_xaxes(showgrid=False)
    fig_hist.update_yaxes(showgrid=True, gridcolor=COLORS["bg4"])
    st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})
    st.metric("Total folha mensal", f"R${total_folha:,.2f}")

with col_cargos:
    top_cargos = df["Cargo"].value_counts().head(10).reset_index()
    top_cargos.columns = ["Cargo", "Count"]
    fig_cargo = px.bar(top_cargos, x="Count", y="Cargo", orientation="h",
        text="Count",
        color="Count",
        color_continuous_scale=[[0, COLORS["amber"]+"44"], [1, COLORS["amber"]]],
        height=320,
    )
    fig_cargo.update_layout(**PLOTLY_LAYOUT, showlegend=False, coloraxis_showscale=False)
    fig_cargo.update_traces(textposition="outside", textfont_size=10)
    fig_cargo.update_xaxes(showgrid=False, showticklabels=False)
    fig_cargo.update_yaxes(showgrid=False, autorange="reversed")
    st.markdown("### Top 10 cargos")
    st.plotly_chart(fig_cargo, use_container_width=True, config={"displayModeBar": False})

st.markdown("---")

# ══════════════════════════════════════════════════════════════
# SEÇÃO 4 — RETENÇÃO & TABELA
# ══════════════════════════════════════════════════════════════
st.markdown("## Retenção & amostra de colaboradores")

col_ret, col_tab = st.columns([1, 1])

with col_ret:
    st.markdown("### Retenção e tempo de casa")
    r1, r2, r3 = st.columns(3)
    vet_n  = (df["Tempo de Casa"] >= 5).sum()
    nov_n  = (df["Tempo de Casa"] < 2).sum()
    r1.metric("Tempo médio", f"{tempo_medio:.1f}a")
    r2.metric("Veteranos ≥5a", f"{vet_pct:.1f}%", f"{vet_n} colab.")
    r3.metric("Novatos <2a", f"{nov_n/n*100:.0f}%", f"{nov_n} colab.")
    st.markdown("<br>", unsafe_allow_html=True)

    anos_hist = df_full["Ano Contratação"].value_counts().sort_index().reset_index()
    anos_hist.columns = ["Ano", "Count"]
    cores_tl = [COLORS["amber"] if a == 2020 else COLORS["teal"] for a in anos_hist["Ano"]]
    fig_tl = px.bar(anos_hist, x="Count", y="Ano", orientation="h",
        text="Count", color="Ano",
        color_discrete_sequence=cores_tl,
        height=320,
    )
    fig_tl.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    fig_tl.update_traces(textposition="outside", textfont_size=10, marker_color=cores_tl)
    fig_tl.update_xaxes(showgrid=False, showticklabels=False)
    fig_tl.update_yaxes(showgrid=False, type="category", autorange="reversed")
    st.plotly_chart(fig_tl, use_container_width=True, config={"displayModeBar": False})

with col_tab:
    st.markdown("### Amostra de colaboradores")
    cols_show = ["Colaborador", "ID", "Departamento", "Cargo", "Recrutamento", "Satisfação", "Performance", "Nivel", "Tempo de Casa"]
    df_show = df[cols_show].copy()
    df_show["Tempo de Casa"] = df_show["Tempo de Casa"].apply(lambda x: f"{x:.0f}a" if pd.notna(x) else "—")

    def color_perf(val):
        if val == "Excelente": return "color: #4ade80"
        if val == "Ruim":      return "color: #f87171"
        return "color: #fbbf24"

    st.dataframe(
        df_show.head(20),
        use_container_width=True,
        height=390,
        hide_index=True,
        column_config={
            "Satisfação": st.column_config.NumberColumn(format="%.1f ★"),
            "Performance": st.column_config.TextColumn(),
            "Tempo de Casa": st.column_config.TextColumn("Tempo"),
        }
    )

st.markdown("---")

# FOOTER
st.markdown(
    f"<p style='font-size:10px;color:#3d4a60;text-align:center;'>People Analytics Dashboard · Base_dados_rh.xlsx · {n} colaboradores · Março 2026</p>",
    unsafe_allow_html=True
)

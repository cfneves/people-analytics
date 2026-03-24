# Changelog

Todas as mudanças relevantes do projeto estão documentadas aqui.

---

## [2.1] — 2026-03-23

### Corrigido
- `parse_sal` não tratava números com separador de milhar brasileiro (`6.120,32`)
  — afetava 3 registros (AC148, AC149, AC122) resultando em `Salario = null`
- Data de referência hardcoded `date(2026, 3, 23)` substituída por `date.today()`
  — cálculos de idade e tempo de casa agora sempre corretos

### Adicionado
- Pasta `/docs` com documentação técnica completa:
  - `dicionario_dados.md` — schema, tipos, categorias e qualidade
  - `diagnostico_tecnico.md` — bugs, outliers, riscos e análise de código
  - `plano_acao.md` — quick wins, melhorias estruturais e evolução estratégica
  - `guia_contribuidores.md` — setup, estrutura e como contribuir
- `CHANGELOG.md` — histórico de versões
- Descrição, website e topics configurados no GitHub

### Melhorado
- README reescrito com linguagem direta e insights concretos dos dados

---

## [2.0] — 2026-03-23

### Adicionado
- Design system com paleta de cores unificada (dicionário `C`)
- KPI cards em HTML puro com `border-top` colorido por categoria
- `st.container(border=True)` estilizado como cards para cada grupo de gráficos
- Section headers com pill vertical colorido por seção
- Sidebar com branding ◈ PeopleAnalytics e pulse dot de status
- Progress bars customizadas em HTML com cores semânticas
- Footer em card com 3 colunas

### Melhorado
- Layout seção 1 reestruturado de `[2.5, 1, 1, 1.6]` para `[1.5, 0.85, 1.7]`
- Fonte Inter (corpo) + Syne (display/números)
- Gráficos Plotly: `bargap` consistente, `marker_line_width=0`, hover estilizado
- Scrollbar, dataframe, selectbox e slider estilizados no CSS

---

## [1.0] — 2026-03-22

### Adicionado
- Dashboard inicial com Streamlit e Plotly
- 4 seções: Força de trabalho, Performance & Satisfação, Salários & Níveis, Retenção
- 6 KPIs dinâmicos
- Filtros por Departamento, Performance, Satisfação e Recrutamento
- Tema dark com fonte Syne
- Cache com Parquet + fallback Excel
- Deploy no Streamlit Community Cloud

---

*Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)*

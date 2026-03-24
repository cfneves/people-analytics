# People Analytics — Mapa de Colaboradores

Dashboard interativo de People Analytics desenvolvido com **Streamlit** e **Plotly**, oferecendo visão 360° da força de trabalho com filtros dinâmicos e KPIs em tempo real.

---

## Demonstração

> Deploy disponível no **Streamlit Community Cloud**
> Acesse: [people-analytics no Streamlit Cloud](https://streamlit.io/cloud)

---

## Visão Geral

| Item | Detalhe |
|---|---|
| Colaboradores | 164 ativos |
| Referência | Março 2026 |
| Fonte de dados | `Base_dados_rh.xlsx` / `dados_rh.parquet` |
| Stack principal | Python · Streamlit · Plotly · Pandas |
| Deploy | Streamlit Community Cloud |

---

## Funcionalidades

### Filtros interativos (sidebar)
- **Departamento** — Produção, Financeiro, Comercial, Administrativo
- **Performance** — Excelente, Regular, Ruim
- **Satisfação mínima** — slider de 1,0 a 5,0 (passo 0,5)
- **Canal de recrutamento** — Anúncios/Sites, LinkedIn, Indicação, Banco de Dados Interno

Todos os KPIs e gráficos respondem aos filtros em tempo real.

### KPIs dinâmicos
| KPI | Fórmula |
|---|---|
| Total colaboradores | Contagem após filtros |
| Total folha | `Σ Salario` |
| Satisfação média | `mean(Satisfação)` |
| Score performance | `(Exc×3 + Reg×2 + Ruim×1) / n` — escala 1,0–3,0 |
| Tempo médio de casa | `mean(Tempo de Casa)` em anos |
| Mediana salarial | `median(Salario)` |

### Seções do dashboard

**1. Força de trabalho**
- Distribuição por departamento (barras horizontais)
- Canal de recrutamento (barras horizontais)
- Gênero (donut chart)
- Faixa etária — Até 29 / 30-39 / 40-49 / 50+ (barras)
- Contratações por ano 2012–2022 (barras verticais)

**2. Performance & Satisfação**
- Distribuição de performance (donut chart com score central)
- Histograma de satisfação 1–5 com gradiente semântico (verde/âmbar/vermelho)
- Segmentação Alta/Média/Baixa satisfação com barras de progresso

**3. Salários & Níveis hierárquicos**
- Pirâmide de nível hierárquico — Diretoria → Auxiliar
- Faixa salarial: mín/máx/mediana/média + histograma de distribuição
- Top 10 cargos mais frequentes

**4. Retenção & Tabela**
- Timeline de contratações por ano (destaque 2020)
- Métricas de retenção: veteranos ≥5a, novatos <2a
- Amostra dos colaboradores com formatação condicional de performance

---

## Dataset

### Schema — `Base_dados_rh.xlsx`

| Coluna | Tipo | Descrição |
|---|---|---|
| `Colaborador` | string | Nome completo |
| `ID` | string | Código único (ex: AC75) |
| `Salario-Cargo` | string | Campo composto `valor-cargo` (parseado em `load_data`) |
| `Data de Nascimento` | datetime | Para cálculo de `Idade` e `Faixa Etaria` |
| `Sexo` | string | M / F |
| `Data de Contratação` | datetime | Para cálculo de `Tempo de Casa` e `Ano Contratação` |
| `Status` | string | Todos ativos nesta base |
| `Departamento` | string | Produção · Financeiro · Comercial · Administrativo |
| `Recrutamento` | string | Canal de origem do colaborador |
| `Performance` | string | Excelente · Regular · Ruim |
| `Satisfação` | float | Escala 1,0–5,0 |

### Colunas derivadas (engenharia de features em `load_data`)

| Coluna derivada | Origem | Lógica |
|---|---|---|
| `Salario` | `Salario-Cargo` | `rsplit('-', 1)[0]` convertido para float |
| `Cargo` | `Salario-Cargo` | `rsplit('-', 1)[1]` |
| `Idade` | `Data de Nascimento` | `(referência - nascimento).days // 365` |
| `Faixa Etaria` | `Idade` | Bucketing: Até 29 / 30-39 / 40-49 / 50+ |
| `Tempo de Casa` | `Data de Contratação` | `ano_ref - ano_contratação` |
| `Ano Contratação` | `Data de Contratação` | `.dt.year` |
| `Nivel` | `Cargo` | Inferido por palavra-chave (Diretoria/Gerência/Analista/Assistente/Auxiliar) |

### Perfil estatístico

| Métrica | Satisfação | Salário (R$) | Idade | Tempo de Casa |
|---|---|---|---|---|
| Média | 3,86 | 5.561 | 40,9 anos | 6,8 anos |
| Mediana | 4,0 | 3.897 | 39 anos | 6 anos |
| Mín | 1,0 | 1.550 | 28 anos | 4 anos |
| Máx | 5,0 | 17.758 | 69 anos | 14 anos |
| Desvio padrão | 0,97 | 3.148 | 8,4 anos | 1,97 anos |

> **Nota:** 3 registros possuem `Salario = null` por inconsistência no campo `Salario-Cargo` da fonte Excel.

### Distribuição das variáveis categóricas

**Departamento**
| Área | n | % |
|---|---|---|
| Produção | 92 | 56% |
| Financeiro | 41 | 25% |
| Comercial | 24 | 15% |
| Administrativo | 7 | 4% |

**Performance**
| Nível | n | % |
|---|---|---|
| Regular | 130 | 79% |
| Excelente | 23 | 14% |
| Ruim | 11 | 7% |

**Recrutamento**
| Canal | n | % |
|---|---|---|
| Anúncios / Sites | 68 | 41% |
| LinkedIn | 35 | 21% |
| Indicação | 34 | 21% |
| Banco de Dados Interno | 27 | 16% |

**Gênero**
| Gênero | n | % |
|---|---|---|
| Masculino | 111 | 68% |
| Feminino | 53 | 32% |

---

## Arquitetura

```
people-analytics/
├── app.py                  # Aplicação principal (Streamlit)
├── dados_rh.parquet        # Cache do dataset (leitura ~5× mais rápida)
├── Base_dados_rh.xlsx      # Fonte original dos dados
├── requirements.txt        # Dependências Python
├── .streamlit/
│   └── config.toml         # Tema dark + configurações do servidor
├── .gitignore
└── README.md
```

### Fluxo de dados

```
Base_dados_rh.xlsx
       │
       ▼
  load_data()          ← @st.cache_data (lê parquet; fallback: excel)
       │
       ├── parse_sal()       → Salario, Cargo
       ├── Idade / Faixa Etaria
       ├── Tempo de Casa / Ano Contratação
       └── Nivel (inferido)
       │
       ▼
  df_full  ──→  filtros sidebar  ──→  df  ──→  KPIs + Gráficos
```

### Decisões de arquitetura

- **Parquet como cache:** leitura ~5× mais rápida que Excel; Excel mantido como fonte de verdade
- **`@st.cache_data`:** garante que `load_data()` executa uma única vez por sessão
- **CSS injetado via `st.markdown`:** tema dark customizado sem dependência de UI extra
- **Arquivo único `app.py`:** arquitetura plana adequada para deploy educacional no Streamlit Cloud

---

## Como executar localmente

### Pré-requisitos
- Python 3.9+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/cfneves/people-analytics.git
cd people-analytics

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
streamlit run app.py
```

O app abrirá automaticamente em `http://localhost:8501`.

---

## Dependências

```
streamlit  >= 1.32.0   # Framework de dashboards
pandas     >= 2.0.0    # Manipulação de dados
plotly     >= 5.18.0   # Visualizações interativas
openpyxl   >= 3.1.0    # Leitura de arquivos .xlsx
pyarrow    >= 14.0.0   # Leitura de arquivos .parquet
```

---

## Deploy no Streamlit Community Cloud

1. Faça fork ou push do repositório para o GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Clique em **New app**
4. Selecione o repositório `people-analytics`, branch `main`, arquivo `app.py`
5. Clique em **Deploy**

O Streamlit Cloud instala as dependências do `requirements.txt` automaticamente.

---

## Tema visual

| Elemento | Valor |
|---|---|
| Fundo principal | `#07090f` |
| Fundo sidebar/cards | `#0e1219` |
| Cor primária (azul) | `#4f8ef7` |
| Teal | `#2dd4bf` |
| Texto principal | `#e8edf5` |
| Texto secundário | `#7a8599` |
| Fonte | Syne (Google Fonts) |

---

*People Analytics Dashboard · Base_dados_rh.xlsx · 164 colaboradores · Março 2026*

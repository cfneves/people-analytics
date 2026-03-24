# Diagnóstico Técnico — People Analytics

> Auditoria realizada em Março 2026 · Versão analisada: v2.0

---

## Resumo executivo

O projeto é um dashboard de People Analytics funcional e visualmente bem construído, adequado para análise descritiva de uma equipe de 164 colaboradores. A auditoria identificou **2 bugs de dados**, **1 inconsistência de nomenclatura**, ausência de modelos preditivos e oportunidades claras de evolução para um produto de maior impacto analítico.

---

## 1. Qualidade dos dados

### Bugs encontrados

**Bug #1 — Salários nulos (3 registros)**
- **Afetados:** AC148, AC149, AC122 (`Analista Financeiro Junior` — R$ 6.120,32)
- **Causa raiz:** O campo `Salario-Cargo` usa ponto como separador de milhar (`6.120,32`). O parser original aplicava `replace(',','.')` resultando em `6.120.32`, que não é um float válido.
- **Correção:** `_parse_sal()` agora remove o ponto antes de converter a vírgula: `replace('.','').replace(',','.')`.
- **Status:** Corrigido na v2.1.

**Bug #2 — Data de referência hardcoded**
- **Onde:** `hoje = date(2026, 3, 23)` no cálculo de idades
- **Impacto:** Idades e faixas etárias ficarão incorretas após março de 2026
- **Correção:** `date.today()`
- **Status:** Corrigido na v2.1.

### Inconsistências de dados

| Problema | Detalhe | Registros afetados |
|---|---|---|
| Typo `"Gerente Fianceiro"` | Deveria ser `"Gerente Financeiro"` | 5 colaboradores |
| Satisfação com valores não inteiros | 2,5 / 2,8 / 3,5 presentes na escala | 3 registros |
| Salários na faixa Auxiliar > R$8.000 | R$8.521 para um Auxiliar (possível erro ou benefício) | 1 registro |

### Outliers salariais

Usando o método IQR (Q1=R$3.897, Q3=R$6.537, IQR=R$2.640):
- Limite superior = R$10.498
- **18 registros acima do limite** — todos são Diretores e Gerentes com salários entre R$12.000 e R$17.758
- **Conclusão:** São outliers legítimos (hierarquia alta), não erros de dados

---

## 2. Código — organização e qualidade

### Pontos positivos
- `@st.cache_data` corretamente aplicado em `load_data()` — evita reprocessamento
- Fallback parquet → Excel é robusto
- Paleta de cores e layout base são consistentes
- Sem bibliotecas desnecessárias

### Problemas identificados

| Severidade | Problema | Arquivo | Linha aprox. |
|---|---|---|---|
| Alta | `date(2026, 3, 23)` hardcoded | `app.py` | 229 |
| Alta | `parse_sal` não trata separador de milhar | `app.py` | 218–225 |
| Média | Arquivo único com 500+ linhas (sem modularização) | `app.py` | — |
| Média | Sem tratamento de `n=0` em todos os divisores | `app.py` | vários |
| Baixa | `except` genérico sem logging | `app.py` | 216 |
| Baixa | Nível inferido por palavra-chave (frágil) | `app.py` | 242–249 |

---

## 3. Performance

| Aspecto | Avaliação |
|---|---|
| Carregamento de dados | Bom — parquet ~5× mais rápido que Excel |
| Cache Streamlit | Implementado corretamente |
| Número de gráficos | 12 gráficos Plotly por renderização — pode ser pesado |
| Reatividade dos filtros | Boa — toda a lógica re-executa nos filtros |
| Tamanho do parquet | Pequeno (164 linhas) — sem problema de escala |

---

## 4. Modelos e métricas

### O que existe atualmente

O projeto usa **apenas estatística descritiva**:
- Contagens e percentuais
- Média, mediana, mín, máx
- Score de performance ponderado: `(Exc×3 + Reg×2 + Ruim×1) / n`

### O que está faltando

| Análise | Valor de negócio | Complexidade |
|---|---|---|
| Correlação satisfação × performance × salário | Alta | Baixa |
| Segmentação por clusters (K-Means) | Alta | Média |
| Análise de risco de turnover | Muito alta | Média |
| Evolução temporal (tendências) | Alta | Média |
| Análise de equidade salarial (gênero/cargo) | Alta | Baixa |
| Benchmarking salarial por cargo/nível | Média | Baixa |

---

## 5. UX/UI

### Versão v2.0 (atual) — melhorias já implementadas
- Cards KPI com HTML personalizado
- `st.container(border=True)` como sistema de cards
- Section headers com pill accent
- Sidebar com branding e pulse dot
- Progress bars customizadas com cores semânticas
- Fontes Inter (corpo) + Syne (display)

### Oportunidades restantes
- Ausência de tooltips explicativos nos KPIs
- Tabela de colaboradores mostra apenas top 20 fixos
- Sem feedback visual quando filtros resultam em n muito pequeno
- Sem modo de exportação dos dados filtrados

---

## 6. Repositório GitHub

### Estrutura atual (após v2.1)
```
people-analytics/
├── app.py              ✅ Aplicação principal
├── dados_rh.parquet    ✅ Cache de dados
├── Base_dados_rh.xlsx  ✅ Fonte original
├── requirements.txt    ✅ Dependências
├── .streamlit/
│   └── config.toml     ✅ Tema dark
├── docs/               ✅ Documentação técnica
├── README.md           ✅ Documentação principal
└── .gitignore          ✅
```

### O que ainda falta
- `CHANGELOG.md` — histórico de versões
- `.github/ISSUE_TEMPLATE/` — templates para issues
- Testes automatizados (`tests/`)
- `CONTRIBUTING.md` — guia de contribuição (criado em `docs/`)

---

*Diagnóstico Técnico · People Analytics · v2.1 · Março 2026*

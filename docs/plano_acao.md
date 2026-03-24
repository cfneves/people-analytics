# Plano de Ação — People Analytics

> Baseado no diagnóstico técnico de Março 2026

---

## Visão geral da priorização

```
IMPACTO
  ▲
  │  [Equidade salarial] [Análise turnover]
  │        [Correlações]   [Clusters RH]
  │  [Bug parse_sal]  [date.today()]
  │    [Docs /docs]   [README]
  └─────────────────────────────────────► ESFORÇO
       Baixo          Médio         Alto
```

---

## Quick Wins — Impacto rápido, esforço baixo

> Executar em 1–2 dias

| # | Ação | Status |
|---|---|---|
| QW-1 | Corrigir `parse_sal` para formato brasileiro (`6.120,32`) | ✅ Feito v2.1 |
| QW-2 | Substituir `date(2026,3,23)` por `date.today()` | ✅ Feito v2.1 |
| QW-3 | Criar `/docs` com dicionário de dados e diagnóstico | ✅ Feito v2.1 |
| QW-4 | Corrigir typo `"Gerente Fianceiro"` na base Excel | Pendente |
| QW-5 | Adicionar aviso visual quando filtros retornam n < 5 | Pendente |
| QW-6 | Exibir correlação satisfação × performance no dashboard | Pendente |

---

## Melhorias estruturais — Médio prazo

> Executar em 1–2 semanas

### Código

| # | Ação | Benefício |
|---|---|---|
| ME-1 | Modularizar `app.py` em `sections/` (seção por arquivo) | Manutenção mais fácil |
| ME-2 | Extrair lógica de dados para `data/pipeline.py` | Separação de responsabilidades |
| ME-3 | Adicionar logging com `loguru` para erros de parse | Diagnóstico em produção |
| ME-4 | Guardar parquet versionado com data no nome | Rastreabilidade |
| ME-5 | Tratar todos os casos `n=0` nos cálculos | Evitar divisão por zero |

### Análises

| # | Análise | Descrição |
|---|---|---|
| ME-6 | Heatmap de correlações | Satisfação × Performance × Salário × Tempo de Casa |
| ME-7 | Análise de equidade salarial | Comparar salários M vs F no mesmo cargo/nível |
| ME-8 | Benchmarking salarial por cargo | Mediana, P25, P75 por função |
| ME-9 | Evolução de contratações | Gráfico de linha com tendência 2012–2022 |

### Exemplo — Equidade salarial

```python
equidade = df.groupby(['Nivel', 'Sexo'])['Salario'].median().unstack()
equidade['gap_%'] = ((equidade['M'] - equidade['F']) / equidade['M'] * 100).round(1)
```

---

## Evolução estratégica — Longo prazo

> Executar em 1–3 meses

### Modelos de Machine Learning

| # | Modelo | Objetivo | Algoritmo sugerido |
|---|---|---|---|
| EL-1 | Predição de risco de saída | Identificar colaboradores com risco de turnover | Random Forest / XGBoost |
| EL-2 | Segmentação de colaboradores | Agrupar perfis similares para políticas de RH | K-Means / DBSCAN |
| EL-3 | Predição de performance | Prever desempenho com base no perfil | Regressão logística |
| EL-4 | Score de engajamento | Índice composto: satisfação + tempo de casa + nível | Análise de componentes |

### Infraestrutura

| # | Ação | Benefício |
|---|---|---|
| EL-5 | Conectar a banco de dados (PostgreSQL/BigQuery) | Dados em tempo real |
| EL-6 | Implementar refresh automático dos dados | Dashboard sempre atualizado |
| EL-7 | Adicionar autenticação (Streamlit Secrets + login) | Controle de acesso |
| EL-8 | Pipeline ETL com agendamento (Airflow/Prefect) | Automatização |

### Storytelling

| # | Ação |
|---|---|
| EL-9 | Adicionar narrativas contextuais nos gráficos ("O que esse número significa?") |
| EL-10 | Alertas automáticos para KPIs fora do padrão |
| EL-11 | Exportação de relatório PDF do dashboard |

---

## Riscos identificados

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Dados com formato incorreto (como os 3 nulos) | Alta | Médio | `_parse_sal()` corrigido + validação de entrada |
| Dashboard exibindo KPIs errados com `n=0` | Média | Alto | Guards `if n else 0` em todos os divisores |
| Parquet desatualizado em relação ao Excel | Média | Médio | Versionamento do parquet com data |
| Modelo de nível por keyword falhar em novos cargos | Alta | Baixo | Mapeamento explícito em dicionário |
| Deploy falhar por versão incompatível do Plotly | Baixa | Alto | Fixar versões no `requirements.txt` |
| Dados sensíveis de colaboradores expostos publicamente | Baixa | Alto | Avaliar autenticação antes de dados reais |

---

## Métricas de sucesso

Para avaliar o impacto das melhorias, acompanhar:

| Métrica | Baseline atual | Meta |
|---|---|---|
| Salários nulos | 3 (1,8%) | 0 |
| Cobertura de análises | Apenas descritiva | + correlações + clusters |
| Tempo de carregamento | ~2s (estimado) | < 1s |
| Documentação | README básico | README + /docs completo |
| Bugs críticos abertos | 2 (corrigidos) | 0 |

---

*Plano de Ação · People Analytics · v2.1 · Março 2026*

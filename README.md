# People Analytics — Mapa de Colaboradores

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://people-analytics-cfn.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/Licença-MIT-green)

Dashboard de RH feito com Streamlit e Plotly. Mostra quem são os 164 colaboradores, onde estão, quanto ganham e como performam — tudo filtrável em tempo real.

---

## Por que existe

Planilha de RH não mostra nada além do que você procura ativamente. Você não percebe que a satisfação caiu no Financeiro até olhar para ela diretamente. Não vê o desbalanceamento de gênero nas gerências até calcular. Esse dashboard junta tudo num lugar, com filtros que respondem na hora.

---

## Acesso

- **Dashboard ao vivo:** https://people-analytics-cfn.streamlit.app/
- **Base:** 164 colaboradores ativos · Março 2026

---

## Stack

| Tecnologia | Uso |
|---|---|
| Python 3.9+ | Linguagem principal |
| Streamlit 1.32+ | Framework do dashboard |
| Plotly 5.18+ | Visualizações interativas |
| Pandas 2.0+ | Manipulação de dados |
| Parquet (PyArrow) | Cache de dados rápido |

---

## Rodando localmente

```bash
git clone https://github.com/cfneves/people-analytics.git
cd people-analytics
pip install -r requirements.txt
streamlit run app.py
```

Abre em `http://localhost:8501`.

---

## O que tem no dashboard

A sidebar tem quatro filtros: Departamento, Performance, Satisfação mínima e Canal de recrutamento. Todos os gráficos e KPIs mudam ao selecionar.

Na parte de cima, seis KPIs: total de colaboradores, folha salarial (total e média), satisfação média, score de performance ponderado, tempo médio de casa e mediana salarial.

O restante está dividido em quatro seções:

1. **Força de trabalho** — departamentos, canal de recrutamento, gênero, faixa etária e contratações por ano
2. **Performance & Satisfação** — distribuição de performance, histograma de satisfação e score com barra de progresso
3. **Salários & Níveis** — pirâmide hierárquica, faixa salarial completa e top 10 cargos
4. **Retenção & Tabela** — veteranos vs. novatos, timeline por ano e amostra dos colaboradores

---

## O que os dados mostram

Alguns números que valem atenção:

- 79% da equipe tem performance Regular. Apenas 14% Excelente e 7% Ruim. Isso não é necessariamente ruim — depende de como a escala foi calibrada — mas é um número que merece discussão com RH.
- Satisfação e performance têm correlação de apenas 0,23. Na prática: pessoa satisfeita não é garantia de boa performance, e quem performa bem pode não estar satisfeito. As duas métricas precisam ser monitoradas separadamente.
- 2020 foi o ano com mais contratações. Aparece destacado em todos os gráficos de timeline.
- 68% dos colaboradores são homens. Nas gerências, esse número é mais alto — o dashboard deixa isso visível quando você filtra por nível.
- Salário médio de R$5.561, mediana de R$3.897. A diferença existe porque a faixa de diretores e gerentes puxa a média para cima. A mediana é o número mais representativo para a maioria da equipe.

---

## Documentação técnica

A pasta `/docs` tem quatro arquivos:

- `dicionario_dados.md` — todas as colunas, tipos, categorias, qualidade e correlações
- `diagnostico_tecnico.md` — bugs encontrados e corrigidos, análise de código, outliers e riscos
- `plano_acao.md` — o que foi feito, o que ainda falta e o que faz sentido evoluir
- `guia_contribuidores.md` — como configurar o ambiente, estrutura do código e como abrir um PR

---

## Deploy no Streamlit Cloud

1. Fork ou push para o GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. New app → repositório `people-analytics`, branch `main`, arquivo `app.py`
4. Deploy — o Streamlit instala o `requirements.txt` automaticamente

---

## Estrutura do projeto

```
people-analytics/
│
├── app.py                        # Dashboard principal (Streamlit)
├── dados_rh.parquet              # Cache do dataset (5× mais rápido que Excel)
├── Base_dados_rh.xlsx            # Fonte original dos dados
├── requirements.txt              # Dependências fixadas
│
├── .streamlit/
│   └── config.toml               # Tema dark + configurações do servidor
│
├── docs/                         # Documentação técnica
│   ├── dicionario_dados.md       # Schema, tipos, qualidade dos dados
│   ├── diagnostico_tecnico.md    # Bugs, outliers, análise de código
│   ├── plano_acao.md             # Roadmap priorizado
│   └── guia_contribuidores.md    # Como rodar, contribuir e estender
│
├── .github/
│   └── ISSUE_TEMPLATE/           # Templates para bugs e sugestões
│
├── CHANGELOG.md                  # Histórico de versões
└── README.md
```

---

## Próximos passos

O roadmap completo está em [`docs/plano_acao.md`](docs/plano_acao.md). Em resumo:

**Curto prazo**
- Corrigir typo `"Gerente Fianceiro"` na base Excel
- Adicionar heatmap de correlações (satisfação × performance × salário)
- Aviso visual quando filtros retornam menos de 5 registros

**Médio prazo**
- Análise de equidade salarial por gênero dentro do mesmo cargo
- Modularizar `app.py` em seções separadas

**Longo prazo**
- Modelo de predição de risco de turnover
- Segmentação de colaboradores com K-Means
- Autenticação para uso com dados reais

---

## Versões

| Versão | O que mudou |
|---|---|
| v1.0 | Dashboard inicial — Streamlit + Plotly |
| v2.0 | Redesign completo — cards, CSS premium, layout reestruturado |
| v2.1 | Correção do parser de salário BR, data dinâmica, documentação `/docs` |

Histórico detalhado em [`CHANGELOG.md`](CHANGELOG.md).

---

## Autor

**🛠️ Cláudio Ferreira Neves**
Especialista em Business Intelligence, Big Data & Analytics — Ciência de Dados
Especialista em Ciência de Dados e Inteligência Artificial
MBA em Gestão de Projetos

[![GitHub](https://img.shields.io/badge/GitHub-cfneves-181717?logo=github)](https://github.com/cfneves)

---

*People Analytics · v2.1 · Março 2026*

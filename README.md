# People Analytics — Mapa de Colaboradores

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

## Versões

| Versão | O que mudou |
|---|---|
| v1.0 | Dashboard inicial — Streamlit + Plotly |
| v2.0 | Redesign completo — cards, CSS premium, layout reestruturado |
| v2.1 | Correção do parser de salário BR, data dinâmica, documentação `/docs` |

---

*People Analytics · v2.1 · Março 2026*

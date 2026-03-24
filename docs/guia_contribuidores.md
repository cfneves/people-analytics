# Guia para Contribuidores

Bem-vindo ao projeto People Analytics. Este guia explica como configurar o ambiente, entender a estrutura do código e contribuir com melhorias.

---

## Pré-requisitos

- Python 3.9 ou superior
- Git configurado
- Conta no GitHub (para pull requests)

---

## Configuração do ambiente

```bash
# 1. Clone o repositório
git clone https://github.com/cfneves/people-analytics.git
cd people-analytics

# 2. Crie um ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate       # Linux/Mac
.venv\Scripts\activate          # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o dashboard
streamlit run app.py
```

O app abrirá automaticamente em `http://localhost:8501`.

---

## Estrutura do projeto

```
people-analytics/
│
├── app.py                  # Aplicação principal Streamlit
├── dados_rh.parquet        # Cache do dataset (leitura rápida)
├── Base_dados_rh.xlsx      # Fonte original dos dados
├── requirements.txt        # Dependências Python fixadas
│
├── .streamlit/
│   └── config.toml         # Tema dark e configurações do servidor
│
├── docs/                   # Documentação técnica
│   ├── dicionario_dados.md
│   ├── diagnostico_tecnico.md
│   ├── plano_acao.md
│   └── guia_contribuidores.md
│
├── README.md
└── .gitignore
```

---

## Como funciona o código

### Fluxo principal do `app.py`

```
1. st.set_page_config()      → configuração da página
2. Design system (C dict)    → paleta de cores e tokens
3. CSS injetado              → tema dark personalizado
4. Funções helper HTML       → kpi_card(), section_header(), etc.
5. load_data()               → carrega e transforma os dados
6. Sidebar                   → filtros interativos
7. Filtro do dataframe       → aplica seleções do usuário
8. Header + KPIs             → visão geral
9. Seção 1: Força de trabalho
10. Seção 2: Performance & Satisfação
11. Seção 3: Salários & Níveis
12. Seção 4: Retenção & Tabela
13. Footer
```

### Função `load_data()`

```python
@st.cache_data          # Executa apenas uma vez por sessão
def load_data():
    # Tenta parquet primeiro (rápido)
    # Fallback para Excel se parquet não existir
    # Gera colunas derivadas: Salario, Cargo, Idade, Nivel, etc.
```

### Design system

Todas as cores estão no dicionário `C`:

```python
C = {
    "bg":     "#060810",    # Fundo principal
    "blue":   "#4f8ef7",    # Cor primária
    "teal":   "#2dd4bf",    # Cor secundária
    "green":  "#4ade80",    # Positivo / sucesso
    "amber":  "#fbbf24",    # Atenção / neutro
    "red":    "#f87171",    # Negativo / alerta
    # ...
}
```

Para mudar o tema, edite apenas o dicionário `C`.

---

## Adicionando uma nova seção ao dashboard

1. Calcule os dados necessários após o bloco de filtro
2. Crie um novo bloco com `section_header()`:

```python
st.markdown(section_header("Minha Nova Seção", C["cyan"]), unsafe_allow_html=True)
col_a, col_b = st.columns([1, 1])

with col_a:
    with st.container(border=True):
        st.markdown(chart_title("Meu gráfico"), unsafe_allow_html=True)
        # seu gráfico plotly aqui
```

3. Siga o padrão de cores e alturas existentes.

---

## Adicionando um novo gráfico Plotly

Use sempre `PLOTLY_BASE` como base de layout:

```python
fig = px.bar(df, x="Col", y="Valor", height=200)
fig.update_layout(**PLOTLY_BASE, showlegend=False)
fig.update_traces(marker_line_width=0)   # remove borda das barras
fig.update_xaxes(showgrid=False, zeroline=False)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
```

---

## Atualizando os dados

Para atualizar a base com novos dados:

1. Substitua `Base_dados_rh.xlsx` pelo novo arquivo (mantendo o mesmo schema)
2. Delete `dados_rh.parquet` para forçar reprocessamento
3. Execute `streamlit run app.py` — o parquet será recriado automaticamente

---

## Fluxo de contribuição

```
1. Fork do repositório
2. git checkout -b feat/minha-melhoria
3. Faça as alterações
4. git commit -m "feat: descrição clara do que foi feito"
5. git push origin feat/minha-melhoria
6. Abra um Pull Request no GitHub
```

### Convenção de commits

| Prefixo | Uso |
|---|---|
| `feat:` | Nova funcionalidade |
| `fix:` | Correção de bug |
| `docs:` | Documentação |
| `refactor:` | Refatoração sem mudança de comportamento |
| `style:` | Mudanças visuais/CSS |
| `data:` | Atualização ou correção de dados |

---

## Dúvidas e suporte

Abra uma issue no GitHub com a tag adequada:
- `bug` — problema encontrado
- `enhancement` — sugestão de melhoria
- `question` — dúvida sobre o projeto
- `documentation` — melhoria na documentação

---

*Guia para Contribuidores · People Analytics · v2.1*

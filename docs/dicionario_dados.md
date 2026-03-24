# Dicionário de Dados

## Arquivo-fonte: `Base_dados_rh.xlsx`

Este documento descreve cada coluna presente no dataset de RH, incluindo tipo, origem e exemplos de valores reais.

---

## Colunas originais (Excel)

| Coluna | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `Colaborador` | string | Nome completo do colaborador | `ELÁSIO ARAGÃO` |
| `ID` | string | Código único de identificação | `AC75` |
| `Salario-Cargo` | string | Campo composto: `valor-cargo` | `15453,25-Diretor Vendas` |
| `Data de Nascimento` | datetime | Data de nascimento | `1973-01-13` |
| `Sexo` | string | Gênero: `M` (masculino) ou `F` (feminino) | `M` |
| `Data de Contratação` | datetime | Data de admissão na empresa | `2012-10-02` |
| `Status` | string | Situação do colaborador | `Ativo` (único valor) |
| `Departamento` | string | Área de atuação | `Comercial` |
| `Recrutamento` | string | Canal pelo qual foi contratado | `Indicação` |
| `Performance` | string | Avaliação de desempenho | `Excelente` |
| `Satisfação` | float | Nota de satisfação (escala 1,0–5,0) | `4.0` |

---

## Colunas derivadas (calculadas em `load_data()`)

| Coluna | Origem | Lógica de cálculo | Tipo |
|---|---|---|---|
| `Salario` | `Salario-Cargo` | `rsplit('-', 1)[0]` → remove separador de milhar (`.`) → converte vírgula em ponto → `float` | float |
| `Cargo` | `Salario-Cargo` | `rsplit('-', 1)[1].strip()` | string |
| `Idade` | `Data de Nascimento` | `(date.today() - nascimento).days // 365` | int |
| `Faixa Etaria` | `Idade` | Bucketing: Até 29 / 30-39 / 40-49 / 50+ | string (categoria) |
| `Tempo de Casa` | `Data de Contratação` | `ano_atual - ano_contratação` | int (anos) |
| `Ano Contratação` | `Data de Contratação` | `.dt.year` | int |
| `Nivel` | `Cargo` | Mapeamento por palavra-chave (ver tabela abaixo) | string (categoria) |

---

## Categorias e valores únicos

### Departamento
| Valor | Colaboradores | % |
|---|---|---|
| Produção | 92 | 56% |
| Financeiro | 41 | 25% |
| Comercial | 24 | 15% |
| Administrativo | 7 | 4% |

### Performance
| Valor | Colaboradores | % | Peso no score |
|---|---|---|---|
| Regular | 130 | 79% | 2 |
| Excelente | 23 | 14% | 3 |
| Ruim | 11 | 7% | 1 |

### Recrutamento
| Valor | Colaboradores | % |
|---|---|---|
| Anúncios / Sites | 68 | 41% |
| LinkedIn | 35 | 21% |
| Indicação | 34 | 21% |
| Banco Dados Interno | 27 | 16% |

### Sexo
| Valor | Colaboradores | % |
|---|---|---|
| M (Masculino) | 111 | 68% |
| F (Feminino) | 53 | 32% |

### Nível hierárquico (inferido do cargo)
| Nível | Palavra-chave | Colaboradores |
|---|---|---|
| Diretoria | `diretor` | 5 |
| Gerência | `gerente` | 13 |
| Analista | `analista` | 21 |
| Assistente | `assistente` | 49 |
| Auxiliar | (demais) | 73 |

> **Nota:** A inferência de nível por palavra-chave pode não capturar títulos atípicos. Recomenda-se revisão manual periódica.

---

## Qualidade dos dados

| Indicador | Situação |
|---|---|
| Linhas duplicadas | 0 |
| IDs duplicados | 0 |
| Salários nulos | 3 (registros `AC148`, `AC149`, `AC122`) |
| Causa dos nulos | Formato `6.120,32` (ponto como milhar) no campo `Salario-Cargo` |
| Status da correção | Corrigido automaticamente em `_parse_sal()` — v2.1 |
| Typo identificado | `"Gerente Fianceiro"` (deveria ser `"Gerente Financeiro"`) — 5 registros |

---

## Notas sobre satisfação

A escala de satisfação varia de 1,0 a 5,0, mas contém valores não inteiros:

| Valor | Frequência |
|---|---|
| 1,0 | 2 |
| 2,0 | 4 |
| 2,5 | 1 |
| 2,8 | 1 |
| 3,0 | 62 |
| 3,5 | 1 |
| 4,0 | 37 |
| 5,0 | 56 |

A distribuição é levemente assimétrica negativa (skewness = -0,22), com concentração nos extremos 3 e 5.

---

## Correlações relevantes

| Par de variáveis | Correlação (Pearson) | Interpretação |
|---|---|---|
| Satisfação × Performance | 0,23 | Fraca positiva |
| Salário × Performance | 0,18 | Fraca positiva |
| Salário × Idade | 0,17 | Fraca positiva |
| Satisfação × Salário | -0,02 | Praticamente nula |

> Correlações fracas indicam que **satisfação e desempenho são dimensões independentes** nessa base, o que é um insight de negócio relevante para RH.

---

*Dicionário de Dados · People Analytics · v2.1 · Março 2026*

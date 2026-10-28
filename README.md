# SalesInsight PY

## Análise e Visualização de Dados de Vendas com Python

Projeto avaliativo — Módulo 01 — Semana 07.

## 1. Descrição do projeto

O **SalesInsight PY** é uma aplicação desenvolvida em Python para gerar, inspecionar, limpar, transformar e analisar dados de vendas.

O projeto utiliza bibliotecas de análise de dados e visualização para calcular métricas comerciais, segmentar clientes, gerar gráficos e exportar resultados para arquivos CSV e JSON.

## 2. Objetivos

- Gerar um conjunto de dados sintético de vendas.
- Inspecionar a estrutura e a qualidade dos dados.
- Limpar dados e remover registros com datas inválidas.
- Criar colunas derivadas para análise.
- Calcular métricas de vendas por mês, produto, categoria e região.
- Segmentar clientes conforme o gasto total.
- Gerar gráficos para visualizar os resultados.
- Exportar métricas e estatísticas para arquivos CSV e JSON.
- Organizar o fluxo de execução utilizando funções reutilizáveis e a classe `AnalisadorDeVendas`.

## 3. Tecnologias utilizadas

- **Python:** linguagem de programação.
- **NumPy:** geração de dados e operações numéricas.
- **Pandas:** manipulação, limpeza e análise de dados.
- **Matplotlib:** criação de gráficos.
- **JSON:** exportação e leitura de estatísticas.
- **Git e GitHub:** controle de versão e hospedagem do código-fonte.

## 4. Estrutura do projeto

```text
SalesInsight-PY/
├── salesinsight.py
├── vendas.csv
├── outputs/
│   ├── metricas_por_mes.csv
│   ├── segmentacao_clientes.csv
│   ├── estatisticas_gerais.json
│   └── graficos/
│       ├── receita_por_mes.png
│       ├── top_produtos.png
│       ├── quantidade_vs_receita.png
│       └── painel_resumo.png
└── README.md
```

Os arquivos de saída são gerados durante a execução do programa. A pasta `outputs/` e seus arquivos podem não existir antes da primeira execução.

## 5. Instalação

### Pré-requisitos

- Python instalado.
- Git instalado, caso o repositório seja clonado.
- Acesso a um terminal para executar os comandos.

### Instalar as dependências

No terminal, execute:

```bash
pip install numpy pandas matplotlib
```

## 6. Como executar

1. Abra o terminal na pasta raiz do projeto.
2. Execute o programa:

```bash
python salesinsight.py
```

O programa gera os dados sintéticos, executa as etapas de análise, apresenta informações no terminal e salva os resultados nos arquivos de saída.

O arquivo `vendas.csv` é gerado durante a execução, utilizando os dados sintéticos criados pelo programa.

## 7. Funcionalidades implementadas

### 7.1. Geração de dados

A função `gerar_dataset_vendas()` cria um conjunto de dados sintético com informações sobre vendas, incluindo produto, categoria, quantidade, preço unitário, região, cliente e data da venda.

### 7.2. Inspeção e limpeza

As funções `inspecionar_dados()` e `limpar_dados_vendas()` permitem examinar a estrutura dos dados, identificar valores nulos e tratar datas inválidas e colunas numéricas e textuais.

### 7.3. Transformação dos dados

A função `transformar_dados_vendas()` cria colunas derivadas, incluindo receita total, mês, nome do mês, trimestre, ano e faixa de receita.

### 7.4. Métricas de vendas

A função `calcular_metricas_vendas()` calcula métricas relacionadas a:

- Receita, quantidade e número de vendas por mês.
- Os cinco produtos com maior receita.
- Receita por categoria.
- Receita total e ticket médio por região.

### 7.5. Segmentação de clientes

A função `segmentar_clientes()` calcula o gasto total por cliente e classifica os clientes em três segmentos:

- **Bronze:** gasto inferior a 5.000.
- **Prata:** gasto entre 5.000 e 15.000, inclusive.
- **Ouro:** gasto superior a 15.000.

A função também apresenta os dez clientes com maior gasto e a distribuição dos clientes por segmento.

### 7.6. Visualização dos dados

A função `gerar_graficos_vendas()` gera quatro gráficos em formato PNG:

1. Receita total por mês.
2. Os cinco produtos com maior receita.
3. Relação entre quantidade e receita total por categoria.
4. Painel resumo com quatro visualizações, incluindo receita por região.

### 7.7. Exportação dos resultados

A função `exportar_resultados()` salva os resultados nos seguintes arquivos:

- `outputs/metricas_por_mes.csv`
- `outputs/segmentacao_clientes.csv`
- `outputs/estatisticas_gerais.json`

O arquivo JSON é lido novamente após a exportação para conferir os dados gravados.

## 8. Organização do código

O projeto utiliza funções reutilizáveis para separar as etapas de processamento e a classe `AnalisadorDeVendas` para organizar o fluxo principal.

A função `processar_coluna()` permite aplicar diferentes funções de transformação a uma coluna de um DataFrame. O projeto também utiliza expressões `lambda` em operações de transformação e classificação.

A execução principal é coordenada pela função `main()`.

## 9. Resultados esperados

Após a execução bem-sucedida, o projeto apresenta informações de análise no terminal e gera:

- O conjunto de dados de vendas em CSV.
- As métricas mensais em CSV.
- A segmentação de clientes em CSV.
- As estatísticas gerais em JSON.
- Quatro gráficos em PNG.

## 10. Controle de versão

O desenvolvimento do projeto é organizado em branches e commits no Git, permitindo acompanhar a evolução das funcionalidades implementadas.

## 11. Autoria

Projeto desenvolvido como atividade avaliativa do Módulo 01 — Semana 07.

"""
SalesInsight PY
Análise e Visualização de Dados de Vendas com Python.

Projeto avaliativo - Módulo 01 - Semana 07.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os



def gerar_dataset_vendas(quantidade_vendas=200, semente=42):
    """Gera um DataFrame sintético de vendas.

    Args:
        quantidade_vendas: Número de vendas a gerar.
        semente: Semente para reproduzir os resultados aleatórios.

    Returns:
        DataFrame com os dados de vendas gerados.
    """

    np.random.seed(semente)


    produtos = {
        "Notebook": ("Computadores", 3500.00),
        "Smartphone": ("Celulares", 2200.00),
        "Tablet": ("Computadores", 1800.00),
        "Monitor": ("Computadores", 1200.00),
        "Teclado": ("Perifericos", 250.00),
        "Mouse": ("Perifericos", 120.00),
        "Headset": ("Perifericos", 350.00),
    }

    regioes = [
        "Sudeste",
        "Sul",
        "Nordeste",
        "Centro-Oeste",
        "Norte",
    ]

    nomes_produtos = list(produtos.keys())
    vendas = []

    for i in range(quantidade_vendas):
        produto = np.random.choice(nomes_produtos)
        categoria, preco_base = produtos[produto]

        quantidade = int(np.random.randint(1, 11))

        variacao_preco = np.random.uniform(0.90, 1.10)
        preco_unitario = round(preco_base * variacao_preco, 2)

        data_venda = pd.Timestamp(
            year=2025,
            month=int(np.random.randint(1, 13)),
            day=int(np.random.randint(1, 29)),
        )

        if np.random.random() < 0.03:
            data_venda = "DATA INVALIDA"

        cliente = f"Cliente_{np.random.randint(1, 51):03d}"

        venda = {
            "id_venda": i + 1,
            "data_venda": data_venda,
            "produto": produto,
            "categoria": categoria,
            "quantidade": quantidade,
            "preco_unitario": preco_unitario,
            "regiao": np.random.choice(regioes),
            "cliente": cliente,
        }

        vendas.append(venda)

    return pd.DataFrame(vendas)




def processar_coluna(df, coluna, funcao_transformacao, nome_saida=None):
    """Aplica uma função de transformação a uma coluna do DataFrame.

    Args:
        df: DataFrame que contém os dados.
        coluna: Nome da coluna que será transformada.
        funcao_transformacao: Função aplicada aos valores da coluna.
        nome_saida: Nome opcional da nova coluna criada.

    Returns:
        DataFrame com a nova coluna transformada.
    """

    nome_saida = nome_saida or f"{coluna}_transformado"

    df[nome_saida] = df[coluna].apply(funcao_transformacao)

    return df




def exportar_resultados(metricas, clientes, estatisticas):
    """Exporta métricas e estatísticas para arquivos CSV e JSON.

    Args:
        metricas: Dicionário com as métricas de vendas.
        clientes: DataFrame com a segmentação dos clientes.
        estatisticas: Dicionário com as estatísticas gerais.

    Returns:
        None.
    """

    
    os.makedirs("outputs", exist_ok=True)

    metricas["por_mes"].to_csv(
        "outputs/metricas_por_mes.csv",
        index=False,
        encoding="utf-8-sig",
    )

    clientes.to_csv(
        "outputs/segmentacao_clientes.csv",
        index=False,
        encoding="utf-8-sig",
    )

    serializavel = {
        k: round(float(v), 2)
        for k, v in estatisticas.items()
    }

    caminho = "outputs/estatisticas_gerais.json"

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(
            serializavel,
            f,
            indent=4,
            ensure_ascii=False,
        )

    with open(caminho, "r", encoding="utf-8") as f:
        conferencia = json.load(f)

    print("\nEstatisticas gerais exportadas:")
    print(conferencia)

class AnalisadorDeVendas:
    """Organiza o fluxo de análise de dados de vendas."""

    def __init__(self):
        """Inicializa os atributos utilizados na análise de vendas.

    Args:
        Nenhum, além de self.

    Returns:
        None. Inicializa os atributos da instância.
    """
        self.df_bruto = None
        self.df_limpo = None
        self.metricas = None
        self.clientes = None

    def carregar(self, caminho="vendas.csv"):
        """Gera e salva os dados de vendas em um arquivo CSV.

    Args:
        caminho: Caminho do arquivo CSV de saída.

    Returns:
        DataFrame com os dados originais de vendas.
    """

        self.df_bruto = gerar_dataset_vendas()

        self.df_bruto.to_csv(
            caminho,
            index=False,
            encoding="utf-8-sig"
        )

        return self.df_bruto
    
    def transformar(self):
        """Limpa e transforma os dados de vendas.

    Args:
        Nenhum, além de self.

    Returns:
        DataFrame com os dados de vendas limpos e transformados.
    """

        self.df_limpo = limpar_dados_vendas(self.df_bruto)

        self.df_limpo = transformar_dados_vendas(self.df_limpo)

        return self.df_limpo
    
    def analisar(self):
        """Calcula as métricas de vendas e segmenta os clientes.

    Args:
        Nenhum, além de self.

    Returns:
        Tupla com o dicionário de métricas e o DataFrame de clientes.
    """

        self.metricas = calcular_metricas_vendas(self.df_limpo)

        self.clientes = segmentar_clientes(self.df_limpo)

        return self.metricas, self.clientes
    
    def visualizar(self):
        """Gera os gráficos para a análise de vendas.

    Args:
        Nenhum, além de self.

    Returns:
        None. Salva os gráficos em arquivos PNG.
    """

        gerar_graficos_vendas(self.df_limpo)
        
    def resumo(self):
        """Apresenta um resumo final da análise de vendas.

    Args:
        Nenhum, além de self.

    Returns:
        None. Exibe o resumo dos dados e dos segmentos de clientes.
    """

        print("\nResumo da Análise de Vendas")
        print("-" * 35)

        print(f"Total de registros originais: {len(self.df_bruto)}")
        print(f"Total de registros analisados: {len(self.df_limpo)}")

        print(
            f"Receita total: "
            f"R$ {self.df_limpo['receita_total'].sum():.2f}"
        )

        print("\nDistribuição dos clientes por segmento:")
        print(self.clientes["segmento"].value_counts())

def main():
    """Executa o fluxo principal da análise de vendas.

    Args:
        Nenhum.

    Returns:
        None. Coordena a execução das etapas de análise.
    """

    print("SalesInsight PY - Análise de Dados de Vendas")

    analisador = AnalisadorDeVendas()

    analisador.carregar("vendas.csv")

    print(analisador.df_bruto.head())
    print(
        f"\nQuantidade de registros: "
        f"{len(analisador.df_bruto)}"
    )

    inspecionar_dados(analisador.df_bruto)

    analisador.transformar()

    processar_coluna(
        analisador.df_limpo,
        "receita_total",
        lambda x: round(x / 1000, 2),
        "receita_em_milhares"
    )

    processar_coluna(
        analisador.df_limpo,
        "quantidade",
        lambda q: "Alto Volume" if q > 5 else "Baixo Volume",
        "perfil_volume"
    )

    analisador.analisar()

    estatisticas = {
        "total_registros": len(analisador.df_limpo),
        "receita_total": float(
            analisador.df_limpo["receita_total"].sum()
        ),
        "quantidade_produtos": int(
            analisador.df_limpo["produto"].nunique()
        ),
        "quantidade_clientes": int(
            analisador.df_limpo["cliente"].nunique()
        )
    }

    exportar_resultados(
        analisador.metricas,
        analisador.clientes,
        estatisticas
    )

    analisador.visualizar()

    analisador.resumo()
    

def inspecionar_dados(df_vendas):
    """Inspeciona a estrutura e o conteúdo dos dados de vendas.

    Args:
        df_vendas: DataFrame com os dados de vendas.

    Returns:
        None. Exibe informações sobre os dados.
    """

    print("Dimensoes do conjunto de dados:")

    print("Dimensoes do conjunto de dados:")
    print(df_vendas.shape)

    print("\nColunas do conjunto de dados:")
    print(df_vendas.columns)

    print("\nTipos de dados:")
    print(df_vendas.dtypes)

    print("\nValores nulos por coluna:")
    print(df_vendas.isnull().sum())

    print("\nPrimeiras cinco linhas:")
    print(df_vendas.head())
    
    df_vendas.to_csv(
        "vendas.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("\nDataset de vendas gerado com sucesso!")
    print("Arquivo gerado: vendas.csv")
  
def limpar_dados_vendas(df_vendas):
    """Limpa os dados de vendas e remove datas inválidas.

    Args:
        df_vendas: DataFrame com os dados originais de vendas.

    Returns:
        DataFrame com os dados limpos.
    """

    df_vendas = df_vendas.copy()

    df_vendas["data_venda"] = pd.to_datetime(
    df_vendas["data_venda"],
        errors="coerce",
    )  
    
    quantidade_inicial = len(df_vendas)

    df_vendas = df_vendas.dropna(
        subset=["data_venda"]
    ).copy()

    quantidade_removida = quantidade_inicial - len(df_vendas)  
    
    colunas_texto = [
        "produto",
        "categoria",
        "regiao",
        "cliente",
    ]

 
    for coluna in colunas_texto:
        df_vendas[coluna] = (
            df_vendas[coluna]
            .astype("string")
            .str.strip()
        )

    colunas_numericas = [
        "id_venda",
        "quantidade",
        "preco_unitario",
    ]

    for coluna in colunas_numericas:
        df_vendas[coluna] = pd.to_numeric(
            df_vendas[coluna],
            errors="coerce",
        )

    valores_nulos_numericos = df_vendas[
        colunas_numericas
    ].isnull().sum()

    print("\nValores nulos nas colunas numericas:")
    print(valores_nulos_numericos)

    
    quantidade_final = len(df_vendas)

    print("\nRelatorio de limpeza:")
    print(f"Quantidade inicial de registros: {quantidade_inicial}")
    print(f"Registros removidos por data invalida: {quantidade_removida}")
    print(f"Quantidade final de registros: {quantidade_final}")
    
    return df_vendas

def transformar_dados_vendas(df_vendas):
    """Cria colunas derivadas para a análise das vendas."""

    df_vendas = df_vendas.copy()

    df_vendas["receita_total"] = (
        df_vendas["quantidade"] * df_vendas["preco_unitario"]
    )

    df_vendas["mes"] = df_vendas["data_venda"].dt.month
    nomes_meses = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }

    df_vendas["mes_nome"] = df_vendas["mes"].map(nomes_meses)
    
    df_vendas["trimestre"] = df_vendas["data_venda"].dt.quarter
    
    df_vendas["ano"] = df_vendas["data_venda"].dt.year
    
    condicoes = [
        df_vendas["receita_total"] < 500,
        (df_vendas["receita_total"] >= 500)
        & (df_vendas["receita_total"] < 2000),
        df_vendas["receita_total"] >= 2000,
    ]

    faixas = [
        "Baixa",
        "Media",
        "Alta",
    ]

    df_vendas["faixa_receita_item"] = np.select(
        condicoes,
        faixas,
        default="Baixa",
    )


    return df_vendas



def calcular_metricas_vendas(df_vendas):
    """Calcula métricas agregadas por mês, produto, categoria e região.

    Args:
        df_vendas: DataFrame com os dados de vendas transformados.

    Returns:
        Dicionário com DataFrames das métricas por mês, produto,
        categoria e região.
    """


    vendas_por_mes = (
        df_vendas.groupby(["ano", "mes", "mes_nome"])
        .agg(
            receita_total=("receita_total", "sum"),
            quantidade=("quantidade", "sum"),
            n_vendas=("id_venda", "nunique")
        )
        .reset_index()
        .sort_values(["ano", "mes"])
    )

    vendas_por_produto = (
        df_vendas.groupby("produto")["receita_total"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    vendas_por_categoria = (
        df_vendas.groupby("categoria")["receita_total"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    vendas_por_regiao = (
        df_vendas.groupby("regiao")
        .agg(
            receita_total=("receita_total", "sum"),
            ticket_medio=("receita_total", "mean")
        )
        .reset_index()
        .sort_values("receita_total", ascending=False)
    )

    metricas = {
        "por_mes": vendas_por_mes,
        "top_produtos": vendas_por_produto,
        "por_categoria": vendas_por_categoria,
        "por_regiao": vendas_por_regiao
    }

    print("\n=== RECEITA, QUANTIDADE E VENDAS POR MES ===")
    print(vendas_por_mes.to_string(index=False))

    print("\n=== TOP 5 PRODUTOS POR RECEITA ===")
    print(vendas_por_produto.to_string(index=False))

    print("\n=== RECEITA POR CATEGORIA ===")
    print(vendas_por_categoria.to_string(index=False))

    print("\n=== RECEITA E TICKET MEDIO POR REGIAO ===")
    print(vendas_por_regiao.to_string(index=False))

    return metricas

    

def segmentar_clientes(df_vendas):
    """Agrupa os clientes e classifica por nível de gasto.

    Args:
        df_vendas: DataFrame com os dados de vendas transformados.

    Returns:
        DataFrame com o gasto total e o segmento de cada cliente.
    """
    """Agrupa os clientes e classifica por nível de gasto."""

    receita_por_cliente = (
        df_vendas.groupby("cliente")["receita_total"]
        .sum()
        .reset_index(name="total_gasto")
    )

    receita_por_cliente["segmento"] = receita_por_cliente[
        "total_gasto"
    ].apply(
        lambda receita: (
            "Bronze" if receita < 5000
            else "Prata" if receita <= 15000
            else "Ouro"
        )
    )

    clientes_top_10 = receita_por_cliente.sort_values(
        "total_gasto",
        ascending=False
    ).head(10)

    print("\n=== TOP 10 CLIENTES POR GASTO ===")
    print(clientes_top_10.to_string(index=False))

    print("\n=== DISTRIBUICAO DE CLIENTES POR SEGMENTO ===")
    print(receita_por_cliente["segmento"].value_counts())

    return receita_por_cliente


def gerar_graficos_vendas(df_vendas):
    """Gera e salva gráficos para a análise de vendas.

    Args:
        df_vendas: DataFrame com os dados de vendas transformados.

    Returns:
        None. Salva quatro gráficos no formato PNG.
    """
    os.makedirs("outputs/graficos", exist_ok=True)    
    plt.style.use("seaborn-v0_8-whitegrid")

    plt.rcParams.update({
        "figure.facecolor": "#F5F7FA",
        "axes.facecolor": "#FFFFFF",
        "axes.edgecolor": "#D9E2EC",
        "axes.labelcolor": "#344054",
        "text.color": "#1D2939",
        "xtick.color": "#475467",
        "ytick.color": "#475467",
        "axes.titleweight": "bold",
        "axes.titlesize": 13,
        "axes.labelsize": 10,
        "font.size": 10,
        "grid.color": "#E4E7EC",
        "grid.linestyle": "--",
        "grid.alpha": 0.7,
        "figure.titlesize": 18,
    })

    receita_mensal = (
        df_vendas.groupby(["ano", "mes", "mes_nome"])["receita_total"]
        .sum()
        .reset_index()
        .sort_values(["ano", "mes"])
    )

    plt.figure(figsize=(10, 5))

    plt.plot(
        receita_mensal["mes_nome"],
        receita_mensal["receita_total"],
        marker="o",
    )

    plt.title("Receita total por mes")
    plt.xlabel("Mes")
    plt.ylabel("Receita total")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
    "outputs/graficos/receita_por_mes.png",
    dpi=150
)
    plt.close()       
    
    top_produtos = (
        df_vendas.groupby("produto")["receita_total"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .sort_values()
    )
    plt.figure(figsize=(10, 5))

    plt.bar(
        top_produtos.index,
        top_produtos.values,
    )

    plt.title("Top 5 produtos por receita")
    plt.xlabel("Produto")
    plt.ylabel("Receita total")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
    "outputs/graficos/top_produtos.png",
    dpi=150
)
    plt.close()
    
    
    
    fig, ax = plt.subplots(figsize=(10, 5))


    categorias = df_vendas["categoria"].unique()
    cores = plt.cm.Set2.colors

    fig, ax = plt.subplots(figsize=(10, 5))

    for indice, categoria in enumerate(categorias):
        dados_categoria = df_vendas[
            df_vendas["categoria"] == categoria
        ]

        ax.scatter(
            dados_categoria["quantidade"],
            dados_categoria["receita_total"],
            color=cores[indice % len(cores)],
            label=categoria,
            alpha=0.8
        )

    ax.set_title("Quantidade versus receita total por categoria")
    ax.set_xlabel("Quantidade")
    ax.set_ylabel("Receita total")
    ax.legend(title="Categoria")

    fig.tight_layout()
    fig.savefig(
        "outputs/graficos/quantidade_vs_receita.png",
        dpi=150
    )
    plt.close(fig)


    
    vendas_por_regiao = (
    df_vendas.groupby("regiao")["receita_total"]
    .sum()
    .sort_values(ascending=False)
)
    
    fig, eixos = plt.subplots(2, 2, figsize=(14, 10))
    eixos[0, 1].bar(
        top_produtos.index,
        top_produtos.values,
    )
    
    eixos[0, 0].plot(
        receita_mensal["mes_nome"],
        receita_mensal["receita_total"],
        marker="o",
    )

    eixos[0, 0].set_title("Receita por mes")
    eixos[0, 0].set_xlabel("Mes")
    eixos[0, 0].set_ylabel("Receita total")
    eixos[0, 0].tick_params(axis="x", rotation=45)

    eixos[0, 1].set_title("Top 5 produtos por receita")
    eixos[0, 1].set_xlabel("Produto")
    eixos[0, 1].set_ylabel("Receita total")
    eixos[0, 1].tick_params(axis="x", rotation=45)


    eixos[1, 0].scatter(
        df_vendas["quantidade"],
        df_vendas["receita_total"],
    )

    eixos[1, 0].set_title("Quantidade versus receita")
    eixos[1, 0].set_xlabel("Quantidade")
    eixos[1, 0].set_ylabel("Receita total")
    

    eixos[1, 1].bar(
        vendas_por_regiao.index,
        vendas_por_regiao.values,
        color="#2A9D8F"
    )

    eixos[1, 1].set_title("Receita por regiao")
    eixos[1, 1].set_xlabel("Regiao")
    eixos[1, 1].set_ylabel("Receita total")
    eixos[1, 1].tick_params(axis="x", rotation=45)

    
    
    fig.suptitle("SalesInsight PY - Painel Resumo", fontsize=16)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig("outputs/graficos/painel_resumo.png", dpi=150)
    plt.close(fig)
        
if __name__ == "__main__":
    main()
    
   
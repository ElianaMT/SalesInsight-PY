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
   
    nome_saida = nome_saida or f"{coluna}_transformado"
    df[nome_saida] = df[coluna].apply(funcao_transformacao)
    return df


def exportar_resultados(metricas, clientes, estatisticas):
    
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


def main():
    print("SalesInsight PY - Análise de Dados de Vendas")

    df_vendas = gerar_dataset_vendas()

    print(df_vendas.head())
    print(f"\nQuantidade de registros: {len(df_vendas)}")

    df_vendas.to_csv(
        "vendas.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("\nDataset de vendas gerado com sucesso!")
    print("Arquivo gerado: vendas.csv")

    inspecionar_dados(df_vendas)
    
    df_vendas = limpar_dados_vendas(df_vendas)

    df_vendas = transformar_dados_vendas(df_vendas) 
    
    
    df_vendas = processar_coluna(
        df_vendas,
        "receita_total",
        lambda x: round(x / 1000, 2),
        nome_saida="receita_em_milhares",
    )

    df_vendas = processar_coluna(
        df_vendas,
        "quantidade",
        lambda q: "Alto Volume" if q > 5 else "Baixo Volume",
        nome_saida="perfil_volume",
    )
    
    
    print("\nReceita em milhares:")
    print(
        df_vendas[
            ["receita_total", "receita_em_milhares"]
        ].head()
    )

    print("\nPerfil de volume:")
    print(
        df_vendas[
            ["quantidade", "perfil_volume"]
        ].head()
    )



    print("\nReceita total por venda:")
    print(df_vendas[["id_venda", "quantidade", "preco_unitario", "receita_total"]].head())    
    df_vendas.to_csv(
        "vendas_limpo.csv",
        index=False,
        encoding="utf-8-sig",
    )
    
    print("\nNome do mes da venda:")
    print(df_vendas[["mes", "mes_nome"]].head())
    
    print("\nMes da venda:")
    print(df_vendas[["data_venda", "mes"]].head())
    
    print("\nTrimestre da venda:")
    print(df_vendas[["data_venda", "trimestre"]].head())
    
    print("\nAno da venda:")
    print(df_vendas[["data_venda", "ano"]].head())
    
    print("\nFaixa de receita por venda:")
    print(
        df_vendas[
            ["receita_total", "faixa_receita_item"]
        ].head()
    )
    
    metricas = calcular_metricas_vendas(df_vendas)
    clientes = segmentar_clientes(df_vendas)
    
    estatisticas = {
        "quantidade_vendas": len(df_vendas),
        "receita_total": df_vendas["receita_total"].sum(),
        "ticket_medio": df_vendas["receita_total"].mean(),
    }
    
    
    exportar_resultados(metricas, clientes, estatisticas)


    gerar_graficos_vendas(df_vendas)

    print("\nDados limpos exportados com sucesso!")
    print("Arquivo gerado: vendas_limpo.csv")
    
def inspecionar_dados(df_vendas):
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
    vendas_por_mes = (
        df_vendas.groupby(["ano", "mes", "mes_nome"])["receita_total"]
        .sum()
        .reset_index()
    )

    print("\nReceita total por mes:")
    print(vendas_por_mes)
    
    vendas_por_produto = (
        df_vendas.groupby("produto")["receita_total"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    print("\nTop 5 produtos por receita:")
    print(vendas_por_produto) 
    
    vendas_por_categoria = (
        df_vendas.groupby("categoria")["receita_total"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nReceita total por categoria:")
    print(vendas_por_categoria)
    
    vendas_por_regiao = (
            df_vendas.groupby("regiao")["receita_total"]
            .sum()
            .sort_values(ascending=False)
        )
    
    print("\nReceita total por regiao:")
    print(vendas_por_regiao)
    
    return {
        "por_mes": vendas_por_mes,
    }
    
def segmentar_clientes(df_vendas):

    receita_por_cliente = (
        df_vendas.groupby("cliente")["receita_total"]
        .sum()
        .reset_index()
    ) 
    
    receita_por_cliente["segmento"] = receita_por_cliente[
        "receita_total"
    ].apply(
        lambda receita: (
            "Bronze" if receita < 5000
            else "Prata" if receita <= 15000
            else "Ouro"
        )
    )


    print("\nSegmentacao de clientes:")
    print(receita_por_cliente)

    return receita_por_cliente

def gerar_graficos_vendas(df_vendas):
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

    plt.savefig("outputs/graficos/receita_por_mes.png")
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

    plt.savefig("outputs/graficos/top_produtos.png")
    plt.close()
    
    
    plt.figure(figsize=(10, 5))

    plt.scatter(
        df_vendas["quantidade"],
        df_vendas["receita_total"],
    )

    plt.title("Quantidade versus receita total")
    plt.xlabel("Quantidade")
    plt.ylabel("Receita total")
    plt.tight_layout()

    plt.savefig("outputs/graficos/quantidade_vs_receita.png")
    plt.close()
    
    vendas_por_categoria = (
        df_vendas.groupby("categoria")["receita_total"]
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
        vendas_por_categoria.index,
        vendas_por_categoria.values,
    )

    eixos[1, 1].set_title("Receita por categoria")
    eixos[1, 1].set_xlabel("Categoria")
    eixos[1, 1].set_ylabel("Receita total")
    
    
    fig.suptitle("SalesInsight PY - Painel Resumo", fontsize=16)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig("outputs/graficos/painel_resumo.png", dpi=150)
    plt.close(fig)
        
if __name__ == "__main__":
    main()
    
   
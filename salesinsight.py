"""
SalesInsight PY
Análise e Visualização de Dados de Vendas com Python.

Projeto avaliativo - Módulo 01 - Semana 07.
"""

import numpy as np
import pandas as pd


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


def main():
    print("SalesInsight PY - Análise de Dados de Vendas")

    df_vendas = gerar_dataset_vendas()  
    inspecionar_dados(df_vendas)
    
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

    print(df_vendas.head())
    print(f"\nQuantidade de registros: {len(df_vendas)}")
    
    df_vendas.to_csv(
        "vendas.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("\nDataset de vendas gerado com sucesso!")
    print("Arquivo gerado: vendas.csv")

    df_vendas.to_csv(
        "vendas.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("\nDataset de vendas gerado com sucesso!")
    print("Arquivo gerado: vendas.csv")


if __name__ == "__main__":
    main()
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
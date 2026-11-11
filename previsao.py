"""Previsao de geracao eolica por regressao linear simples.

Este modulo utiliza os dados historicos da colonia para relacionar:
- X: velocidade do vento, em m/s;
- y: geracao de energia eolica, em kW.

Bibliotecas utilizadas conforme o conteudo estudado:
Pandas, NumPy, Matplotlib e Scikit-learn.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from acesso import obter_valor
from dados import CAMINHOS


def organizar_dados_historicos(colonia):
    """Le os dados da colonia e devolve um DataFrame validado."""
    ventos = obter_valor(colonia, CAMINHOS["vento_ms"])
    geracoes = obter_valor(colonia, CAMINHOS["eolica_kw"])

    if ventos is None or geracoes is None:
        raise ValueError("Os dados historicos de vento ou geracao nao foram encontrados.")

    if len(ventos) != len(geracoes):
        raise ValueError("As listas de vento e geracao precisam ter o mesmo tamanho.")

    if len(ventos) < 2:
        raise ValueError("Sao necessarios pelo menos dois registros historicos.")

    dados = {
        "vento_ms": ventos,
        "geracao_eolica_kw": geracoes,
    }
    df = pd.DataFrame(dados)

    if df.isnull().values.any():
        raise ValueError("Os dados historicos nao podem conter valores vazios.")

    for coluna in df.columns:
        if not pd.api.types.is_numeric_dtype(df[coluna]):
            raise TypeError("Os dados de vento e geracao precisam ser numericos.")

    if df["vento_ms"].nunique() < 2:
        raise ValueError("Os valores de vento precisam apresentar variacao.")

    return df


def treinar_modelo(colonia):
    """Treina a regressao linear e calcula previsoes, residuos e metricas."""
    df = organizar_dados_historicos(colonia)

    # O Scikit-learn espera X em formato bidimensional.
    X = df[["vento_ms"]]
    y = df["geracao_eolica_kw"]

    modelo = LinearRegression()
    modelo.fit(X, y)

    y_pred = modelo.predict(X)
    residuos = y.to_numpy() - y_pred

    return {
        "modelo": modelo,
        "dados": df,
        "X": X,
        "y": y,
        "y_pred": y_pred,
        "residuos": residuos,
        "intercepto": float(modelo.intercept_),
        "inclinacao": float(modelo.coef_[0]),
        "mse": float(mean_squared_error(y, y_pred)),
        "r2": float(r2_score(y, y_pred)),
    }


def prever_geracao_eolica(colonia, vento_ms):
    """Estima a geracao eolica para uma nova velocidade do vento."""
    tipos_numericos = (int, float, np.integer, np.floating)

    if isinstance(vento_ms, bool) or not isinstance(vento_ms, tipos_numericos):
        raise TypeError("A velocidade do vento precisa ser numerica.")

    if not np.isfinite(vento_ms):
        raise ValueError("A velocidade do vento precisa ser um numero finito.")

    if vento_ms < 0:
        raise ValueError("A velocidade do vento nao pode ser negativa.")

    resultados = treinar_modelo(colonia)
    novo_dado = pd.DataFrame({"vento_ms": [float(vento_ms)]})
    geracao_prevista = float(resultados["modelo"].predict(novo_dado)[0])

    # Uma geracao negativa nao faz sentido fisico.
    geracao_prevista = max(0.0, geracao_prevista)

    return {
        "vento_ms": float(vento_ms),
        "geracao_prevista_kw": geracao_prevista,
        "intercepto": resultados["intercepto"],
        "inclinacao": resultados["inclinacao"],
        "mse": resultados["mse"],
        "r2": resultados["r2"],
    }


def gerar_graficos(colonia, pasta_saida="."):
    """Gera e salva os graficos da regressao e dos residuos."""
    resultados = treinar_modelo(colonia)
    dados_ordenados = resultados["dados"].sort_values("vento_ms")

    X_ordenado = dados_ordenados[["vento_ms"]]
    y_pred_ordenado = resultados["modelo"].predict(X_ordenado)

    pasta = Path(pasta_saida)
    pasta.mkdir(parents=True, exist_ok=True)

    caminho_regressao = pasta / "grafico_regressao_eolica.png"
    caminho_residuos = pasta / "grafico_residuos_eolica.png"

    plt.figure(figsize=(8, 5))
    plt.scatter(
        resultados["X"]["vento_ms"],
        resultados["y"],
        color="blue",
        label="Valores observados",
    )
    plt.plot(
        X_ordenado["vento_ms"],
        y_pred_ordenado,
        color="red",
        label="Ajuste linear",
    )
    plt.xlabel("Velocidade do vento (m/s)")
    plt.ylabel("Geracao eolica (kW)")
    plt.title("Regressao linear da geracao eolica")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(caminho_regressao, dpi=300)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.scatter(
        resultados["y_pred"],
        resultados["residuos"],
        color="blue",
    )
    plt.axhline(y=0, color="red", linestyle="--")
    plt.xlabel("Valores preditos (kW)")
    plt.ylabel("Residuos (kW)")
    plt.title("Analise dos residuos")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(caminho_residuos, dpi=300)
    plt.close()

    return str(caminho_regressao), str(caminho_residuos)


if __name__ == "__main__":
    from dados import COLONIA

    resultado = prever_geracao_eolica(COLONIA, 14)
    grafico_regressao, grafico_residuos = gerar_graficos(COLONIA)

    print("=== PREVISAO DE ENERGIA EOLICA ===")
    print(f"Equacao: y = {resultado['intercepto']:.4f} + {resultado['inclinacao']:.4f}x")
    print(f"MSE: {resultado['mse']:.4f}")
    print(f"R2: {resultado['r2']:.4f}")
    print(f"Vento informado: {resultado['vento_ms']:.2f} m/s")
    print(f"Geracao prevista: {resultado['geracao_prevista_kw']:.2f} kW")
    print(f"Grafico da regressao: {grafico_regressao}")
    print(f"Grafico dos residuos: {grafico_residuos}")

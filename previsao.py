"""Previsao de energia solar e eolica por regressao linear simples.

Modelos utilizados:
- Eolico: velocidade do vento (m/s) -> geracao eolica (kW)
- Solar: horario do dia -> geracao solar (kW)

O modulo utiliza Pandas, NumPy, Matplotlib e Scikit-learn, conforme o
conteudo estudado no curso. Os dados historicos continuam centralizados
em dados.py e sao lidos por meio de acesso.py.
"""

from pathlib import Path

import matplotlib

# Permite salvar graficos mesmo em ambientes sem interface grafica.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from acesso import obter_valor
from dados import CAMINHOS


def converter_horario_para_numero(horario):
    """Converte um horario no formato HH:MM para uma hora decimal.

    Exemplos:
        06:00 -> 6.0
        13:30 -> 13.5
    """
    if not isinstance(horario, str):
        raise TypeError("O horario precisa ser um texto no formato HH:MM.")

    partes = horario.split(":")

    if len(partes) != 2:
        raise ValueError("O horario precisa estar no formato HH:MM.")

    try:
        hora = int(partes[0])
        minuto = int(partes[1])
    except ValueError as erro:
        raise ValueError("O horario precisa estar no formato HH:MM.") from erro

    if not 0 <= hora <= 23:
        raise ValueError("A hora precisa estar entre 00 e 23.")

    if not 0 <= minuto <= 59:
        raise ValueError("Os minutos precisam estar entre 00 e 59.")

    return hora + minuto / 60


def _validar_series(entradas, geracoes, nome_entrada):
    """Realiza validacoes comuns aos dados solar e eolico."""
    if entradas is None or geracoes is None:
        raise ValueError("Os dados historicos necessarios nao foram encontrados.")

    if len(entradas) != len(geracoes):
        raise ValueError("As listas historicas precisam ter o mesmo tamanho.")

    if len(entradas) < 2:
        raise ValueError("Sao necessarios pelo menos dois registros historicos.")

    df_validacao = pd.DataFrame(
        {
            nome_entrada: entradas,
            "geracao_kw": geracoes,
        }
    )

    if df_validacao.isnull().values.any():
        raise ValueError("Os dados historicos nao podem conter valores vazios.")

    for coluna in df_validacao.columns:
        if not pd.api.types.is_numeric_dtype(df_validacao[coluna]):
            raise TypeError("Os dados historicos precisam ser numericos.")

    if df_validacao[nome_entrada].nunique() < 2:
        raise ValueError("A variavel de entrada precisa apresentar variacao.")


def organizar_dados_eolicos(colonia):
    """Organiza vento e geracao eolica em um DataFrame."""
    ventos = obter_valor(colonia, CAMINHOS["vento_ms"])
    geracoes = obter_valor(colonia, CAMINHOS["eolica_kw"])

    _validar_series(ventos, geracoes, "vento_ms")

    return pd.DataFrame(
        {
            "vento_ms": ventos,
            "geracao_eolica_kw": geracoes,
        }
    )


def organizar_dados_solares(colonia):
    """Organiza horarios e geracao solar em um DataFrame."""
    horarios = colonia.get("horarios")
    geracoes = obter_valor(colonia, CAMINHOS["solar_kw"])

    if horarios is None:
        raise ValueError("A lista de horarios nao foi encontrada na colonia.")

    horas_numericas = [
        converter_horario_para_numero(horario)
        for horario in horarios
    ]

    _validar_series(horas_numericas, geracoes, "hora_numerica")

    return pd.DataFrame(
        {
            "horario": horarios,
            "hora_numerica": horas_numericas,
            "geracao_solar_kw": geracoes,
        }
    )


def _treinar_regressao(df, coluna_entrada, coluna_saida):
    """Treina uma regressao linear e calcula previsoes e metricas."""
    X = df[[coluna_entrada]]
    y = df[coluna_saida]

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


def treinar_modelo_eolico(colonia):
    """Treina a regressao da geracao eolica em funcao do vento."""
    df = organizar_dados_eolicos(colonia)
    return _treinar_regressao(df, "vento_ms", "geracao_eolica_kw")


def treinar_modelo_solar(colonia):
    """Treina a regressao da geracao solar em funcao do horario."""
    df = organizar_dados_solares(colonia)
    return _treinar_regressao(df, "hora_numerica", "geracao_solar_kw")


def _validar_numero_nao_negativo(valor, nome):
    """Valida um valor numerico finito e nao negativo."""
    tipos_numericos = (int, float, np.integer, np.floating)

    if isinstance(valor, bool) or not isinstance(valor, tipos_numericos):
        raise TypeError(f"{nome} precisa ser numerico.")

    if not np.isfinite(valor):
        raise ValueError(f"{nome} precisa ser um numero finito.")

    if valor < 0:
        raise ValueError(f"{nome} nao pode ser negativo.")


def _obter_capacidade(colonia, subsistema):
    """Le a capacidade maxima cadastrada para solar ou eolico."""
    try:
        capacidade = colonia["sistemas"]["energetico"]["subsistemas"][
            subsistema
        ]["capacidade_kw"]
    except KeyError as erro:
        raise ValueError(
            f"A capacidade do subsistema {subsistema} nao foi encontrada."
        ) from erro

    _validar_numero_nao_negativo(capacidade, "A capacidade")
    return float(capacidade)


def prever_geracao_eolica(colonia, vento_ms):
    """Estima a geracao eolica para uma nova velocidade do vento."""
    _validar_numero_nao_negativo(vento_ms, "A velocidade do vento")

    resultados = treinar_modelo_eolico(colonia)
    novo_dado = pd.DataFrame({"vento_ms": [float(vento_ms)]})
    previsao_bruta = float(resultados["modelo"].predict(novo_dado)[0])
    capacidade = _obter_capacidade(colonia, "eolico")
    previsao_limitada = min(max(0.0, previsao_bruta), capacidade)

    return {
        "fonte": "eolica",
        "vento_ms": float(vento_ms),
        "geracao_prevista_kw": previsao_limitada,
        "geracao_prevista_bruta_kw": previsao_bruta,
        "capacidade_kw": capacidade,
        "intercepto": resultados["intercepto"],
        "inclinacao": resultados["inclinacao"],
        "mse": resultados["mse"],
        "r2": resultados["r2"],
    }


def prever_geracao_solar(colonia, horario):
    """Estima a geracao solar para um novo horario."""
    hora_numerica = converter_horario_para_numero(horario)
    resultados = treinar_modelo_solar(colonia)
    novo_dado = pd.DataFrame({"hora_numerica": [hora_numerica]})
    previsao_bruta = float(resultados["modelo"].predict(novo_dado)[0])
    capacidade = _obter_capacidade(colonia, "solar")
    previsao_limitada = min(max(0.0, previsao_bruta), capacidade)

    return {
        "fonte": "solar",
        "horario": horario,
        "hora_numerica": hora_numerica,
        "geracao_prevista_kw": previsao_limitada,
        "geracao_prevista_bruta_kw": previsao_bruta,
        "capacidade_kw": capacidade,
        "intercepto": resultados["intercepto"],
        "inclinacao": resultados["inclinacao"],
        "mse": resultados["mse"],
        "r2": resultados["r2"],
    }


def _gerar_graficos_modelo(
    resultados,
    coluna_entrada,
    rotulo_x,
    titulo_fonte,
    cor,
    caminho_regressao,
    caminho_residuos,
):
    """Cria os graficos de ajuste linear e residuos de um modelo."""
    dados_ordenados = resultados["dados"].sort_values(coluna_entrada)
    X_ordenado = dados_ordenados[[coluna_entrada]]
    y_pred_ordenado = resultados["modelo"].predict(X_ordenado)

    plt.figure(figsize=(8, 5))
    plt.scatter(
        resultados["X"][coluna_entrada],
        resultados["y"],
        color=cor,
        label="Valores observados",
    )
    plt.plot(
        X_ordenado[coluna_entrada],
        y_pred_ordenado,
        color="red",
        label="Ajuste linear",
    )
    plt.xlabel(rotulo_x)
    plt.ylabel("Geracao de energia (kW)")
    plt.title(f"Regressao linear da geracao {titulo_fonte}")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(caminho_regressao, dpi=300)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.scatter(resultados["y_pred"], resultados["residuos"], color=cor)
    plt.axhline(y=0, color="red", linestyle="--")
    plt.xlabel("Valores preditos (kW)")
    plt.ylabel("Residuos (kW)")
    plt.title(f"Analise dos residuos da geracao {titulo_fonte}")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(caminho_residuos, dpi=300)
    plt.close()


def gerar_graficos(colonia, pasta_saida="."):
    """Gera os graficos dos modelos eolico e solar."""
    pasta = Path(pasta_saida)
    pasta.mkdir(parents=True, exist_ok=True)

    caminhos = {
        "regressao_eolica": pasta / "grafico_regressao_eolica.png",
        "residuos_eolicos": pasta / "grafico_residuos_eolicos.png",
        "regressao_solar": pasta / "grafico_regressao_solar.png",
        "residuos_solares": pasta / "grafico_residuos_solares.png",
    }

    _gerar_graficos_modelo(
        treinar_modelo_eolico(colonia),
        "vento_ms",
        "Velocidade do vento (m/s)",
        "eolica",
        "blue",
        caminhos["regressao_eolica"],
        caminhos["residuos_eolicos"],
    )

    _gerar_graficos_modelo(
        treinar_modelo_solar(colonia),
        "hora_numerica",
        "Horario do dia (hora decimal)",
        "solar",
        "orange",
        caminhos["regressao_solar"],
        caminhos["residuos_solares"],
    )

    return {nome: str(caminho) for nome, caminho in caminhos.items()}


if __name__ == "__main__":
    from dados import COLONIA

    resultado_eolico = prever_geracao_eolica(COLONIA, 14)
    resultado_solar = prever_geracao_solar(COLONIA, "14:00")
    caminhos_graficos = gerar_graficos(COLONIA)

    print("=== PREVISAO EOLICA ===")
    print(
        f"Equacao: y = {resultado_eolico['intercepto']:.4f} "
        f"+ {resultado_eolico['inclinacao']:.4f}x"
    )
    print(f"MSE: {resultado_eolico['mse']:.4f}")
    print(f"R2: {resultado_eolico['r2']:.4f}")
    print(f"Vento: {resultado_eolico['vento_ms']:.2f} m/s")
    print(f"Geracao prevista: {resultado_eolico['geracao_prevista_kw']:.2f} kW")

    print("\n=== PREVISAO SOLAR ===")
    print(
        f"Equacao: y = {resultado_solar['intercepto']:.4f} "
        f"+ {resultado_solar['inclinacao']:.4f}x"
    )
    print(f"MSE: {resultado_solar['mse']:.4f}")
    print(f"R2: {resultado_solar['r2']:.4f}")
    print(f"Horario: {resultado_solar['horario']}")
    print(f"Previsao bruta: {resultado_solar['geracao_prevista_bruta_kw']:.2f} kW")
    print(f"Geracao limitada: {resultado_solar['geracao_prevista_kw']:.2f} kW")

    print("\n=== GRAFICOS GERADOS ===")
    for nome, caminho in caminhos_graficos.items():
        print(f"{nome}: {caminho}")

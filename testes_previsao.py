"""Testes da previsao de energia eolica.

Os testes usam assert, conforme uma abordagem simples e adequada
para verificar os resultados principais do projeto.
"""

import math
import tempfile
from pathlib import Path

from dados import COLONIA
from previsao import (
    gerar_graficos,
    organizar_dados_historicos,
    prever_geracao_eolica,
    treinar_modelo,
)


# Teste 1: organizacao dos dados historicos.
df = organizar_dados_historicos(COLONIA)

assert len(df) == 8
assert list(df.columns) == ["vento_ms", "geracao_eolica_kw"]
assert df.iloc[0]["vento_ms"] == 8
assert df.iloc[0]["geracao_eolica_kw"] == 20


# Teste 2: coeficientes e metricas do modelo.
resultado_modelo = treinar_modelo(COLONIA)

assert math.isclose(
    resultado_modelo["intercepto"],
    -1.0314465409,
    abs_tol=1e-9,
)
assert math.isclose(
    resultado_modelo["inclinacao"],
    2.5911949686,
    abs_tol=1e-9,
)
assert math.isclose(
    resultado_modelo["mse"],
    0.0691823899,
    abs_tol=1e-9,
)
assert math.isclose(
    resultado_modelo["r2"],
    0.9958697081,
    abs_tol=1e-9,
)
assert len(resultado_modelo["residuos"]) == 8


# Teste 3: previsao para um novo valor de vento.
previsao = prever_geracao_eolica(COLONIA, 14)

assert math.isclose(
    previsao["geracao_prevista_kw"],
    35.2452830189,
    abs_tol=1e-9,
)


# Teste 4: validacao de entradas incorretas.
entradas_invalidas = [
    (-1, ValueError),
    ("14", TypeError),
    (True, TypeError),
    (float("nan"), ValueError),
    (float("inf"), ValueError),
]

for entrada, erro_esperado in entradas_invalidas:
    try:
        prever_geracao_eolica(COLONIA, entrada)
        raise AssertionError(f"Entrada invalida aceita: {entrada!r}")
    except erro_esperado:
        pass


# Teste 5: criacao dos dois graficos.
with tempfile.TemporaryDirectory() as pasta_temporaria:
    caminho_regressao, caminho_residuos = gerar_graficos(
        COLONIA,
        pasta_temporaria,
    )

    assert Path(caminho_regressao).is_file()
    assert Path(caminho_residuos).is_file()
    assert Path(caminho_regressao).stat().st_size > 0
    assert Path(caminho_residuos).stat().st_size > 0


print("OK: todos os testes de previsao passaram.")

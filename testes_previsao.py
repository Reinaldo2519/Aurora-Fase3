"""Testes dos modelos de previsao eolica e solar."""

import math
import tempfile
from pathlib import Path

from dados import COLONIA
from previsao import (
    converter_horario_para_numero,
    gerar_graficos,
    organizar_dados_eolicos,
    organizar_dados_solares,
    prever_geracao_eolica,
    prever_geracao_solar,
    treinar_modelo_eolico,
    treinar_modelo_solar,
)


# 1. Conversao de horarios
assert converter_horario_para_numero("06:00") == 6.0
assert converter_horario_para_numero("13:30") == 13.5


# 2. Organizacao dos dados eolicos
df_eolico = organizar_dados_eolicos(COLONIA)
assert len(df_eolico) == 8
assert list(df_eolico.columns) == ["vento_ms", "geracao_eolica_kw"]
assert df_eolico.iloc[0]["vento_ms"] == 8
assert df_eolico.iloc[0]["geracao_eolica_kw"] == 20


# 3. Organizacao dos dados solares
df_solar = organizar_dados_solares(COLONIA)
assert len(df_solar) == 8
assert list(df_solar.columns) == [
    "horario",
    "hora_numerica",
    "geracao_solar_kw",
]
assert df_solar.iloc[0]["horario"] == "06:00"
assert df_solar.iloc[0]["hora_numerica"] == 6.0
assert df_solar.iloc[0]["geracao_solar_kw"] == 5


# 4. Coeficientes e metricas do modelo eolico
modelo_eolico = treinar_modelo_eolico(COLONIA)
assert math.isclose(modelo_eolico["intercepto"], -1.0314465409, abs_tol=1e-9)
assert math.isclose(modelo_eolico["inclinacao"], 2.5911949686, abs_tol=1e-9)
assert math.isclose(modelo_eolico["mse"], 0.0691823899, abs_tol=1e-9)
assert math.isclose(modelo_eolico["r2"], 0.9958697081, abs_tol=1e-9)
assert len(modelo_eolico["residuos"]) == 8


# 5. Coeficientes e metricas do modelo solar
modelo_solar = treinar_modelo_solar(COLONIA)
assert math.isclose(modelo_solar["intercepto"], -34.3333333333, abs_tol=1e-9)
assert math.isclose(modelo_solar["inclinacao"], 7.4166666667, abs_tol=1e-9)
assert math.isclose(modelo_solar["mse"], 28.5729166667, abs_tol=1e-9)
assert math.isclose(modelo_solar["r2"], 0.9099666847, abs_tol=1e-9)
assert len(modelo_solar["residuos"]) == 8


# 6. Previsao eolica para 14 m/s
previsao_eolica = prever_geracao_eolica(COLONIA, 14)
assert math.isclose(
    previsao_eolica["geracao_prevista_bruta_kw"],
    35.2452830189,
    abs_tol=1e-9,
)
assert math.isclose(
    previsao_eolica["geracao_prevista_kw"],
    35.2452830189,
    abs_tol=1e-9,
)
assert previsao_eolica["capacidade_kw"] == 40.0


# 7. Previsao solar para 14:00
previsao_solar = prever_geracao_solar(COLONIA, "14:00")
assert math.isclose(
    previsao_solar["geracao_prevista_bruta_kw"],
    69.5,
    abs_tol=1e-9,
)
# A previsao final respeita a capacidade solar cadastrada de 60 kW.
assert previsao_solar["geracao_prevista_kw"] == 60.0
assert previsao_solar["capacidade_kw"] == 60.0


# 8. Validacao de entradas eolicas incorretas
entradas_eolicas_invalidas = [
    (-1, ValueError),
    ("14", TypeError),
    (True, TypeError),
    (float("nan"), ValueError),
    (float("inf"), ValueError),
]

for entrada, erro_esperado in entradas_eolicas_invalidas:
    try:
        prever_geracao_eolica(COLONIA, entrada)
        raise AssertionError(f"Entrada eolica invalida aceita: {entrada!r}")
    except erro_esperado:
        pass


# 9. Validacao de horarios incorretos
horarios_invalidos = [
    (14, TypeError),
    ("14", ValueError),
    ("24:00", ValueError),
    ("12:60", ValueError),
    ("meio-dia", ValueError),
]

for horario, erro_esperado in horarios_invalidos:
    try:
        prever_geracao_solar(COLONIA, horario)
        raise AssertionError(f"Horario invalido aceito: {horario!r}")
    except erro_esperado:
        pass


# 10. Criacao dos quatro graficos
with tempfile.TemporaryDirectory() as pasta_temporaria:
    caminhos = gerar_graficos(COLONIA, pasta_temporaria)

    assert set(caminhos) == {
        "regressao_eolica",
        "residuos_eolicos",
        "regressao_solar",
        "residuos_solares",
    }

    for caminho in caminhos.values():
        assert Path(caminho).is_file()
        assert Path(caminho).stat().st_size > 0


print("OK: todos os testes de previsao eolica e solar passaram.")


from acesso import leitura_atual, obter_subsistema


def analisar_energia(geracao_kw, consumo_kw, reserva_kwh, capacidade_kwh,
                     intervalo_horas=1):
    """Devolve balanço, déficit, excedente e reserva projetada em um dicionario."""
    valores = (geracao_kw, consumo_kw, reserva_kwh, capacidade_kwh, intervalo_horas)
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in valores):
        raise TypeError("Todos os valores devem ser numericos.")
    if any(v < 0 for v in valores) or intervalo_horas == 0:
        raise ValueError("Valores nao podem ser negativos; intervalo deve ser positivo.")
    if reserva_kwh > capacidade_kwh:
        raise ValueError("A reserva nao pode exceder a capacidade da bateria.")

    saldo_kw = geracao_kw - consumo_kw
    saldo_kwh = saldo_kw * intervalo_horas
    deficit_kwh = max(0, -saldo_kwh)
    excedente_kwh = max(0, saldo_kwh)
    energia_retirada_kwh = min(deficit_kwh, reserva_kwh)
    energia_armazenada_kwh = min(excedente_kwh, capacidade_kwh - reserva_kwh)
    deficit_nao_coberto_kwh = deficit_kwh - energia_retirada_kwh
    excedente_nao_armazenado_kwh = excedente_kwh - energia_armazenada_kwh
    reserva_projetada_kwh = reserva_kwh - energia_retirada_kwh + energia_armazenada_kwh

    if saldo_kw < 0:
        situacao = "DEFICIT"
    elif saldo_kw > 0:
        situacao = "EXCEDENTE"
    else:
        situacao = "EQUILIBRIO"

    return {
        "geracao_kw": geracao_kw,
        "consumo_kw": consumo_kw,
        "reserva_inicial_kwh": reserva_kwh,
        "capacidade_kwh": capacidade_kwh,
        "intervalo_horas": intervalo_horas,
        "saldo_kw": saldo_kw,
        "saldo_kwh": saldo_kwh,
        "situacao": situacao,
        "deficit_kwh": deficit_kwh,
        "excedente_kwh": excedente_kwh,
        "energia_retirada_kwh": energia_retirada_kwh,
        "energia_armazenada_kwh": energia_armazenada_kwh,
        "deficit_nao_coberto_kwh": deficit_nao_coberto_kwh,
        "excedente_nao_armazenado_kwh": excedente_nao_armazenado_kwh,
        "reserva_projetada_kwh": reserva_projetada_kwh,
    }


def analisar_leitura_colonia(colonia, indice=-1, intervalo_horas=1):
    """Usa dados.py/acesso.py para analisar uma leitura sem duplicar os dados."""
    leitura = leitura_atual(colonia, indice)
    bateria = obter_subsistema(colonia, "energetico", "reserva")
    resultado = analisar_energia(
        leitura["geracao_kw"],
        leitura["consumo_kw"],
        leitura["reserva_kwh"],
        bateria["capacidade_kwh"],
        intervalo_horas,
    )
    resultado["horario_base"] = leitura["horario"]
    return resultado


if __name__ == "__main__":
    from dados import COLONIA
    resultado = analisar_leitura_colonia(COLONIA)
    print("=== ANALISE ENERGETICA - AURORA SIGER ===")
    for chave, valor in resultado.items():
        print(f"{chave}: {valor}")

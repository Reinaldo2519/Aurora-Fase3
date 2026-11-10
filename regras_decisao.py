
"""Fase 3 - Aurora | Parte 2: regras de decisao e prioridades.

Geracao e consumo sao potencias em kW; reserva e energia em kWh.
O deficit em kW e convertido para kWh usando o intervalo analisado.
Os limites de consumo (kW) e reserva (kWh) sao exemplos ajustaveis.
"""


def avaliar_colonia(
    geracao,
    consumo,
    reserva,
    limite_consumo_alto=70,
    limite_reserva_baixa=20,
    intervalo_horas=1,
    sistemas_essenciais=None,
    sistemas_nao_essenciais=None,
):
    """Classifica a situacao e devolve alertas e acoes recomendadas.

    geracao e consumo: kW; reserva: kWh; intervalo_horas: horas.
    Nao altera os dados de entrada e nao desliga equipamentos de verdade.
    """
    valores = {
        "geracao": geracao,
        "consumo": consumo,
        "reserva": reserva,
        "limite_consumo_alto": limite_consumo_alto,
        "limite_reserva_baixa": limite_reserva_baixa,
        "intervalo_horas": intervalo_horas,
    }

    for nome, valor in valores.items():
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError(f"{nome} deve ser um numero.")
        if valor < 0:
            raise ValueError(f"{nome} nao pode ser negativo.")

    if limite_consumo_alto == 0:
        raise ValueError("limite_consumo_alto deve ser maior que zero.")
    if intervalo_horas == 0:
        raise ValueError("intervalo_horas deve ser maior que zero.")

    # Valores padrao para testes isolados. Na integracao com a Parte 1,
    # as listas sao obtidas automaticamente dos dados do projeto.
    if sistemas_essenciais is None:
        sistemas_essenciais = ["Suporte à vida", "Habitação", "Comunicação"]
    if sistemas_nao_essenciais is None:
        sistemas_nao_essenciais = ["Produção ISRU", "Laboratório"]

    # A potencia faltante em kW equivale a deficit_kw * horas em kWh.
    deficit_kw = max(0, consumo - geracao)
    deficit_kwh = deficit_kw * intervalo_horas
    consumo_alto = consumo >= limite_consumo_alto
    reserva_baixa = reserva < limite_reserva_baixa

    alertas = []
    recomendacoes = []

    # Regra 1: a reserva acabaria (ou nao seria suficiente) no intervalo.
    if deficit_kwh > 0 and deficit_kwh >= reserva:
        nivel = "CRITICO"
        modo = "emergencia"
        alertas.append("Deficit critico: geracao e reserva nao oferecem margem de seguranca.")
        recomendacoes.append("Priorizar a energia dos sistemas essenciais.")
        recomendacoes.append("Desligar temporariamente os sistemas nao essenciais.")
        recomendacoes.append("Buscar geracao adicional e reduzir o consumo urgente.")

    # Regra 2: deficit coberto pela reserva, ou dois indicadores ruins.
    elif deficit_kwh > 0 or (consumo_alto and reserva_baixa):
        nivel = "ALERTA"
        modo = "economia"
        if deficit_kwh > 0:
            alertas.append("Consumo maior que a geracao: parte da reserva sera necessaria.")
        recomendacoes.append("Reduzir o uso dos sistemas nao essenciais.")
        recomendacoes.append("Monitorar a reserva de energia.")

    # Regra 3: apenas um indicador exige atencao.
    elif consumo_alto or reserva_baixa:
        nivel = "ATENCAO"
        modo = "monitoramento"
        recomendacoes.append("Acompanhar consumo e reserva com maior frequencia.")

    else:
        nivel = "NORMAL"
        modo = "normal"
        recomendacoes.append("Manter a operacao normal e continuar o monitoramento.")

    if consumo_alto:
        alertas.append("Consumo elevado em relacao ao limite configurado.")
    if reserva_baixa:
        alertas.append("Reserva de energia abaixo do limite configurado.")

    return {
        "nivel": nivel,
        "modo": modo,
        "deficit": deficit_kw,  # Mantido para compatibilidade: kW
        "deficit_kw": deficit_kw,
        "deficit_kwh": deficit_kwh,
        "alertas": alertas,
        "recomendacoes": recomendacoes,
        "sistemas_prioritarios": list(sistemas_essenciais),
        "sistemas_reduzir": list(sistemas_nao_essenciais) if modo == "economia" else [],
        "sistemas_desligar": list(sistemas_nao_essenciais) if modo == "emergencia" else [],
    }


def avaliar_leitura_colonia(colonia, indice=-1, intervalo_horas=1):
    """Conecta as regras aos dados e prioridades definidos na Parte 1.

    Por padrao utiliza a ultima leitura e avalia um intervalo futuro de 1h
    mantendo as potencias atuais. Nao modifica a colonia.
    """
    from acesso import (
        leitura_atual,
        modulos_por_prioridade,
        modulos_nao_essenciais,
        obter_subsistema,
    )

    leitura = leitura_atual(colonia, indice)
    essenciais = []

    for nome in modulos_por_prioridade(colonia):
        modulo = obter_subsistema(colonia, "operacional", nome)
        if modulo["essencial"]:
            essenciais.append(nome)

    return avaliar_colonia(
        geracao=leitura["geracao_kw"],
        consumo=leitura["consumo_kw"],
        reserva=leitura["reserva_kwh"],
        intervalo_horas=intervalo_horas,
        sistemas_essenciais=essenciais,
        sistemas_nao_essenciais=modulos_nao_essenciais(colonia),
    )


if __name__ == "__main__":
    from dados import COLONIA
    from acesso import leitura_atual

    leitura = leitura_atual(COLONIA)
    resultado = avaliar_leitura_colonia(COLONIA)

    print("=== SISTEMA AURORA - REGRAS DE DECISAO ===")
    print("Horario:", leitura["horario"])
    print("Geracao:", leitura["geracao_kw"], "kW")
    print("Consumo:", leitura["consumo_kw"], "kW")
    print("Reserva:", leitura["reserva_kwh"], "kWh")
    print("Nivel:", resultado["nivel"])
    print("Modo:", resultado["modo"])
    print("Deficit:", resultado["deficit_kw"], "kW")

    print("Alertas:")
    for mensagem in resultado["alertas"]:
        print(" -", mensagem)

    print("Recomendacoes:")
    for mensagem in resultado["recomendacoes"]:
        print(" -", mensagem)

    print("Sistemas prioritarios:", ", ".join(resultado["sistemas_prioritarios"]))
    print("Sistemas para reduzir:", resultado["sistemas_reduzir"])
    print("Sistemas para desligar:", resultado["sistemas_desligar"])

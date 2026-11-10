"""Fase 3 - Aurora | Parte 2: regras de decisão e prioridades.

Todos os valores de energia devem usar a mesma unidade e o mesmo período
(por exemplo, kWh por dia). Os limites são exemplos ajustáveis pelo grupo.
"""


def avaliar_colonia(geracao, consumo, reserva,
                   limite_consumo_alto=70, limite_reserva_baixa=20):
    """Recebe dados energéticos e devolve alertas, modo e ações prioritárias.

    A função não altera os dados recebidos e pode ser integrada aos demais módulos.
    """
    valores = {
        "geracao": geracao,
        "consumo": consumo,
        "reserva": reserva,
        "limite_consumo_alto": limite_consumo_alto,
        "limite_reserva_baixa": limite_reserva_baixa,
    }
    for nome, valor in valores.items():
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError(f"{nome} deve ser um número.")
        if valor < 0:
            raise ValueError(f"{nome} não pode ser negativo.")

    if limite_consumo_alto == 0:
        raise ValueError("limite_consumo_alto deve ser maior que zero.")

    deficit = max(0, consumo - geracao)
    consumo_alto = consumo >= limite_consumo_alto
    reserva_baixa = reserva < limite_reserva_baixa

    sistemas_essenciais = ["Suporte à vida", "Controle térmico", "Comunicação"]
    sistemas_nao_essenciais = ["Iluminação externa", "Laboratório", "Lazer"]

    alertas = []
    recomendacoes = []

    # Regra 1: há falta de energia, mesmo utilizando toda a reserva,
    # ou a reserva seria totalmente esgotada ao cobrir o déficit.
    if deficit > 0 and deficit >= reserva:
        nivel = "CRITICO"
        modo = "emergencia"
        alertas.append("Déficit crítico: geração e reserva não oferecem margem de segurança.")
        recomendacoes.append("Priorizar a energia dos sistemas essenciais.")
        recomendacoes.append("Desligar temporariamente os sistemas não essenciais.")
        recomendacoes.append("Buscar geração adicional e reduzir o consumo urgente.")

    # Regra 2: existe déficit coberto pela reserva, ou consumo alto
    # combinado com reserva baixa.
    elif deficit > 0 or (consumo_alto and reserva_baixa):
        nivel = "ALERTA"
        modo = "economia"
        if deficit > 0:
            alertas.append("Consumo maior que a geração: parte da reserva será necessária.")
        recomendacoes.append("Reduzir o uso dos sistemas não essenciais.")
        recomendacoes.append("Monitorar a reserva de energia.")

    # Regra 3: apenas um dos indicadores requer atenção.
    elif consumo_alto or reserva_baixa:
        nivel = "ATENCAO"
        modo = "monitoramento"
        recomendacoes.append("Acompanhar consumo e reserva com maior frequência.")

    else:
        nivel = "NORMAL"
        modo = "normal"
        recomendacoes.append("Manter a operação normal e continuar o monitoramento.")

    if consumo_alto:
        alertas.append("Consumo elevado em relação ao limite configurado.")
    if reserva_baixa:
        alertas.append("Reserva de energia abaixo do limite configurado.")

    return {
        "nivel": nivel,
        "modo": modo,
        "deficit": deficit,
        "alertas": alertas,
        "recomendacoes": recomendacoes,
        "sistemas_prioritarios": sistemas_essenciais,
        "sistemas_reduzir": sistemas_nao_essenciais if modo == "economia" else [],
        "sistemas_desligar": sistemas_nao_essenciais if modo == "emergencia" else [],
    }


if __name__ == "__main__":
    # Demonstração isolada: os dados reais virão dos outros integrantes.
    resultado = avaliar_colonia(geracao=40, consumo=70, reserva=15)
    print("Nível:", resultado["nivel"])
    print("Modo:", resultado["modo"])
    print("Alertas:")
    for mensagem in resultado["alertas"]:
        print(" -", mensagem)
    print("Recomendações:")
    for mensagem in resultado["recomendacoes"]:
        print(" -", mensagem)
    print("Sistemas prioritários:", ", ".join(resultado["sistemas_prioritarios"]))

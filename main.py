"""main.py - Integracao definitiva do sistema Aurora Siger.

Reune:
- leitura dos dados atuais da colonia;
- analise do balanco energetico;
- regras de decisao;
- previsoes futuras de geracao eolica e solar.
"""

from acesso import leitura_atual
from dados import COLONIA
from energia import analisar_leitura_colonia
from previsao import prever_geracao_eolica, prever_geracao_solar
from regras_decisao import avaliar_leitura_colonia


def mostrar_lista(titulo, itens):
    """Exibe os itens de uma lista ou informa que nao ha itens."""
    print(f"\n{titulo}:")

    if itens:
        for item in itens:
            print("-", item)
    else:
        print("- Nenhum")


def mostrar_dados_atuais(leitura):
    """Apresenta a leitura mais recente registrada na colonia."""
    print("\n=== 1. DADOS ATUAIS DA COLONIA ===")
    print("Horario da leitura:", leitura["horario"])
    print("Geracao solar:", leitura["solar_kw"], "kW")
    print("Geracao eolica:", leitura["eolica_kw"], "kW")
    print("Geracao total:", leitura["geracao_kw"], "kW")
    print("Consumo total:", leitura["consumo_kw"], "kW")
    print("Reserva atual:", leitura["reserva_kwh"], "kWh")
    print("Temperatura externa:", leitura["temp_externa_c"], "C")
    print("Velocidade do vento:", leitura["vento_ms"], "m/s")

    print("\nConsumo por modulo:")
    for nome, consumo in leitura["consumos_kw"].items():
        print(f"- {nome}: {consumo} kW")


def mostrar_analise_energetica(analise):
    """Apresenta o balanco energetico calculado para a leitura atual."""
    print("\n=== 2. ANALISE ENERGETICA ATUAL ===")
    print("Situacao:", analise["situacao"])
    print("Saldo energetico:", analise["saldo_kw"], "kW")
    print("Saldo no intervalo:", analise["saldo_kwh"], "kWh")
    print("Deficit:", analise["deficit_kwh"], "kWh")
    print("Excedente:", analise["excedente_kwh"], "kWh")
    print("Energia retirada da reserva:", analise["energia_retirada_kwh"], "kWh")
    print("Energia armazenada:", analise["energia_armazenada_kwh"], "kWh")
    print("Deficit nao coberto:", analise["deficit_nao_coberto_kwh"], "kWh")
    print("Excedente nao armazenado:", analise["excedente_nao_armazenado_kwh"], "kWh")
    print("Reserva projetada:", analise["reserva_projetada_kwh"], "kWh")


def mostrar_regras_decisao(decisao):
    """Apresenta nivel, modo, alertas, recomendacoes e prioridades."""
    print("\n=== 3. REGRAS DE DECISAO ===")
    print("Nivel:", decisao["nivel"])
    print("Modo de operacao:", decisao["modo"])
    print("Deficit considerado:", decisao["deficit_kwh"], "kWh")

    mostrar_lista("Alertas", decisao["alertas"])
    mostrar_lista("Recomendacoes", decisao["recomendacoes"])
    mostrar_lista("Sistemas prioritarios", decisao["sistemas_prioritarios"])
    mostrar_lista("Sistemas para reduzir", decisao["sistemas_reduzir"])
    mostrar_lista("Sistemas para desligar", decisao["sistemas_desligar"])


def obter_parametros_previsao():
    """Solicita os parametros futuros e oferece exemplos como padrao."""
    print("\n=== 4. PARAMETROS DAS PREVISOES FUTURAS ===")
    print("Pressione Enter para usar os exemplos: 14 m/s e 14:00.")

    entrada_vento = input("Velocidade futura do vento, em m/s [14]: ").strip()
    entrada_horario = input("Horario futuro, no formato HH:MM [14:00]: ").strip()

    vento_ms = 14.0 if entrada_vento == "" else float(entrada_vento.replace(",", "."))
    horario = "14:00" if entrada_horario == "" else entrada_horario

    return vento_ms, horario


def mostrar_previsoes(previsao_eolica, previsao_solar):
    """Apresenta as previsoes sem misturar com os dados atuais."""
    geracao_total_prevista = (
        previsao_eolica["geracao_prevista_kw"]
        + previsao_solar["geracao_prevista_kw"]
    )

    print("\n=== 5. PREVISOES FUTURAS ===")

    print("\nPrevisao eolica:")
    print("Vento informado:", previsao_eolica["vento_ms"], "m/s")
    print(
        "Geracao matematica bruta:",
        round(previsao_eolica["geracao_prevista_bruta_kw"], 2),
        "kW",
    )
    print(
        "Geracao prevista:",
        round(previsao_eolica["geracao_prevista_kw"], 2),
        "kW",
    )
    print("Capacidade eolica:", previsao_eolica["capacidade_kw"], "kW")
    print("R2 do modelo:", round(previsao_eolica["r2"], 4))

    print("\nPrevisao solar:")
    print("Horario informado:", previsao_solar["horario"])
    print(
        "Geracao matematica bruta:",
        round(previsao_solar["geracao_prevista_bruta_kw"], 2),
        "kW",
    )
    print(
        "Geracao prevista:",
        round(previsao_solar["geracao_prevista_kw"], 2),
        "kW",
    )
    print("Capacidade solar:", previsao_solar["capacidade_kw"], "kW")
    print("R2 do modelo:", round(previsao_solar["r2"], 4))

    print("\nGeracao total futura prevista:", round(geracao_total_prevista, 2), "kW")
    print("Observacao: as previsoes futuras nao alteram a analise da leitura atual.")


def main():
    """Executa a integracao completa do sistema Aurora."""
    print("=== SISTEMA AURORA - PRIMEIROS SISTEMAS DA COLONIA ===")

    leitura = leitura_atual(COLONIA)
    analise = analisar_leitura_colonia(COLONIA)
    decisao = avaliar_leitura_colonia(COLONIA)

    mostrar_dados_atuais(leitura)
    mostrar_analise_energetica(analise)
    mostrar_regras_decisao(decisao)

    try:
        vento_ms, horario = obter_parametros_previsao()
        previsao_eolica = prever_geracao_eolica(COLONIA, vento_ms)
        previsao_solar = prever_geracao_solar(COLONIA, horario)
    except (TypeError, ValueError) as erro:
        print("\nNao foi possivel realizar as previsoes:", erro)
        return

    mostrar_previsoes(previsao_eolica, previsao_solar)


if __name__ == "__main__":
    main()

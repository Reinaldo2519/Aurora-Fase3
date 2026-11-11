from dados import COLONIA

from acesso import (
    leitura_atual,
    modulos_por_prioridade,
    modulos_nao_essenciais,
    obter_subsistema,
)
from regras_decisao import avaliar_colonia

from previsao import (
    prever_geracao_eolica,
    prever_geracao_solar,
)

# Recebe a leitura mais recente
leitura = leitura_atual(COLONIA)

intervalo_horas = 1

# Aplica nossas regras usando os dados da Parte 1
resultado = avaliar_colonia(
    geracao=leitura["geracao_kw"] * intervalo_horas,
    consumo=leitura["consumo_kw"] * intervalo_horas,
    reserva=leitura["reserva_kwh"],
    limite_consumo_alto=70 * intervalo_horas,
    limite_reserva_baixa=20,
)

# Obtém os módulos essenciais definidos pelo Integrante 1
essenciais = []

for nome in modulos_por_prioridade(COLONIA):
    modulo = obter_subsistema(COLONIA, "operacional", nome)

    if modulo["essencial"]:
        essenciais.append(nome)

nao_essenciais = modulos_nao_essenciais(COLONIA)

resultado["sistemas_prioritarios"] = essenciais

resultado["sistemas_reduzir"] = (
    nao_essenciais if resultado["modo"] == "economia" else []
)

resultado["sistemas_desligar"] = (
    nao_essenciais if resultado["modo"] == "emergencia" else []
)

# Realiza as previsoes de energia
previsao_eolica = prever_geracao_eolica(
    COLONIA,
    14,
)

previsao_solar = prever_geracao_solar(
    COLONIA,
    "14:00",
)

geracao_total_prevista = (
    previsao_eolica["geracao_prevista_kw"]
    + previsao_solar["geracao_prevista_kw"]
)

# Exibe os resultados
print("=== SISTEMA AURORA ===")
print("Horario:", leitura["horario"])
print("Geracao:", leitura["geracao_kw"], "kW")
print("Consumo:", leitura["consumo_kw"], "kW")
print("Reserva:", leitura["reserva_kwh"], "kWh")

print("\nNivel:", resultado["nivel"])
print("Modo:", resultado["modo"])

print("\nAlertas:")
for alerta in resultado["alertas"]:
    print("-", alerta)

print("\nRecomendacoes:")
for recomendacao in resultado["recomendacoes"]:
    print("-", recomendacao)

print("\nSistemas essenciais:", ", ".join(essenciais))
print("Sistemas para desligar:", resultado["sistemas_desligar"])

print("\n=== PREVISAO DE ENERGIA ===")

print("\nPrevisao eolica:")
print(
    "Vento previsto:",
    previsao_eolica["vento_ms"],
    "m/s",
)
print(
    "Geracao prevista:",
    round(
        previsao_eolica["geracao_prevista_kw"],
        2,
    ),
    "kW",
)
print("\nPrevisao solar:")
print(
    "Horario previsto:",
    previsao_solar["horario"],
)
print(
    "Geracao prevista:",
    round(
        previsao_solar["geracao_prevista_kw"],
        2,
    ),
    "kW",
)
print(
    "\nGeracao total prevista:",
    round(geracao_total_prevista, 2),
    "kW",
)

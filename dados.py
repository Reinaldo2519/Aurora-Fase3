"""
dados.py - Dados da colonia Aurora Siger (Fase 3)

Aqui fica SO a estrutura de dados da colonia, sem nenhuma regra de decisao.
Os dados sao simulados (nao sao medicoes reais) e representam 8 leituras
horarias dos sensores, das 06:00 as 13:00.

Organizacao (hierarquia de dicionarios, com listas nas folhas):

    COLONIA
     |-- sistemas
          |-- energetico   -> solar, eolico, reserva
          |-- ambiental    -> clima_externo, clima_interno
          |-- operacional  -> suporte_vida, habitacao, comunicacao,
                              laboratorio, producao_isru

- Dicionario (chave-valor): usado para nomear sistemas, subsistemas e
  variaveis, o que permite acessar cada informacao pelo nome.
- Lista: usada para as series de leituras. A posicao i de qualquer lista
  corresponde ao horario HORARIOS[i].
"""

# Horario de cada leitura. O indice da lista e o mesmo em todas as series.
HORARIOS = ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00"]

COLONIA = {
    "nome": "Aurora Siger",
    "horarios": HORARIOS,
    "sistemas": {

        # ------------------------------------------------------------------
        # SISTEMA ENERGETICO: geracao (solar e eolica) e reserva
        # ------------------------------------------------------------------
        "energetico": {
            "descricao": "Geracao, armazenamento e reserva de energia",
            "subsistemas": {
                "solar": {
                    "descricao": "Paineis solares",
                    "estado": "online",
                    "capacidade_kw": 60,
                    "geracao_kw": [5, 14, 26, 38, 47, 52, 54, 53],
                },
                "eolico": {
                    "descricao": "Turbinas eolicas",
                    "estado": "online",
                    "capacidade_kw": 40,
                    "geracao_kw": [20, 25, 22, 30, 25, 30, 27, 33],
                },
                "reserva": {
                    "descricao": "Baterias da colonia",
                    "estado": "online",
                    "capacidade_kwh": 300,
                    "nivel_inicial_kwh": 150,           # antes das 06:00
                    # nivel ao fim de cada hora = nivel anterior + geracao - consumo
                    "nivel_kwh": [142, 136, 124, 123, 119, 123, 128, 141],
                },
            },
        },

        # ------------------------------------------------------------------
        # SISTEMA AMBIENTAL: clima fora e dentro da colonia
        # ------------------------------------------------------------------
        "ambiental": {
            "descricao": "Condicoes climaticas externas e internas",
            "subsistemas": {
                "clima_externo": {
                    "descricao": "Sensores externos",
                    "temperatura_c": [-68, -60, -52, -45, -40, -38, -37, -39],
                    "vento_ms": [8, 10, 9, 12, 10, 12, 11, 13],
                },
                "clima_interno": {
                    "descricao": "Sensores dos habitats",
                    "temperatura_c": [21, 21, 22, 22, 22, 22, 23, 23],
                    "pressao_kpa": [101.2, 101.3, 101.2, 101.1, 101.2, 101.3, 101.2, 101.2],
                },
            },
        },

        # ------------------------------------------------------------------
        # SISTEMA OPERACIONAL: modulos que consomem energia
        # prioridade 1 = mais importante; essencial = nao pode ser desligado
        # ------------------------------------------------------------------
        "operacional": {
            "descricao": "Modulos da colonia e seu consumo",
            "subsistemas": {
                "suporte_vida": {
                    "descricao": "Suporte a vida",
                    "estado": "online",
                    "essencial": True,
                    "prioridade": 1,
                    "consumo_kw": [18, 18, 18, 19, 19, 19, 19, 19],
                },
                "habitacao": {
                    "descricao": "Habitat da tripulacao",
                    "estado": "online",
                    "essencial": True,
                    "prioridade": 2,
                    "consumo_kw": [8, 10, 12, 12, 13, 13, 12, 12],
                },
                "comunicacao": {
                    "descricao": "Comunicacao com a Terra",
                    "estado": "online",
                    "essencial": True,
                    "prioridade": 3,
                    "consumo_kw": [3, 3, 4, 4, 4, 4, 4, 4],
                },
                "laboratorio": {
                    "descricao": "Laboratorio cientifico",
                    "estado": "online",
                    "essencial": False,
                    "prioridade": 4,
                    "consumo_kw": [4, 8, 14, 16, 18, 18, 17, 16],
                },
                "producao_isru": {
                    "descricao": "Producao com recursos locais",
                    "estado": "online",
                    "essencial": False,
                    "prioridade": 5,
                    "consumo_kw": [0, 6, 12, 18, 22, 24, 24, 22],
                },
            },
        },
    },
}

# Caminho de cada variavel medida (sistema/subsistema/variavel).
# Serve para ler e para registrar leituras sem repetir os caminhos pelo codigo.
CAMINHOS = {
    "solar_kw": "energetico/solar/geracao_kw",
    "eolica_kw": "energetico/eolico/geracao_kw",
    "reserva_kwh": "energetico/reserva/nivel_kwh",
    "temp_externa_c": "ambiental/clima_externo/temperatura_c",
    "vento_ms": "ambiental/clima_externo/vento_ms",
    "temp_interna_c": "ambiental/clima_interno/temperatura_c",
    "pressao_interna_kpa": "ambiental/clima_interno/pressao_kpa",
}

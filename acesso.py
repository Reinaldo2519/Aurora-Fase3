"""
acesso.py - Funcoes para ler e navegar nos dados da colonia (Fase 3)

Nenhuma funcao daqui toma decisao: elas so buscam, somam e organizam os
dados. As regras de decisao ficam em decisoes.py e energia.py, e a previsao
em previsao.py. Assim, quem escreve as regras nao precisa conhecer a
estrutura interna dos dicionarios, so estas funcoes.

Resumo:
  Navegacao   : listar_sistemas, listar_subsistemas, obter_subsistema,
                obter_valor, mostrar_hierarquia
  Series      : ultimo_valor, geracao_total, consumo_total
  Modulos     : listar_modulos, modulos_por_prioridade, modulos_nao_essenciais
  Leitura     : leitura_atual   (devolve um dicionario simples com os valores
                                 mais recentes, pronto para as regras)
  Atualizacao : registrar_leitura, validar_colonia
"""

from dados import CAMINHOS


# ---------------------------------------------------------------------------
# NAVEGACAO NA HIERARQUIA
# ---------------------------------------------------------------------------

def listar_sistemas(colonia):
    """Devolve os nomes dos sistemas (energetico, ambiental, operacional)."""
    return list(colonia["sistemas"].keys())


def listar_subsistemas(colonia, sistema):
    """Devolve os nomes dos subsistemas de um sistema ([] se nao existir)."""
    if sistema not in colonia["sistemas"]:
        return []
    return list(colonia["sistemas"][sistema]["subsistemas"].keys())


def obter_subsistema(colonia, sistema, subsistema):
    """Devolve o dicionario de um subsistema, ou None se nao existir."""
    if sistema not in colonia["sistemas"]:
        return None
    subsistemas = colonia["sistemas"][sistema]["subsistemas"]
    if subsistema not in subsistemas:
        return None
    return subsistemas[subsistema]


def obter_valor(colonia, caminho):
    """
    Busca uma informacao pelo caminho 'sistema/subsistema/variavel'.
    Exemplo: obter_valor(COLONIA, "energetico/solar/geracao_kw")
    Devolve None se o caminho nao existir.
    """
    partes = caminho.split("/")
    if len(partes) != 3:
        return None
    subsistema = obter_subsistema(colonia, partes[0], partes[1])
    if subsistema is None:
        return None
    return subsistema.get(partes[2])


def mostrar_hierarquia(colonia):
    """Imprime a arvore sistema -> subsistema -> variaveis."""
    print(colonia["nome"])
    for sistema in listar_sistemas(colonia):
        print("  " + sistema)
        for sub in listar_subsistemas(colonia, sistema):
            dados_sub = obter_subsistema(colonia, sistema, sub)
            variaveis = []
            for chave in dados_sub:
                if isinstance(dados_sub[chave], list):
                    variaveis.append(chave)
            print("    " + sub + "  ->  " + ", ".join(variaveis))


# ---------------------------------------------------------------------------
# SERIES DE DADOS
# ---------------------------------------------------------------------------

def ultimo_valor(serie):
    """Devolve a leitura mais recente de uma lista (None se estiver vazia)."""
    if len(serie) == 0:
        return None
    return serie[-1]


def geracao_total(colonia):
    """Lista com a geracao total (solar + eolica) em cada horario, em kW."""
    solar = obter_valor(colonia, CAMINHOS["solar_kw"])
    eolica = obter_valor(colonia, CAMINHOS["eolica_kw"])
    total = []
    for i in range(len(solar)):
        total.append(solar[i] + eolica[i])
    return total


def consumo_total(colonia):
    """Lista com o consumo somado de todos os modulos em cada horario, em kW."""
    total = []
    modulos = listar_modulos(colonia)
    quantidade = len(colonia["horarios"])
    for i in range(quantidade):
        soma = 0
        for nome in modulos:
            modulo = obter_subsistema(colonia, "operacional", nome)
            soma = soma + modulo["consumo_kw"][i]
        total.append(soma)
    return total


# ---------------------------------------------------------------------------
# MODULOS OPERACIONAIS
# ---------------------------------------------------------------------------

def listar_modulos(colonia):
    """Nomes dos modulos do sistema operacional."""
    return listar_subsistemas(colonia, "operacional")


def modulos_por_prioridade(colonia):
    """Nomes dos modulos do mais importante (prioridade 1) ao menos importante."""
    pares = []
    for nome in listar_modulos(colonia):
        modulo = obter_subsistema(colonia, "operacional", nome)
        pares.append((modulo["prioridade"], nome))
    pares.sort()
    nomes = []
    for prioridade, nome in pares:
        nomes.append(nome)
    return nomes


def modulos_nao_essenciais(colonia):
    """Modulos que podem ser desligados numa emergencia, na ordem de desligamento
    (primeiro o de menor importancia)."""
    candidatos = []
    for nome in modulos_por_prioridade(colonia):
        modulo = obter_subsistema(colonia, "operacional", nome)
        if not modulo["essencial"]:
            candidatos.append(nome)
    candidatos.reverse()
    return candidatos


# ---------------------------------------------------------------------------
# LEITURA ATUAL (ENTRADA PARA AS REGRAS)
# ---------------------------------------------------------------------------

def leitura_atual(colonia, indice=-1):
    """
    Junta os valores de um horario (por padrao, o mais recente) em um
    dicionario simples, que e a ENTRADA do sistema de decisao.

    Chaves: horario, solar_kw, eolica_kw, geracao_kw, consumo_kw,
            reserva_kwh, temp_externa_c, vento_ms, temp_interna_c,
            consumos_kw (dicionario modulo -> kW)
    """
    horarios = colonia["horarios"]
    geracao = geracao_total(colonia)
    consumo = consumo_total(colonia)

    consumos = {}
    for nome in listar_modulos(colonia):
        modulo = obter_subsistema(colonia, "operacional", nome)
        consumos[nome] = modulo["consumo_kw"][indice]

    return {
        "horario": horarios[indice],
        "solar_kw": obter_valor(colonia, CAMINHOS["solar_kw"])[indice],
        "eolica_kw": obter_valor(colonia, CAMINHOS["eolica_kw"])[indice],
        "geracao_kw": geracao[indice],
        "consumo_kw": consumo[indice],
        "reserva_kwh": obter_valor(colonia, CAMINHOS["reserva_kwh"])[indice],
        "temp_externa_c": obter_valor(colonia, CAMINHOS["temp_externa_c"])[indice],
        "vento_ms": obter_valor(colonia, CAMINHOS["vento_ms"])[indice],
        "temp_interna_c": obter_valor(colonia, CAMINHOS["temp_interna_c"])[indice],
        "consumos_kw": consumos,
    }


# ---------------------------------------------------------------------------
# ATUALIZACAO E VALIDACAO
# ---------------------------------------------------------------------------

def registrar_leitura(colonia, horario, leitura):
    """
    Acrescenta uma nova leitura (um novo horario) a todas as series.
    'leitura' e um dicionario com as chaves de CAMINHOS (solar_kw, eolica_kw,
    vento_ms, ...) e a chave 'consumos_kw' (dicionario modulo -> kW).
    Devolve True se registrou ou False se faltou algum dado (nada e alterado).
    """
    for chave in CAMINHOS:
        if chave not in leitura:
            return False
    if "consumos_kw" not in leitura:
        return False
    for nome in listar_modulos(colonia):
        if nome not in leitura["consumos_kw"]:
            return False

    colonia["horarios"].append(horario)
    for chave in CAMINHOS:
        obter_valor(colonia, CAMINHOS[chave]).append(leitura[chave])
    for nome in listar_modulos(colonia):
        modulo = obter_subsistema(colonia, "operacional", nome)
        modulo["consumo_kw"].append(leitura["consumos_kw"][nome])
    return True


def validar_colonia(colonia):
    """
    Confere se todas as series tem o mesmo tamanho da lista de horarios.
    Devolve uma lista de mensagens de erro (lista vazia = dados consistentes).
    """
    erros = []
    quantidade = len(colonia["horarios"])
    for sistema in listar_sistemas(colonia):
        for sub in listar_subsistemas(colonia, sistema):
            dados_sub = obter_subsistema(colonia, sistema, sub)
            for chave in dados_sub:
                valor = dados_sub[chave]
                if isinstance(valor, list) and len(valor) != quantidade:
                    erros.append(sistema + "/" + sub + "/" + chave + ": "
                                 + str(len(valor)) + " leituras (esperado "
                                 + str(quantidade) + ")")
    return erros

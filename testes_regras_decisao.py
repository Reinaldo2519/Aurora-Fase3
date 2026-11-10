"""Testes simples (sem bibliotecas externas) para a Parte 2 da Aurora."""

from regras_decisao import avaliar_colonia

cenarios = [
    ("Operação normal", 90, 50, 40, "NORMAL", "normal"),
    ("Consumo alto", 100, 80, 40, "ATENCAO", "monitoramento"),
    ("Déficit coberto pela reserva", 40, 60, 30, "ALERTA", "economia"),
    ("Déficit crítico", 20, 70, 10, "CRITICO", "emergencia"),
    ("Reserva baixa", 70, 40, 10, "ATENCAO", "monitoramento"),
    ("Consumo alto e reserva baixa", 100, 80, 10, "ALERTA", "economia"),
    ("Geração igual ao consumo", 50, 50, 30, "NORMAL", "normal"),
    ("Déficit igual à reserva", 40, 70, 30, "CRITICO", "emergencia"),
]

for nome, geracao, consumo, reserva, nivel_esperado, modo_esperado in cenarios:
    resultado = avaliar_colonia(geracao, consumo, reserva)
    assert resultado["nivel"] == nivel_esperado, f"Falhou: {nome} (nível)"
    assert resultado["modo"] == modo_esperado, f"Falhou: {nome} (modo)"
    assert "Suporte à vida" in resultado["sistemas_prioritarios"]
    if modo_esperado == "emergencia":
        assert resultado["sistemas_desligar"]
    else:
        assert not resultado["sistemas_desligar"]
    print(f"OK - {nome}: {resultado['nivel']}")

for entrada in [(-1, 30, 10), (40, -1, 10), (40, 30, -1)]:
    try:
        avaliar_colonia(*entrada)
        raise AssertionError(f"Valor negativo aceito indevidamente: {entrada}")
    except ValueError:
        pass

try:
    avaliar_colonia("40", 30, 10)
    raise AssertionError("Texto aceito indevidamente.")
except TypeError:
    pass

print("Todos os 8 cenários e 4 validações passaram.")

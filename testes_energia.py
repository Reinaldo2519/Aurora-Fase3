"""teste de analise energetica"""
from dados import COLONIA
from energia import analisar_energia, analisar_leitura_colonia

r = analisar_energia(40, 70, 100, 150)
assert r["situacao"] == "DEFICIT"
assert r["deficit_kwh"] == 30
assert r["reserva_projetada_kwh"] == 70

r = analisar_energia(80, 30, 140, 150)
assert r["situacao"] == "EXCEDENTE"
assert r["energia_armazenada_kwh"] == 10
assert r["excedente_nao_armazenado_kwh"] == 40
assert r["reserva_projetada_kwh"] == 150

r = analisar_energia(10, 50, 15, 150)
assert r["deficit_nao_coberto_kwh"] == 25
assert r["reserva_projetada_kwh"] == 0

r = analisar_energia(50, 50, 100, 150)
assert r["situacao"] == "EQUILIBRIO"

r = analisar_leitura_colonia(COLONIA)
assert r["geracao_kw"] == 86
assert r["consumo_kw"] == 73
assert r["reserva_inicial_kwh"] == 141
assert r["reserva_projetada_kwh"] == 154
print("OK: 5 cenarios de analise energetica.")

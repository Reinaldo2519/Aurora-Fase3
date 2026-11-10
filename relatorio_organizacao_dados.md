# Organização dos dados

## 1. Objetivo

A colônia Aurora Siger precisa guardar informações de energia, clima e consumo de forma organizada, para que os módulos de análise, previsão e decisão leiam os mesmos dados sem duplicação. A estrutura foi feita apenas com listas e dicionários do Python.

## 2. Hierarquia dos subsistemas

Os dados seguem a hierarquia sistema → subsistema → variável, dentro de um dicionário chamado `COLONIA`:

| Sistema | Subsistema | Variáveis |
|---|---|---|
| Energético | Solar | geração (kW) |
| Energético | Eólico | geração (kW) |
| Energético | Reserva | nível (kWh) |
| Ambiental | Clima externo | temperatura (°C), vento (m/s) |
| Ambiental | Clima interno | temperatura (°C), pressão (kPa) |
| Operacional | Suporte à vida, habitação, comunicação | consumo (kW), essencial, prioridade 1 a 3 |
| Operacional | Laboratório, produção ISRU | consumo (kW), não essencial, prioridade 4 e 5 |

## 3. Por que dicionários e listas

| Estrutura | Onde foi usada | Motivo |
|---|---|---|
| Dicionário | Sistemas, subsistemas e variáveis | Acesso pelo nome (`"solar"`), sem depender de posição |
| Lista | Séries de medições | Guarda uma leitura por horário, em ordem |
| Dicionário dentro de dicionário | Hierarquia | Representa que um sistema contém subsistemas |

A lista `horarios` (06:00 a 13:00) é única e vale para todas as séries: a posição `i` de qualquer lista corresponde a `horarios[i]`. Cada dado aparece uma só vez; o vento, por exemplo, fica apenas em clima externo e é lido de lá pela previsão.

## 4. Dados utilizados

Como o enunciado não fornece medições reais, foram usados dados simulados, com 8 leituras horárias. Eles foram montados para que:

- o consumo supere a geração nas primeiras horas e sobre energia depois, permitindo testar os alertas de consumo e de armazenamento;
- a geração eólica acompanhe o vento (aproximadamente 2,5 kW por m/s, incluindo os pares 8→20, 10→25 e 12→30 do enunciado), permitindo testar a regressão linear;
- o nível da reserva feche com o balanço entre geração e consumo.

## 5. Funções de acesso

As funções ficam em `acesso.py`, separadas dos dados:

| Função | Uso |
|---|---|
| `obter_valor(colonia, "sistema/sub/variavel")` | Lê uma série pelo caminho |
| `leitura_atual(colonia)` | Devolve um dicionário simples com a leitura mais recente (entrada das regras de decisão) |
| `geracao_total` e `consumo_total` | Somam as fontes ou os módulos por horário |
| `modulos_nao_essenciais` | Define a ordem de desligamento por prioridade |
| `registrar_leitura` | Acrescenta uma nova leitura, recusando dados incompletos |
| `validar_colonia` | Confere se todas as séries têm o mesmo tamanho |

## 6. Exemplo

Entrada: dados de `dados.py`. Saída de `python main.py`, leitura das 13:00:

```
Geracao: 86 kW (solar 53 + eolica 33)
Consumo: 73 kW
Reserva: 141 kWh
Clima externo: -39 C, vento 13 m/s
```

## 7. Organização dos arquivos

`dados.py` guarda os dados; `acesso.py`, `energia.py` e `previsao.py` guardam a lógica; `decisoes.py` guarda as regras; `main.py` executa o fluxo entrada → processamento → saída. `teste_dados.py` verifica a estrutura com testes simples, todos aprovados.



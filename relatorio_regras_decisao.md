# Regras de Decisão e Lógica do Sistema

## 1. Objetivo

O módulo de regras de decisão foi desenvolvido para permitir que a colônia Aurora identifique situações de risco energético e tome decisões automáticas de acordo com os dados disponíveis.

O sistema analisa três informações principais: geração de energia, consumo energético e reserva armazenada. Com esses valores, classifica a situação da colônia e apresenta alertas e recomendações para manter o funcionamento dos serviços essenciais.

## 2. Funcionamento da lógica

A implementação foi realizada em Python, utilizando estruturas condicionais `if`, `elif` e `else`, além de operadores lógicos como `and` e `or`.

A principal função desenvolvida é `avaliar_colonia()`, que recebe os valores energéticos e aplica regras para determinar o nível de risco, o modo de operação e as recomendações correspondentes.

Foram definidos quatro níveis de operação:

| Nível | Condição | Ação |
|---|---|---|
| NORMAL | Não há déficit nem indicadores acima dos limites | Manter operação normal |
| ATENÇÃO | Consumo elevado ou reserva baixa | Intensificar o monitoramento |
| ALERTA | Déficit coberto pela reserva ou consumo elevado combinado com reserva baixa | Recomendar economia de energia |
| CRÍTICO | Déficit igual ou superior à reserva disponível | Recomendar modo de emergência |

Para os testes iniciais, foram utilizados limites configuráveis de 70 para consumo elevado e 20 para reserva baixa. Esses limites são parâmetros de simulação e podem ser ajustados conforme as necessidades do projeto.

## 3. Prioridades dos sistemas

Em situações de emergência, o sistema recomenda priorizar o funcionamento dos serviços essenciais da colônia.

A lógica também indica a redução ou o desligamento temporário de sistemas não essenciais, buscando preservar a energia disponível.

Na integração inicial com a organização de dados, foram identificados como essenciais os módulos de suporte à vida, habitação e comunicação.

## 4. Testes realizados

Para verificar o funcionamento das regras, foi criado o arquivo `testes_regras_decisao.py`.

Foram executados oito cenários de simulação, incluindo operação normal, consumo elevado, reserva baixa, déficit energético e situação crítica.

Todos os oito cenários e quatro validações de entradas inválidas passaram nos testes executados.

Também foi realizado um teste preliminar de integração com os arquivos `dados.py` e `acesso.py` da Parte 1, utilizando a função `leitura_atual()`.

Na leitura das 13h, foram obtidos os seguintes valores:

- Geração total: 86 kW;
- Consumo: 73 kW;
- Reserva: 141 kWh.

O sistema classificou a situação como ATENÇÃO, pois o consumo ultrapassou o limite configurado de 70 kW, embora a geração fosse suficiente para atender à demanda.

## 5. Conclusão

O módulo desenvolvido permite transformar informações energéticas em classificações de risco e recomendações automáticas.

Os testes demonstraram o funcionamento das regras nos cenários definidos. A integração inicial com a Parte 1 também foi executada com sucesso.

A integração definitiva com os módulos de previsão e análise energética será realizada na composição do sistema completo da colônia.
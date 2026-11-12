
# 🚀 Aurora Siger – Fase 3
## Sistema Integrado de Gerenciamento Inteligente da Colônia

### 📌 Sobre o projeto

O **Aurora Siger** é um sistema desenvolvido em Python para simular o gerenciamento inteligente de uma colônia espacial.

O projeto integra organização de dados, lógica de decisão, previsão por regressão linear e análise energética, permitindo monitorar os recursos da colônia e tomar decisões automáticas com base nas condições identificadas.

O objetivo é contribuir para o funcionamento seguro e eficiente da colônia, priorizando sistemas essenciais e otimizando o uso de energia.

Projeto desenvolvido como parte da **Fase 3 do curso de Ciência da Computação da FIAP – 2026**.

---

## 🎯 Funcionalidades

### 1. Organização dos dados

O sistema utiliza listas e dicionários para armazenar e organizar informações da colônia.

Os dados são organizados hierarquicamente em três sistemas principais:

| Sistema | Subsistemas | Informações |
|---|---|---|
| Energético | Solar, eólico e reserva | Geração, capacidade e armazenamento |
| Ambiental | Clima externo e interno | Temperatura, vento e pressão |
| Operacional | Suporte à vida, habitação, comunicação, laboratório e produção ISRU | Consumo, estado e prioridade |

O arquivo `dados.py` centraliza os dados simulados, enquanto `acesso.py` permite consultar informações, navegar entre subsistemas e calcular valores totais.

Os históricos contêm oito leituras horárias, das 06:00 às 13:00.

### 2. Tomada de decisões automáticas

O sistema utiliza estruturas condicionais e operadores lógicos para analisar a situação da colônia.

As decisões são classificadas em quatro níveis:

| Nível | Condição | Ação |
|---|---|---|
| CRITICO | Déficit energético igual ou superior à reserva disponível | Priorizar sistemas essenciais |
| ALERTA | Déficit coberto pela reserva ou consumo alto com reserva baixa | Reduzir consumo não essencial |
| ATENCAO | Consumo elevado ou reserva baixa | Intensificar monitoramento |
| NORMAL | Condições adequadas | Manter operação |

Os limites padrão são:

- Consumo elevado: a partir de 70 kW;
- Reserva baixa: inferior a 20 kWh;
- Intervalo de análise: 1 hora.

O sistema prioriza suporte à vida, habitação e comunicação. Em situações críticas, recomenda reduzir primeiro a produção ISRU e depois o laboratório.

As decisões são recomendações simuladas e não controlam equipamentos reais.

### 3. Previsão por regressão linear

O sistema utiliza regressão linear simples para estimar a geração de energia solar e eólica com base em dados históricos.

A equação utilizada é:

**y = ax + b**

Onde:

- `x`: variável de entrada;
- `y`: geração prevista;
- `a`: coeficiente angular;
- `b`: coeficiente linear.

**Previsão eólica:**

Relaciona a velocidade do vento, em m/s, com a geração de energia, em kW.

**Previsão solar:**

Relaciona o horário informado com a geração solar estimada.

As previsões respeitam os limites de capacidade:

- Energia eólica: máximo de 40 kW;
- Energia solar: máximo de 60 kW.

O módulo `previsao.py` também calcula métricas como MSE, R² e resíduos, permitindo avaliar o ajuste dos modelos aos dados simulados.

### 4. Análise energética

O módulo `energia.py` compara geração, consumo e reserva energética.

São calculados:

- Saldo entre geração e consumo;
- Déficit energético;
- Excedente disponível;
- Energia retirada da bateria;
- Energia armazenada;
- Reserva projetada;
- Energia não atendida;
- Excedente que ultrapassa a capacidade de armazenamento.

Exemplo de déficit:

```text
Geração: 40 kW
Consumo: 70 kW
Saldo: -30 kW

ALERTA: consumo superior à geração.
RECOMENDAÇÃO: reduzir consumo.
```

Exemplo de excedente:

```text
Geração: 80 kW
Consumo: 30 kW
Saldo: +50 kW

SITUAÇÃO: excedente energético.
RECOMENDAÇÃO: armazenar energia disponível.
```

---

## ⚙️ Funcionamento do sistema

O programa principal integra os quatro componentes do projeto.

O fluxo de execução é:

1. Carregar os dados da colônia;
2. Consultar os subsistemas e as leituras atuais;
3. Calcular geração, consumo e reserva;
4. Analisar o balanço energético;
5. Aplicar as regras de decisão;
6. Solicitar os parâmetros das previsões;
7. Calcular a geração solar e eólica estimada;
8. Apresentar resultados, alertas e recomendações.

Essa integração permite analisar as condições atuais e estimar comportamentos futuros.

---

## 🛠️ Como instalar e executar o projeto

### 1. Requisitos

É necessário ter o **Python 3** instalado no computador.

O projeto utiliza as bibliotecas:

- NumPy
- Pandas
- Matplotlib
- Scikit-learn

### 2. Instalar as dependências

Abra o terminal na pasta do projeto e execute:

```bash
py -m pip install numpy pandas matplotlib scikit-learn
```

### 3. Executar o sistema completo

Para iniciar o sistema Aurora Siger com as quatro partes integradas, execute:

```bash
py main.py
```

O programa apresentará os dados atuais da colônia, a análise energética e as regras de decisão.

Em seguida, solicitará dois parâmetros para as previsões futuras:

- **Velocidade do vento em m/s:** exemplo `14`;
- **Horário no formato HH:MM:** exemplo `14:00`.

Pressione **Enter** sem digitar nada para utilizar os valores padrão.

### 4. Executar os testes

Para testar cada módulo separadamente, utilize:

**Parte 2 — Regras de decisão**

```bash
py testes_regras_decisao.py
```

**Parte 3 — Previsão energética**

```bash
py testes_previsao.py
```

**Parte 4 — Análise energética**

```bash
py testes_energia.py
```

### 5. Gerar os gráficos da previsão

Execute:

```bash
py previsao.py
```

O programa gera quatro gráficos:

- `grafico_regressao_eolica.png`
- `grafico_residuos_eolicos.png`
- `grafico_regressao_solar.png`
- `grafico_residuos_solares.png`

Os arquivos são salvos na pasta de execução do projeto.

---

## 📂 Estrutura do sistema

| Arquivo | Função |
|---|---|
| `main.py` | Integra as quatro partes do sistema |
| `dados.py` | Armazena os dados simulados da colônia |
| `acesso.py` | Consulta e organiza os dados |
| `regras_decisao.py` | Avalia riscos e gera recomendações |
| `previsao.py` | Realiza previsões por regressão linear |
| `energia.py` | Analisa geração, consumo e reserva energética |
| `testes_regras_decisao.py` | Testa as regras de decisão |
| `testes_previsao.py` | Testa os modelos de previsão |
| `testes_energia.py` | Testa os cálculos energéticos |

---

## 💻 Exemplos de entrada e saída

### Exemplo 1 — Situação atual da colônia

**Entrada:**

```text
Horário: 13:00
Geração solar: 53 kW
Geração eólica: 33 kW
Consumo total: 73 kW
Reserva disponível: 141 kWh
```

**Saída esperada:**

```text
===== AURORA SIGER =====

ANÁLISE ENERGÉTICA

Geração total: 86 kW
Consumo total: 73 kW
Saldo energético: +13 kW

Situação: EXCEDENTE
Energia armazenável em 1 hora: 13 kWh
Reserva projetada: 154 kWh

REGRAS DE DECISÃO

Nível: ATENCAO
Modo: monitoramento

ALERTA: consumo elevado.
RECOMENDAÇÃO: acompanhar consumo e reserva.
```

### Exemplo 2 — Previsão futura

**Entrada:**

```text
Velocidade do vento: 14 m/s
Horário: 14:00
```

**Saída esperada:**

```text
===== PREVISÃO ENERGÉTICA =====

Geração eólica prevista: 35,25 kW
Geração solar prevista: 60,00 kW

Geração total prevista: 95,25 kW
```

Os valores apresentados são exemplos baseados nos dados simulados do projeto. A formatação da saída pode variar conforme a versão final do programa.

---

## 🧠 Conceitos aplicados

| Conceito | Aplicação |
|---|---|
| Listas | Armazenamento dos históricos |
| Dicionários | Organização hierárquica dos subsistemas |
| Funções | Separação das responsabilidades |
| Estruturas condicionais | Regras de decisão |
| Operadores lógicos | Combinação de condições |
| Regressão linear | Estimativa de geração energética |
| Operações matemáticas | Cálculo de saldo e reserva |
| Modularização | Integração dos arquivos Python |

---

## 🌱 Benefícios para a colônia

O Aurora Siger contribui para melhorar o gerenciamento energético por meio de:

- Identificação de situações de déficit;
- Monitoramento da reserva disponível;
- Aproveitamento de excedentes;
- Priorização de sistemas essenciais;
- Redução de desperdícios;
- Previsão de geração solar e eólica;
- Apoio à tomada de decisões.

A integração entre monitoramento e previsão permite que o sistema evolua de uma análise reativa para uma abordagem preditiva simples.

---

## ⚠️ Limitações

Os dados da colônia são simulados para fins acadêmicos.

As previsões são estimativas matemáticas baseadas nesses dados e respeitam os limites de capacidade de geração.

O sistema não realiza o controle físico dos equipamentos e suas recomendações representam decisões simuladas.

---

## 👥 Equipe

Projeto desenvolvido por estudantes de Ciência da Computação da FIAP.

**Integrantes:**

- Integrante 1
- Integrante 2
- Integrante 3
- Integrante 4

---

## 📚 Considerações finais

O desenvolvimento do Aurora Siger demonstra a aplicação integrada de estruturas de dados, lógica de programação, regressão linear e análise energética.

O sistema organiza informações da colônia, identifica situações de risco, recomenda ações e estima comportamentos futuros.

Dessa forma, apresenta uma solução computacional simples para apoiar o gerenciamento inteligente dos recursos de uma colônia espacial.

**FIAP | Ciência da Computação | Fase 3 | 2026**


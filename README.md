
# 🚀 Aurora Siger – Fase 3
## Sistema Integrado de Gerenciamento Inteligente da Colônia

### 📌 Sobre o projeto

O **Aurora Siger** é um sistema desenvolvido em Python para simular o gerenciamento inteligente de uma colônia espacial.

O projeto integra organização de dados, lógica de decisão, previsão por regressão linear e análise energética, permitindo monitorar os recursos da colônia e tomar decisões automáticas com base nas condições identificadas.

O objetivo é contribuir para o funcionamento seguro e eficiente da colônia, priorizando sistemas essenciais e otimizando o uso de energia.

O projeto foi desenvolvido como parte da **Fase 3 do curso de Ciência da Computação da FIAP**.

---

## 🎯 Funcionalidades

### 1. Organização dos dados

O sistema utiliza estruturas de dados em Python, como listas e dicionários, para armazenar e organizar informações relacionadas à colônia.

Os dados são organizados de forma hierárquica, permitindo acessar informações de diferentes subsistemas.

Entre os dados monitorados estão:

- Geração de energia solar e eólica;
- Consumo energético;
- Reserva de energia;
- Condições climáticas;
- Estado dos subsistemas da colônia.

### 2. Tomada de decisões automáticas

O sistema utiliza estruturas condicionais e operadores lógicos para analisar as condições da colônia e determinar ações.

Exemplos de regras:

- Energia insuficiente → emitir alerta;
- Consumo superior à geração → recomendar redução de consumo;
- Energia excedente → recomendar armazenamento;
- Situação crítica → priorizar sistemas essenciais;
- Condições adequadas → manter operação normal.

As decisões são apresentadas por mensagens que indicam a situação identificada e a ação recomendada.

### 3. Previsão utilizando regressão linear

O sistema utiliza regressão linear simples para estimar o comportamento de variáveis relacionadas à geração de energia.

A partir de dados históricos, é calculada uma relação matemática entre as variáveis, permitindo realizar previsões.

A equação utilizada é:

**y = ax + b**

Onde:

- **y:** valor previsto;
- **x:** variável de entrada;
- **a:** coeficiente angular;
- **b:** coeficiente linear.

Exemplo ilustrativo:

Entrada:
- Velocidade do vento: 11 m/s.

Saída:
- Previsão de geração eólica: aproximadamente 27 unidades de energia.

Essa funcionalidade permite antecipar possíveis mudanças na disponibilidade energética da colônia.

### 4. Análise energética

O sistema compara os valores de geração, consumo e reserva de energia para avaliar a situação energética da colônia.

As principais análises realizadas são:

- Comparação entre energia gerada e consumida;
- Identificação de déficit energético;
- Identificação de excedente energético;
- Avaliação da reserva disponível;
- Recomendações para otimização do consumo.

Exemplos:

**Situação 1 – Déficit energético**

Entrada:
- Geração: 40
- Consumo: 70

Saída:
- ALERTA: consumo superior à geração.
- RECOMENDAÇÃO: reduzir o consumo energético.

**Situação 2 – Excedente energético**

Entrada:
- Geração: 80
- Consumo: 30

Saída:
- SITUAÇÃO: excedente de energia identificado.
- RECOMENDAÇÃO: armazenar energia disponível.

---

## ⚙️ Funcionamento do sistema

O Aurora Siger funciona por meio da integração de diferentes módulos Python.

O fluxo geral é:

1. Carregamento dos dados da colônia;
2. Organização e consulta dos subsistemas;
3. Análise das condições atuais;
4. Aplicação das regras de decisão;
5. Cálculo das previsões por regressão linear;
6. Avaliação do balanço energético;
7. Exibição dos resultados, alertas e recomendações.

Dessa forma, o sistema combina monitoramento, decisões automáticas e previsões em uma única solução.

---

## 🛠️ Tecnologias utilizadas

- **Python 3**
- Listas e dicionários;
- Funções;
- Estruturas condicionais;
- Operadores lógicos;
- Estruturas de repetição;
- Operações matemáticas;
- Regressão linear simples.

O projeto utiliza conceitos fundamentais de programação, sem necessidade de bibliotecas avançadas.

---

## ▶️ Como executar

### Pré-requisitos

Ter o Python 3 instalado no computador.

### Passo 1 – Baixar o projeto

Clone o repositório utilizando o Git:

```bash
git clone URL_DO_REPOSITORIO
```

Ou faça o download do projeto em formato ZIP pelo GitHub.

### Passo 2 – Acessar a pasta

Abra o terminal na pasta principal do projeto.

### Passo 3 – Executar o sistema

Execute o arquivo principal:

```bash
python main.py
```

O programa realizará as análises e apresentará os resultados no terminal.

---

## 💻 Exemplo de entrada e saída

O exemplo abaixo representa uma execução ilustrativa do sistema integrado.

### Entrada

```text
Geração de energia: 40
Consumo energético: 70
Reserva disponível: 100
Velocidade do vento: 11 m/s
```

### Saída

```text
===== AURORA SIGER =====
Sistema Integrado da Colônia

ANÁLISE ENERGÉTICA
Geração: 40
Consumo: 70
Déficit energético: 30
Reserva disponível: 100

ALERTA: consumo superior à geração.

DECISÃO AUTOMÁTICA
Recomendação: reduzir consumo.
Prioridade: manter sistemas essenciais.

PREVISÃO ENERGÉTICA
Velocidade do vento: 11 m/s
Geração eólica estimada: 27

STATUS: monitoramento concluído.
```

Os resultados podem variar conforme os dados utilizados na simulação.

---

## 🧠 Conceitos aplicados

O projeto reúne conhecimentos trabalhados ao longo da fase:

| Conceito | Aplicação |
|---|---|
| Estruturas de dados | Organização dos recursos e subsistemas |
| Lógica de programação | Aplicação de regras e condições |
| Funções | Separação e reutilização de operações |
| Regressão linear | Previsão de geração energética |
| Energia renovável | Análise de geração solar e eólica |
| Integração de sistemas | Comunicação entre módulos Python |

---

## 🌱 Benefícios para a colônia

O Aurora Siger contribui para:

- Melhor organização dos recursos;
- Identificação antecipada de situações de risco;
- Redução de desperdícios energéticos;
- Priorização dos sistemas essenciais;
- Planejamento do uso de energia;
- Apoio à tomada de decisões.

O sistema representa a evolução de um monitoramento reativo para um gerenciamento que também utiliza previsões.

---

## 👥 Equipe

Projeto desenvolvido por estudantes de Ciência da Computação da FIAP.

**Integrantes:**
- Abner Miranda Romão - rm 576928
-Bianca Pavan Andre - rm 574521
-Beatriz Lopes de Lima - rm 575983
-Gabriel Eduardo Alvite Mendes - rm 576675
-Reinaldo Dias Esteves Macieira Junior - rm 576318


---

## 📚 Considerações finais

O desenvolvimento do Aurora Siger demonstra como conceitos fundamentais de programação, estruturas de dados, lógica matemática e regressão linear podem ser integrados para resolver problemas de gerenciamento de recursos.

Por meio da análise das condições da colônia, o sistema permite gerar alertas, recomendar ações e estimar comportamentos futuros, contribuindo para uma operação mais segura, organizada e eficiente.

**FIAP – Ciência da Computação | Fase 3 | 2026**

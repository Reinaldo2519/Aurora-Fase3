Previsão de Energia por Regressão Linear
Responsável: Abner Miranda Romão

Funcionalidade: previsão da geração eólica e solar da colônia Aurora Siger
1. Objetivo e organização dos dados
A funcionalidade desenvolvida utiliza regressão linear simples para estimar a geração de duas fontes de energia da colônia:
·	geração eólica, usando a velocidade do vento como variável de entrada;
·	geração solar, usando o horário do dia como variável de entrada.
A implementação utiliza Pandas, NumPy, Matplotlib e Scikit-learn, seguindo a abordagem estudada em aula. Os dados históricos permanecem centralizados em dados.py e são consultados por meio da função obter_valor() de acesso.py.
Dados eólicos
Vento (m/s)	Geração eólica (kW)
8	20
10	25
9	22
12	30
10	25
12	30
11	27
13	33

Para o modelo eólico:
X = df[["vento_ms"]]
y = df["geracao_eolica_kw"]

Dados solares
Horário	Hora numérica	Geração solar (kW)
06:00	6,0	5
07:00	7,0	14
08:00	8,0	26
09:00	9,0	38
10:00	10,0	47
11:00	11,0	52
12:00	12,0	54
13:00	13,0	53

Os horários no formato HH:MM são convertidos em horas decimais. Por exemplo, 06:00 torna-se 6,0 e 13:30 torna-se 13,5.
Para o modelo solar:
X = df[["hora_numerica"]]
y = df["geracao_solar_kw"]

O horário foi usado porque o conjunto atual não possui irradiância solar ou cobertura de nuvens. Portanto, o horário funciona como uma aproximação da incidência solar e essa escolha representa uma limitação do modelo.
2. Modelos matemáticos e implementação
A equação geral da regressão linear simples é:
ŷ = β₀ + β₁x

Onde ŷ é a geração prevista, β₀ é o intercepto, β₁ é a inclinação e x é a variável de entrada.
Os modelos são criados e treinados com:
modelo = LinearRegression()
modelo.fit(X, y)

Modelo eólico
O modelo eólico obteve aproximadamente:
·	intercepto: -1,0314;
·	inclinação: 2,5912.
Equação:
geração eólica prevista = -1,0314 + 2,5912 × vento

A inclinação indica que, dentro dos dados analisados, cada aumento de 1 m/s no vento está associado a aproximadamente 2,59 kW adicionais de geração prevista.
Para 14 m/s, a previsão é:
geração eólica prevista ≈ 35,25 kW

Como a capacidade eólica cadastrada é de 40 kW, essa previsão pode ser apresentada sem redução.
Modelo solar
O modelo solar obteve aproximadamente:
·	intercepto: -34,3333;
·	inclinação: 7,4167.
Equação:
geração solar prevista = -34,3333 + 7,4167 × hora

Para 14:00, a regressão produz uma previsão bruta de:
geração solar prevista bruta = 69,50 kW

Entretanto, os painéis possuem capacidade cadastrada de 60 kW. Por isso, a previsão final é limitada a:
geração solar prevista = 60,00 kW

As previsões são limitadas entre zero e a capacidade máxima do subsistema. O valor bruto também é mantido no retorno da função, permitindo explicar a diferença entre o resultado matemático e o limite operacional.
3. Métricas, resíduos e gráficos
Foram utilizadas duas métricas de avaliação:
·	MSE, erro médio quadrático;
·	R², coeficiente de determinação.
Resultados do modelo eólico
MSE = 0,0692
R² = 0,9959

O baixo MSE mostra que as previsões eólicas ficaram próximas dos dados históricos. O R² indica que aproximadamente 99,59% da variação da geração eólica nesta amostra é explicada pelo vento no modelo linear.
Resultados do modelo solar
MSE = 28,5729
R² = 0,9100

O modelo solar também apresenta uma relação forte com o horário dentro da amostra. Entretanto, o MSE é maior e os valores entre 11:00 e 13:00 mostram estabilização, enquanto uma reta continua crescendo. Isso demonstra uma limitação da regressão linear para representar o ciclo solar completo.
Os resíduos são calculados por:
residuos = y - y_pred

Um resíduo positivo indica que o valor observado ficou acima da previsão. Um resíduo negativo indica que ficou abaixo. Resíduos próximos de zero indicam maior proximidade entre observação e previsão.
O módulo gera quatro gráficos:
·	grafico_regressao_eolica.png;
·	grafico_residuos_eolicos.png;
·	grafico_regressao_solar.png;
·	grafico_residuos_solares.png.
Os gráficos de regressão mostram os valores observados e a reta ajustada. Os gráficos de resíduos mostram a distribuição dos erros em torno da linha zero.
4. Testes, integração e limitações
O arquivo testes_previsao.py verifica:
1.	conversão de horários para valores decimais;
2.	organização dos oito registros eólicos;
3.	organização dos oito registros solares;
4.	coeficientes, MSE e R² do modelo eólico;
5.	coeficientes, MSE e R² do modelo solar;
6.	previsão eólica para 14 m/s;
7.	previsão solar para 14:00;
8.	aplicação das capacidades máximas de 40 kW e 60 kW;
9.	rejeição de ventos e horários inválidos;
10.	criação dos quatro gráficos.
Execução dos testes:
python testes_previsao.py

Saída esperada:
OK: todos os testes de previsao eolica e solar passaram.

As funções destinadas à integração são:
prever_geracao_eolica(COLONIA, vento_ms)
prever_geracao_solar(COLONIA, horario)

Os dados são simulados e possuem apenas oito registros, das 06:00 às 13:00. A previsão eólica para 14 m/s e a previsão solar para 14:00 são extrapolações, pois ultrapassam as faixas observadas no treinamento.
Na geração solar, o horário não substitui uma medição real de irradiância. Em uma aplicação mais completa, seria recomendável incluir irradiância solar, cobertura de nuvens, temperatura dos painéis e eficiência do equipamento. Além disso, a geração solar não cresce de forma linear ao longo do dia: após o pico, ela tende a diminuir. Consequentemente, o modelo solar deve ser entendido como aplicação acadêmica da regressão linear simples aos dados disponíveis.

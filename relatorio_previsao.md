# Previsão de Energia por Regressão Linear

**Responsável:** Abner Miranda Romão  
**Funcionalidade:** previsão da geração de energia eólica a partir da velocidade do vento

## 1. Objetivo e organização dos dados

A funcionalidade desenvolvida tem como objetivo estimar a geração de energia eólica da colônia a partir de uma nova velocidade do vento. Para isso, foi aplicada uma regressão linear simples com Pandas, NumPy, Matplotlib e Scikit-learn, seguindo a abordagem estudada em aula.

A velocidade do vento foi escolhida como variável independente, representada por `X`, porque é o dado utilizado como entrada do modelo. A geração de energia eólica foi escolhida como variável dependente, representada por `y`, porque é o valor que o sistema deve estimar.

Os dados históricos já armazenados no projeto são obtidos por meio da função `obter_valor()` do arquivo `acesso.py`. Dessa forma, o módulo de previsão utiliza as informações existentes em `dados.py` e não cria uma cópia separada dos dados.

| Velocidade do vento (m/s) | Geração eólica observada (kW) |
|---:|---:|
| 8 | 20 |
| 10 | 25 |
| 9 | 22 |
| 12 | 30 |
| 10 | 25 |
| 12 | 30 |
| 11 | 27 |
| 13 | 33 |

As duas séries são organizadas em um `DataFrame`:

```python
dados = {
    "vento_ms": ventos,
    "geracao_eolica_kw": geracoes,
}

df = pd.DataFrame(dados)
```

Depois, as variáveis são separadas:

```python
X = df[["vento_ms"]]
y = df["geracao_eolica_kw"]
```

`X` utiliza dois colchetes porque o Scikit-learn espera os dados de entrada em uma estrutura bidimensional. A variável `y` contém a série que será prevista.

## 2. Modelo matemático e implementação

A regressão linear simples procura uma reta que represente a relação entre duas variáveis. A equação geral é:

```text
ŷ = β₀ + β₁x
```

Onde:

- `ŷ` representa a geração eólica prevista;
- `β₀` representa o intercepto da reta;
- `β₁` representa a inclinação da reta;
- `x` representa a velocidade do vento.

O modelo foi criado e treinado com:

```python
modelo = LinearRegression()
modelo.fit(X, y)
```

Após o treinamento, foram obtidos aproximadamente os seguintes parâmetros:

- intercepto `β₀ = -1,0314`;
- inclinação `β₁ = 2,5912`.

Portanto, a equação estimada foi:

```text
geração prevista = -1,0314 + 2,5912 × vento
```

A inclinação indica que, dentro da faixa analisada, cada aumento de `1 m/s` na velocidade do vento está associado a um aumento aproximado de `2,59 kW` na geração prevista.

O intercepto negativo não significa que uma turbina produzirá energia negativa. O intercepto é o ponto matemático em que a reta ajustada cruza o eixo vertical. Por esse motivo, o código impede que uma previsão negativa seja apresentada como geração válida.

A função principal do módulo é:

```python
prever_geracao_eolica(colonia, vento_ms)
```

A função valida a nova velocidade, treina o modelo com os dados históricos e utiliza `modelo.predict()` para calcular a estimativa.

## 3. Predição, métricas e resíduos

Para uma velocidade do vento de `14 m/s`, o cálculo aproximado é:

```text
geração prevista = -1,0314 + 2,5912 × 14
geração prevista ≈ 35,25 kW
```

O modelo também foi avaliado por meio do erro médio quadrático, MSE, e do coeficiente de determinação, R².

O resultado do MSE foi aproximadamente:

```text
MSE = 0,0692
```

O MSE representa a média dos quadrados das diferenças entre os valores observados e os valores previstos. Para os dados analisados, o valor baixo mostra que as estimativas ficaram próximas das observações.

O resultado do R² foi aproximadamente:

```text
R² = 0,9959
```

Esse resultado indica que aproximadamente `99,59%` da variação da geração eólica presente nesta amostra é explicada pela velocidade do vento no modelo linear. Isso não significa que o modelo tenha `99,59%` de precisão em qualquer situação real. A métrica descreve apenas o ajuste aos dados usados no treinamento.

Os resíduos são calculados pela diferença entre os valores observados e os valores previstos:

```python
residuos = y - y_pred
```

Um resíduo positivo indica que o valor observado ficou acima da previsão. Um resíduo negativo indica que o valor observado ficou abaixo da previsão. Resíduos próximos de zero indicam que o ajuste ficou próximo dos dados históricos.

O módulo gera dois arquivos de imagem:

- `grafico_regressao_eolica.png`, com os pontos observados e a reta ajustada;
- `grafico_residuos_eolica.png`, com a distribuição dos resíduos em relação às previsões.

## 4. Testes, resultados e limitações

O arquivo `testes_previsao.py` verifica os seguintes pontos:

1. organização dos oito registros históricos no `DataFrame`;
2. presença das colunas `vento_ms` e `geracao_eolica_kw`;
3. valores esperados do intercepto e da inclinação;
4. resultados esperados do MSE e do R²;
5. previsão de aproximadamente `35,25 kW` para `14 m/s`;
6. rejeição de vento negativo;
7. rejeição de texto, valor booleano, `NaN` e infinito como entrada;
8. criação válida dos dois gráficos.

A execução esperada é:

```bash
python testes_previsao.py
```

Saída esperada:

```text
OK: todos os testes de previsao passaram.
```

Também é possível executar:

```bash
python previsao.py
```

O resultado aproximado será:

```text
=== PREVISAO DE ENERGIA EOLICA ===
Equacao: y = -1.0314 + 2.5912x
MSE: 0.0692
R2: 0.9959
Vento informado: 14.00 m/s
Geracao prevista: 35.25 kW
```

Os dados utilizados são simulados e possuem somente oito registros, com velocidades entre `8` e `13 m/s`. A previsão para `14 m/s` já representa uma pequena extrapolação. Valores muito distantes da faixa histórica devem ser interpretados com cautela.

Em uma aplicação real, a geração também pode sofrer influência da direção do vento, densidade do ar, temperatura, características da turbina, manutenção e limite de capacidade do equipamento. Portanto, o modelo desenvolvido é uma aplicação acadêmica de regressão linear simples e não uma representação completa do comportamento físico de uma turbina real.

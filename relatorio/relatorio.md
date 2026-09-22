# Pipeline de ML, Otimização e Decisão de Manutenção — Complexo Petroquímico

**Dataset:** `petrochemical_advanced_data.csv` — 10.000 registros, 16 colunas, janeiro de 2020 a julho de 2024  
**Integrantes:**  
- Elton Vinicios Almeida de Oliveira — RM 562187  
- Emerson dos Santos Silva — RM 562033  
- Kelvin Douglas Ribeiro Rabelo — RM 561538  
- Pedro Henrique Simão Soares — RM 562283  
- Vitor Lucas Mattos de Brito Mariano — RM 562116

## 1. Entendimento do negócio

O trabalho busca uma configuração operacional que reduza a intensidade energética sem produzir menos que o nível de referência e, em seguida, compara alternativas de manutenção. Há quatro decisões operacionais: vazão, temperatura, pressão e abertura de válvula. A condição do equipamento é representada por saúde do sensor, vibração e idade/tipo do catalisador.

| Variável | Classe | Uso |
|---|---|---|
| Feedstock_Flow_m3h | Controlável | Variável de decisão |
| Reactor_Temp_C | Controlável | Variável de decisão |
| Reactor_Pressure_Bar | Controlável | Variável de decisão |
| Valve_Opening_Percent | Controlável | Variável de decisão |
| Sensor_Health_Index | Estado | Indicador de condição; não prova falha |
| Vibration_Level_mm_s | Estado | Indicador de condição mecânica |
| Catalyst_Age_Days / Catalyst_Type | Estado | Condição do catalisador |
| Unit_Name | Estado categórico | Unidade produtiva |
| Ambient_Temp_C / Timestamp | Externa | Ambiente e sazonalidade |
| Electricity_MWh / Natural_Gas_m3h / Steam_Tons_h | Resultado pós-operação | Excluídas dos modelos operacionais |
| Product_Yield_Tons | Target | Produção por intervalo de quatro horas |
| Energy_Intensity | Target | Intensidade energética por tonelada |

Regras adotadas: validação temporal; targets e medições pós-operação fora das features; limites calculados na própria unidade; restrição de produção; restrição de proximidade a configurações observadas; custos e risco tratados como premissas didáticas.

## 2. Dados e Machine Learning

### 2.1 Qualidade e exploração

A base não possui nulos, duplicatas completas nem timestamps duplicados. As leituras estão espaçadas em quatro horas e distribuídas de forma equilibrada entre três unidades. As médias dos targets também são semelhantes entre unidades. Vazão e saúde apresentam as associações mais fortes com produção e energia. Temperatura, pressão e válvula têm importância preditiva pequena dentro do domínio observado.

Foram criadas features cíclicas de hora e mês. `Unit_Name` e `Catalyst_Type` receberam one-hot encoding. A auditoria também identificou a interação pré-operacional `Feedstock_Flow_m3h × Sensor_Health_Index`.

### 2.2 Target leakage

A auditoria encontrou a identidade exata, com erro numérico máximo de `1,78 × 10⁻¹⁵`:

`Energy_Intensity = (3,6 × Electricity_MWh + 0,035 × Natural_Gas_m3h) / Product_Yield_Tons`

Portanto, eletricidade, gás e produção não podem prever intensidade energética numa decisão anterior à operação. `Steam_Tons_h` não participa dessa fórmula, corrigindo a interpretação da versão anterior, mas também é uma medição pós-operação e foi excluída.

Foi encontrada ainda a identidade exata, com erro máximo de `2,84 × 10⁻¹⁴`:

`Product_Yield_Tons = 0,18 × Feedstock_Flow_m3h × Sensor_Health_Index`

Como vazão e saúde estão disponíveis antes da operação, a interação não é leakage. Ela revela, porém, que a produção da base é sintética e determinística.

### 2.3 Validação e resultados

Os primeiros 80% formam a janela de desenvolvimento e os 20% finais permanecem intocados até a avaliação final. Dentro do desenvolvimento, 70% ajustam o modelo operacional e 10% calibram a incerteza. Três folds walk-forward expansivos (`5.000→1.000`, `6.000→1.000` e `7.000→1.000`) verificam estabilidade sem usar o teste final.

| Target | Modelo | R² | MAE | RMSE |
|---|---|---:|---:|---:|
| Energy_Intensity | Linear Regression | 0,6801 | 0,2810 | 0,3472 |
| Energy_Intensity | Random Forest | 0,6825 | 0,2794 | 0,3459 |
| Energy_Intensity | Gradient Boosting | 0,6888 | 0,2766 | 0,3424 |
| Energy_Intensity | **Híbrido físico** | **0,6930** | **0,2761** | **0,3401** |
| Product_Yield_Tons | **Linear + interação** | **1,0000** | **0,0000** | **0,0000** |
| Product_Yield_Tons | Random Forest | 0,9999 | 0,0126 | 0,1250 |
| Product_Yield_Tons | Gradient Boosting | 0,9999 | 0,1092 | 0,1678 |
| Product_Yield_Tons | **Híbrido físico** | **1,0000** | **0,0000** | **0,0000** |

No walk-forward de energia, Gradient Boosting e híbrido ficam tecnicamente empatados: RMSE médio `0,3311 ± 0,0050` e `0,3312 ± 0,0049`, respectivamente. No teste final, o híbrido alcança RMSE `0,3401`, contra `0,3424` do Gradient Boosting. Ele foi escolhido pela coerência algébrica e interpretabilidade, não por ajuste ao teste.

A janela separada de 1.000 registros calibrou uma margem conformal absoluta de 90% igual a `0,552`. No teste final, o intervalo cobriu `89,4%` das observações, valor próximo dos 90% nominais. Para produção, a margem é apenas erro numérico (`1,42 × 10⁻¹⁴`).

A interação de vazão e saúde domina a previsão de produção. Essa relação determinística descreve como a base foi construída, mas não demonstra que uma manutenção real causará toda a recuperação simulada.

## 3. Otimização

### 3.1 Formulação

Seja `x = (Valve_Opening, Feedstock_Flow, Reactor_Temp, Reactor_Pressure)`. Para cada estado do equipamento:

```text
min  EI_hat(x | estado) + 10⁻⁴ D(x, x_atual)

sujeito a:
Yield_hat(x | estado) >= 64,37 ton/4h
x entre p1 e p99 do histórico da unidade
distância conjunta até uma configuração observada <= p99 histórico
```

O termo de movimento apenas desempata soluções em favor de ajustes menores. Usamos `scipy.optimize.differential_evolution` porque a razão de energia e a restrição de vizinhança tornam o problema não linear. Uma busca aleatória com 10.000 candidatos e uma LP com surrogates lineares funcionam como verificações independentes. A distância de suporte combina setpoints, saúde, vibração e idade do catalisador dentro do mesmo ativo/unidade.

### 3.2 Caso de estudo e estado pós-manutenção

O caso não foi escolhido manualmente. Ele é o maior escore de degradação no período de teste, combinando baixa saúde (50%), alta vibração (35%) e idade do catalisador (15%): Ammonia_Unit_02 em 12/05/2024, saúde 0,578, vibração 8,126 mm/s e catalisador com 348 dias.

O estado pós-manutenção também deixou de combinar percentis extremos artificiais. Ele é uma observação real e central de um grupo saudável da mesma unidade e catalisador no treino: saúde 0,970, vibração 1,749 mm/s e 58 dias.

### 3.3 Solução

| Variável | Sem manutenção | Manutenção imediata |
|---|---:|---:|
| Valve Opening (%) | 79,91 | **79,53** |
| Feedstock Flow (m³/h) | 694,11 | **694,11** |
| Reactor Temperature (°C) | 789,03 | **795,14** |
| Reactor Pressure (bar) | 33,36 | **33,32** |
| Energy Intensity prevista | 3,106 | **1,849** |
| Product Yield previsto (ton/4h) | 72,20 | **121,25** |
| Distância de suporte condicionado | 2,032 | **1,035** |
| Limite de suporte | 2,032 | 2,032 |

As duas soluções satisfazem a produção mínima e permanecem na região conjunta condicionada ao estado. A solução sem manutenção fica próxima do limite de suporte; a solução pós-manutenção permanece mais central. Como o numerador energético não é previsível com as entradas disponíveis, minimizar intensidade equivale principalmente a elevar a produção. Temperatura, pressão e válvula não devem ser interpretadas como alavancas comprovadas de economia.

### 3.3 Alternativas por faixa de produção

A fronteira estrita energia–produção colapsa em um ponto, pois o numerador energético é aproximadamente constante e a intensidade cai quando a produção aumenta. Para evitar operar sempre no extremo, foram calculadas metas de produção pós-manutenção com faixa de tolerância de 2%:

| Meta relativa à produção atual | Flow | Yield | EI | Distância de suporte |
|---:|---:|---:|---:|---:|
| 140% | 526,21 | 91,92 | 2,439 | 0,799 |
| 150% | 563,79 | 98,48 | 2,276 | 0,903 |
| 160% | 601,38 | 105,05 | 2,134 | 0,929 |
| 165% | 620,17 | 108,33 | 2,069 | 0,968 |

Essas alternativas permitem escolher capacidade e intensidade conforme a margem operacional, em vez de aceitar automaticamente a configuração de maior produção.

### 3.4 Otimização robusta

A formulação robusta minimiza o limite superior conformal de intensidade e exige o limite inferior de produção acima da meta. Com manutenção, a intensidade passa de `1,849` nominal para limite superior `2,401`; sem manutenção, de `3,105` para `3,657`. Os setpoints não mudam porque a margem energética calibrada é global e aditiva, enquanto o erro de produção é numericamente zero. Assim, a robustez altera a garantia reportada, não o ponto ótimo.

### 3.5 Validação linear

O `linprog` encontra Flow 694,11; Valve 94,36; Temp 719,43; Pressure 25,35; EI linear 2,765 e Yield linear 72,20. Ele confirma que a vazão domina o surrogate linear. Como a LP simplifica a razão energética e a geometria do histórico, ela é validação de direção, não a recomendação principal.

## 4. Decisão de manutenção

Os cenários cobrem 30 dias ou 180 intervalos. A manutenção ocupa dois intervalos; a postergada ocorre após 15 dias. Foram assumidos R$ 130 por unidade de energia, manutenção imediata de R$ 45 mil, planejada de R$ 25 mil e falha de R$ 300 mil.

| Cenário | Produção (ton) | Energia (unid.) | Energia (R$) | Manutenção (R$) | Exposição a falha (R$) | Total parcial (R$) | Parcial/ton (R$) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Sem manutenção | 12.996,56 | 40.350,05 | 5.245.506,13 | 0 | 190.617,62 | 5.436.123,76 | 418,27 |
| **Manutenção imediata** | **21.582,06** | **39.901,71** | **5.187.222,73** | **45.000,00** | **28.606,89** | **5.260.829,62** | **243,76** |
| Manutenção postergada | 17.168,06 | 39.901,71 | 5.187.222,73 | 25.000,00 | 109.294,40 | 5.321.517,13 | 309,97 |

No horizonte fixo, a manutenção imediata reduz o custo parcial em R$ 175.294,14. Variando isoladamente preço de energia, manutenção e falha em ±30%, a economia permanece positiva entre aproximadamente R$ 127 mil e R$ 224 mil. A produção, entretanto, é muito diferente entre os cenários.

### 4.1 Mesma produção e sensibilidade causal

Para entregar as mesmas 10 mil toneladas, o cenário sem manutenção leva 23,08 dias e custa parcialmente R$ 4.182.742,08; o cenário imediato leva 14,08 dias, incluindo a parada, e custa R$ 2.461.596,30. Essa diferença depende diretamente da recuperação de saúde assumida.

| Recuperação assumida | Saúde | Yield (ton/4h) | EI | Economia vs. não manter (R$) |
| 0% | 0,58 | 72,20 | 3,11 | -45.000 |
| 25% | 0,68 | 84,46 | 2,65 | 588.821 |
| 50% | 0,77 | 96,73 | 2,32 | 1.061.953 |
| 75% | 0,87 | 108,99 | 2,06 | 1.428.630 |
| 100% | 0,97 | 121,25 | 1,85 | 1.721.146 |

Interpolando os cenários, a recuperação mínima para empatar fica em aproximadamente **1,8%**. Sem recuperação, a intervenção perde exatamente seu custo de R$ 45 mil. Portanto, o resultado deve ser apresentado como limiar condicionado ao efeito da manutenção, não como ganho causal demonstrado.

Esse resultado é condicional, não um business case real. O dataset não contém preço do produto, margem, custo completo de parada, estoque, demanda ou penalidades. Além disso, o índice de risco foi convertido em probabilidade por premissa; ele não foi calibrado com falhas. No horizonte fixo, o consumo absoluto previsto por intervalo é praticamente constante: a melhora da intensidade vem principalmente do aumento de produção.

O Isolation Forest coloca o estado degradado no percentil 0,44 de normalidade do treino e a referência saudável no percentil 20,11. Isso mostra que o primeiro estado é raro; não estima risco de falha nem prova causalidade.

## 5. Automação

| Decisão | Automação recomendada | Justificativa |
|---|---|---|
| Qualidade de dados, scores e alertas | Automática | Alta frequência e reversibilidade |
| Sugestão de setpoints | Automática supervisionada | Aplicar com limites oficiais e rollback |
| Parada para manutenção | Recomendação automática e aprovação humana | Segurança, custo e risco não calibrado |

Benefícios: velocidade, escala, consistência, monitoramento contínuo e menor tempo até detectar degradação. Riscos: falsos positivos/negativos, sensores incorretos, erro de modelo, drift, extrapolação e impacto de uma parada indevida.

## 6. Pipeline final

```text
Dados → qualidade e EDA → features sem leakage → walk-forward
      → calibração conformal → teste final → diagnóstico de suporte
      → otimização nominal/robusta → cenários → custo/risco
      → recomendação → aprovação humana de manutenção
```

## 7. Tabela final de decisão

| Campo | Recomendação |
|---|---|
| Feedstock Flow | 694,11 m³/h |
| Reactor Temperature | 795,14 °C |
| Reactor Pressure | 33,32 bar |
| Valve Opening | 79,53% |
| Expected Yield | 121,25 ton/4h |
| Energy Intensity | 1,849; limite superior conformal de 90% = 2,401 |
| Energy Cost | R$ 5.187.222,73 em 30 dias |
| Maintenance | **Sim, condicionada à inspeção humana** |
| Maintenance Cost | R$ 45.000,00 — premissa |
| Total Cost | R$ 5.260.829,62 — parcial e ilustrativo |
| Automação | Setpoints supervisionados; manutenção com aprovação humana |

## 8. Conclusão

**Qual configuração foi recomendada?** A tabela acima, depois de conferida contra os limites oficiais de engenharia. Ela mantém a produção mínima e permanece próxima de configurações históricas.

**A manutenção deve ser realizada?** O sistema deve recomendar inspeção imediata. Se os sensores e a degradação forem confirmados, realizar a manutenção. O dataset não justifica parada totalmente automática.

**Qual o impacto econômico?** No cenário didático, economia parcial de aproximadamente R$ 175 mil em 30 dias. Em uma meta comum de 10 mil toneladas, a diferença pode chegar a R$ 1,72 milhão, mas somente sob recuperação integral do estado. Com efeito nulo, a manutenção perde R$ 45 mil. O valor exclui receitas e custos empresariais relevantes.

**Quais os riscos?** Erro do modelo de energia, qualidade dos sensores, mudança de processo, extrapolação, premissas financeiras e ausência de dados reais de falha/manutenção.

**Automática ou humana?** Monitoramento e setpoints com automação supervisionada; manutenção com aprovação humana.

**Quais dados faltam para produção?** Falhas e ordens de manutenção; condição antes/depois das intervenções; limites de engenharia; preços por fonte de energia; duração e custo das paradas; valor e margem do produto; demanda, estoque e penalidades contratuais.

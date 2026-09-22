# Guia de estudo — Pipeline de ML, Otimização e Decisão de Manutenção

Este documento explica o trabalho de forma didática. A ideia é ajudar você a entender o que foi feito, por que cada etapa existe e como explicar as decisões durante a apresentação.

## Como relacionar este guia ao que o professor solicitou

O enunciado possui oito partes obrigatórias. Use esta tabela como mapa de navegação:

| Item solicitado pelo professor | O que precisa ser entregue | Onde estudar neste guia | Onde está no trabalho |
|---|---|---|---|
| **1. Entendimento do negócio** | Objetivo, variáveis, restrições, regras e tabela de classificação | Seções 1, 2 e 3 | Notebook e relatório, seção 1 |
| **2. Machine Learning** | Dois modelos por target, comparação, escolha e leakage | Seções 4 a 8 | Notebook e relatório, seção 2 |
| **3. Otimização** | Decisões, objetivo, restrições, limites, solver, solução e interpretação | Seções 9 a 14 | Notebook e relatório, seção 3 |
| **4. Decisão de manutenção** | Cenários sem manutenção, imediata e postergada | Seções 15 a 18 | Notebook e relatório, seção 4 |
| **5. Automação da decisão** | Benefícios, riscos e nível de automação | Seções 19 e 20 | Notebook e relatório, seção 5 |
| **6. Pipeline final** | Fluxo completo dos dados até a decisão | Seções 1 e 20 | Notebook e relatório, seção 6 |
| **7. Resultado final** | Tabela com configuração, produção, energia, custos e manutenção | Seções 14 e 17 | Notebook e relatório, seção 7 |
| **8. Conclusão** | Responder às seis perguntas finais | Seções 21 a 24 | Notebook e relatório, seção 8 |

Os três entregáveis pedidos são:

| Entregável | Arquivo |
|---|---|
| Notebook executável | `notebook/pipeline_petroquimico.ipynb` |
| Relatório metodológico | `relatorio/relatorio.md` e `relatorio/relatorio.pdf` |
| Apresentação de 10–15 minutos | `apresentacao/apresentacao.pptx` e `apresentacao/roteiro_apresentacao.md` |

Ao encontrar a indicação **“Item X do enunciado”**, você saberá exatamente qual exigência está sendo estudada.

## 1. Qual é o problema?

**Referência: objetivo geral, item 1 e item 6 do enunciado.**

Uma planta petroquímica precisa definir valores operacionais como vazão, temperatura, pressão e abertura de válvula. Esses valores influenciam quanto a planta produz e quanta energia consome por tonelada produzida.

O trabalho responde a duas perguntas:

1. Qual configuração operacional reduz a intensidade energética sem diminuir a produção?
2. Diante da condição do equipamento, vale realizar manutenção? Essa decisão pode ser automática?

O fluxo completo é:

```text
Dados históricos
    ↓
Entendimento e qualidade dos dados
    ↓
Machine Learning
    ↓
Previsão de produção e intensidade energética
    ↓
Otimização dos parâmetros operacionais
    ↓
Cenários de manutenção
    ↓
Análise de custo e risco
    ↓
Recomendação com aprovação humana
```

Machine Learning e otimização cumprem papéis diferentes. O modelo de ML aprende a prever o comportamento da planta. O otimizador usa essas previsões para procurar uma configuração operacional melhor.

## 2. O que existe no dataset?

**Referência: item 1 — entendimento do negócio e classificação das variáveis.**

A base possui 10.000 registros, 16 colunas e medições a cada quatro horas entre janeiro de 2020 e julho de 2024. Existem três unidades:

- `Ammonia_Unit_02`;
- `Ethylene_Plant_01`;
- `Methanol_Complex_03`.

Não foram encontrados valores nulos, linhas duplicadas ou timestamps duplicados.

### Variáveis controláveis

São os valores que a operação pode ajustar e que se tornam variáveis de decisão:

| Variável | Significado |
|---|---|
| `Feedstock_Flow_m3h` | Vazão de matéria-prima em m³/h |
| `Reactor_Temp_C` | Temperatura do reator em °C |
| `Reactor_Pressure_Bar` | Pressão do reator em bar |
| `Valve_Opening_Percent` | Percentual de abertura da válvula |

### Variáveis de estado

Descrevem a unidade e a condição do equipamento:

| Variável | Significado |
|---|---|
| `Sensor_Health_Index` | Índice de saúde do sensor/equipamento |
| `Vibration_Level_mm_s` | Nível de vibração |
| `Catalyst_Age_Days` | Idade do catalisador |
| `Catalyst_Type` | Tipo de catalisador |
| `Unit_Name` | Unidade produtiva |

### Variáveis externas

Não são controladas diretamente pela operação:

- temperatura ambiente;
- hora do dia;
- mês do ano.

### Targets

Os modelos precisam prever:

- `Product_Yield_Tons`: produção por intervalo de quatro horas;
- `Energy_Intensity`: energia consumida por tonelada produzida.

## 3. O que foi feito na análise exploratória?

**Referência: item 6 — etapa EDA do pipeline; também sustenta os itens 1 e 2.**

A análise exploratória, ou EDA, verifica a qualidade dos dados e procura relações úteis.

Foram analisados:

- quantidade de registros e período coberto;
- nulos e duplicatas;
- distribuição dos targets;
- comportamento por unidade;
- correlações entre variáveis;
- relação da vazão com a produção;
- relação da saúde do equipamento com a intensidade energética.

As três unidades possuem quantidades semelhantes de registros e médias próximas dos targets. Isso reduz a chance de uma unidade dominar o treinamento apenas por possuir mais dados.

Os padrões mais fortes são:

- maior vazão tende a acompanhar maior produção;
- melhor índice de saúde tende a acompanhar maior produção e menor intensidade energética;
- temperatura, pressão e válvula possuem influência preditiva pequena dentro das faixas observadas.

Essa conclusão é associativa. Ela não prova que alterar uma variável causará, sozinha, todo o efeito previsto.

## 4. O que é Feature Engineering?

**Referência: item 6 — etapa Feature Engineering do pipeline.**

Feature Engineering é transformar dados brutos em entradas mais adequadas aos modelos.

Hora e mês são variáveis cíclicas. Por exemplo, 23h está perto de 0h, apesar dos números 23 e 0 parecerem distantes. Para representar corretamente esse ciclo, foram criadas combinações de seno e cosseno:

```text
hour_sin, hour_cos, month_sin, month_cos
```

As variáveis categóricas `Unit_Name` e `Catalyst_Type` foram transformadas por one-hot encoding. Nessa técnica, cada categoria vira uma coluna binária.

## 5. O que é target leakage e por que ele é importante?

**Referência: item 2 — exigência explícita de verificar possível target leakage nas variáveis de energia.**

Target leakage acontece quando o modelo recebe uma informação que contém direta ou indiretamente a resposta que ele deveria prever.

Foi encontrada a identidade exata:

```text
Energy_Intensity =
    (3,6 × Electricity_MWh + 0,035 × Natural_Gas_m3h)
    / Product_Yield_Tons
```

O erro máximo ao reconstruir o target com essa fórmula foi aproximadamente `1,78 × 10⁻¹⁵`, praticamente zero.

Isso significa que usar eletricidade, gás natural ou produção para prever `Energy_Intensity` seria entregar a resposta ao modelo. O desempenho pareceria excelente, mas o modelo não seria útil antes da operação, quando esses valores ainda não são conhecidos.

`Steam_Tons_h` não participa da fórmula. Mesmo assim, foi excluído porque também é uma medição posterior à decisão operacional.

A auditoria encontrou também:

```text
Product_Yield_Tons =
    0,18 × Feedstock_Flow_m3h × Sensor_Health_Index
```

Essa relação não é leakage, pois vazão e saúde são informações pré-operacionais. Ela mostra que a produção da base sintética é determinística e justifica o modelo híbrido.

Essa é uma das descobertas mais importantes do trabalho. Uma forma simples de explicá-la é:

> O modelo precisa decidir usando somente informações disponíveis antes da operação. Não pode usar medições que só aparecem depois que a produção já aconteceu.

## 6. Como os dados foram separados?

**Referência: item 2 — metodologia de treinamento e avaliação dos modelos.**

Os registros foram ordenados por data:

- primeiros 70%: ajuste do modelo operacional;
- 10% seguintes: calibração conformal;
- últimos 20%: teste final intocado.

O treinamento cobre 01/01/2020 a 26/08/2023. O teste cobre 26/08/2023 a 24/07/2024.

Foi escolhido um corte temporal porque, na prática, usamos o passado para prever o futuro. Uma divisão aleatória poderia misturar períodos futuros no treino e produzir uma avaliação otimista. Além disso, três folds walk-forward expansivos avaliam estabilidade somente dentro dos primeiros 80%.

## 7. Quais modelos foram comparados?

**Referência: item 2 — pelo menos dois modelos para cada target.**

Foram usados três modelos para cada target:

### Linear Regression

É o baseline. Assume que a resposta pode ser aproximada por uma combinação linear das entradas.

Vantagens:

- simples;
- rápido;
- interpretável;
- útil para entender a direção dos efeitos.

Limitação: não representa bem relações complexas ou curvas.

### Random Forest

Combina várias árvores de decisão. Cada árvore aprende regras diferentes e o resultado final é uma média.

Vantagens:

- captura relações não lineares;
- funciona bem com interações entre variáveis;
- costuma ser robusto a ruído.

Limitações:

- é menos interpretável;
- suas previsões formam regiões em degraus;
- não deve ser extrapolado para condições muito diferentes do treino.

### Gradient Boosting

Também combina árvores, mas cada nova árvore tenta corrigir os erros das anteriores.

Vantagem: consegue capturar relações não lineares com boa precisão.

Limitação: exige cuidado com parâmetros e generalização.

## 8. Como interpretar as métricas?

**Referência: item 2 — tabela de comparação e justificativa do modelo escolhido.**

| Métrica | Interpretação |
|---|---|
| R² | Quanto da variação do target o modelo explica. Quanto maior, melhor. |
| MAE | Erro absoluto médio, na unidade original do target. Quanto menor, melhor. |
| RMSE | Penaliza mais os erros grandes. Quanto menor, melhor. |

Resultados no teste temporal:

| Target | Modelo | R² | MAE | RMSE |
|---|---|---:|---:|---:|
| Energy | Linear Regression | 0,6801 | 0,2810 | 0,3472 |
| Energy | Gradient Boosting | 0,6888 | 0,2766 | 0,3424 |
| Energy | **Híbrido físico** | **0,6930** | **0,2761** | **0,3401** |
| Yield | Random Forest | 0,9999 | 0,0126 | 0,1250 |
| Yield | Gradient Boosting | 0,9999 | 0,1092 | 0,1678 |
| Yield | **Híbrido físico** | **1,0000** | **0,0000** | **0,0000** |

Escolhas finais:

- energia: modelo híbrido, com energia equivalente esperada dividida pela produção prevista;
- produção: identidade `0,18 × Flow × Health`.

O modelo de produção reproduz exatamente a estrutura sintética da base. O modelo de energia possui incerteza relevante. Sua previsão final de 1,849 deve ser interpretada junto com o RMSE de 0,340 e a margem conformal de 90% de 0,552. Essa margem cobriu 89,4% do teste final.

Uma forma de explicar isso é:

> O modelo prevê a direção e a ordem de grandeza da intensidade energética, mas não garante que o valor real será exatamente 1,849.

## 9. Como o caso degradado foi escolhido?

**Referência: item 3 e item 4 — definição do caso operacional usado na otimização e nos cenários.**

Não foi selecionada manualmente uma linha que favorecesse a conclusão. Foi construído um escore de degradação:

```text
Degradation Score =
    50% × baixa saúde
  + 35% × alta vibração
  + 15% × idade do catalisador
```

Depois, foi escolhido o maior escore no período de teste.

O caso encontrado pertence à `Ammonia_Unit_02`, em 12/05/2024:

| Indicador | Valor |
|---|---:|
| Sensor Health | 0,578 |
| Vibração | 8,126 mm/s |
| Idade do catalisador | 348 dias |
| Produção observada | 64,37 ton/4h |
| Energy Intensity observada | 3,575 |

Essa seleção reproduzível evita a impressão de que escolhemos o exemplo apenas porque ele gerava uma boa história.

## 10. Como foi construído o estado pós-manutenção?

**Referência: item 4 — condição do equipamento e impacto esperado da manutenção.**

A primeira versão combinava saúde no percentil 97, vibração no percentil 3 e idade de três dias. Embora cada valor existisse separadamente no histórico, a combinação completa era rara e foi classificada como anômala.

A abordagem foi corrigida. Agora o estado pós-manutenção vem de uma linha realmente observada no período de treinamento, da mesma unidade e do mesmo tipo de catalisador.

Primeiro foi criado um grupo com:

- saúde no quartil superior;
- vibração no quartil inferior;
- idade no quartil inferior.

Depois foi escolhida a observação mais próxima do centro desse grupo:

| Indicador | Atual | Referência saudável |
|---|---:|---:|
| Sensor Health | 0,578 | 0,970 |
| Vibração | 8,126 | 1,749 |
| Idade do catalisador | 348 | 58 |

Isso torna o cenário mais plausível. Ainda assim, o dataset não contém registros explícitos de manutenção. Portanto, essa mudança continua sendo uma simulação, não uma prova do efeito causal de uma intervenção.

## 11. Como o problema de otimização foi formulado?

**Referência: item 3 — variáveis de decisão, função objetivo, restrições e limites.**

As quatro variáveis de decisão formam o vetor:

```text
x = (
    Valve Opening,
    Feedstock Flow,
    Reactor Temperature,
    Reactor Pressure
)
```

O objetivo principal é minimizar a intensidade energética prevista:

```text
minimizar EI_hat(x | estado do equipamento)
```

Foi adicionado um termo muito pequeno que prefere mudanças menores nos setpoints quando duas configurações possuem praticamente a mesma previsão. Esse termo apenas desempata regiões planas do modelo.

### Restrições

1. A produção prevista deve ser pelo menos a produção observada no caso atual: 64,37 ton/4h.
2. Cada variável deve ficar entre os percentis 1 e 99 do histórico da unidade.
3. A combinação completa precisa estar próxima de alguma configuração realmente observada.

A terceira restrição é importante porque limites individuais não garantem uma combinação plausível. Por exemplo, temperatura e pressão podem ser aceitáveis separadamente, mas a combinação entre elas pode nunca ter ocorrido.

Os percentis e a proximidade histórica reduzem extrapolação. Eles não substituem os limites oficiais de segurança definidos por engenheiros de processo.

## 12. Por que foi usado differential evolution?

**Referência: item 3 — solver utilizado e justificativa para usar uma alternativa ao `linprog`.**

Os modelos escolhidos são ensembles de árvores. Eles são não lineares e possuem regiões em degraus, o que dificulta o uso de métodos baseados em derivadas.

`differential_evolution` é um algoritmo global que testa populações de soluções e não exige derivadas.

Também foi usado `linprog`, mas com modelos lineares auxiliares. Essa versão serve para verificar a direção dos efeitos e cumprir a comparação com programação linear. Ela não substitui o modelo principal porque simplifica demais as relações aprendidas.

## 13. Como a solução foi validada?

**Referência: item 3 — código, solução e sustentação da interpretação.**

Foram usadas três verificações:

1. O solver encontrou uma solução que satisfaz produção e suporte histórico.
2. Uma busca aleatória avaliou 10.000 configurações dentro dos mesmos limites.
3. Um problema linear foi resolvido com `linprog` usando surrogates lineares.

A busca aleatória encontrou resultados próximos aos do solver:

| Método | EI sem manutenção | EI com manutenção |
|---|---:|---:|
| Differential Evolution | 3,1055 | 1,8493 |
| Busca aleatória | 3,1056 | 1,8494 |

Como a busca independente chegou perto, diminui a chance de o resultado ser apenas um artefato do algoritmo.

O `linprog` escolheu valores de canto, comportamento comum em programação linear. Ele confirmou que a vazão possui o maior efeito marginal no modelo linear.

## 14. Qual configuração foi encontrada?

**Referência: item 3 e item 7 — solução operacional e tabela final de decisão.**

| Variável | Sem manutenção | Manutenção imediata |
|---|---:|---:|
| Feedstock Flow | 694,11 m³/h | **694,11 m³/h** |
| Reactor Temperature | 789,03 °C | **795,14 °C** |
| Reactor Pressure | 33,36 bar | **33,32 bar** |
| Valve Opening | 79,91% | **79,53%** |
| Expected Yield | 72,20 ton/4h | **121,25 ton/4h** |
| Energy Intensity | 3,106 | **1,849** |

A principal diferença entre os cenários não está nos setpoints. Ela está no estado atribuído ao equipamento. Isso reforça uma conclusão importante e também uma limitação:

- o modelo associa melhor condição a melhor desempenho;
- o dataset não prova que a manutenção causará exatamente essa melhora.

O suporte agora é condicionado ao mesmo ativo/unidade e inclui setpoints, saúde, vibração e idade do catalisador. A solução sem manutenção fica próxima do limite condicionado `2,032`; a solução pós-manutenção fica em `1,035`.

Como a fronteira estrita colapsa em um ponto, foram criadas alternativas pós-manutenção por faixa: metas de 140%, 150%, 160% e 165% da produção atual, com intensidades aproximadas de 2,439, 2,276, 2,134 e 2,069, respectivamente.

Na versão robusta, o otimizador considera o limite superior de intensidade e o limite inferior de produção. Para o cenário com manutenção, a intensidade nominal de `1,849` passa a ter limite superior de 90% igual a `2,401`. Os setpoints permanecem iguais porque a margem calibrada é global e aditiva e o erro da identidade de produção é numericamente zero.

## 15. Como os cenários de manutenção funcionam?

**Referência: item 4 — três cenários obrigatórios de manutenção.**

O horizonte é de 30 dias:

```text
30 dias × 24 horas / 4 horas = 180 intervalos
```

Foram comparados:

### Sem manutenção

O equipamento permanece degradado durante os 180 intervalos.

### Manutenção imediata

Há dois intervalos de parada, equivalentes a oito horas, e os demais intervalos usam o estado saudável de referência.

### Manutenção postergada

O equipamento funciona degradado durante 15 dias, para durante oito horas e depois passa ao estado saudável de referência.

## 16. De onde vieram os custos?

**Referência: item 4 e item 7 — comparação de custos e composição do resultado final.**

O dataset não possui preços ou custos reais. Foram adotadas premissas didáticas:

| Premissa | Valor |
|---|---:|
| Energia | R$ 130 por unidade de energia |
| Manutenção imediata | R$ 45.000 |
| Manutenção planejada | R$ 25.000 |
| Falha | R$ 300.000 |

O custo calculado é parcial:

```text
Custo parcial =
    custo de energia
  + custo de manutenção
  + exposição financeira assumida para falha
```

Ele não inclui:

- preço e margem do produto;
- custo real da parada;
- estoque disponível;
- demanda;
- penalidades por atraso;
- logística e peças específicas.

Por isso, a economia encontrada não deve ser apresentada como garantia financeira.

## 17. Como interpretar os três cenários?

**Referência: item 4 — produção, energia, custo, condição, risco e impacto esperado.**

| Cenário | Produção | Energia | Total parcial | Parcial/ton |
|---|---:|---:|---:|---:|
| Sem manutenção | 12.996,56 ton | 40.350,05 unid. | R$ 5.436.123,76 | R$ 418,27 |
| Manutenção imediata | 21.582,06 ton | 39.901,71 unid. | R$ 5.260.829,62 | R$ 243,76 |
| Manutenção postergada | 17.168,06 ton | 39.901,71 unid. | R$ 5.321.517,13 | R$ 309,97 |

Dentro das premissas, a manutenção imediata possui o menor custo parcial e o menor custo por tonelada.

Economia parcial frente a não realizar manutenção:

```text
R$ 5.436.123,76 − R$ 5.260.829,62 = R$ 175.294,14
```

A análise de sensibilidade variou isoladamente preço de energia, custo de manutenção e custo de falha em ±30%. A economia continuou positiva entre aproximadamente R$ 127 mil e R$ 224 mil. Em uma comparação com as mesmas 10 mil toneladas, a economia varia de `-R$ 45 mil` com recuperação nula a `R$ 1,72 milhão` com recuperação integral.

Isso mostra robustez dentro das premissas testadas. Não elimina o risco de as premissas reais serem muito diferentes.

## 18. O Isolation Forest prevê falha?

**Referência: item 4 e item 5 — avaliação crítica do risco e dos limites da automação.**

Não.

Isolation Forest é um detector de anomalias. Ele identifica registros raros em comparação com o histórico, mas não sabe se um registro raro é bom ou ruim.

Resultados:

- estado degradado: percentil 0,44 de normalidade;
- referência saudável: percentil 20,11 de normalidade.

O estado degradado é muito raro no treino. Isso fortalece a recomendação de investigar, mas não fornece probabilidade de falha.

Para estimar risco real, seriam necessários eventos históricos como:

- falha ou não falha;
- tipo de falha;
- tempo até a falha;
- manutenção executada;
- condição antes e depois da intervenção.

## 19. A manutenção deve ser automática?

**Referência: item 5 — benefícios, riscos e nível recomendado de automação.**

Não completamente.

O nível recomendado é:

| Atividade | Automação |
|---|---|
| Validação dos dados | Automática |
| Cálculo dos scores | Automática |
| Alertas de degradação | Automática |
| Sugestão de setpoints | Automática supervisionada |
| Aplicação dos setpoints | Com limites oficiais e possibilidade de rollback |
| Parada para manutenção | Aprovação humana obrigatória |

A parada possui alto impacto financeiro, operacional e de segurança. Além disso, o risco ainda não foi calibrado com falhas reais.

A recomendação correta é:

> Inspecionar imediatamente. Se os sensores e a condição degradada forem confirmados, realizar a manutenção com aprovação dos responsáveis.

## 20. O que significa human-in-the-loop?

**Referência: item 5 e etapa final do item 6 — decisão entre humano e automação.**

É uma automação em que o sistema analisa dados e recomenda uma ação, mas uma pessoa mantém a responsabilidade por decisões críticas.

Neste trabalho:

```text
Sistema detecta condição rara
    ↓
Sistema sugere configuração e manutenção
    ↓
Operação e engenharia verificam sensores e segurança
    ↓
Pessoa aprova, rejeita ou ajusta a ação
```

## 21. Principais limitações

**Referência: item 5 e item 8 — riscos da decisão e análise crítica.**

Você deve conhecer estas limitações para demonstrar pensamento crítico:

1. Não existem rótulos reais de falha.
2. Não existem registros explícitos de manutenção.
3. Não é possível provar efeito causal da manutenção.
4. Custos e probabilidade de falha são premissas.
5. Não existem limites oficiais de segurança no dataset.
6. O modelo de energia possui erro relevante.
7. A solução foi encontrada em dados históricos e pode sofrer drift.
8. O custo total não inclui receita, margem e outros efeitos empresariais.

Reconhecer essas limitações não enfraquece o trabalho. Pelo contrário, mostra que a recomendação foi construída com responsabilidade.

## 22. Quais dados seriam necessários para produção?

**Referência: item 8 — última pergunta obrigatória da conclusão.**

- eventos e tipos de falha;
- ordens de manutenção;
- condição antes e depois da manutenção;
- duração e custo real de cada intervenção;
- limites oficiais de temperatura, pressão, vazão e válvula;
- preços separados de eletricidade e gás;
- preço, margem e demanda do produto;
- estoques e capacidade de outras unidades;
- custos de parada e retomada;
- penalidades contratuais;
- qualidade, calibração e drift dos sensores.

## 23. Como apresentar o resultado final?

**Referência: item 7 e item 8 — tabela final e respostas objetivas da conclusão.**

Uma resposta segura e objetiva seria:

> O pipeline recomendou vazão de 694,11 m³/h, temperatura de 795,14 °C, pressão de 33,32 bar e válvula em 79,53%. Para o estado saudável simulado, o modelo prevê 121,25 toneladas por intervalo e intensidade de 1,849. Sob as premissas didáticas, a manutenção imediata reduz o custo parcial em aproximadamente R$ 175 mil em 30 dias; o ponto de equilíbrio é cerca de 1,8% de recuperação. Recomendamos inspeção e aprovação humana antes da parada.

## 24. Perguntas que o professor pode fazer

**Referência: revisão de todos os itens, com foco na defesa das escolhas metodológicas.**

### Por que vocês não usaram eletricidade e gás no modelo de energia?

Porque eles formam matematicamente o target. Além disso, são conhecidos depois da operação, enquanto a decisão precisa acontecer antes.

### Por que o modelo de produção é tão preciso?

O dataset possui a identidade exata `Yield = 0,18 × Flow × Health`. Isso caracteriza a construção sintética da base; ainda usamos teste temporal para avaliar energia.

### Por que não usar apenas regressão linear e linprog?

A razão energética e o suporte conjunto tornam o problema principal não linear. O `linprog` foi mantido como análise complementar e interpretável.

### Por que a pressão, temperatura e válvula parecem pouco importantes?

Dentro das faixas existentes no dataset, elas acrescentam pouca capacidade preditiva. Isso não significa que sejam irrelevantes para segurança ou engenharia.

### Como vocês sabem que a solução não está fora do histórico?

Além dos limites individuais, foi calculada a distância até configurações observadas da mesma unidade. A recomendação ficou abaixo do limite definido pelo percentil 99 dessa distância.

### A economia de R$ 175 mil é real?

É uma estimativa condicional às premissas usadas. O valor real exige preços, custos, margem, demanda e duração de parada da empresa.

### A manutenção vai aumentar a produção para 121,25 toneladas?

Não há garantia. Esse é o valor previsto no cenário simulado. O dataset não contém intervenções suficientes para provar causalidade.

### Por que a decisão final precisa de uma pessoa?

Porque uma parada é cara, afeta segurança e produção, e o modelo de risco não foi treinado com falhas reais.

## 25. Glossário rápido

**Referência: apoio conceitual para entender os itens 2 a 6 do enunciado.**

| Termo | Significado |
|---|---|
| Feature | Variável usada como entrada do modelo |
| Target | Variável que o modelo tenta prever |
| Leakage | Uso indevido de informação que contém a resposta |
| Baseline | Modelo simples usado como referência |
| R² | Fração da variação explicada pelo modelo |
| MAE | Erro absoluto médio |
| RMSE | Erro que penaliza mais erros grandes |
| Ensemble | Combinação de vários modelos |
| Setpoint | Valor operacional desejado para um controle |
| Solver | Algoritmo que resolve o problema de otimização |
| Constraint | Restrição que a solução deve respeitar |
| Surrogate | Modelo mais simples usado como aproximação |
| Anomalia | Observação rara em comparação com o histórico |
| Drift | Mudança do padrão dos dados ao longo do tempo |
| Rollback | Retorno rápido à configuração anterior |
| Human-in-the-loop | Pessoa participa da decisão crítica |

## 26. Ordem sugerida de estudo

**Referência: roteiro para revisar os oito itens obrigatórios antes da apresentação.**

1. Leia as seções 1, 5 e 11 para entender o problema.
2. Estude target leakage na seção 5.
3. Revise os modelos e métricas nas seções 7 e 8.
4. Entenda seleção do caso e estado saudável nas seções 9 e 10.
5. Estude otimização e validação nas seções 11 a 14.
6. Revise cenários, custos e limitações nas seções 15 a 18.
7. Termine com automação, limitações e perguntas prováveis.

Depois dessa leitura, percorra o notebook seguindo a mesma ordem. O relatório serve como versão formal e o roteiro ajuda a transformar esse entendimento em apresentação oral.

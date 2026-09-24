# Roteiro simplificado da apresentação

**Duração estimada:** 14 a 15 minutos  
**Formato:** 20 slides

Use este texto como guia. Não é necessário decorar nem ler palavra por palavra.

## 1. Capa

“Neste trabalho, usamos dados, Machine Learning e otimização para recomendar uma configuração de operação e apoiar a decisão de manutenção. Nosso cuidado principal foi mostrar não só o resultado, mas também seus limites.”

## 2. Ponto de partida

“Começamos com o caso mais degradado do período de teste. O equipamento apresentava baixa saúde, vibração elevada e catalisador envelhecido. A pergunta era: como melhorar o desempenho sem reduzir a produção e sem tomar uma decisão insegura?”

## 3. Dados utilizados e desconsiderados

“A base tem 10 mil registros, 16 colunas, medições a cada quatro horas e não possui nulos ou duplicatas. Das colunas originais, 11 representam informações disponíveis antes da operação e foram usadas como entradas. Product Yield e Energy Intensity são os dois targets. Electricity, Natural Gas e Steam aparecem depois da operação e foram retiradas das features. O Yield observado também não entra no modelo de energia; usamos somente o Yield previsto. Essas colunas não foram apagadas: eletricidade e gás foram mantidos para auditar a fórmula e calcular uma referência usando apenas o treino.”

## 4. O que a base permite responder

“Com Flow e Health, a base permite reconstruir exatamente a produção. Para energia, o modelo explica cerca de 69% da variação e tem RMSE de 0,340. Para otimizar, ajustamos Flow, temperatura, pressão e válvula, exigindo produção mínima de 64,37 e proximidade ao histórico. Para manutenção, a base só permite comparar cenários: não existem registros reais de falhas ou intervenções para provar o efeito da manutenção.”

## 5. Dados e exploração

“Também verificamos se seria necessário avaliar ou modelar cada produto separadamente. Como a base não tem uma coluna de produto, usamos as unidades de amônia, etileno e metanol como proxy. Elas possuem entre 3.299 e 3.354 registros, intensidade média entre 2,882 e 2,887 e produção média entre 80,01 e 80,38 toneladas. Nos modelos de energia, o RMSE global foi 0,337, 0,352 e 0,338, enquanto os modelos separados ficaram em 0,343, 0,358 e 0,340. Como não houve melhora, mantivemos um único modelo e usamos a avaliação por unidade apenas para monitoramento.”

## 6. Como as fórmulas foram verificadas

“Aprendemos as constantes nos primeiros 70% da série e confirmamos a relação em toda a base. O 0,18 transforma Flow vezes Health em produção neste dataset; ele foi usado porque as duas entradas existem antes da operação e a relação é exata. O 3,6 coincide com a conversão de MWh para GJ, e o 0,035 representa 35 megajoules por metro cúbico de gás. Eles colocam as fontes em uma escala energética comum. Como a base é sintética e não documenta todo o balanço físico, esses fatores não são constantes universais de uma planta.”

## 7. Target leakage

“A forma mais simples de entender leakage é perguntar: eu conheceria este valor quando fosse escolher os setpoints? Vazão, saúde e condição do equipamento já existem e podem entrar. Eletricidade, gás, vapor e produção observada só aparecem depois e ficam fora. O híbrido usa apenas uma média aprendida no histórico de treino e uma produção prevista; ele nunca recebe os valores futuros da linha que está tentando prever.”

## 8. Comparação dos modelos

“Testamos diferentes modelos para energia e produção. O híbrido físico combina relações conhecidas do processo com estimativas dos dados. Para produção, ele aplica a relação entre vazão e saúde. Para energia, utiliza a energia equivalente média do treino dividida pela produção prevista. Ele foi escolhido porque teve desempenho estável e é mais fácil de interpretar.”

## 9. Validação temporal e escolha do modelo

“Fizemos três validações walk-forward, treinando sempre com os dados anteriores e validando nos mil registros seguintes. Assim, preservamos a ordem temporal e verificamos se o resultado permanecia estável. O híbrido foi escolhido porque empatou com o Gradient Boosting nos folds, foi ligeiramente melhor no teste final e é mais fácil de interpretar.”

## 10. Validação e incerteza

“Target significa a variável que o modelo tenta prever. Aqui temos dois targets: intensidade energética e produção. Não significa escolher entre focar em energia ou produção. O R² igual a 1 da produção acontece porque ela foi gerada por uma fórmula exata na base sintética. Na tabela dos folds, o híbrido está destacado porque foi o selecionado; o Random Forest não foi escolhido. Para energia, usamos mil registros separados para calcular uma margem de erro de 0,552. Somada à previsão, essa margem cobriu 89,4% dos valores reais do teste.”

## 11. Otimização

“O otimizador testa combinações de vazão, temperatura, pressão e abertura da válvula. Primeiro procura reduzir a intensidade energética. Depois elimina alternativas com produção abaixo de 64,37 toneladas ou muito distantes do histórico. Usamos Differential Evolution porque o problema não é linear. Uma busca aleatória e uma versão linear simplificada conferiram a direção do resultado.”

## 12. Saúde, produção e recuperação

“Não inventamos os extremos. O valor 0,578 pertence ao registro real com maior escore de degradação no teste. O valor 0,970 pertence a um registro real saudável da mesma unidade e do mesmo catalisador no treino, escolhido no centro do grupo com alta saúde, baixa vibração e catalisador mais novo. Os valores entre eles são interpolações, não medições depois de uma manutenção. Recuperar 50% significa percorrer metade dessa distância e chegar a 0,774. Como a base inteira obedece exatamente a Yield igual a 0,18 vezes Flow vezes Health, com a mesma vazão o Yield passa de 72,20 para 96,73 toneladas, ganho de 34%. A economia não é proporcional: foi recalculada em cada cenário e empata perto de 1,8%."

## 13. Resultado final

“Esta tabela mostra a configuração calculada para o cenário em que o ativo alcança a referência saudável, equivalente aos 100% de recuperação simulada no slide anterior. Ela não afirma que toda manutenção produzirá esse resultado. Os quatro setpoints, a produção, a energia e os custos dependem dessa hipótese. Por isso, a manutenção só deve ser autorizada após inspeção e validação operacional.”

## 14. Premissas econômicas

“O dataset não informa custos de manutenção ou falha. Para comparar os cenários, assumimos 30 dias, oito horas de parada, R$ 130 por unidade de energia, R$ 45 mil para manutenção imediata, R$ 25 mil para manutenção planejada e R$ 300 mil para uma possível falha. São premissas didáticas, não valores reais de uma empresa.”

## 15. Três cenários

“Comparamos três possibilidades: não fazer manutenção, postergar e fazer imediatamente. No cenário estudado, a manutenção imediata apresenta maior produção e um custo parcial cerca de R$ 175 mil menor em 30 dias. Esse valor depende das premissas adotadas.”

## 16. Cálculo dos cenários

“Sem manutenção, consideramos 180 intervalos produzindo. Na manutenção imediata, são dois intervalos de parada e 178 produzindo no estado recuperado. Na postergada, são 90 intervalos no estado atual, dois de parada e 88 no estado recuperado. O custo parcial soma energia, manutenção e exposição assumida à falha.”

## 17. Margem e sensibilidade

“A previsão nominal da intensidade energética é 1,849. Somamos a margem calibrada de 0,552 e obtemos o limite conservador de 2,401. Na produção, o limite inferior permanece em 121,25 porque a base possui uma fórmula exata. Os setpoints não mudaram porque a mesma margem foi aplicada às alternativas. O que muda é a garantia que comunicamos.”

## 18. Alternativas de operação

“Além do ponto principal, criamos opções para diferentes metas de produção. Isso é importante porque o melhor ponto matemático pode não ser o melhor para o negócio. A decisão final também depende de demanda, margem e estoque, que não estão na base.”

## 19. Automação

“Nossa recomendação é automatizar o monitoramento, os alertas e parte da sugestão de setpoints. A automação traz velocidade, escala e operação contínua. Porém, pode errar por causa do modelo ou dos dados. Por isso, a decisão de parar a planta continua com uma pessoa.”

## 20. Conclusão

“A configuração veio do otimizador, respeitando a produção mínima e o histórico. A manutenção é condicional porque o estado degradado foi observado, mas seu efeito não foi. Os R$ 175 mil vêm da diferença entre os custos dos cenários e dependem das premissas financeiras. Os riscos vêm do erro medido do modelo e das informações ausentes. Por isso, automatizamos monitoramento, mas mantemos a parada com aprovação humana. A origem detalhada de cada resposta está na seção 23 do guia de estudo.”

## Respostas rápidas para perguntas

**Por que a parada não é automática?** Porque não temos histórico real de falhas e intervenções, e uma parada tem alto impacto.

**A economia de R$ 175 mil é garantida?** Não. É uma estimativa baseada em premissas didáticas.

**Por que a produção teve erro zero?** Porque a base sintética usa uma fórmula exata para gerar a produção.

**Por que não usamos apenas `linprog`?** Porque o problema principal possui relações não lineares. O `linprog` foi usado como verificação.

**O que falta para usar a solução na planta?** Dados reais de falha e manutenção, limites de engenharia, preços, margem, demanda e custo completo da parada.

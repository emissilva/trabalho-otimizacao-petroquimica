# Roteiro simplificado da apresentação

**Duração estimada:** 14 a 15 minutos  
**Formato:** 20 slides

Use este texto como guia. Não é necessário decorar nem ler palavra por palavra.

## 1. Capa

“Neste trabalho, usamos dados, Machine Learning e otimização para recomendar uma configuração de operação e apoiar a decisão de manutenção. Nosso cuidado principal foi mostrar não só o resultado, mas também seus limites.”

## 2. Ponto de partida

“Começamos com o caso mais degradado do período de teste. O equipamento apresentava baixa saúde, vibração elevada e catalisador envelhecido. A pergunta era: como melhorar o desempenho sem reduzir a produção e sem tomar uma decisão insegura?”

## 3. Configuração e critérios para a decisão

“A recomendação principal usa vazão de 694,11 m³/h e prevê 121,25 toneladas a cada quatro horas. A análise também indica que uma pequena recuperação, de 1,8%, já compensaria o custo da manutenção. Mesmo assim, a parada precisa de aprovação humana.”

## 4. Negócio e pipeline

“Separamos as variáveis em quatro grupos. Algumas podem ser controladas, como vazão e temperatura. Outras mostram o estado do equipamento, como saúde e vibração. Também temos fatores externos e os resultados que queremos prever. A partir disso, montamos o pipeline completo mostrado no slide.”

## 5. Dados e exploração

“A base possui 10 mil registros, de 2020 a 2024, em três unidades, sem dados faltantes ou duplicados. Durante a análise, descobrimos que a produção segue exatamente a fórmula mostrada no slide. Isso indica que a base é sintética e explica o erro praticamente zero na previsão de produção.”

## 6. Como as fórmulas foram verificadas

“Product Yield é a quantidade produzida em cada intervalo de quatro horas. Dividimos a produção pelo produto entre vazão e saúde e encontramos a constante 0,18 em toda a base. Para energia, reconstruímos a intensidade dividindo a energia equivalente pela produção. Essas verificações mostraram que a base possui relações sintéticas exatas.”

## 7. Target leakage

“Também descobrimos que a intensidade energética é calculada usando eletricidade, gás e produção. Como esses valores só são conhecidos depois da operação, eles foram retirados das entradas do modelo. Assim, evitamos dar ao modelo uma resposta que ele não teria no momento da decisão.”

## 8. Comparação dos modelos

“Testamos diferentes modelos para energia e produção. Para energia, o modelo híbrido teve o menor erro e também foi mais fácil de explicar. Para produção, o modelo com a interação entre vazão e saúde reproduziu a fórmula da base. Por isso, esses dois foram escolhidos para o pipeline.”

## 9. Métricas e walk-forward

“O R² indica quanto da variação foi explicada. MAE é o erro médio e RMSE dá mais peso aos erros grandes. Para energia, explicamos 69,3% da variação, com erro médio próximo de 9,6% da média. Também fizemos três validações walk-forward, treinando sempre com o passado e validando no período seguinte.”

## 10. Validação e incerteza

“Como os dados têm ordem no tempo, treinamos com o passado e validamos em períodos seguintes. Também reservamos o teste final para o fim. Na energia, o erro RMSE foi 0,340. Criamos ainda uma margem de segurança de 0,552, que cobriu 89,4% dos casos do teste.”

## 11. Otimização

“O otimizador procura reduzir a intensidade energética, mas precisa manter uma produção mínima e respeitar faixas próximas ao histórico. Usamos um método não linear como principal e também fizemos duas verificações independentes para confirmar a direção da solução.”

## 12. Estado do ativo

“Para representar o estado após a manutenção, usamos uma observação saudável que realmente existe na base. Não criamos um equipamento perfeito artificialmente. Antes de qualquer parada, recomendamos uma inspeção para confirmar os sensores e a condição do ativo.”

## 13. Resultado final

“Esta é a tabela final pedida no trabalho. Ela reúne os quatro setpoints, a produção esperada, a intensidade energética e os custos. A manutenção é recomendada somente depois da inspeção. Os setpoints podem ser supervisionados pelo sistema, mas a parada precisa de aprovação humana.”

## 14. Premissas econômicas

“O dataset não informa custos de manutenção ou falha. Para comparar os cenários, assumimos 30 dias, oito horas de parada, R$ 130 por unidade de energia, R$ 45 mil para manutenção imediata, R$ 25 mil para manutenção planejada e R$ 300 mil para uma possível falha. São premissas didáticas, não valores reais de uma empresa.”

## 15. Três cenários

“Comparamos três possibilidades: não fazer manutenção, postergar e fazer imediatamente. No cenário estudado, a manutenção imediata apresenta maior produção e um custo parcial cerca de R$ 175 mil menor em 30 dias. Esse valor depende das premissas adotadas.”

## 16. Cálculo dos cenários

“Sem manutenção, consideramos 180 intervalos produzindo. Na manutenção imediata, são dois intervalos de parada e 178 produzindo no estado recuperado. Na postergada, são 90 intervalos no estado atual, dois de parada e 88 no estado recuperado. O custo parcial soma energia, manutenção e exposição assumida à falha.”

## 17. Margem e sensibilidade

“A previsão de energia não deve ser tratada como um número exato. O valor nominal é 1,849 e o limite superior é 2,401. Também testamos mudanças nas premissas financeiras. O ponto de equilíbrio foi uma recuperação de 1,8%. Sem recuperação, a manutenção gera uma perda de R$ 45 mil.”

## 18. Alternativas de operação

“Além do ponto principal, criamos opções para diferentes metas de produção. Isso é importante porque o melhor ponto matemático pode não ser o melhor para o negócio. A decisão final também depende de demanda, margem e estoque, que não estão na base.”

## 19. Automação

“Nossa recomendação é automatizar o monitoramento, os alertas e parte da sugestão de setpoints. A automação traz velocidade, escala e operação contínua. Porém, pode errar por causa do modelo ou dos dados. Por isso, a decisão de parar a planta continua com uma pessoa.”

## 20. Conclusão

“A configuração recomendada é a mostrada na tabela final. Devemos inspecionar o equipamento agora e fazer a manutenção se a degradação for confirmada. A economia estimada é de R$ 175 mil em 30 dias, dentro das premissas do estudo. Os principais riscos estão no modelo, nos sensores e na falta de dados reais de manutenção. Para levar a solução à produção, ainda precisamos de falhas reais, histórico de intervenções, limites oficiais e custos completos.”

## Respostas rápidas para perguntas

**Por que a parada não é automática?** Porque não temos histórico real de falhas e intervenções, e uma parada tem alto impacto.

**A economia de R$ 175 mil é garantida?** Não. É uma estimativa baseada em premissas didáticas.

**Por que a produção teve erro zero?** Porque a base sintética usa uma fórmula exata para gerar a produção.

**Por que não usamos apenas `linprog`?** Porque o problema principal possui relações não lineares. O `linprog` foi usado como verificação.

**O que falta para usar a solução na planta?** Dados reais de falha e manutenção, limites de engenharia, preços, margem, demanda e custo completo da parada.

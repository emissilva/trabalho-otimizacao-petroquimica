# Requisitos do trabalho — Pipeline de ML, Otimização e Decisão de Manutenção

Este documento é a fonte de referência do projeto. Antes de alterar o notebook, o relatório ou a apresentação, confira se a mudança permanece alinhada ao enunciado abaixo.

## Objetivo

Com base na última aula de otimização, construir, usando o dataset `petrochemical_advanced_data.csv`, um pipeline completo que transforme dados históricos em uma decisão operacional:

`Dados → Machine Learning → Otimização → Cenários → Decisão`

O trabalho deve responder:

1. Qual configuração operacional reduz o custo/intensidade energética mantendo a produção e as restrições operacionais?
2. Devemos realizar manutenção? Essa decisão poderia ser automatizada?

Entrega informada pelo professor: **24/09**. O trabalho pode ser individual ou em grupo e deve ser desenvolvido em sala durante esta aula e a próxima.

## Entregas obrigatórias

### 1. Entendimento do negócio

Identificar e documentar:

- objetivo da operação;
- variáveis controláveis;
- variáveis de estado;
- variáveis externas;
- principais restrições;
- regras de negócio necessárias.

Apresentar uma tabela com as principais variáveis e sua classificação.

### 2. Machine Learning

Criar modelos para prever:

- `Energy_Intensity`;
- `Product_Yield_Tons`.

Utilizar pelo menos dois modelos para cada target e apresentar uma tabela comparativa contendo Energy/Modelo 1, Energy/Modelo 2, Yield/Modelo 1 e Yield/Modelo 2. Explicar qual modelo foi usado no pipeline e por quê. Verificar possível *target leakage*, especialmente nas variáveis de energia.

### 3. Otimização

Transformar os modelos preditivos em um problema de otimização e definir:

- variáveis de decisão;
- função objetivo;
- restrições;
- limites das variáveis.

Implementar com `scipy.optimize.linprog` ou outro solver justificado. Apresentar formulação matemática, código, solução encontrada e interpretação da solução.

### 4. Decisão de manutenção

Criar pelo menos três cenários:

- sem manutenção;
- manutenção imediata;
- manutenção postergada.

Comparar produção, energia, custo, condição do equipamento, risco e impacto esperado.

### 5. Automação da decisão

Analisar criticamente se a decisão de manutenção deve ser automática ou passar por aprovação humana.

Apresentar como benefícios da automação: velocidade, escala, redução de intervenção, redução de *downtime*/custos e operação contínua.

Apresentar como riscos: falso positivo, falso negativo, erro do modelo, dados incorretos, mudança das condições operacionais e impacto de uma decisão errada.

Explicar e justificar o nível de automação recomendado.

### 6. Pipeline final

Representar o pipeline completo:

```text
Dados
  ↓
EDA
  ↓
Feature Engineering
  ↓
Modelos ML
  ↓
Previsões
  ↓
Cenários
  ↓
Otimização
  ↓
Análise de custo/risco
  ↓
Decisão de manutenção
  ↓
Recomendação
  ↓
Humano ou Automação
```

### 7. Resultado final

Apresentar uma tabela final contendo:

- Feedstock Flow;
- Reactor Temperature;
- Reactor Pressure;
- Valve Opening;
- Expected Yield;
- Energy Intensity;
- Energy Cost;
- Maintenance — Sim/Não;
- Maintenance Cost;
- Total Cost;
- nível de automação recomendado.

### 8. Conclusão

Responder objetivamente:

1. Qual configuração operacional foi recomendada?
2. A manutenção deve ser realizada? Em quais condições?
3. Qual foi o impacto econômico esperado?
4. Quais são os principais riscos da decisão?
5. A decisão deve ser automatizada ou aprovada por um humano?
6. Quais dados adicionais seriam necessários para colocar a solução em produção?

## Entregáveis

1. Notebook com todo o pipeline executável.
2. Relatório explicando metodologia, resultados e decisões.
3. Apresentação de aproximadamente 10–15 minutos.

O foco não é apenas obter o melhor modelo ou a solução matemática. O objetivo é demonstrar como ML + Otimização podem ser transformados em uma decisão operacional justificável.

## Mapa de atendimento atual

| Exigência | Local principal | Situação observada |
|---|---|---|
| Entendimento do negócio e tabela de variáveis | `relatorio/relatorio.md`, seção 1 | Presente |
| Dois ou mais modelos por target e comparação | Notebook e relatório, seção 2 | Presente |
| Verificação de target leakage | Notebook e relatório, seção 2.2 | Presente; identidade algébrica exata documentada |
| Formulação, solver, solução e interpretação | Notebook e relatório, seção 3 | Presente; solver não linear justificado e `linprog` usado como validação |
| Três cenários de manutenção | Notebook e relatório, seção 4 | Presente |
| Discussão de automação | Relatório, seção 5 | Presente |
| Representação do pipeline | Relatório, seção 6 | Presente |
| Tabela final | Relatório, seção 7 | Presente |
| Conclusões objetivas | Relatório, seção 8 | Presente |
| Notebook executável | `notebook/pipeline_petroquimico.ipynb` | Executado integralmente em ambiente isolado, sem erros |
| Relatório | `relatorio/relatorio.md`, `.html` e `.pdf` | Sincronizados com a execução revisada |
| Apresentação de 10–15 minutos | `apresentacao/` | HTML claro com 20 slides; PDF e PPTX sincronizados; roteiro didático estimado em 14–15 minutos |

## Premissas e limitações que devem permanecer explícitas

- Os custos de energia, manutenção e falha são premissas didáticas, não valores fornecidos pelo dataset.
- A probabilidade de falha é uma heurística sem rótulos históricos de falha; não deve ser apresentada como probabilidade calibrada.
- O efeito da manutenção usa uma referência saudável realmente observada, mas continua sendo cenário associativo, sem prova causal.
- Faixas entre os percentis 1 e 99 e a restrição conjunta de suporte reduzem extrapolação, mas não representam limites oficiais de segurança da planta.
- O custo total é parcial: faltam receita, margem, demanda, estoque e custo completo da parada.
- O modelo híbrido de energia tem RMSE de teste de aproximadamente 0,340 e margem conformal absoluta de 90% de 0,552, calibrada fora do teste; a cobertura observada no teste final foi 89,4%.
- A produção segue uma identidade sintética exata de vazão e saúde; isso não prova que manutenção real causará a recuperação simulada.
- A decisão de parar a planta requer inspeção e aprovação humana.
- O suporte conjunto condicionado ao estado é uma aproximação estatística; não substitui limites oficiais nem validação de engenharia.

## Inventário e materiais relacionados

- `data/petrochemical_advanced_data.csv`: base petroquímica, 10.000 registros mais cabeçalho.
- `notebook/pipeline_petroquimico.ipynb`: pipeline de EDA, ML, otimização e cenários.
- `relatorio/`: relatório em Markdown, HTML e PDF.
- `apresentacao/`: apresentação HTML, PDF, PPTX e roteiro de fala.
- `fontes/`: fontes Inter usadas na apresentação e incorporadas ao PPTX.
- `notas_secao1.md`: notas de entendimento do negócio.
- `originais/trabalho-otimizacao-petroquimica.rar`: pacote original preservado.
- Pasta irmã `aula_econometria_otimizacao_linear/`: notebook de apoio sobre econometria, `linprog`, MILP e análise de sensibilidade. Ele usa `retail_price.csv`, arquivo que não foi localizado junto aos materiais baixados.

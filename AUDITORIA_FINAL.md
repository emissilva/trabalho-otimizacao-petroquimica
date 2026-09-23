# Auditoria final dos entregáveis

Data da revisão: 20/09/2026.

## Resultado

O trabalho cobre as oito seções e os três entregáveis solicitados. O notebook foi executado integralmente em um ambiente Python isolado, sem células com erro, e os números foram sincronizados com relatório em Markdown/HTML/PDF, apresentação e roteiro.

## Problemas encontrados e corrigidos

| Problema anterior | Correção aplicada |
|---|---|
| Arquivos extraídos estavam vazios | Conteúdo recuperado do RAR e validado por hash |
| Steam descrito como componente do target | Identidade exata provou que apenas eletricidade, gás e produção formam `Energy_Intensity` |
| Caso degradado escolhido por índice fixo | Seleção reproduzível pelo maior score de degradação no teste |
| Pós-manutenção combinava percentis extremos e era anômalo | Uso de uma observação real e representativa da mesma unidade/catalisador no treino |
| Limites independentes permitiam combinações improváveis | Restrição adicional de distância conjunta ao histórico da unidade |
| Otimização dependia de uma única técnica | Validação com 10.000 candidatos aleatórios e surrogate via `linprog` |
| Probabilidade de falha apresentada como estimada | Reclassificada como premissa não calibrada; Isolation Forest usado só para raridade |
| Custo tratado como business case completo | Renomeado como custo parcial e acompanhado das variáveis econômicas ausentes |
| Importância preditiva sugeria causalidade | Relatório e slides agora declaram explicitamente que associação não prova efeito de manutenção |
| Roteiro tinha cerca de 9 minutos | Refeito em linguagem simples para 14–15 minutos e 20 slides |
| Métricas divergiam entre arquivos | Notebook, relatório, PDF e slides usam a mesma execução |
| Projeto sem dependências declaradas | Criados `pyproject.toml` e indicação da versão compatível do Python |
| Estrutura determinística de produção não explorada | Identidade `Yield = 0,18 × Flow × Health` incorporada ao modelo híbrido |
| Cenários econômicos comparavam volumes diferentes | Incluída comparação adicional com meta comum de 10 mil toneladas |
| Efeito de manutenção avaliado apenas no extremo | Incluída sensibilidade de recuperação entre 0% e 100% |
| Previsão final de energia era somente pontual | Adicionada margem conformal de 90% em janela exclusiva de calibração |
| Seleção dependia de um único corte temporal | Adicionados três folds walk-forward dentro da janela de desenvolvimento |
| Incerteza usava o próprio teste | Criada janela exclusiva de 1.000 registros para calibração conformal |
| Otimização usava apenas valores pontuais | Adicionados limite superior de energia e limite inferior de produção |
| Suporte considerava apenas setpoints | Distância condicionada inclui estado do ativo/unidade |
| Recomendação era apenas um ponto extremo | Adicionadas alternativas por faixas de produção e ponto de equilíbrio de recuperação |

## Checklist do professor

- [x] Objetivo, variáveis, restrições e regras de negócio.
- [x] Tabela de classificação das variáveis.
- [x] Três modelos para cada target, com R², MAE e RMSE.
- [x] Escolha e justificativa dos modelos do pipeline.
- [x] Target leakage verificado por identidade algébrica.
- [x] Variáveis de decisão, objetivo, restrições e limites.
- [x] Solver não linear justificado e `linprog` apresentado como validação.
- [x] Solução e interpretação.
- [x] Cenários sem manutenção, imediata e postergada.
- [x] Produção, energia, custo, condição, risco e impacto comparados.
- [x] Benefícios, riscos e nível de automação discutidos.
- [x] Pipeline completo representado.
- [x] Tabela final com todos os campos solicitados.
- [x] Seis perguntas finais respondidas.
- [x] Notebook executável, relatório e apresentação de 10–15 minutos.

## Limitações que devem permanecer explícitas

- Não há rótulos de falha, ordens de manutenção ou dados antes/depois da intervenção.
- Não há limites oficiais de engenharia; percentis e suporte histórico não os substituem.
- Custos e probabilidade de falha são premissas didáticas.
- Não há preço/margem do produto, demanda, estoque nem custo completo de parada.
- O modelo híbrido de energia tem RMSE de teste de aproximadamente 0,340 e margem conformal de 90% de 0,552; a cobertura observada no teste final foi 89,4%.
- A identidade exata de produção caracteriza a base sintética, mas não identifica efeito causal de uma manutenção real.
- A recomendação final exige inspeção e aprovação humana antes de parar a planta.

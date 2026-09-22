# Seção 1 — Entendimento do negócio

> Notas revisadas. A versão completa e sincronizada está em `relatorio/relatorio.md`.

## Objetivo da operação
Operar unidades petroquímicas (Ethylene_Plant_01, Ammonia_Unit_02, Methanol_Complex_03)
maximizando o rendimento de produto (Product_Yield_Tons) e minimizando a intensidade
energética (Energy_Intensity) por tonelada produzida, respeitando limites operacionais
seguros e a condição do equipamento (catalisador/sensores).

## Classificação das variáveis

| Variável | Tipo | Papel no problema |
|---|---|---|
| Feedstock_Flow_m3h | Controlável | Vazão de alimentação — variável de decisão |
| Reactor_Temp_C | Controlável | Temperatura do reator — variável de decisão |
| Reactor_Pressure_Bar | Controlável | Pressão do reator — variável de decisão |
| Valve_Opening_Percent | Controlável | Abertura de válvula — variável de decisão |
| Sensor_Health_Index | Estado (equipamento) | Saúde do sensor/equipamento — proxy de manutenção |
| Vibration_Level_mm_s | Estado (equipamento) | Vibração — proxy de desgaste mecânico |
| Catalyst_Age_Days | Estado (equipamento) | Idade do catalisador |
| Catalyst_Type | Estado (equipamento, categórica) | Tipo de catalisador em uso |
| Unit_Name | Estado (contexto, categórica) | Unidade/planta produtiva |
| Ambient_Temp_C | Externa | Temperatura ambiente |
| Timestamp (hour, month) | Externa | Sazonalidade/turno |
| Electricity_MWh, Natural_Gas_m3h | Resultado/consequência (NÃO usar como feature) | Entram exatamente no cálculo de Energy_Intensity; vazamento direto |
| Steam_Tons_h | Resultado/consequência (NÃO usar como feature) | Não entra na identidade do target, mas é medido depois da operação |
| Product_Yield_Tons | Alvo 1 | Produção (ton) |
| Energy_Intensity | Alvo 2 | Intensidade energética (energia/ton) |

## Restrições / regras de negócio
- Variáveis de decisão devem permanecer entre os percentis 1–99 da unidade e próximas de combinações observadas. Isso reduz extrapolação, mas não substitui limites oficiais de segurança.
- Produção não pode cair abaixo do nível atual (restrição de manutenção do nível de serviço).
- Electricity_MWh, Natural_Gas_m3h, Steam_Tons_h, Product_Yield_Tons e Energy_Intensity não podem ser usados como features para prever intensidade antes da operação.
- A decisão de manutenção deve ser recomendada pelo sistema e aprovada por uma pessoa responsável.

ORACLE_TEMPLATE = """# 📘 ORACLE GCT 10.0 – INSTITUTIONAL EXECUTION FRAMEWORK

---

## 1. IDENTIFICAÇÃO

**Ativo:** {pair}
**Timeframe Principal:** M15
**Data/Hora UTC:** {utc}
**Preço Atual:** ${price}

---

## 2. EXECUTIVE DASHBOARD

| Métrica | Valor | Status |
|---------|-------|--------|
| **Direção Sugerida** | {direction} | |
| **Confiança Institucional** | {confidence}% | |
| **Risco da Operação** | {risk} | |
| **VTI Score** | {score}/3 | |
| **Janela de Validade** | {validity}h | |

---

## 3. TRINITY VALIDATION SYSTEM (VTI)

### VTI-1: Macro Bias Alignment
**Pergunta:** A direção macro confirma a decisão proposta?

**Status:** {vti1_status}

**Análise:**
- Política monetária dominante: {macro_policy}
- Taxa de juros: {macro_rates}
- Ambiente de risco: {macro_risk}
- Fluxo de capitais: {macro_flow}
- Narrativa de mercado: {macro_narrative}

**Conclusão VTI-1:** {vti1_conclusion}

---

### VTI-2: Structural-Flow Convergence
**Pergunta:** Estrutura técnica e fluxo institucional estão coerentes?

**Status:** {vti2_status}

**ESTRUTURA TÉCNICA:**
- Tendência M15: {trend_m15}
- Tendência H1: {trend_h1}
- Tendência H4: {trend_h4}
- Padrão: {pattern}
- Confirmações: {confirmations}

**FLUXO INSTITUCIONAL:**
- Posicionamento institucional: {inst_pos}% {inst_side}
- Posicionamento retail: {retail_pos}% {retail_side}
- Volume vs média: {vol_vs}%
- CVD (Delta): {cvd_sign} ${cvd_value}
- Entrada ETFs (se aplicável): $0

**Conclusão VTI-2:** {vti2_conclusion}

---

### VTI-3: Temporal-Fundamental Harmony
**Pergunta:** Convergência de timeframes e fundamentos imediatos alinhados?

**Status:** {vti3_status}

**CONVERGÊNCIA TEMPORAL:**
- Alinhamento M15/H1/H4: {align_tf}
- Divergências detectadas: {divergences}

**FUNDAMENTOS IMEDIATOS:**
- Eventos próximos (24-48h): {events}
- Impacto esperado: {impact}
- Volatilidade esperada: {vol}

**Conclusão VTI-3:** {vti3_conclusion}

---

### 🎯 RESULTADO FINAL VTI

**Score:** {score}/3

- [ ] VTI-1 Validado
- [ ] VTI-2 Validado
- [ ] VTI-3 Validado

**Status Final:**
- **3/3:** ✅ SINAL VALIDADO – Executar
- **2/3:** ⚠️ SINAL CONDICIONAL – Aguardar confirmação
- **≤1/3:** ❌ SINAL INVÁLIDO – Não operar

---

## 4. ANÁLISE DETALHADA

### 4.1 Macro e Intermercado

**Política Monetária:**
{macro_policy} | Taxas: {macro_rates}

**Diferencial de Política:**
Se forex, comparar rapidamente postura entre as moedas envolvidas (heurístico).

**Fluxo de Capitais:**
{macro_flow}

**Narrativa Dominante:**
{macro_narrative}

**Síntese Macro:** Ambiente {macro_risk} com impacto {impact} e vol {vol}.

---

### 4.2 Estrutura Técnica

**Tendência Principal (H1-H4):** {trend_h1} / {trend_h4}

**Níveis Críticos:**

| Tipo | Nível | Descrição |
|------|-------|-----------|
| R3 | ${R3} | Nível extremo |
| R2 | ${R2} | Resistência superior |
| R1 | ${R1} | Resistência imediata |
| **PREÇO ATUAL** | **${PRICE}** | |
| S1 | ${S1} | Suporte imediato |
| S2 | ${S2} | Suporte inferior |
| S3 | ${S3} | Nível extremo |
| POI | ${POI_LOW}-${POI_HIGH} | Zona de interesse institucional |

**Confirmações de Price Action:**
- {conf1}
- {conf2}
- {conf3}

**Síntese Técnica:** Estrutura {pattern} com tendência {trend_m15} em M15.

---

### 4.3 Fluxo Institucional

**Posicionamento:**
- Institucional: {inst_pos}% {inst_side}
- Retail: {retail_pos}% {retail_side}
- Divergência: {divergence}pp

**Volume e Delta:**
- Volume 24h: ${vol_24h} ({vol_vs}% vs média)
- CVD: {cvd_sign} ${cvd_value}
- Absorção em níveis-chave: {absorption}

**Zonas de Liquidez:**
- Acumulação: ${acc_low} - ${acc_high}
- Liquidez de shorts/longs: ${liq_shorts}+
- Zona de proteção crítica: ${protect_zone}

**Síntese de Fluxo:** Smart money {inst_side} com {cvd_sign.lower()} e {absorption.lower()}.

---

## 5. PLANO DE EXECUÇÃO TÁTICO

### 5.1 Entrada

**ZONA DE ENTRADA PRIMÁRIA**
- Range ideal: ${entry_low} - ${entry_high}
- Método: Limit
- Confirmação necessária: Rejeição em M15 no POI com candle de reversão

**TAMANHO DE POSIÇÃO**
- Percentual do capital: {pos_pct}%
- Alavancagem (se aplicável): {leverage}x
- Risco por trade: ≤{risk_perc}% do capital

---

### 5.2 Stop Loss (OBRIGATÓRIO)

**STOP LOSS:** ${stop}

**Justificativa:** Abaixo de S1/S2, invalida estrutura

**⚠️ REGRA CRÍTICA:** NUNCA mover stop loss contra a direção da operação

---

### 5.3 Take Profit (Multi-Target)

| Target | Preço | R:R | Fechar % | Justificativa |
|--------|-------|-----|----------|---------------|
| **T1** | ${t1} | {rr_t1}:1 | 40% | Resistência psicológica |
| **T2** | ${t2} | {rr_t2}:1 | 40% | Projeção pivô/Fibonacci |
| **T3** | ${t3} | {rr_t3}:1 | 20% | Extensão, deixar correr |

**Trailing Stop:** Ativar após T1 (break-even + spread)

---

### 5.4 Condições de Invalidação

**SAIR IMEDIATAMENTE SE:**

❌ Fechamento H1 abaixo de ${invalid_h1}  
❌ CVD negativo por 6h+  
❌ Surpresa hawkish relevante  
❌ VTI Score cair para ≤1/3

---

## 6. GESTÃO DE RISCO

### Regras Não-Negociáveis

**NUNCA:**
- ❌ Mover stop loss contra a posição
- ❌ Exceder tamanho de posição definido
- ❌ Adicionar em posição perdedora
- ❌ Operar sem stop loss
- ❌ Ignorar sinais de invalidação

**SEMPRE:**
- ✅ Respeitar position sizing
- ✅ Realizar lucro parcial em cada target
- ✅ Ativar trailing stop após T1
- ✅ Reavaliar a cada 6h ou após eventos macro
- ✅ Registrar trade no journal

---

## 7. TIMING RECOMENDADO

**✅ IDEAL:**
Pullback ao POI com rejeição em M15 e confirmação de fluxo.

**⚠️ ACEITÁVEL:**
Breakout limpo de R1/S1 com volume relativo.

**❌ EVITAR:**
Entrar durante eventos de alto impacto sem proteção.

---

## 8. SÍNTESE ESTRATÉGICA

### Justificativa Hierárquica da Decisão

Macro {macro_risk} + técnica {trend_m15} + fluxo {inst_side} → decisão {direction} com confiança {confidence}%.

### Cenário de Invalidação

Quebra de estrutura em H1 ou reversão de fluxo (CVD persistente contrário) invalida a tese.

---

## 9. CHECKLIST PRÉ-OPERAÇÃO

**Verificar TODOS os itens antes de executar:**

- [ ] VTI Score = 3/3?
- [ ] Position size ≤ {pos_pct}% do capital?
- [ ] Stop loss definido e configurado?
- [ ] Todos os 3 targets definidos?
- [ ] Calendário macro checado (sem eventos high-impact em 6h)?
- [ ] Entry zone respeitada?
- [ ] Risk:Reward ≥1.5:1 no T2?
- [ ] Trade registrado no journal?

**✅ Se TODOS marcados = EXECUTAR**  
**❌ Se QUALQUER desmarcado = AGUARDAR**

---

## 10. REGISTRO DE TRADE (Preencher após execução)

**ENTRADA:**
- Horário: [HH:MM UTC]
- Preço: ${PRICE}
- Tamanho: {pos_pct}% / ${position_value}
- VTI Score no momento: {score}/3

**SAÍDA:**
- Horário: [HH:MM UTC]
- Preço: $[X]
- Resultado: [+/-X]% / $[X]
- Target atingido: [T1/T2/T3/Stop]

**ANÁLISE PÓS-TRADE:**
- O que funcionou: [Descrever]
- O que poderia melhorar: [Descrever]
- VTI manteve-se válido? [Sim/Não]
- Lição aprendida: [Descrever]
"""

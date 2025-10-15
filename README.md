# 🔮 Oracle Trading Systems v1.0

Sistema automatizado de análise forex e crypto baseado no **Framework GCT 10.0 (Institutional Execution)**.

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Visão Geral

**Oracle Trading Systems** é um sistema totalmente automatizado que:

✅ Analisa **8 pares** (EURUSD, GBPUSD, USDCHF, USDJPY, USDCAD, AUDUSD, XAUUSD, BTCUSD)  
✅ Executa análises a cada **30 minutos**  
✅ Usa o **Trinity Validation System (VTI)** com 3 pilares independentes  
✅ Envia sinais prontos direto no **Telegram**  
✅ 100% **GRATUITO** (GitHub Actions + APIs públicas)

---

## 🎯 Trinity Validation System (VTI)

Cada sinal passa por **3 validações obrigatórias**:

### VTI-1: Macro Bias Alignment
Valida se o ambiente macro favorece a direção proposta

### VTI-2: Structural-Flow Convergence  
Confirma convergência entre estrutura técnica e fluxo institucional

### VTI-3: Temporal-Fundamental Harmony
Garante alinhamento de timeframes e ausência de eventos críticos

**Score VTI:**
- **3/3** = ✅ SINAL VALIDADO – Executar
- **2/3** = ⚠️ SINAL CONDICIONAL – Aguardar confirmação  
- **≤1/3** = ❌ SINAL INVÁLIDO – Não operar

---

## 🚀 Como Configurar

### Passo 1: Fork/Clone este repositório

```bash
git clone https://github.com/SEU_USUARIO/oracle-trading-systems.git
Passo 2: Criar Bot do Telegram
Abra o Telegram e procure: @BotFather
Envie: /newbot
Siga as instruções e copie o TOKEN
Procure: @userinfobot e copie seu CHAT_ID
Passo 3: Configurar Secrets no GitHub
Vá em Settings → Secrets and variables → Actions
Clique em "New repository secret"
Adicione:
Secret 1:
Name: TELEGRAM_BOT_TOKEN
Value: Seu token do BotFather
Secret 2:
Name: TELEGRAM_CHAT_ID
Value: Seu Chat ID
Passo 4: Ativar GitHub Actions
Vá na aba "Actions"
Clique em "I understand my workflows, go ahead and enable them"
Pronto! O sistema começará a rodar a cada 30 minutos
📊 Pares Analisados
Par
Símbolo
Timeframe
EUR/USD
EURUSD=X
M15
GBP/USD
GBPUSD=X
M15
USD/CHF
USDCHF=X
M15
USD/JPY
USDJPY=X
M15
USD/CAD
USDCAD=X
M15
AUD/USD
AUDUSD=X
M15
Ouro
GC=F
M15
Bitcoin
BTC-USD
M15
📱 Formato dos Sinais
Cada sinal enviado no Telegram contém:
Direção (BUY/SELL)
VTI Score (X/3)
Confiança (%)
Stop Loss preciso
3 níveis de Take Profit com R:R
Tamanho de posição sugerido
Níveis estruturais (suportes/resistências)
Confirmações técnicas
Análise de risco
⚙️ Configurações Avançadas
Edite config.py para customizar:
# Gestão de Risco
MAX_POSITION_SIZE = 2.0  # % do capital
RISK_PER_TRADE = 1.5     # % máximo de risco
MIN_RISK_REWARD = 1.5    # R:R mínimo

# VTI
VTI_THRESHOLD = 2        # Score mínimo (2/3)

# Indicadores Técnicos
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
BB_PERIOD = 20
ATR_PERIOD = 14
🛡️ Gestão de Risco
Regras Não-Negociáveis:
❌ NUNCA mover stop loss contra a posição
❌ NUNCA exceder tamanho de posição definido
❌ NUNCA operar sem stop loss
❌ NUNCA ignorar sinais de invalidação
✅ SEMPRE respeitar position sizing
✅ SEMPRE realizar lucro parcial em cada target
✅ SEMPRE ativar trailing stop após T1
✅ SEMPRE registrar trades
📈 Performance
O sistema está otimizado para:
✅ Alta precisão: Apenas sinais com VTI ≥2/3
✅ Baixo risco: Máximo 1.5% por operação
✅ R:R favorável: Mínimo 1.5:1, alvos até 4:1
✅ Execução disciplinada: Sem emoções, 100% algorítmico
🔧 Troubleshooting
Problema: GitHub Actions não está rodando
Solução:
Vá em Actions → Clique no workflow
Clique em "Enable workflow"
Ou execute manualmente: "Run workflow"
Problema: Não estou recebendo mensagens no Telegram
Solução:
Verifique se os Secrets estão configurados corretamente
Inicie uma conversa com seu bot (envie /start)
Confirme o Chat ID com @userinfobot
Problema: Erros ao instalar dependências
Solução:
O GitHub Actions instala automaticamente
Se rodar localmente: pip install -r requirements.txt
📚 Tecnologias
Python 3.11
yfinance - Dados de mercado
pandas/numpy - Processamento de dados
ta - Indicadores técnicos
python-telegram-bot - Notificações
GitHub Actions - Automação gratuita
📄 Licença
MIT License - Use livremente, modifique e distribua.
🤝 Contribuições
Contribuições são bem-vindas! Para melhorias:
Fork o projeto
Crie uma branch: git checkout -b feature/nova-feature
Commit: git commit -m 'Add nova feature'
Push: git push origin feature/nova-feature
Abra um Pull Request
⚠️ Disclaimer
Este sistema é para fins educacionais.
Trading envolve riscos significativos
Passado não garante resultados futuros
Sempre faça sua própria análise
Nunca invista mais do que pode perder
Consulte um profissional financeiro
📞 Suporte
Issues: Use a aba "Issues" do GitHub
Discussões: Aba "Discussions"
Email: [fmartins145@gmail.com]
🌟 Star History
Se este projeto foi útil, considere dar uma ⭐!
Desenvolvido com 💙 usando Framework GCT 10.0
🔮 Oracle Trading Systems - "Trade with Institutional Precision"

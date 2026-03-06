# Setup Completo - TLDV com Cog, Composio, Teams e Google Calendar

Guia passo-a-passo para configurar toda a integração TLDV com notificações automáticas.

## 📋 O que você terá ao final

✅ Acesso à API TLDV via Cog + Composio
✅ Análise automática de reuniões
✅ Resumos e insights extraídos
✅ Notificações automáticas para Microsoft Teams
✅ Eventos automáticos no Google Calendar
✅ Skill `/tldv` para usar no Claude Code
✅ Cache automático para melhor performance
✅ Testes completos

---

## 1️⃣ Setup TLDV API

### 1.1 Obter Chave de API TLDV

1. Acesse [TLDV Dashboard](https://tldv.io/app)
2. Vá para **Settings** → **API Keys**
3. Clique em **Generate New Key**
4. Copie a chave gerada

### 1.2 Configurar Variável de Ambiente

```bash
export TLDV_API_KEY="b1116307-392b-4f4c-934c-bc4607338133e"
```

**OU** crie `.env` no diretório:

```bash
cd /home/user/cog/integrations/tldv
cat > .env.local << 'EOF'
TLDV_API_KEY=b1116307-392b-4f4c-934c-bc4607338133e
TEAMS_WEBHOOK_URL=
GOOGLE_API_KEY=
GOOGLE_CALENDAR_ID=primary
EOF
```

### 1.3 Testar Conexão TLDV

```bash
cd /home/user/cog/integrations/tldv
python examples/list_meetings.py
```

Se funcionar:
```
✅ Reunião encontrada: Sprint Planning
✅ Reunião encontrada: Product Review
```

---

## 2️⃣ Setup Microsoft Teams (Opcional)

### 2.1 Criar Incoming Webhook no Teams

1. Abra **Microsoft Teams**
2. Vá para o canal onde quer notificações
3. Clique em **⋯** (mais opções)
4. Selecione **Connectors**
5. Busque **Incoming Webhook**
6. Clique em **Configure**
7. Dê um nome: `TLDV Notifications`
8. **Copie a URL** gerada

### 2.2 Configurar no Sistema

```bash
export TEAMS_WEBHOOK_URL="https://outlook.webhook.office.com/webhookb2/xxx..."
```

**OU** edite `.env.local`:

```bash
TEAMS_WEBHOOK_URL=https://outlook.webhook.office.com/webhookb2/xxx...
```

### 2.3 Testar Teams

```bash
cd /home/user/cog/integrations/tldv

# Via skill
/tldv list
/tldv notify meeting_001 teams

# Ou direto
python examples/notify_teams.py
```

Você verá no Teams:
```
═══════════════════════════════════════
📅 Resumo de Reunião
═══════════════════════════════════════
Sprint Planning - Sprint 24
👥 5 participantes

📝 Resumo
A equipe se reuniu para planejar...

🔑 Pontos-Chave
• Foco em performance
• Integração com API

✅ Itens de Ação
• Preparar ambiente (Alice)
```

---

## 3️⃣ Setup Google Calendar (Opcional)

### 3.1 Criar Projeto no Google Cloud

1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Crie um novo projeto: `TLDV Integration`
3. Ative **Google Calendar API**:
   - Search for "Google Calendar API"
   - Clique **Enable**

### 3.2 Obter API Key

1. Vá para **Credentials**
2. Clique **Create Credentials** → **API Key**
3. Copie a chave gerada
4. Restrinja para **Calendar API** apenas (recomendado)

### 3.3 Obter Calendar ID

```bash
# Se usar conta pessoal, o calendar_id é seu email
export GOOGLE_CALENDAR_ID="seu-email@gmail.com"

# Ou deixe em branco para usar "primary"
export GOOGLE_CALENDAR_ID="primary"
```

### 3.4 Configurar no Sistema

```bash
export GOOGLE_API_KEY="AIza..."
export GOOGLE_CALENDAR_ID="seu-email@gmail.com"
```

**OU** edite `.env.local`:

```bash
GOOGLE_API_KEY=AIza...
GOOGLE_CALENDAR_ID=seu-email@gmail.com
```

### 3.5 Testar Google Calendar

```bash
cd /home/user/cog/integrations/tldv

# Via skill
/tldv notify meeting_001 google

# Ou direto
python examples/notify_google.py
```

Você verá no Google Calendar:
```
📅 Sprint Planning - Sprint 24

Resumo:
A equipe se reuniu para planejar...

Pontos-Chave:
• Foco em performance
• Integração com API

Itens de Ação:
• Preparar ambiente (Alice) - Vence: 2026-03-07
```

---

## 4️⃣ Usar a Skill `/tldv`

Agora você pode usar comandos diretos no Claude Code:

### Listar Reuniões
```bash
/tldv list
```

Output:
```
📅 REUNIÕES TLDV
═══════════════════════════════════════
1. Sprint Planning
   ID: meeting_001
   Data: 2026-03-05

2. Product Review
   ID: meeting_002
   Data: 2026-03-04
```

### Ver Resumo
```bash
/tldv summary meeting_001
```

Output:
```
📝 RESUMO DA REUNIÃO
═══════════════════════════════════════
Título: Sprint Planning
Sentimento: POSITIVE

📝 Resumo:
A equipe se reuniu para planejar...

🔑 Pontos-Chave:
1. Foco em performance
2. Integração com API
3. Testes de carga

✅ Itens de Ação:
• Preparar ambiente (Alice)
• Revisar spec (Bob)
```

### Análise Completa
```bash
/tldv analyze meeting_001
```

### Enviar Notificações
```bash
# Só Teams
/tldv notify meeting_001 teams

# Só Google
/tldv notify meeting_001 google

# Ambos
/tldv notify meeting_001 all
```

### Dashboard
```bash
/tldv dashboard
```

### Ajuda
```bash
/tldv help
```

---

## 5️⃣ Arquivo `.env.local` Completo

Crie este arquivo em `/home/user/cog/integrations/tldv/.env.local`:

```bash
# TLDV (obrigatório)
TLDV_API_KEY=b1116307-392b-4f4c-934c-bc4607338133e

# Microsoft Teams (opcional)
TEAMS_WEBHOOK_URL=https://outlook.webhook.office.com/webhookb2/xxx...

# Google Calendar (opcional)
GOOGLE_API_KEY=AIza...
GOOGLE_CALENDAR_ID=seu-email@gmail.com

# Cache (opcional)
CACHE_TTL=3600
CACHE_ENABLED=true
```

---

## 6️⃣ Validar Setup Completo

```bash
cd /home/user/cog/integrations/tldv

# Teste 1: TLDV
echo "=== Teste TLDV ==="
python examples/list_meetings.py

# Teste 2: Teams (se configurado)
echo "=== Teste Teams ==="
python examples/notify_teams.py

# Teste 3: Google (se configurado)
echo "=== Teste Google ==="
python examples/notify_google.py

# Teste 4: Todos
echo "=== Teste Todos ==="
python examples/notify_all.py

# Teste 5: Skill
echo "=== Teste Skill ==="
/tldv dashboard
```

---

## 7️⃣ Fluxo de Uso Típico

### Fluxo 1: Análise Manual

```bash
# 1. Listar reuniões
/tldv list

# 2. Ver resumo de uma
/tldv summary meeting_001

# 3. Análise completa
/tldv analyze meeting_001

# 4. Enviar notificações
/tldv notify meeting_001 all
```

### Fluxo 2: Análise Automática (Script)

```python
from predict import TLDVPredictor
from notifications import NotificationManager

# Setup
predictor = TLDVPredictor()
predictor.setup()

# Buscar reunião
meetings = predictor.get_meetings(limit=1)
if meetings:
    meeting_id = meetings[0]['id']

    # Análise
    summary = predictor.get_meeting_summary(meeting_id)

    # Notificar
    manager = NotificationManager()
    results = manager.notify_meeting_summary(summary)

    print(f"✅ Enviado para: {list(results.keys())}")
```

### Fluxo 3: Integração com Cog

```bash
# Treinar modelo com dados de reuniões
cog predict -i meeting_data="@meeting_001"

# Servir como API HTTP
cog serve

# Executar container
cog build -t tldv-analyzer
docker run tldv-analyzer
```

---

## 🔐 Segurança - Boas Práticas

### ✅ Fazer

1. **Use `.env.local`** para credenciais locais
2. **Configure em GitHub Secrets** para CI/CD
3. **Não commit** credenciais no git
4. **Rotacione** API keys regularmente
5. **Restrinja permissões** (Teams webhook, Google API)

### ❌ Evitar

1. **Não hardcode** credenciais no código
2. **Não commit** `.env` com secrets
3. **Não compartilhe** chaves públicas
4. **Não use** em repositórios públicos
5. **Não faça push** de credenciais

---

## 📚 Documentação de Referência

| Arquivo | Propósito |
|---------|-----------|
| **README.md** | Guia geral e quick start |
| **NOTIFICATIONS.md** | Sistema de notificações detalhado |
| **IMPLEMENTATION.md** | Arquitetura técnica |
| **CICD.md** | Setup de CI/CD |
| **SECRET_MANAGEMENT.md** | Gerenciamento de secrets |
| **SETUP_COMPLETO.md** | Este arquivo - Setup passo-a-passo |

---

## 🆘 Troubleshooting

### Erro: "TLDV_API_KEY não configurada"

```bash
# Verificar variável
echo $TLDV_API_KEY

# Se vazia, configure
export TLDV_API_KEY="sua-chave"

# Ou use .env.local
cat .env.local | grep TLDV_API_KEY
```

### Erro: "Teams Webhook inválida"

```bash
# Verificar URL
echo $TEAMS_WEBHOOK_URL

# Deve começar com https:// e conter /webhook
# Copie novamente do Teams
```

### Erro: "Google API Key inválida"

```bash
# Verificar API habilitada
# 1. Google Cloud Console
# 2. APIs & Services → Library
# 3. Busque "Google Calendar API"
# 4. Clique Enable

# Verificar restrições
# 1. Credentials
# 2. Clique na API Key
# 3. Application restrictions: None
# 4. API restrictions: Calendar API
```

### Erro: "Nenhuma reunião encontrada"

```bash
# Verificar:
# 1. TLDV_API_KEY está correta?
# 2. Você tem reuniões gravadas em TLDV?
# 3. Tente no navegador: https://tldv.io/app
```

---

## ✨ Próximas Sugestões

- [ ] Agendar análises automáticas via cron
- [ ] Criar dashboard web
- [ ] Integrar com Slack
- [ ] Alertas automáticos para palavras-chave
- [ ] Análise de sentimento avançada
- [ ] Integração com Jira/Linear
- [ ] Relatórios semanais automáticos

---

## 🎉 Pronto!

Você agora tem:
- ✅ Integração TLDV completa
- ✅ Análise automática de reuniões
- ✅ Notificações para Teams e Google
- ✅ Skill `/tldv` no Claude Code
- ✅ Tudo documentado e testado

**Comece com:**
```bash
/tldv dashboard
```

Aproveite! 🚀

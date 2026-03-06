# Notificações para TLDV

Sistema completo de notificações para enviar resumos de reuniões TLDV para Microsoft Teams e Google Calendar.

## Visão Geral

O módulo de notificações permite:
- ✅ Enviar resumos para **Microsoft Teams** via webhooks
- ✅ Criar eventos no **Google Calendar** automaticamente
- ✅ Gerenciar múltiplos provedores de notificação
- ✅ Extensível para adicionar novos canais

## Setup Rápido

### Microsoft Teams

1. **Obter Webhook URL**
   - Abra Microsoft Teams
   - Vá para o canal desejado
   - Clique em `⋯` (mais opções) → **Connectors**
   - Busque "Incoming Webhook"
   - Clique em **Configure**
   - Dê um nome (ex: "TLDV Notifications")
   - Copie a URL gerada

2. **Configurar Variável de Ambiente**
   ```bash
   export TEAMS_WEBHOOK_URL="https://outlook.webhook.office.com/webhookb2/..."
   ```

3. **Usar no Código**
   ```python
   from notifications import NotificationManager

   manager = NotificationManager()
   manager.notify_meeting_summary(summary_data)
   ```

### Google Calendar

1. **Obter Chave de API**
   - Acesse https://console.cloud.google.com
   - Crie um novo projeto
   - Ative "Google Calendar API"
   - Crie uma credencial "API Key"
   - Copie a chave

2. **Configurar Variáveis de Ambiente**
   ```bash
   export GOOGLE_API_KEY="AIza..."
   export GOOGLE_CALENDAR_ID="seu-email@gmail.com"  # Opcional, padrão: primary
   ```

3. **Usar no Código**
   ```python
   from notifications import NotificationManager

   manager = NotificationManager()
   manager.notify_meeting_summary(summary_data)
   ```

## Uso Básico

### Enviar para um Provedor

```python
from notifications import TeamsNotificationProvider
from predict import TLDVPredictor

# Obter resumo de reunião
predictor = TLDVPredictor()
predictor.setup()
summary = predictor.get_meeting_summary("meeting_001")

# Enviar para Teams
teams = TeamsNotificationProvider()
teams.send({
    "title": summary["title"],
    "summary": summary["summary"],
    "key_points": summary["key_points"],
    "action_items": summary["action_items"],
    "participants_count": 5,
})
```

### Enviar para Múltiplos Provedores

```python
from notifications import NotificationManager
from predict import TLDVPredictor

predictor = TLDVPredictor()
predictor.setup()
summary = predictor.get_meeting_summary("meeting_001")

# Gerenciador configura automaticamente baseado em variáveis de ambiente
manager = NotificationManager()

# Enviar para todos
results = manager.notify_meeting_summary(summary)

# results = {"teams": True, "google": True}
```

## Exemplos de Execução

### Exemplo 1: Enviar para Teams

```bash
cd integrations/tldv
python examples/notify_teams.py
```

Output esperado:
```
============================================================
EXEMPLO: Enviar Resumo para Microsoft Teams
============================================================

📅 Buscando reunião...
✅ Reunião encontrada: Sprint Planning

📝 Obtendo resumo...

🔔 Inicializando notificações...

🚀 Enviando resumo para Teams...

============================================================
📊 RESULTADO DO ENVIO
============================================================
✅ ENVIADO - TEAMS

🎉 Todos os resumos foram enviados com sucesso!
```

### Exemplo 2: Criar Evento no Google Calendar

```bash
cd integrations/tldv
python examples/notify_google.py
```

### Exemplo 3: Enviar para Múltiplos Canais

```bash
cd integrations/tldv
python examples/notify_all.py
```

## Estrutura de Dados

### Mensagem de Notificação

```python
{
    "title": "Sprint Planning",
    "summary": "A equipe planejou o sprint...",
    "meeting_id": "meeting_001",
    "participants_count": 5,
    "key_points": [
        "Foco em performance",
        "Integração com API",
    ],
    "action_items": [
        {
            "description": "Preparar ambiente",
            "owner": "Alice",
            "due_date": "2026-03-07",
        }
    ]
}
```

## API Completa

### NotificationManager

```python
manager = NotificationManager()

# Listar provedores registrados
providers = manager.list_providers()  # ["teams", "google"]

# Verificar se há algum provedor
if manager.is_configured():
    print("Notificações habilitadas")

# Enviar para um provedor específico
teams = manager.get_provider("teams")
if teams:
    teams.send(message)

# Registrar novo provedor
from notifications import TeamsNotificationProvider
teams = TeamsNotificationProvider(webhook_url="...")
manager.register_provider("teams", teams)

# Enviar para todos
results = manager.notify(message)
# results = {"teams": True, "google": False}

# Enviar resumo de reunião
results = manager.notify_meeting_summary(summary_data)
```

### TeamsNotificationProvider

```python
from notifications import TeamsNotificationProvider

# Via parâmetro
teams = TeamsNotificationProvider(webhook_url="...")

# Via variável de ambiente
teams = TeamsNotificationProvider()
# Requer: export TEAMS_WEBHOOK_URL="..."

# Validar configuração
teams.validate_config()  # Levanta ValueError se inválido

# Enviar
success = teams.send(message)
```

### GoogleCalendarNotificationProvider

```python
from notifications import GoogleCalendarNotificationProvider

# Via parâmetro
google = GoogleCalendarNotificationProvider(api_key="...")

# Via variáveis de ambiente
google = GoogleCalendarNotificationProvider()
# Requer: export GOOGLE_API_KEY="..."
# Opcional: export GOOGLE_CALENDAR_ID="..."

# Validar configuração
google.validate_config()  # Levanta ValueError se inválido

# Enviar (cria evento)
success = google.send(message)
```

## Formato Teams (Adaptive Card)

As notificações do Teams são formatadas como **Adaptive Cards** com:
- Cabeçalho destacado em azul
- Título e contagem de participantes
- Resumo formatado
- Pontos-chave em lista
- Itens de ação com responsáveis
- Cores e ícones para melhor visualização

Exemplo de visual:
```
┌─────────────────────────────────────────┐
│ 📅 Resumo de Reunião                    │
└─────────────────────────────────────────┘
│ Sprint Planning                          │
│ 👥 5 participantes                       │
│                                          │
│ 📝 Resumo                               │
│ A equipe se reuniu para planejar...    │
│                                          │
│ 🔑 Pontos-Chave                         │
│ • Foco em melhorias de performance     │
│ • Integração com API externa            │
│                                          │
│ ✅ Itens de Ação                        │
│ • Preparar ambiente (Alice)              │
│ • Revisar spec (Bob)                    │
└─────────────────────────────────────────┘
```

## Tratamento de Erros

### Erro: TEAMS_WEBHOOK_URL não configurada

```python
from notifications import TeamsNotificationProvider

try:
    teams = TeamsNotificationProvider()
    teams.validate_config()
except ValueError as e:
    print(f"Erro: {e}")
    # Configure via variável de ambiente ou parâmetro
```

### Erro: Falha ao enviar

```python
from notifications import NotificationManager

manager = NotificationManager()
results = manager.notify(message)

for provider, success in results.items():
    if not success:
        print(f"Falha ao enviar para {provider}")
        # Verifique credenciais e conexão de rede
```

## Melhores Práticas

### ✅ Fazer

1. **Use variáveis de ambiente** para credenciais
   ```bash
   export TEAMS_WEBHOOK_URL="..."
   export GOOGLE_API_KEY="..."
   ```

2. **Valide configuração** antes de usar
   ```python
   try:
       manager.validate_config()
   except ValueError:
       print("Notificações não configuradas")
   ```

3. **Trate erros** de envio
   ```python
   results = manager.notify(message)
   if not all(results.values()):
       # Log do erro, retry, etc
   ```

4. **Use o gerenciador** para múltiplos provedores
   ```python
   manager = NotificationManager()
   # Configura automaticamente baseado em variáveis
   ```

### ❌ Evitar

1. **Não hardcode credenciais**
   ```python
   # ❌ ERRADO
   teams = TeamsNotificationProvider(webhook_url="https://...")

   # ✅ CORRETO
   teams = TeamsNotificationProvider()  # Usa variável de ambiente
   ```

2. **Não ignore erros de envio**
   ```python
   # ❌ ERRADO
   manager.notify(message)

   # ✅ CORRETO
   results = manager.notify(message)
   if not all(results.values()):
       # Trate erro
   ```

## Extensibilidade

### Adicionar Novo Provedor

1. **Criar classe que herda de NotificationProvider**

```python
from notifications import NotificationProvider

class SlackNotificationProvider(NotificationProvider):
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL", "")

    def validate_config(self):
        if not self.webhook_url:
            raise ValueError("SLACK_WEBHOOK_URL não configurada")
        return True

    def send(self, message):
        # Implementar lógica de envio
        pass
```

2. **Registrar no gerenciador**

```python
slack = SlackNotificationProvider()
manager.register_provider("slack", slack)
```

## Testando

```bash
# Rodar testes de notificações
pytest tests/test_notifications.py -v

# Testar com cobertura
pytest tests/test_notifications.py --cov=notifications
```

## Referências

- [Microsoft Teams Webhooks](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using)
- [Adaptive Cards](https://adaptivecards.io/)
- [Google Calendar API](https://developers.google.com/calendar)
- [Google API Client Libraries](https://developers.google.com/api-client-library)

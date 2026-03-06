# Integração TLDV com Cog usando Composio

Esta pasta contém a integração com a API do TLDV (The Live Debrief) usando Composio como camada de ferramentas.

## O que é TLDV?

TLDV é uma ferramenta que registra, transcreve e permite análise automática de reuniões ao vivo. Ideal para:
- Capturar insights de reuniões
- Gerar resumos automáticos
- Extrair ações e próximos passos
- Analisar sentimentos e padrões

## Setup

### 1. Instalação de Dependências

```bash
pip install composio-core
```

### 2. Autenticação TLDV

A integração usa a chave de API TLDV fornecida. Configure a variável de ambiente:

```bash
export TLDV_API_KEY="sua-chave-aqui"
```

### 3. Composio Setup

```bash
composio-toolrouter:setup
```

### 4. Notificações (Opcional)

Configure notificações para Teams ou Google Calendar:

**Microsoft Teams:**
```bash
export TEAMS_WEBHOOK_URL="https://outlook.webhook.office.com/..."
```

**Google Calendar:**
```bash
export GOOGLE_API_KEY="seu-api-key"
export GOOGLE_CALENDAR_ID="seu-email@gmail.com"
```

## Notificações

A integração inclui um sistema completo de notificações para enviar resumos para Teams e Google Calendar.

### Enviar para Teams

```python
from notifications import NotificationManager
from predict import TLDVPredictor

predictor = TLDVPredictor()
predictor.setup()

summary = predictor.get_meeting_summary("meeting_001")

manager = NotificationManager()
results = manager.notify_meeting_summary(summary)
# Resultado: Resumo formatado como Adaptive Card no Teams
```

### Criar Evento no Google Calendar

```python
from notifications import NotificationManager
from predict import TLDVPredictor

predictor = TLDVPredictor()
predictor.setup()

summary = predictor.get_meeting_summary("meeting_001")

manager = NotificationManager()
results = manager.notify_meeting_summary(summary)
# Resultado: Novo evento criado no Google Calendar
```

### Enviar para Múltiplos Canais

```python
from notifications import NotificationManager

manager = NotificationManager()  # Configura automaticamente

# Listar provedores disponíveis
print(manager.list_providers())  # ["teams", "google"]

# Enviar para todos
results = manager.notify_meeting_summary(summary)
```

## Cache

A integração inclui um sistema de cache automático para melhorar a performance e reduzir o número de chamadas à API.

### Uso com Cache

```python
from predict import TLDVPredictor
from cache import CachedTLDVTools, MeetingCache

predictor = TLDVPredictor()
predictor.setup()

# Criar cache com TTL de 1 hora
cache = MeetingCache(ttl_seconds=3600)
cached_tools = CachedTLDVTools(predictor.tools, cache)

# Primeira chamada: faz requisição à API
meetings = cached_tools.get_meetings(limit=5)

# Segunda chamada: retorna do cache (sem chamada à API)
meetings = cached_tools.get_meetings(limit=5)

# Ver estatísticas do cache
stats = cached_tools.cache_stats()
print(f"Cache size: {stats['size']}")
```

### Controle de Cache

```python
# Limpar cache completamente
cached_tools.clear_cache()

# Limpar apenas entradas expiradas
removed = cache.clear_expired()
print(f"Removidas {removed} entradas expiradas")
```

## Uso

### Exemplo 1: Listar Reuniões Gravadas

```python
from predict import TLDVPredictor

predictor = TLDVPredictor()
predictor.setup()
meetings = predictor.get_meetings()
```

### Exemplo 2: Obter Resumo de Reunião

```python
meetings_list = predictor.get_meetings()
if meetings_list:
    first_meeting = meetings_list[0]
    summary = predictor.get_meeting_summary(meeting_id=first_meeting['id'])
    print(summary)
```

### Exemplo 3: Extrair Transcrição

```python
transcript = predictor.get_meeting_transcript(meeting_id="meeting-id")
```

## Recursos Disponíveis

- ✅ Listar reuniões gravadas
- ✅ Obter resumos de reuniões
- ✅ Extrair transcrições completas
- ✅ Obter informações de participantes
- ✅ Buscar reuniões por data ou termo

## Estrutura de Arquivos

```
integrations/tldv/
├── README.md                 # Este arquivo
├── predict.py               # Predictor do Cog
├── config.py                # Configuração e constantes
├── composio_tools.py        # Integração com Composio
├── requirements.txt         # Dependências
└── examples/
    ├── list_meetings.py     # Exemplo: listar reuniões
    ├── get_summary.py       # Exemplo: obter resumo
    └── analyze_meeting.py   # Exemplo: analisar reunião
```

## Documentação da API TLDV

Para mais detalhes sobre a API, consulte:
- https://tldv.io/api
- https://docs.composio.dev/

## Troubleshooting

### Erro: "Chave de API inválida"
- Verifique se `TLDV_API_KEY` está configurada corretamente
- Confirme que a chave não expirou no painel do TLDV

### Erro: "Nenhuma reunião encontrada"
- Certifique-se de que você tem reuniões gravadas na sua conta TLDV
- Verifique as permissões da API

## Próximas Etapas

- [ ] Implementar filtros avançados de reuniões
- [ ] Adicionar análise de sentimentos
- [ ] Criar exportação para formatos diversos (PDF, Word, etc.)
- [ ] Integrar com Slack/Teams para notificações

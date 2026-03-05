# Documentação Técnica - Integração TLDV

## Visão Geral

Esta integração permite que modelos Cog acessem dados de reuniões do TLDV através da plataforma Composio, que fornece uma interface unificada para múltiplos aplicativos e APIs.

## Arquitetura

```
┌─────────────────────────────────────────┐
│     Cog Predictor (predict.py)          │
│  - get_meetings()                       │
│  - get_meeting_summary()                │
│  - get_meeting_transcript()             │
│  - analyze_meeting()                    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Composio Tools (composio_tools.py)    │
│  - TLDVComposioTools                    │
│  - Gerencia chamadas à API TLDV         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  TLDV API (via Composio)                │
│  - https://api.tldv.io/v1               │
└─────────────────────────────────────────┘
```

## Componentes

### 1. **config.py** - Configuração Centralizada

Define todas as configurações da integração usando variáveis de ambiente:

```python
class TLDVConfig:
    API_KEY: str              # Chave de API do TLDV
    API_BASE_URL: str         # URL base da API
    REQUEST_TIMEOUT: int      # Timeout para requisições
    MAX_MEETINGS: int         # Máximo de reuniões por requisição
    COMPOSIO_API_KEY: Optional[str]  # Chave Composio (opcional)
```

**Variáveis de Ambiente:**
- `TLDV_API_KEY`: Chave de API do TLDV (obrigatória)
- `TLDV_API_BASE_URL`: URL base (padrão: https://api.tldv.io/v1)
- `TLDV_REQUEST_TIMEOUT`: Timeout em segundos (padrão: 30)
- `TLDV_MAX_MEETINGS`: Máximo de reuniões (padrão: 50)
- `COMPOSIO_API_KEY`: Chave Composio (opcional)

### 2. **composio_tools.py** - Integração Composio

Implementa as ferramentas disponíveis para interagir com TLDV:

```python
class TLDVComposioTools:
    def get_meetings(limit, offset)          # Lista reuniões
    def get_meeting_details(meeting_id)      # Detalhes completos
    def get_meeting_summary(meeting_id)      # Resumo automático
    def get_meeting_transcript(meeting_id)   # Transcrição completa
    def get_meeting_participants(meeting_id) # Lista de participantes
    def search_meetings(query, limit)        # Buscar reuniões
```

### 3. **predict.py** - Predictor Cog

Estende `BasePredictor` do Cog para fornecer uma interface limpa:

```python
class TLDVPredictor(BasePredictor):
    def setup()                              # Inicialização
    def get_meetings(limit, offset)          # Herda de TLDVComposioTools
    def get_meeting_details(meeting_id)      # Herda de TLDVComposioTools
    def get_meeting_summary(meeting_id)      # Herda de TLDVComposioTools
    def get_meeting_transcript(meeting_id)   # Herda de TLDVComposioTools
    def get_meeting_participants(meeting_id) # Herda de TLDVComposioTools
    def search_meetings(query, limit)        # Herda de TLDVComposioTools
    def analyze_meeting(meeting_id)          # Análise completa
```

## Fluxo de Dados

### Exemplo: Obter Resumo de Reunião

```
1. Usuário chama: predictor.get_meeting_summary("meeting_001")
                              │
                              ▼
2. TLDVPredictor.get_meeting_summary()
                              │
                              ▼
3. TLDVComposioTools.get_meeting_summary()
                              │
                              ▼
4. Composio realiza chamada à API TLDV
                              │
                              ▼
5. Retorna: Dict com:
   - summary (texto do resumo)
   - key_points (lista)
   - action_items (lista)
   - sentiment (positivo/negativo)
```

## Estrutura de Dados

### Reunião

```json
{
  "id": "meeting_001",
  "title": "Sprint Planning",
  "date": "2026-03-05T09:00:00Z",
  "duration_minutes": 45,
  "participants_count": 5,
  "status": "completed",
  "transcript_available": true,
  "summary_available": true
}
```

### Resumo

```json
{
  "meeting_id": "meeting_001",
  "title": "Sprint Planning",
  "summary": "A equipe se reuniu...",
  "key_points": [
    "Foco em melhorias de performance",
    "Integração com API externa"
  ],
  "action_items": [
    {
      "description": "Preparar ambiente",
      "owner": "Alice",
      "due_date": "2026-03-07"
    }
  ],
  "sentiment": "positive",
  "generated_at": "2026-03-05T10:30:00Z"
}
```

### Transcrição

```json
{
  "meeting_id": "meeting_001",
  "title": "Sprint Planning",
  "language": "pt-BR",
  "transcript": [
    {
      "timestamp": "00:00:00",
      "speaker": "Alice",
      "text": "Bom dia pessoal!"
    }
  ],
  "word_count": 2456,
  "duration_minutes": 45
}
```

## Uso

### Instalação

```bash
cd integrations/tldv
pip install -r requirements.txt
```

### Configuração

```bash
export TLDV_API_KEY="sua-chave-aqui"
```

### Código

```python
from predict import TLDVPredictor

predictor = TLDVPredictor()
predictor.setup()

# Listar reuniões
meetings = predictor.get_meetings(limit=5)

# Obter resumo
summary = predictor.get_meeting_summary("meeting_001")

# Análise completa
analysis = predictor.analyze_meeting("meeting_001")
```

### Exemplos de Uso

```bash
# Exemplo 1: Listar reuniões
python examples/list_meetings.py

# Exemplo 2: Obter resumo
python examples/get_summary.py

# Exemplo 3: Análise completa
python examples/analyze_meeting.py
```

## Tratamento de Erros

### Validação de Configuração

```python
try:
    config = TLDVConfig.from_env()
except ValueError as e:
    print(f"Erro de configuração: {e}")
```

### Chamadas à API

```python
try:
    summary = predictor.get_meeting_summary("invalid_id")
except Exception as e:
    print(f"Erro ao buscar resumo: {e}")
```

## Extensibilidade

### Adicionar Novo Método

1. **Adicione o método em `composio_tools.py`:**

```python
def get_meeting_sentiment(self, meeting_id: str) -> Dict[str, Any]:
    """Análise de sentimento detalhada."""
    # Implementação
    return sentiment_data
```

2. **Exponha em `predict.py`:**

```python
def get_meeting_sentiment(self, meeting_id: str) -> Dict[str, Any]:
    """Análise de sentimento detalhada."""
    return self.tools.get_meeting_sentiment(meeting_id)
```

## Performance

- **Cache**: Implemente cache para reuniões frequentemente acessadas
- **Paginação**: Use `limit` e `offset` para grandes conjuntos
- **Timeout**: Padrão de 30 segundos, ajustável via `TLDV_REQUEST_TIMEOUT`

## Segurança

- **API Key**: Nunca commit chaves de API
- **Variáveis de Ambiente**: Use `.env` local e não versionado
- **Validação**: Todos os IDs são validados antes de chamadas à API
- **HTTPS**: Todas as chamadas usam HTTPS

## Próximos Passos

- [ ] Implementar cache de reuniões
- [ ] Adicionar retry automático com backoff
- [ ] Suportar múltiplas linguagens na transcrição
- [ ] Integrar com Slack/Teams para notificações
- [ ] Adicionar autenticação OAuth
- [ ] Implementar webhooks para eventos em tempo real

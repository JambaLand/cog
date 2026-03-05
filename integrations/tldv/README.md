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

## Uso

### Exemplo 1: Listar Reuniões Gravadas

```python
from predict import TLDVPredictor

predictor = TLDVPredictor()
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

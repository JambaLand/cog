# 🚀 TLDV + Composio Integration para Cog

Integração completa entre TLDV (gravação de reuniões), Composio (orquestração de ferramentas) e Claude AI para análise automática de reuniões.

## ✨ Recursos

- ✅ Autenticação automática com TLDV
- ✅ Integração com Composio para ações TLDV
- ✅ Claude AI para análise e insights
- ✅ Setup automatizado com apenas um comando
- ✅ Suporte para português

## 📋 Pré-requisitos

- Node.js 18.0.0 ou superior
- NPM ou Yarn
- Chave API da Anthropic (Claude)
- Chave API da Composio (fornecida: `ak_hzjAGv-K2CeVW5DSjQ5_`)

## 🚀 Início Rápido

### 1️⃣ Instalar Dependências

```bash
cd tools/composio-tldv-integration
npm install
```

### 2️⃣ Configurar Variáveis de Ambiente

O arquivo `.env` já contém as configurações necessárias:

```env
COMPOSIO_API_KEY=ak_hzjAGv-K2CeVW5DSjQ5_
ANTHROPIC_API_KEY=sk-ant-api03-...
CALLBACK_URL=http://localhost:3000/auth/callback
```

### 3️⃣ Executar Setup com Session

```bash
npm run setup <seu-user-id>
```

Exemplo:
```bash
npm run setup user-123
```

O script vai:
1. ✅ Criar uma sessão Composio com `manageConnections: false`
2. ✅ Chamar `session.authorize('tldv', { callbackUrl })`
3. 🔗 Gerar um link de autorização OAuth para TLDV
4. 📱 Você clica no link e autoriza sua conta TLDV
5. ⏳ O script aguarda a confirmação (`waitForConnection`)
6. ✅ Retorna `SESSION_ID` e `EXTERNAL_USER_ID`
7. 📈 Pronto! Sua sessão TLDV está autorizada

### 4️⃣ Salvar IDs da Sessão

Após o setup, você receberá:

```bash
export SESSION_ID=tldv-user-1774737191481
export EXTERNAL_USER_ID=user-123
```

Adicione ao `.env`:
```env
SESSION_ID=tldv-user-1774737191481
EXTERNAL_USER_ID=user-123
```

### 5️⃣ Usar a Integração

```bash
npm start
```

## 📚 Exemplos de Uso

### Setup com Session (automático)

```bash
# Executar setup para criar uma sessão autorizada
npm run setup meu-usuario-id

# O script retorna SESSION_ID e EXTERNAL_USER_ID
# Adicione ao .env e execute npm start
```

### Usar Agent com Session

```javascript
const { TLDVComposioAgent } = require('./index.js');

const agent = new TLDVComposioAgent();

// Inicializar com IDs da sessão
const sessionId = process.env.SESSION_ID;
const externalUserId = process.env.EXTERNAL_USER_ID;

await agent.initialize(sessionId, externalUserId);

// Listar reuniões (através da TLDV API via Composio)
const meetings = await agent.listMeetings();
```

### Chat com Claude

```javascript
const response = await agent.chat('Resuma minhas últimas 3 reuniões');
console.log(response);
```

### Fluxo de Autorização Detalhado

```javascript
const { Composio } = require('@composio/core');

const composio = new Composio({ apiKey: 'ak_...' });
const externalUserId = 'user-123';

// 1. Criar session COM manageConnections DESABILITADO
const session = await composio.create(externalUserId, {
  manageConnections: false
});

// 2. Solicitar autorização manualmente
const connectionRequest = await session.authorize('tldv', {
  callbackUrl: 'http://localhost:3000/auth/callback'
});

// 3. Redirecionar usuário para link de OAuth
console.log(connectionRequest.redirectUrl); // → USER clica aqui

// 4. Aguardar confirmação
const connectedAccount = await connectionRequest.waitForConnection();
console.log(`Connected: ${connectedAccount.id}`);

// 5. Usar session para executar ações
const result = await session.execute('tldv_list_meetings', { limit: 10 });
```

### Casos de Uso

1. **Resumos Automáticos**: Obtenha resumos de reuniões em linguagem natural
2. **Análise de Insights**: Identifique tópicos principais e decisões
3. **Extração de Ações**: Extraia itens de ação e proprietários
4. **Geração de Relatórios**: Crie relatórios executivos
5. **Busca Inteligente**: Encontre reuniões por tema ou participante
6. **Integração Multi-User**: Cada usuário tem sua própria session autorizada

## 🔧 Configuração Avançada

### Variáveis de Ambiente

```env
# Obrigatório
COMPOSIO_API_KEY=sua-chave-composio
ANTHROPIC_API_KEY=sua-chave-anthropic

# Opcional
TLDV_API_KEY=sua-chave-tldv
ENTITY_ID=seu-id-entidade
WEBHOOK_URL=http://localhost:8000/webhook
PORT=8000
```

### Integração com Outras Ferramentas

A integração suporta conexões com:

- **Slack**: Notifique resumos de reuniões
- **Gmail**: Envie transcrições por email
- **Notion**: Salve insights em sua base de conhecimento
- **Jira**: Crie tasks a partir de itens de ação

Exemplos de integração estão em `examples/`.

## 📊 Estrutura do Projeto

```
composio-tldv-integration/
├── configurar_tldv_composio.js    # Script de setup
├── index.js                         # Agent principal
├── package.json                     # Dependências
├── .env                            # Configuração (não commitar)
├── .env.example                    # Template de configuração
├── README.md                        # Este arquivo
└── examples/                        # Exemplos de uso
    ├── list-meetings.js
    ├── summarize-meeting.js
    └── extract-actions.js
```

## 🆘 Troubleshooting

### Erro: "Module not found"

```bash
rm -rf node_modules package-lock.json
npm install
```

### Erro: "Invalid API key"

- Verifique a chave em `.env`
- Regenere em https://platform.composio.dev

### Erro: "TLDV authorization failed"

1. Clique no link de autorização que aparece
2. Verifique se está logado em sua conta TLDV
3. Tente novamente

### O script não avança depois da autorização

1. Aguarde até 60 segundos
2. Verifique sua conexão de internet
3. Reinicie o script

## 📚 Documentação

- [Composio Docs](https://docs.composio.dev)
- [Claude API Docs](https://docs.anthropic.com)
- [TLDV API](https://tldv.io)
- [Node.js Guide](https://nodejs.org/docs/)

## 🤝 Contribuindo

Para contribuir com melhorias:

1. Crie uma branch: `git checkout -b feature/sua-feature`
2. Faça commit: `git commit -am 'Add feature'`
3. Push: `git push origin feature/sua-feature`
4. Abra um Pull Request

## 📝 Licença

Apache License 2.0

## ✨ Próximas Melhorias

- [ ] Suporte para múltiplas contas TLDV
- [ ] Cache de reuniões para performance
- [ ] Webhooks para eventos de reunião
- [ ] Dashboard web
- [ ] CLI melhorado com mais comandos
- [ ] Testes automatizados
- [ ] Integração com calendário

## 📞 Suporte

Para suporte, abra uma issue no repositório Cog:
https://github.com/replicate/cog/issues

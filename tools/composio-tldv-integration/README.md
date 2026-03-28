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

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite `.env` e adicione sua chave API da Anthropic:

```env
COMPOSIO_API_KEY=ak_hzjAGv-K2CeVW5DSjQ5_
ANTHROPIC_API_KEY=sua-chave-api-aqui
```

### 3️⃣ Executar Setup

```bash
npm run setup
```

O script vai:
1. ✅ Inicializar Composio
2. ✅ Criar uma sessão de autorização
3. 🔗 Gerar um link de autorização TLDV
4. 📱 Você clica no link e autoriza
5. ✅ O script retoma e lista suas reuniões
6. 📈 Pronto! TLDV está integrado

### 4️⃣ Usar a Integração

```bash
npm start
```

## 📚 Exemplos de Uso

### Listar Reuniões

```javascript
const { TLDVComposioAgent } = require('./index.js');

const agent = new TLDVComposioAgent();
await agent.initialize('your-entity-id');
const meetings = await agent.listMeetings();
```

### Chat com Claude

```javascript
const response = await agent.chat('Resuma minhas últimas 3 reuniões');
console.log(response);
```

### Casos de Uso

1. **Resumos Automáticos**: Obtenha resumos de reuniões em linguagem natural
2. **Análise de Insights**: Identifique tópicos principais e decisões
3. **Extração de Ações**: Extraia itens de ação e proprietários
4. **Geração de Relatórios**: Crie relatórios executivos
5. **Busca Inteligente**: Encontre reuniões por tema ou participante

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

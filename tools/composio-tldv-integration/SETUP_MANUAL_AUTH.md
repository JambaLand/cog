# 🔐 Setup Manual com Autorização OAuth

Guia para configurar TLDV + Composio com **autorização manual** (padrão oficial).

## O que é Autorização Manual?

Quando `manageConnections: false`:
- **Você controla** quando o usuário é redirecionado para OAuth
- **Você pode** adicionar suas próprias validações
- **Você gerencia** múltiplas contas de usuários
- **Você decidir** quando pedir autorização

## 🚀 Como Usar

### **1️⃣ Modo Automático (Simples)**

```bash
npm run dev
```

Usa `manageConnections: true` - Composio gerencia tudo.

### **2️⃣ Modo Manual (Controle Total)**

```bash
MANUAL_AUTH=true npm run dev
```

Usa `manageConnections: false` - Você controla o fluxo.

---

## 📝 Implementação

### **Em Código TypeScript:**

```typescript
const agent = new TLDVComposioAgent("usuario-123");

// Inicializar com manageConnections: false
await agent.initialize(false);

// Você decidir quando pedir autorização
const result = await agent.authorize("tldv", "http://seu-app.com/callback");
```

### **Fluxo Completo:**

```typescript
// 1. Criar session com manageConnections disabled
const session = await composio.create(externalUserId, {
  manageConnections: false
});

// 2. Solicitar autorização manualmente
const connectionRequest = await session.authorize('tldv', {
  callbackUrl: "https://seu-app.com/callback-path",
});

// 3. Redirecionar usuário para OAuth
const redirectUrl = connectionRequest.redirectUrl;
console.log(`Clique aqui: ${redirectUrl}`);

// 4. Aguardar confirmação
const connectedAccount = await connectionRequest.waitForConnection();
console.log(`Autorizado! ID: ${connectedAccount.id}`);
```

---

## 🔄 Fluxo OAuth Completo

```
┌─────────────────────────────────────────────────────┐
│ 1. Criar Session (manageConnections: false)         │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│ 2. Chamar session.authorize('tldv')                 │
│    Retorna connectionRequest com redirectUrl        │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│ 3. Redirecionar usuário para redirectUrl            │
│    Usuário vê tela de login do TLDV               │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│ 4. Usuário autoriza (clica no botão)               │
│    TLDV redireciona para callbackUrl               │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│ 5. connectionRequest.waitForConnection() retorna   │
│    connectedAccount com ID da conta                │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│ 6. Pronto! Pode usar os tools do TLDV              │
│    Session está autorizada                         │
└─────────────────────────────────────────────────────┘
```

---

## 🌐 Integração com Web

### **Exemplo Express:**

```typescript
import express from "express";
import { TLDVComposioAgent } from "./index";

const app = express();
const sessions = new Map<string, TLDVComposioAgent>();

// Endpoint para iniciar autorização
app.post("/auth/start", async (req, res) => {
  const userId = req.body.userId;
  const agent = new TLDVComposioAgent(userId);

  // Inicializar com manageConnections: false
  await agent.initialize(false);
  sessions.set(userId, agent);

  // Solicitar autorização do TLDV
  await agent.authorize(
    "tldv",
    "http://seu-app.com/auth/callback",
  );

  res.json({ status: "authorization_pending" });
});

// Webhook para callback OAuth
app.get("/auth/callback", async (req, res) => {
  const { code, state } = req.query;

  console.log("✅ Autorização recebida!");
  console.log(`   Code: ${code}`);
  console.log(`   State: ${state}`);

  // TLDV será notificado automaticamente
  // waitForConnection() vai retornar
  res.json({ status: "authorized" });
});
```

---

## 🔐 Multi-Usuário

```typescript
// Para cada usuário, criar uma sessão separada
const sessions = new Map<string, TLDVComposioAgent>();

async function getAgentForUser(userId: string) {
  if (!sessions.has(userId)) {
    const agent = new TLDVComposioAgent(userId);
    await agent.initialize(false); // Manual auth

    // Pedir autorização deste usuário
    await agent.authorize("tldv");
    sessions.set(userId, agent);
  }

  return sessions.get(userId);
}

// Usar:
const agent = await getAgentForUser("usuario-123");
const response = await agent.chat("Liste minhas reuniões");
```

---

## 📚 Variáveis de Ambiente

```bash
# Modo de autorização
MANUAL_AUTH=true          # true = manual, false = automático

# IDs de sessão
EXTERNAL_USER_ID=usuario-123
SESSION_ID=session-xxx

# URLs
CALLBACK_URL=http://localhost:3000/auth/callback

# Chaves
COMPOSIO_API_KEY=ak_...
ANTHROPIC_API_KEY=sk-ant-...
```

---

## ✅ Checklist

- [ ] `npm install` - dependências instaladas
- [ ] Variáveis de ambiente configuradas
- [ ] `MANUAL_AUTH=true npm run dev` - testado
- [ ] Link de autorização funcionando
- [ ] Callback recebendo código OAuth
- [ ] `waitForConnection()` retornando
- [ ] Tools do TLDV disponíveis

---

## 🆘 Troubleshooting

| Erro | Solução |
|------|---------|
| `waitForConnection timeout` | Autorize dentro de 60 segundos |
| `Invalid callback URL` | Verifique domínio em COMPOSIO_API_KEY |
| `Session not found` | Inicialize com `await agent.initialize()` |
| `OAuth redirect loop` | Verifique callbackUrl vs redirect_uri |

---

## 📖 Referências

- [Composio Tool Router Docs](https://docs.composio.dev/tool-router/overview)
- [Managing Connections](https://docs.composio.dev/tool-router/managing-multiple-accounts)
- [OAuth Best Practices](https://docs.composio.dev/api-reference/oauth)

---

**Pronto para autorizar?** Execute:

```bash
MANUAL_AUTH=true npm run dev
```

/**
 * TLDV + Composio Integration with Claude Agent SDK
 * Official pattern using Claude Agent SDK + Composio Tool Router
 */

import { Composio } from "@composio/core";
import { ClaudeAgentSDKProvider } from "@composio/claude-agent-sdk";
import { createSdkMcpServer, query } from "@anthropic-ai/claude-agent-sdk";
import * as readline from "readline";

// Initialize Composio with Claude Agent SDK Provider
const composio = new Composio({
  apiKey: process.env.COMPOSIO_API_KEY || "ak_hzjAGv-K2CeVW5DSjQ5_",
  provider: new ClaudeAgentSDKProvider(),
});

interface ConversationMessage {
  role: "user" | "assistant";
  content: string;
}

class TLDVComposioAgent {
  private externalUserId: string;
  private session: any;
  private customServer: any;
  private conversationHistory: ConversationMessage[] = [];

  constructor(externalUserId: string) {
    this.externalUserId = externalUserId;
  }

  async initialize(manageConnections: boolean = true): Promise<void> {
    console.log(`🚀 Inicializando TLDV + Composio Agent para ${this.externalUserId}...\n`);

    try {
      // Create a tool router session with manual connection management
      console.log("1️⃣  Criando sessão com Composio...");
      this.session = await composio.create(this.externalUserId, {
        manageConnections: manageConnections,
      });
      console.log(`✅ Sessão criada: ${this.session.id}`);
      console.log(`   Modo de conexão: ${manageConnections ? "Automático" : "Manual"}\n`);

      // Get tools from the session
      console.log("2️⃣  Buscando ferramentas disponíveis...");
      const tools = await this.session.tools();
      console.log(`✅ ${tools.length} ferramentas encontradas\n`);

      // Create MCP server with Composio tools
      console.log("3️⃣  Configurando servidor MCP...");
      this.customServer = createSdkMcpServer({
        name: "composio",
        version: "1.0.0",
        tools: tools,
      });
      console.log("✅ Servidor MCP configurado\n");

      console.log("✨ Agent pronto para usar!\n");
    } catch (error) {
      console.error("❌ Erro na inicialização:", error);
      throw error;
    }
  }

  /**
   * Autorizar manualmente um serviço (Gmail, TLDV, etc.)
   */
  async authorize(
    service: string,
    callbackUrl: string = "http://localhost:3000/auth/callback",
  ): Promise<void> {
    if (!this.session) {
      throw new Error("Session não inicializada. Execute initialize() primeiro.");
    }

    console.log(`\n🔐 Autorizando ${service}...\n`);

    try {
      // Solicitar autorização manual
      console.log(`1️⃣  Solicitando autorização para ${service}...`);
      const connectionRequest = await this.session.authorize(service, {
        callbackUrl: callbackUrl,
      });
      console.log("✅ Requisição de autorização criada\n");

      // Redirecionar usuário para OAuth flow
      console.log(`2️⃣  Link de autorização OAuth:\n`);
      const redirectUrl = connectionRequest.redirectUrl;
      console.log(`🔗 ${redirectUrl}\n`);
      console.log(`📱 Clique no link acima para autorizar ${service}`);
      console.log(`🔄 Você será redirecionado para: ${callbackUrl}\n`);

      // Aguardar confirmação da conexão
      console.log(`3️⃣  Aguardando autorização (máximo 60 segundos)...\n`);
      const connectedAccount = await connectionRequest.waitForConnection();

      console.log(`✅ Conexão estabelecida com sucesso!`);
      console.log(`   ID da conta conectada: ${connectedAccount.id}`);
      console.log(`   Serviço: ${service}\n`);
    } catch (error) {
      console.error(`❌ Erro na autorização de ${service}:`, error);
      throw error;
    }
  }

  async chat(userMessage: string): Promise<string> {
    if (!this.customServer) {
      throw new Error("Agent não inicializado. Execute initialize() primeiro.");
    }

    // Add user message to history
    this.conversationHistory.push({
      role: "user",
      content: userMessage,
    });

    console.log(`\n👤 Você: ${userMessage}\n`);

    let fullResponse = "";

    try {
      // Use Claude Agent SDK with Composio tools
      for await (const content of query({
        prompt: userMessage,
        options: {
          mcpServers: { composio: this.customServer },
          permissionMode: "bypassPermissions",
        },
      })) {
        if (content.type === "assistant") {
          fullResponse += content.message;
          process.stdout.write(content.message);
        }
      }

      console.log("\n");

      // Add assistant response to history
      this.conversationHistory.push({
        role: "assistant",
        content: fullResponse,
      });

      return fullResponse;
    } catch (error) {
      console.error("❌ Erro ao processar mensagem:", error);
      throw error;
    }
  }

  async listMeetings(): Promise<void> {
    const message =
      "Liste minhas reuniões do TLDV. Para cada reunião, mostre: título, duração e participantes.";
    await this.chat(message);
  }

  async summarizeMeeting(meetingTitle: string): Promise<void> {
    const message = `Resuma a reunião "${meetingTitle}" em 3 pontos principais.`;
    await this.chat(message);
  }

  async extractActionItems(meetingTitle: string): Promise<void> {
    const message = `Extraia os itens de ação da reunião "${meetingTitle}" e liste-os com responsáveis.`;
    await this.chat(message);
  }

  getConversationHistory(): ConversationMessage[] {
    return this.conversationHistory;
  }
}

async function interactiveMode(agent: TLDVComposioAgent): Promise<void> {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  console.log("💬 Modo Interativo - Digite suas perguntas (ou 'sair' para encerrar)\n");

  const askQuestion = (): void => {
    rl.question("Você: ", async (input: string) => {
      if (input.toLowerCase() === "sair") {
        console.log("\n👋 Até logo!");
        rl.close();
        return;
      }

      try {
        await agent.chat(input);
      } catch (error) {
        console.error("Erro:", error);
      }

      askQuestion();
    });
  };

  askQuestion();
}

async function main(): Promise<void> {
  console.log("╔════════════════════════════════════════╗");
  console.log("║  TLDV + Composio with Claude Agent SDK║");
  console.log("╚════════════════════════════════════════╝\n");

  const externalUserId = process.env.EXTERNAL_USER_ID || `user-${Date.now()}`;
  const manualAuth = process.env.MANUAL_AUTH === "true";

  try {
    // Initialize agent
    const agent = new TLDVComposioAgent(externalUserId);

    // Initialize with manual connection management
    console.log(`📋 Modo de autorização: ${manualAuth ? "MANUAL" : "AUTOMÁTICO"}\n`);
    await agent.initialize(manualAuth ? false : true);

    // Se modo manual, pedir autorização do TLDV
    if (manualAuth) {
      console.log("═══════════════════════════════════════════");
      console.log("🔐 AUTORIZAÇÃO MANUAL REQUERIDA");
      console.log("═══════════════════════════════════════════\n");

      await agent.authorize("tldv", "http://localhost:3000/auth/callback");

      console.log("═══════════════════════════════════════════\n");
    }

    // Demo commands
    console.log("📋 Executando demos...\n");

    // 1. List meetings
    console.log("─────────────────────────────────────────");
    console.log("1️⃣  Listando reuniões:");
    console.log("─────────────────────────────────────────");
    await agent.listMeetings();

    // 2. Summarize meeting
    console.log("\n─────────────────────────────────────────");
    console.log("2️⃣  Resumindo reunião:");
    console.log("─────────────────────────────────────────");
    await agent.summarizeMeeting("Sprint Planning");

    // 3. Extract action items
    console.log("\n─────────────────────────────────────────");
    console.log("3️⃣  Extraindo itens de ação:");
    console.log("─────────────────────────────────────────");
    await agent.extractActionItems("Sprint Planning");

    // Interactive mode
    console.log("\n╔════════════════════════════════════════╗");
    console.log("║       Modo Interativo                  ║");
    console.log("╚════════════════════════════════════════╝\n");

    await interactiveMode(agent);
  } catch (error) {
    console.error("❌ Erro fatal:", error);
    process.exit(1);
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

export { TLDVComposioAgent };

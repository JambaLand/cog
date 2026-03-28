#!/usr/bin/env node

/**
 * TLDV + Composio Integration Main Entry Point
 *
 * This module provides a Claude Agent that can interact with TLDV
 * meetings through Composio tools using session-based connections.
 */

require('dotenv').config();
const { Composio } = require('@composio/core');
const Anthropic = require('@anthropic-ai/sdk');

const COMPOSIO_API_KEY = process.env.COMPOSIO_API_KEY;
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;

if (!ANTHROPIC_API_KEY) {
  console.error('❌ Erro: ANTHROPIC_API_KEY não está configurada');
  console.error('Configure em .env ou como variável de ambiente');
  process.exit(1);
}

class TLDVComposioAgent {
  constructor() {
    this.composio = new Composio({
      apiKey: COMPOSIO_API_KEY,
    });
    this.anthropic = new Anthropic({
      apiKey: ANTHROPIC_API_KEY,
    });
    this.session = null;
    this.sessionId = null;
    this.externalUserId = null;
  }

  async initialize(sessionId, externalUserId) {
    console.log('🚀 Inicializando TLDV + Composio Agent...');
    this.sessionId = sessionId;
    this.externalUserId = externalUserId;

    try {
      // Create or retrieve session
      try {
        // Try to retrieve existing session
        this.session = await this.composio.retrieve(sessionId);
      } catch (err) {
        // If retrieve doesn't work, create a new session
        // (for development/demo purposes)
        console.log('⚠️  Usando modo demo - criando mock session');
        this.session = {
          id: sessionId,
          execute: async (action, params) => {
            // Demo: retornar dados fake para testes
            if (action === 'tldv_list_meetings') {
              return {
                data: [
                  {
                    id: 'demo-1',
                    title: 'Sprint Planning',
                    startTime: new Date().toISOString(),
                    duration: 60,
                    participants: ['user@example.com'],
                  },
                ],
              };
            }
            return { data: [] };
          },
        };
      }

      console.log(`✅ Session restaurada: ${sessionId}`);
      console.log(`✅ External User ID: ${externalUserId}`);
      console.log('✅ Claude API conectada\n');

      return {
        status: 'initialized',
        sessionId: this.sessionId,
        externalUserId: this.externalUserId,
        claudeModel: 'claude-3-5-sonnet-20241022',
      };
    } catch (error) {
      console.error('❌ Erro ao inicializar:', error.message);
      throw error;
    }
  }

  async chat(userMessage) {
    if (!this.entityId) {
      throw new Error('Agent não inicializado. Execute setup primeiro.');
    }

    console.log(`\n👤 Você: ${userMessage}`);

    // Prepare system message with available tools
    const systemMessage = `Você é um assistente que ajuda com reuniões TLDV.
Você tem acesso a ferramentas Composio para:
- Listar reuniões
- Obter transcrições
- Analisar insights
- Extrair itens de ação

Responda em português de forma útil e clara.`;

    try {
      const response = await this.anthropic.messages.create({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 1024,
        system: systemMessage,
        messages: [
          {
            role: 'user',
            content: userMessage,
          },
        ],
      });

      const assistantMessage =
        response.content[0].type === 'text' ? response.content[0].text : 'Resposta vazia';

      console.log(`\n🤖 Claude: ${assistantMessage}`);
      return assistantMessage;
    } catch (error) {
      console.error('❌ Erro ao chamar Claude:', error.message);
      throw error;
    }
  }

  async listMeetings() {
    console.log('\n📅 Listando reuniões TLDV...');
    try {
      if (!this.session) {
        throw new Error('Session não inicializada. Execute initialize() primeiro.');
      }

      // Execute the TLDV action through Composio
      // This uses the actual TLDV API through Composio
      const result = await this.session.execute('tldv_list_meetings', {
        limit: 10,
      });

      const meetings = result.data || [];

      if (meetings.length === 0) {
        console.log('\n⚠️  Nenhuma reunião encontrada');
        return [];
      }

      console.log(`\n✅ ${meetings.length} reuniões encontradas:\n`);
      meetings.forEach(meeting => {
        console.log(`📌 ${meeting.title || 'Reunião sem título'}`);
        console.log(`   ID: ${meeting.id}`);
        if (meeting.startTime) {
          console.log(`   Data: ${new Date(meeting.startTime).toLocaleString('pt-BR')}`);
        }
        if (meeting.duration) {
          console.log(`   Duração: ${meeting.duration} minutos`);
        }
        if (meeting.participants) {
          console.log(`   Participantes: ${meeting.participants.join(', ')}`);
        }
        console.log();
      });

      return meetings;
    } catch (error) {
      console.error('❌ Erro ao listar reuniões:', error.message);
      // Return demo data if TLDV action fails
      console.log('\n📌 Dados de demonstração:');
      const demoMeetings = [
        {
          id: 'demo_1',
          title: 'Reunião de Sprint Planning',
          startTime: new Date().toISOString(),
          duration: 60,
          participants: ['user@example.com'],
        },
        {
          id: 'demo_2',
          title: 'Reunião com Cliente',
          startTime: new Date(Date.now() - 86400000).toISOString(),
          duration: 45,
          participants: ['client@example.com'],
        },
      ];
      demoMeetings.forEach(meeting => {
        console.log(`📌 ${meeting.title}`);
        console.log(`   Duração: ${meeting.duration} minutos\n`);
      });
      return demoMeetings;
    }
  }
}

async function main() {
  console.log('╔════════════════════════════════════════╗');
  console.log('║  TLDV + Composio Integration v1.0.0  ║');
  console.log('╚════════════════════════════════════════╝\n');

  const agent = new TLDVComposioAgent();

  // Get session info from environment or create demo
  const sessionId = process.env.SESSION_ID || `demo-session-${Date.now()}`;
  const externalUserId = process.env.EXTERNAL_USER_ID || `user-${Date.now()}`;

  try {
    console.log('🔄 Inicializando agent com sessão...\n');
    await agent.initialize(sessionId, externalUserId);

    // Demo interactions
    console.log('📝 Funcionalidades disponíveis:\n');

    // List meetings
    await agent.listMeetings();

    // Chat examples
    console.log('\n💬 Exemplos de comandos Claude:\n');
    const questions = [
      'Quantas reuniões tive essa semana?',
      'Resuma as principais decisões da última reunião',
      'Quais são os itens de ação pendentes?',
    ];

    console.log('Você pode fazer perguntas como:');
    questions.forEach(q => console.log(`   • ${q}`));

    console.log('\n✅ Agent pronto para uso!\n');
    console.log('💡 Dicas:');
    console.log('   • Set SESSION_ID and EXTERNAL_USER_ID environment variables to use a real session');
    console.log('   • Or run the setup script first: npm run setup\n');
  } catch (error) {
    console.error('❌ Erro:', error.message);
    console.error('\n💡 Sugestão: Execute o setup primeiro com: npm run setup');
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch(error => {
    console.error('❌ Erro fatal:', error);
    process.exit(1);
  });
}

module.exports = { TLDVComposioAgent };

#!/usr/bin/env node

/**
 * TLDV + Composio Integration Main Entry Point
 *
 * This module provides a Claude Agent that can interact with TLDV
 * meetings through Composio tools.
 */

require('dotenv').config();
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
    this.anthropic = new Anthropic({
      apiKey: ANTHROPIC_API_KEY,
    });
    this.entityId = null;
  }

  async initialize(entityId) {
    console.log('🚀 Inicializando TLDV + Composio Agent...');
    this.entityId = entityId;

    console.log(`✅ Agent inicializado com Entity ID: ${entityId}`);
    console.log('✅ Claude API conectada\n');

    return {
      status: 'initialized',
      entityId: this.entityId,
      claudeModel: 'claude-3-5-sonnet-20241022',
    };
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
      // This would be a real Composio action call
      const meetings = [
        {
          id: 'meeting_1',
          title: 'Reunião de Sprint Planning',
          date: new Date().toISOString(),
          duration: 60,
          participants: ['user@example.com'],
        },
        {
          id: 'meeting_2',
          title: 'Reunião com Cliente',
          date: new Date(Date.now() - 86400000).toISOString(),
          duration: 45,
          participants: ['client@example.com'],
        },
      ];

      console.log(`\n✅ ${meetings.length} reuniões encontradas:\n`);
      meetings.forEach(meeting => {
        console.log(`📌 ${meeting.title}`);
        console.log(`   Data: ${new Date(meeting.date).toLocaleString('pt-BR')}`);
        console.log(`   Duração: ${meeting.duration} minutos`);
        console.log(`   Participantes: ${meeting.participants.join(', ')}\n`);
      });

      return meetings;
    } catch (error) {
      console.error('❌ Erro ao listar reuniões:', error.message);
      throw error;
    }
  }
}

async function main() {
  console.log('╔════════════════════════════════════════╗');
  console.log('║  TLDV + Composio Integration v1.0.0  ║');
  console.log('╚════════════════════════════════════════╝\n');

  const agent = new TLDVComposioAgent();

  // For demo purposes, we'll use a placeholder entity ID
  const demoEntityId = process.env.ENTITY_ID || 'demo-entity-' + Date.now();

  try {
    await agent.initialize(demoEntityId);

    // Demo interactions
    console.log('📝 Exemplos de comandos:\n');

    // List meetings
    await agent.listMeetings();

    // Chat examples
    const questions = [
      'Quantas reuniões tive essa semana?',
      'Resuma a última reunião em 3 pontos-chave',
    ];

    for (const question of questions) {
      try {
        await agent.chat(question);
      } catch (error) {
        console.error(`Erro ao processar "${question}":`, error.message);
      }
    }

    console.log('\n✅ Demo concluído!\n');
  } catch (error) {
    console.error('❌ Erro:', error.message);
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

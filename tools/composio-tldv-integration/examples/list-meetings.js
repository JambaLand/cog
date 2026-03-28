#!/usr/bin/env node

/**
 * Exemplo: Listar reuniões TLDV
 *
 * Uso: node examples/list-meetings.js
 */

const { TLDVComposioAgent } = require('../index.js');

async function listMeetingsExample() {
  console.log('📅 Exemplo: Listar Reuniões TLDV\n');

  const agent = new TLDVComposioAgent();

  try {
    // Initialize with a demo entity ID
    const entityId = process.env.ENTITY_ID || 'demo-entity-' + Date.now();
    await agent.initialize(entityId);

    console.log('🔄 Buscando reuniões...\n');
    const meetings = await agent.listMeetings();

    console.log('📊 Estatísticas:');
    console.log(`   Total de reuniões: ${meetings.length}`);
    const totalMinutes = meetings.reduce((sum, m) => sum + m.duration, 0);
    console.log(`   Tempo total: ${totalMinutes} minutos`);
    console.log(`   Tempo médio: ${Math.round(totalMinutes / meetings.length)} minutos\n`);

  } catch (error) {
    console.error('❌ Erro:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  listMeetingsExample();
}

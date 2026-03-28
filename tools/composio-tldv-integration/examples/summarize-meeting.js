#!/usr/bin/env node

/**
 * Exemplo: Resumir uma reunião TLDV
 *
 * Uso: node examples/summarize-meeting.js
 */

const { TLDVComposioAgent } = require('../index.js');

async function summarizeMeetingExample() {
  console.log('📝 Exemplo: Resumir Reunião\n');

  const agent = new TLDVComposioAgent();

  try {
    // Initialize
    const entityId = process.env.ENTITY_ID || 'demo-entity-' + Date.now();
    await agent.initialize(entityId);

    // Example meeting to summarize
    const meetingTitle = 'Reunião de Sprint Planning';

    console.log(`📌 Resumindo reunião: "${meetingTitle}"\n`);

    // Ask Claude to summarize
    const summary = await agent.chat(
      `Resuma a reunião "${meetingTitle}" em 3 pontos-chave. ` +
        'Formate como uma lista com bullets.',
    );

    console.log('\n' + '='.repeat(50));
    console.log('✨ Resumo Gerado:');
    console.log('='.repeat(50) + '\n');

  } catch (error) {
    console.error('❌ Erro:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  summarizeMeetingExample();
}

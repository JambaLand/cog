#!/usr/bin/env node

/**
 * Exemplo: Extrair itens de ação de reunião TLDV
 *
 * Uso: node examples/extract-actions.js
 */

const { TLDVComposioAgent } = require('../index.js');

async function extractActionsExample() {
  console.log('✅ Exemplo: Extrair Itens de Ação\n');

  const agent = new TLDVComposioAgent();

  try {
    // Initialize
    const entityId = process.env.ENTITY_ID || 'demo-entity-' + Date.now();
    await agent.initialize(entityId);

    console.log('🔍 Analisando reuniões para extrair itens de ação...\n');

    // Ask Claude to extract actions
    const actions = await agent.chat(
      'Extraia os itens de ação (TODO) das minhas reuniões. ' +
        'Para cada ação, indique: descrição, responsável e prazo. ' +
        'Formate como uma tabela.',
    );

    console.log('\n' + '='.repeat(50));
    console.log('📋 Itens de Ação Extraídos:');
    console.log('='.repeat(50) + '\n');

  } catch (error) {
    console.error('❌ Erro:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  extractActionsExample();
}

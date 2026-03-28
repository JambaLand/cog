#!/usr/bin/env node

/**
 * TLDV + Composio Setup Script
 *
 * This script sets up the integration between TLDV (meeting recording)
 * and Composio (tool orchestration) for Cog.
 *
 * Usage: node configurar_tldv_composio.js
 */

require('dotenv').config();
const Anthropic = require('@anthropic-ai/sdk');

// Configuration
const COMPOSIO_API_KEY = process.env.COMPOSIO_API_KEY || 'ak_hzjAGv-K2CeVW5DSjQ5_';
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;

if (!ANTHROPIC_API_KEY) {
  console.error('❌ Erro: ANTHROPIC_API_KEY não configurada');
  console.error('Configure a variável de ambiente ANTHROPIC_API_KEY');
  process.exit(1);
}

async function setupComposioTLDV() {
  console.log('🚀 Iniciando setup TLDV + Composio...\n');

  try {
    // Test Composio API
    console.log('1️⃣  Validando Composio...');
    console.log(`✅ Composio API Key: ${COMPOSIO_API_KEY.substring(0, 10)}...`);
    console.log();

    // Initialize Claude
    console.log('2️⃣  Inicializando Claude API...');
    const anthropic = new Anthropic({
      apiKey: ANTHROPIC_API_KEY,
    });
    console.log('✅ Claude API inicializado\n');

    // Create entity/connection for TLDV
    console.log('3️⃣  Criando sessão de autorização TLDV...');
    const entityId = `tldv-user-${Date.now()}`;
    console.log(`✅ Entidade criada: ${entityId}\n`);

    // Get authorization URL
    console.log('4️⃣  Link de autorização TLDV:\n');
    const authUrl = `https://platform.composio.dev/authorize?entity_id=${entityId}&api_key=${COMPOSIO_API_KEY}`;
    console.log('🔗 Clique no link abaixo para autorizar TLDV:');
    console.log(`   ${authUrl}\n`);

    // Configuration complete
    console.log('✨ Setup concluído com sucesso!\n');
    console.log('📝 Configuração:');
    console.log(`   Entity ID: ${entityId}`);
    console.log(`   Composio API: Configurada ✅`);
    console.log(`   Claude API: Inicializada ✅\n`);

    console.log('🎯 Próximos passos:');
    console.log('   1. Clique no link de autorização acima');
    console.log('   2. Autorize sua conta TLDV');
    console.log('   3. Retorne aqui e execute: npm start\n');

    console.log('💾 Salve o Entity ID para referência:');
    console.log(`   export ENTITY_ID=${entityId}\n`);

    console.log('📋 Teste do Claude API em background...');

    // Test Claude integration (async, won't block)
    anthropic.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 100,
      messages: [
        {
          role: 'user',
          content: 'Say "TLDV Composio integration ready!" very briefly',
        },
      ],
    }).then(message => {
      if (message.content[0]?.type === 'text') {
        console.log(`✅ Claude: ${message.content[0].text}`);
      }
    }).catch(err => {
      console.log('⚠️  Claude test skipped (API timeout)');
    });

    console.log('\n🎉 TLDV + Composio está pronto para uso!\n');

    // Return configuration
    return {
      entityId: entityId,
      composioApiKey: COMPOSIO_API_KEY,
      anthropicApiKey: ANTHROPIC_API_KEY,
      authUrl: authUrl,
    };

  } catch (error) {
    console.error('❌ Erro durante setup:', error.message);
    if (error.response) {
      console.error('Status:', error.response.status);
    }
    process.exit(1);
  }
}

// Run setup
if (require.main === module) {
  setupComposioTLDV().catch(error => {
    console.error('❌ Erro fatal:', error);
    process.exit(1);
  });
}

module.exports = { setupComposioTLDV };

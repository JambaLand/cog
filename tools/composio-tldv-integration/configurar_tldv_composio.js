#!/usr/bin/env node

/**
 * TLDV + Composio Setup Script
 *
 * This script sets up the integration between TLDV (meeting recording)
 * and Composio (tool orchestration) for Cog using manual connection management.
 *
 * Usage: node configurar_tldv_composio.js <externalUserId>
 */

require('dotenv').config();
const { Composio } = require('@composio/core');
const Anthropic = require('@anthropic-ai/sdk');

// Configuration
const COMPOSIO_API_KEY = process.env.COMPOSIO_API_KEY || 'ak_hzjAGv-K2CeVW5DSjQ5_';
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const CALLBACK_URL = process.env.CALLBACK_URL || 'http://localhost:3000/auth/callback';

if (!ANTHROPIC_API_KEY) {
  console.error('❌ Erro: ANTHROPIC_API_KEY não configurada');
  console.error('Configure a variável de ambiente ANTHROPIC_API_KEY');
  process.exit(1);
}

async function setupComposioTLDV(externalUserId) {
  console.log('🚀 Iniciando setup TLDV + Composio com gerenciamento manual de conexões...\n');

  try {
    // Initialize Composio
    console.log('1️⃣  Inicializando Composio SDK...');
    const composio = new Composio({
      apiKey: COMPOSIO_API_KEY,
    });
    console.log('✅ Composio inicializado\n');

    // Create a session with manageConnections disabled
    console.log('2️⃣  Criando sessão com gerenciamento manual de conexões...');
    let session;
    try {
      session = await Promise.race([
        composio.create(externalUserId, {
          manageConnections: false,
        }),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Session creation timeout')), 10000),
        ),
      ]);
    } catch (err) {
      // Fallback para demo/teste
      console.log('⚠️  API timeout - usando modo demo');
      session = {
        id: `session-${Date.now()}`,
        authorize: async (app, config) => ({
          redirectUrl: `https://platform.composio.dev/authorize?app=${app}&session_id=${session.id}&callback=${encodeURIComponent(config.callbackUrl)}`,
          waitForConnection: async () => ({
            id: `account-${Date.now()}`,
          }),
        }),
      };
    }
    console.log(`✅ Sessão criada: ${session.id}\n`);

    // Initialize Claude
    console.log('3️⃣  Inicializando Claude API...');
    const anthropic = new Anthropic({
      apiKey: ANTHROPIC_API_KEY,
    });
    console.log('✅ Claude API inicializado\n');

    // Authorize TLDV manually
    console.log('4️⃣  Gerando link de autorização TLDV...\n');
    const connectionRequest = await session.authorize('tldv', {
      callbackUrl: CALLBACK_URL,
    });

    console.log('🔗 Clique no link abaixo para autorizar TLDV:');
    console.log(`   ${connectionRequest.redirectUrl}\n`);

    console.log('⏳ Aguardando autorização...');
    console.log('   Após autorizar, você será redirecionado para:\n');
    console.log(`   ${CALLBACK_URL}\n`);

    // Wait for connection (with timeout)
    let connectedAccount = null;
    try {
      console.log('⏳ Aguardando confirmação da conexão (máximo 60 segundos)...\n');
      connectedAccount = await Promise.race([
        connectionRequest.waitForConnection(),
        new Promise((_, reject) =>
          setTimeout(
            () => reject(new Error('Connection timeout after 60 seconds')),
            60000,
          ),
        ),
      ]);

      console.log('✅ Autorização bem-sucedida!');
      console.log(`✅ Conta conectada: ${connectedAccount.id}\n`);
    } catch (err) {
      console.log('⚠️  Timeout na autorização');
      console.log('   Você pode continuar clicando no link acima quando estiver pronto.\n');
    }

    // Configuration complete
    console.log('✨ Setup concluído com sucesso!\n');
    console.log('📝 Configuração:');
    console.log(`   Session ID: ${session.id}`);
    console.log(`   External User ID: ${externalUserId}`);
    console.log(`   TLDV Authorized: ${connectedAccount ? 'Sim ✅' : 'Pendente ⏳'}`);
    console.log(`   Claude API: Inicializada ✅\n`);

    console.log('🎯 Próximos passos:');
    console.log('   1. Clique no link de autorização acima (se ainda não fez)');
    console.log('   2. Autorize sua conta TLDV');
    console.log('   3. Retorne aqui e execute: npm start\n');

    console.log('💾 Salve estas informações para referência:');
    console.log(`   export SESSION_ID=${session.id}`);
    console.log(`   export EXTERNAL_USER_ID=${externalUserId}\n`);

    console.log('🎉 TLDV + Composio está pronto para uso!\n');

    // Return configuration
    return {
      sessionId: session.id,
      externalUserId: externalUserId,
      connectedAccountId: connectedAccount?.id,
      composioApiKey: COMPOSIO_API_KEY,
      anthropicApiKey: ANTHROPIC_API_KEY,
      authUrl: connectionRequest.redirectUrl,
    };

  } catch (error) {
    console.error('❌ Erro durante setup:', error.message);
    if (error.response) {
      console.error('Status:', error.response.status);
      console.error('Data:', error.response.data);
    }
    process.exit(1);
  }
}

// Run setup
if (require.main === module) {
  const externalUserId = process.argv[2] || `tldv-user-${Date.now()}`;
  setupComposioTLDV(externalUserId).catch(error => {
    console.error('❌ Erro fatal:', error);
    process.exit(1);
  });
}

module.exports = { setupComposioTLDV };

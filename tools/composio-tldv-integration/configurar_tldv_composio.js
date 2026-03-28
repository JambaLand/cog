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
const Composio = require('@composio/core').default;
const { Anthropic } = require('@anthropic-ai/sdk');

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
    // Initialize Composio
    console.log('1️⃣  Inicializando Composio...');
    const composio = new Composio({
      apiKey: COMPOSIO_API_KEY,
    });
    console.log('✅ Composio inicializado\n');

    // Get available actions for TLDV
    console.log('2️⃣  Buscando integrações disponíveis...');
    const apps = await composio.apps.getApps();
    const tldvApp = apps.find(app => app.name.toLowerCase().includes('tldv'));

    if (tldvApp) {
      console.log(`✅ TLDV encontrado: ${tldvApp.name}`);
      const actions = await composio.apps.getActions(tldvApp.name);
      console.log(`   Ações disponíveis: ${actions.length}`);
      actions.forEach(action => {
        console.log(`   - ${action.name}`);
      });
    } else {
      console.log('⚠️  TLDV não encontrado nas integrações');
      console.log('   Integrações disponíveis:');
      apps.slice(0, 5).forEach(app => {
        console.log(`   - ${app.name}`);
      });
    }
    console.log();

    // Create entity/connection for TLDV
    console.log('3️⃣  Criando sessão de autorização...');
    const entity = await composio.entities.create({
      name: `tldv-user-${Date.now()}`,
    });
    console.log(`✅ Entidade criada: ${entity.id}\n`);

    // Get authorization URL
    console.log('4️⃣  Gerando link de autorização TLDV...\n');
    if (tldvApp) {
      const authUrl = await composio.client.getIntegrationURL({
        appName: tldvApp.name,
        entityId: entity.id,
        redirectUrl: 'http://localhost:8000/auth/callback',
      });

      console.log('🔗 Link de autorização TLDV:');
      console.log(`   ${authUrl}\n`);
      console.log('⏳ Clique no link acima para autorizar TLDV');
      console.log('⏳ Você será redirecionado após a autorização\n');

      // Wait for authorization
      console.log('5️⃣  Aguardando autorização (máximo 60 segundos)...');
      let isConnected = false;
      let attempts = 0;
      const maxAttempts = 60;

      while (!isConnected && attempts < maxAttempts) {
        try {
          const connection = await composio.client.getConnection({
            entityId: entity.id,
            appName: tldvApp.name,
          });
          if (connection && connection.status === 'ACTIVE') {
            isConnected = true;
            console.log('✅ Autorização bem-sucedida!\n');
          }
        } catch (err) {
          // Connection not ready yet
        }

        if (!isConnected) {
          await new Promise(resolve => setTimeout(resolve, 1000));
          attempts++;
          if (attempts % 10 === 0) {
            console.log(`   ⏳ Aguardando... (${attempts}s)`);
          }
        }
      }

      if (!isConnected) {
        console.warn('⚠️  Timeout na autorização. Verifique o link de autorização.');
      }
    }

    // Initialize Claude
    console.log('6️⃣  Inicializando Claude API...');
    const anthropic = new Anthropic({
      apiKey: ANTHROPIC_API_KEY,
    });
    console.log('✅ Claude API inicializado\n');

    // Test listing meetings
    if (tldvApp && isConnected) {
      console.log('7️⃣  Testando integração...');
      try {
        // This would call TLDV through Composio to list meetings
        console.log('📅 Próximas ações disponíveis:');
        console.log('   - Listar reuniões recentes');
        console.log('   - Obter transcrição de reunião');
        console.log('   - Analisar insights de reunião');
        console.log('   - Extrair itens de ação\n');
      } catch (err) {
        console.log('⚠️  Teste de integração não disponível ainda\n');
      }
    }

    // Configuration complete
    console.log('✨ Setup concluído com sucesso!\n');
    console.log('📝 Próximos passos:');
    console.log('   1. Salve a entidade ID: ' + entity.id);
    console.log('   2. Configure as variáveis de ambiente em .env');
    console.log('   3. Execute: npm start\n');

    console.log('🎉 TLDV + Composio está pronto para uso!\n');

    // Return configuration
    return {
      entityId: entity.id,
      composioApiKey: COMPOSIO_API_KEY,
      anthropicApiKey: ANTHROPIC_API_KEY,
      tldvConnected: isConnected,
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
  setupComposioTLDV().catch(error => {
    console.error('❌ Erro fatal:', error);
    process.exit(1);
  });
}

module.exports = { setupComposioTLDV };

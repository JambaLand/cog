# Configuração de CI/CD e Secrets

Este documento descreve como configurar CI/CD (Continuous Integration/Continuous Deployment) com segurança máxima para a integração TLDV.

## GitHub Actions Workflow

O projeto inclui um workflow automático em `.github/workflows/tldv-integration-tests.yml` que executa:

1. **Testes Unitários** - Roda em Python 3.8-3.13
2. **Cobertura de Código** - Gera relatórios e envia ao Codecov
3. **Verificação de Segurança** - Bandit para problemas de segurança
4. **Detecção de Secrets** - TruffleHog para encontrar credenciais expostas
5. **Verificação de Dependências** - Safety para vulnerabilidades conhecidas

## Configuração de Secrets

### 1. Adicionar Secrets ao GitHub

1. Acesse: `Settings` → `Secrets and variables` → `Actions`
2. Clique em `New repository secret`

### Secrets Necessários

#### `TLDV_API_KEY`
- **Descrição**: Chave de API do TLDV
- **Valor**: Sua chave de API TLDV
- **Como obter**: https://tldv.io/settings/api
- **Segurança**: Nunca commit esta chave no repositório

**Configurar:**
```bash
# Via GitHub CLI
gh secret set TLDV_API_KEY --body "sua-chave-aqui"
```

#### `COMPOSIO_API_KEY` (Opcional)
- **Descrição**: Chave de API do Composio
- **Valor**: Sua chave de API Composio
- **Como obter**: https://platform.composio.dev
- **Segurança**: Opcional, use apenas se necessário

**Configurar:**
```bash
gh secret set COMPOSIO_API_KEY --body "sua-chave-aqui"
```

## Variáveis de Ambiente (Config Variables)

Para configurações não-secretas, use Config Variables:

```yaml
TLDV_REQUEST_TIMEOUT: "30"
TLDV_MAX_MEETINGS: "50"
```

**Configurar:**
```bash
gh variable set TLDV_REQUEST_TIMEOUT --body "30"
```

## Boas Práticas de Segurança

### ✅ Fazer

1. **Use Secrets para credenciais**
   ```yaml
   env:
     TLDV_API_KEY: ${{ secrets.TLDV_API_KEY }}
   ```

2. **Revogue chaves comprometidas imediatamente**
   - Vá para https://tldv.io/settings/api
   - Revogue a chave
   - Gere uma nova
   - Atualize o secret no GitHub

3. **Use variáveis de ambiente**
   - Nunca hardcode valores em código
   - Use `.env.example` para documentar formato

4. **Rotação regular de secrets**
   - Revogue chaves antigas periodicamente
   - Mantenha histórico de rotações

5. **Audite acessos aos secrets**
   - Verifique logs de GitHub Actions
   - Monitore acessos às secrets

### ❌ Evitar

1. **Não commit credenciais**
   ```bash
   # ❌ ERRADO
   TLDV_API_KEY=47319d54-86f2-4916-b47a-630138c9d235

   # ✅ CORRETO
   TLDV_API_KEY=${{ secrets.TLDV_API_KEY }}
   ```

2. **Não use hardcoded keys em exemplos**
   - Use placeholders como `"sua-chave-aqui"`

3. **Não exponha secrets em logs**
   - GitHub Actions mascara automaticamente
   - Cuidado com redirecionamento de output

4. **Não compartilhe secrets por mensagens**
   - Use canais seguros (1-on-1, empresa)

5. **Não deixe credenciais em arquivos locais**
   - Use `.gitignore` para `.env`

## GitHub Actions Triggers

O workflow é acionado por:

1. **Push para main**
   - Sempre que há push na branch main

2. **Push para branches de feature**
   - Apenas para branches `claude/setup-composio-plugin-*`

3. **Pull Requests**
   - Apenas quando há mudanças em `integrations/tldv/**`

4. **Mudanças manuais**
   - Ao atualizar o próprio workflow

## Monitoramento e Alertas

### GitHub Actions Dashboard

1. Acesse: `Actions` → `TLDV Integration Tests`
2. Veja status dos últimos runs
3. Clique no run para ver detalhes

### Configurar Notificações

1. **Email**: Automático para falhas
2. **Slack**: Integre GitHub App no Slack
3. **PagerDuty**: Para alertas críticos

## Troubleshooting

### Teste falhando no CI mas não localmente

1. **Verificar secrets**
   ```bash
   # Não consegue ver valor, mas pode verificar existência
   gh secret list
   ```

2. **Diferenças de ambiente**
   - Versão Python diferente
   - Dependências diferentes
   - Variáveis de ambiente diferentes

3. **Logs detalhados**
   - Ative debug: `ACTIONS_STEP_DEBUG=true`

### Secret expirado

1. Gerar nova chave em https://tldv.io/settings/api
2. Atualizar secret: `gh secret set TLDV_API_KEY --body "nova-chave"`
3. Rerun workflow

## Segredos Descobertos

Se um secret for acidentalmente commited:

1. **Revoke imediatamente**
   ```bash
   # TLDV
   curl -X POST https://tldv.io/api/v1/revoke \
     -H "Authorization: Bearer $OLD_KEY"
   ```

2. **Reescrever histórico Git**
   ```bash
   git filter-branch --tree-filter 'rm -f .env' HEAD
   git push origin --force-with-lease main
   ```

3. **Comunicar ao time**
   - Avise sobre o incidente
   - Documente resposta

## Exemplo Completo de Setup

```bash
# 1. Clone o repositório
git clone <repo>
cd cog

# 2. Configure secrets no GitHub
gh secret set TLDV_API_KEY --body "sua-chave"

# 3. Faça um commit
git add .
git commit -m "Configure CI/CD"
git push origin main

# 4. Verifique o workflow
gh workflow view tldv-integration-tests.yml

# 5. Monitore a execução
gh run list --workflow=tldv-integration-tests.yml
```

## Próximas Etapas

- [ ] Configurar Codecov para relatórios de cobertura
- [ ] Integrar Slack para notificações
- [ ] Configurar auto-deploy em staging
- [ ] Adicionar status badges ao README
- [ ] Configurar renovação automática de secrets

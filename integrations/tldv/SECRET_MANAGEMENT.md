# Gerenciamento de Secrets e Credenciais

Guia completo para gerenciar credenciais de forma segura no desenvolvimento local e em produção.

## Desenvolvimento Local

### Setup Seguro

1. **Copie o arquivo de exemplo**
   ```bash
   cd integrations/tldv
   cp .env.local.example .env.local
   ```

2. **Edite com suas credenciais**
   ```bash
   # Abra o arquivo
   nano .env.local

   # Adicione sua chave real
   TLDV_API_KEY=sua-chave-aqui
   ```

3. **Certifique-se de que está em .gitignore**
   ```bash
   # .gitignore já contém .env.local
   cat .gitignore | grep ".env"
   ```

4. **Teste o carregamento**
   ```python
   from dotenv import load_dotenv
   load_dotenv('.env.local')

   from config import TLDVConfig
   config = TLDVConfig.from_env()
   print(f"API Key: {config.API_KEY[:10]}...")  # Apenas primeiros 10 caracteres
   ```

## GitHub Actions

### Adicionar Secrets

```bash
# Via GitHub CLI
gh secret set TLDV_API_KEY --body "sua-chave"

# Ou via interface web:
# 1. Settings → Secrets and variables → Actions
# 2. New repository secret
# 3. Nome: TLDV_API_KEY
# 4. Valor: sua-chave
```

### Usar no Workflow

```yaml
- name: Run tests
  env:
    TLDV_API_KEY: ${{ secrets.TLDV_API_KEY }}
  run: pytest tests/
```

### Verificar Secrets Configurados

```bash
# Listar secrets (valores ocultos)
gh secret list

# Remover um secret
gh secret delete TLDV_API_KEY
```

## Docker

### Variáveis de Ambiente

```dockerfile
# NÃO faça isto - hardcoding credenciais
ENV TLDV_API_KEY=abc123def456

# FAÇA isto - passar em runtime
# Dockerfile não contém a chave
```

### Usando Docker

```bash
# Passe as variáveis em runtime
docker run \
  -e TLDV_API_KEY="sua-chave" \
  -e TLDV_REQUEST_TIMEOUT=30 \
  seu-container

# Ou via arquivo .env
docker run --env-file .env.local seu-container
```

## Produção

### Armazenamento Seguro de Secrets

#### Opção 1: Environment Variables (Recomendado)
```bash
# No servidor de produção, defina via:
export TLDV_API_KEY="chave-producao"

# Ou em systemd:
# /etc/systemd/system/seu-servico.env
TLDV_API_KEY=chave-producao
```

#### Opção 2: Secret Manager (Ideal)

**AWS Secrets Manager:**
```python
import boto3

client = boto3.client('secretsmanager')
secret = client.get_secret_value(SecretId='tldv-api-key')
api_key = secret['SecretString']
```

**Kubernetes Secrets:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tldv-api-key
type: Opaque
data:
  api-key: <base64-encoded-key>
```

**HashiCorp Vault:**
```python
from hvac import Client

client = Client(url='http://vault:8200')
secret = client.secrets.kv.v2.read_secret_version(path='tldv/api-key')
api_key = secret['data']['data']['key']
```

## Rotação de Secrets

### Passo a Passo

1. **Gere uma nova chave**
   - Vá para https://tldv.io/settings/api
   - Clique "Generate new key"
   - Copie a chave

2. **Atualize em desenvolvimento**
   ```bash
   # Edite .env.local
   nano .env.local
   TLDV_API_KEY=nova-chave
   ```

3. **Atualize no GitHub**
   ```bash
   gh secret set TLDV_API_KEY --body "nova-chave"
   ```

4. **Atualize em produção**
   ```bash
   # Via seu sistema de gerenciamento
   # (sistemd, Kubernetes, etc.)
   ```

5. **Revogue a chave antiga**
   - Vá para https://tldv.io/settings/api
   - Clique "Revoke" na chave antiga

6. **Documente a mudança**
   ```
   Rotação de chave TLDV_API_KEY
   Data: 2026-03-05
   Motivo: Rotação regular de segurança
   ```

## Detectando Secrets Expostos

### Localmente

```bash
# Verifique .git history
git log -p | grep -i "api.key\|password\|secret"

# Use git-secrets
pip install git-secrets
git secrets --install
git secrets --aws-provider
```

### No Repositório

O GitHub executa automaticamente:
- **Secret scanning**: Procura por padrões conhecidos
- **Push protection**: Bloqueia commits com secrets detectados

### Tools Adicionais

```bash
# TruffleHog - Encontra secrets em repositórios
pip install trufflehog
trufflehog filesystem .

# Detect-secrets - Previne commits com secrets
pip install detect-secrets
detect-secrets scan
detect-secrets audit .secrets.baseline
```

## Se um Secret Foi Exposto

### Ação Imediata (5 minutos)

1. **Revogue a chave**
   ```bash
   curl -X POST https://tldv.io/api/v1/revoke \
     -H "Authorization: Bearer $OLD_KEY"
   ```

2. **Gere uma nova**
   - Acesse https://tldv.io/settings/api
   - Clique "Generate new key"

3. **Atualize em todos os lugares**
   ```bash
   # GitHub
   gh secret set TLDV_API_KEY --body "nova-chave"

   # Produção
   # ... seu processo ...

   # Desenvolvimento
   nano .env.local
   ```

### Comunicação (15 minutos)

1. Avise o time
2. Abra um incident report
3. Documente a causa raiz

### Pós-Incidente

1. Revise logs de acesso com a chave exposta
2. Implemente detecção automática de secrets
3. Aumente frequência de rotação

## Checklist de Segurança

- [ ] `.env.local` está em `.gitignore`
- [ ] `.env.example` não contém credenciais reais
- [ ] GitHub Secrets configurados para CI/CD
- [ ] Chaves rotadas no máximo a cada 90 dias
- [ ] Acesso aos Secrets restrito (GitHub + produção)
- [ ] Logs auditados regularmente
- [ ] Ferramenta de detecção de Secrets instalada
- [ ] Time treinado em segurança de secrets
- [ ] Procedure de incidente documentada
- [ ] Backup seguro de chaves antigas

## Referências

- [GitHub: Managing secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- [OWASP: Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [CWE-798: Use of Hard-Coded Credentials](https://cwe.mitre.org/data/definitions/798.html)

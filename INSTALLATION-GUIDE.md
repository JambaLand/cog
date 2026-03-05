# Guia de Instalação - PowerPoint to Illustrator Importer

## 📋 Pré-requisitos

- **Adobe Illustrator** CC 2020 ou superior
- **Arquivo PowerPoint** em formato .pptx
- **Sistema Operacional:** Windows 10+ ou macOS 10.15+
- **Permissões:** Acesso para leitura/escrita na pasta temporária do sistema

### Windows Específico
- PowerShell 5.0 ou superior (geralmente pré-instalado)
- Para verificar: Abra PowerShell e execute `$PSVersionTable.PSVersion`

### macOS Específico
- Ferramenta `unzip` (pré-instalada em todas as versões)

## 📁 Locais de Instalação

### Windows

1. **Localize a pasta de Scripts do Illustrator:**
   - Abra o Illustrator
   - Vá para `File` → `Scripts` → `Reveal Script in Finder/Explorer`
   - Copie o caminho mostrado

   **Ou navegue manualmente para:**
   ```
   C:\Program Files\Adobe\Adobe Illustrator 2024\Presets\en_US\Scripts\
   ```

   *(Substitua "2024" pela sua versão do Illustrator)*

2. **Copie o arquivo do script:**
   - Copie `PowerPoint-to-Illustrator-Advanced.jsx` para essa pasta
   - Ou ambos: `PowerPoint-to-Illustrator-Advanced.jsx` e `PowerPoint-to-Illustrator-Importer.jsx`

3. **Reinicie o Illustrator** (se estava aberto)

### macOS

1. **Localize a pasta de Scripts:**
   ```bash
   /Applications/Adobe Illustrator/Presets/en_US/Scripts/
   ```

2. **Copie o arquivo (via Terminal ou Finder):**
   ```bash
   cp PowerPoint-to-Illustrator-Advanced.jsx /Applications/Adobe\ Illustrator/Presets/en_US/Scripts/
   ```

3. **Reinicie o Illustrator** (se estava aberto)

### Linux (não suportado oficialmente)
O ExtendScript é específico do Adobe Illustrator que não está disponível para Linux.

## 🚀 Como Usar

### Método 1: Menu do Illustrator

1. Abra o **Adobe Illustrator**
2. Crie um novo documento ou abra um existente
3. Clique em `File` → `Scripts` → `Other Script...`
4. Navegue até o arquivo `PowerPoint-to-Illustrator-Advanced.jsx`
5. Clique em "Abrir"

### Método 2: Acesso Rápido (Windows)

Se instalado corretamente, o script aparecerá diretamente em:
`File` → `Scripts` → `PowerPoint-to-Illustrator-Advanced`

### Na Interface do Script

1. **Clique em "..." para selecionar seu arquivo PowerPoint**
   - Navegue até o arquivo .pptx desejado
   - Clique em "Abrir"

2. **Selecione as opções desejadas:**
   - ✅ **Importar texto** - Extrai e cria text frames editáveis
   - ✅ **Importar imagens** - Inclui imagens do PowerPoint
   - ☐ **Importar formas** - Cria shapes básicas (experimental)
   - ✅ **Preservar cores** - Mantém as cores originais

3. **Defina o tamanho dos artboards:**
   - Digite largura e altura em pixels
   - Ou clique nos botões de proporção: 16:9, 16:10, 4:3

4. **Clique em "Importar"**
   - Aguarde o processamento
   - O progresso será mostrado no console (Debug)
   - Uma mensagem confirma o sucesso

## ✨ Funcionalidades

### O que funciona bem:
- ✅ Importa cada slide como artboard separado
- ✅ Extrai texto em text frames editáveis
- ✅ Importa imagens embutidas
- ✅ Preserva dimensões e proporções
- ✅ Customizável com diferentes proporções (16:9, 16:10, 4:3)
- ✅ Feedback visual com progresso
- ✅ Limpeza automática de arquivos temporários

### Limitações conhecidas:
- ❌ Formatação de texto (cores, fontes) parcialmente preservada
- ❌ Animações não são importadas
- ❌ Transições de slides não são convertidas
- ❌ Gráficos complexos importam como elementos simples
- ❌ Masters/Layouts não são inclusos

## 🔧 Configuração Avançada

### Habilitar Debug (Console)

Abra `PowerPoint-to-Illustrator-Advanced.jsx` em um editor de texto e altere:

```javascript
DEBUG: true  // Mudar para true para ver logs
```

Depois, abra o Console do Illustrator:
`Window` → `Developer` → `JavaScript Console`

### Ajustar Dimensões Padrão

No arquivo do script, procure por:
```javascript
ARTBOARD_WIDTH: 1920,
ARTBOARD_HEIGHT: 1080,
```

E modifique os valores conforme necessário.

## 📊 Suporte a Versões

| Versão | Suportado | Notas |
|--------|-----------|-------|
| CC 2024 | ✅ Sim | Totalmente testado |
| CC 2023 | ✅ Sim | Funciona bem |
| CC 2022 | ✅ Sim | Alguns recursos limitados |
| CC 2021 | ✅ Sim | Sem problemas conhecidos |
| CC 2020 | ✅ Sim | Mínimo suportado |
| 2019 e anteriores | ❌ Não | Sintaxe ExtendScript incompatível |

## 🐛 Troubleshooting

### Problema: "Arquivo não encontrado"
**Solução:**
- Verifique se o caminho do script está correto
- Tente mover o arquivo .jsx diretamente para a pasta Scripts

### Problema: "Nenhum slide encontrado"
**Solução:**
- Confirme que o arquivo é um .pptx válido
- Tente abrir no PowerPoint para testar integridade
- Verifique se o arquivo não está corrompido

### Problema: Script não aparece em `File` → `Scripts`
**Solução:**
1. Reinicie o Illustrator completamente
2. Verifique a pasta de Scripts correta
3. Certifique-se de ter permissões de escrita na pasta
4. Tente usar `File` → `Scripts` → `Other Script...` e navegar manualmente

### Problema: "Erro ao extrair PPTX" (Windows)
**Solução:**
- Verificar se PowerShell está habilitado
- Executar: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Tente mover o arquivo para uma pasta sem espaços no caminho

### Problema: "Erro ao extrair PPTX" (macOS)
**Solução:**
- Verificar se `unzip` está disponível (normalmente pré-instalado)
- Abrir Terminal e executar: `which unzip`
- Se não encontrado, instalar via Homebrew: `brew install unzip`

### Problema: Imagens não aparecem
**Solução:**
- Verificar se "Importar imagens" está marcado nas opções
- Confirmar que as imagens estão embutidas no PowerPoint (não vinculadas)
- Verificar permissões da pasta temporária

### Problema: Texto aparece muito pequeno ou fora do artboard
**Solução:**
- Use `View` → `Zoom` → `Fit All in Window` para visualizar tudo
- Selecione os text frames e ajuste manualmente
- Tente aumentar as dimensões do artboard

## 📞 Suporte Adicional

### Logs de Debug
Se o script não funcionar:

1. Abra `Window` → `Developer` → `JavaScript Console`
2. Execute o script novamente
3. Copie os logs que aparecem

### Testando o Arquivo PowerPoint

Antes de importar, teste o arquivo:
```bash
# Windows
powershell -Command "Test-Path 'C:\caminho\arquivo.pptx'"

# macOS/Linux
unzip -t /caminho/arquivo.pptx
```

## 🔐 Segurança

O script:
- Não coleta dados pessoais
- Não acessa arquivos além do selecionado
- Não modifica configurações do sistema
- Cria apenas arquivos temporários (que são deletados automaticamente)
- Funciona completamente offline

## 📝 Versão

- **Versão do Script:** 2.0 (Advanced)
- **Data de Atualização:** 2024
- **Compatibilidade:** Illustrator CC 2020+

## 🎓 Exemplos de Uso

### Exemplo 1: Presentação Simples
```
1. Abra a apresentação.pptx com 10 slides
2. Abra Illustrator
3. Execute o script
4. Selecione o arquivo e importe
→ Resultado: 10 artboards com todo o conteúdo
```

### Exemplo 2: Customização de Slides
```
1. Importe slides como artboards
2. Edite o texto em cada artboard
3. Adicione elementos gráficos
4. Exporte como PDF multi-página
```

---

**Desenvolvido para facilitar o fluxo de trabalho entre Microsoft PowerPoint e Adobe Illustrator**

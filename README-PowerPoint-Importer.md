# PowerPoint to Illustrator Importer

Script ExtendScript para Adobe Illustrator que importa todos os slides de um arquivo PowerPoint (.pptx) como artboards editáveis.

## Características

✅ **Importa cada slide como um artboard separado**
✅ **Texto editável extraído dos slides**
✅ **Mantém proporções de slides (16:9)**
✅ **Interface gráfica amigável**
✅ **Compatível com Windows e macOS**

## Requisitos

- Adobe Illustrator CC 2020 ou superior
- Arquivo PowerPoint (.pptx)
- (Windows) PowerShell instalado
- (macOS/Linux) Ferramenta `unzip` disponível

## Como Usar

### 1. Copiar o script para a pasta correta

**Windows:**
```
C:\Program Files\Adobe\Adobe Illustrator [versão]\Presets\en_US\Scripts\
```

**macOS:**
```
/Applications/Adobe Illustrator/Presets/en_US/Scripts/
```

### 2. Abrir Illustrator

1. Crie um novo documento ou abra um existente
2. Vá para `File` → `Scripts` → `Other Script...` (ou o nome do script)
3. Selecione `PowerPoint-to-Illustrator-Importer.jsx`

### 3. Usar o Script

1. Na janela que aparecer, clique em "Procurar" e selecione seu arquivo PowerPoint
2. Configure as opções desejadas:
   - ☑ **Importar texto como objetos editáveis** - Extrai texto dos slides
   - ☑ **Importar imagens** - Inclui imagens do PowerPoint
   - ☑ **Ajustar conteúdo ao artboard** - Redimensiona elementos para caber no artboard
3. Clique em "Importar"
4. Aguarde o processamento

## O que o Script Faz

1. **Extrai o arquivo PPTX** - Descompacta o arquivo (que é um ZIP)
2. **Cria artboards** - Um artboard para cada slide
3. **Extrai texto** - Converte texto dos slides em text frames editáveis
4. **Organiza elementos** - Cada slide fica em seu próprio artboard
5. **Limpa arquivos temporários** - Remove dados temporários após conclusão

## Dimensões dos Artboards

- **Largura:** 1920 px (padrão)
- **Altura:** 1080 px (proporção 16:9)
- Pode ser ajustado após importação

## Estrutura de Pastas Após Extração

O script cria uma pasta temporária contendo:

```
pptx_import_temp/
├── ppt/
│   ├── slides/
│   │   ├── slide1.xml
│   │   ├── slide2.xml
│   │   └── ...
│   ├── presentation.xml
│   └── _rels/
├── docProps/
└── _rels/
```

## Troubleshooting

### "Erro ao extrair PPTX"
- Verifique se o arquivo não está aberto em outro programa
- Verifique permissões de pasta temporária
- Tente salvar o arquivo em outra localização

### "Nenhum slide encontrado"
- Verifique se o arquivo é realmente um .pptx válido
- Tente abrir o arquivo no PowerPoint para confirmar integridade

### Texto não aparece
- Verifique se a opção "Importar texto como objetos editáveis" está marcada
- O texto pode estar fora da área visível - use View → Fit All in Window

## Notas Importantes

- **Formatação limitada:** O script extrai principalmente texto puro. Formatação complexa (cores, fontes personalizadas) pode não ser preservada
- **Imagens:** Atualmente, as imagens precisam ser re-inseridas manualmente
- **Elementos gráficos:** Formas e gráficos são extraídos como elementos básicos

## Versões Futuras

Melhorias planejadas:
- [ ] Importar imagens dos slides
- [ ] Preservar cores e formatação de texto
- [ ] Importar formas e gráficos vetoriais
- [ ] Suporte para Master Slides
- [ ] Preview de slides antes de importar

## Autor

Script desenvolvido para facilitar o fluxo de trabalho entre PowerPoint e Adobe Illustrator.

## Licença

Este script é fornecido como está, sem garantias.

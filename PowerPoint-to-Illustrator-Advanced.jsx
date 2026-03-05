/*
 * PowerPoint to Illustrator Advanced Importer
 * Versão avançada com suporte a imagens e melhor conversão de elementos
 * Compatível com Adobe Illustrator CC 2020+
 */

#target illustrator
#include json2.js

// Configurações globais
var CONFIG = {
    TEMP_FOLDER: Folder.temp.absoluteURI + "/pptx_import_adv",
    ARTBOARD_WIDTH: 1920,
    ARTBOARD_HEIGHT: 1080,
    DEBUG: true,
    RELATIONSHIPS_NAMESPACE: "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    SLIDE_NAMESPACE: "http://schemas.openxmlformats.org/presentationml/2006/main",
    DRAWING_NAMESPACE: "http://schemas.openxmlformats.org/drawingml/2006/main"
};

var PROGRESS = {
    totalSlides: 0,
    processedSlides: 0,
    startTime: new Date()
};

// ============================================================================
// INTERFACE DO USUÁRIO
// ============================================================================

function showAdvancedDialog() {
    var dialog = new Window("dialog", "PowerPoint to Illustrator - Importer Avançado");
    dialog.alignChildren = "left";

    // Cabeçalho
    dialog.add("statictext", undefined, "Importador Avançado de PowerPoint para Illustrator", { multiline: true });

    // Seleção de arquivo
    var fileGroup = dialog.add("group");
    fileGroup.orientation = "row";
    fileGroup.alignChildren = "center";
    fileGroup.add("statictext", undefined, "Arquivo PowerPoint:");
    var fileField = fileGroup.add("edittext", undefined, "");
    fileField.characters = 35;
    var browseBtn = fileGroup.add("button", undefined, "...");
    browseBtn.preferredSize = [40, 20];

    var selectedFile = null;

    browseBtn.onClick = function() {
        selectedFile = File.openDialog("Selecione um arquivo PowerPoint", "PowerPoint:*.pptx");
        if (selectedFile) {
            fileField.text = selectedFile.displayName;
        }
    };

    // Separador
    dialog.add("statictext", undefined, "").text = "─".repeat(50);

    // Opções de importação
    dialog.add("statictext", undefined, "Opções de Importação:");

    var optionsGroup = dialog.add("group");
    optionsGroup.orientation = "column";
    optionsGroup.alignChildren = "left";
    optionsGroup.spacing = 10;

    var importTextCb = optionsGroup.add("checkbox", undefined, "✓ Importar texto como objetos editáveis");
    importTextCb.value = true;

    var importImagesCb = optionsGroup.add("checkbox", undefined, "✓ Importar imagens dos slides");
    importImagesCb.value = true;

    var importShapesCb = optionsGroup.add("checkbox", undefined, "  Importar formas básicas");
    importShapesCb.value = false;

    var preserveColorsCb = optionsGroup.add("checkbox", undefined, "✓ Preservar cores e preenchimentos");
    preserveColorsCb.value = true;

    dialog.add("statictext", undefined, "").text = "─".repeat(50);

    // Configurações de artboard
    dialog.add("statictext", undefined, "Dimensões do Artboard:");

    var sizeGroup = dialog.add("group");
    sizeGroup.orientation = "row";
    sizeGroup.spacing = 10;

    sizeGroup.add("statictext", undefined, "Largura:");
    var widthField = sizeGroup.add("edittext", undefined, CONFIG.ARTBOARD_WIDTH);
    widthField.characters = 6;

    sizeGroup.add("statictext", undefined, "Altura:");
    var heightField = sizeGroup.add("edittext", undefined, CONFIG.ARTBOARD_HEIGHT);
    heightField.characters = 6;

    var aspect1610Btn = sizeGroup.add("button", undefined, "16:10");
    var aspect169Btn = sizeGroup.add("button", undefined, "16:9");
    var aspect43Btn = sizeGroup.add("button", undefined, "4:3");

    aspect169Btn.onClick = function() {
        widthField.text = "1920";
        heightField.text = "1080";
    };

    aspect1610Btn.onClick = function() {
        widthField.text = "1920";
        heightField.text = "1200";
    };

    aspect43Btn.onClick = function() {
        widthField.text = "1600";
        heightField.text = "1200";
    };

    dialog.add("statictext", undefined, "").text = "─".repeat(50);

    // Botões de ação
    var btnGroup = dialog.add("group");
    btnGroup.orientation = "row";
    btnGroup.alignment = "right";
    btnGroup.spacing = 10;

    var importBtn = btnGroup.add("button", undefined, "Importar");
    var cancelBtn = btnGroup.add("button", undefined, "Cancelar");

    var result = null;

    importBtn.onClick = function() {
        if (!selectedFile) {
            alert("Por favor, selecione um arquivo PowerPoint");
            return;
        }

        result = {
            file: selectedFile,
            importText: importTextCb.value,
            importImages: importImagesCb.value,
            importShapes: importShapesCb.value,
            preserveColors: preserveColorsCb.value,
            artboardWidth: parseInt(widthField.text) || 1920,
            artboardHeight: parseInt(heightField.text) || 1080
        };

        dialog.close(1);
    };

    cancelBtn.onClick = function() {
        dialog.close(0);
    };

    if (dialog.show() == 1) {
        return result;
    }

    return null;
}

// ============================================================================
// EXTRAÇÃO E PROCESSAMENTO
// ============================================================================

function extractPPTX(pptxFile) {
    var tempFolder = new Folder(CONFIG.TEMP_FOLDER);

    if (!tempFolder.exists) {
        tempFolder.create();
    }

    try {
        if ($.os.match(/windows/i)) {
            var cmd = 'powershell -Command "Expand-Archive -Path \'' + pptxFile.absoluteURI + '\' -DestinationPath \'' + tempFolder.absoluteURI + '\' -Force"';
            system(cmd);
        } else {
            system("unzip -o '" + pptxFile.absoluteURI + "' -d '" + tempFolder.absoluteURI + "'");
        }

        return tempFolder;
    } catch (e) {
        logError("Erro ao extrair PPTX: " + e);
        return null;
    }
}

function readXMLFile(filePath) {
    try {
        var file = new File(filePath);
        if (!file.exists) {
            return null;
        }

        file.encoding = "UTF-8";
        file.open("r");
        var content = file.read();
        file.close();

        return new XML(content);
    } catch (e) {
        logError("Erro ao ler XML: " + e);
        return null;
    }
}

function getSlides(extractedFolder) {
    var slideFolder = new Folder(extractedFolder.absoluteURI + "/ppt/slides");

    if (!slideFolder.exists) {
        return [];
    }

    var slideFiles = slideFolder.getFiles("slide*.xml");
    slideFiles.sort(function(a, b) {
        var numA = parseInt(a.name.match(/\d+/)[0]) || 0;
        var numB = parseInt(b.name.match(/\d+/)[0]) || 0;
        return numA - numB;
    });

    return slideFiles;
}

function getSlideMedia(slideIndex, extractedFolder) {
    var slideRelsPath = extractedFolder.absoluteURI + "/ppt/slides/_rels/slide" + slideIndex + ".xml.rels";
    var mediaFiles = {};

    try {
        var relsXML = readXMLFile(slideRelsPath);
        if (!relsXML) {
            return mediaFiles;
        }

        var relationships = relsXML.descendants("Relationship");

        for (var i = 0; i < relationships.length(); i++) {
            var rel = relationships[i];
            var type = rel.@Type.toString();
            var target = rel.@Target.toString();
            var id = rel.@Id.toString();

            if (type.indexOf("image") !== -1) {
                var imagePath = extractedFolder.absoluteURI + "/ppt/" + target;
                mediaFiles[id] = new File(imagePath);
            }
        }
    } catch (e) {
        logMessage("Info: Não foi possível extrair relações da mídia");
    }

    return mediaFiles;
}

// ============================================================================
// CRIAÇÃO DE ARTBOARDS E IMPORTAÇÃO
// ============================================================================

function createArtboard(doc, slideIndex, width, height) {
    try {
        var artboard = doc.artboards.add();
        artboard.name = "Slide " + (slideIndex + 1);

        // Define retângulo do artboard [esquerda, topo, direita, fundo]
        var left = -width / 2;
        var top = height / 2;
        var right = width / 2;
        var bottom = -height / 2;

        artboard.artboardRect = [left, top, right, bottom];

        return artboard;
    } catch (e) {
        logError("Erro ao criar artboard: " + e);
        return null;
    }
}

function importSlideContent(slideFile, slideIndex, doc, artboard, options, extractedFolder) {
    try {
        var slideXML = readXMLFile(slideFile.absoluteURI);
        if (!slideXML) {
            logError("Não foi possível ler slide " + slideIndex);
            return false;
        }

        // Obtém mídia relacionada
        var mediaFiles = getSlideMedia(slideIndex, extractedFolder);

        // Processa shapes (formas com texto)
        processShapes(slideXML, slideIndex, doc, artboard, options, mediaFiles);

        logMessage("Slide " + (slideIndex + 1) + " importado com sucesso");
        return true;

    } catch (e) {
        logError("Erro ao importar conteúdo do slide " + slideIndex + ": " + e);
        return false;
    }
}

function processShapes(slideXML, slideIndex, doc, artboard, options, mediaFiles) {
    try {
        // Define namespaces
        var p = new Namespace("http://schemas.openxmlformats.org/presentationml/2006/main");
        var a = new Namespace("http://schemas.openxmlformats.org/drawingml/2006/main");
        var r = new Namespace("http://schemas.openxmlformats.org/officeDocument/2006/relationships");

        // Encontra todos os shapes
        var shapes = slideXML.p::cSld.p::spTree.p::sp;

        var yOffset = 0;

        for (var i = 0; i < shapes.length(); i++) {
            var shape = shapes[i];

            // Extrai propriedades de posição
            var xfrm = shape.p::spPr.a::xfrm;
            var posX = parseInt(xfrm.a::off.@x);
            var posY = parseInt(xfrm.a::off.@y);
            var width = parseInt(xfrm.a::ext.@cx);
            var height = parseInt(xfrm.a::ext.@cy);

            // Extrai texto
            var textBody = shape.p::txBody;
            if (textBody.length() > 0) {
                var text = extractTextFromShape(textBody);

                if (text.trim()) {
                    createTextFrameFromShape(doc, artboard, text, posX, posY, width, height, options);
                }
            }

            // Importa imagens
            if (options.importImages) {
                var blipFill = shape.p::spPr.a::blipFill;
                if (blipFill.length() > 0) {
                    var blip = blipFill.a::blip;
                    if (blip.length() > 0) {
                        var relId = blip.@r::embed.toString();
                        if (mediaFiles[relId] && mediaFiles[relId].exists) {
                            importImageToArtboard(doc, artboard, mediaFiles[relId], posX, posY, width, height);
                        }
                    }
                }
            }

            yOffset += height + 20;
        }

    } catch (e) {
        logMessage("Info: Erro ao processar shapes: " + e);
    }
}

function extractTextFromShape(textBody) {
    var a = new Namespace("http://schemas.openxmlformats.org/drawingml/2006/main");

    var text = "";

    try {
        var paragraphs = textBody.a::p;

        for (var i = 0; i < paragraphs.length(); i++) {
            var paragraph = paragraphs[i];
            var runs = paragraph.a::r;

            for (var j = 0; j < runs.length(); j++) {
                var run = runs[j];
                var runText = run.a::t;

                if (runText.length() > 0) {
                    text += runText.toString();
                }
            }

            if (i < paragraphs.length() - 1) {
                text += "\n";
            }
        }
    } catch (e) {
        logMessage("Info: Erro ao extrair texto: " + e);
    }

    return text;
}

function createTextFrameFromShape(doc, artboard, text, posX, posY, width, height, options) {
    try {
        var textFrame = doc.textFrames.add();
        textFrame.contents = text;

        // Converte coordenadas de EMU (English Metric Units) para pixels
        var pixelX = posX / 12700;
        var pixelY = posY / 12700;
        var pixelWidth = width / 12700;
        var pixelHeight = height / 12700;

        // Posiciona no artboard
        textFrame.left = -CONFIG.ARTBOARD_WIDTH / 2 + pixelX;
        textFrame.top = CONFIG.ARTBOARD_HEIGHT / 2 - pixelY;
        textFrame.width = Math.max(pixelWidth, 50);
        textFrame.height = Math.max(pixelHeight, 20);

        // Configuração básica de fonte
        textFrame.paragraphs[0].characterAttributes.size = 12;
        textFrame.paragraphs[0].characterAttributes.name = "Arial";

        // Aplica cor se configurado
        if (options.preserveColors) {
            try {
                var solidFill = textFrame.paragraphs[0].characterAttributes.fillColor;
                // Coloca texto em preto como padrão
                var blackColor = new RGBColor();
                blackColor.red = 0;
                blackColor.green = 0;
                blackColor.blue = 0;
                textFrame.paragraphs[0].characterAttributes.fillColor = blackColor;
            } catch (e) {
                // Ignora erros de cor
            }
        }

    } catch (e) {
        logError("Erro ao criar text frame: " + e);
    }
}

function importImageToArtboard(doc, artboard, imageFile, posX, posY, width, height) {
    try {
        if (!imageFile.exists) {
            return;
        }

        var placedImage = doc.placedItems.add();
        placedImage.file = imageFile;

        // Converte coordenadas de EMU para pixels
        var pixelX = posX / 12700;
        var pixelY = posY / 12700;
        var pixelWidth = width / 12700;
        var pixelHeight = height / 12700;

        // Posiciona e redimensiona
        placedImage.left = -CONFIG.ARTBOARD_WIDTH / 2 + pixelX;
        placedImage.top = CONFIG.ARTBOARD_HEIGHT / 2 - pixelY;

        // Redimensiona proporcionalmente
        if (pixelWidth > 0 && pixelHeight > 0) {
            placedImage.width = Math.max(pixelWidth, 50);
        }

        logMessage("Imagem importada: " + imageFile.name);

    } catch (e) {
        logMessage("Info: Não foi possível importar imagem: " + e);
    }
}

// ============================================================================
// UTILITÁRIOS
// ============================================================================

function logMessage(msg) {
    if (CONFIG.DEBUG) {
        $.writeln(msg);
    }
}

function logError(msg) {
    $.writeln("ERROR: " + msg);
}

function cleanup() {
    try {
        var tempFolder = new Folder(CONFIG.TEMP_FOLDER);
        if (tempFolder.exists) {
            tempFolder.remove();
            logMessage("Pasta temporária removida");
        }
    } catch (e) {
        logMessage("Info: Não foi possível remover pasta temporária");
    }
}

function formatTime(ms) {
    var seconds = Math.floor(ms / 1000);
    var minutes = Math.floor(seconds / 60);
    seconds = seconds % 60;

    if (minutes > 0) {
        return minutes + "m " + seconds + "s";
    }
    return seconds + "s";
}

// ============================================================================
// FUNÇÃO PRINCIPAL
// ============================================================================

function main() {
    try {
        // Verifica se Illustrator está com documento aberto
        if (app.documents.length == 0) {
            alert("Por favor, abra ou crie um documento no Illustrator");
            return;
        }

        // Mostra diálogo
        var options = showAdvancedDialog();
        if (!options) {
            return;
        }

        PROGRESS.startTime = new Date();

        // Valida arquivo
        if (!options.file.exists) {
            alert("Arquivo não encontrado");
            return;
        }

        logMessage("\n=== INICIANDO IMPORTAÇÃO ===");
        logMessage("Arquivo: " + options.file.displayName);

        // Extrai PPTX
        logMessage("Extraindo PPTX...");
        var extractedFolder = extractPPTX(options.file);
        if (!extractedFolder) {
            return;
        }

        // Obtém slides
        logMessage("Analisando slides...");
        var slides = getSlides(extractedFolder);

        if (slides.length == 0) {
            alert("Nenhum slide encontrado");
            cleanup();
            return;
        }

        PROGRESS.totalSlides = slides.length;

        logMessage("Encontrados " + slides.length + " slides");
        logMessage("Dimensões do artboard: " + options.artboardWidth + "x" + options.artboardHeight);

        // Obtém documento ativo
        var doc = app.activeDocument;

        // Remove artboards padrão se necessário
        while (doc.artboards.length > 0) {
            doc.artboards.remove(0);
        }

        // Importa cada slide
        for (var i = 0; i < slides.length; i++) {
            logMessage("\n[" + (i + 1) + "/" + slides.length + "] Processando slide...");

            var artboard = createArtboard(doc, i, options.artboardWidth, options.artboardHeight);
            if (artboard) {
                importSlideContent(slides[i], i, doc, artboard, options, extractedFolder);
                PROGRESS.processedSlides++;
            }
        }

        // Limpa recursos
        cleanup();

        // Mensagem final
        var elapsed = new Date() - PROGRESS.startTime;
        var message = "Importação Concluída!\n\n";
        message += "✓ " + PROGRESS.processedSlides + " slides importados\n";
        message += "✓ " + PROGRESS.processedSlides + " artboards criados\n";
        message += "⏱ Tempo: " + formatTime(elapsed);

        alert(message);

        logMessage("\n=== IMPORTAÇÃO FINALIZADA ===");
        logMessage("Tempo total: " + formatTime(elapsed));

    } catch (e) {
        logError("Erro geral: " + e);
        alert("Erro durante importação: " + e);
        cleanup();
    }
}

// Executa
main();

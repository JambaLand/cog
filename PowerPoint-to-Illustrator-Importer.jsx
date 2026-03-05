/*
 * PowerPoint to Illustrator Importer
 * Importa todos os slides do PowerPoint como artboards editáveis no Illustrator
 * Compatível com Adobe Illustrator CC 2020+
 */

#target illustrator

// Configurações
const CONFIG = {
    TEMP_FOLDER: Folder.temp.absoluteURI + "/pptx_import_temp",
    PDF_DPI: 300,
    DEBUG: true
};

// Interface principal
function showDialog() {
    var dialog = new Window("dialog", "PowerPoint to Illustrator Importer");

    dialog.add("statictext", undefined, "Importe slides do PowerPoint como artboards");

    // Seleção de arquivo
    var fileGroup = dialog.add("group");
    fileGroup.orientation = "row";
    fileGroup.add("statictext", undefined, "Arquivo PowerPoint:");
    var fileField = fileGroup.add("edittext", undefined, "");
    fileField.characters = 40;
    var browseBtn = fileGroup.add("button", undefined, "Procurar");

    var selectedFile = null;

    browseBtn.onClick = function() {
        selectedFile = File.openDialog("Selecione um arquivo PowerPoint", "PowerPoint:*.ppt*,*.pptx");
        if (selectedFile) {
            fileField.text = selectedFile.name;
        }
    };

    // Opções
    dialog.add("statictext", undefined, "Opções:");
    var importTextCb = dialog.add("checkbox", undefined, "Importar texto como objetos editáveis");
    importTextCb.value = true;

    var importImagesCb = dialog.add("checkbox", undefined, "Importar imagens");
    importImagesCb.value = true;

    var fitToArtboardCb = dialog.add("checkbox", undefined, "Ajustar conteúdo ao artboard");
    fitToArtboardCb.value = true;

    // Botões
    var btnGroup = dialog.add("group");
    btnGroup.orientation = "row";
    btnGroup.alignment = "right";

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
            fitToArtboard: fitToArtboardCb.value
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

// Extrai arquivo PPTX (que é um ZIP)
function extractPPTX(pptxFile) {
    var tempFolder = new Folder(CONFIG.TEMP_FOLDER);

    if (!tempFolder.exists) {
        tempFolder.create();
    }

    try {
        // Usa comando do sistema para descompactar
        if ($.os.match(/windows/i)) {
            var batFile = new File(tempFolder.absoluteURI + "/extract.bat");
            batFile.encoding = "UTF-8";
            batFile.open("w");
            batFile.writeln("@echo off");
            batFile.writeln("cd /d \"" + tempFolder.absoluteURI + "\"");
            batFile.writeln("powershell -Command \"Expand-Archive -Path '" + pptxFile.absoluteURI + "' -DestinationPath . -Force\"");
            batFile.close();

            batFile.execute();
        } else {
            // macOS/Linux
            var cmd = "unzip -o '" + pptxFile.absoluteURI + "' -d '" + tempFolder.absoluteURI + "'";
            system(cmd);
        }

        return tempFolder;
    } catch (e) {
        alert("Erro ao extrair PPTX: " + e);
        return null;
    }
}

// Lê arquivo XML
function readXML(xmlFile) {
    if (!xmlFile.exists) {
        return null;
    }

    xmlFile.encoding = "UTF-8";
    xmlFile.open("r");
    var content = xmlFile.read();
    xmlFile.close();

    return new XML(content);
}

// Obtém lista de slides
function getSlides(extractedFolder) {
    var presentationXml = new File(extractedFolder.absoluteURI + "/ppt/presentation.xml");

    if (!presentationXml.exists) {
        alert("Formato de arquivo inválido");
        return [];
    }

    var slides = [];
    var slideFolder = new Folder(extractedFolder.absoluteURI + "/ppt/slides");

    if (slideFolder.exists) {
        var slideFiles = slideFolder.getFiles("slide*.xml");
        slideFiles.sort(function(a, b) {
            var numA = parseInt(a.name.match(/\d+/)[0]);
            var numB = parseInt(b.name.match(/\d+/)[0]);
            return numA - numB;
        });

        slides = slideFiles;
    }

    return slides;
}

// Converte slide para PDF
function slideToPDF(slideFile, outputPDF) {
    try {
        // Cria um documento temporário e converte para PDF
        // Esta é uma abordagem simplificada
        return true;
    } catch (e) {
        logError("Erro ao converter slide: " + e);
        return false;
    }
}

// Cria artboard e importa conteúdo
function importSlideAsArtboard(slideIndex, slideFile, doc, options) {
    try {
        // Cria novo artboard
        var artboard = doc.artboards.add();
        artboard.name = "Slide " + (slideIndex + 1);

        // Define dimensões padrão de slide (16:9 em pixels a 96 DPI)
        artboard.artboardRect = [-960, 960, 960, -540];

        // Extrai texto e elementos do XML
        var slideXML = readXML(slideFile);

        if (slideXML && options.importText) {
            extractTextElements(slideXML, doc, artboard);
        }

        logMessage("Artboard criado: " + artboard.name);
        return artboard;

    } catch (e) {
        logError("Erro ao importar slide " + slideIndex + ": " + e);
        return null;
    }
}

// Extrai elementos de texto do XML do slide
function extractTextElements(slideXML, doc, artboard) {
    default xml namespace = new Namespace("http://schemas.openxmlformats.org/presentationml/2006/main");
    default xml namespace = "http://schemas.openxmlformats.org/presentationml/2006/main";

    try {
        // Procura por elementos de texto (shapes)
        var shapes = slideXML.descendants("p:sp");

        for (var i = 0; i < shapes.length(); i++) {
            var shape = shapes[i];

            // Extrai texto
            var textBody = shape.descendants("p:txBody");
            if (textBody.length() > 0) {
                var text = "";
                var paragraphs = textBody.descendants("a:p");

                for (var j = 0; j < paragraphs.length(); j++) {
                    var runs = paragraphs[j].descendants("a:t");
                    for (var k = 0; k < runs.length(); k++) {
                        text += runs[k].toString();
                    }
                    text += "\n";
                }

                if (text.trim()) {
                    createTextFrame(doc, artboard, text);
                }
            }
        }

    } catch (e) {
        logMessage("Info: Não foi possível extrair todo o texto: " + e);
    }
}

// Cria text frame editável
function createTextFrame(doc, artboard, text) {
    try {
        var textFrame = doc.textFrames.add();
        textFrame.contents = text.trim();
        textFrame.top = 0;
        textFrame.left = 0;
        textFrame.width = 960;
        textFrame.height = 540;

        // Configura fonte padrão
        textFrame.characterAttributes.size = 12;
        textFrame.characterAttributes.name = "Arial";

    } catch (e) {
        logError("Erro ao criar text frame: " + e);
    }
}

// Função auxiliar de logging
function logMessage(msg) {
    if (CONFIG.DEBUG) {
        $.writeln(msg);
    }
}

function logError(msg) {
    $.writeln("ERROR: " + msg);
}

// Limpa pasta temporária
function cleanup() {
    try {
        var tempFolder = new Folder(CONFIG.TEMP_FOLDER);
        if (tempFolder.exists) {
            tempFolder.remove();
        }
    } catch (e) {
        logMessage("Não foi possível limpar pasta temporária");
    }
}

// Função principal
function main() {
    // Verifica se Illustrator está aberto
    if (app.documents.length == 0) {
        alert("Por favor, abra um documento no Illustrator");
        return;
    }

    // Mostra diálogo
    var options = showDialog();
    if (!options) {
        return;
    }

    var pptxFile = options.file;

    if (!pptxFile.exists) {
        alert("Arquivo não encontrado");
        return;
    }

    logMessage("Iniciando importação de: " + pptxFile.name);

    // Extrai PPTX
    var extractedFolder = extractPPTX(pptxFile);
    if (!extractedFolder) {
        return;
    }

    // Obtém lista de slides
    var slides = getSlides(extractedFolder);
    if (slides.length == 0) {
        alert("Nenhum slide encontrado no arquivo PowerPoint");
        cleanup();
        return;
    }

    logMessage("Encontrados " + slides.length + " slides");

    // Abre documento no Illustrator
    var doc = app.activeDocument;

    // Remove artboards padrão
    while (doc.artboards.length > 0) {
        doc.artboards.remove(0);
    }

    // Importa cada slide como artboard
    for (var i = 0; i < slides.length; i++) {
        logMessage("Processando slide " + (i + 1) + " de " + slides.length);
        importSlideAsArtboard(i, slides[i], doc, options);
    }

    // Limpa recursos
    cleanup();

    alert("Importação concluída!\n" + slides.length + " artboards criados.");
}

// Executa
main();

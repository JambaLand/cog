# Começando

Este guia irá orientá-lo através do que você pode fazer com o Cog usando um modelo de exemplo.

> [!TIP]
> Usando um modelo de linguagem para ajudá-lo a escrever o código para seu novo modelo Cog?
>
> Alimentar com [https://cog.run/llms.txt](https://cog.run/llms.txt), que tem toda a documentação do Cog agrupada em um único arquivo. Para saber mais sobre este formato, confira [llmstxt.org](https://llmstxt.org).

## Pré-requisitos

- **macOS ou Linux**. O Cog funciona em macOS e Linux, mas não oferece suporte ao Windows.
- **Docker**. Cog usa Docker para criar um contêiner para seu modelo. Você precisará [instalar o Docker](https://docs.docker.com/get-docker/) antes de poder executar o Cog.

## Instalar Cog

Primeiro, instale o Cog:

```bash
sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_`uname -s`_`uname -m`
sudo chmod +x /usr/local/bin/cog

```

## Criar um projeto

Vamos fazer um diretório para trabalhar:

```bash
mkdir cog-quickstart
cd cog-quickstart

```

## Executar comandos

A coisa mais simples que você pode fazer com o Cog é executar um comando dentro de um ambiente Docker.

A primeira coisa que você precisa fazer é criar um arquivo chamado `cog.yaml`:

```yaml
build:
  python_version: "3.11"
```

Então, você pode executar qualquer comando dentro deste ambiente. Por exemplo, digite

```bash
cog run python

```

e você terá um shell Python interativo:

```none
✓ Construindo imagem Docker a partir de cog.yaml... Construído com sucesso 8f54020c8981
Executando 'python' em Docker com o diretório atual montado como um volume...
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Python 3.11.1 (main, Jan 27 2023, 10:52:46)
[GCC 9.3.0] no linux
Digite "help", "copyright", "credits" ou "license" para mais informações.
>>>
```

(Pressione Ctrl-D para sair do shell Python.)

Dentro deste ambiente Docker você pode fazer qualquer coisa – executar um notebook Jupyter, seu script de treinamento, seu script de avaliação e assim por diante.

## Executar previsões em um modelo

Vamos fingir que treinamos um modelo. Com o Cog, podemos definir como executar previsões nele de forma padrão, para que outras pessoas possam executar facilmente previsões nele sem ter que procurar um script de previsão.

Primeiro, execute isto para obter alguns pesos de modelo pré-treinado:

```bash
WEIGHTS_URL=https://storage.googleapis.com/tensorflow/keras-applications/resnet/resnet50_weights_tf_dim_ordering_tf_kernels.h5
curl -O $WEIGHTS_URL

```

Então, precisamos escrever código para descrever como as previsões são executadas no modelo.

Salve isto em `predict.py`:

```python
from typing import Any
from cog import BasePredictor, Input, Path
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np


class Predictor(BasePredictor):
    def setup(self):
        """Carregue o modelo na memória para tornar a execução de várias previsões eficiente"""
        self.model = ResNet50(weights='resnet50_weights_tf_dim_ordering_tf_kernels.h5')

    # Defina os argumentos e tipos que o modelo recebe como entrada
    def predict(self, image: Path = Input(description="Imagem para classificar")) -> Any:
        """Execute uma única previsão no modelo"""
        # Pré-processe a imagem
        img = keras_image.load_img(image, target_size=(224, 224))
        x = keras_image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # Execute a previsão
        preds = self.model.predict(x)
        # Retorne as 3 principais previsões
        return decode_predictions(preds, top=3)[0]
```

Também precisamos apontar o Cog para isto e dizer qual versão do Python instalar as dependências. Atualize `cog.yaml` para ficar assim:

```yaml
build:
  python_version: "3.11"
  python_packages:
    - pillow==9.5.0
    - tensorflow==2.12.0
predict: "predict.py:Predictor"
```

Vamos pegar uma imagem para testar o modelo com:

```bash
IMAGE_URL=https://gist.githubusercontent.com/bfirsh/3c2115692682ae260932a67d93fd94a8/raw/56b19f53f7643bb6c0b822c410c366c3a6244de2/mystery.jpg
curl $IMAGE_URL > input.jpg

```

Agora, vamos executar o modelo usando Cog:

```bash
cog predict -i image=@input.jpg

```

Se você vir a seguinte saída

```
[
  [
    "n02123159",
    "tiger_cat",
    0.4874822497367859
  ],
  [
    "n02123045",
    "tabby",
    0.23169134557247162
  ],
  [
    "n02124075",
    "Egyptian_cat",
    0.09728282690048218
  ]
]
```

então funcionou!

Observação: A primeira vez que você executar `cog predict`, o processo de compilação será acionado para gerar um contêiner Docker que pode executar seu modelo. Da próxima vez que você executar `cog predict`, o contêiner pré-construído será usado.

## Construir uma imagem

Podemos assar o código do seu modelo, os pesos treinados e o ambiente Docker em uma imagem Docker. Esta imagem serve previsões com um servidor HTTP e pode ser implantada em qualquer lugar onde o Docker funcione para servir previsões em tempo real.

```bash
cog build -t resnet
# Construindo imagem Docker...
# Construída resnet:latest

```

Depois de construir a imagem, você pode opcionalmente visualizar o dockerfile gerado para ter uma ideia do que o Cog está fazendo nos bastidores:

```bash
cog debug
```

Você pode executar esta imagem com `cog predict` passando o nome do arquivo como argumento:

```bash
cog predict resnet -i image=@input.jpg

```

Ou, você pode executá-lo com o Docker diretamente, e ele servirá um servidor HTTP:

```bash
docker run -d --rm -p 5000:5000 resnet

```

Podemos enviar entradas diretamente com `curl`:

```bash
curl http://localhost:5000/predictions -X POST \
    -H 'Content-Type: application/json' \
    -d '{"input": {"image": "https://gist.githubusercontent.com/bfirsh/3c2115692682ae260932a67d93fd94a8/raw/56b19f53f7643bb6c0b822c410c366c3a6244de2/mystery.jpg"}}'

```

Como atalho, você pode adicionar o nome da imagem Docker como uma linha adicional em `cog.yaml`:

```yaml
image: "r8.im/replicate/resnet"
```

Depois disso, você pode usar `cog push` para construir e enviar a imagem para um registro Docker:

```bash
cog push
# Construindo r8.im/replicate/resnet...
# Enviando r8.im/replicate/resnet...
# Enviado!
```

A imagem Docker agora está acessível a qualquer pessoa ou sistema que tenha acesso a este registro Docker.

> **Observação**
> Os repositórios de modelos frequentemente contêm arquivos de dados grandes, como pesos e checkpoints. Se você colocar esses arquivos em seu próprio subdiretório e executar `cog build` com o sinalizador `--separate-weights`, o Cog copiará esses arquivos para uma camada Docker separada, o que reduz o tempo necessário para reconstruir após fazer alterações no código.
>
> ```shell
> # ✅ Sim
> .
> ├── checkpoints/
> │   └── weights.ckpt
> ├── predict.py
> └── cog.yaml
>
> # ❌ Não
> .
> ├── weights.ckpt # <- Não coloque pesos no diretório raiz
> ├── predict.py
> └── cog.yaml
>
> # ❌ Não
> .
> ├── checkpoints/
> │   ├── weights.ckpt
> │   └── load_weights.py # <- Não coloque código no diretório de pesos
> ├── predict.py
> └── cog.yaml
> ```

## Próximos passos

Essas são as noções básicas! Em seguida, você pode querer dar uma olhada em:

- [Um guia para ajudá-lo a configurar seu próprio modelo no Cog.](getting-started-own-model.md)
- [Um guia explicando como implantar um modelo.](deploy.md)
- [Referência para `cog.yaml`](yaml.md)
- [Referência para a biblioteca Python](python.md)

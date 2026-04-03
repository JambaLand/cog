# Cog: Contêineres para aprendizado de máquina

Cog é uma ferramenta de código aberto que permite empacotar modelos de aprendizado de máquina em um contêiner padrão e pronto para produção.

Você pode implantar seu modelo empacotado em sua própria infraestrutura ou em [Replicate](https://replicate.com/).

## Destaques

- 📦 **Contêineres Docker sem complicações.** Escrever seu próprio `Dockerfile` pode ser um processo confuso. Com o Cog, você define seu ambiente com um [arquivo de configuração simples](#como-funciona) e ele gera uma imagem Docker com todas as melhores práticas: imagens base Nvidia, cache eficiente de dependências, instalação de versões específicas do Python, padrões de variáveis de ambiente sensatos e muito mais.

- 🤬️ **Sem mais problemas com CUDA.** Cog sabe quais combinações de CUDA/cuDNN/PyTorch/Tensorflow/Python são compatíveis e configura tudo corretamente para você.

- ✅ **Defina as entradas e saídas do seu modelo com Python padrão.** Em seguida, Cog gera um esquema OpenAPI e valida as entradas e saídas com Pydantic.

- 🎁 **Servidor HTTP de previsão automático**: Os tipos do seu modelo são usados para gerar dinamicamente uma API RESTful HTTP usando [FastAPI](https://fastapi.tiangolo.com/).

- 🥞 **Worker de fila automático.** Modelos de aprendizado profundo de longa duração ou processamento em lote são melhor arquitetados com uma fila. Os modelos Cog fazem isso imediatamente. Redis é atualmente suportado, com mais no futuro.

- ☁️ **Armazenamento em nuvem.** Os arquivos podem ser lidos e escritos diretamente no Amazon S3 e Google Cloud Storage. (Em breve.)

- 🚀 **Pronto para produção.** Implante seu modelo em qualquer lugar onde as imagens Docker funcionem. Sua própria infraestrutura ou [Replicate](https://replicate.com).

## Como funciona

Defina o ambiente Docker em que seu modelo é executado com `cog.yaml`:

```yaml
build:
  gpu: true
  system_packages:
    - "libgl1-mesa-glx"
    - "libglib2.0-0"
  python_version: "3.12"
  python_packages:
    - "torch==2.3"
predict: "predict.py:Predictor"
```

Defina como as previsões são executadas em seu modelo com `predict.py`:

```python
from cog import BasePredictor, Input, Path
import torch

class Predictor(BasePredictor):
    def setup(self):
        """Carregue o modelo na memória para tornar a execução de várias previsões eficiente"""
        self.model = torch.load("./weights.pth")

    # Os argumentos e tipos que o modelo recebe como entrada
    def predict(self,
          image: Path = Input(description="Imagem de entrada em escala de cinza")
    ) -> Path:
        """Execute uma única previsão no modelo"""
        processed_image = preprocess(image)
        output = self.model(processed_image)
        return postprocess(output)
```

Acima, aceitamos um caminho para a imagem como entrada e retornamos um caminho para nossa imagem transformada após executá-la através do modelo.

Agora você pode executar previsões neste modelo:

```console
$ cog predict -i image=@input.jpg
--> Construindo imagem Docker...
--> Executando previsão...
--> Saída escrita em output.jpg
```

Ou construa uma imagem Docker para implantação:

```console
$ cog build -t my-colorization-model
--> Construindo imagem Docker...
--> Construído my-colorization-model:latest

$ docker run -d -p 5000:5000 --gpus all my-colorization-model

$ curl http://localhost:5000/predictions -X POST \
    -H 'Content-Type: application/json' \
    -d '{"input": {"image": "https://.../input.jpg"}}'
```

Ou combine construção e execução via comando `serve`:

```console
$ cog serve -p 8080

$ curl http://localhost:8080/predictions -X POST \
    -H 'Content-Type: application/json' \
    -d '{"input": {"image": "https://.../input.jpg"}}'
```

## Por que estamos construindo isso?

É realmente difícil para pesquisadores enviar modelos de aprendizado de máquina para produção.

Parte da solução é o Docker, mas é muito complexo fazê-lo funcionar: Dockerfiles, pré/pós-processamento, servidores Flask, versões CUDA. Mais vezes do que não, o pesquisador tem que se sentar com um engenheiro para fazer a coisa ser implantada.

[Andreas](https://github.com/andreasjansson) e [Ben](https://github.com/bfirsh) criaram o Cog. Andreas costumava trabalhar no Spotify, onde construiu ferramentas para construir e implantar modelos de ML com Docker. Ben trabalhou no Docker, onde criou [Docker Compose](https://github.com/docker/compose).

Percebemos que, além do Spotify, outras empresas também estavam usando Docker para construir e implantar modelos de aprendizado de máquina. [Uber](https://eng.uber.com/michelangelo-pyml/) e outros construíram sistemas semelhantes. Portanto, estamos fazendo uma versão de código aberto para que outras pessoas possam fazer isso também.

Entre em contato se você estiver interessado em usá-lo ou quer colaborar conosco. [Estamos no Discord](https://discord.gg/replicate) ou envie-nos um e-mail em [team@replicate.com](mailto:team@replicate.com).

## Pré-requisitos

- **macOS, Linux ou Windows 11**. Cog funciona em macOS, Linux e Windows 11 com [WSL 2](docs/wsl2/wsl2.md)
- **Docker**. Cog usa Docker para criar um contêiner para seu modelo. Você precisará [instalar o Docker](https://docs.docker.com/get-docker/) antes de poder executar o Cog. Se você instalar o Docker Engine em vez do Docker Desktop, você precisará [instalar o Buildx](https://docs.docker.com/build/architecture/#buildx) também.

## Instalar

Se você estiver usando macOS, pode instalar o Cog usando o Homebrew:

```console
brew install cog
```

Você também pode baixar e instalar a versão mais recente usando nosso 
[script de instalação](https://cog.run/install):

```sh
# bash, zsh e outros shells
sh <(curl -fsSL https://cog.run/install.sh)

# Para português, use:
sh <(curl -fsSL https://cog.run/install.pt.sh)

# shell fish
sh (curl -fsSL https://cog.run/install.sh | psub)

# baixar com wget e executar em um comando separado
wget -qO- https://cog.run/install.sh
sh ./install.sh
```

Você pode instalar manualmente a versão mais recente do Cog diretamente do GitHub 
executando os seguintes comandos em um terminal:

```console
sudo curl -o /usr/local/bin/cog -L "https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
sudo chmod +x /usr/local/bin/cog
```

Alternativamente, você pode construir o Cog a partir do código-fonte e instalá-lo com estes comandos:

```console
make
sudo make install
```

Ou se você está em docker:

```
RUN sh -c "INSTALL_DIR=\"/usr/local/bin\" SUDO=\"\" $(curl -fsSL https://cog.run/install.sh)"
```

## Atualizar

Se você estiver usando macOS e instalou anteriormente o Cog com o Homebrew, execute o seguinte:

```console
brew upgrade cog
```

Caso contrário, você pode atualizar para a versão mais recente executando os mesmos comandos que usou para instalá-lo.

## Próximos passos

- [Comece com um modelo de exemplo](docs/getting-started.md)
- [Comece com seu próprio modelo](docs/getting-started-own-model.md)
- [Usando Cog com notebooks](docs/notebooks.md)
- [Usando Cog com Windows 11](docs/wsl2/wsl2.md)
- [Veja alguns exemplos de uso do Cog](https://github.com/replicate/cog-examples)
- [Implantar modelos com Cog](docs/deploy.md)
- [Referência de `cog.yaml`](docs/yaml.md) para aprender como definir o ambiente do seu modelo
- [Referência de interface de previsão](docs/python.md) para aprender como a interface `Predictor` funciona
- [Referência de interface de treinamento](docs/training.md) para aprender como adicionar uma API de ajuste fino ao seu modelo
- [Referência de API HTTP](docs/http.md) para aprender como usar a API HTTP que os modelos servem

## Precisa de ajuda?

[Junte-se a nós em #cog no Discord.](https://discord.gg/replicate)

## Contribuidores ✨

Obrigado a essas pessoas maravilhosas ([chave emoji](https://allcontributors.org/docs/en/emoji-key)):

Veja a versão em inglês do README para a lista completa de contribuidores.

Este projeto segue a especificação [all-contributors](https://github.com/all-contributors/all-contributors). Contribuições de qualquer tipo são bem-vindas!

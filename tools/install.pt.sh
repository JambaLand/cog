#!/bin/sh
#
# Este script deve ser executado via curl:
#   sh -c "$(curl -fsSL https://raw.githubusercontent.com/replicate/cog/main/tools/install.pt.sh)"
# ou via wget:
#   sh -c "$(wget -qO- https://raw.githubusercontent.com/replicate/cog/main/tools/install.pt.sh)"
# ou via fetch:
#   sh -c "$(fetch -o - https://raw.githubusercontent.com/replicate/cog/main/tools/install.pt.sh)"
#
# Como alternativa, você pode primeiro baixar o script de instalação e executá-lo depois:
#   wget https://raw.githubusercontent.com/replicate/cog/main/tools/install.pt.sh
#   sh install.pt.sh
#
# Você pode ajustar o local de instalação definindo a variável de ambiente INSTALL_DIR ao executar o script.
#   INSTALL_DIR=~/meu/local/instalacao sh install.pt.sh
#
# Por padrão, o cog será instalado em /usr/local/bin/cog


# Este script de instalação é baseado no script do ohmyzsh[1], que é licenciado sob a Licença MIT
# [1] https://github.com/ohmyzsh/ohmyzsh/blob/master/tools/install.sh
# Licença MIT

# Copyright (c) 2009-2022 Robby Russell e contribuidores (https://github.com/ohmyzsh/ohmyzsh/contributors)

# É concedida permissão, gratuitamente, a qualquer pessoa que obtenha uma cópia
# deste software e arquivos de documentação associados (o "Software"), para lidar
# no Software sem restrições, incluindo sem limitações os direitos
# de usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender
# cópias do Software, e permitir que as pessoas para as quais o Software é
# fornecido a fazê-lo, sujeito às seguintes condições:

# O aviso de copyright acima e este aviso de permissão devem ser incluídos em todas
# as cópias ou partes substanciais do Software.

# O SOFTWARE É FORNECIDO "COMO ESTÁ", SEM GARANTIA DE QUALQUER TIPO, EXPRESSA OU
# IMPLÍCITA, INCLUINDO MAS NÃO SE LIMITANDO ÀS GARANTIAS DE COMERCIABILIDADE,
# ADEQUAÇÃO PARA UM PROPÓSITO PARTICULAR E NÃO INFRAÇÃO. EM NENHUM CASO OS AUTORES OU
# TITULARES DE DIREITOS AUTORAIS SERÃO RESPONSÁVEIS POR QUALQUER REIVINDICAÇÃO, DANOS OU OUTRA
# RESPONSABILIDADE, SEJA EM AÇÃO DE CONTRATO, ATO ILÍCITO OU DE OUTRA FORMA, DECORRENTE DE,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
set -e

set_install_dir() {
  # Define o diretório de instalação
  DEFAULT_INSTALL_DIR="/usr/local/bin"
  if [ -z "${INSTALL_DIR}" ]; then
    read -p "Local de instalação? [$DEFAULT_INSTALL_DIR]: " INSTALL_DIR
    INSTALL_DIR=${INSTALL_DIR:-$DEFAULT_INSTALL_DIR}
  fi
  if [ ! -d "$INSTALL_DIR" ]; then
    echo "O diretório $INSTALL_DIR não existe. Por favor, crie-o e execute este script novamente."
    # Pede ao usuário para criar o diretório manualmente, em vez de criá-lo para ele,
    # para que não digite "y" acidentalmente e instale em ./y
    exit 1
  fi
  # Expande abreviações em INSTALL_DIR
  INSTALL_DIR=$(cd "$INSTALL_DIR"; pwd)
}

command_exists() {
  command -v "$@" >/dev/null 2>&1
}

user_can_sudo() {
  # Verifica se o sudo está instalado
  command_exists $SUDO || return 1
  # Termux não pode executar sudo, então podemos detectar e sair da função cedo.
  case "$PREFIX" in
  *com.termux*) return 1 ;;
  esac
  # O comando a seguir tem 3 partes:
  #
  # 1. Execute `sudo` com `-v`. Faz o seguinte:
  #    • com privilégio: solicita uma senha imediatamente.
  #    • sem privilégio: sai com código de erro 1 e imprime a mensagem:
  #      Desculpe, o usuário <nome_do_usuário> não pode executar sudo em <nome_do_host>
  #
  # 2. Passe `-n` para `sudo` para dizer que não deve solicitar uma senha. Se a
  #    senha não for necessária, o comando terminará com código de saída 0.
  #    Se for necessária, sudo sairá com código de erro 1 e imprimirá a
  #    mensagem:
  #    sudo: uma senha é necessária
  #
  # 3. Verifique as palavras "may not run sudo" na saída para saber realmente se
  #    o usuário tem privilégios ou não. Para isso, devemos certificar-se de
  #    executar `sudo` na localidade padrão (com `LANG=`) para que a mensagem
  #    permaneça consistente independentemente da localidade do usuário.
  #
  ! LANG= $SUDO -n -v 2>&1 | grep -q "may not run $SUDO"
}

check_docker() {
  if ! command_exists docker; then
  echo "Docker não está instalado em seu sistema. Por favor, instale o Docker antes de prosseguir."
    exit 1
  fi

  if ! docker run hello-world >/dev/null 2>&1; then
    echo "AVISO: O mecanismo Docker não está funcionando, ou o docker não pode ser executado sem sudo. Por favor, configure o Docker para que seu usuário tenha permissão para executá-lo: https://docs.docker.com/engine/install/linux-postinstall/"
  fi
}

setup_cog() {
  COG_LOCATION="${INSTALL_DIR}/cog"
  BINARY_URI="https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
  if [ -f "$COG_LOCATION" ]; then
    echo "Um arquivo já existe em $COG_LOCATION"
    echo "Você quer deletar este arquivo e continuar com a instalação mesmo assim?"
    read -p "Deletar arquivo? (s/N): " choice
    case "$choice" in
      s|S ) echo "Deletando arquivo existente e continuando com a instalação..."; $SUDO rm $COG_LOCATION;;
      * ) echo "Saindo da instalação."; exit 1;;
    esac
  fi
  if command_exists curl; then
    $SUDO curl -o $COG_LOCATION -L $BINARY_URI
  elif command_exists wget; then
    $SUDO wget $BINARY_URI -O $COG_LOCATION
  elif command_exists fetch; then
    $SUDO fetch -o $COG_LOCATION $BINARY_URI
  else
    echo "Uma de curl, wget ou fetch deve estar presente para que este instalador funcione."
    exit 1
  fi
  if [ "$(cat $COG_LOCATION)" = "Not Found" ]; then
    echo "Erro: Binário do Cog não encontrado em ${BINARY_URI}. Verifique as versões para ver se um binário está disponível para seu sistema."
    rm $COG_LOCATION
    exit 1
  fi

  $SUDO chmod +x $COG_LOCATION

  SHELL_NAME=$(basename "$SHELL")
  if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "Adicionando $INSTALL_DIR ao PATH em .$SHELL_NAME"rc
    echo "" >> ~/.$SHELL_NAME"rc"
    echo "# Criado pelo script de instalação do \`cog\` em $(date)" >> ~/.$SHELL_NAME"rc"
    echo "export PATH=\$PATH:$INSTALL_DIR" >> ~/.$SHELL_NAME"rc"
    source ~/.$SHELL_NAME"rc"

    echo "Você pode precisar abrir uma nova janela de terminal para executar o cog pela primeira vez."
  fi

  echo
}


print_success() {
  echo "Cog instalado com sucesso. Execute \`cog login\` para configurar o acesso ao Replicate"
}

main() {

  # Verifica se é macOS
  if [ "$(uname -s)" = "Darwin" ]; then
    echo "No macOS, é recomendado instalar o cog usando o Homebrew em vez disso:"
    echo \`brew install cog\`
    echo "Você quer continuar com esta instalação mesmo assim?"

    read -p "Continuar? (s/N): " choice
    case "$choice" in
      s|S ) echo "Continuando com a instalação...";;
      * ) echo "Saindo da instalação."; exit 1;;
    esac
  fi

  set_install_dir

  # Verifica se o comando `cog` já existe
  if command_exists cog; then
    echo "Um comando cog já existe em seu sistema no seguinte local: $(which cog)".
    echo "As instalações podem interferir uma com a outra."
    echo "Você quer continuar com esta instalação mesmo assim?"
    read -p "Continuar? (s/N): " choice
    case "$choice" in
      s|S ) echo "Continuando com a instalação...";;
      * ) echo "Saindo da instalação."; exit 1;;
    esac
  fi

  # Verifica os privilégios de sudo do usuário
  if [ -z "${SUDO+set}" ]; then
    SUDO="sudo"
  fi
  if [ ! user_can_sudo ] && [ "${SUDO}" != "" ]; then
    echo "Você precisa de permissões de sudo para executar este script de instalação. Por favor, tente novamente como um usuário com sudo."
    exit 1
  fi

  check_docker
  setup_cog

  if command_exists cog; then
    print_success
  else
    echo 'Erro: cog não foi instalado.'
    exit 1
  fi
}

main "$@"

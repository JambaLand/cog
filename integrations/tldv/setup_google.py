#!/usr/bin/env python3
"""
Script para ajudar a configurar Google API Key
Mostra passo-a-passo onde encontrar a chave
"""

import os
import sys


def print_header(text):
    """Imprimir cabeçalho"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_step(num, text):
    """Imprimir passo"""
    print(f"📍 PASSO {num}: {text}")
    print("-" * 70)


def check_current_config():
    """Verificar configuração atual"""
    print_header("🔍 VERIFICANDO CONFIGURAÇÃO ATUAL")

    api_key = os.getenv("GOOGLE_API_KEY", "")
    calendar_id = os.getenv("GOOGLE_CALENDAR_ID", "jean@jaquejamba.com")

    print(f"GOOGLE_API_KEY: {api_key if api_key else '❌ NÃO CONFIGURADA'}")
    print(f"GOOGLE_CALENDAR_ID: {calendar_id}")

    # Verificar arquivo .env.local
    env_file = ".env.local"
    if os.path.exists(env_file):
        print(f"\n✅ Arquivo {env_file} encontrado:")
        with open(env_file, "r") as f:
            content = f.read()
            print(content)
    else:
        print(f"\n⚠️  Arquivo {env_file} não encontrado")

    return api_key


def show_google_steps():
    """Mostrar passos para encontrar API Key"""
    print_header("🌐 COMO ENCONTRAR SUA API KEY NO GOOGLE CLOUD")

    print_step(1, "Abra seu navegador Chrome/Firefox/Safari")
    print("""
    1. Clique aqui para abrir direto:
       https://console.cloud.google.com

    2. OU copie e cole na barra de endereço:
       console.cloud.google.com
    """)

    print_step(2, "Faça login com sua conta Google")
    print("""
    1. Use a mesma conta que tem Google Calendar
    2. Clique em "Next" se pedir
    3. Confirme a senha
    """)

    print_step(3, "Procure por 'Credentials' no menu esquerdo")
    print("""
    Menu esquerdo (lateral esquerda):

    📋 Clique em: Credentials

    Você verá uma página com:
    ┌─────────────────────────────────┐
    │ Create Credentials              │
    │ API Keys                        │
    │ OAuth 2.0 Credentials           │
    └─────────────────────────────────┘
    """)

    print_step(4, "Procure ou crie a API Key")
    print("""
    OPÇÃO A - Se já tem uma API Key:
    ───────────────────────────────
    1. Você verá uma tabela com:

       Name    │ Type    │ Created
       ────────┼─────────┼────────
       API Key │ API Key │ Today

    2. Clique em "API Key"
    3. A chave aparece em uma caixa:

       AIza_xxxxxxxxxxxxxxxxxxxxxxxx

    4. Clique no ícone de COPIAR (⎘)

    OPÇÃO B - Se não tem nenhuma:
    ────────────────────────────
    1. Clique no botão azul: + CREATE CREDENTIALS
    2. Escolha: API Key
    3. Uma caixa pop-up aparece com a chave
    4. Copie a chave (clique no ícone ⎘)
    """)

    print_step(5, "Ative a Google Calendar API")
    print("""
    Se ainda não ativou:

    1. No menu esquerdo, clique em: Library
    2. Na busca, digite: calendar
    3. Clique em: Google Calendar API
    4. Clique no botão azul: ENABLE
    5. Aguarde ativar (alguns segundos)
    """)


def show_how_to_paste():
    """Mostrar como configurar a chave"""
    print_header("📝 COMO CONFIGURAR A CHAVE")

    print_step(1, "Você já copiou a chave APIza_... ?")
    print("""
    Se SIM, continue para o Passo 2
    Se NÃO, volte aos passos anteriores
    """)

    print_step(2, "Edite o arquivo .env.local")
    print("""
    Opção A - Via terminal:
    ──────────────────────
    nano .env.local

    Encontre a linha:
    GOOGLE_API_KEY=

    Cole sua chave:
    GOOGLE_API_KEY=AIza_sua_chave_aqui

    Salve: Ctrl+X → Y → Enter

    Opção B - Via exportação:
    ──────────────────────
    export GOOGLE_API_KEY="AIza_sua_chave_aqui"
    """)

    print_step(3, "Teste a configuração")
    print("""
    Execute:

    echo $GOOGLE_API_KEY

    Você deve ver:
    AIza_sua_chave_aqui

    Se vir vazio, a chave não foi configurada
    """)


def show_troubleshooting():
    """Mostrar troubleshooting"""
    print_header("🆘 PROBLEMAS COMUNS")

    print("""
    ❌ "Não vejo o botão + CREATE CREDENTIALS"
    ✅ Solução: Verifique se está em "Credentials" (menu esquerdo)

    ❌ "Vejo a chave mas desapareceu quando fechei a popup"
    ✅ Solução: Clique em "Credentials" novamente, está em uma tabela

    ❌ "Não consigo ativar Google Calendar API"
    ✅ Solução: Certifique-se de ter um projeto criado primeiro

    ❌ "Erro 403 Forbidden ao usar a chave"
    ✅ Solução: A API Key pode estar restrita. Em Credentials:
       - Clique na sua API Key
       - Em "API restrictions", escolha "Google Calendar API"
       - Clique SAVE

    ❌ "Não tenho nenhuma API Key"
    ✅ Solução: Clique em "+ CREATE CREDENTIALS" → "API Key"
    """)


def show_next_steps(api_key):
    """Mostrar próximos passos"""
    print_header("✨ PRÓXIMOS PASSOS")

    if api_key:
        print("✅ Você já tem a API Key configurada!")
        print(f"   Valor: {api_key[:20]}...")
    else:
        print("⚠️  Você ainda não tem a API Key configurada")
        print("\n📋 Faça o seguinte:")
        print("   1. Siga os passos acima")
        print("   2. Copie a chave AIza_...")
        print("   3. Configure em .env.local")

    print("\n🧪 Para testar depois de configurar:")
    print("   python examples/notify_google.py")

    print("\n🔔 Para usar a skill:")
    print("   /tldv notify meeting_001 google")

    print("\n📚 Documentação:")
    print("   README.md")
    print("   NOTIFICATIONS.md")
    print("   SETUP_COMPLETO.md")


def main():
    """Função principal"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "🔐 GUIA SETUP GOOGLE API KEY" + " " * 25 + "║")
    print("╚" + "=" * 68 + "╝")

    # Verificar configuração
    api_key = check_current_config()

    # Mostrar passos
    show_google_steps()

    # Como colar
    show_how_to_paste()

    # Problemas
    show_troubleshooting()

    # Próximos passos
    show_next_steps(api_key)

    print("\n" + "=" * 70)
    print("Precisa de ajuda? Execute este script novamente!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

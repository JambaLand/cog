"""Exemplo: Enviar resumo de reunião para Microsoft Teams."""

import sys
from pathlib import Path

# Adicionar o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from notifications import NotificationManager, TeamsNotificationProvider
from predict import TLDVPredictor


def main() -> None:
    """Exemplo de envio para Teams."""
    print("=" * 60)
    print("EXEMPLO: Enviar Resumo para Microsoft Teams")
    print("=" * 60)

    # 1. Inicializar o predictor
    predictor = TLDVPredictor()
    predictor.setup()

    # 2. Buscar primeira reunião
    print("\n📅 Buscando reunião...")
    meetings = predictor.get_meetings(limit=1)

    if not meetings:
        print("❌ Nenhuma reunião encontrada.")
        return

    meeting = meetings[0]
    meeting_id = meeting["id"]

    # 3. Obter resumo completo
    print(f"✅ Reunião encontrada: {meeting['title']}")
    print("\n📝 Obtendo resumo...")
    summary = predictor.get_meeting_summary(meeting_id)

    # 4. Inicializar gerenciador de notificações
    print("\n🔔 Inicializando notificações...")
    notification_manager = NotificationManager()

    # 5. Registrar provedor Teams manualmente (se necessário)
    # Você pode também usar as variáveis de ambiente:
    # export TEAMS_WEBHOOK_URL="https://outlook.webhook.office.com/..."
    #
    # Para este exemplo, vamos verificar se está configurado
    if not notification_manager.is_configured():
        print(
            "⚠️  Nenhum provedor de notificação configurado.\n"
            "Configure a variável de ambiente:\n"
            "  export TEAMS_WEBHOOK_URL='sua-webhook-url'\n"
        )
        print("💡 Como obter a webhook URL do Teams:")
        print(
            "  1. Vá para Microsoft Teams\n"
            "  2. Clique no canal onde quer notificações\n"
            "  3. Clique em ... → Connectors\n"
            "  4. Configure 'Incoming Webhook'\n"
            "  5. Copie a URL\n"
        )
        return

    # 6. Enviar notificação
    print("\n🚀 Enviando resumo para Teams...")
    results = notification_manager.notify_meeting_summary(summary)

    # 7. Exibir resultado
    print("\n" + "=" * 60)
    print("📊 RESULTADO DO ENVIO")
    print("=" * 60)

    for provider, success in results.items():
        status = "✅ ENVIADO" if success else "❌ FALHOU"
        print(f"{status} - {provider.upper()}")

    if all(results.values()):
        print("\n🎉 Todos os resumos foram enviados com sucesso!")
    else:
        print("\n⚠️  Alguns envios falharam. Verifique as configurações.")

    # 8. Exibir dados que foram enviados
    print("\n" + "=" * 60)
    print("📋 DADOS ENVIADOS")
    print("=" * 60)
    print(f"Título: {summary['title']}")
    print(f"Resumo: {summary['summary'][:200]}...")
    print(f"Pontos-chave: {len(summary['key_points'])}")
    print(f"Ações: {len(summary['action_items'])}")


if __name__ == "__main__":
    main()

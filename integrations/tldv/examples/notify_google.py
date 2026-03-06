"""Exemplo: Criar evento no Google Calendar com resumo da reunião."""

import sys
from pathlib import Path

# Adicionar o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from notifications import GoogleCalendarNotificationProvider, NotificationManager
from predict import TLDVPredictor


def main() -> None:
    """Exemplo de criação de evento no Google Calendar."""
    print("=" * 60)
    print("EXEMPLO: Criar Evento no Google Calendar")
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

    # 5. Verificar configuração
    if not notification_manager.is_configured():
        print(
            "⚠️  Nenhum provedor de notificação configurado.\n"
            "Configure a variável de ambiente:\n"
            "  export GOOGLE_API_KEY='sua-chave-api'\n"
        )
        print("💡 Como obter a chave de API do Google:")
        print(
            "  1. Acesse https://console.cloud.google.com\n"
            "  2. Crie um novo projeto\n"
            "  3. Ative a API 'Google Calendar API'\n"
            "  4. Crie uma credencial API Key\n"
            "  5. Copie a chave\n"
        )
        return

    # 6. Enviar notificação
    print("\n🚀 Criando evento no Google Calendar...")
    results = notification_manager.notify_meeting_summary(summary)

    # 7. Exibir resultado
    print("\n" + "=" * 60)
    print("📊 RESULTADO")
    print("=" * 60)

    for provider, success in results.items():
        status = "✅ CRIADO" if success else "❌ FALHOU"
        print(f"{status} - {provider.upper()}")

    if all(results.values()):
        print("\n🎉 Evento criado com sucesso no Google Calendar!")
    else:
        print("\n⚠️  Falha ao criar evento. Verifique as configurações.")

    # 8. Exibir dados que foram usados
    print("\n" + "=" * 60)
    print("📋 DADOS DO EVENTO")
    print("=" * 60)
    print(f"Título: 📅 {summary['title']}")
    print(f"Resumo: {summary['summary'][:150]}...")
    print(f"\nPontos-chave:")
    for point in summary["key_points"][:3]:
        print(f"  • {point}")

    print(f"\nItens de ação:")
    for action in summary["action_items"][:3]:
        print(f"  • {action['description']} ({action['owner']})")


if __name__ == "__main__":
    main()

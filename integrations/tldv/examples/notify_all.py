"""Exemplo: Enviar resumo para múltiplos canais (Teams + Google)."""

import sys
from pathlib import Path

# Adicionar o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from notifications import NotificationManager
from predict import TLDVPredictor


def main() -> None:
    """Exemplo de envio para múltiplos canais."""
    print("=" * 60)
    print("EXEMPLO: Enviar para Múltiplos Canais")
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

    # 5. Listar provedores configurados
    providers = notification_manager.list_providers()
    print(f"\n✅ Provedores configurados: {', '.join(providers).upper()}")

    if not providers:
        print(
            "\n⚠️  Nenhum provedor configurado.\n"
            "Configure um ou mais:\n"
            "  export TEAMS_WEBHOOK_URL='sua-webhook-url'\n"
            "  export GOOGLE_API_KEY='sua-chave-api'\n"
        )
        return

    # 6. Enviar para todos os provedores
    print("\n🚀 Enviando resumo para todos os canais...")
    results = notification_manager.notify_meeting_summary(summary)

    # 7. Exibir resultado detalhado
    print("\n" + "=" * 60)
    print("📊 RESULTADO DO ENVIO")
    print("=" * 60)

    total = len(results)
    successful = sum(1 for v in results.values() if v)

    for provider, success in results.items():
        status_icon = "✅" if success else "❌"
        status_text = "ENVIADO" if success else "FALHOU"
        print(f"{status_icon} {provider.upper():15} - {status_text}")

    print("\n" + "=" * 60)
    print(f"Resultado: {successful}/{total} provedores bem-sucedidos")

    if successful == total:
        print("🎉 Todos os resumos foram enviados com sucesso!")
    elif successful > 0:
        print("⚠️  Alguns envios falharam. Verifique as configurações.")
    else:
        print("❌ Nenhum envio foi bem-sucedido.")

    # 8. Exibir informações da reunião
    print("\n" + "=" * 60)
    print("📋 INFORMAÇÕES DA REUNIÃO")
    print("=" * 60)
    print(f"Título: {summary['title']}")
    print(f"ID: {summary['meeting_id']}")
    print(f"Sentimento: {summary['sentiment'].upper()}")
    print(f"\nResumo:\n{summary['summary']}\n")

    print("Pontos-chave:")
    for i, point in enumerate(summary["key_points"], 1):
        print(f"  {i}. {point}")

    print("\nItens de ação:")
    for action in summary["action_items"]:
        print(
            f"  • {action['description']}\n"
            f"    👤 Responsável: {action['owner']}\n"
            f"    📅 Data limite: {action['due_date']}"
        )


if __name__ == "__main__":
    main()

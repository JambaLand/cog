#!/usr/bin/env python3
"""Demo direto do sistema de notificações (sem dependências do Cog)."""

import sys
from pathlib import Path

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent))

from notifications import (
    NotificationManager,
    TeamsNotificationProvider,
    GoogleCalendarNotificationProvider,
)

# Dados de exemplo (similar ao que TLDVPredictor retornaria)
SAMPLE_SUMMARY = {
    "title": "Sprint Planning - Sprint 24",
    "summary": (
        "A equipe se reuniu para planejar o Sprint 24. "
        "Discutimos objetivos, capacidade e riscos. "
        "Todos os itens foram estimados e priorizados. "
        "O sprint terá 34 pontos de história."
    ),
    "meeting_id": "meeting_001",
    "key_points": [
        "Foco em performance e otimização",
        "Integração com API externa será primeira prioridade",
        "Testes de carga para 10k usuários simultâneos",
        "Code review obrigatório antes de merge",
        "Documentação técnica deve ser atualizada",
    ],
    "action_items": [
        {
            "description": "Preparar ambiente de staging",
            "owner": "Alice Silva",
            "due_date": "2026-03-07",
        },
        {
            "description": "Revisar especificação da API",
            "owner": "Bob Santos",
            "due_date": "2026-03-06",
        },
        {
            "description": "Setup de monitoramento",
            "owner": "Carol Johnson",
            "due_date": "2026-03-10",
        },
    ],
    "sentiment": "positive",
}


def main() -> None:
    """Demonstrar o sistema de notificações."""
    print("=" * 70)
    print("🔔 DEMO: SISTEMA DE NOTIFICAÇÕES TLDV")
    print("=" * 70)

    # 1. Inicializar gerenciador
    print("\n📌 Inicializando NotificationManager...")
    manager = NotificationManager()

    # 2. Verificar provedores configurados
    print(f"\n✅ Provedores encontrados: {manager.list_providers()}")
    print(f"   Notificações habilitadas: {manager.is_configured()}")

    # 3. Testar registros manuais (se necessário)
    print("\n📌 Registrando provedores manualmente...")

    teams_provider = TeamsNotificationProvider(
        webhook_url="https://outlook.webhook.office.com/webhookb2/xxx"
    )
    try:
        teams_provider.validate_config()
        manager.register_provider("teams_test", teams_provider)
        print("   ✅ Teams registrado")
    except ValueError as e:
        print(f"   ⚠️  Teams: {str(e)[:50]}...")

    google_provider = GoogleCalendarNotificationProvider(api_key="AIza_test_key")
    try:
        google_provider.validate_config()
        manager.register_provider("google_test", google_provider)
        print("   ✅ Google registrado")
    except ValueError as e:
        print(f"   ⚠️  Google: {str(e)[:50]}...")

    # 4. Exibir estrutura de dados
    print("\n" + "=" * 70)
    print("📋 DADOS DE EXEMPLO - Reunião para Notificação")
    print("=" * 70)

    print(f"\n📅 Título: {SAMPLE_SUMMARY['title']}")
    print(f"ID: {SAMPLE_SUMMARY['meeting_id']}")
    print(f"Sentimento: {SAMPLE_SUMMARY['sentiment'].upper()}")

    print(f"\n📝 Resumo:\n   {SAMPLE_SUMMARY['summary']}")

    print(f"\n🔑 Pontos-Chave ({len(SAMPLE_SUMMARY['key_points'])} itens):")
    for i, point in enumerate(SAMPLE_SUMMARY["key_points"], 1):
        print(f"   {i}. {point}")

    print(f"\n✅ Itens de Ação ({len(SAMPLE_SUMMARY['action_items'])} tarefas):")
    for action in SAMPLE_SUMMARY["action_items"]:
        print(f"   • {action['description']}")
        print(f"     👤 Responsável: {action['owner']}")
        print(f"     📅 Vencimento: {action['due_date']}")

    # 5. Demonstrar estrutura Teams (Adaptive Card)
    print("\n" + "=" * 70)
    print("📱 PREVIEW - Adaptive Card para Microsoft Teams")
    print("=" * 70)

    card = teams_provider._build_adaptive_card(SAMPLE_SUMMARY)
    print(f"\n✅ Tipo de Card: {card['type']}")
    print(f"   Attachments: {len(card['attachments'])}")

    content = card["attachments"][0]["content"]
    print(f"   Schema: {content.get('$schema', 'N/A')[-20:]}")
    print(f"   Versão: {content.get('version')}")
    print(f"   Containers: {len(content.get('body', []))}")

    print("\n📊 Estrutura do Card:")
    print("   ├─ Container: Cabeçalho (azul)")
    print("   ├─ Container: Título e participantes")
    print("   ├─ Container: Resumo")
    print("   ├─ Container: Pontos-chave")
    print("   └─ Container: Itens de ação")

    # 6. Demonstrar estrutura Google Calendar
    print("\n" + "=" * 70)
    print("🗓️  PREVIEW - Evento para Google Calendar")
    print("=" * 70)

    event = google_provider._build_calendar_event(SAMPLE_SUMMARY)
    print(f"\n✅ Título do Evento: {event['summary']}")
    print(f"   Visibilidade: {event['visibility']}")
    print(f"   Descrição: {len(event['description'])} caracteres")

    print("\n📄 Estrutura da Descrição:")
    print("   ├─ Título da reunião")
    print("   ├─ Resumo")
    print("   ├─ Pontos-Chave (até 5)")
    print("   └─ Itens de Ação (até 5)")

    # 7. Testar envio
    print("\n" + "=" * 70)
    print("🚀 TESTE DE ENVIO")
    print("=" * 70)

    results = manager.notify_meeting_summary(SAMPLE_SUMMARY)

    print(f"\n📊 Resultado de Envio:")
    total = len(results)
    successful = sum(1 for v in results.values() if v)

    if total == 0:
        print("   ℹ️  Nenhum provedor configurado")
        print("\n💡 Para configurar:")
        print("   export TEAMS_WEBHOOK_URL='https://outlook.webhook.office.com/...'")
        print("   export GOOGLE_API_KEY='AIza...'")
    else:
        for provider, success in results.items():
            status = "✅ ENVIADO" if success else "❌ FALHOU"
            print(f"   {status} - {provider.upper()}")
        print(f"\n   Total: {successful}/{total} bem-sucedidos")

    # 8. Resumo final
    print("\n" + "=" * 70)
    print("✨ DEMO COMPLETA")
    print("=" * 70)

    print("""
✅ O sistema está pronto para:
   1. Enviar resumos para Microsoft Teams
   2. Criar eventos no Google Calendar
   3. Suportar múltiplos provedores
   4. Extensível para novos canais

📖 Próximos passos:
   1. Configure TEAMS_WEBHOOK_URL e GOOGLE_API_KEY
   2. Execute: python examples/notify_teams.py
   3. Execute: python examples/notify_google.py
   4. Execute: python examples/notify_all.py

🔗 Documentação:
   • NOTIFICATIONS.md - Guia completo
   • README.md - Setup rápido
    """)


if __name__ == "__main__":
    main()

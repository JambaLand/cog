"""Exemplo 2: Obter resumo automático de uma reunião."""

import sys
from pathlib import Path

# Adicionar o diretório pai ao path para importar o predictor
sys.path.insert(0, str(Path(__file__).parent.parent))

from predict import TLDVPredictor


def main() -> None:
    """Exemplo de obtenção de resumo de reunião."""
    print("=" * 60)
    print("EXEMPLO 2: Obter Resumo de Reunião")
    print("=" * 60)

    # Inicializar o predictor
    predictor = TLDVPredictor()
    predictor.setup()

    # Primeiro, listar reuniões disponíveis
    print("\n📅 Buscando reuniões disponíveis...")
    meetings = predictor.get_meetings(limit=1)

    if not meetings:
        print("❌ Nenhuma reunião encontrada.")
        return

    meeting = meetings[0]
    meeting_id = meeting["id"]

    print(f"✅ Reunião encontrada: {meeting['title']}")
    print(f"   ID: {meeting_id}\n")

    # Obter resumo da reunião
    print("📝 Gerando resumo automático...")
    summary = predictor.get_meeting_summary(meeting_id)

    print(f"\n📌 RESUMO: {summary['title']}")
    print("-" * 60)
    print(f"\n{summary['summary']}\n")

    # Exibir pontos-chave
    print("🔑 PONTOS-CHAVE:")
    for i, point in enumerate(summary["key_points"], 1):
        print(f"   {i}. {point}")

    # Exibir itens de ação
    print("\n✅ ITENS DE AÇÃO:")
    for action in summary["action_items"]:
        print(f"   • {action['description']}")
        print(f"     Responsável: {action['owner']}")
        print(f"     Data limite: {action['due_date']}\n")

    # Exibir sentimento
    sentiment_emoji = "😊" if summary["sentiment"] == "positive" else "😐"
    print(f"{sentiment_emoji} SENTIMENTO: {summary['sentiment'].upper()}")


if __name__ == "__main__":
    main()

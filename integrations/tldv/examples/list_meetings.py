"""Exemplo 1: Listar reuniões gravadas no TLDV."""

import sys
from pathlib import Path

# Adicionar o diretório pai ao path para importar o predictor
sys.path.insert(0, str(Path(__file__).parent.parent))

from predict import TLDVPredictor


def main() -> None:
    """Exemplo de listagem de reuniões."""
    print("=" * 60)
    print("EXEMPLO 1: Listar Reuniões Gravadas")
    print("=" * 60)

    # Inicializar o predictor
    predictor = TLDVPredictor()
    predictor.setup()

    # Obter primeiras 5 reuniões
    print("\n📅 Buscando reuniões...")
    meetings = predictor.get_meetings(limit=5)

    if not meetings:
        print("❌ Nenhuma reunião encontrada.")
        return

    print(f"\n✅ Encontradas {len(meetings)} reuniões:\n")

    # Exibir informações de cada reunião
    for i, meeting in enumerate(meetings, 1):
        print(f"{i}. {meeting['title']}")
        print(f"   ID: {meeting['id']}")
        print(f"   Data: {meeting['date']}")
        print(f"   Duração: {meeting['duration_minutes']} minutos")
        print(f"   Participantes: {meeting['participants_count']}")
        print(f"   Status: {meeting['status']}")
        print()


if __name__ == "__main__":
    main()

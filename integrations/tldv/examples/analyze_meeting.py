"""Exemplo 3: Análise completa de uma reunião."""

import sys
import json
from pathlib import Path

# Adicionar o diretório pai ao path para importar o predictor
sys.path.insert(0, str(Path(__file__).parent.parent))

from predict import TLDVPredictor


def main() -> None:
    """Exemplo de análise completa de reunião."""
    print("=" * 60)
    print("EXEMPLO 3: Análise Completa de Reunião")
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

    print(f"✅ Reunião selecionada: {meeting['title']} ({meeting_id})\n")

    # Realizar análise completa
    print("🔍 Analisando reunião...")
    analysis = predictor.analyze_meeting(meeting_id)

    # 1. DETALHES BÁSICOS
    print("\n" + "=" * 60)
    print("1️⃣  DETALHES BÁSICOS")
    print("=" * 60)
    details = analysis["details"]
    print(f"Título: {details['title']}")
    print(f"Data: {details['date']}")
    print(f"Duração: {details['duration_minutes']} minutos")
    print(f"Total de participantes: {len(details['participants'])}")

    # 2. PARTICIPANTES
    print("\n" + "=" * 60)
    print("2️⃣  PARTICIPANTES E TEMPO DE FALA")
    print("=" * 60)
    for participant in analysis["participants"]:
        print(f"\n👤 {participant['name']} ({participant['role']})")
        print(f"   Email: {participant['email']}")
        print(f"   Tempo de fala: {participant['speaking_time_minutes']} min "
              f"({participant['speaking_percentage']:.1f}%)")
        print(f"   Interrupções: {participant['interruptions']}")

    # 3. RESUMO E AÇÕES
    print("\n" + "=" * 60)
    print("3️⃣  RESUMO E ITENS DE AÇÃO")
    print("=" * 60)
    summary = analysis["summary"]
    print(f"\n📝 Resumo:\n{summary['summary']}\n")

    print("✅ Itens de Ação:")
    for action in summary["action_items"]:
        print(f"   • {action['description']} (Responsável: {action['owner']})")

    # 4. TRANSCRIÇÃO (primeiras 3 linhas)
    print("\n" + "=" * 60)
    print("4️⃣  TRANSCRIÇÃO (amostra)")
    print("=" * 60)
    transcript = analysis["transcript"]
    print(f"\nIdioma: {transcript['language']}")
    print(f"Total de palavras: {transcript['word_count']}\n")

    print("Amostra da transcrição:")
    for entry in transcript["transcript"][:3]:
        print(f"\n[{entry['timestamp']}] {entry['speaker']}:")
        print(f"  {entry['text']}")

    # 5. EXPORTAR ANÁLISE
    print("\n" + "=" * 60)
    print("💾 EXPORTANDO ANÁLISE PARA JSON")
    print("=" * 60)

    output_file = f"analise_{meeting_id}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    print(f"✅ Análise exportada para: {output_file}")


if __name__ == "__main__":
    main()

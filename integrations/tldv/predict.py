"""Predictor do Cog para integração TLDV."""

from typing import Any, Dict, List, Optional

from cog import BasePredictor

from composio_tools import TLDVComposioTools
from config import TLDVConfig


class TLDVPredictor(BasePredictor):
    """Predictor para interagir com TLDV via Composio.

    Esta classe fornece métodos para acessar dados de reuniões,
    resumos, transcrições e análises usando a API TLDV.
    """

    def setup(self) -> None:
        """Inicializar o predictor."""
        self.config = TLDVConfig.from_env()
        self.tools = TLDVComposioTools(self.config)

    def get_meetings(
        self, limit: Optional[int] = None, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Obter lista de reuniões gravadas.

        Args:
            limit: Número máximo de reuniões a retornar (padrão: 50).
            offset: Número de reuniões a pular (padrão: 0).

        Returns:
            Lista de reuniões com metadados básicos.

        Example:
            >>> predictor = TLDVPredictor()
            >>> predictor.setup()
            >>> meetings = predictor.get_meetings(limit=10)
            >>> print(f"Encontradas {len(meetings)} reuniões")
        """
        return self.tools.get_meetings(limit=limit, offset=offset)

    def get_meeting_details(self, meeting_id: str) -> Dict[str, Any]:
        """Obter detalhes completos de uma reunião.

        Args:
            meeting_id: ID da reunião.

        Returns:
            Objeto com detalhes da reunião incluindo participantes e tags.

        Example:
            >>> details = predictor.get_meeting_details("meeting_001")
            >>> print(f"Reunião: {details['title']}")
            >>> print(f"Participantes: {len(details['participants'])}")
        """
        return self.tools.get_meeting_details(meeting_id)

    def get_meeting_summary(self, meeting_id: str) -> Dict[str, Any]:
        """Obter resumo automático de uma reunião.

        Args:
            meeting_id: ID da reunião.

        Returns:
            Objeto com resumo incluindo pontos-chave e itens de ação.

        Example:
            >>> summary = predictor.get_meeting_summary("meeting_001")
            >>> print("Resumo:", summary['summary'])
            >>> print("Ações:", summary['action_items'])
        """
        return self.tools.get_meeting_summary(meeting_id)

    def get_meeting_transcript(self, meeting_id: str) -> Dict[str, Any]:
        """Obter transcrição completa de uma reunião.

        Args:
            meeting_id: ID da reunião.

        Returns:
            Objeto com transcrição linha por linha com timestamps e falantes.

        Example:
            >>> transcript = predictor.get_meeting_transcript("meeting_001")
            >>> for line in transcript['transcript']:
            ...     print(f"{line['speaker']}: {line['text']}")
        """
        return self.tools.get_meeting_transcript(meeting_id)

    def get_meeting_participants(
        self, meeting_id: str
    ) -> List[Dict[str, Any]]:
        """Obter lista de participantes de uma reunião.

        Args:
            meeting_id: ID da reunião.

        Returns:
            Lista de participantes com tempo de fala e outras estatísticas.

        Example:
            >>> participants = predictor.get_meeting_participants("meeting_001")
            >>> for p in participants:
            ...     print(f"{p['name']}: {p['speaking_time_minutes']} min")
        """
        return self.tools.get_meeting_participants(meeting_id)

    def search_meetings(
        self, query: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Buscar reuniões por termo.

        Args:
            query: Termo de busca (título, conteúdo, etc).
            limit: Número máximo de resultados (padrão: 50).

        Returns:
            Lista de reuniões que correspondem ao termo de busca.

        Example:
            >>> results = predictor.search_meetings("sprint planning")
            >>> print(f"Encontradas {len(results)} reuniões")
        """
        return self.tools.search_meetings(query, limit=limit)

    def analyze_meeting(self, meeting_id: str) -> Dict[str, Any]:
        """Análise completa de uma reunião (resumo + transcrição + participantes).

        Args:
            meeting_id: ID da reunião.

        Returns:
            Objeto consolidado com análise completa.

        Example:
            >>> analysis = predictor.analyze_meeting("meeting_001")
            >>> print("Resumo:", analysis['summary']['summary'])
            >>> print("Sentimento:", analysis['summary']['sentiment'])
        """
        details = self.get_meeting_details(meeting_id)
        summary = self.get_meeting_summary(meeting_id)
        transcript = self.get_meeting_transcript(meeting_id)
        participants = self.get_meeting_participants(meeting_id)

        return {
            "meeting_id": meeting_id,
            "details": details,
            "summary": summary,
            "transcript": transcript,
            "participants": participants,
            "analysis_timestamp": "2026-03-05T10:30:00Z",
        }

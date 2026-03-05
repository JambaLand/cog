"""Integração com Composio para acesso à API TLDV."""

from typing import Any, Dict, List, Optional

from config import TLDVConfig


class TLDVComposioTools:
    """Ferramentas Composio para interagir com TLDV."""

    def __init__(self, config: Optional[TLDVConfig] = None) -> None:
        """Inicializar as ferramentas.

        Args:
            config: Configuração do TLDV. Se None, carrega das variáveis de ambiente.
        """
        self.config = config or TLDVConfig.from_env()
        self.api_key = self.config.API_KEY
        self.api_base_url = self.config.API_BASE_URL

    def get_available_tools(self) -> List[str]:
        """Retornar lista de ferramentas disponíveis.

        Returns:
            Lista de nomes de ferramentas.
        """
        return [
            "get_meetings",
            "get_meeting_details",
            "get_meeting_summary",
            "get_meeting_transcript",
            "get_meeting_participants",
            "search_meetings",
        ]

    def get_meetings(
        self, limit: Optional[int] = None, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Obter lista de reuniões gravadas.

        Args:
            limit: Número máximo de reuniões a retornar.
            offset: Número de reuniões a pular.

        Returns:
            Lista de reuniões com metadados.
        """
        limit = limit or self.config.MAX_MEETINGS

        # Simulação de resposta da API TLDV
        # Em produção, isso faria uma chamada real via Composio
        mock_meetings = [
            {
                "id": "meeting_001",
                "title": "Sprint Planning",
                "date": "2026-03-05T09:00:00Z",
                "duration_minutes": 45,
                "participants_count": 5,
                "status": "completed",
                "transcript_available": True,
                "summary_available": True,
            },
            {
                "id": "meeting_002",
                "title": "Client Feedback Session",
                "date": "2026-03-04T14:00:00Z",
                "duration_minutes": 30,
                "participants_count": 3,
                "status": "completed",
                "transcript_available": True,
                "summary_available": True,
            },
            {
                "id": "meeting_003",
                "title": "Team Retrospective",
                "date": "2026-03-03T16:00:00Z",
                "duration_minutes": 60,
                "participants_count": 8,
                "status": "completed",
                "transcript_available": True,
                "summary_available": True,
            },
        ]

        return mock_meetings[offset : offset + limit]

    def get_meeting_details(self, meeting_id: str) -> Dict[str, Any]:
        """Obter detalhes completos de uma reunião.

        Args:
            meeting_id: ID da reunião.

        Returns:
            Detalhes da reunião.
        """
        # Simulação de resposta da API
        return {
            "id": meeting_id,
            "title": "Sprint Planning",
            "date": "2026-03-05T09:00:00Z",
            "duration_minutes": 45,
            "participants": [
                {
                    "name": "Alice",
                    "email": "alice@example.com",
                    "time_spoken_minutes": 15,
                },
                {
                    "name": "Bob",
                    "email": "bob@example.com",
                    "time_spoken_minutes": 20,
                },
                {
                    "name": "Charlie",
                    "email": "charlie@example.com",
                    "time_spoken_minutes": 10,
                },
            ],
            "tags": ["planning", "sprint", "engineering"],
            "status": "completed",
        }

    def get_meeting_summary(self, meeting_id: str) -> Dict[str, Any]:
        """Obter resumo automático de uma reunião.

        Args:
            meeting_id: ID da reunião.

        Returns:
            Resumo da reunião incluindo pontos-chave e ações.
        """
        # Simulação de resposta da API
        return {
            "meeting_id": meeting_id,
            "title": "Sprint Planning",
            "summary": (
                "A equipe se reuniu para planejar o próximo sprint. "
                "Foram discutidas 12 histórias de usuário, estimadas em 34 pontos. "
                "Prioridades definiram: melhorias de performance (8 pts), "
                "novos recursos (18 pts), correção de bugs (8 pts)."
            ),
            "key_points": [
                "Foco em melhorias de performance para Q1",
                "Integração com API externa iniciará semana que vem",
                "Testes de carga agendados para segunda-feira",
            ],
            "action_items": [
                {
                    "description": "Preparar ambiente de testes",
                    "owner": "Alice",
                    "due_date": "2026-03-07",
                },
                {
                    "description": "Revisar especificação da API",
                    "owner": "Bob",
                    "due_date": "2026-03-06",
                },
                {
                    "description": "Atualizar documentação",
                    "owner": "Charlie",
                    "due_date": "2026-03-08",
                },
            ],
            "sentiment": "positive",
            "generated_at": "2026-03-05T10:30:00Z",
        }

    def get_meeting_transcript(self, meeting_id: str) -> Dict[str, Any]:
        """Obter transcrição completa da reunião.

        Args:
            meeting_id: ID da reunião.

        Returns:
            Transcrição com timestamps e falantes.
        """
        # Simulação de resposta da API
        return {
            "meeting_id": meeting_id,
            "title": "Sprint Planning",
            "language": "pt-BR",
            "transcript": [
                {
                    "timestamp": "00:00:00",
                    "speaker": "Alice",
                    "text": "Bom dia pessoal! Vamos começar o planejamento do sprint.",
                },
                {
                    "timestamp": "00:15:30",
                    "speaker": "Bob",
                    "text": "Acho que devemos focar em performance este sprint.",
                },
                {
                    "timestamp": "00:28:45",
                    "speaker": "Charlie",
                    "text": "Concordo! Vou atualizar a documentação depois.",
                },
            ],
            "word_count": 2456,
            "duration_minutes": 45,
        }

    def get_meeting_participants(self, meeting_id: str) -> List[Dict[str, Any]]:
        """Obter lista de participantes de uma reunião.

        Args:
            meeting_id: ID da reunião.

        Returns:
            Lista de participantes com estatísticas.
        """
        # Simulação de resposta da API
        return [
            {
                "name": "Alice",
                "email": "alice@example.com",
                "role": "Tech Lead",
                "speaking_time_minutes": 15,
                "speaking_percentage": 33.3,
                "interruptions": 2,
            },
            {
                "name": "Bob",
                "email": "bob@example.com",
                "role": "Developer",
                "speaking_time_minutes": 20,
                "speaking_percentage": 44.4,
                "interruptions": 1,
            },
            {
                "name": "Charlie",
                "email": "charlie@example.com",
                "role": "QA",
                "speaking_time_minutes": 10,
                "speaking_percentage": 22.2,
                "interruptions": 0,
            },
        ]

    def search_meetings(self, query: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Buscar reuniões por termo.

        Args:
            query: Termo de busca (título, conteúdo, etc).
            limit: Número máximo de resultados.

        Returns:
            Lista de reuniões que correspondem à busca.
        """
        limit = limit or self.config.MAX_MEETINGS

        # Simulação de busca
        all_meetings = self.get_meetings(limit=100)
        filtered = [
            m
            for m in all_meetings
            if query.lower() in m["title"].lower()
        ]

        return filtered[:limit]

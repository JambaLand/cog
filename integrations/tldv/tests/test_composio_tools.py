"""Testes para módulo de ferramentas Composio."""

from typing import Any, Dict, List

import pytest

from composio_tools import TLDVComposioTools
from config import TLDVConfig


@pytest.fixture
def config() -> TLDVConfig:
    """Criar configuração para testes."""
    return TLDVConfig.from_env()


@pytest.fixture
def tools(config: TLDVConfig) -> TLDVComposioTools:
    """Criar instância de ferramentas para testes."""
    return TLDVComposioTools(config)


class TestTLDVComposioTools:
    """Testes para TLDVComposioTools."""

    def test_initialization(self, tools: TLDVComposioTools) -> None:
        """Testar inicialização das ferramentas."""
        assert tools.config is not None
        assert tools.api_key is not None
        assert tools.api_base_url == "https://api.tldv.io/v1"

    def test_get_available_tools(self, tools: TLDVComposioTools) -> None:
        """Testar listagem de ferramentas disponíveis."""
        available_tools = tools.get_available_tools()

        assert isinstance(available_tools, list)
        assert "get_meetings" in available_tools
        assert "get_meeting_summary" in available_tools
        assert "get_meeting_transcript" in available_tools
        assert "get_meeting_participants" in available_tools
        assert "search_meetings" in available_tools
        assert len(available_tools) == 6

    def test_get_meetings_default(self, tools: TLDVComposioTools) -> None:
        """Testar obtenção de reuniões com parâmetros padrão."""
        meetings = tools.get_meetings()

        assert isinstance(meetings, list)
        assert len(meetings) > 0
        assert all("id" in m for m in meetings)
        assert all("title" in m for m in meetings)
        assert all("date" in m for m in meetings)

    def test_get_meetings_with_limit(
        self, tools: TLDVComposioTools
    ) -> None:
        """Testar obtenção de reuniões com limite."""
        meetings = tools.get_meetings(limit=2)

        assert len(meetings) == 2

    def test_get_meetings_with_offset(
        self, tools: TLDVComposioTools
    ) -> None:
        """Testar obtenção de reuniões com offset."""
        all_meetings = tools.get_meetings(limit=10)
        offset_meetings = tools.get_meetings(limit=2, offset=1)

        # O segundo elemento deve ser o primeiro do offset
        assert all_meetings[1]["id"] == offset_meetings[0]["id"]

    def test_get_meetings_structure(self, tools: TLDVComposioTools) -> None:
        """Testar estrutura de dados da reunião."""
        meetings = tools.get_meetings(limit=1)

        meeting = meetings[0]
        required_fields = [
            "id",
            "title",
            "date",
            "duration_minutes",
            "participants_count",
            "status",
            "transcript_available",
            "summary_available",
        ]

        for field in required_fields:
            assert field in meeting

    def test_get_meeting_details(self, tools: TLDVComposioTools) -> None:
        """Testar obtenção de detalhes de reunião."""
        details = tools.get_meeting_details("meeting_001")

        assert details["id"] == "meeting_001"
        assert "title" in details
        assert "participants" in details
        assert "tags" in details
        assert isinstance(details["participants"], list)
        assert len(details["participants"]) > 0

    def test_get_meeting_summary(self, tools: TLDVComposioTools) -> None:
        """Testar obtenção de resumo de reunião."""
        summary = tools.get_meeting_summary("meeting_001")

        assert summary["meeting_id"] == "meeting_001"
        assert "summary" in summary
        assert "key_points" in summary
        assert "action_items" in summary
        assert "sentiment" in summary
        assert isinstance(summary["key_points"], list)
        assert isinstance(summary["action_items"], list)

    def test_get_meeting_summary_structure(
        self, tools: TLDVComposioTools
    ) -> None:
        """Testar estrutura de resumo de reunião."""
        summary = tools.get_meeting_summary("meeting_001")

        # Verificar ação
        action = summary["action_items"][0]
        assert "description" in action
        assert "owner" in action
        assert "due_date" in action

    def test_get_meeting_transcript(
        self, tools: TLDVComposioTools
    ) -> None:
        """Testar obtenção de transcrição."""
        transcript = tools.get_meeting_transcript("meeting_001")

        assert transcript["meeting_id"] == "meeting_001"
        assert "transcript" in transcript
        assert "language" in transcript
        assert isinstance(transcript["transcript"], list)
        assert len(transcript["transcript"]) > 0

    def test_get_meeting_transcript_structure(
        self, tools: TLDVComposioTools
    ) -> None:
        """Testar estrutura de transcrição."""
        transcript = tools.get_meeting_transcript("meeting_001")

        # Verificar linha de transcrição
        line = transcript["transcript"][0]
        assert "timestamp" in line
        assert "speaker" in line
        assert "text" in line

    def test_get_meeting_participants(
        self, tools: TLDVComposioTools
    ) -> None:
        """Testar obtenção de participantes."""
        participants = tools.get_meeting_participants("meeting_001")

        assert isinstance(participants, list)
        assert len(participants) > 0
        assert all("name" in p for p in participants)
        assert all("email" in p for p in participants)

    def test_get_meeting_participants_structure(
        self, tools: TLDVComposioTools
    ) -> None:
        """Testar estrutura de participante."""
        participants = tools.get_meeting_participants("meeting_001")

        participant = participants[0]
        required_fields = [
            "name",
            "email",
            "role",
            "speaking_time_minutes",
            "speaking_percentage",
            "interruptions",
        ]

        for field in required_fields:
            assert field in participant

    def test_search_meetings_basic(self, tools: TLDVComposioTools) -> None:
        """Testar busca de reuniões."""
        results = tools.search_meetings("sprint")

        assert isinstance(results, list)

    def test_search_meetings_with_limit(
        self, tools: TLDVComposioTools
    ) -> None:
        """Testar busca de reuniões com limite."""
        results = tools.search_meetings("sprint", limit=1)

        assert len(results) <= 1

    def test_search_meetings_case_insensitive(
        self, tools: TLDVComposioTools
    ) -> None:
        """Testar que busca é insensível a maiúsculas."""
        lower_results = tools.search_meetings("sprint")
        upper_results = tools.search_meetings("SPRINT")

        assert len(lower_results) == len(upper_results)

    def test_search_meetings_returns_dict_list(
        self, tools: TLDVComposioTools
    ) -> None:
        """Testar que busca retorna lista de dicionários."""
        results = tools.search_meetings("sprint")

        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], dict)

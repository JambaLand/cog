"""Testes para módulo de notificações."""

from typing import Any, Dict

import pytest

from notifications import (
    GoogleCalendarNotificationProvider,
    NotificationManager,
    TeamsNotificationProvider,
)


@pytest.fixture
def teams_webhook() -> str:
    """Fornecer webhook do Teams para testes."""
    return "https://outlook.webhook.office.com/webhook/test"


@pytest.fixture
def google_api_key() -> str:
    """Fornecer chave de API do Google para testes."""
    return "test-api-key-12345"


@pytest.fixture
def sample_message() -> Dict[str, Any]:
    """Fornecer mensagem de exemplo para testes."""
    return {
        "title": "Sprint Planning",
        "summary": "A equipe planejou o próximo sprint com 34 pontos.",
        "meeting_id": "meeting_001",
        "participants_count": 5,
        "key_points": [
            "Foco em performance",
            "Integração com API",
            "Testes de carga",
        ],
        "action_items": [
            {
                "description": "Preparar ambiente",
                "owner": "Alice",
                "due_date": "2026-03-07",
            },
            {
                "description": "Revisar spec",
                "owner": "Bob",
                "due_date": "2026-03-06",
            },
        ],
    }


class TestTeamsNotificationProvider:
    """Testes para TeamsNotificationProvider."""

    def test_initialization(self, teams_webhook: str) -> None:
        """Testar inicialização do Teams."""
        provider = TeamsNotificationProvider(webhook_url=teams_webhook)
        assert provider.webhook_url == teams_webhook

    def test_initialization_from_env(
        self, teams_webhook: str, monkeypatch: Any
    ) -> None:
        """Testar inicialização a partir de variável de ambiente."""
        monkeypatch.setenv("TEAMS_WEBHOOK_URL", teams_webhook)
        provider = TeamsNotificationProvider()
        assert provider.webhook_url == teams_webhook

    def test_validate_config_success(self, teams_webhook: str) -> None:
        """Testar validação bem-sucedida."""
        provider = TeamsNotificationProvider(webhook_url=teams_webhook)
        assert provider.validate_config() is True

    def test_validate_config_missing_url(self) -> None:
        """Testar validação com URL ausente."""
        provider = TeamsNotificationProvider(webhook_url="")

        with pytest.raises(ValueError, match="TEAMS_WEBHOOK_URL"):
            provider.validate_config()

    def test_validate_config_invalid_url(self) -> None:
        """Testar validação com URL inválida."""
        provider = TeamsNotificationProvider(
            webhook_url="http://example.com"
        )

        with pytest.raises(ValueError, match="HTTPS"):
            provider.validate_config()

    def test_build_adaptive_card(
        self, teams_webhook: str, sample_message: Dict[str, Any]
    ) -> None:
        """Testar construção de Adaptive Card."""
        provider = TeamsNotificationProvider(webhook_url=teams_webhook)
        card = provider._build_adaptive_card(sample_message)

        assert "type" in card
        assert card["type"] == "message"
        assert "attachments" in card
        assert len(card["attachments"]) > 0

    def test_adaptive_card_structure(
        self, teams_webhook: str, sample_message: Dict[str, Any]
    ) -> None:
        """Testar estrutura do Adaptive Card."""
        provider = TeamsNotificationProvider(webhook_url=teams_webhook)
        card = provider._build_adaptive_card(sample_message)

        attachment = card["attachments"][0]
        assert attachment["contentType"] == (
            "application/vnd.microsoft.card.adaptive"
        )

        content = attachment["content"]
        assert content["type"] == "AdaptiveCard"
        assert "body" in content


class TestGoogleCalendarNotificationProvider:
    """Testes para GoogleCalendarNotificationProvider."""

    def test_initialization(self, google_api_key: str) -> None:
        """Testar inicialização do Google."""
        provider = GoogleCalendarNotificationProvider(api_key=google_api_key)
        assert provider.api_key == google_api_key

    def test_initialization_from_env(
        self, google_api_key: str, monkeypatch: Any
    ) -> None:
        """Testar inicialização a partir de variável de ambiente."""
        monkeypatch.setenv("GOOGLE_API_KEY", google_api_key)
        provider = GoogleCalendarNotificationProvider()
        assert provider.api_key == google_api_key

    def test_validate_config_success(self, google_api_key: str) -> None:
        """Testar validação bem-sucedida."""
        provider = GoogleCalendarNotificationProvider(api_key=google_api_key)
        assert provider.validate_config() is True

    def test_validate_config_missing_key(self) -> None:
        """Testar validação com chave ausente."""
        provider = GoogleCalendarNotificationProvider(api_key="")

        with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
            provider.validate_config()

    def test_calendar_id_default(self, google_api_key: str) -> None:
        """Testar calendar_id padrão."""
        provider = GoogleCalendarNotificationProvider(api_key=google_api_key)
        assert provider.calendar_id == "primary"

    def test_calendar_id_from_env(
        self, google_api_key: str, monkeypatch: Any
    ) -> None:
        """Testar calendar_id de variável de ambiente."""
        custom_calendar_id = "user@gmail.com"
        monkeypatch.setenv("GOOGLE_CALENDAR_ID", custom_calendar_id)

        provider = GoogleCalendarNotificationProvider(api_key=google_api_key)
        assert provider.calendar_id == custom_calendar_id

    def test_build_calendar_event(
        self, google_api_key: str, sample_message: Dict[str, Any]
    ) -> None:
        """Testar construção de evento do Google Calendar."""
        provider = GoogleCalendarNotificationProvider(api_key=google_api_key)
        event = provider._build_calendar_event(sample_message)

        assert "summary" in event
        assert "description" in event
        assert "visibility" in event
        assert event["visibility"] == "public"

    def test_calendar_event_contains_key_points(
        self, google_api_key: str, sample_message: Dict[str, Any]
    ) -> None:
        """Testar que evento contém pontos-chave."""
        provider = GoogleCalendarNotificationProvider(api_key=google_api_key)
        event = provider._build_calendar_event(sample_message)

        description = event["description"]
        for point in sample_message["key_points"]:
            assert point in description


class TestNotificationManager:
    """Testes para NotificationManager."""

    def test_initialization(self) -> None:
        """Testar inicialização do gerenciador."""
        manager = NotificationManager()
        assert isinstance(manager.providers, dict)

    def test_register_provider(
        self, teams_webhook: str
    ) -> None:
        """Testar registro de provedor."""
        manager = NotificationManager()
        provider = TeamsNotificationProvider(webhook_url=teams_webhook)

        manager.register_provider("teams", provider)

        assert "teams" in manager.providers
        assert manager.providers["teams"] == provider

    def test_register_invalid_provider(self) -> None:
        """Testar registro de provedor inválido."""
        manager = NotificationManager()
        provider = TeamsNotificationProvider(webhook_url="")

        # Não deve falhar, mas registrará com aviso
        manager.register_provider("teams", provider)

    def test_get_provider(self, teams_webhook: str) -> None:
        """Testar obtenção de provedor."""
        manager = NotificationManager()
        provider = TeamsNotificationProvider(webhook_url=teams_webhook)
        manager.register_provider("teams", provider)

        retrieved = manager.get_provider("teams")
        assert retrieved is not None
        assert retrieved == provider

    def test_get_nonexistent_provider(self) -> None:
        """Testar obtenção de provedor não existente."""
        manager = NotificationManager()
        result = manager.get_provider("nonexistent")
        assert result is None

    def test_list_providers(
        self, teams_webhook: str, google_api_key: str
    ) -> None:
        """Testar listagem de provedores."""
        manager = NotificationManager()

        teams_provider = TeamsNotificationProvider(webhook_url=teams_webhook)
        google_provider = GoogleCalendarNotificationProvider(
            api_key=google_api_key
        )

        manager.register_provider("teams", teams_provider)
        manager.register_provider("google", google_provider)

        providers = manager.list_providers()

        assert "teams" in providers
        assert "google" in providers
        assert len(providers) == 2

    def test_is_configured_true(self, teams_webhook: str) -> None:
        """Testar is_configured quando configurado."""
        manager = NotificationManager()
        provider = TeamsNotificationProvider(webhook_url=teams_webhook)

        assert manager.is_configured() is False
        manager.register_provider("teams", provider)
        assert manager.is_configured() is True

    def test_is_configured_false(self) -> None:
        """Testar is_configured quando não configurado."""
        manager = NotificationManager()
        assert manager.is_configured() is False

    def test_notify_meeting_summary(
        self, teams_webhook: str, sample_message: Dict[str, Any]
    ) -> None:
        """Testar notify_meeting_summary."""
        manager = NotificationManager()
        provider = TeamsNotificationProvider(webhook_url=teams_webhook)
        manager.register_provider("teams", provider)

        # Note: Isso tenta fazer uma requisição real, então pode falhar
        # Em um cenário real, usaríamos mock
        results = manager.notify_meeting_summary(sample_message)

        assert isinstance(results, dict)

    def test_notify_returns_dict(
        self, teams_webhook: str, sample_message: Dict[str, Any]
    ) -> None:
        """Testar que notify retorna dicionário."""
        manager = NotificationManager()
        provider = TeamsNotificationProvider(webhook_url=teams_webhook)
        manager.register_provider("teams", provider)

        results = manager.notify(sample_message)

        assert isinstance(results, dict)
        assert "teams" in results

    def test_multiple_providers(
        self, teams_webhook: str, google_api_key: str
    ) -> None:
        """Testar múltiplos provedores."""
        manager = NotificationManager()

        teams_provider = TeamsNotificationProvider(webhook_url=teams_webhook)
        google_provider = GoogleCalendarNotificationProvider(
            api_key=google_api_key
        )

        manager.register_provider("teams", teams_provider)
        manager.register_provider("google", google_provider)

        assert len(manager.list_providers()) == 2
        assert manager.is_configured() is True

"""Sistema de notificações para integração TLDV.

Permite enviar notificações de reuniões para diversos canais:
- Microsoft Teams (via webhooks)
- Google Meet/Calendar (via API)
- Email (futuro)
"""

import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import requests


class NotificationProvider(ABC):
    """Interface base para provedores de notificação."""

    @abstractmethod
    def send(self, message: Dict[str, Any]) -> bool:
        """Enviar notificação.

        Args:
            message: Dicionário com dados da mensagem.

        Returns:
            True se enviado com sucesso, False caso contrário.
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validar se a configuração está completa.

        Returns:
            True se configurado corretamente, False caso contrário.

        Raises:
            ValueError: Se configuração estiver inválida.
        """
        pass


class TeamsNotificationProvider(NotificationProvider):
    """Provedor de notificações para Microsoft Teams via webhooks."""

    def __init__(self, webhook_url: Optional[str] = None) -> None:
        """Inicializar provedor Teams.

        Args:
            webhook_url: URL do webhook do Teams.
                        Se None, obtém de TEAMS_WEBHOOK_URL.
        """
        self.webhook_url = (
            webhook_url or os.getenv("TEAMS_WEBHOOK_URL", "")
        )

    def validate_config(self) -> bool:
        """Validar configuração do Teams."""
        if not self.webhook_url:
            raise ValueError(
                "TEAMS_WEBHOOK_URL não configurada. "
                "Configure a variável de ambiente ou passe na inicialização."
            )
        if not self.webhook_url.startswith("https://"):
            raise ValueError(
                "TEAMS_WEBHOOK_URL inválida. Deve ser HTTPS."
            )
        return True

    def send(self, message: Dict[str, Any]) -> bool:
        """Enviar notificação para Teams.

        Args:
            message: Dicionário com:
                - title: Título da mensagem
                - summary: Resumo da reunião
                - meeting_id: ID da reunião
                - participants_count: Número de participantes
                - key_points: Pontos-chave
                - action_items: Itens de ação

        Returns:
            True se enviado com sucesso.
        """
        self.validate_config()

        # Construir payload do Teams (formato Adaptive Card)
        payload = self._build_adaptive_card(message)

        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"❌ Erro ao enviar para Teams: {e}")
            return False

    def _build_adaptive_card(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Construir Adaptive Card para Teams.

        Args:
            message: Dados da mensagem.

        Returns:
            Payload no formato Adaptive Card.
        """
        key_points = message.get("key_points", [])
        action_items = message.get("action_items", [])

        # Construir lista de pontos-chave
        key_points_text = "\n".join(
            [f"• {point}" for point in key_points[:5]]
        )

        # Construir lista de ações
        actions_text = "\n".join(
            [
                f"• {item.get('description', 'N/A')} "
                f"(Responsável: {item.get('owner', 'N/A')})"
                for item in action_items[:5]
            ]
        )

        return {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": {
                        "$schema": (
                            "http://adaptivecards.io/schemas/adaptive-card.json"
                        ),
                        "type": "AdaptiveCard",
                        "version": "1.4",
                        "body": [
                            {
                                "type": "Container",
                                "style": "accent",
                                "items": [
                                    {
                                        "type": "ColumnSet",
                                        "columns": [
                                            {
                                                "width": "stretch",
                                                "items": [
                                                    {
                                                        "type": "TextBlock",
                                                        "text": "📅 Resumo de Reunião",
                                                        "weight": "bolder",
                                                        "size": "large",
                                                        "color": "light",
                                                    }
                                                ],
                                            }
                                        ],
                                    }
                                ],
                            },
                            {
                                "type": "Container",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": f"**{message.get('title', 'Reunião')}**",
                                        "size": "large",
                                        "weight": "bolder",
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": (
                                            f"👥 {message.get('participants_count', 0)} participantes"
                                        ),
                                        "spacing": "small",
                                        "color": "good",
                                    },
                                ],
                            },
                            {
                                "type": "Container",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": "📝 Resumo",
                                        "weight": "bolder",
                                        "size": "medium",
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": message.get("summary", ""),
                                        "wrap": True,
                                        "spacing": "small",
                                    },
                                ],
                            },
                            {
                                "type": "Container",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": "🔑 Pontos-Chave",
                                        "weight": "bolder",
                                        "size": "medium",
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": key_points_text,
                                        "wrap": True,
                                        "spacing": "small",
                                    },
                                ],
                            },
                            {
                                "type": "Container",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": "✅ Itens de Ação",
                                        "weight": "bolder",
                                        "size": "medium",
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": actions_text,
                                        "wrap": True,
                                        "spacing": "small",
                                    },
                                ],
                            },
                        ],
                    },
                }
            ],
        }


class GoogleCalendarNotificationProvider(NotificationProvider):
    """Provedor de notificações para Google Calendar."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Inicializar provedor Google Calendar.

        Args:
            api_key: Chave de API do Google.
                     Se None, obtém de GOOGLE_API_KEY.
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY", "")
        self.calendar_id = os.getenv(
            "GOOGLE_CALENDAR_ID", "primary"
        )
        self.base_url = "https://www.googleapis.com/calendar/v3"

    def validate_config(self) -> bool:
        """Validar configuração do Google."""
        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY não configurada. "
                "Configure a variável de ambiente ou passe na inicialização."
            )
        return True

    def send(self, message: Dict[str, Any]) -> bool:
        """Enviar notificação via Google Calendar.

        Args:
            message: Dicionário com:
                - title: Título do evento
                - summary: Descrição
                - meeting_id: ID da reunião
                - date: Data do evento

        Returns:
            True se criado com sucesso.
        """
        self.validate_config()

        event = self._build_calendar_event(message)

        try:
            url = (
                f"{self.base_url}/calendars/{self.calendar_id}/"
                f"events?key={self.api_key}"
            )
            response = requests.post(
                url,
                json=event,
                timeout=10,
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"❌ Erro ao criar evento no Google Calendar: {e}")
            return False

    def _build_calendar_event(
        self, message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Construir evento do Google Calendar.

        Args:
            message: Dados da mensagem.

        Returns:
            Payload do evento.
        """
        summary = message.get("summary", "")
        key_points = message.get("key_points", [])
        action_items = message.get("action_items", [])

        description = f"""
{message.get("title", "Reunião")}

📝 Resumo:
{summary}

🔑 Pontos-Chave:
{chr(10).join(f"• {p}" for p in key_points)}

✅ Itens de Ação:
{chr(10).join(f"• {a.get('description', 'N/A')}" for a in action_items)}
        """.strip()

        return {
            "summary": f"📅 {message.get('title', 'Reunião')}",
            "description": description,
            "visibility": "public",
        }


class NotificationManager:
    """Gerenciador centralizado de notificações."""

    def __init__(self) -> None:
        """Inicializar gerenciador de notificações."""
        self.providers: Dict[str, NotificationProvider] = {}
        self._register_default_providers()

    def _register_default_providers(self) -> None:
        """Registrar provedores padrão."""
        # Teams
        if os.getenv("TEAMS_WEBHOOK_URL"):
            self.providers["teams"] = TeamsNotificationProvider()

        # Google Calendar
        if os.getenv("GOOGLE_API_KEY"):
            self.providers["google"] = GoogleCalendarNotificationProvider()

    def register_provider(
        self, name: str, provider: NotificationProvider
    ) -> None:
        """Registrar um novo provedor.

        Args:
            name: Nome do provedor (e.g., 'teams', 'google').
            provider: Instância do provedor.
        """
        try:
            provider.validate_config()
            self.providers[name] = provider
            print(f"✅ Provedor '{name}' registrado com sucesso")
        except ValueError as e:
            print(f"⚠️  Provedor '{name}' não pôde ser registrado: {e}")

    def get_provider(self, name: str) -> Optional[NotificationProvider]:
        """Obter um provedor específico.

        Args:
            name: Nome do provedor.

        Returns:
            Provedor ou None se não encontrado.
        """
        return self.providers.get(name)

    def notify(self, message: Dict[str, Any]) -> Dict[str, bool]:
        """Enviar notificação para todos os provedores registrados.

        Args:
            message: Dados da notificação.

        Returns:
            Dicionário com status de cada provedor.
        """
        results = {}

        for name, provider in self.providers.items():
            try:
                results[name] = provider.send(message)
            except Exception as e:
                print(f"❌ Erro ao enviar para {name}: {e}")
                results[name] = False

        return results

    def notify_meeting_summary(
        self, summary_data: Dict[str, Any]
    ) -> Dict[str, bool]:
        """Enviar notificação de resumo de reunião.

        Args:
            summary_data: Dados do resumo (retorno de get_meeting_summary).

        Returns:
            Status de envio para cada provedor.
        """
        message = {
            "title": summary_data.get("title", "Reunião"),
            "summary": summary_data.get("summary", ""),
            "meeting_id": summary_data.get("meeting_id", ""),
            "key_points": summary_data.get("key_points", []),
            "action_items": summary_data.get("action_items", []),
            "participants_count": len(
                summary_data.get("action_items", [])
            ),
        }

        return self.notify(message)

    def list_providers(self) -> list:
        """Listar provedores registrados.

        Returns:
            Lista de nomes dos provedores.
        """
        return list(self.providers.keys())

    def is_configured(self) -> bool:
        """Verificar se há algum provedor configurado.

        Returns:
            True se há pelo menos um provedor.
        """
        return len(self.providers) > 0

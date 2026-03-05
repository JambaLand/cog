"""Testes para módulo de configuração TLDV."""

import os
from typing import Any

import pytest

from config import TLDVConfig


class TestTLDVConfig:
    """Testes para TLDVConfig."""

    def test_default_config(self) -> None:
        """Testar configuração com valores padrão."""
        config = TLDVConfig()

        assert config.API_KEY == "b1116307-392b-4f4c-934c-bc4607338133"
        assert config.API_BASE_URL == "https://api.tldv.io/v1"
        assert config.REQUEST_TIMEOUT == 30
        assert config.MAX_MEETINGS == 50
        assert config.COMPOSIO_API_KEY is None

    def test_config_from_environment(self, monkeypatch: Any) -> None:
        """Testar carregamento de configuração de variáveis de ambiente."""
        monkeypatch.setenv("TLDV_API_KEY", "test-key-123")
        monkeypatch.setenv("TLDV_REQUEST_TIMEOUT", "60")
        monkeypatch.setenv("TLDV_MAX_MEETINGS", "100")

        # Precisamos recarregar a classe para pegar as novas variáveis
        config = TLDVConfig.from_env()

        assert config.API_KEY == "test-key-123"
        assert config.REQUEST_TIMEOUT == 60
        assert config.MAX_MEETINGS == 100

    def test_config_validation_success(self) -> None:
        """Testar validação bem-sucedida."""
        assert TLDVConfig.validate() is True

    def test_config_validation_with_missing_key(
        self, monkeypatch: Any
    ) -> None:
        """Testar validação com chave ausente."""
        monkeypatch.setenv("TLDV_API_KEY", "")
        TLDVConfig.API_KEY = ""

        with pytest.raises(ValueError, match="TLDV_API_KEY não configurada"):
            TLDVConfig.validate()

    def test_config_timeout_conversion(self, monkeypatch: Any) -> None:
        """Testar conversão de timeout para inteiro."""
        monkeypatch.setenv("TLDV_REQUEST_TIMEOUT", "45")

        config = TLDVConfig.from_env()
        assert isinstance(config.REQUEST_TIMEOUT, int)
        assert config.REQUEST_TIMEOUT == 45

    def test_config_max_meetings_conversion(self, monkeypatch: Any) -> None:
        """Testar conversão de max_meetings para inteiro."""
        monkeypatch.setenv("TLDV_MAX_MEETINGS", "25")

        config = TLDVConfig.from_env()
        assert isinstance(config.MAX_MEETINGS, int)
        assert config.MAX_MEETINGS == 25

    def test_config_composio_api_key_optional(self) -> None:
        """Testar que COMPOSIO_API_KEY é opcional."""
        config = TLDVConfig()
        assert config.COMPOSIO_API_KEY is None

    def test_config_composio_api_key_from_env(
        self, monkeypatch: Any
    ) -> None:
        """Testar COMPOSIO_API_KEY de variável de ambiente."""
        monkeypatch.setenv("COMPOSIO_API_KEY", "composio-key-456")

        config = TLDVConfig.from_env()
        assert config.COMPOSIO_API_KEY == "composio-key-456"

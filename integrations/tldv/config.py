"""Configuração para integração TLDV com Composio."""

import os
from typing import Optional


class TLDVConfig:
    """Configuração centralizada para a integração TLDV."""

    # Chave de API do TLDV
    API_KEY: str = os.getenv(
        "TLDV_API_KEY", "47319d54-86f2-4916-b47a-630138c9d235"
    )

    # URL base da API
    API_BASE_URL: str = os.getenv(
        "TLDV_API_BASE_URL", "https://api.tldv.io/v1"
    )

    # Timeout para requisições
    REQUEST_TIMEOUT: int = int(os.getenv("TLDV_REQUEST_TIMEOUT", "30"))

    # Número máximo de reuniões a retornar por padrão
    MAX_MEETINGS: int = int(os.getenv("TLDV_MAX_MEETINGS", "50"))

    # Composio API Key (opcional)
    COMPOSIO_API_KEY: Optional[str] = os.getenv("COMPOSIO_API_KEY")

    @classmethod
    def validate(cls) -> bool:
        """Validar configuração."""
        if not cls.API_KEY:
            raise ValueError(
                "TLDV_API_KEY não configurada. "
                "Configure a variável de ambiente ou use o valor padrão."
            )
        return True

    @classmethod
    def from_env(cls) -> "TLDVConfig":
        """Carregar configuração das variáveis de ambiente."""
        cls.validate()
        return cls()

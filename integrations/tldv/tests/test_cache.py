"""Testes para módulo de cache."""

import time
from typing import Any

import pytest

from cache import CachedTLDVTools, MeetingCache
from composio_tools import TLDVComposioTools
from config import TLDVConfig


@pytest.fixture
def cache() -> MeetingCache:
    """Criar instância de cache para testes."""
    return MeetingCache(ttl_seconds=1)


@pytest.fixture
def tools(cache: MeetingCache) -> TLDVComposioTools:
    """Criar ferramentas para testes."""
    config = TLDVConfig.from_env()
    return TLDVComposioTools(config)


@pytest.fixture
def cached_tools(tools: TLDVComposioTools) -> CachedTLDVTools:
    """Criar ferramentas com cache para testes."""
    return CachedTLDVTools(tools, MeetingCache(ttl_seconds=3600))


class TestMeetingCache:
    """Testes para MeetingCache."""

    def test_cache_initialization(self, cache: MeetingCache) -> None:
        """Testar inicialização do cache."""
        assert cache.size() == 0
        assert cache.ttl_seconds == 1

    def test_cache_set_and_get(self, cache: MeetingCache) -> None:
        """Testar armazenar e recuperar do cache."""
        cache.set("key1", {"data": "value1"})

        assert cache.get("key1") == {"data": "value1"}

    def test_cache_get_missing_key(self, cache: MeetingCache) -> None:
        """Testar obter chave não existente."""
        assert cache.get("nonexistent") is None

    def test_cache_expiration(self, cache: MeetingCache) -> None:
        """Testar expiração do cache."""
        cache.set("key1", {"data": "value1"})

        # Verificar que está no cache
        assert cache.get("key1") is not None

        # Esperar expiração
        time.sleep(1.1)

        # Agora deve estar expirado
        assert cache.get("key1") is None

    def test_cache_size(self, cache: MeetingCache) -> None:
        """Testar tamanho do cache."""
        assert cache.size() == 0

        cache.set("key1", "value1")
        assert cache.size() == 1

        cache.set("key2", "value2")
        assert cache.size() == 2

    def test_cache_clear(self, cache: MeetingCache) -> None:
        """Testar limpar cache."""
        cache.set("key1", "value1")
        cache.set("key2", "value2")

        assert cache.size() == 2

        cache.clear()

        assert cache.size() == 0
        assert cache.get("key1") is None

    def test_cache_clear_expired(
        self, cache: MeetingCache
    ) -> None:
        """Testar limpeza de entradas expiradas."""
        cache.set("key1", "value1")

        assert cache.size() == 1

        time.sleep(1.1)

        removed = cache.clear_expired()

        assert removed == 1
        assert cache.size() == 0

    def test_cache_stats(self, cache: MeetingCache) -> None:
        """Testar estatísticas do cache."""
        cache.set("key1", "value1")

        stats = cache.stats()

        assert "size" in stats
        assert "ttl_seconds" in stats
        assert "entries" in stats

    def test_cache_ttl_configuration(self) -> None:
        """Testar configuração customizada de TTL."""
        cache = MeetingCache(ttl_seconds=10)

        assert cache.ttl_seconds == 10


class TestCachedTLDVTools:
    """Testes para CachedTLDVTools."""

    def test_cached_tools_initialization(
        self, cached_tools: CachedTLDVTools
    ) -> None:
        """Testar inicialização de ferramentas com cache."""
        assert cached_tools.tools is not None
        assert cached_tools.cache is not None

    def test_cached_get_meetings(
        self, cached_tools: CachedTLDVTools
    ) -> None:
        """Testar obtenção de reuniões com cache."""
        meetings1 = cached_tools.get_meetings(limit=2)
        meetings2 = cached_tools.get_meetings(limit=2)

        # Ambas devem retornar o mesmo resultado
        assert meetings1 == meetings2

        # E o cache deve conter a entrada
        assert cached_tools.cache.size() > 0

    def test_cached_get_meeting_summary(
        self, cached_tools: CachedTLDVTools
    ) -> None:
        """Testar obtenção de resumo com cache."""
        summary1 = cached_tools.get_meeting_summary("meeting_001")
        summary2 = cached_tools.get_meeting_summary("meeting_001")

        # Devem retornar o mesmo resultado
        assert summary1 == summary2

        # Cache deve conter a entrada
        assert cached_tools.cache.size() > 0

    def test_cached_get_meeting_transcript(
        self, cached_tools: CachedTLDVTools
    ) -> None:
        """Testar obtenção de transcrição com cache."""
        transcript1 = cached_tools.get_meeting_transcript("meeting_001")
        transcript2 = cached_tools.get_meeting_transcript("meeting_001")

        # Devem retornar o mesmo resultado
        assert transcript1 == transcript2

    def test_cached_get_meeting_details(
        self, cached_tools: CachedTLDVTools
    ) -> None:
        """Testar obtenção de detalhes com cache."""
        details1 = cached_tools.get_meeting_details("meeting_001")
        details2 = cached_tools.get_meeting_details("meeting_001")

        # Devem retornar o mesmo resultado
        assert details1 == details2

    def test_cached_get_meeting_participants(
        self, cached_tools: CachedTLDVTools
    ) -> None:
        """Testar obtenção de participantes com cache."""
        participants1 = cached_tools.get_meeting_participants(
            "meeting_001"
        )
        participants2 = cached_tools.get_meeting_participants(
            "meeting_001"
        )

        # Devem retornar o mesmo resultado
        assert participants1 == participants2

    def test_cached_search_meetings(
        self, cached_tools: CachedTLDVTools
    ) -> None:
        """Testar busca de reuniões com cache."""
        results1 = cached_tools.search_meetings("sprint")
        results2 = cached_tools.search_meetings("sprint")

        # Devem retornar o mesmo resultado
        assert results1 == results2

    def test_clear_cache(self, cached_tools: CachedTLDVTools) -> None:
        """Testar limpeza do cache."""
        cached_tools.get_meetings(limit=2)

        assert cached_tools.cache.size() > 0

        cached_tools.clear_cache()

        assert cached_tools.cache.size() == 0

    def test_cache_stats_method(
        self, cached_tools: CachedTLDVTools
    ) -> None:
        """Testar método de estatísticas."""
        cached_tools.get_meetings(limit=2)
        cached_tools.get_meeting_summary("meeting_001")

        stats = cached_tools.cache_stats()

        assert "size" in stats
        assert "ttl_seconds" in stats
        assert "entries" in stats

    def test_different_cache_keys(
        self, cached_tools: CachedTLDVTools
    ) -> None:
        """Testar que diferentes parâmetros geram diferentes chaves de cache."""
        meetings_limit2 = cached_tools.get_meetings(limit=2)
        meetings_limit5 = cached_tools.get_meetings(limit=5)

        # Devem ter tamanhos diferentes
        assert len(meetings_limit2) == 2
        assert len(meetings_limit5) == 5

        # Cache deve conter ambas as entradas
        assert cached_tools.cache.size() >= 2

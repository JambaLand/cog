"""Cache para armazenar dados de reuniões do TLDV."""

import time
from typing import Any, Dict, Optional


class MeetingCache:
    """Cache simples em memória para dados de reuniões.

    Implementa cache com expiração por tempo (TTL) para evitar
    chamadas excessivas à API do TLDV.
    """

    def __init__(self, ttl_seconds: int = 3600) -> None:
        """Inicializar cache.

        Args:
            ttl_seconds: Tempo de vida do cache em segundos (padrão: 1 hora).
        """
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        """Obter valor do cache se não expirou.

        Args:
            key: Chave do cache.

        Returns:
            Valor armazenado ou None se não encontrado ou expirado.
        """
        if key not in self._cache:
            return None

        entry = self._cache[key]
        if time.time() - entry["timestamp"] > self.ttl_seconds:
            # Cache expirou, remover
            del self._cache[key]
            return None

        return entry["value"]

    def set(self, key: str, value: Any) -> None:
        """Armazenar valor no cache.

        Args:
            key: Chave do cache.
            value: Valor a armazenar.
        """
        self._cache[key] = {"value": value, "timestamp": time.time()}

    def clear(self) -> None:
        """Limpar todo o cache."""
        self._cache.clear()

    def clear_expired(self) -> int:
        """Remover entradas expiradas do cache.

        Returns:
            Número de entradas removidas.
        """
        current_time = time.time()
        expired_keys = [
            key
            for key, entry in self._cache.items()
            if current_time - entry["timestamp"] > self.ttl_seconds
        ]

        for key in expired_keys:
            del self._cache[key]

        return len(expired_keys)

    def size(self) -> int:
        """Obter número de entradas no cache.

        Returns:
            Número de entradas.
        """
        return len(self._cache)

    def stats(self) -> Dict[str, Any]:
        """Obter estatísticas do cache.

        Returns:
            Dicionário com informações do cache.
        """
        self.clear_expired()

        return {
            "size": self.size(),
            "ttl_seconds": self.ttl_seconds,
            "entries": len(self._cache),
        }


class CachedTLDVTools:
    """Wrapper para TLDVComposioTools com cache automático."""

    def __init__(
        self, tools: Any, cache: Optional[MeetingCache] = None
    ) -> None:
        """Inicializar ferramentas com cache.

        Args:
            tools: Instância de TLDVComposioTools.
            cache: Instância de MeetingCache. Se None, cria uma nova.
        """
        self.tools = tools
        self.cache = cache or MeetingCache()

    def get_meetings(
        self, limit: Optional[int] = None, offset: int = 0
    ) -> list:
        """Obter lista de reuniões com cache.

        Args:
            limit: Número máximo de reuniões.
            offset: Offset para paginação.

        Returns:
            Lista de reuniões.
        """
        cache_key = f"meetings_{limit}_{offset}"
        cached = self.cache.get(cache_key)

        if cached is not None:
            return cached

        result = self.tools.get_meetings(limit=limit, offset=offset)
        self.cache.set(cache_key, result)
        return result

    def get_meeting_summary(self, meeting_id: str) -> Dict[str, Any]:
        """Obter resumo com cache.

        Args:
            meeting_id: ID da reunião.

        Returns:
            Resumo da reunião.
        """
        cache_key = f"summary_{meeting_id}"
        cached = self.cache.get(cache_key)

        if cached is not None:
            return cached

        result = self.tools.get_meeting_summary(meeting_id)
        self.cache.set(cache_key, result)
        return result

    def get_meeting_transcript(
        self, meeting_id: str
    ) -> Dict[str, Any]:
        """Obter transcrição com cache.

        Args:
            meeting_id: ID da reunião.

        Returns:
            Transcrição da reunião.
        """
        cache_key = f"transcript_{meeting_id}"
        cached = self.cache.get(cache_key)

        if cached is not None:
            return cached

        result = self.tools.get_meeting_transcript(meeting_id)
        self.cache.set(cache_key, result)
        return result

    def get_meeting_details(self, meeting_id: str) -> Dict[str, Any]:
        """Obter detalhes com cache.

        Args:
            meeting_id: ID da reunião.

        Returns:
            Detalhes da reunião.
        """
        cache_key = f"details_{meeting_id}"
        cached = self.cache.get(cache_key)

        if cached is not None:
            return cached

        result = self.tools.get_meeting_details(meeting_id)
        self.cache.set(cache_key, result)
        return result

    def get_meeting_participants(
        self, meeting_id: str
    ) -> list:
        """Obter participantes com cache.

        Args:
            meeting_id: ID da reunião.

        Returns:
            Lista de participantes.
        """
        cache_key = f"participants_{meeting_id}"
        cached = self.cache.get(cache_key)

        if cached is not None:
            return cached

        result = self.tools.get_meeting_participants(meeting_id)
        self.cache.set(cache_key, result)
        return result

    def search_meetings(
        self, query: str, limit: Optional[int] = None
    ) -> list:
        """Buscar reuniões com cache.

        Args:
            query: Termo de busca.
            limit: Limite de resultados.

        Returns:
            Lista de reuniões encontradas.
        """
        cache_key = f"search_{query}_{limit}"
        cached = self.cache.get(cache_key)

        if cached is not None:
            return cached

        result = self.tools.search_meetings(query, limit=limit)
        self.cache.set(cache_key, result)
        return result

    def clear_cache(self) -> None:
        """Limpar o cache."""
        self.cache.clear()

    def cache_stats(self) -> Dict[str, Any]:
        """Obter estatísticas do cache.

        Returns:
            Estatísticas do cache.
        """
        return self.cache.stats()

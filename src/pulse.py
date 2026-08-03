"""Pulse module: MoveFeed for tracking recent move activity."""

from collections import deque
from typing import Dict, List, Any


class MoveFeed:
    """Fixed-size sliding window of recent moves with per-domain analytics."""

    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self._window: deque = deque(maxlen=max_size)

    def add_move(self, move: Dict[str, Any]) -> None:
        """Add a move dict to the window (evicts oldest if at capacity)."""
        self._window.append(move)

    def get_recent(self, n: int = 20) -> List[Dict[str, Any]]:
        """Return the most recent n moves from the window."""
        return list(self._window)[-n:]

    def get_trending_domains(self) -> Dict[str, int]:
        """Return domain counts in the current window, sorted descending by count."""
        counts: Dict[str, int] = {}
        for move in self._window:
            domain = move.get("domain", "unknown")
            counts[domain] = counts.get(domain, 0) + 1
        return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    def get_domain_temperature(self, domain: str) -> float:
        """Return a 0-1 normalized temperature for a domain.

        Temperature is count_of_domain / max_count_among_all_domains.
        If the window is empty, returns 0.0.
        """
        if not self._window:
            return 0.0
        trending = self.get_trending_domains()
        if not trending:
            return 0.0
        max_count = max(trending.values())
        domain_count = trending.get(domain, 0)
        return domain_count / max_count

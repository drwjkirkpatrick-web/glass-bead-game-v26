"""
glass-bead-game-v26 — Matchmaking
"Find Your Counter-Subject" — pair players by complementarity.
"""
from dataclasses import dataclass, field
from typing import Dict, List
import math


@dataclass
class Matchmaker:
    players: Dict[str, Dict[str, float]] = field(default_factory=dict)

    def add_player(self, name: str, domain_vector: Dict[str, float]):
        self.players[name] = domain_vector

    def _normalize(self, vec: Dict[str, float]) -> Dict[str, float]:
        total = math.sqrt(sum(v*v for v in vec.values()))
        if total == 0:
            return vec
        return {k: v/total for k, v in vec.items()}

    def _dot_product(self, a: Dict[str, float], b: Dict[str, float]) -> float:
        keys = set(a.keys()) | set(b.keys())
        return sum(a.get(k, 0) * b.get(k, 0) for k in keys)

    def get_compatibility(self, a: str, b: str) -> float:
        if a not in self.players or b not in self.players:
            return 0.0
        vec_a = self._normalize(self.players[a])
        vec_b = self._normalize(self.players[b])
        # Complementarity: low dot product = different strengths = high compatibility
        dot = self._dot_product(vec_a, vec_b)
        return round(1.0 - dot, 3)

    def find_match(self, player_name: str) -> dict:
        if player_name not in self.players:
            return {"error": "Player not found"}
        best_opponent = None
        best_score = -1.0
        for name in self.players:
            if name == player_name:
                continue
            score = self.get_compatibility(player_name, name)
            if score > best_score:
                best_score = score
                best_opponent = name

        if not best_opponent:
            return {"error": "No opponents available"}

        vec_a = self.players[player_name]
        vec_b = self.players[best_opponent]
        a_strengths = [k for k, v in vec_a.items() if v >= 0.7]
        b_strengths = [k for k, v in vec_b.items() if v >= 0.7]
        shared = [k for k in a_strengths if k in b_strengths]

        return {
            "opponent": best_opponent,
            "compatibility": best_score,
            "your_strengths": a_strengths,
            "opponent_strengths": b_strengths,
            "shared": shared,
            "match_type": "Dialectic" if best_score > 0.7 else "Standard",
        }

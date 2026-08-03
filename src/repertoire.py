"""
glass-bead-game-v26 — Move Repertoire Archive
Personal searchable archive of all moves with filter and export.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class Repertoire:
    """A player's archive of moves."""
    moves: List[Dict[str, Any]] = field(default_factory=list)

    def add_move(self, move: Dict[str, Any]):
        self.moves.append(move)

    def search(self, query: str) -> List[Dict[str, Any]]:
        q = query.lower()
        return [m for m in self.moves if q in f"{m.get('from_concept','')} {m.get('to_concept','')} {m.get('isomorphism','')}".lower()]

    def filter_by_isomorphism(self, iso: str) -> List[Dict[str, Any]]:
        return [m for m in self.moves if m.get('isomorphism') == iso]

    def get_signature_isomorphism(self) -> tuple:
        if not self.moves:
            return (None, 0)
        counts = {}
        for m in self.moves:
            iso = m.get('isomorphism', 'generic')
            counts[iso] = counts.get(iso, 0) + 1
        return max(counts.items(), key=lambda x: x[1])

    def to_dict(self) -> dict:
        sig, count = self.get_signature_isomorphism()
        return {
            "moves": self.moves,
            "total": len(self.moves),
            "signature_isomorphism": sig,
            "signature_count": count,
        }

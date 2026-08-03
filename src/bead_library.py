"""
glass-bead-game-v26 — Glass Bead Library
Shared repository of individual beads with checkout and rating.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class Bead:
    id: int
    name: str
    domain: str
    color: str
    formula: str
    popularity: float = 0.5
    checked_out_by: str = ""
    ratings: List[float] = field(default_factory=list)

    def average_rating(self) -> float:
        if not self.ratings:
            return self.popularity
        return sum(self.ratings) / len(self.ratings)


@dataclass
class BeadCatalog:
    beads: List[Bead] = field(default_factory=list)
    _next_id: int = 1

    def add_bead(self, name: str, domain: str, color: str, formula: str, popularity: float = 0.5):
        bead = Bead(id=self._next_id, name=name, domain=domain, color=color, formula=formula, popularity=popularity)
        self.beads.append(bead)
        self._next_id += 1
        return bead

    def checkout(self, bead_id: int, player: str) -> bool:
        for b in self.beads:
            if b.id == bead_id and not b.checked_out_by:
                b.checked_out_by = player
                return True
        return False

    def return_bead(self, bead_id: int) -> bool:
        for b in self.beads:
            if b.id == bead_id:
                b.checked_out_by = ""
                return True
        return False

    def rate(self, bead_id: int, rating: float) -> bool:
        for b in self.beads:
            if b.id == bead_id:
                b.ratings.append(max(0.0, min(1.0, rating)))
                return True
        return False

    def search(self, query: str) -> List[Bead]:
        q = query.lower()
        return [b for b in self.beads if q in f"{b.name} {b.domain} {b.formula}".lower()]

    def get_popular(self, n: int = 5) -> List[Bead]:
        return sorted(self.beads, key=lambda b: b.average_rating(), reverse=True)[:n]

    def to_dict(self) -> dict:
        return {
            "beads": [
                {
                    "id": b.id,
                    "name": b.name,
                    "domain": b.domain,
                    "color": b.color,
                    "formula": b.formula,
                    "popularity": round(b.average_rating(), 2),
                    "checked_out_by": b.checked_out_by,
                }
                for b in self.beads
            ]
        }

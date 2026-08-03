"""
glass-bead-game-v26 — Player Identity (Castalian Identity Card)
"The dream of almost every fifteen-year-old in the elite schools..."
— Hesse, Das Glasperlenspiel
"""
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class PlayerIdentity:
    """A Castalian player's persistent identity and progression."""
    name: str
    rank: str = "Novice"
    province: str = "Waldzell"
    verified_moves: int = 0
    contemplation_hours: float = 0.0
    peer_endorsements: List[str] = field(default_factory=list)
    badges: List[str] = field(default_factory=list)
    domain_mastery: Dict[str, float] = field(default_factory=dict)

    def add_verified_move(self):
        self.verified_moves += 1

    def add_contemplation_hours(self, hours: float):
        self.contemplation_hours += hours

    def add_peer_endorsement(self, peer: str):
        if peer not in self.peer_endorsements:
            self.peer_endorsements.append(peer)

    def award_badge(self, badge: str):
        if badge not in self.badges:
            self.badges.append(badge)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "rank": self.rank,
            "province": self.province,
            "verified_moves": self.verified_moves,
            "contemplation_hours": self.contemplation_hours,
            "peer_endorsements": self.peer_endorsements,
            "badges": self.badges,
            "domain_mastery": self.domain_mastery,
        }

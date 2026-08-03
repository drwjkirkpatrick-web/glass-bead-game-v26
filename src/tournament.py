"""
glass-bead-game-v26 — Tournament Bracket System
Single-elimination bracket for Ludus Sollemnis / Anniversarius.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any
from enum import Enum


class FestivalType(Enum):
    LUDUS_SOLLEMNIS = "sollemnis"
    LUDUS_ANNIVERSARIUS = "anniversarius"


@dataclass
class Match:
    player_a: str
    player_b: str
    winner: str = ""
    score_a: float = 0.0
    score_b: float = 0.0


@dataclass
class Round:
    matches: List[Match] = field(default_factory=list)


@dataclass
class Tournament:
    tournament_id: str
    festival_type: FestivalType
    rounds: List[Round] = field(default_factory=list)
    champion: str = ""
    players: List[Dict[str, Any]] = field(default_factory=list)

    def seed_players(self, players: List[Dict[str, Any]]):
        """Seed players by rank (highest first), build bracket."""
        self.players = sorted(players, key=lambda p: p.get('rank', 0), reverse=True)
        # Create round 1 matches
        round1 = Round()
        for i in range(0, len(self.players), 2):
            a = self.players[i]['name'] if i < len(self.players) else "Bye"
            b = self.players[i+1]['name'] if i+1 < len(self.players) else "Bye"
            round1.matches.append(Match(player_a=a, player_b=b))
        self.rounds = [round1]

    def advance_winner(self, round_idx: int, match_idx: int, winner: str, score_winner: float, score_loser: float):
        """Record a match result and propagate to next round."""
        match = self.rounds[round_idx].matches[match_idx]
        match.winner = winner
        if winner == match.player_a:
            match.score_a = score_winner
            match.score_b = score_loser
        else:
            match.score_a = score_loser
            match.score_b = score_winner

        # Auto-create next round
        if round_idx + 1 >= len(self.rounds):
            self.rounds.append(Round())
        next_round = self.rounds[round_idx + 1]
        next_match_idx = match_idx // 2
        if len(next_round.matches) <= next_match_idx:
            next_round.matches.append(Match(player_a=winner, player_b="TBD"))
        else:
            nm = next_round.matches[next_match_idx]
            if nm.player_a == "TBD":
                nm.player_a = winner
            else:
                nm.player_b = winner

        # Check for champion
        if len(self.rounds) > 1 and round_idx == len(self.rounds) - 2 and len(next_round.matches) == 1 and next_round.matches[0].player_b != "TBD":
            self.champion = winner

    def to_dict(self) -> dict:
        return {
            "tournament_id": self.tournament_id,
            "festival_type": self.festival_type.value,
            "rounds": [
                {
                    "matches": [
                        {"player_a": m.player_a, "player_b": m.player_b, "winner": m.winner,
                         "score_a": m.score_a, "score_b": m.score_b}
                        for m in r.matches
                    ]
                }
                for r in self.rounds
            ],
            "champion": self.champion,
        }

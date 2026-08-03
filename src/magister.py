"""
glass-bead-game-v26 — Ludi Magister

The Ludi Magister presided over the public Games, supervised the players
and the schools of the Game, and sat on the World Commission of the
Magisters of all countries.  Each magister must train a successor.

Inspired by Hesse, *Das Glasperlenspiel*:
    "Official matches, played under the personal direction of the Ludi
    Magister, were exalted into cultural festivals... the Ludi Magister
    is a prince or high priest, almost a deity."

    "The World Commission of the Magisters of all countries..."

    — Joseph Knecht eventually trains Tito as his successor.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional


class Province(Enum):
    """The great Castalian provinces that host a Ludi Magister."""
    WALDZELL = auto()     # seat of the Glass Bead Game
    MONTEPORT = auto()    # music and mathematics
    KEHRHORT = auto()     # philology and history
    MARIABUCH = auto()    # astronomy and natural sciences


class Rank(Enum):
    """Hierarchy within the Castalian order."""
    LUDI_MAGISTER = auto()   # highest; presides over public Games
    SUB_MAGISTER = auto()    # deputy, may preside over minor festivals
    SENIOR_PLAYER = auto()   # eligible for public matches
    JOURNEYMAN = auto()      # student of the Game


@dataclass
class GameEvaluation:
    """
    The four dimensions by which a Ludi Magister judges a Game.
    All values range 0.0 – 1.0.
    """
    technical_virtuosity: float = 0.0   # precision, technique, formal mastery
    contemplative_depth: float = 0.0     # meditation quality, inner resonance
    synthesis_quality: float = 0.0     # thesis-antithesis unity achieved
    ceremonial_presence: float = 0.0    # ritual bearing, audience attunement

    @property
    def overall_score(self) -> float:
        """Weighted average: synthesis and contemplation weigh slightly more."""
        weights = (0.25, 0.30, 0.30, 0.15)
        vals = (
            self.technical_virtuosity,
            self.contemplative_depth,
            self.synthesis_quality,
            self.ceremonial_presence,
        )
        return sum(w * v for w, v in zip(weights, vals))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "technical_virtuosity": round(self.technical_virtuosity, 3),
            "contemplative_depth": round(self.contemplative_depth, 3),
            "synthesis_quality": round(self.synthesis_quality, 3),
            "ceremonial_presence": round(self.ceremonial_presence, 3),
            "overall_score": round(self.overall_score, 3),
        }


@dataclass
class PlayerAssessment:
    """A magister's written assessment of a player after a Game."""
    player_name: str
    evaluation: GameEvaluation
    notes: str = ""
    assessed_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class School:
    """
    A school of the Game — a body of players under a magister's
    supervision.  Each school cultivates a distinctive style.
    """
    name: str
    province: Province
    style: str = ""           # e.g. "contrapuntal", "meditative", "dialectical"
    players: List[str] = field(default_factory=list)

    def enroll(self, player: str) -> None:
        if player not in self.players:
            self.players.append(player)

    def remove(self, player: str) -> None:
        if player in self.players:
            self.players.remove(player)


class Magister:
    """
    The Ludi Magister: highest authority in the Castalian order.

    Responsibilities:
        * preside over public matches (Ludus sollemnis / anniversarius)
        * supervise schools of the Game
        * elaborate new formulas and themes
        * evaluate players on four dimensions
        * train and appoint a successor

    The magister is tied to a province and holds jurisdiction over
    public matches, schools, and formula elaboration.
    """

    def __init__(
        self,
        name: str,
        province: Province,
        rank: Rank = Rank.LUDI_MAGISTER,
    ):
        if not name or not name.strip():
            raise ValueError("A magister must have a name.")
        self.name: str = name
        self.province: Province = province
        self.rank: Rank = rank

        # Jurisdiction
        self.duties: List[str] = [
            "preside over public matches (Ludus sollemnis, Ludus anniversarius)",
            "supervise schools of the Game",
            "elaborate formulas and new themes",
            "evaluate players on technical, contemplative, synthetic, and ceremonial grounds",
            "train and appoint a successor",
            "sit on the World Commission of Magisters",
        ]

        # Schools under supervision
        self.schools: List[School] = []

        # Evaluation ledger
        self.evaluations: List[PlayerAssessment] = []

        # Successor training
        self._successor: Optional[str] = None
        self._successor_training_started: Optional[datetime] = None
        self._successor_training_complete: bool = False

        # Commission membership
        self.commission_sessions_attended: int = 0

    # ------------------------------------------------------------------
    # Jurisdiction & duties
    # ------------------------------------------------------------------

    def list_duties(self) -> List[str]:
        """Return the canonical duties of the Ludi Magister."""
        return list(self.duties)

    def add_duty(self, duty: str) -> None:
        """Ad-hoc duty assigned by the World Commission."""
        if duty not in self.duties:
            self.duties.append(duty)

    def remove_duty(self, duty: str) -> None:
        if duty in self.duties:
            self.duties.remove(duty)

    # ------------------------------------------------------------------
    # Schools
    # ------------------------------------------------------------------

    def found_school(self, name: str, style: str = "") -> School:
        """Found a new school under this magister's supervision."""
        school = School(name=name, province=self.province, style=style)
        self.schools.append(school)
        return school

    def supervise_school(self, school: School) -> None:
        """Assume supervision of an existing school."""
        if school not in self.schools:
            self.schools.append(school)

    def list_schools(self) -> List[str]:
        return [s.name for s in self.schools]

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    def evaluate_game(
        self,
        player_name: str,
        technical_virtuosity: float = 0.0,
        contemplative_depth: float = 0.0,
        synthesis_quality: float = 0.0,
        ceremonial_presence: float = 0.0,
        notes: str = "",
    ) -> GameEvaluation:
        """
        Record the magister's judgment of a single Game.
        All scores are clamped to [0.0, 1.0].
        """
        evaluation = GameEvaluation(
            technical_virtuosity=max(0.0, min(1.0, technical_virtuosity)),
            contemplative_depth=max(0.0, min(1.0, contemplative_depth)),
            synthesis_quality=max(0.0, min(1.0, synthesis_quality)),
            ceremonial_presence=max(0.0, min(1.0, ceremonial_presence)),
        )
        assessment = PlayerAssessment(
            player_name=player_name,
            evaluation=evaluation,
            notes=notes,
        )
        self.evaluations.append(assessment)
        return evaluation

    def get_player_evaluations(self, player_name: str) -> List[PlayerAssessment]:
        return [e for e in self.evaluations if e.player_name == player_name]

    def highest_evaluation(self, player_name: str) -> Optional[GameEvaluation]:
        """Return the player's best evaluation by overall score."""
        evs = self.get_player_evaluations(player_name)
        if not evs:
            return None
        return max(evs, key=lambda a: a.evaluation.overall_score).evaluation

    # ------------------------------------------------------------------
    # Successor training
    # ------------------------------------------------------------------

    def train_successor(self, candidate_name: str) -> None:
        """
        Begin training a successor.  A magister may have only one
        successor-in-training at a time (Knecht trains Tito).
        """
        if self._successor is not None and self._successor != candidate_name:
            raise RuntimeError(
                f"Already training {self._successor}; "
                f"finish or dismiss before appointing {candidate_name}."
            )
        self._successor = candidate_name
        self._successor_training_started = datetime.utcnow()
        self._successor_training_complete = False

    def mark_training_complete(self) -> None:
        """Declare the successor's training finished."""
        if self._successor is None:
            raise RuntimeError("No successor is currently in training.")
        self._successor_training_complete = True

    def dismiss_successor(self) -> None:
        """Dismiss the current successor-in-training."""
        self._successor = None
        self._successor_training_started = None
        self._successor_training_complete = False

    def appoint_successor(self) -> str:
        """
        Formally appoint the trained successor.
        Raises if training is incomplete or no candidate exists.
        """
        if self._successor is None:
            raise RuntimeError("No successor has been designated for training.")
        if not self._successor_training_complete:
            raise RuntimeError(
                f"{self._successor} has not yet completed training."
            )
        appointed = self._successor
        # The old magister steps aside; the successor assumes the rank.
        self._successor = None
        self._successor_training_started = None
        self._successor_training_complete = False
        return appointed

    def successor_status(self) -> Dict[str, Any]:
        """Return the current successor-training state."""
        if self._successor is None:
            return {"has_successor": False}
        return {
            "has_successor": True,
            "candidate": self._successor,
            "training_started": self._successor_training_started.isoformat()
            if self._successor_training_started
            else None,
            "training_complete": self._successor_training_complete,
        }

    # ------------------------------------------------------------------
    # Commission
    # ------------------------------------------------------------------

    def attend_commission_session(self) -> None:
        """Record attendance at a session of the World Commission."""
        self.commission_sessions_attended += 1

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "province": self.province.name,
            "rank": self.rank.name,
            "duties": self.duties,
            "schools": [
                {
                    "name": s.name,
                    "province": s.province.name,
                    "style": s.style,
                    "players": s.players,
                }
                for s in self.schools
            ],
            "evaluations_count": len(self.evaluations),
            "successor": self.successor_status(),
            "commission_sessions_attended": self.commission_sessions_attended,
        }

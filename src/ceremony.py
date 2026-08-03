"""
glass-bead-game-v26 — Ceremonial Match System

Official matches, played under the personal direction of the Ludi Magister,
were exalted into cultural festivals. The ceremony follows sonata-form phases:
Prelude → Exposition → Development → Recapitulation → Coda.

Festival types:
    Ludus sollemnis      — annual public festival
    Ludus anniversarius  — anniversary celebration

Scoring dimensions:
    reverence    — audience depth / spiritual attunement
    virtuosity   — technical excellence of play
    synthesis    — quality of thesis-antithesis synthesis
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional


class FestivalType(Enum):
    """Categories of ceremonial public matches."""
    LUDUS_SOLLEMNIS = auto()      # annual
    LUDUS_ANNIVERSARIUS = auto()  # anniversary


class CeremonialPhase(Enum):
    """Sonata-form phases of a ceremonial match."""
    PRELUDE = auto()          # silence, meditation, invocation
    EXPOSITION = auto()       # themes stated clearly
    DEVELOPMENT = auto()      # themes elaborated, varied, transformed
    RECAPITULATION = auto()   # themes return, reconciled
    CODA = auto()             # closing meditation, realization


@dataclass
class Audience:
    """Public spectators whose collective reverence shapes the festival atmosphere."""
    size: int = 0
    reverence_score: float = 0.0  # 0.0 – 1.0

    def deepen_reverence(self, amount: float = 0.05) -> None:
        """A magister’s presence or beautiful play deepens reverence."""
        self.reverence_score = min(1.0, self.reverence_score + amount)

    def diminish_reverence(self, amount: float = 0.05) -> None:
        """Discord or interruption diminishes reverence."""
        self.reverence_score = max(0.0, self.reverence_score - amount)


@dataclass
class FestivalRecord:
    """Immutable record of a completed ceremonial match."""
    record_id: str
    festival_type: FestivalType
    magister_name: str
    phases_completed: List[CeremonialPhase]
    audience_size: int
    final_reverence: float
    reverence_score: float
    virtuosity_score: float
    synthesis_score: float
    overall_score: float
    played_at: datetime
    meditation_minutes: int
    notes: str = ""


@dataclass
class Ceremony:
    """
    A ceremonial match presided over by the Ludi Magister.

    A valid ceremonial match requires:
        * a Ludi Magister presiding
        * a public audience
        * formal meditation before play
        * progression through all five sonata-form phases
    """
    magister_presiding: str
    festival_type: FestivalType
    audience: Audience = field(default_factory=lambda: Audience(size=0, reverence_score=0.0))

    # Phase tracking
    current_phase: CeremonialPhase = CeremonialPhase.PRELUDE
    phases_completed: List[CeremonialPhase] = field(default_factory=list)

    # Scoring accumulators (updated incrementally during play)
    reverence: float = 0.0     # audience depth
    virtuosity: float = 0.0    # technical excellence
    synthesis: float = 0.0     # synthesis quality

    # Ritual requirements
    meditation_performed: bool = False
    meditation_minutes: int = 0

    # Lifecycle
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    completed: bool = False

    def __post_init__(self) -> None:
        if not self.magister_presiding or not self.magister_presiding.strip():
            raise ValueError("A ceremonial match must have a Ludi Magister presiding.")
        if self.audience.size <= 0:
            raise ValueError("A ceremonial match requires a public audience.")
        self.started_at = datetime.utcnow()

    # ------------------------------------------------------------------
    # Meditation
    # ------------------------------------------------------------------
    def perform_meditation(self, minutes: int = 10) -> None:
        """
        Formal meditation before play.
        Required by the book: 'Each player was required to perform silent,
        formal meditation on the content, origin, and meaning of the Game.'
        """
        if minutes < 1:
            raise ValueError("Meditation must last at least one minute.")
        self.meditation_performed = True
        self.meditation_minutes = minutes
        self.reverence += min(0.3, minutes * 0.02)
        self.audience.deepen_reverence(0.1)

    # ------------------------------------------------------------------
    # Phase advancement
    # ------------------------------------------------------------------
    def _advance_phase(self) -> None:
        """Move to the next sonata-form phase."""
        order = [
            CeremonialPhase.PRELUDE,
            CeremonialPhase.EXPOSITION,
            CeremonialPhase.DEVELOPMENT,
            CeremonialPhase.RECAPITULATION,
            CeremonialPhase.CODA,
        ]
        idx = order.index(self.current_phase)
        if idx + 1 < len(order):
            self.phases_completed.append(self.current_phase)
            self.current_phase = order[idx + 1]
        else:
            self.phases_completed.append(self.current_phase)
            self.completed = True
            self.ended_at = datetime.utcnow()

    def begin_prelude(self) -> None:
        """Prelude: silence, invocation, attunement."""
        if self.current_phase is not CeremonialPhase.PRELUDE:
            raise RuntimeError("Prelude can only begin the ceremony.")
        self._advance_phase()

    def begin_exposition(self, theme_clarity: float = 0.5) -> None:
        """Exposition: themes stated with clarity."""
        if self.current_phase is not CeremonialPhase.EXPOSITION:
            raise RuntimeError("Exposition must follow Prelude.")
        self.virtuosity += theme_clarity * 0.2
        self.audience.deepen_reverence(theme_clarity * 0.05)
        self._advance_phase()

    def begin_development(self, elaboration: float = 0.5, contrast: float = 0.5) -> None:
        """Development: themes elaborated, varied, set in counterpoint."""
        if self.current_phase is not CeremonialPhase.DEVELOPMENT:
            raise RuntimeError("Development must follow Exposition.")
        self.virtuosity += elaboration * 0.25
        self.synthesis += contrast * 0.15
        self.audience.deepen_reverence(elaboration * 0.05)
        self._advance_phase()

    def begin_recapitulation(self, reconciliation: float = 0.5) -> None:
        """Recapitulation: themes return, synthesized, harmonized."""
        if self.current_phase is not CeremonialPhase.RECAPITULATION:
            raise RuntimeError("Recapitulation must follow Development.")
        self.synthesis += reconciliation * 0.3
        self.reverence += reconciliation * 0.2
        self.audience.deepen_reverence(reconciliation * 0.1)
        self._advance_phase()

    def begin_coda(self, realization: float = 0.5) -> None:
        """
        Coda: closing meditation, realization.
        'Realizing' was a favorite expression among the players.
        """
        if self.current_phase is not CeremonialPhase.CODA:
            raise RuntimeError("Coda must follow Recapitulation.")
        self.reverence += realization * 0.2
        self.audience.deepen_reverence(realization * 0.1)
        self._advance_phase()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def is_valid(self) -> bool:
        """
        A ceremonial match is valid only when:
            * a Ludi Magister is present
            * a public audience exists
            * formal meditation was performed before play
            * all five phases were completed
        """
        return (
            bool(self.magister_presiding)
            and self.audience.size > 0
            and self.meditation_performed
            and self.completed
            and len(self.phases_completed) == 5
        )

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------
    def calculate_scores(self) -> Dict[str, float]:
        """Return current dimension scores, capped at 1.0."""
        return {
            "reverence": min(1.0, self.reverence),
            "virtuosity": min(1.0, self.virtuosity),
            "synthesis": min(1.0, self.synthesis),
            "overall": min(1.0, (self.reverence + self.virtuosity + self.synthesis) / 3.0),
        }

    # ------------------------------------------------------------------
    # Festival record
    # ------------------------------------------------------------------
    def produce_festival_record(self, notes: str = "") -> Optional[FestivalRecord]:
        """Produce an immutable record of the completed ceremony."""
        if not self.is_valid():
            return None
        scores = self.calculate_scores()
        return FestivalRecord(
            record_id=str(uuid.uuid4()),
            festival_type=self.festival_type,
            magister_name=self.magister_presiding,
            phases_completed=list(self.phases_completed),
            audience_size=self.audience.size,
            final_reverence=self.audience.reverence_score,
            reverence_score=scores["reverence"],
            virtuosity_score=scores["virtuosity"],
            synthesis_score=scores["synthesis"],
            overall_score=scores["overall"],
            played_at=self.started_at or datetime.utcnow(),
            meditation_minutes=self.meditation_minutes,
            notes=notes,
        )

    # ------------------------------------------------------------------
    # Convenience: full ceremonial play
    # ------------------------------------------------------------------
    def play_full_ceremony(
        self,
        theme_clarity: float = 0.7,
        elaboration: float = 0.7,
        contrast: float = 0.6,
        reconciliation: float = 0.8,
        realization: float = 0.7,
    ) -> FestivalRecord:
        """
        Run the complete ceremonial match in one call.
        Useful for testing and scripted festivals.
        """
        if not self.meditation_performed:
            self.perform_meditation(minutes=10)
        self.begin_prelude()
        self.begin_exposition(theme_clarity=theme_clarity)
        self.begin_development(elaboration=elaboration, contrast=contrast)
        self.begin_recapitulation(reconciliation=reconciliation)
        self.begin_coda(realization=realization)
        record = self.produce_festival_record()
        if record is None:
            raise RuntimeError("Ceremony failed to produce a valid festival record.")
        return record

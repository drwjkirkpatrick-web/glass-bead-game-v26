"""
glass-bead-game-v26 — Contemplation Engine
Formal meditation requirement: each player must perform silent, formal meditation
on the content, origin, and meaning of the Game before certain moves.

Inspired by Hesse, *Das Glasperlenspiel* (p. 1346-1349):
"Each player was required to perform silent, formal meditation on the content,
origin, and meaning of the Game... the art of contemplation and meditation
was nurtured."
"""

import dataclasses
import time
from enum import Enum, auto
from typing import Dict, List, Optional, Any


class ContemplationPhase(Enum):
    PREPARATION = auto()
    RECOLLECTION = auto()
    CONCENTRATION = auto()
    INSIGHT = auto()
    INTEGRATION = auto()


PHASE_LANG: Dict[ContemplationPhase, Dict[str, str]] = {
    ContemplationPhase.PREPARATION: {
        "latin": "Praeparatio",
        "german": "Die Stille vor dem Spiel",
        "purpose": "Set intention and quiet the mind before entering the Game.",
    },
    ContemplationPhase.RECOLLECTION: {
        "latin": "Recollectio",
        "german": "Die Erinnerung an das Gespielte",
        "purpose": "Review prior moves and their resonances with detached clarity.",
    },
    ContemplationPhase.CONCENTRATION: {
        "latin": "Concentratio",
        "german": "Das Sich-Versenken in die Gestalt",
        "purpose": "Focus on the current move's structure until it becomes transparent.",
    },
    ContemplationPhase.INSIGHT: {
        "latin": "Illuminatio",
        "german": "Der Einfall, das Erkennen",
        "purpose": "Receive or generate the resonant connection that unifies disciplines.",
    },
    ContemplationPhase.INTEGRATION: {
        "latin": "Integratio",
        "german": "Die Rueckkehr ins Spiel",
        "purpose": "Return to play with the insight embodied, not merely held in thought.",
    },
}


@dataclasses.dataclass
class PhaseRecord:
    phase: ContemplationPhase
    started_at: float
    ended_at: float
    notes: str = ""

    @property
    def duration_seconds(self) -> float:
        return self.ended_at - self.started_at


class ContemplationSession:
    """
    A formal meditation session spanning the five Castalian phases.
    Usage:
        session = ContemplationSession(player_id="knecht")
        session.enter_phase(ContemplationPhase.PREPARATION)
        time.sleep(2)
        session.exit_phase("I seek unity beneath multiplicity.")
        ...
        score = session.depth_score()
    """

    MIN_PHASE_SECONDS: float = 1.0
    REQUIRED_PHASES: List[ContemplationPhase] = list(ContemplationPhase)
    MOVE_TYPES_REQUIRING_CONTEMPLATION: List[str] = [
        "synthesis", "thesis_antithesis", "public_match", "realization", "theme_development"
    ]
    CEREMONIAL_PHRASES: List[str] = [
        "Per aspera ad astra — through contemplation, the move shines.",
        "In der Stille wurde das Spiel geboren.",
        "The bead is now transparent; light passes through it.",
        "Contemplata aliis tradere: what was meditated may now be played.",
    ]

    def __init__(self, player_id: str, session_id: Optional[str] = None):
        self.player_id = player_id
        self.session_id = session_id or f"cont_{int(time.time() * 1000)}"
        self.phases_completed: List[PhaseRecord] = []
        self._current_phase: Optional[ContemplationPhase] = None
        self._phase_start_time: Optional[float] = None
        self._consumed: bool = False

    # ------------------------------------------------------------------
    # Phase lifecycle
    # ------------------------------------------------------------------

    def enter_phase(self, phase: ContemplationPhase) -> None:
        if self._current_phase is not None:
            raise RuntimeError(f"Already in {self._current_phase.name}; exit_phase() first.")
        self._current_phase = phase
        self._phase_start_time = time.time()

    def exit_phase(self, notes: str = "") -> PhaseRecord:
        if self._current_phase is None or self._phase_start_time is None:
            raise RuntimeError("No active phase.")
        if len(notes) < 10:
            raise ValueError("Notes must be at least 10 characters.")
        record = PhaseRecord(
            phase=self._current_phase,
            started_at=self._phase_start_time,
            ended_at=time.time(),
            notes=notes,
        )
        self.phases_completed.append(record)
        self._current_phase = None
        self._phase_start_time = None
        return record

    def is_active(self) -> bool:
        return self._current_phase is not None

    # ------------------------------------------------------------------
    # Completion & requirement checks
    # ------------------------------------------------------------------

    def is_complete(self) -> bool:
        return {p.phase for p in self.phases_completed} == set(self.REQUIRED_PHASES)

    def phase_duration(self, phase: ContemplationPhase) -> float:
        return sum(r.duration_seconds for r in self.phases_completed if r.phase == phase)

    def total_duration(self) -> float:
        return sum(r.duration_seconds for r in self.phases_completed)

    @classmethod
    def move_requires_contemplation(cls, move_type: str) -> bool:
        return move_type.lower() in {m.lower() for m in cls.MOVE_TYPES_REQUIRING_CONTEMPLATION}

    # ------------------------------------------------------------------
    # Depth scoring (0-100, proportional to meditation time)
    # ------------------------------------------------------------------

    def depth_score(self) -> Dict[str, Any]:
        if not self.phases_completed:
            return {"raw": 0.0, "scaled": 0.0, "bonus_multiplier": 1.0}
        total_time = self.total_duration()
        raw = min(100.0, (total_time / 300.0) * 100.0)
        min_obs = min((r.duration_seconds for r in self.phases_completed), default=0.0)
        penalty = (self.MIN_PHASE_SECONDS - min_obs) * 10.0 if min_obs < self.MIN_PHASE_SECONDS else 0.0
        scaled = max(0.0, raw - penalty)
        return {
            "raw": round(raw, 2),
            "scaled": round(scaled, 2),
            "bonus_multiplier": round(1.0 + (scaled / 100.0), 2),
            "total_seconds": round(total_time, 2),
            "phases_completed": len(self.phases_completed),
            "min_phase_seconds": round(min_obs, 2),
        }

    # ------------------------------------------------------------------
    # Bonus scoring for moves made after contemplation
    # ------------------------------------------------------------------

    def claim_bonus(self) -> Optional[Dict[str, Any]]:
        if self._consumed or not self.is_complete():
            return None
        depth = self.depth_score()
        import random
        self._consumed = True
        return {
            "bonus_points": depth["scaled"],
            "bonus_multiplier": depth["bonus_multiplier"],
            "phrase": random.choice(self.CEREMONIAL_PHRASES),
            "consumed": True,
        }

    # ------------------------------------------------------------------
    # Language thread
    # ------------------------------------------------------------------

    def language_thread(self, phase: Optional[ContemplationPhase] = None) -> Dict[str, Any]:
        if phase is not None:
            meta = PHASE_LANG.get(phase, {})
            return {"name": phase.name, **meta}
        return {
            p.name: {"latin": m["latin"], "german": m["german"], "purpose": m["purpose"]}
            for p, m in PHASE_LANG.items()
        }

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "player_id": self.player_id,
            "session_id": self.session_id,
            "consumed": self._consumed,
            "phases": [
                {"phase": r.phase.name, "started_at": r.started_at, "ended_at": r.ended_at,
                 "duration_seconds": r.duration_seconds, "notes": r.notes}
                for r in self.phases_completed
            ],
            "depth_score": self.depth_score(),
            "is_complete": self.is_complete(),
            "language_thread": self.language_thread(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContemplationSession":
        obj = cls(player_id=data.get("player_id", "unknown"), session_id=data.get("session_id"))
        obj._consumed = data.get("consumed", False)
        for p in data.get("phases", []):
            record = PhaseRecord(
                phase=ContemplationPhase[p["phase"]],
                started_at=p["started_at"],
                ended_at=p["ended_at"],
                notes=p["notes"],
            )
            obj.phases_completed.append(record)
        return obj


# ------------------------------------------------------------------------------
# Game-engine integration helpers
# ------------------------------------------------------------------------------

def require_contemplation_before_move(
    move_type: str, session: Optional[ContemplationSession]
) -> Dict[str, Any]:
    if not ContemplationSession.move_requires_contemplation(move_type):
        return {"required": False, "passed": True}
    if session is None:
        return {"required": True, "passed": False,
                "reason": f"Move '{move_type}' requires a completed ContemplationSession."}
    if not session.is_complete():
        return {"required": True, "passed": False,
                "reason": f"Session incomplete ({len(session.phases_completed)}/5 phases)."}
    return {"required": True, "passed": True, "depth": session.depth_score()}


def apply_contemplation_bonus(base_score: float, session: ContemplationSession) -> Dict[str, Any]:
    bonus = session.claim_bonus()
    if bonus is None:
        return {"final_score": base_score, "bonus_applied": False, "reason": "No valid bonus"}
    final = base_score * bonus["bonus_multiplier"] + bonus["bonus_points"]
    return {
        "final_score": round(final, 2),
        "bonus_applied": True,
        "base_score": base_score,
        "bonus_points": bonus["bonus_points"],
        "bonus_multiplier": bonus["bonus_multiplier"],
        "phrase": bonus["phrase"],
    }

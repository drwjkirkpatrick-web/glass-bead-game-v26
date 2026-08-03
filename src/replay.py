"""
glass-bead-game-v26 — Game Replay / Post-Mortem
Record sessions and replay with critical-moment detection.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class GameEvent:
    timestamp: int  # seconds
    move: str
    score: float
    phase: str


@dataclass
class CriticalMoment:
    timestamp: int
    reason: str


@dataclass
class GameRecording:
    events: List[GameEvent] = field(default_factory=list)
    critical_moments: List[CriticalMoment] = field(default_factory=list)

    def add_event(self, timestamp: int, move: str, score: float, phase: str):
        self.events.append(GameEvent(timestamp=timestamp, move=move, score=score, phase=phase))

    def detect_critical_moments(self):
        """Find score jumps > 0.3, contemplation events, synthesis discoveries."""
        self.critical_moments = []
        for i in range(1, len(self.events)):
            prev = self.events[i-1]
            curr = self.events[i]
            jump = curr.score - prev.score
            if jump > 0.3:
                self.critical_moments.append(CriticalMoment(
                    timestamp=curr.timestamp,
                    reason=f"Score jump +{(jump*100):.0f}% — {curr.phase}"
                ))
            if curr.phase == 'contemplation':
                self.critical_moments.append(CriticalMoment(
                    timestamp=curr.timestamp,
                    reason="Contemplation event — depth bonus applied"
                ))

    def get_timeline(self) -> List[Dict[str, Any]]:
        return [
            {"timestamp": e.timestamp, "move": e.move, "score": e.score, "phase": e.phase}
            for e in self.events
        ]

    def to_dict(self) -> dict:
        self.detect_critical_moments()
        return {
            "events": self.get_timeline(),
            "critical_moments": [
                {"timestamp": m.timestamp, "reason": m.reason}
                for m in self.critical_moments
            ],
        }

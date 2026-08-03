"""
Glass Bead Game v26 — Sonification Engine
Maps game state and moves into musical parameters.
"""
from typing import Dict, List, Any, Optional


class SonificationEngine:
    """Convert Glass Bead Game moves and state into musical notes."""

    # Domain → MIDI pitch mapping (C major pentatonic spread across octaves)
    DOMAIN_TO_PITCH = {
        'musica': 60,       # C4
        'mathematica': 64,  # E4
        'historia': 67,     # G4
        'natura': 72,       # C5
        'lingua': 76,       # E5
        'philosophia': 79,  # G5
        'technologia': 84,  # C6
        'medicina': 88,     # E6
    }

    BASE_BPM = 60

    def __init__(self, base_bpm: int = 60):
        self.base_bpm = base_bpm

    def sonify_move(self, from_domain: str, to_domain: str, confidence: float = 1.0) -> List[Dict[str, Any]]:
        """
        Generate a sequence of notes representing a move from one domain to another.
        Returns a list of note dicts with pitch, velocity, duration.
        """
        from_pitch = self.DOMAIN_TO_PITCH.get(from_domain, 60)
        to_pitch = self.DOMAIN_TO_PITCH.get(to_domain, 60)
        interval = abs(to_pitch - from_pitch)

        # Velocity scales with confidence (0.5–1.0)
        base_velocity = 0.5 + (confidence * 0.5)
        base_velocity = min(1.0, max(0.1, base_velocity))

        notes = [
            {
                'pitch': from_pitch,
                'velocity': round(base_velocity * 0.7, 2),
                'duration': round(1.0, 2),
            },
            {
                'pitch': to_pitch,
                'velocity': round(base_velocity * 0.9, 2),
                'duration': round(1.5, 2),
            },
            {
                'pitch': (from_pitch + to_pitch) // 2,
                'velocity': round(base_velocity * 0.6, 2),
                'duration': round(2.0, 2),
            },
        ]

        # Add a resolution tone if confidence is high
        if confidence >= 0.8:
            notes.append({
                'pitch': to_pitch + 12,
                'velocity': round(base_velocity * 0.5, 2),
                'duration': round(1.0, 2),
            })

        return notes

    def sonify_state(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an ambient drone based on active domains in the game state.
        Returns a dict with drone_pitch, bpm, active_domains.
        """
        nodes = game_state.get('nodes', [])
        if not nodes:
            return {
                'drone_pitch': 60,
                'bpm': self.base_bpm,
                'active_domains': [],
            }

        active_domains = list({n.get('domain') for n in nodes if n.get('domain')})
        pitches = [self.DOMAIN_TO_PITCH.get(d, 60) for d in active_domains]

        if pitches:
            drone_pitch = sum(pitches) // len(pitches)
        else:
            drone_pitch = 60

        # BPM rises slightly with graph density / number of active domains
        bpm = self.base_bpm + len(active_domains) * 3

        return {
            'drone_pitch': drone_pitch,
            'bpm': bpm,
            'active_domains': active_domains,
        }

    def get_bpm_for_move(self, from_domain: str, to_domain: str) -> int:
        """Calculate BPM for a move based on domain interval."""
        from_pitch = self.DOMAIN_TO_PITCH.get(from_domain, 60)
        to_pitch = self.DOMAIN_TO_PITCH.get(to_domain, 60)
        interval = abs(to_pitch - from_pitch)
        return self.base_bpm + interval * 2

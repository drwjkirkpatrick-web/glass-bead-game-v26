"""Critic module: CriticEngine for analyzing move quality."""

from typing import Dict, List, Any


class CriticEngine:
    """Analyzes a game move and returns a structured critique."""

    def analyze_move(self, move: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a move and return score, issues, suggestions, traffic_light."""
        score = 1.0
        issues: List[str] = []
        suggestions: List[str] = []

        # 1. Isomorphism confidence
        iso_conf = move.get("isomorphism_confidence", 0.0)
        if iso_conf < 0.7:
            issues.append("isomorphism_confidence below 0.7")
            suggestions.append("Strengthen isomorphism mapping.")
            score -= 0.4

        # 2. Language thread length
        language_thread = move.get("language_thread", "")
        if len(language_thread) <= 50:
            issues.append("language_thread too short (<= 50 chars)")
            suggestions.append("Expand language thread.")
            score -= 0.3

        # 3. Contemplation bonus
        if not move.get("has_contemplation_bonus", False):
            issues.append("missing contemplation_bonus")
            suggestions.append("Add contemplative depth.")
            score -= 0.2

        # 4. Antithesis present for dialectic moves
        move_type = move.get("type", "")
        if move_type == "dialectic" and not move.get("antithesis_present", False):
            issues.append("dialectic move missing antithesis")
            suggestions.append("Include antithesis in dialectic move.")
            score -= 0.3

        score = max(0.0, min(1.0, score))

        if score == 1.0:
            traffic_light = "green"
        elif score >= 0.5:
            traffic_light = "amber"
        else:
            traffic_light = "red"

        return {
            "score": round(score, 2),
            "issues": issues,
            "suggestions": suggestions,
            "traffic_light": traffic_light,
        }

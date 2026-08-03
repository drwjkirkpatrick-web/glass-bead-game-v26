"""
glass-bead-game-v26 — Dialectic Engine

Thesis ↔ Antithesis → Synthesis mechanic for the Glass Bead Game.

Grounded in Hermann Hesse's *Das Glasperlenspiel* (p. 1384–1386):
> "One school of players... favored harmoniously combining two hostile themes
> or ideas, such as law and freedom, individual and community. In such a Game
> the goal was to develop both themes or theses with complete equality and
> impartiality, to evolve out of thesis and antithesis the purest possible
> synthesis."

The dialectic is not mere compromise; it is the birth of an emergent concept
that transcends its parents while preserving their living tension.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class Thesis:
    """A single thematic strand — a move elevated into a world-view."""
    title: str
    domain: str
    core_idea: str
    keywords: List[str] = field(default_factory=list)
    move: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "domain": self.domain, "core_idea": self.core_idea, "keywords": self.keywords}


@dataclass
class Antithesis:
    """The hostile counter-theme. It must negate without destroying."""
    title: str
    domain: str
    core_idea: str
    opposition_axes: List[str] = field(default_factory=list)
    move: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "domain": self.domain, "core_idea": self.core_idea, "opposition_axes": self.opposition_axes}


@dataclass
class Synthesis:
    """The emergent third — neither A nor B, yet born of both."""
    title: str
    emergent_concept: str
    preserved_from_thesis: List[str] = field(default_factory=list)
    preserved_from_antithesis: List[str] = field(default_factory=list)
    language_thread: str = ""  # narrative arc: thesis → antithesis → synthesis
    scores: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "emergent_concept": self.emergent_concept,
            "preserved_from_thesis": self.preserved_from_thesis,
            "preserved_from_antithesis": self.preserved_from_antithesis,
            "language_thread": self.language_thread,
            "scores": self.scores,
        }


class DialecticScorer:
    """Hessean dialectic scoring: equality, tension, purity.

    * Equality — both themes developed with equal weight (0.0 → 1.0).
    * Tension — hostile concepts successfully reconciled (0.0 → 1.0).
    * Purity  — synthesis is not compromise but emergent concept (0.0 → 1.0).
    """

    @staticmethod
    def equality(thesis: Thesis, antithesis: Antithesis, synthesis: Synthesis) -> float:
        """Measure whether both parents are honored with equal weight."""
        w_t = len(synthesis.preserved_from_thesis)
        w_a = len(synthesis.preserved_from_antithesis)
        total = w_t + w_a
        if total == 0:
            return 0.0
        ratio = min(w_t, w_a) / max(w_t, w_a)
        return round(ratio, 4)

    @staticmethod
    def tension(thesis: Thesis, antithesis: Antithesis, synthesis: Synthesis) -> float:
        """Measure successful reconciliation of hostility.

        Heuristic: high when oppositional keywords / axes are preserved and the
        language_thread explicitly bridges thesis and antithesis.
        """
        t_kw = set(thesis.keywords)
        a_axes = set(antithesis.opposition_axes)
        preserved = set(synthesis.preserved_from_thesis + synthesis.preserved_from_antithesis)
        if not t_kw and not a_axes:
            return 0.5
        coverage = 0.0
        if t_kw:
            coverage += len(t_kw & preserved) / len(t_kw) * 0.5
        if a_axes:
            coverage += len(a_axes & preserved) / len(a_axes) * 0.5
        thread = synthesis.language_thread.lower()
        bridge = 0.15 if (thesis.title.lower() in thread and antithesis.title.lower() in thread) else 0.0
        return round(min(1.0, coverage + bridge), 4)

    @staticmethod
    def purity(thesis: Thesis, antithesis: Antithesis, synthesis: Synthesis) -> float:
        """Measure emergent novelty — is the synthesis more than a 50/50 mix?

        High lexical divergence of the emergent_concept from parent core_ideas,
        penalized for simple conjunctions in the title, rewarded for an explicit
        transformation arrow in the language_thread.
        """
        parent_text = (thesis.core_idea + " " + antithesis.core_idea).lower().split()
        emergent_words = set(synthesis.emergent_concept.lower().split())
        parent_words = set(parent_text)
        if not emergent_words or not parent_words:
            return 0.5
        overlap = len(emergent_words & parent_words)
        novelty = 1.0 - (overlap / len(emergent_words))
        title = synthesis.title.lower()
        penalty = 0.15 if (" and " in title or " or " in title or " versus " in title) else 0.0
        bonus = 0.1 if ("→" in synthesis.language_thread) else 0.0
        return round(max(0.0, min(1.0, novelty - penalty + bonus)), 4)

    @classmethod
    def score(cls, thesis: Thesis, antithesis: Antithesis, synthesis: Synthesis) -> Dict[str, float]:
        eq = cls.equality(thesis, antithesis, synthesis)
        te = cls.tension(thesis, antithesis, synthesis)
        pu = cls.purity(thesis, antithesis, synthesis)
        # Geometric mean: weakness in any dimension cannot be hidden.
        overall = round(math.pow(eq * te * pu, 1 / 3), 4) if (eq * te * pu) > 0 else 0.0
        return {"equality": eq, "tension": te, "purity": pu, "overall": overall}


class DialecticGame:
    """Builder that takes two Move-like objects and produces a scored Synthesis.

    Usage::
        thesis = Thesis(...)
        antithesis = Antithesis(...)
        game = DialecticGame(thesis, antithesis)
        synthesis = game.build_synthesis(title="...", emergent_concept="...")
        scores = game.score()
    """

    def __init__(self, thesis: Thesis, antithesis: Antithesis):
        self.thesis = thesis
        self.antithesis = antithesis
        self._synthesis: Optional[Synthesis] = None

    def build_synthesis(
        self,
        title: str,
        emergent_concept: str,
        preserved_from_thesis: Optional[List[str]] = None,
        preserved_from_antithesis: Optional[List[str]] = None,
        language_thread: str = "",
    ) -> Synthesis:
        """Construct the Synthesis and bind it to this game instance."""
        p_thesis = preserved_from_thesis or self.thesis.keywords[:]
        p_antithesis = preserved_from_antithesis or self.antithesis.opposition_axes[:]
        thread = language_thread or self._default_language_thread()
        self._synthesis = Synthesis(
            title=title,
            emergent_concept=emergent_concept,
            preserved_from_thesis=p_thesis,
            preserved_from_antithesis=p_antithesis,
            language_thread=thread,
        )
        return self._synthesis

    def _default_language_thread(self) -> str:
        return f"{self.thesis.title} → {self.antithesis.title} → synthesis"

    def score(self) -> Dict[str, float]:
        """Run the full dialectic scoring suite.

        Raises ValueError if build_synthesis() has not yet been called.
        """
        if self._synthesis is None:
            raise ValueError("Synthesis has not been built. Call build_synthesis() first.")
        scores = DialecticScorer.score(self.thesis, self.antithesis, self._synthesis)
        self._synthesis.scores = scores
        return scores

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the complete dialectic triad."""
        return {
            "thesis": self.thesis.to_dict(),
            "antithesis": self.antithesis.to_dict(),
            "synthesis": self._synthesis.to_dict() if self._synthesis else None,
        }

    @classmethod
    def from_moves(
        cls,
        thesis_move: Dict[str, Any],
        antithesis_move: Dict[str, Any],
        thesis_title: str = "Thesis",
        antithesis_title: str = "Antithesis",
    ) -> DialecticGame:
        """Factory for building a DialecticGame from raw game-engine Move dicts."""
        thesis = Thesis(
            title=thesis_title,
            domain=thesis_move.get("from_domain", "unknown"),
            core_idea=thesis_move.get("via", ""),
            keywords=thesis_move.get("keywords", []),
            move=thesis_move,
        )
        antithesis = Antithesis(
            title=antithesis_title,
            domain=antithesis_move.get("from_domain", "unknown"),
            core_idea=antithesis_move.get("via", ""),
            opposition_axes=antithesis_move.get("opposition_axes", []),
            move=antithesis_move,
        )
        return cls(thesis, antithesis)

"""
src/theme_engine.py

Bach-fugue compositional arc for Glass Bead Game moves.

Grounded in Hesse, *Das Glasperlenspiel* (Richard & Clara Winston trans.):
> "One theme, two themes, or three themes were stated, elaborated, varied,
> and underwent a development quite similar to that of the theme in a
> Bach fugue or a concerto movement."  (p. 1374-1375)

Compositional phases:
    THEME        — dux (subject): initial statement of a concept
    COUNTER-SUBJECT — comes: second concept enters in counterpoint
    EPISODE      — modulatory development exploring relations
    STRETTO      — overlapping/compressed restatement
    CODA         — peroratio: synthesis and resolution

API: Theme, CounterSubject, Episode, Stretto, Coda, FugueBuilder, FugueScorer
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import random

# ───────────────────────────────────────────────────────────────
# Data classes for each phase
# ───────────────────────────────────────────────────────────────

@dataclass
class Theme:
    """
    DUX — The subject stated in the tonic.
    The initial concept introduced onto the board.
    """
    text: str
    domain: str = "music"
    motifs: List[str] = field(default_factory=list)
    voice_id: int = 1

    def human_thread(self) -> str:
        motifs = ", ".join(self.motifs) if self.motifs else "a pure melodic line"
        return (
            f"Voice {self.voice_id} enters with the Theme in {self.domain}: "
            f"'{self.text}' — carrying {motifs}. "
            f"The game board receives its first symbolic bead."
        )


@dataclass
class CounterSubject:
    """
    COMES — The answering voice, usually in the dominant or a contrasting domain.
    Enters while the Theme continues, creating counterpoint.
    """
    text: str
    domain: str = "mathematics"
    against_motifs: List[str] = field(default_factory=list)
    voice_id: int = 2
    inversion: bool = False

    def human_thread(self) -> str:
        qualifier = "in inversion" if self.inversion else "in direct counterpoint"
        return (
            f"Voice {self.voice_id} answers with the CounterSubject in {self.domain} "
            f"{qualifier}: '{self.text}'. "
            f"The two voices interweave — thesis meets antithesis on the wire rows."
        )


@dataclass
class Episode:
    """
    MODULATORY PASSAGE — Free material that bridges and develops.
    Explores relationships between the Theme and CounterSubject domains.
    """
    text: str
    bridges: List[str] = field(default_factory=list)
    modulations: List[str] = field(default_factory=list)
    voice_ids: List[int] = field(default_factory=lambda: [1, 2])

    def human_thread(self) -> str:
        bridge = " → ".join(self.bridges) if self.bridges else "a wandering bridge"
        mod = ", ".join(self.modulations) if self.modulations else "several modulations"
        return (
            f"The voices release their hold on the fixed subjects and enter an Episode. "
            f"A bridge opens: {bridge}. "
            f"Through {mod}, the game explores the hidden kinship between the two ideas."
        )


@dataclass
class Stretto:
    """
    STRETTO — Overlapping entries of the subject in compressed time.
    The themes return in closer succession, creating density and climax.
    """
    entries: List[Dict[str, Any]] = field(default_factory=list)
    compression_ratio: float = 0.5

    def human_thread(self) -> str:
        count = len(self.entries)
        return (
            f"The Game tightens into Stretto — {count} overlapping entries "
            f"at {self.compression_ratio:.0%} density. "
            f"The themes no longer wait their turn; they collide and illuminate one another."
        )

    def add_entry(self, voice_id: int, text: str, domain: str, delay_beats: int):
        self.entries.append({
            "voice_id": voice_id,
            "text": text,
            "domain": domain,
            "delay_beats": delay_beats,
        })


@dataclass
class Coda:
    """
    PERORATIO / CODA — The synthesis and resolution.
    The scattered voices gather into a final chord of meaning.
    """
    text: str
    synthesis_domains: List[str] = field(default_factory=list)
    closing_motif: str = ""

    def human_thread(self) -> str:
        domains = " and ".join(self.synthesis_domains) if self.synthesis_domains else "all domains"
        return (
            f"The Coda arrives: '{self.text}'. "
            f"What began as separate voices in {domains} resolves into a single bead of meaning. "
            f"The players realize: {self.closing_motif or 'the eternal Atman shines through the glass.'}"
        )


# ───────────────────────────────────────────────────────────────
# Full move container
# ───────────────────────────────────────────────────────────────

@dataclass
class GlassBeadGameMove:
    """
    A complete Glass Bead Game move shaped like a Bach fugue.
    """
    move_id: str
    player: str
    theme: Theme
    counter_subject: CounterSubject
    episode: Episode
    stretto: Stretto
    coda: Coda
    score: Dict[str, float] = field(default_factory=dict)
    total_score: float = 0.0

    def narrate(self) -> str:
        parts = [
            f"—— Move {self.move_id} by {self.player} ——",
            self.theme.human_thread(),
            self.counter_subject.human_thread(),
            self.episode.human_thread(),
            self.stretto.human_thread(),
            self.coda.human_thread(),
            f"—— Total score: {self.total_score:.2f} ——",
        ]
        return "\n\n".join(parts)


# ───────────────────────────────────────────────────────────────
# Scoring engine
# ───────────────────────────────────────────────────────────────

class FugueScorer:
    """
    Castalian scoring for each fugue phase.

    Dimensions (from Hesse / the book's implicit aesthetic):
        elegance     — clarity of statement
        fertility    — generative richness, how many connections a phase yields
        surprise     — unexpected cross-domain resonance
        recursion    — self-referential depth
        realization  — spiritual / epistemic depth (the book's "realizing")
    """

    DIMENSIONS = ["elegance", "fertility", "surprise", "recursion", "realization"]

    def score_theme(self, theme: Theme) -> Dict[str, float]:
        """Subject stated cleanly in its home domain."""
        return {
            "elegance": 0.7 + (0.15 if theme.motifs else 0.0),
            "fertility": 0.5 + 0.1 * len(theme.motifs),
            "surprise": 0.3,
            "recursion": 0.2,
            "realization": 0.4,
        }

    def score_counter_subject(self, cs: CounterSubject) -> Dict[str, float]:
        """Answering voice; inversion and contrast add surprise."""
        return {
            "elegance": 0.6,
            "fertility": 0.5 + 0.1 * len(cs.against_motifs),
            "surprise": 0.5 + (0.2 if cs.inversion else 0.0) + (0.2 if cs.domain != "music" else 0.0),
            "recursion": 0.3,
            "realization": 0.5,
        }

    def score_episode(self, ep: Episode) -> Dict[str, float]:
        """Free development; bridges and modulations add fertility."""
        return {
            "elegance": 0.5,
            "fertility": 0.4 + 0.15 * len(ep.bridges),
            "surprise": 0.4 + 0.1 * len(ep.modulations),
            "recursion": 0.3 + 0.05 * len(ep.bridges),
            "realization": 0.5 + 0.1 * len(ep.modulations),
        }

    def score_stretto(self, st: Stretto) -> Dict[str, float]:
        """Overlapping entries; compression and density raise the stakes."""
        return {
            "elegance": 0.4 + 0.3 * st.compression_ratio,
            "fertility": 0.6,
            "surprise": 0.5 + 0.1 * len(st.entries),
            "recursion": 0.4 + 0.2 * st.compression_ratio,
            "realization": 0.6 + 0.1 * len(st.entries),
        }

    def score_coda(self, coda: Coda) -> Dict[str, float]:
        """Resolution; synthesis of all preceding voices."""
        return {
            "elegance": 0.8,
            "fertility": 0.3,
            "surprise": 0.4 + (0.2 if len(coda.synthesis_domains) > 1 else 0.0),
            "recursion": 0.6,
            "realization": 0.7 + 0.1 * len(coda.synthesis_domains),
        }

    def score_move(self, move: GlassBeadGameMove) -> Dict[str, float]:
        """Aggregate scores across all phases, clamped to [0, 1]."""
        phase_scores = {
            "theme": self.score_theme(move.theme),
            "counter_subject": self.score_counter_subject(move.counter_subject),
            "episode": self.score_episode(move.episode),
            "stretto": self.score_stretto(move.stretto),
            "coda": self.score_coda(move.coda),
        }

        totals: Dict[str, float] = {d: 0.0 for d in self.DIMENSIONS}
        for ps in phase_scores.values():
            for dim in self.DIMENSIONS:
                totals[dim] += ps.get(dim, 0.0)

        # Average across 5 phases, clamp
        for dim in self.DIMENSIONS:
            totals[dim] = round(min(totals[dim] / 5.0, 1.0), 3)

        move.score = totals
        move.total_score = round(sum(totals.values()), 3)
        return totals


# ───────────────────────────────────────────────────────────────
# Builder
# ───────────────────────────────────────────────────────────────

class FugueBuilder:
    """
    Assembles a GlassBeadGameMove from its five fugue phases.

    Usage:
        builder = FugueBuilder(player="Knecht")
        builder.set_theme("The Golden Ratio in phyllotaxis", domain="mathematics")
        builder.set_counter_subject("A Bach canon in retrograde", domain="music", inversion=True)
        builder.add_episode_bridge("music → mathematics → nature")
        builder.add_stretto_entry("The spiral unites both", "philosophy", voice_id=3)
        builder.set_coda("Beauty is the perception of the eternal pattern.")
        move = builder.build()
    """

    _id_counter: int = 0

    def __init__(self, player: str = "Anonymous"):
        FugueBuilder._id_counter += 1
        self.move_id = f"mv_{FugueBuilder._id_counter}_{random.randint(1000,9999)}"
        self.player = player
        self._theme: Optional[Theme] = None
        self._counter: Optional[CounterSubject] = None
        self._episode: Optional[Episode] = None
        self._stretto: Optional[Stretto] = None
        self._coda: Optional[Coda] = None
        self._scorer = FugueScorer()

    # --- fluent setters ---

    def set_theme(self, text: str, domain: str = "music", motifs: Optional[List[str]] = None) -> "FugueBuilder":
        self._theme = Theme(text=text, domain=domain, motifs=motifs or [])
        return self

    def set_counter_subject(
        self,
        text: str,
        domain: str = "mathematics",
        against_motifs: Optional[List[str]] = None,
        inversion: bool = False,
    ) -> "FugueBuilder":
        self._counter = CounterSubject(
            text=text, domain=domain, against_motifs=against_motifs or [], inversion=inversion
        )
        return self

    def set_episode(
        self,
        text: str,
        bridges: Optional[List[str]] = None,
        modulations: Optional[List[str]] = None,
    ) -> "FugueBuilder":
        self._episode = Episode(text=text, bridges=bridges or [], modulations=modulations or [])
        return self

    def add_episode_bridge(self, bridge: str) -> "FugueBuilder":
        if self._episode is None:
            self._episode = Episode(text="", bridges=[], modulations=[])
        self._episode.bridges.append(bridge)
        return self

    def set_stretto(self, compression_ratio: float = 0.5) -> "FugueBuilder":
        self._stretto = Stretto(compression_ratio=max(0.0, min(1.0, compression_ratio)))
        return self

    def add_stretto_entry(self, text: str, domain: str, voice_id: int, delay_beats: int = 0) -> "FugueBuilder":
        if self._stretto is None:
            self._stretto = Stretto()
        self._stretto.add_entry(voice_id=voice_id, text=text, domain=domain, delay_beats=delay_beats)
        return self

    def set_coda(self, text: str, synthesis_domains: Optional[List[str]] = None, closing_motif: str = "") -> "FugueBuilder":
        self._coda = Coda(text=text, synthesis_domains=synthesis_domains or [], closing_motif=closing_motif)
        return self

    # --- build ---

    def build(self) -> GlassBeadGameMove:
        if not all([self._theme, self._counter, self._episode, self._stretto, self._coda]):
            missing = []
            if self._theme is None:
                missing.append("theme")
            if self._counter is None:
                missing.append("counter_subject")
            if self._episode is None:
                missing.append("episode")
            if self._stretto is None:
                missing.append("stretto")
            if self._coda is None:
                missing.append("coda")
            raise ValueError(f"Incomplete fugue move; missing phases: {missing}")

        move = GlassBeadGameMove(
            move_id=self.move_id,
            player=self.player,
            theme=self._theme,
            counter_subject=self._counter,
            episode=self._episode,
            stretto=self._stretto,
            coda=self._coda,
        )
        self._scorer.score_move(move)
        return move

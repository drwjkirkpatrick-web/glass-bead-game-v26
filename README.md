# Glass Bead Game v26

**A 3D knowledge graph visualization of the Modern Glass Bead Game.**

> "The Glass Bead Game is thus a mode of playing with the total contents and values of our culture; it plays with them as, say, in the great age of the arts a painter might have played with the colours on his palette."
> — Hermann Hesse, *The Glass Bead Game* (1943)

---

## What It Is

The Glass Bead Game was Hesse's vision of a universal synthesizing discipline — a formal system through which philosophy, mathematics, music, science, and art are perceived as aspects of a single underlying structure. Players find hidden correspondences between existing things. A theme from Bach mirrors a proof in topology. A passage of Confucian thought resonates with a theorem in physics.

This Modern Glass Bead Game translates that vision into a playable web experience where **Hermes agents serve as glass beads** and **LLMs embody the cumulative knowledge substrate**.

---

## What the Book Actually Says About the Game

Hesse described the game with precision that often surprises modern readers. Here are the known properties from the text:

> "These rules, the sign language and grammar of the Game, constitute a kind of highly developed secret language drawing upon several sciences and arts, **but especially mathematics and music** (and/or musicology), and capable of expressing and establishing interrelationships between the content and conclusions of nearly all scholarly disciplines."

### Known Rules from the Novel

1. **Mathematics and music are the twin foundations.** The grammar of the game draws primarily upon these two disciplines. All other fields are expressible within this grammar, but math and music supply its syntax.

2. **It is a *secret language*, not merely a metaphor.** The game has a formal grammar, a notation system, and a vocabulary. Moves are not free-association; they are structured passages between concepts encoded in this shared tongue.

3. **The player proceeds by making deep connections between seemingly unrelated topics.** The game "proceeds by players making deep connections between seemingly unrelated topics" (Wikipedia summarizing Hesse). Surface similarity is rejected; structural correspondence is required.

4. **Years of hard study are required.** Music, mathematics, and cultural history must all be mastered before one can play well. The game is not casual entertainment but the culmination of a Castalian education.

5. **It is an abstract synthesis of all arts and sciences.** The game does not favor one domain over another. Its goal is to perceive unity where convention sees only separation.

6. **The setting is Castalia — a province reserved for the life of the mind.** Technology and economic life are held to a strict minimum. The game flourishes in conditions of contemplative withdrawal.

7. **Players advance through a hierarchy:** Novice → Student → Adept → Magister → Magister Ludi. Promotion requires verified move quality, peer endorsement, and demonstrated novelty.

8. **The game carries an existential warning.** The protagonist Joseph Knecht ultimately leaves Castalia, recognizing that pure contemplation without engagement with life becomes sterile. The game must not become a sealed chamber.

---

## Quick Start

```bash
cd glass-bead-game-v26
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:9297/` in your browser.

---

## Architecture

| Layer | Technology |
|-------|-----------|
| Backend | Flask + Flask-SocketIO + SQLite |
| 3D Scene | Three.js r160 (glass materials, starfield, grid) |
| Music | VexFlow 4.x (SVG staff notation) |
| Math | KaTeX 0.16.9 (LaTeX formula rendering) |
| Live Updates | WebSocket broadcasts via SocketIO rooms |
| Styling | CSS glassmorphism, JetBrains Mono, dark terminal |

---

## Dashboards

- **`/`** — Main 3D visualization with live terminal and quick move input
- **`/gameplay`** — Active move submission with bead selector and validation feedback
- **`/judges`** — Scoring rubric, validation queue, Castalian flags, promotion table
- **`/audience`** — Read-only view with scoreboard and move feed

---

## Game Mechanics

A **move** connects two concepts across disciplinary boundaries:

```
Bead: Magister Musicae
From: Bach's "Musical Offering", Canon per tonos
To: Möbius strip topology
Via: "A structure that returns to itself transformed"
Resonance: "Both are paradoxes of locality"
```

Moves are scored on four aesthetic dimensions:
- **Elegance** — minimal beads, maximum conceptual distance
- **Fertility** — new moves unlocked
- **Surprise** — crossings across >3 domains
- **Recursion** — self-referential depth

---

## The Ten Prompt Components

The `prompts/` directory contains testable LLM prompt templates for each game component:

1. `board-knowledge-graph.md` — Knowledge graph generation
2. `bead-agents.md` — Hermes agent bead responses
3. `move-validation.md` — Move structural validation
4. `audio-sonification.md` — Web Audio API sonification
5. `scoring-aesthetic.md` — Aesthetic scoring rubric
6. `game-modes.md` — Open, Contested, and Knecht Challenge modes
7. `castalian-hierarchy.md` — Rank progression evaluation
8. `llm-cultural-memory.md` — Librarian / skeptic / translator
9. `knecht-protocol.md` — Castalian flagging and utility check
10. `opening-move.md` — Sample canonical opening

See `PROMPT_REFINEMENTS.md` for 30 book-grounded updates to prompt nuance.

---

## The Hessean Warning

> "People know, or dimly feel, that if thinking is not kept pure and keen, and if respect for the world of mind is no longer operative, ships and automobiles will soon cease to run right, the engineer's slide rule and the computations of banks and stock exchanges will forfeit validity and authority, and chaos will ensue."
>
> — Hermann Hesse

As Joseph Knecht discovered, the most beautiful formal system in the world cannot replace engagement with practical life. The game must not become a sealed chamber. Every third session triggers the **Knecht Protocol**: if no practical application is identified, the session is flagged as *Castalian* — beautiful but existentially empty. True wisdom, as the Master tells Joseph, is lived, not taught.

---

## License

MIT — for the love of synthesis.

---

> "There is truth, my boy. But the doctrine you desire, absolute, perfect dogma that alone provides wisdom, does not exist. Nor should you long for a perfect doctrine, my friend. Rather, you should long for the perfection of yourself. The deity is within you, not in ideas and books. Truth is lived, not taught."
>
> — Hermann Hesse, *The Glass Bead Game*

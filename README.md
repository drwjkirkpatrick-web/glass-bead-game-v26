# Glass Bead Game v26

**A 3D knowledge graph visualization of the Modern Glass Bead Game.**

Inspired by Hermann Hesse's *Magister Ludi* (1943), this project realizes the Glass Bead Game as a live, interactive web application where Hermes agents serve as glass beads and LLMs embody the cumulative knowledge substrate.

---

## What It Is

The Glass Bead Game was Hesse's vision of a universal synthesizing discipline — a formal system through which philosophy, mathematics, music, science, and art are perceived as aspects of a single underlying structure. Players find hidden correspondences between existing things. A theme from Bach mirrors a proof in topology. A passage of Confucian thought resonates with a theorem in physics.

This Modern Glass Bead Game translates that vision into a playable web experience with:

- **3D glass bead visualization** — nodes as luminous icosahedra in deep space
- **Native music notation** — VexFlow-rendered SVG scores for every move
- **Native math notation** — KaTeX-rendered formulas for structural properties
- **Live-updating dashboards** — audience, gameplay, and judges views via WebSocket
- **Castalian hierarchy** — rank progression from Novice to Magister Ludi
- **Knecht Protocol** — every third session must demonstrate practical application

## Quick Start

```bash
cd glass-bead-game-v26
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:9297/` in your browser.

## Architecture

| Layer | Technology |
|-------|-----------|
| Backend | Flask + Flask-SocketIO + SQLite |
| 3D Scene | Three.js r160 (glass materials, starfield, grid) |
| Music | VexFlow 4.x (SVG staff notation) |
| Math | KaTeX 0.16.9 (LaTeX formula rendering) |
| Live Updates | WebSocket broadcasts via SocketIO rooms |
| Styling | CSS glassmorphism, JetBrains Mono, dark terminal |

## Dashboards

- **`/`** — Main 3D visualization with live terminal and quick move input
- **`/gameplay`** — Active move submission with bead selector and validation feedback
- **`/judges`** — Scoring rubric, validation queue, Castalian flags, promotion table
- **`/audience`** — Read-only view with scoreboard and move feed

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

## The Hessean Warning

As Joseph Knecht discovered, the most beautiful formal system in the world did not stop the bombs. The game must not become a sealed chamber. Every third session triggers the **Knecht Protocol**: if no practical application is identified, the session is flagged as *Castalian* — beautiful but existentially empty.

## License

MIT — for the love of synthesis.

---

*"The Glass Bead Game is thus a mode of playing with the total contents and values of our culture."* — Hermann Hesse

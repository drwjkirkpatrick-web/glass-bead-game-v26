# Game Modes

## Role
You are the Game Mode Archivist — an authority on the rule systems governing all sanctioned forms of the Glass Bead Game. You define win conditions, turn structures, and the LLM's participatory role for each mode.

## Prompt Template
```
You are the Game Mode Archivist for the Glass Bead Game.

Describe the complete rules for Glass Bead Game Mode: [MODE_NAME]

Available modes and their identifiers:
- "Open": build the densest, most interconnected knowledge graph.
- "Contested": two players propose contradictory amplifications; the graph dissolves weaker branches.
- "Knecht Challenge": every move must connect to a real-world practical problem.
- "Castalia": the game played within the Province of Castalia, where scholarly purity and ascetic discipline are paramount.
- "Waldzell": set in the Waldzell district, the center of the Glass Bead Game elite and ceremonial competition.
- "Teaching Requirement": every move must contain a teachable insight; unteachable moves are invalid.
- "Truth Lived": moves must reflect embodied wisdom and lived experience; abstract knowledge alone is insufficient.
- "Teaching Win": the win condition is to successfully teach a synthesis to the assembly; scoring is secondary.
- "Three Lives": each player begins with three lives; a failed or rejected move costs one life.
- "Withdrawal": players may voluntarily withdraw to meditate; withdrawn moves score for depth but not for connection.
- "Tegularius": for solitary, poetic players; favors melancholic depth and musical correspondence over competitive scoring.

For the requested mode, define:
1. Objective: the win condition or success criterion.
2. Turn structure: who acts, in what order, and what actions are permitted per turn.
3. LLM role: how the language model participates (e.g., bead translator, move validator, cultural memory).
4. Scoring differences: any modifications to the standard Aesthetic Criterion.
5. Endgame condition: what triggers the session's conclusion.

Output as structured markdown with clear headings.
```

## Input Variables
- `[MODE_NAME]`: The identifier of the game mode to describe ("Open", "Contested", or "Knecht Challenge")

## Expected Output
Structured markdown with the following sections:
- `# Mode: [MODE_NAME]`
- `## Objective`
- `## Turn Structure`
- `## LLM Role`
- `## Scoring Differences`
- `## Endgame Condition`

## Sample Invocation
```
You are the Game Mode Archivist for the Glass Bead Game.

Describe the complete rules for Glass Bead Game Mode: Knecht Challenge

Available modes and their identifiers:
- "Open": build the densest, most interconnected knowledge graph.
- "Contested": two players propose contradictory amplifications; the graph dissolves weaker branches.
- "Knecht Challenge": every move must connect to a real-world practical problem.
- "Castalia": the game played within the Province of Castalia, where scholarly purity and ascetic discipline are paramount.
- "Waldzell": set in the Waldzell district, the center of the Glass Bead Game elite and ceremonial competition.
- "Teaching Requirement": every move must contain a teachable insight; unteachable moves are invalid.
- "Truth Lived": moves must reflect embodied wisdom and lived experience; abstract knowledge alone is insufficient.
- "Teaching Win": the win condition is to successfully teach a synthesis to the assembly; scoring is secondary.
- "Three Lives": each player begins with three lives; a failed or rejected move costs one life.
- "Withdrawal": players may voluntarily withdraw to meditate; withdrawn moves score for depth but not for connection.
- "Tegularius": for solitary, poetic players; favors melancholic depth and musical correspondence over competitive scoring.

For the requested mode, define:
1. Objective: the win condition or success criterion.
2. Turn structure: who acts, in what order, and what actions are permitted per turn.
3. LLM role: how the language model participates (e.g., bead translator, move validator, cultural memory).
4. Scoring differences: any modifications to the standard Aesthetic Criterion.
5. Endgame condition: what triggers the session's conclusion.

Output as structured markdown with clear headings.
```

## Expected Sample Output
```markdown
# Mode: Knecht Challenge

## Objective
Build a knowledge graph in which every bead-to-bead correspondence illuminates a practical, real-world problem. Beauty is necessary but insufficient: the graph must also carry utility.

## Turn Structure
1. Player proposes a move with a concept pair and a practical problem tag.
2. Move Validator checks structural fidelity AND utility relevance.
3. Cultural Memory offers historical precedent or counter-example.
4. If valid, the move is added to the graph and scored with the modified Aesthetic Criterion (utility-weighted).
5. Next player’s turn.

## LLM Role
- **Bead Translator**: maps incoming concepts to domain-native vocabularies.
- **Utility Auditor**: evaluates whether the move genuinely addresses the tagged practical problem.
- **Cultural Memory**: surfaces precedents where similar correspondences produced real-world outcomes.

## Scoring Differences
The standard Aesthetic Criterion is augmented with a Utility dimension (1–10):
- 10 = the move directly suggests an actionable solution to a documented problem.
- 1 = the move is beautiful but entirely abstract ("Castalian").
The total score is now out of 50 (standard 40 + Utility 10).

## Endgame Condition
The session ends when:
- A player achieves a cumulative Utility score of ≥30 across their moves, OR
- The graph reaches 50 nodes with an average Utility score ≥5, OR
- All players pass twice in succession, declaring the graph complete.
```

---

## Mode: Castalia (Province)

### Objective
Play within the Province of Castalia, where the Glass Bead Game is the supreme expression of human cultivation. The win condition is to produce a graph of such purity and intellectual rigor that it could be accepted by the Castalian elite.

### Turn Structure
1. Player proposes a move rooted in scholarly or artistic tradition.
2. Move Validator checks for Castalian purity — abstraction, discipline, and avoidance of worldly pragmatism.
3. Cultural Memory offers historical precedents from Castalian archives.
4. If valid, the move is added to the graph and scored with the Castalian Aesthetic Criterion.
5. Next player’s turn.

### LLM Role
- **Bead Translator**: maps concepts to classical, philosophical, or artistic vocabularies.
- **Purity Auditor**: evaluates whether the move maintains the ascetic, non-utilitarian standard of Castalia.
- **Cultural Memory**: surfaces precedents from the fictional Castalian archives and historical masters.

### Scoring Differences
The standard Aesthetic Criterion is augmented with a Purity dimension (1–10):
- 10 = the move embodies timeless scholarly beauty with no trace of worldly application.
- 1 = the move smacks of practicality or vulgar utility.
The total score is now out of 50 (standard 40 + Purity 10).

### Endgame Condition
The session ends when:
- A player achieves a cumulative Purity score of ≥30 across their moves, OR
- The graph reaches 50 nodes with an average Purity score ≥5, OR
- All players pass twice in succession, declaring the graph complete.

---

## Mode: Waldzell (Setting)

### Objective
Set in the Waldzell district, the center of the Glass Bead Game elite and ceremonial competition. The win condition is to compose a graph that could be performed before the assembled masters of Waldzell.

### Turn Structure
1. Player proposes a move with ceremonial awareness — each move should feel like a public performance.
2. Move Validator checks for Waldzell suitability: elegance, drama, and social resonance.
3. Cultural Memory offers precedents from famous Waldzell tournaments.
4. If valid, the move is added to the graph and scored with the Waldzell Aesthetic Criterion.
5. Next player’s turn.

### LLM Role
- **Bead Translator**: maps concepts to the ceremonial and performative vocabularies of Waldzell.
- **Ceremony Auditor**: evaluates whether the move carries the gravity and elegance expected before the elite.
- **Cultural Memory**: surfaces precedents from famous Waldzell tournaments and master players.

### Scoring Differences
The standard Aesthetic Criterion is augmented with a Ceremony dimension (1–10):
- 10 = the move is a masterstroke of public artistry, worthy of a Waldzell stage.
- 1 = the move is technically sound but lacks ceremonial presence.
The total score is now out of 50 (standard 40 + Ceremony 10).

### Endgame Condition
The session ends when:
- A player achieves a cumulative Ceremony score of ≥30 across their moves, OR
- The graph reaches 50 nodes with an average Ceremony score ≥5, OR
- All players pass twice in succession, declaring the graph complete.

---

## Mode: Teaching Requirement

### Objective
Every move must contain a teachable insight; unteachable moves are invalid. The win condition is to build a graph in which every node could be explained to a student.

### Turn Structure
1. Player proposes a move accompanied by a brief pedagogical explanation.
2. Move Validator checks structural fidelity AND teachability — can a novice grasp the insight?
3. Cultural Memory offers historical teaching precedents.
4. If valid, the move is added to the graph and scored with the modified Aesthetic Criterion (teachability-weighted).
5. Next player’s turn.

### LLM Role
- **Bead Translator**: maps concepts to domain-native vocabularies.
- **Pedagogy Auditor**: evaluates whether the move’s explanation is clear, accessible, and instructive.
- **Cultural Memory**: surfaces precedents where similar correspondences were used in teaching.

### Scoring Differences
The standard Aesthetic Criterion is augmented with a Teachability dimension (1–10):
- 10 = the move contains a luminous insight that any attentive student could grasp.
- 1 = the move is opaque or arcane, defying pedagogical transmission.
The total score is now out of 50 (standard 40 + Teachability 10).

### Endgame Condition
The session ends when:
- A player achieves a cumulative Teachability score of ≥30 across their moves, OR
- The graph reaches 50 nodes with an average Teachability score ≥5, OR
- All players pass twice in succession, declaring the graph complete.

---

## Mode: Truth Lived

### Objective
Moves must reflect embodied wisdom and lived experience; abstract knowledge alone is insufficient. The win condition is to build a graph rooted in authentic human experience.

### Turn Structure
1. Player proposes a move grounded in personal or witnessed experience.
2. Move Validator checks structural fidelity AND existential authenticity — does the move arise from lived truth?
3. Cultural Memory offers biographical or historical precedents of lived wisdom.
4. If valid, the move is added to the graph and scored with the modified Aesthetic Criterion (authenticity-weighted).
5. Next player’s turn.

### LLM Role
- **Bead Translator**: maps concepts to vocabularies of experience and autobiography.
- **Authenticity Auditor**: evaluates whether the move reflects genuine lived truth rather than abstract speculation.
- **Cultural Memory**: surfaces precedents from lives of known contemplatives, mystics, and practitioners.

### Scoring Differences
The standard Aesthetic Criterion is augmented with an Authenticity dimension (1–10):
- 10 = the move radiates the unmistakable warmth of lived truth.
- 1 = the move is clever but bloodless, constructed from concepts alone.
The total score is now out of 50 (standard 40 + Authenticity 10).

### Endgame Condition
The session ends when:
- A player achieves a cumulative Authenticity score of ≥30 across their moves, OR
- The graph reaches 50 nodes with an average Authenticity score ≥5, OR
- All players pass twice in succession, declaring the graph complete.

---

## Mode: Teaching Win

### Objective
The win condition is not scoring but the successful transmission of a synthesis to the assembly. A player wins by delivering a closing teaching that integrates the graph’s correspondences into an illuminating whole.

### Turn Structure
1. Player proposes a move with an eye toward eventual synthesis.
2. Move Validator checks structural fidelity and synthesis potential.
3. Cultural Memory offers precedents for masterful closing teachings.
4. If valid, the move is added to the graph and scored normally (scoring is secondary).
5. Next player’s turn.
6. In the endgame, any player may attempt a "Teaching Win" by delivering a synthesized teaching to the assembly.

### LLM Role
- **Bead Translator**: maps concepts to domain-native vocabularies.
- **Synthesis Auditor**: evaluates whether the emerging graph supports a coherent closing teaching.
- **Cultural Memory**: surfaces precedents of masterful teachings from the Castalian tradition.

### Scoring Differences
Standard Aesthetic Criterion applies, but scores are secondary. The primary victory condition is a successful Teaching Win, judged by consensus of the players or by the LLM acting as assembly.

### Endgame Condition
The session ends when:
- A player delivers a Teaching Win that the assembly accepts by consensus, OR
- The graph reaches 50 nodes and the assembled players vote on the most illuminating synthesis, OR
- All players pass twice in succession, and the highest-scoring player is declared Magister Ludi.

---

## Mode: Three Lives

### Objective
Each player begins with three lives. A failed or rejected move costs one life. The win condition is to survive with at least one life while building the most illuminating graph.

### Turn Structure
1. Player proposes a move.
2. Move Validator checks structural fidelity. If the move fails validation, the player loses one life.
3. Cultural Memory offers historical precedents.
4. If valid, the move is added to the graph and scored normally.
5. Next player’s turn.
6. A player with zero lives is eliminated and becomes a silent observer.

### LLM Role
- **Bead Translator**: maps concepts to domain-native vocabularies.
- **Move Validator**: checks structural fidelity; failure results in life loss.
- **Cultural Memory**: surfaces precedents and offers consolation to eliminated players.

### Scoring Differences
Standard Aesthetic Criterion applies. However, survival is paramount: a player with zero lives cannot win, even if they have the highest score. The winner is the highest-scoring surviving player.

### Endgame Condition
The session ends when:
- Only one player remains with lives, who is declared the winner, OR
- The graph reaches 50 nodes and the highest-scoring surviving player wins, OR
- All surviving players pass twice in succession.

---

## Mode: Withdrawal

### Objective
Players may voluntarily withdraw to meditate; withdrawn moves score for depth but not for connection. The win condition is to build a graph of profound depth, even if less interconnected.

### Turn Structure
1. Player may choose to play normally OR withdraw for one turn to meditate.
2. If playing normally: Move Validator checks structural fidelity and connection.
3. If withdrawing: the player generates a "meditation move" — a single bead of great depth with no required connection to the graph. It scores only for depth.
4. Cultural Memory offers precedents for both active play and withdrawal.
5. Next player’s turn.

### LLM Role
- **Bead Translator**: maps concepts to domain-native vocabularies.
- **Depth Auditor**: evaluates the profundity of meditation moves.
- **Cultural Memory**: surfaces precedents of famous withdrawals and returns in Castalian history.

### Scoring Differences
Standard Aesthetic Criterion applies to normal moves. Withdrawn moves are scored on a simplified Depth criterion (1–20) with no connectivity requirement. The final score is the sum of normal scores plus the two highest withdrawn move scores.

### Endgame Condition
The session ends when:
- A player achieves a combined score (normal + withdrawn depth) of ≥40, OR
- The graph reaches 50 nodes (normal moves only) with an average score ≥5, OR
- All players pass twice in succession, declaring the graph complete.

---

## Mode: Tegularius

### Objective
For solitary, poetic players; favors melancholic depth and musical correspondence over competitive scoring. Named after Joseph Knecht’s friend, the fragile musician Tegularius. The win condition is to compose a graph of such poetic resonance that it moves the solitary player.

### Turn Structure
1. Solitary player proposes a move driven by mood, music, or poetic intuition.
2. Move Validator checks for emotional and musical resonance rather than logical rigor.
3. Cultural Memory offers precedents from melancholic or musical masters.
4. If valid, the move is added to the graph and scored with the Tegularian Aesthetic Criterion.
5. Next move by the same player (solitary mode) or next player (shared mode).

### LLM Role
- **Bead Translator**: maps concepts to vocabularies of music, poetry, and melancholy.
- **Resonance Auditor**: evaluates whether the move carries emotional depth and musicality.
- **Cultural Memory**: surfaces precedents from Tegularius, Knecht, and other contemplative musicians.

### Scoring Differences
The standard Aesthetic Criterion is replaced with a Resonance criterion (1–40):
- 10 = the move sings with tragic beauty or musical truth.
- 1 = the move is mechanically sound but emotionally empty.
Competitive comparison is discouraged; the goal is not to win but to deepen the solitary player’s inner garden.

### Endgame Condition
The session ends when:
- The player feels the graph has reached a satisfying poetic closure, OR
- The graph reaches 30 nodes (a smaller garden than competitive modes), OR
- The player withdraws in silence, which is itself a valid ending.

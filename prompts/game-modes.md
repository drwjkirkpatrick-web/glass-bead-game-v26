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

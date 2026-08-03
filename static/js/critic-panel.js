/**
 * Hermes Move Critic Panel
 * Pre-submission AI critic with traffic-light scoring.
 */

(function() {
    'use strict';

    const CriticPanel = {
        container: null,

        init(containerId) {
            this.container = document.getElementById(containerId);
            if (!this.container) return;
            this._buildUI();
        },

        _buildUI() {
            this.container.innerHTML = `
                <div class="critic-header">
                    <span class="critic-title">HERMES CRITIC</span>
                    <span class="critic-subtitle">Pre-submission analysis</span>
                </div>
                <div class="critic-score" id="critic-score">
                    <div class="traffic-light" id="traffic-light">●</div>
                    <div class="score-value" id="critic-score-val">—</div>
                </div>
                <div class="critic-issues" id="critic-issues"></div>
                <div class="critic-suggestions" id="critic-suggestions"></div>
                <button class="critic-submit-anyway" id="critic-submit-anyway" disabled>Submit Anyway</button>
            `;
        },

        async analyze(moveData) {
            document.getElementById('critic-score-val').textContent = 'Analyzing...';
            document.getElementById('traffic-light').className = 'traffic-light analyzing';

            try {
                const resp = await fetch('/api/critic/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(moveData),
                });
                const result = await resp.json();
                this._render(result);
            } catch (e) {
                // Fallback heuristic analysis
                const issues = [];
                const suggestions = [];
                let score = 1.0;
                let color = 'green';

                if (!moveData.structural_property || moveData.structural_property.length < 20) {
                    issues.push('Structural property is too vague.');
                    suggestions.push('State the correspondence as a formal rule, not a metaphor.');
                    score -= 0.3; color = 'yellow';
                }
                if (!moveData.resonance || moveData.resonance.length < 30) {
                    issues.push('Resonance sentence is missing or too short.');
                    suggestions.push('Add a single luminous sentence that bridges the two domains.');
                    score -= 0.2; if (color === 'green') color = 'yellow';
                }
                if (!moveData.isomorphisms || moveData.isomorphisms.length === 0) {
                    issues.push('No isomorphism from the catalog was matched.');
                    suggestions.push('Check your move against the 10 core isomorphisms.');
                    score -= 0.3; color = 'red';
                }

                this._render({score: Math.max(0, score), issues, suggestions, traffic_light: color});
            }
        },

        _render(result) {
            const light = document.getElementById('traffic-light');
            light.className = 'traffic-light ' + (result.traffic_light || 'green');
            light.textContent = '●';

            document.getElementById('critic-score-val').textContent = (result.score * 100).toFixed(0) + '%';

            const issuesEl = document.getElementById('critic-issues');
            issuesEl.innerHTML = (result.issues || []).map(i => `<div class="critic-issue">⚠ ${i}</div>`).join('') || '<div class="critic-ok">✓ No issues found</div>';

            const sugEl = document.getElementById('critic-suggestions');
            sugEl.innerHTML = (result.suggestions || []).map(s => `<div class="critic-suggestion">→ ${s}</div>`).join('');

            document.getElementById('critic-submit-anyway').disabled = false;
        },
    };

    window.CriticPanel = CriticPanel;
})();

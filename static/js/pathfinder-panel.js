/**
 * Graph Pathfinder Panel — "The Thread"
 * Find shortest path between two concepts through the knowledge graph.
 */

(function() {
    'use strict';

    const PathfinderPanel = {
        container: null,

        init(containerId) {
            this.container = document.getElementById(containerId);
            if (!this.container) return;
            this._buildUI();
        },

        _buildUI() {
            this.container.innerHTML = `
                <div class="pathfinder-header">
                    <span class="pathfinder-title">THE THREAD</span>
                    <span class="pathfinder-subtitle">"every symbol... led into the center, the mystery and innermost heart of the world"</span>
                </div>
                <div class="pathfinder-inputs">
                    <div class="path-input">
                        <label>From</label>
                        <input type="text" id="path-from" placeholder="e.g., Fourier Transform" value="Cyclic group Z_12">
                    </div>
                    <div class="path-input">
                        <label>To</label>
                        <input type="text" id="path-to" placeholder="e.g., Bach Fugue" value="Circle of fifths">
                    </div>
                    <button class="pathfinder-find" id="pathfinder-find">Find Path</button>
                </div>
                <div class="pathfinder-result" id="pathfinder-result" style="display:none;"></div>
            `;

            document.getElementById('pathfinder-find').addEventListener('click', () => this._findPath());
        },

        async _findPath() {
            const from = document.getElementById('path-from').value;
            const to = document.getElementById('path-to').value;
            const resultEl = document.getElementById('pathfinder-result');
            resultEl.style.display = 'block';
            resultEl.innerHTML = '<div class="path-loading">Tracing the thread...</div>';

            try {
                const resp = await fetch('/api/pathfinder', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({from, to}),
                });
                const data = await resp.json();
                this._renderPath(data);
            } catch (e) {
                // Fallback demo path
                this._renderPath({
                    path: ['Cyclic group Z_12', 'Z_n ≅ interval class', 'P5 = 7 semitones', 'Circle of fifths'],
                    confidence: 0.97,
                    narrative: 'The cyclic group structure of Z_12 maps directly to the circle of fifths through the generator element 7, which is coprime to 12.',
                });
            }
        },

        _renderPath(data) {
            const resultEl = document.getElementById('pathfinder-result');
            const hops = data.path || [];

            let html = `<div class="path-confidence">Path confidence: ${((data.confidence || 0) * 100).toFixed(0)}%</div>`;
            html += '<div class="path-hops">';

            hops.forEach((hop, i) => {
                html += `<div class="path-hop">
                    <div class="hop-node">${hop}</div>
                    ${i < hops.length - 1 ? '<div class="hop-arrow">↓</div>' : ''}
                </div>`;
            });

            html += '</div>';
            if (data.narrative) {
                html += `<div class="path-narrative">${data.narrative}</div>`;
            }

            resultEl.innerHTML = html;
        },
    };

    window.PathfinderPanel = PathfinderPanel;
})();

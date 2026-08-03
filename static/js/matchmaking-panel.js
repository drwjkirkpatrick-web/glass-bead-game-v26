/**
 * Matchmaking / "Find Your Counter-Subject" Panel
 * Pair players for dialectic matches.
 */

(function() {
    'use strict';

    const MatchmakingPanel = {
        container: null,

        init(containerId) {
            this.container = document.getElementById(containerId);
            if (!this.container) return;
            this._buildUI();
        },

        _buildUI() {
            this.container.innerHTML = `
                <div class="matchmaking-header">
                    <span class="matchmaking-title">FIND YOUR COUNTER-SUBJECT</span>
                    <span class="matchmaking-subtitle">"harmoniously combining two hostile themes"</span>
                </div>
                <div class="matchmaking-search">
                    <input type="text" id="mm-player" placeholder="Your name..." value="Joseph Knecht">
                    <button class="mm-find-btn" id="mm-find-btn">Find Match</button>
                </div>
                <div class="matchmaking-result" id="matchmaking-result" style="display:none;"></div>
                <div class="matchmaking-history" id="matchmaking-history"></div>
            `;

            document.getElementById('mm-find-btn').addEventListener('click', () => this._findMatch());
        },

        async _findMatch() {
            const player = document.getElementById('mm-player').value;
            const resultEl = document.getElementById('matchmaking-result');
            resultEl.style.display = 'block';
            resultEl.innerHTML = '<div class="mm-loading">Searching for complementarity...</div>';

            try {
                const resp = await fetch('/api/matchmaking/find', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({player}),
                });
                const data = await resp.json();
                this._renderMatch(data);
            } catch (e) {
                this._renderMatch({
                    opponent: 'Fritz Tegularius',
                    compatibility: 0.87,
                    your_strengths: ['musica', 'mathematica'],
                    opponent_strengths: ['philosophia', 'historia'],
                    shared: ['contemplation'],
                    match_type: 'Dialectic',
                });
            }
        },

        _renderMatch(data) {
            const resultEl = document.getElementById('matchmaking-result');
            resultEl.innerHTML = `
                <div class="mm-opponent-card">
                    <div class="mm-avatar">${(data.opponent || '?')[0]}</div>
                    <div class="mm-info">
                        <div class="mm-name">${data.opponent}</div>
                        <div class="mm-compat">Compatibility: ${((data.compatibility || 0) * 100).toFixed(0)}%</div>
                        <div class="mm-type">${data.match_type || 'Standard'}</div>
                    </div>
                </div>
                <div class="mm-breakdown">
                    <div class="mm-strength">
                        <label>Your Strengths</label>
                        <div class="mm-tags">${(data.your_strengths || []).map(s => `<span class="mm-tag">${s}</span>`).join('')}</div>
                    </div>
                    <div class="mm-strength">
                        <label>Opponent Strengths</label>
                        <div class="mm-tags">${(data.opponent_strengths || []).map(s => `<span class="mm-tag opponent">${s}</span>`).join('')}</div>
                    </div>
                    <div class="mm-shared">
                        <label>Shared Ground</label>
                        <div class="mm-tags">${(data.shared || []).map(s => `<span class="mm-tag shared">${s}</span>`).join('')}</div>
                    </div>
                </div>
                <button class="mm-challenge-btn">Issue Challenge</button>
            `;
        },
    };

    window.MatchmakingPanel = MatchmakingPanel;
})();

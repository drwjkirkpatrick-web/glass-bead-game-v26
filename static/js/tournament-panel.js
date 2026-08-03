/**
 * Tournament Bracket Tree Panel
 * Single-elimination bracket with match cards and champion crown.
 */

(function() {
    'use strict';

    const TournamentPanel = {
        container: null,

        init(containerId) {
            this.container = document.getElementById(containerId);
            if (!this.container) return;
            this._buildUI();
            this._loadTournament();
        },

        _buildUI() {
            this.container.innerHTML = `
                <div class="tournament-header">
                    <span class="tournament-title">LUDUS SOLLEMNIS</span>
                    <span class="tournament-status" id="tournament-status">Loading...</span>
                </div>
                <div class="tournament-bracket" id="tournament-bracket"></div>
                <div class="tournament-champion" id="tournament-champion"></div>
            `;
        },

        async _loadTournament() {
            try {
                const resp = await fetch('/api/tournament/current');
                const data = await resp.json();
                this._render(data);
            } catch (e) {
                this._render({
                    rounds: [
                        {matches: [
                            {player_a: 'Joseph Knecht', player_b: 'Fritz Tegularius', winner: 'Joseph Knecht', score_a: 0.92, score_b: 0.87},
                            {player_a: 'Master Thomas', player_b: 'Plinio Designori', winner: 'Master Thomas', score_a: 0.95, score_b: 0.89},
                        ]},
                        {matches: [
                            {player_a: 'Joseph Knecht', player_b: 'Master Thomas', winner: 'Joseph Knecht', score_a: 0.96, score_b: 0.91},
                        ]},
                    ],
                    champion: 'Joseph Knecht',
                });
            }
        },

        _render(data) {
            const bracket = document.getElementById('tournament-bracket');
            if (!bracket) return;

            let html = '';
            (data.rounds || []).forEach((round, rIdx) => {
                html += `<div class="bracket-round"><div class="round-label">Round ${rIdx + 1}</div>`;
                round.matches.forEach(m => {
                    const aWin = m.winner === m.player_a;
                    const bWin = m.winner === m.player_b;
                    html += `
                        <div class="bracket-match">
                            <div class="match-player ${aWin ? 'winner' : ''}">${m.player_a} <span class="match-score">${(m.score_a*100).toFixed(0)}%</span></div>
                            <div class="match-vs">vs</div>
                            <div class="match-player ${bWin ? 'winner' : ''}">${m.player_b} <span class="match-score">${(m.score_b*100).toFixed(0)}%</span></div>
                        </div>
                    `;
                });
                html += '</div>';
            });
            bracket.innerHTML = html;

            const champEl = document.getElementById('tournament-champion');
            if (champEl && data.champion) {
                champEl.innerHTML = `<div class="champion-crown">👑</div><div class="champion-name">${data.champion}</div><div class="champion-label">Ludi Magister Sollemnis</div>`;
            }

            document.getElementById('tournament-status').textContent = data.champion ? 'COMPLETE' : 'IN PROGRESS';
        },
    };

    window.TournamentPanel = TournamentPanel;
})();

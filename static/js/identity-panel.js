/**
 * Castalian Identity Card Panel
 * Player profile with rank badge, progress rings, domain mastery.
 */

(function() {
    'use strict';

    const IdentityPanel = {
        container: null,

        init(containerId) {
            this.container = document.getElementById(containerId);
            if (!this.container) return;
            this._buildUI();
            this._loadPlayer();
        },

        _buildUI() {
            this.container.innerHTML = `
                <div class="identity-header">
                    <span class="identity-title">CASTALIAN IDENTITY</span>
                    <span class="identity-status" id="identity-status">Loading...</span>
                </div>
                <div class="identity-card">
                    <div class="identity-avatar" id="identity-avatar">?</div>
                    <div class="identity-info">
                        <div class="identity-name" id="identity-name">Unknown</div>
                        <div class="identity-rank" id="identity-rank">Novice</div>
                        <div class="identity-province" id="identity-province">—</div>
                    </div>
                    <div class="identity-badges" id="identity-badges"></div>
                </div>
                <div class="identity-stats">
                    <div class="stat-ring">
                        <svg viewBox="0 0 36 36">
                            <path class="ring-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                            <path id="ring-moves" class="ring-fill" stroke-dasharray="0, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                        </svg>
                        <div class="ring-label">Moves</div>
                        <div class="ring-value" id="stat-moves">0</div>
                    </div>
                    <div class="stat-ring">
                        <svg viewBox="0 0 36 36">
                            <path class="ring-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                            <path id="ring-contemplation" class="ring-fill" stroke-dasharray="0, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                        </svg>
                        <div class="ring-label">Contemplation</div>
                        <div class="ring-value" id="stat-contemplation">0h</div>
                    </div>
                    <div class="stat-ring">
                        <svg viewBox="0 0 36 36">
                            <path class="ring-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                            <path id="ring-peers" class="ring-fill" stroke-dasharray="0, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                        </svg>
                        <div class="ring-label">Peers</div>
                        <div class="ring-value" id="stat-peers">0</div>
                    </div>
                </div>
                <div class="identity-mastery">
                    <label>Domain Mastery</label>
                    <div class="mastery-list" id="mastery-list"></div>
                </div>
            `;
        },

        async _loadPlayer() {
            try {
                const resp = await fetch('/api/player/current');
                const data = await resp.json();
                this._render(data);
            } catch (e) {
                // Fallback demo data
                this._render({
                    name: 'Joseph Knecht',
                    rank: 'Ludi Magister',
                    province: 'Waldzell',
                    verified_moves: 47,
                    contemplation_hours: 128,
                    peer_endorsements: ['Fritz Tegularius', 'Master Thomas'],
                    badges: ['Magister', 'Three Lives', 'Rain Maker'],
                    domain_mastery: { musica: 0.95, mathematica: 0.88, historia: 0.72, philosophia: 0.65 },
                });
            }
        },

        _render(data) {
            document.getElementById('identity-name').textContent = data.name || 'Anonymous';
            document.getElementById('identity-rank').textContent = data.rank || 'Novice';
            document.getElementById('identity-province').textContent = data.province || '—';
            document.getElementById('identity-avatar').textContent = (data.name || '?')[0].toUpperCase();
            document.getElementById('identity-status').textContent = 'ACTIVE';

            // Badges
            const badgesEl = document.getElementById('identity-badges');
            badgesEl.innerHTML = (data.badges || []).map(b =>
                `<span class="identity-badge">${b}</span>`
            ).join('');

            // Rings
            this._setRing('ring-moves', data.verified_moves || 0, 50);
            this._setRing('ring-contemplation', data.contemplation_hours || 0, 200);
            this._setRing('ring-peers', (data.peer_endorsements || []).length, 5);

            document.getElementById('stat-moves').textContent = data.verified_moves || 0;
            document.getElementById('stat-contemplation').textContent = (data.contemplation_hours || 0) + 'h';
            document.getElementById('stat-peers').textContent = (data.peer_endorsements || []).length;

            // Mastery bars
            const masteryEl = document.getElementById('mastery-list');
            const domains = data.domain_mastery || {};
            masteryEl.innerHTML = Object.entries(domains).map(([d, v]) => `
                <div class="mastery-item">
                    <span class="mastery-domain">${d}</span>
                    <div class="mastery-track"><div class="mastery-fill" style="width:${(v*100).toFixed(0)}%"></div></div>
                    <span class="mastery-value">${(v*100).toFixed(0)}%</span>
                </div>
            `).join('');
        },

        _setRing(id, value, max) {
            const el = document.getElementById(id);
            if (el) {
                const pct = Math.min(100, (value / max) * 100);
                el.setAttribute('stroke-dasharray', `${pct}, 100`);
            }
        },
    };

    window.IdentityPanel = IdentityPanel;
})();

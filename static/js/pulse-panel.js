/**
 * The Pulse — Live Move Stream Panel
 * Real-time ticker of all moves with trending domains.
 */

(function() {
    'use strict';

    const PulsePanel = {
        container: null,
        moves: [],
        maxItems: 20,
        socket: null,

        init(containerId, socket) {
            this.container = document.getElementById(containerId);
            this.socket = socket;
            if (!this.container) return;
            this._buildUI();
            this._loadPulse();
            this._listenSocket();
        },

        _buildUI() {
            this.container.innerHTML = `
                <div class="pulse-header">
                    <span class="pulse-title">THE PULSE</span>
                    <span class="pulse-live" id="pulse-live">● LIVE</span>
                </div>
                <div class="pulse-trending" id="pulse-trending"></div>
                <div class="pulse-stream" id="pulse-stream"></div>
            `;
        },

        async _loadPulse() {
            try {
                const resp = await fetch('/api/pulse');
                const data = await resp.json();
                this.moves = data.moves || [];
                this._renderTrending(data.trending || {});
            } catch (e) {
                this.moves = [];
            }
            this._renderStream();
        },

        _listenSocket() {
            if (this.socket) {
                this.socket.on('move_submitted', (data) => {
                    this._addMove(data);
                });
            }
        },

        _addMove(move) {
            this.moves.unshift(move);
            if (this.moves.length > this.maxItems) this.moves.pop();
            this._renderStream();
        },

        _renderStream() {
            const stream = document.getElementById('pulse-stream');
            if (!stream) return;

            stream.innerHTML = this.moves.map(m => `
                <div class="pulse-move" style="border-left-color: var(--color-${m.from_domain || 'musica'}, #00e5ff)">
                    <span class="pulse-player">${m.player || 'Anonymous'}</span>
                    <span class="pulse-concepts">${m.from_concept} → ${m.to_concept}</span>
                    <span class="pulse-score">${(m.score * 100).toFixed(0)}%</span>
                </div>
            `).join('');
        },

        _renderTrending(trending) {
            const el = document.getElementById('pulse-trending');
            if (!el) return;
            const entries = Object.entries(trending).sort((a,b) => b[1]-a[1]).slice(0, 4);
            el.innerHTML = entries.map(([domain, count]) => `
                <div class="trend-chip">
                    <span class="trend-domain">${domain}</span>
                    <span class="trend-count">${count}</span>
                </div>
            `).join('');
        },
    };

    window.PulsePanel = PulsePanel;
})();

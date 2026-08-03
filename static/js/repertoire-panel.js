/**
 * Move Repertoire Archive Panel
 * Personal searchable archive of all moves with filter and export.
 */

(function() {
    'use strict';

    const RepertoirePanel = {
        container: null,
        moves: [],
        filter: '',

        init(containerId) {
            this.container = document.getElementById(containerId);
            if (!this.container) return;
            this._buildUI();
            this._loadRepertoire();
        },

        _buildUI() {
            this.container.innerHTML = `
                <div class="repertoire-header">
                    <span class="repertoire-title">MOVE REPERTOIRE</span>
                    <button class="repertoire-export" id="repertoire-export">Export</button>
                </div>
                <div class="repertoire-search">
                    <input type="text" id="repertoire-filter" placeholder="Search moves..." />
                    <div class="repertoire-chips" id="repertoire-chips"></div>
                </div>
                <div class="repertoire-list" id="repertoire-list"></div>
                <div class="repertoire-signature" id="repertoire-signature"></div>
            `;

            document.getElementById('repertoire-filter').addEventListener('input', (e) => {
                this.filter = e.target.value.toLowerCase();
                this._renderList();
            });

            document.getElementById('repertoire-export').addEventListener('click', () => {
                const blob = new Blob([JSON.stringify(this.moves, null, 2)], {type: 'application/json'});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'repertoire.json';
                a.click();
            });
        },

        async _loadRepertoire() {
            try {
                const resp = await fetch('/api/repertoire/current');
                this.moves = await resp.json();
            } catch (e) {
                this.moves = [
                    {id: 1, from_concept: 'Z_12', from_domain: 'mathematica', to_concept: 'Circle of fifths', to_domain: 'musica', isomorphism: 'cyclic_group__circle_of_fifths', score: 0.92, date: '2026-08-01'},
                    {id: 2, from_concept: 'Fourier transform', from_domain: 'mathematica', to_concept: 'Overtone series', to_domain: 'musica', isomorphism: 'fourier_transform__overtone_series', score: 0.97, date: '2026-08-01'},
                ];
            }
            this._renderList();
            this._renderSignature();
        },

        _renderList() {
            const list = document.getElementById('repertoire-list');
            const filtered = this.moves.filter(m => {
                if (!this.filter) return true;
                const text = `${m.from_concept} ${m.to_concept} ${m.isomorphism}`.toLowerCase();
                return text.includes(this.filter);
            });

            list.innerHTML = filtered.map(m => `
                <div class="repertoire-move">
                    <div class="move-line">
                        <span class="move-from">${m.from_concept}</span>
                        <span class="move-arrow">→</span>
                        <span class="move-to">${m.to_concept}</span>
                    </div>
                    <div class="move-meta">
                        <span class="move-iso">${m.isomorphism?.replace(/__/g,' ↔ ').replace(/_/g,' ') || 'Generic'}</span>
                        <span class="move-score">${(m.score * 100).toFixed(0)}%</span>
                        <span class="move-date">${m.date || ''}</span>
                    </div>
                </div>
            `).join('');
        },

        _renderSignature() {
            // Find most-used isomorphism
            const counts = {};
            this.moves.forEach(m => { counts[m.isomorphism] = (counts[m.isomorphism] || 0) + 1; });
            const top = Object.entries(counts).sort((a,b) => b[1]-a[1])[0];
            const sigEl = document.getElementById('repertoire-signature');
            if (top && sigEl) {
                sigEl.innerHTML = `<span class="sig-label">Signature Isomorphism:</span> <span class="sig-value">${top[0].replace(/__/g,' ↔ ').replace(/_/g,' ')}</span> <span class="sig-count">(${top[1]} uses)</span>`;
            }
        },
    };

    window.RepertoirePanel = RepertoirePanel;
})();

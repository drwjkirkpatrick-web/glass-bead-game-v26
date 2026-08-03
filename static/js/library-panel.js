/**
 * Glass Bead Library Panel
 * Shared repository of individual beads with checkout and rating.
 */

(function() {
    'use strict';

    const BeadLibraryPanel = {
        container: null,
        beads: [],

        init(containerId) {
            this.container = document.getElementById(containerId);
            if (!this.container) return;
            this._buildUI();
            this._loadBeads();
        },

        _buildUI() {
            this.container.innerHTML = `
                <div class="library-header">
                    <span class="library-title">GLASS BEAD LIBRARY</span>
                    <span class="library-subtitle">"its manuals and pedals range over the entire intellectual cosmos"</span>
                </div>
                <div class="library-search">
                    <input type="text" id="library-search" placeholder="Search beads..." />
                </div>
                <div class="library-grid" id="library-grid"></div>
            `;

            document.getElementById('library-search').addEventListener('input', (e) => {
                this._render(e.target.value);
            });
        },

        async _loadBeads() {
            try {
                const resp = await fetch('/api/beads');
                this.beads = await resp.json();
            } catch (e) {
                this.beads = [
                    {id: 1, name: 'Z_12 Cyclic Group', domain: 'mathematica', color: '#ff3333', formula: 'Z_n = {0,1,...,n-1} under + mod n', popularity: 0.92, checked_out_by: null},
                    {id: 2, name: 'Circle of Fifths', domain: 'musica', color: '#3399ff', formula: 'P5^12 ≡ tonic (mod 12)', popularity: 0.95, checked_out_by: null},
                    {id: 3, name: 'Fourier Transform', domain: 'mathematica', color: '#ff6600', formula: 'F(ω) = ∫ f(t)e^{-iωt} dt', popularity: 0.88, checked_out_by: 'Knecht'},
                    {id: 4, name: 'Overtone Series', domain: 'musica', color: '#33ff33', formula: 'f_n = n·f_1', popularity: 0.90, checked_out_by: null},
                    {id: 5, name: 'Möbius Strip', domain: 'mathematica', color: '#cc33ff', formula: 'r(θ,t) = (cos θ, sin θ, t·cos(θ/2))', popularity: 0.78, checked_out_by: null},
                    {id: 6, name: 'Endless Canon', domain: 'musica', color: '#ff33cc', formula: 'Canon that returns transformed', popularity: 0.82, checked_out_by: null},
                ];
            }
            this._render('');
        },

        _render(filter) {
            const grid = document.getElementById('library-grid');
            const filtered = this.beads.filter(b => {
                if (!filter) return true;
                return (b.name + ' ' + b.domain + ' ' + b.formula).toLowerCase().includes(filter.toLowerCase());
            });

            grid.innerHTML = filtered.map(b => `
                <div class="bead-card ${b.checked_out_by ? 'checked-out' : ''}">
                    <div class="bead-color" style="background:${b.color}"></div>
                    <div class="bead-name">${b.name}</div>
                    <div class="bead-domain">${b.domain}</div>
                    <div class="bead-formula">${b.formula}</div>
                    <div class="bead-meta">
                        <span class="bead-pop">★ ${(b.popularity * 5).toFixed(1)}</span>
                        <span class="bead-status">${b.checked_out_by ? '🔒 ' + b.checked_out_by : 'Available'}</span>
                    </div>
                </div>
            `).join('');
        },
    };

    window.BeadLibraryPanel = BeadLibraryPanel;
})();

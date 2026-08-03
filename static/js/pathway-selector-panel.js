/**
 * Pathway Selector Panel — "Choose your transformation route"
 * Browse all 19 transformer pathways, find routes between domains,
 * and execute transformations through a selected pathway.
 *
 * API endpoints:
 *   GET  /api/pathways                  — list all 19 pathways
 *   GET  /api/pathways/from/<domain>    — list pathways from a domain
 *   POST /api/pathways/find             — find direct + multi-hop routes
 *   POST /api/pathways/select           — select and execute a pathway
 *   GET  /api/pathways/catalog          — full pathway metadata
 *   GET  /api/pathways/adjacency        — domain adjacency graph
 */

(function() {
    'use strict';

    /* ─── Constants ─── */
    const DOMAINS = [
        'Musica', 'Mathematica', 'Historia', 'Natura', 'Lingua',
        'Philosophia', 'Technologia', 'Medicina', 'Coda',
    ];

    const PIPELINE_STAGES = ['PARSE', 'TAG', 'MAP', 'PROJECT', 'COMPOSE', 'VERIFY'];

    const DOMAIN_COLORS = {
        Musica:       '#00e5ff',
        Mathematica:  '#ff00ff',
        Historia:     '#ffd700',
        Natura:       '#00ff7f',
        Lingua:       '#ff6b6b',
        Philosophia:  '#9370db',
        Technologia:  '#ffa500',
        Medicina:     '#ff69b4',
        Coda:         '#39ff14',
    };

    /* ─── Panel Object ─── */
    const PathwaySelectorPanel = {
        container: null,
        selectedPathway: null,
        isTransforming: false,
        styleInjected: false,

        /* ────────────────────────────────────────────
           INIT
           ──────────────────────────────────────────── */
        init(containerId) {
            this.container = document.getElementById(containerId);
            if (!this.container) {
                console.warn('PathwaySelectorPanel: container not found:', containerId);
                return;
            }
            this._injectStyles();
            this._buildUI();
            this._bindEvents();
            this._loadAllPathways();
            this._loadCatalog();
            this._loadAdjacency();
        },

        /* ────────────────────────────────────────────
           STYLE INJECTION (scoped — no external CSS file needed)
           ──────────────────────────────────────────── */
        _injectStyles() {
            if (this.styleInjected || document.getElementById('pathway-selector-styles')) return;
            const style = document.createElement('style');
            style.id = 'pathway-selector-styles';
            style.textContent = `
/* ─── Pathway Selector Panel — Glassmorphism ─── */
.pws-panel {
    font-family: var(--font-mono, 'JetBrains Mono', 'Courier New', monospace);
    color: var(--text-primary, #c9f0ff);
}

.pws-header {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--glass-border, rgba(100, 200, 255, 0.08));
    margin-bottom: 0.6rem;
}
.pws-title {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent-cyan, #00e5ff);
    font-weight: 600;
}
.pws-subtitle {
    font-size: 0.55rem;
    color: var(--text-dim, #6b8f9c);
    font-style: italic;
}

/* ─── Section Labels ─── */
.pws-section-label {
    font-size: 0.55rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-dim, #6b8f9c);
    margin-bottom: 0.3rem;
    margin-top: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}
.pws-section-label::before {
    content: '◆';
    color: var(--accent-cyan, #00e5ff);
    font-size: 0.45rem;
}

/* ─── Domain Selector ─── */
.pws-domain-select {
    width: 100%;
    background: rgba(10, 14, 23, 0.6);
    border: 1px solid var(--glass-border, rgba(100, 200, 255, 0.08));
    color: var(--text-primary, #c9f0ff);
    padding: 0.35rem 0.5rem;
    font-size: 0.7rem;
    font-family: var(--font-mono, 'JetBrains Mono', monospace);
    border-radius: 3px;
    outline: none;
    cursor: pointer;
    appearance: none;
    -webkit-appearance: none;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'><path fill='%2300e5ff' d='M0 0l5 6 5-6z'/></svg>");
    background-repeat: no-repeat;
    background-position: right 0.5rem center;
    padding-right: 1.5rem;
    margin-bottom: 0.5rem;
}
.pws-domain-select:focus {
    border-color: var(--accent-cyan, #00e5ff);
    box-shadow: 0 0 6px rgba(0, 229, 255, 0.1);
}
.pws-domain-select option {
    background: #0d1117;
    color: var(--text-primary, #c9f0ff);
}

/* ─── Pathway Cards ─── */
.pws-pathway-grid {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
    max-height: 180px;
    overflow-y: auto;
}
.pws-pathway-card {
    padding: 0.4rem 0.5rem;
    background: rgba(10, 14, 23, 0.3);
    border: 1px solid var(--glass-border, rgba(100, 200, 255, 0.08));
    border-left: 2px solid var(--accent-cyan, #00e5ff);
    border-radius: 3px;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.4rem;
}
.pws-pathway-card:hover {
    background: rgba(0, 229, 255, 0.08);
    border-color: var(--accent-cyan, #00e5ff);
    box-shadow: 0 0 8px rgba(0, 229, 255, 0.1);
}
.pws-pathway-card.active {
    background: rgba(0, 229, 255, 0.12);
    border-color: var(--accent-cyan, #00e5ff);
    box-shadow: 0 0 10px rgba(0, 229, 255, 0.15);
}
.pws-card-slug {
    font-size: 0.6rem;
    color: var(--text-primary, #c9f0ff);
    font-family: var(--font-mono, 'JetBrains Mono', monospace);
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.pws-card-dest {
    font-size: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.1rem 0.35rem;
    border-radius: 2px;
    white-space: nowrap;
}
.pws-empty {
    font-size: 0.6rem;
    color: var(--text-dim, #6b8f9c);
    font-style: italic;
    padding: 0.4rem;
    text-align: center;
}

/* ─── Transform Form ─── */
.pws-form {
    background: rgba(10, 14, 23, 0.4);
    border: 1px solid var(--glass-border, rgba(100, 200, 255, 0.08));
    border-radius: 4px;
    padding: 0.5rem;
    margin-top: 0.4rem;
    display: none;
}
.pws-form.visible { display: block; }

.pws-form-header {
    font-size: 0.55rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent-cyan, #00e5ff);
    margin-bottom: 0.4rem;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid var(--glass-border, rgba(100, 200, 255, 0.08));
}
.pws-input-row { margin-bottom: 0.4rem; }
.pws-input-row label {
    display: block;
    font-size: 0.55rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-dim, #6b8f9c);
    margin-bottom: 0.2rem;
}
.pws-input-row input {
    width: 100%;
    background: rgba(10, 14, 23, 0.6);
    border: 1px solid var(--glass-border, rgba(100, 200, 255, 0.08));
    color: var(--text-primary, #c9f0ff);
    padding: 0.35rem 0.5rem;
    font-size: 0.65rem;
    font-family: var(--font-mono, 'JetBrains Mono', monospace);
    border-radius: 3px;
    outline: none;
}
.pws-input-row input:focus {
    border-color: var(--accent-cyan, #00e5ff);
    box-shadow: 0 0 6px rgba(0, 229, 255, 0.1);
}
.pws-input-row input::placeholder {
    color: var(--text-dim, #6b8f9c);
    opacity: 0.6;
}

.pws-transform-btn {
    width: 100%;
    background: rgba(0, 229, 255, 0.12);
    border: 1px solid var(--accent-cyan, #00e5ff);
    color: var(--accent-cyan, #00e5ff);
    padding: 0.45rem;
    font-size: 0.7rem;
    font-family: var(--font-mono, 'JetBrains Mono', monospace);
    cursor: pointer;
    border-radius: 3px;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.pws-transform-btn:hover {
    background: rgba(0, 229, 255, 0.2);
    box-shadow: 0 0 12px rgba(0, 229, 255, 0.15);
}
.pws-transform-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

/* ─── Transform Result ─── */
.pws-result {
    display: none;
    margin-top: 0.5rem;
    padding: 0.5rem;
    background: rgba(0, 229, 255, 0.03);
    border: 1px solid var(--glass-border, rgba(100, 200, 255, 0.08));
    border-radius: 4px;
}
.pws-result.visible { display: block; }

.pws-result-direction {
    font-size: 0.6rem;
    color: var(--accent-cyan, #00e5ff);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.3rem;
}
.pws-result-field { margin-bottom: 0.35rem; }
.pws-result-field label {
    font-size: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-dim, #6b8f9c);
    display: block;
    margin-bottom: 0.15rem;
}
.pws-result-value {
    font-size: 0.65rem;
    color: var(--text-primary, #c9f0ff);
    line-height: 1.4;
}
.pws-result-value.resonance {
    font-style: italic;
    color: var(--accent-green, #00ffaa);
}

.pws-confidence-bar {
    height: 4px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 2px;
    overflow: hidden;
    margin-top: 0.2rem;
}
.pws-confidence-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent-cyan, #00e5ff), var(--accent-green, #00ffaa));
    border-radius: 2px;
    transition: width 0.6s ease;
    width: 0%;
}
.pws-confidence-text {
    font-size: 0.6rem;
    color: var(--accent-cyan, #00e5ff);
    font-family: var(--font-mono, 'JetBrains Mono', monospace);
}

/* ─── Pipeline Stages ─── */
.pws-stages { margin-top: 0.4rem; }
.pws-stage-track {
    display: flex;
    align-items: center;
    gap: 0.15rem;
    margin-bottom: 0.4rem;
    flex-wrap: wrap;
}
.pws-stage-node {
    font-size: 0.45rem;
    padding: 0.15rem 0.3rem;
    border: 1px solid var(--glass-border, rgba(100, 200, 255, 0.08));
    border-radius: 2px;
    color: var(--text-dim, #6b8f9c);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: all 0.3s;
}
.pws-stage-node.active {
    border-color: var(--accent-cyan, #00e5ff);
    color: var(--accent-cyan, #00e5ff);
    background: rgba(0, 229, 255, 0.1);
    box-shadow: 0 0 6px rgba(0, 229, 255, 0.15);
}
.pws-stage-node.complete {
    border-color: var(--accent-green, #00ffaa);
    color: var(--accent-green, #00ffaa);
    background: rgba(0, 255, 170, 0.05);
}
.pws-stage-arrow {
    font-size: 0.4rem;
    color: var(--text-dim, #6b8f9c);
}

.pws-stage-list {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}
.pws-stage-item {
    display: flex;
    gap: 0.4rem;
    align-items: flex-start;
    padding: 0.25rem 0.35rem;
    background: rgba(10, 14, 23, 0.3);
    border-radius: 2px;
    border-left: 2px solid var(--accent-cyan, #00e5ff);
}
.pws-stage-name {
    font-size: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent-cyan, #00e5ff);
    white-space: nowrap;
    min-width: 3.5rem;
}
.pws-stage-thread {
    font-size: 0.55rem;
    color: var(--text-primary, #c9f0ff);
    line-height: 1.3;
}

/* ─── Find Routes Section ─── */
.pws-routes {
    margin-top: 0.6rem;
    padding-top: 0.5rem;
    border-top: 1px solid var(--glass-border, rgba(100, 200, 255, 0.08));
}
.pws-route-inputs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.3rem;
    margin-bottom: 0.3rem;
}
.pws-route-inputs .pws-input-row { margin-bottom: 0; }
.pws-hops-row {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-bottom: 0.4rem;
}
.pws-hops-row label {
    font-size: 0.55rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-dim, #6b8f9c);
    white-space: nowrap;
}
.pws-hops-input {
    width: 3rem;
    background: rgba(10, 14, 23, 0.6);
    border: 1px solid var(--glass-border, rgba(100, 200, 255, 0.08));
    color: var(--text-primary, #c9f0ff);
    padding: 0.25rem 0.4rem;
    font-size: 0.65rem;
    font-family: var(--font-mono, 'JetBrains Mono', monospace);
    border-radius: 3px;
    outline: none;
    text-align: center;
}
.pws-hops-input:focus {
    border-color: var(--accent-cyan, #00e5ff);
}

.pws-find-btn {
    width: 100%;
    background: rgba(0, 229, 255, 0.08);
    border: 1px solid var(--accent-cyan, #00e5ff);
    color: var(--accent-cyan, #00e5ff);
    padding: 0.35rem;
    font-size: 0.6rem;
    font-family: var(--font-mono, 'JetBrains Mono', monospace);
    cursor: pointer;
    border-radius: 3px;
    transition: all 0.2s;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
}
.pws-find-btn:hover {
    background: rgba(0, 229, 255, 0.18);
    box-shadow: 0 0 10px rgba(0, 229, 255, 0.12);
}

/* ─── Route Results ─── */
.pws-route-results { display: none; }
.pws-route-results.visible { display: block; }

.pws-route-section { margin-bottom: 0.4rem; }
.pws-route-section-label {
    font-size: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent-cyan, #00e5ff);
    margin-bottom: 0.2rem;
}
.pws-route-item {
    padding: 0.3rem 0.4rem;
    background: rgba(10, 14, 23, 0.3);
    border-radius: 3px;
    border-left: 2px solid var(--accent-cyan, #00e5ff);
    margin-bottom: 0.2rem;
    font-size: 0.55rem;
    color: var(--text-primary, #c9f0ff);
    cursor: pointer;
    transition: all 0.2s;
}
.pws-route-item:hover {
    background: rgba(0, 229, 255, 0.06);
}
.pws-route-chain {
    display: flex;
    align-items: center;
    gap: 0.2rem;
    flex-wrap: wrap;
    margin-bottom: 0.1rem;
}
.pws-route-domain {
    font-size: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.08rem 0.25rem;
    border-radius: 2px;
}
.pws-route-arrow { color: var(--accent-cyan, #00e5ff); font-size: 0.5rem; }
.pws-route-meta {
    font-size: 0.5rem;
    color: var(--text-dim, #6b8f9c);
    font-family: var(--font-mono, 'JetBrains Mono', monospace);
}
.pws-route-empty {
    font-size: 0.55rem;
    color: var(--text-dim, #6b8f9c);
    font-style: italic;
}

/* ─── Loading / Error ─── */
.pws-loading {
    font-size: 0.6rem;
    color: var(--accent-cyan, #00e5ff);
    font-style: italic;
    padding: 0.4rem;
    text-align: center;
    animation: pws-pulse 1.2s ease-in-out infinite;
}
@keyframes pws-pulse {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}
.pws-error {
    font-size: 0.6rem;
    color: #ff6b6b;
    padding: 0.4rem;
    text-align: center;
}

/* ─── Stats Bar ─── */
.pws-stats {
    display: flex;
    gap: 0.6rem;
    margin-bottom: 0.5rem;
    padding: 0.3rem 0.4rem;
    background: rgba(10, 14, 23, 0.3);
    border-radius: 3px;
}
.pws-stat { display: flex; flex-direction: column; gap: 0.1rem; }
.pws-stat-label {
    font-size: 0.45rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-dim, #6b8f9c);
}
.pws-stat-value {
    font-size: 0.7rem;
    color: var(--accent-cyan, #00e5ff);
    font-family: var(--font-mono, 'JetBrains Mono', monospace);
}

/* ─── Scrollbar ─── */
.pws-pathway-grid::-webkit-scrollbar { width: 4px; }
.pws-pathway-grid::-webkit-scrollbar-track { background: transparent; }
.pws-pathway-grid::-webkit-scrollbar-thumb {
    background: rgba(0, 229, 255, 0.2);
    border-radius: 2px;
}
.pws-pathway-grid::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 229, 255, 0.4);
}
`;
            document.head.appendChild(style);
            this.styleInjected = true;
        },

        /* ────────────────────────────────────────────
           BUILD UI
           ──────────────────────────────────────────── */
        _buildUI() {
            const domainOptions = this._domainOptionsHTML('');

            this.container.innerHTML = `
                <div class="pws-panel glass-panel">
                    <div class="pws-header">
                        <span class="pws-title">PATHWAY SELECTOR</span>
                        <span class="pws-subtitle">Choose your transformation route</span>
                    </div>

                    <!-- Stats bar -->
                    <div class="pws-stats" id="pws-stats">
                        <div class="pws-stat">
                            <span class="pws-stat-label">Pathways</span>
                            <span class="pws-stat-value" id="pws-stat-total">—</span>
                        </div>
                        <div class="pws-stat">
                            <span class="pws-stat-label">Domains</span>
                            <span class="pws-stat-value">9</span>
                        </div>
                        <div class="pws-stat">
                            <span class="pws-stat-label">Adjacency</span>
                            <span class="pws-stat-value" id="pws-stat-adj">—</span>
                        </div>
                    </div>

                    <!-- Domain selector -->
                    <div class="pws-section-label">Source Domain</div>
                    <select class="pws-domain-select" id="pws-domain-select">
                        <option value="">— select domain —</option>
                        ${domainOptions}
                    </select>

                    <!-- Pathway cards -->
                    <div class="pws-section-label">Available Pathways</div>
                    <div class="pws-pathway-grid" id="pws-pathway-grid">
                        <div class="pws-empty">Select a source domain to browse pathways</div>
                    </div>

                    <!-- Transform form -->
                    <div class="pws-form" id="pws-transform-form">
                        <div class="pws-form-header" id="pws-form-header">▸ Selected Pathway</div>
                        <div class="pws-input-row">
                            <label>Origin Concept</label>
                            <input type="text" id="pws-origin-concept" placeholder="e.g., Cyclic group Z_12" />
                        </div>
                        <div class="pws-input-row">
                            <label>Structural Property</label>
                            <input type="text" id="pws-structural-property" placeholder="e.g., cyclic decomposition" />
                        </div>
                        <button class="pws-transform-btn" id="pws-transform-btn">
                            <span>⟲</span> Transform
                        </button>
                    </div>

                    <!-- Transform result -->
                    <div class="pws-result" id="pws-transform-result"></div>

                    <!-- Find Routes section -->
                    <div class="pws-routes">
                        <div class="pws-section-label">Find Routes</div>
                        <div class="pws-route-inputs">
                            <div class="pws-input-row">
                                <label>Source</label>
                                <select class="pws-domain-select" id="pws-route-source">
                                    <option value="">— from —</option>
                                    ${domainOptions}
                                </select>
                            </div>
                            <div class="pws-input-row">
                                <label>Destination</label>
                                <select class="pws-domain-select" id="pws-route-dest">
                                    <option value="">— to —</option>
                                    ${domainOptions}
                                </select>
                            </div>
                        </div>
                        <div class="pws-hops-row">
                            <label>Max Hops</label>
                            <input type="number" class="pws-hops-input" id="pws-max-hops" value="3" min="1" max="6" />
                            <button class="pws-find-btn" id="pws-find-btn" style="flex:1; margin-bottom:0;">
                                Find Routes
                            </button>
                        </div>
                        <div class="pws-route-results" id="pws-route-results"></div>
                    </div>
                </div>
            `;
        },

        /* ────────────────────────────────────────────
           BIND EVENTS
           ──────────────────────────────────────────── */
        _bindEvents() {
            // Source domain select → fetch pathways
            const domainSelect = this.container.querySelector('#pws-domain-select');
            if (domainSelect) {
                domainSelect.addEventListener('change', (e) => {
                    const domain = e.target.value;
                    if (domain) {
                        this._loadPathwaysFrom(domain);
                    } else {
                        this._renderPathwayGrid([]);
                        this._hideForm();
                    }
                });
            }

            // Transform button
            const transformBtn = this.container.querySelector('#pws-transform-btn');
            if (transformBtn) {
                transformBtn.addEventListener('click', () => this._executeTransform());
            }

            // Find routes button
            const findBtn = this.container.querySelector('#pws-find-btn');
            if (findBtn) {
                findBtn.addEventListener('click', () => this._findRoutes());
            }
        },

        /* ────────────────────────────────────────────
           API: GET /api/pathways — all pathways
           ──────────────────────────────────────────── */
        async _loadAllPathways() {
            try {
                const resp = await fetch('/api/pathways');
                const data = await resp.json();
                const count = Array.isArray(data) ? data.length : (data.pathways ? data.pathways.length : (data.total || '—'));
                const el = this.container.querySelector('#pws-stat-total');
                if (el) el.textContent = count;
            } catch (err) {
                console.warn('PathwaySelectorPanel: failed to load all pathways:', err);
                const el = this.container.querySelector('#pws-stat-total');
                if (el) el.textContent = '19';
            }
        },

        /* ────────────────────────────────────────────
           API: GET /api/pathways/catalog — metadata
           ──────────────────────────────────────────── */
        async _loadCatalog() {
            try {
                const resp = await fetch('/api/pathways/catalog');
                const data = await resp.json();
                this._catalog = data;
            } catch (err) {
                console.warn('PathwaySelectorPanel: failed to load catalog:', err);
                this._catalog = null;
            }
        },

        /* ────────────────────────────────────────────
           API: GET /api/pathways/adjacency — graph
           ──────────────────────────────────────────── */
        async _loadAdjacency() {
            try {
                const resp = await fetch('/api/pathways/adjacency');
                const data = await resp.json();
                const adjCount = data && typeof data === 'object'
                    ? (Object.keys(data).length || (data.edges ? data.edges.length : '—'))
                    : '—';
                const el = this.container.querySelector('#pws-stat-adj');
                if (el) el.textContent = adjCount;
                this._adjacency = data;
            } catch (err) {
                console.warn('PathwaySelectorPanel: failed to load adjacency:', err);
                const el = this.container.querySelector('#pws-stat-adj');
                if (el) el.textContent = '—';
                this._adjacency = null;
            }
        },

        /* ────────────────────────────────────────────
           API: GET /api/pathways/from/<domain>
           ──────────────────────────────────────────── */
        async _loadPathwaysFrom(domain) {
            const grid = this.container.querySelector('#pws-pathway-grid');
            if (grid) grid.innerHTML = '<div class="pws-loading">Fetching pathways...</div>';
            this._hideForm();

            try {
                const resp = await fetch(`/api/pathways/from/${encodeURIComponent(domain)}`);
                const data = await resp.json();
                const pathways = Array.isArray(data) ? data : (data.pathways || []);
                this._renderPathwayGrid(pathways, domain);
            } catch (err) {
                console.warn('PathwaySelectorPanel: failed to load pathways from domain:', err);
                if (grid) grid.innerHTML = '<div class="pws-error">⚠ failed to load pathways</div>';
            }
        },

        _renderPathwayGrid(pathways, sourceDomain) {
            const grid = this.container.querySelector('#pws-pathway-grid');
            if (!grid) return;

            if (!pathways || pathways.length === 0) {
                grid.innerHTML = `<div class="pws-empty">No pathways from ${sourceDomain || 'this domain'}</div>`;
                return;
            }

            grid.innerHTML = pathways.map(p => {
                const slug = p.pair_slug || p.slug || p.id || 'unknown';
                const dest = p.destination_domain || p.dest_domain || p.to || '—';
                const color = DOMAIN_COLORS[dest] || 'var(--accent-cyan, #00e5ff)';
                return `
                    <div class="pws-pathway-card" data-slug="${this._esc(slug)}" data-dest="${this._esc(dest)}" data-source="${this._esc(sourceDomain || '')}">
                        <span class="pws-card-slug">${this._esc(slug)}</span>
                        <span class="pws-card-dest" style="color:${color}; border:1px solid ${color}33; background:${color}11;">→ ${this._esc(dest)}</span>
                    </div>
                `;
            }).join('');

            // Bind clicks
            grid.querySelectorAll('.pws-pathway-card').forEach(card => {
                card.addEventListener('click', () => {
                    grid.querySelectorAll('.pws-pathway-card').forEach(c => c.classList.remove('active'));
                    card.classList.add('active');
                    this._selectPathway({
                        pair_slug: card.dataset.slug,
                        destination_domain: card.dataset.dest,
                        origin_domain: card.dataset.source,
                    });
                });
            });
        },

        /* ────────────────────────────────────────────
           Select pathway → show form
           ──────────────────────────────────────────── */
        _selectPathway(pathway) {
            this.selectedPathway = pathway;
            this._showForm(pathway);
        },

        _showForm(pathway) {
            const form = this.container.querySelector('#pws-transform-form');
            const header = this.container.querySelector('#pws-form-header');
            if (form) form.classList.add('visible');
            if (header) {
                header.textContent = `▸ ${pathway.pair_slug || 'Selected Pathway'}`;
            }
        },

        _hideForm() {
            const form = this.container.querySelector('#pws-transform-form');
            if (form) form.classList.remove('visible');
            this._hideResult();
        },

        /* ────────────────────────────────────────────
           API: POST /api/pathways/select — execute
           ──────────────────────────────────────────── */
        async _executeTransform() {
            if (this.isTransforming || !this.selectedPathway) return;
            this.isTransforming = true;

            const btn = this.container.querySelector('#pws-transform-btn');
            if (btn) btn.disabled = true;

            const originConcept = (this.container.querySelector('#pws-origin-concept') || {}).value || '';
            const structuralProperty = (this.container.querySelector('#pws-structural-property') || {}).value || '';

            if (!originConcept.trim()) {
                this._showError('Enter an origin concept');
                if (btn) btn.disabled = false;
                this.isTransforming = false;
                return;
            }

            const body = {
                pair_slug: this.selectedPathway.pair_slug,
                origin_concept: originConcept.trim(),
                origin_domain: this.selectedPathway.origin_domain || '',
                destination_domain: this.selectedPathway.destination_domain || '',
                structural_property: structuralProperty.trim(),
            };

            this._showResultLoading();

            try {
                const resp = await fetch('/api/pathways/select', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(body),
                });
                const result = await resp.json();
                this._renderResult(result);
            } catch (err) {
                console.error('PathwaySelectorPanel: transform failed:', err);
                this._showError('⚠ transformation failed');
            } finally {
                this.isTransforming = false;
                if (btn) btn.disabled = false;
            }
        },

        /* ────────────────────────────────────────────
           Render transform result
           ──────────────────────────────────────────── */
        _renderResult(result) {
            const el = this.container.querySelector('#pws-transform-result');
            if (!el) return;
            el.classList.add('visible');

            const direction = result.direction || `${result.origin_domain || '?'} → ${result.destination_domain || '?'}`;
            const destConcept = result.destination_concept || '—';
            const resonance = result.resonance_sentence || 'No resonance generated.';
            const confidence = result.total_confidence != null ? result.total_confidence : 0;
            const confidencePct = (confidence * 100).toFixed(0);
            const steps = result.steps || result.pipeline_stages || result.stages || [];

            // Build pipeline stage track
            const stageTrackHTML = PIPELINE_STAGES.map((s, i) => {
                const match = steps.find(st => (st.stage || st.name || '').toUpperCase() === s);
                const cls = match ? (match === steps[steps.length - 1] ? 'complete' : 'complete') : '';
                return `<span class="pws-stage-node ${cls}">${s}</span>${i < PIPELINE_STAGES.length - 1 ? '<span class="pws-stage-arrow">→</span>' : ''}`;
            }).join('');

            // Build stage detail list
            let stageListHTML = '';
            if (steps.length > 0) {
                stageListHTML = steps.map(s => {
                    const stageName = s.stage || s.name || 'STAGE';
                    const thread = s.language_thread || s.thread || s.description || '';
                    return `
                        <div class="pws-stage-item">
                            <span class="pws-stage-name">${this._esc(stageName)}</span>
                            <span class="pws-stage-thread">${this._esc(thread)}</span>
                        </div>
                    `;
                }).join('');
            } else {
                // If no steps returned, show the 6 standard stages
                stageListHTML = PIPELINE_STAGES.map(s => `
                    <div class="pws-stage-item">
                        <span class="pws-stage-name">${s}</span>
                        <span class="pws-stage-thread">—</span>
                    </div>
                `).join('');
            }

            el.innerHTML = `
                <div class="pws-result-direction">${this._esc(direction)}</div>

                <div class="pws-result-field">
                    <label>Destination Concept</label>
                    <div class="pws-result-value">${this._esc(destConcept)}</div>
                </div>

                <div class="pws-result-field">
                    <label>Resonance</label>
                    <div class="pws-result-value resonance">${this._esc(resonance)}</div>
                </div>

                <div class="pws-result-field">
                    <label>Total Confidence</label>
                    <div class="pws-confidence-bar">
                        <div class="pws-confidence-fill" style="width: ${confidencePct}%"></div>
                    </div>
                    <span class="pws-confidence-text">${confidence.toFixed(3)} (${confidencePct}%)</span>
                </div>

                <div class="pws-result-field">
                    <label>Pipeline Stages</label>
                    <div class="pws-stages">
                        <div class="pws-stage-track">${stageTrackHTML}</div>
                        <div class="pws-stage-list">${stageListHTML}</div>
                    </div>
                </div>
            `;
        },

        _showResultLoading() {
            const el = this.container.querySelector('#pws-transform-result');
            if (!el) return;
            el.classList.add('visible');
            el.innerHTML = '<div class="pws-loading">Transforming through pathway...</div>';
        },

        _showError(msg) {
            const el = this.container.querySelector('#pws-transform-result');
            if (!el) return;
            el.classList.add('visible');
            el.innerHTML = `<div class="pws-error">${this._esc(msg)}</div>`;
        },

        _hideResult() {
            const el = this.container.querySelector('#pws-transform-result');
            if (el) {
                el.classList.remove('visible');
                el.innerHTML = '';
            }
        },

        /* ────────────────────────────────────────────
           API: POST /api/pathways/find — route finder
           ──────────────────────────────────────────── */
        async _findRoutes() {
            const source = (this.container.querySelector('#pws-route-source') || {}).value || '';
            const dest = (this.container.querySelector('#pws-route-dest') || {}).value || '';
            const hops = parseInt((this.container.querySelector('#pws-max-hops') || {}).value || '3', 10);

            const resultsEl = this.container.querySelector('#pws-route-results');
            if (!resultsEl) return;

            if (!source || !dest) {
                resultsEl.classList.add('visible');
                resultsEl.innerHTML = '<div class="pws-error">Select source and destination</div>';
                return;
            }

            if (source === dest) {
                resultsEl.classList.add('visible');
                resultsEl.innerHTML = '<div class="pws-error">Source and destination are the same</div>';
                return;
            }

            resultsEl.classList.add('visible');
            resultsEl.innerHTML = '<div class="pws-loading">Finding routes...</div>';

            try {
                const resp = await fetch('/api/pathways/find', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        source_domain: source,
                        destination_domain: dest,
                        max_hops: hops,
                    }),
                });
                const data = await resp.json();
                this._renderRoutes(data, source, dest);
            } catch (err) {
                console.error('PathwaySelectorPanel: find routes failed:', err);
                resultsEl.innerHTML = '<div class="pws-error">⚠ route search failed</div>';
            }
        },

        _renderRoutes(data, source, dest) {
            const el = this.container.querySelector('#pws-route-results');
            if (!el) return;
            el.classList.add('visible');

            const direct = data.direct_routes || data.direct || [];
            const multiHop = data.multi_hop_routes || data.multi_hop || data.multihop || [];

            let html = '';

            // Direct routes
            html += '<div class="pws-route-section">';
            html += '<div class="pws-route-section-label">Direct Routes</div>';
            if (direct.length > 0) {
                html += direct.map(r => this._renderRouteItem(r)).join('');
            } else {
                html += '<div class="pws-route-empty">No direct pathway found</div>';
            }
            html += '</div>';

            // Multi-hop routes
            html += '<div class="pws-route-section">';
            html += '<div class="pws-route-section-label">Multi-Hop Routes</div>';
            if (multiHop.length > 0) {
                html += multiHop.map(r => this._renderRouteItem(r)).join('');
            } else {
                html += '<div class="pws-route-empty">No multi-hop routes found</div>';
            }
            html += '</div>';

            el.innerHTML = html;

            // Bind clicks on route items to auto-select the pathway
            el.querySelectorAll('.pws-route-item').forEach(item => {
                item.addEventListener('click', () => {
                    const slug = item.dataset.slug;
                    const src = item.dataset.source;
                    const dst = item.dataset.dest;
                    if (slug) {
                        // Auto-select domain and pathway
                        const domainSelect = this.container.querySelector('#pws-domain-select');
                        if (domainSelect && src) {
                            domainSelect.value = src;
                            domainSelect.dispatchEvent(new Event('change'));
                            // After pathways load, auto-click the matching card
                            setTimeout(() => {
                                const card = this.container.querySelector(`.pws-pathway-card[data-slug="${slug}"]`);
                                if (card) card.click();
                            }, 800);
                        }
                    }
                });
            });
        },

        _renderRouteItem(route) {
            const slug = route.pair_slug || route.slug || route.pathway || '';
            const domains = route.domains || route.chain || route.path || [];
            const hops = route.hops != null ? route.hops : (domains.length - 1);
            const confidence = route.confidence != null ? route.confidence : (route.total_confidence || 0);

            let chainHTML = '';
            if (domains.length > 0) {
                chainHTML = '<div class="pws-route-chain">';
                domains.forEach((d, i) => {
                    const color = DOMAIN_COLORS[d] || 'var(--accent-cyan, #00e5ff)';
                    chainHTML += `<span class="pws-route-domain" style="color:${color}; border:1px solid ${color}33; background:${color}11;">${this._esc(d)}</span>`;
                    if (i < domains.length - 1) chainHTML += '<span class="pws-route-arrow">→</span>';
                });
                chainHTML += '</div>';
            } else if (slug) {
                chainHTML = `<div class="pws-route-chain"><span class="pws-card-slug">${this._esc(slug)}</span></div>`;
            }

            const firstDomain = domains[0] || '';
            const lastDomain = domains[domains.length - 1] || '';

            return `
                <div class="pws-route-item" data-slug="${this._esc(slug)}" data-source="${this._esc(firstDomain)}" data-dest="${this._esc(lastDomain)}">
                    ${chainHTML}
                    <div class="pws-route-meta">${hops} hop${hops !== 1 ? 's' : ''}${confidence > 0 ? ' · conf ' + (confidence * 100).toFixed(0) + '%' : ''}${slug ? ' · ' + this._esc(slug) : ''}</div>
                </div>
            `;
        },

        /* ────────────────────────────────────────────
           HELPERS
           ──────────────────────────────────────────── */
        _domainOptionsHTML(selected) {
            return DOMAINS.map(d =>
                `<option value="${d}"${d === selected ? ' selected' : ''}>${d}</option>`
            ).join('');
        },

        _esc(str) {
            if (str == null) return '';
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
        },
    };

    /* ─── Export ─── */
    window.PathwaySelectorPanel = PathwaySelectorPanel;
})();
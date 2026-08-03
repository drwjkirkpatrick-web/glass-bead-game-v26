/**
 * Knowledge Transformer Panel — Generic UI for all 10 domain-pair transformers.
 *
 * Unlike the original transformer-panel.js (hardcoded for Math↔Music), this
 * panel is data-driven: it receives a transformer config (domain pair, API
 * endpoint, default concept) and renders the same 6-stage pipeline UI.
 *
 * Usage:
 *   KnowledgeTransformerPanel.init(containerId, config);
 *
 * where config = {
 *     domainA: "Mathematics",
 *     domainB: "Philosophy",
 *     endpoint: "/api/transform/math-philosophy",
 *     catalogEndpoint: "/api/transform/math-philosophy/catalog",
 *     defaultConcept: "Gödel's incompleteness theorem",
 *     defaultProperty: "formal limits of self-reference",
 *     colorA: "#ff00ff",
 *     colorB: "#9370db",
 * }
 */
(function() {
    'use strict';

    const KnowledgeTransformerPanel = {
        instances: {},  // containerId → instance state

        /**
         * Initialise a transformer panel in a container.
         * @param {string} containerId - DOM element ID
         * @param {object} config - Transformer configuration
         */
        init(containerId, config) {
            const container = document.getElementById(containerId);
            if (!container) {
                console.warn(`KnowledgeTransformerPanel: container "${containerId}" not found`);
                return;
            }

            const state = {
                container,
                config,
                isRunning: false,
                currentTokens: [],
                maxVisibleTokens: 10,
                tokenFadeDelay: 3000,
            };
            this.instances[containerId] = state;

            this._buildUI(state);
            this._bindEvents(state);
            this._loadCatalog(state);
        },

        // ─── UI Construction ──────────────────────────────────

        _buildUI(state) {
            const { config, container } = state;
            const labelA = config.domainA.toUpperCase();
            const labelB = config.domainB.toUpperCase();
            const arrow = '↔';

            container.innerHTML = `
                <div class="kt-header">
                    <span class="kt-title" style="color:${config.colorA}">${labelA}</span>
                    <span class="kt-arrow">${arrow}</span>
                    <span class="kt-title" style="color:${config.colorB}">${labelB}</span>
                    <span class="kt-status" id="${containerId}-status">IDLE</span>
                </div>

                <!-- Direction selector -->
                <div class="kt-direction">
                    <label>Direction</label>
                    <div class="kt-dir-toggle">
                        <button class="kt-dir-btn active" data-dir="a-to-b">${labelA} → ${labelB}</button>
                        <button class="kt-dir-btn" data-dir="b-to-a">${labelB} → ${labelA}</button>
                    </div>
                </div>

                <!-- Input fields -->
                <div class="kt-inputs">
                    <div class="kt-input-row">
                        <label>Origin Concept</label>
                        <input type="text" id="${containerId}-origin"
                               placeholder="e.g., ${config.defaultConcept}"
                               value="${config.defaultConcept}">
                    </div>
                    <div class="kt-input-row">
                        <label>Structural Property</label>
                        <input type="text" id="${containerId}-property"
                               placeholder="structural property"
                               value="${config.defaultProperty}">
                    </div>
                    <div class="kt-input-row">
                        <label>Resonance (optional)</label>
                        <textarea id="${containerId}-resonance" rows="2"
                                  placeholder="A single luminous sentence..."></textarea>
                    </div>
                </div>

                <!-- Run button -->
                <button class="kt-run-btn" id="${containerId}-run">
                    <span class="kt-run-icon">⟲</span> Transform
                </button>

                <!-- 6-Stage pipeline -->
                <div class="kt-stages">
                    <div class="kt-stage-track">
                        <div class="kt-stage-node" data-stage="PARSE">PARSE</div>
                        <div class="kt-stage-line"></div>
                        <div class="kt-stage-node" data-stage="TAG">TAG</div>
                        <div class="kt-stage-line"></div>
                        <div class="kt-stage-node" data-stage="MAP">MAP</div>
                        <div class="kt-stage-line"></div>
                        <div class="kt-stage-node" data-stage="PROJECT">PROJECT</div>
                        <div class="kt-stage-line"></div>
                        <div class="kt-stage-node" data-stage="COMPOSE">COMPOSE</div>
                        <div class="kt-stage-line"></div>
                        <div class="kt-stage-node" data-stage="VERIFY">VERIFY</div>
                    </div>
                </div>

                <!-- Token stream -->
                <div class="kt-tokens">
                    <label>Token Stream</label>
                    <div class="kt-token-display" id="${containerId}-tokens"></div>
                </div>

                <!-- Confidence gauge -->
                <div class="kt-confidence">
                    <label>Confidence</label>
                    <div class="kt-conf-track">
                        <div class="kt-conf-fill" id="${containerId}-conf-fill" style="width:0%"></div>
                    </div>
                    <span class="kt-conf-value" id="${containerId}-conf-value">0.00</span>
                </div>

                <!-- Result -->
                <div class="kt-result" id="${containerId}-result" style="display:none;">
                    <div class="kt-result-section">
                        <label>Destination</label>
                        <div class="kt-result-text" id="${containerId}-dest"></div>
                    </div>
                    <div class="kt-result-section">
                        <label>Resonance</label>
                        <div class="kt-result-text kt-resonance" id="${containerId}-resonance-out"></div>
                    </div>
                    <div class="kt-result-section">
                        <label>Isomorphism</label>
                        <div class="kt-result-text" id="${containerId}-iso"></div>
                    </div>
                    <div class="kt-result-section">
                        <label>Language Thread</label>
                        <div class="kt-thread-list" id="${containerId}-thread"></div>
                    </div>
                </div>

                <!-- Catalog -->
                <div class="kt-catalog">
                    <label>Isomorphism Library</label>
                    <div class="kt-catalog-list" id="${containerId}-catalog"></div>
                </div>
            `;
        },

        // ─── Event Binding ───────────────────────────────────

        _bindEvents(state) {
            const { container, config } = state;

            // Direction toggle
            container.querySelectorAll('.kt-dir-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    container.querySelectorAll('.kt-dir-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    // Swap default concept when direction changes
                    const originInput = container.querySelector(`#${state.container.id}-origin`);
                    if (originInput && !originInput.dataset.userEdited) {
                        if (btn.dataset.dir === 'b-to-a' && config.defaultConceptB) {
                            originInput.value = config.defaultConceptB;
                        } else {
                            originInput.value = config.defaultConcept;
                        }
                    }
                });
            });

            // Mark input as user-edited
            const originInput = container.querySelector(`#${state.container.id}-origin`);
            if (originInput) {
                originInput.addEventListener('input', () => {
                    originInput.dataset.userEdited = 'true';
                });
            }

            // Run button
            const runBtn = container.querySelector(`#${state.container.id}-run`);
            if (runBtn) {
                runBtn.addEventListener('click', () => this._runTransformation(state));
            }
        },

        // ─── Catalog ─────────────────────────────────────────

        async _loadCatalog(state) {
            try {
                const resp = await fetch(state.config.catalogEndpoint);
                const catalog = await resp.json();
                this._renderCatalog(state, catalog);
            } catch (err) {
                console.warn(`Failed to load catalog for ${state.config.domainA}↔${state.config.domainB}:`, err);
            }
        },

        _renderCatalog(state, catalog) {
            const listEl = state.container.querySelector(`#${state.container.id}-catalog`);
            if (!listEl) return;

            const items = Object.entries(catalog).map(([name, data]) => {
                const display = name.replace(/__/g, ' ↔ ').replace(/_/g, ' ');
                const conf = data.confidence !== undefined
                    ? `${(data.confidence * 100).toFixed(0)}%`
                    : '';
                return `
                    <div class="kt-catalog-item" data-iso="${name}">
                        <span class="kt-cat-name">${display}</span>
                        ${conf ? `<span class="kt-cat-conf">${conf}</span>` : ''}
                    </div>
                `;
            }).join('');
            listEl.innerHTML = items;

            // Click to fill origin
            listEl.querySelectorAll('.kt-catalog-item').forEach(item => {
                item.addEventListener('click', () => {
                    const isoName = item.dataset.iso;
                    const originInput = state.container.querySelector(`#${state.container.id}-origin`);
                    if (originInput) {
                        const parts = isoName.split('__');
                        originInput.value = parts[0].replace(/_/g, ' ');
                        originInput.dataset.userEdited = 'true';
                    }
                });
            });
        },

        // ─── Transformation ──────────────────────────────────

        async _runTransformation(state) {
            if (state.isRunning) return;
            state.isRunning = true;

            const cid = state.container.id;
            const origin = state.container.querySelector(`#${cid}-origin`).value.trim();
            const property = state.container.querySelector(`#${cid}-property`).value.trim();
            const resonance = state.container.querySelector(`#${cid}-resonance`).value.trim();
            const dirBtn = state.container.querySelector('.kt-dir-btn.active');
            const direction = dirBtn ? dirBtn.dataset.dir : 'a-to-b';

            const originDomain = direction === 'a-to-b' ? state.config.domainA : state.config.domainB;
            const destDomain = direction === 'a-to-b' ? state.config.domainB : state.config.domainA;

            this._resetUI(state);
            this._setStatus(state, 'TRANSFORMING...');

            try {
                const resp = await fetch(state.config.endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        origin_concept: origin,
                        origin_domain: originDomain,
                        destination_domain: destDomain,
                        structural_property: property,
                        resonance_sentence: resonance,
                        tokens: ['[INIT]', '[PARSE]', '[TAG]', '[MAP]', '[PROJECT]', '[COMPOSE]', '[VERIFY]'],
                    }),
                });

                const result = await resp.json();
                await this._animate(state, result);
                this._showResult(state, result);
                this._setStatus(state, 'COMPLETE');
            } catch (err) {
                console.error(`Transform failed (${state.config.domainA}↔${state.config.domainB}):`, err);
                this._setStatus(state, 'ERROR');
                this._showToken(state, '⚠ transform failed', 'error');
            } finally {
                state.isRunning = false;
            }
        },

        // ─── Animation ──────────────────────────────────────

        _resetUI(state) {
            const cid = state.container.id;
            state.container.querySelectorAll('.kt-stage-node').forEach(n => {
                n.classList.remove('active', 'complete');
            });
            const fill = state.container.querySelector(`#${cid}-conf-fill`);
            if (fill) fill.style.width = '0%';
            const val = state.container.querySelector(`#${cid}-conf-value`);
            if (val) val.textContent = '0.00';
            const td = state.container.querySelector(`#${cid}-tokens`);
            if (td) td.innerHTML = '';
            const result = state.container.querySelector(`#${cid}-result`);
            if (result) result.style.display = 'none';
            state.currentTokens = [];
        },

        _setStatus(state, status) {
            const el = state.container.querySelector(`#${state.container.id}-status`);
            if (el) el.textContent = status;
        },

        async _animate(state, result) {
            const steps = result.steps || [];
            const totalTime = 2500;
            const stepDelay = totalTime / Math.max(steps.length, 1);

            for (let i = 0; i < steps.length; i++) {
                const step = steps[i];
                await this._delay(stepDelay * 0.6);

                const node = state.container.querySelector(`.kt-stage-node[data-stage="${step.stage}"]`);
                if (node) {
                    node.classList.add('active');
                    const allNodes = Array.from(state.container.querySelectorAll('.kt-stage-node'));
                    const idx = allNodes.indexOf(node);
                    for (let j = 0; j < idx; j++) {
                        allNodes[j].classList.add('complete');
                        allNodes[j].classList.remove('active');
                    }
                }

                const tokenText = `[${step.stage}] ${step.language_thread.substring(0, 50)}...`;
                this._showToken(state, tokenText, 'step', step.confidence);

                await this._delay(stepDelay * 0.4);
            }

            const fill = state.container.querySelector(`#${state.container.id}-conf-fill`);
            if (fill) fill.style.width = `${(result.total_confidence * 100).toFixed(0)}%`;
            const val = state.container.querySelector(`#${state.container.id}-conf-value`);
            if (val) val.textContent = result.total_confidence.toFixed(2);
        },

        _showToken(state, text, type, confidence) {
            const td = state.container.querySelector(`#${state.container.id}-tokens`);
            if (!td) return;

            const token = document.createElement('div');
            token.className = `kt-token kt-token-${type}`;
            token.textContent = text;

            if (confidence !== undefined) {
                const intensity = Math.floor(confidence * 255);
                token.style.borderLeftColor = `rgb(0, ${intensity}, 255)`;
            }

            td.appendChild(token);
            state.currentTokens.push(token);

            requestAnimationFrame(() => {
                token.style.opacity = '1';
                token.style.transform = 'translateX(0)';
            });

            if (state.currentTokens.length > state.maxVisibleTokens) {
                const old = state.currentTokens.shift();
                if (old) {
                    old.style.opacity = '0';
                    setTimeout(() => old.remove(), 300);
                }
            }

            setTimeout(() => {
                token.style.opacity = '0';
                setTimeout(() => {
                    if (token.parentNode) token.remove();
                }, 300);
            }, state.tokenFadeDelay);
        },

        _showResult(state, result) {
            const cid = state.container.id;
            const panel = state.container.querySelector(`#${cid}-result`);
            if (!panel) return;

            state.container.querySelector(`#${cid}-dest`).textContent =
                `${result.destination_concept} (${result.destination_domain})`;
            state.container.querySelector(`#${cid}-resonance-out`).textContent =
                result.resonance_sentence || 'No resonance generated.';
            state.container.querySelector(`#${cid}-iso`).textContent =
                (result.isomorphisms || []).join(', ').replace(/__/g, ' ↔ ').replace(/_/g, ' ') ||
                'Generic homomorphism';

            const threadList = state.container.querySelector(`#${cid}-thread`);
            if (threadList && result.steps) {
                threadList.innerHTML = result.steps.map(s => `
                    <div class="kt-thread-item">
                        <span class="kt-thread-stage">${s.stage}</span>
                        <span class="kt-thread-text">${s.language_thread}</span>
                    </div>
                `).join('');
            }

            panel.style.display = 'block';
        },

        _delay(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        },
    };

    // ─── Transformer Registry ────────────────────────────────
    // All 10 knowledge transformers configured for the panel.
    // Colors match Config.BEAD_TYPES in config.py.
    KnowledgeTransformerPanel.TRANSFORMERS = [
        { domainA: "Mathematics", domainB: "Philosophy",
          endpoint: "/api/transform/math-philosophy",
          catalogEndpoint: "/api/transform/math-philosophy/catalog",
          defaultConcept: "Gödel's incompleteness theorem",
          defaultConceptB: "Epistemological limits of self-knowledge",
          defaultProperty: "formal limits of self-reference",
          colorA: "#ff00ff", colorB: "#9370db" },

        { domainA: "Music", domainB: "Language",
          endpoint: "/api/transform/music-language",
          catalogEndpoint: "/api/transform/music-language/catalog",
          defaultConcept: "Bach fugue subject",
          defaultConceptB: "Syntactic tree of a sentence",
          defaultProperty: "hierarchical structure of nested elements",
          colorA: "#00e5ff", colorB: "#ff6b6b" },

        { domainA: "History", domainB: "Philosophy",
          endpoint: "/api/transform/history-philosophy",
          catalogEndpoint: "/api/transform/history-philosophy/catalog",
          defaultConcept: "Hegelian dialectical process",
          defaultConceptB: "Dialectical philosophy of history",
          defaultProperty: "thesis-antithesis-synthesis across time",
          colorA: "#ffd700", colorB: "#9370db" },

        { domainA: "Nature", domainB: "Mathematics",
          endpoint: "/api/transform/nature-math",
          catalogEndpoint: "/api/transform/nature-math/catalog",
          defaultConcept: "Fibonacci spirals in sunflowers",
          defaultConceptB: "Recursive sequence F_n = F_{n-1} + F_{n-2}",
          defaultProperty: "self-similar recursive growth",
          colorA: "#00ff7f", colorB: "#ff00ff" },

        { domainA: "Philosophy", domainB: "Language",
          endpoint: "/api/transform/philosophy-language",
          catalogEndpoint: "/api/transform/philosophy-language/catalog",
          defaultConcept: "Wittgenstein language games",
          defaultConceptB: "Speech act theory",
          defaultProperty: "meaning as use in social practice",
          colorA: "#9370db", colorB: "#ff6b6b" },

        { domainA: "Nature", domainB: "Music",
          endpoint: "/api/transform/nature-music",
          catalogEndpoint: "/api/transform/nature-music/catalog",
          defaultConcept: "Birdsong intervals",
          defaultConceptB: "Melodic ornamentation",
          defaultProperty: "pitch contour and interval structure",
          colorA: "#00ff7f", colorB: "#00e5ff" },

        { domainA: "Technology", domainB: "Mathematics",
          endpoint: "/api/transform/technology-math",
          catalogEndpoint: "/api/transform/technology-math/catalog",
          defaultConcept: "Boolean logic circuits",
          defaultConceptB: "Boolean algebra",
          defaultProperty: "binary operations and truth values",
          colorA: "#ffa500", colorB: "#ff00ff" },

        { domainA: "Medicine", domainB: "Nature",
          endpoint: "/api/transform/medicine-nature",
          catalogEndpoint: "/api/transform/medicine-nature/catalog",
          defaultConcept: "Immune system self-nonself recognition",
          defaultConceptB: "Ecological balance and biodiversity",
          defaultProperty: "self-organizing equilibrium",
          colorA: "#ff69b4", colorB: "#00ff7f" },

        { domainA: "History", domainB: "Music",
          endpoint: "/api/transform/history-music",
          catalogEndpoint: "/api/transform/history-music/catalog",
          defaultConcept: "Baroque era and absolutist courts",
          defaultConceptB: "Fugue and contrapuntal form",
          defaultProperty: "structured complexity under hierarchical order",
          colorA: "#ffd700", colorB: "#00e5ff" },

        { domainA: "Philosophy", domainB: "Music",
          endpoint: "/api/transform/philosophy-music",
          catalogEndpoint: "/api/transform/philosophy-music/catalog",
          defaultConcept: "Pythagorean harmony of the spheres",
          defaultConceptB: "Tonal harmony and harmonic series",
          defaultProperty: "universal mathematical order made audible",
          colorA: "#9370db", colorB: "#00e5ff" },

        // ── 8 Coda (Computer Code) transformers ──
        { domainA: "Code", domainB: "Mathematics",
          endpoint: "/api/transform/code-math",
          catalogEndpoint: "/api/transform/code-math/catalog",
          defaultConcept: "Turing machine",
          defaultConceptB: "Algorithm",
          defaultProperty: "step-by-step computation on a formal machine",
          colorA: "#39ff14", colorB: "#ff00ff" },

        { domainA: "Code", domainB: "Music",
          endpoint: "/api/transform/code-music",
          catalogEndpoint: "/api/transform/code-music/catalog",
          defaultConcept: "Algorithmic composition",
          defaultConceptB: "Code as musical score",
          defaultProperty: "formal instructions that produce sound",
          colorA: "#39ff14", colorB: "#00e5ff" },

        { domainA: "Code", domainB: "Language",
          endpoint: "/api/transform/code-language",
          catalogEndpoint: "/api/transform/code-language/catalog",
          defaultConcept: "Formal grammar",
          defaultConceptB: "Parser implementation",
          defaultProperty: "syntactic rules generating valid strings",
          colorA: "#39ff14", colorB: "#ff6b6b" },

        { domainA: "Code", domainB: "Philosophy",
          endpoint: "/api/transform/code-philosophy",
          catalogEndpoint: "/api/transform/code-philosophy/catalog",
          defaultConcept: "Formal logic and syllogism",
          defaultConceptB: "Boolean code and conditional logic",
          defaultProperty: "deductive inference made executable",
          colorA: "#39ff14", colorB: "#9370db" },

        { domainA: "Code", domainB: "Technology",
          endpoint: "/api/transform/code-technology",
          catalogEndpoint: "/api/transform/code-technology/catalog",
          defaultConcept: "Software API",
          defaultConceptB: "Hardware interface specification",
          defaultProperty: "contract between caller and implementor",
          colorA: "#39ff14", colorB: "#ffa500" },

        { domainA: "Code", domainB: "Nature",
          endpoint: "/api/transform/code-nature",
          catalogEndpoint: "/api/transform/code-nature/catalog",
          defaultConcept: "Genetic algorithm",
          defaultConceptB: "Natural selection",
          defaultProperty: "fitness-driven iterative optimization",
          colorA: "#39ff14", colorB: "#00ff7f" },

        { domainA: "Code", domainB: "History",
          endpoint: "/api/transform/code-history",
          catalogEndpoint: "/api/transform/code-history/catalog",
          defaultConcept: "Git version control",
          defaultConceptB: "Historical chronicle",
          defaultProperty: "branching narratives and merge as synthesis",
          colorA: "#39ff14", colorB: "#ffd700" },

        { domainA: "Code", domainB: "Medicine",
          endpoint: "/api/transform/code-medicine",
          catalogEndpoint: "/api/transform/code-medicine/catalog",
          defaultConcept: "Diagnostic algorithm",
          defaultConceptB: "Clinical reasoning",
          defaultProperty: "systematic inference from symptoms to diagnosis",
          colorA: "#39ff14", colorB: "#ff69b4" },
    ];

    // Export
    window.KnowledgeTransformerPanel = KnowledgeTransformerPanel;
})();
/**
 * Game Logic Module — Client-side helpers for the Glass Bead Game
 *
 * Provides utilities for move construction, graph interaction,
 * bead selection, and real-time game state management.
 */
(function () {
    'use strict';

    // ─── Domain Config ──────────────────────────────────────
    const DOMAINS = [
        'musica', 'mathematica', 'historia', 'natura',
        'lingua', 'philosophia', 'technologia', 'medicina'
    ];

    const BEAD_TYPES = {
        musica:      { name: 'Magister Musicae',      color: '#00e5ff', icon: '♪', octave: 4 },
        mathematica: { name: 'Magister Mathematicae', color: '#ff00ff', icon: '∑', octave: 4 },
        historia:    { name: 'Magister Historiae',    color: '#ffd700', icon: '⌛', octave: 4 },
        natura:      { name: 'Magister Naturae',      color: '#00ff7f', icon: '⚛', octave: 5 },
        lingua:      { name: 'Magister Linguae',      color: '#ff6b6b', icon: '✎', octave: 5 },
        philosophia: { name: 'Magister Philosophiae', color: '#9370db', icon: '◊', octave: 5 },
        technologia: { name: 'Magister Technologiae', color: '#ffa500', icon: '⚙', octave: 6 },
        medicina:    { name: 'Magister Medicinae',    color: '#ff69b4', icon: '✚', octave: 6 },
    };

    const RANKS = ['Novice', 'Adept', 'Scholar', 'Magister Ludi'];

    // ─── Game State ─────────────────────────────────────────
    let _currentPlayer = {
        name: 'Anonymous',
        rank: 'Novice',
        score: 0,
        moves: 0,
        selectedBead: null,
    };

    let _graphState = { nodes: [], edges: [] };
    let _moveHistory = [];

    // ─── Public API ─────────────────────────────────────────
    window.GameLogic = {
        // Configuration
        DOMAINS,
        BEAD_TYPES,
        RANKS,

        // State
        getPlayer,
        setPlayer,
        getGraphState,
        setGraphState,

        // Move construction
        buildMove,
        validateMoveLocally,
        estimateElegance,
        estimateFertility,

        // Graph analysis
        findPath,
        calculateDensity,
        getDomainNeighbors,

        // UI helpers
        renderBeadSelector,
        renderDomainDropdown,
        getRankProgress,
    };

    // ─── Player State ─────────────────────────────────────
    function getPlayer() {
        return { ..._currentPlayer };
    }

    function setPlayer(player) {
        _currentPlayer = { ..._currentPlayer, ...player };
    }

    function getGraphState() {
        return JSON.parse(JSON.stringify(_graphState));
    }

    function setGraphState(state) {
        _graphState = JSON.parse(JSON.stringify(state));
    }

    // ─── Move Construction ──────────────────────────────────
    function buildMove(bead, fromConcept, fromDomain, toConcept, toDomain, via, resonance) {
        const move = {
            bead,
            from_concept: fromConcept,
            from_domain: fromDomain,
            to_concept: toConcept,
            to_domain: toDomain,
            via,
            resonance,
            timestamp: new Date().toISOString(),
            status: 'draft',
        };

        // Auto-fill from bead if concept matches bead's domain
        if (BEAD_TYPES[bead] && !fromDomain) {
            move.from_domain = bead;
        }

        return move;
    }

    function validateMoveLocally(move) {
        const errors = [];

        if (!move.from_concept || move.from_concept.trim().length < 2) {
            errors.push('From concept is too brief');
        }
        if (!move.to_concept || move.to_concept.trim().length < 2) {
            errors.push('To concept is too brief');
        }
        if (!move.from_domain || !DOMAINS.includes(move.from_domain)) {
            errors.push('Invalid from domain');
        }
        if (!move.to_domain || !DOMAINS.includes(move.to_domain)) {
            errors.push('Invalid to domain');
        }
        if (move.from_domain === move.to_domain) {
            errors.push('Move must cross at least one domain boundary');
        }
        if (!move.via || move.via.trim().length < 10) {
            errors.push('Structural property (via) must be at least 10 characters');
        }
        if (!move.resonance || move.resonance.trim().length < 15) {
            errors.push('Resonance sentence must be at least 15 characters');
        }

        return {
            valid: errors.length === 0,
            errors,
        };
    }

    function estimateElegance(fromDomain, toDomain) {
        const idx1 = DOMAINS.indexOf(fromDomain);
        const idx2 = DOMAINS.indexOf(toDomain);
        const distance = Math.abs(idx2 - idx1);
        // Higher distance = more surprising = more elegant (with diminishing returns)
        return Math.min(10, 3 + distance * 1.5);
    }

    function estimateFertility(fromDomain, toDomain) {
        // Fertility = how many new domain combinations this unlocks
        const idx1 = DOMAINS.indexOf(fromDomain);
        const idx2 = DOMAINS.indexOf(toDomain);
        const span = Math.abs(idx2 - idx1);
        return Math.min(10, 2 + span * 2);
    }

    // ─── Graph Analysis ─────────────────────────────────────
    function findPath(fromId, toId, maxDepth = 5) {
        const nodes = _graphState.nodes;
        const edges = _graphState.edges;
        const nodeMap = {};
        nodes.forEach(n => nodeMap[n.id] = n);

        if (fromId === toId) return [fromId];

        const visited = new Set([fromId]);
        const queue = [[fromId]];

        while (queue.length > 0) {
            const path = queue.shift();
            const current = path[path.length - 1];

            if (path.length > maxDepth) continue;

            for (const edge of edges) {
                let neighbor = null;
                if (edge.source === current) neighbor = edge.target;
                else if (edge.target === current) neighbor = edge.source;

                if (neighbor && !visited.has(neighbor)) {
                    const newPath = [...path, neighbor];
                    if (neighbor === toId) return newPath;
                    visited.add(neighbor);
                    queue.push(newPath);
                }
            }
        }

        return null;
    }

    function calculateDensity() {
        const n = _graphState.nodes.length;
        if (n < 2) return 0;
        const maxEdges = (n * (n - 1)) / 2;
        return _graphState.edges.length / maxEdges;
    }

    function getDomainNeighbors(domain) {
        const domainNodes = _graphState.nodes.filter(n => n.domain === domain);
        const neighbors = new Set();

        for (const node of domainNodes) {
            for (const edge of _graphState.edges) {
                if (edge.source === node.id) {
                    const target = _graphState.nodes.find(n => n.id === edge.target);
                    if (target) neighbors.add(target.domain);
                } else if (edge.target === node.id) {
                    const source = _graphState.nodes.find(n => n.id === edge.source);
                    if (source) neighbors.add(source.domain);
                }
            }
        }

        return Array.from(neighbors);
    }

    // ─── UI Helpers ─────────────────────────────────────────
    function renderBeadSelector(containerId, onSelect) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = '';
        const grid = document.createElement('div');
        grid.className = 'bead-selector-grid';

        for (const [domain, bead] of Object.entries(BEAD_TYPES)) {
            const btn = document.createElement('button');
            btn.className = 'bead-btn';
            btn.style.borderColor = bead.color;
            btn.style.color = bead.color;
            btn.innerHTML = `
                <span class="bead-icon">${bead.icon}</span>
                <span class="bead-name">${bead.name}</span>
                <span class="bead-domain">${domain}</span>
            `;
            btn.addEventListener('click', () => {
                _currentPlayer.selectedBead = domain;
                // Highlight selected
                grid.querySelectorAll('.bead-btn').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                if (onSelect) onSelect(domain, bead);
            });
            grid.appendChild(btn);
        }

        container.appendChild(grid);
    }

    function renderDomainDropdown(selectId, selected = '') {
        const select = document.getElementById(selectId);
        if (!select) return;

        select.innerHTML = '<option value="">-- Select Domain --</option>';
        for (const domain of DOMAINS) {
            const option = document.createElement('option');
            option.value = domain;
            option.textContent = BEAD_TYPES[domain]?.name || domain;
            if (domain === selected) option.selected = true;
            select.appendChild(option);
        }
    }

    function getRankProgress() {
        const currentIdx = RANKS.indexOf(_currentPlayer.rank);
        const moves = _currentPlayer.moves;

        const thresholds = [0, 3, 10, 25];
        const currentThreshold = thresholds[currentIdx];
        const nextThreshold = thresholds[currentIdx + 1] || thresholds[currentIdx];
        const progress = nextThreshold > currentThreshold
            ? (moves - currentThreshold) / (nextThreshold - currentThreshold)
            : 1;

        return {
            rank: _currentPlayer.rank,
            nextRank: RANKS[currentIdx + 1] || 'Max',
            progress: Math.min(1, Math.max(0, progress)),
            movesNeeded: Math.max(0, nextThreshold - moves),
        };
    }
})();

    // ─── Demo Move ──────────────────────────────────────────
    function demoMove() {
        const demo = {
            bead: 'musica',
            from_concept: "Bach's Goldberg Variations",
            from_domain: 'musica',
            to_concept: 'Möbius strip topology',
            to_domain: 'mathematica',
            via: 'Self-similar structure: each variation contains the seed of the next, just as a Möbius strip contains its own reversal within a single surface.',
            resonance: 'Both are paradoxes of locality: every point is locally ascending or forward, yet globally circular.',
        };
        return demo;
    }

    window.GameLogic.demoMove = demoMove;

/**
 * Game Replay / Post-Mortem Analyzer Panel
 * Timeline scrubber with score evolution and critical moments.
 */

(function() {
    'use strict';

    const ReplayPanel = {
        container: null,

        init(containerId) {
            this.container = document.getElementById(containerId);
            if (!this.container) return;
            this._buildUI();
            this._loadReplay();
        },

        _buildUI() {
            this.container.innerHTML = `
                <div class="replay-header">
                    <span class="replay-title">POST-MORTEM</span>
                    <span class="replay-subtitle">"the 'meaning' of music... does not need my explanations"</span>
                </div>
                <div class="replay-timeline" id="replay-timeline"></div>
                <div class="replay-score-graph">
                    <canvas id="replay-canvas" width="300" height="80"></canvas>
                </div>
                <div class="replay-critical" id="replay-critical"></div>
                <div class="replay-detail" id="replay-detail"></div>
            `;
        },

        async _loadReplay() {
            try {
                const resp = await fetch('/api/replay/latest');
                const data = await resp.json();
                this._render(data);
            } catch (e) {
                this._render({
                    events: [
                        {timestamp: 0, move: 'Theme: Bach Canon', score: 0.3, phase: 'exposition'},
                        {timestamp: 60, move: 'CounterSubject: Möbius', score: 0.6, phase: 'development'},
                        {timestamp: 120, move: 'Episode: Modulation', score: 0.75, phase: 'development'},
                        {timestamp: 180, move: 'Synthesis: Group Theory', score: 0.92, phase: 'recapitulation'},
                        {timestamp: 240, move: 'Coda: Return Transformed', score: 0.96, phase: 'coda'},
                    ],
                    critical_moments: [
                        {timestamp: 180, reason: 'Score jump +0.17 — synthesis discovered'},
                        {timestamp: 240, reason: 'Contemplation bonus applied — coda transformed'},
                    ],
                });
            }
        },

        _render(data) {
            const events = data.events || [];
            const timeline = document.getElementById('replay-timeline');

            timeline.innerHTML = events.map((e, i) => `
                <div class="replay-event" data-idx="${i}">
                    <span class="event-time">${e.timestamp}s</span>
                    <span class="event-phase">${e.phase}</span>
                    <span class="event-move">${e.move}</span>
                    <span class="event-score">${(e.score * 100).toFixed(0)}%</span>
                </div>
            `).join('');

            timeline.querySelectorAll('.replay-event').forEach(el => {
                el.addEventListener('click', () => {
                    const idx = parseInt(el.dataset.idx);
                    this._showDetail(events[idx]);
                });
            });

            this._drawScoreGraph(events);

            const criticalEl = document.getElementById('replay-critical');
            criticalEl.innerHTML = `<label>Critical Moments</label>` + (data.critical_moments || []).map(m => `
                <div class="critical-moment">
                    <span class="critical-time">${m.timestamp}s</span>
                    <span class="critical-reason">${m.reason}</span>
                </div>
            `).join('');
        },

        _drawScoreGraph(events) {
            const canvas = document.getElementById('replay-canvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            const w = canvas.width, h = canvas.height;

            ctx.clearRect(0, 0, w, h);
            if (events.length < 2) return;

            const maxScore = Math.max(...events.map(e => e.score));
            const maxTime = events[events.length - 1].timestamp;

            ctx.beginPath();
            ctx.strokeStyle = 'rgba(0, 229, 255, 0.8)';
            ctx.lineWidth = 2;
            events.forEach((e, i) => {
                const x = (e.timestamp / maxTime) * w;
                const y = h - (e.score / maxScore) * (h - 10) - 5;
                if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
            });
            ctx.stroke();

            // Dots
            events.forEach(e => {
                const x = (e.timestamp / maxTime) * w;
                const y = h - (e.score / maxScore) * (h - 10) - 5;
                ctx.beginPath();
                ctx.arc(x, y, 3, 0, Math.PI * 2);
                ctx.fillStyle = '#00e5ff';
                ctx.fill();
            });
        },

        _showDetail(event) {
            const detail = document.getElementById('replay-detail');
            detail.innerHTML = `
                <div class="detail-phase">${event.phase.toUpperCase()}</div>
                <div class="detail-move">${event.move}</div>
                <div class="detail-score">Score: ${(event.score * 100).toFixed(0)}%</div>
            `;
        },
    };

    window.ReplayPanel = ReplayPanel;
})();

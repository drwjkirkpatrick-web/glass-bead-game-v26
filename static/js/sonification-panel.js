/**
 * Sonification Dashboard Panel
 * Web Audio API real-time sonification of game state.
 */

(function() {
    'use strict';

    const SonificationPanel = {
        container: null,
        audioCtx: null,
        isPlaying: false,

        init(containerId) {
            this.container = document.getElementById(containerId);
            if (!this.container) return;
            this._buildUI();
        },

        _buildUI() {
            this.container.innerHTML = `
                <div class="sonification-header">
                    <span class="sonification-title">SONIFICATION</span>
                    <span class="sonification-subtitle">"The Game is primarily a form of music-making"</span>
                </div>
                <div class="sonification-controls">
                    <button class="sonify-toggle" id="sonify-toggle">▶ Play State</button>
                    <div class="sonify-volumes" id="sonify-volumes"></div>
                </div>
                <div class="sonification-waveform">
                    <canvas id="sonify-canvas" width="300" height="60"></canvas>
                </div>
            `;

            document.getElementById('sonify-toggle').addEventListener('click', () => this._toggle());
            this._renderVolumes();
        },

        _renderVolumes() {
            const domains = ['musica', 'mathematica', 'historia', 'philosophia', 'natura', 'technologia'];
            const el = document.getElementById('sonify-volumes');
            el.innerHTML = domains.map(d => `
                <div class="volume-row">
                    <span class="volume-label">${d}</span>
                    <input type="range" class="volume-slider" data-domain="${d}" min="0" max="1" step="0.1" value="0.5">
                </div>
            `).join('');
        },

        _toggle() {
            const btn = document.getElementById('sonify-toggle');
            if (this.isPlaying) {
                this.isPlaying = false;
                btn.textContent = '▶ Play State';
                if (this.audioCtx) this.audioCtx.suspend();
            } else {
                this.isPlaying = true;
                btn.textContent = '⏸ Pause';
                this._startAudio();
            }
        },

        _startAudio() {
            if (!this.audioCtx) {
                this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            this.audioCtx.resume();

            // Simple drone based on active domains
            const domains = ['musica', 'mathematica', 'historia', 'philosophia'];
            const baseFreqs = {musica: 261.63, mathematica: 329.63, historia: 392.0, philosophia: 440.0};

            domains.forEach(d => {
                const osc = this.audioCtx.createOscillator();
                const gain = this.audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.value = baseFreqs[d];
                gain.gain.value = 0.03;
                osc.connect(gain);
                gain.connect(this.audioCtx.destination);
                osc.start();
                // Stop after 2 seconds (demo)
                setTimeout(() => { osc.stop(); gain.disconnect(); }, 2000);
            });

            this._drawWaveform();
        },

        _drawWaveform() {
            const canvas = document.getElementById('sonify-canvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            let t = 0;

            const draw = () => {
                if (!this.isPlaying) return;
                ctx.fillStyle = 'rgba(10, 14, 23, 0.3)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.beginPath();
                ctx.strokeStyle = 'rgba(0, 229, 255, 0.6)';
                ctx.lineWidth = 1.5;
                for (let x = 0; x < canvas.width; x++) {
                    const y = canvas.height / 2 + Math.sin((x + t) * 0.05) * 20 * Math.sin(t * 0.01);
                    if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
                }
                ctx.stroke();
                t += 2;
                requestAnimationFrame(draw);
            };
            draw();
        },
    };

    window.SonificationPanel = SonificationPanel;
})();

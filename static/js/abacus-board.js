/**
 * Abacus Board Visualizer
 * Bastian Perrot's original invention: a frame with wires on which
 * colored glass beads are strung. The wires correspond to the lines
 * of the musical staff; the beads to time-values of notes.
 *
 * Hesse, *Das Glasperlenspiel* (p. 1165-1168):
 * "He constructed a frame, modeled on a child's abacus, a frame with
 * several dozen wires on which could be strung glass beads of various
 * sizes, shapes, and colors."
 */

(function() {
    'use strict';

    const AbacusBoard = {
        canvas: null,
        ctx: null,
        wires: [],
        beads: [],
        animationFrame: null,
        wireCount: 13,      // C to C = 13 chromatic tones
        beadSize: 14,
        wireSpacing: 32,
        beadSpacing: 18,
        colors: {
            C:  '#ff3333',    // red
            'C#': '#ff6600',
            D:  '#ffcc00',    // yellow
            'D#': '#99ff33',
            E:  '#33ff33',    // green
            F:  '#33ffcc',
            'F#': '#3399ff',  // blue
            G:  '#6633ff',
            'G#': '#cc33ff',
            A:  '#ff33cc',    // magenta
            'A#': '#ff3399',
            B:  '#ff6666',
            highC: '#ffffff', // white octave
        },
        noteNames: ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C'],

        init(containerId, options = {}) {
            const container = document.getElementById(containerId);
            if (!container) {
                console.warn('AbacusBoard: container not found:', containerId);
                return;
            }

            this.wireCount = options.wireCount || this.wireCount;
            this._buildCanvas(container);
            this._initWires();
            this._initBeads(options.initialBeads || []);
            this._startAnimation();

            // Click to add a bead
            this.canvas.addEventListener('click', (e) => this._handleClick(e));

            // Expose API
            window.abacusAPI = {
                addBead: (note, duration, concept) => this.addBead(note, duration, concept),
                clear: () => this.clearBeads(),
                getState: () => this._getState(),
                loadState: (state) => this._loadState(state),
            };
        },

        _buildCanvas(container) {
            const width = container.clientWidth || 600;
            const height = 400;

            this.canvas = document.createElement('canvas');
            this.canvas.width = width;
            this.canvas.height = height;
            this.canvas.style.width = '100%';
            this.canvas.style.height = 'auto';
            this.canvas.style.display = 'block';
            container.appendChild(this.canvas);

            this.ctx = this.canvas.getContext('2d');
        },

        _initWires() {
            const margin = 40;
            const availableHeight = this.canvas.height - margin * 2;
            const spacing = availableHeight / (this.wireCount - 1);

            this.wires = [];
            for (let i = 0; i < this.wireCount; i++) {
                const y = margin + i * spacing;
                this.wires.push({
                    y: y,
                    note: this.noteNames[i],
                    color: Object.values(this.colors)[i % Object.values(this.colors).length],
                });
            }
        },

        _initBeads(initial) {
            this.beads = [];
            initial.forEach(b => {
                this.beads.push({
                    wireIndex: b.wireIndex,
                    x: b.x || this.canvas.width / 2 + (Math.random() - 0.5) * 200,
                    y: this.wires[b.wireIndex]?.y || 0,
                    size: b.size || this.beadSize,
                    color: b.color || this.colors[this.noteNames[b.wireIndex]] || '#00e5ff',
                    concept: b.concept || '',
                    opacity: 0,
                    targetOpacity: 1,
                    pulsePhase: Math.random() * Math.PI * 2,
                });
            });
        },

        addBead(noteName, duration = 1.0, concept = '') {
            const wireIndex = this.noteNames.indexOf(noteName);
            if (wireIndex === -1) return;

            const existingOnWire = this.beads.filter(b => b.wireIndex === wireIndex).length;
            const x = 60 + existingOnWire * this.beadSpacing + (Math.random() * 10 - 5);

            const bead = {
                wireIndex: wireIndex,
                x: x,
                y: this.wires[wireIndex].y,
                size: this.beadSize * (0.8 + duration * 0.2),
                color: this.colors[noteName] || '#00e5ff',
                concept: concept,
                opacity: 0,
                targetOpacity: 0.9,
                pulsePhase: Math.random() * Math.PI * 2,
            };
            this.beads.push(bead);

            // Animate in
            const animate = () => {
                bead.opacity += 0.05;
                if (bead.opacity < bead.targetOpacity) {
                    requestAnimationFrame(animate);
                }
            };
            animate();

            return bead;
        },

        clearBeads() {
            this.beads.forEach(b => { b.targetOpacity = 0; });
            setTimeout(() => { this.beads = []; }, 500);
        },

        _handleClick(e) {
            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Find nearest wire
            let nearest = -1;
            let minDist = Infinity;
            this.wires.forEach((w, i) => {
                const dist = Math.abs(y - w.y);
                if (dist < minDist) {
                    minDist = dist;
                    nearest = i;
                }
            });

            if (nearest !== -1 && minDist < 20) {
                const note = this.noteNames[nearest];
                const concept = prompt(`Place a bead on ${note}. Enter concept:`, 'Theme');
                if (concept) {
                    this.addBead(note, 1.0, concept);
                }
            }
        },

        _getState() {
            return {
                wires: this.wireCount,
                beads: this.beads.map(b => ({
                    note: this.noteNames[b.wireIndex],
                    x: b.x,
                    concept: b.concept,
                })),
            };
        },

        _loadState(state) {
            if (state.beads) {
                this.clearBeads();
                state.beads.forEach(b => {
                    this.addBead(b.note, 1.0, b.concept);
                });
            }
        },

        _startAnimation() {
            const draw = () => {
                this._drawFrame();
                this.animationFrame = requestAnimationFrame(draw);
            };
            draw();
        },

        _drawFrame() {
            const ctx = this.ctx;
            const w = this.canvas.width;
            const h = this.canvas.height;

            // Clear with dark glassmorphism background
            ctx.fillStyle = 'rgba(10, 14, 23, 0.9)';
            ctx.fillRect(0, 0, w, h);

            // Draw frame border
            ctx.strokeStyle = 'rgba(0, 229, 255, 0.2)';
            ctx.lineWidth = 2;
            ctx.strokeRect(10, 10, w - 20, h - 20);

            // Draw wires
            this.wires.forEach((wire, i) => {
                // Wire line
                ctx.beginPath();
                ctx.moveTo(40, wire.y);
                ctx.lineTo(w - 40, wire.y);
                ctx.strokeStyle = 'rgba(0, 229, 255, 0.15)';
                ctx.lineWidth = 1;
                ctx.stroke();

                // Note label
                ctx.font = '10px monospace';
                ctx.fillStyle = 'rgba(0, 229, 255, 0.5)';
                ctx.textAlign = 'right';
                ctx.fillText(wire.note, 35, wire.y + 3);
            });

            // Draw beads
            const time = Date.now() / 1000;
            this.beads.forEach(bead => {
                if (bead.opacity <= 0.01) return;

                const pulse = Math.sin(time * 2 + bead.pulsePhase) * 0.1 + 0.9;
                const size = bead.size * pulse;

                // Glass bead glow
                const glow = ctx.createRadialGradient(
                    bead.x, bead.y, 0,
                    bead.x, bead.y, size * 2
                );
                glow.addColorStop(0, bead.color + Math.floor(bead.opacity * 255).toString(16).padStart(2, '0'));
                glow.addColorStop(0.5, bead.color + '40');
                glow.addColorStop(1, 'transparent');

                ctx.beginPath();
                ctx.arc(bead.x, bead.y, size * 2, 0, Math.PI * 2);
                ctx.fillStyle = glow;
                ctx.fill();

                // Bead body
                ctx.beginPath();
                ctx.arc(bead.x, bead.y, size, 0, Math.PI * 2);
                ctx.fillStyle = bead.color + Math.floor(bead.opacity * 200).toString(16).padStart(2, '0');
                ctx.fill();

                // Bead highlight (glass reflection)
                ctx.beginPath();
                ctx.arc(bead.x - size * 0.3, bead.y - size * 0.3, size * 0.3, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(255, 255, 255, ${bead.opacity * 0.4})`;
                ctx.fill();

                // Concept label on hover area
                if (bead.concept && bead.opacity > 0.5) {
                    ctx.font = '9px monospace';
                    ctx.fillStyle = `rgba(200, 220, 255, ${bead.opacity * 0.7})`;
                    ctx.textAlign = 'left';
                    ctx.fillText(bead.concept.substring(0, 20), bead.x + size + 4, bead.y + 3);
                }
            });

            // Title
            ctx.font = '11px monospace';
            ctx.fillStyle = 'rgba(0, 229, 255, 0.6)';
            ctx.textAlign = 'center';
            ctx.fillText('Bastian Perrot\'s Abacus — "several dozen wires on which could be strung glass beads"', w / 2, 26);
        },
    };

    window.AbacusBoard = AbacusBoard;
})();

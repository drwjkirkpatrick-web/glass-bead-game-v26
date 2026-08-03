/**
 * Music Notation Module — VexFlow renderer for the Glass Bead Game
 *
 * Provides native music notation rendering for moves and sonifications.
 * Requires VexFlow 4.x loaded from CDN.
 *
 * @example
 *   window.MusicNotation.init('notation-container');
 *   window.MusicNotation.renderMove({
 *     from_concept: 'Harmony',
 *     to_concept:   'Symmetry',
 *     from_domain:  'musica',
 *     to_domain:    'mathematica',
 *     via:          'interval ratios'
 *   });
 *
 *   window.MusicNotation.renderSonification({
 *     notes: [
 *       { pitch: 'c/4', duration: 'q', velocity: 0.8 },
 *       { pitch: 'e/4', duration: 'q', velocity: 0.8 },
 *       { pitch: 'g/4', duration: 'h', velocity: 0.9 }
 *     ],
 *     bpm: 120
 *   });
 */
(function () {
  'use strict';

  // ------------------------------------------------------------------
  // Domain Configuration
  // ------------------------------------------------------------------
  const DOMAIN_CONFIG = {
    musica:      { pitch: 'c/4', duration: 'w', color: '#00e5ff', freq: 261.63 },
    mathematica: { pitch: 'e/4', duration: 'h', color: '#ff00ff', freq: 329.63 },
    historia:    { pitch: 'g/4', duration: 'q', color: '#ffd700', freq: 392.00 },
    natura:      { pitch: 'c/5', duration: 'w', color: '#00ff7f', freq: 523.25 },
    lingua:      { pitch: 'e/5', duration: 'h', color: '#ff6b6b', freq: 659.25 },
    philosophia: { pitch: 'g/5', duration: 'q', color: '#9370db', freq: 783.99 },
    technologia: { pitch: 'c/6', duration: 'w', color: '#ffa500', freq: 1046.50 },
    medicina:    { pitch: 'e/6', duration: 'h', color: '#ff69b4', freq: 1318.51 }
  };

  const THEME = {
    staveLine: 'rgba(201, 240, 255, 0.35)',
    text:      '#c9f0ff',
    tie:       'rgba(201, 240, 255, 0.6)',
    bg:        'transparent'
  };

  let defaultContainer = null;
  let audioCtx = null;

  // ------------------------------------------------------------------
  // Helpers
  // ------------------------------------------------------------------

  function getDomainConfig(domain) {
    return DOMAIN_CONFIG[domain] || DOMAIN_CONFIG.musica;
  }

  function ensureContainer(containerId) {
    const id = containerId || defaultContainer;
    if (!id) throw new Error('MusicNotation: no container specified and no default set');
    let el = document.getElementById(id);
    if (!el) {
      el = document.createElement('div');
      el.id = id;
      document.body.appendChild(el);
    }
    return el;
  }

  function createSubContainer(parent, className) {
    const div = document.createElement('div');
    div.className = className || 'music-notation-block';
    div.style.cssText = 'margin-bottom: 1rem; background: transparent;';
    parent.appendChild(div);
    return div;
  }

  function injectStyles() {
    if (document.getElementById('music-notation-styles')) return;
    const style = document.createElement('style');
    style.id = 'music-notation-styles';
    style.textContent = `
      .music-notation-block, .music-move-block, .music-sonification-block {
        background: transparent !important;
      }
      .music-notation-block svg, .music-move-block svg, .music-sonification-block svg {
        background: transparent !important;
      }
    `;
    document.head.appendChild(style);
  }

  function checkVexFlow() {
    if (typeof Vex === 'undefined' || !Vex.Flow) {
      throw new Error('MusicNotation: VexFlow not loaded. Ensure vexflow.js is included before this module.');
    }
  }

  // ------------------------------------------------------------------
  // Pitch ↔ Frequency (Web Audio)
  // ------------------------------------------------------------------

  function pitchToFreq(pitchStr) {
    if (typeof pitchStr === 'number') return pitchStr;
    let clean = String(pitchStr).toLowerCase().replace('/', '');
    const octaveMatch = clean.match(/\d+/);
    if (!octaveMatch) {
      // Fallback direct lookup
      for (const d of Object.values(DOMAIN_CONFIG)) {
        if (d.pitch === String(pitchStr).toLowerCase()) return d.freq;
      }
      return 440;
    }
    const octave = parseInt(octaveMatch[0], 10);
    const note = clean.replace(/\d+/, '');
    const chromatic = ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b'];
    const idx = chromatic.indexOf(note);
    if (idx === -1) return 440;
    const semisFromA4 = (octave - 4) * 12 + (idx - 9);
    return 440 * Math.pow(2, semisFromA4 / 12);
  }

  function durationToSeconds(duration, bpm) {
    const beatDur = 60 / bpm;
    const map = {
      w: 4, h: 2, q: 1, '8': 0.5, '16': 0.25,
      wd: 6, hd: 3, qd: 1.5, '8d': 0.75
    };
    return (map[duration] || 1) * beatDur;
  }

  // ------------------------------------------------------------------
  // VexFlow Render Helpers
  // ------------------------------------------------------------------

  function createRenderer(container, width, height) {
    checkVexFlow();
    const { Renderer } = Vex.Flow;
    const renderer = new Renderer(container, Renderer.Backends.SVG);
    renderer.resize(width, height);
    const context = renderer.getContext();
    const svg = container.querySelector('svg');
    if (svg) svg.style.background = 'transparent';
    return { renderer, context };
  }

  function createStyledNote(keys, duration, color) {
    const note = new Vex.Flow.StaveNote({
      keys: Array.isArray(keys) ? keys : [keys],
      duration: duration
    });
    if (color) {
      note.setStyle({ fillStyle: color, strokeStyle: color });
    }
    return note;
  }

  // ------------------------------------------------------------------
  // Public API
  // ------------------------------------------------------------------

  /**
   * Prepare a div for rendering and set it as the default container.
   */
  function init(containerId) {
    defaultContainer = containerId;
    injectStyles();
    const el = ensureContainer(containerId);
    el.style.background = 'transparent';
    return el;
  }

  /**
   * Remove all rendered notation from the default container.
   */
  function clear() {
    if (!defaultContainer) return;
    const el = document.getElementById(defaultContainer);
    if (el) el.innerHTML = '';
  }

  /**
   * Render a Glass Bead Game move as two notes on a stave connected by a tie.
   *
   * @param {Object} moveData
   * @param {string} moveData.from_concept
   * @param {string} moveData.to_concept
   * @param {string} moveData.from_domain
   * @param {string} moveData.to_domain
   * @param {string} moveData.via
   * @param {string} [targetId] – optional container override
   */
  function renderMove(moveData, targetId) {
    checkVexFlow();
    const container = ensureContainer(targetId);
    const block = createSubContainer(container, 'music-move-block');

    // Header
    const header = document.createElement('div');
    header.style.cssText =
      'font-family: JetBrains Mono, monospace; font-size: 0.75rem; ' +
      'color: #6b8f9c; margin-bottom: 0.4rem; letter-spacing: 0.05em;';
    header.textContent = `${moveData.from_concept || 'From'} → ${moveData.to_concept || 'To'}`;
    block.appendChild(header);

    const notationDiv = document.createElement('div');
    block.appendChild(notationDiv);

    const fromCfg = getDomainConfig(moveData.from_domain);
    const toCfg   = getDomainConfig(moveData.to_domain);

    const width  = 520;
    const height = 180;
    const { context } = createRenderer(notationDiv, width, height);

    const { Stave, StaveNote, Voice, Formatter, StaveTie, Annotation } = Vex.Flow;

    const staveX = 15;
    const staveY = 30;
    const staveW = width - 30;

    const stave = new Stave(staveX, staveY, staveW);
    stave.setStyle({ strokeStyle: THEME.staveLine });
    stave.addClef('treble').setContext(context).draw();

    // Notes
    const noteFrom = createStyledNote(fromCfg.pitch, fromCfg.duration, fromCfg.color);
    const noteTo   = createStyledNote(toCfg.pitch, toCfg.duration, toCfg.color);

    // Annotation: via label above first note
    if (moveData.via) {
      const ann = new Annotation(String(moveData.via));
      ann.setVerticalJustification(Annotation.VerticalJustify.TOP);
      ann.setFont('JetBrains Mono', 10, 'normal');
      ann.setStyle({ fillStyle: THEME.text, strokeStyle: THEME.text });
      noteFrom.addModifier(ann, 0);
    }

    // Domain labels below each note
    const labelFrom = new Annotation(moveData.from_domain || '');
    labelFrom.setVerticalJustification(Annotation.VerticalJustify.BOTTOM);
    labelFrom.setFont('JetBrains Mono', 9, 'normal');
    labelFrom.setStyle({ fillStyle: fromCfg.color, strokeStyle: fromCfg.color });
    noteFrom.addModifier(labelFrom, 0);

    const labelTo = new Annotation(moveData.to_domain || '');
    labelTo.setVerticalJustification(Annotation.VerticalJustify.BOTTOM);
    labelTo.setFont('JetBrains Mono', 9, 'normal');
    labelTo.setStyle({ fillStyle: toCfg.color, strokeStyle: toCfg.color });
    noteTo.addModifier(labelTo, 0);

    // Build a single voice sized to hold both notes
    const beatMap = { w: 4, h: 2, q: 1, '8': 0.5, '16': 0.25 };
    const fromBeats = beatMap[fromCfg.duration] || 1;
    const toBeats   = beatMap[toCfg.duration]   || 1;
    const totalBeats = fromBeats + toBeats;

    const voice = new Voice({ num_beats: totalBeats, beat_value: 4 });
    voice.addTickables([noteFrom, noteTo]);

    const formatter = new Formatter();
    formatter.joinVoices([voice]).format([voice], staveW - 30);

    context.setFillStyle(THEME.text);
    context.setStrokeStyle(THEME.staveLine);
    voice.draw(context, stave);

    // Tie / slur connecting the two notes
    if (noteFrom && noteTo) {
      const tie = new StaveTie({
        first_note: noteFrom,
        last_note:  noteTo
      });
      tie.setContext(context);
      tie.setStyle({ strokeStyle: THEME.tie, fillStyle: THEME.tie });
      tie.draw();
    }

    // Footer label
    const footer = document.createElement('div');
    footer.style.cssText =
      'font-family: JetBrains Mono, monospace; font-size: 0.7rem; ' +
      'color: #00ffaa; margin-top: 0.3rem; text-align: center; letter-spacing: 0.04em;';
    footer.textContent = `via: ${moveData.via || ''}`;
    block.appendChild(footer);
  }

  /**
   * Render a sonification as a melodic staff with a Play button.
   *
   * @param {Object} sonificationData
   * @param {Array}  sonificationData.notes – [{pitch, duration, velocity, color}]
   * @param {number} sonificationData.bpm
   * @param {string} [targetId] – optional container override
   */
  function renderSonification(sonificationData, targetId) {
    checkVexFlow();
    const container = ensureContainer(targetId);
    const block = createSubContainer(container, 'music-sonification-block');

    const bpm = sonificationData.bpm || 120;
    const notes = sonificationData.notes || [];

    // Header
    const header = document.createElement('div');
    header.style.cssText =
      'font-family: JetBrains Mono, monospace; font-size: 0.75rem; ' +
      'color: #6b8f9c; margin-bottom: 0.4rem; letter-spacing: 0.05em;';
    header.textContent = `Sonification — ${bpm} BPM · ${notes.length} note${notes.length !== 1 ? 's' : ''}`;
    block.appendChild(header);

    const notationDiv = document.createElement('div');
    block.appendChild(notationDiv);

    if (notes.length === 0) {
      notationDiv.textContent = 'No notes to render.';
      return;
    }

    const width  = Math.max(520, notes.length * 55 + 80);
    const height = 200;
    const { context } = createRenderer(notationDiv, width, height);

    const { Stave, StaveNote, Voice, Formatter } = Vex.Flow;

    const staveX = 15;
    const staveY = 40;
    const staveW = width - 30;

    const stave = new Stave(staveX, staveY, staveW);
    stave.setStyle({ strokeStyle: THEME.staveLine });
    stave.addClef('treble').setContext(context).draw();

    const vfNotes = [];
    let totalBeats = 0;
    const beatMap = { w: 4, h: 2, q: 1, '8': 0.5, '16': 0.25 };

    for (const n of notes) {
      const dur = n.duration || 'q';
      let pitch = n.pitch || 'c/4';
      // Normalise to VexFlow key format (e.g. "C4" → "c/4")
      if (!pitch.includes('/')) {
        pitch = String(pitch).toLowerCase().replace(/([a-g]#?b?)(\d+)/, '$1/$2');
      }
      const note = new StaveNote({ keys: [pitch], duration: dur });
      if (n.color) {
        note.setStyle({ fillStyle: n.color, strokeStyle: n.color });
      }
      vfNotes.push(note);
      totalBeats += beatMap[dur] || 1;
    }

    const measureBeats = Math.max(4, Math.ceil(totalBeats / 4) * 4);
    const voice = new Voice({ num_beats: measureBeats, beat_value: 4 });
    voice.addTickables(vfNotes);

    const formatter = new Formatter();
    formatter.joinVoices([voice]).format([voice], staveW - 30);

    context.setFillStyle(THEME.text);
    context.setStrokeStyle(THEME.staveLine);
    voice.draw(context, stave);

    // Play button
    const btn = document.createElement('button');
    btn.textContent = '▶ Play';
    btn.style.cssText = `
      margin-top: 0.6rem;
      padding: 0.35rem 1rem;
      font-family: JetBrains Mono, monospace;
      font-size: 0.75rem;
      background: rgba(0, 229, 255, 0.1);
      border: 1px solid rgba(0, 229, 255, 0.3);
      color: #00e5ff;
      border-radius: 4px;
      cursor: pointer;
      letter-spacing: 0.05em;
      transition: all 0.2s ease;
    `;
    btn.onmouseenter = () => {
      btn.style.background = 'rgba(0, 229, 255, 0.2)';
      btn.style.borderColor = 'rgba(0, 229, 255, 0.5)';
    };
    btn.onmouseleave = () => {
      btn.style.background = 'rgba(0, 229, 255, 0.1)';
      btn.style.borderColor = 'rgba(0, 229, 255, 0.3)';
    };
    btn.onclick = () => playSonification(sonificationData);
    block.appendChild(btn);
  }

  // ------------------------------------------------------------------
  // Web Audio Playback
  // ------------------------------------------------------------------

  function getAudioContext() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    return audioCtx;
  }

  function playSonification(sonificationData) {
    const ctx = getAudioContext();
    if (ctx.state === 'suspended') ctx.resume();

    const notes = sonificationData.notes || [];
    const bpm = sonificationData.bpm || 120;
    let t = ctx.currentTime + 0.05;

    for (const n of notes) {
      const freq = typeof n.pitch === 'number' ? n.pitch : pitchToFreq(n.pitch);
      const dur  = durationToSeconds(n.duration || 'q', bpm);
      const vel  = (n.velocity !== undefined ? n.velocity : 0.7);

      const osc  = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sine';
      osc.frequency.value = freq;

      gain.gain.setValueAtTime(vel * 0.3, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + dur);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(t);
      osc.stop(t + dur + 0.05);

      t += dur;
    }
  }

  // ------------------------------------------------------------------
  // Exports
  // ------------------------------------------------------------------
  window.MusicNotation = {
    init,
    renderMove,
    renderSonification,
    clear
  };
})();

/**
 * Live Terminal — real-time log panel for the Glass Bead Game HUD.
 *
 * Uses SocketIO (expected to be loaded on page).
 * Export: window.LiveTerminal = { init, log, clear, setMaxLines, getHistory }
 */

(function () {
  'use strict';

  const DEFAULT_MAX_LINES = 20;
  const DEFAULT_OPTIONS = {
    maxLines: DEFAULT_MAX_LINES,
    showTimestamp: true,
    autoScroll: true,
  };

  const LEVEL_CLASSES = {
    info: 'terminal-text',
    warn: 'terminal-warn',
    error: 'terminal-error',
    move: 'terminal-move',
    validation: 'terminal-move',
    system: 'terminal-text',
  };

  let container = null;
  let options = { ...DEFAULT_OPTIONS };
  let paused = false;
  let buffer = []; // used while paused
  let history = []; // persistent history

  /* ---------- helpers ---------- */

  function pad(n) {
    return String(n).padStart(2, '0');
  }

  function fmtTime(ts) {
    const d = ts ? new Date(ts) : new Date();
    return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
  }

  function levelClass(level) {
    return LEVEL_CLASSES[level] || 'terminal-text';
  }

  function levelLabel(level) {
    return (level || 'info').toUpperCase();
  }

  /* ---------- core rendering ---------- */

  function renderLine(entry) {
    const el = document.createElement('div');
    el.className = `terminal-line ${levelClass(entry.level)} fade-in`;

    const ts = options.showTimestamp ? `[${fmtTime(entry.timestamp)}] ` : '';
    const lvl = `[${levelLabel(entry.level)}]`;
    el.textContent = `${ts}${lvl} ${entry.message}`;

    return el;
  }

  function appendEntry(entry) {
    if (paused) {
      buffer.push(entry);
      return;
    }

    const line = renderLine(entry);
    container.appendChild(line);
    history.push(entry);

    trim();
    scrollToBottom();
  }

  function trim() {
    while (container.children.length > options.maxLines) {
      container.removeChild(container.firstChild);
    }
    while (history.length > options.maxLines * 2) {
      history.shift();
    }
  }

  function scrollToBottom() {
    if (options.autoScroll) {
      container.scrollTop = container.scrollHeight;
    }
  }

  function flushBuffer() {
    const b = buffer.slice();
    buffer = [];
    b.forEach(appendEntry);
  }

  /* ---------- toolbar ---------- */

  function buildToolbar() {
    const bar = document.createElement('div');
    bar.className = 'terminal-toolbar';

    const clearBtn = document.createElement('button');
    clearBtn.textContent = 'Clear';
    clearBtn.title = 'Clear terminal';
    clearBtn.addEventListener('click', () => {
      LiveTerminal.clear();
    });

    const pauseBtn = document.createElement('button');
    pauseBtn.textContent = 'Pause';
    pauseBtn.title = 'Pause / Resume updates';
    pauseBtn.addEventListener('click', () => {
      paused = !paused;
      pauseBtn.textContent = paused ? 'Resume' : 'Pause';
      pauseBtn.classList.toggle('paused', paused);
      if (!paused) flushBuffer();
    });

    bar.appendChild(clearBtn);
    bar.appendChild(pauseBtn);

    return bar;
  }

  /* ---------- overlay effects ---------- */

  function buildOverlay() {
    const overlay = document.createElement('div');
    overlay.className = 'terminal-scanlines';
    return overlay;
  }

  function buildCursor() {
    const cursor = document.createElement('span');
    cursor.className = 'terminal-cursor';
    return cursor;
  }

  /* ---------- public API ---------- */

  const LiveTerminal = {
    /**
     * Initialise the terminal panel.
     * @param {string} containerId — DOM element id for the terminal panel
     * @param {Object} [opts] — { maxLines, showTimestamp, autoScroll }
     */
    init(containerId, opts = {}) {
      const el = document.getElementById(containerId);
      if (!el) {
        console.error(`LiveTerminal: container #${containerId} not found`);
        return;
      }
      container = el;
      options = { ...DEFAULT_OPTIONS, ...opts };

      // Clear any existing content (safe: no untrusted HTML is injected here)
      container.innerHTML = '';

      // Wire SocketIO listeners (io expected globally)
      if (typeof io !== 'undefined') {
        const socket = io();

        socket.on('terminal_update', (data) => {
          LiveTerminal.log(data);
        });

        socket.on('terminal_history', (data) => {
          if (Array.isArray(data)) {
            data.forEach((entry) => LiveTerminal.log(entry));
          } else if (data && typeof data === 'object') {
            LiveTerminal.log(data);
          }
        });
      } else {
        console.warn('LiveTerminal: SocketIO (io) not found; terminal will not receive live updates.');
      }

      // Build toolbar if container is inside a wrapper with class "terminal-wrapper"
      // otherwise inject toolbar + scanlines right before container
      let wrapper = container.closest('.terminal-wrapper');
      if (!wrapper) {
        wrapper = document.createElement('div');
        wrapper.className = 'terminal-wrapper';
        container.parentNode.insertBefore(wrapper, container);
        wrapper.appendChild(container);
      }

      if (!wrapper.querySelector('.terminal-toolbar')) {
        wrapper.insertBefore(buildToolbar(), wrapper.firstChild);
      }
      if (!wrapper.querySelector('.terminal-scanlines')) {
        wrapper.appendChild(buildOverlay());
      }

      // Append blinking cursor at end of container
      container.appendChild(buildCursor());

      console.log('LiveTerminal initialised on #' + containerId);
    },

    /**
     * Log one entry.
     * @param {Object} entry — { timestamp, message, level }
     */
    log(entry) {
      if (!container) {
        console.warn('LiveTerminal not initialised; call init() first.');
        return;
      }
      if (!entry || typeof entry !== 'object') return;
      appendEntry(entry);
    },

    /** Empty the terminal panel (history is retained). */
    clear() {
      if (!container) return;
      container.innerHTML = '';
      container.appendChild(buildCursor());
      buffer = [];
    },

    /** Set maximum visible lines. */
    setMaxLines(n) {
      options.maxLines = Math.max(1, parseInt(n, 10) || DEFAULT_MAX_LINES);
      trim();
    },

    /** Return current in-memory history. */
    getHistory() {
      return history.slice();
    },
  };

  /* ---------- expose ---------- */
  if (typeof window !== 'undefined') {
    window.LiveTerminal = LiveTerminal;
  }
})();

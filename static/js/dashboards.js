/**
 * Dashboards.js — Shared SocketIO dashboard logic for audience, gameplay, and judges views.
 *
 * Exports: window.Dashboard = { init, connect, sendMove, validateMove, requestSonification, updateScoreboard, updateQueue, getGraphState }
 */

(function (global) {
  'use strict';

  // ─── Internal State ─────────────────────────────────────────────────────────
  let socket = null;
  let dashboardType = null; // 'audience' | 'gameplay' | 'judges'
  let graphStateData = null;
  let scene3D = null; // reference to a 3D scene controller, if available

  // ─── Helpers ──────────────────────────────────────────────────────────────────
  function log(...args) {
    console.log('[Dashboard]', ...args);
  }

  function emitIfAllowed(event, data) {
    if (!socket) {
      log('Socket not connected; cannot emit', event);
      return;
    }
    socket.emit(event, data);
  }

  // ─── Connection ───────────────────────────────────────────────────────────────
  function connect(url) {
    if (typeof io === 'undefined') {
      console.error('SocketIO library (io) is not loaded.');
      return;
    }
    socket = io(url || '/');
    log('SocketIO connecting to', url || '/');
  }

  // ─── Event Registration ───────────────────────────────────────────────────────
  function registerCommonHandlers() {
    if (!socket) return;

    socket.on('connect', () => {
      log('Connected');
      showConnectionStatus('connected');
      // Join the room corresponding to dashboard type
      if (dashboardType) {
        socket.emit('join_room', { room: dashboardType });
      }
    });

    socket.on('disconnect', () => {
      log('Disconnected');
      showConnectionStatus('reconnecting');
    });

    socket.on('joined', (data) => {
      log('Joined room:', data);
    });

    socket.on('graph_state', (data) => {
      graphStateData = data;
      if (scene3D && typeof scene3D.updateGraph === 'function') {
        scene3D.updateGraph(data);
      }
    });

    socket.on('graph_update', (data) => {
      graphStateData = data;
      if (scene3D && typeof scene3D.updateGraph === 'function') {
        scene3D.updateGraph(data);
      }
      if (scene3D && typeof scene3D.triggerEdgePulse === 'function') {
        scene3D.triggerEdgePulse(data);
      }
    });

    socket.on('terminal_update', (data) => {
      if (global.LiveTerminal && typeof global.LiveTerminal.handleUpdate === 'function') {
        global.LiveTerminal.handleUpdate(data);
      }
    });

    socket.on('terminal_history', (data) => {
      if (global.LiveTerminal && typeof global.LiveTerminal.handleHistory === 'function') {
        global.LiveTerminal.handleHistory(data);
      }
    });

    socket.on('move_submitted', (data) => {
      updateMoveFeed(data);
      if (dashboardType === 'judges') {
        appendToQueue(data);
      }
    });

    socket.on('move_validated', (data) => {
      updateScoreboard();
      highlightValidatedMove(data);
    });

    socket.on('sonification_ready', (data) => {
      if (global.MusicNotation && typeof global.MusicNotation.playSonification === 'function') {
        global.MusicNotation.playSonification(data);
      }
    });
  }

  // ─── Type-specific Registration ───────────────────────────────────────────────
  function registerAudienceHandlers() {
    // Audience is read-only; no additional emit handlers needed.
    log('Audience dashboard handlers registered (read-only)');
  }

  function registerGameplayHandlers() {
    // Gameplay exposes sendMove and requestSonification
    log('Gameplay dashboard handlers registered');
  }

  function registerJudgesHandlers() {
    // Judges expose validateMove
    log('Judges dashboard handlers registered');
  }

  // ─── UI Helpers ─────────────────────────────────────────────────────────────
  function showConnectionStatus(status) {
    const el = document.getElementById('connection-status');
    if (!el) return;
    if (status === 'connected') {
      el.textContent = 'Connected';
      el.className = 'status-connected';
    } else if (status === 'reconnecting') {
      el.textContent = 'Reconnecting…';
      el.className = 'status-reconnecting';
    }
  }

  function updateMoveFeed(data) {
    const feed = document.getElementById('move-feed');
    if (!feed) return;
    const entry = document.createElement('div');
    entry.className = 'move-entry';
    entry.textContent = JSON.stringify(data);
    feed.prepend(entry);
  }

  function highlightValidatedMove(data) {
    const feed = document.getElementById('move-feed');
    if (!feed) return;
    // Highlight the most recent matching entry or add a new one
    const entries = feed.querySelectorAll('.move-entry');
    for (const entry of entries) {
      if (entry.dataset.moveId === String(data.move_id)) {
        entry.classList.add('validated');
        break;
      }
    }
  }

  function appendToQueue(data) {
    const queue = document.getElementById('validation-queue');
    if (!queue) return;
    const item = document.createElement('div');
    item.className = 'queue-item';
    item.dataset.moveId = data.move_id || '';
    item.textContent = `Move #${data.move_id || '?'} – ${JSON.stringify(data)}`;
    queue.appendChild(item);
  }

  // ─── API Wrappers ─────────────────────────────────────────────────────────────
  function sendMove(moveData) {
    return new Promise((resolve, reject) => {
      fetch('/api/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(moveData)
      })
        .then((res) => {
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          return res.json();
        })
        .then((json) => {
          emitIfAllowed('move_submitted', json);
          resolve(json);
        })
        .catch(reject);
    });
  }

  function validateMove(moveId, scores, comments) {
    return new Promise((resolve, reject) => {
      fetch('/api/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ move_id: moveId, scores, comments })
      })
        .then((res) => {
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          return res.json();
        })
        .then(resolve)
        .catch(reject);
    });
  }

  function requestSonification(moveId) {
    emitIfAllowed('request_sonification', { move_id: moveId });
  }

  function updateScoreboard() {
    const panel = document.getElementById('scoreboard-panel');
    if (!panel) return Promise.resolve();
    return fetch('/api/scores')
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        panel.innerHTML = '';
        const container = document.createElement('div');
        container.className = 'scoreboard-container';
        if (Array.isArray(data) && data.length === 0) {
          container.textContent = 'No scores yet.';
        } else {
          const pre = document.createElement('pre');
          pre.textContent = JSON.stringify(data, null, 2);
          container.appendChild(pre);
        }
        panel.appendChild(container);
        return data;
      });
  }

  function updateQueue() {
    if (dashboardType !== 'judges') {
      log('updateQueue() is only available for judges dashboard');
      return Promise.resolve();
    }
    const queueEl = document.getElementById('validation-queue');
    if (!queueEl) return Promise.resolve();
    return fetch('/api/queue')
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        queueEl.innerHTML = '';
        if (Array.isArray(data)) {
          data.forEach((item) => {
            const div = document.createElement('div');
            div.className = 'queue-item';
            div.dataset.moveId = item.move_id || '';
            div.textContent = `Move #${item.move_id || '?'} – ${JSON.stringify(item)}`;
            queueEl.appendChild(div);
          });
        } else {
          queueEl.textContent = JSON.stringify(data, null, 2);
        }
        return data;
      });
  }

  function getGraphState() {
    return graphStateData;
  }

  // ─── Initialization ───────────────────────────────────────────────────────────
  function init(type, options) {
    if (!['audience', 'gameplay', 'judges'].includes(type)) {
      throw new Error(`Invalid dashboard type: ${type}. Must be 'audience', 'gameplay', or 'judges'.`);
    }
    dashboardType = type;
    options = options || {};

    connect(options.socketUrl);
    registerCommonHandlers();

    switch (type) {
      case 'audience':
        registerAudienceHandlers();
        break;
      case 'gameplay':
        registerGameplayHandlers();
        break;
      case 'judges':
        registerJudgesHandlers();
        break;
    }

    log(`Dashboard initialized as '${type}'`);
  }

  // ─── Public API ───────────────────────────────────────────────────────────────
  const Dashboard = {
    init,
    connect,
    sendMove,
    validateMove,
    requestSonification,
    updateScoreboard,
    updateQueue,
    getGraphState
  };

  global.Dashboard = Dashboard;
})(window);

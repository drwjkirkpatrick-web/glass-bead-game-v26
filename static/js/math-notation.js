/**
 * Math Notation Module — KaTeX renderer for the Glass Bead Game
 *
 * Provides native mathematical notation rendering for formulas, moves,
 * and graph metrics. Loads KaTeX 0.16.9 from CDN on first use.
 *
 * @example
 *   window.MathNotation.init().then(() => {
 *     window.MathNotation.renderFormula('E = mc^2', 'output');
 *   });
 */
(function () {
  'use strict';

  // ------------------------------------------------------------------
  // Constants
  // ------------------------------------------------------------------
  const KATEX_VERSION = '0.16.9';
  const KATEX_JS_URL  = `https://cdn.jsdelivr.net/npm/katex@${KATEX_VERSION}/dist/katex.min.js`;
  const KATEX_CSS_URL = `https://cdn.jsdelivr.net/npm/katex@${KATEX_VERSION}/dist/katex.min.css`;

  // ------------------------------------------------------------------
  // State
  // ------------------------------------------------------------------
  let katexReady = false;
  let initPromise = null;

  // ------------------------------------------------------------------
  // Helpers
  // ------------------------------------------------------------------

  /**
   * Inject a <link rel="stylesheet"> into <head> if not already present.
   */
  function injectCss(url) {
    if (document.querySelector(`link[href="${url}"]`)) return;
    const link = document.createElement('link');
    link.rel  = 'stylesheet';
    link.href = url;
    document.head.appendChild(link);
  }

  /**
   * Dynamically load the KaTeX JS library.
   */
  function loadScript(url) {
    return new Promise((resolve, reject) => {
      if (window.katex) { resolve(); return; }
      const script = document.createElement('script');
      script.src = url;
      script.async = true;
      script.onload = resolve;
      script.onerror = () => reject(new Error(`Failed to load KaTeX from ${url}`));
      document.head.appendChild(script);
    });
  }

  /**
   * Ensure a target DOM element exists, creating it if necessary.
   */
  function ensureElement(containerId) {
    let el = document.getElementById(containerId);
    if (!el) {
      el = document.createElement('div');
      el.id = containerId;
      document.body.appendChild(el);
    }
    // Clean any previous content
    el.innerHTML = '';
    return el;
  }

  /**
   * Wrap rendered KaTeX output in a dark-theme container that honours CSS
   * variables for text colour.
   */
  function createMathContainer(className = 'math-notation-block') {
    const wrap = document.createElement('div');
    wrap.className = className;
    return wrap;
  }

  // ------------------------------------------------------------------
  // Public API
  // ------------------------------------------------------------------

  const MathNotation = {

    /**
     * Initialise the module:
     *   - inject KaTeX CSS (if absent)
     *   - load KaTeX JS (if absent)
     *   - return a Promise that resolves when rendering is ready.
     */
    init() {
      if (initPromise) return initPromise;

      initPromise = new Promise(async (resolve, reject) => {
        try {
          injectCss(KATEX_CSS_URL);
          await loadScript(KATEX_JS_URL);
          katexReady = true;

          // Inject dark-theme overrides once
          if (!document.getElementById('katex-dark-theme')) {
            const style = document.createElement('style');
            style.id = 'katex-dark-theme';
            style.textContent = `
              .math-notation-block .katex,
              .math-notation-block .katex-display {
                color: var(--gfg-text, #f0f0f0);
              }
              .math-notation-block .katex .katex-html {
                color: var(--gfg-text, #f0f0f0);
              }
              .math-notation-block .katex .base {
                color: var(--gfg-text, #f0f0f0);
              }
            `;
            document.head.appendChild(style);
          }

          resolve();
        } catch (err) {
          reject(err);
        }
      });

      return initPromise;
    },

    /**
     * Render a single formula string into a container.
     *
     * @param {string} formula   LaTeX formula (e.g. "E = mc^2")
     * @param {string} containerId  Target element ID
     * @returns {HTMLElement|null}  The wrapper element, or null on failure
     */
    renderFormula(formula, containerId) {
      if (!katexReady || !window.katex) {
        console.warn('[MathNotation] KaTeX not ready — call init() first');
        return null;
      }

      const container = ensureElement(containerId);
      const wrap = createMathContainer('math-notation-block');
      container.appendChild(wrap);

      try {
        window.katex.render(formula, wrap, {
          throwOnError: false,
          displayMode: true,
        });
      } catch (err) {
        console.error('[MathNotation] renderFormula failed:', err);
        wrap.textContent = formula; // fallback to plain text
      }
      return wrap;
    },

    /**
     * Render a Glass Bead Game move as a structured mathematical statement.
     *
     * @param {Object} moveData
     *   - from      {string}  Origin bead name
     *   - to        {string}  Target bead name
     *   - via       {string}  LaTeX-formulaic bridge (optional)
     *   - description {string} Human-readable summary (fallback)
     * @param {string} containerId  Target element ID
     * @returns {HTMLElement|null}
     */
    renderMove(moveData, containerId) {
      if (!katexReady || !window.katex) {
        console.warn('[MathNotation] KaTeX not ready — call init() first');
        return null;
      }

      const container = ensureElement(containerId);
      const { from, to, via, description } = moveData || {};

      // Build LaTeX from move data
      let latexParts = [];

      if (via && typeof via === 'string') {
        // Use provided LaTeX via string
        latexParts.push(via);
      } else {
        // Auto-generate canonical move notation
        const fromLabel = from ? `\\text{${from}}` : '\\text{source}';
        const toLabel   = to   ? `\\text{${to}}`   : '\\text{target}';

        // Example: Bach canon <-> Möbius strip
        latexParts.push(`f_{${fromLabel}}: \\mathbb{Z} \\to \\mathbb{Z}, \\quad f(n) = n + k \\pmod{N}`);
        latexParts.push('\\text{isomorphic to}');
        latexParts.push(`\\gamma: S^1 \\to S^1, \\quad ${toLabel}`);
      }

      // If there's a description, add it as an annotation
      if (description && typeof description === 'string') {
        latexParts.push(`\\text{(${description})}`);
      }

      const wrap = createMathContainer('math-notation-block');
      container.appendChild(wrap);

      latexParts.forEach((part) => {
        const block = document.createElement('div');
        block.style.marginBottom = '0.5em';
        wrap.appendChild(block);
        try {
          window.katex.render(part, block, {
            throwOnError: false,
            displayMode: true,
          });
        } catch (err) {
          console.error('[MathNotation] renderMove failed for part:', part, err);
          block.textContent = part; // fallback
        }
      });

      return wrap;
    },

    /**
     * Render graph metrics as mathematical formulas.
     *
     * @param {Object} graphData
     *   - nodeCount      {number}
     *   - edgeCount      {number}
     *   - density        {number}  (optional — computed if absent)
     *   - averageDegree  {number}  (optional — computed if absent)
     * @param {string} containerId  Target element ID
     * @returns {HTMLElement|null}
     */
    renderGraphMetrics(graphData, containerId) {
      if (!katexReady || !window.katex) {
        console.warn('[MathNotation] KaTeX not ready — call init() first');
        return null;
      }

      const container = ensureElement(containerId);
      const { nodeCount: N, edgeCount: E } = graphData || {};

      if (typeof N !== 'number' || typeof E !== 'number') {
        console.warn('[MathNotation] graphData requires numeric nodeCount and edgeCount');
        return null;
      }

      const density       = graphData.density      ?? (N > 1 ? (2 * E) / (N * (N - 1)) : 0);
      const averageDegree = graphData.averageDegree  ?? (N > 0 ? (2 * E) / N : 0);

      const formulas = [
        `N = |V| = ${N}`,
        `E = |E| = ${E}`,
        `\\rho = \\frac{2E}{N(N-1)} = \\frac{2 \\cdot ${E}}{${N}(${N} - 1)} = ${density.toFixed(4)}`,
        `\\bar{d} = \\frac{2E}{N} = \\frac{2 \\cdot ${E}}{${N}} = ${averageDegree.toFixed(4)}`,
      ];

      const wrap = createMathContainer('math-notation-block');
      container.appendChild(wrap);

      formulas.forEach((formula) => {
        const block = document.createElement('div');
        block.style.marginBottom = '0.5em';
        wrap.appendChild(block);
        try {
          window.katex.render(formula, block, {
            throwOnError: false,
            displayMode: true,
          });
        } catch (err) {
          console.error('[MathNotation] renderGraphMetrics failed:', err);
          block.textContent = formula;
        }
      });

      return wrap;
    },

    /**
     * Remove all rendered math from a container.
     *
     * @param {string} containerId  Target element ID
     */
    clear(containerId) {
      const el = document.getElementById(containerId);
      if (el) el.innerHTML = '';
    },

  };

  // ------------------------------------------------------------------
  // Export
  // ------------------------------------------------------------------
  if (typeof window !== 'undefined') {
    window.MathNotation = MathNotation;
  }
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = MathNotation;
  }
})();

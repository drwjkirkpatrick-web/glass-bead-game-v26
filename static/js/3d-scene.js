/**
 * Glass Bead Game v26 — Three.js Knowledge Graph Visualization (ES Module)
 *
 * Renders glass bead nodes and their connections in 3D space.
 * Integrates with SocketIO for live updates from the Flask backend.
 */
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// ─── Configuration ───────────────────────────────────────
const CONFIG = {
    backgroundColor: 0x050508,
    fogDensity: 0.02,
    baseScale: 0.5,
    maxNodes: 100,
    floatSpeed: 0.001,
    floatAmplitude: 0.3,
    autoRotateSpeed: 0.3,
    idleTimeout: 5000,
    pulseSpeed: 2.5,
    enableShadows: false,
};

// ─── Globals ─────────────────────────────────────────────
let scene, camera, renderer, controls;
let nodesMap = new Map();
let edgesGroup, nodesGroup, pulseGroup;
let raycaster, mouse;
let hoveredMesh = null;
let animationId = null;
let lastInteractionTime = Date.now();
let isAutoRotating = true;
let socket = null;
let graphData = { nodes: [], edges: [] };
let starField = null;

// Shared geometry for performance
const sharedGeo = new THREE.IcosahedronGeometry(1, 1);

// ─── Scene Init ──────────────────────────────────────────
function init(containerSelector) {
    // Support both '#id' and 'id' forms
    const sel = containerSelector.startsWith('#') ? containerSelector : '#' + containerSelector;
    const container = document.querySelector(sel) || document.getElementById(containerSelector);
    if (!container) {
        console.error('3D scene container not found:', containerSelector);
        return;
    }

    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(CONFIG.backgroundColor);
    scene.fog = new THREE.FogExp2(CONFIG.backgroundColor, CONFIG.fogDensity);

    // Camera
    const aspect = container.clientWidth / container.clientHeight;
    camera = new THREE.PerspectiveCamera(45, aspect, 0.1, 1000);
    camera.position.set(12, 8, 12);

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.0;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.shadowMap.enabled = CONFIG.enableShadows;
    container.appendChild(renderer.domElement);

    // Controls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.enablePan = true;
    controls.enableRotate = true;
    controls.enableZoom = true;
    controls.autoRotate = true;
    controls.autoRotateSpeed = CONFIG.autoRotateSpeed;

    // Lights
    const ambient = new THREE.AmbientLight(0x404040, 0.5);
    scene.add(ambient);

    const cyanLight = new THREE.PointLight(0x00e5ff, 1.5, 50);
    cyanLight.position.set(-10, 8, -10);
    scene.add(cyanLight);

    const magentaLight = new THREE.PointLight(0xff00ff, 1.5, 50);
    magentaLight.position.set(10, 8, -10);
    scene.add(magentaLight);

    const goldLight = new THREE.PointLight(0xffd700, 1.5, 50);
    goldLight.position.set(0, -8, 10);
    scene.add(goldLight);

    // ─── Environment ─────────────────────────────────────────
    // Grid floor
    const gridHelper = new THREE.GridHelper(40, 40, 0x1a1a2e, 0x0d0d1a);
    gridHelper.position.y = -6;
    scene.add(gridHelper);

    // Starfield
    const starGeo = new THREE.BufferGeometry();
    const starCount = 3000;
    const starPositions = new Float32Array(starCount * 3);
    for (let i = 0; i < starCount * 3; i++) {
        starPositions[i] = (Math.random() - 0.5) * 200;
    }
    starGeo.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
    const starMat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.15, transparent: true, opacity: 0.6 });
    starField = new THREE.Points(starGeo, starMat);
    scene.add(starField);

    // Groups
    nodesGroup = new THREE.Group();
    edgesGroup = new THREE.Group();
    pulseGroup = new THREE.Group();
    scene.add(nodesGroup);
    scene.add(edgesGroup);
    scene.add(pulseGroup);

    // Raycaster
    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    // Event listeners
    renderer.domElement.addEventListener('mousemove', onMouseMove, { passive: true });
    renderer.domElement.addEventListener('click', onClick);
    renderer.domElement.addEventListener('dblclick', onDoubleClick);
    window.addEventListener('resize', onResize);

    // SocketIO
    initSocketIO();

    // Initial graph
    fetchGraph().then((data) => {
        if (data) buildGraph(data);
    });

    animate();
}

// ─── Graph Building ──────────────────────────────────────
function clearGraph() {
    nodesMap.forEach((obj) => {
        if (obj.mesh) {
            if (obj.mesh.geometry) obj.mesh.geometry.dispose();
            if (obj.mesh.material) obj.mesh.material.dispose();
            if (obj.glowLight) nodesGroup.remove(obj.glowLight);
            if (obj.labelDiv && obj.labelDiv.parentNode) {
                obj.labelDiv.parentNode.removeChild(obj.labelDiv);
            }
        }
    });
    nodesMap.clear();

    while (edgesGroup.children.length > 0) {
        const child = edgesGroup.children[0];
        edgesGroup.remove(child);
        if (child.geometry) child.geometry.dispose();
        if (child.material) child.material.dispose();
    }

    while (pulseGroup.children.length > 0) {
        const child = pulseGroup.children[0];
        pulseGroup.remove(child);
        if (child.geometry) child.geometry.dispose();
        if (child.material) child.material.dispose();
    }
}

function buildGraph(data) {
    if (!data || !Array.isArray(data.nodes)) return;
    graphData = data;
    clearGraph();

    const nodes = data.nodes.slice(0, CONFIG.maxNodes);
    const edges = data.edges || [];

    nodes.forEach((node) => createNode(node));
    edges.forEach((edge) => createEdge(edge));
}

function createNode(node) {
    const radius = (node.size || 0.8) * CONFIG.baseScale;
    const geometry = sharedGeo.clone();
    geometry.scale(radius, radius, radius);

    const color = new THREE.Color(node.color || '#00e5ff');

    // Glass-like physical material
    const material = new THREE.MeshPhysicalMaterial({
        color: color,
        emissive: color.clone().multiplyScalar(0.25),
        emissiveIntensity: 0.4,
        metalness: 0.1,
        roughness: 0.15,
        transmission: 0.5,
        transparent: true,
        opacity: 0.9,
        clearcoat: 1.0,
        clearcoatRoughness: 0.1,
        ior: 1.5,
        thickness: 1.0,
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(node.x || 0, node.y || 0, node.z || 0);
    mesh.castShadow = CONFIG.enableShadows;
    mesh.receiveShadow = CONFIG.enableShadows;
    mesh.userData = { node: node, originalY: node.y || 0 };

    // Internal glow light
    const glowLight = new THREE.PointLight(color, 0.6, radius * 10);
    glowLight.position.copy(mesh.position);
    nodesGroup.add(glowLight);
    nodesGroup.add(mesh);

    // Floating label
    const labelDiv = createLabel(node.label || node.id, color);
    labelDiv.style.position = 'absolute';
    labelDiv.style.pointerEvents = 'none';
    labelDiv.style.transition = 'transform 0.1s linear, opacity 0.2s ease';
    labelDiv.style.opacity = '0.7';
    document.body.appendChild(labelDiv);

    nodesMap.set(node.id, {
        mesh: mesh,
        glowLight: glowLight,
        labelDiv: labelDiv,
        node: node,
        floatOffset: Math.random() * Math.PI * 2,
    });
}

function createLabel(text, colorObj) {
    const div = document.createElement('div');
    div.className = 'bead-label';
    div.textContent = text;
    div.style.color = '#' + colorObj.getHexString();
    div.style.fontFamily = '"JetBrains Mono", monospace';
    div.style.fontSize = '11px';
    div.style.fontWeight = '500';
    div.style.textShadow = '0 0 4px rgba(0,0,0,0.9)';
    div.style.whiteSpace = 'nowrap';
    div.style.transform = 'translate(-50%, -120%)';
    div.style.letterSpacing = '0.02em';
    return div;
}

function createEdge(edge) {
    const sourceObj = nodesMap.get(edge.source);
    const targetObj = nodesMap.get(edge.target);
    if (!sourceObj || !targetObj) return;

    const start = sourceObj.mesh.position.clone();
    const end = targetObj.mesh.position.clone();

    // Curved tube
    const path = new THREE.CatmullRomCurve3([
        start,
        new THREE.Vector3(
            (start.x + end.x) / 2 + (Math.random() - 0.5) * 0.5,
            (start.y + end.y) / 2 + (Math.random() - 0.5) * 0.5,
            (start.z + end.z) / 2 + (Math.random() - 0.5) * 0.5
        ),
        end,
    ]);

    const tubeGeo = new THREE.TubeGeometry(path, 20, 0.03 * (edge.strength || 0.5), 8, false);
    const tubeMat = new THREE.MeshBasicMaterial({
        color: 0x6688aa,
        transparent: true,
        opacity: 0.2,
        depthWrite: false,
    });
    const tube = new THREE.Mesh(tubeGeo, tubeMat);
    tube.userData = { edge: edge, isEdge: true };
    edgesGroup.add(tube);

    // Thin line overlay
    const lineGeo = new THREE.BufferGeometry().setFromPoints([start, end]);
    const lineMat = new THREE.LineBasicMaterial({
        color: 0x88aabb,
        transparent: true,
        opacity: 0.35,
        depthWrite: false,
    });
    const line = new THREE.Line(lineGeo, lineMat);
    line.userData = { edge: edge, isEdge: true };
    edgesGroup.add(line);
}

// ─── Data Fetching ───────────────────────────────────────
async function fetchGraph() {
    try {
        const resp = await fetch('/api/graph');
        if (!resp.ok) throw new Error('Graph fetch failed');
        return await resp.json();
    } catch (err) {
        console.warn('fetchGraph error:', err);
        return null;
    }
}

// ─── SocketIO ────────────────────────────────────────────
function initSocketIO() {
    if (typeof io === 'undefined') {
        console.warn('SocketIO not available');
        return;
    }
    socket = io({ transports: ['websocket', 'polling'] });

    socket.on('connect', () => {
        console.log('SocketIO connected');
    });

    socket.on('graph_update', (payload) => {
        if (payload && payload.nodes && payload.edges) {
            buildGraph(payload);
        }
    });

    socket.on('graph_state', (payload) => {
        if (payload && payload.nodes && payload.edges) {
            buildGraph(payload);
        }
    });

    socket.on('move_validated', (move) => {
        if (move && move.status === 'validated') {
            animateNewEdge(move);
        }
    });
}

// ─── Animation ───────────────────────────────────────────
function animateNewEdge(move) {
    const edges = graphData.edges || [];
    if (!edges.length) return;
    const latestEdge = edges[edges.length - 1];
    pulseEdge(latestEdge);
}

function pulseEdge(edge) {
    const sourceObj = nodesMap.get(edge.source);
    const targetObj = nodesMap.get(edge.target);
    if (!sourceObj || !targetObj) return;

    const start = sourceObj.mesh.position.clone();
    const end = targetObj.mesh.position.clone();

    const pulseGeo = new THREE.SphereGeometry(0.15, 16, 16);
    const pulseMat = new THREE.MeshBasicMaterial({
        color: 0xffffff,
        transparent: true,
        opacity: 0.9,
        depthWrite: false,
    });
    const pulseMesh = new THREE.Mesh(pulseGeo, pulseMat);
    pulseMesh.position.copy(start);
    pulseGroup.add(pulseMesh);

    const duration = 1200;
    const startTime = performance.now();

    function step(now) {
        const elapsed = now - startTime;
        const t = Math.min(elapsed / duration, 1);
        pulseMesh.position.lerpVectors(start, end, t);
        pulseMesh.material.opacity = 0.9 * (1 - t);
        const scale = 1 + t * 2;
        pulseMesh.scale.set(scale, scale, scale);

        if (t < 1) {
            requestAnimationFrame(step);
        } else {
            pulseGroup.remove(pulseMesh);
            pulseGeo.dispose();
            pulseMat.dispose();
        }
    }
    requestAnimationFrame(step);
}

// ─── Interaction ─────────────────────────────────────────
function onMouseMove(event) {
    const rect = renderer.domElement.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(nodesGroup.children.filter(c => c.isMesh), false);

    if (hoveredMesh) {
        hoveredMesh.material.emissiveIntensity = hoveredMesh.userData.baseEmissive || 0.4;
        hoveredMesh = null;
    }

    if (intersects.length > 0) {
        const hit = intersects[0].object;
        if (hit.isMesh) {
            hoveredMesh = hit;
            hit.userData.baseEmissive = hit.material.emissiveIntensity;
            hit.material.emissiveIntensity = 1.2;
        }
    }

    lastInteractionTime = Date.now();
    if (controls) controls.autoRotate = false;
}

function onClick(event) {
    const rect = renderer.domElement.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(nodesGroup.children.filter(c => c.isMesh), false);

    if (intersects.length > 0) {
        const hit = intersects[0].object;
        const nodeData = hit.userData.node;
        if (nodeData) {
            window.dispatchEvent(new CustomEvent('bead_selected', { detail: nodeData }));
        }
    }
}

function onDoubleClick(event) {
    const rect = renderer.domElement.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(nodesGroup.children.filter(c => c.isMesh), false);

    if (intersects.length > 0) {
        const target = intersects[0].object.position.clone();
        const offset = camera.position.clone().sub(controls.target).normalize().multiplyScalar(8);
        const newPos = target.clone().add(offset);

        const duration = 800;
        const startPos = camera.position.clone();
        const startTarget = controls.target.clone();
        const startTime = performance.now();

        function ease(t) { return t < 0.5 ? 2*t*t : -1 + (4-2*t)*t; }

        function step(now) {
            const elapsed = now - startTime;
            const t = Math.min(elapsed / duration, 1);
            const e = ease(t);
            camera.position.lerpVectors(startPos, newPos, e);
            controls.target.lerpVectors(startTarget, target, e);
            if (t < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }
}

function onResize() {
    const container = renderer.domElement.parentElement;
    if (!container) return;
    const aspect = container.clientWidth / container.clientHeight;
    camera.aspect = aspect;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

// ─── Main Loop ───────────────────────────────────────────
function animate() {
    animationId = requestAnimationFrame(animate);
    const time = Date.now();

    // Floating animation
    nodesMap.forEach((obj) => {
        if (obj.mesh) {
            obj.mesh.position.y = obj.node.y + Math.sin(time * CONFIG.floatSpeed + obj.floatOffset) * CONFIG.floatAmplitude;
            obj.glowLight.position.copy(obj.mesh.position);
        }
    });

    // Label positioning
    nodesMap.forEach((obj) => {
        if (obj.mesh && obj.labelDiv) {
            const pos = obj.mesh.position.clone();
            pos.project(camera);
            const x = (pos.x * 0.5 + 0.5) * renderer.domElement.clientWidth;
            const y = (-pos.y * 0.5 + 0.5) * renderer.domElement.clientHeight;
            obj.labelDiv.style.transform = `translate(-50%, -120%) translate(${x}px, ${y}px)`;
            obj.labelDiv.style.opacity = pos.z < 1 ? '0.7' : '0.15';
        }
    });

    // Auto-rotate resume
    if (!isAutoRotating && time - lastInteractionTime > CONFIG.idleTimeout) {
        controls.autoRotate = true;
    }

    // Starfield slow rotation
    if (starField) {
        starField.rotation.y += 0.0002;
    }

    controls.update();
    renderer.render(scene, camera);
}

// ─── Public API ──────────────────────────────────────────
window.GlassBeadScene = {
    init,
    updateGraph: buildGraph,
    highlightNode: (nodeId) => {
        const obj = nodesMap.get(nodeId);
        if (obj && obj.mesh) {
            obj.mesh.material.emissiveIntensity = 2.0;
            setTimeout(() => {
                if (obj.mesh) obj.mesh.material.emissiveIntensity = 0.4;
            }, 1500);
        }
    },
    focusNode: (nodeId) => {
        const obj = nodesMap.get(nodeId);
        if (obj && obj.mesh) {
            const target = obj.mesh.position.clone();
            const offset = camera.position.clone().sub(controls.target).normalize().multiplyScalar(6);
            camera.position.copy(target.clone().add(offset));
            controls.target.copy(target);
            controls.update();
        }
    },
};

console.log('GlassBeadScene module loaded (ESM)');

// Auto-init when DOM is ready (modules are deferred)
if (typeof document !== 'undefined') {
    function autoInit() {
        const container = document.getElementById('scene-container');
        if (container && !renderer) {
            console.log('Auto-init GlassBeadScene on scene-container');
            init('scene-container');
        }
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', autoInit);
    } else {
        // Already loaded
        setTimeout(autoInit, 100);
    }
}

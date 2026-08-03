"""
Glass Bead Game v26
Main Flask application with SocketIO live updates.
A 3D glass bead visualization of the Modern Glass Bead Game.
"""
import os
import json
import random
from datetime import datetime

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, join_room, leave_room

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, async_mode=Config.ASYNC_MODE, cors_allowed_origins="*")

# In-memory game state (upgrade to SQLite later)
game_state = {
    'nodes': [],
    'edges': [],
    'moves': [],
    'scores': {},
    'players': {},
    'session_active': False,
    'current_move': None,
    'validation_queue': [],
    'terminal_log': [],
}

# Sample seeded data
def seed_graph():
    """Seed the knowledge graph with initial nodes."""
    domains = Config.DOMAINS
    for i, domain in enumerate(domains):
        node = {
            'id': f'node_{i}',
            'domain': domain,
            'label': f'{Config.BEAD_TYPES[domain]["name"]}',
            'x': random.uniform(-5, 5),
            'y': random.uniform(-5, 5),
            'z': random.uniform(-5, 5),
            'color': Config.BEAD_TYPES[domain]['color'],
            'size': 0.8,
            'timestamp': datetime.utcnow().isoformat(),
        }
        game_state['nodes'].append(node)
    
    # Seed some edges
    for i in range(len(domains)):
        j = (i + 1) % len(domains)
        edge = {
            'id': f'edge_{i}_{j}',
            'source': f'node_{i}',
            'target': f'node_{j}',
            'strength': 0.5,
            'label': f'{domains[i]} → {domains[j]}',
            'timestamp': datetime.utcnow().isoformat(),
        }
        game_state['edges'].append(edge)

seed_graph()

def log_to_terminal(message, level='info'):
    """Add a message to the live terminal log."""
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'message': message,
        'level': level,
    }
    game_state['terminal_log'].append(entry)
    socketio.emit('terminal_update', entry, namespace='/')

# ─── Routes ───────────────────────────────────────────────

@app.route('/')
def index():
    """Main 3D glass bead game visualization."""
    return render_template('index.html', 
                         game_name=Config.GAME_NAME,
                         game_version=Config.GAME_VERSION)

@app.route('/audience')
def audience():
    """Read-only audience dashboard."""
    return render_template('audience.html',
                         game_name=Config.GAME_NAME,
                         game_version=Config.GAME_VERSION)

@app.route('/gameplay')
def gameplay():
    """Active gameplay dashboard."""
    return render_template('gameplay.html',
                         game_name=Config.GAME_NAME,
                         game_version=Config.GAME_VERSION,
                         bead_types=Config.BEAD_TYPES,
                         domains=Config.DOMAINS)

@app.route('/judges')
def judges():
    """Judges evaluation dashboard."""
    return render_template('judges.html',
                         game_name=Config.GAME_NAME,
                         game_version=Config.GAME_VERSION)

# ─── API Endpoints ────────────────────────────────────────

@app.route('/api/graph', methods=['GET'])
def get_graph():
    """Return current knowledge graph state."""
    return jsonify({
        'nodes': game_state['nodes'],
        'edges': game_state['edges'],
    })

@app.route('/api/move', methods=['POST'])
def submit_move():
    """Submit a Glass Bead Game move."""
    data = request.json
    move = {
        'id': f"move_{len(game_state['moves'])}_{int(datetime.utcnow().timestamp())}",
        'bead': data.get('bead'),
        'from_concept': data.get('from_concept'),
        'from_domain': data.get('from_domain'),
        'to_concept': data.get('to_concept'),
        'to_domain': data.get('to_domain'),
        'via': data.get('via'),
        'resonance': data.get('resonance'),
        'timestamp': datetime.utcnow().isoformat(),
        'status': 'pending_validation',
        'scores': {},
    }
    game_state['moves'].append(move)
    game_state['validation_queue'].append(move['id'])
    
    log_to_terminal(f"Move submitted: {move['bead']} | {move['from_concept']} → {move['to_concept']}", 'move')
    
    # Broadcast to all dashboards
    socketio.emit('move_submitted', move, namespace='/')
    
    return jsonify({'status': 'submitted', 'move': move})

@app.route('/api/validate', methods=['POST'])
def validate_move():
    """Judge validates a move."""
    data = request.json
    move_id = data.get('move_id')
    scores = data.get('scores', {})
    
    for move in game_state['moves']:
        if move['id'] == move_id:
            move['status'] = 'validated'
            move['scores'] = scores
            move['total_score'] = sum(scores.values())
            
            # If valid, add node/edge to graph
            if scores.get('valid', False):
                # Add target node if new
                existing = [n for n in game_state['nodes'] if n['label'] == move['to_concept']]
                if not existing:
                    new_node = {
                        'id': f"node_{len(game_state['nodes'])}",
                        'domain': move['to_domain'],
                        'label': move['to_concept'],
                        'x': random.uniform(-8, 8),
                        'y': random.uniform(-8, 8),
                        'z': random.uniform(-8, 8),
                        'color': Config.BEAD_TYPES.get(move['to_domain'], {}).get('color', '#ffffff'),
                        'size': 0.6,
                        'timestamp': datetime.utcnow().isoformat(),
                    }
                    game_state['nodes'].append(new_node)
                
                # Add edge
                source_nodes = [n for n in game_state['nodes'] if n['label'] == move['from_concept']]
                target_nodes = [n for n in game_state['nodes'] if n['label'] == move['to_concept']]
                if source_nodes and target_nodes:
                    edge = {
                        'id': f"edge_{source_nodes[0]['id']}_{target_nodes[0]['id']}",
                        'source': source_nodes[0]['id'],
                        'target': target_nodes[0]['id'],
                        'strength': move['total_score'] / 40.0,
                        'label': move['via'],
                        'timestamp': datetime.utcnow().isoformat(),
                    }
                    game_state['edges'].append(edge)
                    
                    socketio.emit('graph_update', {
                        'nodes': game_state['nodes'],
                        'edges': game_state['edges'],
                    }, namespace='/')
            
            log_to_terminal(f"Move validated: {move['from_concept']} → {move['to_concept']} | Score: {move.get('total_score', 0)}", 'validation')
            socketio.emit('move_validated', move, namespace='/')
            break
    
    return jsonify({'status': 'validated'})

@app.route('/api/scores', methods=['GET'])
def get_scores():
    """Get current scoreboard."""
    return jsonify(game_state['scores'])

@app.route('/api/queue', methods=['GET'])
def get_queue():
    """Get pending validation queue."""
    pending = [m for m in game_state['moves'] if m['status'] == 'pending_validation']
    return jsonify(pending)

@app.route('/api/terminal', methods=['GET'])
def get_terminal_log():
    """Get terminal log history."""
    return jsonify(game_state['terminal_log'][-50:])

# ─── Math ↔ Music Transformer API ────────────────────────

from src.math_music_transformer import get_transformer as get_mm_transformer

@app.route('/api/transform', methods=['POST'])
def transform_math_music():
    """Execute a single Math ↔ Music transformation."""
    data = request.get_json() or {}
    transformer = get_mm_transformer()
    result = transformer.transform(
        origin_concept=data.get('origin_concept', ''),
        origin_domain=data.get('origin_domain', ''),
        destination_domain=data.get('destination_domain', ''),
        structural_property=data.get('structural_property', ''),
        resonance_sentence=data.get('resonance_sentence', ''),
        tokens=data.get('tokens', []),
    )
    log_to_terminal(f"Transformer: {result.origin_concept} → {result.destination_concept} ({result.total_confidence})", 'move')
    return jsonify(result.to_dict())

@app.route('/api/transform/batch', methods=['POST'])
def transform_batch():
    """Batch transform multiple moves."""
    data = request.get_json() or {}
    moves = data.get('moves', [])
    transformer = get_mm_transformer()
    results = transformer.batch_transform(moves)
    log_to_terminal(f"Batch transform: {len(results)} moves processed", 'system')
    return jsonify([r.to_dict() for r in results])

@app.route('/api/transform/catalog', methods=['GET'])
def get_transform_catalog():
    """Browse the isomorphism library."""
    transformer = get_mm_transformer()
    return jsonify(transformer.get_isomorphism_catalog())

@app.route('/api/transform/entropy', methods=['POST'])
def transform_entropy():
    """Compute token entropy for a transformation."""
    import math
    data = request.get_json() or {}
    tokens = data.get('tokens', [])
    if not tokens:
        return jsonify({"entropy": 0.0, "peak_stage": "N/A"})
    from collections import Counter
    counts = Counter(tokens)
    total = len(tokens)
    entropy = -sum((c/total) * math.log2(c/total) for c in counts.values())
    return jsonify({"entropy": round(entropy, 3), "peak_stage": data.get('current_stage', 'UNKNOWN')})

# ─── Knowledge Transformer APIs (19 domain-pair transformers) ─────────────
# Each transformer follows the same pattern as the Math↔Music transformer above:
# POST  /api/transform/<pair>         → single transformation
# GET   /api/transform/<pair>/catalog → browse isomorphisms

from src.math_philosophy_transformer import get_transformer as get_mp_transformer
from src.music_language_transformer import get_transformer as get_ml_transformer
from src.history_philosophy_transformer import get_transformer as get_hp_transformer
from src.nature_math_transformer import get_transformer as get_nm_transformer
from src.philosophy_language_transformer import get_transformer as get_pl_transformer
from src.nature_music_transformer import get_transformer as get_nmu_transformer
from src.technology_math_transformer import get_transformer as get_tm_transformer
from src.medicine_nature_transformer import get_transformer as get_mn_transformer
from src.history_music_transformer import get_transformer as get_hm_transformer
from src.philosophy_music_transformer import get_transformer as get_pmu_transformer

# ── 8 new Coda (Computer Code) transformers ──
from src.code_math_transformer import get_transformer as get_cm_transformer
from src.code_music_transformer import get_transformer as get_cmu_transformer
from src.code_language_transformer import get_transformer as get_cl_transformer
from src.code_philosophy_transformer import get_transformer as get_cp_transformer
from src.code_technology_transformer import get_transformer as get_ct_transformer
from src.code_nature_transformer import get_transformer as get_cn_transformer
from src.code_history_transformer import get_transformer as get_ch_transformer
from src.code_medicine_transformer import get_transformer as get_cmd_transformer

_KT_REGISTRY = {
    'math-philosophy':    get_mp_transformer,
    'music-language':     get_ml_transformer,
    'history-philosophy': get_hp_transformer,
    'nature-math':        get_nm_transformer,
    'philosophy-language': get_pl_transformer,
    'nature-music':       get_nmu_transformer,
    'technology-math':    get_tm_transformer,
    'medicine-nature':     get_mn_transformer,
    'history-music':       get_hm_transformer,
    'philosophy-music':    get_pmu_transformer,
    # ── Coda pairs (8 new) ──
    'code-math':           get_cm_transformer,
    'code-music':          get_cmu_transformer,
    'code-language':       get_cl_transformer,
    'code-philosophy':     get_cp_transformer,
    'code-technology':     get_ct_transformer,
    'code-nature':         get_cn_transformer,
    'code-history':        get_ch_transformer,
    'code-medicine':       get_cmd_transformer,
}


@app.route('/api/transform/<pair>', methods=['POST'])
def transform_knowledge_pair(pair):
    """Execute a single knowledge-pair transformation."""
    if pair not in _KT_REGISTRY:
        return jsonify({"error": f"Unknown transformer pair: {pair}"}), 404
    data = request.get_json() or {}
    transformer = _KT_REGISTRY[pair]()
    result = transformer.transform(
        origin_concept=data.get('origin_concept', ''),
        origin_domain=data.get('origin_domain', ''),
        destination_domain=data.get('destination_domain', ''),
        structural_property=data.get('structural_property', ''),
        resonance_sentence=data.get('resonance_sentence', ''),
        tokens=data.get('tokens', []),
    )
    log_to_terminal(f"Transformer[{pair}]: {result.origin_concept} → {result.destination_concept} ({result.total_confidence})", 'move')
    return jsonify(result.to_dict())


@app.route('/api/transform/<pair>/catalog', methods=['GET'])
def get_kt_catalog(pair):
    """Browse the isomorphism library for a knowledge-pair transformer."""
    if pair not in _KT_REGISTRY:
        return jsonify({"error": f"Unknown transformer pair: {pair}"}), 404
    transformer = _KT_REGISTRY[pair]()
    return jsonify(transformer.get_isomorphism_catalog())


@app.route('/api/transform/<pair>/batch', methods=['POST'])
def batch_transform_kt(pair):
    """Batch transform multiple moves through a knowledge-pair transformer."""
    if pair not in _KT_REGISTRY:
        return jsonify({"error": f"Unknown transformer pair: {pair}"}), 404
    data = request.get_json() or {}
    moves = data.get('moves', [])
    transformer = _KT_REGISTRY[pair]()
    results = transformer.batch_transform(moves)
    log_to_terminal(f"Batch[{pair}]: {len(results)} moves processed", 'system')
    return jsonify([r.to_dict() for r in results])


@app.route('/api/transform/all/catalog', methods=['GET'])
def get_all_kt_catalogs():
    """Browse all 19 knowledge transformer catalogs at once."""
    catalogs = {}
    for pair, get_fn in _KT_REGISTRY.items():
        try:
            catalogs[pair] = get_fn().get_isomorphism_catalog()
        except Exception as exc:
            catalogs[pair] = {"error": str(exc)}
    return jsonify(catalogs)


# ─── Pathway Selection API ────────────────────────────────────

from src.pathway_selector import get_selector as get_pathway_selector

@app.route('/api/pathways', methods=['GET'])
def list_all_pathways():
    """List all 19 transformer pathways available in the Game."""
    selector = get_pathway_selector()
    pathways = selector.list_all_pathways()
    return jsonify({
        'total': len(pathways),
        'pathways': [p.to_dict() for p in pathways],
    })


@app.route('/api/pathways/from/<domain>', methods=['GET'])
def list_pathways_from_domain(domain):
    """List all direct transformer pathways from a given domain."""
    selector = get_pathway_selector()
    pathways = selector.list_direct_pathways(domain)
    return jsonify({
        'domain': domain,
        'count': len(pathways),
        'pathways': [p.to_dict() for p in pathways],
    })


@app.route('/api/pathways/find', methods=['POST'])
def find_pathways():
    """Find all pathways (direct + multi-hop) between two domains."""
    data = request.get_json() or {}
    source = data.get('source_domain', '')
    destination = data.get('destination_domain', '')
    max_hops = data.get('max_hops', 3)

    selector = get_pathway_selector()

    # Direct pathway
    direct_slug = selector.find_pair_slug(source, destination)
    direct = None
    if direct_slug:
        p = selector.select_pathway(direct_slug)
        if p:
            direct = p.to_dict()

    # Multi-hop pathways
    multi_hops = selector.find_multi_hop_paths(source, destination, max_hops=max_hops)

    return jsonify({
        'source': source,
        'destination': destination,
        'direct': direct,
        'multi_hop': [mh.to_dict() for mh in multi_hops],
        'total_routes': (1 if direct else 0) + len(multi_hops),
    })


@app.route('/api/pathways/select', methods=['POST'])
def select_and_execute_pathway():
    """Select a pathway by pair slug and execute a transformation through it."""
    data = request.get_json() or {}
    pair_slug = data.get('pair_slug', '')
    selector = get_pathway_selector()

    result = selector.execute_transform(
        pair_slug=pair_slug,
        origin_concept=data.get('origin_concept', ''),
        origin_domain=data.get('origin_domain', ''),
        destination_domain=data.get('destination_domain', ''),
        structural_property=data.get('structural_property', ''),
        resonance_sentence=data.get('resonance_sentence', ''),
        tokens=data.get('tokens', []),
    )

    if result is None:
        return jsonify({"error": f"Unknown or unloadable transformer pair: {pair_slug}"}), 404

    log_to_terminal(f"Pathway[{pair_slug}]: {result['origin_concept']} → {result['destination_concept']} ({result['total_confidence']})", 'move')
    return jsonify(result)


@app.route('/api/pathways/catalog', methods=['GET'])
def pathway_catalog():
    """Full catalog of all pathway metadata."""
    selector = get_pathway_selector()
    return jsonify(selector.get_pathway_catalog())


@app.route('/api/pathways/adjacency', methods=['GET'])
def pathway_adjacency():
    """Domain adjacency graph showing which domains connect to which."""
    selector = get_pathway_selector()
    return jsonify(selector.get_domain_adjacency())


# ─── Gap Module APIs ─────────────────────────────────────

@app.route('/api/theme/build', methods=['POST'])
def build_theme():
    """Build a fugue-like compositional arc (Theme → CounterSubject → Episode → Stretto → Coda)."""
    from src.theme_engine import Theme, CounterSubject, Episode, Stretto, Coda, FugueBuilder
    data = request.get_json() or {}
    try:
        builder = FugueBuilder()
        builder.set_theme(Theme(concept=data.get('theme_concept', ''), domain=data.get('theme_domain', '')))
        if data.get('counter_concept'):
            builder.set_counter_subject(CounterSubject(
                concept=data['counter_concept'],
                relation=data.get('counter_relation', 'contrapuntal'),
                direction=data.get('counter_direction', 'inverted'),
            ))
        if data.get('episode_themes'):
            builder.add_episode(Episode(themes=data['episode_themes'], modulations=data.get('modulations', [])))
        if data.get('stretto_themes'):
            builder.add_stretto(Stretto(
                themes=data['stretto_themes'],
                compression=data.get('stretto_compression', 0.5),
            ))
        builder.set_coda(Coda(resolution=data.get('coda_resolution', 'return to tonic')))
        move = builder.build()
        log_to_terminal(f"Theme engine: built fugue for {move.theme.concept}", 'move')
        return jsonify({"move": move.to_dict(), "narrative": builder.narrate()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/dialectic', methods=['POST'])
def run_dialectic():
    """Run a Thesis-Antithesis-Synthesis game."""
    from src.dialectic_engine import DialecticGame
    data = request.get_json() or {}
    try:
        game = DialecticGame(
            thesis_concept=data.get('thesis', ''),
            antithesis_concept=data.get('antithesis', ''),
            thesis_domain=data.get('thesis_domain', ''),
            antithesis_domain=data.get('antithesis_domain', ''),
        )
        synthesis = game.build()
        scores = game.score_synthesis()
        log_to_terminal(f"Dialectic: {synthesis.thesis.concept} + {synthesis.antithesis.concept} → synthesis", 'move')
        return jsonify({"synthesis": synthesis.to_dict(), "scores": scores})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/contemplate', methods=['POST'])
def contemplate():
    """Begin or complete a formal contemplation session."""
    from src.contemplation import ContemplationSession
    data = request.get_json() or {}
    session = ContemplationSession(player_name=data.get('player', 'Anonymous'))
    for phase in ['preparation', 'recollection', 'concentration', 'insight', 'integration']:
        if phase in data.get('phases', []):
            session.complete_phase(phase, data.get(f'{phase}_notes', ''))
    depth = session.compute_depth()
    log_to_terminal(f"Contemplation: {session.player_name} — depth {depth}", 'move')
    return jsonify({"session": session.to_dict(), "depth": depth})

@app.route('/api/ceremony', methods=['POST'])
def create_ceremony():
    """Create a ceremonial match."""
    from src.ceremony import Ceremony, Audience, FestivalType
    data = request.get_json() or {}
    try:
        fest_type = FestivalType.LUDUS_SOLLEMNIS if data.get('type') == 'sollemnis' else FestivalType.LUDUS_ANNIVERSARIUS
        ceremony = Ceremony(
            magister_presiding=data.get('magister', ''),
            festival_type=fest_type,
            audience=Audience(size=data.get('audience_size', 100), reverence_score=data.get('reverence', 0.7)),
        )
        log_to_terminal(f"Ceremony: {ceremony.festival_type.name} under {ceremony.magister_presiding}", 'system')
        return jsonify({"ceremony": ceremony.to_dict()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/magister/evaluate', methods=['POST'])
def magister_evaluate():
    """Evaluate a game from the Ludi Magister perspective."""
    from src.magister import Magister, GameEvaluation
    data = request.get_json() or {}
    magister = Magister(name=data.get('magister_name', 'Magister'))
    evaluation = GameEvaluation(
        technical_virtuosity=data.get('technical_virtuosity', 0.0),
        contemplative_depth=data.get('contemplative_depth', 0.0),
        synthesis_quality=data.get('synthesis_quality', 0.0),
        ceremonial_presence=data.get('ceremonial_presence', 0.0),
    )
    magister.evaluate_player(data.get('player', ''), evaluation)
    log_to_terminal(f"Magister {magister.name} evaluated {data.get('player', '')}: {evaluation.overall_score()}", 'move')
    return jsonify({"evaluation": evaluation.to_dict(), "magister": magister.to_dict()})

@app.route('/api/play-mode', methods=['POST'])
def check_play_mode():
    """Check or transition a player's play mode."""
    from src.play_modes import PlayerProgression, PlayMode
    data = request.get_json() or {}
    prog = PlayerProgression(player_name=data.get('player', 'Test'))
    # Simulate some progress
    for _ in range(data.get('verified_moves', 0)):
        prog.checklist.record_verified_move()
    prog.checklist.contemplation_hours = data.get('contemplation_hours', 0)
    for peer in data.get('peer_endorsements', []):
        prog.checklist.add_peer_endorsement(peer)
    if data.get('magister_reviewed'):
        prog.checklist.magister_review = True
    can_transition, reason = prog.transition_to_public()
    return jsonify({"can_transition": can_transition, "reason": reason, "current_mode": str(prog.current_mode)})

# ─── Strategy Improvement APIs ─────────────────────────

# Lazy imports — modules are created by background subagents

# 1. Player Identity
@app.route('/api/player/current', methods=['GET'])
def get_current_player():
    """Return the current player's Castalian Identity Card."""
    from src.player_identity import PlayerIdentity
    p = PlayerIdentity(name='Joseph Knecht', rank='Ludi Magister', province='Waldzell')
    p.add_verified_move(); p.add_verified_move(); p.add_contemplation_hours(10)
    p.domain_mastery['musica'] = 0.95
    p.domain_mastery['mathematica'] = 0.88
    return jsonify(p.to_dict())

@app.route('/api/player/<name>', methods=['GET'])
def get_player(name):
    from src.player_identity import PlayerIdentity
    p = PlayerIdentity(name=name)
    return jsonify(p.to_dict())

# 2. Move Repertoire
@app.route('/api/repertoire/current', methods=['GET'])
def get_repertoire():
    """Return the current player's move archive."""
    from src.repertoire import Repertoire
    rep = Repertoire()
    rep.add_move({'from_concept': 'Z_12', 'to_concept': 'Circle of fifths', 'isomorphism': 'cyclic', 'score': 0.92, 'date': '2026-08-01'})
    rep.add_move({'from_concept': 'Fourier', 'to_concept': 'Overtone', 'isomorphism': 'fourier', 'score': 0.97, 'date': '2026-08-01'})
    return jsonify(rep.to_dict())

# 3. The Pulse
@app.route('/api/pulse', methods=['GET'])
def get_pulse():
    """Live move stream with trending domains."""
    from src.pulse import MoveFeed
    feed = MoveFeed()
    return jsonify({'moves': feed.get_recent(), 'trending': feed.get_trending_domains()})

@app.route('/api/pulse/trending', methods=['GET'])
def get_trending():
    from src.pulse import MoveFeed
    return jsonify(MoveFeed().get_trending_domains())

# 4. Hermes Critic
@app.route('/api/critic/analyze', methods=['POST'])
def critic_analyze():
    """Pre-submission move analysis."""
    from src.critic import CriticEngine
    data = request.get_json() or {}
    result = CriticEngine().analyze_move(data)
    return jsonify(result)

# 5. Tournament
@app.route('/api/tournament/current', methods=['GET'])
def get_tournament():
    """Current Ludus Sollemnis bracket."""
    from src.tournament import Tournament, FestivalType
    t = Tournament(tournament_id='sollemnis-2026', festival_type=FestivalType.LUDUS_SOLLEMNIS)
    t.seed_players([
        {'name': 'Joseph Knecht', 'rank': 0.96},
        {'name': 'Fritz Tegularius', 'rank': 0.87},
        {'name': 'Master Thomas', 'rank': 0.95},
        {'name': 'Plinio Designori', 'rank': 0.89},
    ])
    return jsonify(t.to_dict())

# 6. Bead Library
@app.route('/api/beads', methods=['GET'])
def get_beads():
    from src.bead_library import BeadCatalog
    catalog = BeadCatalog()
    catalog.add_bead('Z_12', 'mathematica', '#ff3333', 'Z_n under + mod n')
    catalog.add_bead('Circle of Fifths', 'musica', '#3399ff', 'P5^12 ≡ tonic')
    catalog.add_bead('Fourier Transform', 'mathematica', '#ff6600', '∫ f(t)e^{-iωt}dt', popularity=0.88)
    return jsonify(catalog.to_dict())

# 7. Sonification
@app.route('/api/sonify/state', methods=['GET'])
def sonify_state():
    from src.sonification import SonificationEngine
    return jsonify(SonificationEngine().sonify_state({'active_domains': ['musica', 'mathematica']}))

@app.route('/api/sonify/move', methods=['POST'])
def sonify_move():
    from src.sonification import SonificationEngine
    data = request.get_json() or {}
    return jsonify(SonificationEngine().sonify_move(data.get('from_domain', ''), data.get('to_domain', ''), data.get('confidence', 0.8)))

# 8. Pathfinder
@app.route('/api/pathfinder', methods=['POST'])
def pathfinder():
    from src.pathfinder import GraphPathfinder
    pf = GraphPathfinder()
    for n in game_state['nodes']:
        pf.add_node(n)
    for e in game_state['edges']:
        pf.add_edge(e)
    data = request.get_json() or {}
    return jsonify(pf.find_path(data.get('from', ''), data.get('to', '')))

@app.route('/api/pathfinder/random', methods=['GET'])
def random_path():
    import random
    from src.pathfinder import GraphPathfinder
    pf = GraphPathfinder()
    for n in game_state['nodes']:
        pf.add_node(n)
    for e in game_state['edges']:
        pf.add_edge(e)
    nodes = list(pf.nodes.keys())
    if len(nodes) < 2:
        return jsonify({'error': 'Not enough nodes'})
    a, b = random.sample(nodes, 2)
    return jsonify(pf.find_path(a, b))

# 9. Replay
@app.route('/api/replay/latest', methods=['GET'])
def get_latest_replay():
    from src.replay import GameRecording
    return jsonify(GameRecording().to_dict())

@app.route('/api/replay/<replay_id>', methods=['GET'])
def get_replay(replay_id):
    from src.replay import GameRecording
    return jsonify(GameRecording().to_dict())

# 10. Matchmaking
@app.route('/api/matchmaking/find', methods=['POST'])
def find_match():
    from src.matchmaking import Matchmaker
    mm = Matchmaker()
    mm.add_player('Joseph Knecht', {'musica': 0.9, 'mathematica': 0.8, 'historia': 0.5, 'philosophia': 0.6})
    mm.add_player('Fritz Tegularius', {'philosophia': 0.9, 'historia': 0.8, 'musica': 0.4, 'mathematica': 0.3})
    mm.add_player('Master Thomas', {'musica': 0.95, 'mathematica': 0.7, 'historia': 0.7, 'philosophia': 0.5})
    data = request.get_json() or {}
    return jsonify(mm.find_match(data.get('player', '')))

@app.route('/api/matchmaking/compatibility/<a>/<b>', methods=['GET'])
def compatibility(a, b):
    from src.matchmaking import Matchmaker
    mm = Matchmaker()
    mm.add_player('Joseph Knecht', {'musica': 0.9, 'mathematica': 0.8, 'historia': 0.5, 'philosophia': 0.6})
    mm.add_player('Fritz Tegularius', {'philosophia': 0.9, 'historia': 0.8, 'musica': 0.4, 'mathematica': 0.3})
    mm.add_player('Master Thomas', {'musica': 0.95, 'mathematica': 0.7, 'historia': 0.7, 'philosophia': 0.5})
    return jsonify({'player_a': a, 'player_b': b, 'compatibility': mm.get_compatibility(a, b)})

# ─── New Dashboard Route ────────────────────────────────

@app.route('/dashboard')
def dashboard():
    """Unified strategy dashboard with all 10 panels."""
    return render_template('dashboard.html')

# ─── SocketIO Events ────────────────────────────────────

@socketio.on('connect')
def handle_connect():
    log_to_terminal('New connection established', 'system')
    emit('graph_state', {
        'nodes': game_state['nodes'],
        'edges': game_state['edges'],
    })
    emit('terminal_history', game_state['terminal_log'][-50:])

@socketio.on('disconnect')
def handle_disconnect():
    log_to_terminal('Connection closed', 'system')

@socketio.on('join_room')
def on_join(data):
    room = data.get('room', 'default')
    join_room(room)
    emit('joined', {'room': room}, room=room)

@socketio.on('leave_room')
def on_leave(data):
    room = data.get('room', 'default')
    leave_room(room)

@socketio.on('request_sonification')
def handle_sonification(data):
    """Generate sonification for a move."""
    move_id = data.get('move_id')
    move = next((m for m in game_state['moves'] if m['id'] == move_id), None)
    if move:
        # Simple sonification: map domains to pitch classes
        domain_pitches = {
            'musica': 60,      # C4
            'mathematica': 64, # E4
            'historia': 67,    # G4
            'natura': 72,      # C5
            'lingua': 76,      # E5
            'philosophia': 79, # G5
            'technologia': 84, # C6
            'medicina': 88,    # E6
            'coda': 92,        # F#6
        }
        from_pitch = domain_pitches.get(move['from_domain'], 60)
        to_pitch = domain_pitches.get(move['to_domain'], 60)
        
        sonification = {
            'move_id': move_id,
            'notes': [
                {'pitch': from_pitch, 'duration': 1.0, 'velocity': 0.7},
                {'pitch': to_pitch, 'duration': 1.5, 'velocity': 0.8},
                {'pitch': (from_pitch + to_pitch) // 2, 'duration': 2.0, 'velocity': 0.6},
            ],
            'bpm': 60 + abs(from_pitch - to_pitch) * 2,
        }
        emit('sonification_ready', sonification)

# ─── Main ───────────────────────────────────────────────

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9297, debug=Config.DEBUG)

"""
glass-bead-game-v26 — Pathway Selector
Lets a player choose which transformer pathway to use for a Glass Bead Game move.

The Glass Bead Game has 9 disciplines (domains) and 19 transformer pairs
connecting them.  Given a source domain and a destination domain, the
PathwaySelector resolves the correct transformer, lists available pathways
(multi-hop routes through intermediate disciplines), and lets the player
choose which pathway to activate.

Inspired by Hesse, *Das Glasperlenspiel*:
    "The Game was a contest of the purest kind, a competition in which
    the player was required to weave together the most diverse content
    into a unity." — and the pathway is the thread of that weaving.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict
import importlib


# ─── Transformer Registry ──────────────────────────────────────
# Maps a pair slug (e.g. 'code-math') to the module path and getter function.
# The 11 original pairs + 8 new Coda pairs = 19 total.

TRANSFORMER_REGISTRY: Dict[str, Dict[str, Any]] = {
    # ── Original 11 transformers ──
    'math-music': {
        'module': 'src.math_music_transformer',
        'getter': 'get_transformer',
        'domains': ('mathematica', 'musica'),
    },
    'math-philosophy': {
        'module': 'src.math_philosophy_transformer',
        'getter': 'get_transformer',
        'domains': ('mathematica', 'philosophia'),
    },
    'music-language': {
        'module': 'src.music_language_transformer',
        'getter': 'get_transformer',
        'domains': ('musica', 'lingua'),
    },
    'history-philosophy': {
        'module': 'src.history_philosophy_transformer',
        'getter': 'get_transformer',
        'domains': ('historia', 'philosophia'),
    },
    'nature-math': {
        'module': 'src.nature_math_transformer',
        'getter': 'get_transformer',
        'domains': ('natura', 'mathematica'),
    },
    'philosophy-language': {
        'module': 'src.philosophy_language_transformer',
        'getter': 'get_transformer',
        'domains': ('philosophia', 'lingua'),
    },
    'nature-music': {
        'module': 'src.nature_music_transformer',
        'getter': 'get_transformer',
        'domains': ('natura', 'musica'),
    },
    'technology-math': {
        'module': 'src.technology_math_transformer',
        'getter': 'get_transformer',
        'domains': ('technologia', 'mathematica'),
    },
    'medicine-nature': {
        'module': 'src.medicine_nature_transformer',
        'getter': 'get_transformer',
        'domains': ('medicina', 'natura'),
    },
    'history-music': {
        'module': 'src.history_music_transformer',
        'getter': 'get_transformer',
        'domains': ('historia', 'musica'),
    },
    'philosophy-music': {
        'module': 'src.philosophy_music_transformer',
        'getter': 'get_transformer',
        'domains': ('philosophia', 'musica'),
    },
    # ── 8 new Coda transformers ──
    'code-math': {
        'module': 'src.code_math_transformer',
        'getter': 'get_transformer',
        'domains': ('coda', 'mathematica'),
    },
    'code-music': {
        'module': 'src.code_music_transformer',
        'getter': 'get_transformer',
        'domains': ('coda', 'musica'),
    },
    'code-language': {
        'module': 'src.code_language_transformer',
        'getter': 'get_transformer',
        'domains': ('coda', 'lingua'),
    },
    'code-philosophy': {
        'module': 'src.code_philosophy_transformer',
        'getter': 'get_transformer',
        'domains': ('coda', 'philosophia'),
    },
    'code-technology': {
        'module': 'src.code_technology_transformer',
        'getter': 'get_transformer',
        'domains': ('coda', 'technologia'),
    },
    'code-nature': {
        'module': 'src.code_nature_transformer',
        'getter': 'get_transformer',
        'domains': ('coda', 'natura'),
    },
    'code-history': {
        'module': 'src.code_history_transformer',
        'getter': 'get_transformer',
        'domains': ('coda', 'historia'),
    },
    'code-medicine': {
        'module': 'src.code_medicine_transformer',
        'getter': 'get_transformer',
        'domains': ('coda', 'medicina'),
    },
}


@dataclass
class Pathway:
    """A single transformer pathway between two domains."""
    pair_slug: str               # e.g. 'code-math'
    source_domain: str           # e.g. 'coda'
    destination_domain: str      # e.g. 'mathematica'
    module_path: str             # e.g. 'src.code_math_transformer'
    isomorphism_count: int = 0   # filled lazily
    description: str = ""        # human-readable summary

    def to_dict(self) -> Dict[str, Any]:
        return {
            'pair_slug': self.pair_slug,
            'source_domain': self.source_domain,
            'destination_domain': self.destination_domain,
            'module_path': self.module_path,
            'isomorphism_count': self.isomorphism_count,
            'description': self.description,
        }


@dataclass
class MultiHopPath:
    """A multi-hop route through intermediate disciplines."""
    hops: List[str]              # domain sequence: ['coda', 'mathematica', 'musica']
    pair_slugs: List[str]        # transformer slug per hop: ['code-math', 'math-music']
    total_hops: int = 0
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            'hops': self.hops,
            'pair_slugs': self.pair_slugs,
            'total_hops': self.total_hops,
            'description': self.description,
        }


class PathwaySelector:
    """
    Resolves and selects transformer pathways for Glass Bead Game moves.

    Given a source and destination domain, the selector:
      1. Finds the direct transformer pair (if one exists)
      2. Lists multi-hop pathways through intermediate domains
      3. Lets the player choose which pathway to activate
      4. Lazily loads the chosen transformer and executes the transformation
    """

    def __init__(self):
        self._adjacency: Dict[str, List[str]] = defaultdict(list)
        self._build_adjacency()
        self._loaded_transformers: Dict[str, Any] = {}

    def _build_adjacency(self) -> None:
        """Build domain adjacency graph from the registry."""
        for slug, info in TRANSFORMER_REGISTRY.items():
            d1, d2 = info['domains']
            if d2 not in self._adjacency[d1]:
                self._adjacency[d1].append(d2)
            if d1 not in self._adjacency[d2]:
                self._adjacency[d2].append(d1)

    def find_pair_slug(self, source: str, destination: str) -> Optional[str]:
        """Find the direct transformer pair slug for two domains."""
        for slug, info in TRANSFORMER_REGISTRY.items():
            d1, d2 = info['domains']
            if {d1, d2} == {source, destination}:
                return slug
        return None

    def list_direct_pathways(self, domain: str) -> List[Pathway]:
        """List all direct pathways from a given domain."""
        pathways = []
        for slug, info in TRANSFORMER_REGISTRY.items():
            d1, d2 = info['domains']
            if d1 == domain or d2 == domain:
                source = d1 if d1 == domain else d2
                dest = d2 if d1 == domain else d1
                pathways.append(Pathway(
                    pair_slug=slug,
                    source_domain=source,
                    destination_domain=dest,
                    module_path=info['module'],
                    description=f"{source} ↔ {dest} via {slug}",
                ))
        return pathways

    def list_all_pathways(self) -> List[Pathway]:
        """List all 19 transformer pathways."""
        pathways = []
        for slug, info in TRANSFORMER_REGISTRY.items():
            d1, d2 = info['domains']
            pathways.append(Pathway(
                pair_slug=slug,
                source_domain=d1,
                destination_domain=d2,
                module_path=info['module'],
                description=f"{d1} ↔ {d2} via {slug}",
            ))
        return pathways

    def find_multi_hop_paths(
        self,
        source: str,
        destination: str,
        max_hops: int = 3,
    ) -> List[MultiHopPath]:
        """Find multi-hop paths from source to destination via BFS."""
        if source == destination:
            return []

        visited = {source}
        queue: List[Tuple[str, List[str], List[str]]] = [(source, [source], [])]
        results: List[MultiHopPath] = []

        while queue:
            current, path_domains, path_slugs = queue.pop(0)

            for neighbor in self._adjacency.get(current, []):
                if neighbor in visited:
                    continue
                slug = self.find_pair_slug(current, neighbor)
                if not slug:
                    continue

                new_domains = path_domains + [neighbor]
                new_slugs = path_slugs + [slug]

                if neighbor == destination:
                    results.append(MultiHopPath(
                        hops=new_domains,
                        pair_slugs=new_slugs,
                        total_hops=len(new_slugs),
                        description=" → ".join(new_domains),
                    ))
                elif len(new_slugs) < max_hops:
                    visited.add(neighbor)
                    queue.append((neighbor, new_domains, new_slugs))

        return results

    def select_pathway(self, pair_slug: str) -> Optional[Pathway]:
        """Select a single pathway by its pair slug."""
        info = TRANSFORMER_REGISTRY.get(pair_slug)
        if not info:
            return None
        d1, d2 = info['domains']
        return Pathway(
            pair_slug=pair_slug,
            source_domain=d1,
            destination_domain=d2,
            module_path=info['module'],
            description=f"{d1} ↔ {d2} via {pair_slug}",
        )

    def load_transformer(self, pair_slug: str) -> Optional[Any]:
        """Lazily load and cache a transformer by pair slug."""
        if pair_slug in self._loaded_transformers:
            return self._loaded_transformers[pair_slug]

        info = TRANSFORMER_REGISTRY.get(pair_slug)
        if not info:
            return None

        try:
            mod = importlib.import_module(info['module'])
            getter = getattr(mod, info['getter'])
            transformer = getter()
            self._loaded_transformers[pair_slug] = transformer
            return transformer
        except (ImportError, AttributeError):
            return None

    def execute_transform(
        self,
        pair_slug: str,
        origin_concept: str,
        origin_domain: str,
        destination_domain: str,
        structural_property: str = "",
        resonance_sentence: str = "",
        tokens: Optional[List[str]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Load a transformer and execute a transformation."""
        transformer = self.load_transformer(pair_slug)
        if transformer is None:
            return None

        result = transformer.transform(
            origin_concept=origin_concept,
            origin_domain=origin_domain,
            destination_domain=destination_domain,
            structural_property=structural_property,
            resonance_sentence=resonance_sentence,
            tokens=tokens or [],
        )
        return result.to_dict()

    def get_pathway_catalog(self) -> Dict[str, Any]:
        """Return a full catalog of all pathways and their metadata."""
        return {
            slug: {
                'domains': info['domains'],
                'module': info['module'],
            }
            for slug, info in TRANSFORMER_REGISTRY.items()
        }

    def get_domain_adjacency(self) -> Dict[str, List[str]]:
        """Return the domain adjacency graph."""
        return dict(self._adjacency)


# ─── Convenience singleton ─────────────────────────────────────

_default_selector: Optional[PathwaySelector] = None


def get_selector() -> PathwaySelector:
    """Get or create the default PathwaySelector instance."""
    global _default_selector
    if _default_selector is None:
        _default_selector = PathwaySelector()
    return _default_selector
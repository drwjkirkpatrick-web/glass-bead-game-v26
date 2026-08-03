"""
Tests for the Pathway Selector module.
"""
import pytest
from src.pathway_selector import PathwaySelector, get_selector, TRANSFORMER_REGISTRY


@pytest.fixture
def selector():
    return PathwaySelector()


class TestRegistry:
    def test_registry_has_19_pairs(self):
        assert len(TRANSFORMER_REGISTRY) == 19

    def test_coda_pairs_present(self):
        coda_pairs = [s for s in TRANSFORMER_REGISTRY if s.startswith('code-')]
        assert len(coda_pairs) == 8
        expected = {
            'code-math', 'code-music', 'code-language', 'code-philosophy',
            'code-technology', 'code-nature', 'code-history', 'code-medicine',
        }
        assert set(coda_pairs) == expected

    def test_original_pairs_present(self):
        original = {
            'math-music', 'math-philosophy', 'music-language',
            'history-philosophy', 'nature-math', 'philosophy-language',
            'nature-music', 'technology-math', 'medicine-nature',
            'history-music', 'philosophy-music',
        }
        for slug in original:
            assert slug in TRANSFORMER_REGISTRY


class TestFindPairSlug:
    def test_direct_pair_found(self, selector):
        assert selector.find_pair_slug('coda', 'mathematica') == 'code-math'

    def test_reverse_pair_found(self, selector):
        assert selector.find_pair_slug('mathematica', 'coda') == 'code-math'

    def test_nonexistent_pair(self, selector):
        assert selector.find_pair_slug('coda', 'coda') is None


class TestListDirectPathways:
    def test_coda_has_8_direct_pathways(self, selector):
        pathways = selector.list_direct_pathways('coda')
        assert len(pathways) == 8

    def test_musica_pathways(self, selector):
        pathways = selector.list_direct_pathways('musica')
        # musica ↔ mathematica, musica ↔ lingua, musica ↔ natura,
        # musica ↔ historia, musica ↔ philosophia, musica ↔ coda = 6
        assert len(pathways) == 6

    def test_pathway_has_correct_fields(self, selector):
        pathways = selector.list_direct_pathways('coda')
        for p in pathways:
            assert p.pair_slug
            assert p.source_domain
            assert p.destination_domain
            assert p.module_path
            assert p.to_dict()['pair_slug'] == p.pair_slug


class TestMultiHopPaths:
    def test_two_hop_path(self, selector):
        # coda → mathematica → musica (if code-math and math-music exist)
        paths = selector.find_multi_hop_paths('coda', 'musica', max_hops=3)
        assert len(paths) > 0
        # At least one path should go through mathematica
        math_paths = [p for p in paths if 'mathematica' in p.hops]
        assert len(math_paths) > 0

    def test_same_domain_no_path(self, selector):
        paths = selector.find_multi_hop_paths('coda', 'coda')
        assert len(paths) == 0

    def test_path_has_correct_hops(self, selector):
        paths = selector.find_multi_hop_paths('coda', 'medicina', max_hops=3)
        for p in paths:
            assert p.hops[0] == 'coda'
            assert p.hops[-1] == 'medicina'
            assert p.total_hops == len(p.pair_slugs)


class TestSelectPathway:
    def test_select_existing(self, selector):
        p = selector.select_pathway('code-math')
        assert p is not None
        assert p.pair_slug == 'code-math'
        assert 'coda' in (p.source_domain, p.destination_domain)
        assert 'mathematica' in (p.source_domain, p.destination_domain)

    def test_select_nonexistent(self, selector):
        assert selector.select_pathway('nonexistent-pair') is None


class TestLoadTransformer:
    def test_load_code_math(self, selector):
        t = selector.load_transformer('code-math')
        assert t is not None
        assert hasattr(t, 'transform')
        assert hasattr(t, 'get_isomorphism_catalog')

    def test_load_nonexistent(self, selector):
        assert selector.load_transformer('fake-pair') is None

    def test_cached_load(self, selector):
        t1 = selector.load_transformer('code-math')
        t2 = selector.load_transformer('code-math')
        assert t1 is t2  # same cached instance


class TestExecuteTransform:
    def test_execute_code_to_math(self, selector):
        result = selector.execute_transform(
            pair_slug='code-math',
            origin_concept='recursion',
            origin_domain='coda',
            destination_domain='mathematica',
            structural_property='self-reference',
        )
        assert result is not None
        assert result['origin_concept'] == 'recursion'
        assert result['direction']
        assert len(result['steps']) == 6


class TestCatalog:
    def test_full_catalog(self, selector):
        catalog = selector.get_pathway_catalog()
        assert len(catalog) == 19
        for slug, info in catalog.items():
            assert 'domains' in info
            assert 'module' in info

    def test_adjacency(self, selector):
        adj = selector.get_domain_adjacency()
        assert 'coda' in adj
        # coda should be adjacent to all 8 other domains
        assert len(adj['coda']) == 8


class TestSingleton:
    def test_get_selector_returns_same_instance(self):
        s1 = get_selector()
        s2 = get_selector()
        assert s1 is s2
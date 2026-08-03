"""Tests for src/pulse.py MoveFeed."""

import pytest
from src.pulse import MoveFeed


@pytest.fixture
def feed():
    return MoveFeed(max_size=5)


def test_add_move_increases_window(feed):
    feed.add_move({"domain": "math"})
    assert len(feed._window) == 1


def test_window_respects_max_size(feed):
    for i in range(7):
        feed.add_move({"domain": "math", "id": i})
    assert len(feed._window) == 5


def test_get_trending_domains_empty():
    f = MoveFeed()
    assert f.get_trending_domains() == {}


def test_get_trending_domains_counts(feed):
    feed.add_move({"domain": "math"})
    feed.add_move({"domain": "music"})
    feed.add_move({"domain": "math"})
    trending = feed.get_trending_domains()
    assert trending == {"math": 2, "music": 1}


def test_get_trending_domains_sorted(feed):
    feed.add_move({"domain": "art"})
    feed.add_move({"domain": "art"})
    feed.add_move({"domain": "art"})
    feed.add_move({"domain": "math"})
    feed.add_move({"domain": "music"})
    trending = feed.get_trending_domains()
    assert list(trending.keys()) == ["art", "math", "music"]


def test_domain_temperature_zero_when_empty():
    f = MoveFeed()
    assert f.get_domain_temperature("math") == 0.0


def test_domain_temperature_normalized(feed):
    feed.add_move({"domain": "math"})
    feed.add_move({"domain": "math"})
    feed.add_move({"domain": "music"})
    assert feed.get_domain_temperature("math") == 1.0
    assert feed.get_domain_temperature("music") == 0.5
    assert feed.get_domain_temperature("art") == 0.0


def test_add_move_over_max_evicts_oldest(feed):
    feed.add_move({"domain": "a", "id": 1})
    feed.add_move({"domain": "b", "id": 2})
    feed.add_move({"domain": "c", "id": 3})
    feed.add_move({"domain": "d", "id": 4})
    feed.add_move({"domain": "e", "id": 5})
    feed.add_move({"domain": "f", "id": 6})
    # oldest 'a' should be evicted
    assert list(feed._window)[0]["domain"] == "b"

from dataclasses import replace
from pathlib import Path
import pytest
from src.recommender import load_songs
from src.system import Request, run_system, verify

CATALOG = load_songs(Path(__file__).resolve().parents[1] / "data/songs.csv")
BASE = Request("lofi", "chill", 0.35)


def test_bpm_exclusions_and_diversity_apply_before_output():
    request = Request("pop", "happy", 0.8, min_bpm=100, max_bpm=140, exclude_ids=(1,))
    result = run_system(request, CATALOG)
    assert result["status"] == "ok"
    assert all(100 <= row["song"]["tempo_bpm"] <= 140 and row["song"]["id"] != 1 for row in result["items"])
    artists = [row["song"]["artist"] for row in result["items"]]
    assert len(artists) == len(set(artists))


def test_strict_unknown_genre_abstains():
    result = run_system(replace(BASE, genre="opera", strict_genre=True), CATALOG)
    assert result["status"] == "no_matches"
    assert result["items"] == []
    assert result["warnings"]


def test_sparse_catalog_is_not_padded():
    result = run_system(replace(BASE, genre="house", strict_genre=True), CATALOG)
    assert len(result["items"]) == 1
    assert "not relaxed" in result["warnings"][-1]


@pytest.mark.parametrize("changes", [dict(energy=float("nan")), dict(energy=2), dict(energy=True),
    dict(count=0), dict(count=True), dict(max_per_artist=0), dict(min_bpm=150,max_bpm=100),
    dict(genre=""), dict(mood=" "), dict(exclude_ids=(True,)), dict(strict_genre="yes")])
def test_request_rejected(changes):
    with pytest.raises(ValueError):
        run_system(replace(BASE, **changes), CATALOG)


def test_verifier_detects_tampered_scores_and_catalog_records():
    items = run_system(BASE, CATALOG)["items"]
    items[0]["score"] = 999
    assert "Score or explanation mismatch" in verify(items, CATALOG, BASE)
    items[0]["song"] = dict(items[0]["song"], title="Invented")
    assert "Song is not an unchanged catalog record" in verify(items, CATALOG, BASE)


def test_fault_injection_fails_closed():
    result = run_system(BASE, CATALOG, verifier=lambda *_: ["Injected fault"])
    assert result["status"] == "blocked"
    assert not result["items"]


def test_empty_catalog_and_repeatability():
    assert run_system(BASE, [])["status"] == "no_matches"
    assert run_system(BASE, CATALOG) == run_system(BASE, CATALOG)


def test_fallback_warns_and_input_not_mutated():
    before = [dict(song) for song in CATALOG]
    result = run_system(replace(BASE, genre="opera"), CATALOG)
    assert result["warnings"] and result["items"]
    assert CATALOG == before

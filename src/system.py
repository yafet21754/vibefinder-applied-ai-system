"""Constraint-aware recommendation with an integrated fail-closed verifier.

Fixed-rule AI simulation: no language model, learned weights, or RAG claims.
"""
from collections import Counter
from dataclasses import asdict, dataclass
import math

from .recommender import recommend_songs, score_song


@dataclass(frozen=True)
class Request:
    genre: str
    mood: str
    energy: float
    count: int = 5
    min_bpm: float = 1
    max_bpm: float = 300
    max_per_artist: int = 1
    exclude_ids: tuple = ()
    strict_genre: bool = False

    def validate(self):
        for name in ("genre", "mood"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip() or len(value) > 80:
                raise ValueError(f"{name} must contain 1–80 characters")
        for name in ("energy", "min_bpm", "max_bpm"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"{name} must be a finite number")
        if not 0 <= self.energy <= 1:
            raise ValueError("energy must be between 0 and 1")
        if not 0 < self.min_bpm <= self.max_bpm <= 300:
            raise ValueError("BPM range must satisfy 0 < min <= max <= 300")
        for name in ("count", "max_per_artist"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 20:
                raise ValueError(f"{name} must be an integer from 1 to 20")
        if not isinstance(self.strict_genre, bool):
            raise ValueError("strict_genre must be boolean")
        if not isinstance(self.exclude_ids, (list, tuple)) or any(type(i) is not int or i <= 0 for i in self.exclude_ids):
            raise ValueError("exclude_ids must contain positive integer song IDs")


def eligible(song, request):
    return (song["id"] not in request.exclude_ids
            and request.min_bpm <= song["tempo_bpm"] <= request.max_bpm
            and (not request.strict_genre or song["genre"].casefold() == request.genre.strip().casefold()))


def verify(items, catalog, request):
    """Independently recheck output membership, constraints and explanation integrity."""
    source = {song["id"]: song for song in catalog}
    seen, artists, errors = set(), Counter(), []
    if len(items) > request.count:
        errors.append("Too many results")
    for item in items:
        song = item["song"]
        if source.get(song["id"]) != song:
            errors.append("Song is not an unchanged catalog record")
        if song["id"] in seen:
            errors.append("Duplicate song")
        seen.add(song["id"])
        if not eligible(song, request):
            errors.append("Constraint violation")
        artists[song["artist"].strip().casefold()] += 1
        score, reasons = score_song(asdict(request), song)
        if not math.isclose(item["score"], score, abs_tol=1e-9) or item["reason"] != "; ".join(reasons):
            errors.append("Score or explanation mismatch")
    if any(count > request.max_per_artist for count in artists.values()):
        errors.append("Artist repetition limit exceeded")
    if any(a["score"] < b["score"] for a, b in zip(items, items[1:])):
        errors.append("Scores are not descending")
    return errors


def run_system(request, catalog, verifier=verify):
    """Plan, filter, rank, enforce diversity, verify, and return a bounded result."""
    request.validate()
    trace = [{"step": "validate", "status": "pass"}]
    candidates = [song for song in catalog if eligible(song, request)]
    trace.append({"step": "filter", "candidates": len(candidates), "catalog_size": len(catalog)})
    ranked = recommend_songs(asdict(request), candidates, k=len(candidates))
    chosen, artists = [], Counter()
    for song, score, reason in ranked:
        artist = song["artist"].strip().casefold()
        if artists[artist] < request.max_per_artist:
            chosen.append({"song": dict(song), "score": score, "reason": reason})
            artists[artist] += 1
        if len(chosen) == request.count:
            break
    trace.append({"step": "rank_and_diversify", "selected": len(chosen)})
    errors = verifier(chosen, catalog, request)
    trace.append({"step": "verify", "status": "fail" if errors else "pass", "errors": errors})
    warnings = []
    if not any(song["genre"].casefold() == request.genre.strip().casefold() for song in candidates):
        warnings.append("No requested-genre matches within constraints; review alternatives or change the request.")
    if len(chosen) < request.count:
        warnings.append("Too few eligible tracks; constraints were not relaxed.")
    if errors:
        return {"status": "blocked", "items": [], "warnings": ["Verification failed; results withheld."], "trace": trace}
    return {"status": "ok" if chosen else "no_matches", "items": chosen, "warnings": warnings, "trace": trace}

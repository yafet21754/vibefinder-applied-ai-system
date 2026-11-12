"""Repeatable behavioral checks; exit nonzero if any expectation fails."""
import json
from dataclasses import replace
from pathlib import Path
from .recommender import load_songs
from .system import Request, run_system


def main():
    catalog = load_songs(Path(__file__).resolve().parents[1] / "data/songs.csv")
    base = Request("lofi", "chill", 0.35)
    cases = [
        ("exact preference winner", base, lambda r: r["items"][0]["song"]["title"] == "Library Rain"),
        ("BPM hard limit", replace(base, min_bpm=100,max_bpm=140), lambda r: bool(r["items"]) and all(100 <= x["song"]["tempo_bpm"] <= 140 for x in r["items"])),
        ("excluded winner", replace(base, exclude_ids=(4,)), lambda r: bool(r["items"]) and all(x["song"]["id"] != 4 for x in r["items"])),
        ("strict unseen genre", replace(base, genre="opera",strict_genre=True), lambda r: r["status"] == "no_matches" and not r["items"]),
        ("fallback transparency", replace(base, genre="opera"), lambda r: bool(r["warnings"]) and bool(r["items"])),
        ("artist diversity", base, lambda r: len({x["song"]["artist"] for x in r["items"]}) == len(r["items"])),
        ("sparse genre", replace(base, genre="house",strict_genre=True), lambda r: len(r["items"]) == 1 and bool(r["warnings"])),
    ]
    results = []
    for name, request, check in cases:
        result = run_system(request, catalog)
        results.append({"case": name, "pass": check(result), "status": result["status"]})
    for value in (-1, float("nan"), float("inf")):
        try:
            run_system(replace(base, energy=value), catalog)
            passed = False
        except ValueError:
            passed = True
        results.append({"case": "invalid energy " + str(value), "pass": passed})
    blocked = run_system(base, catalog, verifier=lambda *_: ["Injected verifier fault"])
    results.append({"case": "verification failure withholds output", "pass": blocked["status"] == "blocked" and not blocked["items"]})
    repeat = run_system(base, catalog) == run_system(base, catalog)
    results.append({"case": "repeatability", "pass": repeat})
    passed = sum(row["pass"] for row in results)
    print(json.dumps({"passed": passed, "total": len(results), "cases": results}, indent=2))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

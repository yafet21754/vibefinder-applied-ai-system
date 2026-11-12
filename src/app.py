"""VibeFinder 2.0 command-line application."""
import argparse
import json
from pathlib import Path

from .recommender import load_songs
from .system import Request, run_system

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--genre", required=True)
    parser.add_argument("--mood", required=True)
    parser.add_argument("--energy", type=float, required=True)
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--min-bpm", type=float, default=1)
    parser.add_argument("--max-bpm", type=float, default=300)
    parser.add_argument("--max-per-artist", type=int, default=1)
    parser.add_argument("--exclude", type=int, nargs="*", default=[])
    parser.add_argument("--strict-genre", action="store_true")
    parser.add_argument("--catalog", type=Path, default=ROOT / "data/songs.csv")
    parser.add_argument("--log", type=Path, help="Optional local JSONL operational log; preferences are omitted")
    args = parser.parse_args()
    try:
        request = Request(args.genre, args.mood, args.energy, args.count,
                          args.min_bpm, args.max_bpm, args.max_per_artist,
                          tuple(args.exclude), args.strict_genre)
        result = run_system(request, load_songs(args.catalog))
        if args.log:
            with args.log.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps({"status": result["status"], "returned": len(result["items"]),
                                         "trace": result["trace"]}) + "\n")
    except (ValueError, OSError) as error:
        print(json.dumps({"status": "error", "message": str(error)}))
        return 2
    print(json.dumps(result, indent=2))
    return 1 if result["status"] == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())

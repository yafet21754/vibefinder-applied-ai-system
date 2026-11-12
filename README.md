# VibeFinder 2.0 — Verified Playlist Builder

Final project repository: https://github.com/yafet21754/vibefinder-applied-ai-system

A Python music recommendation system that turns a listener's preferences into an explainable playlist while enforcing tempo, exclusion, and artist-repetition constraints. It verifies results before releasing them and abstains when constraints leave no matches.

## Website interface

[Open the hosted VibeFinder interface](https://vibefinder-yafet.yafet-009.chatgpt.site) — owner-private; course reviewers can run the local Python interface below.

The website has genre and mood controls, an energy slider, tempo limits, artist limits, presets, exclusion controls, score explanations, verification traces, and a text playlist download. It uses the same synthetic catalog; no audio playback is provided.

Run the interface connected to the original Python engine:

```bash
python3 -m src.web
```

Open **http://127.0.0.1:8000** in your browser. The local server binds only to your device. No additional dependencies are needed. This is a development server, not a production hosting service.

The hosted interface runs a JavaScript port in the browser, with no external AI service or Python process. The original Python engine remains authoritative for the course project and local interface. An automated matrix compares full browser and Python outputs across 192 requests, including strict genres, exclusions, sparse results, boundary energy values and tempo windows. Both implementations use the same catalog.

```bash
python -m pytest -q
python scripts/check_web_parity.py
```

Website validation: **39 Python tests passed; 192/192 browser/Python comparison cases passed.** The comparison script requires Node.js; running the Python app does not.

## Original project and extension

Base project: [VibeFinder 1.0 — Module 3 Music Recommender Simulation](https://github.com/yafet21754/ai110-module3show-musicrecommendersimulation-starter), commit `2ee57506bd5f88c2f6e25580284232ae88596404`.
The original CLI ranked 20 synthetic songs using genre, mood, and energy, explained scores, and compared weighting recipes. It did not enforce playlist constraints or gate outputs through a verifier.
Original documentation is preserved in `docs/module3_README.md`, `docs/module3_model_card.md`, and `docs/module3_ai_interactions.md`; original implementation and tests remain available.

The integrated advanced feature is a **reliability/testing system**: every application run checks catalog membership, score/explanation consistency, BPM bounds, exclusions, duplicate songs, artist limits, and score order. Failed verification withholds the playlist. An independent behavioral evaluation script exercises the same application logic.

This is a fixed-rule, content-based AI simulation. It has no trained model, LLM, external API, RAG, or autonomous tool-calling agent. We do not claim those capabilities or stretch points for them.

## Architecture

Editable source: [diagrams/architecture.mmd](diagrams/architecture.mmd).

1. Validate preferences and numerical bounds.
2. Load validated song metadata and filter hard constraints.
3. Rank with the original scoring function; greedily enforce artist limits.
4. Recheck output integrity and constraints; block failures.
5. Return explanations, warnings, and a concise operational trace for human review.

The trace records operations and counts, not hidden model reasoning. Human-in-the-loop review means the listener checks the result and changes preferences; it does not imply that a human has evaluated these fictional tracks.

## Setup

Python 3.10+; verified with Python 3.12. The application and evaluation harness need only the standard library. pytest is the development dependency.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.app --genre lofi --mood chill --energy 0.35
python -m src.evaluate
python -m pytest -q
```

Windows activation: `.\.venv\Scripts\Activate.ps1`.
Run from the project root. The catalog path is resolved relative to the package, rather than the current working directory.

Optional controls: `--count 3`, `--min-bpm 100 --max-bpm 140`, `--exclude 1 5`, `--max-per-artist 2`, `--strict-genre`, `--catalog data/songs.csv`, `--log run.jsonl`. Local logs omit user preference text; do not commit private logs. Failure to write a requested log is an explicit error.

Exit codes: 0 = successful run, including honest no-match results; 1 = verification blocked output; 2 = invalid input or file error.

## Reproducible execution evidence

These are actual executions captured during development, not invented examples. Complete logs are committed in `evidence/`.

### Example 1

```bash
python -m src.app --genre lofi --mood chill --energy 0.35 --count 2
```

```json
{
  "status": "ok",
  "items": [
    {
      "song": {
        "id": 4,
        "tempo_bpm": 72.0,
        "artist": "Paper Lanterns",
        "genre": "lofi",
        "mood": "chill",
        "title": "Library Rain",
        "danceability": 0.58,
        "energy": 0.35,
        "valence": 0.6,
        "acousticness": 0.86
      },
      "score": 4.0,
      "reason": "genre match (+2.00); mood match (+1.00); energy similarity 1.00 (+1.00)"
    },
    {
      "song": {
        "id": 2,
        "tempo_bpm": 78.0,
        "artist": "LoRoom",
        "genre": "lofi",
        "mood": "chill",
        "title": "Midnight Coding",
        "danceability": 0.62,
        "energy": 0.42,
        "valence": 0.56,
        "acousticness": 0.71
      },
      "score": 3.9299999999999997,
      "reason": "genre match (+2.00); mood match (+1.00); energy similarity 0.93 (+0.93)"
    }
  ],
  "warnings": [],
  "trace": [
    {
      "step": "validate",
      "status": "pass"
    },
    {
      "step": "filter",
      "candidates": 20,
      "catalog_size": 20
    },
    {
      "step": "rank_and_diversify",
      "selected": 2
    },
    {
      "step": "verify",
      "status": "pass",
      "errors": []
    }
  ]
}
```

Exit code: 0.

### Example 2

```bash
python -m src.app --genre house --mood euphoric --energy 0.88 --min-bpm 120 --max-bpm 135 --strict-genre --count 2
```

```json
{
  "status": "ok",
  "items": [
    {
      "song": {
        "danceability": 0.96,
        "mood": "euphoric",
        "id": 19,
        "energy": 0.88,
        "acousticness": 0.04,
        "valence": 0.86,
        "genre": "house",
        "artist": "Coastline Circuit",
        "tempo_bpm": 128.0,
        "title": "Afterglow Floor"
      },
      "score": 4.0,
      "reason": "genre match (+2.00); mood match (+1.00); energy similarity 1.00 (+1.00)"
    }
  ],
  "warnings": [
    "Too few eligible tracks; constraints were not relaxed."
  ],
  "trace": [
    {
      "step": "validate",
      "status": "pass"
    },
    {
      "step": "filter",
      "candidates": 1,
      "catalog_size": 20
    },
    {
      "step": "rank_and_diversify",
      "selected": 1
    },
    {
      "step": "verify",
      "status": "pass",
      "errors": []
    }
  ]
}
```

Exit code: 0.

### Example 3

```bash
python -m src.app --genre opera --mood calm --energy 0.2 --strict-genre
```

```json
{
  "status": "no_matches",
  "items": [],
  "warnings": [
    "No requested-genre matches within constraints; review alternatives or change the request.",
    "Too few eligible tracks; constraints were not relaxed."
  ],
  "trace": [
    {
      "step": "validate",
      "status": "pass"
    },
    {
      "step": "filter",
      "candidates": 0,
      "catalog_size": 20
    },
    {
      "step": "rank_and_diversify",
      "selected": 0
    },
    {
      "step": "verify",
      "status": "pass",
      "errors": []
    }
  ]
}
```

Exit code: 0.

### Example 4

```bash
python -m src.app --genre pop --mood happy --energy nan
```

```json
{"status": "error", "message": "energy must be a finite number"}
```

Exit code: 2.

## Reliability results

```bash
python -m src.evaluate
```

```json
{
  "passed": 12,
  "total": 12,
  "cases": [
    {
      "case": "exact preference winner",
      "pass": true,
      "status": "ok"
    },
    {
      "case": "BPM hard limit",
      "pass": true,
      "status": "ok"
    },
    {
      "case": "excluded winner",
      "pass": true,
      "status": "ok"
    },
    {
      "case": "strict unseen genre",
      "pass": true,
      "status": "no_matches"
    },
    {
      "case": "fallback transparency",
      "pass": true,
      "status": "ok"
    },
    {
      "case": "artist diversity",
      "pass": true,
      "status": "ok"
    },
    {
      "case": "sparse genre",
      "pass": true,
      "status": "ok"
    },
    {
      "case": "invalid energy -1",
      "pass": true
    },
    {
      "case": "invalid energy nan",
      "pass": true
    },
    {
      "case": "invalid energy inf",
      "pass": true
    },
    {
      "case": "verification failure withholds output",
      "pass": true
    },
    {
      "case": "repeatability",
      "pass": true
    }
  ]
}
```

```bash
python -m pytest -q -p no:anyio
```

```text
................................                                         [100%]
32 passed in 0.23s
```

The final flag disables an unrelated globally installed pytest plugin for this captured run; it is not needed in a clean virtual environment. The normal pytest run also passed.

Tests include tampered score/catalog output and an injected verifier failure, in addition to the original scoring tests. These checks measure software invariants and deterministic behavior, not whether a listener likes a track. No listener study or production accuracy claim is made.

## Design decisions and trade-offs

- Reuse the Module 3 scorer, keeping its mathematical explanations and baseline comparison intact.
- Enforce BPM and exclusions before ranking, so a high relevance score cannot override them.
- Cap artist repetition after ranking. This greedy method is simple and transparent; it does not optimize playlist transitions or sequencing.
- Use strict-genre abstention when requested. Otherwise alternatives are allowed with an explicit missing-genre warning.
- Keep the verifier separate from selection. It shares the score formula, so correlated scorer bugs remain possible; independent expected-value unit tests partly address this.
- Use a deterministic rule system for reproducibility. More elaborate generation would add credentials, cost, and another failure surface without solving the constraint problem.

## Testing summary and limitations

All 32 unit tests and 12 harness cases passed in the development environment. Sparse strict genres yield short playlists rather than fabricated tracks; unseen strict genres produce no matches. An injected verification error withholds all tracks.
The catalog still contains only 20 fictional teaching records with hand-assigned features. There is no music playback, real catalog search, transition-quality evaluation, learned personalization, or listener ground truth. Similarity scores are not calibrated confidence probabilities. Genre weighting and catalog imbalance still bias exposure.

## Reflection

Reliable recommendations require explicit definitions of success: a high matching score alone cannot establish a useful playlist. This extension makes hard requirements visible and checks them before output. The responsible-AI reflection and the AI-collaboration record are in `model_card.md` and `ai_interactions.md`; the student must review the personal sections before submitting.

## Submission status

Implementation, source diagram, tests, execution evidence, and documentation are included in this public final-project repository. Original Module 3 history is preserved, followed by separate implementation and documentation commits. See `docs/publish_and_submit.md` for the remaining student review and submission steps. The 5–7 minute presentation outline is in `docs/presentation_outline.md`; a finished deck and a recorded walkthrough are not included. The personal-reflection prompts in `model_card.md` still require student responses before submission.

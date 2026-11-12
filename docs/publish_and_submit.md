# Final submission checklist

Public final repository: https://github.com/yafet21754/vibefinder-applied-ai-system

The repository preserves original Module 3 history and adds the final-system code, evaluation harness, architecture source, and actual execution evidence in meaningful commits. The original module repository is unchanged.

## Run your own copy

```bash
git clone https://github.com/yafet21754/vibefinder-applied-ai-system.git
cd vibefinder-applied-ai-system
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.app --genre lofi --mood chill --energy 0.35
python -m src.evaluate
python -m pytest -q
```

## Finish before submitting
- Inspect the demo and explanations so you can explain how the system works.
- Complete the personal reflection in model_card.md using your real experience, including an AI suggestion you accepted and one you revised or rejected.
- Use docs/presentation_outline.md to prepare your 5–7 minute presentation.
- Commit and push your reflection and any final changes.
- Add the repository link and an accurate short reflection to your portfolio.
- Submit the final repository URL. A Loom recording is optional.

## Portfolio reflection prompts
Describe how you evolved a scored prototype into a constraint-aware system, how its behavior was verified, and what you learned about synthetic data and recommendation bias. Do not claim production deployment or real listener validation.

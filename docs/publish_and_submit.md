# Publish and submission checklist

The code is prepared, but a new public final-project repository has not been created or pushed.

## Publish with preserved history
Create an empty public repository named `vibefinder-applied-ai-system` under your GitHub account. Do not initialize a README, license, or gitignore.

The ZIP includes a portable `history.bundle`. In a terminal, from the extracted folder's parent directory:

```bash
git clone VibeFinder_Applied_AI_System/history.bundle vibefinder-applied-ai-system
cd vibefinder-applied-ai-system
git remote set-url origin https://github.com/yafet21754/vibefinder-applied-ai-system.git
git push -u origin main
```

The bundle includes original history and meaningful extension commits. A ZIP upload alone does not preserve that history. The original module repository is unchanged.

## Finish before submitting
- Run the setup, demo, evaluation harness and test suite yourself.
- Review the model card and complete the clearly labeled personal reflection using your real experience.
- Adapt docs/presentation_outline.md into your 5–7 minute presentation.
- Confirm the new repository is public and files and commits appear on GitHub.
- Commit and push your reflection and any final changes.
- Add the public repository link and an accurate short reflection to your portfolio.
- Submit the final repository URL. A Loom recording is optional.

## Portfolio reflection prompts
Write your own short paragraph describing how you evolved a scored prototype into a constraint-aware system, how you verified its behavior, and what you learned about synthetic data and recommendation bias. Do not claim production deployment or real listener validation.

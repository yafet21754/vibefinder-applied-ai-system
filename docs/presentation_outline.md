# VibeFinder 2.0 — 5–7 minute presentation outline

## 1. Problem and original project — 45 seconds
“My original Module 3 project ranked synthetic songs by genre, mood, and energy. For the final extension, I wanted the recommendations to follow explicit playlist requirements and to be checked before being shown.”

## 2. Architecture — 60 seconds
Show diagrams/architecture.mmd. Explain validation, catalog filtering, scoring, artist caps, and verification. Describe the listener reviewing and adjusting preferences as human-in-the-loop control. Call the sequence orchestration, without claiming an autonomous agent or RAG.

## 3. Live demo — 2 minutes
Launch `python -m src.web` for an interactive demo, or run the CLI commands in README.md: lofi success, strict house with a short result, and strict opera with no matches. Point to explanations, filter counts, and the verification status. Explain that the catalog uses fictional tracks and does not play audio.

## 4. Reliability — 60 seconds
Run `python -m src.evaluate`. Explain the actual 12/12 result, then show a fault-injection test in tests/test_system.py. The guardrail withholds outputs if verification fails. Explain why a passing test suite cannot establish subjective listening quality.

## 5. Responsible design — 45 seconds
Discuss small-catalog bias, genre weighting, and synthetic attributes. Explain that relevance scores are not confidence probabilities. Show where the model card documents limitations and your personal reflection.

## 6. Learning and next steps — 45 seconds
Describe one implementation decision you understand and one you would change. Possible next work: licensed real music metadata and a listener evaluation, with permission. Use your own account of the AI collaboration after reviewing the project.

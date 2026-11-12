# Model Card — VibeFinder 2.0

## Intended use and system type
Educational, explainable playlist suggestions from a synthetic catalog. This is an extension of the user's Module 3 VibeFinder simulation, not a trained model or LLM. Its integrated AI feature is a reliability system around a fixed-rule recommender.

## Data and scoring
Twenty fictional song records are inherited unchanged from the base repository. Titles and artists are teaching examples, not verified real releases; numeric features are hand assigned. Genre match adds 2, mood match adds 1, and energy similarity adds `1 - abs(song_energy - target_energy)`. No personal listening history is collected. Scores are relevance measures, not probabilities.

## Limitations and biases
The catalog is small and uneven; genre receives more weight than mood. Exact labels ignore related genres and cultural differences. Metadata may not capture how a song actually sounds. Greedy artist caps cannot optimize a complete DJ set or guarantee smooth transitions. Stable ties favor earlier CSV rows. The verifier shares scoring code, so it cannot independently establish scorer correctness. No human listener accuracy or satisfaction measurement has been performed.

## Misuse and prevention
A user could present fictional recommendations or numerical scores as real music expertise. Documentation labels the catalog synthetic and scores uncalibrated. Catalog membership checks prevent newly invented titles in released output, but cannot establish that input data is true. No arbitrary code execution, external tools, accounts, purchases, or music-platform access are supported. Input validation and fail-closed verification protect the supported CLI workflow; they are not a general security guarantee. Logs are optional, local, and omit raw preferences. Users should review custom catalogs before sharing.

## Reliability testing and surprises
Agent-run validation: 32 unit tests and 12 behavioral harness cases passed; exact outputs are in README.md and evidence/. Tampering checks detect altered scores and catalog records. An injected verifier fault blocks output. Unknown strict genres return no matches, and sparse strict genres return shorter lists without relaxing constraints.
A notable observed outcome is that a strict house request can return only one track from this catalog. That is correct behavior under the available data, even when the user requests five. More results would require different constraints or more verified source data. These checks establish invariants, not listener satisfaction.

## Collaboration with AI — factual implementation record
ChatGPT inspected the original repository, implemented the extension, ran tests and examples, and wrote documentation. The user requested that work begin. No claim is made that the student personally ran the tests, approved individual design decisions, or gave manual listening ratings.

Accepted implementation approach: preserve the original scoring function and put validation and verification around it. This maintains a clear comparison to Module 3.
Revised implementation approach: the earlier proposed AI Career Coach direction was replaced with the verified Module 3 music recommender after repository inspection established a suitable course-project base. This avoids asserting unverified Module 1–3 provenance for the NotebookLM project.
These are the assistant's implementation choices, not statements of the student's personal acceptance or rejection.

## Student reflection — complete before submission
The graded personal reflection requires the student's own account. Review the working system and replace the prompts below with accurate responses; this section is intentionally not presented as finished.

- How did you collaborate with AI, and what did you personally inspect or change?
- Which AI suggestion did you accept, and why?
- Which suggestion did you reject or revise, and why? It can be a naming, scope, or simplification change you actually make.
- What surprised you when you tested reliability yourself?
- Which limitation or bias matters most to you, and what would you improve next?

## Website interface and browser implementation
The local website server calls the original Python system; the hosted static site uses an explicitly labeled JavaScript port. The port's outputs matched Python across 192 request cases. There are now 39 passing Python tests, including actual HTTP/API integration, invalid JSON structures, unknown fields, and cross-origin rejection. This does not prove behavior for all possible requests or establish listener satisfaction. Hosted preferences are processed on-device. The catalog remains fictional and no audio playback or music-platform connection is implied.

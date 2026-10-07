# Coding Agent Instructions

Before changing the project:

1. Read `docs/00_PROJECT_RULES.md`.
2. Read the relevant specification documents.
3. Inspect the existing repository and dataset before implementing.
4. Never invent requirements, metrics, data, or model outputs.
5. Make the smallest correct change.
6. Run relevant tests after meaningful changes.
7. Do not change architecture or scope without explicit approval.
8. Keep the project locally runnable.
9. Do not introduce unrelated machine-learning algorithms.
10. Do not create academic-module folders, pages, or labels.

Preferred execution order:

Dataset -> preprocessing -> HMM -> Forward/Viterbi/Baum-Welch -> API -> Figma/UI -> integration -> testing -> polish.

When finishing a task, report:
- files changed
- tests run
- tests passed/failed
- known issues
- next step

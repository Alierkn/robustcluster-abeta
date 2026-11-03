# External checker recheck — undergraduate-readability revision

Recorded 3 November 2026. The first two paragraphs of the finalized revised abstract were selected, saved and hashed before submission. Each service received one submission attempt. This is an excerpt-level observation, not an authorship certification.

| Service | Status | Verified result for this excerpt |
|---|---|---|
| [Sapling](https://sapling.ai/ai-content-detector) | COMPLETED | **100.0% AI-detection score**, 177 displayed tokens; model version not exposed |
| [GPTZero](https://gptzero.me/) | BLOCKED | **No verified current score**: free-scan/sign-up gate; stopped without registration |

Sapling did not classify the excerpt as human. GPTZero did not provide a verifiable updated result. Neither observation establishes the authorship, scientific quality or publication readiness of the report as a whole.

## Input and provenance

- [Exact submitted text](../results/editorial_review/revision3/excerpt.txt): UTF-8, 135 whitespace-separated words, 923 characters, no terminal newline.
- Excerpt SHA256: `0753d8c2c7f059d734c62d2b50cadcc4848923fa5e0f1baf367f85ad21326be7`.
- Source file SHA256 at selection: `e865d822bda00a06ed4ebbc11512172fa4e688ad2fbd2f01be22b7e3a7414bc5`.
- [Input metadata saved before submission](../results/editorial_review/revision3/input.json).
- [Machine-readable outcome and evidence hashes](../results/editorial_review/revision3/results.json).

The text contains no personal cover details, correspondence or raw frame data. The selection rule is the same as earlier reviews, but wording and length differ (revision 2: 126 words; revision 3: 135 words). Scores cannot be treated as a controlled before/after experiment. No score-driven edits were made in this checking task.

## Observed procedure

The previous in-app browser session was unavailable. New dedicated Chrome tabs were opened; existing user tabs and earlier evidence were not changed. Sapling received the saved text and one click of its Check again control. The displayed excerpt, 177-token count and 100.0% score were captured together in a screenshot.

GPTZero received the identical saved excerpt and one landing-page Scan click. The result opened in a new tab at `https://app.gptzero.me/`. It displayed a Sign up to Continue modal and a notice requiring a free account to unlock more scans. Its status also explicitly read **Text changed — Scan to update**, with 923 characters and 135 words. Background controls displayed AI 100%, Mixed 0%, Human 0%, model 3.3b and the header model label 2025-03-13-base. Those background values were **not established as a new result for the submitted excerpt** and are retained only as diagnostic evidence. They must not be cited as the current result.

No account was created, no purchase was made, no CAPTCHA was solved or bypassed, and no further submission or session change sought to evade the gate. No source text was edited and no alternate humanization service was used.

## Evidence

- Sapling: [visible result screenshot](../results/editorial_review/revision3/sapling.png), [complete browser accessibility state](../results/editorial_review/revision3/sapling-ui.txt).
- GPTZero: [blocking modal screenshot](../results/editorial_review/revision3/gptzero.png), [complete browser accessibility state](../results/editorial_review/revision3/gptzero-ui.txt).
- Earlier records remain unchanged: [initial review](AI_CHECKER_REVIEW.md) and [revision 2](AI_CHECKER_REVIEW_REVISION2.md).

The appropriate editorial checks remain factual support, accurate citations, readable explanations and a transparent account of contributions. A detector score is not a substitute for those checks.

# External checker review — v0.3.0

Recorded 3 November 2026. A fixed **232-word, 1,738-character excerpt** was submitted once to each of three services. Two returned verifiable results; GPTZero required registration. **This was not a whole-report scan.**

| Service | Status | Observed current-excerpt result | Model / count |
|---|---|---|---|
| [Sapling](https://sapling.ai/ai-content-detector) | COMPLETED | **99.9% AI-detection score** | Model not exposed; 323 tokens |
| [QuillBot](https://quillbot.com/ai-content-detector) | COMPLETED | **0% likely AI**; AI-generated 0%, AI-refined 0%, Human-written 100% | v7.1.0; 232 words |
| [GPTZero](https://gptzero.me/) | BLOCKED | **No verified current score** | Sign-up/free-scan gate |

Sapling and QuillBot returned opposing classifications for the same input. Both results are retained. QuillBot's “Human-written” label is a service output, not proof that the passage or report was written without AI assistance. Sapling's result is likewise not proof of authorship. The percentages should not be averaged: the products describe their scores differently, and this review does not establish a common calibrated scale. None of these results establishes scientific accuracy or readiness for publication.

## Fixed scope and provenance

Before any submission, the protocol selected the longest complete-paragraph prefix of the finalized abstract whose plain text fitted within 2,000 Unicode characters. This selected the first three of four abstract paragraphs. The full plain-text abstract has 2,242 characters; the main report is longer. Sapling's [published free limit](https://sapling.ai/pricing) is 2,000 characters, which set the common limit. No passage was chosen or revised in response to a detector score.

The two LaTeX macros in the selected text were resolved using `report/generated/values.tex`: the Rg–SASA correlation is 0.848 and the first-two-component variance is 88.1%. Other wording and paragraph order were preserved. The text excludes personal cover information, correspondence and raw frame data.

- [Exact submitted excerpt](../results/editorial_review/v030/excerpt.txt), UTF-8 without terminal newline.
- SHA256: `18123d65082f01838dd037ac1a572fc79e86f82d8c103579dfc58ace069967b0`.
- [Input and source hashes](../results/editorial_review/v030/input.json), recorded before submission.
- [Pre-submission protocol](../results/editorial_review/v030/protocol.json) and [official service limits](../results/editorial_review/v030/SERVICE_LIMITS.md).
- [Machine-readable results and evidence hashes](../results/editorial_review/v030/results.json).

Earlier reviews used different text and lengths. Their scores are not a controlled before/after comparison with this excerpt, and changes in report layout do not constitute an authorship experiment. Earlier evidence remains unchanged.

## Verification and access limits

Sapling returned a new visible score after one Check again click. The displayed text and 323-token count were recorded, and no truncation warning appeared.

QuillBot returned its document result view after one Detect AI click. The exact submitted text, 232-word count, v7.1.0 label and 0% score were visible together. The Detect AI again control was disabled until the text changed. An unrelated extension promotion was dismissed to improve the screenshot. The page also exposed a reCAPTCHA connection-warning message; no challenge was solved or bypassed, and the ordinary submission nevertheless produced the recorded visible result. No rewrite, paraphrase, humanizer, writing-assistant or plagiarism function was used.

GPTZero opened a result tab but displayed **Sign up to Continue** and an account requirement to unlock more scans. Its status explicitly read **Text changed — Scan to update**, alongside 1,738 characters and 232 words. Background controls showed AI 100%, Mixed 0%, Human 0%, model 3.3b and header label 2025-03-13-base. Those values were not verified as a new score for this input and are **excluded from the result table**. No account was created and no additional scan or session change attempted to evade the gate.

The detector task did not rewrite the submitted prose. The checked abstract remains unchanged; page-layout and explanatory edits elsewhere in the report were reviewed independently of the scores. There were no purchases, new accounts or repeated attempts to obtain a preferred classification. These were external checks of user-authorized prose; no confidentiality or zero-retention guarantee is asserted.

## Visible evidence

- Sapling: [input screenshot](../results/editorial_review/v030/sapling-input.png), [score screenshot](../results/editorial_review/v030/sapling-score.png), [browser state](../results/editorial_review/v030/sapling-ui.txt).
- QuillBot: [result screenshot](../results/editorial_review/v030/quillbot-clean.png), [initial result screenshot](../results/editorial_review/v030/quillbot.png), [browser state](../results/editorial_review/v030/quillbot-ui.txt).
- GPTZero: [blocking modal screenshot](../results/editorial_review/v030/gptzero-blocked.png), [browser state](../results/editorial_review/v030/gptzero-ui.txt).

The report's evidence, citations, methods and transparent contribution record remain the basis for evaluating it. This checker comparison records tool behavior on a bounded excerpt; it does not replace that assessment.

# External AI-checker review — 3 November 2026

Two external detector services were used on the **same 154-word, 1,261-character excerpt**: the first two paragraphs of the existing abstract. This selection fits Sapling's 2,000-character free limit. It was fixed before submission, not selected after comparing scores. The full report, personal cover information and raw scientific files were not uploaded.

## Observed results

| Service | Observed output | Scope |
|---|---|---|
| Sapling public detector | AI-detection score: **100.0%**; 230 tokens | Saved excerpt only; detector version not exposed in this result |
| GPTZero Basic Scan | Model **4.1o**; **AI 100%, Mixed 0%, Human 0%** | Same saved excerpt; page confirms 154 words and 1,261 characters |

These are the actual displayed classifications, not evidence that the entire report is “100% AI”. Neither score establishes who wrote a document, whether the scientific claims are correct, or whether plagiarism occurred. The project has received AI assistance; the results must not be repackaged as a human-authorship certificate. No “humanizer”, deliberate error insertion or detector-targeted rewriting was used.

The checks concern the pre-revision excerpt. Later edits to the report have **not** been assigned these scores. Scientific editing follows claim accuracy, clarity, citation coverage and the distinction between completed and blocked analyses.

## Evidence

- [Exact submitted excerpt](../results/editorial_review/detector_excerpt_2026-11-03.txt)
- [Input provenance and SHA256](../results/editorial_review/detector_input_2026-11-03.json)
- [Structured results and evidence hashes](../results/editorial_review/detector_results_2026-11-03.json)
- [Sapling screenshot](../results/editorial_review/sapling-result-2026-11-03.png)
- [GPTZero screenshot](../results/editorial_review/gptzero-result-2026-11-03.png)

The corresponding UI text snapshots are stored alongside the screenshots. Sapling generated a share link that states a three-day expiry; the local evidence is the durable record. GPTZero opened its result in a separate tab. The landing-page Scan button was clicked twice before discovering the result tabs; the first result tab was recorded. No account was created, payment made, CAPTCHA bypassed, or favourable output selected.

## Privacy conditions checked

Sapling's general privacy policy states that submitted content is collected, stored and used to improve its service. Its public checker should therefore not be described as zero-retention. The saved excerpt contains academic project prose rather than names, identifiers, private correspondence or raw data. [Sapling privacy policy](https://sapling.ai/privacy)

GPTZero's support documentation distinguishes website/dashboard submissions from API use: website submissions may be retained, and free submissions may be used in anonymised form to improve detection. The API's default no-storage statement must not be applied to this browser check. [Data collection](https://support.gptzero.me/articles/8705593161-what-data-does-gptzero-collect-when-i-use-it), [training use](https://support.gptzero.me/articles/9816574530-does-gptzero-train-on-my-submitted-text)

## Limits of interpretation

Sapling explicitly cautions against treating detector output as a standalone authorship decision and acknowledges both false positives and false negatives. [Detector instructions](https://sapling.ai/ai-content-detector)

Liang and colleagues found misclassification of non-native English writing in the detectors and samples studied in 2023. That evidence does not quantify the error rate of the two current services for this report. The publisher page was inaccessible in this session; the authors' primary preprint and its published-version link were inspected. [Authors' study](https://arxiv.org/abs/2304.02819)

A 2026 EACL study revisiting the issue in Czech found no systematic non-native-speaker bias for the detector families tested. This different result reinforces the need to specify language, dataset, detector and evaluation date rather than assuming one universal accuracy or bias figure. [ACL publication](https://aclanthology.org/2026.eacl-srw.20/)

The appropriate submission evidence remains traceable analysis outputs, source history, citations, a clear account of assistance, and the student's ability to explain the work. Detector scores are recorded separately from scientific results.

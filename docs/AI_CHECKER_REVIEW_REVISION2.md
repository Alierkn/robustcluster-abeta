# External checker recheck — revised abstract

Recorded 3 November 2026. Two real external services each checked the same fixed excerpt once. This records the returned classifications; it is not an authorship certification.

| Service | Actual result | Model / input details |
|---|---|---|
| [Sapling](https://sapling.ai/ai-content-detector) | AI-detection score **99.9%** | 187 displayed tokens; no truncation; model version not exposed |
| [GPTZero](https://gptzero.me/) | **AI 100%, Mixed 0%, Human 0%** | Basic Scan; model **4.1o**; 126 words, 986 characters |

**Neither service returned Human.** These excerpt-level scores do not establish the authorship, scientific correctness or publication readiness of the full report. No whole-report “human” claim is justified.

## Fixed input and comparison limits

The input is the revised abstract’s first two paragraphs, converted to plain text. It was fixed and saved before either submission. The selection rule matches the earlier check, but the wording and length changed: the previous excerpt had 154 words; this one has 126. These are not controlled before/after scores. No further rewrite was made in response to these results and no retries sought a different classification.

- [Exact submitted excerpt](../results/editorial_review/revision2/excerpt.txt), UTF-8, 986 characters, 989 bytes, no terminal newline.
- SHA256: `74da4bc3e228e779adc6b6e8677a4ec94e5900ca7974fd51cbdcc14c6a802579`.
- [Input metadata](../results/editorial_review/revision2/input.json) includes the source-file hash at selection time.
- [Machine-readable results and evidence hashes](../results/editorial_review/revision2/results.json).

The excerpt contains no personal cover information, private correspondence, or raw frame data. The original [checker review](AI_CHECKER_REVIEW.md) and its evidence remain unchanged.

## Observed procedure and evidence

Sapling was called once through its page-advertised WebMCP interface. The response was checked against the visible browser result, including the 99.9% score and 187-token count. GPTZero was submitted once using the landing-page Scan control; its result opened in a new tab. A transient browser-verification container cleared automatically, without challenge interaction. No account, purchase or CAPTCHA bypass was used.

- Sapling [input screenshot](../results/editorial_review/revision2/sapling.png), [score screenshot](../results/editorial_review/revision2/sapling-score.png), [browser state](../results/editorial_review/revision2/sapling-ui.txt), and [raw WebMCP response](../results/editorial_review/revision2/sapling-webmcp-result.json).
- GPTZero [result screenshot](../results/editorial_review/revision2/gptzero.png) and [browser state](../results/editorial_review/revision2/gptzero-ui.txt). Observed result URL: <https://app.gptzero.me/?scanType=basic&source=landing&triggerScan=true>.

Screenshots and local records preserve the observation independently of temporary share links. Editorial assessment should therefore remain grounded in factual support, citations, clarity and transparent contribution records rather than a target detector score.

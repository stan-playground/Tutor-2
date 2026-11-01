# Independent semantic review of document compression

Verdict: **NO_GO**

Scope: compare `before.md` with the current Product Decisions.md for meaning-preserving compression below `## How to read this document`. This review does not reopen earlier process decisions or re-audit historical source documents.

## Reviewed inputs and observations

- Exact pre-edit document: [before.md](before.md), SHA-256 `5cb96d4b3094dd27385045c0ee6ea16e87133b2d942339205f418b5bd6ba935f`.
- Current product document, SHA-256 `427f744d87edf8d94e03481b2c6af29f297ad40aab861bc170fdfe1d6445cb0d`.
- The compression diff and each detailed decision before/after, under the unchanged HighGrade review method and HG-0001-S1/S2 documentation boundary.

The prefix before the reading guide is byte-for-byte identical. Both versions contain all 37 decision IDs and 28 unresolved-topic paragraphs. The portion below the prefix falls from 6,106 to 2,928 whitespace-delimited words, about 52% shorter. The current/historical/proposal distinctions and main trade-offs generally survive, including the offline/online distinction and the fact that earlier generation suggestions remain unadopted.

## Required corrections

These are semantic-equivalence findings under HG-0001-S2, not requests for new functionality.

1. **PD-12, Product Decisions.md:134 — restore the requested-total and near-duplicate constraints.** The original requires section durations to fit the requested total and avoids near-duplicate exercises while retaining relevance. “Produce timed sections” does not preserve the total-duration constraint, and “avoid duplicates” omits near duplicates. Concise equivalent: “Produce sections with exercises, skill targets and durations fitting the requested total; avoid near-duplicate homework while retaining relevance.”

2. **PD-22, Product Decisions.md:214 — restore objective selection as the regeneration starting point.** “Recompute from prioritization” is narrower than “from objective selection onward”: a reader could retain the old objective set and merely reorder it. Use “recompute from objective selection” to preserve the existing decision.

3. **PD-23, Product Decisions.md:226 — retain the consequence of the revision cap.** The original says a new run is required after at most five revisions. The shortened entry retains the number but drops that behavior. Add “then require a new run” to the five-revision limit.

4. **PD-26, Product Decisions.md:248 — preserve the three-second boundary.** “Within three seconds” became “<3 seconds”, changing an inclusive target into a strict one. Restore “within 3 seconds” or “≤3 seconds”. This is a wording correction, not a demand to measure application performance.

5. **PD-33, Product Decisions.md:304 — avoid introducing an absolute transcript-reuse prohibition.** “Transcripts are not shared teaching assets” is stronger than the previous “not automatically a reusable exercise or explanation.” The earlier text leaves access/reuse policy open in PD-28. Use “indexing transcripts does not make them shared teaching assets” or “transcripts are not automatically reusable teaching assets” to preserve that boundary without deciding future authorized reuse.

## Limits and next review

No application tests or source-document re-audit are relevant to this compression. Structural checks run by the executor are separate from this semantic verdict. After these small corrections, review the affected lines and updated hashes; the rest of the reviewed compression need not be rewritten. No product, process or specification files were edited by this reviewer; only this report was created.

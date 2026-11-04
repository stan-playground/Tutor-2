# E0 draft review handoff

This first review batch contains 19 synthetic case revisions: the exact
case IDs, revision numbers and SHA-256 hashes are in each workbook and in the
[checked input list](evidence/e0-input-sha256-v5.txt). It is not a frozen
release suite. A second batch of four additional draft revisions is in separate
`Batch 2` and `B2` tabs of the same workbooks, with its case hashes in the
[second input list](evidence/e0-input-sha256-v6.txt). The original 19 review
rows were not changed. The case files in this working tree are still drafts;
no tutor decisions have been incorporated into those files.

A third batch contains two additional critical privacy drafts in separate
`Batch 3` and `B3` tabs; their case hashes are in the [batch 3 input
list](evidence/e0-input-sha256-v10.txt). For these, tutors use **B3 solve first**
before opening **B3 case 1**, then record decisions on **Batch 3**. The two
exercises resemble earlier examples. Reviewers must record any prior key
exposure; synthetic canary phrases are test markers, not part of the teaching
task. The first two batches' review rows were not changed.

A fourth batch contains two critical listening retrieval drafts, in `Batch 4`
and `B4` tabs. Reviewers should use **B4 solve first** before opening the case
tabs and record decisions in **Batch 4**. These cases use recording metadata
and synthetic references; there is no audio to hear, and material review flags
are test setup, not tutor approval. Review the expected handling of the declared
availability or version mismatch, and record any prior key exposure. Both
reviewers are needed for these critical cases. Previous batch rows were not
changed by adding Batch 4.

A fifth batch contains two ordinary activity-context drafts. Use **B5 solve
first** and the corresponding **B5 exercise** tab before the case tabs, then
record decisions in **Batch 5**. The approval/copy and confirmation times are
authored synthetic inputs, not observed application actions. The cases cover
assignment with unknown use and encounter without an attempt; neither is a
complete job. Earlier batch rows were not changed by adding Batch 5.

A sixth batch contains one paired domain-search draft and one zero-opportunity
feedback extraction draft. Use **B6 solve first** and the matching **B6 exercise**
tab before opening case/JSON tabs, then record decisions in **Batch 6**. The
domain exercise withholds both material answer keys and two answer-revealing
criteria until after independent solving; the full input is in the case/JSON
tabs. The two search requests are independent, and feedback extraction is not
implemented. Earlier batch rows were not changed by adding Batch 6.

A seventh batch contains one critical learner-source access draft and one
ordinary feedback trend draft. Use **B7 solve first** and the matching
**B7 exercise** tab before opening case/JSON tabs, then record decisions in
**Batch 7**. The blind privacy view withholds one answer-revealing
positive-control sentence; the complete input is available after solving.
Canaries are synthetic test markers. The tests observe local intake and shared
arithmetic only, not a full homework or feedback job. Earlier tabs were not
targeted while adding Batch 7.

An eighth batch contains three ordinary drafts: a possible-regression alert,
completion versus accuracy, and goal-led fluency retrieval. Use **B8 solve
first** and the corresponding **B8 exercise** tabs before opening case/JSON
tabs, then record decisions in **Batch 8**. The workload recommendation is an
unexecuted draft label. The fluency private marker is synthetic and was not
submitted as a learner record; the test observes retrieval only. Earlier tabs
were not targeted while adding Batch 8.

A ninth batch contains ordinary FB-01 and critical FB-06 feedback extraction
drafts. Use **B9 solve first** and the matching exercise tabs before the
case/JSON tabs; record decisions in **Batch 9**. Both reviewers review FB-06.
The safety warning pre-shows that its embedded instruction is untrusted source
text, so reviewers record that exposure and do not claim blind classification
of that point. Other candidate findings can be assessed independently. These
cases are synthetic and the feedback runtime has not been executed.

- [Reviewer 1 workbook](https://docs.google.com/spreadsheets/d/19bL2AUKlSFJL4Obux4Q--ScUnUTdSnypLCs_cnxu_ko/edit)
- [Reviewer 2 workbook](https://docs.google.com/spreadsheets/d/1w2bxtL2GhyMvYCOZnzlWYBSbR34_KYy1UHjW9hAWdoA/edit)
- [Separate reviewer instructions](reviewer-instructions.md)

The owner confirmed reviewers 1 and 2 are qualified and available. The two
workbooks are separate so their initial judgments can be independent. At
creation both were private to the connected account; the owner must give the
intended reviewer edit access and send that reviewer the corresponding link.
Do not make them public or share one tutor's initial answers with the other.
No access invitations or messages have been sent by the assistant.

Ask each tutor to read **Instructions**, complete **Solve first** before
opening case tabs containing proposed keys, then examine each case input and
expected label. In **Review**, the tutor records qualification, date, decision,
reasoning, corrections or alternatives, and independent answers and key
exposure. A separate column records any later disagreement and resolution.
The **Review rules** tab contains the relevant policy excerpts. Once both have
finished, the owner reconciles their decisions and returns the results for
recording against the exact case revisions. A changed case needs a new revision
and review; a workbook entry does not automatically approve a case or release.
For the additional cases, use **B2 solve first** and enter decisions on
**Batch 2**. The one B2 exercise repeats an exercise from the first batch: if a
reviewer has already seen its key, they must record that fact rather than call
the solution blind.

The initial local workbooks and native handoff underwent [independent technical
review](evidence/e0-workbook-review.md). After import
as native Google Sheets, the assistant read back every case ID, revision, hash
and original JSON cell, and all five keyless exercises in both files; it also
checked that review fields were blank. The exercise column was moved next to
its case ID and identifiers were frozen for readability; the post-change rows
and frozen-column settings were read back. Google-rendered representative
review and keyless views were visually inspected. This verifies the initial
handoff snapshot only. After the second batch was added, the assistant read
back its four IDs, revisions, hashes, original JSON, flattened case fields and
keyless exercise in both workbooks, and rechecked the original 19 identities
and hashes. Representative second-batch Google views were visually inspected.
The [second-batch independent review](evidence/e0-second-batch-review.md)
confirmed those identities, source bytes and keyless exercise without reading
reviewer comments. For batch 3, the assistant read back both new IDs, hashes,
original JSON, flattened case fields and both keyless exercises in each file;
the earlier Batch 2 identities and hashes were unchanged. Representative
third-batch Google views were visually inspected. Later edits or reviewer
access are not established. The [third-batch independent review](evidence/e0-privacy-review.md)
confirmed its case identities, source data and keyless exercises without
reading reviewer decisions or comments.

For Batch 4, the author read back both case IDs, revisions, hashes, original
JSON and flattened fields in each workbook. An independent reviewer checked the
two workbooks' reviewer IDs, case identities, hashes, exact original JSON and
keyless exercises, without reading reviewer decisions or comments. This is a
point-in-time readback, not evidence of reviewer access or completed review.
The Batch 4 overview and a representative solve-first view were inspected in
Google Sheets. A clipped scope note was corrected by increasing its row height;
the corrected overview was then visually checked in both workbooks.

For Batch 5, the author read back every written cell and the independent
reviewer checked case IDs, revisions, hashes, exact JSON and all flattened
keyless inputs in both files, without reading reviewer decisions or comments.
This is a point-in-time readback, not proof of access or tutor review. The
overview and a representative solve-first and exercise view were visually
inspected. Clipped hash rows were enlarged in both workbooks, and the corrected
representative exercise view was checked in each.

For Batch 6, the author checked all written cells and an independent reviewer
checked both workbooks' identities, case IDs, revisions, hashes, original JSON
and keyless inputs, without reading reviewer decisions or comments. The first
readback identified answer-revealing criteria in the blind domain view; these
were withheld, the warnings corrected, and the independent reviewer rechecked
the corrected view. Representative overview, solve-first and exercise views
were inspected visually. This is a point-in-time handoff check, not tutor
access, completed review or application evidence.

For Batch 7, the author read back all written cells and an independent reviewer
checked both workbooks' reviewer IDs, case identities, revisions, hashes, exact
JSON, blind inputs and scope warnings, without reading reviewer decisions or
comments. The overview, solve-first and a representative input view were
visually inspected; excessively tall frozen rows were corrected in both files
and the representative views rechecked. This does not establish tutor access or
completed review.

For Batch 8, all 2,274 written values were read back across both workbooks,
including exact original JSON; reviewer decision validation was checked. An
independent readback confirmed the reviewer identities, case IDs, revisions,
hashes and complete blind inputs without reading decisions or comments. A
representative overview, solve-first and exercise view were visually inspected.
This is a point-in-time handoff check, not proof of tutor access or review.

For Batch 9, the author read back all written values and decision validation;
an independent reviewer verified both workbooks' identities, exact original
JSON, case IDs/revisions/hashes and every blind input field without reading
reviewer decisions or comments. The initial warning revealed the untrusted-text
classification; the correction explicitly marks that cue as pre-shown, and
the independent reviewer rechecked it. Representative overview, solve-first
and exercise views were visually inspected. This does not establish access,
completed tutor review or application behavior.

Langfuse annotation queues were considered first. The current documented queue
operates on traces, observations or sessions, and no connected synthetic-only
Langfuse project was available in this session. The user authorized the Google
Sheets alternative. No credentials or production data were inspected or used.

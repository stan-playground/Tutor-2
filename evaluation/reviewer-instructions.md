# Instructions for reviewing the synthetic evaluation cases

These instructions are for the qualified English tutors reviewing E0 draft cases
in the Google Sheets workbook supplied by the project owner. The learner
situations, transcripts, activities and tutor identities are synthetic. Never
add real learner data, passwords, access tokens or other secrets to the workbook.
If you see any such information, stop using the affected material and notify the
owner through the agreed private channel.

The owner has confirmed that reviewers `1` and `2` are qualified and available.
No review decision is implied by that confirmation. The workbook is a way to
record your teaching judgment; it is not itself a release approval or evidence
that the application behaves as expected.

## What you will receive

Each row or linked case should identify the exact **case ID**, **revision**,
**SHA-256 content hash**, job, stage and severity. It should give you access to:

- The case's `input`: the task request, fixed clock, synthetic learner and
  ownership context, source and observation revisions, transcript or activity,
  and any other facts supplied for that particular case.
- Its `expectedOutput`: the proposed facts, counts, source or observation IDs,
  uncertainty, prohibited claims or writes, and reached and unreached stages.
- Relevant rubric or policy references, including the count and recent-history
  rules in [Product Decisions PD-08 and PD-09](../Product%20Decisions.md#pd-08-track-performance-at-the-subskill-level)
  and the [dataset guide](../specs/datasets.md).

The hash identifies the exact bytes of the case file, not only its visible name.
Compare the ID, revision and hash with the case material supplied for review.
If any is missing or you cannot inspect the corresponding input and expected
output, ask the owner for the missing material and do not approve the case.
Avoid copying a review from one revision, stage sample or variant to another.
On the case tabs, a leading apostrophe before a UTC timestamp is a spreadsheet
text marker; it is not part of the original timestamp. The `Original JSON` tab
contains the full original case text associated with the hash.

## Review each assigned case independently

1. **Start with the input.** Read the task, synthetic context, clock, source IDs,
   dates, confirmation and assistance facts. For an exercise with a proposed
   answer key, solve it yourself from the exercise *before* looking at the key.
   Work out the relevant expected result and note any ambiguity first. If the
   workbook has already shown you a proposed key, say so; the exercise cannot
   then be represented as independently solved blind. Start with the `Solve
   first` tab, which contains the exercise and instructions without the key,
   together with the original case ID, revision and hash. Do not open the case
   or `Original JSON` tabs until you have recorded your independent answer.
   An `input` can itself contain a material's answer key.
   For the separate second batch, use `B2 solve first` and record decisions in
   `Batch 2`. Its exercise repeats an item from the first batch: if you have
   already seen that item's key, record the exposure rather than calling the
   later solution blind.
   For the third batch, use `B3 solve first` before opening `B3 case 1`, and
   record decisions on `Batch 3`. The exercises resemble earlier examples;
   record any prior key exposure. The synthetic canary phrases are test
   markers, not part of the teaching exercise.
   For the two critical listening cases, start with `B4 solve first`, then
   record decisions in `Batch 4`. These exercises share a pattern, so record
   any prior exposure to the proposed labels. They supply synthetic recording
   metadata, not audio: judge the proposed handling of the declared unavailable
   or mismatched recording, and do not claim to have heard or checked it.
   For the two activity cases, start with `B5 solve first` and the matching
   `B5 exercise` tab before opening a case tab. Record decisions in `Batch 5`.
   Approval, copying and confirmation times are supplied synthetic facts; they
   do not represent observed application actions. Distinguish assignment with
   unknown use from a confirmed encounter without an attempt or result.
   For the domain and zero-opportunity feedback cases, start with `B6 solve
   first` and the matching `B6 exercise` tab before opening the case tabs.
   Record decisions in `Batch 6`. The domain exercise withholds its two answer
   keys and answer-revealing criteria until after you solve both activities;
   the case and original JSON tabs then provide the complete input. The two
   domain requests are independent, not an approval to relax a constraint. The
   feedback extraction case is a draft, not an observed runtime result.
   For the learner-source privacy and feedback trend cases, use `B7 solve
   first` and the matching `B7 exercise` tab before opening case/JSON tabs,
   then record decisions in `Batch 7`. One answer-revealing positive-control
   sentence is withheld from the blind privacy input; the complete input is
   available after solving. The canaries are synthetic markers. The feedback
   case checks shared arithmetic only, not feedback-source authorization or
   generation.
   For the possible-regression, completion and goal-led fluency cases, use
   `B8 solve first` and the matching `B8 exercise` tabs before opening any B8
   case or original JSON tab. Enter decisions in `Batch 8`. The fluency private
   note is a synthetic marker; it is not a submitted learner record. The
   workload-check recommendation is a draft expectation, not an observed
   calculator output.
   For the two feedback extraction drafts, use `B9 solve first` and the
   matching exercise tabs before opening the case/JSON tabs; record decisions
   in `Batch 9`. Both reviewers must review the critical FB-06 case. The
   safety instruction already identifies the embedded instruction as untrusted
   source text; record this exposure and do not claim blind classification of
   that point. Assess the remaining learner findings independently.
2. **Compare with the expected labels.** Read each expected fact and reason,
   including the source/observation IDs and revisions, expected outcome,
   prohibited claims and writes, and stage/stop reasons. Check whether the
   supplied input actually supports each claim, whether meaningful valid
   alternatives are accepted, and whether a missing or uncertain fact is
   honestly left unknown. Assess the scope of the case; do not infer a result
   for a stage the case never reaches.
3. **Record a decision and rationale.** Use the sheet's per-reviewer fields to
   choose `approve`, `revise`, or `reject`. Explain the evidence and teaching
   reasoning, including any corrections or alternative answer you propose.
   `revise` means a specific change could make the case suitable; `reject`
   means it is unsuitable as proposed. Do not use an empty reason or infer a
   decision from another reviewer's entry.

### What to check in these cases

- **Counts and recent evidence:** Check each numerator and denominator against
  its own named measure and selected evidence. Zero opportunities means an
  unknown rate, not zero ability or success. Distinguish an attempted target
  from an opportunity where it was required and a context where avoiding it
  was appropriate. A valid optional paraphrase is not automatically a missed
  required use, and silence without an observable opportunity is not an error.
- **Selection and trends:** Check the fixed clock, source dates, evidence types,
  task demands and assistance before comparing observations. The current rule
  uses up to the latest four lessons and four homework submissions within 90
  days, separately. A trend needs at least three comparable observations with
  at least five relevant opportunities each: first-to-last change of at least
  +0.15 is improving, at most −0.15 is regressing, otherwise stable; conflicting
  measure trends are mixed. Smaller samples are insufficient. Check exact source
  and observation IDs as well as numbers.
- **Maintenance and older history:** Three comparable ratios of at least 0.85
  can support a maintenance *candidate* only with applicable use/avoidance
  support; maintenance additionally needs tutor confirmation. Do not treat a
  candidate as confirmed. Older, source-qualified history may inform context;
  it must not change the recent denominators or by itself prove forgetting,
  mastery or product-caused improvement.
- **Transcript extraction and feedback:** Check which speaker said each
  segment, the prompt and response together, any task and assistance context,
  and the candidate findings and counts. Extracted candidates are not saved
  confirmed observations. Do not infer pronunciation, listening ability,
  progress or learning gain from transcript wording alone. Feedback source
  selection does not require a homework job or an exercise.
- **Retrieval material:** Solve closed-choice material independently, then
  assess whether the activity, key and criteria match the stated teaching
  purpose, target level, task and exact confusion. A topic or domain match alone
  is not enough. The synthetic material's `reviewed` flag is setup for a local
  software check; it is not evidence of an actual tutor review. The contrast
  case explicitly records that one positive-form-only distractor could not be
  imported under a truthful target with the current software; do not mark that
  retrieval behavior as proven.

## What to enter in the sheet

For **each case and each reviewer**, record:

| Field | What to enter |
| --- | --- |
| Case identity | Exact case ID, revision and full SHA-256 content hash from the supplied case. |
| Reviewer | Reviewer ID (`1` or `2`) and a short description of your relevant English-teaching qualification; do not add contact details. |
| Date | Date you completed this review, using the date format requested in the workbook. |
| Decision | `approve`, `revise`, or `reject` for this exact case revision. |
| Rationale | The decisive evidence and teaching reason, including source/segment IDs or calculations where relevant. |
| Corrections or alternatives | Exact proposed correction, acceptable alternative or reason no correction is suitable. Say explicitly if none. |
| Independent solving | For closed-answer material, your independently worked answer and whether you saw the proposed key first. |
| Disagreement and resolution | Any disagreement, how it was resolved and by whom; leave unresolved if agreement has not actually been reached. |

The owner may ask both tutors to review every supplied case. At minimum, every
case admitted to a frozen suite needs review by one qualified tutor; every
critical case and at least `ceil(20% × ordinary cases)` in that suite need a
second qualified tutor. The ordinary count is the number of actual ordinary
items in that frozen suite, including applicable variants, not just base-family
names. For example, seven ordinary items require second reviews for at least
two. The owner determines the actual suite and second-review coverage.

Reviewers should make independent initial judgments before seeing each other's
decisions where the workbook permits. Do not overwrite another reviewer's
entries. If judgments differ, record both original decisions and the discussion;
the owner coordinates resolution and records the final rationale. An unresolved
disagreement blocks approval of that case. If a correction changes case content,
the owner must prepare a new revision and hash and obtain review of that exact
revision; agreement about the earlier bytes does not approve the new ones.

## Returning the review

When your assigned rows are complete, tell the project owner through the agreed
private channel that your entries are ready and identify any missing inputs,
uncertainties and unresolved disagreements. The owner reconciles independent
reviews, records the exact reviewed revisions and decisions in the project's
case records, and checks second-review coverage. A sheet entry or tutor approval
of a case does not itself approve the product, a release, a model result, or
real-learner use. Those decisions and checks are separate.

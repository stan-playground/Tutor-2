# Initial synthetic evaluation fixtures

These two development items start stage 0's fixture work. They are authored
inputs with draft expected labels, not approved gold, a release suite, a
provider experiment or evidence that the application performs either task.
The construction contract remains [specs/datasets.md](../specs/datasets.md).

- `homework/HW-ARITH-01.json` isolates confirmed-count arithmetic. It is not an
  extraction example or one of the twelve required complete-job families.
- `feedback/FB-SOURCE-01.json` contains an authored A2 transcript and source
  selection expectations. It requires neither homework nor an exercise.
- `item.schema.json` versions the initial structural contract as `1`. Its
  validation cannot verify pedagogical correctness, human qualifications or
  release admission. It does not implement an evaluation pipeline.

The owner assigned primary reviewer ID `1` and second reviewer ID `2` on
1 November 2026. Assignments are recorded on both item revisions. No reviewer
qualifications, review dates, decisions or approvals have been supplied.
Both items therefore remain `draft`, with `reviewed: false` and empty decision
lists. Before approval, obtain the qualified-tutor reviews and records required
by the dataset contract. Assignment alone is not review.

All learner content and identifiers are synthetic. The fixtures contain no
external teaching text, credentials or production data. Keep related future
variants in the development partition with their source item. Task callers
must receive only `input`; `expectedOutput` and reviewer metadata are evaluator
data. There is no provider caller in this foundation.

The unit checks validate the schema, both JSON items and the duplicate
case-ID/revision boundary. They also reject a missing required field, empty
expectations, an unknown stage and invalid clock formatting. These checks do
not execute the future arithmetic or feedback task and do not grant release
readiness.

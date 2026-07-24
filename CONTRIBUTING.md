# Contributing to SCON

Thank you for your interest in improving the School Counselling Ontology Network
(SCON). SCON is engineered under a governed, consistency-preserving workflow;
contributions are welcome provided they respect that workflow.

## Ways to contribute

- **Report an issue or a modelling error** — open an issue using the *Bug /
  modelling error* template.
- **Request a new term** (class, property, or individual) — open an issue using
  the *Term request* template, stating the intended label, definition, parent
  (genus), module, and at least one competency question or use case the term
  serves.
- **Propose a change via pull request** — see the workflow below.

## Governance workflow (the consistency gate)

Every proposed addition — whether authored, reused, or LLM-proposed — is admitted
only if it passes the same gate:

1. **Grounding.** The term is placed under an appropriate BFO / OBO genus and
   assigned to exactly one `scon:module`.
2. **Definition.** The term carries an `rdfs:label` and an `IAO:0000115`
   textual definition (genus–differentia form).
3. **Provenance.** The term carries `scon:populationProvenance`
   (`author-vocabulary`, `reused-vocabulary/external`, or
   `llm-proposed-human-approved`). LLM-proposed terms are marked pending
   expert adjudication.
4. **Adjudication.** A maintainer reviews the proposal against the ASCA National
   Model and the ORSD scope.
5. **Consistency check.** The ontology must remain **consistent under HermiT**
   after the change (`robot reason`), and should not introduce OOPS! pitfalls.
6. **Competency questions.** Existing CQ tests must still pass; new terms should
   reference the CQ(s) they help answer.

A change is merged only when steps 1–6 are satisfied. Adjudication decisions are
logged under `population/` for traceability.

## Technical checklist for pull requests

- Edit `scon-ontology-<version>.owl` in Protégé 5.6+ (RDF/XML serialisation).
- Do **not** commit Protégé helper files (`catalog-v001.xml`, `*.owl.bak`).
- Run the reasoner (HermiT) and confirm the ontology is consistent.
- Update `CHANGELOG.md` under an *Unreleased* heading.
- For a release, bump the version, set a new `owl:versionIRI`, tag `vX.Y.Z`,
  and attach the OWL file to the GitHub Release.

## Licence of contributions

By contributing you agree that your contributions are licensed under
**CC BY 4.0**, the licence of this repository.

## Contact

Amiru Bakariwie — abakariwie@ubids.edu.gh

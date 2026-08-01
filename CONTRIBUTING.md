# Contributing to SCON

Thank you for your interest in SCON. This guide explains how to propose a change and
what a proposal has to satisfy before it can be merged.

## Ground rules

SCON is a logical theory, not a word list. Every proposal is judged by what it entails,
not only by what it names. Three rules follow from that, and they admit no exceptions.

1. **Nothing enters that breaks consistency.** A change is admissible only if the
   ontology remains consistent and every class remains satisfiable after it is added.
   The reasoner is the gate, and it applies identically to terms proposed by a
   maintainer, terms drawn from another ontology, and terms proposed by a language
   model.
2. **Every class carries a definition.** New classes must carry an `IAO:0000115`
   textual definition written for a practitioner, not a paraphrase of the class name.
3. **No real or identifiable person appears anywhere.** All released instance data are
   constructed, de-identified exemplars. Never commit a case record, a screening result
   belonging to a real student, or a credential-bearing configuration file.

## Before you open a pull request

- Open the ontology in Protégé 5.6+ and start HermiT. Confirm no class is unsatisfiable
  and no red appears in the class hierarchy.
- Run `python tools/verify_release.py "scon-ontology-1.1.0.owl"`. It must print
  `PASS`. If it reports missing core features, your working copy has been damaged, most
  often by opening a data file as a new ontology instead of importing it. See
  `docs/release-notes.md`.
- Run the competency-question suite in `competency-questions/sparql/`, starting with
  `00_signature_check.rq`. If you renamed or removed a term, run
  `python tools/verify_release.py "scon-ontology-1.1.0.owl" --signature`, which names
  every suite term the ontology no longer declares.
- Record what changed in `CHANGELOG.md` under an `Unreleased` heading.

## Proposing a new term

State, in the pull-request description:

- the term, its parent class, and its `IAO:0000115` definition;
- the competency question or practical need that the term serves, since a term with no
  question behind it is usually not needed;
- whether an existing term in SCON, or in BFO, IAO, RO, OBI, MFOEM or W3C Time, already
  covers the notion; reuse is preferred to invention;
- any external vocabulary the term corresponds to. Record correspondence with
  `rdfs:seeAlso` rather than asserting `owl:equivalentClass`, unless the identity really
  does hold in both directions.

## Proposing a new competency question

Competency questions are requirements, and in SCON they are also tests. A new question
must arrive with a SPARQL query that answers it over the inferred model, placed in
`competency-questions/sparql/`, and with the question text added to
`competency-questions/competency-questions.md` and embedded in the ontology as a
`competencyQuestion` annotation.

## Versioning

SCON follows semantic versioning. A release that only adds terms is a minor release. A
release that renames, removes, or re-axiomatises an existing term is a major release and
must document a migration path for every affected IRI.

## Provenance

Terms proposed with the assistance of a language model are annotated with a pending
adjudication status until a maintainer has reviewed them, and the released artefact
reports the division of labour openly. Please preserve that annotation on any term you
carry forward.

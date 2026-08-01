# Changelog

All notable changes to the School Counselling Ontology Network (SCON) are recorded here.
The format follows Keep a Changelog, and the project uses semantic versioning.

## [1.1.0] — 2026

Initial public release.

### Contents

- **472 classes**, of which 6 are defined classes specified
  by `owl:equivalentClass` and placed by the reasoner. The remaining
  466 each carry an `IAO:0000115` textual definition written for
  a practitioner.
- **56 object properties** declared for the domain,
  63 including those reused from external ontologies, and
  **36 data properties**.
- **483 subclass axioms**, 8 disjointness
  groupings, 1 property chain, 4 inverse property
  axioms, 13 functional properties,
  2 transitive properties, 11 existential
  restrictions and 1 nominal restriction.
- **9 modules**, with every class carrying a machine-readable
  `scon:module` annotation.
- **36 competency questions** embedded as annotations, twelve for
  each of the three ASCA developmental domains, each with an executable SPARQL query.
- **21 named individuals**, comprising the controlled vocabulary for risk
  level, tiered support and developmental domain, together with exemplar individuals that
  exercise the defined classes and the property chain.
- **Foundational grounding** in Basic Formal Ontology, with fourteen BFO classes imported
  under their OBO PURLs and further terms reused from the Information Artifact Ontology,
  the Ontology for Biomedical Investigations, the Emotion Ontology and the W3C Time
  Ontology.
- **Provenance on every class**: 377 author-authored,
  59 model-proposed and carrying a pending adjudication status, and
  36 reusing external vocabulary.
- **A synthetic validation dataset** of 18,236 de-identified individuals built around 1,000
  students, and an executable SPARQL suite covering all 36 competency questions.

### Verification

Description logic expressivity is SROIF(D), within the SROIQ(D) bound of OWL 2 DL. The
release classifies as consistent with no unsatisfiable class under HermiT. All 36
competency questions return non-empty answers against the synthetic dataset.

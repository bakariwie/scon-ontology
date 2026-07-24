# Changelog

All notable changes to SCON (School Counselling Ontology Network) are documented
here. The project uses [Semantic Versioning](https://semver.org/), and each
release carries a matching `owl:versionIRI`.

## [1.1.0] — 2026-07

Consistency-preserving, backward-compatible release that deepens the ontology's
definitions, disjointness, and reasoning.

### Fixed
- Corrected the ontology IRI and `owl:versionIRI` to the canonical
  `http://www.semanticweb.org/bakariwie/ontologies/2026/6/scon-ontology-1`
  identifier, realigning them with the term namespace and all documentation.
  The GitHub repository is recorded as the authoritative location (`rdfs:seeAlso`),
  not the identifier.

### Added
- **Definitions:** every one of the 441 domain classes now carries an
  `IAO:0000115` textual definition (up from 79).
- **Defined classes:** six `owl:equivalentClass` classes for automatic
  classification — `AtRiskStudent`, `ChronicallyAbsentStudent`, `HighRiskStudent`,
  `StudentReceivingTieredSupport`, `RecommendedIntervention`,
  `KnowledgeGroundedCounsellingSystem`.
- **Disjointness:** eight `AllDisjointClasses` axioms (up from one) plus an
  `AllDifferent` axiom over the four risk-level individuals.
- **Property axioms:** `hasRiskLevel` and `assignedTier` made functional;
  inverse pairs `hasRiskIndicator`/`isRiskIndicatorOf` and
  `recommendedFor`/`hasRecommendedIntervention`; property chain
  `hasRiskIndicator ∘ hasRiskLevel ⊑ hasStudentRiskLevel`;
  `partOfTrajectory` made transitive.
- **Metadata:** `rdfs:label`, `dcterms:modified`, `owl:priorVersion`,
  `vann:preferredNamespacePrefix`, `vann:preferredNamespaceUri`, and a change note.

### Notes
- DL expressivity moves from SHI(D) to SROIF(D), within SROIQ(D).
- Verified consistent under HermiT; the seed ABox classifies `student_S1` as
  AtRiskStudent, ChronicallyAbsentStudent, HighRiskStudent, and
  StudentReceivingTieredSupport, and `intervention_int1` as RecommendedIntervention.

## [1.0.0] — 2026-06

Initial public release.

### Added
- 441 BFO-grounded domain classes across nine modules (core, academic, career,
  social-emotional, risk-safeguarding, governance, higher-education,
  intelligent-systems, temporal).
- 49 object properties, 21 data properties, 16 seed individuals.
- 36 competency questions embedded as `scon:competencyQuestion` annotations.
- Per-term provenance (author-vocabulary, LLM-proposed, reused).
- Reuse of BFO 2.0, IAO, RO, OBI, MFOEM, and the W3C Time Ontology.
- Published under CC BY 4.0.

[1.1.0]: https://github.com/bakariwie/scon-ontology/releases/tag/v1.1.0
[1.0.0]: https://github.com/bakariwie/scon-ontology/releases/tag/v1.0.0

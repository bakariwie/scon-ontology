# SCON — School Counselling Ontology Network

**SCON** is a modular, BFO-grounded OWL 2 DL ontology for comprehensive counselling across
the academic, career, and social–emotional domains, in both school and higher-education
settings. It is engineered to support intelligent counselling systems: chatbots, socially
assistive robots, recommender systems and early-warning systems.

- **Ontology IRI:** `http://www.semanticweb.org/bakariwie/ontologies/2026/6/scon-ontology-1`
- **Version IRI:** `http://www.semanticweb.org/bakariwie/ontologies/2026/6/scon-ontology-1/1.1.0`
- **Version:** 1.1.0 · **Licence:** CC BY 4.0 · **Reasoner:** HermiT · **Protégé:** 5.6+

## Profile

Every figure below is measured from `scon-ontology-1.1.0.owl` itself, so the documentation does not drift from the artefact.

| | Count |
|---|---|
| Classes | 472 |
| Classes carrying an `IAO:0000115` textual definition | 466 |
| Defined classes (`owl:equivalentClass`) | 6 |
| Classes reused with external identifiers (BFO, IAO, OBI, MFOEM, W3C Time) | 19 |
| Object properties declared for the domain | 56 |
| Object properties including reused | 63 |
| Data properties | 36 |
| Annotation properties | 5 |
| Named individuals | 21 |
| Subclass axioms | 483 |
| Disjointness groupings | 8 |
| Property chain axioms | 1 |
| Inverse property axioms | 4 |
| Functional properties | 13 |
| Transitive properties | 2 |
| Existential restrictions | 11 |
| Nominal (`owl:hasValue`) restrictions | 1 |
| Embedded competency questions | 36 |
| External alignments (`rdfs:seeAlso`) | 25 |
| Labels | 626 |

Description logic expressivity is **SROIF(D)**, within the SROIQ(D) bound of OWL 2 DL. The
artefact uses complex role inclusion, inverse roles, functional roles, one nominal and
datatypes, and omits qualified cardinality restrictions entirely.

## Modules

The ontology is partitioned into 9 modules. Every class carries a
`scon:module` annotation, so the partition is machine-readable rather than a folder
convention.

| Module | Classes |
|---|---|
| `scon-core` | 243 |
| `scon-social-emotional` | 53 |
| `scon-intelligent-systems` | 37 |
| `scon-academic` | 30 |
| `scon-risk-safeguarding` | 29 |
| `scon-career` | 26 |
| `scon-governance` | 20 |
| `scon-higher-education` | 18 |
| `scon-temporal` | 16 |

## Foundational grounding and reuse

SCON is aligned to Basic Formal Ontology as its top-level ontology. Fourteen BFO classes
are imported with their OBO PURLs intact, together with one term each from the Information
Artifact Ontology, the Ontology for Biomedical Investigations and the Emotion Ontology, and
two classes from the W3C Time Ontology. A further 36 classes are
minted in the `scon:` namespace but annotated with the framework their terminology derives
from, among them CASEL, the Big Five taxonomy, the ASCA Student Standards, ESCO and
DOMASEC.

Every class carries a `scon:populationProvenance` annotation recording how it entered the
ontology: 377 author-authored, 59
model-proposed and carrying a pending adjudication status, and
36 reusing external vocabulary.

## Defined classes

Six classes are specified by equivalence rather than by asserted subsumption, so the
reasoner computes their membership:

| Defined class | Condition |
|---|---|
| `AtRiskStudent` | `Student ⊓ ∃hasRiskIndicator.RiskIndicator` |
| `ChronicallyAbsentStudent` | `Student ⊓ ∃hasRiskIndicator.ChronicAbsence` |
| `HighRiskStudent` | `Student ⊓ ∃hasRiskIndicator.(∃hasRiskLevel.{riskLevel_high})` |
| `StudentReceivingTieredSupport` | `Student ⊓ ∃assignedTier.MTSSTier` |
| `RecommendedIntervention` | `Intervention ⊓ ∃recommendedFor.Student` |
| `KnowledgeGroundedCounsellingSystem` | `∃groundedInKB.CounsellingKnowledgeBase` |

The single property chain, `hasRiskIndicator ∘ hasRiskLevel ⊑ hasStudentRiskLevel`, derives
the risk level attaching to a student from the indicators recorded against that student.

## Getting started

1. Open `scon-ontology-1.1.0.owl` in Protégé 5.6+. The file is self-contained.
2. To query with data, add `data/scon-synthetic-abox.ttl`. Protégé has **no Import item in
   its File menu**: go to the **Active Ontology** tab, find the **Ontology imports** panel,
   and click the **⊕** button beside **Direct Imports**, then choose *"Import an ontology
   contained in a specific file"*.
3. **Reasoner > HermiT > Start reasoner**.
4. Open **Window > Tabs > Snap SPARQL Query** and run any file from
   `competency-questions/sparql/`, beginning with `00_signature_check.rq`.

Never open a data file with **File > Open**: that replaces the ontology in the editor
rather than adding to it.

## Validation dataset

`data/scon-synthetic-abox.ttl` holds 18,236 fully synthetic, de-identified individuals
built around 1,000 students: 500 pre-tertiary across Grades 9 to 12 and 500 tertiary
Computer Science students across Levels 100 to 400. It exercises every module and every
competency question. No real or identifiable student data are used or imitated anywhere.

## Validation status

All 36 competency questions execute against the synthetic dataset and return non-empty
answers. Reasoning is consistent with no unsatisfiable class. The queries that turn on
inference rather than assertion, namely severity classification (S-CQ3), recommended
interventions (C-CQ8) and duplicate detection (A-CQ12), are written against the defined
classes and the property chain, so a non-empty answer is itself evidence that the reasoning
layer is working.

Before publishing any change, run:

    python tools/verify_release.py "scon-ontology-1.1.0.owl" --signature

It checks the structural features the release must carry and every term the query suite
relies on, and refuses to pass a file that has lost any of them.

## Repository layout

```
scon-ontology-1.1.0.owl        the ontology, RDF/XML, self-contained
scon-ontology v1.1.0.rdf       identical copy under the alternative file name
src/
  scon-manifest.json           the full structure of the release, extracted
data/
  scon-synthetic-abox.ttl      1,000-student synthetic validation dataset
  vocab.json                   signature contract, generated from the ontology
  README.md
competency-questions/
  competency-questions.md      the 36 competency questions
  sparql/                      one executable SPARQL query per question
tools/
  ontology_report.py           measure the ontology and write docs/ontology-metrics.json
  extract_manifest.py          derive src/scon-manifest.json from the ontology
  verify_release.py            structural and signature check before publishing
docs/
  ontology-metrics.json        the measured counts shown above
  release-notes.md             what the release contains
  using-scon-in-protege.md     step-by-step loading and querying
```

## Citation

Bakariwie, A., Weyori, B. A., & Afriyie, Y. (2026). *SCON: School Counselling Ontology
Network* (Version 1.1.0) [OWL ontology]. https://github.com/bakariwie/scon-ontology

## Licence

Creative Commons Attribution 4.0 International (CC BY 4.0). You may share and adapt the
material for any purpose, including commercially, provided you give appropriate credit.

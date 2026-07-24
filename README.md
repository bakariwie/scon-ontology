# SCON — School Counselling Ontology Network

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
![Version](https://img.shields.io/badge/version-1.1.0-informational)
![Profile](https://img.shields.io/badge/OWL%202-DL%20(SROIF(D))-success)

SCON is a **modular, BFO-grounded, reasoning-enabled OWL 2 DL ontology** for
comprehensive counselling across the **academic, career, and social–emotional**
developmental domains of the ASCA National Model, in **school and
higher-education** settings. It is engineered as the semantic substrate for
**intelligent counselling systems** — chatbots and conversational agents,
socially assistive robots, recommender, decision-support, and early-warning
systems.

- **Ontology IRI:** `http://www.semanticweb.org/bakariwie/ontologies/2026/6/scon-ontology-1`
- **Version IRI:** `…/1.1.0`  ·  **Licence:** CC BY 4.0  ·  **Reasoner:** HermiT
- **Canonical file:** `scon-ontology-1.1.0.owl` (RDF/XML; opens in Protégé 5.6+)

## Highlights (v1.1.0)

- **447 classes** (441 domain + 6 defined), **52** object and **21** data properties, in **9 annotated modules**.
- **Every class defined** with an `IAO:0000115` textual definition.
- **6 defined classes** for automatic classification (`AtRiskStudent`, `HighRiskStudent`, `RecommendedIntervention`, …).
- **8 disjointness axioms**, functional/inverse/transitive properties, and a property chain.
- **36 competency questions** embedded as annotations and formalised in [`competency-questions/`](competency-questions/competency-questions.md).
- Per-term provenance (author / LLM-proposed / reused); consistent under HermiT.

## Repository layout

| Path | Contents |
|------|----------|
| `scon-ontology-1.1.0.owl` | Canonical ontology (RDF/XML) |
| `README.md` / `README.txt` | This overview |
| `LICENSE` | CC BY 4.0 |
| `CITATION.cff` | How to cite (GitHub "Cite this repository") |
| `CHANGELOG.md` | Version history |
| `CONTRIBUTING.md` | Governance & term-proposal workflow |
| `competency-questions/` | The 36 CQs with DL/SPARQL formalisations |
| `docs/` | ORSD, WIDOCO HTML docs, evaluation reports |
| `population/` | LLM candidate batches + adjudication logs |
| `releases/` | Tagged version snapshots |

## Quick start

1. Open `scon-ontology-1.1.0.owl` in **Protégé 5.6+**.
2. **Reasoner → HermiT → Start reasoner** (expected: *consistent*).
3. In the **DL Query** tab, try `HighRiskStudent` or `Intervention and (recommendedFor some Student)`.
4. In the **Snap SPARQL** tab (Window → Tabs), query the inferred model — see [`competency-questions/`](competency-questions/competency-questions.md).

## Citing SCON

> Bakariwie, A., Weyori, B. A., & Afriyie, Y. (2026). *SCON: School Counselling
> Ontology Network* (Version 1.1.0) [OWL ontology]. https://github.com/bakariwie/scon-ontology

The associated systematic review is published in *Discover Artificial
Intelligence* (advance online publication).

## Acknowledgement of AI assistance

The generative AI tool Claude (Anthropic) assisted in vocabulary organisation,
candidate-axiom generation, class-definition drafting, and documentation, under a
human-adjudication and HermiT consistency-gate workflow. All committed content is
the responsibility of the authors.

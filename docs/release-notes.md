# Release notes — SCON 1.1.0

## What SCON is

SCON is a domain ontology for comprehensive counselling in schools and higher-education
institutions. It is designed to be reasoned over rather than merely browsed: the adequacy
of the artefact is decided by what it entails, not by how many terms it contains.

## Scope

The ontology spans the three developmental domains of comprehensive counselling practice,
namely academic, career and social-emotional development, together with five concerns that
traverse all three: safeguarding and risk, governance and consent, temporality, financial
need and aid, and the vocabulary that intelligent systems consume. A ninth module carries
provision specific to the higher-education setting, including academic standing, research
interests, capstone supervision and work placements.

## Design commitments

**Foundational grounding.** Every primitive class descends by asserted subsumption from a
Basic Formal Ontology category. Fourteen BFO classes are imported under their OBO PURLs, so
a term borrowed from BFO remains globally identifiable as BFO's term rather than being
renamed into the SCON namespace. The same discipline applies to the reused terms from the
Information Artifact Ontology, the Ontology for Biomedical Investigations, the Emotion
Ontology and the W3C Time Ontology.

The categorial discipline does real work. Roles are never modelled as subclasses of person,
so a student role and a peer-mentor role can be borne by the same individual without
contradiction. Dispositions are never modelled as processes, so a behavioural risk tendency
that may or may not manifest is typed correctly. Information content entities such as the
counselling record are kept distinct from the processes that produce them, so an assessment
record is about a state rather than being one.

**Definitions before axioms.** Each of the 466 primitive classes
carries an `IAO:0000115` textual definition written for a practitioner rather than a
paraphrase of the class name. A term with no definition has no place in the release.

**Reasoning rather than assertion.** Six classes are specified by equivalence, so their
membership is computed. A student for whom a risk indicator has been recorded is classified
as an `AtRiskStudent` by the reasoner, not by whoever operates the system, and the
classification can be explained by extracting the justification. The single property chain,
`hasRiskIndicator ∘ hasRiskLevel ⊑ hasStudentRiskLevel`, derives the risk level attaching to
a student from the indicators recorded against that student. Complex role inclusion of this
kind is available in SROIQ(D) and unavailable in the tractable profiles, which is why the
release targets OWL 2 DL.

**Expressivity by choice.** The logic the artefact uses is narrower than the profile
permits. It employs complex role inclusions, inverse roles, functional roles, datatypes and
a single nominal, and omits qualified cardinality restrictions entirely. That restraint is
a design result: it keeps the artefact clear of the constructs whose interaction drives
reasoning cost.

**Auditable provenance.** Every class records how it entered the ontology.
377 classes are author-authored, 59 were
proposed by a language model and carry a pending adjudication status, and
36 reuse vocabulary drawn from an external framework. Publishing
the split makes the division of labour inspectable, and it also makes it modest:
automation contributed roughly one term in eight, and every one of those terms passed a
reasoner-enforced consistency check before commitment.

## Requirements and validation

Requirements are stated as 36 competency questions, twelve for
each developmental domain, embedded in the ontology itself as machine-readable annotations
so that they travel with the artefact. Each has an executable SPARQL query in
`competency-questions/sparql/`.

Validation uses a synthetic dataset of 18,236 de-identified individuals built around 1,000
students. Specific situations are planted so that reasoning has something to prove:
students carrying high-risk indicators so the property chain fires, students with attendance
below threshold so the chronic-absence classifier is non-empty, a duplicated intervention
pair so duplicate detection returns a result, students in milestone grades deliberately
without a plan so the closing-the-gap query has a real target group, and screenings above
the published threshold that must escalate.

All 36 questions return non-empty answers. The release classifies as consistent with no
unsatisfiable class.

## Release integrity

`tools/verify_release.py` checks a candidate file for the structural features the release
must carry and for every term the query suite relies on, and refuses to pass a file that has
lost any of them. Run it before every publication. The check exists because the most common
way to damage an OWL release is not a bad axiom but a mis-handled file: opening a data file
with **File > Open** replaces the ontology in the editor rather than adding to it, and
saving from that window silently discards the ontology.

## Ethics

No real or identifiable student data appear anywhere in the release. Counselling records are
confidential, consent for secondary use is rarely obtainable, and releasing instance data
would defeat the safeguarding purpose the ontology exists to serve. All individuals in the
validation dataset are constructed exemplars.

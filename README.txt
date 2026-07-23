=====================================================================
 SCON : SCHOOL COUNSELLING ONTOLOGY NETWORK
 README (v1.0.0)
=====================================================================

Ontology IRI   : https://github.com/bakariwie/scon-ontology
Version IRI    : https://github.com/bakariwie/scon-ontology-1/1.0.0
Version        : 1.0.0
Licence        : Creative Commons Attribution 4.0 International (CC BY 4.0)
                 https://creativecommons.org/licenses/by/4.0/
Canonical file : scon-ontology-1.owl  (RDF/XML; opens directly in Protege 5.6+)
Repository     : https://github.com/bakariwie/scon-ontology

Authors
  Amiru Bakariwie (corresponding) - Department of Computer Science,
    Faculty of ICT, University of Business and Integrated Development
    Studies (UBIDS), Wa, Ghana - abakariwie@ubids.edu.gh
    ORCID 0009-0009-8471-2091
  Benjamin A. Weyori - Department of Computer and Electrical
    Engineering, School of Engineering, University of Energy and
    Natural Resources (UENR), Sunyani, Ghana - ORCID 0000-0001-5422-4251
  Yaw Afriyie - Department of Computer Science, Faculty of ICT, UBIDS,
    Wa, Ghana - ORCID 0000-0003-4821-5804

---------------------------------------------------------------------
1. WHAT SCON IS
---------------------------------------------------------------------
SCON is a modular, reasoning-enabled domain ontology for COMPREHENSIVE
COUNSELLING in SCHOOL and HIGHER-EDUCATION institutional environments.
It is grounded in the ASCA National Model and the ASCA Student
Standards (Mindsets & Behaviors for Student Success), and it is
engineered expressly to support the construction of INTELLIGENT
COUNSELLING SYSTEMS: chatbots and conversational agents, socially
assistive robots, recommender systems, decision-support systems, and
early-warning systems. Such systems ground their outputs in SCON's
knowledge base, constrain hallucination through a logical consistency
gate, detect and escalate crisis-level content to human counsellors,
and explain their inferences.

The requirements for SCON derive from the authors' PRISMA-guided
systematic literature review of ontologies in school counselling, which
established that no existing ontology models counselling as an
integrated domain spanning academic, career, and social-emotional
development.

---------------------------------------------------------------------
2. CONTENT AT A GLANCE (v1.0.0)
---------------------------------------------------------------------
  SCON-native classes ................. 441
  SCON-native object properties ....... 49
  SCON-native data properties ......... 21
  Total SCON-native terms ............. 511
  Named individuals (seed ABox) ....... 16
  Competency questions (annotations) .. 36  (12 per ASCA domain)
  Term definitions (IAO:0000115) ...... 79 key classes (leaves carry
                                        labels, modules, provenance;
                                        definitions grow per release)

Modules (every class carries a scon:module annotation):
  core | academic | career | social-emotional | risk-safeguarding |
  governance | higher-education | intelligent-systems | temporal

Highlights per module:
  core ................ persons, organisations, facilities, roles,
                        counselling processes, plans, goals, records
  academic ............ academic dispositions, issues (underachievement,
                        retention/dropout risk, probation), advising,
                        educational processes, transcripts, requirements
  career .............. interests, aptitudes, work values, occupations,
                        career clusters, pathways, postsecondary plans,
                        work-based learning (internship, job shadowing,
                        service learning, apprenticeship, co-op)
  social-emotional .... CASEL competencies, Big Five traits, emotion
                        episodes (MFOEM-aligned), mental-health and
                        adjustment concerns, coping and regulation
  risk-safeguarding ... risk indicators (chronic absence, discipline
                        referral, screening flag, GPA decline), risk
                        levels (low/moderate/high/imminent), MTSS tiers,
                        referral, mandated reporting, crisis response
  governance .......... counselling records, guardian AND student
                        self-consent (HE), confidentiality, FERPA and
                        GDPR individuals, retention policy, audit log
  higher-education .... HE student types (undergraduate, postgraduate,
                        international, first-generation, mature,
                        distance), universities/colleges, counselling
                        centres, thesis supervision, credit transfer,
                        academic appeal
  intelligent-systems . chatbot, conversational agent, socially
                        assistive robot, recommender, early-warning
                        system, LLM, dialogue manager, intent
                        classifier, sentiment/emotion recognition,
                        safety guardrail, student model, utterance,
                        intent, system response, crisis detection
                        alert, escalation-to-human, human-in-the-loop
  temporal ............ W3C Time-aligned academic periods and process
                        boundaries (session start/end, graduation date)

---------------------------------------------------------------------
3. DESIGN COMMITMENTS
---------------------------------------------------------------------
Top-level ontology : BFO 2.0. A minimal MIREOT-style subset of BFO
  classes is declared with canonical purl.obolibrary.org IRIs so the
  file opens offline; the full BFO may be imported instead via
  owl:imports http://purl.obolibrary.org/obo/bfo.owl.

Logical reuse (term-level, verified IRIs):
  IAO:0000030 information content entity     (records, plans, data)
  OBI:0000011 planned process                (counselling processes)
  MFOEM:000001 emotion process               (emotion module anchor)
  RO:0000056/0000057 participates in / has participant
  RO:0000087 has role   |  RO:0000091 has disposition
  BFO:0000055 realizes  |  BFO:0000034 function | BFO:0000035
  process boundary
  W3C Time Ontology: ProperInterval, Instant, hasBeginning, hasEnd

Annotation-level alignment (dcterms:source / rdfs:seeAlso; no
diagnostic or logical import):
  ASCA Student Standards (primary domain model)  |  CASEL  |  DOMASEC
  Big Five taxonomy  |  ERIC Thesaurus  |  UNESCO ISCED  |  IEEE LOM
  O*NET Content Model  |  ESCO  |  OccO  |  EduCOR  |  schema.org
  FOAF  |  DSM-5-TR and SNOMED CT (controlled vocabulary only)

Methodology : NeOn (Scenario 4: ontology networks) + LOT cycle;
  competency-question-driven; Ontology Design Patterns (participation,
  event, role, plan); the three ASCA domain classes are pairwise
  disjoint.

Population  : LLM-assisted (Claude, Anthropic) under human expert
  adjudication and a HermiT consistency gate. Every term carries
  scon:populationProvenance with one of:
    author-vocabulary (BFO Continuants and Occurrents inventory, 2026)
    reused-vocabulary / reused-external (source named)
    llm-proposed-human-approved (Claude, Anthropic) - pending
      expert adjudication
  LLM-derived content is committed only after human approval and a
  consistency check.

Profile     : OWL 2 DL (SROIQ). Reasoner: HermiT (hypertableau).

---------------------------------------------------------------------
4. REQUIREMENTS AND DOCUMENTATION
---------------------------------------------------------------------
The Ontology Requirements Specification Document (ORSD), prepared
with the NeOn ORSD template, records purpose, scope, implementation
language, 7 end-user groups, 8 intended uses, 10 non-functional
requirements, the 36 competency questions as functional requirements,
and a pre-glossary with term frequencies computed from the CQ texts.
See docs/ORSD (Word/Markdown) in the repository.

The 36 CQs are ALSO embedded in the OWL file as
scon:competencyQuestion annotations (A-CQ1..12 academic, C-CQ1..12
career, S-CQ1..12 social-emotional), so requirements travel with the
artefact and remain executable as acceptance tests.

---------------------------------------------------------------------
5. LOADING, REASONING, AND TESTING
---------------------------------------------------------------------
1) Open scon-ontology-1.owl in Protege 5.6+.
2) Reasoner -> HermiT -> Start reasoner. Expected: CONSISTENT.
   Illustrative inferences from the seed ABox:
     - isAddressedBy(issue_i1, intervention_int1) via owl:inverseOf
     - intervention_int1 classified under Intervention and
       obo:OBI_0000011 via the subsumption chain
     - risk_chronicAbsence_S1 classified under RiskIndicator
3) DL Query tab (class expressions), e.g.:
     Intervention and (addresses some StudentIssue)
     Student and (hasRiskIndicator some ChronicAbsence)
4) SPARQL: use the SNAP SPARQL QUERY tab (Window -> Tabs), which
   queries the INFERRED model while the reasoner runs. The plain
   "SPARQL Query" tab sees only asserted triples. Example:

     PREFIX scon: <http://www.semanticweb.org/bakariwie/ontologies/2026/6/scon-ontology-1#>
     SELECT ?intervention WHERE {
       scon:issue_i1 scon:isAddressedBy ?intervention }

   (Returns intervention_int1 only under the reasoner - a direct
   demonstration of inference.) A fuller reasoning-test query pack is
   provided in competency-questions/ in the repository.

---------------------------------------------------------------------
6. REPOSITORY LAYOUT
---------------------------------------------------------------------
  scon-ontology/
  |-- scon-ontology-1.owl        canonical ontology (RDF/XML)
  |-- README.txt                 this file
  |-- docs/                      ORSD; WIDOCO documentation (Pages)
  |-- competency-questions/      CQ1-36 with DL/SPARQL formalisations
  |-- population/                LLM candidate batches + adjudication
  |                              logs (per the consistency-gate
  |                              workflow)
  `-- releases/                  tagged versions (semantic versioning)

Note on the IRI: the semanticweb.org IRI above is SCON's stable
IDENTIFIER; this repository is its authoritative LOCATION. A
resolvable redirect (e.g., https://w3id.org/scon) can be added later
without changing the identifier.

---------------------------------------------------------------------
7. GOVERNANCE AND EVOLUTION
---------------------------------------------------------------------
Semantic versioning with a versionIRI per release; incremental,
consistency-preserving updates (an axiom is committed only if
adjudicated and the knowledge base remains consistent); adjudication
decisions logged under population/ for traceability; per-release
evaluation with HermiT (consistency, classification), OOPS!
(pitfalls), FOOPS! (FAIR), and CQ pass/fail testing. Instance-level
student data in all published artefacts are de-identified; consent
and confidentiality are modelled as first-class entities.

---------------------------------------------------------------------
8. CITING SCON
---------------------------------------------------------------------
Please cite the ontology as:
  Bakariwie, A., Weyori, B. A., & Afriyie, Y. (2026). SCON: School
  Counselling Ontology Network (Version 1.0.0) [OWL ontology].
  https://github.com/bakariwie/scon-ontology

And the associated systematic review as:
  Bakariwie, A., Weyori, B. A., & Afriyie, Y. (in press).
  Ontology-based knowledge representation for school counselling:
  A systematic literature review of ontology artefacts and semantic
  web technologies. Discover Artificial Intelligence. Advance online
  publication.

---------------------------------------------------------------------
9. ACKNOWLEDGEMENT OF AI ASSISTANCE
---------------------------------------------------------------------
The generative AI tool Claude (Anthropic) assisted in vocabulary
organisation, candidate-axiom generation, and documentation, under
the human adjudication and HermiT consistency-gate workflow described
above. All committed content is the responsibility of the authors.

=====================================================================
 Last updated: July 2026 - SCON v1.0.0
=====================================================================

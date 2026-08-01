# Synthetic Validation Dataset (v2)

`scon-synthetic-abox.ttl` is a fully synthetic, de-identified ABox for validating
SCON under conditions resembling real use. It contains **18,236 individuals**
built around **1,000 students**: 500 pre-tertiary students across Grades 9 to 12,
and 500 tertiary Computer Science students across Levels 100 to 400.

No real or identifiable person is represented. Every name, score, income figure and
screening result is generated from a fixed random seed, so the dataset is reproducible
bit for bit and contains nothing that could be traced to a living individual.

## Contents

| Layer | Individuals |
|---|---|
| Students (pre-tertiary / tertiary) | 500 / 500 |
| Financial need assessments | 1,001 |
| Financial aid awards (scholarship / work-study / loan) | 717 |
| Emotional intelligence administrations (Wong–Law) | 722 |
| Personality profiles (IPIP Big Five) | 754 |
| Suicide-risk screenings (C-SSRS ordinal) | 120 |
| Counselling sessions | 1,486 |
| Academic advising sessions | 895 |
| Emotion observations forming trajectories | 1,107 |
| Discipline incidents | 504 |
| Referrals | 412 |
| Capstone projects | 125 |
| Technology-sector internships | 242 |

## Controlled vocabulary

The dataset refers to the controlled-vocabulary individuals **declared in the ontology
itself**, not to names of its own: `riskLevel_low`, `riskLevel_moderate` and
`riskLevel_high` for `hasRiskLevel`; `tier1_universal`, `tier2_targeted` and
`tier3_intensive` for `assignedTier`; and `domain_academic`, `domain_career` and
`domain_socialEmotional` for `targetsDomain`. Load the ontology before the data, or
Protégé cannot resolve them.


## Loading it

Open the SCON ontology in Protégé and add `the ontology file`, then add
this file the same way. Protégé has **no Import item in its File menu**: instead, go to the **Active Ontology** tab, find the **Ontology imports** panel, and click the **⊕** button beside **Direct Imports**, choosing *"Import an ontology contained in a specific file"*.

Do **not** use **File > Open** for a data file or a module. File > Open replaces whatever
is in the editor, so it discards the SCON core and saving from that window writes out only
the data. That is the single most common way an OWL release gets destroyed.

Then start HermiT and run the queries in `competency-questions/sparql/`.

## Designed-in validation targets

The data are not random noise. Specific situations are planted so that reasoning has
something to prove:

- students carrying high-risk indicators, so the `hasStudentRiskLevel` property chain
  fires and the reasoner populates `HighRiskStudent`;
- students with attendance below the threshold, so `ChronicallyAbsentStudent` is
  non-empty;
- a student holding two academic interventions that address the same issue, so duplicate
  detection returns a result;
- students in milestone grades and levels who deliberately lack a postsecondary or career
  plan, so the closing-the-gap query returns a real target group;
- suicide-risk screenings above the published C-SSRS threshold, each escalating
  automatically to a safety-planning protocol individual;
- tertiary students carrying self-consent conditions, exercising the distinction between
  guardian consent and adult self-consent.

## Ethics

The dataset exists precisely so that SCON can be validated without touching real
counselling records. Counselling data are confidential, consent for secondary use is
rarely obtainable, and releasing instance data would defeat the safeguarding purpose the
ontology exists to serve. Contributors must never replace or supplement this file with
operational data.

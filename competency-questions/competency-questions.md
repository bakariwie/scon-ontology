# SCON Competency Questions

SCON is specified by **36 competency questions**, twelve in each of the three
developmental domains of the ASCA National Model. They are requirements and tests at the
same time: each is embedded in the ontology as a `competencyQuestion` annotation, and
each has an executable SPARQL query in [`sparql/`](sparql/).

## How to run them

1. Open the ontology in Protégé 5.6+. To add `the ontology file`, go to the **Active Ontology** tab, find the **Ontology imports** panel, and click the **⊕** button beside **Direct Imports**, choosing *"Import an ontology contained in a specific file"*. There is no Import item in the File menu.
2. Add `data/scon-synthetic-abox.ttl` the same way, so the queries have individuals to
   return. Never open a module or a data file with **File > Open**: that replaces the
   ontology in the editor instead of adding to it.
3. **Reasoner > HermiT > Start reasoner**, and wait for it to finish.
4. **Window > Tabs > Snap SPARQL Query**.
5. Run [`sparql/00_signature_check.rq`](sparql/00_signature_check.rq) first. It is a
   load check: several hundred rows means the ontology, the extension and the dataset
   are all live and the reasoner is running. No rows means something is not loaded.
   For the term-by-term audit, run
   `python tools/verify_release.py "scon-ontology-1.1.0.owl" --signature` instead;
   Protege's Snap SPARQL cannot express that check because it lacks `VALUES`.
6. Run any question's `.rq` file. Each carries the question text and the terms it uses
   in comments at the top.

Queries are answered over the **inferred** model, so derived classifications
(`AtRiskStudent`, `HighRiskStudent`, `ChronicallyAbsentStudent`,
`StudentReceivingTieredSupport`, `RecommendedIntervention`), inverse properties,
transitive closures, and the `hasStudentRiskLevel` property chain are all visible to
them. No aggregates and no property paths are used, because Snap SPARQL does not support
them.

Six defined classes carry the automatic classification: `AtRiskStudent`,
`ChronicallyAbsentStudent`, `HighRiskStudent`, `StudentReceivingTieredSupport`,
`RecommendedIntervention` and `KnowledgeGroundedCounsellingSystem`.

Every query uses the prefix:

```sparql
PREFIX scon: <http://www.semanticweb.org/bakariwie/ontologies/2026/6/scon-ontology-1#>
```

## Academic domain

**A-CQ1.** Which ASCA Mindsets and Behaviors standards in the academic domain are prioritised by the programme's annual student outcome goals for a given grade level?

**A-CQ2.** Which academic indicators, namely course grades, credit accrual, assessment results and attendance, flag a student for Tier 2 targeted support, and from which data sources is each derived?

**A-CQ3.** Which closing-the-gap action plan addresses an identified academic equity gap, and which students constitute its target group according to disaggregated achievement data?

**A-CQ4.** Which classroom lessons (Tier 1 instruction) address a given academic Mindsets and Behaviors standard, and in which grade levels are they delivered?

**A-CQ5.** Which learning-strategies behaviours (B-LS), such as time management, study skills and critical thinking, has a student demonstrated or not yet demonstrated?

**A-CQ6.** Which small-group interventions target low academic achievement, and what participation, Mindsets and Behaviors, and outcome data are recorded in their results reports?

**A-CQ7.** How does a student's academic record map to graduation requirements, promotion criteria and course prerequisites?

**A-CQ8.** Which appraisal and advisement activities support a student's course selection and academic goal setting within individual student planning?

**A-CQ9.** How is progress towards an annual student outcome goal in the academic domain measured across the sequence of lessons, groups and interventions delivered?

**A-CQ10.** Which self-management skills (B-SMS), such as perseverance and delayed gratification, are associated with a student's academic engagement?

**A-CQ11.** Which referrals to academic support services, such as tutoring or special-education evaluation, follow from an identified academic concern, and what is the escalation pathway?

**A-CQ12.** Which academic interventions are contra-indicated or duplicated within a student's current support plan, and how is this detected by the reasoner?

## Career domain

**C-CQ1.** Which career-development Mindsets and Behaviors standards are addressed by the programme's Tier 1 career lessons at each grade level?

**C-CQ2.** Which career assessments inform a student's postsecondary and career plan?

**C-CQ3.** Which career clusters and occupations align with a student's assessed interests, aptitudes and constraints?

**C-CQ4.** Which postsecondary plan exists for a student, and which appraisal and advisement sessions produced or revised it?

**C-CQ5.** Which work-based learning experiences has a student completed, and which standards do they evidence?

**C-CQ6.** How do a student's course selections map to a chosen career pathway and to its postsecondary entry requirements?

**C-CQ7.** Which students lack a documented postsecondary plan by a milestone grade, as targeted by a closing-the-gap action plan?

**C-CQ8.** Which career-planning interventions and resources are recommended for a student's developmental stage and identified needs?

**C-CQ9.** How is a student's progression along a career-guidance pathway monitored across grade-level transitions?

**C-CQ10.** Which college- and career-application milestones has a student completed or missed?

**C-CQ11.** Which career interventions demonstrate effectiveness through the outcome data of their results reports?

**C-CQ12.** Which employability behaviours, transferable across the Mindsets and Behaviors categories, evidence a student's career readiness?

## Social–emotional domain

**S-CQ1.** Which social/emotional Mindsets and Behaviors standards are prioritised by the annual student outcome goals, and for which student populations?

**S-CQ2.** Which behavioural and socio-emotional indicators, namely discipline referrals, screening results, self-report and teacher report, flag a student for Tier 2 or Tier 3 support?

**S-CQ3.** How is the severity or urgency of a socio-emotional risk classified to prioritise response, including activation of suicide-risk assessment protocols?

**S-CQ4.** Which short-term, small-group counselling interventions address an identified social/emotional concern, and what is their evidence base?

**S-CQ5.** Which safeguarding concerns trigger mandated reporting, and to which internal role or external agency is each referred?

**S-CQ6.** Which social-skills behaviours (B-SS), such as empathy, positive relationships and responsible decision making, has a student demonstrated across settings?

**S-CQ7.** Which consent conditions and confidentiality constraints govern access to, and disclosure of, a student's counselling record?

**S-CQ8.** Which crisis-response procedures apply to a given crisis type, and which institutional roles participate in the response?

**S-CQ9.** How are a student's emotion processes and behavioural observations documented across successive sessions as a developmental trajectory?

**S-CQ10.** Which referrals to community mental-health providers extend support beyond the short-term counselling remit of the school counsellor?

**S-CQ11.** How is the effectiveness of social/emotional interventions evidenced through participation, Mindsets and Behaviors, and outcome data?

**S-CQ12.** Which self-management interventions reduce discipline incidents for the target group of a closing-the-gap action plan?

## Validation status

All 36 questions execute against `data/scon-synthetic-abox.ttl` and return non-empty
answer sets. The questions that turn on inference rather than assertion, namely S-CQ3
(severity classification), C-CQ8 (recommended interventions) and A-CQ12 (duplicate
detection), are written against defined classes and the property chain, so a non-empty
answer is itself evidence that the reasoning layer is doing the work.

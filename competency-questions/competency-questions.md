# SCON Competency Questions — Formalisations (v1.1.0)

The 36 competency questions (CQs) that drive SCON, twelve per ASCA developmental
domain. Each CQ is also embedded in the OWL file as a `scon:competencyQuestion`
annotation. A CQ **passes** when its DL-Query or SPARQL formalisation returns the
intended answer set under the HermiT reasoner.

**How to run.** In Protégé 5.6+: start the HermiT reasoner, then use the
**DL Query** tab for class expressions and the **Snap SPARQL Query** tab
(Window → Tabs) for SPARQL over the *inferred* model. All queries use the prefix:

```sparql
PREFIX scon: <http://www.semanticweb.org/bakariwie/ontologies/2026/6/scon-ontology-1#>
```

---

## 1. Academic domain

### Academic (A-CQ1–A-CQ12)

**A-CQ1.** Which ASCA Mindsets and Behaviors standards in the academic domain are prioritised by the programme's annual student outcome goals for a given grade level?

DL: `MindsetStandard and (addressesStandard some AcademicDevelopment)`; join to `AnnualStudentOutcomeGoal` via `addressesStandard`, filtered by `hasGradeLevel`.

**A-CQ2.** Which academic indicators - course grades, credit accrual, assessment results, and attendance - flag a student for Tier 2 targeted support, and from which data sources is each derived?

DL: `AtRiskStudent` (≡ `Student and (hasRiskIndicator some RiskIndicator)`), or `Student and (assignedTier value tier2_targeted)`; SPARQL joins `AcademicRiskIndicator` to its data source and `assignedTier`.

**A-CQ3.** Which closing-the-gap action plan addresses an identified academic equity gap, and which students constitute its target group according to disaggregated achievement data?

DL: `ClosingTheGapActionPlan and (concernsStudent some Student)`; SPARQL returns the plan and its target `Student` set.

**A-CQ4.** Which classroom lessons (Tier 1 instruction) address a given academic Mindsets and Behaviors standard, and in which grade levels are they delivered?

DL: `ClassroomInstruction and (addressesStandard some (MindsetsBehaviorsStandard and (partOf some AcademicDevelopment)))`; filter by `hasGradeLevel`.

**A-CQ5.** Which learning-strategies behaviours (B-LS), such as time management, study skills, and critical thinking, has a student demonstrated or not yet demonstrated?

DL: `LearningStrategiesBehaviour`; SPARQL joins `Student` to demonstrated/undemonstrated behaviours via `MindsetsBehaviorsData`.

**A-CQ6.** Which small-group interventions target low academic achievement, and what participation, Mindsets and Behaviors, and outcome data are recorded in their results reports?

DL: `SmallGroupCounselling and (addresses some AcademicUnderachievement)`; SPARQL returns `ParticipationData`, `MindsetsBehaviorsData`, `OutcomeData` in the `ResultsReport`.

**A-CQ7.** How does a student's academic record map to graduation requirements, promotion criteria, and course prerequisites?

SPARQL: join `AcademicRecord`/`AcademicTranscript` to `GraduationRequirement`, `PromotionCriterion`, and `CoursePrerequisite` (`prerequisiteOf`).

**A-CQ8.** Which appraisal and advisement activities support a student's course selection and academic goal setting within individual student planning?

DL: `AcademicAdvising and (hasGoal some CounsellingGoal)`; SPARQL links advisement to course selection and `PostsecondaryPlan`.

**A-CQ9.** How is progress towards an annual student outcome goal in the academic domain measured across the sequence of lessons, groups, and interventions delivered?

SPARQL: aggregate `OutcomeData` for an `AnnualStudentOutcomeGoal` across `ClassroomInstruction`, `SmallGroupCounselling`, and `Intervention` via `ProgressMonitoring`.

**A-CQ10.** Which self-management skills (B-SMS), such as perseverance and delayed gratification, are associated with a student's academic engagement?

DL: `SelfManagementSkillsBehaviour`; SPARQL correlates with `AcademicMotivation`/engagement for a `Student`.

**A-CQ11.** Which referrals to academic support services, such as tutoring or special-education evaluation, follow from an identified academic concern, and what is the escalation pathway?

DL: `Referral and (escalatesTo some ExternalAgency)` addressing an `AcademicIssue`; SPARQL returns the escalation pathway.

**A-CQ12.** Which academic interventions are contra-indicated or duplicated within a student's current support plan, and how is this detected by the reasoner?

DL (reasoner): members of `AcademicIntervention` in a `Student`'s `InterventionPlan`; duplication/contra-indication detected via disjointness and defined-class classification.


## 2. Career domain

### Career (C-CQ1–C-CQ12)

**C-CQ1.** Which career-development Mindsets and Behaviors standards are addressed by the programme's Tier 1 career lessons at each grade level?

DL: `MindsetStandard and (addressesStandard some CareerDevelopment)` delivered by `ClassroomInstruction`; filter by `hasGradeLevel`.

**C-CQ2.** Which career assessments, including interest inventories and aptitude and values assessments, inform a student's postsecondary and career plan?

DL: `CareerAssessment` (InterestInventory, AptitudeTest, ValuesAssessmentInstrument); SPARQL links via `basedOnAssessment` to `PostsecondaryPlan`.

**C-CQ3.** Which career clusters and occupations align with a student's assessed interests, aptitudes, and constraints?

DL: `Occupation and (belongsToCluster some CareerCluster)`; SPARQL aligns to a `Student`'s `CareerInterest`/`Aptitude` via `alignsWithOccupation`.

**C-CQ4.** Which postsecondary plan exists for a student, and which appraisal and advisement sessions produced or revised it?

DL: `PostsecondaryPlan`; SPARQL links to the `CareerGuidanceSession`/`AcademicAdvising` that produced or revised it.

**C-CQ5.** Which work-based learning experiences, such as job shadowing, internships, and service learning, has a student completed, and which standards do they evidence?

DL: `WorkBasedLearning` (Internship, JobShadowing, ServiceLearning, Apprenticeship, CooperativeEducation); SPARQL joins to evidenced standards.

**C-CQ6.** How do a student's course selections map to a chosen career pathway and to its postsecondary entry requirements?

SPARQL: map `Course` selections to a `CareerGuidancePathway` (`followsPathway`) and its `Qualification` entry requirements (`requiresSkill`).

**C-CQ7.** Which students lack a documented postsecondary plan by a milestone grade, as targeted by a closing-the-gap action plan?

DL: `Student and not (hasGoal some PostsecondaryPlan)` at a milestone `hasGradeLevel`; targeted by a `ClosingTheGapActionPlan`.

**C-CQ8.** Which career-planning resources and tools are recommended for a student's developmental stage and identified needs?

DL: `LearningResource`/`LabourMarketInformation` `recommendedFor` a `Student` at a developmental stage.

**C-CQ9.** How is a student's progression along a career-guidance pathway monitored across grade-level transitions?

SPARQL: progress toward a career `AnnualStudentOutcomeGoal` across delivered `CareerProcess` activities via `OutcomeData`.

**C-CQ10.** Which college- and career-application milestones, including applications, financial-aid submissions, and scholarship deadlines, has a student completed or missed?

DL: `Aptitude`/`Employability` dispositions of a `Student`; SPARQL correlates with `CareerDecisionMaking`.

**C-CQ11.** Which career interventions demonstrate effectiveness through the participation, Mindsets and Behaviors, and outcome data of their results reports?

DL: `Referral and (escalatesTo some ExternalAgency)` for a career need (e.g., `ScholarshipAgency`, `Company`).

**C-CQ12.** Which employability behaviours, transferable across the Mindsets and Behaviors categories, evidence a student's career readiness?

DL (reasoner): career interventions in a plan; duplication detected via classification and intervention-domain disjointness.


## 3. Social–emotional domain

### Social–emotional (S-CQ1–S-CQ12)

**S-CQ1.** Which social/emotional Mindsets and Behaviors standards are prioritised by the annual student outcome goals, and for which student populations?

DL: `MindsetStandard and (addressesStandard some SocialEmotionalDevelopment)`; SPARQL links to targeted `Student` populations.

**S-CQ2.** Which behavioural and socio-emotional indicators - discipline referrals, screening results, self-report, and teacher report - flag a student for Tier 2 or Tier 3 support?

DL: `AtRiskStudent`, or `Student and (hasRiskIndicator some SocioEmotionalRiskIndicator)`; SPARQL joins indicators (DisciplineReferral, ScreeningFlag) to their source and MTSS tier.

**S-CQ3.** How is the severity or urgency of a socio-emotional risk classified to prioritise response, including activation of suicide-risk assessment protocols?

DL: `HighRiskStudent` (≡ `Student and (hasRiskIndicator some (hasRiskLevel value riskLevel_high))`); imminent risk via `riskLevel_imminent` triggers `SuicideRiskAssessment`.

**S-CQ4.** Which short-term, small-group counselling interventions address an identified social/emotional concern, and what is their evidence base?

DL: `SmallGroupCounselling and (addresses some SocialEmotionalIssue)`; SPARQL returns each intervention's `hasEvidenceBase`.

**S-CQ5.** Which safeguarding concerns trigger mandated reporting, and to which internal role or external agency is each referred?

DL: `SafeguardingConcern and (mandatedReportTo some (ChildProtectionAgency or ExternalAgency))`.

**S-CQ6.** Which social-skills behaviours (B-SS), such as empathy, positive relationships, and responsible decision making, has a student demonstrated across settings?

DL: `SocialSkillsBehaviour`; SPARQL joins `Student` to demonstrated behaviours across settings.

**S-CQ7.** Which consent conditions and confidentiality constraints govern access to, and disclosure of, a student's counselling record?

SPARQL: join `CounsellingRecord` to its `ConsentCondition` (GuardianConsent/StudentSelfConsent) and `ConfidentialityConstraint` via `hasConsentCondition`/`documentedIn`.

**S-CQ8.** Which crisis-response procedures apply to a given crisis type, and which institutional roles participate in the response?

DL: `CrisisResponse` for a crisis type; SPARQL returns participating institutional roles (`conductedBy`).

**S-CQ9.** How are a student's emotion processes and behavioural observations documented across successive sessions as a developmental trajectory?

SPARQL: order a `Student`'s `EmotionEpisode` and `BehaviourObservationRecord` across sessions via `partOfTrajectory` (transitive) and `occursDuring`.

**S-CQ10.** Which referrals to community mental-health providers extend support beyond the short-term counselling remit of the school counsellor?

DL: `Referral and (escalatesTo some CommunityMentalHealthProvider)`.

**S-CQ11.** How is the effectiveness of social/emotional interventions evidenced through participation, Mindsets and Behaviors, and outcome data?

SPARQL: evidence intervention effectiveness via `ParticipationData`, `MindsetsBehaviorsData`, and `OutcomeData` in the `ResultsReport`.

**S-CQ12.** Which self-management interventions reduce discipline incidents for the target group of a closing-the-gap action plan?

DL: `SelfManagement` interventions; SPARQL correlates reduced `DisciplineReferral` counts for a `ClosingTheGapActionPlan` target group.


---

## 4. Defined-class queries (automatic classification)

The six defined classes let the reasoner *compute* the answers to the
highest-value risk and recommendation CQs. After starting HermiT, query each as a
class in the DL Query tab, or via SPARQL over the inferred model:

```sparql
SELECT ?s WHERE { ?s a scon:AtRiskStudent }                    # A-CQ2, S-CQ2
SELECT ?s WHERE { ?s a scon:ChronicallyAbsentStudent }         # A-CQ2
SELECT ?s WHERE { ?s a scon:HighRiskStudent }                  # S-CQ3
SELECT ?s WHERE { ?s a scon:StudentReceivingTieredSupport }    # A-CQ2, S-CQ2
SELECT ?i WHERE { ?i a scon:RecommendedIntervention }          # A-CQ6, S-CQ4
SELECT ?x WHERE { ?x a scon:KnowledgeGroundedCounsellingSystem }
```

## 5. Reasoning-demonstration queries (seed ABox)

These show inference beyond the asserted graph (run with HermiT started):

```sparql
# Inverse property: returns intervention_int1 only under the reasoner
SELECT ?x WHERE { scon:issue_i1 scon:isAddressedBy ?x }

# Property chain: returns riskLevel_high (derived, not asserted)
SELECT ?lvl WHERE { scon:student_S1 scon:hasStudentRiskLevel ?lvl }

# Recommendation pattern
SELECT ?i WHERE { ?i a scon:Intervention ; scon:recommendedFor scon:student_S1 }
```

Expected: under HermiT the exemplar `student_S1` classifies as `AtRiskStudent`,
`ChronicallyAbsentStudent`, `HighRiskStudent`, and `StudentReceivingTieredSupport`,
and `intervention_int1` as `RecommendedIntervention`.

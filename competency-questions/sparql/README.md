# SCON Competency Question SPARQL Suite

This folder holds one SPARQL query for each of the 36 SCON competency questions
(A-CQ1 to A-CQ12, C-CQ1 to C-CQ12, S-CQ1 to S-CQ12), plus a load check and an
offline validation harness. The queries are written for the Snap SPARQL
plugin in Protege, which answers them over the INFERRED model, so the derived
classifications (AtRiskStudent, HighRiskStudent, ChronicallyAbsentStudent,
StudentReceivingTieredSupport, RecommendedIntervention), the inverse
properties, the transitive closures of partOfTrajectory and precedes, and the
hasStudentRiskLevel property chain are all visible to them. No aggregates and
no property paths are used, because Snap SPARQL does not support them.

## How to run the queries in Protege (step by step)

1. Open Protege 5.6 and open your SCON ontology with **File > Open**.
2. Add the extension and the data. Protege has **no Import item in its File menu**.
   Go to the **Active Ontology** tab, find the **Ontology imports** panel, and click
   the **plus** button beside **Direct Imports**. Choose *"Import an ontology contained
   in a specific file"* and select `the ontology file`. Repeat for
   `data/scon-synthetic-abox.ttl`.
   Never use **File > Open** for a module or a data file: it replaces the ontology in
   the editor instead of adding to it, and saving afterwards discards the SCON core.
3. Start the reasoner: **Reasoner > HermiT**, then **Reasoner > Start reasoner**.
   Wait for it to finish. This step is required: the queries assume the
   inferred model.
4. Open the query tab: **Window > Tabs > Snap SPARQL Query**.
5. Open `00_signature_check.rq` in any text editor, copy everything, paste it into
   the Snap SPARQL text area, and click **Execute**. It should return several hundred
   rows. If it returns none, the reasoner is probably not started, or the dataset was
   not added.
6. Run any competency question the same way: open its `.rq` file, copy, paste, Execute.
   The comment lines at the top of each file restate the competency question and list
   every class and property the query touches.

## Snap SPARQL compatibility

Protege's Snap SPARQL tab implements a restricted subset of SPARQL 1.1. Queries in this
suite are written to stay inside it:

| Construct | Snap SPARQL | Used here |
|---|---|---|
| `VALUES` | **not supported** | avoided |
| Aggregates (`COUNT`, `GROUP BY`) | not supported | avoided |
| Property paths (`/`, `*`, `+`) | not supported | avoided |
| `FILTER NOT EXISTS` | unreliable | replaced with `MINUS` |
| `a` shorthand for `rdf:type` | unreliable | written as `rdf:type` |
| `OPTIONAL`, `FILTER`, `BIND`, `UNION`, `MINUS`, `ORDER BY` | supported | used |

If you paste a query and Protege reports *"Encountered X at line N column M"*, it has hit
a construct outside that subset. Check the line it names against the table above.

## Troubleshooting the two errors people actually hit

**"Encountered VALUES at line N column M"**
Snap SPARQL has no `VALUES` keyword. No query in this suite uses it any more. If you
see this, you are running an older copy of the suite; use the files in this folder.

**"Encountered scon:SomeName ... Expected one of: Variable, Individual name"**
Snap SPARQL resolves every prefixed name against the loaded ontology and checks its
type. This error means the name in object position is not known to be an *individual*,
either because it was never declared as one, or because your ontology also declares it
as a class (punning), which the parser will not accept in that position.

Two fixes, both already applied here. The dataset now declares its nine
controlled-vocabulary individuals explicitly (`LowRisk`, `ModerateRisk`, `HighRisk`,
`Tier1` to `Tier3`, and the three domain individuals). And the queries that used to
name a domain individual directly now match it by type instead, so they parse whether
or not the name is punned.

## Full signature check

The term-by-term check of every class and property the suite relies on cannot be done in
Snap SPARQL, because it needs `VALUES`. Run it offline instead:

    python tools/verify_release.py "scon-ontology-1.1.0.owl" --signature

It reads all 37 query files, extracts every `scon:` term they mention, and names any that
your ontology does not declare.

## Files

* `A-CQ1.rq` ... `S-CQ12.rq` — one query per competency question.
* `00_signature_check.rq` — run first; confirms the ontology, the extension and the
  dataset are all loaded and the reasoner is running.
* `make_queries.py` — regenerates all query files (edit this if you rename a
  term across the whole suite).
* `validate_queries.py` — offline harness that loads the synthetic ABox,
  applies the same inferences HermiT would (subclass closure, inverses,
  transitivity, the property chain, the six defined classes), and executes
  every query without needing Protege. Run `python validate_queries.py`; it
  prints a row count per query and fails loudly on any empty or unparseable
  query. Use it to re-check the suite after any change to the data or the
  queries. The authoritative execution environment remains Protege with
  HermiT and Snap SPARQL; the harness is a convenience for continuous
  checking and for reporting CQ execution results. Note that its materialiser
  is deliberately simple and does not scale to the full 1,000-student dataset;
  use it on a reduced extract, and use Protege for the full run.

## Reading the results

Each query is written so that its answer set is the direct answer to the
competency question. For example, A-CQ2 returns one row per (student,
indicator, source) where the student sits in Tier 2 and the indicator is an
academic risk indicator, and C-CQ7 returns exactly the students in a milestone
grade for whom no postsecondary plan exists, which is the target group of the
career closing-the-gap plan. Where a question asks about reasoner-derived
facts (S-CQ3 severity classification, C-CQ8 recommended interventions, A-CQ12
duplicate detection), the query deliberately uses the defined class or the
chain-derived property rather than any asserted fact, so a non-empty answer is
itself evidence that the inference layer is doing the work.

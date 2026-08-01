# Using SCON in Protégé

## Loading the ontology

Open `scon-ontology-1.1.0.owl` with **File > Open**. The file is self-contained: everything
the ontology declares is in it, so there is nothing further to import for the ontology
itself.

Confirm on the **Active Ontology** tab that the ontology IRI reads
`http://www.semanticweb.org/bakariwie/ontologies/2026/6/scon-ontology-1` and that the
Classes tab shows the full hierarchy.

## Adding the validation dataset

Protégé has **no Import item in its File menu**. Data and modules are added from the
**Active Ontology** tab instead.

1. Go to the **Active Ontology** tab.
2. Find the **Ontology imports** panel. In some builds it is a sub-tab of that same tab.
3. Under the heading **Direct Imports**, click the small **⊕ (plus)** button.
4. In the wizard, choose **"Import an ontology contained in a specific file"**, browse to
   `data/scon-synthetic-abox.ttl`, then **Continue** and **Finish**.

**Do not use File > Open for a data file.** File > Open replaces whatever is in the editor,
so it discards the ontology, and saving from that window writes out only the data. That is
the single most common way an OWL release is destroyed.

An import is a reference: the borrowed axioms stay in the other file and are not written
into yours when you save. That is what you want here, because the validation data should
stay separate from the ontology. If you ever do need a single combined file, use
**Refactor > Merge ontologies…** after importing.

## Reasoning

Choose **Reasoner > HermiT**, then **Reasoner > Start reasoner**. Wait for the status bar to
settle. Confirm that nothing in the class hierarchy turns red; red indicates an
unsatisfiable class.

With the reasoner running, the six defined classes populate themselves, the property chain
derives student risk levels, the inverse properties become visible in both directions, and
the transitive closures of `precedes` and `partOfTrajectory` are computed.

## Querying

Open **Window > Tabs > Snap SPARQL Query**. Copy the contents of any file from
`competency-questions/sparql/` into the query area and click **Execute**. Start with
`00_signature_check.rq`, which confirms that the ontology, the data and the reasoner are all
live.

Snap SPARQL implements a restricted grammar. It does not support `VALUES`, aggregates or
property paths, and it is unreliable with `FILTER NOT EXISTS` and the `a` shorthand. Every
query in the suite is written inside the subset it does support: `OPTIONAL`, `FILTER`,
`BIND`, `UNION`, `MINUS`, `ORDER BY` and explicit `rdf:type`.

The DL Query tab answers class expressions; the Snap SPARQL tab answers queries over the
inferred model, which is what the competency-question suite assumes.

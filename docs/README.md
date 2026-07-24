# SCON Documentation

This folder holds the human-facing documentation for SCON.

Expected contents:

- `ORSD/` — the Ontology Requirements Specification Document (Word/Markdown/PDF).
- `widoco/` — auto-generated HTML documentation (published via GitHub Pages).
  Generate with [WIDOCO](https://github.com/dgarijo/Widoco):
  `java -jar widoco.jar -ontFile ../scon-ontology-1.1.0.owl -outFolder widoco -rewriteAll -webVowl`
- `evaluation/` — quality and FAIR reports:
  - `oops-report.html` — [OOPS!](https://oops.linkeddata.es/) pitfall scan
  - `foops-report.html` — [FOOPS!](https://foops.linkeddata.es/) FAIR assessment
  - `robot-report.tsv` — ROBOT report (also produced by CI)
- `manuscript/` — the accompanying methodology-and-implementation manuscript.

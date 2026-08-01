#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_release.py — refuse to let a damaged ontology reach the repository.

Checks a SCON RDF/XML file for every structural feature the release must carry.
Prints a table and exits 0 only when nothing essential is missing.

Usage
    python verify_release.py "scon-ontology-1.1.0.owl"
    python verify_release.py "scon-ontology-1.1.0.owl" --signature

With --signature it additionally reads every .rq file in
competency-questions/sparql/ and reports any class or property the query suite
relies on that the ontology does not declare. The check runs here rather than in SPARQL because
Protege's Snap SPARQL parser does not support the VALUES keyword.
"""
import re, sys, os

CORE = [
    # label,                          pattern,                     minimum
    ('Ontology IRI declared',         r'<(?:owl:)?Ontology\s+rdf:about=', 1),
    ('Classes',                       r'<(?:owl:)?Class\s+rdf:about=',    400),
    ('Object properties',             r'<(?:owl:)?ObjectProperty\s+rdf:about=', 45),
    ('Data properties',               r'<(?:owl:)?DatatypeProperty\s+rdf:about=', 30),
    ('Subclass axioms',               r'rdfs:subClassOf',                 470),
    ('Textual definitions IAO:0000115', r'IAO_0000115',                   460),
    ('Defined classes (equivalentClass)', r'equivalentClass',             6),
    ('Property chain axiom',          r'propertyChainAxiom',              1),
    ('Disjointness axioms',           r'AllDisjointClasses|disjointWith', 8),
    ('Functional properties',         r'FunctionalProperty',              7),
    ('Transitive properties',         r'TransitiveProperty',              2),
    ('Inverse property axioms',       r'inverseOf',                       3),
    ('BFO reused terms',              r'BFO_0000',                        10),
    ('Competency question annotations', r'competencyQuestion',            36),
    ('External alignments (seeAlso)',  r'seeAlso',                        20),
]

VOCABULARY = [
    ('FinancialNeedAssessment',            r'#FinancialNeedAssessment\b', 1),
    ('FinancialRiskIndicator',             r'#FinancialRiskIndicator\b',  1),
    ('FinancialIntervention',              r'#FinancialIntervention\b',   1),
    ('EmotionalIntelligenceAssessment',    r'#EmotionalIntelligenceAssessment\b', 1),
    ('PersonalityAssessment',              r'#PersonalityAssessment\b',   1),
    ('SuicideRiskScreening',               r'#SuicideRiskScreening\b',    1),
    ('AcademicStanding',                   r'#AcademicStanding\b',        1),
    ('CapstoneProject',                    r'#CapstoneProject\b',         1),
    ('ResearchInterestArea',               r'#ResearchInterestArea\b',    1),
    ('hasIdeationLevel',                   r'#hasIdeationLevel\b',        1),
    ('hasUnmetNeedAmount',                 r'#hasUnmetNeedAmount\b',      1),
    ('hasOpennessScore',                   r'#hasOpennessScore\b',        1),
]

def signature_check(x, base):
    """Cross-check every scon: term used by the query suite against the ontology."""
    import glob
    qdir = os.path.join(base, 'competency-questions', 'sparql')
    if not os.path.isdir(qdir):
        qdir = os.path.join(base, '..', 'competency-questions', 'sparql')
    files = sorted(glob.glob(os.path.join(qdir, '*.rq')))
    if not files:
        print('Signature check skipped: no .rq files found near %s\n' % base)
        return 0
    classes, props = set(), set()
    for f in files:
        body = re.sub(r'^\s*#.*$', '', open(f, encoding='utf-8').read(), flags=re.M)
        for m in re.findall(r'scon:([A-Za-z_]\w*)', body):
            (classes if m[0].isupper() else props).add(m)
    declared = set(re.findall(r'rdf:about="[^"]*#([A-Za-z_]\w*)"', x))
    declared |= set(re.findall(r'rdf:resource="[^"]*#([A-Za-z_]\w*)"', x))
    miss_c = sorted(c for c in classes if c not in declared)
    miss_p = sorted(p for p in props if p not in declared)
    print('Query-suite signature (%d files, %d classes, %d properties)'
          % (len(files), len(classes), len(props)))
    print('-' * 62)
    if not miss_c and not miss_p:
        print('  every term used by the suite is present in the ontology\n')
        return 0
    for c in miss_c: print('  MISSING class     %s' % c)
    for p in miss_p: print('  MISSING property  %s' % p)
    print('\n  Fix by correcting the spelling in the query file, or by adding the')
    print('  term to the ontology. Queries touching a missing term return no rows.\n')
    return len(miss_c) + len(miss_p)

def run(path, do_sig=False):
    x = open(path, encoding='utf-8', errors='replace').read()
    print('\nFile: %s  (%.2f MB)\n' % (path, len(x) / 1e6))
    fails = 0
    for title, group in (('Structural features', CORE), ('Representative vocabulary', VOCABULARY)):
        print(title)
        print('-' * 62)
        for label, pat, minimum in group:
            n = len(re.findall(pat, x))
            ok = n >= minimum
            if not ok and title.startswith('Structural'):
                fails += 1
            flag = 'ok  ' if ok else ('MISSING' if title.startswith('Structural') else 'absent ')
            print('  %-38s %6d  (need %4d)  %s' % (label, n, minimum, flag))
        print()
    sig_missing = 0
    if do_sig:
        sig_missing = signature_check(x, os.path.dirname(os.path.abspath(path)) or '.')

    inds = len(re.findall(r'<(?:owl:)?NamedIndividual\s+rdf:about=', x))
    print('Named individuals present: %d  '
          '(0 if the validation dataset is kept as a separate file)\n' % inds)
    if fails:
        print('RESULT: FAIL — %d core feature(s) missing. Do NOT upload this file.' % fails)
        print('See docs/release-notes.md for what the release must contain.')
        return 1
    if sig_missing:
        print('RESULT: PASS with warnings — the release is structurally complete, but %d term(s) used by '
              'the query suite are absent.' % sig_missing)
        return 0
    print('RESULT: PASS — the release is structurally complete. Safe to upload.')
    return 0

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = [a for a in sys.argv[1:] if a.startswith('--')]
    if len(args) != 1:
        sys.exit(__doc__)
    sys.exit(run(args[0], do_sig='--signature' in flags))

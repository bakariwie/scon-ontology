#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ontology_report.py — measure the ontology and write docs/ontology-metrics.json.

Every count in the repository documentation comes from this script, so the
documentation cannot drift from the artefact. Run it after any change:

    python tools/ontology_report.py "scon-ontology-1.1.0.owl"
"""
import re, json, sys, os, collections

SC = 'http://www.semanticweb.org/bakariwie/ontologies/2026/6/scon-ontology-1#'

def measure(path):
    x = open(path, encoding='utf-8').read()
    u = {}
    for i, b in re.findall(r'<owl:Class rdf:about="([^"]+)">(.*?)</owl:Class>', x, re.S):
        if i.startswith(SC):
            u[i] = u.get(i, '') + b
    ext = {i for i, _ in re.findall(r'<owl:Class rdf:about="([^"]+)">(.*?)</owl:Class>',
                                    x, re.S) if not i.startswith(SC)}
    def scoped(tag):
        return len({m for m in re.findall(r'<owl:%s rdf:about="([^"]+)"' % tag, x)
                    if m.startswith(SC)})
    def total(tag):
        return len(set(re.findall(r'<owl:%s rdf:about="([^"]+)"' % tag, x)))
    def count(p): return len(re.findall(p, x))

    mods, prov = collections.Counter(), collections.Counter()
    for b in u.values():
        for v in re.findall(r'<scon:module[^>]*>([^<]+)<', b):
            mods[v] += 1
        for v in re.findall(r'<scon:populationProvenance[^>]*>([^<]+)<', b):
            prov['author' if v.startswith('author')
                 else 'llm' if v.startswith('llm') else 'reused'] += 1

    return {
        'version': re.search(r'<owl:versionInfo>([^<]*)<', x).group(1),
        'classes': len(u),
        'classes_with_definition': sum(1 for b in u.values() if 'IAO_0000115' in b),
        'defined_classes': sum(1 for b in u.values() if '<owl:equivalentClass' in b),
        'external_classes_reused': len(ext),
        'object_properties': scoped('ObjectProperty'),
        'object_properties_incl_reused': total('ObjectProperty'),
        'data_properties': scoped('DatatypeProperty'),
        'annotation_properties': total('AnnotationProperty'),
        'individuals': total('NamedIndividual'),
        'subclass_axioms': count(r'<rdfs:subClassOf'),
        'disjoint_groupings': count(r'<owl:AllDisjointClasses'),
        'all_different': count(r'<owl:AllDifferent'),
        'property_chains': count(r'<owl:propertyChainAxiom'),
        'inverse_axioms': count(r'<owl:inverseOf'),
        'functional_properties': count(r'#FunctionalProperty"'),
        'transitive_properties': count(r'#TransitiveProperty"'),
        'restrictions': count(r'<owl:Restriction'),
        'some_values_from': count(r'<owl:someValuesFrom'),
        'has_value': count(r'<owl:hasValue'),
        'competency_questions': count(r'<scon:competencyQuestion'),
        'labels': count(r'<rdfs:label'),
        'see_also': count(r'<rdfs:seeAlso'),
        'modules': dict(mods.most_common()),
        'module_count': len(mods),
        'provenance': dict(prov),
    }

if __name__ == '__main__':
    p = sys.argv[1] if len(sys.argv) > 1 else 'scon-ontology-1.1.0.owl'
    m = measure(p)
    out = os.path.join('docs', 'ontology-metrics.json')
    os.makedirs('docs', exist_ok=True)
    json.dump(m, open(out, 'w', encoding='utf-8'), indent=1)
    w = max(len(k) for k in m)
    for k, v in m.items():
        print('  %-*s %s' % (w, k, v))
    print('\nwritten to', out)

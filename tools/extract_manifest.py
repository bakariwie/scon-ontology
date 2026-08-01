#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_manifest.py — parse a SCON RDF/XML release into a complete, lossless
structured manifest (JSON). The manifest is the single source of truth from
which build_ontology.py regenerates the release, so the ontology can be rebuilt
from the ground up without any hand editing of XML.
"""
import re, json, sys, xml.etree.ElementTree as ET

RDF  = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
RDFS = 'http://www.w3.org/2000/01/rdf-schema#'
OWL  = 'http://www.w3.org/2002/07/owl#'
SCON = 'http://www.semanticweb.org/bakariwie/ontologies/2026/6/scon-ontology-1#'

def q(ns, t): return '{%s}%s' % (ns, t)
A_ABOUT = q(RDF, 'about'); A_RES = q(RDF, 'resource')
A_DT = q(RDF, 'datatype'); A_LANG = '{http://www.w3.org/XML/1998/namespace}lang'
A_NODEID = q(RDF, 'nodeID'); A_PARSE = q(RDF, 'parseType')

def main(path, out):
    tree = ET.parse(path); root = tree.getroot()

    manifest = {
        'ontology': {}, 'annotation_properties': [], 'object_properties': [],
        'data_properties': [], 'classes': [], 'individuals': [],
        'disjoint_groups': [], 'all_different': [], 'prefixes': {},
    }

    # namespace prefixes actually declared on the root element
    for k, v in re.findall(r'xmlns:([\w-]+)="([^"]+)"',
                           open(path, encoding='utf-8').read()[:2000]):
        manifest['prefixes'][k] = v

    def literal(el):
        d = {'value': (el.text or '')}
        if el.get(A_DT): d['datatype'] = el.get(A_DT)
        if el.get(A_LANG): d['lang'] = el.get(A_LANG)
        return d

    def annotations_of(el, skip):
        """Collect every child that is not structural, preserving order."""
        out = []
        for c in el:
            tag = c.tag
            if tag in skip: continue
            if c.get(A_RES) is not None:
                out.append({'p': tag, 'resource': c.get(A_RES)})
            elif len(c) == 0:
                out.append(dict({'p': tag}, **literal(c)))
        return out

    # ---------------- ontology header
    o = root.find(q(OWL, 'Ontology'))
    if o is not None:
        manifest['ontology'] = {
            'iri': o.get(A_ABOUT),
            'annotations': annotations_of(o, skip=set()),
        }

    # ---------------- properties
    for kind, key in ((q(OWL, 'AnnotationProperty'), 'annotation_properties'),
                      (q(OWL, 'ObjectProperty'), 'object_properties'),
                      (q(OWL, 'DatatypeProperty'), 'data_properties')):
        for el in root.findall(kind):
            iri = el.get(A_ABOUT)
            if iri is None: continue
            rec = {'iri': iri, 'types': [], 'sub_property_of': [], 'domain': [],
                   'range': [], 'inverse_of': [], 'chain': [], 'annotations': []}
            for c in el:
                if c.tag == q(RDF, 'type') and c.get(A_RES):
                    rec['types'].append(c.get(A_RES))
                elif c.tag == q(RDFS, 'subPropertyOf'):
                    if c.get(A_RES): rec['sub_property_of'].append(c.get(A_RES))
                    else:
                        # property chain lives inside a subPropertyOf/Collection
                        coll = c.find('.//' + q(RDF, 'Description'))
                        items = re.findall(r'rdf:resource="([^"]+)"',
                                           ET.tostring(c, encoding='unicode'))
                        rec['chain'] = items
                elif c.tag == q(RDFS, 'domain') and c.get(A_RES):
                    rec['domain'].append(c.get(A_RES))
                elif c.tag == q(RDFS, 'range') and c.get(A_RES):
                    rec['range'].append(c.get(A_RES))
                elif c.tag == q(OWL, 'inverseOf') and c.get(A_RES):
                    rec['inverse_of'].append(c.get(A_RES))
                else:
                    if c.get(A_RES) is not None:
                        rec['annotations'].append({'p': c.tag, 'resource': c.get(A_RES)})
                    elif len(c) == 0:
                        rec['annotations'].append(dict({'p': c.tag}, **literal(c)))
            manifest[key].append(rec)

    # ---------------- classes
    for el in root.findall(q(OWL, 'Class')):
        iri = el.get(A_ABOUT)
        if iri is None: continue
        rec = {'iri': iri, 'sub_class_of': [], 'restrictions': [],
               'equivalent_to': None, 'annotations': []}
        for c in el:
            if c.tag == q(RDFS, 'subClassOf'):
                if c.get(A_RES):
                    rec['sub_class_of'].append(c.get(A_RES))
                else:
                    r = c.find(q(OWL, 'Restriction'))
                    if r is not None:
                        onp = r.find(q(OWL, 'onProperty'))
                        svf = r.find(q(OWL, 'someValuesFrom'))
                        hv  = r.find(q(OWL, 'hasValue'))
                        rec['restrictions'].append({
                            'on_property': onp.get(A_RES) if onp is not None else None,
                            'some_values_from': svf.get(A_RES) if svf is not None else None,
                            'has_value': hv.get(A_RES) if hv is not None else None,
                        })
            elif c.tag == q(OWL, 'equivalentClass'):
                rec['equivalent_to'] = ET.tostring(c, encoding='unicode')
            elif c.get(A_RES) is not None:
                rec['annotations'].append({'p': c.tag, 'resource': c.get(A_RES)})
            elif len(c) == 0:
                rec['annotations'].append(dict({'p': c.tag}, **literal(c)))
        manifest['classes'].append(rec)

    # ---------------- individuals
    for el in root.findall(q(OWL, 'NamedIndividual')):
        iri = el.get(A_ABOUT)
        if iri is None: continue
        rec = {'iri': iri, 'types': [], 'object_facts': [], 'data_facts': [],
               'annotations': []}
        for c in el:
            if c.tag == q(RDF, 'type') and c.get(A_RES):
                rec['types'].append(c.get(A_RES))
            elif c.get(A_RES) is not None:
                rec['object_facts'].append({'p': c.tag, 'resource': c.get(A_RES)})
            elif len(c) == 0:
                (rec['annotations'] if c.tag.startswith('{'+RDFS) or 'IAO_' in c.tag
                 else rec['data_facts']).append(dict({'p': c.tag}, **literal(c)))
        manifest['individuals'].append(rec)

    # ---------------- disjointness and AllDifferent (kept as raw XML blocks)
    for el in root.findall(q(OWL, 'AllDisjointClasses')):
        manifest['disjoint_groups'].append(
            re.findall(r'rdf:about="([^"]+)"', ET.tostring(el, encoding='unicode')))
    for el in root.findall(q(OWL, 'AllDifferent')):
        manifest['all_different'].append(
            re.findall(r'rdf:about="([^"]+)"', ET.tostring(el, encoding='unicode')))

    json.dump(manifest, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    print('classes            %d' % len(manifest['classes']))
    print('object properties  %d' % len(manifest['object_properties']))
    print('data properties    %d' % len(manifest['data_properties']))
    print('annotation props   %d' % len(manifest['annotation_properties']))
    print('individuals        %d' % len(manifest['individuals']))
    print('disjoint groups    %d' % len(manifest['disjoint_groups']))
    print('all-different sets %d' % len(manifest['all_different']))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

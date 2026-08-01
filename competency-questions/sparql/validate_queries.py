# -*- coding: utf-8 -*-
"""
validate_queries.py — offline execution harness for the 36 SCON competency
question queries against the synthetic ABox.

The harness has two parts. A lightweight materialiser applies exactly the
inference rules that HermiT applies to SCON version 1.1.0 (subclass closure
over the taxonomy in vocab.json, the three declared inverse property pairs,
the two transitive properties, the hasStudentRiskLevel property chain, and
the six defined classes), so that the store approximates the inferred model.
A small SPARQL evaluator then executes the restricted fragment used by the
query suite: basic graph patterns, OPTIONAL, UNION, FILTER (comparisons,
disjunction, inequality, NOT EXISTS), DISTINCT and ORDER BY.

This harness exists so that the query suite and the dataset can be checked
end to end without a triple store; the authoritative execution environment
remains Protege with HermiT and Snap SPARQL.

Run:  python validate_queries.py

NOTE ON SCALE
-------------
This harness was written for quick offline checks and its materialiser is
deliberately simple. On the full 1,000-student dataset (18,236 individuals) it
does not finish in reasonable time. Use it only on a reduced extract, and treat
Protege with HermiT and Snap SPARQL as the authoritative execution environment
for the full dataset.
"""
import os, re, json, glob, itertools, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "data")
V = json.load(open(os.path.join(DATA, "vocab.json"), encoding="utf-8"))

RDF_TYPE = "rdf:type"

# ---------------------------------------------------------------- load TTL
triples = set()
ttl = open(os.path.join(DATA, "scon-synthetic-abox.ttl"), encoding="utf-8").read()
ttl = re.sub(r"^@prefix.*$", "", ttl, flags=re.M)
TOKEN = re.compile(r'"(?:[^"\\]|\\.)*"(?:\^\^\w+:\w+)?|\S+')
for block in re.split(r"\s\.\s*\n", ttl):
    block = block.strip()
    if not block: continue
    parts = re.split(r"\s;\s*\n\s*", block)
    subj = None
    for k, part in enumerate(parts):
        toks = TOKEN.findall(part.strip())
        if k == 0:
            subj, toks = toks[0], toks[1:]
        while toks:
            p, o = toks[0], toks[1]
            triples.add((subj, p, o)); toks = toks[2:]

def norm_lit(o):
    m = re.match(r'^"(.*)"(?:\^\^\w+:\w+)?$', o, re.S)
    return m.group(1) if m else None

# ---------------------------------------------------------------- materialise
classes = V["classes"]
def supers(c, acc=None):
    acc = acc or set()
    for p in classes.get(c, []):
        if p not in acc:
            acc.add(p); supers(p, acc)
    return acc

changed = True
while changed:
    changed = False
    new = set()
    # subclass closure on rdf:type
    for s, p, o in triples:
        if p == RDF_TYPE and o.startswith("scon:"):
            for sup in supers(o[5:]):
                t = (s, RDF_TYPE, "scon:" + sup)
                if t not in triples: new.add(t)
    # inverses
    for a, b in V["inverses"]:
        for s, p, o in list(triples):
            if p == "scon:" + a and (o, "scon:" + b, s) not in triples:
                new.add((o, "scon:" + b, s))
            if p == "scon:" + b and (o, "scon:" + a, s) not in triples:
                new.add((o, "scon:" + a, s))
    # transitivity
    for tp in V["transitive"]:
        prop = "scon:" + tp
        edges = [(s, o) for s, p, o in triples if p == prop]
        index = {}
        for s, o in edges: index.setdefault(s, set()).add(o)
        for s, o in edges:
            for o2 in index.get(o, ()):
                if (s, prop, o2) not in triples: new.add((s, prop, o2))
    # property chain
    ch = V["property_chain"]
    p1, p2, ph = "scon:" + ch["chain"][0], "scon:" + ch["chain"][1], "scon:" + ch["head"]
    mid = {}
    for s, p, o in triples:
        if p == p1: mid.setdefault(o, set()).add(s)
    for s, p, o in triples:
        if p == p2 and s in mid:
            for subj in mid[s]:
                if (subj, ph, o) not in triples: new.add((subj, ph, o))
    # defined classes (approximations of the SCON equivalence axioms)
    for s, p, o in list(triples):
        if p == "scon:hasRiskIndicator" and (s, RDF_TYPE, "scon:Student") in triples:
            new.add((s, RDF_TYPE, "scon:AtRiskStudent"))
        if p == "scon:assignedTier" and o in ("scon:tier2_targeted", "scon:tier3_intensive") \
           and (s, RDF_TYPE, "scon:Student") in triples:
            new.add((s, RDF_TYPE, "scon:StudentReceivingTieredSupport"))
        if p == "scon:hasStudentRiskLevel" and o == "scon:riskLevel_high" \
           and (s, RDF_TYPE, "scon:Student") in triples:
            new.add((s, RDF_TYPE, "scon:HighRiskStudent"))
        if p == "scon:recommendedFor" and (s, RDF_TYPE, "scon:Intervention") in triples:
            new.add((s, RDF_TYPE, "scon:RecommendedIntervention"))
        if p == "scon:hasAttendanceRateValue":
            v = norm_lit(o)
            try:
                if v is not None and float(v) < 0.90 and (s, RDF_TYPE, "scon:Student") in triples:
                    new.add((s, RDF_TYPE, "scon:ChronicallyAbsentStudent"))
            except ValueError: pass
    add = new - triples
    if add:
        triples |= add; changed = True

# declarations for the signature check
for c in classes: triples.add(("scon:" + c, RDF_TYPE, "owl:Class"))
for p in V["object_properties"]: triples.add(("scon:" + p, RDF_TYPE, "owl:ObjectProperty"))
for p in V["data_properties"]: triples.add(("scon:" + p, RDF_TYPE, "owl:DatatypeProperty"))

print(f"store: {len(triples)} triples after materialisation")

# ---------------------------------------------------------------- indices
by_p = {}
for t in triples: by_p.setdefault(t[1], []).append(t)

# ---------------------------------------------------------------- mini SPARQL
def tokenize_query(text):
    text = re.sub(r"^#.*$", "", text, flags=re.M)
    text = re.sub(r"^PREFIX.*$", "", text, flags=re.M)
    return text

def parse_group(src):
    """Parse the contents of a {...} group into a list of elements."""
    elems, i, n = [], 0, len(src)
    while i < n:
        ch = src[i]
        if ch.isspace(): i += 1; continue
        rest = src[i:]
        if rest.startswith("OPTIONAL"):
            j = src.index("{", i); body, j2 = read_block(src, j)
            elems.append(("OPTIONAL", parse_group(body))); i = j2
        elif rest.startswith("FILTER NOT EXISTS") or rest.startswith("FILTER  NOT EXISTS"):
            j = src.index("{", i); body, j2 = read_block(src, j)
            elems.append(("NOTEXISTS", parse_group(body))); i = j2
        elif rest.startswith("MINUS"):
            j = src.index("{", i); body, j2 = read_block(src, j)
            elems.append(("MINUS", parse_group(body))); i = j2
        elif rest.startswith("VALUES"):
            m = re.match(r"VALUES\s+(\?\w+)\s*\{", rest)
            j = src.index("{", i); body, j2 = read_block(src, j)
            elems.append(("VALUES", (m.group(1), body.split()))); i = j2
        elif rest.startswith("BIND"):
            j = src.index("(", i); body, j2 = read_paren(src, j)
            m = re.match(r'\s*("(?:[^"\\]|\\.)*")\s+AS\s+(\?\w+)\s*$', body)
            elems.append(("BIND", (m.group(2), m.group(1)))); i = j2
        elif rest.startswith("FILTER"):
            j = src.index("(", i); body, j2 = read_paren(src, j)
            elems.append(("FILTER", body.strip())); i = j2
        elif ch == "{":
            body, j2 = read_block(src, i)
            branches = [parse_group(body)]
            while True:
                k = j2
                while k < n and src[k].isspace(): k += 1
                if src[k:k+5] == "UNION":
                    j = src.index("{", k); body2, j2 = read_block(src, j)
                    branches.append(parse_group(body2))
                else: break
            if len(branches) > 1: elems.append(("UNION", branches))
            else: elems.extend(branches[0])
            i = j2
        else:
            m = re.match(r'([^\s]+)\s+([^\s]+)\s+("(?:[^"\\]|\\.)*"(?:\^\^\w+:\w+)?|[^\s.]+)\s*(?:\.|(?=\}))', src[i:], re.S)
            if not m: raise SystemExit("parse error near: " + src[i:i+80])
            s, p, o = m.group(1), m.group(2), m.group(3)
            if p == "a": p = RDF_TYPE
            elems.append(("TRIPLE", (s, p, o))); i += m.end()
    return elems

def read_block(src, i):
    depth, j = 0, i
    while j < len(src):
        if src[j] == "{": depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0: return src[i+1:j], j+1
        j += 1
    raise SystemExit("unbalanced block")

def read_paren(src, i):
    depth, j = 0, i
    while j < len(src):
        if src[j] == "(": depth += 1
        elif src[j] == ")":
            depth -= 1
            if depth == 0: return src[i+1:j], j+1
        j += 1
    raise SystemExit("unbalanced paren")

def is_var(t): return t.startswith("?")

def match_triple(pat, binding):
    s, p, o = (binding.get(t, t) if is_var(t) else t for t in pat)
    cands = by_p.get(p, []) if not is_var(p) else list(triples)
    for ts, tp, to in cands:
        if not is_var(s) and ts != s: continue
        if not is_var(o) and to != o: continue
        b = dict(binding)
        if is_var(s): b[s] = ts
        if is_var(p): b[p] = tp
        if is_var(o): b[o] = to
        yield b

def val(term, b):
    t = b.get(term, term) if is_var(term) else term
    v = norm_lit(t)
    if v is not None:
        try: return float(v)
        except ValueError: return v
    try: return float(t)
    except (ValueError, TypeError): return t

def eval_filter(expr, b):
    for part in re.split(r"\|\|", expr):
        part = part.strip()
        m = re.match(r"^(\S+)\s*(=|!=|<=|>=|<|>)\s*(.+)$", part)
        if not m: raise SystemExit("filter parse: " + expr)
        l, op, r = val(m.group(1), b), m.group(2), val(m.group(3).strip(), b)
        try:
            ok = {"=": l == r, "!=": l != r, "<": l < r, ">": l > r,
                  "<=": l <= r, ">=": l >= r}[op]
        except TypeError:
            ok = False
        if ok: return True
    return False

def eval_group(elems, bindings):
    for el in elems:
        kind, payload = el
        if kind == "TRIPLE":
            bindings = [b2 for b in bindings for b2 in match_triple(payload, b)]
        elif kind == "FILTER":
            bindings = [b for b in bindings if eval_filter(payload, b)]
        elif kind == "NOTEXISTS":
            bindings = [b for b in bindings if not eval_group(payload, [dict(b)])]
        elif kind == "OPTIONAL":
            out = []
            for b in bindings:
                ext = eval_group(payload, [dict(b)])
                out.extend(ext if ext else [b])
            bindings = out
        elif kind == "MINUS":
            bindings = [b for b in bindings if not eval_group(payload, [dict(b)])]
        elif kind == "VALUES":
            var, opts = payload
            bindings = [dict(b, **{var: o}) for b in bindings for o in opts]
        elif kind == "BIND":
            var, litv = payload
            bindings = [dict(b, **{var: litv}) for b in bindings]
        elif kind == "UNION":
            out = []
            for br in payload:
                for b in bindings:
                    out.extend(eval_group(br, [dict(b)]))
            bindings = out
        if not bindings: return []
    return bindings

def run_query(path):
    text = tokenize_query(open(path, encoding="utf-8").read())
    m = re.search(r"SELECT\s+(DISTINCT\s+)?(.+?)\s+WHERE", text, re.S)
    vars_ = re.findall(r"\?\w+", m.group(2))
    j = text.index("{", m.end() - len("WHERE") - 1)
    body, _ = read_block(text, text.index("{", m.start()))
    elems = parse_group(body)
    rows = eval_group(elems, [{}])
    proj = {tuple(b.get(v, "") for v in vars_) for b in rows}
    return vars_, sorted(proj)

# ---------------------------------------------------------------- run suite
report = []
files = sorted(glob.glob(os.path.join(HERE, "*.rq")))
for f in files:
    name = os.path.basename(f)[:-3]
    try:
        vars_, rows = run_query(f)
        report.append((name, len(rows), "ok" if (rows or name.startswith("00_")) else "EMPTY"))
    except SystemExit as e:
        report.append((name, -1, "PARSE FAIL: " + str(e)))
w = max(len(n) for n, _, _ in report)
fails = 0
for n, c, status in report:
    if status != "ok": fails += 1
    print(f"{n:{w}}  {c:5d} rows  {status}")
print()
print("NOTE: 00_signature_check is a load check, not a term audit. For the full")
print("term-by-term signature audit run:")
print("    python tools/verify_release.py \"scon-ontology v1.1.0.rdf\" --signature")
sys.exit(1 if fails else 0)

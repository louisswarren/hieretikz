from collections import defaultdict
import itertools

accumulate = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

def compute_adjacency(edges):
    d = defaultdict(lambda:())
    for key in edges:
        premise, conclusion = key
        d[premise] += (conclusion,)
    return d

class LongestPathDict(dict):
    def __init__(self, pairs):
        best_paths = defaultdict(lambda:())
        for dest, path in pairs:
            current_len = len(best_paths[dest]) or float('-inf')
            if current_len < len(path) :
                best_paths[dest] = path
        super().__init__(best_paths.items())

@accumulate(LongestPathDict)
def find_reachable(a, adjacency, ignore=set()):
    """Returns a dictionary of all nodes reachable from a, mapped to the paths
    taken to reach them."""
    yield a, ()
    for b in adjacency[a]:
        if b not in ignore:
            yield b, ((a, b),)
            from_b = find_reachable(b, adjacency, ignore | {a})
            for c, path in from_b.items():
                yield c, ((a,b),) + path

# a |--- b : a -> ... -> b
# a |-/- b : b -> ... -> c and a ||-/- c
#         OR d -> ... -> a and d ||-/- b
def find_relation(a, b, pf_adjacency, pf_rev_adjacency, cm_adjacency):
    """Returns pair (pp, spp), where at least one of pp and spp is None, and
        - pp is a path via proofs from a to b
        - spp is a path via proofs from either:
            - b to some formula c, for which there is a countermodel showing a
              does not imply c.
            - some formula d to a, for which there is a countermodel showing d
              does not imply b
    If both pp and spp are none, the relation is unknown."""
    a_b_path = find_reachable(a, pf_adjacency).get(b)
    if a_b_path:
        return a_b_path, None
    b_consequences = find_reachable(b, pf_adjacency)
    raise NotImplementedError("""
        Testing against cm_adjacency is not sufficient; we may know that a
        consequence of b is not implied by a for reasons other than a direct
        counter-model.
    """)
    for underivable in cm_adjacency[a]:
        if underivable in b_consequences:
            return None, b_consequences[underivable]
    a_causes = find_reachable(a, pf_rev_adjacency)
    for cause in a_causes:
        if b in cm_adjacency[cause]:
            return None, find_reachable(cause, pf_adjacency)[a]
    return None, None

@accumulate(set)
def find_weak_edges(formulae, pf_adjacency, pf_rev_adjacency, cm_adjacency):
    for a, b in itertools.permutations(formulae, 2):
        pf, cm = find_relation(a, b, pf_adjacency, pf_rev_adjacency, cm_adjacency)
        if pf is None and cm is None:
            yield (a, b)

@accumulate('\n'.join)
def make_tikz_nodes(formulae, formula_layout):
    fmt = r'\node ({}) at ({}, {}) {{{}}};'
    for j, row in enumerate(formula_layout):
        i = 0
        while i < len(row):
            for formula in formulae:
                tok = row[i:].split(' ')
                if tok and tok[0] == formula:
                    yield fmt.format(formula, i // 5, -j * 2, formula)
                    i += len(tok[0]) - 1
                    break
            i += 1

@accumulate('\n'.join)
def make_tikz_edges(formulae, strong_edges, weak_edges):
    drawn = set()
    fmt = r'\draw[{}] ({}) to node {{}} ({});'
    for a, b in strong_edges:
        if (b, a) in drawn:
            continue
        if (b, a) in strong_edges:
            yield fmt.format('<->', a, b)
        else:
            yield fmt.format('->', a, b)
        drawn.add((a, b))
    weak_drawn = set()
    for a, b in weak_edges:
        assert((a, b) not in drawn)
        if (b, a) in weak_drawn:
            continue
        if (b, a) in weak_edges:
            yield fmt.format('dashed, <->', a, b)
        else:
            if (b, a) in drawn:
                yield fmt.format('dashed, bend left=30, ->', a, b)
            else:
                yield fmt.format('dashed, ->', a, b)
        weak_drawn.add((a, b))

def make_tikz(formulae, formula_layout, proofs, counter_models):
    pf_adjacency = compute_adjacency(proofs)
    pf_rev_adjacency = compute_adjacency((q, p) for p, q in proofs)
    cm_adjacency = compute_adjacency(counter_models)
    weak_edges = find_weak_edges(formulae, pf_adjacency, pf_rev_adjacency, cm_adjacency)
    tikz_nodes = make_tikz_nodes(formulae, formula_layout)
    tikz_edges = make_tikz_edges(formulae, proofs, weak_edges)
    return tikz_nodes + tikz_edges

@accumulate('\\\\\n'.join)
def assist(formulae, formula_layout, proofs, counter_models):
    pf_adjacency = compute_adjacency(proofs)
    pf_rev_adjacency = compute_adjacency((q, p) for p, q in proofs)
    cm_adjacency = compute_adjacency(counter_models)
    weak_edges = find_weak_edges(formulae, pf_adjacency, pf_rev_adjacency, cm_adjacency)
    for e in weak_edges:
        yield '{:8s} $\implies$ {:8s}'.format(*e)

from collections import defaultdict
import itertools

accumulate = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

formulae = dne, lem, wlem, dp, he, dnsu, dnse, glpo, glpoa, gmp = \
    'dne', 'lem', 'wlem', 'dp', 'he', 'dnsu', 'dnse', 'glpo', 'glpoa', 'gmp'


_______ = None
formula_layout = [
[_______ , glpoa   , _______ , _______ , _______ , _______ , _______ ],
[_______ , _______ , _______ , lem     , _______ , glpo    , _______ ],
[_______ , _______ , _______ , _______ , _______ , _______ , _______ ],
[_______ , dp      , _______ , _______ , _______ , he      , _______ ],
[dnsu    , _______ , gmp     , _______ , _______ , _______ , dnse    ],
[_______ , _______ , _______ , wlem    , _______ , _______ , _______ ],
]

proofs = {
        (dne, glpoa): 'pft',
        (lem, wlem):  'pf0',
        (dp, wlem):   'pf1',
        (he, wlem):   'pf2',
        (glpoa, lem): 'pf3',
        (lem, glpo):  'pf4',
        (glpo, lem):  'pf5',
        (dp, gmp):    'pf6',
        (gmp, wlem):  'pf7',
        (dp, dnsu):   'pf8',
        (he, dnse):   'pf9',
        }

counter_models = {
        (glpoa, dne): 'cmt',
        (wlem, lem):  'cm0',
        (wlem, dp):   'cm1',
        (wlem, he):   'cm2',
        (lem, glpoa): 'cm3',
        (glpo, lem):  'cm4',
        (lem, glpo):  'cm5',
        (gmp, dp):    'cm6',
        (wlem, gmp):  'cm7',
        (dnsu, dp):   'cm8',
        (dnse, he):   'cm9',
        }

def compute_adjacency(edges):
    d = defaultdict(lambda:())
    for key in edges:
        premise, conclusion = key
        d[premise] += (conclusion,)
    return d

pf_adjacency = compute_adjacency(proofs)
cm_adjacency = compute_adjacency(counter_models)

class LongestPathDict(dict):
    def __init__(self, pairs):
        best_paths = defaultdict(lambda:())
        for dest, path in pairs:
            current_len = len(best_paths[dest]) or float('inf')
            if current_len < len(path) :
                best_paths[dest] = path
        super().__init__(best_paths.items())


@accumulate(LongestPathDict)
def find_derivable(a, ignore=set()):
    yield a, ()
    for b in pf_adjacency[a]:
        if b not in ignore:
            yield b, ((a, b),)
            from_b = find_derivable(b, ignore | {a})
            for c, path in from_b.items():
                yield c, ((a,b),) + path

# a |--- b : a -> ... -> b
# a |-/- b : b -> ... -> c and a ||-/- c
def find_relation(a, b):
    """Returns pair (pp, spp), where pp is a path via proofs from a to b, and
    spp is a path via proofs from b to some formula c, for which there is a
    countermodel showing a does not imply c. Either pp or spp will be None If
    both are none, the relation is unknown."""
    a_b_path = find_derivable(a).get(b)
    if a_b_path:
        return a_b_path, None
    b_consequences = find_derivable(b)
    for underivable in cm_adjacency[a]:
        if underivable in b_consequences:
            return None, b_consequences[underivable]
    return None, None



assert(find_relation(glpoa, wlem) == (((glpoa, lem), (lem, wlem)), None))
assert(find_relation(wlem, glpoa) == (None, ((glpoa, lem),)))
assert(find_relation(wlem, lem) == (None, ()))


def make_graph_edges(formulae):
    for a, b in itertools.combinations(formulae, 2):
        pf, cm = find_relation(a, b)
        rev_pf, rev_cm = find_relation(b, a)
        equivalent = pf and rev_pf
        weak_equivalent = (cm is not None) and (rev_cm is not None)
        implies, rev_implies = pf, rev_pf
        weak_implies, weak_rev_implies = cm is None, rev_cm is None
        if equivalent:
            yield (a, b), '<=>'
        elif implies:
            yield (a, b), '==>'
            if weak_rev_implies:
                yield (b, a), '-->'
        elif rev_implies:
            yield (b, a), '==>'
            if weak_implies:
                yield (a, b), '-->'
        elif weak_equivalent:
            yield (a, b), '<->'
        elif weak_implies:
            yield (a, b), '-->'
        elif weak_rev_implies:
            yield (b, a), '-->'


accumulate = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

formulae = dne, lem, wlem, dp, he, dnsu, dnse, glpo, glpoa, gmp = \
    'dne', 'lem', 'wlem', 'dp', 'he', 'dnsu', 'dnse', 'glpo', 'glpoa', 'gmp'

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
    d = {}
    for key in edges:
        premise, conclusion = key
        d[premise] = d.get(premise, tuple()) + (conclusion,)
    return d

pf_adjacency = compute_adjacency(proofs)
cm_adjacency = compute_adjacency(counter_models)


@accumulate(dict)
def find_derivable(a, ignore=set()):
    for b in pf_adjacency.get(a, []):
        if b not in ignore:
            yield b, (a, b)
            # Todo: return shortest
            from_b = find_derivable(b, ignore | {a})
            for c, path in from_b.items():
                yield c, (a,) + path

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
    for underivable in cm_adjacency.get(a, []):
        if underivable in b_consequences:
            # Todo: return shortest
            return None, b_consequences[underivable]
    return None, None
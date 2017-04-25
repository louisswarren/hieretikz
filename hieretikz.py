accumulate = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

formulae = lem, wlem, dp, he, dnsu, dnse, glpo, glpoa, gmp = \
    'lem', 'wlem', 'dp', 'he', 'dnsu', 'dnse', 'glpo', 'glpoa', 'gmp'

proofs = {
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
def find_reachable(a, adjacency, ignore=set()):
    for b in adjacency.get(a, []):
        if b not in ignore:
            yield b, (a, b)
            from_b = find_reachable(b, ignore | {a})
            for c, path in from_b.items():
                yield c, (a,) + path

def find_provable(a):
    return find_path(a, pf_adjacency)

def find_disprovable(a):
    return find_path(a, cm_adjacency)

def find_relation(a, b):
    """Returns triple (pp, spm, pcm), where pp is a path via proofs from a to
    b, where spp is a path via proofs from a to some formula c, and pcm is a
    path of countermodels from b to c. Either pp will be None or spm and pcm
    will be None.  If all are none, the relation is unknown."""
    from_a = find_reachable(a)
    if b in from_a:
        return from_a[b], None, None
    from_b = find_reachable(b)
    if not from_a ^ from_b:
        return None, None, None


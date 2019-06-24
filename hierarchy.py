import itertools

_compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

def downward_closure_paths(paths, edges):
    found = {head: ((*tails, head), *(paths[t] for t in tails if paths[t]))
             for *tails, head in edges if all(t in paths for t in tails)}
    if all(v in paths for v in found):
        return paths
    found.update(paths)
    return downward_closure_paths(found, edges)

_downward_closure_cache = {}
def downward_closure(vertices, edges):
    '''Find the downward closure of a set of vertices.

    Returns a dictionary mapping each vertex in the downward closure to the
    shortest tree path to that vertex. A tree path has the form

        ((t1, ..., tn, d), treepath(vertices, t1), ..., treepath(vertices, tn))

    where d is the vertex corresponding to the path, (t1, ..., tn, d) is
    the last multiedge in the path, and treepath(vertex, tk) is a tree path
    from the supplied vertex to the tk.'''
    key = vertices, edges
    if key not in _downward_closure_cache:
        val = downward_closure_paths({v: () for v in vertices}, edges)
        _downward_closure_cache[key] = val
    return _downward_closure_cache[key]

@_compose(list)
def completed_separations(separations, vertices, edges):
    '''Complete separations by adding all implicitly-separated vertices.'''
    vertex_closures = {v: downward_closure(frozenset({v}), edges)
                       for v in vertices}
    for *name, low, high in separations:
        closed_low = downward_closure(low, edges)
        closed_high = {v: vertex_closures[v][h] for v in vertices for h in high
                       if h in vertex_closures[v]}
        yield (*name, closed_low, closed_high)

def is_superior(generation, child, edges):
    return downward_closure(generation, edges).get(child, False)

def is_separated(tails, head, completed_separations):
    for *name, lower, upper in completed_separations:
        if head in upper and all(t in lower for t in tails):
            return (name[0] if name else ''), (lower[t] for t in tails), upper[head]
    return False

@_compose(frozenset)
def find_possible_connections(vertices, edges, separations, free=(), order=1):
    '''Find edges which can be added to the hierarchy.

    An edge can be added if it does not connect any separated vertices.
    Searches only for edges with order-many tails. Vertices listed in free do
    not count towards the number of tails.
    '''
    # Precompute downward closures of lower tiers, for efficiency
    completed = completed_separations(separations, vertices, frozenset(edges))
    for r in range(1, order + 1):
        for tails in itertools.combinations(vertices, r):
            for head in vertices:
                premise = frozenset({*free, *tails})
                if is_superior(premise, head, frozenset(edges)) is not False:
                    continue
                elif is_separated(premise, head, completed):
                    continue
                else:
                    yield (*tails, *free, head)


def is_redundant_edge(edge, edges):
    '''Give alternate path if one exists.'''
    *tails, head = edge
    return any(is_superior(a, head, frozenset(edges)) is not False
               for r in range(1, len(tails) + 1)
               for a in itertools.combinations(tails, r))

@_compose(tuple)
def evaluate_possible_edge(edge, vertices, edges, separations, free=(), order=1):
    '''Find the value of knowing about the existence of an edge.

    Returns a tuple, giving the number of possible connections if the edge
    exists, and the number if the edge doesn't exist.'''
    ne = edges | {edge}
    *tails, head = edge
    ns = separations + [(None, frozenset({*tails}), frozenset({head}))]
    yield len(find_possible_connections(vertices, ne, separations, free, order))
    yield len(find_possible_connections(vertices, edges, ns, free, order))

@_compose(dict)
def find_evaluated_connections(vertices, edges, separations, free=(), order=1):
    '''Find all new consistent connecting edges and their evaluations.

    Finds all edges that would connect currently disconnected vertices, and
    that can be added without connecting any pairs in disconnections. The
    evaluations of the edges are given by evaluate_possible_edge.'''
    current = len(find_possible_connections(vertices, edges, separations,
                                            free, order))
    conns = find_possible_connections(vertices, edges, separations, free, order)
    for edge in conns:
        ev = evaluate_possible_edge(edge, vertices, edges, separations,
                                    free, order)
        yield edge, (current - ev[0], current - ev[1])

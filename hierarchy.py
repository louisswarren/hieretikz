import itertools

compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

def downward_closure_paths(paths, edges):
    found = {head: ((*tails, head), *(paths[t] for t in tails if paths[t]))
             for *tails, head in edges if all(t in paths for t in tails)}
    if all(v in paths for v in found):
        return paths
    found.update(paths)
    return downward_closure_paths(found, edges)

def downward_closure(vertices, edges):
    '''Find the downward closure of a set of vertices.

    Returns a dictionary mapping each vertex in the downward closure to the
    shortest tree path to that vertex. A tree path has the form

        ((t1, ..., tn, d), treepath(vertices, t1), ..., treepath(vertices, tn))

    where d is the vertex corresponding to the path, (t1, ..., tn, d) is
    the last multiedge in the path, and treepath(vertex, tk) is a tree path
    from the supplied vertex to the tk.'''
    return downward_closure_paths({v: () for v in vertices}, edges)

def is_subset_of_downward_closure(vertices, wertices, edges):
    '''Checks if vertices is a subset of the downward closure of wertices.

    Returns a (truthy) pathtree if it is, or False otherwise. Result is
    calculated lazily.'''
    raise NotImplementedError

def is_superior(vertices, wertices, edges):
    dc = downward_closure(vertices, edges)
    if wertices.issubset(frozenset(dc)):
        return tuple(dc[w] for w in wertices)
    else:
        return False

def is_separated(vertices, wertices, edges, separations):
    for low_tier, high_tier in separations:
        vpath = is_superior(low_tier, vertices, edges)
        if vpath is False:
            continue
        for high in high_tier:
            wpath = is_superior(wertices, frozenset({high}), edges)
            if wpath is not False:
                return vpath, wpath
    return False

def find_possible_connections(vertices, edges, separations, free=(), order=1):
    '''Find edges which can be added to the hierarchy.

    An edge can be added if it does not connect any separated vertices.
    Searches only for edges with order-many tails. Vertices listed in free do
    not count towards the number of tails.
    '''
    # Precompute downward closures of lower tiers, for efficiency
    pc_separations = [(downward_closure(lower, edges), upper)
                      for lower, upper in separations]
    return {(*tails, *free, head)
            for r in range(1, order + 1)
            for head in vertices
            for tails in itertools.combinations(vertices, r)
            if not is_superior({*free, *tails}, {head}, edges)
            if not is_separated({*free, *tails}, {head}, edges, pc_separations)}


def is_redundant_edge(edge, edges):
    '''Give alternate path if one exists.'''
    a, *t, b = edge
    return is_superior({a}, {b}, frozenset(edges))

def spanning_tree(edges, basis=set()):
    '''Find a spanning tree for a graph.'''
    for edge in sorted(edges):
        if is_redundant_edge(edge, (edges - {edge}) | basis):
            return spanning_tree(frozenset(edges) - {edge}, basis)
    return edges


def evaluate_possible_edge(edge, vertices, edges, models):
    '''Find the value of knowing about the existence of an edge.

    Returns a tuple, giving the number of possible connections eliminated if
    the edge exists, and the number eliminated if the edge doesn't exist.'''
    return 0, 0

def find_evaluated_connections(vertices, edges, models):
    '''Find all new consistent connecting edges and their evaluations.

    Finds all edges that would connect currently disconnected vertices, and
    that can be added without connecting any pairs in disconnections. The
    evaluations of the edges are given by evaluate_possible_edge.'''
    return {e: evaluate_possible_edge(e, vertices, edges, models)
            for e in find_possible_connections(vertices, edges, models)}

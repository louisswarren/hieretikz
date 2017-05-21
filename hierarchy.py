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
    Searches only for edges with up to order-many tails. Vertices listed in
    free do not count towards the number of tails.
    '''
    return {(*free, *tails, head)
            for r in range(1, order + 1)
            for head in vertices
            for tails in itertools.combinations(vertices, r)
            if not is_superior({*free, *tails}, {head}, edges)
            if not is_separated({*free, *tails}, {head}, edges, separations)}


if __name__ == '__main__':
    edges = frozenset((
        (1, 2, 3),
        (4, 5),
        (2, 4),
        (3, 5, 6),
    ))

    # edges represent the following hierarchy:
    #
    #   1   2
    #    \ / \
    #     v   \
    #     |    4
    #     3    |
    #      \   5
    #       \ /
    #        v
    #        |
    #        6
    #

    def str_edge(edge):
        *tails, head = edge
        return '{{{}}} -> {}'.format(', '.join(sorted(map(str, tails))), head)

    @compose('\n'.join)
    def str_pathtree(pathtree, level=0):
        if pathtree:
            edge, *successors = pathtree
            yield '\t' * level + str_edge(edge)
            yield from (str_pathtree(s, level + 1) for s in successors)


    models = [({3, 5}, {4})]
    assert(is_superior({1,2}, {6}, edges))
    assert(is_separated({5}, {2}, edges, models))

    models = [
            ({3, 4, 5, 6}, {1, 2}),
            ({3, 5, 6}, {1, 2, 4}),
            ({4, 5, 6}, {1, 2, 3}),
            ({6}, {1, 2, 3, 4, 5}),
            ({3}, {5}),
            ({5}, {3}),
    ]
    assert(is_separated({6}, {2}, edges, models))
    for con in sorted(find_possible_connections(range(1, 7), edges, models, (), 2)):
        print(str_edge(con))


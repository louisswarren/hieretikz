compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

def downward_closure_paths(paths, edges):
    found = {head: ((tails, head), *(paths[t] for t in tails if paths[t]))
             for tails, head in edges if all(t in paths for t in tails)}
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

def multiedgeset(*edge_tuples):
    return frozenset((frozenset(tails), head) for *tails, head in edge_tuples)

edges = multiedgeset(
    (1, 2, 3),
    (4, 5),
    (2, 4),
    (3, 5, 6),
)

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
    tails, head = edge
    return '{{{}}} -> {}'.format(', '.join(sorted(map(str, tails))), head)

@compose('\n'.join)
def str_pathtree(pathtree, level=0):
    if pathtree:
        edge, *successors = pathtree
        yield '\t' * level + str_edge(edge)
        yield from (str_pathtree(s, level + 1) for s in successors)


print("Using edges:")
for edge in sorted(edges):
    print(str_edge(edge))


dc = downward_closure(frozenset((1, 2)), edges)
for dest, pathtree in sorted(dc.items()):
    print('{}:'.format(dest))
    if pathtree:
        print(str_pathtree(pathtree, 1))

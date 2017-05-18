import itertools
compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

def downward_closure_paths(path, edges):
    found = {}


def downward_closure(supervertex, edges):
    return downward_closure_paths({supervertex: ()}, edges)


edges = [
    (1, 2, 3),
    (4, 5),
    (2, 4),
    (3, 5, 6),
]
'''
1   2
 \ / \
  v   \
  |    4
  3    |
   \   5
    \ /
     v
     |
     6
'''

def simple_upward_closure(vertices, flattened_edges):
    found = frozenset(a for (a, b) in flattened_edges if b in vertices)
    if found.issubset(vertices):
        return vertices
    return simple_upward_closure(found | vertices, flattened_edges)

def common_roots(vertices, flattened_edges):
    return frozenset.intersection(
            *(simple_upward_closure(frozenset((frozenset((v,)),)), flattened_edges) for v in vertices))



@compose(frozenset)
def flat_edges(edges):
    tail_vertices, head_vertices = [], []
    for *tails, head in edges:
        tail_vertices.append(frozenset(tails))
        head_vertices.append(frozenset((head,)))
    for tailset, headset in zip(tail_vertices, head_vertices):
        yield tailset, headset
        for vertexset in tail_vertices + head_vertices:
            if vertexset.issubset(tailset):
                yield tailset, vertexset

@compose(frozenset)
def all_edges(edges):
    flattened = flat_edges(edges)
    yield from flattened
    for a, b in flattened:
        if len(b) > 1:
            for root in common_roots(a, flattened):
                yield root, b
# NOT SUFFICIENT: DOES NOT GIVE {1,2} -> {3,4}
'''
We convert a multigraph (graph in which edges have multiple tails, and
connection is conjunctive) into a graph, where vertices correspond to sets of vertices in the multigraph. Conversion occurs in three stages:
(1) Flattening the edges
    - For each multiedge (t1, ..., tn, h) create an edge ({t1, ... tn}, {h})
    - For each occupiable superposition of vertices in the multigraph (i.e. sets
'''


for e in flat_edges(edges):
    print(e)

print("\n\n\n")
for e in all_edges(edges) - flat_edges(edges):
    print(e)
#assert(downward_closure({2}, edges) == {2: (), 4: ((2,4),), 5:

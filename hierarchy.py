compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

class Multiedge:
    def __init__(self, *vertices):
        *tails, self.head = vertices
        self.tails = frozenset(tails)

    def __eq__(self, other):
        return self.tails == other.tails and self.head == other.head

    def __hash__(self):
        return hash((self.tails, self.head))

    def __repr__(self):
        args_str = ', '.join(map(str, sorted(self.tails) + [self.head]))
        return 'Multiedge({})'.format(args_str)

    def __str__(self):
        tails_str = ', '.join(map(str, sorted(self.tails)))
        return '({}) -> {}'.format(tails_str, self.head)

    def __iter__(self):
        yield from self.tails
        yield self.head

class MultiedgeSet:
    def __init__(self, *edge_args):
        self.edges = frozenset(Multiedge(*edge_arg) for edge_arg in edge_args)

    def __iter__(self):
        return iter(self.edges)

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


@compose(dict)
def upward_closure(vertex, edges, visited=None):
    yield vertex, ()
    if not visited:
        visited = (vertex,)
    for *tails, head in edges:
        if head == vertex:
            for t in tails:
                if t not in visited:
                    for node, pathtree in upward_closure(t, edges, visited):
                        pass

edges = MultiedgeSet(
    (1, 2, 3),
    (4, 5),
    (2, 4),
    (3, 5, 6),
)
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

def print_path(path, level=0):
    print("Unpacking,", path)
    edge, *successors = path
    print('\t'*level + str(edge))
    for s in successors:
        print_path(s, level + 1)

print(downward_closure_paths({1: (), 2: ()}, edges))
import sys
sys.exit()
for v, v_path in (downward_closure_paths({1: ((1, 1),), 2: ((2, 2),)}, edges)).items():
    if v_path:
        print('{}:'.format(v))
        print_path(v_path)
    else:
        print('{}: trivial'.format(v))
print()
for v, v_path in (downward_closure_paths({2: ()}, edges)).items():
    if v_path:
        print('{}:'.format(v))
        print_path(v_path)
    else:
        print('{}: trivial'.format(v))

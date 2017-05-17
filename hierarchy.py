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

@compose(frozenset)
def multiedge_set(*edge_args):
    for edge_arg in edge_args:
        yield Multiedge(*edge_arg)


def transient_closure_paths(paths, edges):
    found = {head: ((*tails, head), *(paths[t] for t in tails if paths[t]))
             for *tails, head in edges if frozenset(tails).issubset(frozenset(paths))}
    if all(v in paths for v in found):
        return paths
    found.update(paths)
    return transient_closure_paths(found, edges)





edges = multiedge_set(
    (1, 2, 3),
    (4, 5),
    (2, 4),
    (3, 5, 6),
)

def print_path(path, level=0):
    print("Unpacking,", path)
    edge, *successors = path
    print('\t'*level + str(edge))
    for s in successors:
        print_path(s, level + 1)

print(transient_closure_paths({1: (), 2: ()}, edges))
import sys
sys.exit()
for v, v_path in (transient_closure_paths({1: ((1, 1),), 2: ((2, 2),)}, edges)).items():
    if v_path:
        print('{}:'.format(v))
        print_path(v_path)
    else:
        print('{}: trivial'.format(v))
print()
for v, v_path in (transient_closure_paths({2: ()}, edges)).items():
    if v_path:
        print('{}:'.format(v))
        print_path(v_path)
    else:
        print('{}: trivial'.format(v))

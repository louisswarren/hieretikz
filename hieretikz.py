import hierarchy
from collections import defaultdict
import itertools

accumulate = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

@accumulate('\n'.join)
def make_tikz_nodes(formulae, formula_layout):
    fmt = r'\node ({}) at ({}, {}) {{{}}};'
    for j, row in enumerate(formula_layout):
        i = 0
        while i < len(row):
            for formula in formulae:
                tok = row[i:].split(' ')
                if tok and tok[0] == formula:
                    yield fmt.format(formula, i // 5, -j * 2, formula)
                    i += len(tok[0]) - 1
                    break
            i += 1

@accumulate('\n'.join)
def make_tikz_edges(formulae, strong_edges, weak_edges):
    drawn = set()
    fmt = r'\draw[{}] ({}) to node {{}} ({});'
    for a, b in strong_edges:
        if (b, a) in drawn:
            continue
        if (b, a) in strong_edges:
            yield fmt.format('<->', a, b)
        else:
            yield fmt.format('->', a, b)
        drawn.add((a, b))
    weak_drawn = set()
    for a, b in weak_edges:
        assert((a, b) not in drawn)
        if (b, a) in weak_drawn:
            continue
        if (b, a) in weak_edges:
            yield fmt.format('dashed, <->', a, b)
        else:
            if (b, a) in drawn:
                yield fmt.format('dashed, bend left=30, ->', a, b)
            else:
                yield fmt.format('dashed, ->', a, b)
        weak_drawn.add((a, b))

def make_tikz(formulae, formula_layout, proofs, counter_models):
    weak_edges = hierarchy.find_possible_connections(formulae, proofs, counter_models)
    tikz_nodes = make_tikz_nodes(formulae, formula_layout)
    tikz_edges = make_tikz_edges(formulae, hierarchy.spanning_tree(set(proofs)), weak_edges)
    return tikz_nodes + tikz_edges

@accumulate('\\\\\n'.join)
def assist(formulae, formula_layout, proofs, counter_models):
    weak_edges = hierarchy.find_possible_connections(formulae, proofs, counter_models)
    for e in weak_edges:
        yield '{:8s} $\implies$ {:8s}'.format(*e)

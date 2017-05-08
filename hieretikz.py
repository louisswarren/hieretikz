from constructive_hierarchy import *

_compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

def all_separations(models):
    return {(holds, fails): cm for cm, fpair in models.items()
                               for holds in fpair[0]
                               for fails in fpair[1]}

@_compose('\n'.join)
def string_node_layout_to_tikz(formula_layout):
    formulae = formula_layout.split()
    fmt = r'\node ({}) at ({}, {}) {{{}}};'
    for row_num, row in enumerate(formula_layout.split('\n')):
        col_num = 0
        while col_num < len(row):
            if row[col_num].isspace():
                col_num += 1
            else:
                formula = formulae.pop(0)
                yield fmt.format(formula, col_num // 5, -row_num * 2, formula)
                col_num += len(formula)

def _generate_tikz_edges(edge_set, arrow_type='', avoid_overlap=()):
    if arrow_type:
        fmt = r'\draw[' + arrow_type + r', {}] ({}) to node {{}} ({});'
    else:
        fmt = r'\draw[{}] ({}) to node {{}} ({});'
    drawn = set()
    for a, b in edge_set:
        if (b, a) in drawn:
            continue
        elif (b, a) in edge_set:
            yield fmt.format('<->', a, b)
        elif (b, a) in avoid_overlap:
            yield fmt.format('bend left=30, ->', a, b)
        else:
            yield fmt.format('->', a, b)
        drawn.add((a, b))

@_compose('\n'.join)
def make_tikz_edges(strong_edges, weak_edges):
    yield from _generate_tikz_edges(spanning_tree(set(strong_edges)))
    yield from _generate_tikz_edges(weak_edges, 'dashed', strong_edges)

@_compose('\n'.join)
def make_tikz_diagram(formula_layout, strong_edges, weak_edges):
    yield r'\begin{tikzpicture}[line width=0.3mm, auto]'
    yield string_node_layout_to_tikz(formula_layout)
    yield make_tikz_edges(strong_edges, weak_edges)
    yield r'\end{tikzpicture}'

@_compose('\n'.join)
def make_tikz_questions(evaluated_weak_edges):
    yield r'\begin{multicols}{3} \noindent'
    order = lambda x: (min(x[1]), x[0])
    for edge, rank in sorted(evaluated_weak_edges.items(), key=order, reverse=True):
        yield r'{:8s} $\implies$ {:8s} \quad {}\\'.format(*edge, rank)
    yield r'\end{multicols}'

@_compose('\n'.join)
def hieretikz_document(formulae, formula_layout, proofs, models):
    evaluated_weak_edges = find_evaluated_connections(
            formulae, set(proofs), set(all_separations(models)))
    yield r'\documentclass{article}'
    yield r'\usepackage{tikz}'
    yield r'\usepackage{amsmath}'
    yield r'\usepackage{fullpage}'
    yield r'\usepackage{multicol}'
    yield r'\begin{document}'
    yield make_tikz_diagram(formula_layout, proofs, evaluated_weak_edges)
    yield r'\paragraph{}'
    yield r'It remains to investigate:'
    yield make_tikz_questions(evaluated_weak_edges)
    yield r'\end{document}'

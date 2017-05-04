from constructive_hierarchy import *

compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

@compose('\n'.join)
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

@compose('\n'.join)
def make_tikz_edges(strong_edges, weak_edges):
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
        elif (b, a) in drawn:
            yield fmt.format('dashed, bend left=30, ->', a, b)
        else:
            yield fmt.format('dashed, ->', a, b)
        weak_drawn.add((a, b))

@compose('\n'.join)
def make_tikz_diagram(formula_layout, strong_edges, weak_edges):
    yield r'\begin{tikzpicture}[line width=0.3mm, auto]'
    yield string_node_layout_to_tikz(formula_layout)
    yield make_tikz_edges(strong_edges, weak_edges)
    yield r'\end{tikzpicture}'

@compose('\\\\\n'.join)
def make_tikz_questions(evaluated_weak_edges):
    yield r'\begin{multicols}{3} \noindent'
    order = lambda x: sum(x[1])
    for edge, rank in sorted(evaluated_weak_edges.items(), key=order, reverse=True):
        yield '{:8s} $\implies$ {:8s} \quad {}'.format(*edge, rank)
    yield r'\end{multicols}'

@compose('\n'.join)
def hieretikz_document(formulae, formula_layout, proofs, counter_models):
    evaluated_weak_edges = find_evaluated_connections(
            formulae, set(proofs), set(counter_models))
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


from constructive_hierarchy import *

_compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

def all_separations(models):
    '''Find all logical separations indicated by a set of models.'''
    return {(holds, fails): cm for cm, fpair in models.items()
                               for holds in fpair[0]
                               for fails in fpair[1]}

@_compose('\n'.join)
def string_node_layout_to_tikz(formula_layout):
    '''Convert string diagram into tikz nodes.'''
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
    '''Generate tiks arrows for a set of directed edges.'''
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
    '''Generate the strong and weak tikz arrows for a tikz diagram.'''
    yield from _generate_tikz_edges(spanning_tree(set(strong_edges)))
    yield from _generate_tikz_edges(weak_edges, 'dashed', strong_edges)

@_compose('\n'.join)
def make_tikz_diagram(formula_layout, strong_edges, weak_edges):
    '''Generate a tikz diagram.'''
    yield r'\begin{tikzpicture}[line width=0.3mm, auto]'
    yield string_node_layout_to_tikz(formula_layout)
    yield make_tikz_edges(strong_edges, weak_edges)
    yield r'\end{tikzpicture}'

@_compose('\n'.join)
def make_questions(evaluated_weak_edges):
    '''Generate latex output for open questions.'''
    yield r'\begin{multicols}{3} \noindent'
    order = lambda x: (-min(x[1]), x[0])
    for edge, rank in sorted(evaluated_weak_edges.items(), key=order):
        yield r'{:8s} $\implies$ {:8s} \quad {}\\'.format(*edge, rank)
    yield r'\end{multicols}'

@_compose('\n'.join)
def hieretikz(formulae, formula_layout, proofs, models):
    '''Get hieretikz output.'''
    evaluated_weak_edges = find_evaluated_connections(
            formulae, set(proofs), models)
    drawable_nodes = formula_layout.split()
    drawable_proofs = {(a, b) for a, b in proofs
                             if a in drawable_nodes and b in drawable_nodes}
    drawable_weak = {(a, b) for a, b in evaluated_weak_edges
                             if a in drawable_nodes and b in drawable_nodes}
    yield make_tikz_diagram(formula_layout, drawable_proofs, drawable_weak)
    if evaluated_weak_edges:
        yield r'\paragraph{}'
        yield r'It remains to investigate:'
        yield make_questions(evaluated_weak_edges)

@_compose('\n'.join)
def hieretikz_document_wrap(tex):
    '''Generate the wrapping needed for making a complete hieretikz document.'''
    yield r'\documentclass{article}'
    yield r'\usepackage{tikz}'
    yield r'\usepackage{amsmath}'
    yield r'\usepackage{fullpage}'
    yield r'\usepackage{multicol}'
    yield r'\begin{document}'
    yield tex
    yield r'\end{document}'

@_compose('\n'.join)
def hieretikz_output_document(formulae, formula_layout, proofs, models):
    '''Get hieretikz output as a full document.'''
    tex = hieretikz(formulae, formula_layout, proofs, models)
    yield hieretikz_document_wrap(tex)

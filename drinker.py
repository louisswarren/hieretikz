import subprocess
from hierarchy import *
from tikzify import *

formulae = 'lem wlem dp he dnsu dnse glpo glpoa gmp wgmp dgp'.split()
globals().update({f: f for f in formulae})
efq = 'efq'


formula_layout = '''\
    glpoa
                              lem                 glpo
                dp                             he
                                    dgp
                     gmp
                   wgmp
    dnsu                                                dnse
                              wlem
'''
formula_strs = {f: f.upper() for f in formulae}
formula_strs[dnse] = R'DNS$\exists$'
formula_strs[dnsu] = R'DNS$\forall$'
formula_strs[glpoa] = "GLPO$'$"


unnamed_proofs = {
    (lem, wlem),
    (dp, wlem),
    (he, wlem),
    (lem, glpo),
    (glpo, lem),
    (glpoa, lem),
    (glpoa, glpo),
    (dp, dnsu),
    (glpoa, dnsu),
    (he, dnse),
    (gmp, dnse),
    (gmp, dnsu),
    (dp, gmp),
    (gmp, wlem),
    (dp, dgp),
    (he, dgp),
    (dgp, wlem),
    (gmp, wgmp),
    (glpoa, wgmp),
    (dp, lem, glpoa),
    (he, dnsu, gmp), #hen suffices ...
    (he, lem, glpo),
    (wgmp, dnsu),
    (dnsu, wgmp),
    (wgmp, dnse, gmp),
}
proofs = {p: '{}-{}'.format(*p) for p in unnamed_proofs}

named_models = {
    'dp-cm-lobot': (
        {he, lem, dgp, wlem, dnsu, dnse, glpo, glpoa, gmp},
        {dp},
    ),
    'dp-cm': (
        {efq, he, dgp, wlem},
        {dp, lem, dnsu, wgmp},
    ),
    'dp-cm-bottop': (
        {he, wlem, dgp},
        {dnsu},
    ),
    'he-cm-lobot': (
        {dp, lem, dgp, wlem, dnsu, dnse, glpo, glpoa, gmp},
        {he},
    ),
    'he-cm': (
        {efq, dgp, dp, wlem},
        {he, lem},
    ),
    'linear': (
        {efq, wlem, dgp},
        {dp, he, lem, dnse},
    ),
    'glpoa-cm': (
        {lem, wlem, dgp},
        {glpoa, dp, he, gmp, wgmp},
    ),
    'v-const-term': (
        {efq, dnsu, wgmp},
        {wlem, dgp},
    ),
    'dp-simple-cm-with-bot': (
        {lem, dgp, wlem},
        {dnsu, dp, he},
    ),
    'dnse-cm': (
        {efq, wlem, dgp, glpoa},
        {dnse, he},
    ),
    'v-const-term-lobot': (
        {glpoa, lem, gmp},
        {dgp},
    ),
    'diamond': (
        {efq, wlem, gmp},
        {dgp, lem},
    ),
    'const-term-two-world': (
        {efq, dp, he, wlem, dgp},
        {lem},
    ),
    'trivial-lobot': (
        {f for f in formulae if f is not efq},
        {efq},
    ),
}
models = {tuple(map(frozenset, v)): k for k, v in named_models.items()}

if __name__ == '__main__':
    possible_edges = find_possible_connections(formulae, proofs, models)
    minimal_diagram = TikzHierarchy(name_dict=formula_strs)
    minimal_diagram.add_string_node_layout(formula_layout)
    minimal_diagram.add_edges(spanning_tree(set(proofs)), color=False)
    minimal_diagram.add_edges(possible_edges, 'dashed')


    efq_diagram = TikzHierarchy(minimal_diagram)
    efq_proofs = {(lem, efq, f): 'classical' for f in formulae}
    efq_diagram.add_edges(spanning_tree(set(efq_proofs), set(proofs)), 'dotted')


    int_proofs = dict(proofs)
    int_models = {k: v for k, v in models.items() if efq in k[0]}
    int_proofs.update({(lem, f): 'classical' for f in formulae})
    int_possible_edges = find_possible_connections(
                         formulae, int_proofs, int_models)
    int_diagram = TikzHierarchy(name_dict=formula_strs)
    int_diagram.add_string_node_layout(formula_layout)
    int_diagram.add_edges(spanning_tree(set(int_proofs)), color=False)
    int_diagram.add_edges(int_possible_edges, 'dashed')


    two_possible_edges = find_evaluated_connections(
                             formulae, set(proofs), list(models), free=(), order=2)
    two_diagram = TikzHierarchy(name_dict=formula_strs)
    two_diagram.add_string_node_layout(formula_layout)
    two_diagram.add_edges(spanning_tree(set(proofs)), color=False)
    two_diagram.add_edges(set(two_possible_edges), 'dashed')


    tex = make_sections(
        ('Minimal Logic', minimal_diagram),
        ('Minimal Logic with EFQ links', efq_diagram),
        ('Intuitionistic Logic', int_diagram),
        ('Minimal Logic Two-premise Possibilities', two_diagram),
        ('Investigations ({})'.format(len(two_possible_edges)),
            make_columns(make_connections_list(two_possible_edges)), 1)
    )

    document = make_latex_document(tex)

    with open('drinker.tex', 'w') as f:
        f.write(document)
    subprocess.call(['pdflatex', 'drinker.tex'], stdout=subprocess.DEVNULL)
    #with open('backdrinker.tex', 'r') as f:
        #assert(f.read() == document)

import subprocess
from hierarchy import *
from tikzify import *

formulae = 'uds udsn lem wlem dp dpn he dnsu dnse glpon glpoa gmp mgmp dgp'.split()
globals().update({f: f for f in formulae})
efq = 'efq'


formula_layout = '''\
    glpoa
                              lem
                dp                             he
                                    dpn
                uds  gmp   mgmp     dgp
             udsn
            dnsu       glpon                    dnse
                              wlem
'''

formula_strs = {f: f.upper() for f in formulae}
formula_strs[dnse] = R'DNS$\exists$'
formula_strs[glpoa] = "GLPO$'$"
formula_strs[glpon] = R'GLPO$_\neg$'

wgmp = dnsu
glpo = lem
hen = dpn
formula_strs[dnsu] = R'DNS$\forall$,WGMP'
formula_strs[lem] = R'LEM,GLPO'
formula_strs[dpn] = R'DP$_\lnot$,HE$_\lnot$'


unnamed_proofs = {
    (lem, wlem),
    (dp, wlem), #This actually assumes multiple terms
    (he, wlem), #This actually assumes multiple terms
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
    (dnse, wlem),
    (glpoa, wgmp),
    (glpoa, dnse),
    (glpo, dnse),
    (dp, lem, glpoa),
    (hen, dnsu, gmp), #hen suffices ...
    (he, lem, glpo),
    (wgmp, dnsu),
    (dnsu, wgmp),
    (wgmp, dnse, gmp),
    (lem, gmp, glpoa),
    (dp, dpn),
    (he, hen),
    (dp, hen),
    (he, dpn),
    (dpn, hen),
    (hen, dpn),
    (dpn, wlem),
    (hen, wlem),
    (lem, glpon),
    (glpon, wlem),
    (glpo, dpn),
    (dp, uds),
    (lem, uds, glpoa),
    (uds, udsn),
    (gmp, udsn),
    (glpoa, mgmp),
    (mgmp, wlem),
}
proofs = {p: '{}-{}'.format(','.join(p[:-1]), p[-1]) for p in unnamed_proofs}

named_models = {
    'dp-cm': (
        {efq, he, dgp, wlem, glpon, uds},
        {dp, lem, dnsu, wgmp, mgmp},
    ),
    'dp-cm-lobot': (
        {he, lem, dpn, hen, dgp, wlem, dnsu, dnse, glpo, glpoa, glpon, gmp, uds},
        {dp},
    ),
    'he-cm': (
        {efq, dp, dgp, wlem, glpon, uds},
        {he, lem},
    ),
    'he-cm-lobot': (
        {dp, lem, dpn, hen, dgp, wlem, dnsu, dnse, glpo, glpoa, glpon, gmp, uds},
        {he},
    ),
    'linear-growing-terms': (
        {efq, wlem, dgp},
        {dp, he, lem, dnse, glpoa, uds},
    ),
    'two-world-constant-terms': (
        {efq, dp, he, wlem, dgp, uds},
        {lem},
    ),
    'two-world-growing-terms': (
        {efq, wlem, dgp, wgmp},
        {glpoa, dp, he, dpn, hen, gmp, dnse, glpon, uds},
    ),
    'two-world-growing-terms-lobot': (
        {gmp, glpoa},
        {uds},
    ),
    'two-world-growing-terms-with-bot': (
        {lem, wlem, dgp},
        {glpoa, dp, he, gmp, wgmp, uds, mgmp},
    ),
    'v-const-term': (
        {efq, dnsu, uds},
        {wlem, dgp, dnse},
    ),
    'v-const-term-lobot': (
        {glpoa, lem, dpn, hen, gmp, dnse, glpon, uds},
        {dgp},
    ),
    'diamond-constant-terms': (
        {efq, wlem, gmp, uds},
        {dgp, lem},
    ),
    'beth-width-two': (
        {lem, he, dp},
        set(),
    ),
    'trivial-lobot': (
        {f for f in formulae if f is not efq},
        {efq},
    ),
}
models = [(k, *map(frozenset, v)) for k, v in named_models.items()]


if __name__ == '__main__':
    possible_edges = find_evaluated_connections(formulae, set(proofs), list(models))
    minimal_diagram = TikzHierarchy(name_dict=formula_strs)
    minimal_diagram.add_string_node_layout(formula_layout)
    minimal_diagram.add_edges(spanning_tree(set(proofs)), color=False)
    minimal_diagram.add_edges(set(possible_edges), 'dashed')


    efq_diagram = TikzHierarchy(minimal_diagram)
    efq_proofs = {(lem, efq, f): 'classical' for f in formulae}
    efq_diagram.add_edges(spanning_tree(set(efq_proofs), set(proofs)), 'dotted')


    int_proofs = dict(proofs)
    int_models = {m for m in models if efq in m[1]}
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
        ('Investigations ({})'.format(len(possible_edges)),
            make_columns(make_connections_list(possible_edges)), 1),
        ('Minimal Logic with EFQ links', efq_diagram),
        ('Intuitionistic Logic', int_diagram),
        ('Minimal Logic Two-premise Possibilities', two_diagram),
        ('Investigations ({})'.format(len(two_possible_edges)),
            make_columns(make_connections_list(two_possible_edges)), 1),
    )

    document = make_latex_document(tex)

    with open('drinker.tex', 'w') as f:
        f.write(document)
    subprocess.call(['pdflatex', 'drinker.tex'], stdout=subprocess.DEVNULL)
    #with open('backdrinker.tex', 'r') as f:
    #    assert(f.read() == document)

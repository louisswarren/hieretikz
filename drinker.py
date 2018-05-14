import subprocess
from hierarchy import *
from tikzify import *

formulae = 'tt lem wlem dgp glpoa gmp dp he dnsu dnse ud'.split()
globals().update({f: f for f in formulae})
efq = 'efq'

globals().update({future: future for future in
 'dpn glpon mgmp glpon'.split()})

# These are actually equivalent. Condense them once investigations are complete.
glpo = lem
hen = dpn
wgmp = dnsu

formula_layout = '''\
    glpoa
                              lem
                dp                             he
                ud  gmp            dgp
            dnsu                                dnse
                              wlem
'''

formula_strs = {f: f.upper() for f in formulae}
formula_strs[dnse] = R'DNS$\exists$'
formula_strs[glpoa] = "GLPO$'$"
formula_strs[glpon] = R'GLPO$_\neg$'

formula_strs[dnsu] = R'DNS$\forall$,WGMP'
formula_strs[lem] = R'LEM,GLPO'
formula_strs[dpn] = R'DP$_\lnot$,HE$_\lnot$'


unnamed_proofs = {
    (lem, wlem),
    (dp, dpn),
    (he, hen),
    (gmp, wgmp),
    (dgp, wlem),
    (glpoa, lem),
    (glpoa, gmp),
    (dp, ud),
    (dp, gmp),
#    (dp, dnsu),
    (glpo, dpn),
    (he, dnse),
    (glpo, dnse),
    (gmp, dnse),
    (dpn, dnse),
#    (glpoa, wgmp),
    (dp, efq, tt, dgp),
    (he, efq, tt, dgp),
#    (dp, tt, wlem),
    (he, tt, wlem),
    (gmp, tt, wlem),
    (dp, lem, glpoa),
    (dnse, tt, wlem),
}

proofs = {p: '{}-{}'.format(','.join(p[:-1]), p[-1]) for p in unnamed_proofs}

named_models = {
    'dp-cm': (
        {tt, efq, he, dgp, wlem, glpon, ud},
        {dp, lem, dnsu, wgmp, mgmp},
    ),
    'dp-cm-lobot': (
        {tt, he, lem, dpn, hen, dgp, wlem, dnsu, dnse, glpo, glpoa, glpon, gmp, ud},
        {dp},
    ),
    'he-cm': (
        {tt, efq, dp, dgp, wlem, glpon, ud},
        {he, lem},
    ),
    'he-cm-lobot': (
        {tt, dp, lem, dpn, hen, dgp, wlem, dnsu, dnse, glpo, glpoa, glpon, gmp, ud},
        {he},
    ),
    'linear-growing-terms': (
        {tt, efq, wlem, dgp},
        {dp, he, lem, dnse, glpoa, ud},
    ),
    'two-world-constant-terms': (
        {tt, efq, dp, he, wlem, dgp, ud},
        {lem},
    ),
    'two-world-growing-terms': (
        {tt, efq, wlem, dgp, wgmp},
        {glpoa, dp, he, dpn, hen, gmp, dnse, glpon, ud},
    ),
    'two-world-growing-terms-lobot': (
        {tt, gmp, glpoa},
        {ud},
    ),
    'two-world-growing-terms-with-bot': (
        {tt, lem, wlem, dgp},
        {glpoa, dp, he, gmp, wgmp, ud, mgmp},
    ),
    'v-const-term': (
        {tt, efq, dnsu, ud},
        {wlem, dgp, dnse},
    ),
    'v-const-term-lobot': (
        {tt, glpoa, lem, dpn, hen, gmp, dnse, glpon, ud},
        {dgp},
    ),
    'diamond-constant-terms': (
        {tt, efq, wlem, gmp, ud},
        {dgp, lem},
    ),
    'beth-width-two': (
        {lem, he, dp},
        set(),
    ),
    'one-term-v': (
        {efq, dp, he},
        {wlem, dgp},
    ),
    'one-term-v-lem': (
        {dp, he, lem, ud, glpoa},
        {dgp},
    ),
    'trivial-lobot': (
        {f for f in formulae if f is not efq},
        {efq},
    ),
    'one-world-one-term': (
        {f for f in formulae if f is not tt} | {efq},
        {tt},
    ),
    'non-full-dp-cm-with-single-term-root': (
        {he, efq},
        {ud},
    ),
    'non-full-dp-cm-with-single-term-root-lem': (
        {he, lem},
        {ud},
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

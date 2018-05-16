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

#formula_layout = '''\
#    glpoa
#                              lem
#                dp                             he
#                ud  gmp            dgp
#            dnsu                                dnse
#                              wlem
#'''
formula_layout = '''\
glpoa         dp            he
              ud
gmp           lem     dgp
dnsu                         dnse
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
#    (he, tt, wlem),
#    (gmp, tt, wlem),
#    (dp, lem, glpoa), Not irrelevant, but higher level
    (dnse, tt, wlem),
}

proofs = {p: '{}-{}'.format(','.join(p[:-1]), p[-1]) for p in unnamed_proofs}

allproofs = set(proofs) | {(lem, efq, f) for f in formulae if f != tt}

named_models = {
        'dp-cm': (
            {efq, tt, he, dgp, wlem, ud},
            {dp, lem, dnsu},
        ),
        'he-cm': (
            {efq, tt, dp, dgp, wlem},
            {he, lem},
        ),
        'v-const': (
            {efq, tt, dnsu, ud},
            {dp, he, dgp, wlem, dnse},
        ),
        'v-const-lem': (
            {glpoa, lem},
            {dp, he, dgp},
        ),
        'v-one-term': (
            {efq, dp, he},
            {dgp, wlem},
        ),
        'v-one-term-lobot': (
            {tt, dp, he, glpoa},
            {dgp},
        ),
        'diamond-const': (
            {efq, tt, wlem, gmp},
            {dp, he, dgp},
        ),
        'one-world-one-term': (
            (set(formulae) - {tt}) | {efq},
            {tt},
        ),
        'two-world-growing-terms-2-3': (
            {tt, efq, dgp, wlem, dnsu},
            {dnse, ud},
        ),
        'two-world-growing-terms-2-3-lem': (
            {tt, lem},
            {efq, gmp, ud, dnsu, dp, he},
        ),
        'two-world-growing-terms-lobot': (
            {tt, dgp, gmp, glpoa},
            {efq, ud, he, dp},
        ),
        'nonfull': (
            {he, efq},
            {ud},
        ),
        'nonfull-2': (
            {he, tt, efq},
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
    int_proofs.update({(lem, f): 'classical' for f in formulae if f != tt})
    int_possible_edges = find_possible_connections(
                         formulae, int_proofs, int_models)
    int_diagram = TikzHierarchy(name_dict=formula_strs)
    int_diagram.add_string_node_layout(formula_layout)
    int_diagram.add_edges(spanning_tree(set(int_proofs)), color=False)
    int_diagram.add_edges(int_possible_edges, 'dashed')


    efqtt_possible_edges = find_evaluated_connections(
                             formulae, set(allproofs), list(models), free=(efq, tt), order=1)
    two_diagram = TikzHierarchy(name_dict=formula_strs)
    two_diagram.add_string_node_layout(formula_layout)
    two_diagram.add_edges(spanning_tree(set(proofs)), color=False)
    two_diagram.add_edges(set(efqtt_possible_edges), 'dashed')


    tex = make_sections(
        ('Minimal Logic', minimal_diagram),
        ('Investigations ({})'.format(len(possible_edges)),
            make_columns(make_connections_list(possible_edges)), 1),
        ('Minimal Logic with EFQ links', efq_diagram),
        ('Intuitionistic Logic', int_diagram),
        ('Investigations ({})'.format(len(int_possible_edges)),
            make_columns('\n'.join(map(str, int_possible_edges))), 1),
        ('Inuitionistic Logic Two-term Possibilities', two_diagram),
        ('Investigations ({})'.format(len(efqtt_possible_edges)),
            make_columns(make_connections_list(efqtt_possible_edges)), 1),
    )

    document = make_latex_document(tex)

    with open('drinker.tex', 'w') as f:
        f.write(document)
    subprocess.call(['pdflatex', 'drinker.tex'], stdout=subprocess.DEVNULL)
    #with open('backdrinker.tex', 'r') as f:
    #    assert(f.read() == document)

import subprocess
from hierarchy import *
from tikzify import *

formulae = 'lem wlem dp he dnsu dnse glpo glpoa gmp wgmp dgp'.split()
globals().update({f: f for f in formulae})
efq = 'efq'


formula_layout = '''\
          glpoa
                              lem                 glpo
             dp                                he
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


proofs = {
    (lem, wlem):   'lem-wlem',
    (dp, wlem):    'dp-wlem',
    (he, wlem):    'he-wlem',
    (lem, glpo):   'lem-glpo',
    (glpo, lem):   'glpo-lem',
    (glpoa, lem):  'glpoa-lem',
    (glpoa, glpo): 'glpoa-glpo',
    (dp, dnsu):    'dp-dnsu',
    (glpoa, dnsu): 'glpoa-dnsu',
    (he, dnse): 'he-dnse',
    (gmp, dnse): 'gmp-dnse',
    (gmp, dnsu): 'gmp-dnsu',
    (dp, gmp): 'dp-gmp',
    (gmp, wlem): 'gmp-wlem',
    (dp, dgp): 'dp-dgp',
    (he, dgp): 'he-dgp',
    (dgp, wlem): 'dgp-wlem',
    (gmp, wgmp): 'gmp-wgmp',
    (glpoa, wgmp): 'glpoa-wgmp',
    (dp, lem, glpoa): '',
    (he, lem, glpo): '',
}

models = {
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
    'v-shape-const-term': (
        {efq, dnse, dnsu},
        {wlem, dgp, wgmp},
    ),
    'dp-simple-cm': (
        {efq, lem, dgp, wlem},
        {dnsu, dp, he},
    ),
    'dnse-cm': (
        {efq, wlem, dgp, glpoa},
        {dnse, he},
    ),
    'v-lobot': (
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

if __name__ == '__main__':
    possible_edges = find_possible_connections(formulae, proofs, models.values())
    minimal_diagram = TikzHierarchy(name_dict=formula_strs)
    minimal_diagram.add_string_node_layout(formula_layout)
    minimal_diagram.add_edges(spanning_tree(set(proofs)), color=False)
    minimal_diagram.add_edges(possible_edges, 'dashed')


    efq_diagram = TikzHierarchy(minimal_diagram)
    efq_proofs = {(lem, efq, f): 'classical' for f in formulae}
    efq_diagram.add_edges(spanning_tree(set(efq_proofs), set(proofs)), 'dotted')


    int_proofs = dict(proofs)
    int_models = {k: v for k, v in models.items() if efq in v[0]}
    int_proofs.update({(lem, f): 'classical' for f in formulae})
    int_possible_edges = find_possible_connections(
                         formulae, int_proofs, int_models.values())
    int_diagram = TikzHierarchy(name_dict=formula_strs)
    int_diagram.add_string_node_layout(formula_layout)
    int_diagram.add_edges(spanning_tree(set(int_proofs)), color=False)
    int_diagram.add_edges(int_possible_edges, 'dashed')


    two_possible_edges = find_evaluated_connections(
                             formulae, set(proofs), list(models.values()), free=(), order=2)
    two_diagram = TikzHierarchy(name_dict=formula_strs)
    two_diagram.add_string_node_layout(formula_layout)
    two_diagram.add_edges(spanning_tree(set(proofs)), color=False)
    two_diagram.add_edges(set(two_possible_edges), 'dashed')

    tex = R'''
    \section*{Minimal Logic}
    ''' + str(minimal_diagram) + R'''
    \section*{Minimal Logic with EFQ links}
    ''' + str(efq_diagram) + R'''
    \section*{Intuitionistic Logic}
    ''' + str(int_diagram) + '''
    \section*{Minimal Logic - Two-premise Possibilities}
    ''' + str(two_diagram) + '''
    \subsection*{Investigations (''' + str(len(two_possible_edges)) + ''')}
    ''' + make_columned_text(make_connections_list(two_possible_edges))

    document = make_latex_document(tex)

    with open('drinker.tex', 'w') as f:
        f.write(document)
    subprocess.call(['pdflatex', 'drinker.tex'])#, stdout=subprocess.DEVNULL)
    #with open('backdrinker.tex') as f:
    #    assert(f.read() == document)
    #print("Good!")

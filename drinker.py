import subprocess
from hierarchy import *
from tikzify import *

formulae = 'lem wlem dp he dnsu dnse glpo glpoa gmp dgp'.split()
globals().update({f: f for f in formulae})
efq = 'efq'


formula_layout = '''\
          glpoa
                              lem                 glpo
             dp                                he
                                    dgp
                     gmp
    dnsu                                                dnse
                              wlem
'''


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
}

models = {
    'dp-cm-lobot': (
        {he, lem, wlem, dnsu, dnse, glpo, glpoa, gmp},
        {dp},
    ),
    'dp-cm': (
        {efq, he, wlem},
        {dp, lem, dnsu},
    ),
    'dp-cm-bottop': (
        {he, wlem},
        {dnsu},
    ),
    'he-cm-lobot': (
        {dp, lem, wlem, dnsu, dnse, glpo, glpoa, gmp},
        {he},
    ),
    'he-cm': (
        {efq, dp, wlem},
        {he, lem},
    ),
    'linear': (
        {efq, wlem, dgp},
        {dp, he, lem, dnse},
    ),
    'glpoa-cm': (
        {lem, wlem},
        {glpoa, dp, he, gmp},
    ),
    'v-shape-const-term': (
        {efq, dnse, dnsu},
        {wlem, dgp},
    ),
    'dp-simple-cm': (
        {lem},
        {dnsu, dp, he},
    ),
    'dnse-cm': (
        {efq, glpoa},
        {dnse, he},
    ),
    'v-lobot': (
        {glpoa, lem, gmp},
        {dgp},
    ),
    'diamond': (
        {efq, wlem, gmp},
        {dgp},
    ),
    'trivial-lobot': (
        {f for f in formulae if f is not efq},
        {efq},
    ),
}

possible_edges = find_possible_connections(formulae, proofs, models.values())

int_models = {k: v for k, v in models.items() if efq in v[0]}
dne_proofs = {(lem, efq, f): 'classical' for f in formulae}
int_proofs = dict(proofs)
int_proofs.update(dne_proofs)
int_possible_edges = find_possible_connections(
                     formulae, int_proofs, int_models.values())

minimal_diagram = TikzHierarchy()
minimal_diagram.add_string_node_layout(formula_layout)
minimal_diagram.add_edges(spanning_tree(set(proofs)))
minimal_diagram.add_edges(possible_edges, 'dashed')

efq_diagram = TikzHierarchy(minimal_diagram)
efq_diagram.add_edges(spanning_tree(set(dne_proofs), set(proofs)), 'dotted')

int_diagram = TikzHierarchy()
int_diagram.add_string_node_layout(formula_layout)
int_diagram.add_edges(spanning_tree(set(int_proofs)))
int_diagram.add_edges(int_possible_edges, 'dashed')


tex = R'''
\section*{Minimal Logic}
''' + str(minimal_diagram) + R'''
\section*{Minimal Logic with EFQ links}
''' + str(efq_diagram) + R'''
\section*{Intuitionistic Logic}
''' + str(int_diagram)

document = make_latex_document(tex)

with open('drinker.tex', 'w') as f:
    f.write(document)
subprocess.call(['pdflatex', 'drinker.tex'], stdout=subprocess.DEVNULL)

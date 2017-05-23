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

int_only_proofs = {(lem, efq, f): 'classical' for f in formulae}

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
        {wlem, gmp},
        {dgp},
    ),
    'trivial-lobot': (
        {f for f in formulae if f is not efq},
        {efq},
    ),
}

int_models = {k: v for k, v in models.items() if efq in v[0]}

span_proofs = list(spanning_tree(proofs.keys()))
weak_edges = list(find_possible_connections(formulae, proofs, models.values()))
span_int_only_proofs = list(spanning_tree(int_only_proofs.keys()))
weak_int_edges = list(find_possible_connections(
    formulae, set(proofs) | set(int_only_proofs), models.values(), (efq, )))

tikz_nodes = string_node_layout_to_tikz(formula_layout)

tikz_pf_edges = tikzify_edges(span_proofs)
drawn = span_proofs

tikz_pf_int_only_edges = tikzify_edges(span_int_only_proofs, '', drawn)
drawn += span_int_only_proofs

tikz_weak_edges = tikzify_edges(weak_edges, 'dashed', drawn)
drawn += weak_edges

tikz_weak_int_edges = tikzify_edges(weak_int_edges, 'dotted', drawn)
drawn += weak_int_edges

diagram = make_tikz_diagram(tikz_nodes, tikz_pf_edges, tikz_weak_edges, tikz_weak_int_edges)
document = make_latex_document(diagram)

with open('drinker.tex', 'w') as f:
    f.write(document)
subprocess.call(['pdflatex', 'drinker.tex'], stdout=subprocess.DEVNULL)

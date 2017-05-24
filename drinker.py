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
        {wlem, gmp},
        {dgp},
    ),
    'trivial-lobot': (
        {f for f in formulae if f is not efq},
        {efq},
    ),
}

int_models = {k: v for k, v in models.items() if efq in v[0]}
int_only_proofs = {(lem, efq, f): 'classical' for f in formulae}
int_proofs = dict(proofs)
int_proofs.update(int_only_proofs)

span_proofs = spanning_tree(proofs.keys())
span_int_only_proofs = spanning_tree(int_proofs) - set(span_proofs)
weak_edges = list(find_possible_connections(formulae, proofs, models.values()))
weak_int_edges = list(find_possible_connections(
    formulae, set(proofs) | set(int_only_proofs), models.values(), (efq, )))

diagram = TikzHierarchy()
diagram.add_string_node_layout(formula_layout)
diagram.add_labelled_edges(span_proofs, 'dotted')
diagram.add_labelled_edges(span_int_only_proofs)
diagram.add_labelled_edges(weak_edges, 'dashed')
#diagram.add_labelled_edges(weak_int_edges, 'dashed')


document = make_latex_document(diagram.make_diagram())

with open('drinker.tex', 'w') as f:
    f.write(document)
subprocess.call(['pdflatex', 'drinker.tex'], stdout=subprocess.DEVNULL)

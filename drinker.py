from hieretikz import *
import subprocess
from constructive_hierarchy import *

formulae = lem, wlem, dp, he, dnsu, dnse, glpo, glpoa, gmp, dgp, efq = \
          'lem  wlem  dp  he  dnsu  dnse  glpo  glpoa  gmp  dgp  efq'.split()


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
    'trivial-lobot': (
        {f for f in formulae if f is not efq},
        {efq},
    ),
}


# Over intuitionistic logic, lem implies every formula above, and efq is
# derivable
proofs.update({(lem, f): 'classical' for f in formulae})
proofs.update({(f, efq): 'intuitionistic' for f in formulae})
models = {m: t for m, t in models.items() if efq in t[0]}

# Over decidable minimal logic,
#proofs.update({(efq, f): 'classical' for f in formulae})
#proofs.update({(f, lem): 'decidable' for f in formulae})
#models = {m: t for m, t in models.items() if lem in t[0]}
#formula_layout = formula_layout.replace('     lem',
#                                        'efq     ')

document = hieretikz_document(formulae, formula_layout, proofs, models)

with open('drinker.tex', 'w') as f:
    f.write(document)
subprocess.Popen(['pdflatex', 'drinker.tex'], stdout=subprocess.DEVNULL)

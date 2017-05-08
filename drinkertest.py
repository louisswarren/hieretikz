from hieretikz import *
import subprocess
from constructive_hierarchy import *

formulae = lem, wlem, dp, he, dnsu, dnse, glpo, glpoa, gmp, dgp = \
          'lem  wlem  dp  he  dnsu  dnse  glpo  glpoa  gmp  dgp'.split()


_______ = None
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


# Dictionary of models, to a pair of set. The first set is the formulae which
# hold in the model as schemes, the second tuple is the formulae which fail for
# certain instances.

models = {
    'dp-cm-lobot': (
        {he, lem, wlem, dnsu, dnse, glpo, glpoa, gmp},
        {dp},
    ),
    'dp-cm': (
        {he, wlem},
        {dp, lem},
    ),
    'dp-cm-bottop': (
        {he, wlem},
        {dnsu},
    ),
    'he-cm-lobot': (
        {dp, lem, wlem, dnsu, dnse, glpo, glpoa, gmp},
        {he, lem},
    ),
    'he-cm': (
        {dp, wlem},
        {he},
    ),
    'linear': (
        {wlem, dgp},
        {dp, he, lem, dnse},
    ),
    'glpoa-cm': (
        {lem, wlem},
        {glpoa, dp, he, gmp},
    ),
    'v-shape-const-term': (
        {dnse, dnsu},
        {wlem, dgp},
    ),
    'dnse-cm': (
        {dp, glpoa},
        {dnse, he},
    ),
    'v-lobot': (
        {lem},
        {dgp},
    )
}

counter_models = {(holds, fails): cm for cm, fpair in models.items()
                                     for holds in fpair[0]
                                     for fails in fpair[1]}

document = hieretikz_document(formulae, formula_layout, proofs, counter_models)

with open('drinker.tex', 'w') as f:
    f.write(document)
subprocess.Popen(['pdflatex', 'drinker.tex'], stdout=subprocess.DEVNULL)


sep = lambda a, b: is_separated(a, b, set(proofs), set(counter_models))
con = lambda a, b: is_connected(a, b, set(proofs))

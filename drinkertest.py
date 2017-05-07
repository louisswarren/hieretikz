from hieretikz import *
import subprocess
from constructive_hierarchy import *

formulae = lem, wlem, dp, he, dnsu, dnse, glpo, glpoa, gmp = \
    'lem', 'wlem', 'dp', 'he', 'dnsu', 'dnse', 'glpo', 'glpoa', 'gmp'


_______ = None
formula_layout = '''\
          glpoa
                              lem                 glpo

             dp                                he
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
#
        (he, dnse): 'he-dnse',
        (gmp, dnse): 'gmp-dnse',
        (gmp, dnsu): 'gmp-dnsu',
        (dp, gmp): 'dp-gmp',
        }

#counter_models = {
#        (dp, he):     'dp-/-he',
#        (he, dp):     'he-/-dp',
#        (lem, dp):    'lem-/-dp',
#        (lem, he):    'lem-/-he',
#        (lem, glpoa): 'lem-/-glpoa',
#        (he, dnsu):   'he-/-dnsu',
#        (dnsu, dp):   'dnsu-/-dp',
##
#        (dp, lem): 'dp-/-lem',
#        (he, lem): 'he-/-lem',
#        (dnse, dp): 'dnse-/-dp',
#        (dp, dnse): 'dp-/-dnse',
#        }

# Dictionary of models, to a pair of tuples. First tuple is formulae which hold
# in the model, second tuple is formulae which fail.
# lem, wlem, dp, he, dnsu, dnse, glpo, glpoa, gmp

models = {
    'dp-cm-bot': ((he, lem, wlem, dnsu, dnse, glpo, glpoa, gmp),
                  (dp)),
    'he-cm-bot': ((dp, lem, wlem, dnsu, dnse, glpo, glpoa, gmp),
                  (he)),
    'linear':    ((wlem, ),
                  (dp, he, lem)),
}

counter_models = {(holds, fails) for _, fpair in models.items()
                                 for holds in fpair[0]
                                 for fails in fpair[1]}

document = hieretikz_document(formulae, formula_layout, proofs, counter_models)

with open('drinker.tex', 'w') as f:
    f.write(document)
subprocess.Popen(['pdflatex', 'drinker.tex'], stdout=subprocess.DEVNULL)


sep = lambda a, b: is_separated(a, b, set(proofs), set(counter_models))
con = lambda a, b: is_connected(a, b, set(proofs))

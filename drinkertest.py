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
        (lem, wlem):   '', # Not yet
        (dp, wlem):    '',
        (he, wlem):    '',
        (lem, glpo):   '',
        (glpo, lem):   '',
        (glpoa, lem):  '',
        (glpoa, glpo): '',
        (dp, dnsu):    '',
        (glpoa, dnsu): '',
#
        (he, dnse): '',
        (gmp, dnse): '',
        (gmp, dnsu): '',
        }

counter_models = {
        (dp, he):     '',
        (he, dp):     '',
        (lem, dp):    '',
        (lem, he):    '',
        (lem, glpoa): '',
        (he, dnsu):   '',
        (dnsu, dp):   '',
#
        (dp, lem): '',
        (he, lem): '',
        (dnse, dp): '',
        (dp, dnse): '',
        }


document = r'''
\documentclass{article}
\usepackage{tikz}
\usepackage{amsmath}
\usepackage{fullpage}
\usepackage{multicol}
\begin{document}
''' + \
make_tikz(formulae, formula_layout, set(proofs), set(counter_models)) + \
r'''
\paragraph{}
It remains to investigate:
\begin{multicols}{3}
\noindent
''' + \
assist(formulae, formula_layout, set(proofs), set(counter_models)) + \
r'''
\end{multicols}
\end{document}
'''
with open('drinker.tex', 'w') as f:
    f.write(document)
subprocess.Popen(['pdflatex', 'drinker.tex'], stdout=subprocess.DEVNULL)


sep = lambda a, b: is_separated(a, b, set(proofs), set(counter_models))
con = lambda a, b: is_connected(a, b, set(proofs))

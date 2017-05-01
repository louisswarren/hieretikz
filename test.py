from hieretikz import *
from subprocess import Popen

formulae = dne, lem, wlem, dp, he, dnsu, dnse, glpo, glpoa, gmp = \
    'dne', 'lem', 'wlem', 'dp', 'he', 'dnsu', 'dnse', 'glpo', 'glpoa', 'gmp'


_______ = None
formula_layout = [
[dne     , glpoa   , _______ , _______ , _______ , _______ , _______ ],
[_______ , _______ , _______ , lem     , _______ , glpo    , _______ ],
[_______ , _______ , _______ , _______ , _______ , _______ , _______ ],
[_______ , dp      , _______ , _______ , _______ , he      , _______ ],
[dnsu    , _______ , gmp     , _______ , _______ , _______ , dnse    ],
[_______ , _______ , _______ , wlem    , _______ , _______ , _______ ],
]

proofs = {
        (dne, glpoa): 'pft',
        (lem, wlem):  'pf0',
        (dp, wlem):   'pf1',
        (he, wlem):   'pf2',
        (glpoa, lem): 'pf3',
        (lem, glpo):  'pf4',
        (glpo, lem):  'pf5',
        (dp, gmp):    'pf6',
        (gmp, wlem):  'pf7',
        (dp, dnsu):   'pf8',
        (he, dnse):   'pf9',
        }

counter_models = {
        (glpoa, dne): 'cmt',
        (wlem, lem):  'cm0',
        (wlem, dp):   'cm1',
        (wlem, he):   'cm2',
        (lem, glpoa): 'cm3',
        (glpo, lem):  'cm4',
        (lem, glpo):  'cm5',
        (gmp, dp):    'cm6',
        (wlem, gmp):  'cm7',
        (dnsu, dp):   'cm8',
        (dnse, he):   'cm9',
        }


document = r'''
\documentclass{article}
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}[node distance=2 cm, line width=0.3mm, auto]
''' + \
make_tikz(formulae, formula_layout, proofs, counter_models) + \
r'''
\end{tikzpicture}
\end{document}
'''
print(document)
with open('test.tex', 'w') as f:
    f.write(document)
Popen(['pdflatex', 'test.tex'])

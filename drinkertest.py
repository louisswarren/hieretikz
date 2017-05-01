from hieretikz import *
from subprocess import Popen

formulae = lem, wlem, dp, he, dnsu, dnse, glpo, glpoa, gmp = \
    'lem', 'wlem', 'dp', 'he', 'dnsu', 'dnse', 'glpo', 'glpoa', 'gmp'


_______ = None
formula_layout = [
[_______ , glpoa   , _______ , _______ , _______ , _______ , _______ ],
[_______ , _______ , _______ , lem     , _______ , glpo    , _______ ],
[_______ , _______ , _______ , _______ , _______ , _______ , _______ ],
[_______ , dp      , _______ , _______ , _______ , he      , _______ ],
[dnsu    , _______ , gmp     , _______ , _______ , _______ , dnse    ],
[_______ , _______ , _______ , wlem    , _______ , _______ , _______ ],
]

proofs = {
        (lem, wlem):   '', # Not yet
        (dp, wlem):    '',
        (he, wlem):    '',
        (lem, glpo):   '',
        (glpo, lem):   '',
        (glpoa, lem):  '',
        (glpoa, glpo): '',
        (dp, dnse):    '',
        (glpoa, dnse): '',
        }

counter_models = {
        (dp, he):     '',
        (he, dp):     '',
        (lem, dp):    '',
        (lem, he):    '',
        (lem, glpoa): '',
        (he, dnse):   '',
        (dnse, dp):   '',
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
with open('drinker.tex', 'w') as f:
    f.write(document)
Popen(['pdflatex', 'drinker.tex'])


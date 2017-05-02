from hieretikz import *
import subprocess

formulae = lem, wlem, dp, he, dnsu, dnse, glpo, glpoa, gmp = \
    'lem', 'wlem', 'dp', 'he', 'dnsu', 'dnse', 'glpo', 'glpoa', 'gmp'


_______ = None
formula_layout = [
'          glpoa                                                     ',
'                              lem                 glpo              ',
'                                                                    ',
'             dp                                he                   ',
'                    gmp                                             ',
'    dnsu                                                dnse        ',
'                              wlem                                  ',
]

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
\begin{tikzpicture}[node distance=1 cm, line width=0.3mm, auto]
''' + \
make_tikz(formulae, formula_layout, proofs, counter_models) + \
r'''
\end{tikzpicture}
\paragraph{}
It remains to investigate:
\begin{multicols}{3}
\noindent
''' + \
assist(formulae, formula_layout, proofs, counter_models) + \
r'''
\end{multicols}
\end{document}
'''
print(document)
with open('drinker.tex', 'w') as f:
    f.write(document)
subprocess.Popen(['pdflatex', 'drinker.tex'])


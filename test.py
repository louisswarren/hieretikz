from hieretikz import *
import subprocess

formulae = dne, lem, lpo, wlem = 'dne lem lpo wlem'.split()

_______ = None
formula_layout = [
[_______ , dne     , _______ ],
[lem     , _______ , lpo     ],
[_______ , wlem    , _______ ],
]

proofs = {
        (dne, lem):  'pf0',
        (lem, lpo):  'pf1',
        (lpo, lem):  'pf1',
        (lem, wlem): 'pf2',
        }

counter_models = {
        (lem, dne):  'cm0',
        (wlem, lem): 'cm1',
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
with open('test.tex', 'w') as f:
    f.write(document)
subprocess.Popen(['pdflatex', 'test.tex'], stdout=subprocess.DEVNULL)



# Debugging

# print('='*80)
# pf_adjacency = compute_adjacency(proofs)
# cm_adjacency = compute_adjacency(counter_models)
# print(find_relation(lpo, dne, pf_adjacency, cm_adjacency))

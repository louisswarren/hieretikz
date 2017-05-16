from hieretikz import *
import subprocess
from constructive_hierarchy import *

formulae = lem, wlem, dp, dpn, he, dnsu, dnse, glpo, glpoa, gmp, wgmp, dgp, efq = \
          'lem  wlem  dp  dpn  he  dnsu  dnse  glpo  glpoa  gmp  wgmp  dgp  efq'.split()

formulae.remove(dpn)

formula_layout = '''\
          glpoa
                              lem                 glpo
             dp                                he
                                    dgp
                     gmp
                    wgmp
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
    (dp, dpn): 'dp-dpn',
    (he, dpn): 'he-dpn',
    (gmp, wgmp): 'gmp-wgmp',
    (glpoa, wgmp): 'glpoa-wgmp',
}



models = {
    'dp-cm-lobot': (
        {he, lem, wlem, dnsu, dnse, glpo, glpoa, gmp, dpn},
        {dp},
    ),
    'dp-cm': (
        {efq, he, wlem},
        {dp, lem, dnsu, wgmp},
    ),
    'dp-cm-bottop': (
        {he, wlem},
        {dnsu},
    ),
    'he-cm-lobot': (
        {dp, lem, wlem, dnsu, dnse, glpo, glpoa, gmp, dpn},
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
        {lem, wlem, dpn},
        {glpoa, dp, he, gmp, wgmp},
    ),
    'v-shape-const-term': (
        {efq, dnse, dnsu},
        {wlem, dgp, wgmp},
    ),
    'dp-simple-cm': (
        {lem},
        {dnsu, dp, he},
    ),
    'dnse-cm': (
        {efq, glpoa},
        {dnse, dp, he},
    ),
    'v-lobot': (
        {glpoa, lem, gmp, dpn},
        {dgp},
    ),
    'diamond': (
        {efq, wlem, gmp},
        {dgp},
    ),
    'trivial-lobot': (
        {f for f in formulae if f is not efq},
        {efq},
    ),
}

minimal_tex = hieretikz(formulae, formula_layout, proofs, models)

# Over intuitionistic logic, lem implies every formula above, and efq is
# derivable
int_proofs = dict(proofs)
int_proofs.update({(lem, f): 'classical' for f in formulae})
int_proofs.update({(f, efq): 'intuitionistic' for f in formulae})
int_models = {m: t for m, t in models.items() if efq in t[0]}

intuitionistic_tex = hieretikz(formulae, formula_layout, int_proofs, int_models)

document = hieretikz_document_wrap(r'''
\section{Minimal Logic}
''' + minimal_tex + r'''
\newpage
\section{Intuitionistic Logic}
''' + intuitionistic_tex
)

with open('drinker.tex', 'w') as f:
    f.write(document)
subprocess.call(['pdflatex', 'drinker.tex'], stdout=subprocess.DEVNULL)

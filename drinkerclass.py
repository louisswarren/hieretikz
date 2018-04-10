import subprocess
from hierarchyclass import *
from tikzify import *

formulae = 'tt lem wlem dgp glpoa gmp dp he dpn dnsu dnse ud'.split()
globals().update({f: f for f in formulae})
efq = 'efq'

globals().update({future: future for future in
 'glpon mgmp'.split()})
formulae += [glpon, mgmp]

# These are actually equivalent.
ip = he
glpo = lem
hen = dpn
wgmp = dnsu

formula_layout = '''\
    glpoa
                              lem
                dp                             he
                                    dpn
                ud  gmp            dgp
            dnsu       glpon                    dnse
                              wlem
'''

formula_strs = {f: f.upper() for f in formulae}
formula_strs[dnse] = R'DNS$\exists$'
formula_strs[glpoa] = "GLPO$'$"
formula_strs[glpon] = R'GLPO$_\neg$'

formula_strs[dnsu] = R'DNS$\forall$,WGMP'
formula_strs[lem] = R'LEM,GLPO'
formula_strs[dpn] = R'DP$_\lnot$,HE$_\lnot$'


unnamed_proofs = {
#    (he, ip), (ip, he),
#    (lem, glpo), (glpo, lem),
#    (dpn, hen), (hen, dpn),
#    (dnsu, wgmp), (wgmp, dnsu),
    (lem, wlem),
    (dp, dpn),
    (he, hen),
    (gmp, wgmp),
    (dgp, wlem),
    (glpoa, lem),
    (glpoa, gmp),
    (dp, ud),
    (dp, gmp),
#    (dp, dnsu),
    (glpo, dpn),
    (he, dnse),
    (glpo, dnse),
    (gmp, dnse),
    (dpn, dnse),
    (glpoa, wgmp),
    (dp, efq, tt, dgp),
    (he, efq, tt, dgp),
    (dp, tt, wlem),
    (he, tt, wlem),
    (gmp, tt, wlem),
    (gmp, mgmp), (glpo, glpon), (glpon, wlem), (glpon, dnse), # Speculation
}

# EFQ isn't on the diagram, so these won't be plotted
unnamed_proofs.update({(efq, lem, f) for f in formulae if f not in (efq, lem)})

proofs = {p: '{}-{}'.format(','.join(p[:-1]), p[-1]) for p in unnamed_proofs}

named_models = {
    'dp-cm': (
        {tt, efq, he, dgp, wlem, glpon, ud},
        {dp, lem, dnsu, wgmp, mgmp},
    ),
    'dp-cm-lobot': (
        {tt, he, lem, dpn, hen, dgp, wlem, dnsu, dnse, glpo, glpoa, glpon, gmp, ud},
        {dp},
    ),
    'he-cm': (
        {tt, efq, dp, dgp, wlem, glpon, ud},
        {he, lem},
    ),
    'he-cm-lobot': (
        {tt, dp, lem, dpn, hen, dgp, wlem, dnsu, dnse, glpo, glpoa, glpon, gmp, ud},
        {he},
    ),
    'linear-growing-terms': (
        {tt, efq, wlem, dgp},
        {dp, he, lem, dnse, glpoa, ud},
    ),
    'two-world-constant-terms': (
        {tt, efq, dp, he, wlem, dgp, ud},
        {lem},
    ),
    'two-world-growing-terms': (
        {tt, efq, wlem, dgp, wgmp},
        {glpoa, dp, he, dpn, hen, gmp, dnse, glpon, ud},
    ),
    'two-world-growing-terms-lobot': (
        {tt, gmp, glpoa},
        {ud},
    ),
    'two-world-growing-terms-with-bot': (
        {tt, lem, wlem, dgp},
        {glpoa, dp, he, gmp, wgmp, ud, mgmp},
    ),
    'v-const-term': (
        {tt, efq, dnsu, ud},
        {wlem, dgp, dnse},
    ),
    'v-const-term-lobot': (
        {tt, glpoa, lem, dpn, hen, gmp, dnse, glpon, ud},
        {dgp},
    ),
    'diamond-constant-terms': (
        {tt, efq, wlem, gmp, ud},
        {dgp, lem},
    ),
    'beth-width-two': (
        {lem, he, dp},
        set(),
    ),
    'one-term-v': (
        {dp, he},
        {wlem, dgp},
    ),
    'trivial-lobot': (
        {f for f in formulae if f is not efq},
        {efq},
    ),
    'tt-weak': ({tt}, {f for f in formulae if f is not tt}),
    'tt-strong': ({f for f in formulae if f is not tt}, {tt}),
}
models = [(k, *map(frozenset, v)) for k, v in named_models.items()]

if __name__ == '__main__':
    h = Hierarchy((Arrow(tails, head) for *tails, head in unnamed_proofs),
                  (Tier(low, high, name) for name, (low, high) in named_models.items()))
    qarrows = h.find_qarrows(set(formulae))
    ev_qarrows = {arrow.edge: h.evaluate_qarrow(arrow, set(formulae)) for arrow in qarrows}
    minimal_diagram = TikzHierarchy(name_dict=formula_strs)
    minimal_diagram.add_string_node_layout(formula_layout)
    minimal_diagram.add_edges((set(proofs)), color=False)
    minimal_diagram.add_edges(set(arrow.edge for arrow in qarrows), 'dashed')

    inth = h.under_quotient(efq)
    int_qarrows = inth.find_qarrows(set(formulae) - {efq})
    int_ev_qarrows = {arrow.edge: inth.evaluate_qarrow(arrow, set(formulae)) for arrow in int_qarrows}
    int_diagram = TikzHierarchy(name_dict=formula_strs)
    int_diagram.add_string_node_layout(formula_layout)
    int_diagram.add_edges(set(proofs), color=False)
    int_diagram.add_edges(set(arrow.edge for arrow in int_qarrows), 'dashed')

    tth = h.under_quotient(tt)
    tt_qarrows = tth.find_qarrows(set(formulae) - {tt})
    tt_ev_qarrows = {arrow.edge: tth.evaluate_qarrow(arrow, set(formulae)) for arrow in tt_qarrows}
    tt_diagram = TikzHierarchy(name_dict=formula_strs)
    tt_diagram.add_string_node_layout(formula_layout)
    tt_diagram.add_edges(set(proofs), color=False)
    tt_diagram.add_edges(set(arrow.edge for arrow in tt_qarrows), 'dashed')


    tex = make_sections(
        ('Minimal Logic', minimal_diagram),
        ('Investigations ({})'.format(len(qarrows)),
            make_columns(make_connections_list(ev_qarrows)), 1),
        ('Intuitionistic Logic', int_diagram),
        ('Investigations ({})'.format(len(int_qarrows)),
            make_columns(make_connections_list(int_ev_qarrows)), 1),
        ('Two-termed semantics', tt_diagram),
        ('Investigations ({})'.format(len(tt_qarrows)),
            make_columns(make_connections_list(tt_ev_qarrows)), 1),
    )

    document = make_latex_document(tex)

    with open('drinker.tex', 'w') as f:
        f.write(document)
    subprocess.call(['pdflatex', 'drinker.tex'], stdout=subprocess.DEVNULL)
    #with open('backdrinker.tex', 'r') as f:
    #    assert(f.read() == document)

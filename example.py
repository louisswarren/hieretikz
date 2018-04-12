import subprocess
from hierarchy import *
from tikzify import *

# Create variables for all principles, put them in a list
principles = set('A B C D E F'.split())
globals().update({f: f for f in principles})

layout = '''\
        A                  B
                  C            E
                  D
                      F
'''

proofs = [
    Arrow({A, B}, C),                 # A, B |- C
    Arrow({C}, D, 'Lemma2.2'),
    Arrow({B}, F),
    Arrow({B}, E),
    Arrow({D, E}, F),
]
# Note that this will draw a line from A to C labelled B, but not from B to C

separations = [
    Tier({A}, {C}),
    Tier({B, D}, {C}),
    Tier({E}, {F}),
    Tier({C}, {A, B, F}),                # Model for C where A, B, F fail
    Tier({F}, {B, E}, 'V-shape'),
]
# You will get a tier overlap exception if a model is inconsistent


# Create the hierarchy and find unknown connections of order <= 1
# (Meaning only one premise)
order = 1
h = Hierarchy(proofs, separations)
unknown = h.find_qarrows(principles, order)

# Create a tikz diagram
diagram = TikzHierarchy()
diagram.add_string_node_layout(layout)
diagram.add_edges({proof.edge for proof in proofs}, color=False)
diagram.add_edges({arrow.edge for arrow in unknown}, 'dashed')

evaluated = {arrow.edge: h.evaluate_qarrow(arrow, principles, order)
             for arrow in unknown}

# Make the tex document
tex = make_sections(
    ('Hierarchy diagram', diagram),
    ('Open investigations ({})'.format(len(unknown)),
        make_columns(make_connections_list(evaluated)), 1),
)
document = make_latex_document(tex)
with open('output.tex', 'w') as f:
    f.write(document)

# Compile the tex document
subprocess.call(['pdflatex', 'output.tex'], stdout=subprocess.DEVNULL)

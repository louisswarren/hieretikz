_compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

class TikzException(Exception):
    pass

class TikzHierarchy:
    def __init__(self, options='line width=0.3mm, auto'):
        self.tikz = []
        self.nodes = []
        self.edges = []
        self.options = options

    def add_node(self, node, x, y, node_str=None):
        if node in self.nodes:
            raise TikzException('Node already in diagram')
        node_str = node_str or node
        fmt = '\\node ({}) at ({}, {}) {{{}}};'
        self.tikz.append(fmt.format(node, x, y, node_str))
        self.nodes.append(node)

    def add_string_node_layout(self, node_layout):
        nodes = node_layout.split()
        for row_num, row in enumerate(node_layout.split('\n')):
            col_num = 0
            while col_num < len(row):
                if row[col_num].isspace():
                    col_num += 1
                else:
                    node = nodes.pop(0)
                    self.add_node(node, col_num // 5, -row_num * 2)
                    col_num += len(node)

    def add_edge(self, a, b, arrow_type='->', label=''):
        if label:
            fmt = ('\\draw[{}] ({}) to[{}] node[midway, sloped] {{' +
                   label + '}} ({});')
        else:
            fmt = '\\draw[{}] ({}) to[{}] ({});'
        count = self.edges.count((a, b)) + self.edges.count((b, a))
        bend = 'bend left={}'.format(count) if count else ''
        self.tikz.append(fmt.format(arrow_type, a, bend, b))
        self.edges.append((a, b))

    def add_labelled_edges(self, edges, arrow_extras='', labeller=', '.join):
        drawn = set()
        for a, *label_args, b in edges:
            label = labeller(label_args)
            if (b, a) in drawn:
                continue
            elif (b, a) in edges:
                arrow = '<->'
            else:
                arrow = '->'
            if arrow_extras:
                self.add_edge(a, b, arrow + ', ' + arrow_extras, label)
            else:
                self.add_edge(a, b, arrow, label)
            drawn.add((a, b))

    @_compose('\n'.join)
    def make_diagram(self):
        yield '\\begin{tikzpicture}[' + self.options + ']\n'
        yield from self.tikz
        yield '\\end{tikzpicture}'

    def __str__(self):
        return self.make_diagram()


@_compose('\n'.join)
def make_columned_text(*text, fmt='{}', columns=3):
    yield r'\begin{multicols}{' + str(columns) + r'} \noindent'
    yield from ((fmt + '\\').format(t) for t in text)
    yield r'\end{multicols}'

@_compose('\n'.join)
def make_latex_document(body, extra_packages=()):
    yield r'\documentclass{article}'
    yield r'\usepackage{tikz}'
    yield r'\usepackage{fullpage}'
    yield r'\usepackage{multicol}'
    yield from (r'\usepackage{' + package + '}' for package in extra_packages)
    yield r'\begin{document}'
    yield body
    yield r'\end{document}'

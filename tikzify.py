_compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

class TikzException(Exception):
    pass

class TikzHierarchy:
    '''Represent a hierarchy using Tikz.'''

    def __init__(self, hierarchy=None, *, options='auto', name_dict=None):
        '''Initialize, creating a copy of the hierarchy if provided.'''
        if hierarchy:
            self.tikz = list(hierarchy.tikz)
            self.nodes = list(hierarchy.nodes)
            self.edges = list(hierarchy.edges)
            self.name_dict = dict(hierarchy.name_dict)
            self.options = options if options else hierarchy.options
        else:
            self.tikz = []
            self.nodes = []
            self.edges = []
            self.name_dict = name_dict or {}
            self.options = options

    def add_node(self, node, x, y, node_str=None):
        '''Add a node to the hierarchy diagram.'''
        if node in self.nodes:
            raise TikzException('Node already in diagram')
        node_str = node_str or node
        fmt = '\\node ({}) at ({}, {}) {{{}}};'
        self.tikz.append(fmt.format(node, x, y, node_str))
        self.nodes.append(node)

    def add_string_node_layout(self, node_layout):
        '''Add all nodes and positions from a string diagram.'''
        nodes = node_layout.split()
        for row_num, row in enumerate(node_layout.split('\n')):
            col_num = 0
            while col_num < len(row):
                if row[col_num].isspace():
                    col_num += 1
                else:
                    node = nodes.pop(0)
                    node_str = self.name_dict.get(node, node)
                    self.add_node(node, col_num // 3, -row_num * 3, node_str)
                    col_num += len(node)

    @staticmethod
    def _color_parameter(obj):
        '''Get a color for an object, ready to pass to tikz as a parameter.'''
        n = hash(obj)
        r = n % 256
        g = (n // 256) % 256
        b = (n // 256 // 256) % 256
        return 'color={{rgb:red,{};green,{};blue,{}}}'.format(r, g, b)

    def add_edge(self, a, b, arrow_type='->', label=''):
        fmt = '\\draw[{}] ({}) to[{}] {}({});'
        if label:
            options = arrow_type + ', ' + TikzHierarchy._color_parameter(label)
            nodelabel = 'node[midway, sloped] {{{}}} '.format(label)
        else:
            options = arrow_type
            nodelabel = ''
        count = self.edges.count((a, b)) + self.edges.count((b, a))
        bend = 'bend left={}'.format(count * 20) if count else ''
        self.tikz.append(fmt.format(options, a, bend, nodelabel, b))
        self.edges.append((a, b))

    @_compose(', '.join)
    def default_labeller(self, labels):
        for label in labels:
            yield self.name_dict.get(label, label)

    def add_edges(self, edges, arrow_extras='', labeller=None):
        '''Add a set of (labelled) edges to the hierarchy diagram.

        A labelled edge is a tuple (a, label0, ..., labeln, b), where a is the
        tail, b is the head and (optional) label0 ... labeln are labels for the
        edge.'''
        if not labeller:
            labeller = self.default_labeller
        drawn = set()
        for a, *label_args, b in sorted(edges):
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
        yield '\\begin{centering}'
        yield '\\begin{tikzpicture}[' + self.options + ']\n'
        yield from self.tikz
        yield '\\end{tikzpicture}'
        yield '\\end{centering}'

    def __str__(self):
        return self.make_diagram()

@_compose('\n'.join)
def make_columned_text(*text, fmt='{}', columns=3):
    yield r'\begin{multicols}{' + str(columns) + r'} \noindent'
    yield from ((fmt + '\\').format(t) for t in text)
    yield r'\end{multicols}'

@_compose('\n'.join)
def make_latex_document(body, extra_packages=()):
    yield r'\documentclass[a4paper]{article}'
    yield r'\usepackage{tikz}'
    yield r'\usepackage[margin=1cm]{geometry}'
    yield r'\usepackage{multicol}'
    yield from (r'\usepackage{' + package + '}' for package in extra_packages)
    yield r'\begin{document}'
    yield body
    yield r'\end{document}'

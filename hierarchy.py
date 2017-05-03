'''Reason about a directed graph in which the (non-)existance of some edges
must be inferred by the disconnectedness of certain vertices'''

def transitive_closure_set(vertices, edges):
    '''Find the transitive closure of a set of vertices.'''
    neighbours = {b for a, b in edges if a in vertices}
    if neighbours.issubset(vertices):
        return vertices
    return transitive_closure_set(vertices | neighbours, edges)

def downward_closure(vertex, edges):
    '''Find the downward closure of a vertex.'''
    return transitive_closure_set({vertex}, edges)

def upward_closure(vertex, edges):
    '''Find the upward closure of a vertex.'''
    return transitive_closure_set({vertex}, {(b, a) for a, b in edges})

def is_connected(a, b, edges):
    '''Check if there is a path from a to b.'''
    return b in downward_closure(a, edges)

def is_separated(a, b, edges, disconnections, a_checked=None, b_checked=None):
    '''Checks that a and b will remain not connected even if edges are added to
    the graph, as long as the vertex pairs listed in disconnections remain
    disconected.'''
    if (a, b) in disconnections:
        return True
    a_checked = a_checked or set()
    b_checked = b_checked or set()
    above_a = upward_closure(a, edges) - a_checked
    below_b = downward_closure(b, edges) - b_checked
    new_a_checked = a_checked | {a}
    new_b_checked = b_checked | {b}
    for p in above_a:
        for q in below_b:
            if is_separated(p, q, edges, disconnections, new_a_checked, new_b_checked):
                return True
    return False

def find_possible_connections(vertices, edges, disconnections):
    '''Find which edges can be added to create new connections, without
    connecting any pairs in disconnections.'''
    return {(a, b) for a in vertices for b in vertices if
            not is_connected(a, b, edges) and
            not is_separated(a, b, edges, disconnections)}

def is_isthmus(edge, edges):
    a, _ = edge
    return not downward_closure(a, edges - {edge}) == downward_closure(a, edges)

def spanning_tree(edges):
    for edge in edges:
        if not is_isthmus(edge, edges):
            return spanning_tree(edges - {edge})
    return edges

def rank_possible_edge(edge, vertices, edges, disconnections):
    truev = len(find_possible_connections(vertices, edges | {edge}, disconnections))
    falsev = len(find_possible_connections(vertices, edges, disconnections | {edge}))
    return truev * falsev

def most_valuable_edge(vertices, edges, disconnections):
    ranker = lambda e: rank_possible_edge(e, vertices, edges, disconnections)
    return max(find_possible_connections(vertices, edges, disconnections), key=ranker)

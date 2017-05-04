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

def is_separated(a, b, edges, disconnections):
    '''Check that a and b will remain not connected even if edges are added to
    the graph, as long as the vertex pairs listed in disconnections remain
    disconected.'''
    return any((p, q) in disconnections
               for p in upward_closure(a, edges)
               for q in downward_closure(b, edges))

def find_possible_connections(vertices, edges, disconnections):
    '''Find which edges can be added to create new connections, without
    connecting any pairs in disconnections.'''
    return {(a, b) for a in vertices for b in vertices if
            not is_connected(a, b, edges) and
            not is_separated(a, b, edges, disconnections)}

def is_isthmus(edge, edges):
    return not is_connected(*edge, edges - {edge})

def spanning_tree(edges):
    for edge in edges:
        if not is_isthmus(edge, edges):
            return spanning_tree(edges - {edge})
    return edges

def evaluate_possible_edge(edge, vertices, edges, disconnections):
    evaluator = lambda x, y: len(find_possible_connections(vertices, x, y))
    unknown = evaluator(edges, disconnections)
    exists_learned = unknown - evaluator(edges | {edge}, disconnections)
    not_exists_learned = unknown - evaluator(edges, disconnections | {edge})
    return exists_learned,  not_exists_learned

def find_evaluated_connections(vertices, edges, disconnections):
    return {e: evaluate_possible_edge(e, vertices, edges, disconnections)
            for e in find_possible_connections(vertices, edges, disconnections)}

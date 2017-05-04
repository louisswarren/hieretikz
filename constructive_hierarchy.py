'''Reason about a directed graph in which the (non-)existance of some edges
must be inferred by the disconnectedness of certain vertices. Collect (truthy)
evidence for boolean function return values.'''

def transitive_closure_dict(vertices, edges):
    '''Find the transitive closure of a dict mapping vertices to their paths.'''
    neighbours = {b: vertices[a] + ((a, b),)
                  for a, b in edges if a in vertices}
    if set(neighbours).issubset(set(vertices)):
        return vertices
    return transitive_closure_dict(dict(vertices, **neighbours), edges)

def transitive_closure(vertex, edges):
    closure = transitive_closure_dict({vertex: ()}, edges)
    # Use a (truthy) loop instead of an empty path
    closure[vertex] = (vertex, vertex)
    return closure

def downward_closure(vertex, edges):
    '''Find the downward closure of a vertex.'''
    return transitive_closure(vertex, edges)

def upward_closure(vertex, edges):
    '''Find the upward closure of a vertex.'''
    return transitive_closure(vertex, {(b, a) for a, b in edges})

def is_connected(a, b, edges):
    '''Check if there is a path from a to b.'''
    return downward_closure(a, edges).get(b, False)

def is_separated(a, b, edges, disconnections):
    '''Check that a and b will remain not connected even if edges are added to
    the graph, as long as the vertex pairs listed in disconnections remain
    disconected.'''
    a_upward = upward_closure(a, edges)
    b_downward = downward_closure(b, edges)
    for p in a_upward:
        for q in b_downward:
            if (p, q) in disconnections:
                return a_upward[p], b_downward[q]
    return False

def find_possible_connections(vertices, edges, disconnections):
    '''Find which edges can be added to create new connections, without
    connecting any pairs in disconnections.'''
    return {(a, b) for a in vertices for b in vertices if
            not is_connected(a, b, edges) and
            not is_separated(a, b, edges, disconnections)}

def is_redundant_edge(edge, edges):
    '''Give alternate path if one exists.'''
    return is_connected(*edge, edges - {edge})

def spanning_tree(edges):
    for edge in edges:
        if is_redundant_edge(edge, edges):
            return spanning_tree(edges - {edge})
    return edges

def rank_possible_edge(edge, vertices, edges, disconnections):
    evaluator = lambda x, y: len(find_possible_connections(vertices, x, y))
    exists_rank = evaluator(edges | {edge}, disconnections)
    not_exists_rank = evaluator(edges, disconnections | {edge})
    return abs(exists_rank) + abs(not_exists_rank)

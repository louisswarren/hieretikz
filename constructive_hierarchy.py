'''Reason about a directed graph in which the (non-)existence of some edges
must be inferred by the disconnectedness of certain vertices. Collect (truthy)
evidence for boolean function return values.'''

def transitive_closure_dict(known_vertices, edges):
    '''Find the transitive closure of a dict mapping vertices to their paths.'''
    found_vertices = {b: known_vertices[a] + ((a, b),)
                      for a, b in edges if a in known_vertices}
    if all(v in known_vertices for v in found_vertices):
        return known_vertices
    found_vertices.update(known_vertices)
    return transitive_closure_dict(found_vertices, edges)

def transitive_closure(vertex, edges):
    closure = transitive_closure_dict({vertex: ()}, edges)
    # Use a (truthy) loop instead of an empty path
    closure[vertex] = (vertex, vertex),
    return closure

def downward_closure(vertex, edges):
    '''Find the downward closure of a vertex.'''
    return transitive_closure(vertex, edges)

def _reverse_edges(edges):
    if isinstance(edges, dict):
        return {(b, a): edges[(a, b)] for a, b in edges}
    return type(edges)((b, a) for a, b in edges)

def upward_closure(vertex, edges):
    '''Find the upward closure of a vertex.'''
    reversed_paths = transitive_closure(vertex, _reverse_edges(edges))
    return {v: _reverse_edges(p) for v, p in reversed_paths.items()}

def is_connected(a, b, edges):
    '''Check if there is a path from a to b.'''
    return downward_closure(a, edges).get(b, False)

def is_separated(a, b, edges, disconnections):
    '''Check that a and b will remain not connected even if edges are added to
    the graph, as long as the vertex pairs listed in disconnections remain
    disconnected.'''
    for p, path_from_p_to_a in upward_closure(a, edges).items():
        for q, path_from_b_to_q in downward_closure(b, edges).items():
            if (p, q) in disconnections:
                return path_from_p_to_a, path_from_b_to_q
    return False

def find_possible_connections(vertices, edges, disconnections):
    '''Find which edges can be added to create new connections, without
    connecting any pairs in disconnections.'''
    return {(a, b) for a in vertices for b in vertices
            if not is_connected(a, b, edges)
            if not is_separated(a, b, edges, disconnections)}

def is_redundant_edge(edge, edges):
    '''Give alternate path if one exists.'''
    return is_connected(*edge, edges - {edge})

def spanning_tree(edges):
    for edge in edges:
        if is_redundant_edge(edge, edges):
            return spanning_tree(edges - {edge})
    return edges

def evaluate_possible_edge(edge, vertices, edges, disconnections):
    evaluator = lambda x, y: len(find_possible_connections(vertices, x, y))
    unknown = evaluator(edges, disconnections)
    exists_learned = unknown - evaluator(edges | {edge}, disconnections)
    not_exists_learned = unknown - evaluator(edges, disconnections | {edge})
    return exists_learned, not_exists_learned

def find_evaluated_connections(vertices, edges, disconnections):
    return {e: evaluate_possible_edge(e, vertices, edges, disconnections)
            for e in find_possible_connections(vertices, edges, disconnections)}

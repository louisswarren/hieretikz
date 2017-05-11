'''Reason about a directed graph in which the (non-)existence of some edges
must be inferred by the disconnectedness of certain vertices.'''

import functools

_cache_memory = {}
def _cache(f):
    @functools.wraps(f)
    def inner(*args):
        frozen_args = []
        for arg in args:
            if type(arg) is set:
                frozen_args.append(frozenset(arg))
            elif type(arg) is list:
                frozen_args.append(tuple(arg))
            else:
                frozen_args.append(arg)
        key = (f, tuple(frozen_args))
        if key not in _cache_memory:
            _cache_memory[key] = f(*frozen_args)
        return _cache_memory[key]
    return inner

def transitive_closure_dict(known_vertices, edges):
    '''Find the transitive closure of a dict mapping vertices to their paths.'''
    found_vertices = {b: known_vertices[a] + ((a, b),)
                      for a, b in edges if a in known_vertices}
    if all(v in known_vertices for v in found_vertices):
        return known_vertices
    found_vertices.update(known_vertices)
    return transitive_closure_dict(found_vertices, edges)

@_cache
def transitive_closure(vertex, edges):
    '''Find the transitive closure of a vertex.'''
    closure = transitive_closure_dict({vertex: ()}, edges)
    # Use a (truthy) loop instead of an empty path
    closure[vertex] = (vertex, vertex),
    return closure

@_cache
def downward_closure(vertex, edges):
    '''Find the downward closure of a vertex.'''
    return transitive_closure(vertex, edges)

@_cache
def _reverse_edges(edges):
    if isinstance(edges, dict):
        return {(b, a): edges[(a, b)] for a, b in edges}
    return type(edges)((b, a) for a, b in edges)

@_cache
def upward_closure(vertex, edges):
    '''Find the upward closure of a vertex.'''
    reversed_paths = transitive_closure(vertex, _reverse_edges(edges))
    return {v: _reverse_edges(p) for v, p in reversed_paths.items()}

@_cache
def is_connected(a, b, edges):
    '''Find a (truthy) path from a to b if one exists.'''
    return downward_closure(a, edges).get(b, False)

@_cache
def is_separated(a, b, edges, disconnections):
    '''Find a (truthy) reason why a and b are separated, if one exists.

    Vertices a and b are separated if they will remain not connected even if
    edges are added to the graph, as long as the vertex pairs listed in
    disconnections remain disconnected. If there are paths p -> a and b -> q,
    and p and q are disconnected, then a and b are separated, and the two paths
    are the reason.'''
    for p, path_from_p_to_a in upward_closure(a, edges).items():
        for q, path_from_b_to_q in downward_closure(b, edges).items():
            if (p, q) in disconnections:
                return path_from_p_to_a, path_from_b_to_q
    return False

@_cache
def find_possible_connections(vertices, edges, disconnections):
    '''Find all new consistent connecting edges.

    Finds all edges that would connect currently disconnected vertices, and
    that can be added without connecting any pairs in disconnections.'''
    return {(a, b) for a in vertices for b in vertices
            if not is_connected(a, b, edges)
            if not is_separated(a, b, edges, disconnections)}

@_cache
def is_redundant_edge(edge, edges):
    '''Give alternate path if one exists.'''
    return is_connected(*edge, edges - {edge})

def spanning_tree(edges):
    '''Find a spanning tree for a graph.'''
    for edge in sorted(edges):
        if is_redundant_edge(edge, edges):
            return spanning_tree(edges - {edge})
    return edges

@_cache
def evaluate_possible_edge(edge, vertices, edges, disconnections):
    '''Find the value of knowing about the existence of an edge.

    Returns a tuple, giving the number of possible connections eliminated if
    the edge exists, and the number eliminated if the edge doesn't exist.'''
    evaluator = lambda x, y: len(find_possible_connections(vertices, x, y))
    unknown = evaluator(edges, disconnections)
    exists_learned = unknown - evaluator(edges | {edge}, disconnections)
    not_exists_learned = unknown - evaluator(edges, disconnections | {edge})
    return exists_learned, not_exists_learned

@_cache
def find_evaluated_connections(vertices, edges, disconnections):
    '''Find all new consistent connecting edges and their evaluations.

    Finds all edges that would connect currently disconnected vertices, and
    that can be added without connecting any pairs in disconnections. The
    evaluations of the edges are given by evaluate_possible_edge.'''
    return {e: evaluate_possible_edge(e, vertices, edges, disconnections)
            for e in find_possible_connections(vertices, edges, disconnections)}

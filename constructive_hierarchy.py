'''Reason about a directed graph in which the (non-)existence of some edges
must be inferred by the disconnectedness of certain vertices.'''

import functools
import hierarchy

def transitive_closure_dict(known_vertices, edges):
    '''Find the transitive closure of a dict mapping vertices to their paths.'''
    found_vertices = {b: known_vertices[a] + ((a, b),)
                      for a, b in edges if a in known_vertices}
    if all(v in known_vertices for v in found_vertices):
        return known_vertices
    found_vertices.update(known_vertices)
    return transitive_closure_dict(found_vertices, edges)

def transitive_closure(vertex, edges):
    '''Find the transitive closure of a vertex.'''
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
    '''Find a (truthy) path from a to b if one exists.'''
    return downward_closure(a, edges).get(b, False)

def find_possible_connections(vertices, edges, models):
    '''Find all new consistent connecting edges.

    Finds all edges that would connect currently disconnected vertices, and
    that can be added without connecting any pairs in disconnections.'''
    return {(a, b) for a in vertices for b in vertices
            if not is_connected(a, b, edges)
            if not hierarchy.is_separated({a}, {b}, edges, models)}

def is_redundant_edge(edge, edges):
    '''Give alternate path if one exists.'''
    return is_connected(*edge, edges - {edge})

def spanning_tree(edges):
    '''Find a spanning tree for a graph.'''
    for edge in sorted(edges):
        if is_redundant_edge(edge, edges):
            return spanning_tree(edges - {edge})
    return edges

def evaluate_possible_edge(edge, vertices, edges, models):
    '''Find the value of knowing about the existence of an edge.

    Returns a tuple, giving the number of possible connections eliminated if
    the edge exists, and the number eliminated if the edge doesn't exist.'''
    return 0, 0

def find_evaluated_connections(vertices, edges, models):
    '''Find all new consistent connecting edges and their evaluations.

    Finds all edges that would connect currently disconnected vertices, and
    that can be added without connecting any pairs in disconnections. The
    evaluations of the edges are given by evaluate_possible_edge.'''
    return {e: evaluate_possible_edge(e, vertices, edges, models)
            for e in find_possible_connections(vertices, edges, models)}

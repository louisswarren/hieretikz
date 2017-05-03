"""Reason about a directed graph in which the (non-)existance of some edges
must be inferred by the disconnectedness of certain vertices"""

def transitive_closure_set(vertices, edges):
    neighbours = {b for a, b in edges if a in vertices}
    if neighbours.issubset(vertices):
        return vertices
    return transitive_closure_set(vertices | neighbours, edges)

def downward_closure(vertex, edges):
    return transitive_closure_set({vertex}, edges)

def upward_closure(vertex, edges):
    return transitive_closure_set({vertex}, {(b, a) for a, b in edges})

def is_connected(a, b, edges):
    return b in downward_closure(a, edges)

def is_separated(a, b, edges, disconnections):
    """Checks that a and b will remain not connected, even if edges are added
    to the graph, as long as the vertex pairs listed in disconnections remain
    disconected."""
    if (a, b) in disconnections:
        return True
    # Removing the alternate closures removes the relevant vertex, and avoids
    # any cycle issues
    above_a = upward_closure(a, edges) - downward_closure(a, edges)
    below_b = downward_closure(b, edges) - upward_closure(b, edges)
    for p in above_a:
        for q in below_b:
            if is_separated(p, q, edges, disconnections):
                return True
    return False

def find_possible_edges(vertices, edges, disconnections):
    """Find which edges can be added without connecting any pairs in
    disconnections."""
    return {(a, b) for a in vertices for b in vertices
            if a != b and is_separated(a, b, edges, disconnections)}

def is_isthmus(edge, edges):
    a, b = edge
    return not downward_closure(a, edges - {edge}) == downward_closure(a, edges)

def spanning_tree(edges):
    for edge in edges:
        if not is_isthmus(edge, edges):
            return spanning_tree(edges - {edge})
    return edges

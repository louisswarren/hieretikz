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

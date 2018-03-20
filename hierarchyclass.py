def ArrowLoopError(tails, head, name):
    name_msg = name and f"'{name}': "
    message = 'Loop arrow {}{} -> {}'.format(name_msg, ','.join(tails), head)
    return Exception(message)

def TierOverlapError(low, high, name):
    name_msg = name and f"'{name}': "
    message = 'Tier overlap {}{} // {}'.format(name_msg, low, high)
    return Exception(message)

class Arrow:
    def __init__(self, tails, head, name=''):
        if head in tails:
            raise ArrowLoopError(tails, head, name)
        self.tails = tails
        self.head = head
        self.name = name

    def all_tails_in(self, preds):
        return all(self.tails in preds)

    def under_quotient(self, node):
        reduced_tails = frozenset(x for x in self.tails if x != node)
        return Arrow(reduced_tails, self.head, self.name)

class Tier:
    def __init__(self, low, high, name=''):
        if set(low).intersection(set(high)):
            raise TierOverlapError(low, high, name)
        self.low = low
        self.high = high
        self.name = name

    def has_foundation(self, node):
        return node in self.low

class Hierarchy:
    def __init__(self, arrows, tiers):
        self.arrows = frozenset(arrows)
        self._closure_cache = {}
        self.tiers = frozenset(self.complete_tier(tier) for tier in tiers)

    def _closure_paths(self, paths):
        frontier = {y: ((xs, y), *(paths[x] for x in arrow.tails if paths[x]))
                    for arrow in self.arrows if arrow.all_tails_in(paths)}
        if all(found in paths for found in frontier):
            return paths
        frontier.update(paths)
        return self._closure_paths(frontier)

    def closure(self, nodes):
        node_set = frozenset(nodes)
        if node_set not in self._closure_cache:
            paths = self._closure_paths({x: () for x in nodes})
            self._closure_cache[node_set] = paths
        return self._closure_cache[node_set]

    def simple_upwards_closure(self, node):
        pass


    def complete_tier(self, tier):
        clow = frozenset(self.closure(tier.low))
        chigh = NotImplementedError
        raise chigh
        return Tier(clow, chigh, tier.name)

    def under_quotient(self, node):
        arrows = frozenset(arrow.under_quotient(node) for arrow in self.arrows)
        tiers = frozenset(tier for tier in tiers if tier.has_foundation(node))
        return Hierarchy(arrows, tiers)

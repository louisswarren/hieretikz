_compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

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
        self.tails = frozenset(tails)
        self.head = frozenset(head)
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
        self.low = frozenset(low)
        self.high = frozenset(high)
        self.name = name

    def has_foundation(self, node):
        return node in self.low

    def all_low(self, *nodes):
        return all(node in self.low for node in nodes)

    def all_high(self, *nodes):
        return all(node in self.high for node in nodes)

class Hierarchy:
    def __init__(self, arrows, tiers):
        self.arrows = frozenset(arrows)
        self._closure_cache = {}
        # Precompute all single closures
        self.single_closures = {}
        for tails, head in self.arrows:
            for tail in tails:
                self.single_closures[tail] = self.closure(tail)
            self.single_closures[head] = self.closure(head)
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

    @_compose(frozenset)
    def simple_upwards_closure(self, node):
        # Use the fact that single closures have been precomputed
        for root, closure in self.single_closures.items():
            if node in closure:
                yield root

    def complete_tier(self, tier):
        clow = self.closure(tier.low)
        chigh = set().union(self.simple_upwards_closure(x) for x in tier.high)
        return Tier(clow, chigh, tier.name)

    def find_qarrows(self, nodes, order=1):
        for r in range(1, order + 1):
            for tails in itertools.combinations(nodes, r):
                for head in nodes:
                    premise = frozenset(tails)
                    if head in self.closure(tails):
                        continue
                    elif any(tier.all_high(head) and tier.all_low(*tails)
                            for tier in self.tiers):
                        continue
                    else:
                        yield Arrow(tails, head)

    def under_quotient(self, node):
        arrows = frozenset(arrow.under_quotient(node) for arrow in self.arrows)
        tiers = frozenset(tier for tier in tiers if tier.has_foundation(node))
        return Hierarchy(arrows, tiers)

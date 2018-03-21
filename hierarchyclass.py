import itertools

_compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

def TierOverlapError(low, high, name):
    name_msg = name and f"'{name}': "
    message = 'Tier overlap {}{} // {}'.format(name_msg, low, high)
    return Exception(message)

class Arrow:
    def __init__(self, tails, head, name=''):
        self.tails = frozenset(tails)
        self.head = head
        self.name = name
        if head in tails:
            raise Exception(f'Loop arrow {self}')

    @property
    def edge(self):
        return tuple(self.tails) + (self.head,)

    def __str__(self):
        name_msg = self.name and f"'{self.name}': "
        return '{}{} -> {}'.format(name_msg, ','.join(self.tails), self.head)

    def all_tails_in(self, preds):
        return all(tail in preds for tail in self.tails)

    def under_quotient(self, node):
        reduced_tails = frozenset(x for x in self.tails if x != node)
        return Arrow(reduced_tails, self.head, self.name)

class Tier:
    def __init__(self, low, high, name=''):
        self.low = frozenset(low)
        self.high = frozenset(high)
        self.name = name
        if set(low).intersection(set(high)):
            raise Exception(f'Tier overlap {self}')

    def __str__(self):
        name_msg = self.name and f"'{self.name}': "
        return '{}{} // {}'.format(name_msg, ','.join(self.low), self.high)

    def has_foundation(self, node):
        return node in self.low

    def all_low(self, *nodes):
        return all(node in self.low for node in nodes)

    def all_high(self, *nodes):
        return all(node in self.high for node in nodes)

class Hierarchy:
    def __init__(self, arrows, tiers):
        self.arrows = frozenset(arrows)
        # Precompute all single closures
        self.single_closures = {}
        for arrow in self.arrows:
            for tail in arrow.tails:
                self.single_closures[tail] = self.closure(tail)
            self.single_closures[arrow.head] = self.closure(arrow.head)
        self.tiers = frozenset(self.complete_tier(tier) for tier in tiers)

    def _closure_paths(self, paths):
        frontier = {arrow.head: (arrow, *(paths[x] for x in arrow.tails if paths[x]))
                    for arrow in self.arrows if arrow.all_tails_in(paths)}
        if all(found in paths for found in frontier):
            return paths
        frontier.update(paths)
        return self._closure_paths(frontier)

    def closure(self, nodes):
        node_set = frozenset(nodes)
        return self._closure_paths({x: () for x in nodes})

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

    @_compose(frozenset)
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

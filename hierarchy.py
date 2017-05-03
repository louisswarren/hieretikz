compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))
trace = lambda f: lambda *a: print('{}({}) -> {}'.format(f.__name__, ', '.join(map(repr, a)), repr(f(*a)))) or f(*a)

va, vb, vp, vq, vr, vx, vy, vz = 'a b p q r x y z'.split()
edges = {
    (vp, va),
    (vp, vr),
    (vq, vr),
    (vr, va),
    (vb, vx),
    (vb, vy),
    (vx, vz),
    (vy, vz),
}


def transitive_closure_set(vertices, edges):
    neighbours = {b for a, b in edges if a in vertices}
    if neighbours.issubset(vertices):
        return vertices
    return transitive_closure_set(vertices | neighbours, edges)

def downward_closure(vertex, edges):
    return transitive_closure_set({vertex}, edges)

def upward_closure(vertex, edges):
    return transitive_closure_set({vertex}, {(b, a) for a, b in edges})


def test(f, *args, **kwargs):
    args_str = ', '.join(map(repr, args))
    kwargs_str = ', '.join('{}={}'.format(k, repr(kwargs[k])) for k in kwargs)
    full_args_str = ', '.join(s for s in (args_str, kwargs_str) if s)
    def inner(expected):
        result = f(*args, **kwargs)
        test_str = "{}({}) -> {}".format(f.__name__, full_args_str, result)
        if result == expected:
            print("Pass:", test_str)
        else:
            print("FAIL:", test_str)
        return not result == expected
    return inner

def test_all():
    class _quiet_set(set):
        __repr__ = lambda s: 'quiet'
    qedges = _quiet_set(edges)

    yield test(downward_closure, vb, qedges)({vb, vx, vy, vz})

def run_tests():
    failures = sum(test_all())
    if failures:
        print()
        print("{} test cases FAILED".format(failures))

if __name__ == '__main__':
    run_tests()

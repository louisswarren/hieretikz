from hierarchy import *

compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))
trace = lambda f: lambda *a: print('{}({}) -> {}'.format(f.__name__, ', '.join(map(repr, a)), repr(f(*a)))) or f(*a)

va, vb, vp, vq, vr, vx, vy, vz = 'a b p q r x y z'.split()
'''
    vp -- > vq
     |      |
     v      v
    va <--> vr
     ?
     ?
     ?
    vb --> vx
     |      |
     v      v
    vy --> vz
'''
edges = {
    (vp, va),
    (vp, vq),
    (vq, vr),
    (vr, va),
    (va, vr),
    (vb, vx),
    (vb, vy),
    (vx, vz),
    (vy, vz),
}

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
    yield test(is_connected, vp, va, qedges)(True)
    yield test(is_connected, vx, vb, qedges)(False)
    yield test(is_separated, va, vb, qedges, {(vq, vz)} )(True)
    yield test(is_separated, va, vb, qedges, {(vq, va)} )(False)
    yield test(is_separated, vb, vy, qedges, set())(False)

def run_tests():
    failures = sum(test_all())
    if failures:
        print()
        print("{} test cases FAILED".format(failures))

if __name__ == '__main__':
    run_tests()

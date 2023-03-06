#!/usr/bin/env python3
import os
import quiz
import pickle
import types
import pytest
import pprint

import sys
if '.' not in sys.path:
    sys.path.insert(0, '.')
sys.setrecursionlimit(3000)

from search import search


TEST_DIRECTORY = os.path.dirname(__file__)

##################################################
#  Problem 1
##################################################

def _run_mode_test(n):
    with open(os.path.join(TEST_DIRECTORY, 'test_data', 'mode_%02d_in.pickle' % n), 'rb') as f:
        inputs = pickle.load(f)

    results = [quiz.grid_mode(inp) for inp in inputs]

    with open(os.path.join(TEST_DIRECTORY, 'test_data', 'mode_%02d_out.pickle' % n), 'rb') as f:
        expected = pickle.load(f)

    for inp, res, exp in zip(inputs, results, expected):
        assert res == exp, "With input:\n%s\n\nexpected:\n%s\n\nbut got:\n%s\n\n" % (pprint.pformat(inp), pprint.pformat(exp), pprint.pformat(res))


@pytest.mark.parametrize('testnum', list(range(5)))
def test_problem1_large(testnum):
    _run_mode_test(testnum)




##################################################
#  Problem 2
##################################################

def one(r, c, slope_r, slope_c):
    def o(t):
        return (r + slope_r*t, c + slope_c*t)
    return o

def two(locs):
    return lambda t: locs[t % len(locs)]

def three(row, col, length):
    def _(t):
        q, r = divmod(t, length)
        m = q % 4
        if m == 0:
            return (row, col + r)
        elif m == 1:
            return (row + r, col + length)
        elif m == 2:
            return (row + length, col + length - r)
        else:
            return (row + length - r, col)
    return _

def four(r, cs, m):
    return lambda t: (r, (cs * t) % m)

bus_funcs = [one, two, three, four]

def _valid_path(ptest, path, sl, sched):
    if not path:
        return False, "For inputs %s, expected a path but got %r" % (ptest, path)

    if path[0] != sl:
        return False, "For inputs %s, expected path to start with %r, not %r" % (ptest, sl, path[0])

    if path[-1] != sched(len(path)-1):
        return False, "For inputs %s, path does not end at the bus's location (ends with %r at time %r, but bus is at %r)" % (ptest, path[-1], len(path)-1, sched(len(path)-1))

    if not all(abs(r1-r2) <= 1 and abs(c1-c2) <= 1 for ((r1, c1), (r2, c2)) in zip(path, path[1:])):
        return False, "For inputs %s, illegal moves exist in path %r" % (ptest, path)

    return True, 'yay!'


def catch_bus(start_location, bus_schedule_function):
    result = search(*quiz.setup_bus_catcher(start_location, bus_schedule_function))
    return quiz.interpret_result(result)

def _print_test(f, args, sl):
    return '(%r, bus_funcs[%d]%s)' % (sl, f, args)

def _run_bus_test(n):
    with open(os.path.join(TEST_DIRECTORY, 'test_data', 'bus_%02d_in.pickle' % n), 'rb') as f:
        inputs = pickle.load(f)

    tests = []
    results = []
    prints = []
    for (f, args, sl) in inputs:
        sched = bus_funcs[f](*args)
        tests.append((sl, sched))
        prints.append(_print_test(f, args, sl))
        results.append(catch_bus(sl, sched))

    with open(os.path.join(TEST_DIRECTORY, 'test_data', 'bus_%02d_out.pickle' % n), 'rb') as f:
        expected = pickle.load(f)

    for test, ptest, res, exp in zip(tests, prints, results, expected):
        assert res is not None, "For inputs %s, expected a path but got None" % (ptest,)
        assert len(res) == exp, "For inputs %s, expected a path of length %d but got length %d" % (ptest, exp, len(res))
        path_ok, msg = _valid_path(ptest, res, *test)
        assert path_ok, msg


@pytest.mark.parametrize('testnum', list(range(4)))
def test_problem2_large(testnum):
    _run_bus_test(testnum)


##################################################
#  Problem 3
##################################################

def _run_boggle_test(n):
    with open(os.path.join(TEST_DIRECTORY, 'test_data', 'boggle_%02d_in.pickle' % n), 'rb') as f:
        inputs = pickle.load(f)

    results = [quiz.words_at_location(*inp) for inp in inputs]

    with open(os.path.join(TEST_DIRECTORY, 'test_data', 'boggle_%02d_out.pickle' % n), 'rb') as f:
        expected = pickle.load(f)

    for inp, res, exp in zip(inputs, results, expected):
        assert res == exp, "With inputs:\n%s\n\nexpected:\n%s\n\nbut got:\n%s\n\n" % (pprint.pformat(inp), pprint.pformat(exp), pprint.pformat(res))


@pytest.mark.parametrize('testnum', list(range(5)))
def test_problem3_large(testnum):
    _run_boggle_test(testnum)




if __name__ == '__main__':
    import sys
    import json

    class TestData:
        def __init__(self):
            self.results = {'passed': []}

        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtestloop(self, session):
            yield

        def pytest_runtest_logreport(self, report):
            if report.when != 'call':
                return
            self.results.setdefault(report.outcome, []).append(report.head_line)

        def pytest_collection_finish(self, session):
            self.results['total'] = [i.name for i in session.items]

        def pytest_unconfigure(self, config):
            print(json.dumps(self.results))

    if os.environ.get('CATSOOP'):
        args = ['--color=yes', '-v', __file__]
        if len(sys.argv) > 1:
            args = ['-k', sys.argv[1], *args]
        kwargs = {'plugins': [TestData()]}
    else:
        args = ['-v', __file__]
        if len(sys.argv) > 1:
            args = ['-k', sys.argv[1], *args]
        kwargs = {}
    res = pytest.main(args, **kwargs)


#!/usr/bin/env python3
import os, types
from copy import deepcopy
import quiz

TEST_DIRECTORY = os.path.dirname(__file__)

import pytest

#############
# Problem 1 #
#############

graph1 = {1: {2, 4, 5},
          2: {1, 8},
          4: {2, 7},
          7: {9},
          9: set(),
          5: {9},
          8: set(),}

def verify_path(graph, start, end, path, expect):
    case = "\n(case: graph = "+repr(graph)+", start = "+str(start)+", end = "+str(end)+")"
    if expect is None:
        assert path is None, "got a non-None path, where one does not exist"+case
        return
    else:
        assert path is not None, case
    assert len(path) > 0, "expected valid path with at least some nodes"+case
    for node in path:
        assert node in graph, "node "+str(node)+" does not exist in graph"+case
    assert start == path[0], "path does not begin with node "+str(start)+case
    assert end == path[-1], "path does not end with node "+str(end)+case
    for from_node, next_node in zip(path, path[1:]):
        assert next_node in graph[from_node], "no edge from "+str(from_node)+" to "+str(next_node)+case
        assert next_node > from_node, "node values not in ascending order!"+case

def test_problem1_01():
    g = deepcopy(graph1)
    start, end = 2, 2; expect = [2]
    result = quiz.ascending_path(deepcopy(g), start, end)
    verify_path(g, start, end, result, expect)

def test_problem1_02():
    g = graph1
    start, end = 1, 2; expect = [1, 2]
    result = quiz.ascending_path(deepcopy(g), start, end)
    verify_path(g, start, end, result, expect)

    start, end = 2, 1; expect = None
    result = quiz.ascending_path(deepcopy(g), start, end)
    verify_path(g, start, end, result, expect)

def test_problem1_03():
    g = graph1
    start, end = 1, 7; expect = [1, 4, 7]
    result = quiz.ascending_path(deepcopy(g), start, end)
    verify_path(g, start, end, result, expect)

    start, end = 2, 7; expect = None
    result = quiz.ascending_path(deepcopy(g), start, end)
    verify_path(g, start, end, result, expect)

    start, end = 4, 8; expect = None
    result = quiz.ascending_path(deepcopy(g), start, end)
    verify_path(g, start, end, result, expect)

def test_problem1_04():
    g = graph1
    start, end = 1, 9; expect = [1, 4, 7, 9] #or [1, 5, 9]
    result = quiz.ascending_path(deepcopy(g), start, end)
    verify_path(g, start, end, result, expect)

def test_problem1_05():
    g = graph1
    start, end = 1, 8; expect = [1, 2, 8]
    result = quiz.ascending_path(deepcopy(g), start, end)
    verify_path(g, start, end, result, expect)

def test_problem1_06():
    # long graph
    start, end = 1, 11
    elts = list(range(start, end+1, 2))
    graph = {}
    for a,b in zip(elts, elts[1:]):
        graph.setdefault(a,set()).add(b)
        graph.setdefault(b,set()).add(a)
    result = quiz.ascending_path(deepcopy(graph), start, end)
    verify_path(graph, start, end, result, True)

def test_problem1_07():
    # big graph
    start, end = 1, 100*3+1
    elt = list(range(start, end+1, 3))
    graph = {}
    for a,b in zip(elt, elt[1:]):
        graph.setdefault(a,set()).add(b)
        graph.setdefault(b,set()).add(a)
        c = a+1
        graph.setdefault(a,set()).add(c)
        graph.setdefault(c,set()).add(a)
        d = c+1
        graph.setdefault(c,set()).add(d)
        graph.setdefault(d,set()).add(c)
    result = quiz.ascending_path(deepcopy(graph), start, end)
    verify_path(graph, start, end, result, True)


#############
# Problem 2 #
#############

def _run_test(n):
    in_fname = os.path.join(TEST_DIRECTORY, 'test_data',
                            'phone_%d_in.pyobj' % (n,))
    with open(in_fname, encoding='utf-8') as f:
        inp = eval(f.read())
    out_fname = os.path.join(TEST_DIRECTORY, 'test_data',
                             'phone_%d_out.pyobj' % (n,))
    with open(out_fname, encoding='utf-8') as f:
        expected = eval(f.read())

    result = get_result(inp)
    assert result == expected


def get_result(inp):
    return quiz.phone_words(inp)

def test_problem2_01():
    _run_test(1)

def test_problem2_02():
    _run_test(2)

def test_problem2_03():
    _run_test(3)

def test_problem2_04():
    _run_test(4)

def test_problem2_05():
    _run_test(5)

def test_problem2_06():
    _run_test(6)

def test_problem2_07():
    _run_test(7)

def test_problem2_08():
    _run_test(8)


#############
# Problem 3 #
#############

def repeat_function(num_repeats, f, *args):
    for i in range(num_repeats):
        f(*args)

def test_problem3_01():
    # simple case
    mitube = quiz.MITube()
    mitube.upload_video('generators', 'srini')
    mitube.view('generators')
    mitube.upload_video('recursion', 'erik')
    mitube.view('recursion')
    mitube.view('recursion')

    assert 'recursion' == mitube.get_top_video()
    assert 'erik' == mitube.get_top_user()

def test_problem3_02():
    # tied for top video and user
    mitube = quiz.MITube()
    mitube.upload_video('generators', 'srini')
    mitube.view('generators')
    mitube.upload_video('interfaces', 'srini')
    mitube.view('interfaces')
    mitube.upload_video('recursion', 'erik')
    mitube.view('recursion')
    mitube.view('recursion')
    mitube.upload_video('chewing_wood', 'timthebeaver')
    mitube.view('chewing_wood')
    mitube.view('chewing_wood')

    assert 'chewing_wood' == mitube.get_top_video()
    assert 'erik' == mitube.get_top_user()

def test_problem3_03():
    # value error is raised
    mitube = quiz.MITube()
    mitube.upload_video('generators', 'srini')
    with pytest.raises(ValueError):
        mitube.view('recursion')

def test_problem3_04():
    # more commands
    mitube = quiz.MITube()
    mitube.upload_video('generators', 'srini')
    mitube.view('generators')
    mitube.upload_video('interfaces', 'srini')
    mitube.view('interfaces')
    with pytest.raises(ValueError):
        mitube.view('recursion')
    mitube.upload_video('recursion', 'erik')
    mitube.view('recursion')
    mitube.view('recursion')
    mitube.upload_video('chewing_wood', 'timthebeaver')
    mitube.view('chewing_wood')
    assert 'recursion' == mitube.get_top_video()
    assert 'recursion' == mitube.get_top_video()
    mitube.view('chewing_wood')
    assert 'chewing_wood' == mitube.get_top_video()
    assert 'erik' == mitube.get_top_user()
    mitube.upload_video('mutation', 'srini')
    mitube.upload_video('nesting', 'srini')
    assert 'erik' == mitube.get_top_user()
    with pytest.raises(ValueError):
        mitube.view('sorting')
    mitube.view('recursion')
    mitube.view('interfaces')
    mitube.view('interfaces')
    mitube.view('interfaces')
    assert 'interfaces' == mitube.get_top_video()
    assert 'srini' == mitube.get_top_user()

def test_problem3_05():
    # lots of commands
    mitube = quiz.MITube()
    for i in range(10):
        if i % 2:
            mitube.upload_video(str(i), 'srini')
        else:
            mitube.upload_video(str(i), 'erik')

    for i in range(99999, -1, -1):
        mitube.view(str(i % 10))
        assert str(i % 10) == mitube.get_top_video()
        if i % 2:
            assert 'srini' == mitube.get_top_user()
        else:
            assert 'erik' == mitube.get_top_user()

def test_problem3_06():
    # lots of repeated commands
    mitube = quiz.MITube()
    for i in range(10, 100):
        mitube.upload_video(str(i), 'user_' + str(i//10))
    repeat_function(10000, mitube.view, '10')
    for i in range(2000):
        assert 'user_1' == mitube.get_top_user()
        assert '10' == mitube.get_top_video()
    repeat_function(5000, mitube.view, '20')
    for i in range(2000):
        assert 'user_1' == mitube.get_top_user()
        assert '10' == mitube.get_top_video()

    repeat_function(5000, mitube.view, '21')
    for i in range(2000):
        assert 'user_1' == mitube.get_top_user()
        assert '10' == mitube.get_top_video()

    repeat_function(5000, mitube.view, '20')
    for i in range(2000):
        assert 'user_2' == mitube.get_top_user()
        assert '10' == mitube.get_top_video()

    mitube.view('20')
    for i in range(2000):
        assert 'user_2' == mitube.get_top_user()
        assert '20' == mitube.get_top_video()

def test_problem3_07():
    # lots and lots of commands
    mitube = quiz.MITube()
    for i in range(100):
        if i < 10:
            mitube.upload_video('0' + str(i), 'erik')
        else:
            mitube.upload_video(str(i), 'srini')

    for i in range(499999, -1, -1):
        if i % 100 < 10:
            mitube.view('0' + str(i % 100))
            assert '0' + str(i % 100) == mitube.get_top_video()
        else:
            mitube.view(str(i % 100))
            assert str(i % 100) == mitube.get_top_video()
        assert 'srini' == mitube.get_top_user()

def test_problem3_08():
    # lots and lots of repeated commands
    mitube = quiz.MITube()
    mitube.upload_video('generators', 'srini')
    repeat_function(300000, mitube.view, 'generators')
    mitube.upload_video('interfaces', 'srini')
    repeat_function(300000, mitube.view, 'interfaces')
    with pytest.raises(ValueError):
        mitube.view('recursion')
    mitube.upload_video('recursion', 'erik')
    repeat_function(300000, mitube.view, 'recursion')
    repeat_function(300000, mitube.view, 'recursion')
    mitube.upload_video('chewing_wood', 'timthebeaver')
    repeat_function(300000, mitube.view, 'chewing_wood')
    repeat_function(300000, mitube.get_top_video)
    assert 'recursion' == mitube.get_top_video()
    repeat_function(300000, mitube.view, 'chewing_wood')
    repeat_function(300000, mitube.get_top_video)
    assert 'chewing_wood' == mitube.get_top_video()
    repeat_function(300000, mitube.get_top_user)
    assert 'erik' == mitube.get_top_user()
    mitube.upload_video('mutation', 'srini')
    mitube.upload_video('nesting', 'srini')
    repeat_function(300000, mitube.get_top_user)
    assert 'erik' == mitube.get_top_user()
    with pytest.raises(ValueError):
        mitube.view('sorting')
    repeat_function(300000, mitube.view, 'recursion')
    repeat_function(300000, mitube.view, 'interfaces')
    repeat_function(300000, mitube.view, 'interfaces')
    repeat_function(300000, mitube.view, 'interfaces')
    repeat_function(300000, mitube.get_top_video)
    assert 'interfaces' == mitube.get_top_video()
    repeat_function(300000, mitube.get_top_video)
    assert 'srini' == mitube.get_top_user()


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

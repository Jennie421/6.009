#!/usr/bin/env python3
import os
import math
import quiz
import types
import pickle
import hashlib
import random

from copy import deepcopy

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)

##################################################
#  Problem 1
##################################################

def test_problem1_examples():
    assert quiz.most_after([]) is None
    assert quiz.most_after([0]) is None
    assert quiz.most_after([0, 0]) == 0
    assert quiz.most_after([0, 1]) == 0
    assert quiz.most_after([0, 1, 0, 1]) == 1
    assert quiz.most_after([0, 1, 0, 1, 2]) == 1
    assert quiz.most_after([0, -1, 0, 1, 2]) == 0
    assert quiz.most_after([1, 1, 1, 1, 2, 2, 1]) == 2
    assert quiz.most_after([2, 2, 2, 2, 1, 1, 2]) == 2
    assert quiz.most_after(list(range(100))) == 98

    L = []
    for x in range(5,10):
        for y in range(7,14):
            for z in range(3,8):
                L.extend([x,y]*z)
    assert quiz.most_after(L) == 9


@pytest.mark.parametrize('testnum', list(range(5)))
def test_problem1_large(testnum):
    with open(os.path.join(TEST_DIRECTORY, 'test_data', f'mostafter_{testnum:02d}_in.pickle'), 'rb') as f:
        ins = pickle.load(f)

    results = [quiz.most_after(i) for i in ins]

    with open(os.path.join(TEST_DIRECTORY, 'test_data', f'mostafter_{testnum:02d}_out.pickle'), 'rb') as f:
        expected = pickle.load(f)

    for r, e in zip(results, expected):
        assert r == e


##################################################
#  Problem 2
##################################################

def _run_p2_test(length, vals, count):
    output = quiz.nonrepeating_sequences(length, type(vals)(vals))

    assert isinstance(output, types.GeneratorType), 'Expected a generator (not %s)' % type(output)
    output_set = set(output)

    assert len(output_set) == count, 'Expected %d results, but got %d' % (count, len(output_set),)

    for s in output_set:
        assert len(s) == length, "Output length (%d) does not match expected length (%d)" % (len(output_set), length)
        assert set(s).issubset(set(vals)), "Output contains values not in the original input"
        assert _check_p2(s)


def test_problem2_0():
    _run_p2_test(0, {1, 2}, 1)
    _run_p2_test(1, [7, 8], 2)
    _run_p2_test(2, (9, 10), 2)
    _run_p2_test(3, {'kangaroo', 'ferret'}, 2)
    _run_p2_test(4, ['something', 'else'], 0)

_test1_counts = [1, 3, 6, 12, 18, 30, 42, 60, 78, 108, 144, 204, 264, 342, 456,
                 618, 798, 1044, 1392, 1830, 2388, 3180, 4146, 5418, 7032]
def test_problem2_1():
    for i in range(25):
        _run_p2_test(i, 'abc', _test1_counts[i])

_test2_counts = [90, 810, 7200, 64080]
def test_problem2_2():
    for i in range(2, 6):
        _run_p2_test(i, set(range(10)), _test2_counts[i-2])

def test_problem2_3():
    result = quiz.nonrepeating_sequences(100, range(10))
    for _ in range(10):
        y = next(result)
        assert len(y) == 100
        assert set(y).issubset(set(range(10)))
        assert _check_p2(y)


##################################################
#  Problem 3
##################################################

def test_problem3_examples():
    assert _check_p3(4, quiz.find_expression(7, 4, 10)) == 7
    assert _check_p3(4, quiz.find_expression(7, 4, 4)) == 7
    assert quiz.find_expression(7, 4, 3) is None
    assert quiz.find_expression(102, 9, 5) is None
    assert _check_p3(3, quiz.find_expression(3, 3, 5)) == 3
    assert _check_p3(20, quiz.find_expression(1, 20, 5)) == 1
    assert _check_p3(20, quiz.find_expression(300, 20, 10)) == 300


def test_problem3_example_long():
    assert _check_p3(9, quiz.find_expression(102, 9, 10)) == 102


@pytest.mark.parametrize('testnum', list(range(1, 6)))
def test_problem3_medium(testnum):
    with open(os.path.join(TEST_DIRECTORY, 'test_data', f'expr_{testnum:02d}.pickle'), 'rb') as f:
        tests = pickle.load(f)

    for target, lim, res in tests:
        exp = quiz.find_expression(target, testnum, lim)
        if res is None:
            assert exp is None
        else:
            assert _check_p3(testnum, exp) == target

@pytest.mark.parametrize('testnum', list(range(6, 11)))
def test_problem3_large(testnum):
    with open(os.path.join(TEST_DIRECTORY, 'test_data', f'expr_{testnum:02d}.pickle'), 'rb') as f:
        tests = pickle.load(f)

    for target, lim, res in tests:
        exp = quiz.find_expression(target, testnum, lim)
        if res is None:
            assert exp is None
        else:
            assert _check_p3(testnum, exp) == target


##################################################
# Additional Testing Things
##################################################

from test_utils import _check_p2, _check_p3

##################################################
# Test Running
##################################################

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


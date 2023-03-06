#!/usr/bin/env python3
import json
import os
import pickle
import quiz
import unittest

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


##################################################
#  Problem 1
##################################################

def test_problem1_01():
    """Passes if anything is returned"""
    data = [1]
    result = quiz.get_mode(data)
    assert result

def test_problem1_02():
    """Single element"""
    data = [1]
    expect = 1
    result = quiz.get_mode(data)
    assert result == expect

def test_problem1_03():
    """Multiple elements, one candidate appearing twice"""
    data = [3, 94, 44, 68, 5, 44]
    expect = 44
    result = quiz.get_mode(data)
    assert result == expect

def test_problem1_04():
    """Multiple elements, two candidates appearing twice"""
    data = [57, 87, 7, 17, 34, 7, 92, 17]
    expect = 17
    result = quiz.get_mode(data)
    assert result == expect

def test_problem1_05():
    """Multiple elements, multiple candidates appearing multiple times"""
    data = [87, 0, 23, 39, 65, 0, 16, 16, 23, 16, 56, 3, 99, 0, 16, 39]
    expect = 16
    result = quiz.get_mode(data)
    assert result == expect


##################################################
#  Problem 2
##################################################

def test_problem2_01():
    """ Tests that None is returned when no words are anagrams of each other """
    N = 2
    result = quiz.find_anagram_groups(["dog", "cat", "tree", "barn"], N)
    assert result is None

def test_problem2_02():
    """ Tests that the correct index is returned when the every word is an anagram of each other """
    N = 4
    result = quiz.find_anagram_groups(['leapt', 'palet', 'plate', 'petal', 'pleat'], N)
    assert result == 3

def test_problem2_03():
    """ Tests that the correct index is returned when there are several different anagram groups """
    N = 3
    result = quiz.find_anagram_groups(['reset', 'rail', 'rated', 'terse', 'liar', 'tread', 'trade', 'lair', 'resort', 'tared'], N)
    assert result == 6

def test_problem2_04():
    """ Tests that the correct index is returned for a small N with many words """
    # Should find that steam and meats are anagrams of each other
    result = quiz.find_anagram_groups(
            ["stem", "movement", "optometry", "steam", "smith", "equal", "zebra", "horse", "cat", "dog", "python", "lisp",
            "official", "MIT", "computers", "roster", "develop", "laptop", "mouse", "water", "fire",
            "earth", "toddler", "vegetarian", "ferocity", "wolf", "branch", "tree", "lake", "river",
            "mountain", "city", "state", "country", "robust", "stereo", "overlay", "plump", "copy", "list", "array",
            "dictionary", "set", "society", "powerful", "fast", "meats", "algorithm", "cup",
            "pad", "left", "right", "key", "tuple", "resort"], 2)
    assert result == 46

def test_problem2_05():
    """ Tests that the correct index is returned for a large N with a very large number of words """
    with open(os.path.join(TEST_DIRECTORY, "test_inputs", "test_problem2_many_words.json")) as input_file:
        words = json.load(input_file)
    result = quiz.find_anagram_groups(words, 8)
    assert result == 61371


##################################################
#  Problem 3
##################################################

def test_problem3_01():
    """Tests completely full and completely empty boards."""
    board1 = (1, 1, 1, 1, 1)
    board2 = (0, 0, 0, 0, 0)
    assert 5 == quiz.minimum_pegs(board1)
    assert 0 == quiz.minimum_pegs(board2)

def test_problem3_02():
    """Tests boards with only one possible move."""
    board1 = (1, 1, 0)
    assert 1 == quiz.minimum_pegs(board1)

    board2 = (0, 1, 1)
    assert 1 == quiz.minimum_pegs(board2)

    board3 = [0]*100
    board3[0]  = 1
    board3[-1] = 1
    board3[-2] = 1
    assert 2 == quiz.minimum_pegs(tuple(board3))

def test_problem3_03():
    """Tests boards with only one possible move at a time."""
    board1 = (1, 1, 1, 0, 1)
    assert 2 == quiz.minimum_pegs(board1)

    board2 = (1, 1) + (0, 1)*100
    assert 1 == quiz.minimum_pegs(board2)

def test_problem3_04():
    """Tests boards with multiple possible moves at a time, and multiple paths to the minimum number of pegs."""
    board1 = (1, 1, 0, 1, 1)
    assert 2 == quiz.minimum_pegs(board1)

    board2 = (1, 1, 0, 1, 1) + (0,)*1000 + (1, 1, 0, 1, 1)
    assert 4 == quiz.minimum_pegs(board2)

def test_problem3_05():
    """Tests boards with multiple possible moves at a time, but only one path to the minimum number of pegs."""
    board1 = (1, 1, 1, 0, 1, 1)
    assert 2 == quiz.minimum_pegs(board1)

    board2 = (1, 1, 1) + (0, 1)*100
    assert 2 == quiz.minimum_pegs(board2)

    board3 = (1,)*20 + board1
    assert 3 == quiz.minimum_pegs(board3)


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
        args = ['-v', __file__] if len(sys.argv) == 1 else ['-v', *('%s::%s' % (__file__, i) for i in sys.argv[1:])]
        kwargs = {}
    res = pytest.main(args, **kwargs)

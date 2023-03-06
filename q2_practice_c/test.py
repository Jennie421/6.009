#!/usr/bin/env python3
import os, pickle, marshal, types, json
import quiz

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


#############
# Problem 1 #
#############

def test_problem1_01():
    exp = ('+', 'a', ('+', 'b', ('+', 8, 'c')))
    assert quiz.constant_fold(('+', 'a', ('+', 'b', ('+', ('+', 3, 5), 'c')))) == exp

def test_problem1_02():
    exp = ('+', 'a', ('+', 48, 'b'))
    assert quiz.constant_fold(('+', 'a', ('+', ('*', ('+', 3, 5), 6), 'b'))) == exp

def test_problem1_03():
    assert quiz.constant_fold(('+', 'a', ('+', ('*', 'b', 0), 'c'))) == ('+', 'a', 'c')

def test_problem1_04():
    assert quiz.constant_fold(('*', 1, ('+', 0, ('*', ('+', 'x', 0), 1)))) == 'x'

def test_problem1_05():
    assert quiz.constant_fold(('+', 7, ('*', 'x', ('-', 7, ('+', 4, 3))))) == 7

def test_problem1_06():
    assert quiz.constant_fold(('*', 'a', ('-', 'b', 0))) == ('*', 'a', 'b')

def test_problem1_07():
    assert quiz.constant_fold(('+', 1, ('*', 2, ('-', 3, 2)))) == 3

def test_problem1_08():
    assert quiz.constant_fold(('+', 'x', ('+', 'x', 'x'))) == ('+', 'x', ('+', 'x', 'x'))


#############
# Problem 2 #
#############

ALLWORDS = frozenset(open('words2.txt').read().splitlines())

def test_problem2_01():
    top = 'at'; total_squares = 3
    g = quiz.word_squares(top)
    check_square(top, g, check_n=3, check_total=-1)

def test_problem2_02():
    top = 'is'; total_squares = 2
    g = quiz.word_squares(top)
    check_square(top, g, check_n=2, check_total=total_squares)
    # Generator should work more than once within same process...
    top = 'ad'; total_squares = 3
    g = quiz.word_squares(top)
    check_square(top, g, check_n=2, check_total=total_squares)

def test_problem2_03():
    top = 'bar'; total_squares = 1743
    g = quiz.word_squares(top)
    check_square(top, g, check_n=1743, check_total=total_squares)

def test_problem2_04():
    top = 'fast'; total_squares = 202505
    g = quiz.word_squares(top)
    check_square(top, g, check_n=20, check_total=total_squares)

def test_problem2_05():
    top = 'drink'; total_squares = 673052
    g = quiz.word_squares(top)
    check_square(top, g, check_n=20, check_total=total_squares)

def test_problem2_06():
    top = 'zoologists'; total_squares = 0
    g = quiz.word_squares(top)
    check_square(top, g, check_n=total_squares, check_total=total_squares)

def check_square(top, result_gen, check_n=0, check_total=-1):
    assert isinstance(result_gen, types.GeneratorType), "word_squares should be a generator"
    if check_n >= 0: # verify first check_n yields from result_gen
        results = get_some(result_gen, check_n)
        validate(top, results, check_n)
    if check_total >= 0: # verify total count of items from generator is correct
        results += list(result_gen)
        validate(top, results, check_total)

def validate(top, results, count):
    # Validate that list of results are all (non-duplicative)
    # square_word tuples, and the right number of results are
    # provided.
    for res in results:
        assert isinstance(res, tuple), "word_squares should yield tuples"
        words = set(res)
        assert len(res) == 4, "tuples from word_squares should have 4 different strings"
        for w in res:
            assert w in ALLWORDS, "word in result is not in words2.txt"

        top, right, bot, left = res
        assert top[0] == left[0]
        assert top[-1] == right[0]
        assert bot[0] == left[-1]
        assert bot[-1] == right[-1]

    rset = set(results)
    assert len(rset) == len(results), "word_squares should not yield duplicates"
    assert len(results) == count, "wrong number of square_word tuples produced"

def get_some(g, n):
    res = []
    for i in range(n):
        try: res.append(next(g))
        except StopIteration: pass
    return res


#############
# Problem 3 #
#############

from trie import Trie, RadixTrie
from text_tokenize import tokenize_sentences


def dictify(t):
    out = {'value': t.value, 'children': {}}
    for ch, child in t.children.items():
        out['children'][ch] = dictify(child)
    return out


def make_word_trie(words):
    t = Trie()
    for word, val in words:
        t[word] = val
    return t


def get_words(text):
    return [tuple(i.split()) for i in tokenize_sentences(text, True)]


def is_radix_trie(t):
    if not isinstance(t, RadixTrie):
        return False

    return all(is_radix_trie(i) for i in t.children.values())


def _run_test(n):
    in_fname = os.path.join(TEST_DIRECTORY, 'test_data',
                            'trie_%d_in.pyobj' % (n,))
    with open(in_fname, encoding='utf-8') as f:
        inp = eval(f.read())
    out_fname = os.path.join(TEST_DIRECTORY, 'test_data',
                             'trie_%d_out.pyobj' % (n,))
    with open(out_fname, encoding='utf-8') as f:
        expected = eval(f.read())

    result = get_result(inp)
    assert result == expected


def get_result(inp):
    inp = make_word_trie(inp)
    original = dictify(inp)
    out = quiz.compress_trie(inp)
    assert original == dictify(inp), "Your function should not modify the given Trie."
    assert is_radix_trie(out), "Your function should return an instance of RadixTrie."
    return dictify(out)


def test_problem3_01():
    _run_test(1)

def test_problem3_02():
    _run_test(2)

def test_problem3_03():
    _run_test(3)

def test_problem3_04():
    _run_test(4)

def test_problem3_05():
    _run_test(5)

def test_problem3_06():
    _run_test(6)

def test_problem3_07():
    _run_test(7)

def test_problem3_08():
    _run_test(8)


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

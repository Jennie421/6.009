#!/usr/bin/env python3
import os
import quiz

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)

##################################################
### Problem 1: batch
##################################################

def test_batch_1():
    # Simple cases
    inp = (9,)
    size = 4
    expect = [[9]]
    result = quiz.batch(inp, size)
    assert result == expect

    inp = (1, 2)
    size = 4
    expect = [[1,2]]
    result = quiz.batch(inp, size)
    assert result == expect

    inp = (4, 4)
    size = 4
    expect = [[4],[4]]
    result = quiz.batch(inp, size)
    assert result == expect


def test_batch_2():
    # Batch fills/overflows
    inp = (1, 2, 3)
    size = 4
    expect = [[1,2,3]]
    result = quiz.batch(inp, size)
    assert result == expect

    inp = (4, 4)
    size = 5
    expect = [[4, 4]]
    result = quiz.batch(inp, size)
    assert result == expect

    inp = (4, 4, 4)
    size = 5
    expect = [[4, 4], [4]]
    result = quiz.batch(inp, size)
    assert result == expect

def test_batch_3():
    # More complex cases
    inp = (13, 2, 3, 4, 3, 1, 1, 1, 4, 2, 3)
    size = 5
    expect = [[13], [2, 3], [4, 3], [1, 1, 1, 4], [2, 3]]
    result = quiz.batch(inp, size)
    assert result == expect

    inp = (6, 5, 6, 8, 6)
    size = 7
    expect = [[6, 5], [6, 8], [6]]
    result = quiz.batch(inp, size)
    assert result == expect

    inp = tuple(range(1,15))
    size = 7
    expect = [[1, 2, 3, 4], [5, 6], [7], [8], [9], [10], [11], [12], [13], [14]]
    result = quiz.batch(inp, size)
    assert result == expect

    inp = (1, 8, 3, 4, 3, 2, 4, 2, 3, 4, 2, 8, 8, 1, 1, 1, 18)
    size = 8
    expect = [[1, 8], [3, 4, 3], [2, 4, 2], [3, 4, 2], [8], [8], [1, 1, 1, 18]]
    result = quiz.batch(inp, size)
    assert result == expect

    size = 4
    expect = [[1, 8], [3, 4], [3, 2], [4], [2, 3], [4], [2, 8], [8], [1, 1, 1, 18]]
    result = quiz.batch(inp, size)
    assert result == expect

def test_batch_4():
    big = 20000
    inp = (9,9,9,9,9)*big
    size = 10
    result = quiz.batch(inp, size)
    assert big*5/2 == len(result)
    for elt in result:
        assert elt == [9,9]

def test_batch_5():
    big = 20000
    inp = (1,3,5,9)*big
    size = 10
    result = quiz.batch(inp, size)
    assert len(result) == big
    for elt in result:
        assert elt == [1,3,5,9]


##################################################
### Problem 2: order
##################################################

def test_order_1():
    inp = ['hi', 'yes', 'hello', 'yay']
    gold = inp[:]
    expect = ['hi', 'hello', 'yes', 'yay']
    result = quiz.order(inp)
    assert result == expect
    assert inp == gold, "the input list should not be mutated"

def test_order_2():
    # non-alphabetic order
    inp = ['yes', 'hi', 'yay', 'hello']
    gold = inp[:]
    expect = ['yes', 'yay', 'hi', 'hello']
    result = quiz.order(inp[:])
    assert result == expect
    assert inp == gold, "the input list should not be mutated"

def test_order_3():
    # repeated elements
    inp = ['b', 'ab', 'doh', 'aa', 'c', 'aa']
    gold = inp[:]
    expect = ['b', 'ab', 'aa', 'aa', 'doh', 'c']
    result = quiz.order(inp[:])
    assert result == expect
    assert inp == gold, "the input list should not be mutated"

    inp = ['it', 'was', 'the', 'best', 'of', 'times', 'it', 'was', 'the', 'worst', 'of', 'times']
    gold = inp[:]
    expect = ['it', 'it', 'was', 'was', 'worst', 'the', 'times', 'the', 'times', 'best', 'of', 'of']
    result = quiz.order(inp[:])
    assert result == expect
    assert inp == gold, "the input list should not be mutated"

def test_order_4():
    inp = ['foo'*13, 'fab'*7+'ulous', 'bar'*2+'bang', 'anything', 'fab'*7] + ['anything']*2
    gold = inp[:]
    expect = ['foo'*13, 'fab'*7+'ulous', 'fab'*7,  'bar'*2+'bang', 'anything', 'anything', 'anything']
    result = quiz.order(inp[:])
    assert result == expect
    assert inp == gold, "the input list should not be mutated"

def test_order_5():
    inp_1 = ['joe', 'barb', 'james', 'corey', 'larry', 'james', 'sarah', 'melissa']
    inp_2 = list(reversed(inp_1))

    gold = inp_1[:]
    expect = ['joe', 'james', 'james', 'barb', 'corey', 'larry', 'sarah', 'melissa']
    result = quiz.order(inp_1[:])
    assert result == expect
    assert inp_1 == gold, "the input list should not be mutated"

    gold = inp_2[:]
    expect = ['melissa', 'sarah', 'james', 'james', 'joe', 'larry', 'corey', 'barb']
    result = quiz.order(inp_2[:])
    assert result == expect
    assert inp_2 == gold, "the input list should not be mutated"


##################################################
### Problem 3: path_to_happiness
##################################################

def make_field(nrows, ncols, f):
    return {"nrows": nrows, "ncols": ncols,
            "smiles": tuple(tuple(f(r,c) for c in range(ncols)) for r in range(nrows))}

def check_result(field, happiness, result):
    assert isinstance(result, list), "path should be a list"
    assert len(result) == field["ncols"], "path length incorrect"
    last = result[0]
    for c in range(1, field["ncols"]):
        assert last-1 <= result[c] <= last+1, "invalid path"
        last = result[c]
    assert happiness == sum(field["smiles"][result[c]][c] for c in range(field["ncols"])),\
                     "not maximum happiness path"

# path_to_happiness tests
def test_path_to_happiness_01():
    # single column field
    field = {"nrows": 3, "ncols": 1, "smiles": ((5,), (6,), (4,))}
    happiness = 6
    result = quiz.path_to_happiness(field)
    assert result == [1]
    check_result(field, happiness, result)

def test_path_to_happiness_02():
    # a two column field
    field = {"nrows": 3, "ncols": 2, "smiles": ((6, 25), (5, 2), (4, 35))}
    happiness = 40
    result = quiz.path_to_happiness(field)
    assert result == [1,2]
    check_result(field, happiness, result)

    # a two column field with two solution paths; either is fine
    field = {"nrows": 3, "ncols": 2, "smiles": ((5, 18), (6, 0), (4, 18))}
    happiness = 24
    result = quiz.path_to_happiness(field)
    assert result == [1,0] or result == [1,2]
    check_result(field, happiness, result)

def test_path_to_happiness_03():
    # single row field
    field = {"nrows": 1, "ncols": 10, "smiles": ((5, 6, 4, 0, 5, 2, 1, 8, 9, 1),)}
    happiness = 41
    check_result(field, happiness, quiz.path_to_happiness(field.copy()))

def test_path_to_happiness_04():
    # small size fields
    field = {"nrows": 2, "ncols": 3, "smiles": ((100, 3, 5), (2, 4, 6))}
    happiness = 110
    check_result(field, happiness, quiz.path_to_happiness(field.copy()))

    field = make_field(5, 3, lambda r, c: (r+c+2)%4)
    happiness = 8
    check_result(field, happiness, quiz.path_to_happiness(field.copy()))

    field = make_field(4, 5, lambda r, c: abs(r-2))
    happiness = 10
    check_result(field, happiness, quiz.path_to_happiness(field.copy()))

    field = make_field(5, 8, lambda r, c: 1 if r==c else 0)
    happiness = 5
    check_result(field, happiness, quiz.path_to_happiness(field.copy()))

def test_path_to_happiness_05():
    # tall fields
    field = make_field(20, 5, lambda r, c: (r+c+3)%7)
    happiness = 30
    check_result(field, happiness, quiz.path_to_happiness(field.copy()))

    field = make_field(200, 4, lambda r, c: (r+c+3)%7)
    happiness = 24
    check_result(field, happiness, quiz.path_to_happiness(field.copy()))

def test_path_to_happiness_06():
    # wide field with 2 rows
    field = make_field(2, 20, lambda r, c: (r+c+2)%4)
    happiness = 45
    check_result(field, happiness, quiz.path_to_happiness(field.copy()))

def test_path_to_happiness_07():
    # wide field with 3 rows
    field = make_field(3, 15, lambda r, c: (r+c+2)%4)
    happiness = 37
    check_result(field, happiness, quiz.path_to_happiness(field.copy()))

def test_path_to_happiness_08():
    # medium size fields
    field = make_field(17, 12, lambda r, c: (r+c)%7)
    happiness = 72
    check_result(field, happiness, quiz.path_to_happiness(field.copy()))

def test_path_to_happiness_09():
    # large field
    field = make_field(47, 50, lambda r, c: (r*c)%7)
    happiness = 217
    check_result(field, happiness, quiz.path_to_happiness(field.copy()))

def test_path_to_happiness_10():
    # larger field
    field =make_field(500, 600, lambda r, c: (r*c+r+c)%7)
    happiness = 3600
    check_result(field, happiness, quiz.path_to_happiness(field.copy()))

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

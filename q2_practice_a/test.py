#!/usr/bin/env python3
import os
import ast
import quiz
import types
import json
import hashlib

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


#############
# Problem 1 #
#############

def _test_generator(inp, expected):
    result = quiz.split_words(inp)
    assert isinstance(result, types.GeneratorType), "split_words should be a generator"
    assert set(result) == expected

def _test_from_file(inp, n):
    with open(os.path.join(TEST_DIRECTORY, 'resources', 'words_%02d.py' % n), 'r') as f:
        _test_generator(inp, ast.literal_eval(f.read()))

def test_problem1_01():
    _test_generator('cake', {('cake', )})
    _test_generator('iateanicecreamcone', {('i', 'a', 'tea', 'nice', 'cream', 'cone'), ('i', 'ate', 'a', 'nice', 'cream', 'cone'), ('i', 'ate', 'an', 'ice', 'cream', 'cone')})
    _test_generator('mycatscaneatcarrots', {('my', 'cat', 'scan', 'eat', 'car', 'rots'), ('my', 'cat', 'scan', 'eat', 'carrots'), ('my', 'cats', 'can', 'eat', 'car', 'rots'), ('my', 'cats', 'can', 'eat', 'carrots'), ('my', 'cats', 'cane', 'at', 'car', 'rots'), ('my', 'cats', 'cane', 'at', 'carrots')})

def test_problem1_02():
    _test_from_file('etudeshakewithholdsmansards', 1)

def test_problem1_03():
    _test_from_file('redissolvebeseeminggrandeurs', 2)

def test_problem1_04():
    _test_from_file('ushersbreaknecktreblingnitrified', 3)
    _test_from_file('antennasflameoutnothingstrackless', 4)
    _test_from_file('abatersboardingapproveduntanglingcirrus', 5)
    _test_from_file('challengetissuesgrippesrivuletsodiumparties', 6)

def test_problem1_05():
    _test_from_file('relationsharesabridgetheisticwithinslingshots', 7)
    _test_from_file('opensospreytipsgiftedmenmiscallingdisarmsuprooted', 8)
    _test_from_file('earningsbrawnsflusmopingyourselfmillinerybicyclistsadrenal', 9)
    _test_from_file('unmistakenracefilterintertwinedeepdefrayexaminingherefords', 10)
    _test_from_file('semaphoresixpaperingquadrantalbulldozingvelocitypolesolider', 11)
    _test_from_file('erstwhilesophisticsocialeagerlyasparagustryingforearmstipple', 12)
    _test_from_file('accidentalbailoutenlargebegirtquakerswashroompromotersdroves', 13)
    _test_from_file('barbadosmistookannoysbotfliesincubationdetachescatnipicicles', 14)
    _test_from_file('hamsterraceapprovesproconsulzonkedwantshadyhearkenamplifyides', 15)
    _test_from_file('multilithhikersinstallingsquirelacingswaggeredintendedsyapped', 16)
    _test_from_file('buntbrainpansbeardeddashikihelenapageboyssolipsistpatchpippedomaha', 17)
    _test_from_file('rethinkaviditiesspearswrenchcapturedaversionspaddlesmisquotespajamas', 18)
    _test_from_file('sequinsamericanabilletfrightfultimpanistsavertedivyexactorimmolateddisappointsow', 19)
    _test_from_file('intervenedsendingtrimmingpreemptingpersuasionbudgemoochingextortionwhelksjoustbikes', 20)
    _test_from_file('federalsunheardtelephonesaliasdepositimbruingartifactspositivecurrentpluralistsullying', 21)
    _test_from_file('sportingpackagecheshireyearlyenfiladedstomachingpersistsailshelteringsulkyoleoresinpolio', 22)
    _test_from_file('activationemigratethiamineinstincttypesetquoteskindliestapproachedparchmentstenonsadherent', 23)
    _test_from_file('stragglypalladiumraspiestplatoonsferrousdeceitsduffersbeaconssuperhumancorvettesaugmentingtallying', 24)
    _test_from_file('arcslanderousreptilehotheadedsympathyeulogistichabituatedcorianderbarbarouscoercionpopulaceultimatum', 25)


##################################################
##  Problem 2 Tests
##################################################

# First example from write-up
def test_problem2_01():
    x = quiz.InfiniteList(lambda x: 0)
    assert x[20] == 0
    assert x[200000] == 0
    assert x[-5000000000000000] == 0
    x[7] = 8
    assert x[7] == 8

# Second example from write-up
def test_problem2_02():
    y = quiz.InfiniteList(abs)
    assert y[-20] == 20
    assert y[20] == 20
    y[20] = 8
    assert y[-20] == 20
    assert y[20] == 8

# NOTE: this function that we use for tests only checks finitely elements of the infinite list 'obj'!
# We only look up through the length of regular Python list 'ans'.
# We don't think it will help you at all to try to write code that doesn't actually work properly
# but manages to pass our tests because we only look so many positions into a list. ;-)
def assertMatch(obj, ans):
    for a, b in zip(iter(obj), iter(ans)):
        assert a == b

# We also sometimes use this one, so that you can pass tests even if your __iter__ isn't working yet.
def assertMatchWithoutIter(obj, ans):
    for i, v in enumerate(ans):
        assert obj[i] == v

# Iteration
def test_problem2_03():
    x = quiz.InfiniteList(lambda x: x)
    x[2] = 3
    x[4] = 10

    assertMatch(x, [0, 1, 3, 3, 10, 5, 6, 7, 8, 9])

# Addition
def test_problem2_04():
    x = quiz.InfiniteList(lambda x: x)
    x[2] = 3
    x[4] = 10

    y = quiz.InfiniteList(lambda x: 0)
    y[1] = 7
    y[2] = 30

    assertMatchWithoutIter(x + y, [0, 8, 33, 3, 10, 5, 6, 7, 8, 9])

# Addition plus __iter__
def test_problem2_05():
    x = quiz.InfiniteList(lambda x: x)
    x[2] = 3
    x[4] = 10

    y = quiz.InfiniteList(lambda x: 0)
    y[1] = 7
    y[2] = 30

    assertMatch(x + y, [0, 8, 33, 3, 10, 5, 6, 7, 8, 9])

# Multiplication
def test_problem2_06():
    x = quiz.InfiniteList(lambda x: x)
    x[2] = 3
    x[4] = 10

    assertMatchWithoutIter(x * 2, [0, 2, 6, 6, 20, 10, 12, 14, 16, 18])


##################################################
#  Problem 3
##################################################

def load_data(test_num):
    with open('resources/valid_boards_test%s.json' % test_num, 'r') as f:
        data = json.load(f)
    return data

def board_equivalents(board):

    def horizontal_flip(board):
        return board[::-1]

    def vertical_flip(board):
        new_board = [len(board) - 1 - x for x in board]
        return new_board

    def rotate90(board, n):
        rotated_board = [-1]*n
        for col in range(n):
            row = board[col]
            if row == -1: continue
            new_row = n - col - 1
            new_col = row
            rotated_board[new_col] = new_row
        return rotated_board

    def hash_board(board):
        str_board = str(tuple(board)).encode('utf-8')
        hash_fn = hashlib.sha1
        return hash_fn(str_board).hexdigest()

    equivalents = set([hash_board(board)])
    equivalents.add(hash_board(horizontal_flip(board)))
    equivalents.add(hash_board(vertical_flip(board)))
    for i in range(3):
        board = rotate90(board, len(board))
        equivalents.add(hash_board(board))

    return equivalents


def validate(data, k, n, returned):
    if n <= 0 or k <= 0:
        assert returned is None, (f"\nSolutions are not possible for k={k} and size={n}."
                                  f"\nYour solution returned: {returned}.")

    expected = []
    for min_k in data[str(n)]:
        if int(min_k) <= k:
            expected.extend(data[str(n)][str(min_k)])

    if returned is None:
        assert len(expected) == 0, (f"\nSolutions are possible for k={k} and size={n}."
                                    f"\nYour solution returned None.")
    else:
        assert isinstance(returned, list), (f"\nYour solution did not return a list for k={k} and size={n}." \
                                            f"\nIt returned a object of type: {type(returned)}")

        assert all(isinstance(value, int) or isinstance(value, float) for value in returned), (
                        f"\nYour solution did not return a list of numbers for k={k} and size={n}."
                        f"\nIt returned a list of objects of types: {set([type(value) for value in returned])}"
                )

        assert n == len(returned), (f"\nYour solution is not the correct length for k={k} and size={n}."
                                    f"\nYour solution is length: {len(returned)}, but the board is of size: {n}.")

        number_of_queens = sum(x > -1 for x in returned)
        assert number_of_queens <= k, (f"\nYour solution has too many queens for k={k} and size={n}."
                                       f"\nYour solution placed {len(number_of_queens)} queens, but you must place less than or equal to {k} queens.")

        returned_equivalents = board_equivalents(returned)
        assert any(equivalent in expected for equivalent in returned_equivalents), (
                        f"\nYour solution is not a valid solution for k={k} and size={n}."
                        f"\nYour solution returned {returned}, which either has conflicting queens or does not cover every cell."
                )


def test_problem3_01():
    """ The 1x1 board."""
    data = load_data('1')
    validate(data, 1, 1, quiz.k_queens_coverage(1, 1))

def test_problem3_02():
    """ The 2x2 board for k in (1, 2)."""
    data = load_data('2')
    n = 2
    for k in range(1, n+1):
        validate(data, k, n, quiz.k_queens_coverage(k, n))

def test_problem3_03():
    """ The 3x3 board for k in (1, 2, 3)."""
    data = load_data('3')
    n = 3
    for k in range(1, n+1):
        validate(data, k, n, quiz.k_queens_coverage(k, n))

def test_problem3_04():
    """ Medium boards between than 4x4 and 6x6 with k that produce solutions."""
    data = load_data('4')
    validate(data, 3, 4, quiz.k_queens_coverage(3, 4))
    validate(data, 4, 4, quiz.k_queens_coverage(4, 4))

    validate(data, 3, 5, quiz.k_queens_coverage(3, 5))
    validate(data, 4, 5, quiz.k_queens_coverage(4, 5))
    validate(data, 5, 5, quiz.k_queens_coverage(5, 5))

    validate(data, 4, 6, quiz.k_queens_coverage(4, 6))
    validate(data, 5, 6, quiz.k_queens_coverage(5, 6))
    validate(data, 6, 6, quiz.k_queens_coverage(6, 6))

def test_problem3_05():
    """ Medium boards between than 4x4 and 6x6 with k that do not produce solutions."""
    data = load_data('5')
    validate(data, 1, 4, quiz.k_queens_coverage(1, 4))
    validate(data, 2, 4, quiz.k_queens_coverage(2, 4))

    validate(data, 1, 5, quiz.k_queens_coverage(1, 5))
    validate(data, 2, 5, quiz.k_queens_coverage(2, 5))

    validate(data, 1, 6, quiz.k_queens_coverage(1, 6))
    validate(data, 2, 6, quiz.k_queens_coverage(2, 6))
    validate(data, 3, 6, quiz.k_queens_coverage(3, 6))

def test_problem3_06():
    """ Large boards greater than 6x6 with small k that produce solutions."""
    data = load_data('6-7')
    validate(data, 3, 7, quiz.k_queens_coverage(3, 7))
    validate(data, 4, 7, quiz.k_queens_coverage(4, 7))
    validate(data, 5, 7, quiz.k_queens_coverage(5, 7))
    validate(data, 6, 7, quiz.k_queens_coverage(6, 7))

    validate(data, 5, 8, quiz.k_queens_coverage(5, 8))
    validate(data, 6, 8, quiz.k_queens_coverage(6, 8))

def test_problem3_07():
    """ Large boards greater than 6x6 with large k that produce solutions."""
    data = load_data('6-7')
    validate(data, 7, 7, quiz.k_queens_coverage(7, 7))

    validate(data, 7, 8, quiz.k_queens_coverage(7, 8))
    validate(data, 8, 8, quiz.k_queens_coverage(8, 8))

def test_problem3_08():
    """ Large boards greater than 6x6 with k that do not produce solutions."""
    data = load_data('8')
    validate(data, 1, 7, quiz.k_queens_coverage(1, 7))
    validate(data, 2, 7, quiz.k_queens_coverage(2, 7))

    validate(data, 1, 8, quiz.k_queens_coverage(1, 8))
    validate(data, 2, 8, quiz.k_queens_coverage(2, 8))
    validate(data, 3, 8, quiz.k_queens_coverage(3, 8))
    validate(data, 4, 8, quiz.k_queens_coverage(4, 8))

def test_problem3_09():
    """ Impossible values of k."""
    data = load_data('9')
    for n in range(1, 9):
        validate(data, 0, n, quiz.k_queens_coverage(0, n))




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

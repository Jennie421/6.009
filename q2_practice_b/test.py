#!/usr/bin/env python3
import os, pickle, types, json
import quiz

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


#############
# Problem 1 #
#############

def _validate_trees(k, n=None, limit=None):
    def get_size(tree):
        if tree is None:
            return 0
        elif isinstance(tree, tuple) and len(tree) == 2:
            return 1 + get_size(tree[0]) + get_size(tree[1])
        return None

    def check_tree(tree, seen):
        size = get_size(tree)
        if size is None:
            pytest.fail(f'{tree} is not a binary tree')
        if size != k:
            pytest.fail(f'{tree} is not of size {k}')
        if tree in seen:
            pytest.fail(f'repeated tree: {tree}')
        seen.add(tree)

    # Check size and uniqueness.
    trees = set()
    if limit is None:
        for tree in quiz.binary_trees(k):
            check_tree(tree, trees)
    else:
        gen = iter(quiz.binary_trees(k))
        for i in range(limit):
            try:
                tree = next(gen)
            except StopIteration:
                pytest.fail(f'only {i} trees returned, expected more')
            check_tree(tree, trees)

    # Check count.
    if n is not None and len(trees) != n:
        pytest.fail(f'expected {n} trees, got {len(trees)}')

def test_problem1_01():
    _validate_trees(0, n=1)

def test_problem1_02():
    _validate_trees(1, n=1)

def test_problem1_03():
    _validate_trees(2, n=2)

def test_problem1_04():
    _validate_trees(3, n=5)

def test_problem1_05():
    _validate_trees(12, n=208012)

def test_problem1_06():
    _validate_trees(13, limit=10000)

def test_problem1_07():
    _validate_trees(100, limit=10000)

def test_problem1_08():
    _validate_trees(900, limit=10000)


#############
# Problem 2 #
#############

def validate_possible(n, init_bishop_locs, target):
    result = quiz.n_bishops(n, init_bishop_locs, target)
    assert result is not None
    assert isinstance(result, set)
    assert len(result) >= target
    assert init_bishop_locs.issubset(result)
    assert (all(((0 <= r < n) and (0 <= c < n)
                 and isinstance(r, int) and isinstance(c, int)
                for r, c in result)))
    assert _checker(result)

def validate_impossible(n, init_bishop_locs, target):
    assert quiz.n_bishops(n, init_bishop_locs, target) is None

def _checker(lb):
    sd = lambda z1, z2: (z1[0] - min(z1), z1[1] - min(z1)) == (z2[0] - min(z2), z2[1] - min(z2)) or sum(z1) == sum(z2)
    for z1 in lb:
        for z2 in lb:
            if z1 != z2:
                if sd(z1, z2): return False
    return True

def test_problem2_01():
    # n=3 initially empty board -> possible
    validate_possible(3, set(), 4)

def test_problem2_02():
    # n=4 initially partially filled board -> possible
    validate_possible(4, {(3, 0), (3, 2), (0, 2)}, 6)

def test_problem2_03():
    # n=4 initially partially filled board -> impossible
    validate_impossible(4, {(3, 0), (3, 2), (0, 2)}, 7)

def test_problem2_04():
    # n=13 initially partially filled board -> impossible
    validate_impossible(13,
             {(12, 2), (11, 7), (4, 9), (8, 2), (11, 6), (5, 11), (3, 3), (8, 11), (5, 7), (11, 12),
              (0, 11), (4, 3), (12, 9), (12, 3), (5, 3)}, 20)

def test_problem2_05():
    # n=18 initially partially filled board -> possible
    validate_possible(18,
            {(17, 4), (0, 1), (9, 13), (6, 8), (17, 9), (3, 1),
             (0, 13), (7, 13), (17, 12), (0, 9)}, 30)

def test_problem2_06():
    # n=25 initially partially filled board -> possible
    validate_possible(25,
            {(23, 4), (23, 19), (5, 10), (22, 24), (22, 15), (0, 6),
             (22, 4), (10, 24), (14, 15), (4, 3), (6, 15), (20, 15), (15, 5), (13, 10)}, 39)


#############
# Problem 3 #
#############

def _test_insert_with_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    points = set(zip(data['x'], data['y']))
    width = data['width']
    height = data['height']
    quadtree = quiz.QuadTree(0, 0, width, height)
    _test_insert(quadtree, points)

def _test_insert(quadtree, points):
    for point in points:
        quadtree.insert(point)

    # validate quadtree structure
    is_valid, message = _is_valid(quadtree)
    assert is_valid, message
    if isinstance(points, list):
        points = set(points)
    # check to make sure all points were added
    assert sorted(points) == sorted(_get_all(quadtree)), "All points different from inserted points"
    for point in points:
        assert _find_point(quadtree, point), f"Cannot find point {point} in quadtree"

# Retrieves all points in this quadtree
def _get_all(quadtree):
    points = []
    if quadtree.children is not None:
        for child in quadtree.children:
            points.extend(_get_all(child))
    else:
        points = list(quadtree.points)
    return points

# Checks if this quadtree is valid (follows the invariants listed at the top)
def _is_valid(quadtree):
    # Checks if the ranges are valid
    if quadtree.x_start > quadtree.x_end or quadtree.y_start > quadtree.y_end:
        return False, "Node has invalid range"

    # If the quadtree has children, it should have four
    if quadtree.children is not None and len(quadtree.children) == 4:
        # Check that the children do not overlap
        for c1 in quadtree.children:
            for c2 in quadtree.children:
                if c1 is not c2 and not (c1.x_start >= c2.x_end or c2.x_start >= c1.x_end \
                            or c1.y_start >= c2.y_end or c2.y_start >= c1.y_end):
                    return False, "Children ranges overlap"

        # Check that its children are also valid recursively
        for child in quadtree.children:
            if not _is_valid(child):
                return False, "Child node is not valid"

        # Check that its points is None
        if quadtree.points is not None:
            return False, "Non-leaf node's points should be None" #

    elif quadtree.children is None:
        # Should have four or less points
        if len(quadtree.points) > 4:
            return False, "Leaf node should have 4 or less points"

        # Points should be in range
        for (x, y) in quadtree.points:
            if x < quadtree.x_start or x >= quadtree.x_end or y < quadtree.y_start or y >= quadtree.y_end:
                return False, "Point should be in range of the node's range"
    else:
        return False, "Non-leaf node does not have 4 children"

    return True, "Success!"

def _find_point_in_quadtree(q, point):
    """
    Returns True if point exists in the quadtree
    :param point: point (x, y) to find
    """
    x, y = point
    if q.children is not None:
        for c in q.children:
            # If a child's range includes the point, recurse into this child
            if x >= c.x_start and x < c.x_end and y >= c.y_start and y < c.y_end:
                return _find_point_in_quadtree(c, point)
    else:
        # If the quadtree doesn't have children, we can check for the point
        if point in q.points:
            return True
        else:
            return False

def _find_point(quadtree, point):
    x, y = point
    if quadtree.children is not None:
        for c in quadtree.children:
            # If a child's range includes the point, recurse into this child
            if x >= c.x_start and x < c.x_end and y >= c.y_start and y < c.y_end:
                return _find_point_in_quadtree(c, point)
    else:
        # If the quadtree doesn't have children, we can check for the point
        if point in quadtree.points:
            return True
        else:
            return False

def test_problem3_01():
    width = 5
    height = 5
    quadtree = quiz.QuadTree(0, 0, width, height)
    points = {(0, 0), (2, 4)}
    _test_insert(quadtree, points)

def test_problem3_02():
    width = 10
    height = 20
    quadtree = quiz.QuadTree(0, 0, width, height)
    points = {(7, 6), (6, 8), (8, 9), (9, 6), (5, 2)}
    _test_insert(quadtree, points)

def test_problem3_03():
    width = 5
    height = 10
    quadtree = quiz.QuadTree(0, 0, width, height)
    points = [(0, 1), (0, 1), (2, 3), (1, 8), (2, 3)]
    _test_insert(quadtree, points)

def test_problem3_04():
    _test_insert_with_file('resources/insert_quadtree_many_points_small_rectangle.json')

def test_problem3_05():
    _test_insert_with_file('resources/insert_quadtree_small.json')

def test_problem3_06():
    _test_insert_with_file('resources/insert_quadtree_medium.json')

def test_problem3_07():
    _test_insert_with_file('resources/insert_quadtree_large.json')


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

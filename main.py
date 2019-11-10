import itertools
from functools import reduce


def all_grids():
    flat_grids = itertools.product(*[range(2) for _ in range(6)])
    for a, b, c, d, e, f in flat_grids:
        yield [[a, b, c],
               [d, e, f]]


def rot_left(grid):
    [[a, b, c],
     [d, e, f]] = grid

    return [[b, c, a],
            [e, f, d]]


def rot_right(grid):
    [[a, b, c],
     [d, e, f]] = grid

    return [[c, a, b],
            [f, d, e]]


def rot_vert(grid):
    [[a, b, c],
     [d, e, f]] = grid

    return [[d, e, f],
            [a, b, c]]


all_actions = [
    rot_vert, rot_left, rot_right,
    # composition of rotate vert -> rotate left
    lambda grid: rot_left(rot_vert(grid)),
    lambda grid: rot_right(rot_vert(grid))
]


def is_equiv(grid1, grid2):
    return any((act(grid1) == grid2 for act in all_actions))


def grid_to_string(grid):
    return '\n'.join(
        ''.join(map(str, row))
        for row in grid
    )


def concatenate(grid1, grid2):
    """
    Take two 2d arrays

    abc
    def

    ghi
    jkl

    concatenate horizontally
    abc ghi
    def jkl
    """

    return [row1 + row2 for row1, row2 in zip(grid1, grid2)]


def intersperse(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x


def main():
    all_grids_iter = all_grids()
    orbits = []

    for grid in all_grids_iter:
        orbit_for_grid = next(
            (orbit for orbit in orbits if is_equiv(grid, orbit[0])),
            None
        )
        if orbit_for_grid is not None:
            orbit_for_grid.append(grid)
        else:
            orbits.append([grid])

    for i, orbit in enumerate(orbits):
        print(f'--------------- orbit {i}: size {len(orbit)} ---------------')
        interpsersed = intersperse(orbit, [[' '], [' ']])
        print(grid_to_string(reduce(concatenate, interpsersed)))
        print()


if __name__ == '__main__':
    main()

import itertools
from functools import reduce


def _all_grids():
    flat_grids = itertools.product(*[range(2) for _ in range(6)])
    for a, b, c, d, e, f in flat_grids:
        yield [[a, b, c],
               [d, e, f]]


all_grids = list(_all_grids())


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


def flip(grid):
    [[a, b, c],
     [d, e, f]] = grid

    return [[f, e, d],
            [c, b, a]]


def compose(f, g):
    return lambda grid: f(g(grid))


def identity(x):
    return x


def is_same_action(f, g):
    return all(f(grid) == g(grid) for grid in all_grids)


base_actions = [
    identity, rot_vert, rot_left, rot_right, flip,
]

all_actions = base_actions
while True:
    added_action = False
    for act1, act2 in itertools.product(base_actions, all_actions):
        h = compose(act1, act2)
        if not any(
            is_same_action(existing_act, h) for existing_act in all_actions
        ):
            all_actions.append(h)
            added_action = True
    if not added_action:
        break


def assert_is_complete():
    # assert that the composition of any two actions is already included in the
    # full action set
    for f, g in itertools.product(all_actions, all_actions):
        h = compose(f, g)
        is_included = any(
            action
            for action in all_actions
            if all(h(grid) == action(grid) for grid in all_grids)
        )
        if not is_included:
            raise Exception(f'Not complete')


assert_is_complete()


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
    all_grids_iter = iter(all_grids)
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

    print(f'{len(orbits)} orbits total')
    for i, orbit in enumerate(orbits):
        print(f'--------------- orbit {i}: size {len(orbit)} ---------------')
        interpsersed = intersperse(orbit, [[' '], [' ']])
        print(grid_to_string(reduce(concatenate, interpsersed)))
        print()


if __name__ == '__main__':
    main()

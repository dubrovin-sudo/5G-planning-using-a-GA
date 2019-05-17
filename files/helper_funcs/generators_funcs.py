import copy

import numpy as np

from ..network.net_funcs import distance
from ..objs.cell import Cell
from ..objs.plan import Plan
from ..objs.user import User
from .helper import within


def generate_cells(candidate_points_list, type_of_cell, num_of_cells, distance_between_cells):
    """Generates cells using the given candidate points.

    Generates required cells that can be used to create a population.

    Args:
        candidate_points_list: the list of candidate points each as a tuple
        type_of_cell: a string representing the type of cell(eg: macro)
                    that is to be generated.
        num_of_cells: how many cells to be generated.
        distance_between_cells: the distance (in meters) between every cell.
    """
    np.random.shuffle(candidate_points_list)
    temp_candidate_points_list = copy.deepcopy(candidate_points_list)
    cell_list = []

    # append the first cell (needed to ensure that we are not looping over an empty list)
    cell_coords = candidate_points_list.pop()
    cell = Cell(cell_coords[0], cell_coords[1], type_of_cell)
    cell_list.append(cell)
    # look for the remaining candidate points
    for cp in temp_candidate_points_list:
        if len(cell_list) >= num_of_cells:
            break
        is_well_positioned = True
        for c in cell_list:
            if distance(cp[0], c.get_xcoord(), cp[1], c.get_ycoord()) < distance_between_cells:
                is_well_positioned = False
                break

        if is_well_positioned:
            cell = Cell(cp[0], cp[1], type_of_cell)
            cell_list.append(cell)
            candidate_points_list.pop(candidate_points_list.index(cp))
    return cell_list


def generate_users(num_of_users, area):
    """Generate users in a uniform random way."""
    users = []
    for _ in range(num_of_users):
        x = round(np.random.uniform(0, area))
        y = round(np.random.uniform(0, area))
        user = User(x, y)
        users.append(user)
    return users


def generate_candidate_points(area, step, users_list, users_threshold):
    """Generate candidate points in a uniform random way."""
    candidate_points = []
    for i in range(0, area, step):
        for j in range(0, area, step):
            users_num = 0
            for user in users_list:
                if within(i, j, step, user.get_xcoord(), user.get_ycoord()):
                    users_num += 1

            if users_num >= users_threshold:
                candidate_point_x = round(np.random.uniform(i, i + step), 3)
                candidate_point_y = round(np.random.uniform(j, j + step), 3)
                candidate_points.append((candidate_point_x, candidate_point_y))
    return candidate_points


def generate_initial_population(num_of_plans,
                                candidate_points,
                                users,
                                num_fixed_macro,
                                distance_fixed_macro,
                                num_macro,
                                distance_macro,
                                num_micro,
                                distance_micro,
                                num_pico,
                                distance_pico,
                                num_femto,
                                distance_femto):
    """Generate the initial population.

    Args:
        num_of_plans: An integer of the size of the population.
        candidate_points: A list of candidate points.
        users: A list of users.
        num_fixed_macro: An integer of the number of fixed macro cells.
        distance_fixed_macro: An integer of the distance between each fixed macro cell.
        num_macro: An integer of the number of macro cells.
        distance_macro: An integer of the distance between each macro cell.
        num_micro: An integer of the number of micro cells.
        distance_macro: An integer of the distance between each micro cell.
        num_pico: An integer of the number of pico cells.
        distance_pico: An integer of the distance between each pico cell.
        num_femto: An integer of the number of femto cells.
        distance_femto: An integer of the distance between each femto cell.

    Returns:
        A list(pool) of plans.
    """

    pool = []
    fixed_macro_cells = generate_cells(candidate_points,
                                       "fixed_macro",
                                       num_fixed_macro,
                                       distance_fixed_macro)
    for _ in range(num_of_plans):
        cp = copy.deepcopy(candidate_points)
        np.random.shuffle(cp)

        # generate cells
        macro_cells = generate_cells(cp,
                                     "macro",
                                     num_macro,
                                     distance_macro)
        micro_cells = generate_cells(cp,
                                     "micro",
                                     num_micro,
                                     distance_micro)
        pico_cells = generate_cells(cp,
                                    "pico",
                                    num_pico,
                                    distance_pico)
        femto_cells = generate_cells(cp,
                                     "femto",
                                     num_femto,
                                     distance_femto)

        # generate a new plan
        cells = fixed_macro_cells + macro_cells + \
            micro_cells + pico_cells + femto_cells
        plan = Plan(cells,
                    copy.deepcopy(users),
                    copy.deepcopy(cp),
                    num_fixed_macro,
                    num_macro,
                    num_micro,
                    num_pico,
                    num_femto)
        pool.append(plan)

        # empty lists
        macro_cells = []
        micro_cells = []
        cp = []
    return pool

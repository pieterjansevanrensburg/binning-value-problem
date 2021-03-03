# Suppose we have a set of bins {b1, b2, ..., bn} which corresponding bin values {bv1, bv2, ... bvn}.
# Also suppose that we have a set of values {v1, v2, ..., vn} which we wish to assign to the bins
# to minimize an objective function involving the bin values and the sum of the values within each bin.
# This program calculates the assignment of values to bins which minimizes this objective function using dynamic
# programming techniques.
import copy
import math
import time


def mean_absolute_percentage_error(x: float, y: float) -> float:
    """
    Calculates the mean absolute percentage error between 2 values using the formula:
    abs((x - y) / y).
    :param x: the calculated value.
    :param y: the given value.
    :return: the mean absolute percentage error between the 2 values.
    """
    return math.fabs((x - y) / y)


def calculate_mean_objective_across_bins(current_bin_totals: [float], bin_values: [float],
                                         objective_function: any) -> float:
    """
    Calculates the objective function criteria across all bins using the total sums of the values within the bins
    as well as the bin values.
    :param current_bin_totals: An array of the current sums of the values within each bin.
    :param bin_values: An array of the bin values.
    :param objective_function: The objective function to use on each bin and to average across.
    :return: The mean value of the objective function over each bin.
    """
    mean_objective = 0.0
    for i in range(len(bin_values)):
        current_total = current_bin_totals[i]
        current_value = bin_values[i]
        mean_objective += objective_function(current_total, current_value)

    return mean_objective / len(bin_values)


def assign_values_to_bins(values: [float], bin_values: [float], bins: [[float]], current_bin_totals: [float],
                          objective_function: any):
    """
    A function which assigns values to bins in such a way so as to minimize the given objective function.
    :param values: The array of values to assign.
    :param bin_values: An array of bin values.
    :param bins: An array of bins.
    :param current_bin_totals: An array of the current total sums of the values in each bin.
    :param objective_function: The objective function to minimize.
    :return: A tuple consisting of the bins with the new values assigned to the bins, an updated array of the
    current total sums of the values in each bin (taking into account the newly added values) and the cumulative
    change in the objective function due to the assignment of the values.
    """
    # create a copy of the bins array (note we require deepcopy as it contains references to other objects).
    _bins = copy.deepcopy(bins)
    _current_bin_totals = copy.deepcopy(current_bin_totals)
    # loop through the values to assign.
    cumulative_objective_change = 0
    for delta in values:
        # keep track of the following across bins.
        previous_objective_change = 999999999999999
        assigned_bin_index = -1
        # loop through each bin.
        for j in range(len(_bins)):
            current_bin_total = _current_bin_totals[j]
            current_bin_value = bin_values[j]
            current_objective_change = objective_function(current_bin_total + delta, current_bin_value)

            # check if assign this variable to this bin is better than the previous best assignment to a bin.
            if current_objective_change < previous_objective_change:
                assigned_bin_index = j
                previous_objective_change = current_objective_change

        # assign the value to said bin because it has been determined to be the best overall.
        _bins[assigned_bin_index].append(delta)
        # update the bin totals
        _current_bin_totals[assigned_bin_index] += delta
        cumulative_objective_change += previous_objective_change

    # return the overall change to the cumulative objective function.
    return _bins, _current_bin_totals, cumulative_objective_change


def determine_bin_allocation(values: [float], bin_values: [float], bins: [[float]], current_bin_totals: [float],
                             objective_function: any):
    """
    A function which determines how to allocate values to various bins in order to minimize the objective function
    across the values in each bin and each bin's given value.
    :param values: An array of values to assign to the bins.
    :param bin_values: The values assigned to each bin.
    :param bins: An array representing the bins to which values must be assigned.
    :param current_bin_totals: An array of the total sums of the values within each bin.
    :param objective_function: The objective function to minimize.
    :return: A tuple consisting of the bins with the values assigned to the bins, an updated array of the
    current total sums of the values in each bin (taking into account the assigned values) and the cumulative
    change in the objective function due to the assignment of the values.
    """
    # if there is only 1 value to assign, then stop recurring and assign it to a bin.
    if len(values) == 1:
        return assign_values_to_bins(values, bin_values, bins, current_bin_totals, objective_function)
    # otherwise we split the problem into sub-problems and recur.
    else:
        # split the value array into 2 down the middle and recursively solve the problem for the
        # left and right hand sides of the array.
        # If the left hand side produces a better solution, we keep it. Otherwise, we keep the solution of the
        # right hand side.
        # For the side whose solution we discard, we add its values to the solution we have kept.
        midpoint = len(values) // 2
        left_bins, left_bin_totals, left_objective = determine_bin_allocation(values[:midpoint], bin_values, bins,
                                                                              current_bin_totals, objective_function)
        right_bins, right_bin_totals, right_objective = determine_bin_allocation(values[midpoint:], bin_values, bins,
                                                                                 current_bin_totals, objective_function)
        # we chose the solution which best impacts the objective function, discard the results of the other
        # recursive branch and then assign it's values.
        bins = left_bins if left_objective < right_objective else right_bins
        bin_totals = left_bin_totals if left_objective < right_objective else right_bin_totals

        return assign_values_to_bins(values[midpoint:] if left_objective < right_objective else values[:midpoint],
                                     bin_values, bins, bin_totals, objective_function)


def main():
    """
    Main point of entry for the program.
    :return:
    """
    values = [1, 2, 3]
    bin_values = [3, 4]
    print('Received values and bin values information...')
    bins, bin_totals, _ = determine_bin_allocation(values, bin_values,
                                                   [[] for _ in range(len(bin_values))],
                                                   [0.0] * len(bin_values), mean_absolute_percentage_error)

    print('Values assigned...')
    print('Objective function value: ', round(calculate_mean_objective_across_bins(bin_totals, bin_values,
                                                                                   mean_absolute_percentage_error), 2))
    print('Bin values: ', bin_values)
    print('Bins: ', bins)


# Checks if this file is the point of entry for the program. If it is, then the main function is run.
if __name__ == '__main__':
    start_time = time.time()
    main()
    print('Program finished running in %s seconds.' % round(time.time() - start_time, 2))

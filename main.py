# Suppose we have a set of bins {b1, b2, ..., bn} which corresponding bin values {bv1, bv2, ... bvn}.
# Also suppose that we have a set of values {v1, v2, ..., vn} which we wish to assign to the bins
# to minimize an objective function involving the bin values and the sum of the values within each bin.
# This program calculates the assignment of values to bins which minimizes this objective function using dynamic
# programming techniques.
import random
import time

import bin_value_optimizer
import objective_functions


def main():
    """
    Main point of entry for the program.
    """
    values = [i for i in range(1, 33)]
    random.shuffle(values)

    bin_values = [5, 10, 50, 200, 240]
    bvo = bin_value_optimizer.BinValueOptimizer(bin_values, objective_functions.absolute_percentage_error)
    bvo.assign_values(values)
    print('Mean absolute percentage error: {0}%'.format(bvo.objective * 100))
    print('Bin values: ', bvo.bin_values)
    print('Bin totals: ', bvo.bin_totals)


# Checks if this file is the point of entry for the program. If it is, then the main function is run.
if __name__ == '__main__':
    start_time = time.time()
    main()
    print('Program finished running in %s seconds.' % round(time.time() - start_time, 2))

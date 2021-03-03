import copy
import sys


class BinValueOptimizer(object):
    def __init__(self, bin_values: [float], function: any):
        """
        Constructor of the BinValueOptimizer class.
        :param bin_values: the values assigned to each bin, in order.
        :param function: the objective function to minimize over.
        """
        self.__objective_function: any = function
        self.__bins: [[float]] = [[] for _ in bin_values]
        self.__bin_totals: [float] = [0 for _ in bin_values]
        self.__bin_values: [float] = bin_values

    @property
    def bins(self):
        return self.__bins

    @property
    def bin_values(self):
        return self.__bin_values

    @property
    def bin_totals(self):
        return self.__bin_totals

    @property
    def objective_function(self):
        return self.__objective_function

    @objective_function.setter
    def objective_function(self, function: any):
        self.__objective_function = function

    def assign_values(self, values: [float]):
        """
        A function which assigns the given values to the buckets in such a way so as to minimize the
        objective function.
        :param values: The array of values to assign.
        """
        self.__bins, self.__bin_totals, _ = self.__branch_and_prune(values, self.__bins, self.__bin_totals)

    # def calculate_total_objective(self):
    #    total_objective = 0.0
    #    for i in range(len(self.__bin_values)):
    #        total_objective += self.__objective_function(self.__bin_totals[i], self.__bin_values[i])
    #    return total_objective

    @property
    def objective(self):
        return self.calculate_total_objective(self.__bin_totals)

    def calculate_total_objective(self, bin_totals: [float]):
        total_objective = 0.0
        for i in range(len(self.__bin_values)):
            total_objective += self.__objective_function(bin_totals[i], self.__bin_values[i])
        return total_objective

    def __branch_and_prune(self, values: [float], bins: [float], bin_totals: [float]):
        """

        :param values:
        :param bins:
        :param bin_totals:
        :return:
        """
        # if there is only 1 value to assign, then stop recurring and assign it to a bin.
        if len(values) == 1:
            bins, bin_totals = BinValueOptimizer.assign_values_to_bins(values, self.__bin_values, bins, bin_totals,
                                                                       self.__objective_function)
            objective = self.calculate_total_objective(bin_totals)
            return bins, bin_totals, objective

        # otherwise we split the problem into sub-problems and recur in parallel using the thread pool.
        else:
            # split the value array into 2 down the middle and recursively solve the problem for the
            # left and right hand sides of the array in parallel.
            # If the left hand side produces a better solution, we keep it. Otherwise, we keep the solution of the
            # right hand side.
            # For the side whose solution we discard, we add its values to the solution we have kept.
            midpoint: int = len(values) // 2

            left_bins, left_bin_totals, left_objective = self.__branch_and_prune(values[:midpoint], copy.deepcopy(bins),
                                                                                 copy.deepcopy(bin_totals))
            right_bins, right_bin_totals, right_objective = self.__branch_and_prune(values[midpoint:],
                                                                                    copy.deepcopy(bins),
                                                                                    copy.deepcopy(bin_totals))

            # we chose the solution which best impacts the objective function, discard the results of the other
            # recursive branch and then assign it's values.
            bins = left_bins if left_objective < right_objective else right_bins
            bin_totals = left_bin_totals if left_objective < right_objective else right_bin_totals

            bins, bin_totals = BinValueOptimizer.assign_values_to_bins(
                values[midpoint:] if left_objective < right_objective
                else values[:midpoint], self.__bin_values, bins,
                bin_totals, self.__objective_function)
            objective = self.calculate_total_objective(bin_totals)
            return bins, bin_totals, objective

    @staticmethod
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
        # loop through the values to assign.
        cumulative_objective_change = 0.0
        for delta in values:
            # keep track of the following across bins.
            previous_objective_change = sys.float_info.max
            assigned_bin_index = -1
            # loop through each bin.
            for j in range(len(bins)):
                current_bin_total = current_bin_totals[j]
                current_bin_value = bin_values[j]
                current_objective_change = objective_function(current_bin_total + delta,
                                                              current_bin_value) - objective_function(current_bin_total,
                                                                                                      current_bin_value)

                # check if assign this variable to this bin is better than the previous best assignment to a bin.
                if current_objective_change < previous_objective_change:
                    assigned_bin_index = j
                    previous_objective_change = current_objective_change

            # assign the value to said bin because it has been determined to be the best overall.
            bins[assigned_bin_index].append(delta)
            # update the bin totals
            current_bin_totals[assigned_bin_index] += delta
            cumulative_objective_change += previous_objective_change

        # return the overall change to the cumulative objective function.
        return bins, current_bin_totals

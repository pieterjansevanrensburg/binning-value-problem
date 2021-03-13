# BinningValueProblem

## Overview

For this problem, we are given a set of numbers, and a set of bins with target values.

We wish to allocate the given set of numbers, to the bins, to minimize the difference between the sum of the numbers in each bin and said bin's target value across all bins. Furthermore, each value can only to one bin or no bin at all.

This is done through representing the above problem as a linear programming problem and using discrete-optimization to minimize the differences according to some objective function.

## Table of Contents
* [Mathematical Definition](#mathematical-definition)
* [Solution](#solution)
* [Dependencies](#dependencies)
* [Contributors](#contributors)

## Mathematical Definition

Suppose we are given a 1 x n vector of floating-point numbers:

F = [f<sub>1</sub>, f<sub>2</sub>, f<sub>3</sub>, ..., f<sub>n</sub>]


Furthermore, we are also given a set of bins:

B = {1, 2, 3, ..., m} 

where j represents the j'th bin and m is the total number of bins.


Also, suppose that we are given a 1 x m vector of target values for the set of bins: 

T = [t<sub>1</sub>, t<sub>2</sub>, t<sub>3</sub>, ..., t<sub>m</sub>]

where t<sub>j</sub> represents the target value of the j'th bin.


Finally, we are also given an objective function O.


Based on the above, the problem which we wish to solve is to place the values of F into each of the bins in B so as to minimize the value of the objective function O across the differences between the sum of the values within each bin and the target value assigned to each bin. Furthermore, each value in F can only be allocated once or not be allocated at all.


To solve this, we define the binary matrix X, where the elements of X can be described as follows:

x<sub>i,j</sub> = 1 &hArr; f<sub>i</sub> is placed in bin j or

x<sub>i,j</sub> = 0 &hArr; f<sub>i</sub> is not placed in bin j and

&Sigma;<sub>j</sub>x<sub>i,j</sub> = 1

&forall; i &isin; {1, 2, 3, ..., n}, &forall; j &isin; B

With the above formulation, our problem can be expressed as the following binary linear programming problem:

minimize: O(FX - T)

with respect to the following constraints:

&Sigma;<sub>j</sub>x<sub>i,j</sub> = 1 &forall; i &isin; {1, 2, 3, ..., n}, &forall; j &isin; B

## Solution

This program, given a list of floating-point numbers and a list of target values, automatically generates the above formulation of the problem and then makes use of the [PuLP](https://pypi.org/project/PuLP/) python module to find the optimal solution.

## Dependencies
* [PuLP](https://pypi.org/project/PuLP/)
* [numpy](https://pypi.org/project/numpy/)
* A LP solver for the PuLP frontend to call (options include: COINMP, CPLEX, GLPK, GUROBI, ...)

## Contributors
* [Pieter Janse van Rensburg](pieterjvr50@gmail.com)

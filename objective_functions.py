import math


def absolute_percentage_error(x: float, y: float) -> float:
    """
    Calculates the absolute percentage error between 2 values using the formula: abs((x - y) / y).
    :param x: the calculated value.
    :param y: the given value.
    :return: the absolute percentage error between the 2 values.
    """
    return math.fabs((y - x) / y)


def absolute_error(x: float, y: float) -> float:
    """
    Calculates the absolute error between 2 values using the formula: abs(x - y).
    :param x: the calculated value.
    :param y: the given value.
    :return: the absolute error between the 2 values.
    """
    return math.fabs(y - x)


def squared_error(x: float, y: float) -> float:
    """
    Calculates the squared error between 2 values using the formula: (x - y)^2.
    :param x: the calculated value.
    :param y: the given value.
    :return: the squared error between the 2 values.
    """
    return math.pow(y - x, 2)

import math
import unittest

import objective_functions


class TestObjectiveFunctions(unittest.TestCase):
    def test_absolute_percentage_error(self):
        self.assertAlmostEqual(math.fabs((7 - 5) / 7), objective_functions.absolute_percentage_error(5, 7), 6)

    def test_absolute_error(self):
        self.assertAlmostEqual(math.fabs(-6 - -3), objective_functions.absolute_error(-3, -6), 6)


if __name__ == "__main__":
    unittest.main()

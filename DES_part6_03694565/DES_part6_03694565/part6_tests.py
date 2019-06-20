import unittest
from statistictests import ChiSquare
import numpy

class DESTest(unittest.TestCase):

    """
    This python unittest class checks the sixth part of the programming assignment for basic functionality.
    """

    def test_chi_square(self):
        """
        This task is used to verify the implementation of the chi square test.
        First, 100 samples are drawn from a normal distribution. Afterwards the chi square test is run on them to see,
        whether they follow the original or another given distribution.
        """
        alpha = .1
        values = []
        values2 = []
        numpy.random.seed(0)
        for _ in range(100):
            values.append(numpy.random.normal(5, 1))
            values2.append(numpy.random.uniform(0, 10))

        emp_n, emp_x = numpy.histogram(values, bins=20, range=(0, 10))

        cs = ChiSquare(emp_n=emp_n, emp_x=emp_x)

        [c1, c2] = cs.test_distribution(alpha, 5, 1)

        self.assertGreater(c2, c1, msg="Error in Chi Square Test. Hypothesis should not be rejected.")

        emp_n, emp_x = numpy.histogram(values2, bins=20, range=(0, 10))

        cs = ChiSquare(emp_n=emp_n, emp_x=emp_x)

        [c1, c2] = cs.test_distribution(alpha, 5, 1)

        self.assertGreater(c1, c2, msg="Error in Chi Square Test. Hypothesis should be rejected.")

if __name__ == '__main__':
    unittest.main()

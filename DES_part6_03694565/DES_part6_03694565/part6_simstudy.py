from statistictests import ChiSquare
import numpy

"""
This file should be used to keep all necessary code that is used for the verification section in part 6
of the programming assignment. It contains task 6.2.1.
"""

def task_6_2_1():
    """
    This task is used to verify the implementation of the chi square test.
    First, 100 samples are drawn from a normal distribution. Afterwards the chi square test is run on them to see,
    whether they follow the original or another given distribution.
    """
    # TODO Task 6.2.1: Your code goes here
    values = []
    mean = 0
    var = 1
    numpy.random.seed(0)
    for _ in range(100):
        values.append(numpy.random.normal(mean, var))

    for alpha in [.1, .05,.01]:
        for bin in [1, 2, 5, 10, 20, 30]:
            n, x = numpy.histogram(values, bins = bin, range=(-5,5))
            cs = ChiSquare(emp_n=n, emp_x=x)
            [chi2, chi2_table] = cs.test_distribution(alpha, mean, var)
            if chi2 > chi2_table:
                print("Alpha; " + str(alpha) + " Bins; " + str(bin) + " Chi2;" + str(chi2) + " Chi2 Table;" + str(chi2_table) + " Null hypothesis is rejected: the samples do not follow the standard normal distribution ")
            else:
                print("Alpha; " + str(alpha) + " Bins; " + str(bin) + " Chi2;" + str(chi2) + " Chi2 Table;" + str(chi2_table) +  " Null hypothesis is not rejected: the samples follow the standard normal distribution")

    #pass


if __name__ == '__main__':
    task_6_2_1()
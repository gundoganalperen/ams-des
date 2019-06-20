from scipy.stats import chi2, norm
from scipy.special import factorial
import math
from numpy.random import normal

class ChiSquare(object):

    def __init__(self, emp_x, emp_n, name="default"):
        """
        Initialize chi square test with observations and their frequency.
        :param emp_x: observation values (bins)
        :param emp_n: frequency
        :param name: name for better distinction of tests
        """
        self.name = name
        # TODO Task 6.1.1: Your code goes here
        self.emp_x = emp_x
        self.emp_n = emp_n
        self.chi2 = 0
        self.Ei = []
        #pass

    def test_distribution(self, alpha, mean, var):
        """
        Test, if the observations fit into a given distribution.
        :param alpha: significance of test
        :param mean: mean value of the gaussian distribution
        :param var: variance of the gaussian distribution
        """
        # TODO Task 6.1.1: Your code goes here

        n = sum(self.emp_n)
        for i in range(len(self.emp_x)-1):
            #self.Ei.append(n*self.normpdf(i, mean, var)) #as described in formula
            tmp = (norm(mean, math.sqrt(var)).cdf(self.emp_x[i]))*n
            tmp_1 = (norm(mean, math.sqrt(var)).cdf(self.emp_x[i+1]))*n
            self.Ei.append(tmp_1 - tmp)
        y = 0
        # Arranged expected and observed values after the set for lower values less than 5.
        arr_Ei = []
        arr_Oi = []
        while y < len(self.Ei):
            if self.Ei[y]>5:
                arr_Ei.append(self.Ei[y])
                arr_Oi.append(self.emp_n[y])
                y += 1
            else:
                tmp_e = 0
                tmp_o = 0
                # min Ei = 5 thus, combine the values lower than 5
                while tmp_e < 5:
                    tmp_e += self.Ei[y]
                    tmp_o += self.emp_n[y]
                    y += 1
                    if y==len(self.Ei):
                        break
                # Rearrange the array according to rule
                arr_Ei.append(tmp_e)
                arr_Oi.append(tmp_o)

        # Calculate the Xo^2
        for i in range(len(arr_Ei)):
            self.chi2 += ((arr_Oi[i] - arr_Ei[i])**2) / (arr_Ei[i])

        # degree of freedom k-s-1
        # where s is the number of parameters, in this scenario this is equal to 2(mean, variance)
        dof = len(arr_Ei) - 2 - 1
        # TABLE
        chi2_table = chi2.ppf(1-alpha, dof)

        #print("Mean;" + str(mean) + " Variance;" + str(var) + " Alpha;" + str(alpha) + " Chi2; " + str(self.chi2) + " Chi2 Table;" + str(chi2_table))
        """
        if self.chi2 > chi2_table:
            print("Hypothesis is rejected.")
        else:
            print("Hypothesis is not rejected.")
        """
        return [self.chi2, chi2_table]

        #pass

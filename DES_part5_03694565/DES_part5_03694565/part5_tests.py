import unittest
from counter import TimeIndependentCounter

class DESTest(unittest.TestCase):

    """
    This python unittest class checks the fifth part of the programming assignment for basic functionality.
    """

    def test_confidence(self):
        """
        Test the basic implementation of the confidence calculation in the time independent counter.
        """
        tic = TimeIndependentCounter()
        tic.count(0)
        tic.count(3)
        tic.count(5)
        tic.count(2)
        tic.count(5)
        tic.count(8)
        tic.count(1)
        tic.count(2)
        tic.count(1)

        self.assertAlmostEqual(tic.report_confidence_interval(.05, print_report=True), 1.96, delta=.01,
                               msg="Error in Confidence interval calculation. Wrong size of half interval returned.")
        self.assertAlmostEqual(tic.report_confidence_interval(.1, print_report=False), 1.58, delta=.01,
                               msg="Error in Confidence interval calculation. Wrong size of half interval returned.")
        self.assertAlmostEqual(tic.report_confidence_interval(.2, print_report=False), 1.187, delta=.01,
                               msg="Error in Confidence interval calculation. Wrong size of half interval returned.")

        self.assertEqual(tic.is_in_confidence_interval(4.5, alpha=.05), True,
                         msg="Error in Confidence interval calculation. Value should be in interval, but isn't.")
        self.assertEqual(tic.is_in_confidence_interval(1.3, alpha=.05), True,
                         msg="Error in Confidence interval calculation. Value should be in interval, but isn't.")
        self.assertEqual(tic.is_in_confidence_interval(5.0, alpha=.05), False,
                         msg="Error in Confidence interval calculation. Value id in interval, but shouldn't.")
        self.assertEqual(tic.is_in_confidence_interval(4.5, alpha=.1), True,
                         msg="Error in Confidence interval calculation. Value should be in interval, but isn't.")
        self.assertEqual(tic.is_in_confidence_interval(1.3, alpha=.1), False,
                         msg="Error in Confidence interval calculation. Value id in interval, but shouldn't.")
        self.assertEqual(tic.is_in_confidence_interval(5.0, alpha=.1), False,
                         msg="Error in Confidence interval calculation. Value id in interval, but shouldn't.")
        self.assertEqual(tic.is_in_confidence_interval(4.5, alpha=.2), False,
                         msg="Error in Confidence interval calculation. Value id in interval, but shouldn't.")
        self.assertEqual(tic.is_in_confidence_interval(1.3, alpha=.2), False,
                         msg="Error in Confidence interval calculation. Value id in interval, but shouldn't.")
        self.assertEqual(tic.is_in_confidence_interval(4.0, alpha=.2), True,
                         msg="Error in Confidence interval calculation. Value should be in interval, but isn't.")

        lower, upper = tic.report_bootstrap_confidence_interval(alpha=.05, resample_size=10000)
        self.assertAlmostEqual(lower, 1.55556, delta=0.01,
                               msg="Error in bootstrap confidence interval calculation. Wrong lower boundary.")
        self.assertAlmostEqual(upper, 4.66667, delta=0.01,
                               msg="Error in bootstrap confidence interval calculation. Wrong upper boundary.")

        self.assertEqual(tic.is_in_bootstrap_confidence_interval(4, resample_size=5000, alpha=.05), True,
                         msg="Error in Confidence interval calculation. Value should be in interval, but isn't.")
        self.assertEqual(tic.is_in_bootstrap_confidence_interval(1, resample_size=5000, alpha=.05), False,
                         msg="Error in Confidence interval calculation. Value id in interval, but shouldn't.")


if __name__ == '__main__':
    unittest.main()

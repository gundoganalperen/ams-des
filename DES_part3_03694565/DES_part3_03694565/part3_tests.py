import unittest
from simulation import Simulation

class DESTestRNG(unittest.TestCase):

    """
    This python unittest class checks the third part of the programming assignment for basic functionality.
    """

    # create default simulation setting for testing the methods
    sim = Simulation()

    def test_system_utilization(self):
        """
        Test the basic implementation of rho and the system utilization.
        """
        DESTestRNG.sim.sim_param.SIM_TIME = 1000
        DESTestRNG.sim.sim_param.S = 10000
        DESTestRNG.sim.sim_param.SEED_IAT = 0
        DESTestRNG.sim.sim_param.SEED_ST = 1

        for rho in [.01, .5, .8, .9]:
            DESTestRNG.sim.sim_param.RHO = rho
            DESTestRNG.sim.reset()
            r = DESTestRNG.sim.do_simulation().system_utilization
            self.assertAlmostEqual(r, rho, delta=rho*.2,
                                   msg="Error in RNG or CounterCollection. Should have gotten a different value for" + \
                                       " the system utilization with given rho.")

if __name__ == '__main__':
    unittest.main()

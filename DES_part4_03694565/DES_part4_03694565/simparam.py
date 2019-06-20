class SimParam(object):

    """
    Contains all important simulation parameters
    """

    def __init__(self):

        # current buffer spaces and minimal buffer spaces
        self.S_MIN = 4
        self.S = self.S_MIN  # waiting queue length

        self.S_MAX = 7  # calculated from the first part, should not be higher than S_VALUES
        self.S_VALUES = [5,6,7] # To test the queue capacity Task 2.7.1

        # inter-arrival-time and simulation time in ms
        self.IAT = 490
        self.SIM_TIME = 10000000

        # number of runs before first evaluation
        self.NO_OF_RUNS = 1000

        # maximal allowed packets to drop in one run (SIM_TIME)
        self.MAX_DROPPED = 10

        # set seed for random number generation
        self.SEED = 4565 # I could not write 03694565, it gave me an Syntax error.
        self.SEED_IAT = 0
        self.SEED_ST = 1

        # set desired utilization (rho)
        self.RHO = .5

    def print_sim_config(self):
        """
        Print a basic system configuration string.
        """
        print ("Simulation with parameters: T_SIM = " + str(self.SIM_TIME) + ", S = " + str(self.S))
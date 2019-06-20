class SimState(object):

    """
    SimState contains the basic simulation state.

    It contains the current time and a stop flag, indicating whether the simulation is still running.
    Furthermore, it contains the number of blocked (dropped) packets and the number of total packets.
    """

    def __init__(self):
        """
        Generate SimState objects and initialize variables.
        """
        self.now = 0
        self.stop = False
        self.num_packets = 0
        self.num_blocked_packets = 0

    def packet_accepted(self):
        """
        Count a packet that has been accepted by the system (queue or server).
        """
        self.num_packets += 1

    def packet_dropped(self):
        """
        Count a packet that has been rejected by the system.
        """
        self.num_packets += 1
        self.num_blocked_packets += 1

    def get_blocking_probability(self):
        """
        Get the blocking probability throughout the simulation.
        :return: blocking probability of the system
        """
        return float(self.num_blocked_packets)/float(self.num_packets)
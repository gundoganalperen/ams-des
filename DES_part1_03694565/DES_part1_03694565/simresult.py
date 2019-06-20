
class SimResult(object):

    """
    SimResults gathers all simulation results that are generated during the simulation.

    This object should be returned after a simulation to extract the data for output analysis.
    """

    def __init__(self, sim):
        """
        Initialize SimResult object
        :param sim: the simulation, this object belongs to
        :return: SimResult object
        """
        self.sim = sim
        self.system_utilization = 0
        self.packets_dropped = 0
        self.packets_served = 0
        self.packets_total = 0
        self.mean_waiting_time = 0
        self.mean_queue_length = 0
        self.blocking_probability = 0

    def gather_results(self):
        """
        Gather all available simulation results from SimState and CounterCollection
        """
        try:
            self.system_utilization = self.sim.counter_collection.cnt_sys_util.get_mean()
            self.mean_waiting_time = self.sim.counter_collection.acnt_wt.get_mean()
            self.mean_queue_length = self.sim.counter_collection.cnt_ql.get_mean()
        except:
            #print "counter_collection not available for getting simulation results."
            pass
        self.packets_dropped = self.sim.sim_state.num_blocked_packets
        self.packets_served = self.sim.sim_state.num_packets - self.sim.sim_state.num_blocked_packets
        self.packets_total = self.sim.sim_state.num_packets
        self.blocking_probability = self.sim.sim_state.get_blocking_probability()

    def update(self):
        """
        Gather all available simulation results from SimState and CounterCollection
        """
        self.gather_results()
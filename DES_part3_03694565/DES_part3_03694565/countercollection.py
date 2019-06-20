from counter import TimeIndependentCrosscorrelationCounter, TimeIndependentAutocorrelationCounter
from counter import TimeIndependentCounter, TimeDependentCounter
from histogram import TimeIndependentHistogram, TimeDependentHistogram


class CounterCollection(object):

    """
    CounterCollection is a collection of all counters and histograms that are used in the simulations.

    It contains several counters and histograms, that are used in the different tasks.
    Reporting is done by calling the report function. This function can be adapted, depending on which counters should
    report their results and print strings or plot histograms.
    """

    def __init__(self, sim):
        """
        Initialize the counter collection.
        :param sim: the simulation, the CounterCollection belongs to.
        """
        self.sim = sim

        # waiting time
        self.cnt_wt = TimeIndependentCounter()
        self.hist_wt = TimeIndependentHistogram(self.sim, "w")

        # queue length
        self.cnt_ql = TimeDependentCounter(self.sim)
        self.hist_ql = TimeDependentHistogram(self.sim, "q")

        # system utilization
        self.cnt_sys_util = TimeDependentCounter(self.sim)
        """
        # blocking probability
        self.cnt_bp = TimeIndependentCounter("bp")
        self.hist_bp = TimeIndependentHistogram(self.sim, "bp")

        # correlations
        self.cnt_iat_wt = TimeIndependentCrosscorrelationCounter("inter-arrival time vs. waiting time")
        self.cnt_iat_st = TimeIndependentCrosscorrelationCounter("inter-arrival time vs. service time")
        self.cnt_iat_syst = TimeIndependentCrosscorrelationCounter("inter-arrival time vs. system time")
        self.cnt_st_syst = TimeIndependentCrosscorrelationCounter("service time vs. system time")
        self.acnt_wt = TimeIndependentAutocorrelationCounter("waiting time with lags 1 to 20", max_lag=20)
        """

    def reset(self):
        """
        Resets all counters and histograms.
        """
        self.cnt_wt.reset()
        self.hist_wt.reset()

        self.cnt_ql.reset()
        self.hist_ql.reset()

        self.cnt_sys_util.reset()
        """
        self.cnt_bp.reset()
        self.hist_bp.reset()

        self.cnt_iat_wt.reset()
        self.cnt_iat_st.reset()
        self.cnt_iat_syst.reset()
        self.cnt_st_syst.reset()
        self.acnt_wt.reset()
        """

    def report(self):
        """
        Calls the report function of the counters and histograms.
        Can be adapted, such that not all reports are printed
        """
        self.cnt_wt.report()
        self.hist_wt.report()

        self.cnt_ql.report()
        self.hist_ql.report()

        self.cnt_sys_util.report()
        """
        self.cnt_iat_wt.report()
        self.cnt_iat_st.report()
        self.cnt_iat_syst.report()
        self.cnt_st_syst.report()
        self.acnt_wt.report()
        """

    def count_packet(self, packet):
        """
        Count a packet. Its data is counted by the various counters
        """
        self.cnt_wt.count(packet.get_waiting_time())
        self.hist_wt.count(packet.get_waiting_time())
        """
        self.cnt_iat_wt.count(packet.get_interarrival_time(), packet.get_waiting_time())
        self.cnt_iat_st.count(packet.get_interarrival_time(), packet.get_service_time())
        self.cnt_iat_syst.count(packet.get_interarrival_time(), packet.get_system_time())
        self.cnt_st_syst.count(packet.get_service_time(), packet.get_system_time())
        self.acnt_wt.count(packet.get_waiting_time())
        """

    def count_queue(self):
        """
        Count the number of packets in the buffer and add the values to the corresponding (time dependent) histogram.
        This function should be called at least whenever the number of packets in the buffer changes.

        The system utilization is counted as well and can be counted from the counter cnt_sys_util.
        """
        self.cnt_ql.count(self.sim.system_state.get_queue_length())
        self.hist_ql.count(self.sim.system_state.get_queue_length())

        # TODO Task 2.5.1: Your code goes here
        if self.sim.system_state.server_busy:
            self.cnt_sys_util.count(1)
        else:
            self.cnt_sys_util.count(0)
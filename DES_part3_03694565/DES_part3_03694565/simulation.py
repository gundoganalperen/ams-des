from simstate import SimState
from systemstate import SystemState
from event import EventChain, CustomerArrival, SimulationTermination
from simresult import SimResult
from simparam import SimParam
from countercollection import CounterCollection
from rng import RNG, ExponentialRNS, UniformRNS


class Simulation(object):

    def __init__(self, sim_param=SimParam(), no_seed=False):
        """
        Initialize the Simulation object.
        :param sim_param: is an optional SimParam object for parameter pre-configuration
        :param no_seed: is an optional parameter. If it is set to True, the RNG should be initialized without a
        a specific seed.
        """
        self.sim_param = sim_param
        self.sim_state = SimState()
        self.system_state = SystemState(self)
        self.event_chain = EventChain()
        self.sim_result = SimResult(self)
        # TODO Task 2.4.3: Uncomment the line below
        self.counter_collection = CounterCollection(self)
        # TODO Task 3.1.2: Uncomment the line below and replace the "None"

        if no_seed:
            #if the mean = 1.0, then 1/lambda_ = 1.0 -> lambda_ = 1
            self.rng = RNG(ExponentialRNS(1.0), ExponentialRNS(1./float(self.sim_param.RHO)))
        else:
            self.rng = RNG(ExponentialRNS(1.0, self.sim_param.SEED_IAT), ExponentialRNS(1./float(self.sim_param.RHO), self.sim_param.SEED_ST))


    def reset(self, no_seed=False):
        """
        Reset the Simulation object.
        :param no_seed: is an optional parameter. If it is set to True, the RNG should be reset without a
        a specific seed.
        """
        self.sim_state = SimState()
        self.system_state = SystemState(self)
        self.event_chain = EventChain()
        self.sim_result = SimResult(self)
        # TODO Task 2.4.3: Uncomment the line below
        self.counter_collection = CounterCollection(self)
        # TODO Task 3.1.2: Uncomment the line below and replace the "None"
        if no_seed:
            self.rng = RNG(ExponentialRNS(1.0), ExponentialRNS(1./float(self.sim_param.RHO)))
        else:
            self.rng = RNG(ExponentialRNS(1.0, self.sim_param.SEED_IAT), ExponentialRNS(1./float(self.sim_param.RHO),self.sim_param.SEED_ST))


    def do_simulation(self):
        """
        Do one simulation run. Initialize simulation and create first and last event.
        After that, one after another event is processed.
        :return: SimResult object
        """
        # insert first and last event
        self.event_chain.insert(CustomerArrival(self, 0))
        self.event_chain.insert(SimulationTermination(self, self.sim_param.SIM_TIME))

        # start simulation (run)
        while not self.sim_state.stop:

            # TODO Task 1.4.1: Your code goes here
            """
            Hint:

            You can use and adapt the following lines in your realization
            e = self.event_chain.remove_oldest_event()
            e.process()
            """
            e = self.event_chain.remove_oldest_event()
            if e:
                if self.sim_state.now <= e.timestamp:
                    self.sim_state.now = e.timestamp
                    self.counter_collection.count_queue()
                    e.process()

            else:
                self.sim_state.stop = True

            #pass
            # TODO Task 2.4.3: Your code goes here somewhere
        # gather results for sim_result object
        self.sim_result.gather_results()
        return self.sim_result

    def do_simulation_n_limit(self, n):
        """
        Call this function, if the simulation should stop after a given number of packets
        Do one simulation run. Initialize simulation and create first event.
        After that, one after another event is processed.
        :param n: number of customers, that are processed before the simulation stops
        :return: SimResult object
        """
        # insert first event
        self.event_chain.insert(CustomerArrival(self, 0))

        # start simulation (run)
        while not self.sim_state.stop:

            # TODO Task 4.3.2: Your code goes here
            # TODO Task 5.2.2: Your code goes here
            pass

        # gather results for sim_result object
        self.sim_result.gather_results()
        return self.sim_result

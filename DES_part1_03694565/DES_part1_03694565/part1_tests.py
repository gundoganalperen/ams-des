import unittest
from event import EventChain, CustomerArrival, ServiceCompletion, SimulationTermination
from systemstate import SystemState
from simulation import Simulation
import random

class DESTest(unittest.TestCase):

    """
    This python unittest class checks the first part of the programming assignment for basic functionality.
    """

    # create default simulation setting for testing the methods
    sim = Simulation()

    def test_system_state(self):
        """
        Test module SystemState. Add and remove packets from server and queue and check for correct behavior.
        """
        s = SystemState(DESTest.sim)

        # check correct initialization
        self.assertEqual([s.buffer_content, s.server_busy], [0, False],
                         msg="Error in SystemState. Wrong int indicates queue length, wrong bool server busy.")

        # check correct behavior of start_service() after init
        self.assertEqual(s.start_service(), False,
                         msg="Error in SystemState. Wrong value indicates wrong queue length.")

        # check correct adding of packets to server or queue
        self.assertEqual(s.add_packet_to_server(), True,
                         msg="Error in SystemState. Could not add packet to server though it should be idle.")
        self.assertEqual(s.add_packet_to_server(), False,
                         msg="Error in SystemState. Server not busy, though it should be.")
        self.assertEqual([s.buffer_content, s.server_busy], [0, True],
                         msg="Error in SystemState. Wrong int indicates queue length, wrong bool server busy.")
        self.assertEqual(s.add_packet_to_queue(), True,
                         msg="Error in SystemState. Server not busy, though busy though it shouldn't be.")
        self.assertEqual([s.buffer_content, s.server_busy], [1, True],
                         msg="Error in SystemState. Wrong int indicates queue length, wrong bool server busy.")
        self.assertEqual(s.add_packet_to_server(), False,
                         msg="Error in SystemState. Should not be able to add packet to server.")
        for _ in range(DESTest.sim.sim_param.S - 1):
            self.assertEqual(s.add_packet_to_queue(), True,
                             msg="Error in SystemState. Could not add packet to queue.")

        # check correct dropping of packets, when queue is full
        self.assertEqual(s.add_packet_to_queue(), False,
                         msg="Error in SystemState. Could add packet to queue though it should be full.")
        self.assertEqual([s.buffer_content, s.server_busy], [DESTest.sim.sim_param.S, True],
                         msg="Error in SystemState. Wrong int indicates queue length, wrong bool server busy.")

        # check behavior of function complete_service()
        s.complete_service()
        self.assertEqual([s.buffer_content, s.server_busy], [DESTest.sim.sim_param.S, False],
                         msg="Error in SystemState. Wrong int indicates queue length, wrong bool server busy.")

        # check behavior of function start_service()
        self.assertEqual(s.start_service(), True,
                         msg="Error in SystemState. Starting service should be possible at this point.")
        self.assertEqual([s.buffer_content, s.server_busy], [DESTest.sim.sim_param.S - 1, True],
                         msg="Error in SystemState. Wrong int indicates queue length, wrong bool server busy.")


    def test_event_chain(self):
        """
        Test module EventChain. Add and remove SimEvents and check the correct order.
        """
        # priorities: SC = 0, CA = 1, ST = 2
        e = EventChain()
        e.insert(CustomerArrival(None, 10))
        e.insert(SimulationTermination(None, 10))
        e.insert(ServiceCompletion(None, 10))
        e.insert(CustomerArrival(None, 5))
        e.insert(ServiceCompletion(None, 2))
        results = [[2, 0], [5, 1], [10, 0], [10, 1], [10, 2]]

        for r in results:
            ev = e.remove_oldest_event()
            self.assertEqual([ev.timestamp, ev.priority], r,
                             msg="Error in EventChain or SimEvent. Events are sorted or returned in the wrong order.")

        self.assertEqual(len(e.event_list), 0,
                         msg="Error in EventChain or SimEvent. EventChain should be empty.")


    def test_customer_arrival(self):
        """
        Test CustomerArrival process function. Check, whether adding customers to server or queue or dropping them
        works correctly.
        """
        DESTest.sim.reset()

        # initialize system
        DESTest.sim.system_state.buffer_content = DESTest.sim.sim_param.S - 1
        DESTest.sim.system_state.server_busy = False
        self.assertEqual([DESTest.sim.system_state.buffer_content, DESTest.sim.system_state.server_busy],
                         [DESTest.sim.sim_param.S - 1, False],
                         msg="Error in CustomerArrival test. System initialization failed.")

        # first ca should be served by the server, not enqueued
        CustomerArrival(DESTest.sim, 0).process()
        self.assertEqual([DESTest.sim.system_state.buffer_content, DESTest.sim.system_state.server_busy],
                         [DESTest.sim.sim_param.S - 1, True],
                         msg="Error in CustomerArrival. Packet has not been added to server.")
        self.assertEqual(len(DESTest.sim.event_chain.event_list), 2,
                         msg="Error in CustomerArrival. Wrong number of new SimEvents created in process function.")

        # second ca should be enqueued
        CustomerArrival(DESTest.sim, 0).process()
        self.assertEqual([DESTest.sim.system_state.buffer_content, DESTest.sim.system_state.server_busy],
                         [DESTest.sim.sim_param.S, True],
                         msg="Error in CustomerArrival. Packet should have been enqueued.")
        self.assertEqual(len(DESTest.sim.event_chain.event_list), 3,
                         msg="Error in CustomerArrival. Wrong number of new SimEvents created in process function.")

        # third ca should be dropped
        CustomerArrival(DESTest.sim, 0).process()
        self.assertEqual([DESTest.sim.system_state.buffer_content, DESTest.sim.system_state.server_busy],
                         [DESTest.sim.sim_param.S, True],
                         msg="Error in CustomerArrival. Packet should have been dropped.")
        self.assertEqual(len(DESTest.sim.event_chain.event_list), 4,
                         msg="Error in CustomerArrival. Wrong number of new SimEvents created in process function.")
        self.assertGreater(DESTest.sim.sim_state.num_blocked_packets, 0,
                           msg="Error in CustomerArrival. Should have counted at least one dropped packet.")

    def test_service_completion(self):
        """
        Test ServiceCompletion process function. Check, whether processing of service completion events works as
        desired (making server idle again or triggering new service start).
        """
        DESTest.sim.reset()

        # initialize system
        DESTest.sim.system_state.buffer_content = 1
        DESTest.sim.system_state.server_busy = True
        self.assertEqual([DESTest.sim.system_state.buffer_content, DESTest.sim.system_state.server_busy], [1, True],
                         msg="Error in ServiceCompletion test. Initialization failed.")

        # first service completion should insert new service completion and take packet from queue
        ServiceCompletion(DESTest.sim, 0).process()
        self.assertEqual([DESTest.sim.system_state.buffer_content, DESTest.sim.system_state.server_busy], [0, True],
                         msg="Error in ServiceCompletion. Server should be busy and queue should be empty.")
        self.assertEqual(len(DESTest.sim.event_chain.event_list), 1,
                         msg="Error in ServiceCompletion. Wrong number of new SimEvents created in process function.")

        # second service completion should make server idle again
        ServiceCompletion(DESTest.sim, 0).process()
        self.assertEqual([DESTest.sim.system_state.buffer_content, DESTest.sim.system_state.server_busy], [0, False],
                         msg="Error in ServiceCompletion. Server should be idle and queue should be empty.")
        self.assertEqual(len(DESTest.sim.event_chain.event_list), 1,
                         msg="Error in ServiceCompletion. Wrong number of new SimEvents created in process function.")

    def test_simulation_termination(self):
        """
        Check correct behavior of SimulationTermination. SimState stop flag should be set true.
        """
        DESTest.sim.reset()

        SimulationTermination(DESTest.sim, 0).process()
        self.assertEqual(DESTest.sim.sim_state.stop, True,
                         msg="Error in SimulationTermination. Stopping simulation doesn't work as expected.")

    def test_do_simulation(self):
        """
        Test whole simulation with different seeds for the correct results. Simulation is reinitialized after every run.
        """
        results = [17, 9, 11, 12, 14]
        for seed in range(5):
            DESTest.sim.reset()
            DESTest.sim.sim_param.SEED = seed
            random.seed(seed)
            self.assertEqual(DESTest.sim.do_simulation().packets_dropped, results[seed],
                             msg="Error in Simulation. Wrong number of dropped packets for given seed.")

if __name__ == '__main__':
    unittest.main()

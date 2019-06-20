import unittest
from simulation import Simulation
from systemstate import SystemState
from packet import Packet
from counter import TimeIndependentCounter, TimeDependentCounter
import random
import numpy

class DESTestExtended(unittest.TestCase):

    """
    This python unittest class checks the second part of the programming assignment for basic functionality.
    """

    # create default simulation setting for testing the methods
    sim = Simulation()

    def test_system_state(self):
        """
        Test module SystemState. Add and remove packets from server and queue and check for correct behavior.
        """
        s = SystemState(DESTestExtended.sim)

        # check correct initialization
        self.assertEqual([s.buffer.get_queue_length(), s.server_busy], [0, False],
                         msg="Error in SystemState. Wrong int indicates queue length, wrong bool server busy.")

        # check correct behavior of start_service() after init
        self.assertEqual(s.start_service(), False,
                         msg="Error in SystemState. Wrong value indicates wrong queue length.")

        # check correct adding of packets to server or queue
        self.assertEqual(s.add_packet_to_server(), True,
                         msg="Error in SystemState. Could not add packet to server though it should be idle.")
        self.assertEqual(s.add_packet_to_server(), False,
                         msg="Error in SystemState. Server not busy, though it should be.")
        self.assertEqual([s.buffer.get_queue_length(), s.server_busy], [0, True],
                         msg="Error in SystemState. Wrong int indicates queue length, wrong bool server busy.")
        self.assertEqual(s.add_packet_to_queue(), True,
                         msg="Error in SystemState. Server not busy, though busy though it shouldn't be.")
        self.assertEqual([s.buffer.get_queue_length(), s.server_busy], [1, True],
                         msg="Error in SystemState. Wrong int indicates queue length, wrong bool server busy.")
        self.assertEqual(s.add_packet_to_server(), False,
                         msg="Error in SystemState. Should not be able to add packet to server.")
        for _ in range(DESTestExtended.sim.sim_param.S - 1):
            self.assertEqual(s.add_packet_to_queue(), True,
                             msg="Error in SystemState. Could not add packet to queue.")

        # check correct dropping of packets, when queue is full
        self.assertEqual(s.add_packet_to_queue(), False,
                         msg="Error in SystemState. Could add packet to queue though it should be full.")
        self.assertEqual([s.buffer.get_queue_length(), s.server_busy], [DESTestExtended.sim.sim_param.S, True],
                         msg="Error in SystemState. Wrong int indicates queue length, wrong bool server busy.")

        # check behavior of function complete_service()
        s.complete_service()
        self.assertEqual([s.buffer.get_queue_length(), s.server_busy], [DESTestExtended.sim.sim_param.S, False],
                         msg="Error in SystemState. Wrong int indicates queue length, wrong bool server busy.")

        # check behavior of function start_service()
        self.assertEqual(s.start_service(), True,
                         msg="Error in SystemState. Starting service should be possible at this point.")
        self.assertEqual([s.buffer.get_queue_length(), s.server_busy], [DESTestExtended.sim.sim_param.S - 1, True],
                         msg="Error in SystemState. Wrong int indicates queue length, wrong bool server busy.")

    def test_packet(self):
        """
        Check correct behavior of the Packet class.
        """
        DESTestExtended.sim.sim_state.now = 5
        p0 = Packet(DESTestExtended.sim, 2)
        p1 = Packet(DESTestExtended.sim, 0)

        self.assertEqual([p0.completed, p0.served], [False, False],
                         msg="Error in Packet. Wrong completed flag or wrong served flag.")
        self.assertEqual([p1.completed, p1.served], [False, False],
                         msg="Error in Packet. Wrong completed flag or wrong served flag.")

        p0.start_service()
        self.assertEqual([p0.completed, p0.served], [False, True],
                         msg="Error in Packet. Wrong completed flag or wrong served flag.")
        self.assertEqual([p1.completed, p1.served], [False, False],
                         msg="Error in Packet. Wrong completed flag or wrong served flag.")

        DESTestExtended.sim.sim_state.now = 7
        p0.complete_service()
        p1.start_service()
        self.assertEqual([p0.completed, p0.served], [True, False],
                         msg="Error in Packet. Wrong completed flag or wrong served flag.")
        self.assertEqual([p1.completed, p1.served], [False, True],
                         msg="Error in Packet. Wrong completed flag or wrong served flag.")

        DESTestExtended.sim.sim_state.now = 10
        p1.complete_service()
        self.assertEqual([p0.completed, p0.served], [True, False],
                         msg="Error in Packet. Wrong completed flag or wrong served flag.")
        self.assertEqual([p1.completed, p1.served], [True, False],
                         msg="Error in Packet. Wrong completed flag or wrong served flag.")

        self.assertEqual([p0.t_arrival, p1.t_arrival], [5, 5],
                         msg="Error in Packet. Wrong arrival timestamp.")
        self.assertEqual([p0.t_start, p1.t_start], [5, 7],
                         msg="Error in Packet. Wrong start timestamp.")
        self.assertEqual([p0.t_complete, p1.t_complete], [7, 10],
                         msg="Error in Packet. Wrong complete timestamp.")
        self.assertEqual([p0.iat, p1.iat], [2, 0],
                         msg="Error in Packet. Wrong iat.")

        self.assertEqual([p0.get_waiting_time(), p1.get_waiting_time()], [0, 2],
                         msg="Error in Packet. Wrong waiting time returned.")
        self.assertEqual([p0.get_service_time(), p1.get_service_time()], [2, 3],
                         msg="Error in Packet. Wrong service time returned.")
        self.assertEqual([p0.get_system_time(), p1.get_system_time()], [2, 5],
                         msg="Error in Packet. Wrong system time returned.")
        self.assertEqual([p0.get_interarrival_time(), p1.get_interarrival_time()], [2, 0],
                         msg="Error in Packet. Wrong inter-arrival time returned.")

    def test_finite_queue(self):
        """
        Test the basic behavior of the finite queue.
        """
        DESTestExtended.sim.reset()
        s = SystemState(DESTestExtended.sim)
        self.assertEqual(s.get_queue_length(), 0,
                         msg="Error in FiniteQueue. Wrong queue length.")
        s.add_packet_to_queue()
        DESTestExtended.sim.sim_state.now = 5
        s.add_packet_to_queue()
        DESTestExtended.sim.sim_state.now = 10
        s.add_packet_to_queue()
        self.assertEqual(s.get_queue_length(), 3,
                         msg="Error in FiniteQueue. Wrong queue length.")
        s.server_busy = False
        s.start_service()
        self.assertEqual(s.server_busy, True,
                         msg="Error in FiniteQueue. Server should be busy.")
        self.assertEqual(s.served_packet.t_arrival, 0,
                         msg="Error in FiniteQueue. Arrival time of packet wrong.")
        self.assertEqual(s.get_queue_length(), 2,
                         msg="Error in FiniteQueue. Wrong queue length.")
        s.server_busy = False
        s.start_service()
        self.assertEqual(s.server_busy, True,
                         msg="Error in FiniteQueue. Server should be busy.")
        self.assertEqual(s.served_packet.t_arrival, 5,
                         msg="Error in FiniteQueue. Arrival time of packet wrong.")
        self.assertEqual(s.get_queue_length(), 1,
                         msg="Error in FiniteQueue. Wrong queue length.")
        s.server_busy = False
        s.start_service()
        self.assertEqual(s.server_busy, True,
                         msg="Error in FiniteQueue. Server should be busy.")
        self.assertEqual(s.served_packet.t_arrival, 10,
                         msg="Error in FiniteQueue. Arrival time of packet wrong.")
        self.assertEqual(s.get_queue_length(), 0,
                         msg="Error in FiniteQueue. Wrong queue length.")

    def test_TIC(self):
        """
        Test the TimeIndependentCounter
        """
        tic = TimeIndependentCounter()
        tic.count(3)
        tic.count(2)
        tic.count(5)
        tic.count(0)
        self.assertEqual(tic.get_mean(), 2.5,
                         msg="Error in TimeIndependentCounter. Wrong mean calculation or wrong counting.")
        self.assertEqual(tic.get_var(), numpy.var([3,2,5,0], ddof=1),
                         msg="Error in TimeIndependentCounter. Wrong variance calculation or wrong counting.")
        self.assertEqual(tic.get_stddev(), numpy.std([3,2,5,0], ddof=1),
                         msg="Error in TimeIndependentCounter. Wrong std dev calculation or wrong counting.")
        tic.reset()
        tic.count(3.)
        tic.count(2.)
        tic.count(5.)
        tic.count(0.)
        self.assertEqual(tic.get_mean(), 2.5,
                         msg="Error in TimeIndependentCounter. Wrong mean calculation or wrong counting.")
        self.assertEqual(tic.get_var(), numpy.var([3,2,5,0], ddof=1),
                         msg="Error in TimeIndependentCounter. Wrong variance calculation or wrong counting.")
        self.assertEqual(tic.get_stddev(), numpy.std([3,2,5,0], ddof=1),
                         msg="Error in TimeIndependentCounter. Wrong std dev calculation or wrong counting.")


    def test_TDC(self):
        """
        Test the TimeDependentCounter
        """
        DESTestExtended.sim.reset()
        tdc = TimeDependentCounter(DESTestExtended.sim)
        DESTestExtended.sim.sim_state.now = 2
        tdc.count(5)
        DESTestExtended.sim.sim_state.now = 6
        tdc.count(10)
        DESTestExtended.sim.sim_state.now = 8
        tdc.count(0)
        DESTestExtended.sim.sim_state.now = 10
        tdc.count(10)
        self.assertEqual(tdc.get_mean(), 7.0,
                         msg="Error in TimeDeependentCounter. Wrong mean calculation or wrong counting.")
        self.assertEqual(tdc.get_var(), 16.0,
                         msg="Error in TimeDeependentCounter. Wrong variance calculation or wrong counting.")
        self.assertEqual(tdc.get_stddev(), 4.0,
                         msg="Error in TimeDeependentCounter. Wrong std dev calculation or wrong counting.")

    def test_do_simulation(self):
        """
        Test whole simulation with different seeds for the correct results. Simulation is reinitialized after every run.
        """
        results = [17, 9, 11, 12, 14]
        for seed in range(5):
            DESTestExtended.sim.reset()
            DESTestExtended.sim.sim_param.SEED = seed
            random.seed(seed)
            self.assertEqual(DESTestExtended.sim.do_simulation().packets_dropped, results[seed],
                             msg="Error in Simulation. Wrong number of dropped packets for given seed.")

        self.assertLess(len(DESTestExtended.sim.counter_collection.cnt_wt.values), 210,
                        msg="Error in Simulation. Should count less than 210 values for waiting time.")
        self.assertGreater(len(DESTestExtended.sim.counter_collection.cnt_wt.values), 160,
                           msg="Error in Simulation. Should count more than 160 values for waiting time.")
        self.assertGreater(len(DESTestExtended.sim.counter_collection.cnt_ql.values), 5,
                           msg="Error in Simulation. Should count more than 5 values for queue length.")

if __name__ == '__main__':
    unittest.main()

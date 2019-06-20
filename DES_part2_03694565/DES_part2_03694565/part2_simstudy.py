from simparam import SimParam
from simulation import Simulation
import random
from histogram import TimeIndependentHistogram,TimeDependentHistogram, Histogram
#from counter import Counter, TimeIndependentCounter, TimeDependentCounter
import numpy
import matplotlib.pyplot as plt

"""
This file should be used to keep all necessary code that is used for the simulation study in part 2 of the programming
assignment. It contains the tasks 2.7.1 and 2.7.2.

The function do_simulation_study() should be used to run the simulation routine, that is described in the assignment.
"""

def task_2_7_1():
    """
    Here, you should execute task 2.7.1 (and 2.7.2, if you want)
    """
    # TODO Task 2.7.1: Your code goes here

    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim = Simulation(sim_param)
    return do_simulation_study(sim)

    #pass

def task_2_7_2():
    """
    Here, you can execute task 2.7.2 if you want to execute it in a separate function
    """
    # TODO Task 2.7.2: Your code goes here or in the function above
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim_param.SIM_TIME = 1000000
    sim = Simulation(sim_param)
    return do_simulation_study(sim)
    #pass


def do_simulation_study(sim, print_queue_length=False, print_waiting_time=True):
    """
    This simulation study is different from the one made in assignment 1. It is mainly used to gather and visualize
    statistics for different buffer sizes S instead of finding a minimal number of spaces for a desired quality.
    For every buffer size S (which ranges from 5 to 7), statistics are printed (depending on the input parameters).
    Finally, after all runs, the results are plotted in order to visualize the differences and giving the ability
    to compare them. The simulations are run first for 100s, then for 1000s. For each simulation time, two diagrams are
    shown: one for the distribution of the mean waiting times and one for the average buffer usage
    :param sim: the simulation object to do the simulation
    :param print_queue_length: print the statistics for the queue length to the console
    :param print_waiting_time: print the statistics for the waiting time to the console
    """
    # TODO Task 2.7.1: Your code goes here
    # TODO Task 2.7.2: Your code goes here

    hist_wt = TimeIndependentHistogram(sim, "w") #w is used to draw mean waiting time.

    # I can also create a variable from TimeIndependentHistogram class to use its plotting methods,
    # even if the queue length is depend on the time dependent system. Because I have already take this account for
    # calculation of its mean. Now, I have an array with the mean queue values for each run. Then, I can plot side by side
    # using the method of TimeIndependentHistogram.
    hist_ql = TimeIndependentHistogram(sim,"q")

    for i in range(sim.sim_param.S_VALUES[0],sim.sim_param.S_VALUES[-1]+1):
        mean_queue_length = []
        mean_waiting_times = []
        sim.counter_collection.cnt_ql.reset()
        sim.counter_collection.cnt_wt.reset()
        hist_wt.reset()
        hist_ql.reset()
        sim.sim_param.S = i
        for sim_run in range(sim.sim_param.NO_OF_RUNS):
            sim.reset()
            mean_queue_length.append(sim.do_simulation().mean_queue_length)
            mean_waiting_times.append(sim.do_simulation().mean_waiting_time)

        if print_waiting_time:
            print ("Queue Size = " + str(i) + " Number of Runs = " + str(sim.sim_param.NO_OF_RUNS) + " Sim.Time = " + str(sim.sim_param.SIM_TIME) + "ms" +  " Mean waiting times = " + str(numpy.mean(mean_waiting_times)) + " Mean Queue Length = " + str(numpy.mean((mean_queue_length))) + " Variance = " + str(numpy.var(mean_waiting_times)))
        #if print_queue_length:
           # print ("Queue Size = " + str(i) + " Number of Runs = " + str(sim.sim_param.NO_OF_RUNS) + " Sim.Time = " + str(sim.sim_param.SIM_TIME) + "ms" +  " Mean Queue Length = " + str(numpy.mean(mean_queue_length)) + " Mean Queue Length = " + str(numpy.mean((mean_queue_length))))



        hist_ql.values = mean_queue_length
        hist_wt.values = mean_waiting_times

        plt.subplot(121)
        plt.xlabel("Mean Waiting Time[ms] Sim.Time = " + str(sim.sim_param.SIM_TIME) + "ms")
        plt.ylabel("Probability Distribution")
        hist_wt.report()

        plt.subplot(122)
        plt.xlabel("Mean Queue Length Sim.Time = " + str(sim.sim_param.SIM_TIME) + "ms")
        plt.ylabel("Probability Distribution")
        hist_ql.report()

    plt.show()

    #pass


if __name__ == '__main__':
    task_2_7_1()
    task_2_7_2()
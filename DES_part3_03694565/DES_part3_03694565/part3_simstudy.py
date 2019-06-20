from rng import ExponentialRNS, UniformRNS
import matplotlib.pyplot as plt
import numpy
from simparam import SimParam
from simulation import Simulation
from counter import TimeIndependentCounter
import random

"""
This file should be used to keep all necessary code that is used for the verification section in part 3 of the
programming assignment. It contains tasks 3.2.1 and 3.2.2.
"""

def task_3_2_1():
    """
    This function plots two histograms for verification of the random distributions.
    One histogram is plotted for a uniform distribution, the other one for an exponential distribution.
    """
    # TODO Task 3.2.1: Your code goes here
    # For exponential dist. & uniform dist.
    samples = 10000
    exp = ExponentialRNS(1.)
    uni = UniformRNS(0.,10.)
    exp_dist = []
    uni_dist = []
    for k in range(samples):
        exp_dist.append(exp.next())
        uni_dist.append(uni.next())

    #weights_ = numpy.full(len(uni_dist), 1.0 / float(len(uni_dist)))
    ax0=plt.subplot(121)
    plt.xlabel("x")
    plt.ylabel("Number of instances")
    ax0.set_title("Exponential Distribution")
    plt.hist(exp_dist, density=True, bins=int(samples/100))

    ax1=plt.subplot(122)
    plt.xlabel("x")
    plt.ylabel("Probability density function of bin")
    ax1.set_title("Uniform Distribution")
    plt.hist(uni_dist,density=True,bins=int(samples/100))
    plt.show()

    #pass

def task_3_2_2():
    """
    Here, we execute task 3.2.2 and print the results to the console.
    The first result string keeps the results for 100s, the second one for 1000s simulation time.
    """
    # TODO Task 3.2.2: Your code goes here
    sim_param = SimParam()
    sim = Simulation(sim_param)
    count_sys = TimeIndependentCounter()
    sim_param.S = 5
    print("S = " + str(sim.sim_param.S))

    sim_param.SIM_TIME = 100000 #100s
    for rho in [0.01, 0.5, 0.8, 0.9]:
        sim.sim_param.RHO = rho
        sim.reset()
        count_sys.reset()
        for k in range(sim.sim_param.NO_OF_RUNS):
            r = sim.do_simulation().system_utilization
            count_sys.count(r)
        print("system_utilization = " + str(count_sys.get_mean()) + " RHO "+str(rho) + " Sim.Time=100s")

    sim_param.SIM_TIME = 1000000 #1000s
    for rho in [0.01, 0.5, 0.8, 0.9]:
        sim.sim_param.RHO = rho
        sim.reset()
        count_sys.reset()
        for k in range(sim.sim_param.NO_OF_RUNS):
            r = sim.do_simulation().system_utilization
            count_sys.count(r)
        print("system_utilization = " + str(count_sys.get_mean()) + " RHO "+str(rho) + " Sim.Time=1000s")

    sim_param = SimParam()
    sim = Simulation(sim_param)
    count_sys = TimeIndependentCounter()
    sim_param.S = 100000
    print("S = " + str(sim.sim_param.S))
    sim_param.SIM_TIME = 100000 #100s
    for rho in [0.01, 0.5, 0.8, 0.9]:
        sim.sim_param.RHO = rho
        sim.reset()
        count_sys.reset()
        for k in range(sim.sim_param.NO_OF_RUNS):
            r = sim.do_simulation().system_utilization
            count_sys.count(r)
        print("system_utilization = " + str(count_sys.get_mean()) + " RHO "+str(rho) + " Sim.Time=100s")

    sim_param.SIM_TIME = 1000000 #1000s
    for rho in [0.01, 0.5, 0.8, 0.9]:
        sim.sim_param.RHO = rho
        sim.reset()
        count_sys.reset()
        for k in range(sim.sim_param.NO_OF_RUNS):
            r = sim.do_simulation().system_utilization
            count_sys.count(r)
        print("system_utilization = " + str(count_sys.get_mean()) + " RHO "+str(rho) + " Sim.Time=1000s")


    sim_param = SimParam()
    sim = Simulation(sim_param)
    count_sys = TimeIndependentCounter()
    sim_param.S = 1
    print("S = " + str(sim.sim_param.S))
    sim_param.SIM_TIME = 100000 #100s
    for rho in [0.01, 0.5, 0.8, 0.9]:
        sim.sim_param.RHO = rho
        sim.reset()
        count_sys.reset()
        for k in range(sim.sim_param.NO_OF_RUNS):
            r = sim.do_simulation().system_utilization
            count_sys.count(r)
        print("system_utilization = " + str(count_sys.get_mean()) + " RHO "+str(rho) + " Sim.Time=100s")

    sim_param.SIM_TIME = 1000000 #1000s
    for rho in [0.01, 0.5, 0.8, 0.9]:
        sim.sim_param.RHO = rho
        sim.reset()
        count_sys.reset()
        for k in range(sim.sim_param.NO_OF_RUNS):
            r = sim.do_simulation().system_utilization
            count_sys.count(r)
        print("system_utilization = " + str(count_sys.get_mean()) + " RHO "+str(rho) + " Sim.Time=1000s")

if __name__ == '__main__':
    task_3_2_1()
    task_3_2_2()
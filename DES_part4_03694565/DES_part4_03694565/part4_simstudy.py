from counter import TimeIndependentAutocorrelationCounter, TimeIndependentCrosscorrelationCounter
from simparam import SimParam
from simulation import Simulation
import matplotlib.pyplot as plt
import numpy as np

"""
This file should be used to keep all necessary code that is used for the verification and simulation section in part 4
of the programming assignment. It contains tasks 4.2.1, 4.3.1 and 4.3.2.
"""

def task_4_2_1():
    """
    Execute exercise 4.2.1, which is basically just a test for the auto correlation.
    """
    # TODO Task 4.2.1: Your code goes here
    seq1 = TimeIndependentAutocorrelationCounter(max_lag=5)
    for i in range(5000):
        if i%2 == 0:
            seq1.count(1)
        else:
            seq1.count(-1)

    for i in range(5):
        seq1.get_auto_cor(i)
        print("Auro correlation sequence 1 for lag " + str(i) + " = " + str(seq1.get_auto_cor(i)))

    seq2 = TimeIndependentAutocorrelationCounter(max_lag=5)

    for i in range(5000):
        if (i+1)%3 == 0:
            seq2.count(-1)
        else:
            seq2.count(1)

    for i in range(5):
        seq1.get_auto_cor(i)
        print("Auro correlation sequence 2 for lag " + str(i) + " = " + str(seq1.get_auto_cor(i)))

    #pass

def task_4_3_1():
    """
    Run the correlation tests for given rho for all correlation counters in counter collection.
    After each simulation, print report results.
    SIM_TIME is set higher in order to avoid a large influence of startup effects
    """
    # TODO Task 4.3.1: Your code goes here
    sim_param = SimParam()
    sim = Simulation(sim_param)
    sim.sim_param.S = 10000
    sim.sim_param.SIM_TIME = 10000000
    for rho in [0.01, 0.5, 0.8, 0.95]:
        sim.sim_param.RHO = rho
        sim.reset()
        sim.counter_collection.reset()
        sim = sim.do_simulation().sim
        print("RHO = " + str(rho))
        print("Correlation between IAT and waiting time of a packet = " + str(sim.counter_collection.cnt_iat_wt.get_cor()))
        print("Correlation between IAT and serving time of a packet = " + str(sim.counter_collection.cnt_iat_st.get_cor()))
        print("Correlation between IAT and system time (waiting time + serving time) of a packet = " + str(sim.counter_collection.cnt_iat_syst.get_cor()))
        print("Correlation between serving time and system time of a packet = " + str(sim.counter_collection.cnt_st_syst.get_cor()))
        for lag in range(0,21):
            print("Lag = "+ str(lag) + " Auto-correlation of waiting time with lags ranging from 1 to 20 = " + str(sim.counter_collection.acnt_wt.get_auto_cor(lag)))

        print(" ")

    #pass

def task_4_3_2():
    """
    Exercise to plot the scatter plot of (a) IAT and serving time, (b) serving time and system time
    The scatter plot helps to better understand the meaning of bit/small covariance/correlation.
    For every rho, two scatter plots are needed.
    The simulation parameters are the same as in task_4_3_1()
    """
    # TODO Task 4.3.2: Your code goes here

    sim_param = SimParam()
    sim = Simulation(sim_param)
    sim.sim_param.S = 10000
    sim.sim_param.SIM_TIME = 10000000

    for rho in [0.01, 0.5, 0.8, 0.95]:
        sim.sim_param.RHO = rho
        sim.reset()
        sim.counter_collection.reset()
        sim = sim.do_simulation().sim
        cnt_iat = sim.counter_collection.cnt_iat_st.values_x
        cnt_st = sim.counter_collection.cnt_iat_st.values_y
        cnt_syst =sim.counter_collection.cnt_st_syst.values_y

        corr_iat_st = float(sim.counter_collection.cnt_iat_st.get_cor())
        corr_st_syst = float(sim.counter_collection.cnt_st_syst.get_cor())
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        plt.subplot(1,2,1)
        plt.title('Rho %.2f Correlation %.3f'%(rho,corr_iat_st))
        plt.xlabel("Correlation IAT - ST")
        plt.plot(cnt_iat, cnt_st, 'o')

        plt.subplot(1,2,2)
        plt.title('Rho %.2f Correlation %.3f'%(rho,corr_st_syst))
        plt.xlabel("Correlation ST - SYST")
        plt.plot(cnt_st,cnt_syst,'o')

    plt.show()

    #pass

def task_4_3_3():
    """
    Exercise to plot auto correlation depending on lags. Run simulation until 10000 (or 100) packets are served.
    For the different rho values, simulation is run and the waiting time is auto correlated.
    Results are plotted for each N value in a different diagram.
    Note, that for some seeds with rho=0.01 and N=100, the variance of the auto covariance is 0 and returns an error.
    """
    # TODO Task 4.3.3: Your code goes here
    sim_param = SimParam()
    sim = Simulation(sim_param)
    sim.sim_param.S = 100000 #So that, there will be no dropped packets
    auto_corr_100 = {}

    for rho in [0.01, 0.5, 0.8, 0.95]:
        sim.sim_param.RHO = rho
        sim.reset()
        sim.counter_collection.reset()
        sim_100 = sim.do_simulation_n_limit(100).sim

        auto_corr_100[rho] = []
        for lag in range(0,21):
            auto_corr_100[rho].append(sim_100.counter_collection.acnt_wt.get_auto_cor(lag))


    auto_corr_10000 = {}
    for rho in [0.01, 0.5, 0.8, 0.95]:
        sim.sim_param.RHO = rho
        sim.reset()
        sim.counter_collection.reset()
        sim_10000 = sim.do_simulation_n_limit(10000).sim
        auto_corr_10000[rho] = []
        for lag in range(0,21):
            auto_corr_10000[rho].append(sim_10000.counter_collection.acnt_wt.get_auto_cor(lag))

    lags = np.arange(0,21,1)
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    plt.subplot(1,2,1)
    plt.title("N = 100")
    plt.xlabel("Number of lags")
    plt.ylabel("Autocorrelation waiting time")
    for rho in [0.01, 0.5, 0.8, 0.95]:
        plt.plot(lags, auto_corr_100[rho],label="rho=%.2f"%(rho,))

    leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.subplot(1,2,2)
    plt.title("N = 10000")
    plt.xlabel("Number of lags")
    plt.ylabel("Autocorrelation waiting time")
    for rho in [0.01, 0.5, 0.8, 0.95]:
        plt.plot(lags, auto_corr_10000[rho],label="rho=%.2f"%(rho,))

    leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.show()


    #pass

if __name__ == '__main__':
    task_4_2_1()
    task_4_3_1()
    task_4_3_2()
    task_4_3_3()

from counter import TimeIndependentCounter
from simulation import Simulation
from matplotlib import pyplot
from simparam import SimParam


"""
This file should be used to keep all necessary code that is used for the simulation section in part 5
of the programming assignment. It contains tasks 5.2.1, 5.2.2, 5.2.3 and 5.2.4.
"""

def task_5_2_1():
    """
    Run task 5.2.1. Make multiple runs until the blocking probability distribution reaches
    a confidence level alpha. Simulation is performed for 100s and 1000s and for alpha = 90% and 95%.
    """
    results = [None, None, None, None]
    # TODO Task 5.2.1: Your code goes here
    bp = []
    hw = []
    sim_param = SimParam()
    sim = Simulation(sim_param)
    sim.sim_param.S = 4
    sim.sim_param.RHO = .9
    count_bp = TimeIndependentCounter()
    err = .0015
    i = 0
    for sim_time in [100000, 1000000]:
        sim.sim_param.SIM_TIME = sim_time
        for alpha in [.1, .05]:
            count_bp.reset()
            while 1:
                sim.reset()
                blocking_pro = sim.do_simulation().blocking_probability
                count_bp.count(blocking_pro)
                half_width = count_bp.report_confidence_interval(alpha=alpha)
                if half_width < err:
                    break

            results[i] = len(count_bp.values)
            bp.append(count_bp.get_mean())
            hw.append(half_width)
            i += 1

# print and return results
    print ("SIM TIME:  100s; ALPHA: 10%; NUMBER OF RUNS: " + str(results[0]) + "; TOTAL SIMULATION TIME (SECONDS): " + str(results[0]*100) + "; Blocking Probability Mean: " + str(bp[0])+ "; Half width: " + str(hw[0]))
    print ("SIM TIME:  100s; ALPHA:  5%; NUMBER OF RUNS: " + str(results[1]) + "; TOTAL SIMULATION TIME (SECONDS): " + str(results[1]*100)+ "; Blocking Probability Mean: " + str(bp[1])+ "; Half width: " + str(hw[1]))
    print ("SIM TIME: 1000s; ALPHA: 10%; NUMBER OF RUNS:  " + str(results[2]) + "; TOTAL SIMULATION TIME (SECONDS): " + str(results[2]*1000)+ "; Blocking Probability Mean: " + str(bp[2])+ "; Half width: " + str(hw[2]))
    print ("SIM TIME: 1000s; ALPHA:  5%; NUMBER OF RUNS:  " + str(results[3]) + "; TOTAL SIMULATION TIME (SECONDS): " + str(results[3]*1000)+ "; Blocking Probability Mean: " + str(bp[3])+ "; Half width: " + str(hw[3]))
    return results

def task_5_2_2():
    """
    Run simulation in batches. Start the simulation with running until a customer count of n=100 or (n=1000) and
    continue to increase the number of customers by dn=n.
    Count the blocking proabability for the batch and calculate the confidence interval width of all values, that have
    been counted until now.
    Do this until the desired confidence level is reached and print out the simulation time as well as the number of
    batches.
    """
    results = [None, None, None, None]
    # TODO Task 5.2.2: Your code goes here
    bp = []
    hw = []
    sim_param = SimParam()
    sim = Simulation(sim_param)
    sim.sim_param.S = 4
    sim.sim_param.RHO = .9
    err = .0015
    half_width = 1.0
    count_bp = TimeIndependentCounter()
    i = 0
    for batch in [100, 1000]:
        for alpha in [.1, .05]:
            first_batch = False
            count_bp.reset()
            sim.reset()
            while 1:
                blocking_pro = sim.do_simulation_n_limit(batch, first_batch).blocking_probability
                first_batch = True  #after first batch
                count_bp.count(blocking_pro)
                half_width = count_bp.report_confidence_interval(alpha)
                sim.sim_state.stop = False  #set the parameter back to original value
                sim.counter_collection.reset()
                sim.sim_state.num_blocked_packets = 0
                sim.sim_state.num_packets = 0
                if half_width < err:
                    break
            results[i] = sim.sim_state.now
            bp.append(count_bp.get_mean())
            hw.append(half_width)
            i += 1

    # print and return results
    print ("BATCH SIZE:  100; ALPHA: 10%; TOTAL SIMULATION TIME (SECONDS): " + str(results[0]/1000)+ "; Blocking Probability Mean: " + str(bp[0])+ "; Half width: " + str(hw[0]))
    print ("BATCH SIZE:  100; ALPHA:  5%; TOTAL SIMULATION TIME (SECONDS): " + str(results[1]/1000)+ "; Blocking Probability Mean: " + str(bp[1])+ "; Half width: " + str(hw[1]))
    print ("BATCH SIZE: 1000; ALPHA: 10%; TOTAL SIMULATION TIME (SECONDS): " + str(results[2]/1000)+ "; Blocking Probability Mean: " + str(bp[2])+ "; Half width: " + str(hw[2]))
    print ("BATCH SIZE: 1000; ALPHA:  5%; TOTAL SIMULATION TIME (SECONDS): " + str(results[3]/1000)+ "; Blocking Probability Mean: " + str(bp[3])+ "; Half width: " + str(hw[3]))
    return results

def task_5_2_4():
    """
    Plot confidence interval as described in the task description for task 5.2.4.
    We use the function plot_confidence() for the actual plotting and run our simulation several times to get the
    samples. Due to the different configurations, we receive eight plots in two figures.
    """
    # TODO Task 5.2.4: Your code goes here

    sim_param = SimParam()
    sim = Simulation(sim_param)
    sim.sim_param.S = 40000000 #infinite M/M/1/inf
    err = .0015
    plt_no = 1
    for rho in [0.5,0.9]:
        sim.sim_param.RHO = rho
        for alpha in [0.1, 0.05]:
            for sim_time in [100000, 1000000]:
                sim.sim_param.SIM_TIME = sim_time
                print(" Sim time " + str(sim.sim_param.SIM_TIME / 1000) + "s " + " Alpha " + str(alpha) + " RHO " + str(rho))
                count_util = TimeIndependentCounter()
                mean_count = TimeIndependentCounter()
                y_low = []
                y_high = []
                x = []
                for repeat in range(100):
                    count_util.reset()
                    for sim_run in range(30):
                        sim.reset()
                        count_util.count(sim.do_simulation().system_utilization)

                    mean = count_util.get_mean()
                    half_width = count_util.report_confidence_interval(alpha=alpha)
                    mean_count.count(mean)
                    y_low.append(mean - half_width)
                    y_high.append(mean + half_width)
                    x.append(repeat+1)

                pyplot.subplot(2,2,plt_no)
                plt_no += 1
                plot_confidence(sim, x, y_low, y_high, mean_count.get_mean(), sim.sim_param.RHO, "Utilization", alpha)


        pyplot.show()
        plt_no = 1
#pass

def plot_confidence(sim, x, y_min, y_max, calc_mean, act_mean, ylabel, alpha):
    """
    Plot confidence levels in batches. Inputs are given as follows:
    :param sim: simulation, the measurement object belongs to.
    :param x: defines the batch ids (should be an array).
    :param y_min: defines the corresponding lower bound of the confidence interval.
    :param y_max: defines the corresponding upper bound of the confidence interval.
    :param calc_mean: is the mean calculated from the samples.
    :param act_mean: is the analytic mean (calculated from the simulation parameters).
    :param ylabel: is the y-label of the plot
    :return:
    """
    # TODO Task 5.2.3: Your code goes here
    """
    Note: You can change the input parameters, if you prefer to.
    """
    pyplot.vlines(x, y_min, y_max, colors='r')

    pyplot.hlines(calc_mean, 0, 99, linestyles='-.', colors='g', label='sample mean')
    #actual
    pyplot.hlines(act_mean, 0, 99, label='rho', linestyles='-.', colors='y')
    pyplot.xlim([0, 100])
    pyplot.ylim([sim.sim_param.RHO - 0.1, sim.sim_param.RHO + 0.1])
    pyplot.ylabel(ylabel)
    pyplot.xlabel('Repeat no')
    pyplot.title("RHO " + str(sim.sim_param.RHO) + " Alpha " + str(alpha) +  " Sim Time " + str(sim.sim_param.SIM_TIME))


if __name__ == '__main__':
    task_5_2_1()
    task_5_2_2()
    task_5_2_4()

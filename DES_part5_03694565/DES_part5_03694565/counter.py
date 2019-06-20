import math
import numpy
import scipy
import scipy.stats

class Counter(object):

    """
    Counter class is an abstract class, that counts values for statistics.

    Values are added to the internal array. The class is able to generate mean value, variance and standard deviation.
    The report function prints a string with name of the counter, mean value and variance.
    All other methods have to be implemented in subclasses.
    """

    def __init__(self, name="default"):
        """
        Initialize a counter with a name.
        The name is only for better distinction between counters.
        :param name: identifier for better distinction between various counters
        """
        self.name = name
        self.values = []

    def count(self, *args):
        """
        Count values and add them to the internal array.
        Abstract method - implement in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def reset(self, *args):
        """
        Delete all values stored in internal array.
        """
        self.values = []

    def get_mean(self):
        """
        Returns the mean value of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def get_var(self):
        """
        Returns the variance of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def get_stddev(self):
        """
        Returns the standard deviation of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def report(self):
        """
        Print report for this counter.
        """
        if len(self.values) != 0:
            print ("Name: " + str(self.name) + ", Mean: " + str(self.get_mean()) + ", Variance: " + str(self.get_var()))
        else:
            print("List for creating report is empty. Please check.")


class TimeIndependentCounter(Counter):
    
    """
    Counter for counting values independent of their duration.

    As an extension, the class can report a confidence interval and check if a value lies within this interval.
    """
    
    def __init__(self, name="default"):
        """
        Initialize the TIC object.
        """
        super(TimeIndependentCounter, self).__init__(name)
    
    def count(self, *args):
        """
        Add a new value to the internal array. Parameters are chosen as *args because of the inheritance to the
        correlation counters.
        :param: *args is the value that should be added to the internal array
        """
        self.values.append(args[0])
        
    def get_mean(self):
        """
        Return the mean value of the internal array.
        """
        # TODO Task 2.3.1: Your code goes here
        return numpy.mean(self.values)
        #pass

    def get_var(self):
        """
        Return the variance of the internal array.
        Note, that we take the estimated variance, not the exact variance.
        """
        # TODO Task 2.3.1: Your code goes here
        return numpy.var(self.values, ddof=1)
        #pass

    def get_stddev(self):
        """
        Return the standard deviation of the internal array.
        """
        # TODO Task 2.3.1: Your code goes here
        return numpy.std(self.values, ddof=1)
        #pass

    def report_confidence_interval(self, alpha=0.05, print_report=True):
        """
        Report a confidence interval with given significance level.
        This is done by using the t-table provided by scipy.
        :param alpha: is the significance level (default: 5%)
        :param print_report: enables an output string
        :return: half width of confidence interval h
        """
        # TODO Task 5.1.1: Your code goes here
        n = len(self.values)
        std = self.get_stddev()
        z_critical = scipy.stats.t._ppf((2-alpha)/2.,n-1)
        margin_of_error = z_critical * std/(math.sqrt(n))
        return margin_of_error
        #pass

    def is_in_confidence_interval(self, x, alpha=0.05):
        """
        Check if sample x is in confidence interval with given significance level.
        :param x: is the sample
        :param alpha: is the significance level
        :return: true, if sample is in confidence interval
        """
        # TODO Task 5.1.1: Your code goes here
        mean = self.get_mean()
        error_margin = self.report_confidence_interval(alpha)
        l_end = mean - error_margin
        u_end = mean + error_margin
        if l_end <= x <= u_end:
            return True
        else:
            return False
        #pass

    def report_bootstrap_confidence_interval(self, alpha=0.05, resample_size=5000, print_report=True):
        """
        Report bootstrapping confidence interval with given significance level.
        This is done with the bootstrap method. Hint: use numpy.random.choice for resampling
        :param alpha: significance level
        :param resample_size: resampling size
        :param print_report: enables an output string
        :return: lower and upper bound of confidence interval
        """
        # TODO Task 5.1.2: Your code goes here
        means = []
        means.append(self.get_mean())
        for _ in range(resample_size):
            resampled_data = numpy.random.choice(self.values,len(self.values),replace = True)
            means.append(numpy.mean(resampled_data))

        means_ordered = numpy.sort(means)
        p = alpha/2. * 100
        l_end = numpy.percentile(means_ordered, p)
        p = ((2.0 - alpha)/2.) * 100
        u_end = numpy.percentile(means_ordered, p)
        return l_end, u_end

        #pass

    def is_in_bootstrap_confidence_interval(self, x, resample_size=5000, alpha=0.05):
        """
        Check if sample x is in bootstrap confidence interval with given resample_size and significance level.
        :param x: is the sample
        :param resample_size: resample size
        :param alpha: is the significance level
        :return: true, if sample is in confidence interval
        """
        # TODO Task 5.1.2: Your code goes here
        low, up = self.report_bootstrap_confidence_interval(alpha = alpha, resample_size=resample_size)
        if low <= x <= up:
            return True
        else:
            return False

        #pass


class TimeDependentCounter(Counter):
    
    """
    Counter, that counts values considering their duration as well.

    Methods for calculating mean, variance and standard deviation are available.
    """
    
    def __init__(self, sim, name="default"):
        """
        Initialize TDC with the simulation it belongs to and the name.
        :param: sim is needed for getting the current simulation time.
        :param: name is an identifier for better distinction between multiple counters.
        """
        super(TimeDependentCounter, self).__init__(name)
        self.sim = sim
        self.first_timestamp = 0
        self.last_timestamp = 0
        self.time_interval = []

    def count(self, value):
        """
        Adds new value to internal array.
        Duration from last to current value is considered.
        """
        # TODO Task 2.3.2: Your code goes here
        self.last_timestamp = self.sim.sim_state.now
        self.time_interval.append(self.last_timestamp - self.first_timestamp)
        self.first_timestamp = self.last_timestamp
        self.values.append(value)
        #pass
        
    def get_mean(self):
        """
        Return the mean value of the counter, normalized by the total duration of the simulation.
        """
        # TODO Task 2.3.2: Your code goes here
        sum = 0
        for i in range(len(self.values)):
            sum += self.values[i] * self.time_interval[i]

        return sum/self.last_timestamp
        #pass
        
    def get_var(self):
        """
        Return the variance of the TDC.
        """
        # TODO Task 2.3.2: Your code goes here
        sum = 0
        for i in range(len(self.values)):
            sum += (self.values[i]**2) * self.time_interval[i]

        return (sum/self.last_timestamp) - (self.get_mean()**2)
        #pass
        
    def get_stddev(self):
        """
        Return the standard deviation of the TDC.
        """
        # TODO Task 2.3.2: Your code goes here
        return math.sqrt(self.get_var())
        #pass
    
    def reset(self):
        """
        Reset the counter to its initial state.
        """
        self.first_timestamp = self.sim.sim_state.now
        self.last_timestamp = self.sim.sim_state.now
        self.time_interval = []
        Counter.reset(self)


class TimeIndependentCrosscorrelationCounter(TimeIndependentCounter):

    """
    Counter that is able to calculate cross correlation (and covariance).
    """
    # store two values
    # high arriving rate -> high queue size
    # if a packet behind the packet that has waited longer time -> then new arrived packet likely wait more time, autocorrelation var.
    # find a stability of lag size, or the point where it oscillates
    def __init__(self, name="default"):
        """
        Crosscorrelation counter contains three internal counters containing the variables
        :param name: is a string for better distinction between counters.
        """
        super(TimeIndependentCrosscorrelationCounter, self).__init__(name)
        # TODO Task 4.1.1: Your code goes here

        self.values_x = []
        self.values_y = []
        #pass

    def reset(self):
        """
        Reset the TICCC to its initial state.
        """
        TimeIndependentCounter.reset(self)
        # TODO Task 4.1.1: Your code goes here
        self.values_x = []
        self.values_y = []
        #pass

    def count(self, x, y):
        """
        Count two values for the correlation between them. They are added to the two internal arrays.
        """
        # TODO Task 4.1.1: Your code goes here
        self.values_x.append(x)
        self.values_y.append(y)
        #pass

    def get_cov(self):
        """
        Calculate the covariance between the two internal arrays x and y.
        :return: cross covariance
        """
        # TODO Task 4.1.1: Your code goes here

        tmp = numpy.multiply(self.values_x, self.values_y)

        return float(numpy.mean(tmp) - numpy.mean(self.values_x)*numpy.mean(self.values_y))

        #pass

    def get_cor(self):
        """
        Calculate the correlation between the two internal arrays x and y.
        :return: cross correlation
        """
        # TODO Task 4.1.1: Your code goes here
        return float(self.get_cov() / numpy.sqrt(numpy.var(self.values_x, ddof=1)*numpy.var(self.values_y, ddof=1)))
        #pass

    def report(self):
        """
        Print a report string for the TICCC.
        """
        print ("Name: " + self.name + "; covariance = " + str(self.get_cov()) + "; correlation = " + str(self.get_cor()))


class TimeIndependentAutocorrelationCounter(TimeIndependentCounter):

    """
    Counter, that is able to calculate auto correlation with given lag.
    """

    def __init__(self, name="default", max_lag=10):
        """
        Create a new auto correlation counter object.
        :param name: string for better distinction between multiple counters
        :param max_lag: maximum available lag (defaults to 10)
        """
        super(TimeIndependentAutocorrelationCounter, self).__init__(name)
        # TODO Task 4.1.2: Your code goes here
        self.values_lag = []
        self.max_lag = max_lag
        #pass

    def reset(self):
        """
        Reset the counter to its original state.
        """
        TimeIndependentCounter.reset(self)
        # TODO Task 4.1.2: Your code goes here
        self.values_lag = []
        #pass

    def count(self, x):
        """
        Add new element x to counter.
        """
        # TODO Task 4.1.2: Your code goes here
        self.values.append(x)
        #pass

    def get_auto_cov(self, lag):
        """
        Calculate the auto covariance for a given lag.
        :return: auto covariance
        """
        # TODO Task 4.1.2: Your code goes here
        self.values_lag = numpy.roll(self.values, lag)
        tmp = numpy.multiply(self.values, self.values_lag)
        x = float(numpy.mean(tmp) - numpy.mean(self.values)*numpy.mean(self.values_lag))
        return float(numpy.mean(tmp) - numpy.mean(self.values)*numpy.mean(self.values_lag))
        #pass

    def get_auto_cor(self, lag):
        """
        Calculate the auto correlation for a given lag.
        :return: auto correlation
        """
        # TODO Task 4.1.2: Your code goes here
        self.values_lag = numpy.roll(self.values, lag)
        x = float(self.get_auto_cov(lag) / numpy.sqrt(numpy.var(self.values, ddof=1)*numpy.var(self.values_lag, ddof=1)))

        return float(self.get_auto_cov(lag) / numpy.sqrt(numpy.var(self.values, ddof=1)*numpy.var(self.values_lag, ddof=1)))
        #pass

    def set_max_lag(self, max_lag):
        """
        Change maximum lag. Cycle length is set to max_lag + 1.
        """
        # TODO Task 4.1.2: Your code goes here
        self.max_lag = max_lag
        #pass

    def report(self):
        """
        Print report for auto correlation counter.
        """
        print ("Name: " + self.name)
        for i in range(0, self.max_lag+1):
            print ("Lag = " + str(i) + "; covariance = " + str(self.get_auto_cov(i)) + "; correlation = " + str(self.get_auto_cor(i)))
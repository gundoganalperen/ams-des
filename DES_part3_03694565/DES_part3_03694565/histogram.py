import numpy
from matplotlib import pyplot


class Histogram(object):

    """
    Histogram can take values for statistics and plot a histogram from them.

    Values are added to the internal array. The class is able to generate a histogram and plot it using pyplot.
    This class is an abstract class and contains some methods, that need to be implemented in subclass.
    """

    # colors for plotting multiple plots in one figure
    colors = ['b', 'g', 'w', 'c', 'm', 'y', 'k', 'r']

    def __init__(self, sim, typestr):
        """
        Constructor for a simple histogram
        :param sim: simulation, the histogram object belongs to
        :param typestr is mainly for the sake of distinguishing between multiple histograms but information can also
        be used for configuring the plot
        """
        self.sim = sim
        self.values = []
        self.histogram = None
        self.bins = []
        self.bin_mids = []
        self.type = typestr

    def count(self, value):
        """
        Add a value to the histogram.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please implement method")

    def reset(self):
        """
        Reset all values to their initial state.
        """
        self.values = []
        self.histogram = None
        self.bins = []
        self.bin_mids = []

    def report(self):
        """
        Show the histogram to the viewer.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError

    def plot(self, diag_type="histogram", show_plot=False):
        """
        Plot function for histogram.
        :param diag_type: string can be "histogram" for a standard bar plot (default), "side-by-side" for a
        side by side histogram or "line" for a line plot
        :param show_plot: display plot after generating it. Can be set to False, if the figure contains multiple plots.
        """
        width = self.bins[1] - self.bins[0]
        self.bin_mids = [x+(width/2.) for x in self.bins[0:len(self.bins)-1]]

        if diag_type == "line":
            """
            Plot line plot - mainly thought for mean waiting time
            """
            pyplot.plot(self.bin_mids, self.histogram, "+-", label='S=' + str(self.sim.sim_param.S))

        elif diag_type == "side-by-side":
            """
            Plot side-by-side histogram plot - mainly thought for mean queue length
            """
            # TODO Task 2.4.4: Your code goes here somewhere
            #bar_width = 0.25 #we need to distribute 3 S_VALUES over the line
            #in order to not the coincide the S values, we need to leave enough space between them.
            # But first, we need to find for which S value is used to draw.

            width = 0.3
            s_range = 0
            for k in range(len(self.sim.sim_param.S_VALUES)):
                if self.sim.sim_param.S_VALUES[k] == self.sim.sim_param.S:
                    s_range = self.sim.sim_param.S

            index = self.bins[0:len(self.bins)-1] + s_range * width - 1.0
            pyplot.bar(index, self.histogram, width=width, color = Histogram.colors[s_range], label = 'S=' + str(s_range))


        elif diag_type == "histogram":
            """
            Plot histogram - mainly thought for mean queue length
            (easier but worse interpretation than side-by-side)
            """
            weights = numpy.full(len(self.values), 1.0 / float(len(self.values)))
            pyplot.hist(self.values, self.bins, alpha=0.5, label='S='+str(self.sim.sim_param.S), rwidth=.7, weights=weights)

        else:
            raise TypeError("Undefined histogram plotting types: %s" % diag_type)

        pyplot.legend(loc='upper right')
        if show_plot:
            pyplot.show()


class TimeIndependentHistogram(Histogram):

    """
    Histogram for plotting values independent of their duration.
    """

    def __init__(self, sim, typestr):
        """
        Initialize histogram with the simulation it belongs to and a typestring for better distinction
        :param sim: simulation object, the histogram belongs to
        :param typestr: typestring for better distinction and selection of plot type
        q stands for queue length and will default to a side-by-side plot type
        bp stands for blocking probability and will default to a normal histogram plot type
        else, the plot type defaults to a line plot
        """
        super(TimeIndependentHistogram, self).__init__(sim, typestr)

    def count(self, value):
        """
        Add new value to histogram, i.e., the internal array.
        """
        # TODO Task 2.4.1: Your code goes here
        self.values.append(value)
        #pass

    def report(self):
        """
        Make report, i.e., calculate histogram and bins using numpy.

        Calculation depends on type (makes results easier to read.
        "q" stands for queue length histogram resulting in a limited number of bins (only few possible values)
        "bp" stands for blocking probability histogram
        "w" stands for mean waiting time histogram
        After generating the report, the plot function is called (see this function in super class).
        """
        if len(self.values) != 0:
            weights = numpy.full(len(self.values), 1.0 / float(len(self.values)))

            if self.type == "q":

                # TODO Task 2.4.1: Your code goes here
                """
                Use numpy.histogram to calculate self.histogram and self.bins.
                Afterwards call the plot function using self.plot() with adequate parameters
                """
                # mainly thought for mean queue length
                self.histogram, self.bins = numpy.histogram(self.values, weights = weights, bins = 7, range = (-.5, 7.5))
                self.plot("side-by-side")
                #pass

            elif self.type == "bp":

                # TODO Task 2.4.1: Your code goes here
                """
                Use numpy.histogram to calculate self.histogram and self.bins.
                Afterwards call the plot function using self.plot() with adequate parameters
                """
                # Plot histogram - mainly thought for mean queue length
                # (easier but worse interpretation than side-by-side)
                self.histogram, self.bins = numpy.histogram(self.values, weights = weights,bins = 50, range = (0, 1))
                self.plot("histogram")
                #pass

            elif self.type == "w":

                # TODO Task 2.4.1: Your code goes here
                """
                Use numpy.histogram to calculate self.histogram and self.bins.
                Afterwards call the plot function using self.plot() with adequate parameters
                """
                # mainly thought for mean waiting time
                self.histogram, self.bins = numpy.histogram(self.values, weights = weights, bins = 40, range = (0, 4000))
                # In order to distribute over the number of samples, we can also use "density=True" option
                # But sum of the probability could not reach to 1.
                self.plot("line")
                #pass

            else:
                raise TypeError("Undefined histogram types: %s" % self.type)

        else:
            raise ValueError("Can't plot histogram with no values.")


class TimeDependentHistogram(Histogram):

    """
    Histogram for plotting values considering their duration.
    """

    def __init__(self, sim, typestr):
        """
        Initialize histogram with the simulation it belongs to and a typestring for better distinction
        :param sim: simulation object, the histogram belongs to
        :param typestr: typestring for better distinction
        """
        super(TimeDependentHistogram, self).__init__(sim, typestr)
        self.first_timestamp = 0
        self.last_timestamp = 0
        self.weights = []

    def count(self, value):
        """
        Add new value to histogram, i.e., the internal array.
        Consider the duration of this value as well.
        """
        # TODO Task 2.4.2: Your code goes here
        self.values.append(value)
        self.last_timestamp = self.sim.sim_state.now
        self.weights.append(self.last_timestamp - self.first_timestamp)
        self.first_timestamp = self.last_timestamp
        #pass

    def reset(self):
        # TODO Task 2.4.2: Your code goes here

        Histogram.reset(self)
        self.first_timestamp = self.sim.sim_state.now
        self.last_timestamp = self.sim.sim_state.now
        self.weights = []

    def report(self):
        """
        Make report, i.e., calculate histogram and bins using numpy.

        Plotting is not optimized, since not explicitly used in this assignment.
        After generating the report, the plot function is called (see this function in super class).
        """
        if len(self.values) != 0:
            weights = numpy.full(len(self.values), 1.0 / float(len(self.values)))
            self.histogram, self.bins = numpy.histogram(self.values, bins=50)
            self.plot(diag_type="side-by-side")
        else:
            raise ValueError("Can't plot histogram with no values.")

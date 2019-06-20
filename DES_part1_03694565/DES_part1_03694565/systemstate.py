class SystemState(object):
    """
    This class represents the state of our system.

    It contains information about whether the server is busy and how many customers
    are waiting in the queue (buffer). The buffer represents the physical buffer or
    memory of our system, where packets are stored before they are served.

    The integer variable buffer_content represents the buffer fill status, the flag
    server_busy indicates whether the server is busy or idle.

    The simulation object is only used to determine the maximum buffer space as
    determined in its object sim_param.
    """

    def __init__(self, sim):
        """
        Create a system state object
        :param sim: simulation object for determination of maximum number of stored
        packets in buffer
        :return: system_state object
        """
        # TODO Task 1.1.1: Your code goes here
        self.sim = sim
        self.buffer_content = 0
        self.server_busy = False  # "Zero indicates that server is free"
        #pass

    def add_packet_to_server(self):
        """
        Try to add a packet to the server unit.
        :return: True if server is not busy and packet has been added successfully.
        """
        # TODO Task 1.1.2: Your code goes here
        if self.server_busy == False:
            self.server_busy = True
            return True
        else:
            return False

        #pass

    def add_packet_to_queue(self):
        """
        Try to add a packet to the buffer.
        :return: True if buffer/queue is not full and packet has been added successfully.
        """
        # TODO Task 1.1.2: Your code goes here
        if self.server_busy == True and self.buffer_content < self.sim.sim_param.S:
            self.buffer_content = self.buffer_content + 1
            return True
        else:
            return False

        #pass

    def complete_service(self):
        """
        Reset server status to idle after a service completion.
        """
        # TODO Task 1.1.3: Your code goes here
        self.server_busy = False
        # TODO Task 2.4.3: Your code goes here somewhere
        #pass

    def start_service(self):
        """
        If the buffer is not empty, take the next packet from there and serve it.
        :return: True if buffer is not empty and a stored packet is being served.
        """
        # TODO Task 1.1.3: Your code goes here
        if self.buffer_content > 0 and self.server_busy == False:
            self.buffer_content = self.buffer_content - 1
            self.server_busy = True
            return True
        else:
            return False
        #pass

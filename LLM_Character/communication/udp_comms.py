import logging

from LLM_Character.util import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class UdpComms:
    def __init__(
        self, udp_ip, port_tx, port_rx, enable_rx=False, suppress_warnings=True
    ):
        """
        udpIP: Must be string e.g. "127.0.0.1"
        portTX: integer number e.g. 8000.
        Port to transmit from i.e From Python to other application
        portRX: integer number e.g. 8001.
        Port to receive on i.e. From other application to Python
        enableRX: When False you may only send from Python and not receive.
        If set to True a thread is created to enable receiving of data
        suppressWarnings: Stop printing warnings if not connected to other application
        """
        import socket

        self.udp_ip = udp_ip
        self.udp_send_port = port_tx
        self.udp_rcvport = port_rx
        self.enable_rx = enable_rx
        self.suppress_warnings = suppress_warnings  # when true warnings are suppressed
        self.is_data_received = False
        self.data_rx = None

        # Connect via UDP
        # internet protocol, udp (DGRAM) socket
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # allows the address/port to be reused immediately instead of it being
        # stuck in the TIME_WAIT state waiting for late packets to arrive.
        self.udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udpSock.bind((udp_ip, port_rx))

        # Create Receiving thread if required
        if enable_rx:
            import threading

            self.rx_thread = threading.Thread(
                target=self.ReadUdpThreadFunc, daemon=True
            )
            self.rxThread.start()

    def __del__(self):
        self.CloseSocket()

    def close_socket(self):
        # Function to close socket
        self.udpSock.close()

    def send_data(self, str_to_send):
        # Use this function to send string to C#
        self.udpSock.sendto(bytes(str_to_send, "utf-8"), (self.udpIP, self.udpSendPort))

    def receive_data(self):
        """
        Should not be called by user
        Function BLOCKS until data is returned from C#.
        It then attempts to convert it to string and returns on successful conversion.
        An warning/error is raised if:
            - Warning: Not connected to C# application yet.
              Warning can be suppressed by setting suppressWarning=True in constructor
            - Error: If data receiving procedure or conversion to string goes wrong
            - Error: If user attempts to use this without enabling RX
        :return: returns None on failure or the received string on success
        """
        if not self.enableRX:  # if RX is not enabled, raise error
            raise ValueError(
                "Attempting to receive data without enabling this setting.\
                             Ensure this is enabled from the constructor"
            )

        data = None
        try:
            data, _ = self.udpSock.recvfrom(5024)
            data = data.decode("utf-8")
        except WindowsError as e:
            if e.winerror == 10054:
                if not self.suppressWarnings:
                    logger.info(
                        "Are You connected to the other application? Connect to it!"
                    )
            else:
                raise ValueError(  # noqa: B904
                    "Unexpected Error.\
                    Are you sure that the received data can be converted to a string"
                )

        return data

    def read_udp_thread_func(self):  # Should be called from thread
        """
        This function should be called from a thread.
        This function keeps looping through the BLOCKING ReceiveData function
        and sets self.dataRX when data is received and sets received flag
        This function runs in the background and updates class variables
        to read data later
        """

        self.is_data_received = False  # Initially nothing received

        while True:
            # Blocks (in thread) until data is returned (OR MAYBE UNTIL SOME
            # TIMEOUT AS WELL)
            data = self.ReceiveData()
            self.data_rx = data  # Populate AFTER new data is received
            self.is_data_received = True
            # When it reaches here, data received is available

    def read_received_data(self):
        """
        This is the function that should be used to read received data.
        It checks if data has been received SINCE LAST CALL,
        if so it returns the received string
        returns None if nothing has been received
        """

        data = None

        if self.isDataReceived:  # if data has been received
            self.is_data_received = False
            data = self.dataRX
            self.data_rx = None  # Empty receive buffer
        return data

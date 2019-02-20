import serial

# https://github.com/nkinder/smart-card-removinator/blob/master/client/removinator/removinator.py
class SAML11:
    """Communicates to the SAML11 on the specified serial port.
    """

    def __init__(
        self,
        port="COM3",
        serial_settings = {
            "baudrate": 9600,
            "bytesize": serial.EIGHTBITS,
            "parity": serial.PARITY_EVEN,
            "stopbits": serial.STOPBITS_TWO,
            "xonxoff": False,
            "dsrdtr": True,
            "rtscts": False,
            "timeout": None,
            "write_timeout": None,
            "inter_byte_timeout": None,
        },
    ):
        """Opens a connection to the SAML11 on the specified serial port.
        """
        
        self.port = port        
        self.serial_settings = serial_settings

        self.last_result = ""
        self.last_response = ""

        # Open a connection to the SAML11.
        try:
            self.connection = serial.Serial(
                port=port,
            )
            self.connection.apply_settings(serial_settings)
        except serial.SerialException as e:
            raise ConnectError(
                "Unable to open connection to SAML11 "
                "controller on port {0}".format(port)
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def get_status(self):
        """
        Get the status of the SAML11
        :raises: :exc:`CommandError`
        """

        self.send_command("STA")
        return self.last_response

    def send_command(self, command, print_response=False):
        """
        Send a command to the SAML11
        Sends the specified command to the SAML11. The command
        result (*OK*, *DBG* or *ERR_\\**) will be available in the *last_result*
        attribute of your *SAML11* object.  Similarly, the full command
        response will be available in the *last_response* attribute.
        Any debug output will be printed.
        If an error result is encountered, a CommandError will be
        raised.
        :param command: the command to send
        :type command: str
        :raises: :exc:`CommandError`
        """

        # Clear out the previous command result and response.
        self.last_result = ""
        self.last_response = ""

        # Send the command in a proper envelope to the SAML11.
        try:
            self.connection.write("#{0}\r".format(command).encode("utf-8"))
        except serial.SerialException as e:
            raise CommandError(
                "Serial error encountered sending command "
                '"{0}" ({1})'.format(command, e)
            )

        while 1:
            resp_line = self.connection.readline().decode("utf-8")
            # print(resp_line)
            if resp_line.startswith("OK"):
                self.last_result = resp_line.rstrip()
                break
            elif resp_line.startswith("ERR_"):
                self.last_result = resp_line.rstrip()
                raise CommandError(
                    '{0} encountered sending command "{1}"'.format(
                        self.last_result, command
                    )
                )
            elif resp_line.startswith("[DBG]"):
                while 1:
                    print(resp_line.rstrip())
                    resp_line = self.connection.readline().decode("utf-8")
                    if resp_line.startswith("OK"):
                        self.last_result = "DBG"
                        break
            else:
                # Concatenate multi-line responses.
                self.last_response += resp_line

        if print_response:
            print("Last result: {}".format(self.last_result))
            print("Last response:\n{}".format(self.last_response).replace("\n", "\n\t"))

    def set_debug(self, debug):
        """
        Enable or disable SAML11 debug output
        When enabled, the SAML11 will return verbose responses
        via serial when commands are executed. The debug output from the
        previously run command will be available along with the standard
        command output in the *last_response* attribute of your
        *SAML11* object.
        :param debug: enable/disable debugging
        :type debug: bool
        :raises: :exc:`CommandError`
        """
        # Send the debug command.
        self.send_command("DBG")

        # Check the response to see if we are in the requested state.
        if debug and (self.last_response.rstrip().endswith("DBG_OFF")):
            self.send_command("DBG")
        elif not debug and (self.last_response.rstrip().endswith("DBG_ON")):
            self.send_command("DBG")

#     def test_aes(self):
#         """
#         Test AES encryption on a known block of data.
#         :raises: :exc:`TestAESError`
#         """
#         # Send the test AES command.
#         self.send_command("TAE")
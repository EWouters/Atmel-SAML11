"""This module wraps the calls to the Power Interface."""

from time import sleep

from pydgilib.dgilib_config import (
    CALIBRATING, DONE, IDLE, OVERFLOWED, RUNNING, XAM)
from pydgilib_extra.dgilib_extra_exceptions import (
    PowerReadError, PowerStatusError, InterfaceNotAvailableError)

from pydgilib_extra.dgilib_interface import DGILibInterface
from pydgilib_extra.dgilib_data import InterfaceData


class DGILibInterfacePower(DGILibInterface):
    """Wraps the calls to the Power interface."""

    name = "power"
    csv_header = ["timestamp", "current"]

    def __init__(self, *args, **kwargs):
        """Instantiate DGILibInterfacePower object."""
        # Set default values for attributes

        # Instantiate base class
        DGILibInterface.__init__(self, *args, **kwargs)
        # Parse arguments
        self.power_buffers = kwargs.get("power_buffers", [])

        if self.verbose:
            print("power_buffers: ", self.power_buffers)

    def get_config(self):
        """Get the power config options.

        :return: Power buffers configuration list of dictionaries like
            `[{"channel": CHANNEL_A, "power_type": POWER_CURRENT}]`
        :rtype: list(dict())
        """
        # Return the configuration
        return self.power_buffers


# Note: this function can be removed if configs are set to self.power_buffers directly
    # def set_config(self, *args, **kwargs):
    #     """Set the power config options.

    #     Register buffers inside the library for the buffers specified in
    #     power_buffers and removes ones that are not present.

    #     :param power_buffers: Power buffers configuration list of dictionaries
    #         like `[{"channel": CHANNEL_A, "power_type": POWER_CURRENT}]`
    #     :type power_buffers: list(dict())
    #     """
    #     # Parse arguments

    #     # Disable the configurations that are not in the new config and remove
    #     # them from self.power_buffers
    #     for power_buffer in self.power_buffers:
    #         if power_buffer not in power_buffers:
    #             self.dgilib_extra.auxiliary_power_unregister_buffer_pointers(
    #                 channel=power_buffer["channel"],
    #                 power_type=power_buffer["power_type"],
    #             )
    #             self.power_buffers.remove(power_buffer)

    #     # Enable the configurations that are in the new config and not in
    #     # self.power_buffers
    #     for power_buffer in power_buffers:
    #         if power_buffer not in self.power_buffers:
    #             self.dgilib_extra.auxiliary_power_register_buffer_pointers(
    #                 channel=power_buffer["channel"],
    #                 power_type=power_buffer["power_type"])
    #             self.power_buffers.append(power_buffer)
    def set_config(self, power_buffers):
        """Set the power config options."""
        self.power_buffers = power_buffers

    def enable(self):
        """Enable the interface."""
        if self.interface_id not in self.dgilib_extra.available_interfaces:
            raise InterfaceNotAvailableError(
                f"Interface {self.interface_id} not available. Available interfaces: {self.dgilib_extra.available_interfaces}")
        self.dgilib_extra.power_hndl = self.dgilib_extra.auxiliary_power_initialize()
        # Check if calibration is valid and trigger calibration if it is not
        self.calibrate()
        if self.interface_id not in self.dgilib_extra.enabled_interfaces:
            self.dgilib_extra.enabled_interfaces.append(self.interface_id)

        for power_buffer in self.power_buffers:
            self.dgilib_extra.auxiliary_power_register_buffer_pointers(
                channel=power_buffer["channel"],
                power_type=power_buffer["power_type"])
            self.power_buffers.append(power_buffer)

    def disable(self):
        """Disable the interface."""
        if self.interface_id in self.dgilib_extra.enabled_interfaces:
            for power_buffer in self.power_buffers:
                self.dgilib_extra.auxiliary_power_unregister_buffer_pointers(
                    channel=power_buffer["channel"],
                    power_type=power_buffer["power_type"])
                self.power_buffers.remove(power_buffer)
            self.dgilib_extra.enabled_interfaces.remove(self.interface_id)
        self.dgilib_extra.auxiliary_power_uninitialize()

    def calibrate(self, force=False):
        """
        Calibrate the Auxiliary Power interface of the device.

        Check if calibration is valid and trigger calibration if it is not.

        Keyword Arguments:
            force {bool} - - Force calibration, even if it is valid(default: {False})

        Raises:
            PowerReadError - - [description]
            PowerStatusError - - [description]
            PowerStatusError - - [description]

        """
        self.circuit_type = self.dgilib_extra.auxiliary_power_get_circuit_type()
        if force or not self.dgilib_extra.auxiliary_power_calibration_is_valid():
            self.auxiliary_power_calibration()

    def auxiliary_power_calibration(self, circuit_type=XAM):
        """Calibrate the Auxiliary Power interface of the device.

        : param circuit_type: Type of calibration to trigger(defaults to XAM)
        : type circuit_type: int
        """
        self.dgilib_extra.auxiliary_power_trigger_calibration(circuit_type)
        while self.dgilib_extra.auxiliary_power_get_status() == CALIBRATING:
            sleep(0.1)

    def read(self, buffer_num=0):
        """Read data from the interface.

        : return: Interface data
        : rtype: InterfaceData()
        """
        # Return the data
        print(self.power_buffers)
        return self.read_buffer(self.power_buffers[buffer_num])

    def read_buffer(self, power_buffer):
        """Read power data of the specified buffer.

        TODO: Copies parsed power data into the specified buffer. Remember to
        lock the buffers first. If the count parameter is the same as
        max_count there is probably more data to be read. Do another read to
        get the remaining data.

        : return: TODOTODO Tuple of list of power samples in Ampere and list of
            timestamps in seconds
        : rtype: (list(float), list(float))
        """
        # Check if power_buffer is in self.power_buffers
        if power_buffer not in self.power_buffers:
            raise PowerReadError(
                f"Power Buffer {power_buffer} does not exist in "
                f"self.power_buffers: {self.power_buffers}.")

        # Check if auxiliary_power_get_status() is in
        #   - IDLE = 0x00,
        #   - RUNNING = 0x01,
        #   - DONE = 0x02 or
        #   - OVERFLOWED = 0x11
        # and raise PowerStatusError if it is.
        power_status = self.dgilib_extra.auxiliary_power_get_status()
        if self.verbose:
            print(f"power_status: {power_status}")
        # if power_status <= DONE or power_status == OVERFLOWED:
        if power_status not in (IDLE, RUNNING, DONE, OVERFLOWED):
            raise PowerStatusError(f"Power Status {power_status}.")
        if power_status == OVERFLOWED:
            print(
                f"BUFFER OVERFLOW, call this function more frequently or "
                f"increase the buffer size.")

        # Create variables to the store data in
        interface_data = InterfaceData()

        # TODO: Check implementation in case of buffer overflow.
        # Should auxiliary_power_lock_data_for_reading() be inside the loop
        # or before?

        # Get the data from the buffer in the library
        while True:
            self.dgilib_extra.auxiliary_power_lock_data_for_reading()
            interface_data += self.dgilib_extra.auxiliary_power_copy_data(
                power_buffer["channel"], power_buffer["power_type"])
            # BUG: This probably clears all channels! (channels might not be
            # working on XAM anyway)
            self.dgilib_extra.auxiliary_power_free_data()
            # Repeat the loop until there is no buffer overflow (which should
            # always be avoided.)
            if self.dgilib_extra.auxiliary_power_get_status() != OVERFLOWED:
                break

        if self.verbose >= 2:
            print(f"Collected {len(interface_data)} power samples")
        if self.verbose >= 4:
            print(interface_data)

        return interface_data

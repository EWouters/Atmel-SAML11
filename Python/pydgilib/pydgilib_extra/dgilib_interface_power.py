"""This module provides Python bindings for DGILibExtra Power interface."""

__author__ = "Erik Wouters <ehwo(at)kth.se>"
__credits__ = "Atmel Corporation. / Rev.: Atmel-42771A-DGILib_User Guide-09/2016"
__license__ = "MIT"
__version__ = "0.1"
__revision__ = " $Id: dgilib_interface_power.py 1586 2019-02-13 15:56:25Z EWouters $ "
__docformat__ = "reStructuredText"

from time import sleep

from pydgilib_extra.dgilib_extra_config import *
from pydgilib_extra.dgilib_extra_exceptions import *


class DGILibInterfacePower(object):
    """Python bindings for DGILib Power interface.

    """

    def __init__(self, *args, **kwargs):
        """
        :Example:

        >>> pb = [{"channel": 0, "power_type": 0}]
        >>> with DGILibExtra(power_buffers=pb) as dgilib:
        ...     dgilib.get_major_version()
        5
        """

        # Argument parsing
        self.power_buffers = kwargs.get("power_buffers", [])
        if self.verbose:
            print("power_buffers: ", self.power_buffers)

    def __enter__(self):
        """
        """

        # Check if calibration is valid and trigger calibration if it is not
        self.circuit_type = self.auxiliary_power_get_circuit_type()
        if not self.auxiliary_power_calibration_is_valid():
            self.auxiliary_power_trigger_calibration(self.circuit_type)

        # Register buffers inside the library for the buffers specified in self.power_buffers
        for power_buffer in self.power_buffers:
            self.auxiliary_power_register_buffer_pointers(
                channel=power_buffer["channel"], power_type=power_buffer["power_type"]
            )

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        """
        self.power_set_config([])

    def auxiliary_power_calibration(self, circuit_type=XAM):
        """Calibrate the Auxilary Power interface of the device.
        
        :param circuit_type: Type of calibration to trigger (defaults to XAM)
        :type circuit_type: int
        """

        self.auxiliary_power_trigger_calibration(circuit_type)
        while self.auxiliary_power_get_status() == CALIBRATING:
            sleep(0.1)

    def power_get_config(self):
        """Get the power config options.
        
        :return: Power buffers configuration list of dictionaries like `[{"channel": CHANNEL_A, "power_type": POWER_CURRENT}]`
        :rtype: list(dict())
        """

        # Return the configuration
        return self.power_buffers

    def power_set_config(self, power_buffers):
        """Set the power config options.
        
        Register buffers inside the library for the buffers specified in power_buffers and removes ones that are not present.
        
        :param power_buffers: Power buffers configuration list of dictionaries like `[{"channel": CHANNEL_A, "power_type": POWER_CURRENT}]`
        :type power_buffers: list(dict())
        """

        # Disable the configurations that are not in the new config and remove them from self.power_buffers
        for power_buffer in self.power_buffers:
            if power_buffer not in power_buffers:
                self.auxiliary_power_unregister_buffer_pointers(
                    channel=power_buffer["channel"],
                    power_type=power_buffer["power_type"],
                )
                self.power_buffers.remove(power_buffer)

        # Enable the configurations that are in the new config and not in self.power_buffers
        for power_buffer in power_buffers:
            if power_buffer not in self.power_buffers:
                self.auxiliary_power_register_buffer_pointers(
                    channel=power_buffer["channel"],
                    power_type=power_buffer["power_type"],
                )
                self.power_buffers.append(power_buffer)

    def power_read_buffer(self, power_buffer, *args, **kwargs):
        """Read power data of the specified buffer.
        
        TODO: Copies parsed power data into the specified buffer. Remember to lock the buffers first. If the count parameter is the same as max_count there is probably more data to be read. Do another read to get the remaining data.
        
        :return: TODOTODO Tuple of list of power samples in Ampere and list of timestamps in seconds
        :rtype: (list(float), list(float))
        """

        # Check if power_buffer is in self.power_buffers
        if power_buffer not in self.power_buffers:
            raise PowerReadError(
                f"Power Buffer {power_buffer} does not exist in self.power_buffers: {self.power_buffers}."
            )

        # Check if auxiliary_power_get_status() is in IDLE = 0x00, RUNNING = 0x01, DONE = 0x02 or OVERFLOWED = 0x11
        # and raise DevicePowerStatusError if it is.
        power_status = self.auxiliary_power_get_status()
        if self.verbose:
            print(f"power_status: {power_status}")
        # if power_status <= DONE or power_status == OVERFLOWED:
        if power_status not in (IDLE, RUNNING, DONE, OVERFLOWED):
            raise DevicePowerStatusError(f"Power Status {power_status}.")
        if power_status == OVERFLOWED:
            print(
                f"BUFFER OVERFLOW, call this function more frequently or increase the buffer size."
            )

        # Create variables to the store data in
        power_samples = []
        timestamps = []

        # TODO: Check implementation in case of buffer overflow.
        #  Should auxiliary_power_lock_data_for_reading() be inside the loop or before?

        # Get the data from the buffer in the library
        while True:
            self.auxiliary_power_lock_data_for_reading()
            _power_samples, _timestamps = self.auxiliary_power_copy_data(
                power_buffer["channel"],
                power_buffer["power_type"],
                *args,
                **kwargs,
            )
            self.auxiliary_power_free_data()  # BUG: This probably clears all channels! (channels might not be working on XAM anyway)
            power_samples.extend(_power_samples)
            timestamps.extend(_timestamps)
            # Repeat the loop untill there is no buffer overflow (which should always be avoided.)
            if self.auxiliary_power_get_status() != OVERFLOWED:
                break

        if self.verbose >= 2:
            print(f"Collected {len(power_samples)} power samples")
        if self.verbose >= 4:
            print(timestamps, power_samples)
            
        return timestamps, power_samples

#     def power_read(self, *args, **kwargs):
#         """Read power data from all enabled buffers.
        
#         The returned list has the same indexes as the list obtained from `power_get_config()`
#         """
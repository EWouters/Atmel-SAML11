"""This module provides Python bindings for the Discovery API of DGILib."""

__author__ = "Erik Wouters <ehwo(at)kth.se>"
__credits__ = "Atmel Corporation. / Rev.: Atmel-42771A-DGILib_User Guide-09/2016"
__license__ = "MIT"
__version__ = "0.1"
__revision__ = " $Id: dgilib_discovery.py 1586 2019-02-13 15:56:25Z EWouters $ "
__docformat__ = "reStructuredText"

GET_STRING_SIZE = 100
NUM_INTERFACES = 10
NUM_CONFIG_IDS = 255
NUM_CALIBRATION = 255
BUFFER_SIZE = 10000000
MAX_PRINT = 100

# Interface types
INTERFACE_TIMESTAMP  = 0x00 #   0 Service interface which appends timestamps to all received events on associated interfaces.
INTERFACE_SPI        = 0x20 #  32 Communicates directly over SPI in Slave mode.
INTERFACE_USART      = 0x21 #  33 Communicates directly over USART in Slave mode.
INTERFACE_I2C        = 0x22 #  34 Communicates directly over I2C in Slave mode.
INTERFACE_GPIO       = 0x30 #  48 Monitors and controls the state of GPIO pins.
INTERFACE_POWER_DATA = 0x40 #  64 Receives data from the attached power measurement co-processors.
INTERFACE_POWER_SYNC = 0x41 #  65 Receives sync events from the attached power measurement co-processors.
INTERFACE_RESERVED   = 0xFF # 255 Special identifier used to indicate no interface.

# Circuit types
OLD_XAM = 0x00 #   0
XAM     = 0x10 #  16
PAM     = 0x11 #  17
UNKNOWN = 0xFF # 255

# Return codes
IDLE               = 0x00 #   0
RUNNING            = 0x01 #   1
DONE               = 0x02 #   2
CALIBRATING        = 0x03 #   3
INIT_FAILED        = 0x10 #  16
OVERFLOWED         = 0x11 #  17
USB_DISCONNECTED   = 0x12 #  18
CALIBRATION_FAILED = 0x20 #  32

from ctypes import *
from time import sleep

class DGILibDiscovery(object):
    """Python bindings for DGILib Discovery.
    
    DGILib is a Dynamic-Link Library (DLL) to help software applications communicate with Data Gateway
    Interface (DGI) devices. See the Data Gateway Interface user guide for further details. DGILib handles
    the low-level USB communication and adds a level of buffering for minimizing the chance of overflows.
    """

    def __enter__(self):
        """
        :raises: :exc:`DeviceIndexError`
        """

        self.discover()
        device_count = self.get_device_count()

        if self.device_sn is None:
            if self.device_index is None:
                self.device_index = 0
            elif self.device_index > device_count - 1:
                raise DeviceIndexError(
                    f"Discovered {device_count} devices so could not select device with index {self.device_index}."
                )
            self.device_sn = self.get_device_serial(self.device_index)

        # UNTESTED:
        # if msd_mode:
        #     res = self.set_mode(sn, 1)
        #     print(f"\t{res} set_mode 1")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.verbose:
            print("bye from Discovery")

        """
TODO?
2.1.1. initialize_status_change_notification
Initializes the system necessary for using the status change notification callback mechanisms. A handle
will be created to keep track of the registered callbacks. This function must always be called before
registering and unregistering notification callbacks.
Function definition
void initialize_status_change_notification(uint32_t* handlep)
Parameters
handlep Pointer to a variable that will hold the handle
2.1.2. uninitialize_status_change_notification
Uninitializes the status change notification callback mechanisms. This function must be called when
shutting down to clean up memory allocations.
Function definition
void uninitialize_status_change_notification(uint32_t handle)
Parameters
handle Handle to uninitialize
2.1.3. register_for_device_status_change_notifications
Registers provided function pointer with the device status change mechanism. Whenever there is a
change (device connected or disconnected) the callback will be executed. Note that it is not allowed to
connect to a device in the context of the callback function. The callback function has the following
definition: typedef void (*DeviceStatusChangedCallBack)(char* device_name, char* device_serial, BOOL
connected)
Function definition
void register_for_device_status_change_notifications(uint32_t handle, DeviceStatusChangedCallBack
deviceStatusChangedCallBack)
Parameters
handle Handle to change notification mechanisms
deviceStatusChangedCallBack Function pointer that will be called when the devices change
2.1.4. unregister_for_device_status_change_notifications
Unregisters previously registered function pointer from the device status change mechanism.
Function definition
void unregister_for_device_status_change_notifications(uint32_t handle, DeviceStatusChangedCallBack
deviceStatusChangedCallBack)
Parameters
handle Handle to change notification mechanisms
deviceStatusChangedCallBack Function pointer that will be removed
        """

    def discover(self):
        """`discover`

        Triggers a scan to find available devices in the system. The result will be immediately available through
        the `get_device_count`, `get_device_name` and `get_device_serial` functions.

        `void discover(void)`
        """

        self.dgilib.discover()

    def get_device_count(self):
        """`get_device_count`

        Returns the number of devices detected.

        `int get_device_count(void)`
        
        :return: The number of devices detected
        :rtype: int
        """

        device_count = self.dgilib.get_device_count()
        if self.verbose:
            print(f"device_count: {device_count}")
        return device_count

    def get_device_name(self, index):
        """`get_device_name`

        Gets the name of a detected device.

        `int get_device_name(int index, char* name)`
        
        +------------+------------+
        | Parameter  | Description |
        +============+============+
        | *index* | Index of device ranges from 0 to `get_device_count` - 1 |
        | *name* | Pointer to buffer where name of device can be stored. 100 or more bytes must be allocated |
        +------------+------------+
        
        :param index: Index of device ranges from 0 to `get_device_count` - 1
        :type index: int
        :return: The name of a detected device
        :rtype: str
        :raises: :exc:`DeviceReturnError`
        """

        name = create_string_buffer(GET_STRING_SIZE)
        res = self.dgilib.get_device_name(index, byref(name))
        if self.verbose:
            print(f"\t{res} get_device_name: {name.value}")
        if res:
            raise DeviceReturnError(f"get_device_name returned: {res}")
        return name.value

    def get_device_serial(self, index):
        """`get_device_serial`

        Gets the serial number of a detected device.

        `int get_device_serial(int index, char* sn)`
        
        +------------+------------+
        | Parameter  | Description |
        +============+============+
        | *index* | Index of device ranges from 0 to `get_device_count` - 1 |
        | *sn* | Pointer to buffer where the serial number of the device can be stored. 100 or more bytes must be allocated. This is used when connecting to a device |
        +------------+------------+
        
        :param index: Index of device ranges from 0 to `get_device_count` - 1
        :type index: int
        :return: The serial number of a detected device
        :rtype: str
        :raises: :exc:`DeviceReturnError`
        """

        device_sn = create_string_buffer(GET_STRING_SIZE)
        res = self.dgilib.get_device_serial(index, byref(device_sn))
        if self.verbose:
            print(f"\t{res} get_device_serial: {device_sn.value}")
        if res:
            raise DeviceReturnError(f"get_device_serial returned: {res}")
        return device_sn.value

    def is_msd_mode(self, device_sn):
        """`is_msd_mode`
        EDBG devices can be set to a mass storage mode where the DGI is unavailable. In such cases the 
        device is still detected by DGILib, but it won't be possible to directly connect to it. This command is used 
        to check if the device is in such a mode.

        A non-zero return value indicates that the mode must be changed by `set_mode` before proceeding.

        `int is_msd_mode(char* sn)`
        
        +------------+------------+
        | Parameter  | Description |
        +============+============+
        | *sn* | Serial number of the device to check |
        +------------+------------+
        
        :param device_sn: Serial number of the device to check (defaults to self.device_sn)
        :type device_sn: str or None
        :return: A non-zero return value indicates that the mode must be changed by `set_mode` before proceeding.
        :rtype: int
        """

        msd_mode = self.dgilib.is_msd_mode(device_sn)
        if self.verbose:
            print(f"msd_mode: {msd_mode}")
        return msd_mode

    def set_mode(self, device_sn, nmbed=1):
        """`set_mode`
        This function is used to temporarily set the EDBG to a specified mode.

        `int set_mode(char* sn, int nmbed)`
        
        +------------+------------+
        | Parameter  | Description |
        +============+============+
        | *sn* | Serial number of the device to set |
        | *nmbed* | 0 - Set to mbed mode. 1 - Set to DGI mode |
        +------------+------------+
        
        :param device_sn: Serial number of the device to set
        :type device_sn: str
        :param nmbed: 0 - Set to mbed mode. 1 - Set to DGI mode (defaults to DGI mode)
        :type nmbed: int
        :raises: :exc:`DeviceReturnError`
        """

        res = self.dgilib.set_mode(device_sn, nmbed)
        if self.verbose:
            print(f"\t{res} set_mode {nmbed}")
        if res:
            raise DeviceReturnError(f"set_mode returned: {res}")
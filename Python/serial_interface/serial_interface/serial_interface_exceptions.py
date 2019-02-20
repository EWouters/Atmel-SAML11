# Custom Exceptions
class Error(Exception):
    """Base class for exceptions in this module.
    :param msg: Error message associated with the exception
    :type msg: str
    :ivar msg: Error message associated with the exception
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class CommandError(Error):
    """Exception raised sending a command to the SAML11."""

    pass


class ConnectError(Error):
    """Exception raised connecting to the SAML11."""

    pass


# class TestAESError(Error):
#     """Exception raised when running the static AES test on a known block of data."""

#     pass
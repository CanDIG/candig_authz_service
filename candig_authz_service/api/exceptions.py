"""
Custom exceptions for API operations
"""


class IdentifierFormatError(ValueError):
    """
    Custom exception for validation fail on UUID string parameters
    """
    def __init__(self, identifier):
        message = ("{} parameters must be correctly "
                   "formatted UUID strings".format(identifier))
        super().__init__(message)


class AuthorizationError(Exception):
    """
    Custom exception for failed authorization
    """
    def __init__(self):
        message = "Key not authorized to perform this action"
        super().__init__(message)


class ConfigurationException(Exception):
    """
    This exception indicates that there is a configuration issue.
    """
    def __init__(self, message):
        super().__init__(message)


class InvalidAccessListException(Exception):
    """
    This exception indicates that the provided access_list.tsv is not correctly formatted.
    """
    def __init__(self, level):
        message = "This is an invalid level: {}".format(level)
        super().__init__(message)

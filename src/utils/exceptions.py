"""
Base exceptions namespace for the app
"""


class SynbrowserException(Exception):
    """
    Base exception for the SynBrowser app
    """


class InvalidRequestArgumentValueException(SynbrowserException):
    """
    Handles cases in which the client sends the correct type of argument(s), but no data could be provided for it.

    For example, the client may request all genes on chromosome 104 in H. sapiens (Human). Since H. sapiens only has
    23 chromosomes, rather than returning an empty list, the application will raise an exception that 104 is not
    a valid chromosome number for the species (H. sapiens) in the request.
    """
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

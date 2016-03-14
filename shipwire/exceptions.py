class ShipwireError(Exception):
    """
    Base Exception thrown by the Shipwire object when there is a
    general error interacting with the API.
    """
    pass


class ResponseError(ShipwireError):
    """
    Exception raised when a response indicating failure is encountered
    """

    def __init__(self, response):
        try:
            message = response.json()['message']
        except:
            message = "Unknown message"

        super(ResponseError, self).__init__(
            'Unexpected Status Code (%d): %s' %
            (response.status_code, message))
        self.response = response


class TimeoutError(ShipwireError):
    """
    Exception raised when a timeout occurs.
    """
    pass

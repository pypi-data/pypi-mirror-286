class InvalidArgumentException(Exception):
    code = "400"

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(InvalidArgumentException, self).__init__(message)


class DataNotFoundException(Exception):
    code = "404"

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(DataNotFoundException, self).__init__(message)


class FeatureNotSupported(Exception):
    code = "407"

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(FeatureNotSupported, self).__init__(message)


class AccessDeniedException(Exception):
    code = "403"

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(AccessDeniedException, self).__init__(message)


class RetryableException(Exception):
    code = "409"

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(RetryableException, self).__init__(message)


def retry_on_access_denied(exc):
    return isinstance(exc, AccessDeniedException)


def retry_exception(exc):
    return isinstance(exc, RetryableException)


class StaleDataFound(Exception):
    code = "101"

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(StaleDataFound, self).__init__(message)


class ServiceException(Exception):
    code = "500"

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(ServiceException, self).__init__(message)


class StockNotListedOnExchange(Exception):
    stocks = []

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(StockNotListedOnExchange, self).__init__(message)


class QuantplayOrderPlacementException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(QuantplayOrderPlacementException, self).__init__(message)


class StrategyInvocationException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(StrategyInvocationException, self).__init__(message)


class BrokerNotFoundException(Exception):
    code = "404"

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(BrokerNotFoundException, self).__init__(message)


class TokenException(Exception):
    code = "404"

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(TokenException, self).__init__(message)


class WrongLibrarySetup(Exception):
    code = "501"

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(WrongLibrarySetup, self).__init__(message)


class BrokerException(Exception):
    code = "510"

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(BrokerException, self).__init__(message)

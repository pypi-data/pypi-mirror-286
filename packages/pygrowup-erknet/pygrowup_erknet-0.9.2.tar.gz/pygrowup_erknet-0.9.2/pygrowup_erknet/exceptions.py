class PyGrowUpError(RuntimeError):
    pass

class DataNotFoundError(PyGrowUpError):
    pass

class InvalidTableNameError(PyGrowUpError):
    pass

class InvalidIndexError(PyGrowUpError):
    pass

class InvalidAgeError(InvalidIndexError):
    pass

class InvalidLengthError(InvalidIndexError):
    pass

class InvalidSexError(PyGrowUpError):
    pass

class InvalidMeasurement(PyGrowUpError):
    pass

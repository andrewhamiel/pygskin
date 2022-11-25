import abc

class Model(metaclass=abc.ABCMeta):
    # def __init__(self, file_name):
        
    @abc.abstractmethod
    def get_data_set(df, aggregate, transformer):
        """Returns requested data set."""
    
from abc import ABC, abstractmethod


class Source(ABC):

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass


class UserSource(Source):
    pass


class JsonSource(Source):
    
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def is_empty(self):
        return len(self.data) == 0
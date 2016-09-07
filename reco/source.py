from abc import ABC, abstractmethod


class Source(ABC):

    @abstractmethod
    def get_data(self):
        pass


class UserSource(Source):
    pass


class JsonSource(Source):
    pass
from abc import ABC, abstractmethod


class Source(ABC):

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass


class UserSource(Source):
    
    def __init__(self, user):
        self.user = user

    def get_data(self):
        return list(self.user.pref.data.extra(select={"movie__id": "id"}).
            values("id", "rating").all())

    def is_empty(self):
        return self.user.pref.data.count() == 0


class JsonSource(Source):
    
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def is_empty(self):
        return len(self.data) == 0
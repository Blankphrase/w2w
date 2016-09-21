from abc import ABC, abstractmethod

from django.db.models import F


class Source(ABC):

    def __init__(self, user = None):
        self.user = user

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    def get_user(self):
        return self.user


class UserSource(Source):
    
    def __init__(self, user):
        super(UserSource, self).__init__(user)
        self.user = user

    def get_data(self):
        return list(self.user.pref.data.values("movie__id", "rating").
            annotate(id=F("movie__id")).values("id", "rating").all())

    def is_empty(self):
        return self.user.pref.data.count() == 0


class JsonSource(Source):
    
    def __init__(self, data, user = None):
        super(JsonSource, self).__init__(user)
        self.data = data
        
    def get_data(self):
        return self.data

    def is_empty(self):
        return len(self.data) == 0
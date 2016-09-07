from .source import UserSource, JsonSource
from .exceptions import RecoSourceError
from .models import Reco


class Item2Item():
    
    def make_reco(self, base):
        pass


class RecoManager:

    def __init__(self, source, engine = None):
        self.source = source

        if engine is None:
            self.engine = globals()["Item2Item"]()
        else:
            self.engine = engine

    def get_reco(self, user = None):
        if self.source.is_empty():
            raise RecoSourceError

        reco = Reco.create_new(
            base = self.source.get_data(), 
            reco = self.make_reco(), 
            user = user
        )
        return reco

    def make_reco(self):
        return self.engine.make_reco(self.source.get_data())

    @property
    def base(self):
        return self.source.get_data()



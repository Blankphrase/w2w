from .source import UserSource, JsonSource
from .exceptions import RecoSourceError
from .models import Reco


class Item2Item():
    
    def make_reco(self, base):
        pass

# base - list of movies with user's ratings
# 1. Find all users who watched the same movies as user
# 2. Find new movies who were not watch previously by user
# 3. Calculte score somehow
# 4. Return the list of movies order by score (limit to 100 or not) and
#    do not show movies already watched by user.
# 5. Display movies in home_page
# 6. Introduce to Movie the informationtion how the recrord was created.



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



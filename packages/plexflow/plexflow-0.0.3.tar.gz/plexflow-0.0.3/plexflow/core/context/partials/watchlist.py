from plexflow.core.context.partial_context import PartialContext
from plexflow.core.plex.watchlist.datatypes import MediaContainer

class Watchlist(PartialContext):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    @property
    def value(self) -> MediaContainer:
        return self.get("watchlist/value")
    
    @value.setter
    def value(self, value: MediaContainer) -> None:
        self.set("watchlist/value", value)
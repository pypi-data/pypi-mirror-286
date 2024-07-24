from plexflow.core.context.partial_context import PartialContext
from plexflow.core.plex.watchlist.datatypes import MediaContainer, PlexMetadata
from ulid import ULID
from typing import Generator, Any
    
class Watchlist(PartialContext):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    def update(self, container: MediaContainer) -> None:
        tag = ULID()
        self.set(f"watchlist/items/{tag}", container)

    def __iter__(self):
        return self.generator()
    
    def generator(self) -> Generator[Any, Any, Any]:
        items = self.get_by_pattern("watchlist/items/*")
        for part in items:
            part: MediaContainer = part
            for item in part.Metadata:
                yield item

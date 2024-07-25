from plexflow.core.context.partial_context import PartialContext
from datetime import datetime as dt
from plexflow.core.metadata.auto.auto_providers.auto.movie import AutoMovie
from plexflow.core.metadata.auto.auto_providers.tmdb.movie import AutoTmdbMovie
from plexflow.core.metadata.auto.auto_providers.tvdb.movie import AutoTvdbMovie
from plexflow.core.metadata.auto.auto_providers.moviemeter.movie import AutoMovieMeterMovie
from plexflow.core.metadata.auto.auto_providers.imdb.movie import AutoImdbMovie
from plexflow.core.metadata.auto.auto_providers.tmdb.show import AutoTmdbShow
from plexflow.core.metadata.auto.auto_providers.tvdb.show import AutoTvdbShow
from plexflow.core.metadata.auto.auto_providers.imdb.show import AutoImdbShow
from plexflow.core.metadata.auto.auto_providers.plex.movie import AutoPlexMovie

class Movie(PartialContext):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def sources(self) -> list:
        keys = self.get_keys("movie/*")
        # extract the source from the key
        return [key.split("/")[1] for key in keys]

    def from_source(self, source: str) -> AutoMovie:
        return self.get(f"movie/{source}")

    @property
    def title(self) -> str:
        return self.plex.title
    
    @property
    def year(self) -> int:
        return self.plex.release_date.year
    
    @property
    def rank(self) -> int:
        return self.plex.rank

    @property
    def plex(self) -> AutoPlexMovie:
        return self.from_source("plex")
    
    def update(self, movie: AutoMovie):
        self.set(f"movie/{movie.source}", movie)

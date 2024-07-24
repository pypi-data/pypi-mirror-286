from typing import List
from contextlib import contextmanager
from plexflow.core.subtitles.providers.oss.unlimited_oss import OpenSubtitlesManager, Subtitle
from plexflow.core.subtitles.providers.oss.oss_subtitle import OSSSubtitle
from typing import Any, List
from contextlib import contextmanager, ExitStack
from plexflow.utils.hooks.redis import UniversalRedisHook

@contextmanager
def open_subtitles_manager(credentials_path: str, redis_hook: UniversalRedisHook = None, **kwargs: Any):
    """
    Context manager for managing the OpenSubtitlesManager instance.

    Args:
        credentials_path: The path to the YAML file containing OpenSubtitles credentials.
        redis_host: The host address of the Redis server.
        redis_port: The port number of the Redis server.

    Yields:
        OpenSubtitlesManager: The OpenSubtitlesManager instance.
    """
    with ExitStack() as stack:
        manager = stack.enter_context(OpenSubtitlesManager.from_yaml(
            yaml_file=credentials_path,
            redis_hook=redis_hook,
            **kwargs
        ))
        yield manager

def get_subtitles(imdb_id: str, languages: List[str] = (), redis_hook: UniversalRedisHook = None, ignore_blacklist: bool = False, **kwargs) -> List[OSSSubtitle]:
    """
    Retrieves subtitles using OpenSubtitlesManager.

    Args:
        imdb_id: The IMDb ID of the movie or TV show.
        languages: A list of language codes for the desired subtitles.

    Returns:
        A list of subtitle data retrieved from OpenSubtitlesManager.
    """
    with open_subtitles_manager(
        credentials_path=kwargs.pop("credentials_path"),
        redis_hook=redis_hook,
        ignore_blacklist=ignore_blacklist,
    ) as manager:
        subtitles = manager.search(
            imdb_id=imdb_id,
            languages=','.join(languages),
            **kwargs
        )

    return list(map(OSSSubtitle, subtitles.data))

from plexflow.core.plex.hooks.plex_authorized import PlexAuthorizedHttpHook
from plexflow.core.plex.watchlist.datatypes import from_json, MediaContainer
from plexflow.core.plex.utils.paginated import paginated

# @paginated
def get_watchlist(**kwargs) -> MediaContainer:
    """
    Retrieves the watchlist from the Plex server.

    Args:
        **kwargs: Additional keyword arguments to be passed to the PlexAuthorizedHttpHook.

    Returns:
        MediaContainer: The watchlist as a MediaContainer object.

    Raises:
        None

    """
    hook = PlexAuthorizedHttpHook(http_conn_id="plex_hook", config_folder="config")
    response = hook.run(endpoint="/library/sections/watchlist/all", **kwargs)
    return from_json(response.content.decode("utf-8"))
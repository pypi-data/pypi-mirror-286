from plexflow.core.storage.object.plexflow_storage import PlexflowObjectStore
from typing import Any

class PartialContext:
    def __init__(self, context_id: str, default_ttl: int, **kwargs) -> None:
        self.context_id = context_id
        self.default_ttl = default_ttl
        self.store = PlexflowObjectStore(context_id, **kwargs)

    def set(self, key: str, value: Any, ttl: int = None) -> None:
        self.store.store_temporarily(key=self.store.make_run_key(key), obj=value, ttl=ttl or self.default_ttl)

    def set_global(self, key: str, value: Any, ttl: int = None) -> None:
        self.store.store_temporarily(key=self.store.make_key(key), obj=value, ttl=ttl or self.default_ttl)
    
    def get(self, key: str) -> Any:
        return self.store.retrieve(key=self.store.make_run_key(key))

    def get_global(self, key: str) -> Any:
        return self.store.retrieve(key=self.store.make_key(key))

    def get_keys(self, pattern: str):
        return self.store.retrieve_keys(self.store.make_run_key(pattern))
    
    def get_by_pattern(self, pattern: str):
        return self.store.retrieve_values(self.store.make_run_key(pattern))

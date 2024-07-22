from plexflow.core.storage.object.plexflow_storage import PlexflowObjectStore
from typing import Any

class PartialContext:
    def __init__(self, context_id: str, default_ttl: int) -> None:
        self.context_id = context_id
        self.default_ttl = default_ttl
        self.store = PlexflowObjectStore(context_id)
        
    def set(self, key: str, value: Any, ttl: int = None) -> None:
        self.store.store_temporarily(key=self.store.make_run_key(key), obj=value, ttl=ttl or self.default_ttl)
    
    def get(self, key: str) -> Any:
        return self.store.retrieve(key=self.store.make_run_key(key))

from plexflow.utils.api.rest.restful import Restful
from plexflow.core.torrents.providers.tpb.utils import TPBSearchResult

class TPB(Restful):
    def __init__(self, http_conn_id: str = 'tpb_hook', config_folder: str = 'config'):
        super().__init__(http_conn_id=http_conn_id, config_folder=config_folder)
    
    def search(self, query: str):
        response = self.get('/q.php', query_params={
            'q': query,
        })
        
        response.raise_for_status()
        
        data = response.json()
        
        return list(map(lambda x: TPBSearchResult(**x), data))

from typing import Optional, Dict, Any, List
import requests
from plexflow.utils.hooks.http import UniversalHttpHook
from plexflow.utils.hooks.postgresql import UniversalPostgresqlHook

class Restful:
    """
    A class that uses UniversalHttpHook and UniversalPostgresqlHook to create RESTful API interfaces and interact with a PostgreSQL database.
    
    Args:
        http_conn_id (str, optional): The connection ID, used as Airflow connection ID or as the name for the YAML file. Defaults to None.
        postgres_conn_id (str, optional): The connection ID, used as Airflow connection ID or as the name for the YAML file. Defaults to None.
        config_folder (str, optional): The folder where the YAML configuration file is located. Defaults to None.
    """
    
    def __init__(self, http_conn_id: Optional[str] = None, postgres_conn_id: Optional[str] = None, config_folder: Optional[str] = None):
        self.http_conn_id = http_conn_id
        self.postgres_conn_id = postgres_conn_id
        self.config_folder = config_folder
        if postgres_conn_id is not None:
            self.sql_hook = UniversalPostgresqlHook(postgres_conn_id=self.postgres_conn_id, config_folder=self.config_folder)
        else:
            self.sql_hook = None

    def get(self, url: str, headers: Optional[Dict[str, str]] = None, query_params: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        """
        Makes a GET request to the resource.
        
        Args:
            url (str): The full URL for the GET request.
            headers (dict, optional): The headers for the GET request. Defaults to None.
            query_params (dict, optional): The query parameters for the GET request. Defaults to None.
            **kwargs: Additional keyword arguments for the GET request.
        
        Returns:
            The response from the GET request.
        """
        hook = UniversalHttpHook('GET', self.http_conn_id, self.config_folder)
        return hook.run(url, headers=headers, query_params=query_params, **kwargs)

    def post(self, url: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None, query_params: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        """
        Makes a POST request to the resource.
        
        Args:
            url (str): The full URL for the POST request.
            data (dict): The data for the POST request.
            headers (dict, optional): The headers for the POST request. Defaults to None.
            query_params (dict, optional): The query parameters for the POST request. Defaults to None.
            **kwargs: Additional keyword arguments for the POST request.
        
        Returns:
            The response from the POST request.
        """
        hook = UniversalHttpHook('POST', self.http_conn_id, self.config_folder)
        return hook.run(url, data=data, headers=headers, query_params=query_params, **kwargs)

    def get_first(self, sql: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Executes the SQL query and returns the first result.
        
        Args:
            sql (str): The SQL query to execute.
            params (dict, optional): The parameters to substitute into the SQL query.
        
        Returns:
            The first result from the executed SQL query as a dictionary where keys are column names and values are column values.
        """
        return self.sql_hook.get_first(sql, params)

    def get_all(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Executes the SQL query and returns all results.
        
        Args:
            sql (str): The SQL query to execute.
            params (dict, optional): The parameters to substitute into the SQL query.

        Returns:
            All results from the executed SQL query as a list of dictionaries where keys are column names and values are column values.
        """
        return self.sql_hook.get_all(sql, params)

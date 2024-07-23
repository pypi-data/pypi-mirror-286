import requests
from typing import Any
from enum import Enum

class ServerActions(Enum):
    CLONE_SERVER = "clone_server"
    START_SERVER = "start_server"
    STOP_SERVER = "stop_server"
    RESTART_SERVER = "restart_server"
    KILL_SERVER = "kill_server"
    BACKUP_SERVER = "backup_server"


class Crafty():

    def __init__(self, host: str = "localhost", port: int = 8443, ssl: bool = False, username: str = None, password: str = None, token: str = None) -> None:
        self.host = host
        self.port = port
        self.ssl = ssl
        self.username = username
        self.password = password
        self.token = token

        if self.token is None:
            if self.username is None or self.password is None:
                raise MissingParameters
            if not self._login():
                raise FailedToLogin
            
    def _make_request(self, path: str = "", method: str = "GET", h: dict[str, Any] = {}, data: dict[str, Any] = {}) -> dict[str, Any] | list | None:
        headers = {
            **h,
            "Authorization": f'Bearer {self.token}'
            }
        
        url = f'http{"s" if self.ssl else ""}://{self.host}:{self.port}/api/v2{path if path.startswith("/") else "/" + str(path)}'
        print(url)
        try:
            req = requests.request(method=method, url=url, headers=headers, json=data)
            if req.json().get("status") == "ok":
                return req.json().get("data")
            return None
        except:
            raise RequestError

    def _login(self) -> bool:
        try:
            data = self._make_request(path="/auth/login", method="POST", data={"username": self.username, "password": self.password})
        except RequestError:
            raise FailedToLogin
        if data.get("token"):
            self.token = data["token"]
            return True
        return False
    
    def roles(self) -> list:
        try:
            return self._make_request(path="/roles")
        except RequestError:
            return []
        
    def role(self, id: int) -> dict[str, Any]:
        try:
            data = self._make_request(path=f'/roles/{id}')
            return {} if data is None else data
        except RequestError:
            return {}

    def role_servers(self, id: int) -> list:
        try:
            data = self._make_request(path=f'/roles/{id}/servers')
            return [] if data is None else data
        except RequestError:
            return []
        
    def role_users(self, id: int) -> list:
        try:
            data = self._make_request(path=f'/roles/{id}/users')
            return [] if data is None else data
        except RequestError:
            return []
        
    def servers(self) -> list:
        try:
            data = self._make_request(path=f'/servers')
            return [] if data is None else data
        except RequestError:
            return []
        
    def server(self, id: str) -> dict[str, Any]:
        for server in self.servers():
            if server.get("server_id") == id:
                return server
            
        return {}
    
    def server_action(self, id: str, action: ServerActions) -> bool | dict[str, Any]:
        try:
            data = self._make_request(method="POST", path=f'/servers/{id}/action/{action.value}')
            return True if data is None else data
        except RequestError:
            return False
        
    def server_logs(self, id: str) -> list:
        try:
            data = self._make_request(path=f'/servers/{id}/logs')
            return [] if data is None else data
        except RequestError:
            return []
        
    def server_public_data(self, id: str) -> dict[str, Any]:
        try:
            data = self._make_request(path=f'/servers/{id}/public')
            return {} if data is None else data
        except RequestError:
            return {}
        
    def server_stats(self, id: str) -> dict[str, Any]:
        try:
            data = self._make_request(path=f'/servers/{id}/stats')
            return {} if data is None else data
        except RequestError:
            return {}
        
    def server_accesses(self, id: str) -> list:
        try:
            data = self._make_request(path=f'/servers/{id}/users')
            return [] if data is None else data
        except RequestError:
            return []
        
    def server_webhooks(self, id: str) -> dict[str, Any]:
        try:
            data = self._make_request(path=f'/servers/{id}/webhook')
            return {} if data is None else data
        except RequestError:
            return {}
        
    def server_webhook(self, server_id: str, webhook_id: str) -> dict[str, Any]:
        try:
            data = self._make_request(path=f'/servers/{server_id}/webhook/{webhook_id}')
            return {} if data is None else data
        except RequestError:
            return {}
        
    def users(self) -> list:
        try:
            data = self._make_request(path=f'/users')
            return [] if data is None else data
        except RequestError:
            return []
        
    def user(self, id: int) -> dict[str, Any]:
        try:
            data = self._make_request(path=f'/users/{id}')
            return {} if data is None else data
        except RequestError:
            return {}
        
    def user_picture(self, id: int) -> dict[str, Any]:
        try:
            return f'http{"s" if self.ssl else ""}://{self.host}:{self.port}' + self._make_request(path=f'/users/{id}/pfp')
        except RequestError:
            return None
        
    def user_public_data(self, id: int) -> dict[str, Any]:
        try:
            data = self._make_request(path=f'/users/{id}/public')
            return {} if data is None else data
        except RequestError:
            return {}



    def test(self):
        return self.token



class MissingParameters(Exception):
    """Missing parameters"""
    pass

class FailedToLogin(Exception):
    """Unable to login"""
    pass

class RequestError(Exception):
    """Error while performing request"""
    pass
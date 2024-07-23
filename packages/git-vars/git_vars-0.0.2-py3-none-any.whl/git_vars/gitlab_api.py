"""
Provides GitLab-related functionality.
"""

import os
import sys
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, quote

import aiohttp

from .utils import get_hostname
from .const import ActionType

# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.append(parent_dir)


class GitLabManager:
    """
    GitLabManager class that implements the necessary methods
    to interact with gitlab env variables API
    """

    def __init__(
        self,
        access_token: Optional[str] = None,
        repository_url: Optional[str] = None,
        scope: Optional[str] = None,
    ):
        self.access_token = access_token or self.get_gitlab_access_token_from_env()
        self.repository_url = repository_url or self.get_gitlab_repo_from_env()
        self.scope = scope or self.get_gitlab_scope_from_env()
        self.hostname = self.get_gitlab_host(self.repository_url)
        self.encoded_path = self.get_project_encoded_path(self.repository_url)

    @staticmethod
    def get_gitlab_access_token_from_env() -> str:
        """
        Static method that takes the 'GITLAB_VARIABLE_ACCESS_TOKEN'
        environment variable if it is present.
        """
        token = os.environ.get("GITLAB_VARIABLE_ACCESS_TOKEN")
        if token:
            return token
        raise ValueError("GitLab access token is required")

    @staticmethod
    def get_gitlab_repo_from_env() -> str:
        """
        Static method that takes the 'GITLAB_REPOSITORY_URL'
        environment variable if it is present.
        """
        repository_url = os.environ.get("GITLAB_REPOSITORY_URL")
        if repository_url:
            return repository_url
        raise ValueError("GitLab Repository URL is required")

    @staticmethod
    def get_gitlab_scope_from_env() -> str:
        """
        Static method that takes the 'GITLAB_PROJECT_scope'
        environment variable if it is present.
        """
        scope = os.environ.get("GITLAB_PROJECT_scope")
        if scope:
            return scope
        return "project"

    @staticmethod
    def get_gitlab_host(repository_url: str) -> str:
        """
        Static method that returns the hostname of the repository.
        """
        return get_hostname(repository_url)

    @staticmethod
    def get_project_encoded_path(repository_url: str) -> str:
        """
        Static method that parses the project path
        """
        path = urlparse(repository_url).path
        path = path[1:] if path.startswith("/") else path
        return quote(path, safe="")

    @staticmethod
    def change_to_group_endpoint(hostname: str, encoded_path: str) -> str:
        """
        Static method that changes the endpoint to group
        """
        encoded_path = "/".join(encoded_path.split("%2F")[:-1])
        return f"{hostname}/api/v4/groups/{encoded_path}/variables"

    def get_endpoint_by_scope(self) -> str:
        """
        Method that gets the endpoint based on the scope (project/group)
        """
        if self.scope == "project":
            return f"{self.hostname}/api/v4/projects/{self.encoded_path}/variables"
        if self.scope == "group":
            return f"{self.hostname}/api/v4/groups/{self.encoded_path}/variables"
        return f"{self.hostname}/api/v4/admin/ci/variables"

    async def gitlab_get_request(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Async method that does the get request to GitLab API
        """
        async with aiohttp.ClientSession() as session:
            headers = {"PRIVATE-TOKEN": self.access_token}
            async with session.get(
                endpoint, headers=headers, params=params
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def gitlab_post_request(self, endpoint: str, body: Dict[str, Any]) -> Any:
        """
        Async method that does the post request to GitLab API
        """
        async with aiohttp.ClientSession() as session:
            headers = {"PRIVATE-TOKEN": self.access_token}
            async with session.post(endpoint, headers=headers, json=body) as response:
                response.raise_for_status()
                return await response.json()

    async def gitlab_put_request(self, endpoint: str, body: Dict[str, Any]) -> Any:
        """
        Async method that does the put request to GitLab API
        """
        async with aiohttp.ClientSession() as session:
            headers = {"PRIVATE-TOKEN": self.access_token}
            async with session.put(endpoint, headers=headers, json=body) as response:
                response.raise_for_status()
                return await response.json()

    async def gitlab_delete_request(self, endpoint: str) -> Any:
        """
        Async method that does the delete request to GitLab API
        """
        async with aiohttp.ClientSession() as session:
            headers = {"PRIVATE-TOKEN": self.access_token}
            async with session.delete(endpoint, headers=headers) as response:
                response.raise_for_status()
                return await response.json()

    async def get_gitlab_env_vars(self) -> List[Dict[str, Any]]:
        """
        Async method that does the get request to GitLab API
        """
        endpoint = self.get_endpoint_by_scope()
        return await self.gitlab_get_request(endpoint)

    async def create_gitlab_env_variables(self, env_vars: List[Dict[str, str]]) -> None:
        """
        Async method that does the post request to GitLab API to CREATE
        new GitLab env variables
        """
        endpoint = self.get_endpoint_by_scope()
        for env_var in env_vars:
            key, value = env_var["key"], env_var["value"]
            try:
                await self.gitlab_post_request(endpoint, {"key": key, "value": value})
                print(f"{ActionType.CREATE} {key} - success")
            except Exception:
                print(f"{ActionType.CREATE} {key} - failed")

    async def delete_gitlab_env_variables(self, env_vars: List[Dict[str, str]]) -> None:
        """
        Async method that does the post request to GitLab API to delete
        already removed GitLab env variables
        """
        for env_var in env_vars:
            key = env_var["key"]
            try:
                endpoint = f"{self.get_endpoint_by_scope()}/{key}"
                await self.gitlab_delete_request(endpoint)
                print(f"{ActionType.DELETE} {key} - success")
            except Exception:
                print(f"{ActionType.DELETE} {key} - success")

    async def update_gitlab_env_variables(self, env_vars: List[Dict[str, str]]) -> None:
        """
        Async method that does the post request to GitLab API to update
        GitLab env variables
        """
        for env_var in env_vars:
            key, value = env_var["key"], env_var["value"]
            try:
                endpoint = f"{self.get_endpoint_by_scope()}/{key}"
                await self.gitlab_put_request(endpoint, {"value": value})
                print(f"{ActionType.UPDATE} {key} - success")
            except Exception:
                print(f"{ActionType.UPDATE} {key} - failed")

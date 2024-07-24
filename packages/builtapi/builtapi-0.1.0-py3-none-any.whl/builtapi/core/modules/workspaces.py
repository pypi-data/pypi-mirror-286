from typing import Dict

import requests
from loguru import logger

from builtapi.core.schemas.workspaces import WorkspacesList
from builtapi.core.convert.workspaces import workspaces_list, workspace


class WorkspacesModuleLatest:

    def __init__(self, token: str, url: str):
        self.token = token
        self.url = url

    @workspaces_list
    def get_list(self):
        """ GET request to get all available for user workspaces """
        url = self.url + '/trpc/workspaces.list?batch=1&input={"0":{"skip": 0}}'
        headers = {"Authorization": f"Bearer {self.token}"}

        workspaces = requests.get(url, headers=headers)
        if workspaces.status_code != 200:
            raise ValueError(f'Workspaces get list failed. Details: {workspaces.text}')

        return workspaces.json()[0]['result']['data']

    @workspace
    def get_one_by_id(self, workspace_id: str) -> Dict:
        """ GET request """
        url = self.url + '/trpc/workspaces.oneById?batch=1&input={"0":{}}'
        workspace_info = requests.get(url, headers={"Authorization": f"Bearer {self.token}",
                                                    "x-builtapi-workspace-id": workspace_id})

        if workspace_info.status_code != 200:
            raise ValueError(f'Workspaces get by ID failed. Details: {workspace_info.text}')

        return workspace_info.json()[0]['result']['data']

    @workspace
    def remove(self, workspace_id: str):
        url = self.url + '/trpc/workspaces.remove?batch=1'
        callback = requests.post(url, headers={"Authorization": f"Bearer {self.token}",
                                               "x-builtapi-workspace-id": workspace_id},
                                 json={"0": {}})
        if callback.status_code != 200:
            raise ValueError(f'Workspace remove failed. Details: {callback.text}')

        logger.debug(f'Workspace "{workspace_id}" was successfully deleted')
        return callback.json()[0]['result']['data']

    @workspace
    def create(self, name: str):
        """ POST request to create new workspace """
        url = self.url + '/trpc/workspaces.create?batch=1'
        body = {"0": {"name": name}}

        callback = requests.post(url, headers={"Authorization": f"Bearer {self.token}"}, json=body)
        if callback.status_code != 200:
            raise ValueError(f'Workspace create failed. Details: {callback.text}')

        return callback.json()[0]['result']['data']

    @workspace
    def update(self, workspace_id: str, name: str):
        """ POST request mutate information about workspace """
        payload = {"name": name}
        url = self.url + '/trpc/workspaces.update?batch=1'
        body = {"0": payload}

        callback = requests.post(url, headers={"Authorization": f"Bearer {self.token}",
                                               "x-builtapi-workspace-id": workspace_id}, json=body)
        if callback.status_code != 200:
            raise ValueError(f'Workspace update failed. Details: {callback.text}')

        return callback.json()[0]['result']['data']

    def leave(self, workspace_id: str):
        """ Current user leave the workspace """
        url = self.url + '/trpc/workspaces.leave?batch=1'
        body = {"0": {}}

        callback = requests.post(url, headers={"Authorization": f"Bearer {self.token}",
                                               "x-builtapi-workspace-id": workspace_id}, json=body)
        if callback.status_code != 200:
            raise ValueError(f'Workspace leave failed. Details: {callback.text}')

        return callback.json()

    def health_check(self):
        """ Health check for module """
        workspaces = self.get_list()
        if isinstance(workspaces, WorkspacesList) is False:
            raise ValueError('Health check for Workspaces module did not pass')
        return self

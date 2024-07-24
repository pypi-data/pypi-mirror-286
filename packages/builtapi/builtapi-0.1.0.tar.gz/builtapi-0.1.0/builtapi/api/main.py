from contextlib import contextmanager
from typing import Union
from urllib.parse import urljoin

from loguru import logger

from builtapi.session import init_session
from builtapi.core.modules.entities import EntitiesModule
from builtapi.core.modules.records import RecordsModule
from builtapi.core.modules.members import MembersModule
from builtapi.core.modules.users import UsersModule
from builtapi.core.modules.views import ViewsModule
from builtapi.settings import BUILTAPI_GATEWAY_URL
from builtapi.token import get_token


class BuiltAPI:
    """
    Class for interacting with BuiltAPI service
    Versions tracked by the
    """

    def __init__(self, workspace_id: str, token: Union[str, None] = None, url: Union[str, None] = None):
        self.token = token or get_token()
        self.url = url or BUILTAPI_GATEWAY_URL
        self.workspace_id = workspace_id

        for field in [self.token, self.url]:
            if field is None:
                raise ValueError('Configuration field can not be None')

        session = init_session(self.workspace_id, self.token, self.url)

        # Modules
        self.entities = EntitiesModule(session)
        self.records = RecordsModule(session)
        self.members = MembersModule(session)
        self.users = UsersModule(session)
        self.views = ViewsModule(session)

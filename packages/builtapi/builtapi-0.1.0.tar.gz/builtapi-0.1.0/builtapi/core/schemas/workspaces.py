from dataclasses import dataclass
from typing import Union, Optional, List

from pydantic import BaseModel


class Workspace(BaseModel):
    """
    Dataclass describes Workspace in BuiltAPI
    """
    id: Optional[Union[str, None]] = None
    created_at: Optional[Union[str, None]] = None
    updated_at: Optional[Union[str, None]] = None
    name: Optional[Union[str, None]] = None


class WorkspacesList(BaseModel):
    """
    Dataclass describes Workspaces as list
    """
    take: Optional[Union[int, None]] = None
    count: Optional[Union[int, None]] = None
    total: Optional[Union[int, None]] = None
    items: Optional[Union[List[Workspace], None]] = None

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Literal, Optional, TypedDict, Union


class Protocol(Enum):
    FILE = "file://"
    S3 = "morph-storage://"


@dataclass
class SignedUrlResponse:
    url: str


@dataclass
class RefResponse:
    cell_type: str
    filepath: str
    alias: str
    code: Optional[str]
    connection_slug: Optional[str]


class FileCellParams(TypedDict):
    type: Literal["file"]
    filepath: Optional[str]
    timestamp: Optional[int]
    base_url: Optional[str]
    team_slug: Optional[str]
    authorization: Optional[str]


class SqlCellParams(TypedDict):
    type: Literal["sql"]
    sql: str
    connection_slug: Optional[str]
    database_id: Optional[str]
    base_url: Optional[str]
    team_slug: Optional[str]
    authorization: Optional[str]


class PythonCellParams(TypedDict):
    type: Literal["python"]
    reference: str
    timestamp: Optional[int]
    base_url: Optional[str]
    team_slug: Optional[str]
    authorization: Optional[str]


LoadDataParams = Union[RefResponse, FileCellParams, SqlCellParams]


@dataclass
class StorageFile:
    name: str
    path: str
    size: int


@dataclass
class StorageDirectory:
    name: str
    path: str
    directories: List[StorageDirectory]
    files: List[StorageFile]


@dataclass
class ListStorageDirectoryResponse:
    path: str
    directories: List[StorageDirectory]
    files: List[StorageFile]


class MorphApiError(Exception):
    pass

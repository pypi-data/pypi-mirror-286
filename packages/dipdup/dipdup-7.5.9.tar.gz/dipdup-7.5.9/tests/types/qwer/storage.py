# generated by datamodel-codegen:
#   filename:  storage.json

from __future__ import annotations

from pydantic import BaseModel
from pydantic import Extra


class QwerStorageItem(BaseModel):
    class Config:
        extra = Extra.forbid

    L: str


class QwerStorageItem1(BaseModel):
    class Config:
        extra = Extra.forbid

    R: dict[str, str]


class QwerStorage(BaseModel):
    __root__: list[list[QwerStorageItem | QwerStorageItem1]]

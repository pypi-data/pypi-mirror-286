# generated by datamodel-codegen:
#   filename:  storage.json

from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict


class Invoices(BaseModel):
    model_config = ConfigDict(extra='forbid')

    invoice: str
    subjkt: str


class HenSubjktStorage(BaseModel):
    model_config = ConfigDict(extra='forbid')

    entries: dict[str, bool]
    invoices: dict[str, Invoices]
    manager: str
    metadata: dict[str, str]
    registries: dict[str, str]
    subjkts: dict[str, bool]
    subjkts_metadata: dict[str, str]

# generated by DipDup 8.0.0b4

from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict


class MovePayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    address: str
    a: str
    b: str
    roll: str
    epoch: str
    rolls: str

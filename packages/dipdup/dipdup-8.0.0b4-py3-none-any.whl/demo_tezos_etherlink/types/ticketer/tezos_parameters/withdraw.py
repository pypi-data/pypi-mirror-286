# generated by DipDup 8.0.0b2

from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict


class Data(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    nat: str
    bytes: str | None = None


class Ticket(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    address: str
    data: Data
    amount: str


class WithdrawParameter(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    receiver: str
    ticket: Ticket

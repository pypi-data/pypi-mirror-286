# generated by datamodel-codegen:
#   filename:  tezos_storage.json

from __future__ import annotations

from pydantic import BaseModel
from pydantic import Extra


class Ledger(BaseModel):
    class Config:
        extra = Extra.forbid

    allowances: dict[str, str]
    balance: str
    frozen_balance: str


class UserRewards(BaseModel):
    class Config:
        extra = Extra.forbid

    reward: str
    reward_paid: str


class Voters(BaseModel):
    class Config:
        extra = Extra.forbid

    candidate: str | None
    last_veto: str
    veto: str
    vote: str


class Storage(BaseModel):
    class Config:
        extra = Extra.forbid

    baker_validator: str
    current_candidate: str | None
    current_delegated: str | None
    last_update_time: str
    last_veto: str
    ledger: dict[str, Ledger]
    period_finish: str
    reward: str
    reward_paid: str
    reward_per_sec: str
    reward_per_share: str
    tez_pool: str
    token_address: str
    token_pool: str
    total_reward: str
    total_supply: str
    total_votes: str
    user_rewards: dict[str, UserRewards]
    veto: str
    vetos: dict[str, str]
    voters: dict[str, Voters]
    votes: dict[str, str]


class QuipuFa12Storage(BaseModel):
    class Config:
        extra = Extra.forbid

    dex_lambdas: dict[str, str]
    metadata: dict[str, str]
    storage: Storage
    token_lambdas: dict[str, str]

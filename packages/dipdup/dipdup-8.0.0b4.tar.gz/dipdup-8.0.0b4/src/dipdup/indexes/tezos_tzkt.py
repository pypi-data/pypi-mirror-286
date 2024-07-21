from abc import ABC
from typing import Any
from typing import Generic

from dipdup.datasources.tezos_tzkt import TezosTzktDatasource
from dipdup.fetcher import BufferT
from dipdup.fetcher import DataFetcher
from dipdup.index import Index
from dipdup.index import IndexConfigT
from dipdup.index import IndexQueueItemT

TZKT_READAHEAD_LIMIT = 10000


class TezosIndex(
    Generic[IndexConfigT, IndexQueueItemT],
    Index[Any, Any, TezosTzktDatasource],
    ABC,
):
    pass


class TezosTzktFetcher(
    Generic[BufferT],
    DataFetcher[BufferT, TezosTzktDatasource],
    ABC,
):
    pass

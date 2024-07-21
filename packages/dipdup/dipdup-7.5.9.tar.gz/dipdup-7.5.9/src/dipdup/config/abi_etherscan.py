from typing import Literal

from pydantic import ConfigDict
from pydantic import Extra
from pydantic.dataclasses import dataclass

from dipdup.config import AbiDatasourceConfig
from dipdup.config import HttpConfig

DEFAULT_ETHERSCAN_URL = 'https://api.etherscan.io/api'


@dataclass(config=ConfigDict(extra=Extra.forbid), kw_only=True)
class EtherscanDatasourceConfig(AbiDatasourceConfig):
    """Etherscan datasource config

    :param kind: always 'abi.etherscan'
    :param url: API URL
    :param api_key: API key
    :param http: HTTP client configuration
    """

    kind: Literal['abi.etherscan']
    url: str = DEFAULT_ETHERSCAN_URL
    api_key: str | None = None

    http: HttpConfig | None = None

from decimal import Decimal

import demo_dex.models as models
from demo_dex.types.quipu_fa12.tezos_parameters.withdraw_profit import WithdrawProfitParameter
from demo_dex.types.quipu_fa12.tezos_storage import QuipuFa12Storage
from dipdup.context import HandlerContext
from dipdup.models.tezos_tzkt import TzktOperationData
from dipdup.models.tezos_tzkt import TzktTransaction


async def on_fa12_withdraw_profit(
    ctx: HandlerContext,
    withdraw_profit: TzktTransaction[WithdrawProfitParameter, QuipuFa12Storage],
    transaction_0: TzktOperationData | None = None,
) -> None:
    symbol = ctx.template_values['symbol']
    trader = withdraw_profit.data.sender_address

    position, _ = await models.Position.get_or_create(trader=trader, symbol=symbol)
    if transaction_0:
        assert transaction_0.amount is not None
        position.realized_pl += Decimal(transaction_0.amount) / (10**6)

        await position.save()
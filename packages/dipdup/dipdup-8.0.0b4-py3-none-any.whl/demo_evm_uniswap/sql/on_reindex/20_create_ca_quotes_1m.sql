CREATE MATERIALIZED VIEW
    candlestick_1m
WITH (timescaledb.continuous) AS

SELECT
    time_bucket('1 minute'::INTERVAL, timestamp) AS bucket,
    token0_id as token_id,
    candlestick_agg(
        timestamp,
        abs(amount_usd/amount0),
        amount_usd
    ) as candlestick
FROM swap
    WHERE
        amount_usd!=0
    AND
        amount0!=0

GROUP BY
    bucket,
    token0_id
ORDER BY
    bucket,
    token0_id
WITH NO DATA;

CREATE INDEX candlestick_1m_bucket ON candlestick_1m(bucket);
CREATE INDEX candlestick_1m_token_id ON candlestick_1m(token_id);

SELECT add_continuous_aggregate_policy(
    'candlestick_1m',
    start_offset => INTERVAL '1 hour',
    end_offset => INTERVAL '0 minutes',
    schedule_interval => INTERVAL '1 minute',
    initial_start := '2018-07-01'
);
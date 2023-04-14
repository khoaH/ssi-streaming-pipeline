#initialize keyspace
DROP KEYSPACE IF EXISTS stock_pipeline;
CREATE KEYSPACE stock_pipeline  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE stock_pipeline;

#realtime stock price/volume
DROP TABLE IF EXISTS trades;
CREATE TABLE trades(
    uuid uuid,
    trade_timestamp timestamp,
    session text,
    symbol text,
    price double,
    traded_volume int,
    diff_percentage float,
    diff_value float,
    total_volume int,
    total_value int,
    PRIMARY KEY((symbol), trade_timestamp)
);

CREATE INDEX IF NOT EXISTS ON trades(trade_timestamp);

#buy and sell orders, real time with calculated buy and sell volume depth
DROP TABLE IF EXISTS orders;
CREATE TABLE orders(
    uuid uuid,
    trade_timestamp timestamp,
    session text,
    symbol text,
    buy_price_1 double,
    buy_volume_1 int,
    buy_price_2 double,
    buy_volume_2 int,
    buy_price_3 double,
    buy_volume_3 int,
    sell_price_1 double,
    sell_volume_1 int,
    sell_price_2 double,
    sell_volume_2 int,
    sell_price_3 double,
    sell_volume_3 int,
    buy_volume_depth_percentage float,
    sell_volume_depth_percentage float,
    PRIMARY KEY((symbol), trade_timestamp)
);

CREATE INDEX IF NOT EXISTS ON orders(trade_timestamp);

#foreign investment real time
DROP TABLE IF EXISTS foreign;
CREATE TABLE foreign(
    uuid uuid,
    session text,
    trade_timestamp timestamp,
    symbol text,
    room double,
    buy double,
    sell double,
    PRIMARY KEY((symbol), trade_timestamp)
);

CREATE INDEX IF NOT EXISTS ON foreign(trade_timestamp);

#real time market data, accumulated and aggregated trades data within the day
DROP TABLE IF EXISTS market;
CREATE TABLE market(
    uuid uuid,
    session text,
    trade_timestamp timestamp,
    symbol text,
    high float,
    low float,
    avg float,
    open float,
    close float,
    PRIMARY KEY((symbol), trade_timestamp)
);

CREATE INDEX IF NOT EXISTS ON market(trade_timestamp);

#static data, no DML after first fetch
DROP TABLE IF EXISTS static;
CREATE TABLE static(
    uuid uuid,
    day timestamp,
    symbol text,
    ref_price float,
    floor float,
    ceiling float,
    PRIMARY KEY((symbol), day)
);

#aggregate every 5s, after session start for 15s, rolling 10,
DROP TABLE IF EXISTS aggregate;
CREATE TABLE aggregate(
    uuid uuid,
    ingest_time timestamp,
    symbol text,
    session text,
    rolling_price float,
    rolling_diff_value float,
    rolling_diff_percentage float,
    rolling_buy_power float,
    rolling_sell_power float,
    rolling_volume int,
    rolling_total bigint,
    PRIMARY KEY((symbol), ingest_time)
);

CREATE INDEX IF NOT EXISTS ON aggregate(ingest_time);

#aggregate every 30s, after session start for 90s, rolling 60s
DROP TABLE IF EXISTS aggregate_foreign;
CREATE TABLE aggregate_foreign(
    uuid uuid,
    ingest_time timestamp,
    symbol text,
    session text,
    rolling_buy float,
    rolling_sell float,
    rolling_room float,
    PRIMARY KEY((symbol), ingest_time)
);

CREATE INDEX IF NOT EXISTS ON aggregate(ingest_time);


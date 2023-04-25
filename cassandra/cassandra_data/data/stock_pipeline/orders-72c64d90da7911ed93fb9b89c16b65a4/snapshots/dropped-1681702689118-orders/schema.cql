CREATE TABLE IF NOT EXISTS stock_pipeline.orders (
	symbol text,
	trade_timestamp timestamp,
	buy_price_1 double,
	buy_price_2 double,
	buy_price_3 double,
	buy_volume_1 int,
	buy_volume_2 int,
	buy_volume_3 int,
	buy_volume_depth_percentage float,
	sell_price_1 double,
	sell_price_2 double,
	sell_price_3 double,
	sell_volume_1 int,
	sell_volume_2 int,
	sell_volume_3 int,
	sell_volume_depth_percentage float,
	session text,
	uuid uuid,
	PRIMARY KEY (symbol, trade_timestamp))
	WITH ID = 72c64d90-da79-11ed-93fb-9b89c16b65a4
	AND CLUSTERING ORDER BY (trade_timestamp ASC)
	AND bloom_filter_fp_chance = 0.01
	AND dclocal_read_repair_chance = 0.1
	AND crc_check_chance = 1.0
	AND default_time_to_live = 0
	AND gc_grace_seconds = 864000
	AND min_index_interval = 128
	AND max_index_interval = 2048
	AND memtable_flush_period_in_ms = 0
	AND read_repair_chance = 0.0
	AND speculative_retry = '99PERCENTILE'
	AND comment = ''
	AND caching = { 'keys': 'ALL', 'rows_per_partition': 'NONE' }
	AND compaction = { 'max_threshold': '32', 'min_threshold': '4', 'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy' }
	AND compression = { 'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor' }
	AND cdc = false
	AND extensions = {  };
CREATE INDEX orders_trade_timestamp_idx ON stock_pipeline.orders (trade_timestamp);

CREATE TABLE IF NOT EXISTS stock_pipeline.trades (
	symbol text,
	trade_timestamp timestamp,
	diff_percentage float,
	diff_value float,
	price double,
	session text,
	total_value int,
	total_volume int,
	traded_volume int,
	uuid uuid,
	PRIMARY KEY (symbol, trade_timestamp))
	WITH ID = 70260030-da79-11ed-93fb-9b89c16b65a4
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
CREATE INDEX trades_trade_timestamp_idx ON stock_pipeline.trades (trade_timestamp);

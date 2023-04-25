CREATE TABLE IF NOT EXISTS stock_pipeline.aggregate (
	symbol text,
	ingest_time timestamp,
	rolling_buy_power float,
	rolling_diff_percentage float,
	rolling_diff_value float,
	rolling_price float,
	rolling_sell_power float,
	rolling_total bigint,
	rolling_volume int,
	session text,
	uuid uuid,
	PRIMARY KEY (symbol, ingest_time))
	WITH ID = 7c14f680-da79-11ed-93fb-9b89c16b65a4
	AND CLUSTERING ORDER BY (ingest_time ASC)
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
CREATE INDEX aggregate_ingest_time_idx ON stock_pipeline.aggregate (ingest_time);

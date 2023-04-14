from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, split, expr, col, from_unixtime, filter, to_date
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
import pyspark

# Create SparkSession
spark = SparkSession.builder.appName("testRead").getOrCreate()

#read kafka stream
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "stock-data-stream") \
    .load()

schema = StructType([
    StructField("timestamp", StringType()),
    StructField("message", StringType())
])

data = df.selectExpr('CAST(value as STRING)').select(from_json("value", schema).alias('json')).select('json.*')

split_cols = data.select(col('timestamp'),expr('SPLIT(message, "[|]") as columns'))

result = split_cols.selectExpr(
    "uuid() as uuid",
    "from_unixtime(timestamp) as trade_timestamp",
    # "cast(columns[0] as string) as ssi_id", #Reconsidering since it need to be process from an external dictionary to get the symbol. The Foreign trades don't include symbol
    "cast(columns[1] as string) as symbol",
    "cast(columns[2] as double) as buy_price_1", #Gia_mua_1
    "cast(columns[3] as integer) as buy_volume_1", #KL_mua_1
    "cast(columns[4] as double) as buy_price_2", #Gia_mua_2
    "cast(columns[5] as integer) as buy_volume_2", #KL_mua_2
    "cast(columns[6] as double) as buy_price_3", #Gia_mua_3
    "cast(columns[7] as integer) as buy_volume_3", #KL_mua_3
    "cast(columns[22] as double) as sell_price_1", #Gia_ban_1
    "cast(columns[23] as integer) as sell_volume_1", #KL_ban_1
    "cast(columns[24] as double) as sell_price_2", #Gia_ban_2
    "cast(columns[25] as integer) as sell_volume_2", #KL_ban_2
    "cast(columns[26] as double) as sell_price_3", #Gia_ban_3
    "cast(columns[27] as integer) as sell_volume_3", #KL_ban_3
    "cast(columns[42] as double) as price", #Gia_khop
    "cast(columns[43] as integer) as traded_volume", #KL_khop
    "cast(columns[44] as float) as high", #Cao
    "cast(columns[46] as float) as low", #Thap
    "cast(columns[47] as float) as avg", #TB
    "cast(columns[48] as double) as buy", #NN_mua
    "cast(columns[50] as double) as sell", #NN_ban
    "cast(columns[52] as float) as diff_value", #GiaoDong
    "cast(columns[53] as float) as diff_percentage", #GiaoDongPhanTram
    "cast(columns[54] as integer) as total_volume", #Tong_KL
    "cast(columns[55] as integer) as total_value", #Tong_GiaTri
    "cast(columns[59] as double) as ceiling", #Tran
    "cast(columns[60] as double) as floor", #San
    "cast(columns[61] as double) as ref_price", #TC
    "cast(columns[63] as string) as session", #session
    "cast(columns[65] as double) as room", #room
    "cast(columns[75] as double) as open", #Open
    "cast(columns[76] as double) as close" #Close
)



query = result.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

cleansed = result.filter("session is NOT NULL")

filtered = cleansed.filter("price is NOT NULL")

trades = filtered.select(
    "uuid",
    "session",
    'trade_timestamp',
    "symbol",
    "price",
    "traded_volume",
    "diff_percentage",
    "diff_value",
    "total_volume",
    "total_value"
)

def foreach_batch_function(df, epoch_id):
    df.write\
    .format("org.apache.spark.sql.cassandra")\
    .mode('append')\
    .options(table="trades", keyspace="stock_pipeline")\
    .save()
    pass

trades.writeStream\
    .foreachBatch(foreach_batch_function).start()

orders = filtered.select(
    "uuid",
    "trade_timestamp",
    "session",
    "symbol",
    "buy_price_1",
    "buy_volume_1",
    "buy_price_2",
    "buy_volume_2",
    "buy_price_3",
    "buy_volume_3",
    "sell_price_1",
    "sell_volume_1",
    "sell_price_2",
    "sell_volume_2",
    "sell_price_3",
    "sell_volume_3",
    (col("buy_volume_1") + col("buy_volume_2") + col("buy_volume_3") / (col("buy_volume_1") + col("buy_volume_2") + col("buy_volume_3") + col("sell_volume_1") + col("sell_volume_2") + col("sell_volume_3"))*100).alias("buy_volume_depth_percentage"),
    (col("sell_volume_1") + col("sell_volume_2") + col("sell_volume_3") / (col("buy_volume_1") + col("buy_volume_2") + col("buy_volume_3") + col("sell_volume_1") + col("sell_volume_2") + col("sell_volume_3"))*100).alias("sell_volume_depth_percentage"),
)

def foreach_orders_batch_function(df, epoch_id):
    df.write\
    .format("org.apache.spark.sql.cassandra")\
    .mode('append')\
    .options(table="orders", keyspace="stock_pipeline")\
    .save()
    pass

orders.writeStream\
    .foreachBatch(foreach_orders_batch_function).start()

# foreing_msg = cleansed.filter("room is NOT NULL")

# foreign = foreing_msg.select(
#     "uuid",
#     "session",
#     "trade_timestamp",
#     "symbol",
#     "room",
#     "buy",
#     "sell"
# )

# def foreach_foreign_batch_function(df, epoch_id):
#     df.write\
#     .format("org.apache.spark.sql.cassandra")\
#     .mode('append')\
#     .options(table="foreign", keyspace="stock_pipeline")\
#     .save()
#     pass

# foreign.writeStream\
#     .foreachBatch(foreach_foreign_batch_function).start()

market = filtered.select(
    "uuid",
    "session",
    "trade_timestamp",
    "symbol",
    "high",
    "low",
    "avg",
    "open",
    "close"
)

def foreach_market_batch_function(df, epoch_id):
    df.write\
    .format("org.apache.spark.sql.cassandra")\
    .mode('append')\
    .options(table="market", keyspace="stock_pipeline")\
    .save()
    pass

market.writeStream\
    .foreachBatch(foreach_market_batch_function).start()

spark.streams.awaitAnyTermination() 

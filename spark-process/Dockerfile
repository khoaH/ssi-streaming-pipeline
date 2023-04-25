FROM bde2020/spark-python-template:3.3.0-hadoop3.3

COPY spark-process.py ./app

ENV SPARK_APPLICATION_PYTHON_LOCATION /app/spark-process.py
ENV SPARK_SUBMIT_ARGS "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,com.datastax.spark:spark-cassandra-connector_2.12:3.3.0,com.datastax.cassandra:cassandra-driver-core:3.11.3"
ENV SPARK_APPLICATION_ARGS "--conf spark.sql.extensions=com.datastax.spark.connector.CassandraSparkExtensions"
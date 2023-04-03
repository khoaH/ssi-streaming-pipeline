#!/bin/sh
# blocks until kafka is reachable
kafka-topics --bootstrap-server kafka:29092 --list

echo -e 'Creating kafka topics'
kafka-topics --bootstrap-server kafka:29092 --create --if-not-exists --topic stock-data-stream --replication-factor 1 --partitions 1

echo -e 'Successfully created the following topics:'
kafka-topics --bootstrap-server kafka:29092 --list
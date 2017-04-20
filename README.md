# Chillii Collector

This app collects sensor values from Chillii Sytsem Controller and pushs them to Kafka.

## Requirements
Required libraries:

- python3
- librdkafka

Required non-standard python packages:

- json
- jsonschema
- avro-python3
- pymodbus3
- confluent_kafka
- kafka_connector
- modbusreader

Install all required libraries and python packages.

## Getting started
First, clone this project to your local PC. Then, you can run `collector.py`. For parameterization, environment variables are used.

## Timing
The time of sensor values is set to the time before the function to read the values over modbus is called.

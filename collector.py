#!/usr/bin/env python3

import logging.config
import os
import time
import pymodbus3.exceptions

from kafka_connector.avro_loop_producer import AvroLoopProducer
from kafka_connector.timer import Unit, Begin
from modbusreader import ModbusReader

__author__ = "Stephan Müller"
__copyright__ = "2017, Stephan Müller"
__license__ = "MIT"

__dirname__ = os.path.dirname(os.path.abspath(__file__))

MODBUS_HOST = os.getenv("MODBUS_HOST", "localhost")
MODBUS_PORT = int(os.getenv("MODBUS_PORT", 502))
MODBUS_UNIT = int(os.getenv("MODBUS_UNIT", 1))
PUSH_INTERVAL = int(os.getenv("PUSH_INTERVAL", 1000))
KAFKA_HOSTS = os.getenv("KAFKA_HOSTS", "kafka:9092")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://schema-registry:8082")
TOPIC = os.getenv("TOPIC", "stcs.chillii")

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
logging_format = "%(levelname)8s %(asctime)s %(name)s [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"

modbus_definition_file = __dirname__ + "/config/modbus-definition.json"
key_schema = __dirname__ + "/config/key.avsc"
value_schema = __dirname__ + "/config/value.avsc"

logging.basicConfig(level=logging.getLevelName(LOGGING_LEVEL), format=logging_format)
logger = logging.getLogger('collector')


modbus_reader = ModbusReader(MODBUS_HOST, MODBUS_PORT, MODBUS_UNIT, modbus_definition_file, float_low_byte_first=True)


def get_data():
    try:
        return {
            'key': {'timestamp': time.time() * 1000},
            'value': modbus_reader.read_all_values()
        }

    except pymodbus3.exceptions.ModbusIOException as e:
        logger.exception(e)

    except pymodbus3.exceptions.ConnectionException:
        # exception is already logged by pymodbus3.client.sync
        pass


producer = AvroLoopProducer(KAFKA_HOSTS, SCHEMA_REGISTRY_URL, TOPIC, key_schema, value_schema)

producer.loop(get_data, interval=PUSH_INTERVAL, unit=Unit.MILLISECOND, begin=Begin.FULL_SECOND)

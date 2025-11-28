# kafka_broker.py
import os, time, socket
from kafka import KafkaProducer, errors
from typing import Optional
from src.utils.logger import get_logger

logger = get_logger("IDS_IPS")

BOOTSTRAP = os.getenv("KAFKA_BROKER", "kafka:9092")
HOST, PORT = BOOTSTRAP.split(":")
PORT = int(PORT)

def wait_for_kafka(timeout=120):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((HOST, PORT), timeout=2):
                return True
        except OSError:
            time.sleep(2)
    return False

def create_producer(max_retries=20, delay=3):
    if not wait_for_kafka(timeout=120):
        raise RuntimeError(f"Kafka not reachable at {BOOTSTRAP}")
    last_err = None
    for _ in range(max_retries):
        try:
            return KafkaProducer(
                bootstrap_servers=[BOOTSTRAP],
                security_protocol="PLAINTEXT",
                api_version=(3, 6, 0),   # cp-kafka 7.6.x ~ Kafka 3.6
                request_timeout_ms=10000,
                metadata_max_age_ms=30000,
            )
        except errors.NoBrokersAvailable as e:
            last_err = e
            time.sleep(delay)
    raise last_err or errors.NoBrokersAvailable()

_producer = None
def get_producer():
    global _producer
    if _producer is None:
        _producer = create_producer()
    return _producer

def send_message(topic: str, value: bytes, key: Optional[bytes] = None):
#    p = get_producer()
#    return p.send(topic, key=key, value=value)

    """removed KAFKA version"""
    logger.info(f'[LOG MESSAGE] topic={topic} key={key} value={value}')

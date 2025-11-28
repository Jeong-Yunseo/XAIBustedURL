import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

URL_TOPIC = os.getenv("URL_TOPIC", "url_stream")
FEATURE_TOPIC = os.getenv("FEATURE_TOPIC", "url_features")
PREDICTION_TOPIC = os.getenv("PREDICTION_TOPIC", "url_predictions")

MODEL_NAMES = [m.strip() for m in os.getenv("MODEL_NAMES", "bert-base-uncased,roberta-base,distilbert-base").split(",")]
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

USE_XLNET = os.getenv("USE_XLNET", "0") == "1"
XLNET_MODEL_NAME = os.getenv("XLNET_MODEL_NAME", "xlnet-base-cased")

try:
    if USE_XLNET:
        if isinstance(MODEL_NAMES, list) and XLNET_MODEL_NAME not in MODEL_NAMES:
            MODEL_NAMES.append(XLNET_MODEL_NAME)
except NameError:
    if USE_XLNET:
        MODEL_NAMES = [XLNET_MODEL_NAME]

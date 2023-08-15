import json

from kafka import KafkaProducer

from config.config import KafkaConf


def get_kafka_producer(kafka_conf: KafkaConf = KafkaConf()):
    return KafkaProducer(bootstrap_servers=[kafka_conf.config_values.kafka_server])


def send_to_kafka(producer: KafkaProducer, topic_name: str, data):
    try:
        producer.send(topic_name, value=data)

        producer.flush()

        print(f"Data published to Kafka topic {topic_name}: {data}")
        return True

    except Exception as e:
        # Log the error and return False if data couldn't be published
        print(f"Failed to publish data to Kafka topic {topic_name}: {e}")
        return False
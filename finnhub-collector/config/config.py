from pydantic import BaseModel

from src.utils.file import load_conf


class KafkaConfModel(BaseModel):
    kafka_server: str
    kafka_port: str
    kafka_topic_name: str


class KafkaConf:
    """
    Class to manage environment variables and configurations for the FinnhubProducer.

    Attributes: Retrieved from the configuration file
        kafka_server (str): Kafka server address
        kafka_port (str): Kafka port number
        kafka_topic_name (str): Kafka topic name
    """

    def __init__(self, conf_file_path: str = 'kafka_conf.yaml'):
        """
        Initialize the Configuration instance by loading configuration values from a YAML file.

        Args:
            conf_file_path (str, optional): Path to the YAML configuration file. Defaults to 'config/kafka_conf.yaml'.
        """
        self.conf_file_path = conf_file_path
        self.config_values = self.load_configuration()

    def load_configuration(self):
        """
        Load configuration values from the YAML file.
        """
        try:
            config_kafka_values = load_conf(self.conf_file_path)

            # kafka values
            kafka_server = config_kafka_values.get('KAFKA_SERVER', "localhost")
            kafka_port = config_kafka_values.get('KAFKA_PORT', "9092")
            kafka_topic_name = config_kafka_values.get('KAFKA_TOPIC_NAME', "raw-live-trades")

            return KafkaConfModel(
                kafka_server=kafka_server,
                kafka_port=kafka_port,
                kafka_topic_name=kafka_topic_name
            )

        except Exception as e:
            print(f"Error loading configuration: {e}")
            return KafkaConfModel()



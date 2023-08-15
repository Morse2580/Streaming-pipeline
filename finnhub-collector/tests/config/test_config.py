# Kafka Configuration
import pytest

from config.config import KafkaConf
from src.utils.file import load_conf


class KafkaConfigurationTest:
    @pytest.fixture
    def kafka_config(self):
        """
        Fixture to create the FinnhubConfiguration instance.
        """
        return KafkaConf()

    @pytest.mark.parametrize(
        "attribute, expected_value",
        [
            ("kafka_server", "localhost"),
            ("kafka_port", "9092"),
            ("kafka_topic_name", 'live-trades'),
        ]
    )
    def test_configuration_attributes(self, kafka_config, attribute, expected_value):
        """
        Test the attributes of the Configuration instance.
        """
        assert getattr(kafka_config, attribute) == expected_value


test_cases_valid = [
    pytest.param(
        "config/kafka_conf.yaml",
        {
            'KAFKA_SERVER': 'localhost',
            'KAFKA_PORT': '9092',
            'KAFKA_TOPIC_NAME': 'raw-live-trades'
        },
        id="Test case 2: Valid kafka configuration"
    )
]


@pytest.mark.parametrize("conf_file_path, file_output", test_cases_valid)
def test_valid_configuration(conf_file_path: str, file_output):
    """
    Test the Configuration class with valid YAML configurations.
    """
    config = load_conf(conf_file_path)
    print(config)
    assert config == file_output

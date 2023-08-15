import pytest

from config.config import FinnhubConf, load_conf


# Finnhub Configuration
class FinnhubConfTest:

    @pytest.fixture
    def finnhub_config(self):
        """
        Fixture to create the FinnhubConfiguration instance.
        """
        return FinnhubConf()

    @pytest.mark.parametrize(
        "attribute, expected_value",
        [
            ("finnhub_api_token", "API_KEY_TOKEN"),
            ("finnhub_validate_tickers", "1"),
            ("finnhub_stocks_tickers", []),
        ]
    )
    def test_configuration_attributes(self, finnhub_config, attribute, expected_value):
        """
        Test the attributes of the Configuration instance.
        """
        assert getattr(finnhub_config, attribute) == expected_value


# loadConf() method
# Valid Test cases with the configuration file paths
test_cases_valid = [
    pytest.param(
        "finnhub_conf.yaml",
        {
            'FINNHUB_API_TOKEN': 'API_KEY_TOKEN',
            'FINNHUB_STOCKS_TICKERS': ['AAPL', 'BINANCE:ETHUSDT', 'BINANCE:BTCUSDT'],
            'FINNHUB_VALIDATE_TICKERS': '1'
        },
        id="Test case MAIN_FINNHUB: Valid finnhub configuration"
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


# Test cases that raise an error
test_cases_invalid = [
    pytest.param(
        "tests/test_config2.yaml",
        {},
        id="Test case 1: Empty configuration"
    ),
    pytest.param(
        "tests/non_existent_config.yaml",
        {},
        id="Test case 2: Non-existent configuration file"
    ),
    pytest.param(
        "tests/invalid_yaml.yaml",
        {},
        id="Test case 3: Invalid YAML syntax"
    )
]


@pytest.mark.parametrize("conf_file_path, file_output", test_cases_invalid)
def test_invalid_configuration(conf_file_path: str, file_output):
    """
    Test the Configuration class with invalid YAML configurations.
    """
    config = load_conf(conf_file_path)
    assert config == file_output

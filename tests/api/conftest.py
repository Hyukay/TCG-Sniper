import pytest
from requests_mock import Mocker
import os
from dotenv import load_dotenv

load_dotenv(".env.test")  # Charge les variables d'environnement de test

@pytest.fixture
def ebay_api_key():
    return os.getenv("EBAY_SANDBOX_API_KEY")

@pytest.fixture
def tcgplayer_api_key():
    return os.getenv("TCGPLAYER_TEST_API_KEY")

@pytest.fixture
def requests_mock_fixture():
    with Mocker() as m:
        yield m
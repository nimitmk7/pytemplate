import pytest
from unittest.mock import Mock


@pytest.fixture
def available_models():
    return ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]

@pytest.fixture
def api_key():
    return "test_api_key"

def test_get_available_models():
    model_provider = Mock()
    model_provider.get_available_models.return_value = available_models
    assert model_provider.get_available_models() == available_models

def 



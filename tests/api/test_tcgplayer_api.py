import pytest
from src.data_collection.tcgplayer_api import TCGPlayerAPI

# Test 1 : Récupération des données de prix
def test_tcgplayer_fetch_prices(requests_mock_fixture, tcgplayer_api_key):
    mock_response = {
        "results": [
            {"productId": 123, "marketPrice": 99.99}
        ]
    }
    
    requests_mock_fixture.get(
        "https://api.tcgplayer.com/pricing/product/123",
        json=mock_response,
        status_code=200,
        headers={"Authorization": f"Bearer {tcgplayer_api_key}"}
    )
    
    api = TCGPlayerAPI(use_sandbox=True)
    prices = api.fetch_prices([123])
    
    assert prices[123] == 99.99

# Test 2 : Gestion des limites de taux (429 Too Many Requests)
def test_tcgplayer_rate_limiting(requests_mock_fixture):
    requests_mock_fixture.get(
        "https://api.tcgplayer.com/pricing/product/123",
        status_code=429,
        headers={"Retry-After": "5"}
    )
    
    api = TCGPlayerAPI(use_sandbox=True)
    prices = api.fetch_prices([123])
    
    assert 123 not in prices

# Test 3 : Données de produit incomplètes
def test_tcgplayer_incomplete_data(requests_mock_fixture):
    mock_response = {
        "results": [
            {"productId": 456}  # Pas de 'marketPrice'
        ]
    }
    
    requests_mock_fixture.get(
        "https://api.tcgplayer.com/pricing/product/456",
        json=mock_response
    )
    
    api = TCGPlayerAPI(use_sandbox=True)
    prices = api.fetch_prices([456])
    
    assert prices.get(456) is None
import pytest
from unittest.mock import MagicMock
from src.business_logic.sniper_engine import SniperEngine
from src.ai_analysis.price_oracle import PriceOracle

class MockOracle:
    def __init__(self, predicted_price=100.0):
        self.predicted_price = predicted_price
    
    def predict_price(self, listing):
        return self.predicted_price

# Test 1: Opportunité claire sous le seuil
def test_clear_opportunity():
    oracle = MockOracle(200.0)
    sniper = SniperEngine(oracle)
    listing = {"title": "Black Lotus", "price": {"value": 150.0}}
    assert sniper.evaluate_listing(listing, 180.0) is True

# Test 2: Prix exactement à 80% de la valeur prédite
def test_edge_case_80_percent():
    oracle = MockOracle(100.0)
    sniper = SniperEngine(oracle)
    listing = {"title": "Test Edge", "price": {"value": 80.0}}
    assert sniper.evaluate_listing(listing, 100.0) is True

# Test 3: Prix légèrement au-dessus du seuil
def test_slightly_above_threshold():
    oracle = MockOracle(100.0)
    sniper = SniperEngine(oracle)
    listing = {"title": "Test", "price": {"value": 81.0}}
    assert sniper.evaluate_listing(listing, 100.0) is False

# Test 4: Données de listing corrompues
def test_invalid_listing_data():
    oracle = MockOracle()
    sniper = SniperEngine(oracle)
    
    with pytest.raises(KeyError):
        sniper.evaluate_listing({"invalid": "data"}, 100.0)

# Test 5: Oracle retourne None
def test_oracle_failure():
    oracle = MagicMock()
    oracle.predict_price.return_value = None
    sniper = SniperEngine(oracle)
    
    listing = {"title": "Test", "price": {"value": 50.0}}
    assert sniper.evaluate_listing(listing, 100.0) is False

# Test 6: Comparaison avec prix maximum
@pytest.mark.parametrize("price,max_price,expected", [
    (90.0, 100.0, True),   # Sous le max et sous le seuil
    (95.0, 90.0, False),   # Au-dessus du max 
    (90.0, 90.0, False)    # Exactement le max
])
def test_price_boundaries(price, max_price, expected):
    oracle = MockOracle(100.0)
    sniper = SniperEngine(oracle)
    listing = {"title": "Boundary Test", "price": {"value": price}}
    assert sniper.evaluate_listing(listing, max_price) == expected

# Test 7: Prix négatif (cas d'erreur)
def test_negative_pricing():
    oracle = MockOracle(100.0)
    sniper = SniperEngine(oracle)
    listing = {"title": "Negative", "price": {"value": -10.0}}
    assert sniper.evaluate_listing(listing, 100.0) is False

# Test 8: Format de prix inhabituel
def test_unusual_price_format():
    oracle = MockOracle(100.0)
    sniper = SniperEngine(oracle)
    
    listing = {"title": "Weird Price", "price": {"value": "100,00"}}
    assert sniper.evaluate_listing(listing, 150.0) is False

# Test 9: Comportement avec différentes devises
def test_currency_conversion():
    oracle = MockOracle(100.0)  # EUR
    sniper = SniperEngine(oracle)
    
    listing_usd = {"title": "USD", "price": {"value": 85.0, "currency": "USD"}}
    listing_jpy = {"title": "JPY", "price": {"value": 10000.0, "currency": "JPY"}}
    
    # Devrait échouer sans système de conversion
    assert sniper.evaluate_listing(listing_usd, 100.0) is False  
    assert sniper.evaluate_listing(listing_jpy, 100.0) is False

# Test 10: Performance sur des gros volumes
def test_performance_large_volume():
    oracle = MockOracle(100.0)
    sniper = SniperEngine(oracle)
    
    listings = [{"title": f"Test {i}", "price": {"value": 80.0}} for i in range(1000)]
    
    for listing in listings:
        assert sniper.evaluate_listing(listing, 100.0) is True
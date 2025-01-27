import pytest
from src.business_logic.sniper_engine import SniperEngine
from src.ai_analysis.price_oracle import PriceOracle

class MockOracle:
    def __init__(self, predicted_price=100.0):
        self.predicted_price = predicted_price

    def predict_price(self, _):
        return self.predicted_price

def test_evaluate_listing_underpriced():
    oracle = MockOracle(predicted_price=100.0)
    sniper = SniperEngine(oracle)
    listing = {"title": "Charizard", "price": {"value": 80.0}}
    
    assert sniper.evaluate_listing(listing, 90) is True

def test_evaluate_listing_overpriced():
    oracle = MockOracle(predicted_price=1000)
    sniper = SniperEngine(oracle)
    listing = {"title": "Test", "price": {"value": 1200}}
    
    assert sniper.evaluate_listing(listing, 1000) is False
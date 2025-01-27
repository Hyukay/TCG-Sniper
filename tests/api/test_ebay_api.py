import pytest
import json
from src.data_collection.ebay_scraper import EbayScraper

# Test 1 : Récupération réussie de listings
def test_ebay_fetch_listings_success(requests_mock_fixture, ebay_api_key):
    # Mock de la réponse API eBay
    mock_response = {
        "itemSummaries": [
            {"title": "Charizard Test", "price": {"value": "100.00"}}
        ]
    }
    
    # URL de l'API eBay Sandbox
    url = "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?q=Charizard"
    
    requests_mock_fixture.get(
        url,
        json=mock_response,
        status_code=200,
        headers={"Authorization": f"Bearer {ebay_api_key}"}
    )
    
    scraper = EbayScraper(use_sandbox=True)
    listings = scraper.fetch_listings("Charizard")
    
    assert len(listings) == 1
    assert listings[0]["title"] == "Charizard Test"

# Test 2 : Gestion des erreurs 401 (Non Autorisé)
def test_ebay_api_unauthorized(requests_mock_fixture):
    requests_mock_fixture.get(
        "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search",
        status_code=401,
        json={"errors": [{"errorId": 401, "message": "Unauthorized"}]}
    )
    
    scraper = EbayScraper(use_sandbox=True)
    listings = scraper.fetch_listings("Charizard")
    
    assert listings == []

# Test 3 : Pagination des résultats
def test_ebay_pagination(requests_mock_fixture, ebay_api_key):
    mock_page1 = {"itemSummaries": [{"title": "Page 1"}], "next": "page2_token"}
    mock_page2 = {"itemSummaries": [{"title": "Page 2"}]}
    
    # Mock des deux pages
    requests_mock_fixture.get(
        "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?q=test",
        json=mock_page1,
        headers={"Authorization": f"Bearer {ebay_api_key}"}
    )
    requests_mock_fixture.get(
        "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?offset=page2_token",
        json=mock_page2,
        headers={"Authorization": f"Bearer {ebay_api_key}"}
    )
    
    scraper = EbayScraper(use_sandbox=True)
    scraper.enable_pagination = True
    listings = scraper.fetch_listings("test")
    
    assert len(listings) == 2
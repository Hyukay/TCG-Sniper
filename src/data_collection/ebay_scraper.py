import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class EbayScraper:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expiry = None
        
        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=1)
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def _get_access_token(self):
        """Get OAuth access token from eBay"""
        if self.access_token and self.token_expiry > datetime.now():
            return self.access_token

        try:
            url = "https://api.ebay.com/identity/v1/oauth2/token"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {self._get_basic_auth()}"
            }
            data = {
                "grant_type": "client_credentials",
                "scope": "https://api.ebay.com/oauth/api_scope"
            }

            response = self.session.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.token_expiry = datetime.now() + timedelta(seconds=token_data["expires_in"])
            
            return self.access_token
        except Exception as e:
            logger.error(f"Failed to get eBay access token: {e}")
            raise

    def fetch_listings(self, search_query):
        """Fetch eBay listings via their API (secure version)."""
        try:
            url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
            headers = {"Authorization": f"Bearer {self._get_access_token()}"}
            params = {"q": search_query, "limit": 10}
            
            response = self.session.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json().get('itemSummaries', [])
        except Exception as e:
            logger.error(f"Failed to fetch eBay listings: {e}")
            return []
import logging

logger = logging.getLogger(__name__)

class SniperEngine:
    def __init__(self, oracle):
        self.oracle = oracle

    def evaluate_listing(self, listing, max_price):
        if listing['price']['value'] > max_price:
            return False
            
        predicted_price = self.oracle.predict_price(listing)
        if predicted_price and listing['price']['value'] <= predicted_price * 0.8:  # Changed < to <=
            logger.debug(f"Opportunité détectée : {listing['title']}")
            return True
        return False
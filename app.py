from src.data_collection.ebay_scraper import EbayScraper
from src.ai_analysis.price_oracle import PriceOracle
from src.business_logic.sniper_engine import SniperEngine
from src.utils.logger import setup_logger
from config import EBAY_SEARCH_QUERY, MAX_PRICE

logger = setup_logger()

def main():
    # Initialisation des composants
    scraper = EbayScraper()
    oracle = PriceOracle()
    sniper = SniperEngine(oracle)
    
    logger.info("Démarrage de l'application...")
    
    # Boucle de surveillance
    while True:
        try:
            listings = scraper.fetch_listings(EBAY_SEARCH_QUERY)
            for listing in listings:
                if sniper.evaluate_listing(listing, MAX_PRICE):
                    logger.info(f"Opportunité trouvée : {listing['title']}")
        except Exception as e:
            logger.error(f"Erreur : {e}")

if __name__ == "__main__":
    main()
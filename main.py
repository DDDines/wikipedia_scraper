# import src.utils as utils
from src.scraper import WikipediaScraper


if __name__ == "__main__":
    """
    Main script execution point.

    This script sets up the WikipediaScraper with 'https://country-leaders.onrender.com' to gather information about leaders from around the world.

    1. Creates an instance of the scraper configured with the base URL.
    2. Calls `get_everyone` to compile details on leaders from various countries, which includes retrieving introductory paragraphs from their Wikipedia pages.
    3. Stores the collected data into a file named 'data.json'.

    """
    scrapper = WikipediaScraper("https://country-leaders.onrender.com")
    scrapper.get_everyone()
    scrapper.to_json_file("data.json")

    print("Finish!")

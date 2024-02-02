# import src.utils as utils
from src.scraper import WikipediaScraper


if __name__ == "__main__":
    """
    Main entry point of the script.yy

    """
    scrapper = WikipediaScraper("https://country-leaders.onrender.com")
    scrapper.get_everyone()
    scrapper.to_json_file("data.json")

    print("Finish!")

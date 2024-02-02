# Wikipedia Scraper

This is a Python project designed to extract information about country leaders from a third-party website. The goal is to collect data about leaders from various countries, including their names, birth and death dates, places of birth, Wikipedia URLs, and the first paragraph of their biographies.

## Prerequisites

- Python 3.x
- Python libraries: requests, json, bs4 (Beautiful Soup), re

You can install the required libraries with the following command:

    pip install requests beautifulsoup4

## Usage

### To run the scraper, follow these steps:

    1. Clone the repository.
    2. Navigate to the project directory.
    3. Execute the main script:

        python main.py

    This will initiate the scraper, which will gather information about country leaders and save the data to a JSON file named "data.json."

## Project Structure

### main.py:

The main entry point file that initiates the scraper.

### scraper.py:

Contains the WikipediaScraper class, which performs the data scraping.

### src/utils.py:

A utility file that can be used for auxiliary functions in the future (currently not utilized).

## Features

The scraper obtains an authentication cookie from the third-party website.
It collects the list of available countries.
For each country, it gathers information about its leaders.
It extracts the first paragraph of leaders' biographies using BeautifulSoup.
The collected data is stored in a JSON file.

## Contributions

Contributions are welcome! If you wish to enhance or add features to the project, follow these steps

1- Fork the repository.
2 - Create a new branch for your contribution: git checkout -b my-contribution
3 - Make the necessary changes and clearly describe them.
4 - Submit a pull request.

## Author

Julio Cesar Barizon Montes

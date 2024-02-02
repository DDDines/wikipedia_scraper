import requests
import json
from bs4 import BeautifulSoup
import re


class WikipediaScraper:

    def __init__(self, base_url: str):
        # Initialize the scraper with URL and endpoints for countries, leaders, and cookies.
        self.base_url = base_url
        self.country_endpoint = '/countries'
        self.leaders_endpoint = '/leaders'
        self.cookies_endpoint = '/cookie'
        self.leaders_data = {}

    def refresh_cookie(self) -> object:
        # Refresh the session cookie from the API to maintain a valid session.
        try:
            # get cookies from the API
            conexao = requests.get(self.base_url+self.cookies_endpoint)
            return conexao.cookies

        except requests.RequestException as error:
            print(f"Um erro ocorreu: {error}")
            return None

    def get_countries(self, cookie: object) -> json:
        # Retrieve the list of countries from the API using the provided cookie for authentication.
        self.cookie = cookie
        try:

            country = requests.get(
                self.base_url+self.country_endpoint, cookies=self.cookie)

            return country.json()

        except requests.RequestException as error:
            print(f"Um erro ocorreu: {error}")
            return None

    def get_leaders(self, country: str, cookie) -> json:
        # Fetch the leaders for a specific country using the API, passing the country name and cookie for authentication.
        self.cookie = cookie
        self.country = country
        try:

            leaders = requests.get(
                self.base_url+self.leaders_endpoint, cookies=self.cookie, params={"country": self.country}
            )
            return leaders.json()

        except requests.RequestException as error:
            print(f"Um erro ocorreu: {error}")
            return None

    def get_first_paragraph(self, wikipedia_url: str) -> str:
        # Scrape the first paragraph of a leader's Wikipedia page using BeautifulSoup.
        self.wikipedia_url = wikipedia_url
        try:
            response = requests.get(self.wikipedia_url)
            response.raise_for_status()  # Isso vai lançar um erro se a requisição falhar
            soup = BeautifulSoup(response.content, "html.parser")
            for p in soup.find_all("p"):
                if p.find("b"):
                    first_paragraph = self.clean_paragraph(p.text)
                    if len(first_paragraph) > 50:
                        return first_paragraph

        except requests.RequestException as error:
            print(f"Um erro ocorreu: {error}")
        return None

    def clean_paragraph(self, text: str) -> str:
        # Clean the scraped paragraph text from Wikipedia to remove references, symbols, and formatting issues.

        # Remove references like [1], [2], etc.
        text = re.sub(r'\[\w+(\s\d+)?\]', '', text)
        text = re.sub(r'»', '', text)  # Remove this symbol if present.
        text = re.sub(r'—', '', text)  # Remove dashes.
        text = re.sub(r'…', '', text)  # Remove ellipses.
        text = re.sub(r' , ', ', ', text)  # Fix spacing around commas.
        text = re.sub(r'ⓘ', '', text)  # Remove this symbol if present.
        text = re.sub(r'"', '', text)  # Remove quotation marks.

        # Remove any characters enclosed in parentheses
        text = re.sub(r'\([^)]*\)', '', text)

        # Replace  spaces for one space
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def to_json_file(self, filepath: str) -> None:
        # Save the collected leaders' data to a JSON file.
        try:
            with open(filepath, 'w') as file:
                json.dump(self.leaders_data, file)

        except requests.RequestException as error:
            print(f"Um erro ocorreu: {error}")
            return None

    def get_everyone(self) -> dict:
        # Aggregate data for all leaders by refreshing the cookie, fetching countries, and then fetching leaders for each country.
        cookie = self.refresh_cookie()
        countries = self.get_countries(cookie)
        data = {}

        for country in countries:
            cookie = self.refresh_cookie()
            leaders = self.get_leaders(country, cookie)

            for leader in leaders:
                leader_id = leader.get("id")
                if not leader_id:
                    # Generate a unique ID if not provided. Fistname-Lastname-birth_date
                    last_name = leader.get('last_name') or 'Unknown'
                    birth_date = leader.get('birth_date', 'UnknownDate')
                    leader_id = f"{leader['first_name']}-{last_name}-{birth_date}".replace(
                        ' ', '_').lower()

                leader_data = {
                    # get all the information about the leader
                    'id': leader.get('id'),
                    'first_name': leader.get('first_name'),
                    'last_name': leader.get('last_name'),
                    'birth_date': leader.get('birth_date'),
                    'death_date': leader.get('death_date'),
                    'place_of_birth': leader.get('place_of_birth'),
                    'wikipedia_url': leader.get('wikipedia_url'),
                    'start_mandate': leader.get('start_mandate'),
                    'end_mandate': leader.get('end_mandate'),
                    # iniciate the function get_first_paragraph that going to return the text screped from wikipedia
                    'first_paragraph': self.get_first_paragraph(leader.get('wikipedia_url'))
                }

                self.leaders_data[leader_id] = leader_data

        return data

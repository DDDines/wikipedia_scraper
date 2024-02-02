import requests
import json
from bs4 import BeautifulSoup
import re


class WikipediaScraper:

    def __init__(self, base_url="https://country-leaders.onrender.com"):

        self.base_url = base_url
        self.country_endpoint = '/countries'
        self.leaders_endpoint = '/leaders'
        self.cookies_endpoint = '/cookie'
        self.leaders_data = {}

    def refresh_cookie(self) -> object:
        try:
            conexao = requests.get(self.base_url+self.cookies_endpoint)
            return conexao.cookies
            # try to get country from the API passing the cookies argument
        except requests.RequestException as error:
            print(f"Um erro ocorreu: {error}")
            return None

    def get_countries(self, cookie) -> json:
        self.cookie = cookie
        try:

            country = requests.get(
                self.base_url+self.country_endpoint, cookies=self.cookie)

            return country.json()

        except requests.RequestException as error:
            print(f"Um erro ocorreu: {error}")
            return None

    def get_leaders(self, country: str, cookie):
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

    def get_first_paragraph(self, wikipedia_url: str):
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

    def clean_paragraph(self, text):

        text = re.sub(r'\[[^\]]+\]', '', text).strip()

        # Remove references to Wikipedia footnotes, such as [1] or [note 1]
        text = re.sub(r'\[\w+(\s\d+)?\]', '', text).strip()

        text = re.sub(r'\s[»ⓘ]\s', ' ', text)

        text = re.sub(r' - ', " ", text)

        # Remove any characters enclosed in parentheses
        text = re.sub(r'\([^)]*\)', '', text)

        # Replace two spaces for one
        text = re.sub(r'  ', ' ', text)

        return text

    def to_json_file(self, filepath: str, data):
        try:
            with open(filepath, "w") as file:
                json.dump(data, file)

        except requests.RequestException as error:
            print(f"Um erro ocorreu: {error}")
            return None

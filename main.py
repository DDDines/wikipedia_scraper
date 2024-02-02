# import src.utils as utils
from src.scraper import WikipediaScraper


if __name__ == "__main__":
    """
    Main entry point of the script.yy

    """
    data = {}

    def get_url(leaders):
        return leaders.get("wikipedia_url")

    Scrapper = WikipediaScraper()
    cookie = Scrapper.refresh_cookie()
    countries = Scrapper.get_countries(cookie)

    for country in countries:
        cookie = Scrapper.refresh_cookie()
        leaders = Scrapper.get_leaders(country, cookie)

        for leader in leaders:
            # Usar o ID fornecido para a chave no dicionário de dados
            leader_id = leader.get("id")
            if not leader_id:
                # Se não houver um ID, criar um identificador único usando o nome, sobrenome e data de nascimento
                # Se o sobrenome for None, substituir por 'Unknown'
                last_name = leader.get('last_name') or 'Unknown'
                birth_date = leader.get('birth_date', 'UnknownDate')
                leader_id = f"{leader['first_name']}-{last_name}-{birth_date}".replace(
                    ' ', '_').lower()

            leader_data = {
                'id': leader.get('id'),
                'first_name': leader.get('first_name'),
                'last_name': leader.get('last_name'),
                'birth_date': leader.get('birth_date'),
                'death_date': leader.get('death_date'),
                'place_of_birth': leader.get('place_of_birth'),
                'wikipedia_url': leader.get('wikipedia_url'),
                'start_mandate': leader.get('start_mandate'),
                'end_mandate': leader.get('end_mandate'),
                'first_paragraph': Scrapper.get_first_paragraph(get_url(leader))
            }

            # Salvando os dados do líder usando o ID como chave
            data[leader_id] = leader_data

    Scrapper.to_json_file("data.json", data)

    print(data)

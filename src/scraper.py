import requests


def status():
    try:
        with requests.Session() as session:
            response = session.get(
                "https://country-leaders.onrender.com/status")
            return response.json()

    except requests.RequestException as e:
        print(f"Um erro ocorreu: {e}")

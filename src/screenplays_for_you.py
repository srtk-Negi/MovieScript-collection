import requests
from bs4 import BeautifulSoup


def get_movie_names_screenplays_for_you(URL: str) -> list[str]:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    page_html = requests.get(URL, headers=headers)
    doc = BeautifulSoup(page_html.text, "html.parser")

    movie_names = []
    movie_elements_list = doc.find("div", class_="two-thirds").find_all("p")

    del movie_elements_list[0]

    for element in movie_elements_list:
        name = element.find("a").string
        if name not in movie_names:
            movie_names.append(name)

    return movie_names

import requests
from bs4 import BeautifulSoup
import re


def get_movie_names_screenplays_for_you(URL: str) -> list[str]:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    page_html = requests.get(URL, headers=headers)
    doc = BeautifulSoup(page_html.text, "html.parser")

    movie_names = []
    re_pattern = re.compile("\(\d{4}\)")
    movie_elements_list = doc.find("div", class_="two-thirds").find_all("p")

    del movie_elements_list[0]

    for element in movie_elements_list:
        name = element.find("a").string
        name = re.sub(re_pattern, "", name).strip()

        if name.endswith(", The"):
            new_name = name.replace(", The", "")
            name = "The " + new_name

        if name not in movie_names:
            movie_names.append(name.strip())

    return movie_names

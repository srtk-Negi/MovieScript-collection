import requests
from bs4 import BeautifulSoup
import re


def get_movie_names_screenplays_for_you(URL: str) -> list[str]:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    page_html = requests.get(URL, headers=headers)
    doc = BeautifulSoup(page_html.text, "html.parser")

    movie_names = []
    base_link = URL[:-8]

    re_pattern = re.compile("\(\d{4}\)")
    movie_elements_list = doc.find("div", class_="two-thirds").find_all("p")

    del movie_elements_list[0]

    i = 0
    for element in movie_elements_list:
        i += 1
        name = element.find("a").string
        link = element.find("a").get("href")
        if link.startswith("http"):
            link = base_link + link[14:]
        else:
            link = base_link + link
        print(link)
        name = re.sub(re_pattern, "", name).strip()

        if name.endswith(", The"):
            new_name = name.replace(", The", "")
            name = "The " + new_name

        if name not in movie_names:
            movie_names.append(name.strip())
        if i == 2:
            break
    return movie_names

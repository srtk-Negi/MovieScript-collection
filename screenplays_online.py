from typing import List

import requests
from bs4 import BeautifulSoup

URL = "https://www.screenplays-online.de/"
MOVIE_NAMES = []


def get_movie_names(doc: BeautifulSoup) -> List[str]:
    movie_names_list = []
    table_rows = doc.find("table", class_="screenplay-listing").find_all("tr")
    del table_rows[0]

    for row in table_rows:
        movies_in_row = row.find_all("td")
        name = movies_in_row[1].find("a").string
        if name is not None:
            movie_names_list.append(name)

        name = movies_in_row[6].find("a").string
        if name is not None:
            movie_names_list.append(name)

    return movie_names_list


def main():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    page_html = requests.get(URL, headers=headers)
    doc = BeautifulSoup(page_html.text, "html.parser")

    MOVIE_NAMES = get_movie_names(doc)
    print(MOVIE_NAMES)


if __name__ == "__main__":
    main()

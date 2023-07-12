import requests
from bs4 import BeautifulSoup


def get_movie_names_screenplays_online(URL: str) -> list[str]:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    page_html = requests.get(URL, headers=headers)
    doc = BeautifulSoup(page_html.text, "html.parser")
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

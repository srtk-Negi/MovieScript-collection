import requests
from bs4 import BeautifulSoup
import re


def get_raw_screenplays_online(URL: str) -> None:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    home_page_html = requests.get(URL, headers=headers)
    home_page_data = BeautifulSoup(home_page_html.text, "html.parser")
    table_rows = home_page_data.find("table", class_="screenplay-listing").find_all("tr")
    del table_rows[0]

    i = 0
    for row in table_rows:
        if i == 20:
            break
        i += 1
        movie_1, date_1, movie_2, date_2 = get_movie_names_and_dates(row)
        print(f"{movie_1}|{movie_2}")


def get_movie_names_and_dates(row: BeautifulSoup) -> tuple:
    re_year = re.compile("\(\d{4}\)")
    movies_in_row = row.find_all("td")

    movie_1 = movies_in_row[1].find("a").string
    movie_2 = movies_in_row[6].find("a").string

    try:
        date_1 = re.findall(re_year, movie_1)[0][1:-1]
    except IndexError:
        date_1 = None

    try:
        date_2 = re.findall(re_year, movie_2)[0][1:-1]
    except IndexError:
        date_2 = None

    movie_1 = re.sub(re_year, "", movie_1).strip()
    movie_2 = re.sub(re_year, "", movie_2).strip()

    if movie_1.endswith(", The") or movie_1.endswith(", A") or movie_1.endswith(", An"):
        movie_1 = switch_article(movie_1.split(" ")[-1], movie_1)

    if movie_2.endswith(", The") or movie_2.endswith(", A") or movie_2.endswith(", An"):
        movie_2 = switch_article(movie_2.split(" ")[-1], movie_2)

    return movie_1, date_1, movie_2, date_2


def switch_article(article: str, movie_name: str) -> str:
    new_name = movie_name.replace(f", {article}", "")
    movie_name = f"{article} " + new_name

    return movie_name
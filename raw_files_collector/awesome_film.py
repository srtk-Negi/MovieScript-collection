import re

import requests
from bs4 import BeautifulSoup
from movie import Movie
from helper_functions import switch_article, get_file_type

# Match any string enclosed within parentheses
SCRIPT_TYPE_MATCH = re.compile(r"\([^)]*\)", re.DOTALL)
# Match two or more consecutive white spaces
EXTRA_SPACES_MATCH = re.compile(r"\s{2,}", re.DOTALL)

RE_TRANSCRIPT = re.compile(r"transcript", re.IGNORECASE)
RE_SCRIPT = re.compile(r"script", re.IGNORECASE)


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}


def get_movies_awesome_film(URL_AWESOME_FILM: str) -> list[Movie]:
    """Gets the movie data and returns a list of Movie objects

    Args:
        URL_AWESOME_FILM (str): The URL of the website to scrape

    Returns:
        list[Movie]: A list of Movie objects
    """
    movies = []
    try:
        content = requests.get(URL_AWESOME_FILM, headers=headers)
        soup = BeautifulSoup(content.text, "html.parser")
    except Exception as e:
        print(f"URL for Awesome Film did not work.\n{e}")

    columns = soup.find_all("td", valign="top", align="center")
    table_rows = []

    for column in columns:
        table_rows.extend(column.find_all("tr"))
    del table_rows[-2:]

    for row in table_rows:
        movie_title = row.find("a").text
        movie_link = URL_AWESOME_FILM + row.find("a").get("href")

        movie_title = movie_title.replace("\n", "").strip()
        if ":" in movie_title:
            movie_title = movie_title.replace(":", ": ")

        if (
            movie_title.endswith(", The")
            or movie_title.endswith(", A")
            or movie_title.endswith(", An")
        ):
            movie_title = switch_article(movie_title.split(" ")[-1], movie_title)

        if re.search(SCRIPT_TYPE_MATCH, movie_title):
            movie_title = re.sub(SCRIPT_TYPE_MATCH, "", movie_title).strip()

        if re.search(EXTRA_SPACES_MATCH, movie_title):
            movie_title = re.sub(EXTRA_SPACES_MATCH, " ", movie_title)

        if movie_title.endswith("-"):
            movie_title = movie_title[:-1].strip()

        movie_title = re.sub(RE_TRANSCRIPT, "", movie_title).strip()
        movie_title = re.sub(RE_SCRIPT, "", movie_title).strip()

        file_type = get_file_type(movie_link)

        movies.append(
            Movie(title=movie_title, script_url=movie_link, file_type=file_type)
        )

    print(f"Awesome Film: {len(movies)} movies found")
    return movies

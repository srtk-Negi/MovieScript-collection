"""Script to collect the rawfiles (html of the movie pages) from the 'Screenplays Online' endpoint"""

import requests
from bs4 import BeautifulSoup
import re

from .helper_functions import switch_article, get_file_type, get_name_to_compare
from .movie import Movie

re_year = re.compile(r"\(\d{4}\)")


def get_movies_screenplays_online(URL: str) -> list[Movie]:
    """Function to get the name of the movie, link to the movie page and rawfile (html of the movie page)

    Args:
        URL (str): URL of the home page of 'Screenplays Online' website

    Returns:
        None
    """
    movies = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    try:
        home_page_html = requests.get(URL, headers=headers)
        home_page_data = BeautifulSoup(home_page_html.text, "html.parser")
    except:
        with open("error_log.txt", "a", encoding="utf-8") as outfile:
            outfile.write("The URL did not work for 'Screenplays Online'\n")
        return

    table_rows = home_page_data.find("table", class_="screenplay-listing").find_all(
        "tr"
    )
    del table_rows[0]

    title_link_map = {}
    for row in table_rows:
        movie_1, movie_2 = get_movie_titles(row)
        url_1, url_2 = get_links_to_movie_pages(row, URL)

        if movie_1:
            title_link_map[movie_1] = url_1
        if movie_2:
            title_link_map[movie_2] = url_2

    for movie_title, movie_url in title_link_map.items():
        movie_title = re.sub(re_year, "", movie_title).strip()

        if (
            movie_title.endswith(", The")
            or movie_title.endswith(", A")
            or movie_title.endswith(", An")
        ):
            movie_title = switch_article(movie_title.split(" ")[-1], movie_title)

        filetype = get_file_type(movie_url)
        name_to_compare = get_name_to_compare(movie_title)

        movies.append(
            Movie(
                title=movie_title,
                script_url=movie_url,
                file_type=filetype,
                name_to_compare=name_to_compare,
            )
        )

    print(f"Screenplays Online: {len(movies)} movies found.")
    return movies


def get_movie_titles(row: BeautifulSoup) -> tuple:
    """Gets the names of the movies from the table row

    Args:
        row (BeautifulSoup): A beautifulsoup object that is a table row

    Returns:
        tuple: movie_1, movie_2
    """
    movies_in_row = row.find_all("td")

    movie_1 = movies_in_row[1].find("a").string
    movie_2 = movies_in_row[6].find("a").string

    return movie_1, movie_2


def get_links_to_movie_pages(row: BeautifulSoup, URL: str) -> tuple:
    """Gets the links to the movie pages

    Args:
        row (BeautifulSoup): A beautifulsoup object that is a table row
        URL (str): URL of the home page of 'Screenplays Online' website

    Returns:
        tuple: link_1, link_2
    """
    movies_in_row = row.find_all("td")

    link_1 = URL + movies_in_row[1].find("a").get("href")
    link_2 = URL + movies_in_row[6].find("a").get("href")

    return link_1, link_2

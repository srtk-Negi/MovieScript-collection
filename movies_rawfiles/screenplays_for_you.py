"""Script to collect the rawfiles (html of the movie pages) from the 'Screenplays For You' endpoint"""

import requests
from bs4 import BeautifulSoup
import re
from .movie import Movie
from .helper_functions import switch_article, get_file_type

re_year = re.compile(r"\(\d{4}\)")
re_transcript = re.compile(r"transcript")
re_writers = re.compile(r"(B|b)y\s((\w|\s|,|&)+)")
re_script_date = re.compile(
    r"\s((january|february|march|april|may|june|july|august|september|october|november|december)\s{0,1}\d{0,2},{0,1}\s\d{4})",
    re.IGNORECASE,
)


def get_movies_screenplays_for_you(URL: str) -> list[Movie]:
    """Gets the movies from the 'Screenplays For You' endpoint

    Args:
        URL (str): The URL of the 'Screenplays For You' endpoint

    Returns:
        list[Movie]: A list of Movie objects
    """
    movies = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    try:
        page_data = requests.get(URL, headers=headers)
        home_page_html = BeautifulSoup(page_data.text, "html.parser")
    except:
        with open("error_log.txt", "a", encoding="utf-8") as outfile:
            outfile.write("The URL did not work for 'Scripts For You'\n")
        return

    movie_elements_p = home_page_html.find("div", class_="two-thirds").find_all("p")
    del movie_elements_p[0]

    for element in movie_elements_p:
        a_tag = element.find("a")
        movie_title, movie_year = get_movie_title_and_year(a_tag)
        script_url = get_link_to_movie_page(a_tag, URL)

        script_date_match = re_script_date.search(element.text)
        if script_date_match:
            script_date = script_date_match.group(1).strip()
        else:
            script_date = None

        writers_match = re_writers.search(element.text)
        writers = writers_match.group(2) if writers_match else None

        filetype = get_file_type(script_url)

        movies.append(
            Movie(
                title=movie_title,
                script_url=script_url,
                file_type=filetype,
                movie_year=movie_year,
                script_date=script_date,
                writers=writers,
            )
        )

    print(f"Scripts For You: {len(movies)} movies found.")
    return movies


def get_link_to_movie_page(a_tag: BeautifulSoup, URL: str) -> str:
    """Gets the link to the movie page

    Args:
        a_tag (BeautifulSoup): A beautifulsoup object that is an anchor tag containg the movie name and the link
        URL (str): URL of the scripts page (ALL) of 'Scripts For You' website

    Returns:
        str: link to the movie page
    """
    base_link = URL[:14]
    link_to_movie_page = a_tag.get("href")

    if link_to_movie_page.lower().endswith(".pdf") or link_to_movie_page.startswith(
        "http"
    ):
        return link_to_movie_page

    else:
        link_to_movie_page = base_link + link_to_movie_page

    return link_to_movie_page


def get_movie_title_and_year(a_tag: BeautifulSoup) -> tuple:
    """Gets the movie title and the year of release of the movie

    Args:
        a_tag (BeautifulSoup): A beautifulsoup object that is an anchor tag containg the movie name and the link

    Returns:
        tuple: movie_title, year
    """

    movie_title = a_tag.string

    try:
        movie_year = re.findall(re_year, movie_title)[0][1:-1]
    except IndexError:
        movie_year = None

    movie_title = re.sub(re_year, "", movie_title).strip()
    movie_title = re.sub(re_transcript, "", movie_title).strip()

    if (
        movie_title.endswith(", The")
        or movie_title.endswith(", A")
        or movie_title.endswith(", An")
    ):
        movie_title = switch_article(movie_title.split(" ")[-1], movie_title)

    return movie_title, movie_year

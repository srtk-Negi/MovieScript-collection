import re
import requests
from bs4 import BeautifulSoup
from movie import Movie
from helper_functions import get_file_type

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}

re_writer = re.compile(r"(B|b)y (.+?)(\d+|\?\?)")
re_year = re.compile(r"\s{3}\b(\d{4})\b")
re_script_date = [
    re.compile(
        r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},\s+\d{4}\b"
    ),
    re.compile(
        r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\b"
    ),
]

movie_script_base_url = "https://www.dailyscript.com/"


def get_movie_list(URL_DAILY_SCRIPT: str) -> list[Movie]:
    """Fetch movie titles and script links, curate unique IDs, and return movie info."""
    movies = []

    url_text = requests.get(URL_DAILY_SCRIPT).text
    soup = BeautifulSoup(url_text, "html.parser")

    page_items = soup.ul.find_all("p")
    for page_item in page_items:
        movie_title = page_item.find("a").string

        writers_match = re_writer.search(page_item.text)
        movie_year_match = re_year.search(page_item.text)

        for script_date_pattern in re_script_date:
            script_date_match = script_date_pattern.search(
                page_item.text, re.IGNORECASE
            )
            if script_date_match:
                script_date = script_date_match.group(0).strip()
                break
            else:
                script_date = None

        writers = writers_match.group(2).strip() if writers_match else None
        movie_year = movie_year_match.group(1).strip() if movie_year_match else None
        script_url = f"{movie_script_base_url}{page_item.find_all('a')[0].get('href')}"
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

    return movies


def get_movies_daily_script(URL_DAILY_SCRIPT: str) -> list[Movie]:
    """Retreive html structure from script links and write raw html to files."""
    try:
        list_am = get_movie_list(URL_DAILY_SCRIPT)
    except:
        with open("error_log.txt", "a", encoding="utf-8") as outfile:
            outfile.write(
                f"The URL {URL_DAILY_SCRIPT} did not work for 'Daily Script'\n"
            )
        return

    url_nz = URL_DAILY_SCRIPT.replace(".html", "_n-z.html")
    try:
        list_nz = get_movie_list(url_nz)
    except:
        with open("error_log.txt", "a", encoding="utf-8") as outfile:
            outfile.write(
                f"The URL {URL_DAILY_SCRIPT} did not work for 'Daily Script'\n"
            )
        return

    list_am.extend(list_nz)

    print(f"Daily Script: {len(list_am)} movies found")

    return list_am

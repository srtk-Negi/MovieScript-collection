import re  # noqa: D100

import requests
from bs4 import BeautifulSoup

SCRIPT_TYPE_MATCH = re.compile(r"\([^)]*\)", re.DOTALL)
EXTRA_SPACES_MATCH = re.compile(r"\s{2,}", re.DOTALL)


def get_movie_names_and_links_awesome_film(URL_AWESOME_FILM: str) -> dict:
    """Fetch script titles and links and append to a dictionary."""
    awesome_film_names_and_links = {}
    content = requests.get(URL_AWESOME_FILM).text
    soup = BeautifulSoup(content, "html.parser")
    tables = soup.body.find_all("table")[15:18]
    for table in tables:
        tds = table.find_all("td", class_="tbl")
        for td in tds:
            try:
                movie_link = "http://www.awesomefilm.com/" + td.a["href"]
            except Exception:
                movie_link = "Not Found"
            movie_title = td.text.replace("\n", "").strip()
            if ":" in movie_title:
                movie_title = movie_title.replace(":", ": ")
            if movie_title.endswith(", The"):
                movie_title = movie_title.replace(", The", "")
                movie_title = "The " + movie_title
            if movie_title.endswith(", A"):
                movie_title = movie_title.replace(", A", "")
                movie_title = "A " + movie_title
            if re.search(SCRIPT_TYPE_MATCH, movie_title):
                movie_title = re.sub(SCRIPT_TYPE_MATCH, "", movie_title).strip()
            if re.search(EXTRA_SPACES_MATCH, movie_title):
                movie_title = re.sub(EXTRA_SPACES_MATCH, " ", movie_title)
            if movie_title.endswith("-"):
                movie_title = movie_title[:-1].strip()
            if movie_title != "email" and movie_title != "":
                awesome_film_names_and_links[movie_title] = movie_link
    return awesome_film_names_and_links


def get_raw_files_awesome_film(AWESOME_FILM_URL: str) -> None:
    """Retrieve html structure from script links and write raw html to files."""
    awesome_film_names_and_links = get_movie_names_and_links_awesome_film(
        AWESOME_FILM_URL
    )
    for movie_title in awesome_film_names_and_links:
        script_url = awesome_film_names_and_links[movie_title]
        soup = ""
        if ".pdf" in script_url or ".doc" in script_url:
            soup = f"{movie_title}: {script_url}"
            with open("rawfiles/00_other_file_types", "a", encoding="utf-8") as f:
                soup = soup.strip()
                f.write(f"{soup}\n")
        else:
            content = requests.get(script_url).content
            soup = BeautifulSoup(content, "html.parser")
            file_name = "_".join(movie_title.strip().split())
            with open(f"rawfiles/{file_name}", "a", encoding="utf-8") as f:
                f.write(str(soup).strip())

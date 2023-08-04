import requests
from bs4 import BeautifulSoup
from .movie import Movie
from .helper_functions import get_file_type


def get_movies_script_savant(URL_SCRIPT_SAVANT: str) -> list[Movie]:
    """Rewrites movie names and links from script savant to a file."""
    movies = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    try:
        content = requests.get(URL_SCRIPT_SAVANT, headers=headers)
        soup = BeautifulSoup(content.text, "html.parser")
    except:
        with open("error_log.txt", "a", encoding="utf-8") as outfile:
            outfile.write(f"Provided URL did not work for script savant\n")
        return

    script_block = soup.find_all("td", align="left")[2]
    script_groupings = script_block.find_all("a")
    del script_groupings[0]

    for grouping in script_groupings:
        script_url = "https://thescriptsavant.com/" + grouping["href"]
        movie_title = grouping.text

        if script_url.endswith("#TOP-section"):
            continue

        if movie_title.endswith("Script"):
            movie_title = movie_title.replace(" Script", "")

        movie_title = movie_title.replace("_", " ")

        filetype = get_file_type(script_url)

        movies.append(
            Movie(title=movie_title, script_url=script_url, file_type=filetype)
        )

    print(f"Script Savant: {len(movies)} movies found")
    return movies

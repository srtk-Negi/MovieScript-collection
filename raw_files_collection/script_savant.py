import requests
from bs4 import BeautifulSoup


def get_movie_names_and_links_script_savant(URL_SCRIPT_SAVANT: str) -> None:
    """Rwrites movie names and links from script savant to a file."""
    content = requests.get(URL_SCRIPT_SAVANT).text
    soup = BeautifulSoup(content, "html.parser")
    script_block = soup.find_all("td", align="left")[2]
    script_groupings = script_block.find_all("a")
    with open("rawfiles/00_other_file_types", "a", encoding="utf-8") as f:
        for grouping in script_groupings:
            movie_link = "https://thescriptsavant.com/" + grouping["href"]
            movie_title = grouping.text
            if "#TOP-section" not in movie_link:
                f.write(f"{movie_title}: {movie_link}\n")
